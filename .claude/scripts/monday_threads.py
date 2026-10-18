#!/usr/bin/env python3
"""Monday thread updates: for each engagement that already has a top-level thread in
#active-engagements, look for new developments since the last message in that thread and, if
there are any, draft a short thread reply in Ivo's voice. Drafts only, never posted.

New-development sources (read-only): engagement STATUS/ARTEFACTS git changes, Tactiq calls
(Cognion summaries + Tactiq list), calendar events, emails Ivo sent to the client's domains
(Gmail search, readonly scope), Bitbucket commits on linked repos (Cognion activity.json).

Output:
  atlas/briefs/YYYY/WNN/YYYY-MM-DD_monday-thread-updates.md
  one slack_thread_reply item per draft in the approvals queue (http://127.0.0.1:8096);
  the reply is posted only when Ivo clicks "Approve & reply in thread" there.

One Bedrock call for all drafts. Cost guard as in weekly_rollup (est checked before the call).

    monday_threads.py [--date YYYY-MM-DD] [--no-notify] [--dry]
"""
import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from autopilot_common import (  # noqa: E402
    tcc_guard,
    ATLAS, ENG, CHANNEL, IVO_SLACK, MODEL, PRICE_IN, PRICE_OUT, MAX_COST_USD, CLOSED, SYSTEM,
    Slack, set_log, log, clean, d, aliases, matcher, match, git, find_threads, calendar, cognion_meetings,
    tactiq_week, gmail_sent, bitbucket_commits, bedrock, voice_block, notify)
import approval_queue as Q  # noqa: E402

set_log("monday_threads")
APPROVALS_URL = "http://127.0.0.1:8096"
LOOKBACK_CAP = 60          # never look further back than this, even if the thread is older
SKIP = {"yettel", "nielsen", "aumovio"}   # owned outside Ivo's tracker (Vankata/Viktor) or archived

TASK = """Today is {today} ({weekday}). Below, per engagement: the last messages of its \
#active-engagements thread, and what happened SINCE the last thread message.

For each engagement, decide if there is a real development worth a thread update (a call, a \
decision, a deliverable/demo sent, a client email, a date set, a blocker). Formatting-only or \
internal-housekeeping commits alone are NOT worth it: output SKIP for that engagement.

For each worth-it engagement, draft Ivo's thread reply: the short delta version of his real post \
format. Shape:

Update {today_label}:
What changed:
• <fact, with date>
• <fact>
Status: <stage, and the blocker if any, one line>
What we need:
• <step> - <owner> - <date>

2-4 bullets under What changed, 1-3 under What we need. Max 90 words. Do not repeat anything the \
thread already says. Facts only from the data; no invented commitments, owners or dates; a missing \
fact is "(?: ...)". Jordan-owned items stay plain facts ("Jordan sends the invite"), never drafted \
for him. Optional "cc: @Name" first line only if a named person must act.

Output, per engagement, exactly:
### [<engagement>]
```text
<reply or SKIP>
```

{blocks}
"""


def since_data(n, info, since_dt, today, rx, events, meetings, tq, sent, bb):
    out, has = [], False
    st = (ENG / n / "STATUS.md")
    text = st.read_text(errors="ignore") if st.exists() else ""
    ents = []
    for e in re.split(r"\n(?=## )", text):
        if not e.startswith("## "):
            continue
        ds = re.findall(r"\d{4}-\d\d-\d\d", e.split("\n", 1)[0])
        if ds and max(ds) >= since_dt.date().isoformat():
            ents.append(e[:1800])
    if ents:
        has = True
        out.append("[STATUS entries since]\n" + "\n".join(ents[:3]))
    commits = git("log", f"--since={since_dt.isoformat(timespec='seconds')}", "--format=%ad %s", "--date=short",
                  "--", f"{n}/").strip().splitlines()
    if commits:
        out.append("[engagement repo commits since]\n" + "\n".join(commits[:12]))
        if any(not re.search(r"rename|typo|format|whitespace|profile", c, re.I) for c in commits):
            has = True
    art = git("log", f"--since={since_dt.isoformat(timespec='seconds')}", "-p", "--format=", "--", f"{n}/ARTEFACTS.md")
    added = [ln[1:] for ln in art.splitlines() if ln.startswith("+") and not ln.startswith("+++") and "http" in ln]
    if added:
        out.append("[ARTEFACTS added since]\n" + "\n".join(added[:8]))
    cal = [e for e in events if n in e["eng"]]
    past = [e for e in cal if e["start_ts"] >= since_dt.timestamp() and e["start_ts"] <= dt.datetime.now().timestamp()]
    fut = [e for e in cal if e["start_ts"] > dt.datetime.now().timestamp()]
    if past:
        has = has or any(e["external"] for e in past)
        out.append("[calls since]\n" + "\n".join(f"- {e['label']}" for e in past))
    if fut:
        out.append("[upcoming calls, next 14 days]\n" + "\n".join(f"- {e['label']}" for e in fut))
    ms = [m for m in meetings if n in match(rx, m["title"] + " " + m["participants"]) and m["date"] >= since_dt.date().isoformat()]
    if ms:
        has = True
        out.append("[meeting summaries since]\n" + "\n".join(f"- {m['date']} {m['title']}: {m['summary'][:900]}" for m in ms[:3]))
    tqs = [t for t in tq if n in match(rx, t["title"]) and t["date"] >= since_dt.date().isoformat()]
    if tqs and not ms:
        out.append("[Tactiq recordings since (titles only)]\n" + "\n".join(f"- {t['date']} {t['title']}" for t in tqs))
    if sent:
        has = True
        out.append("[emails Ivo sent to the client since]\n" + "\n".join(
            f"- {x['date']} to {x['to']}: {x['subject']} | {x['snippet']}" for x in sent))
    if bb:
        has = True
        out.append("[Bitbucket commits on linked repos since]\n" + "\n".join(bb[:8]))
    return has, "\n".join(out)


