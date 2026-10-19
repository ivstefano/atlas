#!/usr/bin/env python3
"""Approvals inbox: http://127.0.0.1:8096. One place to review every autopilot draft.

Reads/writes the queue in approval_queue.py. Executors (approval_executors.py) run ONLY when Ivo
clicks "Approve & send" (or "Approve selected"). Bound to 127.0.0.1; every POST must carry the
X-Approvals header (a cross-site form cannot set it, and no CORS is served, so a fetch from another page
is blocked at preflight), its Host must be this inbox (stops DNS rebinding) and its Origin, when sent, must
be this inbox. Undo additionally requires the Origin header, so it only works from the inbox page itself.

Undo (status_entry items the autopilot auto-wrote): runs target.undo_cmd, which must be exactly
"<autopilot python> meeting_autopilot.py undo <target.undo_id>" (checked, never passed to a shell),
then marks the item rejected.

    approvals_app.py            (launchd: ai.iris.atlas.approvals, KeepAlive)
"""
import html
import json
import os
import re
import shlex
import subprocess
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import approval_queue as Q  # noqa: E402
import approval_executors as X  # noqa: E402

from fastapi import APIRouter, FastAPI, HTTPException, Request  # noqa: E402
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse  # noqa: E402

FONTS = Path.home() / "Documents" / "Cognion" / "proto" / "static" / "fonts"
ENG = Path.home() / "Documents" / "engagements"
PORT = int(os.environ.get("APPROVALS_PORT", "8096"))
HOSTS = {f"127.0.0.1:{PORT}", f"localhost:{PORT}"}
ORIGINS = {f"http://{h}" for h in HOSTS}
# The command center (autopilot/web.py, :8095) is the front page now; this port keeps the API and redirects "/".
COMMAND_CENTER = os.environ.get("COMMAND_CENTER_URL", "http://127.0.0.1:8095")
AUTOPILOT = Path(__file__).resolve().parent / "meeting_autopilot.py"
AUTOPILOT_PY = "/Users/iris/Documents/Cognion/atlas/.venv/bin/python"   # = meeting_autopilot.PY
app = FastAPI(title="Approvals")


def make_guard(port):
    """POST guard bound to one local port (the inbox, or the command center that embeds this API)."""
    hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
    origins = {f"http://{h}" for h in hosts}

    def guard(req: Request, need_origin=False):
        if req.headers.get("x-approvals") != "1":
            raise HTTPException(403, "missing X-Approvals header")
        if req.headers.get("host") not in hosts:
            raise HTTPException(403, "wrong Host")
        origin = req.headers.get("origin")
        if (origin is None and need_origin) or (origin is not None and origin not in origins):
            raise HTTPException(403, "request not from the inbox origin")
        if req.headers.get("sec-fetch-site") not in (None, "same-origin"):
            raise HTTPException(403, "cross-site request")
    return guard


_guard = make_guard(PORT)


def undo_argv(it):
    """The undo command for an auto-written status_entry, or None. Only the exact known form is accepted."""
    t = it.get("target") or {}
    key = t.get("undo_id") or ""
    if it.get("kind") != "status_entry" or not re.fullmatch(r"[\w.:-]+", key):
        return None
    try:
        argv = shlex.split(t.get("undo_cmd") or "")
    except ValueError:
        return None
    want = [AUTOPILOT_PY, str(AUTOPILOT), "undo", key]
    if len(argv) != 4 or argv[0] != AUTOPILOT_PY or Path(argv[1]).resolve() != AUTOPILOT or argv[2:] != want[2:]:
        return None
    return want


def open_url(it):
    t = it.get("target") or {}
    if t.get("permalink"):
        return t["permalink"]
    if t.get("prefill_url") or t.get("form_url"):
        return t.get("prefill_url") or t.get("form_url")
    if it["kind"] in ("email_draft", "gmail_draft") and t.get("to"):
        q = dict(view="cm", to=X.addr(t.get("to")), su=t.get("subject", ""), body=it.get("body", ""))
        if t.get("cc"):
            q["cc"] = X.addr(t["cc"])
        return "https://mail.google.com/mail/?" + urllib.parse.urlencode(q)
    if it["kind"] == "asana":
        return t.get("task_url") or X.ASANA_PROJECT_URL
    if it["kind"] == "slack_post":
        return f"https://irisai.slack.com/archives/{t.get('channel') or X.DEFAULT_CHANNEL}"
    return ""


