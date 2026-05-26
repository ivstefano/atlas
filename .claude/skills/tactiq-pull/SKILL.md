---
name: tactiq-pull
description: Pull a Tactiq meeting transcript and file it into the right engagement folder. Use when a meeting has just ended and the user wants the transcript captured locally, or when filling a gap in an engagement's transcripts/.
---

# tactiq-pull

Pull one Tactiq transcript by meeting ID or URL, write it to the right `<engagement>/<stage>/transcripts/` folder with the project's naming convention.

## Usage

The script is at `.claude/scripts/tactiq_pull.py`. It takes:

- A meeting ID (e.g. `8btqs919sbrISDQAvDi1`) OR a Tactiq URL (e.g. `https://app.tactiq.io/meeting/8btqs919sbrISDQAvDi1`).
- `--dest <dir>`: where to write the file. Required for filing into engagements. If omitted, prints to stdout.

```bash
python3 .claude/scripts/tactiq_pull.py <id_or_url> --dest <engagements/<client>/<stage>/transcripts/>
```

## Where to file

Inspect the transcript's participants and decide:

| Pattern | Destination |
|---|---|
| External client attendees (e.g. Lucy Todorovska + Justyna at Heineken) | `engagements/<client>/<stage>/transcripts/` — pick the stage the engagement is currently at (read its STATUS.md or check the highest-numbered stage folder). |
| All IRIS people | `engagements/_internal/<thread>/meetings/` — see `engagements/_internal/README.md` for the thread mapping (platform-product, marketing-demos, tech-engineering, tech-rdd, commercial-rhythm, people-1on1/<name>/). |
| Mix of IRIS + Jordan-pipeline prospect (no engagement folder yet) | Decide if it's a real prospect (create scaffold) or one-off (file in `_misc/`). Don't auto-create folders without confirming with the user. |

If the engagement folder doesn't exist yet (new prospect), ask the user before creating it. Use `/new-engagement` slash command for that.

## Filename convention

The script names files as `<YYYY-MM-DD>_<Title_With_Underscores>.txt`. Hash suffixes from Tactiq IDs are dropped (the ID stays in the file's header). This matches the convention used in the May 2026 mass migration; don't deviate.

## Credentials

The script reads `~/.tactiq-credentials.json`. If that file is missing, the script will tell the user how to populate it (sign in to app.tactiq.io, copy refresh_token + id_token from devtools). Don't try to fetch credentials another way.

## What this skill does NOT do

- Does NOT auto-update STATUS.md from the transcript. Use the post-meeting digest workflow (`/post-meeting-digest` slash command) for that.
- Does NOT live-poll a meeting in progress. Use `tactiq_watch.py` directly for that (a different tool).
- Does NOT bulk-download. The existing `Axion/tactiq_export/export.py` covers that.

## When invoked autonomously

If you decide on your own that a transcript needs pulling (e.g. user mentions a call and the transcript isn't in the engagement folder), confirm the destination path before writing. Don't assume.

## Related

- `atlas/.claude/scripts/tactiq_pull.py` — the script.
- `atlas/.claude/scripts/tactiq_client.py` — shared GraphQL client.
- `atlas/.claude/scripts/tactiq_watch.py` — live polling variant.
- `atlas/.claude/commands/tactiq-pull.md` — the slash command surface (same script, different invocation).
- `engagements/_internal/README.md` — thread mapping for internal transcripts.
- Memory `tactiq-transcript-fetch.md` — original reference (now superseded by this skill).
