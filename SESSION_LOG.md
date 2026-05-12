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

## How to resume in a new Claude Code session

Open it in `~/Documents/atlas/`. Read `STATE.md`, then `ENGAGEMENT_PLAN.md`, then (if you want the
full narrative) this file. That's the whole picture — nothing critical lives only in the chat.
