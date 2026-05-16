# Session log — 2026-05-12

A narrative record of the session that built the agent map and bootstrapped the engagement
system. For "what's the state / what's next" read `STATE.md`; for the plan read
`ENGAGEMENT_PLAN.md`. This file is the long-form "how we got here" in case the conversation
itself is gone.

## Part 1 — the AI agent map

- Context: IRIS Strategy Day, 12 May 2026, Part 2 ("AI Driven Development Knowledge Sharing").
  The room brainstormed integrating AI into how IRIS works; Victor asked for a diagram of "what
  context feeds which agent and how they hand off". Source transcript:
  `Strategy Day - Part 2 - AI Driven Development Knowledge Sharing.txt` (also folded in updates as
  the live meeting progressed via the Tactiq API — `_live/fetch_current.py`, meeting id
  `8btqs919sbrISDQAvDi1`; final ~817 blocks / ~76 min, then the meeting ended).
- Built `AGENT_MAP.html` (v1): 5 lanes — context sources → unified knowledge store (+ a central
  agent-settings repo) → dev pipeline (1 requirements → 2 planner → 3 implementer ↔ 4 reviewer →
  5 human review → 6 docs+hooks) → 11 standalone agents (repo-monitoring auto-fixer, code-reuse/
  dedup, onboarding generator, deployment agent, email-reply agent, code-intelligence/migration,
  personal meeting assistant, business↔tech translator, team-orchestration, org-wide PR dashboard,
  personalization layer). Flat Lucide-style SVG icons in tinted badges; trigger pills (event-driven
  / live-in-IDE / scheduled / on-commit / on-demand / passive); impact (●●●/●●/●) + build-effort
  (◆/◆◆/◆◆◆) badges; "How to read this" legend with the takeaways.
- Built `AGENT_MAP_V2.html`: a redesign per a self-critique — cards trimmed to headline + one
  sentence, lane 4 a true 3-column grid, impact/effort moved to a quiet card footer alongside the
  trigger, all dense detail moved to a numbered "Detail notes" section + "The takeaways" at the
  bottom, ~5-step type scale, beefier arrows. V1 kept untouched.
- Instructions captured along the way: **no em dashes** in docs; **no PNG/PDF exports** of the map
  (HTML only).
