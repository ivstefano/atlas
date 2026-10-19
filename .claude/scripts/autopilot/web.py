#!/usr/bin/env python3
"""Atlas command center: 127.0.0.1:8095. Today strip, week calendar, client meeting cards, approvals inline.

Replaces the old autopilot log viewer (now at /admin) and the front page of the approvals inbox (:8096 redirects
here; its API stays there too). Kept routes, used by notifications and the autopilot: /brief/<key>,
/brief-file?path=, /live/<key>, /api/live/<key>, /digest/<key>, /health.

Read-only over atlas/_autopilot, briefs, autopilot state and engagements/*; the only writes go through the
approval queue API (approvals_app.make_router, same X-Approvals/Host/Origin guard, bound to this port) and the
CRM refresh (crm_refresh.py, spend-capped). Nothing sends without a click.

    CC_PORT=8097 CC_AUTO_REFRESH=0 <venv python> web.py      (test copy; launchd runs it on 8095)
"""
import datetime as dt
import html
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))
import meeting_autopilot as A  # noqa: E402
import approvals_app as APR  # noqa: E402
import approval_queue as Q  # noqa: E402
import crm_refresh as CRM  # noqa: E402
import cc_data  # noqa: E402

PORT = int(os.environ.get("CC_PORT", str(A.PORT)))
AUTO_REFRESH = os.environ.get("CC_AUTO_REFRESH", "1" if PORT == A.PORT else "0") == "1"
STATIC = HERE / "static"
SCRIPT = f"{A.PY} {Path(A.__file__).resolve()}"

