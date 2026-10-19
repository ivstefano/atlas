#!/usr/bin/env python3
"""CRM snapshot for the command center: HubSpot deals + Asana commercial tracker -> _autopilot/cache/crm.json.

The dashboard server cannot call MCP, so this runs a headless `claude -p` (Bedrock, Haiku) with ONLY the
hubspot and asana MCP servers (strict config) and only their read tools exposed (the rest are denied, which
also keeps the tool list small: about $0.04 per run instead of $0.12). The model just fetches and dumps JSON;
matching deals/tasks to engagements happens in Python at read time (autopilot/cc_data.py).

Spend goes to _autopilot/spend.jsonl as step "crm", so it counts toward the autopilot's daily soft/hard caps
(meeting_autopilot.pick_model). On top: a CRM sub-cap (config crm_cap_usd, default $0.40/day); the automatic
refresh stops there, a manual Refresh still runs until the hard cap. A failed source keeps its last good data.

    crm_refresh.py            run once (manual)
    crm_refresh.py auto       run only if work hours, cache older than crm_refresh_min, and under the sub-cap
    crm_refresh.py show       print the cache summary
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import meeting_autopilot as A  # noqa: E402

CACHE = A.AP / "cache" / "crm.json"
LOCK = A.AP / "run" / "crm_refresh.lock"
PROJECT = "1214855342290138"     # Asana "Iris.ai Commercial Engagements"
DEFAULTS = dict(crm_refresh_min=60, crm_cap_usd=0.40, crm_hours=[8, 19])

ALLOWED = ["mcp__hubspot__search_crm_objects", "mcp__hubspot__search_owners", "mcp__hubspot__get_properties",
           "mcp__asana__get_tasks", "mcp__asana__get_task"]
# Every other tool these two servers expose (2026-10-19). Denied = not even loaded into the model's context.
DENY = """mcp__asana__add_comment mcp__asana__create_project mcp__asana__create_project_from_template
mcp__asana__create_project_status_update mcp__asana__create_task_from_template mcp__asana__create_tasks
mcp__asana__delete_task mcp__asana__get_agent mcp__asana__get_attachments mcp__asana__get_items_for_portfolio
mcp__asana__get_me mcp__asana__get_my_tasks mcp__asana__get_portfolio mcp__asana__get_portfolios
mcp__asana__get_project mcp__asana__get_projects mcp__asana__get_status_overview mcp__asana__get_task_stories
mcp__asana__get_teams mcp__asana__get_user mcp__asana__get_users mcp__asana__get_workspace_agents
mcp__asana__search_objects mcp__asana__search_tasks mcp__asana__update_project mcp__asana__update_tasks
mcp__hubspot__discover_hubspot_schema mcp__hubspot__get_aeo_metrics mcp__hubspot__get_campaign_attribution_reports
mcp__hubspot__get_content_analytics_report mcp__hubspot__get_conversation_channel_metadata mcp__hubspot__get_crm_objects
mcp__hubspot__get_marketing_email_analytics mcp__hubspot__get_organization_details mcp__hubspot__get_user_details
mcp__hubspot__manage_aeo_prompts mcp__hubspot__manage_aeo_recommendations mcp__hubspot__manage_campaign_objects
mcp__hubspot__manage_crm_objects mcp__hubspot__manage_landing_page mcp__hubspot__manage_marketing_email
mcp__hubspot__manage_onboarding mcp__hubspot__manage_segment mcp__hubspot__query_crm_data mcp__hubspot__query_segments
mcp__hubspot__read_campaign_data mcp__hubspot__search_conversations mcp__hubspot__search_intent_signals
mcp__hubspot__search_properties mcp__hubspot__submit_feedback mcp__hubspot__tool_guidance""".split()

PROMPT = """Read-only data fetch. Never create, update or delete anything.

1. HubSpot: mcp__hubspot__search_crm_objects, objectType "deals", only the "Sales" pipeline (look up its id with
   mcp__hubspot__get_properties on deals/pipeline or dealstage if needed), hs_lastmodifieddate in the last 120 days,
   sorted by hs_lastmodifieddate descending, limit 100. Properties: dealname, dealstage, pipeline, hs_next_step, amount,
   deal_currency_code, closedate, hubspot_owner_id, hs_lastmodifieddate, notes_next_activity_date.
   Resolve dealstage ids to stage labels and owner ids to names (mcp__hubspot__search_owners).
   Then, for each of these company names that matches no dealname from that first search, run one more search
   (dealname contains the name, any modified date, limit 3) and add what you find: {names}.
