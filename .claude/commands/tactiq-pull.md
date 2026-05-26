---
description: Pull a Tactiq meeting transcript by ID or URL into an engagement's transcripts/ folder.
---

# /tactiq-pull

Pull one Tactiq transcript and file it.

## Argument

A Tactiq meeting ID (e.g. `8btqs919sbrISDQAvDi1`) or full URL (`https://app.tactiq.io/meeting/8btqs919sbrISDQAvDi1`). Required.

## What you do

1. Run `python3 .claude/scripts/tactiq_pull.py "$ARG" --print` to fetch the transcript and read the header (date, title, participants).
2. From participants, decide where the transcript belongs:
   - External client attendees → `engagements/<client>/<stage>/transcripts/`
   - All-IRIS → `engagements/_internal/<thread>/meetings/`
   - Ambiguous → ask the user.
3. Show the user the proposed destination + 5-line preview of the transcript.
4. On confirm, re-run: `python3 .claude/scripts/tactiq_pull.py "$ARG" --dest <chosen_dir>`.
5. After writing, suggest the user run `/post-meeting-digest <path>` to fold a summary into STATUS.md and draft follow-ups (if that command exists yet).

## Naming convention

Script auto-names files as `<YYYY-MM-DD>_<Title_With_Underscores>.txt`. Hash suffixes from Tactiq are dropped.

## Credentials

Script reads `~/.tactiq-credentials.json`. If missing, surface the error message — it tells the user what to do.

## See also

- Project skill `tactiq-pull` — same workflow, invoked autonomously by Claude.
- `engagements/_internal/README.md` — internal thread mapping.
