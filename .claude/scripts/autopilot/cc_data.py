"""Data layer for the command center (web.py). Read-only over local files plus the Google Calendar read the
autopilot already does. Nothing here calls an LLM or MCP; HubSpot/Asana come from the crm_refresh.py cache.

    snapshot(week_offset=0) -> dict   everything the page needs, one call
"""
import datetime as dt
import json
import os
import re
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import meeting_autopilot as A  # noqa: E402
import approval_queue as Q  # noqa: E402
import crm_refresh as CRM  # noqa: E402

TIME_FILE = Path(os.environ.get("CC_TIME_FILE") or A.ATLAS / "__private" / "time" / "weekly.json")   # {week, total_h, note, items: [{label, hours}]}
CAL_CACHE = A.CACHE / "calendar_week.json"
CAL_TTL = 180
_cal = {}
_cal_lock = threading.Lock()
CLOSED = {"closed-lost", "closed", "lost", "archived", "dead"}


def _now():
    return dt.datetime.now().astimezone()


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


# ---------------------------------------------------------------- calendar
def week_start(offset=0, today=None):
    d = today or _now().date()
    if d.weekday() >= 5:                      # weekend: show the coming week
        d += dt.timedelta(days=7 - d.weekday())
    return d - dt.timedelta(days=d.weekday()) + dt.timedelta(weeks=offset)


def calendar_week(monday):
    """Mon-Fri events. 3 min memory cache; on a failed read, the last disk copy for that week, marked stale."""
    key = monday.isoformat()
    with _cal_lock:
        hit = _cal.get(key)
        if hit and time.time() - hit[0] < CAL_TTL:
            return hit[1], hit[2], None
    t0 = dt.datetime.combine(monday, dt.time()).astimezone()
    try:
        evs = A.calendar_events(t0, t0 + dt.timedelta(days=5))
        at = _now().isoformat(timespec="seconds")
        with _cal_lock:
            _cal[key] = (time.time(), evs, at)
        try:
            disk = json.loads(CAL_CACHE.read_text()) if CAL_CACHE.exists() else {}
        except ValueError:
            disk = {}
        disk = {k: v for k, v in disk.items() if k >= (monday - dt.timedelta(weeks=2)).isoformat()}
        disk[key] = {"at": at, "events": evs}
        CAL_CACHE.parent.mkdir(parents=True, exist_ok=True)
        CAL_CACHE.write_text(json.dumps(disk, ensure_ascii=False))
        return evs, at, None
    except BaseException as e:               # calendar_events raises SystemExit on token problems
        if isinstance(e, KeyboardInterrupt):
            raise
        try:
            d = json.loads(CAL_CACHE.read_text()).get(key) or {}
        except (OSError, ValueError):
            d = {}
        return d.get("events") or [], d.get("at"), f"calendar read failed: {str(e)[:120]}"


# ---------------------------------------------------------------- engagement files
def _entries(eng):
    return A._entries(A.read(A.ENG / eng / "STATUS.md"))


def _entry_head(e):
    return e.split("\n", 1)[0].lstrip("# ").strip()


def _bullets(e):
    out = []
    for ln in e.split("\n")[1:]:
        if ln.startswith("<!--"):
            continue
        m = re.match(r"^\s*[-*]\s+(.*)", ln)
        if m:
            out.append(re.sub(r"\*\*", "", m.group(1)).strip())
        elif ln.strip() and out:
            out[-1] += " " + ln.strip()
    return out


BY_RX = re.compile(r"\bby:?\s*(\d{4}-\d{2}-\d{2})", re.I)
OWNER_RX = re.compile(r"\bowner:?\s*([^-—;(.]+)", re.I)


def split_actions(text, src_date=""):
    """'Next action:' text -> [{what, owner, by, date}]. Several actions are joined by '. ' in one line."""
    t = re.sub(r"^(next actions?|next):\s*", "", text.strip(), flags=re.I).strip()
    parts = re.split(r"(?<=[.)])\s+(?=[A-Z])", t) if len(re.findall(r"owner:", t, re.I)) > 1 else [t]
    out = []
    for p in parts:
        p = p.strip().rstrip(".")
        if not p:
            continue
        o = OWNER_RX.search(p)
        b = BY_RX.search(p)
        what = re.split(r"\s+[-—]\s+owner:", p, flags=re.I)[0].strip()
        owner = o.group(1).strip() if o else ""
        if not owner:
            m = re.match(r"^([A-Z][a-z]+(?:\s*/\s*[A-Z][a-z]+)*)[:,]\s", what)
            owner = m.group(1) if m else ""
        out.append(dict(what=what[:300], owner=owner, by=b.group(1) if b else "", src=src_date))
    return out


