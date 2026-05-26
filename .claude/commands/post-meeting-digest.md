---
description: After a meeting, generate STATUS entry + follow-up drafts from a transcript. External meetings get email drafts; internal get Slack. Never auto-writes; surfaces drafts for review.
---

# /post-meeting-digest

After-meeting workflow: read transcript, draft STATUS entry, draft follow-ups.

## Argument

Path to a transcript `.txt` file. Usually under `engagements/<client>/<stage>/transcripts/` or `engagements/_internal/<thread>/meetings/`. If omitted, ask the user which transcript.

## What you do

1. Run `python3 .claude/scripts/post_meeting_digest.py "$ARG"`. The script outputs a structured context block with: meeting classification (external/internal), engagement context (CONTEXT.md excerpt + last 3 STATUS entries), and the full transcript.
2. Read the output carefully. Note the classification — external vs internal materially changes what you produce.
3. Generate the requested artefacts:
   - **External meeting**: STATUS entry + follow-up email draft + action items table + commercial state delta (if stage changed).
   - **Internal meeting**: STATUS entry + Slack message draft + action items list.
4. Surface ALL drafts in the conversation for the user to review. Do NOT write to STATUS.md yet.
5. After user approval/edits: write the STATUS.md entry (newest on top). Do NOT send the email or post to Slack — surface the final draft for the user to copy-paste.

## House style anchors

- No em-dashes. Terse. No trailing summaries.
- STATUS entries match the existing format in the target STATUS.md (read the file, mimic the pattern).
- Follow-up emails use `email-drafting-style.md` + `ivo-voice-profile.md` rules from memory.
- For external emails: lead with the commercial gate (decision / blocker / money / timeline), tech detail only if asked.
- For Slack: 1-3 messages, conversational, no AI-tells.

## Approval rule

`outward-facing-actions.md` in memory: never auto-send anything outward. Draft → Ivo approves → Ivo sends (or you write the STATUS entry only). Internal repo edits (the STATUS.md write) are fine after approval.

## When the transcript path doesn't resolve to an engagement

The script reports `engagement kind: unknown`. Ask the user:
- Is this for an existing engagement? (Give them the candidate names from the participants list.)
- Or does it need a new scaffold? (Suggest `/new-engagement`.)

## See also

- Project skill `post-meeting-digest` — same workflow, Claude-triggered.
- `tactiq-pull` — the upstream step (gets the transcript onto disk).
- `engagements/_internal/README.md` — internal thread mapping.