@app.get("/fonts/{name}")
def fonts(name: str):
    p = (FONTS / name).resolve()
    if p.parent != FONTS.resolve() or not p.exists():
        raise HTTPException(404)
    return FileResponse(p)


def make_router(port):
    """The queue API, guarded for one local port. Mounted by this inbox (:8096) and by the command center (:8095)."""
    guard = make_guard(port)
    r = APIRouter()

    @r.get("/api/items")
    def items(status: str = None):
        return Q.list_items(status.split(",") if status else None)

    @r.post("/api/items/{item_id}/save")
    async def save(item_id: str, req: Request):
        guard(req)
        data = await req.json()
        return Q.update(item_id, "edited", body=data["body"])

    @r.post("/api/items/{item_id}/approve")
    async def approve(item_id: str, req: Request):
        guard(req)
        data = await req.json()
        return JSONResponse(_approve(item_id, data.get("body")))

    @r.post("/api/batch/approve")
    async def batch(req: Request):
        guard(req)
        data = await req.json()
        return [dict(id=i, **_approve(i)) for i in data.get("ids", [])]

    @r.post("/api/items/{item_id}/undo")
    async def undo(item_id: str, req: Request):
        guard(req, need_origin=True)
        return JSONResponse(_undo(item_id))

    @r.post("/api/items/{item_id}/{action}")
    async def act(item_id: str, action: str, req: Request):
        guard(req)
        return _act(item_id, action)
    return r


def _approve(item_id, body=None):
    it = Q.get(item_id)
    if not it:
        raise HTTPException(404)
    if it["status"] != "pending":
        return dict(ok=False, error=f"item is {it['status']}")
    if it["kind"] not in X.EXECUTABLE:
        return dict(ok=False, error=f"no executor for {it['kind']}: use Copy / Open, then Mark done")
    if body is not None and body != it["body"]:
        it = Q.update(item_id, "edited", body=body)
    Q.update(item_id, "approved", status="approved")
    try:
        res = X.execute(it)
    except Exception as e:
        Q.update(item_id, "send_failed", status="pending", note=str(e)[:300])
        return dict(ok=False, error=str(e)[:300])
    Q.update(item_id, "sent", status="sent", note=res["result"], sent_link=res.get("link", ""))
    return dict(ok=True, **res)


def _undo(item_id):
    it = Q.get(item_id)
    if not it:
        raise HTTPException(404)
    argv = undo_argv(it)
    if not argv:
        return dict(ok=False, error="no valid undo command on this item")
    if it["status"] != "done":
        return dict(ok=False, error=f"item is {it['status']}")
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=180, cwd=str(Path.home()))
    except subprocess.TimeoutExpired:
        Q.update(item_id, "undo_failed", note="timed out")
        return dict(ok=False, error="undo timed out")
    if r.returncode != 0:
        err = (r.stderr.strip() or r.stdout.strip())[-300:]
        Q.update(item_id, "undo_failed", note=err)
        return dict(ok=False, error=err)
    out = r.stdout.strip()[-300:]
    Q.update(item_id, "undone from inbox", status="rejected", note=out)
    return dict(ok=True, result=out)


def _act(item_id, action):
    it = Q.get(item_id)
    if not it:
        raise HTTPException(404)
    if action == "reject":
        return Q.update(item_id, "rejected", status="rejected")
    if action == "done":
        return Q.update(item_id, "marked done", status="done")
    if action == "reopen":
        return Q.update(item_id, "reopened", status="pending")
    if action == "open-path":
        p = (it.get("target") or {}).get("path")
        if p:
            p = Path(p) if Path(p).is_absolute() else ENG / p
            subprocess.Popen(["/usr/bin/open", str(p)])
            return dict(ok=True)
        return dict(ok=False)
    raise HTTPException(400, "unknown action")


app.include_router(make_router(PORT))


