# atlas — next priorities

Working priority list, framed by **toil removed per build day**, not "hours saved per week".
Baseline: 40 hr/wk. Goal: less context-switching + reconstruction + babysitting; more analyst-work + calm.
Companion to `ENGAGEMENT_PLAN.md` §6 (the canonical Track A / Track B sequence).

Updated 2026-05-18.

---

## The product reframe (2026-05-18)

What was a "Track B harness + HTML generator" is becoming a **Solutions Architect product surface**: a web UI where IRIS SAs (Ivo, Matyo, Petar, future hires) upload client files, watch extraction run, **edit results in-browser** (text, brand, bucket assignments), publish to S3 or Neuralith. Similar shape to `claude.ai/design`, scoped to scoping deliverables.

**Why the reframe**: every showcase to date (Agrolimen → Garrett v1/v2/v3/combined → TandF × 3 → DB) was the same skeleton re-hand-tuned. The "make it look nice" loop is product work, not per-engagement work. Centralise it once.

**Triggered by**: today's Platform Design Sync (Vankata's reintegration push) + Rosen's 2026-05-18 green-light on EC2 + S3 self-serve (only IAM still owed by him).

**Three paths considered, recommendation = Path 3 (hybrid):**

| | Path 1 — Atlas standalone | Path 2 — Inside Neuralith | Path 3 — Hybrid (recommended) |
|---|---|---|---|
| Where it lives | EC2 box, own frontend | Neuralith codebase | EC2 box now, designed to migrate |
| Velocity | Ships in 3-4 wks | Gated on platform roadmap | Ships in 3-4 wks |
| Strategic fit | Parallel product, may duplicate Neuralith later | Becomes first SA-facing platform feature | First on EC2, migrates into Neuralith when ready |
| Risk | Maintaining a side product | Slow + spec-by-committee | Migration friction if Neuralith diverges |

Path 3 = build standalone on EC2 using Neuralith's component library + a JSON edit-model Neuralith can adopt. Publish target dual (S3 today, Neuralith when Vova ships upload API). **Approved by Ivo 2026-05-18. Tomorrow's Vova + Vankata meeting confirms (a) we can use Neuralith's component library, (b) the JSON edit-model will be acceptable as a platform standard.** If either is "no" → fall back to Path 1.

**Decisions locked 2026-05-18:**

- **Name**: keep "Atlas". The product surface is Atlas's flagship; other pieces (morning brief, post-meeting digest, weekly rollup) become "Atlas loops". Pitched to Vankata as one IRIS surface, not a competing product name.
- **Other SAs (Matyo, Petar)**: not in tomorrow's Vova/Vankata meeting (that's platform-strategy). Async-pinged for tech preferences before B4b implementation starts. Spec input shapes the editor model, not the platform conversation.
- **Auth in v0**:
  - SA login to the UI → IRIS Google SSO (~30 min with NextAuth or similar). Cheap, lets Matyo/Petar in day-1 without provisioning.
  - Service-to-service (S3, EC2, GPU) → IAM via Rosen's instance profile (B3).
  - Client-facing publish links → access-code on S3 (DB pattern) or Neuralith-side auth later. No SSO for clients.

**Three layers (clarifies what each B-task is doing):**

```
LAYER 1 — Extraction  (B1 + B2 + B3)
  Chandra + GPT pipeline on EC2 GPU (Matyo's i-06aa73900ca43c1e9, eu-central-1)
  → buckets.json, relational_db.json, groundedness_audit.json, evidence_bbox.json, summary.csv

LAYER 2 — Deliverable rendering  (B4a)
  One parameterised template (steal best of Agrolimen SQL playground + Garrett tabs
  + DB groundedness panel). Brand colours, logo, font, ontology shape are parameters.

LAYER 3 — The product surface  (B4b + B4c + B4d)
  Web UI: upload → run → edit-in-browser → publish.
  LLM-tuner step fills template parameters from CONTEXT.md §4 + brand JSON.
  Publish endpoint = S3 (today) or Neuralith (when ready).
```

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

### 3. B3 — EC2 controller box

