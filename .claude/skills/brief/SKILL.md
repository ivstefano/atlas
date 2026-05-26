---
name: brief
description: Use when the user invokes /brief to compose a high-stakes prompt (SoW, client email, status update, strategic analysis). Walks them through a 5-field checklist via AskUserQuestion, assembles a well-formed prompt, then executes it.
---

# /brief — pre-prompt checklist for high-stakes asks

The user has invoked `/brief` because they're about to ask for something where output quality matters (client artifact, strategic recommendation, anything that'll take >2 min of work). Their natural prompting style buries the goal and leaves audience/format/length unspecified. This skill forces them through a structured intake before work starts.

## Execution flow

1. If the user passed text after `/brief` (e.g. `/brief draft email to Norbert`), treat that as the rough ask. Otherwise, ask: "What's the rough ask? (one sentence)"

2. Ask the 5 checklist questions using `AskUserQuestion`. Batch them into a single tool call (one call, up to 4 questions; the 5th asked in a follow-up if needed). Use multiple-choice options where possible — the user picks faster than they type.

   **Q1 — Goal (one line, what done looks like):**
   - Open-ended. Phrase: "What does 'done' look like in one sentence?"
   - Skip if the user's rough ask already contains a clear goal.

   **Q2 — Project / engagement:**
   - Options derived from the current working directory + recent activity. Typical: Aumovio, SMS Group, Agrolimen, Atlas, Heineken, T&F, NHS, HubSpot, Riyad Bank, IRIS internal, Other.
   - Auto-fill if the CWD makes it obvious; only ask if ambiguous.

   **Q3 — Audience:**
   - Options: (A) Me (internal notes), (B) IRIS internal team, (C) Specific client contact [ask who], (D) Mixed.
   - Drives tone, jargon level, and what's safe to expose (paths, names).

   **Q4 — Output format:**
   - Options: (A) Draft document/email, (B) Ranked recommendation with owner+deadline, (C) Options matrix with trade-offs, (D) Short analysis/explanation, (E) Other.

   **Q5 — Stop-when (length cap or success criterion):**
   - Options: (A) ~1 page / under 300 words, (B) Half page / under 150 words, (C) 3 bullets, (D) As long as needed, (E) Custom.

3. Assemble the well-formed prompt in this shape:

   ```
   GOAL: <Q1>
   PROJECT: <Q2>
   AUDIENCE: <Q3>
   FORMAT: <Q4>
   STOP WHEN: <Q5>

   <user's rough ask + any context they provided>
   ```

4. Show the assembled prompt to the user in a code block and ask: "Execute this, or edit first?" via AskUserQuestion with options (A) Execute, (B) Let me edit, (C) Cancel.

5. On Execute: proceed with the work using the assembled prompt as the spec. Apply House Style rules from the project CLAUDE.md.

## When to skip the full flow

- If the rough ask already contains 4+ of the 5 fields explicitly, skip ahead to step 3 (just confirm the assembled brief).
- If the user invokes `/brief --quick`, ask only Audience + Format, infer the rest.

## Notes

- The point isn't bureaucracy — it's catching the 2-3 fields the user habitually forgets (audience, format, stop-when).
- Keep it under 60 seconds end-to-end. If it feels slow, the user will stop invoking it.
- The skill is itself the training: each round of multiple-choice questions teaches the user which fields matter, so eventually they pre-fill them and skip `/brief` entirely.