def status_info(eng):
    ents = _entries(eng)
    if not ents:
        return None
    first = ents[0]
    actions = []
    for e in ents[:2]:                        # newest entry with a next action wins
        for b in _bullets(e):
            if re.match(r"^next actions?\b", b, re.I):
                actions += split_actions(b, A._entry_date(e))
        if actions:
            break
    bl = _bullets(first)
    blocked = next((re.sub(r"^blocked on:\s*", "", b, flags=re.I) for b in bl if re.match(r"^blocked on", b, re.I)), "")
    stage = next((re.sub(r"^stage:\s*", "", b, flags=re.I).rstrip(".") for b in bl if re.match(r"^stage:", b, re.I)), "")
    return dict(date=A._entry_date(first), head=_entry_head(first), bullets=bl[:12], actions=actions,
                blocked=blocked, stage=stage, auto="autopilot:" in first or "meeting autopilot" in first)


DUE_RX = re.compile(r"\b(?:by|before|due|until|deadline)\b:?\s*~?\s*(\d{4}-\d{2}-\d{2})", re.I)


def pending_artefacts(eng, limit=12):
    t = A.read(A.ENG / eng / "ARTEFACTS.md")
    m = re.search(r"^## Pending.*?\n(.*?)(?=^## |\Z)", t, re.M | re.S)
    if not m:
        return []
    out = []
    for ln in m.group(1).splitlines():
        mm = re.match(r"^\s*[-*]\s+(.*)", ln)
        if mm:
            s = re.sub(r"\*\*|`", "", mm.group(1)).strip()
            d = DUE_RX.findall(s)          # due dates only; "(2026-10-19, promised)" is when it was logged
            out.append(dict(text=s[:280], dates=d))
    return out[:limit]


def _alias(eng):
    return (A.aliases().get(eng) or {}) if isinstance(A.aliases().get(eng), dict) else {}


def eng_label(eng):
    al = _alias(eng)
    titles = [str(t) for t in al.get("titles") or []]
    return titles[0] if titles else eng.replace("-", " ").title()


def active_engagements():
    out = []
    for k, v in A.aliases().items():
        if k.startswith("_") or not isinstance(v, dict) or not (A.ENG / k).is_dir():
            continue
        if str(v.get("status") or "").lower() in CLOSED:
            continue
        out.append(k)
    return out


# ---------------------------------------------------------------- digests (follow-ups owed)
_IRIS_FIRST = None


def iris_first():
    global _IRIS_FIRST
    if _IRIS_FIRST is None:
        try:
            names = A.iris_names()
        except Exception:
            names = ["Ivo", "Jordan", "Vankata", "Steven", "Eric", "Viktor", "Velislav", "Vasil", "Veronika"]
        _IRIS_FIRST = {n.split()[0].lower() for n in names} | {"ivo", "eric", "iris", "iris.ai"}
    return _IRIS_FIRST


def _ours(owner):
    words = re.findall(r"[a-z.]+", (owner or "").lower())
    return any(w in iris_first() for w in words)


def digests():
    """{engagement: [digest meta + actions], newest first} from _autopilot/drafts/*/digest.json."""
    out = {}
    for p in A.DRAFTS.glob("*/digest.json"):
        try:
            d = json.loads(p.read_text())
        except (OSError, ValueError):
            continue
        meta = d.get("meta") or {}
        eng = meta.get("engagement")
        if not eng:
            continue
        acts = [dict(what=a.get("what", ""), owner=a.get("owner", ""), when=a.get("when", ""), type=a.get("type", ""),
                     ours=_ours(a.get("owner")), jordan=bool(a.get("jordan_owned")))
                for a in d.get("actions") or []]
        out.setdefault(eng, []).append(dict(key=meta.get("key") or p.parent.name, title=meta.get("title", ""),
                                            date=meta.get("date", ""), actions=acts))
    for v in out.values():
        v.sort(key=lambda x: x["key"], reverse=True)
    return out


# ---------------------------------------------------------------- CRM cache matching
def _match_keys(eng):
    al = _alias(eng)
    keys = {_norm(eng)} | {_norm(t) for t in al.get("titles") or [] if len(_norm(t)) >= 4}
    for d in al.get("domains") or []:
        base = _norm(str(d).split(".")[0])
        if len(base) >= 4:
            keys.add(base)
    return {k for k in keys if len(k) >= 3}


def _hits(text, keys):
    n = _norm(text)
    return any(n.startswith(k) or (len(k) >= 5 and k in n) for k in keys)


