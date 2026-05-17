# atlas — next priorities

Working priority list, framed by **toil removed per build day**, not "hours saved per week".
Baseline: 40 hr/wk. Goal: less context-switching + reconstruction + babysitting; more analyst-work + calm.
Companion to `ENGAGEMENT_PLAN.md` §6 (the canonical Track A / Track B sequence).

Updated 2026-05-17.

---

## Framing rules (from memory: `working-hours.md`)

- **"Toil removed"** > "hours saved". The 40 hr/wk doesn't grow; the *quality* of the hour does.
- **Operator-work → analyst-work** is the shift. Examples of operator-work:
  - reconstructing where each engagement stands before a call
  - babysitting an extraction on the laptop
  - hand-building deliverable HTML
  - hunting through Drive for "where did I put X"
  - writing weekly briefs from scratch
- Examples of analyst-work (the target):
  - judging which extraction misses matter
  - scoping calls (the actual scoping cognition)
  - negotiating commercial terms (with Jordan)
  - pattern-matching across engagements
- **Surge work** (evenings, weekends) is OK for build sprints, not for steady-state. If a loop only saves time by surging — it doesn't count.

---

## Priority queue (build order, toil-removed lens)

### 1. A8 — Post-meeting digest loop **(highest toil-per-build-day)**

- **What**: watches `engagements/*/<stage>/transcripts/` for new files. New transcript → folds summary into the right `STATUS.md` (newest on top), extracts action items + owners + dates, drafts the follow-up email + Slack message for review.
- **Toil it removes**: every external call today, you read the transcript cold, write a STATUS entry, draft a follow-up. ~30 min × ~8 client calls/wk = ~4 hr/wk pure operator-work.
- **What's left for you**: review the digest, send the draft email. Analyst-judgment kept.
- **Build effort**: ~1 day.
- **Status**: not started.
- **Why first**: highest toil-per-build-day in the entire backlog. Pairs naturally with the morning brief (which reads STATUS).
- **Constraint**: never auto-send. Drafts only.

### 2. B2 — Reusable scoping harness

- **What**: one repo/folder with the Chandra runner + GPT extraction parameterised by doc-type (PDF-unstructured / XML / Excel / hybrid) + the 10%-sample eval scaffold. Point at S3 prefix + config → produces structured results.
- **Toil it removes**: bespoke-per-engagement scripting. Today every new scoping = ~5-8 hr of "wire up Chandra, write extraction prompts, run, debug, score". With B2: 30 min of config + harness runs.
- **What's left for you**: prompt tuning + judging which misses matter (analyst-work).
- **Build effort**: 3-5 days (real work).
- **Status**: not started.
- **Why second**: biggest single source of "babysitting on the laptop" toil. Unlocks B3 + B4 + B5.
- **Gated on**: nothing — code patterns already exist in Aumovio/TandF/Welo/Garrett showcase pipelines.

### 3. B3 — EC2 worker box