2. Asana: mcp__asana__get_tasks for project {project}, incomplete tasks only, fields name, due_on, assignee.name,
   memberships.section.name, permalink_url, notes.

Output ONLY one JSON object, no prose, no code fence. Cut next_step to 300 characters and notes to 160.
{{"hubspot":{{"deals":[{{"id":"","name":"","stage":"","pipeline":"","next_step":"","amount":"","currency":"","close_date":"YYYY-MM-DD","owner":"","modified":"YYYY-MM-DD","next_activity":""}}]}},
 "asana":{{"tasks":[{{"gid":"","name":"","section":"","due_on":"","assignee":"","url":"","notes":""}}]}},
 "errors":[]}}
If a source fails, leave its list empty and put "hubspot: <reason>" or "asana: <reason>" in errors."""


def watch_names():
    """Display names of active engagements, so deals not modified recently still get looked up by name."""
    rank = {"active": 0, "pre-scoping": 1, "scoping": 1}
    out = []
    for k, v in A.aliases().items():
        if k.startswith("_") or not isinstance(v, dict) or str(v.get("status") or "").lower() not in rank:
            continue
        t = [str(x) for x in v.get("titles") or [] if len(str(x)) >= 3]
        out.append((rank[str(v.get("status")).lower()], t[0] if t else k))
    return [n for _, n in sorted(out)][:24]


def conf():
    c = A.cfg()
    return {k: c.get(k, v) for k, v in DEFAULTS.items()}


def load():
    try:
        return json.loads(CACHE.read_text())
    except (OSError, ValueError):
        return {}


def crm_spend(day=None):
    day = day or dt.date.today().isoformat()
    tot = 0.0
    try:
        for ln in A.SPEND.read_text().splitlines():
            r = json.loads(ln)
            if r.get("day") == day and r.get("step") == "crm" and not r.get("dry"):
                tot += r.get("usd", 0)
    except OSError:
        pass
    return tot


def running():
    """pid of a refresh in progress, else None (stale locks are ignored)."""
    try:
        pid = int(LOCK.read_text().split()[0])
    except (OSError, ValueError, IndexError):
        return None
    return pid if A.pid_alive(pid) and time.time() - LOCK.stat().st_mtime < 900 else None


def _mcp_config():
    """hubspot + asana entries copied from the user MCP config (type/url/oauth client id only; tokens and client
    secrets stay in Claude's keychain)."""
    user = json.loads((A.HOME / ".claude.json").read_text()).get("mcpServers") or {}
    servers = {k: {kk: vv for kk, vv in user[k].items() if kk in ("type", "url", "oauth")} for k in ("hubspot", "asana") if k in user}
    A.RUN.mkdir(parents=True, exist_ok=True)
    p = A.RUN / "mcp_crm.json"
    p.write_text(json.dumps({"mcpServers": servers}))
    return str(p)


def _warm_tokens():
    """`claude mcp get` health-checks the servers with the user config, which refreshes an expired OAuth token.
    A strict-config headless run could not refresh the Asana token on 2026-10-19 and marked it needs-auth."""
    for name in ("asana", "hubspot"):
        try:
            subprocess.run([A.CLAUDE, "mcp", "get", name], capture_output=True, text=True, timeout=60, cwd=str(A.HOME), env=A._env())
        except Exception:
            pass


def _parse(txt):
    if not txt:
        return None
    t = txt.strip()
    t = re.sub(r"^```\w*\n|\n```$", "", t)
    try:
        return json.loads(t[t.index("{"):t.rindex("}") + 1])
    except ValueError:
        return None


def refresh(reason="manual"):
    if running():
        return dict(ok=False, error="refresh already running")
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    LOCK.write_text(f"{os.getpid()} {reason}")
    t0 = time.time()
    try:
        mk = A.pick_model("crm")            # None at the hard cap
        if not mk:
            return _finish(dict(ok=False, error="daily spend cap reached"), t0)
        _warm_tokens()
        cmd = [A.CLAUDE, "-p", "--model", A.MODELS["haiku"]["id"], "--strict-mcp-config", "--mcp-config", _mcp_config(),
               "--tools", "", "--allowedTools", ",".join(ALLOWED), "--disallowedTools", " ".join(DENY),
               "--permission-mode", "dontAsk", "--output-format", "json", "--no-session-persistence", "--max-budget-usd", "0.20"]
        try:
            r = subprocess.run(cmd, input=PROMPT.format(project=PROJECT, names=", ".join(watch_names())), capture_output=True, text=True, timeout=600,
                               cwd=str(A.RUN), env=dict(A._env(), MCP_TIMEOUT="60000"))
        except subprocess.TimeoutExpired:
            return _finish(dict(ok=False, error="claude timed out"), t0)
        try:
            d = json.loads(r.stdout)
        except ValueError:
            err = (r.stderr or r.stdout)[-300:]
            if re.search(r"ExpiredToken|SSO|security token", err):
                err = "AWS login expired: aws sso login --profile Iris_Devs"
            return _finish(dict(ok=False, error=err), t0)
        usd = d.get("total_cost_usd") or 0.0
        inp = out = 0
        for mu in (d.get("modelUsage") or {}).values():
            inp += mu.get("inputTokens", 0) + mu.get("cacheReadInputTokens", 0) + mu.get("cacheCreationInputTokens", 0)
            out += mu.get("outputTokens", 0)
        A.record_spend("crm", f"crm-{reason}", "haiku", inp, out, usd)
        data = _parse(d.get("result"))
        if not data:
            return _finish(dict(ok=False, error=f"no JSON in answer ({d.get('subtype')})", usd=usd), t0)
        return _finish(dict(ok=True, usd=usd, data=data), t0)
    finally:
        try:
            LOCK.unlink()
        except OSError:
            pass


def _finish(res, t0):
    old = load()
    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    new = dict(old)
    data = res.pop("data", None)
    if data:
        errs = data.get("errors") or []
        for src, key in (("hubspot", "deals"), ("asana", "tasks")):
            rows = (data.get(src) or {}).get(key) or []
            err = next((e for e in errs if e.lower().startswith(src)), None)
            if rows:
                new[src] = {"as_of": now, key: rows, "error": None}
            else:
                new[src] = {**(old.get(src) or {}), "error": err or "empty result"}
        new["notes"] = errs
    elif res.get("error"):
        for src in ("hubspot", "asana"):
            if src in new:
                new[src] = {**new[src], "error": res["error"]}
    new["last_run"] = {"at": now, "secs": round(time.time() - t0), **res}
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE.with_suffix(".tmp")
    tmp.write_text(json.dumps(new, indent=1, ensure_ascii=False))
    os.replace(tmp, CACHE)
    A.log(f"crm refresh {'ok' if res.get('ok') else 'failed: ' + str(res.get('error'))[:120]} ${res.get('usd', 0):.3f} {round(time.time() - t0)}s")
    return res


def due_auto(now=None):
    """Why an automatic refresh should not run now (str), or None if it should."""
    c = conf()
    now = now or dt.datetime.now()
    if now.weekday() >= 5 or not (c["crm_hours"][0] <= now.hour < c["crm_hours"][1]):
        return "outside work hours"
    if crm_spend() >= c["crm_cap_usd"]:
        return f"CRM cap ${c['crm_cap_usd']:.2f} reached"
    last = (load().get("last_run") or {}).get("at")
    if last and (now.astimezone() - dt.datetime.fromisoformat(last)) < dt.timedelta(minutes=c["crm_refresh_min"]):
        return "fresh"
    return None


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    if cmd == "show":
        c = load()
        for src, key in (("hubspot", "deals"), ("asana", "tasks")):
            s = c.get(src) or {}
            print(f"{src}: {len(s.get(key) or [])} {key}, as of {s.get('as_of')}, error {s.get('error')}")
        print("last run:", c.get("last_run"), "| crm spend today $%.3f" % crm_spend())
    elif cmd == "auto":
        why = due_auto()
        print(why or json.dumps(refresh("auto")))
    else:
        print(json.dumps(refresh("manual")))
