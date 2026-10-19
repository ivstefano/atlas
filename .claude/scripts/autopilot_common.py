#!/usr/bin/env python3
"""Shared read-only plumbing for the atlas autopilot scripts (weekly_rollup, monday_threads).

Slack (read-only methods only here), Google Calendar/Gmail read tokens, Tactiq list, Cognion copies,
engagement aliases + matching, Bedrock call with cost, Ivo's voice block, macOS notify.
Posting to Slack / creating Gmail drafts lives ONLY in approval_executors.py, run on Ivo's click.
"""
import argparse
import datetime as dt
import glob
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HOME = Path.home()
ATLAS = HOME / "Documents" / "atlas"
ENG = HOME / "Documents" / "engagements"
COGNION = HOME / "Documents" / "Cognion"
TWIN = HOME / "Documents" / "digital-twin-ivo" / "work"
LOG_DIR = ATLAS / "_autopilot" / "logs"
LOG = LOG_DIR / "autopilot.log"

CHANNEL = "C0B8GPS4DCN"            # #active-engagements (public)
IVO_SLACK = "U09QHUPJZ7W"
IVO_EMAIL = "ivo@iris.ai"
SLACK_CRED = HOME / ".config" / "slack-mcp"
GOOGLE_CRED = HOME / ".config" / "workspace-mcp" / "creds" / "ivo@iris.ai.json"
CAL_SCOPE = "https://www.googleapis.com/auth/calendar.readonly"

MODEL = os.environ.get("AUTOPILOT_MODEL", "eu.anthropic.claude-sonnet-5-5")
PRICE_IN, PRICE_OUT = 2.2e-6, 11e-6     # USD/token, Sonnet 5.5 ($2/$10 per MTok) + 10% EU-profile headroom
EFFORT = os.environ.get("AUTOPILOT_EFFORT", "medium")
MAX_OUT = 7000
MAX_COST_USD = 0.50
TARGET_COST_USD = 0.35                  # trim input until the estimate is under this

HISTORY_DAYS = 84                       # 12 weeks of channel history for format + staleness
STALE_DAYS = 14
ACTIVE_DAYS = 60                        # engagement counts as live if anything moved in this window
CLOSED = {"closed-lost", "closed-paused", "closed-won", "closed"}


# ----------------------------------------------------------------------------- utils
def tcc_guard(job):
    """launchd jobs cannot read ~/Documents (macOS TCC). Every ai.iris.atlas.* job runs through the
    AtlasAutopilot launcher (autopilot/launcher.c), which holds the one Documents grant; this guard only
    fires if a job is started some other way. Fail loudly with a notification instead of silently."""
    try:
        os.listdir(ENG)
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        (LOG_DIR / ".tcc_ok").write_text(dt.datetime.now().isoformat())
    except PermissionError:
        py = os.path.realpath(sys.executable)
        msg = (f"{job}: no access to ~/Documents ({py}). Run it via the AtlasAutopilot launcher and turn on: "
               "System Settings > Privacy & Security > Files and Folders > AtlasAutopilot > Documents Folder")
        Path.home().joinpath(".cache", "atlas").mkdir(parents=True, exist_ok=True)
        with open(Path.home() / ".cache" / "atlas" / "autopilot_tcc.log", "a") as f:
            f.write(f"{dt.datetime.now().isoformat()}  {msg}\n")
        subprocess.run(["/usr/bin/osascript", "-e", f'display notification "{msg}" with title "Atlas autopilot blocked"'])
        sys.exit(3)


def set_log(name):
    global LOG
    LOG = LOG_DIR / f"{name}.log"


def log(msg):
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = f"{dt.datetime.now().isoformat(timespec='seconds')}  {msg}"
    with LOG.open("a") as f:
        f.write(line + "\n")
    print(line, flush=True)


_MON = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
                                     "Nov", "Dec"], 1)}
_WD = r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*"


def fix_weekdays(s, ref=None):
    """Models get weekdays wrong. Recompute every 'Wed 16 Oct' / 'Wednesday 16 October' from the date."""
    ref = ref or dt.date.today()

    def fix(m):
        day, mon = int(m.group(2)), _MON.get(m.group(3)[:3].title())
        if not mon:
            return m.group(0)
        yr = ref.year + (1 if mon < ref.month - 6 else 0) - (1 if mon > ref.month + 6 else 0)
        try:
            wd = dt.date(yr, mon, day).strftime("%a")
        except ValueError:
            return m.group(0)
        return f"{wd} {m.group(2)} {m.group(3)}"
    return re.sub(r"\b(" + _WD + r"),? (\d{1,2}) (Jan\w*|Feb\w*|Mar\w*|Apr\w*|May|Jun\w*|Jul\w*|Aug\w*|Sep\w*|Oct\w*|Nov\w*|Dec\w*)\b",
                  fix, s)


