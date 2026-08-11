# Engagement-context system: the plan

A living plan for restructuring how engagement context is stored, bootstrapped, and
pre-filled. Built **incrementally** — Ivo adds ideas, we sequence them, nothing gets
built or moved until the relevant step says so.

Status: **structure decided (2026-05-12), ready to build the bootstrap (step A2).**
Related: `README.md` (the broader optimisation thesis), `LAYER1_CONTEXT_TEMPLATE.md`
(earlier draft this supersedes for the engagement-folder part), `OPEN_QUESTIONS.md`.

---

## 0. Decisions (logged 2026-05-12)

- **Top-level folder**: `engagements/` (plural), in a **new dedicated private repo** — the
  existing `Axion` folder is a mix (engagements, playground demos, commercial talks, experiments,
  conversation extracts) and needs its own cleanup separately; the new engagements tree starts
  clean in its own repo. ✔
- **Per-company layout**: numbered stage folders `1_pre-scoping / 2_scoping / 3_contracting /
  4_poc / 5_implementation` (contracting gets its own stage). Created lazily — bootstrap drops in
  `1_pre-scoping/` + the core files; later stages appear when work starts on them. ✔
- **Core files at the company-folder top level**: `CONTEXT.md` + `STATUS.md` + `SOURCES.md` +
  `COMMERCIAL.md` (the Jordan/HubSpot thread — pricing, deal stage, NDA/SoW status, negotiation
  notes — gets its own file, distinct from the technical context). Heineken's existing
  `human-in-the-loop/CONTEXT.md` stays where it is (different folder, no clash). ✔
- **Bootstrap mechanism**: a `/new-engagement <company>` command (not a `cp -r` template) that
  creates the skeleton and prompts for lead source / stakeholders / known type, filling
  `CONTEXT.md` / `COMMERCIAL.md` as it goes. ✔
