#!/usr/bin/env python3
"""Fetch the live transcript for a single Tactiq meeting and write it + a diff.

Reuses ../../Axion/tactiq_export/export.py for auth + GraphQL. Run repeatedly (every 2-3 min);
on each run it writes the full current transcript to _live/transcript.txt and, if
new blocks appeared since last run, appends them to _live/new_blocks.txt and prints
"NEW: <n> blocks". Otherwise prints "NO CHANGE".

NOTE: depends on Axion/tactiq_export/export.py (hardcoded Firebase tokens). When the
tactiq tooling moves into atlas/, update this path.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# atlas/_live/ -> ../../Axion/tactiq_export/
sys.path.insert(0, os.path.join(HERE, "..", "..", "Axion", "tactiq_export"))
import export  # noqa: E402

MEETING_ID = sys.argv[1] if len(sys.argv) > 1 else "8btqs919sbrISDQAvDi1"
FULL_PATH = os.path.join(HERE, "transcript.txt")
NEW_PATH = os.path.join(HERE, "new_blocks.txt")
COUNT_PATH = os.path.join(HERE, ".last_count")


def main():
    export.refresh_id_token()
    r = export.gql("meetingWithTranscript", export.MEETING_QUERY, {"meetingId": MEETING_ID})
    m = r["data"]["meeting"]
    if not m:
        print("ERROR: meeting not found")
        return 1
    t = m.get("transcript") or {}
    blocks = [b for b in t.get("blocks", []) if not b.get("isDeleted") and b.get("transcript", "").strip()]
    if not blocks:
        print("ERROR: no blocks")
        return 1
    origin = min(b["timestamp"] for b in blocks)
    lines = []
    for b in blocks:
        ts = export.fmt_ts(b["timestamp"], origin)
        spk = b.get("speakerName") or "Unknown"
        lines.append(f"[{ts}] {spk}: {b['transcript'].strip()}")
    full = "\n".join(lines)

    try:
        with open(COUNT_PATH) as f:
            last = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        last = 0

    n = len(blocks)
    with open(FULL_PATH, "w", encoding="utf-8") as f:
        f.write(f"# {m.get('title')}\n# {n} blocks · duration {m.get('duration')}s · "
                f"participants: {', '.join(p['name'] for p in (m.get('participants') or []))}\n\n")
        f.write(full + "\n")
    with open(COUNT_PATH, "w") as f:
        f.write(str(n))

    if n > last:
        new_lines = lines[last:]
        with open(NEW_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines) + "\n")
        print(f"NEW: {n - last} blocks (total {n})")
        print("--- new content ---")
        print("\n".join(new_lines))
    elif n < last:
        # transcript shrank (re-segmentation) — treat whole thing as fresh-ish, but don't spam
        print(f"RESET: now {n} blocks (was {last}); full transcript rewritten")
    else:
        print(f"NO CHANGE ({n} blocks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