def clean(s):
    """House style: no em/en dashes, plain arrows, correct weekdays."""
    s = fix_weekdays(s)
    s = s.replace(" \u2014 ", ", ").replace("\u2014", ", ").replace(" \u2013 ", " - ").replace("\u2013", "-")
    return s.replace("\u2192", "->").replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'")


def d(s):
    return dt.date.fromisoformat(s[:10])


# ----------------------------------------------------------------------------- slack
class Slack:
    def __init__(self):
        self.xc = (SLACK_CRED / "xoxc").read_text().strip()
        self.xd = (SLACK_CRED / "xoxd").read_text().strip()
        self.last = 0.0
        self.users = {}

    def api(self, method, **params):
        for attempt in range(6):
            wait = 1.3 - (time.time() - self.last)
            if wait > 0:
                time.sleep(wait)
            self.last = time.time()
            req = urllib.request.Request(
                "https://slack.com/api/" + method, data=urllib.parse.urlencode(params).encode(),
                headers={"Authorization": "Bearer " + self.xc, "Cookie": "d=" + self.xd,
                         "Content-Type": "application/x-www-form-urlencoded"})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = json.loads(r.read())
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    time.sleep(int(e.headers.get("Retry-After") or 20) + 1)
                    continue
                if e.code >= 500:
                    time.sleep(2 ** attempt)
                    continue
                raise
            if data.get("ok"):
                return data
            if data.get("error") == "ratelimited":
                time.sleep(20)
                continue
            raise RuntimeError(f"slack {method}: {data.get('error')}")
        raise RuntimeError(f"slack {method}: retries exhausted")

    def name(self, uid):
        if uid not in self.users:
            try:
                u = self.api("users.info", user=uid)["user"]
                self.users[uid] = u.get("real_name") or u.get("name") or uid
            except Exception:
                self.users[uid] = uid
        return self.users[uid]

    def text(self, m):
        t = m.get("text") or ""
        t = re.sub(r"<@(U[A-Z0-9]+)>", lambda x: "@" + self.name(x.group(1)), t)
        t = re.sub(r"<(https?://[^|>]+)\|[^>]*>", r"\1", t)
        t = re.sub(r"<(https?://[^>]+)>", r"\1", t)
        t = t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        return t.strip()

    def tops(self, oldest_ts):
        """Top-level messages only (no replies) since oldest_ts, newest first."""
        out, cursor = [], None
        while True:
            p = dict(channel=CHANNEL, oldest=f"{oldest_ts:.6f}", limit=200)
            if cursor:
                p["cursor"] = cursor
            r = self.api("conversations.history", **p)
            out += r.get("messages", [])
            cursor = (r.get("response_metadata") or {}).get("next_cursor")
            if not cursor:
                return out

    def thread(self, ts):
        r = self.api("conversations.replies", channel=CHANNEL, ts=ts, limit=200)
        return r.get("messages", [])

    def channel(self, oldest_ts):
        """Top-level messages + their thread replies since oldest_ts. Flat list of dicts."""
        tops, cursor = [], None
        while True:
            p = dict(channel=CHANNEL, oldest=f"{oldest_ts:.6f}", limit=200)
            if cursor:
                p["cursor"] = cursor
            r = self.api("conversations.history", **p)
            tops += r.get("messages", [])
            cursor = (r.get("response_metadata") or {}).get("next_cursor")
            if not cursor:
                break
        # threads started earlier but active in the window show up only via replies;
        # the parent is outside `oldest`, so also scan older parents with recent latest_reply
        older, cursor = [], None
        while True:
            p = dict(channel=CHANNEL, latest=f"{oldest_ts:.6f}",
                     oldest=f"{oldest_ts - 200 * 86400:.6f}", limit=200)
            if cursor:
                p["cursor"] = cursor
            r = self.api("conversations.history", **p)
            older += [m for m in r.get("messages", [])
                      if float(m.get("latest_reply") or 0) >= oldest_ts]
            cursor = (r.get("response_metadata") or {}).get("next_cursor")
            if not cursor:
                break
        out = []
        for top in tops + older:
            thread = [top]
            if top.get("reply_count"):
                try:
                    r = self.api("conversations.replies", channel=CHANNEL, ts=top["ts"], limit=200)
                    thread = r.get("messages", [top])
                except Exception as e:
                    log(f"slack replies {top['ts']} failed: {e}")
            parent_txt = self.text(top)[:80]
            for m in thread:
                if m.get("subtype") in ("channel_join", "channel_leave"):
                    continue
                ts = float(m["ts"])
                if ts < oldest_ts:
                    continue
                out.append(dict(
                    ts=ts, date=dt.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M"),
                    user=m.get("user", ""), who=self.name(m.get("user", "")) if m.get("user") else "bot",
                    text=self.text(m), thread=top["ts"], parent=parent_txt,
                    top=(m["ts"] == top["ts"]),
                    link=f"https://irisai.slack.com/archives/{CHANNEL}/p{m['ts'].replace('.', '')}"))
        out.sort(key=lambda x: x["ts"])
        return out