- **What**: small always-on CPU EC2 box (`t3.small` or `t4g.small`) in **eu-central-1**. Holds the git repo, runs B2's harness, starts/stops Matyo's existing GPU instance (`i-06aa73900ca43c1e9`, eu-central-1) via boto3 lift of `start_gpu_instance.py`. Future home for Track A loops + the B4 product API server.
- **Toil it removes**: extraction runs *overnight on the box*, you wake up to results. No "can't close the laptop because Chandra is running". Removes evening-trigger constraint from morning brief (currently the loop can't run while laptop sleeps).
- **What's left for you**: judging the morning's output.
- **Build effort**: ~0.5 day provision + ~1 day to lift B2 + GPU-control scripts onto it.
- **Status**: Rosen green-lit EC2 + S3 self-serve 2026-05-18. **IAM role pending Rosen** (`iam:CreateRole` not in `Iris_Devs` SSO role — he'll create the controller's instance profile with `ec2:Run/Start/Stop` + `s3:*` on the engagements bucket). Region locked to eu-central-1 (no reason to leave it, GPU lives there).
- **Reuse vs. own GPU**: reuse Matyo's existing GPU instance for now (capacity-sharing risk with extract team noted; revisit if it bites).
- **Why third**: B2 first (the work); B3 makes B2 not run on the laptop and hosts the B4 product backend.

### 4. A9 — Weekly cross-engagement rollup + CFO brief

- **What**: Friday job. Reads all `STATUS.md`. Two outputs from the same data: (a) Monday-commercial-call brief (tech-flavoured, what moved + what's blocked + what needs a decision); (b) CFO brief for Steven (commercial-flavoured: milestones, slippage, pipeline, no tech detail).
- **Toil it removes**: you currently hand-write the Monday commercial brief (~2 hr Friday). CFO brief doesn't exist yet, so this *adds* value rather than just removing toil — but the Monday-brief half is pure toil-removal.
- **What's left for you**: edit + send.
- **Build effort**: ~0.5 day (STATUS.md is consistent across 13 engagements; the data is there).
- **Status**: not started.
- **Why fourth**: cheap, Friday-recurring, pairs with Viktor's Asana directive (the brief becomes the source for the Asana sync).

### 5. ~~B6 — PoC status dashboard~~ (deprioritised 2026-05-17)

- **What was**: single self-contained HTML page rendering a week-by-stage roadmap grid from `CONTEXT.md` + `STATUS.md`.
- **Why dropped**: Asana now holds engagement state (Viktor's 2026-05-15 directive). Asana's Gantt view does the same job Steven would have wanted; Ivo will present Asana Gantt on Mondays. HubSpot (once wired) covers commercial-pipeline view. Building a third surface = duplication for negative value.
- **If revisited later**: only if Asana Gantt + HubSpot prove insufficient — but that's the directional bet right now.

### 6. HubSpot MCP (A6)

- **What**: read-only MCP on companies/contacts/deals/engagements. Pulls deal stage + Jordan's call summaries into a draft section of `COMMERCIAL.md` you edit (never auto-overwrite).
- **Toil it removes**: manually checking HubSpot before each commercial call. ~30 min/wk.
- **Build effort**: ~0.5 day after admin authorisation.
- **Status**: blocked — no admin yet (OQ-1).
- **Why sixth**: gated on someone else; not a build-effort priority for you.

### 7. A2 — `/new-engagement` slash command **(DONE 2026-05-17)**

- ✅ shipped. Scaffolds 5-file engagement from `_template/`, asks 5 Qs, registers in `_aliases.yaml`.

### 8. B1 — S3 prefix standardisation **(promoted; foundation for B3+B4)**

- **What**: `s3://iris-engagements/<company>/{raw,processed,results,ground-truth}/` in eu-central-1. Convention + light migration of existing local data up to S3.
- **Toil it removes**: confusion about where files live (currently mixed across Axion remnants, Drive, S3, repo). Unblocks Track B fully.
- **Build effort**: ~0.5 day.
- **Status**: **unblocked 2026-05-18** — Rosen green-lit self-serve bucket creation, naming `iris-engagements` is fine (open to prefix preference if he signals one). Should land alongside or before B3.
- **Why eighth (but really do it early)**: foundational for B3 + B4. Realistically build it during the B3 provisioning window.

### 9. B4 — Solutions Architect product surface **(reframed 2026-05-18 — was "deliverable HTML generator")**

The big shift. What was a one-script HTML generator is now a small web product for SAs to run + edit + publish scoping deliverables. Splits into four sub-tasks:

#### 9a. B4a — Templated showcase renderer

- **What**: one parameterised showcase template (one place to invest in design quality). Steal best of: Agrolimen SQL playground + 15-table SQLite + Garrett 5-tab structure (Dashboard / Page Explorer / Compressor Maps / Tables / Semantic Understanding) + DB groundedness audit panel.
- **Parametrise**: brand colours, logo URL, font, ontology section names, "what this client cares about" copy block (from `CONTEXT.md §4`).
- **Toil it removes**: the "ask Claude per engagement to make it look nice" loop. Garrett went through 4 rebuilds (`build_showcase.py` → `_v2` → `_combined` → `_combined_v3`); TandF had 3 separate build scripts. One template ends that.
- **Build effort**: 2-3 days.
- **Gated on**: B2 (harness output schema). Path-3 decision from tomorrow's meeting (whether to use Neuralith's component library or stay agnostic).

#### 9b. B4b — Web product UI (the editor)

- **What**: small Next.js/React frontend on the B3 EC2 controller box. Pages:
  - **Inputs**: new-engagement form (client name, brand colours, logo upload, font, "what they care about" text), file uploader (drag PDFs/XMLs/xlsx → backend sends to S3 → triggers B2 harness on GPU), job queue with progress.
  - **Editor**: per-document view with extracted blocks (text/tables/images/charts). Toggle confidence, hide low-confidence rows, edit field values inline, drag fields between Confidently-Extractable / Needs-PoC-Discovery / Cannot-Extract buckets. Live preview pane of the showcase.
  - **Publish**: render via B4a → choose target (S3 + access code, Neuralith link, PDF export). Per-engagement audit log.
- **Toil it removes**: the entire per-client re-skinning + manual showcase editing loop. ~6-12 hr per scoping × ~2 scopings/month = ~3-6 hr/wk recurring once mature.
- **Build effort**: 4-6 days.
- **Gated on**: B4a (template to render). Decision on auth (IRIS Google SSO presumed).
- **Multi-user from day 1**: Matyo + Petar are also Solutions Architects who'd use this. Spec input from them before locking the editor model.

#### 9c. B4c — Neuralith publish adapter

- **What**: when Vova ships an upload API for extraction artefacts, B4b's "publish" flow can target Neuralith in addition to S3.
- **Build effort**: 1-2 days once the API spec exists.
- **Gated on**: Vova's upload-API stub (tomorrow's meeting outcome).

#### 9d. B4d — JSON edit-model + audit log spec

- **What**: design the editor's data model up front so Neuralith's Artifact Viewer can adopt the same JSON shape later. Avoids the migration trap where Atlas-side and Neuralith-side diverge.
- **Build effort**: ~1 day spec, folded into B4b implementation.
- **Why**: this is the bridge between Path 3 today and Path 2 eventually.

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
| Today (post-A2 + Drive reorg) | 12.5 | 31% |
| + A8 | 16 | 40% |
| + B1 + B2 + B3 | 23 | 58% |
| + B4a (templated showcase) | 26 | 65% |
| + B4b (editor UI) | 30 | 75% |
| + A9 | 32 | 80% |
| + HubSpot + B5 / B7 / B8 + B4c | 34 | 85% |

~85% = the *operator hour* shrinks to ~6/wk. The remaining ~34 hr is the analyst-work the role actually pays for (client calls, judgment on extraction, scope decisions, prompt tuning, commercial negotiation). That's the target: calmer, more focused, same hours, better quality.

**Caveat**: B4b's toil-removal estimate (~3-6 hr/wk) is contingent on Matyo + Petar also using it. If only Ivo uses it, drop ~2 hr/wk off the cumulative.

(B6 dropped 2026-05-17 — Asana Gantt covers the dashboard need without building a third surface.)

---

## Reminder

Every loop drafts. None send. Outward-facing actions stay on the approval rule (`outward-facing-actions.md` memory). The point is removing toil, not removing the human.