def crm_for(eng, crm):
    keys = _match_keys(eng)
    deals = [d for d in ((crm.get("hubspot") or {}).get("deals") or []) if _hits((d.get("name") or "").split(" - ")[0], keys)]
    order = {"closed lost": 2, "closed won": 1}
    deals.sort(key=lambda d: (order.get((d.get("stage") or "").lower(), 0), -(int(re.sub(r"\D", "", d.get("modified") or "0") or 0))))
    tasks = []
    for t in (crm.get("asana") or {}).get("tasks") or []:
        name = re.sub(r"^\[PIPELINE\]\s*", "", t.get("name") or "")
        if _hits(t.get("section") or "", keys) or _hits(name, keys) or _hits(name.split(":")[0], keys):
            tasks.append(t)
    tasks.sort(key=lambda t: (not (t.get("name") or "").startswith("[PIPELINE]"), t.get("due_on") or "9999"))
    return deals[:3], tasks[:12]


# ---------------------------------------------------------------- meetings
def is_client(ev, eng):
    return bool(eng) or (A.select(ev) and bool(A.external_attendees(ev)))


def brief_for(key, ev, eng, st):
    m = st["meetings"].get(key) or {}
    b = (m.get("phases") or {}).get("brief") or {}
    if b.get("path") and Path(b["path"]).exists():
        return dict(state="ready", url=f"/brief/{key}" if key in st["meetings"] else "/brief-file?path=" + b["path"], path=b["path"])
    s = A.parse_time(ev["start"])
    y, w, _ = s.isocalendar()
    name = f"{s:%Y-%m-%d}_{A.slug((eng + '-' if eng else '') + ev['title'], 50)}.md"
    p = A.ATLAS / "briefs" / str(y) / f"W{w:02d}" / name
    if p.exists():
        return dict(state="ready", url="/brief-file?path=" + str(p), path=str(p))
    if b.get("status"):
        return dict(state=b["status"].split(" ")[0], note=b["status"])
    if not eng:
        return dict(state="none", note="no engagement match, no auto brief")
    at = s - dt.timedelta(minutes=A.cfg()["brief_lead_min"])
    return dict(state="planned" if _now() < at else "missing", at=at.isoformat())


def meeting_row(ev, st, digs, crm):
    eng, _ = A.match_engagement(ev)
    key = A.meeting_key(ev)
    client = is_client(ev, eng)
    m = st["meetings"].get(key) or {}
    ph = m.get("phases") or {}
    ext = A.external_attendees(ev)
    row = dict(key=key, title=ev["title"], start=ev["start"], end=ev["end"], link=ev.get("link", ""),
               cal=ev.get("html_link", ""), client=client, engagement=eng, eng_label=eng_label(eng) if eng else "",
               external=[a["name"] or a["email"] for a in ext][:8], n_attendees=len(ev["attendees"]),
               live=(ph.get("live") or {}).get("status"), digest=(ph.get("digest") or {}).get("status"))
    if client:
        row["brief"] = brief_for(key, ev, eng, st)
        if not eng:                           # unmatched prospect: try HubSpot by company name in the title
            t = _norm(ev["title"])
            row["deals"] = [d for d in (crm.get("hubspot") or {}).get("deals") or []
                            if len(_norm((d.get("name") or "").split(" - ")[0])) >= 5
                            and _norm(" ".join((d.get("name") or "").split(" - ")[0].split()[:2])) in t][:2]
        own = next((d for d in digs.get(eng or "", []) if d["key"] == key), None)
        prev = next((d for d in digs.get(eng or "", []) if d["key"] < key), None)
        row["followups"] = own or prev       # this call's digest once it exists, else the previous call's
        row["followups_from"] = "this call" if own else ("last call" if prev else "")
    return row


# ---------------------------------------------------------------- today
def due_items(engs, st_by_eng, crm, today):
    """Next actions / pending artefacts / Asana tasks due today or overdue up to 14 days back."""
    lo = (today - dt.timedelta(days=14)).isoformat()
    t = today.isoformat()
    out = []
    for eng in engs:
        si = st_by_eng.get(eng)
        for a in (si or {}).get("actions") or []:
            if a["by"] and lo <= a["by"] <= t:
                out.append(dict(src="STATUS", eng=eng, eng_label=eng_label(eng), what=a["what"], owner=a["owner"],
                                due=a["by"], ivo="ivo" in a["owner"].lower() or not a["owner"]))
        for p in pending_artefacts(eng):
            ds = [d for d in p["dates"] if lo <= d <= t]
            if ds:
                out.append(dict(src="ARTEFACTS", eng=eng, eng_label=eng_label(eng), what=p["text"], owner="",
                                due=max(ds), ivo=True))
    for task in (crm.get("asana") or {}).get("tasks") or []:
        d = task.get("due_on") or ""
        if d and lo <= d <= t and not (task.get("name") or "").startswith("[PIPELINE]"):
            eng = next((e for e in engs if _hits(task.get("section") or "", _match_keys(e)) or _hits(task.get("name") or "", _match_keys(e))), "")
            out.append(dict(src="Asana", eng=eng, eng_label=eng_label(eng) if eng else task.get("section", ""),
                            what=task.get("name", ""), owner=task.get("assignee", ""), due=d, url=task.get("url", ""),
                            ivo="ivo" in (task.get("assignee") or "").lower()))
    out.sort(key=lambda x: (not x["ivo"], x["due"] != t, x["due"]))
    return out