- Sidebar: briefly deployed v1 to a private S3 bucket (`iris-internal-agent-map`, eu-west-1, via
  Ivo's SSO profile `Iris_Devs-565393074262`) with a presigned link, then **deleted it** at Ivo's
  request (no AWS resources left from that). Discussed but rejected: client-side password gate,
  EC2+nginx basic-auth, Cloudflare — decided the HTML file is just shared directly.

## Part 2 — the engagement-context system

- Established Ivo's actual lifecycle: lead-in (Jordan, sometimes external agency) → intro call
  (Jordan; Ivo not in it) → optional tech-Q&A call (Ivo answers questions) → **pre-scoping call**
  (Ivo enters: explains the "file sign", generates a Neuralith upload link → client uploads → S3)
  → scoping work (pull from S3, run Chandra → GPT, decide what matters, build an HTML demo) →
  scoping presentation (Ivo presents, Jordan runs it, last 10-15 min on which NDA/SoW docs are
  needed) → contracting (NDA + SoW back-and-forth, ~100 docs agreed) → PoC/MVP kickoff (8-10 wks:
  ~2 wk kickoff → 4-6 wk implementation, tech uses Kiro/Claude Code, **Ivo's info package is
  load-bearing here** → eval + deliver; weekly checkup call throughout).
- The fork: **axion-extraction** (PDF/XML; Chandra → GPT; eval ritual = give the client 10% → they
  return ground truth → optimise) / **rag** (files into a DB, SQL-agent answers) / **hybrid** (both,
  agent on top — SMS Group is the extreme). Stakeholder pattern: a business-owner/SME Ivo talks to
  daily over Teams chat + a manager Ivo syncs with weekly (Heineken = Justyna + Lucy).
- Wrote `ENGAGEMENT_PLAN.md` — the canonical plan. Decisions logged in its §0:
  - top-level folder `engagements/` (plural), in a **new dedicated private repo** (`~/Documents/
    engagements/`) — the old `Axion/` is a junk drawer needing its own cleanup.
  - per-company: `CONTEXT.md` + `STATUS.md` + `SOURCES.md` + `COMMERCIAL.md` at the top; numbered
    stage folders `1_pre-scoping / 2_scoping / 3_contracting / 4_poc / 5_implementation`, created
    lazily; `_legacy/` for old flat files; `_briefs/` for auto meeting-prep briefs (committed);
    `_pending/` for trigger-staged new engagements awaiting Ivo's promotion.
  - bootstrap via a `/new-engagement <company>` slash command (not a bare `cp -r`).
  - new-engagement trigger (Calendar/HubSpot): ask first → stage in `_pending/` → Ivo promotes;
    tighten later.
  - migration: active engagements first (Heineken, SMS, Aumovio, Agrolimen, T&F), then earlier-
    stage, then dead ones get a one-line tombstone `STATUS.md`.
  - the trigger idea: Calendar MCP (works now, OAuth) + HubSpot MCP (needs an admin) → a loop that
    bootstraps new engagements from calendar events and produces a meeting-prep brief before each
    call. Plus extensions discussed: reusable scoping harness, deliverable-HTML generator, eval-
    driven extraction loop, PoC status dashboard (week-by-stage roadmap grid) + CFO brief for
    Steven, SoW/NDA drafter, PoC handoff generator. And the AWS move: S3 for data, an EC2 worker
    box (Ross approved) to run the harness overnight + the loops + the dashboard cron, "context is
    git, data is S3", Drive as a downstream projection only.
- **Built (step A2):** the `engagements` repo — `_template/` (the four core files + `1_pre-scoping/`
  with `transcripts/.gitkeep` and `notes.md`), `.claude/commands/new-engagement.md`, `README.md`,
  `.gitignore` (keeps client data + credentials out). Committed `fb5ba2a`.
- **Moved `_optimize/` → `~/Documents/atlas/`**, made it its own git repo (commit `3b3b6dc`),
  fixed cross-references (`engagements/README.md` → `~/Documents/atlas/ENGAGEMENT_PLAN.md`;
  `_live/fetch_current.py` path → `../../Axion/tactiq_export/`), left `Axion/_optimize/MOVED.md`
  as a breadcrumb, wrote `STATE.md`, updated the auto-memory (`atlas_engagements_relocation.md` +
  a `⚑ Relocation` line atop `~/.claude/projects/-Users-iris-Documents-Axion/memory/MEMORY.md`).

## What's next

**Step A3 — migrate Heineken as the proof of the structure.** Move everything from
`Axion/scoping/heineken/` into `engagements/heineken/_legacy/`, build clean `CONTEXT / STATUS /
SOURCES / COMMERCIAL` at the top + the stage folders for stages it's actually reached. Ivo reviews
and answers: **"could Alex start the Heineken PoC from these four files cold, without asking me
anything?"** If yes → roll out to the other active engagements + start Track B (S3 prefixes,
scoping harness) in parallel. If no → fix the template before touching anything else.

Still open / Ivo to find out: who has HubSpot admin; how Jordan names calendar events (confirmed
inconsistent); EC2 box specifics (Chandra is GPU-ish); the S3 bucket Ross provisioned; whether
Google Drive stays as a projection or is retired; the `Axion/` cleanup (separate exercise).

## Session log — 2026-05-13 (afternoon): SMS demo-prep live-assist

Live-assist session during back-to-back SMS calls (Vankata + Aleksandar internal demo-team
sync → Vankata + Victor demo-narrative call → Vankata + Jordan + Steven + Petar presentation
sync). Ivo was running between calls; Claude provided real-time briefings off transcript
fragments + the engagement docs.

What got produced (all in `engagements/sms-group/`):

