#!/usr/bin/env python3
"""Shared approval queue: one JSON file per draft in atlas/_autopilot/queue/<id>.json (gitignored).

Every autopilot producer (weekly-rollup, monday-thread, missing-post, post-call, session-hook,
cognion-daily, slash-command) drops drafts here. Nothing is sent from here: the Approvals inbox
(approvals_app.py, http://127.0.0.1:8096) shows them, and an executor runs only on Ivo's click.

Item schema:
  id        str   "<yyyymmdd-hhmmss>-<source>-<engagement>-<4 hex>"
  created   str   ISO timestamp
  source    weekly-rollup | monday-thread | missing-post | post-call | session-hook | cognion-daily |
            slash-command (/reply, /email run by Ivo in a Claude tab)
  engagement str  engagements/ folder name, or "operations"
  kind      slack_post | slack_thread_reply | email_draft | gmail_draft | form | status_entry |
            calendar_event | note | asana
  target    {channel, thread_ts, permalink} | {to, cc, subject} | {form_url, prefill_url} | {path}
  title     str
  body      str   markdown, editable in the inbox
  sources   [{label, path_or_url}]
  status    pending | approved | sent | rejected | done
  history   [{ts, action, by, note?}]
  surface_at str  optional ISO time; the inbox hides the item until then (set automatically for items
                  created in quiet hours, 19:00-08:00 Europe/Sofia, see autopilot_common.quiet_until)
  key       str   optional dedupe key: add() with the same key updates the pending item instead
                  of creating a second one (e.g. "monday-thread:intertek:2026-W43")

API (import from any script):
  add(source, engagement, kind, title, body, target=None, sources=None, key=None, by="autopilot", surface_at=None) -> item
  get(id) -> item | None
  list_items(status=None, engagement=None, source=None, visible_only=False) -> [item], newest first
  update(id, action, by="ivo", note=None, **fields) -> item      (records history)
  pending_count(visible_only=True) -> int ; held_count() -> int (quiet-hours items not yet shown)

CLI:  approval_queue.py list [status] | show <id> | count
      approval_queue.py add --kind slack_thread_reply --title T --channel C --thread-ts TS
                            [--permalink URL] [--engagement E] [--source S] [--key K]  < body.txt
"""
import datetime as dt
import fcntl
import json
import os
import re
import secrets
import sys
from contextlib import contextmanager
from pathlib import Path

QUEUE = Path.home() / "Documents" / "atlas" / "_autopilot" / "queue"

SOURCES = {"weekly-rollup", "monday-thread", "missing-post", "post-call", "session-hook", "cognion-daily",
           "slash-command"}
KINDS = {"slack_post", "slack_thread_reply", "email_draft", "gmail_draft", "form", "status_entry",
         "calendar_event", "note", "asana"}
STATUSES = {"pending", "approved", "sent", "rejected", "done"}


def _now():
    return dt.datetime.now().isoformat(timespec="seconds")


@contextmanager
def _lock():
    QUEUE.mkdir(parents=True, exist_ok=True)
    with open(QUEUE / ".lock", "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def _path(item_id):
    if not re.fullmatch(r"[\w.-]+", item_id or ""):
        raise ValueError(f"bad id: {item_id!r}")
    return QUEUE / f"{item_id}.json"


def _write(item):
    p = _path(item["id"])
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(item, indent=1, ensure_ascii=False))
    os.replace(tmp, p)


def _read_all():
    out = []
    for p in QUEUE.glob("*.json"):
        try:
            out.append(json.loads(p.read_text()))
        except Exception:
            continue
    return out