def _card(it):
    e = html.escape
    t = it.get("target") or {}
    tgt = (f"#{'active-engagements' if (t.get('channel') or X.DEFAULT_CHANNEL) == X.DEFAULT_CHANNEL else t.get('channel')}"
           + (" thread" if t.get("thread_ts") else "")) if it["kind"].startswith("slack") else \
        (X.addr(t.get("to")) or t.get("path") or t.get("form_url") or "")
    srcs = "".join(
        f'<li><a href="{e(s.get("path_or_url", ""))}" target="_blank">{e(s.get("label", ""))}</a></li>'
        if str(s.get("path_or_url", "")).startswith("http") else
        f'<li title="{e(str(s.get("path_or_url", "")))}">{e(s.get("label", ""))}</li>'
        for s in it.get("sources") or [])
    url = open_url(it)
    can = it["kind"] in X.EXECUTABLE and it["status"] == "pending"
    can_undo = it["status"] == "done" and undo_argv(it) is not None
    hist = " · ".join(f"{h['ts'][5:16].replace('T', ' ')} {h['action']}" + (f" ({e(h['note'])})" if h.get("note") else "")
                      for h in it.get("history", [])[-4:])
    sent = f'<a href="{e(it["sent_link"])}" target="_blank">sent link</a>' if it.get("sent_link") else ""
    label = {"slack_post": "Approve &amp; post", "slack_thread_reply": "Approve &amp; reply in thread",
             "gmail_draft": "Approve &amp; create Gmail draft", "status_entry": "Approve &amp; write STATUS",
             "asana": "Approve &amp; apply in Asana"}.get(it["kind"], "")
    return f"""
<div class="card {e(it['status'])}" data-id="{e(it['id'])}">
  <div class="meta">
    {'<input type="checkbox" class="sel">' if can else ''}
    <span class="pill">{e(it['source'])}</span><span class="pill k">{e(it['kind'])}</span>
    <b>{e(it['title'])}</b>
    <span class="tgt">{e(tgt)}</span>
    <span class="when">{e(it['created'][:16].replace('T', ' '))}</span>
  </div>
  <textarea {'readonly' if it['status'] != 'pending' else ''}>{e(it['body'])}</textarea>
  <div class="row">
    {f'<button class="go" onclick="approve(this)">{label}</button>' if can else ''}
    <button onclick="copyBody(this)">Copy</button>
    {f'<a class="btn" href="{e(url)}" target="_blank">Open target</a>' if url else ''}
    {'<button onclick="act(this,&quot;open-path&quot;)">Open file</button>' if t.get('path') else ''}
    {'<button class="no" onclick="undo(this)">Undo write</button>' if can_undo else ''}
    {'<button onclick="save(this)">Save edit</button><button onclick="act(this,&quot;done&quot;)">Mark done</button><button class="no" onclick="act(this,&quot;reject&quot;)">Reject</button>' if it['status'] == 'pending' else '<button onclick="act(this,&quot;reopen&quot;)">Reopen</button>'}
    <span class="status">{e(it['status'])} {sent}</span>
  </div>
  {f'<ul class="srcs">{srcs}</ul>' if srcs else ''}
  <div class="hist">{hist}</div>
</div>"""


@app.get("/")
def index():
    """Front page moved to the command center; the old inbox stays reachable at /legacy."""
    return RedirectResponse(COMMAND_CENTER + "/#drafts")


@app.get("/legacy", response_class=HTMLResponse)
def legacy():
    pend = Q.list_items("pending", visible_only=True)
    held = Q.held_count()
    groups = {}
    for it in pend:
        groups.setdefault(it["engagement"], []).append(it)
    order = sorted(groups, key=lambda g: max(i["created"] for i in groups[g]), reverse=True)
    body = "".join(f'<h2>{html.escape(g)} <small>{len(groups[g])}</small></h2>' + "".join(_card(i) for i in groups[g])
                   for g in order) or "<p class='empty'>Nothing waiting.</p>"
    done = Q.list_items(["sent", "done", "rejected"], visible_only=True)[:25]
    recent = "".join(_card(i) for i in done) or "<p class='empty'>Nothing yet.</p>"
    held_txt = f'<span style="color:var(--mute);font-size:12px">{held} more surface at 08:00 (quiet hours)</span>' if held else ""
    return (PAGE.replace("{{PENDING}}", body).replace("{{RECENT}}", recent).replace("{{N}}", str(len(pend)))
            .replace("{{HELD}}", held_txt))


PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>Approvals ({{N}})</title>
<style>
@font-face{font-family:Saira;src:url(/fonts/Saira-latin-8eed14.woff2) format('woff2');font-weight:100 900}
@font-face{font-family:Poppins;src:url(/fonts/Poppins-latin-350a5a.woff2) format('woff2');font-weight:400}
:root{--ink:#14171f;--mute:#6b7280;--line:#e4e6eb;--bg:#f6f7f9;--acc:#2c4bff;--ok:#0f7b4a;--no:#b42318}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 Poppins,system-ui,sans-serif}
header{position:sticky;top:0;background:#fff;border-bottom:1px solid var(--line);padding:12px 28px;display:flex;gap:16px;align-items:center;z-index:2}
h1{font:600 20px Saira,system-ui;margin:0;letter-spacing:.02em}
h2{font:600 15px Saira,system-ui;margin:28px 0 8px;text-transform:uppercase;letter-spacing:.06em;color:var(--mute)}
h2 small{font-weight:400}
main{max-width:1000px;margin:0 auto;padding:0 28px 80px}
.card{background:#fff;border:1px solid var(--line);border-radius:6px;padding:12px 14px;margin:10px 0}
.card.sent{border-left:3px solid var(--ok)}.card.rejected{opacity:.6}
.meta{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.pill{font-size:11px;border:1px solid var(--line);border-radius:3px;padding:1px 6px;color:var(--mute)}
.pill.k{color:var(--acc);border-color:#cdd5ff}
.tgt,.when{color:var(--mute);font-size:12px}.when{margin-left:auto}
textarea{width:100%;box-sizing:border-box;min-height:180px;margin:8px 0;font:13px/1.45 ui-monospace,Menlo,monospace;border:1px solid var(--line);border-radius:4px;padding:8px;resize:vertical}
.row{display:flex;gap:6px;flex-wrap:wrap;align-items:center}
button,.btn{font:13px Poppins,system-ui;border:1px solid var(--line);background:#fff;border-radius:4px;padding:5px 10px;cursor:pointer;color:var(--ink);text-decoration:none}
button.go{background:var(--acc);color:#fff;border-color:var(--acc)}button.no{color:var(--no)}
.status{margin-left:auto;color:var(--mute);font-size:12px}
.srcs{margin:6px 0 0;padding-left:18px;color:var(--mute);font-size:12px}
.hist{color:var(--mute);font-size:11px;margin-top:4px}
.empty{color:var(--mute)}
#toast{position:fixed;bottom:18px;right:18px;background:var(--ink);color:#fff;padding:8px 12px;border-radius:4px;display:none}
</style></head><body>
<header><h1>Approvals</h1><span>{{N}} pending</span>{{HELD}}
<button class="go" onclick="batch()">Approve selected</button>
<span style="color:var(--mute);font-size:12px">Nothing is sent until you click. Slack posts go out as you.</span></header>
<main>{{PENDING}}<h2>Recent</h2>{{RECENT}}</main><div id="toast"></div>
<script>
const H={'Content-Type':'application/json','X-Approvals':'1'};
const card=b=>b.closest('.card'), id=b=>card(b).dataset.id, txt=b=>card(b).querySelector('textarea').value;
function toast(m){const t=document.getElementById('toast');t.textContent=m;t.style.display='block';setTimeout(()=>t.style.display='none',3500)}
async function post(u,d){const r=await fetch(u,{method:'POST',headers:H,body:JSON.stringify(d||{})});return r.json()}
async function save(b){await post(`/api/items/${id(b)}/save`,{body:txt(b)});toast('Saved')}
async function act(b,a){await post(`/api/items/${id(b)}/${a}`);location.reload()}
async function undo(b){if(!confirm('Revert this STATUS entry? Adds a revert commit in engagements.'))return;
  const r=await post(`/api/items/${id(b)}/undo`);toast(r.ok?r.result:('Failed: '+(r.error||r.detail)));if(r.ok)setTimeout(()=>location.reload(),900)}
function copyBody(b){navigator.clipboard.writeText(txt(b));toast('Copied')}
async function approve(b){if(!confirm(card(b).querySelector('.pill.k').textContent==='asana'?'Apply this change in Asana now?':'Send this now? It goes out as you.'))return;
  const r=await post(`/api/items/${id(b)}/approve`,{body:txt(b)});toast(r.ok?r.result:('Failed: '+r.error));if(r.ok)setTimeout(()=>location.reload(),900)}
async function batch(){const ids=[...document.querySelectorAll('.sel:checked')].map(c=>card(c).dataset.id);
  if(!ids.length)return toast('Nothing selected');if(!confirm(`Send ${ids.length} item(s) now, as you?`))return;
  for(const c of document.querySelectorAll('.sel:checked')){await post(`/api/items/${card(c).dataset.id}/save`,{body:card(c).querySelector('textarea').value})}
  const r=await post('/api/batch/approve',{ids});toast(r.map(x=>x.ok?'sent':'failed').join(', '));setTimeout(()=>location.reload(),1200)}
</script></body></html>"""


if __name__ == "__main__":
    import uvicorn
    from autopilot_common import tcc_guard
    tcc_guard("approvals")
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")