app = FastAPI(title="Atlas", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")
app.include_router(APR.make_router(PORT))
guard = APR.make_guard(PORT)


@app.middleware("http")
async def _no_cache(request, call_next):
    resp = await call_next(request)
    p = request.url.path
    if p == "/" or p.startswith("/api/") or p.endswith((".js", ".css", ".html")):
        resp.headers["Cache-Control"] = "no-cache"
    return resp


# ---------------------------------------------------------------- command center
@app.get("/health")
def health():
    return {"ok": True}


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/cc")
def api_cc(week: int = 0):
    return JSONResponse(cc_data.snapshot(max(-4, min(4, week))))


def _spawn_refresh(reason):
    if CRM.running():
        return dict(ok=False, error="already running")
    subprocess.Popen([A.PY, str(Path(CRM.__file__).resolve()), "auto" if reason == "auto" else "run"],
                     cwd=str(A.HOME), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    return dict(ok=True, started=True)


@app.post("/api/refresh")
async def api_refresh(req: Request):
    guard(req)
    if A.day_spend() >= A.cfg()["hard_cap_usd"]:
        return dict(ok=False, error="daily spend cap reached")
    cc_data._cal.clear()                     # the next /api/cc re-reads the calendar too
    return _spawn_refresh("manual")


def _auto_loop():
    while True:
        time.sleep(120)
        try:
            if not CRM.due_auto():
                _spawn_refresh("auto")
        except Exception as e:
            A.log(f"command center auto refresh: {type(e).__name__}: {e}")


if AUTO_REFRESH:
    threading.Thread(target=_auto_loop, daemon=True).start()


# ---------------------------------------------------------------- doc pages (brief, live, admin)
MD_JS = r"""
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function inl(s){s=esc(s);return s.replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>')
 .replace(/(^|[^*])\*([^*\s][^*]*)\*/g,'$1<i>$2</i>').replace(/_([^_\s][^_]*)_(?=\s|$|[.,])/g,'<i>$1</i>')
 .replace(/\[([^\]]+)\]\((https?:[^)\s]+)\)/g,'<a href="$2">$1</a>').replace(/(^|[\s(])(https?:\/\/[^\s<)]+)/g,'$1<a href="$2">$2</a>')}
function md(src){const L=src.replace(/<!--[\s\S]*?-->/g,'').split('\n');let o=[],i=0,list=null;
 const close=()=>{if(list){o.push('</'+list+'>');list=null}};
 while(i<L.length){let l=L[i];
  if(/^```/.test(l)){close();let b=[];i++;while(i<L.length&&!/^```/.test(L[i]))b.push(esc(L[i++]));o.push('<pre>'+b.join('\n')+'</pre>');i++;continue}
  let h=l.match(/^(#{1,4})\s+(.*)/);if(h){close();o.push('<h'+h[1].length+'>'+inl(h[2])+'</h'+h[1].length+'>');i++;continue}
  if(/^\|/.test(l)){close();let rows=[];while(i<L.length&&/^\|/.test(L[i]))rows.push(L[i++]);
   o.push('<table>'+rows.filter(r=>!/^\|[\s:|-]+\|$/.test(r)).map((r,j)=>'<tr>'+r.replace(/^\||\|$/g,'').split('|').map(c=>(j?'<td>':'<th>')+inl(c.trim())+(j?'</td>':'</th>')).join('')+'</tr>').join('')+'</table>');continue}
  let li=l.match(/^\s*(?:[-*]|\d+\.)\s+(.*)/);if(li){const t=/^\s*\d+\./.test(l)?'ol':'ul';if(list!==t){close();o.push('<'+t+'>');list=t}o.push('<li>'+inl(li[1])+'</li>');i++;continue}
  if(/^---+$/.test(l.trim())){close();o.push('<hr>');i++;continue}
  if(!l.trim()){close();i++;continue}
  if(/^>/.test(l)){close();o.push('<p class="muted">'+inl(l.replace(/^>\s?/,''))+'</p>');i++;continue}
  close();o.push('<p>'+inl(l)+'</p>');i++}
 close();return o.join('\n')}
"""


def page(title, body, script=""):
    return HTMLResponse(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/static/fonts.css"><link rel="stylesheet" href="/static/colors_and_type.css">
<link rel="stylesheet" href="/static/cc.css"></head><body class="doc">
<nav class="docnav"><a href="/">Command center</a><a href="/admin">Admin</a></nav><main class="docmain">{body}</main>
<script>{MD_JS}{script}</script></body></html>""")


def md_page(title, text, extra=""):
    return page(title, f'{extra}<article id="md"></article><pre id="raw" hidden>{html.escape(text)}</pre>',
                "document.getElementById('md').innerHTML=md(document.getElementById('raw').textContent);")


def all_meetings():
    """Real meetings plus dry-run replays (marked), so dry-run output can be reviewed in the same viewer."""
    out = dict(A.load_state()["meetings"])
    try:
        dry = json.loads((A.DRY / "autopilot.json").read_text())["meetings"]
        out.update({k: {**v, "dry": True} for k, v in dry.items() if k not in out})
    except (OSError, ValueError, KeyError):
        pass
    return out


def _meeting(key):
    m = all_meetings().get(key)
    if not m:
        raise HTTPException(404, "unknown meeting")
    return m


@app.get("/brief/{key}", response_class=HTMLResponse)
def brief(key: str):
    m = _meeting(key)
    p = (m.get("phases", {}).get("brief") or {}).get("path")
    if not p or not Path(p).exists():
        return page("Brief", "<p>No brief yet.</p>")
    return md_page(m["event"]["title"], Path(p).read_text(),
                   f'<p class="muted"><a href="/live/{key}">Live sidekick</a> <span class="mono">{html.escape(p)}</span></p>')


@app.get("/brief-file", response_class=HTMLResponse)
def brief_file(path: str):
    p = Path(path).resolve()
    if not (str(p).startswith(str(A.ATLAS / "briefs")) or str(p).startswith(str(A.AP))) or p.suffix != ".md" or not p.exists():
        raise HTTPException(404, "not a brief")
    return md_page(p.name, p.read_text())


def _live_file(key):
    for p in (A.LIVE / key / "live.json", A.DRY / key / "live.json"):
        if p.exists():
            return p
    return None


@app.get("/api/live/{key}")
def api_live(key: str):
    p = _live_file(key)
    return JSONResponse(json.loads(p.read_text()) if p else {"status": "not started"})


LIVE_JS = """
const KEY=%s;
function h(s){return esc(String(s??''))}
async function load(){const r=await fetch('/api/live/'+KEY);const L=await r.json();
 document.getElementById('st').textContent=(L.status||'')+' | '+(L.n_lines||0)+' lines | updated '+(L.updated||'-').slice(11,16)+' | Tactiq lags 1-2 min';
 document.getElementById('tail').innerHTML=(L.tail||[]).slice(-22).map(x=>'<div>'+h(x)+'</div>').join('')+(L.unstable?'<div class="unstable">'+h(L.unstable)+' (still arriving)</div>':'');
 document.getElementById('q').innerHTML=(L.questions||[]).slice().reverse().map(q=>'<div class="card"><b>'+h(q.who)+'</b> <span class="muted">'+h(q.ts)+'</span><br>'+h(q.question)+
  (q.answer?'<p>'+h(q.answer)+'</p>':'<p class="muted">'+h(q.skipped||'answer pending...')+'</p>')+
  (q.pocket_line?'<p><i>Pocket line: '+h(q.pocket_line)+'</i></p>':'')+
  ((q.flags||[]).length?'<p class="flag">'+q.flags.map(h).join('<br>')+'</p>':'')+
  ((q.sources||[]).length?'<p class="muted">Sources: '+q.sources.map(s=>'['+s.n+'] '+h(s.title)).join(', ')+'</p>':(q.answer&&!q.cognion?'<p class="muted">No Cognion sources</p>':''))+'</div>').join('')||'<p class="muted">none yet</p>';
 document.getElementById('c').innerHTML=(L.commitments||[]).map(c=>'<li><b>'+h(c.who)+'</b>: '+h(c.what)+' <span class="muted">('+h(c.when)+', '+h(c.ts)+')</span></li>').join('')||'<li class="muted">none yet</li>';
 document.getElementById('n').innerHTML=(L.next_questions||[]).map(x=>'<li>'+h(x)+'</li>').join('')||'<li class="muted">none yet</li>';}
load();setInterval(load,10000);
"""


@app.get("/live/{key}", response_class=HTMLResponse)
def live(key: str):
    m = _meeting(key)
    return page("Live: " + m["event"]["title"], f"""<h1>{html.escape(m['event']['title'])}</h1>
<p class="muted" id="st"></p><p class="muted"><a href="/brief/{key}">Brief</a></p>
<div class="grid2"><div><h2>Client questions, suggested answers</h2><div id="q"></div></div>
<div><h2>Next questions to ask</h2><ul id="n"></ul><h2>Commitments heard</h2><ul id="c"></ul>
<h2>Transcript tail</h2><div class="tail" id="tail"></div></div></div>""", LIVE_JS % json.dumps(key))


@app.get("/digest/{key}")
def digest(key: str):
    """Drafts are reviewed inline on the command center now."""
    return RedirectResponse("/#drafts")


def _tail(p, n=40):
    try:
        return Path(p).read_text(errors="ignore").splitlines()[-n:]
    except OSError:
        return []


@app.get("/admin", response_class=HTMLResponse)
def admin():
    e = html.escape
    st = A.load_state()
    rows = []
    for k, m in sorted(all_meetings().items(), reverse=True):
        ph = m.get("phases", {})
        ev = m.get("event") or {}
        bits = [f'<a href="/brief/{e(k)}">brief</a>' if "path" in (ph.get("brief") or {}) else "brief: -",
                f'<a href="/live/{e(k)}">live</a>']
        phs = ", ".join(f"{p}: {v.get('status')}" for p, v in ph.items())
        rows.append(f"<tr><td class='mono'>{e(k[:16].replace('_', ' '))}{' (dry-run)' if m.get('dry') else ''}</td><td>{e(ev.get('title', k))}</td>"
                    f"<td>{e(m.get('engagement') or 'unmatched')}</td><td>{' | '.join(bits)}</td><td class='muted'>{e(phs)}</td></tr>")
    mb = "".join(f'<li><a href="/brief-file?path={e(p)}">{e(d)}</a></li>' for d, p in sorted(st.get("morning", {}).items(), reverse=True)[:7])
    c = CRM.load()
    lr = c.get("last_run") or {}
    crm = (f"<p>Last run {e(str(lr.get('at', '-')))}, {'ok' if lr.get('ok') else 'failed: ' + e(str(lr.get('error')))}"
           f", ${lr.get('usd', 0):.3f}, {lr.get('secs', '-')}s. CRM spend today ${CRM.crm_spend():.3f} of ${CRM.conf()['crm_cap_usd']:.2f}."
           f" Auto: {e(CRM.due_auto() or 'due')}, every {CRM.conf()['crm_refresh_min']} min, hours {CRM.conf()['crm_hours']}.</p>")
    hist = []
    for it in Q.list_items(["sent", "done", "rejected"])[:25]:
        last = (it.get("history") or [{}])[-1]
        hist.append(f"<tr><td class='mono'>{e(it['created'][:16].replace('T', ' '))}</td><td>{e(it['status'])}</td><td>{e(it['kind'])}</td>"
                    f"<td>{e(it['engagement'])}</td><td>{e(it['title'][:80])}</td><td class='muted'>{e(str(last.get('action', '')))} {e(str(last.get('note', ''))[:80])}</td></tr>")
    log = "\n".join(e(x) for x in _tail(A.LOGS / "autopilot.log", 50))
    spend = A.day_spend()
    return page("Admin", f"""<h1>Admin</h1><p class="muted">Spend today ${spend:.3f} (soft cap ${A.cfg()['soft_cap_usd']:.2f}, hard cap ${A.cfg()['hard_cap_usd']:.2f}). Nothing here sends anything.</p>
<h2>Meetings (autopilot state, incl. dry-run)</h2>
<table><tr><th>When</th><th>Meeting</th><th>Engagement</th><th>Open</th><th>Phases</th></tr>{''.join(rows) or '<tr><td colspan=5>No meetings yet</td></tr>'}</table>
<h2>CRM snapshot</h2>{crm}
<h2>Morning briefs</h2><ul>{mb or '<li>none yet</li>'}</ul>
<h2>Queue history</h2><table><tr><th>Created</th><th>Status</th><th>Kind</th><th>Engagement</th><th>Title</th><th>Last</th></tr>{''.join(hist)}</table>
<p class="muted"><a href="http://127.0.0.1:8096/legacy">Old approvals inbox</a></p>
<h2>Commands</h2><pre>{SCRIPT} status
{SCRIPT} apply &lt;key&gt;        # fallback STATUS write
{SCRIPT} undo &lt;key|engagement&gt;
{SCRIPT} gmail-draft &lt;key&gt;  # creates a Gmail DRAFT, never sends
{SCRIPT} uninstall
{A.PY} {Path(CRM.__file__).resolve()} show|run</pre>
<h2>Autopilot log</h2><pre class="log">{log}</pre>""")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")
