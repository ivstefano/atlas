#!/usr/bin/env python3
"""Prepare a post-meeting digest context block for Claude to process in-session.

This script does NOT call any LLM. It builds a structured prompt:
- Identifies the engagement from the transcript path.
- Classifies external (client present) vs internal (all-IRIS).
- Loads relevant engagement state (CONTEXT.md core, last ~3 STATUS entries).
- Embeds the transcript body.
- Surfaces a target STATUS path + convention pointers.

Usage:
    post_meeting_digest.py <path-to-transcript.txt>

Output: a markdown context block on stdout. The caller (slash command or skill)
hands it to Claude in-session to produce the digest + drafts.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

ATLAS_ROOT = Path(__file__).resolve().parent.parent.parent
ENGAGEMENTS_ROOT = ATLAS_ROOT.parent / "engagements"

# IRIS team — names that mark "internal participant". Extracted from memory/iris-people.md.
# When extending, add only first-name + last-name forms that actually appear in transcripts.
IRIS_PEOPLE = {
    "ivo stefanov", "ivaylo stefanov", "ivo",
    "ivan tsenov", "vankata tsenov", "vankata", "vanka", "wanka", "ivan_tsenov",
    "borislava", "borislava bagaliyska", "bobi", "bobby",
    "martina", "martina bilyanska", "marti",
    "matyo", "matyo ivanov",
    "viktor botev", "victor botev", "viktor", "victor",
    "jordan ryken", "jordan",
    "steven fung", "steven", "steven iris ai", "steven iris",
    "michael sica-lieber",
    "petar ivanov",
    "martin kondov",
    "william le roux",
    "aleksandar georgiev", "aleksandar",
    "liana hakobyan", "liana",
    "ada kretkowska", "ada",
    "rosen krumov", "rosen",
    "hatche halil", "hatche",
    "anita",
    "volodymyr krekhovetskyi", "vova",
    "vladimir mikov", "vladimir",
    "vladi",
    "yevhenii kondratiev", "yevhenii",
    "yovcho gandjurov",
    "roman sierikov",
    "denis",
    "ivan",
    "amine",
    "shtiliyan",
    "iryna wight",
    "william",
    "ahmed",
    "iris ai as' notetaker",
}


def parse_transcript_header(path):
    """Extract metadata from transcript file header."""
    meta = {
        "title": None,
        "date": None,
        "meeting_id": None,
        "duration_s": None,
        "participants": [],
        "language": None,
        "body": "",
    }
    with open(path, encoding="utf-8") as f:
        text = f.read()

    # Header style 1 (from tactiq_export.py): Title: foo / Date: ... / etc, separator "===..."
    if text.startswith("Title:"):
        head, _, body = text.partition("\n" + "=" * 60 + "\n\n")
        meta["body"] = body.strip()
        for line in head.splitlines():
            if line.startswith("Title:"):
                meta["title"] = line[len("Title:"):].strip()
            elif line.startswith("Date:"):
                meta["date"] = line[len("Date:"):].strip()
            elif line.startswith("Meeting ID:"):
                meta["meeting_id"] = line[len("Meeting ID:"):].strip()
            elif line.startswith("Duration:"):
                m = re.search(r"(\d+)", line)
                if m:
                    meta["duration_s"] = int(m.group(1))
            elif line.startswith("Participants:"):
                ps = line[len("Participants:"):].strip()
                meta["participants"] = [p.strip() for p in ps.split(",") if p.strip()]
            elif line.startswith("Language:"):
                meta["language"] = line[len("Language:"):].strip()
        return meta

    # Header style 2 (from tactiq_watch.py): # Title \n # N blocks · ... · participants: ...
    if text.startswith("# "):
        lines = text.splitlines()
        meta["title"] = lines[0][2:].strip()
        if len(lines) > 1 and "participants:" in lines[1]:
            ps = lines[1].split("participants:")[1].strip()
            meta["participants"] = [p.strip() for p in ps.split(",") if p.strip()]
        # Body starts after first blank line
        try:
            blank_idx = next(i for i, ln in enumerate(lines) if ln == "")
            meta["body"] = "\n".join(lines[blank_idx + 1:]).strip()
        except StopIteration:
            meta["body"] = "\n".join(lines[2:]).strip()
        # Derive date from filename if not in header
        fname_date = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(path))
        if fname_date:
            meta["date"] = fname_date.group(1)
        return meta

    # Fallback: derive date from filename anyway
    fname_date = re.search(r"(\d{4}-\d{2}-\d{2})", os.path.basename(path))
    if fname_date and not meta["date"]:
        meta["date"] = fname_date.group(1)

    # No recognised header — treat whole thing as body
    meta["body"] = text.strip()
    return meta


def classify_meeting(participants):
    """Return ('external' | 'internal', external_participants, internal_participants)."""
    external = []
    internal = []
    for p in participants:
        # Strip @ mentions and email-like decorations
        key = re.sub(r"\s*@.*$", "", p).strip().lower()
        key = re.sub(r"\(.*?\)", "", key).strip()
        if key in IRIS_PEOPLE:
            internal.append(p)
        else:
            # Heuristic: if name has Cyrillic, probably internal (lots of Bulgarian colleagues)
            # but only when other markers don't override
            external.append(p)
    kind = "external" if external else "internal"
    return kind, external, internal


def find_engagement(transcript_path):
    """Infer engagement context from transcript path.

    Returns dict with: client | thread, folder_path, stage, target_status_path.
    """
    p = Path(transcript_path).resolve()
    try:
        rel = p.relative_to(ENGAGEMENTS_ROOT)
    except ValueError:
        return {"kind": "unknown", "folder": None, "stage": None, "target_status": None}

    parts = rel.parts
    if not parts:
        return {"kind": "unknown", "folder": None, "stage": None, "target_status": None}

    first = parts[0]
    if first == "_internal":
        # engagements/_internal/<thread>/meetings/<file>
        if len(parts) >= 3:
            thread = parts[1]
            folder = ENGAGEMENTS_ROOT / "_internal" / thread
            return {
                "kind": "internal",
                "thread": thread,
                "folder": folder,
                "stage": None,
                "target_status": folder / "STATUS.md" if (folder / "STATUS.md").exists() else None,
            }
        return {"kind": "internal-misc", "folder": None, "stage": None, "target_status": None}

    # Client engagement: engagements/<client>/<stage>/transcripts/<file>
    client = first
    stage = parts[1] if len(parts) > 1 else None
    folder = ENGAGEMENTS_ROOT / client
    return {
        "kind": "client",
        "client": client,
        "folder": folder,
        "stage": stage,
        "target_status": folder / "STATUS.md",
    }


def load_engagement_state(eng):
    """Load CONTEXT.md core + last ~3 STATUS entries."""
    folder = eng.get("folder")
    if not folder or not folder.exists():
        return {"context_excerpt": None, "status_recent": None}

    context_path = folder / "CONTEXT.md"
    status_path = folder / "STATUS.md"
    out = {"context_excerpt": None, "status_recent": None}

    if context_path.exists():
        text = context_path.read_text(encoding="utf-8")
        # First ~80 lines or up to second "##" section, whichever is shorter
        lines = text.splitlines()
        cut = min(80, len(lines))
        for i, line in enumerate(lines[1:], 1):  # skip title
            if i > 5 and line.startswith("## "):
                cut = i
                break
        out["context_excerpt"] = "\n".join(lines[:cut])

    if status_path.exists():
        text = status_path.read_text(encoding="utf-8")
        # Last ~3 entries (entries delimited by "## " headers)
        entries = re.split(r"^## ", text, flags=re.MULTILINE)
        # entries[0] = preamble; entries[1..] are the dated blocks
        if len(entries) > 1:
            last3 = entries[1:4]  # newest 3 (status is newest-on-top)
            out["status_recent"] = "\n\n".join("## " + e.rstrip() for e in last3)
        else:
            out["status_recent"] = text[:2000]
    return out


def render_prompt(transcript_path, meta, classification, eng, state):
    """Render the markdown context block Claude will process."""
    kind, external, internal = classification
    out = []
    out.append("# Post-meeting digest context")
    out.append("")
    out.append(f"**Transcript**: `{transcript_path}`")
    out.append(f"**Meeting**: {meta.get('title') or '(no title)'}")
    out.append(f"**Date**: {meta.get('date') or '(unknown)'}")
    if meta.get('duration_s'):
        m, s = divmod(meta['duration_s'], 60)
        out.append(f"**Duration**: {m}m {s}s")
    out.append(f"**Classification**: **{kind.upper()}**")
    if external:
        out.append(f"**External participants**: {', '.join(external)}")
    if internal:
        out.append(f"**Internal participants**: {', '.join(internal)}")
    out.append("")

    # Engagement context
    out.append("## Engagement")
    if eng["kind"] == "client":
        out.append(f"- **Client**: `{eng['client']}` (active engagement)")
        out.append(f"- **Stage folder**: `{eng['stage']}`")
        out.append(f"- **Folder**: `{eng['folder']}`")
        out.append(f"- **Target STATUS**: `{eng['target_status']}`")
    elif eng["kind"] == "internal":
        out.append(f"- **Internal thread**: `{eng['thread']}`")
        out.append(f"- **Folder**: `{eng['folder']}`")
        if eng['target_status']:
            out.append(f"- **Target STATUS**: `{eng['target_status']}`")
        else:
            out.append("- **Target STATUS**: (no STATUS.md exists — append to thread's STATUS.md or note this is rhythm-folder content)")
    else:
        out.append(f"- **Engagement could not be inferred** from path: `{transcript_path}`")
        out.append("- Ask the user where to file this.")
    out.append("")

    # Engagement state
    if state.get("context_excerpt"):
        out.append("## CONTEXT.md (excerpt)")
        out.append("")
        out.append("```markdown")
        out.append(state["context_excerpt"])
        out.append("```")
        out.append("")

    if state.get("status_recent"):
        out.append("## STATUS.md (recent entries)")
        out.append("")
        out.append("```markdown")
        out.append(state["status_recent"])
        out.append("```")
        out.append("")

    # Transcript body
    out.append("## Transcript body")
    out.append("")
    out.append("```")
    out.append(meta["body"])
    out.append("```")
    out.append("")

    # Instructions
    out.append("---")
    out.append("")
    out.append("## Your task")
    out.append("")
    if kind == "external":
        out.append("Generate (do NOT write to files yet, surface as drafts for review):")
        out.append("")
        out.append("1. **STATUS.md entry** — newest-on-top format, dated `## YYYY-MM-DD: <one-line summary>`. Include: what happened (3-6 bullets), decisions made, blockers if any, next action with owner + date. Keep tone factual, third-person.")
        out.append("2. **Follow-up email draft** — to the external attendees. Subject line + body. Use house style: no em-dashes, terse, lead with the commercial gate if there is one. Never auto-send.")
        out.append("3. **Action items table** — IRIS owns / they own / mutual. Each row: action, owner, date.")
        out.append("4. **Commercial state delta** — if stage changed (e.g. scoping → PoC, PoC → contracting), flag it for COMMERCIAL.md update and HubSpot/Asana sync.")
    else:
        out.append("Generate (do NOT write to files yet, surface as drafts for review):")
        out.append("")
        out.append("1. **STATUS.md entry** — newest-on-top format, dated `## YYYY-MM-DD: <one-line summary>`. Append to the target STATUS.md. Include: what happened (3-6 bullets), decisions, blockers, next action with owner + date.")
        out.append("2. **Internal Slack message draft** — to the most relevant channel (ask the user which). Casual, direct, links to the STATUS entry.")
        out.append("3. **Action items list** — owners + dates. Mine vs others.")
    out.append("")
    out.append("After review and approval, write the STATUS.md entry. Surface the email/Slack draft for the user to copy-paste manually (never auto-send).")
    out.append("")
    out.append("Style references:")
    out.append("- Global: `~/.claude/CLAUDE.md` (House Style: no em-dashes, terse, no trailing summaries).")
    out.append("- For external emails: `~/.claude/projects/-Users-iris-Documents-atlas/memory/email-drafting-style.md`, `ivo-voice-profile.md`, `comms-style-improvements.md`.")
    out.append("- For STATUS entries: existing entries in the same STATUS.md (match the format).")

    return "\n".join(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("transcript", help="Path to the transcript .txt file")
    p.add_argument("--json", action="store_true", help="Output raw JSON instead of markdown prompt (for headless / loop use)")
    args = p.parse_args()

    transcript_path = os.path.abspath(args.transcript)
    if not os.path.exists(transcript_path):
        print(f"ERROR: transcript not found: {transcript_path}", file=sys.stderr)
        return 1

    meta = parse_transcript_header(transcript_path)
    classification = classify_meeting(meta["participants"])
    eng = find_engagement(transcript_path)
    state = load_engagement_state(eng)

    if args.json:
        out = {
            "transcript_path": transcript_path,
            "meta": meta,
            "classification": {
                "kind": classification[0],
                "external": classification[1],
                "internal": classification[2],
            },
            "engagement": {k: str(v) if isinstance(v, Path) else v for k, v in eng.items()},
            "state": state,
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(render_prompt(transcript_path, meta, classification, eng, state))

    return 0


if __name__ == "__main__":
    sys.exit(main())
