---
name: post-meeting-digest
description: Generate STATUS entry + follow-up drafts from a meeting transcript. Use when a new transcript appears in an engagement folder, when the user mentions a recent call without context, or when STATUS.md hasn't been updated after a known meeting.
---

# post-meeting-digest

Process a meeting transcript into a STATUS.md entry + follow-up drafts. External vs internal handling differs.

## When to invoke autonomously

- A new transcript file lands in `engagements/<client>/<stage>/transcripts/` or `engagements/_internal/<thread>/meetings/`.
- The user mentions a recent meeting whose summary isn't in STATUS yet.
- After `/tactiq-pull` completes, naturally chain into digest generation (ask the user first).

## How

1. Run `python3 .claude/scripts/post_meeting_digest.py <transcript_path>`. The script outputs a structured context block:
   - Meeting metadata + classification (external/internal).
   - Engagement context (CONTEXT.md excerpt + recent STATUS entries).
   - Full transcript body.
   - Instructions tailored to external vs internal.

2. Read the output carefully. Match your output to what the instructions request.

3. Produce drafts (do NOT write to disk yet):
   - **External meeting**: STATUS entry, follow-up email, action items, commercial delta.
   - **Internal meeting**: STATUS entry, Slack draft, action items.

4. Surface all drafts to the user. After review and approval:
   - Write the STATUS.md entry (newest on top, match the file's existing format).
   - Show the final email/Slack draft for manual copy-paste — never send.

## Key constraints

- **Never auto-send anything outward** (`outward-facing-actions.md` memory).
- **Never auto-write to STATUS.md** before user approval. Draft first.
- **Match the target STATUS.md's existing format.** Read it first; mimic it.
- **House style** (`~/.claude/CLAUDE.md` + memory entries `email-drafting-style.md`, `ivo-voice-profile.md`, `comms-style-improvements.md`): no em-dashes, terse, no trailing summaries.

## Headless / loop mode

For future cloud `/schedule` use: the script supports `--json` flag for raw structured output. A loop runner can feed this to a separate LLM call (Sonnet for cost) to generate drafts headless. Not used today; reserved for the loop-graduation step in atlas's roadmap.

## Edge cases

- **Transcript outside `engagements/`**: script returns `engagement: unknown`. Ask the user where to file it (or whether to scaffold a new engagement).
- **Empty STATUS.md** (new engagement, no prior entries): generate the entry without "match existing format" — use the convention from `engagements/_template/STATUS.md` or a similar engagement.
- **Mixed-language transcript** (Bulgarian + English, common in IRIS internal calls): keep the STATUS entry in English; quote Bulgarian only if directly relevant.
- **Transcript is mostly garbled** (bad Tactiq parse, "Sushila more pour"): note that and ask the user whether to skip or generate a best-effort summary.

## Related

- `atlas/.claude/scripts/post_meeting_digest.py` — the prep script.
- `atlas/.claude/commands/post-meeting-digest.md` — user-facing slash.
- `atlas/.claude/skills/tactiq-pull/SKILL.md` — gets transcripts onto disk in the first place.
- Memory `engagement-drive-symlinks.md` — where transcripts live.
- Memory `iris-people.md` — IRIS team name list (used by the script for classification).