def slack_from_cognion(oldest_date):
    """Fallback: parse the Cognion weekly text copies into the same flat shape."""
    out = []
    for f in sorted(glob.glob(str(COGNION / "text" / "Slack" / "#active-engagements" / "*.txt"))):
        for ln in Path(f).read_text(errors="ignore").splitlines():
            m = re.match(r"^\s*(?:> )?\[(\d{4}-\d\d-\d\d \d\d:\d\d)\] ([^:]+): (.*)$", ln)
            if m and m.group(1)[:10] >= oldest_date.isoformat():
                who = m.group(2).strip()
                out.append(dict(ts=dt.datetime.fromisoformat(m.group(1)).timestamp(), date=m.group(1),
                                user=IVO_SLACK if who == "Ivo Stefanov" else "", who=who,
                                text=m.group(3), thread="", parent="", top=not ln.lstrip().startswith(">"),
                                link=""))
            elif out and ln.startswith("    ") and not ln.strip().startswith("["):
                out[-1]["text"] += "\n" + ln.strip().lstrip("> ").strip()
    out.sort(key=lambda x: x["ts"])
    return out


# ----------------------------------------------------------------------------- calendar
FREE_MAIL = {"gmail.com", "googlemail.com", "outlook.com", "hotmail.com", "live.com", "yahoo.com", "icloud.com",
             "me.com", "proton.me", "protonmail.com", "abv.bg", "mail.bg", "gmx.de", "web.de"}


def is_external(email):
    dom = email.lower().split("@")[-1] if "@" in email else ""
    return bool(dom) and dom != "iris.ai" and dom not in FREE_MAIL and "calendar.google.com" not in dom


def google_token(scope=CAL_SCOPE):
    """Short-lived access token narrowed to `scope`, from the workspace-mcp refresh token (in memory only)."""
    c = json.loads(GOOGLE_CRED.read_text())
    body = urllib.parse.urlencode(dict(client_id=c["client_id"], client_secret=c["client_secret"],
                                       refresh_token=c["refresh_token"], grant_type="refresh_token",
                                       scope=scope)).encode()
    with urllib.request.urlopen(urllib.request.Request(c.get("token_uri") or "https://oauth2.googleapis.com/token",
                                                       data=body), timeout=30) as r:
        return json.loads(r.read())["access_token"]


def calendar(t0, t1):
    tok = google_token()
    events, page = [], None
    while True:
        q = dict(timeMin=t0.isoformat() + "T00:00:00Z", timeMax=t1.isoformat() + "T00:00:00Z",
                 singleEvents="true", orderBy="startTime", maxResults=2500)
        if page:
            q["pageToken"] = page
        url = "https://www.googleapis.com/calendar/v3/calendars/primary/events?" + urllib.parse.urlencode(q)
        with urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": "Bearer " + tok}),
                                    timeout=60) as r:
            data = json.loads(r.read())
        for e in data.get("items", []):
            if e.get("status") == "cancelled" or "dateTime" not in (e.get("start") or {}):
                continue
            if e.get("eventType") in ("outOfOffice", "focusTime", "workingLocation"):
                continue
            att = e.get("attendees") or []
            me = next((a for a in att if a.get("self") or a.get("email") == IVO_EMAIL), None)
            if me and me.get("responseStatus") == "declined":
                continue
            if len(att) < 2:
                continue
            events.append(dict(title=e.get("summary") or "(no title)", start=e["start"]["dateTime"],
                               emails=[a.get("email", "").lower() for a in att],
                               external=any(is_external(a.get("email", "")) and not a.get("resource") for a in att),
                               response="accepted" if (e.get("organizer") or {}).get("self")
                               else (me or {}).get("responseStatus", "")))
        page = data.get("nextPageToken")
        if not page:
            break
    return events


GMAIL_RO = "https://www.googleapis.com/auth/gmail.readonly"