- **What**: small AWS box (Ross approved). Runs B2's harness triggered by S3 events. Holds the git repo checked out. Future home for Track A loops + dashboard cron.
- **Toil it removes**: extraction runs *overnight on the box*, you wake up to results. No "can't close the laptop because Chandra is running". Removes evening-trigger constraint from morning brief (currently the loop can't run while laptop sleeps).
- **What's left for you**: judging the morning's output.
- **Build effort**: ~0.5 day provision + ~1 day to move B2 to the box.
- **Status**: Ross OK'd, not provisioned.
- **Gated on**: instance size decision (Chandra is GPU-ish — `g4dn`? or call a hosted endpoint like AlexFert's PaddleOCR pattern?). OQ-3 in ENGAGEMENT_PLAN.
- **Why third**: B2 first (the work); B3 makes B2 not run on the laptop.

### 4. A9 — Weekly cross-engagement rollup + CFO brief

- **What**: Friday job. Reads all `STATUS.md`. Two outputs from the same data: (a) Monday-commercial-call brief (tech-flavoured, what moved + what's blocked + what needs a decision); (b) CFO brief for Steven (commercial-flavoured: milestones, slippage, pipeline, no tech detail).
- **Toil it removes**: you currently hand-write the Monday commercial brief (~2 hr Friday). CFO brief doesn't exist yet, so this *adds* value rather than just removing toil — but the Monday-brief half is pure toil-removal.
- **What's left for you**: edit + send.
- **Build effort**: ~0.5 day (STATUS.md is consistent across 13 engagements; the data is there).
- **Status**: not started.
- **Why fourth**: cheap, Friday-recurring, pairs with Viktor's Asana directive (the brief becomes the source for the Asana sync).

### 5. B6 — PoC status dashboard

- **What**: single self-contained HTML page. Reads every `CONTEXT.md` + `STATUS.md`. Renders week-by-stage roadmap grid (rows = engagements, cols = calendar weeks, cells coloured by stage, current week marked) + per-row side panel (blocked-on, next milestone, commercial gate). Cron-regenerated.
- **Toil it removes**: kills "what's the state of X?" pings. Replaces Viktor's killed-Excel directive with a thing that's never stale. Removes ~1.5 hr/wk of "let me check / reconstruct / explain".
- **What's left for you**: glance at it, trust it.
- **Build effort**: ~1 day (the data already exists in repo; just rendering + a cron).
- **Status**: not started.
- **Why fifth**: cheap, high visibility (Viktor, Steven), turns the engagement repo into a *view* not just a store.

### 6. HubSpot MCP (A6)

- **What**: read-only MCP on companies/contacts/deals/engagements. Pulls deal stage + Jordan's call summaries into a draft section of `COMMERCIAL.md` you edit (never auto-overwrite).
- **Toil it removes**: manually checking HubSpot before each commercial call. ~30 min/wk.
- **Build effort**: ~0.5 day after admin authorisation.
- **Status**: blocked — no admin yet (OQ-1).
- **Why sixth**: gated on someone else; not a build-effort priority for you.

### 7. A2 — `/new-engagement` slash command **(DONE 2026-05-17)**

- ✅ shipped. Scaffolds 5-file engagement from `_template/`, asks 5 Qs, registers in `_aliases.yaml`.

### 8. B1 — S3 prefix standardisation

- **What**: `s3://iris-engagements/<company>/{raw,processed,results,ground-truth}/`. Convention + light migration of existing local data up to S3.
- **Toil it removes**: confusion about where files live (currently mixed across Axion remnants, Drive, S3, repo). Unblocks Track B fully.
- **Build effort**: ~0.5 day.
- **Status**: not started.
- **Gated on**: confirm bucket name with Ross (OQ-5).
- **Why eighth**: foundational for Track B but no immediate toil-removal until B2/B3 land.

### 9. B4 — Deliverable HTML generator

- **What**: turns B2 harness output + "what this client cares about" (`CONTEXT.md §4`) into a first-draft scoping presentation HTML. You edit, don't build from scratch.
- **Toil it removes**: ~6-12 hr per scoping deliverable. ~1 scoping/2wks = ~3 hr/wk recurring.
- **Build effort**: ~2-3 days.
- **Gated on**: B2 (need the harness output schema first).

### 10. B5 — Eval-driven extraction loop

- **What**: client returns ground truth → box re-runs harness → scores → surfaces worst cases → you adjust prompt → re-runs.
- **Toil it removes**: ~2 hr/wk during PoCs.
- **Build effort**: ~1-2 days.
- **Gated on**: B2 + B3.

### 11. B7 — SoW/NDA drafter

- **What**: reads `CONTEXT.md` + closest prior SoW (Agrolimen ← SMS ← Aumovio lineage) + standard legal language → first draft. Hard human gate. Second "judge" agent checks numbers/dates/scope.
- **Toil it removes**: ~3 hr per first-draft SoW, ~2 SoWs/month.
- **Build effort**: ~1-2 days + careful human-gate setup.
- **Why later**: lower frequency, higher risk if it gets numbers wrong.

### 12. B8 — PoC kickoff handoff generator

- **What**: produces `5_implementation/handoff.md` synthesising scattered context for tech team.
- **Toil it removes**: ~3 hr per PoC kickoff (~1/month).
- **Build effort**: ~1 day.

### 13. A10 — Gmail MCP integration + graduate stable loops to cloud `/schedule`

- **What**: Gmail MCP is wired (used by `_gmail_digest_protocol.md`); the "graduate stable loops to cloud" piece needs B3 first.
- **Status**: half-done. Cloud graduation gated on B3.

---

## What's NOT on this list (and why)

- **Tactiq MCP**: no MCP exists, no plan to build one. Stays manual via `_digest_protocol.md`.
- **Asana write-side MCP**: read works, write-trust not established. Stay manual until a need forces it.
- **Auto-send anything outward**: by memory rule, never. Always draft → Ivo approves.
- **Cross-engagement pattern recognition agent** ("Agrolimen looks like SMS Group"): too speculative, no clear toil today.
- **Replacing Tactiq / Gemini-Notes**: they work; their *output* is what we automate around.

---

## Cumulative state (after each step, toil-removed)

| After step | Toil removed (hr/wk equivalent) | % of 40-hr week shifted to analyst-work |
|---|---|---|
| Today (post-A2) | 12.5 | 31% |
| + A8 | 16 | 40% |
| + B2 | 21 | 53% |
| + B3 | 23 | 58% |
| + A9 | 25 | 63% |
| + B6 | 26.5 | 66% |
| + HubSpot | 27 | 68% |
| + B1 / B4 / B5 / B7 / B8 | 32 | 80% |

80% = the *operator hour* shrinks to ~8/wk. The remaining 32 hr is the analyst-work the role actually pays for (client calls, judgment on extraction, scope decisions, prompt tuning, commercial negotiation). That's the target: calmer, more focused, same hours, better quality.

---

## Reminder

Every loop drafts. None send. Outward-facing actions stay on the approval rule (`outward-facing-actions.md` memory). The point is removing toil, not removing the human.