def _quiet_until():
    """End of quiet hours (19:00-08:00 Europe/Sofia, autopilot_common) if we are inside them, else None."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from autopilot_common import quiet_until
        return quiet_until()
    except Exception:
        return None


def visible(item, now=None):
    """False while a new item is held back by quiet hours (surface_at in the future)."""
    s = item.get("surface_at")
    if not s:
        return True
    try:
        return dt.datetime.fromisoformat(s) <= (now or dt.datetime.now().astimezone())
    except ValueError:
        return True


def add(source, engagement, kind, title, body, target=None, sources=None, key=None, by="autopilot", surface_at=None):
    """surface_at: ISO time before which the inbox hides the item. Default: end of quiet hours when created
    inside them (so nothing new shows up after 19:00), else visible at once."""
    if source not in SOURCES:
        raise ValueError(f"unknown source {source!r}")
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}")
    with _lock():
        if key:
            for it in _read_all():
                if it.get("key") == key and it.get("status") == "pending":
                    it.update(title=title, body=body, target=target or {}, sources=sources or [])
                    it["history"].append(dict(ts=_now(), action="refreshed", by=by))
                    _write(it)
                    return it
        slug = re.sub(r"[^\w-]", "", (engagement or "operations"))[:30]
        item = dict(id=f"{dt.datetime.now():%Y%m%d-%H%M%S}-{source}-{slug}-{secrets.token_hex(2)}",
                    created=_now(), source=source, engagement=engagement or "operations", kind=kind,
                    target=target or {}, title=title, body=body, sources=sources or [], status="pending",
                    history=[dict(ts=_now(), action="created", by=by)])
        if key:
            item["key"] = key
        if surface_at is None:
            q = _quiet_until()
            surface_at = q.isoformat(timespec="seconds") if q else None
        if surface_at:
            item["surface_at"] = surface_at
            item["history"].append(dict(ts=_now(), action=f"held until {surface_at[:16]} (quiet hours)", by=by))
        _write(item)
        return item


def get(item_id):
    p = _path(item_id)
    return json.loads(p.read_text()) if p.exists() else None


def list_items(status=None, engagement=None, source=None, visible_only=False):
    """visible_only: drop items still held by quiet hours (the inbox view). Dedupe/supersede callers keep the default."""
    items = _read_all()
    if visible_only:
        items = [i for i in items if visible(i)]
    if status:
        st = {status} if isinstance(status, str) else set(status)
        items = [i for i in items if i.get("status") in st]
    if engagement:
        items = [i for i in items if i.get("engagement") == engagement]
    if source:
        items = [i for i in items if i.get("source") == source]
    return sorted(items, key=lambda i: i.get("created", ""), reverse=True)


def update(item_id, action, by="ivo", note=None, **fields):
    with _lock():
        it = get(item_id)
        if not it:
            raise KeyError(item_id)
        if "status" in fields and fields["status"] not in STATUSES:
            raise ValueError(f"bad status {fields['status']!r}")
        it.update(fields)
        h = dict(ts=_now(), action=action, by=by)
        if note:
            h["note"] = note
        it["history"].append(h)
        _write(it)
        return it


def pending_count(visible_only=True):
    return len(list_items("pending", visible_only=visible_only))


def held_count():
    """Pending items created in quiet hours that surface in the morning."""
    return len(list_items("pending")) - pending_count()


def _cli_add(argv):
    """Queue a draft from the shell (body on stdin). Prints the item id. Nothing is sent."""
    import argparse
    ap = argparse.ArgumentParser(prog="approval_queue.py add")
    ap.add_argument("--kind", required=True, choices=sorted(KINDS))
    ap.add_argument("--title", required=True)
    ap.add_argument("--engagement", default="operations")
    ap.add_argument("--source", default="slash-command", choices=sorted(SOURCES))
    ap.add_argument("--key")
    ap.add_argument("--channel")
    ap.add_argument("--thread-ts")
    ap.add_argument("--permalink")
    ap.add_argument("--to")
    ap.add_argument("--cc")
    ap.add_argument("--subject")
    x = ap.parse_args(argv)
    body = sys.stdin.read().strip()
    if not body:
        sys.exit("empty body on stdin")
    if x.kind == "slack_thread_reply" and not (x.channel and x.thread_ts):
        sys.exit("slack_thread_reply needs --channel and --thread-ts")
    target = {k: v for k, v in dict(channel=x.channel, thread_ts=x.thread_ts, permalink=x.permalink,
                                    to=x.to, cc=x.cc, subject=x.subject).items() if v}
    it = add(x.source, x.engagement, x.kind, x.title, body, target=target, key=x.key, by="ivo")
    print(it["id"])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "add":
        _cli_add(sys.argv[2:])
    elif cmd == "count":
        print(pending_count())
    elif cmd == "show":
        print(json.dumps(get(sys.argv[2]), indent=1, ensure_ascii=False))
    else:
        for i in list_items(sys.argv[2] if len(sys.argv) > 2 else None):
            held = "" if visible(i) else f" (held until {i['surface_at'][11:16]})"
            print(f"{i['status']:8}{held} {i['created'][:16]} {i['source']:14} {i['engagement']:24} {i['kind']:18} {i['title'][:60]}")
