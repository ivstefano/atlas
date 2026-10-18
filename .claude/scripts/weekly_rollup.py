#!/usr/bin/env python3
"""Weekly engagements rollup: a DRAFT for Jordan + Steven, in Ivo's voice. Never posted.

Gathers (all read-only):
  - Slack #active-engagements (public, C0B8GPS4DCN) via the Slack Web API with the
    browser tokens the local slack MCP uses (~/.config/slack-mcp/xoxc, xoxd). Only
    conversations.history, conversations.replies, users.info. Fallback: the Cognion
    weekly text copy. No DMs, no private channels.
  - engagements/*/STATUS.md + ARTEFACTS.md, change dates by git log.
  - Google Calendar (primary, read-only scope) using the workspace-mcp refresh token,
    exchanged in memory for a calendar.readonly access token. Fallback: Cognion events.json.
  - Tactiq meeting list (titles, dates) + Cognion meeting summaries (front matter).
Then two Bedrock calls (Sonnet 5.5, AWS_PROFILE Iris_Devs; override AUTOPILOT_MODEL) draft
section 1 (rollup) and section 3 (missing-post drafts). Section 2 (stale flags) is computed here.
Every draft also goes into the approvals queue (approval_queue.py, inbox at http://127.0.0.1:8096):
the rollup as a note, each missing post as a Slack thread reply (or new thread). Nothing is sent
from this script.

Writes  atlas/briefs/YYYY/WNN/YYYY-MM-DD_weekly-rollup.md
Logs    atlas/_autopilot/logs/weekly_rollup.log (gitignored)

Cost guard: estimated cost is checked before the call (trims input, aborts above
MAX_COST_USD); actual cost from Bedrock usage is logged and written into the draft.

    weekly_rollup.py [--date YYYY-MM-DD] [--no-notify] [--force] [--dry] [--preflight]

--dry        gather + write the prompt to the log dir, no LLM call
--preflight  check every source + a 1-token Bedrock ping, write nothing else (for launchd checks)
"""
import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from autopilot_common import *  # noqa: E402,F401,F403
from autopilot_common import (  # noqa: E402
    tcc_guard,
    ATLAS, ENG, LOG_DIR, CHANNEL, IVO_SLACK, MODEL, PRICE_IN, PRICE_OUT, MAX_COST_USD, TARGET_COST_USD,
    HISTORY_DAYS, STALE_DAYS, ACTIVE_DAYS, CLOSED, DATE_RX, SYSTEM)

import approval_queue as Q  # noqa: E402

set_log("weekly_rollup")
APPROVALS_URL = "http://127.0.0.1:8096"


DATE_KEY = "Date key (use these weekdays, never guess): {days}"

TASK_ROLLUP = """Today is {today} ({weekday}). Week {week}: {t0} to {t1}. Next week: {n0} to {n1}.
{date_key}

Write ONE ready-to-paste Slack message from Ivo to Jordan and Steven, inside a ```text fence. Nothing \
outside the fence.

Shape:
Line 1: a casual opener in his words, e.g. "Hey Jordan, Steven, weekly rollup on the engagements".
Then one block per engagement in ENGAGEMENTS THAT MOVED, most commercially urgent first (money, \
signature, year-end AWS credit deadlines first). Block shape, exactly four labelled lines:

*<Client name>*
Status: <what moved THIS week only: 1-2 short sentences, the one or two facts a sales lead cares about>
Commercial gate: <the single decision or blocker and who holds it; Jordan-owned asks as "Over to Jordan: ...">
Timeline: <next step - owner - date (weekday from the date key); add next week's call on it if any>
Links: <only demo/showcase URLs from DEMO LINKS for this client, with access code if given; drop the line if none>

Hard limits: max 45 words per block (Links line not counted). Max 8 blocks; fold the rest into the \
quiet line. No technical detail (no F1, OCR, tables, symbols, model names) unless it is the proof a sales \
lead would repeat to the client, then one number max. Do not copy STATUS sentences verbatim; compress.
After the blocks:
- one line "Quiet this week: <names only>, details in the stale list" (names of engagements in STALE FLAGS)
- one line with the single most important ask to a named person (from the data), if any.
Total under 550 words. Ivo's register: plain, slightly loose, capitals at line starts, no bold except the \
*Client* lines, no wrap-up.

=== ENGAGEMENTS THAT MOVED (STATUS entries dated this week, ARTEFACTS added this week) ===
{engagements}

=== CALLS THIS WEEK (Ivo attended; [T] = transcript exists) ===
{calls}

=== CALLS NEXT WEEK ===
{next_calls}

=== #active-engagements THIS WEEK (all authors) ===
{slack_week}

=== DEMO LINKS FOUND THIS WEEK ===
{links}

=== STALE FLAGS (names only needed) ===
{stale_names}
"""

