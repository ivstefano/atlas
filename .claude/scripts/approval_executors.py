#!/usr/bin/env python3
"""Executors for the approval queue. Called ONLY by approvals_app.py when Ivo clicks "Approve & send".

  slack_post          chat.postMessage to target.channel. If the body has a "--- thread reply ---"
                      line, the part above is posted top-level and the part below as its thread reply.
  slack_thread_reply  chat.postMessage with thread_ts = target.thread_ts.
  gmail_draft         Gmail users.drafts.create (a DRAFT, never sent), gmail.compose scope.
  status_entry        insert the body as the newest entry of target.path (an engagement STATUS.md),
                      then commit only that file in the engagements repo (skipped if the file already
                      had uncommitted edits, so nobody else's work gets swept into the commit).
  asana               one change in the Iris.ai Commercial Engagements project (complete a task, create a
                      next-action task, update a task or the [PIPELINE] summary). The body is the editable JSON
                      spec; it is validated here, then a headless claude (Haiku) with ONLY the Asana MCP and only
                      the read tools + the write tool that op needs (never delete) applies exactly that change.
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

EXECUTABLE = {"slack_post", "slack_thread_reply", "gmail_draft", "status_entry", "asana"}
ASANA_PROJECT = "1214855342290138"
ASANA_PROJECT_URL = "https://app.asana.com/1/61830076465436/project/1214855342290138"
ASANA_OPS = {"complete", "create", "update", "update_pipeline"}


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


def addr(v):
    """Recipients may be stored as a list (meeting autopilot digests) or a comma string."""
    return ", ".join(x for x in v if x) if isinstance(v, (list, tuple)) else (v or "")


def _gmail_draft(target, body):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from autopilot_common import google_token
    msg = MIMEText(body, "plain", "utf-8")
    msg["To"] = addr(target.get("to"))
    if target.get("cc"):
        msg["Cc"] = addr(target["cc"])
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


def asana_spec(body):
    """Parse + validate the editable Asana spec (the item body). Raises ValueError with a readable reason."""
    try:
        s = json.loads(_strip_fence(body))
    except ValueError as e:
        raise ValueError(f"Asana spec is not valid JSON: {e}")
    if not isinstance(s, dict) or s.get("op") not in ASANA_OPS:
        raise ValueError(f"op must be one of {sorted(ASANA_OPS)}")
    allowed = {"op", "section", "task", "task_gid", "name", "notes", "due_on", "assignee", "stage", "reason"}
    extra = set(s) - allowed
    if extra:
        raise ValueError(f"unknown fields: {sorted(extra)}")
    for k in allowed - {"op"}:
        v = s.get(k)
        if v is not None and (not isinstance(v, str) or len(v) > 3000):
            raise ValueError(f"{k} must be a string under 3000 chars")
    if not s.get("section"):
        raise ValueError("section is required (the engagement's section in the project)")
    if s["op"] == "create" and not s.get("name"):
        raise ValueError("create needs name")
    if s["op"] != "create" and not (s.get("task") or s.get("task_gid")):
        raise ValueError(f"{s['op']} needs task (exact name) or task_gid")
    if s["op"] == "update_pipeline" and not (s.get("stage") or s.get("notes")):
        raise ValueError("update_pipeline needs stage and/or notes")
    if s.get("task_gid") and not re.fullmatch(r"\d{6,20}", s["task_gid"]):
        raise ValueError("task_gid must be digits")
    if s.get("due_on") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s["due_on"]):
        raise ValueError("due_on must be YYYY-MM-DD")
    a = s.get("assignee")
    if a and a != "me" and not re.fullmatch(r"[\w.+-]+@iris\.ai", a):
        raise ValueError('assignee must be "me", an @iris.ai email, or null')
    for k in ("name", "notes", "stage"):
        if s.get(k):
            s[k] = s[k].replace(" — ", ", ").replace("—", ", ").replace("–", "-").replace("→", "->")
    return s


ASANA_PROMPT = """You apply exactly ONE approved change in Asana and nothing else. Never delete, never send, never touch
any other project, task or field. Project: "Iris.ai Commercial Engagements" (gid {project}).

Approved change (JSON):
{spec}

