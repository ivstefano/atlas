#!/usr/bin/env python3
"""Local viewer for the meeting autopilot: briefs, live sidekick, digest drafts.

127.0.0.1:8095 only. Read-only over atlas/_autopilot, atlas/briefs and the autopilot state; it never
sends anything. Started by launchd (ai.iris.atlas.autopilot-web) with the Cognion venv python.
"""
import html
import json
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import meeting_autopilot as A  # noqa: E402

app = FastAPI()
SCRIPT = f"{A.PY} {Path(A.__file__).resolve()}"

CSS = """
body{font:15px/1.5 -apple-system,BlinkMacSystemFont,"Helvetica Neue",sans-serif;margin:0;color:#1d2228;background:#f6f6f3}
main{max-width:980px;margin:0 auto;padding:24px 28px 60px}
a{color:#22568a} h1{font-size:22px;margin:0 0 4px} h2{font-size:16px;margin:26px 0 8px;border-bottom:1px solid #ddd;padding-bottom:4px}
h3{font-size:15px;margin:18px 0 6px} code,pre{font:13px/1.45 ui-monospace,Menlo,monospace;background:#ecebe6;border-radius:3px}
code{padding:1px 4px} pre{padding:10px 12px;white-space:pre-wrap;overflow-x:auto}
table{border-collapse:collapse;margin:8px 0} td,th{border:1px solid #d8d8d2;padding:4px 8px;vertical-align:top;text-align:left}
.muted{color:#6b7177;font-size:13px} .card{background:#fff;border:1px solid #e1e0da;border-radius:6px;padding:12px 16px;margin:10px 0}
.flag{color:#9a3412} .ok{color:#166534} button{font:13px sans-serif;padding:3px 10px;cursor:pointer}
.tail div{font:13px/1.45 ui-monospace,Menlo,monospace;padding:1px 0} .unstable{color:#8a8f94;font-style:italic}
nav{font-size:13px;margin-bottom:14px} nav a{margin-right:12px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px} @media(max-width:860px){.grid{grid-template-columns:1fr}}
"""

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
function copy(id){navigator.clipboard.writeText(document.getElementById(id).innerText);}
"""


def page(title, body, script=""):
    return HTMLResponse(f"""<!doctype html><html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>{CSS}</style></head><body><main><nav><a href="/">Autopilot</a></nav>{body}</main>
<script>{MD_JS}{script}</script></body></html>""")


def md_page(title, text, extra=""):
    return page(title, f'<div id="md"></div>{extra}<pre id="raw" style="display:none">{html.escape(text)}</pre>',
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


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/", response_class=HTMLResponse)
def index():
    st = A.load_state()
    rows = []
    for k, m in sorted(all_meetings().items(), reverse=True):
        ph = m.get("phases", {})
        ev = m.get("event") or {}
        bits = [f'<a href="/brief/{k}">brief</a>' if "path" in (ph.get("brief") or {}) else "brief: -",
                f'<a href="/live/{k}">live</a>', f'<a href="{A.QUEUE_UI}">drafts (inbox)</a>' if ph.get("digest") else "digest: -"]
        phs = ", ".join(f"{p}: {v.get('status')}" for p, v in ph.items())
        rows.append(f"<tr><td>{html.escape(k[:16].replace('_', ' '))}{' (dry-run)' if m.get('dry') else ''}</td><td>{html.escape(ev.get('title', k))}</td>"
                    f"<td>{html.escape(m.get('engagement') or 'unmatched')}</td><td>{' | '.join(bits)}</td>"
                    f"<td class='muted'>{html.escape(phs)}</td></tr>")
    mb = "".join(f'<li><a href="/brief-file?path={html.escape(p)}">{d}</a></li>' for d, p in sorted(st.get("morning", {}).items(), reverse=True)[:7])
    spend = A.day_spend()
    return page("Autopilot", f"""<h1>Meeting autopilot</h1><p class="muted">Spend today ${spend:.3f}. Nothing here sends anything.</p>
<table><tr><th>When</th><th>Meeting</th><th>Engagement</th><th>Open</th><th>Phases</th></tr>{''.join(rows) or '<tr><td colspan=5>No meetings yet</td></tr>'}</table>
<h2>Morning briefs</h2><ul>{mb or '<li>none yet</li>'}</ul>
<h2>Commands</h2><pre>{SCRIPT} status
{SCRIPT} apply &lt;key&gt;        # fallback STATUS write
{SCRIPT} undo &lt;key|engagement&gt;
{SCRIPT} gmail-draft &lt;key&gt;  # creates a Gmail DRAFT, never sends
{SCRIPT} uninstall</pre>""")


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
                   f'<p class="muted"><a href="/live/{key}">Live sidekick</a> | file: {html.escape(p)}</p>')


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
<div class="grid"><div><h2>Client questions, suggested answers</h2><div id="q"></div></div>
<div><h2>Next questions to ask</h2><ul id="n"></ul><h2>Commitments heard</h2><ul id="c"></ul>
<h2>Transcript tail</h2><div class="tail" id="tail"></div></div></div>""", LIVE_JS % json.dumps(key))


@app.get("/digest/{key}")
def digest(key: str):
    """Drafts live in the approval queue inbox now (one pipeline for every draft)."""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(A.QUEUE_UI)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=A.PORT, log_level="warning")
