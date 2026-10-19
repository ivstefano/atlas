#!/usr/bin/env python3
"""Desktop notification hook for Claude Code (Stop / Notification / PermissionRequest).

Usage (from ~/.claude/settings.json):
    python3 notify_hook.py Stop|Notification|PermissionRequest   < hook JSON on stdin

Rules:
  - headless runs (claude -p, state flush, autopilot) never notify
  - Stop: only if the turn took >= STOP_MIN_SECONDS, silent banner
  - Notification (needs input) / PermissionRequest: banner + Basso
  - during a calendar call: Stop says nothing; input/permission banner without sound
  - title = task name (engagements/<name> -> <name>, else "operations")
  - -group <session_id>: each tab replaces its own previous notification
Meeting state comes from ~/.cache/atlas/meetings_now.json (written by dnd_sync.py,
launchd every 5 min). No network calls here. Fails silent, always exits 0.
"""
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

STOP_MIN_SECONDS = float(os.environ.get("CLAUDE_NOTIFY_STOP_MIN_SECONDS", "60"))
ALERT_SOUND = "Basso"
TN = "/opt/homebrew/bin/terminal-notifier"
MEETINGS_CACHE = Path(os.environ.get("NOTIFY_HOOK_MEETINGS") or Path.home() / ".cache" / "atlas" / "meetings_now.json")
CACHE_MAX_AGE_H = 6
TAIL_BYTES = 4 * 1024 * 1024

HEADLESS_ENV = ("ATLAS_STATE_FLUSH", "ATLAS_AUTOPILOT_CHILD", "ATLAS_MONDAY_THREADS")
# Injected "user" entries that are not Ivo typing.
NOT_REAL_PREFIXES = ("<task-notification>", "<local-command-stdout>", "<local-command-caveat>",
                     "<system-reminder>", "Caveat:")


def headless():
    if any(os.environ.get(k) == "1" for k in HEADLESS_ENV):
        return True
    if os.environ.get("CLAUDE_CODE_SESSION_ATTENDED") == "0":
        return True
    ep = os.environ.get("CLAUDE_CODE_ENTRYPOINT", "")
    return ep.startswith("sdk")  # claude -p reports "sdk-cli"


def task_name(cwd):
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from state_common import resolve_task
        return resolve_task(cwd)
    except Exception:
        return "operations"


def parse_ts(s):
    try:
        t = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)
    except Exception:
        return None


def is_real_user(d):
    if d.get("type") != "user" or d.get("isMeta") or d.get("isSidechain"):
        return False
    c = (d.get("message") or {}).get("content")
    if isinstance(c, str):
        text = c
    elif isinstance(c, list):
        if any(isinstance(x, dict) and x.get("type") == "tool_result" for x in c):
            return False
        text = " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
        if not text and any(isinstance(x, dict) and x.get("type") == "image" for x in c):
            return True
    else:
        return False
    text = text.lstrip()
    return bool(text) and not text.startswith(NOT_REAL_PREFIXES)


def turn_seconds(transcript_path, now):
    """Seconds since the last real user message. None if unknown."""
    try:
        with open(transcript_path, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - TAIL_BYTES))
            chunk = f.read()
    except Exception:
        return None
    lines = chunk.split(b"\n")
    if size > TAIL_BYTES:
        lines = lines[1:]  # first line may be partial
    for raw in reversed(lines):
        if b'"user"' not in raw:
            continue
        try:
            d = json.loads(raw)
        except Exception:
            continue
        if is_real_user(d):
            t = parse_ts(d.get("timestamp") or "")
            return (now - t).total_seconds() if t else None
    # No user prompt in the last 4 MB: a very long turn.
    return float("inf") if size > TAIL_BYTES else None


def in_meeting(now):
    try:
        c = json.loads(MEETINGS_CACHE.read_text())
        fetched = parse_ts(c.get("fetched_at") or "")
        if not fetched or (now - fetched).total_seconds() > CACHE_MAX_AGE_H * 3600:
            return False
        for m in c.get("meetings") or []:
            s, e = parse_ts(m.get("start") or ""), parse_ts(m.get("end") or "")
            if s and e and s <= now < e:
                return True
    except Exception:
        pass
    return False


def decide(event, data, now):
    """Return (message, sound) or None to stay quiet. sound None = silent banner."""
    meeting = in_meeting(now)
    if event == "Stop":
        if meeting:
            return None
        secs = turn_seconds(data.get("transcript_path") or "", now)
        if secs is None or secs < STOP_MIN_SECONDS:
            return None
        return "finished", None
    if event == "PermissionRequest":
        return "needs permission", (None if meeting else ALERT_SOUND)
    if event == "Notification":
        ntype = data.get("notification_type") or ""
        msg = (data.get("message") or "").lower()
        # Permission prompts also arrive as PermissionRequest; don't double up.
        if ntype == "permission_prompt" or (not ntype and "permission" in msg):
            return None
        if ntype == "auth_success":
            return None
        return "needs input", (None if meeting else ALERT_SOUND)
    return None


def main():
    if headless():
        return
    event = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        data = {}
    now = dt.datetime.now(dt.timezone.utc)
    out = decide(event, data, now)
    if not out:
        return
    message, sound = out
    cmd = [TN, "-title", task_name(data.get("cwd") or os.getcwd()), "-message", message]
    if data.get("session_id"):
        cmd += ["-group", data["session_id"]]
    if sound:
        cmd += ["-sound", sound]
    if os.environ.get("NOTIFY_HOOK_DRY") == "1":
        print(json.dumps(cmd))
        return
    subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, start_new_session=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