Steps:
1. Find the section named like "{section}" in project {project} (case-insensitive; "DeutscheBahn InfraGO" = DB InfraGO).
2. {find}
3. {act}
If anything is ambiguous (no such section, no task, or more than one plausible task), change nothing.
Typography in anything you write: no em dashes, use "-" or ",".
Finally output ONE line of JSON only: {{"ok": true|false, "task_gid": "...", "did": "what you changed, or why not"}}"""


def asana_instructions(s):
    """(find, act) prompt lines for a validated spec. Pure, so it is testable without Asana."""
    op = s["op"]
    if s.get("task_gid"):
        find = f"Use task gid {s['task_gid']} (check it is in that section)."
    elif op == "create":
        find = "Check no open task with the same name already exists in that section; if one does, stop."
    else:
        find = (f'Find the task in that section whose name matches {json.dumps(s.get("task"))} (exact, or the single '
                "obvious match ignoring a leading status emoji).")
    notes_add = (f"Append to its notes, keeping the existing text, after a blank line: {json.dumps(s['notes'])}."
                 if s.get("notes") else "Do not change notes.")
    if op == "complete":
        act = ("Mark that task completed. If its name starts with a status emoji, change that emoji to ✅ and keep the rest "
               "of the name. " + notes_add)
    elif op == "create":
        act = (f"Create one task named {json.dumps(s['name'])} in project {ASANA_PROJECT}, in that section"
               + (f", due_on {s['due_on']}" if s.get("due_on") else "")
               + (f", assignee {s['assignee']}" if s.get("assignee") else "")
               + (f", notes {json.dumps(s['notes'])}" if s.get("notes") else "") + ".")
    elif op == "update":
        fields = ", ".join(f"{k}={json.dumps(s[k])}" for k in ("name", "due_on", "assignee") if s.get(k))
        act = (f"Update only these fields on that task: {fields}. " if fields else "Do not change name, due date or assignee. ") + notes_add
    else:
        act = ('This is the [PIPELINE] summary task (name format "[PIPELINE] <Company> - <Industry> | <Stage> | <Amount> | '
               '<Probability> | <Close>"). '
               + (f"Replace only the <Stage> field of the name with {json.dumps(s['stage'])}; keep every other field exactly "
                  "(Amount, Probability and Close are Jordan's, never change them). " if s.get("stage") else "Do not change the name. ")
               + (f"Add this dated line at the top of its notes, keeping all existing text: {json.dumps(s['notes'])}."
                  if s.get("notes") else "Do not change notes."))
    return find, act


def _asana(target, body):
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import autopilot_common as AC
    s = asana_spec(body)
    op = s["op"]

    def has_write(allowed):
        return any(AC.ASANA_WRITE_RX[op].search(re.sub(r"^asana_", "", x.split("__")[-1])) for x in allowed.split(",") if x)
    allowed = AC.asana_allowed([op])
    if not has_write(allowed):
        AC.mcp_tools("asana", refresh=True)
        allowed = AC.asana_allowed([op])
        if not has_write(allowed):
            raise RuntimeError("Asana MCP not available to headless runs (not authenticated?): in Claude Code run /mcp, "
                               "asana, Authenticate. Item stays pending.")
    find, act = asana_instructions(s)
    prompt = ASANA_PROMPT.format(project=ASANA_PROJECT, spec=json.dumps(s, ensure_ascii=False, indent=1),
                                 section=s["section"], find=find, act=act)
    out, usd = AC.claude_headless(prompt, ["asana"], allowed, budget=0.25, timeout=300)
    _log(f"asana {op} ${usd:.3f} allowed={allowed} -> {str(out)[:300]}")
    m = re.findall(r"\{[^{}]*\"ok\"[^{}]*\}", out or "")
    try:
        res = json.loads(m[-1]) if m else None
    except ValueError:
        res = None
    if not res or not res.get("ok"):
        raise RuntimeError(f"Asana change not applied: {(res or {}).get('did') or (out or 'no answer')[:200]}")
    gid = str(res.get("task_gid") or "")
    link = f"https://app.asana.com/0/{ASANA_PROJECT}/{gid}" if gid.isdigit() else ASANA_PROJECT_URL
    return f"Asana: {res.get('did') or op} (task {gid or '?'})", link


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
    elif kind == "asana":
        r, link = _asana(t, body)
        res = dict(result=r, link=link)
    else:
        raise RuntimeError(f"no executor for kind {kind}")
    _log(f"EXECUTED {item['id']} kind={kind} target={json.dumps(t)} -> {res['result']} {res.get('link', '')}\n"
         + "\n".join("    | " + ln for ln in body.splitlines()))
    return res
