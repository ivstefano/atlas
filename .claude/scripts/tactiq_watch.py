#!/usr/bin/env python3
"""Watch a live Tactiq meeting transcript for new blocks (poll mode).

Run repeatedly (every 2-3 min during a meeting); on each run it writes the full
current transcript to _live/transcript.txt and, if new blocks appeared since the
last run, appends them to _live/new_blocks.txt and prints "NEW: <n> blocks".
Otherwise prints "NO CHANGE".

Usage:
    tactiq_watch.py <meeting_id>

Output files go into atlas/_live/.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tactiq_client as tc  # noqa: E402

ATLAS_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
LIVE_DIR = os.path.join(ATLAS_ROOT, "_live")
# Note: _live/ is gitignored. If it doesn't exist, this script creates it on first run.
FULL_PATH = os.path.join(LIVE_DIR, "transcript.txt")
NEW_PATH = os.path.join(LIVE_DIR, "new_blocks.txt")
COUNT_PATH = os.path.join(LIVE_DIR, ".last_count")


def main():
    if len(sys.argv) < 2:
        print("usage: tactiq_watch.py <meeting_id>", file=sys.stderr)
        return 1
    meeting_id = tc.extract_meeting_id(sys.argv[1])

    os.makedirs(LIVE_DIR, exist_ok=True)

    header, body = tc.fetch_meeting(meeting_id)
    lines = body.split("\n")
    n = len(lines)

    # Header + body to the persistent live transcript
    with open(FULL_PATH, "w", encoding="utf-8") as f:
        f.write(f"# {header['title']}\n")
        f.write(f"# {n} blocks · duration {header['duration_s']}s · "
                f"participants: {', '.join(header['participants'])}\n\n")
        f.write(body + "\n")

    try:
        with open(COUNT_PATH) as f:
            last = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        last = 0

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
        print(f"RESET: now {n} blocks (was {last}); full transcript rewritten")
    else:
        print(f"NO CHANGE ({n} blocks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