TASK_POSTS = """Today is {today} ({weekday}). Week {week}: {t0} to {t1}.
{date_key}

These client calls happened this week and nobody posted about them in #active-engagements. For EACH one, \
draft the post Ivo would put in the channel, copying the shape of his real posts below:
- a top-level message that is just the client name (that is how he opens a thread)
- a thread reply: "*<Client>* - <deal or topic>", then "cc: @Jordan" (+ others only if they attended), \
then "Contact: <name, role>" and "Call: <weekday date>, with <who>", then 3-5 plain bullets of what we \
learned that matter commercially, then "Status: ..." (one line), then "Next: <step> - <owner> - <date>" \
(1-3 lines; Jordan-owned items stay as plain facts, e.g. "Jordan sends the invite", never drafted for him), \
then an honest caveat line if something is unproven or unknown.
Max 130 words per thread reply. Facts only from the data below; if a fact is missing write "(?: ...)".
If two calls are on the same client, write one post covering both.

Output markdown only, per client:
### [<engagement folder name exactly as in CALLS WITHOUT A POST>] <Client>, <call title>, <weekday date>
```text
<Client>
--- thread reply ---
<thread message>
```

=== CALLS WITHOUT A POST ===
{missing}

=== DATA FOR THOSE CLIENTS (STATUS entries this week) ===
{engagements}

=== MEETING SUMMARIES (Tactiq) ===
{meetings}

=== IVO'S REAL #active-engagements POSTS (format reference only, do not reuse their facts) ===
{examples}
"""