def gmail_sent(domains, since, limit=8):
    """Read-only: emails Ivo SENT to any of `domains` since `since` (date). Subject, date, to, snippet."""
    if not domains:
        return []
    tok = google_token(GMAIL_RO)
    q = "in:sent after:{} ({})".format(since.strftime("%Y/%m/%d"), " OR ".join(f"to:{x}" for x in sorted(domains)))
    url = "https://gmail.googleapis.com/gmail/v1/users/me/messages?" + urllib.parse.urlencode(dict(q=q, maxResults=limit))
    hdr = {"Authorization": "Bearer " + tok}
    with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=30) as r:
        ids = [m["id"] for m in json.loads(r.read()).get("messages", [])]
    out = []
    for i in ids:
        u = (f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{i}?format=metadata"
             "&metadataHeaders=Subject&metadataHeaders=Date&metadataHeaders=To")
        with urllib.request.urlopen(urllib.request.Request(u, headers=hdr), timeout=30) as r:
            m = json.loads(r.read())
        h = {x["name"]: x["value"] for x in m.get("payload", {}).get("headers", [])}
        out.append(dict(date=dt.datetime.fromtimestamp(int(m["internalDate"]) / 1000).strftime("%Y-%m-%d"),
                        subject=h.get("Subject", ""), to=h.get("To", "")[:120], snippet=html.unescape(m.get("snippet", ""))[:300]))
    return out


def bitbucket_commits(rx, since):
    """Commits on Bitbucket repos linked to an engagement (Cognion activity.json), since `since`.
    The engagements repo itself is skipped (its per-folder git log is read directly)."""
    p = COGNION / "proto" / "data" / "bitbucket" / "activity.json"
    data = json.loads(p.read_text())
    out = {}
    for r in data.get("repos", []):
        if r.get("slug") == "engagements":
            continue
        hits = match(rx, " ".join([r.get("slug", "").replace("_", " ").replace("-", " ")]
                                  + [str(c).replace("-", " ") for c in (r.get("clients") or [])]))
        for c in r.get("commits") or []:
            if c.get("date", "")[:10] >= since.isoformat():
                for h in hits:
                    out.setdefault(h, []).append(f"{c['date'][:10]} {r['slug']}: {c.get('msg', '')[:120]} ({c.get('author', '')})")
    return out


def calendar_from_cognion(t0, t1):
    data = json.loads((COGNION / "proto" / "data" / "calendar" / "events.json").read_text())
    out = []
    for e in data["events"]:
        if not (t0.isoformat() <= e["date"] < t1.isoformat()):
            continue
        me = next((a for a in e["attendees"] if a.get("email") == IVO_EMAIL), None)
        if not me or me.get("response") == "declined":
            continue
        emails = [a.get("email", "") for a in e["attendees"]]
        out.append(dict(title=e["title"], start=e["start"], emails=emails,
                        external=any(is_external(x) for x in emails), response=me.get("response", "")))
    return out


# ----------------------------------------------------------------------------- tactiq
def tactiq_week(t0):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import tactiq_client as T
    out, offset = [], 0
    while True:
        r = T.gql("ListMeetings", T.LIST_QUERY, {"type": "MyMeetings", "offset": offset, "filter": {},
                                                  "sortBy": "CREATED_NEWEST_FIRST"})
        page = r["data"]["meetings"]
        stop = False
        for m in page["meetings"]:
            day = dt.datetime.fromtimestamp((m.get("created") or 0) / 1000).date()
            if day < t0:
                stop = True
                break
            out.append(dict(id=m["id"], title=m.get("title") or "", date=day.isoformat()))
        if stop or not page.get("hasMore"):
            break
        offset += len(page["meetings"])
    return out


def cognion_meetings(t0, t1):
    """Front-matter summaries of this week's meetings Ivo was in (Cognion text copy)."""
    out = []
    for month in {t0.strftime("%Y-%m"), (t1 - dt.timedelta(days=1)).strftime("%Y-%m")}:
        for f in sorted(glob.glob(str(COGNION / "text" / "Meetings" / month / "*.txt"))):
            name = os.path.basename(f)
            if not (t0.isoformat() <= name[:10] < t1.isoformat()):
                continue
            head = Path(f).read_text(errors="ignore")[:6000]
            fm = dict(re.findall(r"^(\w+): (.*)$", head.split("\n---", 2)[0] if head.startswith("---") else "", re.M))
            if "ivo-stefanov" not in fm.get("participant_ids", "") and "Ivo" not in fm.get("participants", ""):
                continue
            if fm.get("sensitivity") == "restricted":
                continue
            out.append(dict(date=name[:10], title=fm.get("title", name)[11:], url=fm.get("url", ""),
                            participants=fm.get("participants", ""), summary=fm.get("summary", "")))
    return out


# ----------------------------------------------------------------------------- engagements
def aliases():
    import yaml
    data = yaml.safe_load((ENG / "_aliases.yaml").read_text()) or {}
    return {k: v or {} for k, v in data.items() if isinstance(v, dict) or v is None}


def git(*args, cwd=ENG):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=60)
    return r.stdout


