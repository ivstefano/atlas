#!/usr/bin/env python3
"""Gap-recovery scan: surface what happened across atlas + engagements since the last brief.

Returns a structured report (markdown) that the morning-brief flow integrates. No LLM calls.

Usage:
    gap_scan.py [--since YYYY-MM-DD] [--json]

Without --since: uses filename date of the most recent brief in briefs/YYYY/W*/.

Sources covered (offline only — git + filesystem):
- Git log on engagements/ in the gap.
- Git log on atlas/ in the gap.
- New transcripts in engagements/*/transcripts/ since last brief.
- Open STATUS "next action" lines from every engagement's STATUS.md.

Sources NOT covered here (live MCP calls; the calling skill/command pulls these in parallel):
- Gmail threads in the gap.
- Slack messages in the gap.
- Asana task state changes.
- Calendar events that happened in the gap.

The split keeps this script fast + offline-runnable. The expensive MCP calls happen in
the calling Claude session where pagination/auth is already set up.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ATLAS_ROOT = Path(__file__).resolve().parent.parent.parent
ENG_ROOT = ATLAS_ROOT.parent / "engagements"
BRIEFS_ROOT = ATLAS_ROOT / "briefs"


def latest_brief_date():
    """Find the most recent brief file's date (from filename YYYY-MM-DD prefix)."""
    candidates = []
    for p in BRIEFS_ROOT.rglob("*.md"):
        m = re.match(r"(\d{4}-\d{2}-\d{2})", p.name)
        if m:
            candidates.append(m.group(1))
    return max(candidates) if candidates else None


def git_log(repo, since, until):
    """Return list of {date, subject, files} for commits in window."""
    try:
        out = subprocess.run(
            ["git", "log",
             f"--since={since}", f"--until={until}",
             "--pretty=format:===%ad %s", "--date=short", "--name-only"],
            cwd=repo, capture_output=True, text=True, check=True
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

    commits = []
    current = None
    for line in out.splitlines():
        if line.startswith("==="):
            if current:
                commits.append(current)
            parts = line[3:].split(" ", 1)
            date = parts[0]
            subject = parts[1] if len(parts) > 1 else ""
            current = {"date": date, "subject": subject, "files": []}
        elif line.strip():
            if current:
                current["files"].append(line.strip())
    if current:
        commits.append(current)
    return commits


def new_transcripts(since):
    """Find transcripts in engagements/*/transcripts/ with mtime newer than since."""
    since_dt = datetime.strptime(since, "%Y-%m-%d")
    found = []
    for tdir in ENG_ROOT.rglob("transcripts"):
        if not tdir.is_dir() or tdir.is_symlink():
            continue
        for f in tdir.glob("*.txt"):
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if mtime >= since_dt:
                m = re.match(r"(\d{4}-\d{2}-\d{2})", f.name)
                date_from_name = m.group(1) if m else None
                rel = f.relative_to(ENG_ROOT)
                eng = rel.parts[0]
                found.append({
                    "engagement": eng,
                    "path": str(rel),
                    "mtime": mtime.isoformat(),
                    "date_from_name": date_from_name,
                })
    found.sort(key=lambda x: x["mtime"], reverse=True)
    return found


def open_next_actions():
    """Scan every engagement STATUS.md for the latest 'Next action:' line."""
    items = []
    for status_path in ENG_ROOT.glob("*/STATUS.md"):
        eng = status_path.parent.name
        if eng.startswith("_"):
            continue
        try:
            text = status_path.read_text(encoding="utf-8")
        except Exception:
            continue
        entries = re.split(r"^## ", text, flags=re.MULTILINE)
        if len(entries) < 2:
            continue
        first_entry = "## " + entries[1]
        summary = first_entry.splitlines()[0].lstrip("#").strip()
        m = re.search(r"^-?\s*\*?\*?Next action\*?\*?:?\s*(.+?)$",
                      first_entry, flags=re.MULTILINE | re.IGNORECASE)
        action = m.group(1).strip() if m else None
        if action:
            items.append({"engagement": eng, "summary": summary, "next_action": action})
    return items


def render_markdown(since, gap_days, eng_commits, atlas_commits, transcripts, actions):
    out = []
    out.append("# Gap-recovery scan")
    out.append("")
    out.append(f"**Window**: {since} to today ({gap_days} day{'s' if gap_days != 1 else ''})")
    out.append("")

    by_eng = {}
    for c in eng_commits:
        for f in c["files"]:
            parts = f.split("/")
            if not parts or parts[0].startswith("_"):
                continue
            eng = parts[0]
            by_eng.setdefault(eng, []).append({"date": c["date"], "subject": c["subject"], "file": f})

    out.append("## Engagement-side changes (git)")
    out.append("")
    if not by_eng:
        out.append("No engagement file changes in the window.")
    else:
        for eng in sorted(by_eng):
            out.append(f"### {eng}")
            seen_subjects = set()
            for entry in by_eng[eng]:
                key = (entry["date"], entry["subject"])
                if key in seen_subjects:
                    continue
                seen_subjects.add(key)
                out.append(f"- {entry['date']}: {entry['subject']}")
            out.append("")

    out.append("## Atlas-side changes (git)")
    out.append("")
    if not atlas_commits:
        out.append("No atlas changes in the window.")
    else:
        for c in atlas_commits:
            out.append(f"- {c['date']}: {c['subject']}")
    out.append("")

    out.append("## New transcripts since last brief")
    out.append("")
    if not transcripts:
        out.append("No new transcripts.")
    else:
        for t in transcripts:
            out.append(f"- `{t['path']}` (mtime {t['mtime'][:10]})")
    out.append("")

    out.append("## Open 'next action' items (from latest STATUS entries)")
    out.append("")
    if not actions:
        out.append("No explicit next-action lines found.")
    else:
        for a in actions:
            out.append(f"- **{a['engagement']}**: {a['next_action']}")
            out.append(f"  ↳ from: _{a['summary']}_")
    out.append("")

    out.append("---")
    out.append("")
    out.append("## Sources NOT covered by this scan (need MCP calls in the brief flow)")
    out.append("")
    out.append("- **Calendar events in the gap** — `mcp__claude_ai_Google_Calendar__list_events`.")
    out.append("- **Gmail threads in the gap** — `mcp__claude_ai_Gmail__search_threads` with `newer_than:` filter.")
    out.append("- **Slack messages in the gap** — `mcp__slack__conversations_history` for relevant channels + DMs.")
    out.append("- **Asana task state changes** — `mcp__asana__list_tasks` modified in window.")

    return "\n".join(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--since", help="YYYY-MM-DD; default: most recent brief")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    since = args.since or latest_brief_date()
    if not since:
        print("ERROR: no prior briefs found and --since not provided", file=sys.stderr)
        return 1

    today = datetime.now().strftime("%Y-%m-%d")
    gap_days = (datetime.strptime(today, "%Y-%m-%d") - datetime.strptime(since, "%Y-%m-%d")).days

    eng_commits = git_log(ENG_ROOT, since, today)
    atlas_commits = git_log(ATLAS_ROOT, since, today)
    transcripts = new_transcripts(since)
    actions = open_next_actions()

    if args.json:
        print(json.dumps({
            "since": since,
            "today": today,
            "gap_days": gap_days,
            "engagement_commits": eng_commits,
            "atlas_commits": atlas_commits,
            "new_transcripts": transcripts,
            "open_next_actions": actions,
        }, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(since, gap_days, eng_commits, atlas_commits, transcripts, actions))
    return 0


if __name__ == "__main__":
    sys.exit(main())