# ----------------------------------------------------------------------------- main
def main():
    if os.environ.get("ATLAS_WEEKLY_ROLLUP") == "1":
        return  # recursion guard (never re-enter from a nested run)
    os.environ["ATLAS_WEEKLY_ROLLUP"] = "1"
    tcc_guard("weekly-rollup")
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="as-of date YYYY-MM-DD (default today)")
    ap.add_argument("--no-notify", action="store_true")
    ap.add_argument("--force", action="store_true", help="overwrite an existing draft")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--preflight", action="store_true")
    a = ap.parse_args()

    today = d(a.date) if a.date else dt.date.today()
    t0 = today - dt.timedelta(days=today.weekday())           # Monday
    t1 = t0 + dt.timedelta(days=7)
    n0, n1 = t1, t1 + dt.timedelta(days=7)
    iso = today.isocalendar()
    week = f"{iso[0]}-W{iso[1]:02d}"
    now = dt.datetime.now()
    log(f"run start as-of {today} {week} preflight={a.preflight} dry={a.dry}")
    src = {}

    # Slack
    hist_start = today - dt.timedelta(days=HISTORY_DAYS)
    sl = None
    try:
        sl = Slack()
        msgs = sl.channel(dt.datetime.combine(hist_start, dt.time()).timestamp())
        src["slack"] = f"live API, {len(msgs)} msgs since {hist_start}"
    except Exception as e:
        log(f"slack live failed: {e}; using Cognion copy")
        msgs = slack_from_cognion(hist_start)
        src["slack"] = f"Cognion copy (live failed: {str(e)[:60]}), {len(msgs)} msgs"

    # Calendar
    cal_start = today - dt.timedelta(days=ACTIVE_DAYS)
    try:
        events = calendar(cal_start, n1)
        src["calendar"] = f"live primary, {len(events)} events"
    except Exception as e:
        log(f"calendar live failed: {e}; using Cognion events.json")
        events = calendar_from_cognion(cal_start, n1)
        src["calendar"] = f"Cognion events.json (live failed: {str(e)[:60]}), {len(events)} events"

    # Tactiq + meeting summaries
    try:
        tq = tactiq_week(t0)
        src["tactiq"] = f"{len(tq)} meetings this week"
    except Exception as e:
        tq = []
        src["tactiq"] = f"unavailable ({str(e)[:60]})"
        log(f"tactiq failed: {e}")
    meetings = cognion_meetings(t0, t1)
    src["meeting summaries"] = f"{len(meetings)} (Cognion copy)"
    src["asana"] = "not read (asana MCP not authenticated; script has no Asana token)"

    if a.preflight:
        try:
            _, u, c = bedrock("Reply with: ok", "ok", max_tokens=5)
            src["bedrock"] = f"ok ({MODEL}, ${c:.5f})"
        except Exception as e:
            src["bedrock"] = f"FAILED: {e}"
        for k, v in src.items():
            log(f"preflight {k}: {v}")
        ok = not src["bedrock"].startswith("FAILED")
        log("preflight " + ("OK" if ok else "FAILED"))
        sys.exit(0 if ok else 1)

    # Engagements
    al = aliases()
    names = sorted(p.name for p in ENG.iterdir()
                   if p.is_dir() and not p.name.startswith((".", "_")) and (p / "STATUS.md").exists())
    rx = {k: v for k, v in matcher(al).items() if k in names}
    for n in names:
        rx.setdefault(n, (re.compile(r"\b" + re.escape(n.replace("-", " ")) + r"\b", re.I), set()))

    last_slack, week_slack_hits = {}, {}
    for m in msgs:
        hits = match(rx, m["text"] + " " + m.get("parent", ""))
        for h in hits:
            last_slack[h] = max(last_slack.get(h, ""), m["date"][:10])
            if m["date"][:10] >= t0.isoformat():
                week_slack_hits.setdefault(h, []).append(m)

    # Ivo left some invites unanswered but still joined: count those as attended when a
    # meeting summary for that day lists him
    for e in events:
        if e["response"] != "accepted" and any(
                m["date"] == e["start"][:10] and (m["title"][:20].lower() in e["title"].lower()
                                                   or e["title"][:20].lower() in m["title"].lower())
                for m in meetings):
            e["response"] = "accepted"
    last_call, week_calls, next_calls = {}, [], []
    tq_by_day = {}
    for t in tq:
        tq_by_day.setdefault(t["date"], []).append(t["title"].lower())
    for e in events:
        day = e["start"][:10]
        start_dt = dt.datetime.fromisoformat(e["start"].replace("Z", "+00:00"))
        hits = match(rx, e["title"], e["emails"] if e["external"] else ())
        e["eng"] = sorted(hits)
        e["day"] = day
        e["tactiq"] = any(e["title"].lower()[:18] in tt or tt[:18] in e["title"].lower() for tt in tq_by_day.get(day, []))
        if start_dt.timestamp() <= now.timestamp() and e["external"] and e["response"] == "accepted":
            for h in hits:
                last_call[h] = max(last_call.get(h, ""), day)
        if t0.isoformat() <= day < t1.isoformat() and start_dt.timestamp() <= now.timestamp():
            if e["response"] == "accepted":          # only calls Ivo actually took
                week_calls.append(e)
        elif start_dt.timestamp() > now.timestamp() and day < n1.isoformat():
            next_calls.append(e)

    info = {}
    for n in names:
        meta = al.get(n, {})
        f = engagement_files(n, t0)
        acts = [x for x in (f["last_status"], last_call.get(n), last_slack.get(n)) if x]
        last_any = max(acts) if acts else None
        info[n] = dict(meta=meta, **f, last_call=last_call.get(n), last_slack=last_slack.get(n), last_any=last_any)

    def live(n):
        i = info[n]
        if (i["meta"].get("status") or "") in CLOSED:
            return False
        return bool(i["last_any"]) and d(i["last_any"]) >= today - dt.timedelta(days=ACTIVE_DAYS)

    active = [n for n in names if live(n)]
    upcoming = {h for e in next_calls for h in e["eng"]}
    moved = [n for n in active if (info[n]["last_any"] or "") >= t0.isoformat()]

    # Stale flags (deterministic)
    stale_rows = []
    for n in active:
        i = info[n]
        reasons = []
        if d(i["last_any"]) <= today - dt.timedelta(days=STALE_DAYS):
            reasons.append(f"no STATUS change, call or Slack post in {(today - d(i['last_any'])).days} days")
        for na in i["next_actions"]:
            for ds in DATE_RX.findall(na):
                if d(ds) < today:
                    reasons.append(f"overdue next action (by {ds}): {na[:140]}")
        if reasons:
            stale_rows.append((n, i, reasons))
    stale_md = ["| Engagement | Stage | Last STATUS | Last call | Last Slack | Flag |", "|---|---|---|---|---|---|"]
    for n, i, rs in stale_rows:
        stale_md.append(f"| {n} | {i['meta'].get('status', '?')} | {i['last_status'] or '-'} | {i['last_call'] or '-'} | "
                        f"{i['last_slack'] or '-'} | {'; '.join(rs).replace('|', '/')} |")
    if not stale_rows:
        stale_md = ["None."]
    stale_txt = "\n".join(stale_md)

    # Missing posts: external engagement calls this week with no channel message on that engagement this week
    missing = []
    for e in week_calls:
        if not e["external"] or not e["eng"]:
            continue
        for h in e["eng"]:
            posts = [m for m in week_slack_hits.get(h, []) if m["date"][:10] >= e["day"]]
            if not posts and not any(x[0] == h for x in missing):
                missing.append((h, e))
    # one post per client family: keep fresenius-complaint-coding, drop the bare "fresenius" twin
    hs = {h for h, _ in missing}
    missing = [(h, e) for h, e in missing if not any(o != h and o.startswith(h + "-") for o in hs)]

    # Links (demos/showcases) this week
    url_rx = re.compile(r"https?://[^\s)>\]|`]+|[\w.-]+\.s3[\w.-]*\.amazonaws\.com/[^\s)>\]|`]*")
    links = []
    for m in msgs:
        if m["date"][:10] >= t0.isoformat() and m["user"] == IVO_SLACK:
            for u in url_rx.findall(m["text"]):
                if "slack.com/archives" not in u and "<" not in u:
                    links.append(f"- Slack {m['date']} ({', '.join(sorted(match(rx, m['text'] + ' ' + m['parent']))) or '?'}): {u}")
    for n in names:
        for u in url_rx.findall(info[n]["artefacts_added"]):
            if "<" not in u and any(k in u for k in ("s3", "amazonaws", "drive.google", "docs.google", "duckdns", "iris.ai")):
                links.append(f"- ARTEFACTS.md {n}: {u}")
    links = list(dict.fromkeys(links))

    # Format examples: Ivo's long channel posts
    ex = [m for m in msgs if m["user"] == IVO_SLACK and len(m["text"]) > 300]
    try:
        ex += [m for m in slack_from_cognion(today - dt.timedelta(days=200))
               if m["user"] == IVO_SLACK and len(m["text"]) > 300]
    except Exception as e:
        log(f"cognion slack copy unreadable: {e}")

    def ex_score(m):   # his channel-update shape: *Title* line, Status:, demo link; not email drafts
        t = m["text"]
        s = 2 * bool(re.search(r"^\*[^*\n]{3,80}\*", t, re.M)) + bool(re.search(r"Status:|demo|s3\.", t, re.I))
        return s - 3 * bool(re.search(r"^(Hi|Dear) ", t, re.M))
    ex = sorted({m["text"][:60]: m for m in ex}.values(), key=lambda m: (-ex_score(m), -m["ts"]))[:5]

    # ----- assemble prompts with a cost-driven budget
    def day(iso_s):
        return d(iso_s).strftime("%a %-d %b")

    def eng_block(ns, cap):
        out = []
        for n in ns:
            i = info[n]
            out.append(f"### {n} (stage {i['meta'].get('status', '?')}; last STATUS {i['last_status']}, "
                       f"last call {i['last_call']}, last Slack {i['last_slack']})\n"
                       + i["newest"][:cap]
                       + (f"\n[ARTEFACTS added this week]\n{i['artefacts_added'][:cap // 4]}" if i["artefacts_added"] else ""))
        return "\n\n".join(out) or "(none)"

    def call_line(e):
        return (f"- {day(e['day'])} {e['start'][11:16]} Sofia, {e['title']} | engagement: {', '.join(e['eng']) or '?'} | "
                f"{'external' if e['external'] else 'internal'}{' [T]' if e.get('tactiq') else ''}"
                f"{'' if e['response'] == 'accepted' else ' (Ivo: ' + (e['response'] or 'not invited') + ')'}")

    moved_sorted = sorted(set(moved) | (upcoming & set(active)), key=lambda x: (x not in moved, x))
    moved_sorted = [n for n in moved_sorted if info[n]["has_week_entry"] or n in upcoming
                    or n in week_slack_hits or n in {h for e in week_calls for h in e["eng"]}]
    miss_names = list(dict.fromkeys(h for h, _ in missing))
    slack_week = "\n".join(f"[{m['date']}] {m['who']}{'' if m['top'] else ' (thread: ' + m['parent'][:50] + ')'}: {m['text'][:700]}"
                           for m in msgs if m["date"][:10] >= t0.isoformat())
    days = ", ".join(day((t0 + dt.timedelta(days=k)).isoformat()) + f" = {(t0 + dt.timedelta(days=k)).isoformat()}"
                     for k in range(14))
    base = dict(today=today.isoformat(), weekday=today.strftime("%a"), week=week, t0=t0,
                t1=t1 - dt.timedelta(days=1), n0=n0, n1=n1 - dt.timedelta(days=1),
                date_key=DATE_KEY.format(days=days))
    miss_meet = [m for m in meetings if match(rx, m["title"] + " " + m["participants"]) & set(miss_names)]
    examples = "\n\n---\n".join(f"[{m['date']}]\n{m['text'][:1500]}" for m in ex) or "(none found)"
    system = SYSTEM.format(voice=voice_block())
    out_posts = 900 * len(miss_names) + 1500 if miss_names else 0
    out_roll = 5000
    cap = 2400
    while True:
        u1 = TASK_ROLLUP.format(engagements=eng_block(moved_sorted, cap),
                                calls="\n".join(call_line(e) for e in week_calls) or "(none)",
                                next_calls="\n".join(call_line(e) for e in next_calls) or "(none)",
                                slack_week=slack_week[:15000] or "(none)", links="\n".join(links) or "(none)",
                                stale_names=", ".join(r[0] for r in stale_rows
                                                      if r[0] not in moved_sorted and r[0] not in miss_names) or "(none)", **base)
        u2 = TASK_POSTS.format(missing="\n".join(f"- {h}: {e['title']} on {day(e['day'])}" for h, e in missing),
                               engagements=eng_block(miss_names, cap),
                               meetings="\n".join(f"- {day(m['date'])} {m['title']} ({m['participants'][:150]})\n  {m['summary'][:1500]}"
                                                   for m in miss_meet) or "(none)",
                               examples=examples, **base) if miss_names else ""
        n_in = len(system) * (2 if u2 else 1) + len(u1) + len(u2)
        est = (n_in / 3.2) * PRICE_IN + (out_roll + out_posts) * PRICE_OUT
        if est <= TARGET_COST_USD or cap <= 600:
            break
        cap -= 300
    log(f"prompt {n_in} chars, STATUS cap {cap}, est ${est:.3f}; active={len(active)} moved={len(moved_sorted)} "
        f"stale={len(stale_rows)} missing={len(missing)}")
    if est > MAX_COST_USD:
        log(f"ABORT: estimated ${est:.3f} > ${MAX_COST_USD}")
        sys.exit(2)

    if a.dry:
        p = LOG_DIR / f"{today}_weekly-rollup.prompt.txt"
        p.write_text(system + "\n\n===== ROLLUP\n\n" + u1 + "\n\n===== POSTS\n\n" + u2)
        log(f"dry run, prompts at {p}")
        return

    out_dir = ATLAS / "briefs" / str(iso[0]) / f"W{iso[1]:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{today}_weekly-rollup.md"
    if out.exists() and not a.force:
        out = out_dir / f"{today}_weekly-rollup_{now.strftime('%H%M')}.md"

    cost, tin, tout = 0.0, 0, 0
    try:
        part1, u, c = bedrock(system, u1, max_tokens=out_roll)
        cost, tin, tout = cost + c, tin + u["inputTokens"], tout + u["outputTokens"]
        part3 = "None this week."
        if u2:
            part3, u, c = bedrock(system, u2, max_tokens=out_posts)
            cost, tin, tout = cost + c, tin + u["inputTokens"], tout + u["outputTokens"]
    except Exception as e:
        msg = str(e)
        hint = (" Run: aws sso login --profile Iris_Devs, then rerun." if "Token" in msg or "SSO" in msg or "expired" in msg.lower() else "")
        log(f"bedrock failed: {msg}")
        out.write_text(f"# Weekly rollup {week}: FAILED\n\nBedrock call failed: {clean(msg)[:400]}.{hint}\n\n"
                       f"## 2. Stale flags\n\n{stale_txt}\n")
        if not a.no_notify:
            notify(out, "Weekly rollup failed", "Bedrock call failed." + hint)
        sys.exit(1)
    part1 = "## 1. Rollup for Jordan and Steven\n\n" + clean(part1.strip())
    part3 = "## 3. Missing #active-engagements posts\n\n" + clean(part3.strip())
    usage = dict(inputTokens=tin, outputTokens=tout)
    srcs = "\n".join(f"- {k}: {v}" for k, v in src.items())
    doc = f"""# Weekly engagements rollup, {week} ({t0} to {t1 - dt.timedelta(days=1)})

> DRAFT for Ivo. Never posted or sent. Review, edit, then paste yourself.
> Generated {now.strftime('%Y-%m-%d %H:%M')} by `.claude/scripts/weekly_rollup.py`, {MODEL.split('.')[-1]}, \
{usage['inputTokens']} in / {usage['outputTokens']} out tokens, ${cost:.3f}.

{part1.strip()}

## 2. Stale flags

Live engagements (not closed, something moved in the last {ACTIVE_DAYS} days) with nothing in {STALE_DAYS}+ days, \
or an overdue next action in the newest STATUS entry.

{stale_txt}

{part3.strip()}

## Sources

{srcs}
"""
    out.write_text(clean(doc))
    log(f"wrote {out} cost ${cost:.4f} usage {usage}")
    n = enqueue(out, week, part1, part3, sl, rx, info)
    log(f"queued {n} items; {Q.pending_count()} pending in the approvals inbox")
    if not a.no_notify:
        notify(APPROVALS_URL, "Weekly rollup draft ready",
               f"{week}: {len(moved_sorted)} moved, {len(stale_rows)} stale, {len(missing)} missing posts. "
               f"{Q.pending_count()} drafts waiting in Approvals.")


