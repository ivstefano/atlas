#!/usr/bin/env python3
"""Read-only helper for /wrap: what did this session touch, where does it get committed,
and how much meta-work (own tooling) happened this week vs the cap.

Usage:
  wrap.py                      # report for the current session (CLAUDE_CODE_SESSION_ID)
  wrap.py --session <id>       # any past session, by id
  wrap.py --transcript <path>  # any past session, by JSONL path
  wrap.py --json               # machine-readable
  wrap.py meta [--week-of YYYY-MM-DD] [-v]   # meta-work hours vs cap only

Never writes, commits or pushes. /wrap (the command) does that, from this report.

Touched files = file_path of Edit / Write / MultiEdit / NotebookEdit tool_use blocks in the
session JSONL plus its subagents/*.jsonl. Files written via Bash (cp, mv, heredoc, scripts)
are not in tool_use inputs: they show up as "dirty, not confirmed" candidates (dirty in a
touched repo, mtime inside the session window). /wrap must ask before committing those.

Meta-work heuristic (cheap, documented, not exact):
  - Scan ~/.claude/projects/*/*.jsonl modified since Monday 00:00 local.
  - A session is META if its cwd is under a tooling repo (Cognion, capabilities,
    digital-twin-ivo) OR at least half of its non-scratch file edits (own + subagents) land in
    infra paths: atlas/.claude, atlas/_autopilot, atlas/_config, ~/.claude (not projects/),
    ~/.config, Cognion, capabilities, digital-twin-ivo. Edits to atlas/_state (bookkeeping)
    and /tmp scratch are ignored. Bash-only infra sessions are missed (undercount).
  - Hours = active time: sum of gaps between consecutive message timestamps, each gap capped
    at 5 min (idle cutoff), only gaps inside the week. Subagent time overlaps its parent, so
    it is not added.
  - Cap: _autopilot/config.json `meta_cap_hours_week` (default 5), via autopilot_common.meta_cap_hours().
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from state_common import resolve_task, ATLAS, ENGAGEMENTS, HOME  # noqa: E402

PROJECTS = HOME / ".claude" / "projects"
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
IDLE_CAP_S = 300
WT_RX = re.compile(r"/\.claude/worktrees/[^/]+(?=/|$)")      # atlas/.claude/worktrees/<n>/x -> atlas/x
TOOLING_REPOS = [HOME / "Documents" / n for n in ("Cognion", "capabilities", "digital-twin-ivo")]
INFRA_ROOTS = [ATLAS / ".claude", ATLAS / "_autopilot", ATLAS / "_config",
               HOME / ".claude", HOME / ".config", *TOOLING_REPOS]
INFRA_EXCLUDE = [HOME / ".claude" / "projects", ATLAS / ".claude" / "worktrees"]
SCRATCH = ["/tmp/", "/private/tmp/", "/var/folders/", str(PROJECTS) + "/"]


def meta_cap():
    try:
        from autopilot_common import meta_cap_hours
        return meta_cap_hours()
    except Exception:
        return 5.0


# ----------------------------------------------------------------------------- transcript
def find_transcript(session=None, transcript=None):
    if transcript:
        return Path(transcript)
    sid = session or os.environ.get("CLAUDE_CODE_SESSION_ID")
    if not sid:
        return None
    hits = glob.glob(str(PROJECTS / "*" / f"{sid}.jsonl"))
    return Path(max(hits, key=os.path.getmtime)) if hits else None


def subagent_files(tp):
    return sorted((tp.parent / tp.stem / "subagents").glob("*.jsonl")) if tp else []


def ts(s):
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def scan(path):
    """-> (edits [(ts, tool, path)], timestamps [datetime], first cwd)."""
    edits, stamps, cwd = [], [], None
    try:
        fh = open(path, errors="ignore")
    except OSError:
        return edits, stamps, cwd
    with fh:
        for ln in fh:
            if '"timestamp"' not in ln:
                continue
            try:
                o = json.loads(ln)
            except ValueError:
                continue
            t = ts(o.get("timestamp"))
            if t and o.get("type") in ("user", "assistant"):
                stamps.append(t)
            cwd = cwd or o.get("cwd")
            m = o.get("message")
            if o.get("type") != "assistant" or not isinstance(m, dict) or not isinstance(m.get("content"), list):
                continue
            for c in m["content"]:
                if isinstance(c, dict) and c.get("type") == "tool_use" and c.get("name") in EDIT_TOOLS:
                    inp = c.get("input") or {}
                    p = inp.get("file_path") or inp.get("notebook_path")
                    if p:
                        edits.append((t, c["name"], p))
    return edits, stamps, cwd


# ----------------------------------------------------------------------------- git
def git(cwd, *args, strip=True):
    try:
        r = subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True, timeout=20)
        return (r.stdout.strip() if strip else r.stdout) if r.returncode == 0 else None
    except Exception:
        return None


def existing_parent(p):
    p = Path(p)
    while not p.exists() and p != p.parent:
        p = p.parent
    return p if p.is_dir() else p.parent


def repo_of(path, cache={}):
    d = existing_parent(path)
    if d not in cache:
        cache[d] = git(d, "rev-parse", "--show-toplevel")
    return cache[d]


def porcelain(repo):
    """{relpath: XY} for dirty files in repo."""
    out = {}
    raw = git(repo, "status", "--porcelain", "-uall", "-z", strip=False) or ""
    items = raw.split("\0")
    i = 0
    while i < len(items):
        e = items[i]
        if len(e) > 3:
            xy, rel = e[:2], e[3:]
            out[rel] = xy
            if xy[0] in "RC":
                i += 1   # skip rename source
        i += 1
    return out


def worktree_info(cwd):
    gd, cd = git(cwd, "rev-parse", "--absolute-git-dir"), git(cwd, "rev-parse", "--path-format=absolute", "--git-common-dir")
    if not gd or not cd or Path(gd) == Path(cd):
        return None
    return {"path": git(cwd, "rev-parse", "--show-toplevel"), "branch": git(cwd, "branch", "--show-current"),
            "main_repo": str(Path(cd).parent)}


def engagement_of(path):
    try:
        parts = Path(path).resolve().relative_to(ENGAGEMENTS.resolve()).parts
    except ValueError:
        return None
    return parts[0] if parts and not parts[0].startswith((".", "_")) and len(parts) > 1 else None


def in_artefacts(eng, path):
    af = ENGAGEMENTS / eng / "ARTEFACTS.md"
    try:
        txt = af.read_text(errors="ignore")
    except OSError:
        return False
    rel = str(Path(path).resolve().relative_to((ENGAGEMENTS / eng).resolve()))
    return rel in txt or Path(path).name in txt


# ----------------------------------------------------------------------------- session report
def session_report(tp):
    files = [tp, *subagent_files(tp)]
    edits, stamps, cwd = [], [], None
    for i, f in enumerate(files):
        e, s, c = scan(f)
        edits += e
        if i == 0:
            stamps, cwd = s, c
    start = min(stamps) if stamps else None
    seen = {}
    for t, tool, p in edits:
        seen.setdefault(p, {"tools": set(), "last": t})["tools"].add(tool)
        seen[p]["last"] = t or seen[p]["last"]

    repos, outside = {}, []
    for p, info in seen.items():
        if any(p.startswith(s) for s in SCRATCH):
            continue
        r = repo_of(p)
        if not r:
            outside.append(p)
            continue
        repos.setdefault(r, {"confirmed": [], "candidates": []})
        repos[r]["confirmed"].append(p)

    for r, bucket in repos.items():
        st = porcelain(r)
        conf = set()
        rows = []
        for p in sorted(bucket["confirmed"]):
            rel = os.path.relpath(Path(p).resolve(), Path(r).resolve()) if Path(p).exists() else os.path.relpath(p, r)
            conf.add(rel)
            state = st.get(rel)
            ignored = state is None and git(r, "check-ignore", "-q", rel) is not None
            rows.append({"path": p, "rel": rel, "git": (state or ("ignored" if ignored else "clean")).strip() or "clean",
                         "engagement": engagement_of(p),
                         "in_artefacts": (in_artefacts(engagement_of(p), p) if engagement_of(p) else None)})
        bucket["confirmed"] = rows
        # Bash-written candidates: dirty, not in edit list, mtime inside session window
        if start:
            for rel, xy in st.items():
                if rel in conf:
                    continue
                fp = Path(r) / rel
                try:
                    mt = dt.datetime.fromtimestamp(fp.stat().st_mtime, dt.timezone.utc)
                except OSError:
                    continue
                if mt >= start:
                    bucket["candidates"].append({"rel": rel, "git": xy.strip()})
        bucket["branch"] = git(r, "branch", "--show-current")
        up = git(r, "rev-list", "--count", "@{u}..HEAD")
        bucket["unpushed"] = int(up) if up and up.isdigit() else None
        bucket["remote"] = git(r, "remote", "get-url", "origin")

    cwd = cwd or os.getcwd()
    return {"transcript": str(tp), "subagents": len(files) - 1, "cwd": cwd,
            "task": resolve_task(WT_RX.sub("", cwd)), "start": start.isoformat() if start else None,
            "worktree": worktree_info(cwd), "repos": repos, "outside_repos": sorted(outside)}


# ----------------------------------------------------------------------------- meta-work
def norm(p):
    return Path(WT_RX.sub("", p))


def under(p, roots):
    return any(p == r or r in p.parents for r in roots)


def is_infra(p):
    p = norm(p)
    return under(p, INFRA_ROOTS) and not under(p, INFRA_EXCLUDE)


def classify(cwd, edits):
    c = norm(cwd or "")
    if under(c, TOOLING_REPOS):
        return True, "tooling repo cwd"
    real = [p for _, _, p in edits
            if not any(p.startswith(s) for s in SCRATCH) and not under(norm(p), [ATLAS / "_state"])]
    infra = sum(is_infra(p) for p in real)
    if infra and infra * 2 >= len(real):
        return True, f"{infra}/{len(real)} edits infra"
    return False, f"{infra}/{len(real)} edits infra"


def active_seconds(stamps, since):
    stamps = sorted(t for t in stamps if t >= since)
    return sum(min((b - a).total_seconds(), IDLE_CAP_S) for a, b in zip(stamps, stamps[1:]))


def meta_week(week_of=None, verbose=False):
    day = week_of or dt.date.today()
    monday = day - dt.timedelta(days=day.weekday())
    since = dt.datetime.combine(monday, dt.time()).astimezone()
    until = since + dt.timedelta(days=7)
    total, rows = 0.0, []
    for f in glob.glob(str(PROJECTS / "*" / "*.jsonl")):
        if os.path.getmtime(f) < since.timestamp():
            continue
        tp = Path(f)
        edits, stamps, cwd = scan(tp)
        for sf in subagent_files(tp):
            edits += scan(sf)[0]
        stamps = [t for t in stamps if t < until]
        secs = active_seconds(stamps, since)
        if secs < 60:
            continue
        meta, why = classify(cwd, edits)
        if meta:
            total += secs
        rows.append((meta, secs / 3600, tp.stem[:8], cwd, why))
    out = {"week": monday.isoformat(), "hours": round(total / 3600, 1), "cap": meta_cap()}
    if verbose:
        out["sessions"] = [{"meta": m, "h": round(h, 2), "id": i, "cwd": c, "why": w}
                           for m, h, i, c, w in sorted(rows, key=lambda r: (-r[0], -r[1]))]
    return out


# ----------------------------------------------------------------------------- output
def print_report(rep, meta):
    print(f"session {Path(rep['transcript']).stem}  (+{rep['subagents']} subagents)  task={rep['task']}  start={rep['start']}")
    print(f"cwd {rep['cwd']}")
    wt = rep["worktree"]
    if wt:
        print(f"WORKTREE {wt['path']}  branch={wt['branch']}  main repo={wt['main_repo']}")
    for r, b in rep["repos"].items():
        print(f"\n[{r}]  branch={b['branch']}  unpushed={b['unpushed']}  remote={b['remote']}")
        for x in b["confirmed"]:
            tag = ""
            if x["engagement"]:
                tag = f"  eng={x['engagement']}" + ("" if x["in_artefacts"] else "  NOT-IN-ARTEFACTS")
            print(f"  {x['git']:>7}  {x['rel']}{tag}")
        if b["candidates"]:
            print("  dirty, not confirmed (Bash-written or someone else's, ask):")
            for x in b["candidates"]:
                print(f"  {x['git']:>7}  {x['rel']}")
    if rep["outside_repos"]:
        print("\noutside any repo:")
        for p in rep["outside_repos"]:
            print(f"  {p}")
    if meta:
        flag = "  OVER CAP" if meta["hours"] > meta["cap"] else ""
        print(f"\nmeta-work week {meta['week']}: {meta['hours']} h / {meta['cap']:g} h cap{flag}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", nargs="?", default="session", choices=["session", "meta"])
    ap.add_argument("--session")
    ap.add_argument("--transcript")
    ap.add_argument("--week-of", type=dt.date.fromisoformat)
    ap.add_argument("--no-meta", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()

    if a.mode == "meta":
        m = meta_week(a.week_of, a.verbose)
        if a.json:
            print(json.dumps(m, indent=1))
        else:
            print(f"meta-work week {m['week']}: {m['hours']} h / {m['cap']:g} h cap")
            for s in m.get("sessions", []):
                print(f"  {'META' if s['meta'] else '    '} {s['h']:5.2f}h {s['id']} {s['cwd']}  ({s['why']})")
        return

    tp = find_transcript(a.session, a.transcript)
    if not tp or not tp.exists():
        sys.exit("no transcript: set CLAUDE_CODE_SESSION_ID or pass --session/--transcript")
    rep = session_report(tp)
    meta = None if a.no_meta else meta_week(a.week_of)
    if a.json:
        print(json.dumps({**rep, "meta": meta}, indent=1, default=str))
    else:
        print_report(rep, meta)


if __name__ == "__main__":
    main()
