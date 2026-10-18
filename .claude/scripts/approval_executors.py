#!/usr/bin/env python3
"""Executors for the approval queue. Called ONLY by approvals_app.py when Ivo clicks "Approve & send".

  slack_post          chat.postMessage to target.channel. If the body has a "--- thread reply ---"
                      line, the part above is posted top-level and the part below as its thread reply.
  slack_thread_reply  chat.postMessage with thread_ts = target.thread_ts.
  gmail_draft         Gmail users.drafts.create (a DRAFT, never sent), gmail.compose scope.
  status_entry        insert the body as the newest entry of target.path (an engagement STATUS.md),
                      then commit only that file in the engagements repo (skipped if the file already
                      had uncommitted edits, so nobody else's work gets swept into the commit).
Other kinds (email_draft, form, calendar_event, note) have no executor: Copy / Open / Mark done.

Slack uses the same browser tokens as the local slack MCP (~/.config/slack-mcp), read at call
time and never logged. Everything executed is logged to _autopilot/logs/executor.log.
"""
import base64
import datetime as dt
import json
import re
import subprocess
import urllib.parse
import urllib.request
from email.mime.text import MIMEText
from pathlib import Path

HOME = Path.home()
ENG = HOME / "Documents" / "engagements"
SLACK_CRED = HOME / ".config" / "slack-mcp"
LOG = HOME / "Documents" / "atlas" / "_autopilot" / "logs" / "executor.log"
GMAIL_COMPOSE = "https://www.googleapis.com/auth/gmail.compose"
DEFAULT_CHANNEL = "C0B8GPS4DCN"   # #active-engagements

MENTIONS = {"Jordan": "U09UYT1C13M", "Steven": "U08PWNWRET1", "Ivan Tsenov": "U06SV8XB45N",
            "Vankata": "U06SV8XB45N", "Ivan Georgiev": "U09QB0QDL93", "Eric": "U0BU23Z2X70",
            "Vasil": "U0BLFBEJYDS"}

EXECUTABLE = {"slack_post", "slack_thread_reply", "gmail_draft", "status_entry"}


def _log(msg):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(f"{dt.datetime.now().isoformat(timespec='seconds')}  {msg}\n")


def _strip_fence(body):
    b = body.strip()
    m = re.match(r"^```\w*\n(.*?)\n```$", b, re.S)
    return m.group(1).strip() if m else b


def _mentions(text):
    for name in sorted(MENTIONS, key=len, reverse=True):
        text = re.sub(r"@" + re.escape(name) + r"\b", f"<@{MENTIONS[name]}>", text)
    return text


def _slack_post(channel, text, thread_ts=None):
    xc = (SLACK_CRED / "xoxc").read_text().strip()
    xd = (SLACK_CRED / "xoxd").read_text().strip()
    params = dict(channel=channel, text=_mentions(text), unfurl_links="false")
    if thread_ts:
        params["thread_ts"] = thread_ts
    req = urllib.request.Request("https://slack.com/api/chat.postMessage", data=urllib.parse.urlencode(params).encode(),
                                 headers={"Authorization": "Bearer " + xc, "Cookie": "d=" + xd,
                                          "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    if not data.get("ok"):
        raise RuntimeError(f"slack chat.postMessage: {data.get('error')}")
    ts = data["ts"]
    return ts, f"https://irisai.slack.com/archives/{channel}/p{ts.replace('.', '')}"


def _gmail_draft(target, body):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from autopilot_common import google_token
    msg = MIMEText(body, "plain", "utf-8")
    msg["To"] = target.get("to", "")
    if target.get("cc"):
        msg["Cc"] = target["cc"]
    msg["Subject"] = target.get("subject", "")
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    req = urllib.request.Request("https://gmail.googleapis.com/gmail/v1/users/me/drafts",
                                 data=json.dumps({"message": {"raw": raw}}).encode(),
                                 headers={"Authorization": "Bearer " + google_token(GMAIL_COMPOSE),
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read())
    return d["id"], "https://mail.google.com/mail/u/0/#drafts"


def _status_entry(target, body):
    p = Path(target["path"])
    if not p.is_absolute():
        p = ENG / p
    p = p.resolve()
    if ENG.resolve() not in p.parents or p.name != "STATUS.md":
        raise RuntimeError(f"refusing to write outside engagements/*/STATUS.md: {p}")
    rel = str(p.relative_to(ENG.resolve()))
    dirty = subprocess.run(["git", "status", "--porcelain", "--", rel], cwd=ENG, capture_output=True, text=True).stdout.strip()
    text = p.read_text()
    entry = body.strip() + "\n\n"
    i = text.find("\n## ")
    text = (text[:i + 1] + entry + text[i + 1:]) if i >= 0 else (text.rstrip() + "\n\n" + entry)
    p.write_text(text)
    if dirty:
        return "written, not committed (file had uncommitted edits)", str(p)
    title = body.strip().split("\n", 1)[0].lstrip("# ").strip()
    subprocess.run(["git", "commit", "-m", f"log {title} in {p.parent.name} STATUS", "--", rel],
                   cwd=ENG, check=True, capture_output=True, text=True)
    return "written and committed", str(p)


def execute(item, body=None):
    """Run the executor for an item. Returns dict(result=..., link=...). Raises on failure."""
    kind, t = item["kind"], item.get("target") or {}
    body = _strip_fence(body if body is not None else item["body"])
    if kind == "slack_post":
        ch = t.get("channel") or DEFAULT_CHANNEL
        parts = re.split(r"^-{3}\s*thread reply\s*-{3}\s*$", body, maxsplit=1, flags=re.M | re.I)
        ts, link = _slack_post(ch, parts[0].strip())
        res = dict(result=f"posted top-level {ts}", link=link, ts=ts)
        if len(parts) > 1 and parts[1].strip():
            ts2, link2 = _slack_post(ch, parts[1].strip(), thread_ts=ts)
            res.update(result=f"posted top-level {ts} + thread reply {ts2}", link=link2)
    elif kind == "slack_thread_reply":
        if not t.get("thread_ts"):
            raise RuntimeError("no target.thread_ts")
        body = re.sub(r"^-{3}\s*thread reply\s*-{3}\s*$", "", body, flags=re.M | re.I).strip()
        ts, link = _slack_post(t.get("channel") or DEFAULT_CHANNEL, body, thread_ts=t["thread_ts"])
        res = dict(result=f"posted thread reply {ts}", link=link, ts=ts)
    elif kind == "gmail_draft":
        did, link = _gmail_draft(t, body)
        res = dict(result=f"Gmail draft created {did} (not sent)", link=link)
    elif kind == "status_entry":
        r, path = _status_entry(t, body)
        res = dict(result=r, link=path)
    else:
        raise RuntimeError(f"no executor for kind {kind}")
    _log(f"EXECUTED {item['id']} kind={kind} target={json.dumps(t)} -> {res['result']} {res.get('link', '')}\n"
         + "\n".join("    | " + ln for ln in body.splitlines()))
    return res
