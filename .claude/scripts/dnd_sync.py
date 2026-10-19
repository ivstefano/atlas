#!/usr/bin/env python3
"""Sync Slack DND to client meetings on Google Calendar.

Run every ~5 min from launchd. Looks at events overlapping now; if any is a
client meeting (see dnd_rules.py), snoozes Slack until that event ends.
Slack snoozing is OFF since 2026-10-19 (SNOOZE_SLACK): Ivo needs DMs mid-call.
The job still writes MEETINGS_CACHE (upcoming calls) for notify_hook.py.

Only ever clears a snooze this script set itself (state file), so a manual
/dnd from the Slack client is never stomped.

Usage:
    dnd_sync.py            # act
    dnd_sync.py --dry-run  # print decision only
"""
import datetime as dt
import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dnd_rules import classify, is_meeting  # noqa: E402
import slack_dnd  # noqa: E402

STATE = pathlib.Path.home() / ".cache" / "atlas" / "dnd_sync.json"
LOG = pathlib.Path.home() / ".cache" / "atlas" / "dnd_sync.log"
MEETINGS_CACHE = pathlib.Path.home() / ".cache" / "atlas" / "meetings_now.json"
SNOOZE_SLACK = False  # 2026-10-19: keep Slack live during calls
LOOKAHEAD_MIN = 0   # no early buffer: silence at start, not before
MIN_SNOOZE_MIN = 1


def log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"{dt.datetime.now().isoformat(timespec='seconds')} {msg}"
    with LOG.open("a") as f:
        f.write(line + "\n")
    print(line)


def read_state():
    try:
        return json.loads(STATE.read_text())
    except Exception:
        return {}


def write_state(d):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(d))


def parse_ts(s):
    if not s:
        return None
    if len(s) == 10:  # all-day date
        return None
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


GCALCLI_OAUTH = (
    pathlib.Path.home()
    / "Library" / "Application Support" / "gcalcli" / "oauth"
)
GCALCLI_PY = (
    pathlib.Path.home()
    / ".local" / "share" / "uv" / "tools" / "gcalcli" / "bin" / "python"
)
CALENDAR_ID = "ivo@iris.ai"   # only Ivo's own calendar, not colleagues' shared ones


def fetch_events(hours=6):
    """Query the Calendar API directly, reusing gcalcli's cached OAuth
    credentials (it stores a pickled google.oauth2 Credentials with a refresh
    token, so this keeps working without re-auth).

    gcalcli's own venv has the google-api libs, so we shell out to its
    interpreter and get JSON back.
    """
    import subprocess

    now = dt.datetime.now(dt.timezone.utc)
    end = now + dt.timedelta(hours=hours)
    code = f"""
import pickle, json
from googleapiclient.discovery import build
creds = pickle.load(open({str(GCALCLI_OAUTH)!r}, "rb"))
svc = build("calendar", "v3", credentials=creds, cache_discovery=False)
res = svc.events().list(
    calendarId={CALENDAR_ID!r},
    timeMin={now.isoformat()!r},
    timeMax={end.isoformat()!r},
    singleEvents=True,
    orderBy="startTime",
).execute()
print(json.dumps(res.get("items", [])))
"""
    out = subprocess.run(
        [str(GCALCLI_PY), "-c", code],
        capture_output=True, text=True, check=True, timeout=60,
    ).stdout
    return json.loads(out)


def main():
    dry = "--dry-run" in sys.argv
    now = dt.datetime.now(dt.timezone.utc)

    try:
        events = fetch_events()
    except FileNotFoundError:
        log("ERROR gcalcli not installed")
        return 1
    except Exception as e:
        log(f"ERROR fetching calendar: {e}")
        return 1

    meetings = []
    for e in events:
        if is_meeting(e):
            meetings.append({"start": e["start"]["dateTime"], "end": (e.get("end") or {}).get("dateTime"),
                             "summary": e.get("summary"), "client": classify(e)[0]})
    if not dry:
        MEETINGS_CACHE.parent.mkdir(parents=True, exist_ok=True)
        tmp = MEETINGS_CACHE.with_suffix(".tmp")
        tmp.write_text(json.dumps({"fetched_at": now.isoformat(), "meetings": meetings}))
        tmp.replace(MEETINGS_CACHE)

    active = None
    for e in events:
        start = parse_ts((e.get("start") or {}).get("dateTime"))
        endt = parse_ts((e.get("end") or {}).get("dateTime"))
        if not start or not endt:
            continue
        if start - dt.timedelta(minutes=LOOKAHEAD_MIN) <= now < endt:
            is_client, why = classify(e)
            if is_client:
                active = (e, endt, why)
                break

    state = read_state()

    if active and not SNOOZE_SLACK:
        log(f"client meeting {active[0].get('summary')!r}, Slack snooze disabled")
        active = None

    if active:
        e, endt, why = active
        mins = max(MIN_SNOOZE_MIN, int((endt - now).total_seconds() // 60) + 1)
        title = e.get("summary")
        if state.get("event") == title and state.get("until") == endt.isoformat():
            log(f"already snoozed for {title!r} ({mins}m left)")
            return 0
        log(f"SNOOZE {mins}m for {title!r} [{why}]" + (" (dry-run)" if dry else ""))
        if not dry:
            res = slack_dnd.call("dnd.setSnooze", num_minutes=mins)
            if not res.get("ok"):
                log(f"ERROR setSnooze: {res}")
                return 1
            write_state({"event": title, "until": endt.isoformat()})
        return 0

    # No client meeting now. Clear only if WE set it.
    if state.get("event"):
        log(f"clearing snooze set for {state['event']!r}" + (" (dry-run)" if dry else ""))
        if not dry:
            res = slack_dnd.call("dnd.endSnooze")
            if not res.get("ok") and res.get("error") != "snooze_not_active":
                log(f"ERROR endSnooze: {res}")
            write_state({})
    else:
        log("no client meeting, nothing set by us")
    return 0


if __name__ == "__main__":
    sys.exit(main())
