---
name: morning-brief-gap
description: When generating a morning brief and there's a multi-day gap since the last brief (weekend, busy stretch), produce a state-recovery section that reconstructs what happened across engagements + atlas before today's prep section.
---

# morning-brief-gap

Companion to the `/morning-brief` command. Invoked autonomously when the gap between today and the most recent prior brief is 2+ days.

## When to fire

- The morning-brief flow detects `gap_days >= 2`.
- User explicitly asks for "what happened since last brief" or similar reconstruction.

## How

1. Run `python3 .claude/scripts/gap_scan.py`. With no args it picks the most recent brief date automatically. Output is a markdown report with: engagement-side git changes, atlas-side git changes, new transcripts, open next-action items.

2. The script covers git + filesystem only. To make the recovery complete, ALSO run in parallel (as MCP calls within the current session):
   - **Calendar in the gap**: `mcp__claude_ai_Google_Calendar__list_events` from `since` to today. Identify calls that happened, especially those with no STATUS update yet (digest gap).
   - **Gmail in the gap**: for each active engagement's attendee domains, `mcp__claude_ai_Gmail__search_threads` with `newer_than:<gap_days>d`. Snippets only.
   - **Slack in the gap**: `mcp__slack__conversations_history` for `#C0AEY7YBBA8` + DMs to/from Vankata, Viktor, Steven, Jordan. Filter to window.
   - **Asana in the gap**: `mcp__asana__list_tasks` in commercial-engagements project (`1214855342290138`), modified in window.

3. Synthesise into the brief's "Since last brief" section (see `morning-brief.md` step 5b for the exact structure).

4. **Flag the digest gaps**: any meeting that happened but has no STATUS update → recommend the user run `/post-meeting-digest` on the transcript. These are the highest-leverage action items.

## Output style

The gap-recovery section sits between TL;DR and Today's calls in the brief. Don't double-count: if a call from yesterday produced a STATUS entry that's already in the engagement's "Since last touchpoint" block of the per-engagement section, don't repeat it in the gap recovery.

Keep it terse — bullets, not paragraphs. The point is to recover state, not narrate.

## Edge cases

- **No prior briefs at all** (fresh atlas install): skip the gap-recovery scan, proceed with full state synthesis.
- **gap > 14 days** (e.g. holiday, leave): clamp to 14 days for Gmail/Slack/Asana queries — older deltas should already be reflected in STATUS files.
- **Calendar events in the gap that ARE in atlas**: if `STATUS.md` already has an entry for the date+engagement, no follow-up needed.
- **Calendar events in the gap with NO transcript AND NO STATUS**: flag as "missed digest". User decides whether to chase the transcript or just note it.

## Related

- `atlas/.claude/scripts/gap_scan.py` — the offline script.
- `atlas/.claude/commands/morning-brief.md` — the parent flow (this skill is a sub-step).
- `atlas/.claude/skills/post-meeting-digest/SKILL.md` — what to run on the "missed digest" items.