def engagement_files(name, t0):
    folder = ENG / name
    st = folder / "STATUS.md"
    # last commit that added or removed an entry heading; skips mechanical edits (renames, typo fixes)
    last = (git("log", "-1", "--format=%ad", "--date=short", "-G^## ", "--", f"{name}/STATUS.md").strip()
            or git("log", "-1", "--format=%ad", "--date=short", "--", f"{name}/STATUS.md").strip())
    if git("status", "--porcelain", "--", f"{name}/STATUS.md").strip():
        last = dt.date.today().isoformat()   # uncommitted edit counts as a change today
    text = st.read_text(errors="ignore") if st.exists() else ""
    sections = re.split(r"\n(?=## )", text)
    entries = [s for s in sections if s.startswith("## ")]
    week = []
    for e in entries:
        ds = re.findall(r"\d{4}-\d\d-\d\d", e.split("\n", 1)[0])
        if ds and max(ds) >= t0.isoformat():
            week.append(e)
    newest = "\n".join(week) if week else (
        "[no STATUS entry this week; newest older entry, context only]\n" + (entries[0][:700] if entries else ""))
    nxt = []
    if entries:
        for m in re.finditer(r"Next action:(.*)", entries[0]):
            nxt.append(m.group(1).strip())
    art = git("log", f"--since={t0.isoformat()}", "-p", "--format=", "--", f"{name}/ARTEFACTS.md")
    added = [ln[1:] for ln in art.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    return dict(last_status=last or None, newest=newest, has_week_entry=bool(week), next_actions=nxt,
                artefacts_added="\n".join(added))


def matcher(al):
    rx = {}
    for name, v in al.items():
        terms = set(v.get("titles") or []) | {name.replace("-", " ")}
        terms = {t for t in terms if t and len(t) >= 4}
        if name == "benefit-software":
            terms |= {"Benefit Network", "Benefit chat", "Benefit x"}
        rx[name] = (re.compile(r"\b(" + "|".join(re.escape(t) for t in sorted(terms, key=len, reverse=True)) + r")\b", re.I)
                    if terms else None, {x.lower() for x in (v.get("domains") or [])})
    return rx


def match(rx, text="", emails=()):
    """Engagements hit by text aliases or attendee domains. When several engagements share a
    domain (fresenius, fresenius-complaint-coding, ...), keep only the best title match."""
    score = {}
    doms = {e.split("@")[-1].lower() for e in emails if "@" in e}
    for name, (r, ds) in rx.items():
        best = 0
        if r and text:
            best = max((len(m.group(0)) for m in r.finditer(text)), default=0)
        if not best and ds and doms & ds:
            best = 1
        if best:
            score[name] = best
    hits = set(score)
    for a in list(hits):
        for b in list(hits):
            if a != b and score[a] < score[b] and (rx[a][1] & rx[b][1] or a.startswith(b) or b.startswith(a)):
                hits.discard(a)
    return hits


def find_threads(slack, rx, days=365):
    """engagement -> newest top-level #active-engagements message that names it in its first line.
    Ivo opens a thread per engagement with a short top-level line (e.g. "Intertek")."""
    tops = slack.tops((dt.datetime.now() - dt.timedelta(days=days)).timestamp())
    found = {}
    for m in tops:  # newest first
        if m.get("subtype"):
            continue
        first = (m.get("text") or "").strip().split("\n", 1)[0][:120]
        hits = match(rx, first)
        if len(hits) != 1:
            continue
        h = hits.pop()
        if h not in found:
            found[h] = dict(ts=m["ts"], text=first, reply_count=m.get("reply_count", 0),
                            latest_reply=m.get("latest_reply") or m["ts"],
                            permalink=f"https://irisai.slack.com/archives/{CHANNEL}/p{m['ts'].replace('.', '')}")
    return found


DATE_RX = re.compile(r"by:?\s*(\d{4}-\d\d-\d\d)")


# ----------------------------------------------------------------------------- people away
AP_CONFIG = ATLAS / "_autopilot" / "config.json"
COVER_DEFAULT = "[cover]"


def load_config():
    try:
        return json.loads(AP_CONFIG.read_text())
    except (OSError, ValueError):
        return {}


def save_config(c):
    AP_CONFIG.parent.mkdir(parents=True, exist_ok=True)
    tmp = AP_CONFIG.with_suffix(".tmp")
    tmp.write_text(json.dumps(c, indent=1, ensure_ascii=False) + "\n")
    tmp.replace(AP_CONFIG)


def _rule_rx(match):
    """'AWS (credits, funding, co-sell, marketplace)' -> regex hitting any of those words."""
    words = [w for w in re.split(r"[^\w-]+", match or "") if len(w) >= 3]
    return re.compile(r"\b(" + "|".join(re.escape(w) for w in words) + r")\b", re.I) if words else None


def people_away(today=None):
    """config.json people_away entries whose from..until (inclusive) covers `today`.
    Each: key, name, first, start, until, rule, cover (name or "[cover]"), cover_rules [(match, cover, rx)],
    email, slack_id."""
    today = today or dt.date.today()
    out = []
    for key, p in (load_config().get("people_away") or {}).items():
        try:
            f, u = d(p["from"]), d(p["until"])
        except (KeyError, TypeError, ValueError):
            continue
        if f <= today <= u:
            name = (p.get("name") or key).strip()
            rules = [(r["match"], r["cover"].strip(), _rule_rx(r["match"])) for r in (p.get("cover_rules") or [])
                     if isinstance(r, dict) and r.get("match") and (r.get("cover") or "").strip()]
            out.append(dict(key=key, name=name, first=name.split()[0], start=f, until=u, rule=p.get("rule") or "",
                            cover=(p.get("cover") or "").strip() or COVER_DEFAULT, cover_rules=rules,
                            email=(p.get("email") or "").lower(), slack_id=p.get("slack_id") or ""))
    return out


def _first(name):
    return name if name == COVER_DEFAULT else name.split()[0]


def _who(name, slack):
    """How a cover is written: "@Steven" in Slack drafts, "Steven" elsewhere, "[cover]" as is."""
    return name if name == COVER_DEFAULT else ("@" if slack else "") + _first(name)


def cover_for(p, text):
    """Cover for one item: the first cover_rule whose words appear in `text`, else the default cover."""
    for _, cov, rx in p["cover_rules"]:
        if rx and rx.search(text or ""):
            return cov
    return p["cover"]


def away_rule(today=None, away=None):
    """Prompt block for the model. Empty string when nobody is away."""
    away = people_away(today) if away is None else away
    if not away:
        return ""
    out = ["", "PEOPLE AWAY (hard rule, overrides every other instruction, example and source text):"]
    for p in away:
        f, c = p["first"], p["cover"]
        routes = "; ".join(f"{m} items -> {cov} (@{_first(cov)})" for m, cov, _ in p["cover_rules"])
        dflt = c if c == COVER_DEFAULT else f"{c} (@{_first(c)})"
        out += [
            f"- {p['name']} ({f}) is away {p['start']:%a %-d %b} to {p['until']:%a %-d %b %Y}."
            + (f" Ivo's rule: {p['rule']}." if p["rule"] else ""),
            f"  - Never @mention {f}. No \"cc: @{f}\" line, never cc {f} on an email, do not address him in an opener.",
            f"  - Never make {f} the owner of a next step, gate or action, even where the data or older posts name him.",
            "  - Cover owners for what would have been his: " + (routes + "; everything else -> " if routes else "")
            + dflt + ". In Slack drafts @mention the cover where he would have been (cc line, \"Over to @<cover>\", "
            "owner); in emails and STATUS text write the cover's first name, no @.",
            f"  - Things only {f} can decide or do go on a \"For {f} when back\" list where the task asks for one; "
            "otherwise state them with the cover as owner.",
        ]
    return "\n".join(out) + "\n"


def _name_rx(p):
    parts = [re.escape(p["name"])] + ([re.escape(p["first"])] if p["first"] != p["name"] else [])
    return "(?:" + "|".join(parts) + ")"


_OWNER_VERBS = (r"(?:sends?|to send|will|owns|books?|to book|chases?|to chase|follows? up|to follow up|confirms?|"
                r"to confirm|drafts?|to draft|shares?|to share|schedules?|to schedule|picks? up|takes? over|handles?|"
                r"to handle|replies|to reply|signs?|to sign)")


def scrub_away(text, today=None, away=None, slack=True):
    """Deterministic backstop for generated drafts while someone is away. Removes @mentions of him and
    swaps him out as owner of next steps for the cover (cover_rules matched on that line, else the default
    cover). cc lines lose him; in Slack drafts they get the covers used in this draft instead (default
    cover if none). slack=True writes covers as @First; False (email, STATUS) as First."""
    away = people_away(today) if away is None else away
    if not away or not text:
        return text
    cc_rx = re.compile(r"^(\s*(?:[-*•]\s*)?cc:?\s*)(.*)$", re.I)
    for p in away:
        N = _name_rx(p)
        lines, used = text.split("\n"), []
        for i, ln in enumerate(lines):
            if cc_rx.match(ln):
                continue
            cov = cover_for(p, ln)
            w, before = _who(cov, slack), ln
            if p["slack_id"]:
                ln = ln.replace(f"<@{p['slack_id']}>", "@" + p["first"])
            ln = re.sub(rf"\b(Hey|Hi|Hello)\s+@?{N},\s*", r"\1 ", ln)
            ln = re.sub(rf"\b(Over to)\s+@?{N}\b", rf"\1 {w}", ln, flags=re.I)
            ln = re.sub(rf"\b(owner:?\s*)@?{N}\b", rf"\g<1>{w}", ln, flags=re.I)
            ln = re.sub(rf"(\s-\s+)@?{N}(\s+-\s)", rf"\g<1>{w}\g<2>", ln)        # "<step> - Jordan - <date>"
            ln = re.sub(rf"(\s-\s+)@?{N}\s*$", rf"\g<1>{w}", ln)                  # "<step> - Jordan"
            ln = re.sub(rf"(^|[:•]\s*|^\s*[-*]\s+)@?{N}\s+(?={_OWNER_VERBS}\b)", rf"\g<1>{w} ", ln)
            if ln != before and w in ln and cov not in used:
                used.append(cov)
            lines[i] = re.sub(rf"@({N})\b", r"\1", ln, flags=re.I)              # any mention left: plain name
        out = []
        for ln in lines:
            m = cc_rx.match(ln)
            if m and re.search(N, m.group(2), re.I):
                rest = re.sub(rf"(?:\s*(?:,|&|\band\b)\s*)?@?{N}\b", "", m.group(2), flags=re.I)
                rest = re.sub(r"^\s*(?:,|&|\band\b)\s*", "", rest, flags=re.I).strip()
                if slack:
                    add = [_who(c, True) for c in (used or [p["cover"]]) if c != COVER_DEFAULT
                           and not re.search(rf"@{re.escape(_first(c))}\b", rest)]
                    rest = ", ".join(add + ([rest] if rest else []))
                if not re.search(r"\w", rest):
                    continue                          # the cc line was only him
                ln = m.group(1) + rest
            out.append(ln)
        text = "\n".join(out)
    return text


def drop_away_emails(addrs, today=None, away=None):
    """Remove away people from an email address list (explicit `email`, else name parts in the local part)."""
    away = people_away(today) if away is None else away
    if not away or not addrs:
        return addrs

    def hit(a):
        a = a.lower()
        local = a.split("<")[-1].split("@")[0]
        for p in away:
            if p["email"] and p["email"] in a:
                return True
            if not p["email"] and a.rstrip(">").endswith("@iris.ai") and p["first"].lower() in re.split(r"[._\-+]", local):
                return True
        return False
    return [a for a in addrs if not hit(a)]


# ----------------------------------------------------------------------------- llm
def bedrock(system, user, max_tokens=MAX_OUT):
    import boto3
    from botocore.config import Config
    c = boto3.Session(profile_name=os.environ.get("AWS_PROFILE", "Iris_Devs"),
                      region_name=os.environ.get("AWS_REGION", "eu-west-1")).client(
        "bedrock-runtime", config=Config(read_timeout=600, retries={"max_attempts": 2}))
    r = c.converse(modelId=MODEL, system=[{"text": system}],
                   messages=[{"role": "user", "content": [{"text": user}]}],
                   inferenceConfig={"maxTokens": max_tokens},
                   additionalModelRequestFields={"output_config": {"effort": EFFORT}})
    u = r["usage"]
    cost = u["inputTokens"] * PRICE_IN + u["outputTokens"] * PRICE_OUT   # outputTokens includes thinking
    text = "".join(b["text"] for b in r["output"]["message"]["content"] if "text" in b)
    if r.get("stopReason") == "max_tokens":
        log(f"WARNING: output hit max_tokens={max_tokens}, draft may be cut")
    return text, u, cost


def est_cost(chars):
    return (chars / 3.2) * PRICE_IN + MAX_OUT * PRICE_OUT


def voice_block():
    v = json.loads((TWIN / "voice_written.json").read_text())
    tp = (TWIN / "backtest" / "twin_prompt.md").read_text()
    real = tp.split("Real messages he wrote", 1)[-1].split("How Ivo writes", 1)[0]
    en_real = "\n".join(ln for ln in real.splitlines() if ln.startswith("- ") and re.match(r"^- [\x00-\x7f]+$", ln))
    return "\n".join([
        "Ivo's written voice (from his digital twin, learned from his own Slack):",
        "Do:", *("- " + x for x in v["do"]),
        "Don't:", *("- " + x for x in v["dont"]),
        "Phrases (sparingly): " + "; ".join(v["phrases"]),
        "Long posts: " + v["long_post_guidance"],
        "What survives of him in long posts: " + v["ai_assisted_vs_own"],
        "Real short messages he wrote:", en_real,
    ])




SYSTEM = """You draft text for Ivo Stefanov, Solutions Architect at Iris.ai. You only write drafts; \
nothing you write is sent automatically. Ivo reviews and posts himself.

Audience: Jordan Ryken (Principal Sales Director, owns every commercial thread and client relationship) \
and Steven Fung (CRO, never "CCO"). Non-technical commercial readers. Ivan Tsenov = "Vankata" = CPO.

Hard rules:
- Use ONLY facts present in the data. Never invent dates, prices, commitments, owners, links or numbers. \
If something needed is missing, write "(?: <what is missing>)" inline so Ivo sees the gap.
- No em dashes or en dashes anywhere. Use commas, colons or parentheses. Arrows as "->".
- Jordan owns commercial: frame commercial items as handoffs to Jordan ("Over to Jordan: ..."). \
Never draft Jordan's replies, emails, reschedules or follow-ups to clients.
- Client-facing product names: Axion, Neuralith, Iris.ai models. Never mention GPT, Qwen, Chandra, vLLM, \
Claude, Bedrock or run IDs.
- Every list item and sentence starts with a capital letter (work Slack). Keep hedges ("I think") only on \
real opinions, never on facts or commitments.
- No bold section headers inside Slack-ready text except the *Client* title lines Ivo really uses. \
No tidy wrap-up summary at the end. Slight looseness is fine.
- Dates as "Mon 19 Oct". Times with zone when known.

{voice}
"""


def system_prompt(today=None):
    """SYSTEM with Ivo's voice, plus the people-away hard rule when someone is away."""
    return SYSTEM.format(voice=voice_block()) + away_rule(today)


# ----------------------------------------------------------------------------- notify
def notify(path, title, msg):
    p = str(path).replace('"', '\\"')
    m = msg.replace('"', "'")
    script = (f'display notification "{m}" with title "{title}" sound name "Glass"\n'
              f'set r to display dialog "{m}" with title "{title}" buttons {{"Later", "Open draft"}} '
              f'default button "Open draft" giving up after 3600\n'
              f'if button returned of r is "Open draft" then do shell script "open " & quoted form of "{p}"')
    subprocess.Popen(["/usr/bin/osascript", "-e", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ----------------------------------------------------------------------------- cli
def _cli():
    ap = argparse.ArgumentParser(prog="autopilot_common.py", description="Autopilot config helpers")
    sub = ap.add_subparsers(dest="cmd", required=True)
    aw = sub.add_parser("away", help="people_away map in _autopilot/config.json").add_subparsers(dest="op", required=True)
    a = aw.add_parser("add", help="add or replace a person away")
    a.add_argument("key")
    a.add_argument("name")
    a.add_argument("start", metavar="from", help="YYYY-MM-DD")
    a.add_argument("until", help="YYYY-MM-DD (inclusive)")
    a.add_argument("--cover", help="owner to use instead of [cover]")
    a.add_argument("--cover-rule", action="append", default=None, metavar="MATCH=NAME",
                   help='route matching items to NAME, e.g. "AWS (credits, funding, co-sell, marketplace)=Eric Frances"; '
                        "repeatable; any word of MATCH on a line hits")
    a.add_argument("--rule", help="free-text rule shown to the model")
    a.add_argument("--email", help="address to drop from email cc (default: name match on @iris.ai)")
    aw.add_parser("list", help="show everyone in the map, marking who is away today")
    r = aw.add_parser("rm", help="remove a person")
    r.add_argument("key")
    x = ap.parse_args()
    c = load_config()
    pa = c.setdefault("people_away", {})
    if x.op == "add":
        f, u = d(x.start), d(x.until)
        if u < f:
            sys.exit("until is before from")
        e = dict(name=x.name, **{"from": f.isoformat()}, until=u.isoformat(),
                 rule=x.rule or (pa.get(x.key) or {}).get("rule")
                 or "no @mentions; route his items to the cover owner or a 'for <name> when back' list")
        for k in ("cover", "email"):
            v = getattr(x, k) or (pa.get(x.key) or {}).get(k)
            if v:
                e[k] = v
        if x.cover_rule is not None:
            rules = []
            for cr in x.cover_rule:
                m, sep, n = cr.rpartition("=")
                if not sep or not m.strip() or not n.strip():
                    sys.exit(f"bad --cover-rule {cr!r}, want MATCH=NAME")
                rules.append(dict(match=m.strip(), cover=n.strip()))
            e["cover_rules"] = rules
        elif (pa.get(x.key) or {}).get("cover_rules"):
            e["cover_rules"] = pa[x.key]["cover_rules"]
        pa[x.key] = e
        save_config(c)
        print(f"added {x.key}: {x.name} {f} to {u}" + (f", cover {e['cover']}" if e.get("cover") else ""))
    elif x.op == "rm":
        if pa.pop(x.key, None) is None:
            sys.exit(f"no such key: {x.key}")
        save_config(c)
        print(f"removed {x.key}")
    else:
        now_away = {p["key"] for p in people_away()}
        if not pa:
            print("nobody in people_away")
        for k, p in pa.items():
            print(f"{'AWAY ' if k in now_away else '     '}{k}: {p.get('name')} {p.get('from')} to {p.get('until')}"
                  f", cover {p.get('cover') or COVER_DEFAULT}" + (f", email {p['email']}" if p.get("email") else ""))
            for r in p.get("cover_rules") or []:
                print(f"       {r.get('match')} -> {r.get('cover')}")


if __name__ == "__main__":
    _cli()
