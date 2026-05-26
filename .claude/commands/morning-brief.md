---
description: Generate the morning brief for a given date. Pulls Calendar → matches engagements → gathers state → writes a brief to briefs/YYYY/WNN/YYYY-MM-DD_auto.md.
argument-hint: [date | "tomorrow" | "today"]
---

# Morning brief loop

Generate the morning brief for `$ARGUMENTS` (target date). Default: tomorrow if it's evening (after 18:00), today otherwise.

## Output

- **Path**: `briefs/YYYY/WNN/YYYY-MM-DD_auto.md` where:
  - `YYYY` = target-date year
  - `WNN` = ISO week number, zero-padded (e.g. `W21`)
  - `YYYY-MM-DD_auto.md` = the brief file
- **First 2 weeks (until 2026-05-31): write `_auto.md` suffix.** After that, switch to direct `YYYY-MM-DD.md`.
- **If a hand-written brief already exists at the target path (without `_auto` suffix), still write the `_auto.md` sibling.** Don't overwrite human work.

## Steps

### 1. Determine target date

- Parse `$ARGUMENTS`. Accept `today`, `tomorrow`, or ISO date `YYYY-MM-DD`.
- If empty: tomorrow if current local time ≥ 18:00, else today.
- Compute ISO week number (`date -u -d "$DATE" +%V` or similar) to build the output path.

### 2. Pull Calendar events for that date

Use `mcp__claude_ai_Google_Calendar__list_events` with the target date range (00:00 to 23:59 local time, Sofia / Europe-Sofia timezone).

For each event, record:
- title, start time (local), duration
- attendees (email + name when available)
- description (often has Tactiq link, Teams link, meeting context)
- conference link (Teams/Meet/Webex)

### 3. Match each event to an engagement

Read `engagements/_aliases.yaml`. For each event:

1. **Internal-only test**: if every attendee is `@iris.ai`, treat as INTERNAL. Include only if:
   - Title matches one of `_internal.recurring_meetings`, OR
   - At least one attendee is in `_internal.always_include_attendees`
   Otherwise skip with note "internal meeting skipped: <title>".

2. **Domain match**: any attendee's email domain matches an engagement's `domains` list → use that engagement.

3. **Title match**: title (case-insensitive) contains any string from an engagement's `titles` list.

4. **Folder fuzzy match**: engagement folder name (or its substrings) appears in title.

5. **Multiple matches**: pick the one with status `active` if exactly one; otherwise flag.

6. **No match**: include event in brief under "Unmatched events" with attendee list + title; do NOT auto-create folders.

### 4. Gather state per matched engagement

For each engagement in today's events, read from `engagements/<co>/`:

- `CONTEXT.md` — read the header (Stage / Type / Lead source / Aliases) and §6 Stakeholders + §7 Current phase
- `STATUS.md` — last 5 dated entries (newest on top)
- The most recent transcript file in `<active-stage>/transcripts/` whose mtime is newer than the previous brief's date (skip if none)
- `COMMERCIAL.md` — last 2 dated entries

Additionally, via MCPs (parallel where possible):

- **Drive (`mcp__claude_ai_Google_Drive__search_files`)**: find Gemini notes for this engagement modified in the last 7 days. Use the drive_id from ARTEFACTS.md as `parentId =` if available.
- **Asana (`mcp__asana__search_tasks`)**: tasks in the engagement's section (project `1214855342290138`), status `in_progress` or `pending` with due dates this week.
- **Gmail (`mcp__claude_ai_Gmail__search_threads`)**: threads with any attendee in `from:` or `to:` from the last 7 days. Read snippet/subject only, not full bodies.

### 5. Gap-recovery scan (NEW — runs BEFORE state-per-engagement synthesis when gap > 1 day)

Find the most recent brief in `briefs/YYYY/W*/`. Compute `gap_days = today - last_brief_date`.

If `gap_days <= 1`: skip this section, proceed with normal per-engagement "Since last brief" diff (existing behaviour).

If `gap_days >= 2`: run the **comprehensive recovery scan** first. The brief becomes a state-recovery tool, not just a today-prep, because Saturday-Sunday or busy-day gaps drop activity that today's brief needs to integrate.

Sources to pull (parallel where possible):

**Git deltas (cheap, do first):**
```bash
# engagements changes since last brief
git -C ~/Documents/engagements log --since="<last_brief_date>" --until="<today>" --pretty=format:"%ad %s" --date=short --name-only

# atlas changes since last brief
git -C ~/Documents/atlas log --since="<last_brief_date>" --until="<today>" --pretty=format:"%ad %s" --date=short
```

Parse the output to identify:
- New STATUS.md entries (which engagements?).
- New transcripts (which engagements got new calls?).
- New CONTEXT/SOURCES/ARTEFACTS edits (what shifted?).
- Atlas-side: new briefs in the gap, NEXT_PRIORITIES updates, new memory entries.

