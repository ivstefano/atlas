#!/usr/bin/env python3
"""Pull a single Tactiq transcript into a target directory with proper naming.

Usage:
    tactiq_pull.py <meeting_id_or_url> [--dest <dir>] [--print]

Examples:
    # Print to stdout (don't write a file):
    tactiq_pull.py 8btqs919sbrISDQAvDi1 --print

    # Write to a specific transcripts/ folder:
    tactiq_pull.py 8btqs919sbrISDQAvDi1 --dest engagements/heineken/4_poc/transcripts/

    # URL form:
    tactiq_pull.py https://app.tactiq.io/meeting/8btqs919sbrISDQAvDi1 --dest <...>

Naming convention: <YYYY-MM-DD>_<Title_With_Underscores>.txt (hash suffix dropped).
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tactiq_client as tc  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("meeting", help="Tactiq meeting ID or URL")
    p.add_argument("--dest", help="Output directory. If omitted, prints to stdout.")
    p.add_argument("--print", action="store_true", help="Print the transcript to stdout (also).")
    args = p.parse_args()

    meeting_id = tc.extract_meeting_id(args.meeting)
    header, body = tc.fetch_meeting(meeting_id)
    full = tc.render_with_header(header, body)

    if args.print or not args.dest:
        sys.stdout.write(full)
        if not args.dest:
            return 0

    fname = f"{header['date']}_{tc.slug(header['title'])}.txt"
    os.makedirs(args.dest, exist_ok=True)
    path = os.path.join(args.dest, fname)
    if os.path.exists(path):
        print(f"SKIP (already exists): {path}", file=sys.stderr)
        return 0
    with open(path, "w", encoding="utf-8") as f:
        f.write(full)
    print(f"WROTE: {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