def main():
    if os.environ.get("ATLAS_MONDAY_THREADS") == "1":
        return
    os.environ["ATLAS_MONDAY_THREADS"] = "1"
    tcc_guard("monday-threads")
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    ap.add_argument("--no-notify", action="store_true")
    ap.add_argument("--dry", action="store_true", help="gather + write prompt, no LLM call, nothing queued")
    a = ap.parse_args()
    today = d(a.date) if a.date else dt.date.today()
    iso = today.isocalendar()
    week = f"{iso[0]}-W{iso[1]:02d}"
    log(f"run start {today} {week}")

    al = aliases()
    names = sorted(p.name for p in ENG.iterdir()
                   if p.is_dir() and not p.name.startswith((".", "_")) and (p / "STATUS.md").exists())
    rx = {k: v for k, v in matcher(al).items() if k in names}
    sl = Slack()
    threads = find_threads(sl, rx)
    log(f"{len(threads)} engagement threads found: {', '.join(sorted(threads))}")

    floor = today - dt.timedelta(days=LOOKBACK_CAP)
    try:
        evs = calendar(floor, today + dt.timedelta(days=14))
    except Exception as e:
        log(f"calendar failed: {e}")
        evs = []
    for e in evs:
        e["eng"] = sorted(match(rx, e["title"], e["emails"] if e["external"] else ()))
        sd = dt.datetime.fromisoformat(e["start"].replace("Z", "+00:00"))
        e["start_ts"] = sd.timestamp()
        e["label"] = (f"{sd.strftime('%a %-d %b %H:%M')} Sofia, {e['title']}"
                      f"{'' if e['response'] == 'accepted' else ' (Ivo: ' + (e['response'] or '?') + ')'}")
    meetings = cognion_meetings(floor, today + dt.timedelta(days=1))
    try:
        tq = tactiq_week(floor)
    except Exception as e:
        log(f"tactiq failed: {e}")
        tq = []

    blocks, metas = [], {}
    for n, th in sorted(threads.items()):
        meta = al.get(n, {}) or {}
        if (meta.get("status") or "") in CLOSED or n in SKIP:
            continue
        fresh = [i for i in Q.list_items("pending", source="missing-post")
                 if (i["engagement"] == n or i["engagement"].startswith(n + "-"))]
        if fresh:
            log(f"{n}: pending missing-post draft already covers it, skip")
            continue
        try:
            msgs = sl.thread(th["ts"])
        except Exception as e:
            log(f"{n}: thread read failed {e}")
            continue
        last_ts = max(float(m["ts"]) for m in msgs)
        since_dt = max(dt.datetime.fromtimestamp(last_ts), dt.datetime.combine(floor, dt.time()))
        doms = {x.lower() for x in (meta.get("domains") or [])}
        try:
            sent = gmail_sent(doms, since_dt.date())
        except Exception as e:
            log(f"{n}: gmail failed {e}")
            sent = []
        try:
            bb = bitbucket_commits({n: rx[n]}, since_dt.date()).get(n, [])
        except Exception as e:
            log(f"{n}: bitbucket failed {e}")
            bb = []
        # a thread named for the client covers its sibling engagements too
        # (the "Fresenius" thread carries fresenius-complaint-coding, fresenius-cmc, ...)
        fam = [n] + [m for m in names if m != n and m not in threads and m.startswith(n + "-")]
        has, parts = False, []
        for m in fam:
            h, dtxt = since_data(m, None, since_dt, today, rx, evs, meetings, tq,
                                 sent if m == n else [], bb if m == n else [])
            has = has or h
            if dtxt:
                parts.append((f"({m})\n" if len(fam) > 1 else "") + dtxt)
        data = "\n".join(parts)
        if not has:
            log(f"{n}: nothing new since {since_dt:%Y-%m-%d %H:%M}")
            continue
        tail = "\n".join(f"[{dt.datetime.fromtimestamp(float(m['ts'])):%Y-%m-%d %H:%M}] "
                         f"{'Ivo' if m.get('user') == IVO_SLACK else sl.name(m.get('user', ''))}: {sl.text(m)[:500]}"
                         for m in msgs[-3:])
        blocks.append(f"=== ENGAGEMENT: {n} (stage {meta.get('status', '?')}) ===\n"
                      f"[thread top line] {th['text']}\n[last thread messages]\n{tail}\n"
                      f"[NEW SINCE {since_dt:%a %-d %b %H:%M}]\n{data[:6000]}")
        metas[n] = dict(th=th, since=since_dt, sources=[dict(label="thread", path_or_url=th["permalink"]),
                                                        dict(label=f"{n}/STATUS.md", path_or_url=str(ENG / n / "STATUS.md"))])
        log(f"{n}: new since {since_dt:%Y-%m-%d %H:%M}")

    out_dir = ATLAS / "briefs" / str(iso[0]) / f"W{iso[1]:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{today}_monday-thread-updates.md"
    if not blocks:
        out.write_text(f"# Monday thread updates, {today}\n\n> DRAFT. Nothing new since the last message in any engagement thread.\n")
        log("nothing new anywhere")
        if not a.no_notify:
            notify(APPROVALS_URL, "Monday thread updates", f"Nothing new. {Q.pending_count()} drafts waiting in Approvals.")
        return

    system = SYSTEM.format(voice=voice_block())
    user = TASK.format(today=today.isoformat(), weekday=today.strftime("%a"),
                       today_label=today.strftime("%a %-d %b"), blocks="\n\n".join(blocks))
    max_out = 450 * len(blocks) + 1500   # includes thinking tokens
    est = ((len(system) + len(user)) / 3.2) * PRICE_IN + max_out * PRICE_OUT
    log(f"prompt {len(system) + len(user)} chars, {len(blocks)} engagements, est ${est:.3f}")
    if est > MAX_COST_USD:
        log(f"ABORT: est ${est:.3f} > ${MAX_COST_USD}")
        sys.exit(2)
    if a.dry:
        (ATLAS / "_autopilot" / "logs" / f"{today}_monday-threads.prompt.txt").write_text(system + "\n\n=====\n\n" + user)
        log("dry run, prompt written")
        return
    try:
        body, usage, cost = bedrock(system, user, max_tokens=max_out)
    except Exception as e:
        log(f"bedrock failed: {e}")
        if not a.no_notify:
            notify(APPROVALS_URL, "Monday thread updates failed", "Bedrock call failed (aws sso login --profile Iris_Devs?)")
        sys.exit(1)
    body = clean(body)
    drafts = []
    for blk in re.split(r"\n(?=### )", body):
        h = re.match(r"### \[([\w-]+)\]", blk)
        f = re.search(r"```text\n(.*?)```", blk, re.S)
        if not h or not f or h.group(1) not in metas:
            continue
        txt = f.group(1).strip()
        if txt.upper().startswith("SKIP"):
            log(f"{h.group(1)}: model skipped")
            continue
        drafts.append((h.group(1), txt))

    md = [f"# Monday thread updates, {today} ({week})", "",
          f"> DRAFTS. Never posted automatically. Approve per item at {APPROVALS_URL}.",
          f"> {MODEL.split('.')[-1]}, {usage['inputTokens']} in / {usage['outputTokens']} out tokens, ${cost:.3f}.", ""]
    for n, txt in drafts:
        m = metas[n]
        md += [f"## {n}", f"Thread: {m['th']['text'][:60]} ({m['th']['permalink']}), new since {m['since']:%a %-d %b %H:%M}",
               "", "```text", txt, "```", ""]
        Q.add("monday-thread", n, "slack_thread_reply", f"Thread update: {m['th']['text'][:50]}", txt,
              target=dict(channel=CHANNEL, thread_ts=m["th"]["ts"], permalink=m["th"]["permalink"]),
              sources=m["sources"] + [dict(label=f"draft {out.name}", path_or_url=str(out))],
              key=f"monday-thread:{n}:{week}")
    skipped = sorted(set(metas) - {n for n, _ in drafts})
    if skipped:
        md += ["## Skipped (new activity, nothing worth a post)", ", ".join(skipped), ""]
    out.write_text("\n".join(md))
    log(f"wrote {out}: {len(drafts)} drafts, cost ${cost:.4f}")
    if not a.no_notify:
        notify(APPROVALS_URL, "Monday thread updates", f"{len(drafts)} thread drafts. {Q.pending_count()} waiting in Approvals.")


if __name__ == "__main__":
    main()