**Calendar events that happened in the gap:**
- `mcp__claude_ai_Google_Calendar__list_events` from `<last_brief_date>` to today, exclude all-day events.
- For each: was it likely attended (the user was the organiser or accepted)? If yes, did it produce a transcript that's now in the engagement folder?
- Flag any meeting that happened but has NO STATUS update → that's a digest gap.

**Gmail threads in the gap (lightweight):**
- For each engagement that's active per Asana / STATUS, search Gmail for threads with that engagement's attendee domains modified in the gap window.
- Use `mcp__claude_ai_Gmail__search_threads` with `newer_than:<gap_days>d`.
- Read snippets only, not full bodies.

**Slack threads in the gap (lightweight, sampled):**
- `mcp__slack__conversations_history` for #C0AEY7YBBA8 + DMs to/from key counterparts (Vankata, Viktor, Steven, Jordan).
- Filter to the gap window. Snippets only.

**Asana task state changes:**
- `mcp__asana__list_tasks` in commercial-engagements project (`1214855342290138`), modified in the gap window. State transitions only — what moved from pending → done, or got reassigned.

### 5b. Gap-recovery output section

If `gap_days >= 2`, the brief gets a new section near the top, between TL;DR and Today's calls:

```markdown
## Since last brief (gap: N days — DD May to DD May)

### What happened (by engagement)

**heineken**
- 2026-05-23: STATUS entry on <topic>
- 2026-05-24 Gmail: thread from Lucy re <subject>
- 2026-05-24 Slack: Vankata DM thread about <topic>
- Asana: task "X" moved to done

**aumovio**
- ...

### What happened (atlas-side)
- New briefs: <list>
- NEXT_PRIORITIES updates: <one-liner>
- Memory entries added: <list>

### Calls that happened with NO STATUS update yet (digest gap)
- DD May HH:MM — <title> — <engagement>. Transcript: present | absent. Recommend running `/post-meeting-digest` on it.

### Open action items still due (from STATUS "next action" lines)
- <engagement> — <action with owner + date>
```

After this gap-recovery section, proceed with normal per-engagement state synthesis (existing step 6).

### 6. Synthesise the brief

Write to `briefs/YYYY/WNN/YYYY-MM-DD_auto.md` with this structure:

```markdown
# Morning brief — YYYY-MM-DD (Day of week)

Auto-generated <timestamp>. Trigger: evening-before from <prev brief date>.

## TL;DR — the 3 things that matter today

- [highest-priority commercial/decision point across all of today's calls]
- [second]
- [third — or "everything else is routine"]

## Today's calls

### NN:MM — <Engagement> — <call topic / Tactiq title> (<duration>)

- **Who**: <client names + role> + <iris.ai people>
- **Stage / commercial gate**: <one line from CONTEXT/COMMERCIAL>
- **Since last touchpoint**: <what changed; 2-3 lines max>
- **You'll need to say**: <3 specific things — what to bring, what to confirm, what to ask>
- **Open Qs / blockers**: <if any>
- **Links**: <Teams/Meet link>, <Tactiq URL>, <Gemini notes drive_id if found>

### NN:MM — <Next engagement> — ...
...

## Unmatched events (needs your call)

- HH:MM — <title> — attendees: <list> — reason no match: <why>

## Internal meetings included

- HH:MM — <title> (rationale: matched <recurring_meeting> | exec 1:1)

## Internal meetings skipped

- HH:MM — <title> (all-iris.ai, no recurring-match)
```

### 7. Write + commit

- Write the file.
- `cd /Users/iris/Documents/atlas && git add briefs/ && git commit -m "auto: morning brief YYYY-MM-DD"`
- Do NOT push (you're on the laptop with no push permissions for atlas; engagements is a separate repo).

### 8. Report to user

Single message back, terse:
- Brief written to `briefs/2026/W21/2026-05-18_auto.md`
- N engagements covered, M unmatched events, K internal skipped
- Top thing: <one-liner from TL;DR>

## Constraints

- **Never** auto-create a new engagement folder. Unmatched events → flag, no action.
- **Never** send anything (no calendar replies, no Gmail drafts, no Asana edits). The loop reads + writes the brief only.
- **Never** modify any engagement's CONTEXT/STATUS/COMMERCIAL/SOURCES/ARTEFACTS files. Read-only on those.
- Use parallel MCP calls where possible (Drive search + Gmail search + Asana search can fire concurrently per engagement).
- If a Drive folder search returns the "ineligible for generative AI contexts" error for a gdoc, note its title + drive_id without reading content.
- Tactiq links in event descriptions: capture but do not click/fetch (manual review).
- Keep the brief under ~300 lines total. If today has >10 calls, prioritise: external client calls > exec 1:1s > recurring internal.

## When in doubt

- Match ambiguous? Flag for user, don't guess.
- Missing data? Note "no data available" in the engagement block, don't fabricate.
- Past brief seems stale or contradictory to current state? Trust the engagement folder, not the brief.