def enqueue(out, week, part1, part3, sl, rx, info):
    """Rollup -> one note item; each missing-post draft -> a slack item (thread reply when the engagement
    already has a top-level thread in #active-engagements, else a new top-level post + thread reply)."""
    rel = str(out.relative_to(ATLAS))
    srcs = [dict(label=f"draft {rel}", path_or_url=str(out))]
    m = re.search(r"```text\n(.*?)```", part1, re.S)
    Q.add("weekly-rollup", "operations", "note", f"Weekly rollup {week} for Jordan + Steven",
          (m.group(1) if m else part1).strip(), target=dict(path=str(out)), sources=srcs,
          key=f"weekly-rollup:{week}")
    n = 1
    threads = {}
    if sl:
        try:
            threads = find_threads(sl, rx)
        except Exception as e:
            log(f"thread lookup failed: {e}")
    for blk in re.split(r"\n(?=### )", part3):
        h = re.match(r"### \[([\w-]+)\]\s*(.*)", blk)
        f = re.search(r"```text\n(.*?)```", blk, re.S)
        if not h or not f:
            continue
        eng, title, body = h.group(1), h.group(2).strip(), f.group(1).strip()
        th = threads.get(eng) or next((v for k, v in threads.items() if eng.startswith(k + "-")), None)
        for old in Q.list_items("pending", engagement=eng, source="monday-thread"):
            Q.update(old["id"], "superseded by this week's missing-post draft", by="autopilot", status="rejected")
        ssrc = srcs + [dict(label=f"{eng}/STATUS.md", path_or_url=str(ENG / eng / "STATUS.md"))]
        if th:
            reply = re.split(r"^-{3}\s*thread reply\s*-{3}\s*$", body, maxsplit=1, flags=re.M | re.I)[-1].strip()
            Q.add("missing-post", eng, "slack_thread_reply", f"Missing post: {title}", reply,
                  target=dict(channel=CHANNEL, thread_ts=th["ts"], permalink=th["permalink"]),
                  sources=ssrc + [dict(label=f"thread: {th['text'][:40]}", path_or_url=th["permalink"])],
                  key=f"missing-post:{eng}:{week}")
        else:
            Q.add("missing-post", eng, "slack_post", f"Missing post (new thread): {title}", body,
                  target=dict(channel=CHANNEL, thread_ts=None,
                              permalink=f"https://irisai.slack.com/archives/{CHANNEL}"),
                  sources=ssrc, key=f"missing-post:{eng}:{week}")
        n += 1
    return n


if __name__ == "__main__":
    main()