- **SMS demo brief** (one-shot, in chat) — full state of where the Gerald demo prep stands:
  what Thorsten signed off on May 7 (locate-on-PDF, 4 NL queries incl. PD12, PLC symbolic-
  address Excel export, tree/document/chat views), Victor's framing from May 12 (lead with
  business case, 3 differentiators, careful with "digital twin", reuse Neuralith viewers),
  the 5-stage Phase-2 plan, commercial levers Jordan flagged, date status (Thorsten asked to
  reschedule next-Tue 19 May → now June 2 floated → Vankata fighting to keep ~19 May
  to avoid 3-week gap; resolved in-call to Wed 20 May).
- **Thorsten "knowledge in heads" quote pull** — for the deck's vision/opening slide. The
  May 7 retirement / tens-of-millions quote (*"60 years old… the guy is not there in the
  future"*), the Dec 17 Gerald-in-the-room *"old SMS world — only a human guy reading
  these documents knows"*, and the Apr 21 *"100 modules, I have to go to the EPLAN page
  by page… but then I can ask the system"*.
- **Live-call catch-ups** — during the May 13 demo-narrative call (Vankata + Victor + Alex
  + Petar) Ivo stepped away repeatedly; Claude reconstructed where the architecture debate
  had landed (Victor: hydraulic chains stored as separate JSON not connected to ontology
  ⇒ refactor for Phase-2; cables = device-properties, not device-relations; datasheets =
  chunked-and-chatted, not extracted; document occurrences live inside device-detail) and
  the final demo flow (dataset view in Neuralith → action view with device list + tree
  view → device detail with embedded document/datasheet/PLC panels → graph view triggered
  *from* a device, layered hydraulic/electrical/hierarchy, not the hero → chat as overlay).
- **Architecture-vs-feasibility translation** — Ivo flagged he felt disconnected because
  Neuralith is a real platform with a playground; Alex's PoC is a streamlit backend that
  Yevhenii will re-skin. Claude translated: it's **two apps stitched by a hyperlink**, not
  one integrated app — that's Vankata's actual instruction (*"we can link to another very
  similar-looking interface"*). For demo only — Phase-2 work is the real integration.
- **МuK acronym lookup** — the migrated files only carry "Mookelist" phonetically; not
  spelled out anywhere. Filename `Terminal equipment` hints at "Material- und Komponenten…"
  or "Mess- und Kontrolltechnik". Inference, not confirmed — ask Thorsten if it matters.
- **Translation help** — drafted the Bulgarian phrasing for Ivo's clarifying question to
  Vankata about the two-app architecture.

What got committed to the repos:

- `engagements/sms-group/4_poc/presentation/` — new folder. First draft (`draft.md`) of
  the presentation outline was created at Ivo's request, then **deleted** when Ivo
  learned Vankata had already started writing the story doc in Drive
  (`sms-group-presentation-story-v2-2026-05-13.docx`, owned by Vankata, shared with Ivo).
  Replaced with `jordan-alignment-receipts.md` — a different cut for Jordan's specific
  ask (three slide structures: "what you said you needed" / "what we delivered" / "how
  what we delivered aligns to your explicit needs"). This is the receipts/proof-artifact
  complement to Vankata's narrative-arc story. Awaiting Jordan's confirmation on table-vs-
  prose framing before slide-ifying.
- `engagements/_presentation-templates.md` — new top-level reference. Lists the 3 IRIS-
  standard client-facing decks: AWS Better Together Enablement Master (Liana, latest
  edit 2026-05-12), Iris.ai Company Overview April 2026 (Jordan, Axion-focused — the
  strongest single source for SMS-style problem framing: retiring-experts quote,
  ArcelorMittal-7yr-on-prem, 330M+ docs / 94% precision / 68 langs, Kozloduy
  nuclear-schematics quote), AWS Better Together Master Introduction (Jordan's copy).
  Plus Steven's 92-slide `Company Introduction_Master Deck` for case-study slides
  (Finnish Food Authority RSpace, ArcelorMittal Axion).

Memory updates (`~/.claude/projects/-Users-iris-Documents-atlas/memory/`):

- New: `presentation-templates.md` (reference) — indexed in MEMORY.md.
- New (added by Ivo, not Claude): `outward-facing-actions.md` — approval rule: never
  auto-create calendar events or send emails. Draft in chat → Ivo approves → then create.
  Internal repo edits are fine without asking.

Where things stand at session close:

- **Vankata is owning the story doc**; Claude is not duplicating that work.
- **Jordan-alignment-receipts.md awaits Jordan's review** before being turned into slides.
- **Ivo is on the Neuralith dataset** (ingest SMS docs as a Neuralith dataset, chunk
  manufacturer datasheets + functional descriptions, verify in playground, set up the
  dataset→action click-through for the demo).
- **Zhenya is re-skinning Alex's PoC frontend** to look like Neuralith chrome on Alex's
  branch (link to be dropped in `axion-deliveries`).
- **Demo date is Wed 20 May** (resolved in-call from the 19th-vs-June-2 binary).
- **Presentation preview to Thorsten is due EOD today / tomorrow** so he can soft-check
  with Gerald before the live session.

Open / next session:

- Confirm with Jordan whether the alignment-receipts table format is what he wanted, or
  whether he wanted prose extracted from Vankata's story.
- Once Neuralith dataset is ingested, draft the screenshots-and-video email to Thorsten.
- Wed 20 May (the actual Gerald presentation) is the next big checkpoint.

## How to resume in a new Claude Code session

Open it in `~/Documents/atlas/`. Read `STATE.md`, then `ENGAGEMENT_PLAN.md`, then (if you want the
full narrative) this file. That's the whole picture — nothing critical lives only in the chat.

---

# Session log — Thu 14 May to Mon 18 May 2026

Five-day session covering DB demo prep + delivery, TandF bundle, Postbank handover, Asana
bootstrap, and the Monday commercial-call brief. This picks up from the 2026-05-12 session
above.

## What was delivered

### Deutsche Bahn InfraGO
Friday 2026-05-15 scoping demo with Hannah Richta landed strongly: *"really impressed"*,
*"excellent material to convince people"*. Showcase HTML built (84 MB, DB Verkehrsrot palette,
641 page images inline, Welocalize-style Doc Explorer, Agrolimen-style Database Browser,
English UI / German values). Groundedness audit: 96.6% value-in-source, 0 confirmed
hallucinations, 100% on local rules. Sat 2026-05-16 deployed showcase to S3
(`https://iris-db-scoping-showcase.s3.eu-central-1.amazonaws.com/showcase.html`, access code
`DBInfraGO-Axion-2026`). Email sent to Hannah with 5 open ontology questions + 7 take-aways.
Mid-June follow-up call booked: Mon 15 Jun 10:30 BG. See `db-infrago-deal` memory.

### TandF
Scoping bundle (viewer + 4 JSONs + sources/pdf + sources/xml + slim README) trimmed to ~281 MB,
placed in shared Drive `Iris.ai - Everyone/Commercial/POC/Scoping Exercises/TandF/Deliverable/`.
Email sent to Paolo 2026-05-15. Paolo had Drive-access friction (corporate email blocked);
folder set to "anyone with the link". Ivana sent MNDA directly 2026-05-15 12:29 UTC, cc Ivan
Georgiev (CTO/signatory), Jordan, Ivo. NDA action item closed. Jordan owes formal proposal
Tue 19 May. Paolo's next call ~9 June.

### Postbank
Svetla Yankova departed Postbank week of 12 May; handed conversation to Lina Varbanova on the
existing Gmail thread. Welcome reply sent 2026-05-14 (Tue 19 May 11:30 BG confirmed). Pre-read
pack drafted in chat (Mon 18 May EOD send). Lena (Svetla's boss = VP Marketing & Sales Ops)
vs Lina Varbanova (new primary) are DIFFERENT people — don't confuse.

### Agrolimen — CLOSED-LOST
Patricia emailed Jordan 2026-05-15 10:17 UTC: going internal with team already running other AI
initiatives. Lost ~€40K immediate + ~€50K next quarter + larger upside. Marco Sterbizzi's AI
team likely the build owner; flagged as 3-6 month re-engagement target. See
`agrolimen-closed-lost` memory.

### Asana Commercial Engagements tracker — NEW
Created `Iris.ai Commercial Engagements` project (GID `1214855342290138`). Asana MCP installed
and OAuth-authenticated 2026-05-18. Bootstrapped 13 sections + 12 `[PIPELINE]` summary tasks +
~28 next-action tasks + 64 phase-lifecycle tasks (retrospective + forward, modelled on the
spreadsheet PoC Pipeline Tracker `1xvD7XiPnutXvJhgELokkwuXrRZYf8r88akby8XEy_jY`). Emoji status
scheme: ✅ ⏳ 📅 ❌. Aumovio split into Parts (live) + Software Impact (DISCONTINUED W17, in
Archive). NHS dormant; Agrolimen closed-lost; both in Archive. Iris.ai Product Roadmap
(Vankata's) NOT touched. See `asana-commercial-tracker` memory.

### Monday 18 May commercial-call brief
At `briefs/2026-05-18_commercial_call.md`. TL;DR + per-engagement state + pipeline-value
summary + 7 verbal flags + HubSpot/Asana sync action lists + open questions. Per Viktor's
directive 2026-05-15: state lives in Asana + HubSpot, not Excel. See `state-tracking-tools`
memory.

## Pipeline state at end of session

| Engagement | Stage | Headline |
|---|---|---|
| SMS Group | PoC | Wed 20 May Gerald presentation. €950K-€1.3M for 150 machines |
| Aumovio (Parts) | PoC / Validation | Fri 22 May follow-up. Close target 1st week June |
| DB InfraGO | Awaiting eng eval | Mid-June follow-up. Jordan proposal due mid-June |
| Postbank | Scoping | Tue 19 May 11:30 BG — first call with Lina |
| TandF | Proposal | Jordan due Tue 19 May. Next call ~9 June |
| Garrett | Scoping | Tue 19 May 13:30. Liviu's internal answer |
| Heineken | Eval-deliver | PoC presentation Mon 18 May 15:00 BG |
| Welocalize | Cold (Steven) | ~13 days silent. Escalation pending |
| Daikin | Pre-scoping | Maria reschedule by 25 May |
| Finom | Pre-scoping | Decide close-lost at Mon commercial call |
| Basamh | Pre-scoping | Tue 3 June (Stan) |
| Fresenius | Dormant | Confirm next-touch owner |
| Agrolimen | CLOSED-LOST | 2026-05-15 — internal build |
| NHS | Dormant | Confirm closed-status |

## New memory files this session

- `asana-commercial-tracker.md` — the new canonical project + structure + conventions
- `db-infrago-deal.md` — DB demo delivered well; awaiting eng eval mid-June
- `agrolimen-closed-lost.md` — closed-lost 2026-05-15; FMCG extractor reusable; Marco
  re-engagement target

(Previously: `model-selection-protocol.md`, `state-tracking-tools.md`.)

## Outstanding work going into next session

1. Lina pre-read pack — drafted in chat; create Gmail draft for Mon EOD send.
2. Monday commercial call — walk the brief at `briefs/2026-05-18_commercial_call.md`.
3. Heineken PoC presentation Mon 18 May 15:00 BG.
4. Custom fields in Asana UI (10 fields including Stage, SA owner, Commercial owner, Eng lead,
   HubSpot deal ID + URL, Expected close, Amount EUR, Probability %, Industry).
5. Workspace invites in Asana for Jordan, Maria, Stan (their phase tasks are unassigned).
6. Tue 19 May: Postbank Lina call, Garrett Liviu call, TandF proposal deadline (Jordan).
7. Wed 20 May: SMS Group Gerald presentation (Jordan presents, Ivo demoed already).
8. Fri 22 May: Aumovio follow-up.

## Cleanup pending (manual UI, 5 min)

- Delete 3 stale Gmail drafts: `r4113356437335798010`, `r8363508829320785699`, `r781636672409101060`.
- Delete 2 stale Drive folders: `1D3GnMv5KlAPHShelJvrFwLhXphdh8D3U`, `1Yoca5fr5D_5xiFl3iN1ufh9jNg3uVK8D`.