- **New-engagement trigger behaviour**: ask first ("looks like a new engagement *Acme*, create
  it?") → on yes, build under `engagements/_pending/` → Ivo promotes to `engagements/` when sure.
  First few weeks only; tighten to direct-create once company-matching is trusted. ✔
- **Brief / loop-output location**: per-engagement briefs in `engagements/<company>/_briefs/`,
  committed to git; the weekly cross-engagement rollup + CFO brief in a central `atlas/rollups/`
  (or the new repo's equivalent), committed. ✔
- **Migration scope**: active engagements first (Heineken, SMS, Aumovio, Agrolimen, T&F, + any
  other live ones), then earlier-stage ones, then dead ones get a one-line tombstone `STATUS.md`.
  Not all 28 in one pass. ✔
- **HubSpot MCP admin**: TBD — Ivo to find out who has HubSpot admin. Until then the trigger runs
  on Calendar alone; the commercial half of the context stays manual. ⏳
- **Calendar event naming**: inconsistent (sometimes company name, sometimes the contact person's
  name, sometimes both). The Calendar→company matching has to be designed defensively (attendee
  email domains + an `Aliases` line in `CONTEXT.md` + fuzzy title match + ask-Ivo fallback);
  investigate the actual patterns once the Calendar MCP is connected. ⏳

---

## 1. Why this first

Ivo's actual daily job is running scoping exercises and PoCs across many parallel
engagements. The bottleneck is *understanding* — keeping the live state of ~28 engagements
in his head so he can direct them and so the tech team can pick one up cold without "ask Ivo".
Today the context lives in inconsistent `scoping/<client>/` folders + ad-hoc Drive uploads.

This is the highest-leverage thing **for Ivo specifically** (the org-wide PR dashboard etc.
are the tech team's wins): it's already mostly being done by hand, it's the documented
bottleneck ("Alex asks me, I check, I answer"), and it's the data layer the company knowledge
base + the business↔tech translator both need anyway.

---

## 2. The engagement lifecycle (the thing the structure has to model)

One pipeline, long pre-history, a fork near the end. Ivo enters around the pre-scoping call.

| #  | Stage                    | Who                                  | Notes                                                                                                                                                                                              |
|----|--------------------------|--------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0  | Lead in                  | Jordan (+ external agency sometimes) | conference / LinkedIn / common contact                                                                                                                                                             |
| 1  | Intro call               | Jordan; HubSpot set up               | Ivo NOT in it                                                                                                                                                                                      |
| 1b | (optional) tech Q&A call | Ivo                                  | only if the contact is technical (e.g. T&F); Ivo just answers questions                                                                                                                            |
| 2  | Pre-scoping call         | Ivo                                  | explains the "file sign", generates the Neuralith upload link → client uploads → S3. **Ivo enters here for real.**                                                                                 |
| 3  | Scoping work             | Ivo, solo                            | pull from S3, run extraction (Chandra script → GPT models → results), decide what matters *to this client* from their notes                                                                        |
| 4  | Scoping presentation     | Ivo presents; Jordan runs it         | the HTML deliverable, 1-2 wks after pre-scoping; maybe send results. Jordan does the last 10-15 min on which NDA/SoW docs are needed                                                               |
| 5  | Contracting              | Ivo preps docs; legal                | NDA + SoW back-and-forth, 2-5 docs, scope the use case, ~100 docs agreed                                                                                                                           |
| 6  | PoC / MVP                | Ivo + tech team                      | 8-10 wks: ~2 wk kickoff (gather all case info) → 4-6 wk implementation (tech uses Kiro/Claude Code — **Ivo's info package is load-bearing here**) → eval + deliver; weekly checkup call throughout |

**The fork** (decided around stage 4-5, fully clear by stage 6):

- **Axion / extraction** — unstructured (PDF) and/or structured (XML); Chandra → GPT; eval ritual = give the client
  10% (10 of ~100 docs), they return ground truth, optimise against it. (iBrul, Garrett, Donev, SMS, Agrolimen, Aumovio)
- **RAG / SQL-agent** — files into a DB, an agent answers questions. (Heineken)
- **Hybrid** — both, wired together with a Claude-Code agent on top. SMS Group is the extreme: Excel extraction +
  hydraulic-from-.cut + electronic-from-PDF + tables-in-PDF, all connected.

**Stakeholder pattern** (consistent): ~2 people per call — a **business owner / SME** Ivo talks to daily over Teams
chat (has the rules), and a **manager** Ivo syncs with weekly (has the gates). Heineken: Justyna (business owner) +
Lucy (manager). The folder must capture both threads.

**Current state varies wildly** — SMS/Aumovio/Heineken wrapping up PoCs; Agrolimen pre-PoC with a changed SoW; others
earlier; T&F just got a scoping proposal. The structure must make "where is this one" obvious.

---

## 3. The folder structure (proposed)

### Top level: `engagement/<company>/`

Rename `scoping/` → `engagement/`. Each company folder holds:

```
engagement/
  <company>/
    CONTEXT.md            ← the stable picture (one per engagement)
    STATUS.md             ← the live log, whole lifecycle, newest on top   (one per engagement)
    SOURCES.md            ← index pointing into all the numbered folders + Drive/HubSpot/Teams
    COMMERCIAL.md         ← the Jordan/HubSpot thread: pricing, deal stage, NDA/SoW status, negotiation notes
    _legacy/              ← the old flat files, moved here wholesale, untouched, referenced from SOURCES.md
    _briefs/              ← auto-generated meeting-prep briefs (YYYY-MM-DD.md), see §5; committed to git
    1_pre-scoping/        ← created by /new-engagement; later stages appear when work starts on them
      transcripts/        ← intro / tech-Q&A / pre-scoping call transcripts
      notes.md            ← Ivo's working notes from this stage
    2_scoping/
      transcripts/
      data/               ← pointer to the S3 docs pulled for the demo (s3://iris-engagements/<company>/raw/)
      extraction/         ← Chandra/harness config + intermediate results (if Axion-type)
      deliverable.html    ← the scoping presentation
    3_contracting/
      transcripts/        ← contracting calls
      contracts/          ← NDA, SoW, the back-and-forth clarification docs (working copies; signed originals referenced)
    4_poc/
      transcripts/        ← weekly checkup calls
      data/               ← pointer to the agreed ~100 docs in S3
      sample-10pct/       ← initial extraction sent to the client for ground truth (Axion-type)
      ground-truth/       ← what the client sent back (Axion-type)
      eval/               ← scores over time (Axion-type)
    5_implementation/
      transcripts/
      handoff.md          ← the package handed to the tech team to start building
```

(The new structure starts in a **dedicated private repo**, not in `Axion/`. The `Axion/` folder
is a mix — engagements, playground demos, commercial talks, experiments, conversation extracts —
and needs its own cleanup separately. the agent map and this plan live in `~/Documents/atlas/`.)

### The principle: stage-scoped vs engagement-scoped

- **Stage-scoped** (lives inside a numbered folder): anything that *happened during* that stage — transcripts of that
  stage's calls, that stage's data/scripts/deliverables, that stage's contracts.
- **Engagement-scoped** (lives at `engagements/<company>/` top level): the things there's only ever *one* of —
  `CONTEXT.md`, `STATUS.md`, `SOURCES.md`, `COMMERCIAL.md`, `_legacy/`, `_briefs/`. Content that spans stages (the
  business owner's rules carry from scoping into PoC) lives in `CONTEXT.md`, which is *derived from* the transcripts.
  Raw transcripts are events; events happen during a stage.

### Why numbered prefixes

So the folder listing sorts in lifecycle order — same trick as `aws-usecase/__examples/01_intro...`. Glance at the
listing → know the stage (`4_poc/` has stuff, `5_implementation/` empty → mid-PoC). The tech-Q&A call's transcript (when
there is one) just goes in `1_pre-scoping/transcripts/` — no separate `0_intro/`, since Ivo isn't doing work there.

### Lazy creation

`/new-engagement` drops in the core files + `1_pre-scoping/` only. Later stage folders appear when work starts on them.
Empty stage folders are clutter; some engagements skip stages (e.g. no separate tech-Q&A call).

### Legacy

Per engagement: the new canonical files go at the top of `engagements/<company>/`; everything that exists today (in old
`scoping/<company>/`) moves wholesale into `engagements/<company>/_legacy/` (the pattern
`arcelormittal-usecase/_legacy/` already uses). Nothing deleted, nothing converted in place, referenced from
`SOURCES.md`.

---

## 4. The three core files

### `CONTEXT.md` — the stable picture (changes rarely; regenerated, not hand-maintained from scratch)

Top of the file, machine-readable header:

- **Stage**: one of
  `lead-in / intro / pre-scoping / scoping / contracting / poc-kickoff / poc-implementation / eval-deliver / closed-won / closed-lost`
- **Type**: `axion-extraction / rag / hybrid / TBD`
- **Lead source** + who introduced them

Then sections:

1. **Engagement** — client, what they do, one-paragraph use-case summary.
2. **The problem** — what the client is trying to solve, in their words.
3. **The Axion/Neuralith angle** — which product, what it does for this case.
4. **What this client cares about** — the 2-3 things that matter most (the thing currently only in Ivo's head between
   the notes and the HTML demo; exactly what the tech team needs in stage 6).
5. **Data** — what exists, where it lives (S3 paths), format, quality, access status, key gotchas ("tab 'In progress' is
   source of truth, the rest is derived").
6. **Stakeholders** — table: name, org, role (business-owner / SME / manager / champion / decision-maker), how Ivo
   reaches them (Teams chat daily / weekly call), availability notes (holidays, OOO).
7. **Current phase + "done"** — where in the lifecycle, what "done" looks like for this phase. (The *commercial* gate —
   signed? budget? decision from whom? — lives in `COMMERCIAL.md`, cross-referenced here.)
8. **Source pointers** — link to `SOURCES.md`, call out the 2-3 canonical artifacts.

- **Aliases** — "also known as: Acme Corp, ACME, acme.io" — used by the Calendar/HubSpot matching (§5).

Voice: descriptive, factual, system-prompt style. No em dashes (commas / colons / parentheses).

### `COMMERCIAL.md` — the sales/commercial thread (the Jordan / HubSpot side)

Distinct from the technical context; the tech team mostly ignores it, Ivo and Jordan and Steven care. Sections: deal
stage (mirrors HubSpot once that MCP is wired), how the lead came in, pricing discussed / agreed, the commercial gate (
what has to happen to progress, decision from whom), NDA/SoW status and the back-and-forth, how Jordan plans to
negotiate the PoC based on how the scoping landed, anything Steven needs for the commercial meeting. Once the HubSpot
MCP is connected, the deal-stage / activity parts get pulled in as a draft section Ivo edits — never auto-overwritten.

### `STATUS.md` — the live log (changes constantly; append-only, newest on top)

One entry per meaningful event (call, blocker, decision, doc sent). Shape:

```
## 2026-05-12
- What happened: <one or two lines>
- Blocked on: <thing> — owner: <who> (or "not blocked")
- Next action: <thing> — owner: <Ivo / whom> — by: <date if any>
- Notes: <optional>
```

Meeting transcripts get **summarised into** this, not left raw (the raw transcript stays in the stage's `transcripts/`,
referenced from `SOURCES.md`). Honest: blocked means blocked, skipped means skipped. This is what the morning brief, the
weekly rollup, and the stale-engagement watchdog read.

### `SOURCES.md` — the artifact index ("docs written for the agent")

One line per artifact + (where relevant) which sheet/section is the one that matters. Lets an agent find "tab 7 is
source of truth" without Ivo saying so. Sections: Canonical / Meeting notes & transcripts / Data samples / Generated
artifacts / Contracts / External (Drive links, HubSpot, Slack/Teams channels).

### Extraction extras (Axion-type only)

When the fork is known to be Axion-type, the bootstrap (or a later step) adds, under `2_scoping/` and `4_poc/`:
`extraction/` (Chandra/harness config + intermediate results), `sample-10pct/`, `ground-truth/`, `eval/` (scores over
time). RAG-type engagements don't get these. Large binary (the actual client docs, Chandra output, results) lives in S3,
not git — the folders hold pointers; see §8a.

---

## 5. The trigger: Calendar + HubSpot pre-fill engagements for Ivo

The high-value part. Ivo sees upcoming meetings via Google Calendar (Jordan books them); a lot of pre-Ivo context lives
in HubSpot (company, contacts, deal stage, Jordan's call summaries). With MCPs to both, a loop can bootstrap and
pre-fill engagements *before Ivo walks into a meeting cold*.

### The two jobs (don't conflate)

**Job 1 — bootstrap a new engagement.** A Calendar event whose title/attendees match a company with *no*
`engagement/<company>/` folder → a new lead at the pre-scoping stage. The loop: creates the folder skeleton (the lazy
bootstrap from §3), seeds `CONTEXT.md` with what HubSpot knows (company, who introduced them, deal stage, Jordan's call
summaries), flags it for Ivo: "new engagement *Acme* — pre-scoping call Tue 3pm — folder started, here's the draft
context, fill the gaps."

**Job 2 — prep an upcoming meeting (new or existing).** Each morning (or N hours before each call): for each Calendar
event, find the matching engagement folder, pull `CONTEXT.md` + recent `STATUS.md` + recent transcripts + (once wired)
latest HubSpot activity + the relevant Slack/Teams thread → a one-page brief: who's on the call, what stage, what
happened last time, open action items, the 3 things this client cares about, what Ivo should be ready to say. Drops it
in `engagement/<company>/_briefs/YYYY-MM-DD.md` and pings Ivo. (This is the agent-map "personal meeting assistant" + "
morning brief", pointed at Ivo's job.)

### The matching problem (design for it from the start)

Calendar event ↔ HubSpot company ↔ engagement folder. Title text won't always be clean ("Iris <> Acme call" vs "Acme –
tech sync"). Keys, in priority order: (1) HubSpot meeting↔company association if Jordan set it; (2) attendee email
domains; (3) the `Aliases` line in `CONTEXT.md`; (4) fuzzy title match as last resort. Unmatched → ask Ivo, don't guess.

### Human-in-the-loop rules

The loop **drafts**, never acts: no email sent, no HubSpot edit, no overwrite of `CONTEXT.md` (it writes a
`CONTEXT.draft.md` diff to merge, or appends a "from HubSpot" section Ivo edits). On bootstrap especially — an agent
matching the wrong company to a calendar event and creating a junk folder is the classic "Stripe email matched to a
Google email" failure — it either asks before creating, or creates into `engagement/_pending/` for Ivo to promote.
Default for the first few weeks: ask → stage in `_pending/` → Ivo promotes; tighten to direct-create once the matching
is trusted.

### MCP availability

- **Google Calendar MCP** — available in this environment, needs an OAuth handshake. Low effort, do first.
- **HubSpot MCP** — official server exists; not wired here yet. Needs a HubSpot admin to authorize + a scope decision (
  read-only on companies/contacts/deals/engagements is enough). Medium effort, gated on an admin.
- **Gmail MCP** — available (deferred). Picks up the pre-Jordan email threads + external-agency intro emails. Optional,
  cheap.

---

## 6. Build order (incremental — each step useful on its own)

Two parallel tracks once the folder structure exists. **Track A** = the context system (folders,
loops, MCPs). **Track B** = the tooling/infra (scoping harness, AWS, dashboard). Track B can
start as soon as the folder *spec* is settled; it doesn't wait for the migration.

### Track A — the context system

1. **Spec** — this doc. ✔ structure decided (§0). Remaining: the `/new-engagement` prompt flow + the exact
   `CONTEXT/STATUS/SOURCES/COMMERCIAL` templates (done as part of A2).
2. **New repo + bootstrap** — create the dedicated private `engagements` repo with a `_template/` and a
   `/new-engagement <company>` command that creates `engagements/<company>/` with the core files + `1_pre-scoping/`,
   prompting for lead source / stakeholders / known type and filling `CONTEXT.md` / `COMMERCIAL.md`. Ivo runs it
   manually first. Half a day.
3. **Migrate ONE engagement as proof** — Heineken (most files, most mature, RAG-type): move everything to `_legacy/`,
   build clean `CONTEXT / STATUS / SOURCES / COMMERCIAL` at the top + the stage folders for stages it's actually
   reached. Ivo reviews: "could a tech person start the PoC from this cold?" If yes → step 4. If no → fix the template
   before touching anything else.
4. **Roll out to active engagements** — SMS, Aumovio, Agrolimen, T&F, + any other live ones; then earlier-stage ones;
   then dead ones in old `scoping/` get a one-line tombstone `STATUS.md` (or are left as-is until touched). Same
   fold-down, faster once the pattern's set.
5. **Wire Calendar MCP** → build the **meeting-prep loop** (Job 2): every morning, brief each of today's/tomorrow's
   calls from the folders. Smallest thing that changes Ivo's routine; valuable even before HubSpot.
6. **Wire HubSpot MCP** (once an admin authorizes it) → the prep brief + the bootstrap get the commercial half (deal
   stage, Jordan's notes, prior summaries); the trigger can also detect new engagements from HubSpot deal-stage changes,
   not just Calendar.
7. **Connect the two** → Calendar event for an unknown company → bootstrap into `_pending/` → ping Ivo to confirm →
   promoted to a real engagement folder. Known company → prep brief.
8. **Post-meeting digest loop** — a `/loop` that watches the stage `transcripts/` dirs and folds new meeting notes into
   `STATUS.md` + extracts action items/owners/dates + drafts the follow-up message (Ivo reviews/sends).
9. **Weekly cross-engagement rollup + CFO brief** — every Friday: what moved on all engagements, what's blocked and on
   whom, what needs an Ivo decision, which SoWs are pending. Two outputs from the same data: the Monday-product-sync
   rollup (tech-flavoured) and the **CFO brief** for Steven (commercial-flavoured: milestones, slippage, pipeline — no
   tech detail). Falls out of the dashboard data (§9b).
10. **(later)** Gmail MCP for pre-Jordan email threads; graduate stable loops from local `/loop` to cloud `/schedule` (
    the cloud = the EC2 box, §9c).

### Track B — tooling & infra (can start in parallel after step 1)

B1. **S3 prefix standardisation** — the Neuralith upload link already drops client files into an S3 bucket; standardise
the layout (`s3://iris-engagements/<company>/raw/ | processed/ | results/ | ground-truth/`). Half done already — mostly
a naming convention + a small migration of existing local data up. Unblocks everything else in Track B.
B2. **Reusable scoping harness** — one repo/folder with the Chandra runner + the GPT-extraction step parameterised by
doc-type (PDF-unstructured / XML-structured / Excel / hybrid) + the eval scaffold (10%-sample → ground-truth → optimise
loop). Point it at an engagement's S3 prefix + a config → it produces structured results. Replaces the
bespoke-per-engagement scripting. **Biggest hours-saver after the context system.** *(◆◆◆)*
B3. **EC2 worker box** (the one Ross OK'd, ~`t3.small`) — runs the scoping harness triggered by new objects landing in
an engagement's S3 prefix (S3 event or a cron), so **extraction runs overnight on the box, not on Ivo's laptop while he
waits**. Also the future home for the Track A loops + the dashboard cron. *(◆◆)*
B4. **Deliverable (HTML demo) generator** — turns the harness output + the "what this client cares about" section of
`CONTEXT.md` into a first-draft scoping-presentation HTML (same self-contained style as the agent map). Ivo edits,
doesn't build from scratch. *(◆◆)*
B5. **Eval-driven extraction loop** — when the client returns ground truth into `.../ground-truth/`, the box re-runs the
harness, scores against it, surfaces the worst cases; Ivo adjusts prompt/config; re-runs. Tight verifiable loop: agent
grinds, Ivo judges which misses matter. *(◆◆)*
B6. **PoC status dashboard** — a single self-contained HTML page that reads every `CONTEXT.md`/`STATUS.md` and draws the
**week-by-stage roadmap grid** (rows = engagements, columns = calendar weeks, cells coloured by stage, current week
marked, expected stage-ends shown lighter) + a per-row side panel (blocked-on, next milestone, commercial gate).
Regenerates on a cron so it's never stale (the problem with the hand-maintained Excel). The CFO brief (step 9) is the
same data in prose. *(◆ once folders + dashboard data exist)*
B7. **SoW/NDA drafter** — reads `CONTEXT.md` + the closest prior SoW (Agrolimen←SMS←Aumovio lineage) + the standard
legal language → first draft. Hard human gate: never leaves / not final without Ivo's review; a second "judge" agent
checks numbers/dates/scope against the source docs. Already sketched in `LOOPS.md`. *(◆◆)*
B8. **PoC kickoff handoff generator** — produces `4_implementation/handoff.md`: synthesises the scattered context (
transcripts, business rules, data gotchas, eval criteria) into language a Kiro/Claude-Code session can act on. The "
business→tech translator" scoped to the kickoff moment. *(◆◆)*

### Suggested interleave

`A1 (spec)` → then **fork**: `A2→A3 (bootstrap + Heineken proof)` in series, and `B1 (S3 prefixes)` +
`B2 (scoping harness)` in parallel. Then `A4 (rollout)` ‖ `B3 (EC2 worker)`. Then `A5 (Calendar+meeting-prep)`,
`B6 (dashboard)` falls out cheaply, `B4/B5 (deliverable gen + eval loop)` ride on B2/B3. `A6-A10` and `B7-B8` after the
structure is load-bearing.

---

## 7. Open questions

**Resolved 2026-05-12** (see §0): top-level name, stage folders, core file names, the
`COMMERCIAL.md` split, bootstrap mechanism, trigger behaviour, brief location, migration scope,
new repo. The rest:

1. **HubSpot MCP admin** — who has HubSpot admin and can authorize a read-only MCP (
   companies/contacts/deals/engagements)? *Ivo to find out.* Until then the Calendar-only path runs.
2. **Calendar event naming** — confirmed inconsistent (company name / contact-person name / both, no fixed format).
   Matching has to be defensive (attendee email domains + `Aliases` in `CONTEXT.md` + fuzzy title + ask-Ivo fallback);
   investigate the real patterns once the Calendar MCP is connected.
3. **EC2 box specifics** — instance size (Chandra is GPU-ish — `t3.small` likely not enough; consider `g4dn`, or call a
   hosted OCR endpoint instead, cf. the AlexFert PaddleOCR endpoint pattern), region (eu-west-1 to match the
   SSO/Neuralith setup?), auth (instance profile + SSM Parameter Store for the OpenAI/Tactiq/HubSpot keys).
4. **Google Drive** — keep it as a one-way git→Drive projection for the tech team (Drive MCP), or retire the Drive step
   and give the tech team repo / dashboard-link access directly? *Decide once repo-as-source-of-truth is settled.*
5. **S3 bucket name + structure** — confirm with Ross whether
   `s3://iris-engagements/<company>/{raw,processed,results,ground-truth}/` matches what he provisioned, and whether
   that's the same bucket the Neuralith upload link already writes to (or a different one to consolidate).
6. **`atlas/` (this folder)** — the ops layer: this plan, the agent map, LOOPS / MCP_SETUP / MOBILE_APPROVAL, the
   scoping harness when built. Its own git repo at `~/Documents/atlas/`. The remaining `Axion/` folder (the *-usecase
   reference dirs, tactiq_export, playground demos, loose files) is a separate cleanup, not blocking.

---

## 8. Getting it off the laptop: AWS + sync architecture

Today most of this lives locally on Ivo's machine because he runs Claude Code there; some files
are shared with the tech team via Google Drive; client uploads already land in S3 via the
Neuralith link. The goal: one place that's authoritative, reachable from the laptop, from the
EC2 box, and (read-only) from the tech team — without Ivo babysitting syncs.

### 8a. What lives where (the split)

| Thing                                                                                                 | Home                                                                                                                                           | Why                                                                       |
|-------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| Client docs, Chandra output, extraction results, ground truth                                         | **S3** (`s3://iris-engagements/<company>/{raw,processed,results,ground-truth}/`)                                                               | already lands here from Neuralith; big binary; doesn't belong in git      |
| The `engagement/<company>/` markdown context (`CONTEXT/STATUS/SOURCES`, stage `notes.md`, `_briefs/`) | **git repo** (this `Axion` repo or a dedicated one), checked out on Ivo's laptop *and* on the EC2 box                                          | small, diffable, the thing both humans and agents read; git *is* the sync |
| Transcripts                                                                                           | **git repo** under the stage's `transcripts/` (they're small text) — large audio (rare) goes to S3, referenced                                 | so the digest loop can read them on either machine                        |
| Deliverable HTML, the dashboard HTML                                                                  | git repo (`atlas/` or per-engagement) + optionally pushed to S3 for sharing a link                                                             | small; the source of truth is git                                         |
| SoWs / NDAs / contracts                                                                               | git repo under `<company>/3_poc/contracts/` (the working copies); the *signed* originals wherever legal keeps them, referenced in `SOURCES.md` | contract-grade — versioned, but the legally-binding copy isn't here       |

**The principle:** *context is git, data is S3.* Git handles the markdown sync between laptop and
box for free (commit on one, pull on the other — or a cron `git pull` on the box). S3 is the
shared blob store the EC2 worker reads from and writes to. Nothing needs a separate sync tool.

### 8b. Google Drive's role

Drive stays as the **share-out channel with the tech team and Jordan**, not a source of truth.
Two cleaner ways to handle it than today's manual uploads:

1. **Drive MCP** (available, deferred) → a loop that, when an engagement reaches PoC-kickoff,
   pushes the relevant `engagement/<company>/` markdown + the deliverable HTML to a Drive folder
   the tech team can read. One-way: git → Drive. Drive is a *projection*, never edited back.
2. Or simpler: don't sync to Drive at all — give the tech team read access to the git repo (or
   the dashboard HTML link) and retire the Drive step. Decide later (OQ-13).
   Either way: Drive is downstream, never upstream. Avoids the "which copy is right" problem.

### 8c. The EC2 worker

A small box in IRIS's AWS account (Ross approved EC2 + S3 + budget), e.g. `t3.small`:

- has the git repo checked out (cron `git pull`, or a webhook)
- runs the **scoping harness** (B2) when new objects land in an engagement's S3 `raw/` prefix
  (S3 event notification, or a cron polling) — extraction runs *overnight on the box*, not on
  Ivo's laptop while he waits
- runs the **dashboard + CFO-brief generators** on a morning cron
- runs the **eval-driven extraction loop** (B5) when ground truth lands
- later: the Track A `/loop` jobs (meeting prep, post-meeting digest, weekly rollup) move here —
  this *is* "graduate from local `/loop` to cloud `/schedule`" in `LOOPS.md`
- writes back: results to S3, status updates committed to git, briefs committed to git
- **Mobile-in-the-loop still holds** — the box drafts and runs, but anything outward-facing or a
  real decision pings Ivo's phone to approve (Layer 4 / `MOBILE_APPROVAL.md`). A cloud worker
  with no phone gate is just unsupervised.

### 8d. Security notes (it's IRIS client data on a shared account)

- All S3 buckets **private**, block public access, default encryption; the engagement repo is
  private; the EC2 box in a restricted security group (ideally a private subnet + SSM access, not
  a public IP). No presigned-link sharing of client data without thinking.
- Be deliberate about **git vs. not**: client docs and credentials never go in git (they're in S3
  / a secrets store); the markdown context does. A `.gitignore` enforces it. Credentials the box
  needs (OpenAI key, Tactiq token, HubSpot token) go in SSM Parameter Store / Secrets Manager,
  not in the repo (the repo currently has `tactiq_export/export.py` with hardcoded tokens — that
  pattern doesn't move to the box).
- The Neuralith upload link is already time-boxed (2-3 days) — fine; just confirm the bucket it
  writes to is the standardised one (8a).

### 8e. Migration order (don't do it all at once)

1. **S3 prefix standardisation** (B1) — convention + move existing local data up. Lowest risk, unblocks the rest.
2. **EC2 worker for the scoping harness** (B2→B3) — the biggest "stop doing this on my laptop" win. The box reads S3,
   writes S3, doesn't touch git yet.
3. **Repo on the box** — check out the engagement repo on the box, cron `git pull`. Now the dashboard cron (B6) and CFO
   brief can run there.
4. **Move the Track A loops to the box** — once they're proven locally (per `LOOPS.md`'s graduation rule). Layer 4
   phone-gate becomes mandatory at this point.
5. **Drive projection** (8b option 1) or **retire Drive** (option 2) — decide once the repo-as-source-of-truth is
   settled.

---

## 9. More ideas (parking lot — Ivo adds here as they come)

- *(add freely; we sequence them into §6 when they're ripe)*