def time_cost():
    try:
        d = json.loads(TIME_FILE.read_text())
    except (OSError, ValueError):
        return None
    return d if isinstance(d, dict) else None


def crm_meta(crm):
    out = {}
    for src, key in (("hubspot", "deals"), ("asana", "tasks")):
        s = crm.get(src) or {}
        out[src] = dict(as_of=s.get("as_of"), n=len(s.get(key) or []), error=s.get("error"))
    out["last_run"] = crm.get("last_run")
    out["running"] = bool(CRM.running())
    out["spend"] = round(CRM.crm_spend(), 3)
    out["auto"] = CRM.due_auto() or "due"
    return out


def queue_view(it):
    import approvals_app as AP_
    t = it.get("target") or {}
    return dict(id=it["id"], kind=it["kind"], source=it["source"], engagement=it["engagement"], title=it["title"],
                body=it["body"], status=it["status"], created=it["created"], target=t,
                sources=it.get("sources") or [], history=(it.get("history") or [])[-4:], sent_link=it.get("sent_link", ""),
                open_url=AP_.open_url(it), executable=it["kind"] in AP_.X.EXECUTABLE,
                can_undo=it["status"] == "done" and AP_.undo_argv(it) is not None)


def snapshot(week_offset=0):
    now = _now()
    today = now.date()
    monday = week_start(week_offset)
    evs, cal_at, cal_err = calendar_week(monday)
    st = A.load_state()
    digs = digests()
    crm = CRM.load()
    rows = [meeting_row(e, st, digs, crm) for e in evs]

    pend = [queue_view(i) for i in Q.list_items("pending", visible_only=True)]   # quiet hours: held items surface at 08:00
    recent_cut = (now - dt.timedelta(days=3)).isoformat()
    undoable = [queue_view(i) for i in Q.list_items("done") if i.get("created", "") >= recent_cut]
    undoable = [i for i in undoable if i["can_undo"]]

    engs = set(r["engagement"] for r in rows if r.get("engagement"))
    act = active_engagements()
    st_by_eng = {e: status_info(e) for e in set(act) | engs}
    eng_data = {}
    for e in engs | {i["engagement"] for i in pend if (A.ENG / i["engagement"]).is_dir()}:
        deals, tasks = crm_for(e, crm)
        eng_data[e] = dict(name=e, label=eng_label(e), status=st_by_eng.get(e) or status_info(e),
                           pending=pending_artefacts(e), deals=deals, tasks=tasks,
                           alias_status=_alias(e).get("status", ""))

    days = []
    for i in range(5):
        d = monday + dt.timedelta(days=i)
        days.append(dict(date=d.isoformat(), events=[r for r in rows if r["start"][:10] == d.isoformat()]))

    upcoming = [r for r in rows if r["end"] > now.isoformat() and r["start"][:10] == today.isoformat()]
    cur = next((r for r in upcoming if r["start"] <= now.isoformat()), None)
    nxt = [r for r in upcoming if r["start"] > now.isoformat()]
    nxt_client = next((r for r in nxt if r["client"]), None)
    return dict(now=now.isoformat(timespec="seconds"), today=today.isoformat(), week=dict(monday=monday.isoformat(), offset=week_offset, days=days),
                cal=dict(at=cal_at, error=cal_err),
                today_strip=dict(current=cur, next=nxt[0] if nxt else None, next_client=nxt_client,
                                 due=due_items(act, st_by_eng, crm, today), left_today=len(nxt)),
                drafts=pend, undoable=undoable, engagements=eng_data, crm=crm_meta(crm), time_cost=time_cost(),
                spend=round(A.day_spend(), 3), caps=dict(soft=A.cfg()["soft_cap_usd"], hard=A.cfg()["hard_cap_usd"]))
