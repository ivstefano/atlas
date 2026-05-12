# atlas — current state (read this first)

This is the ops layer for Ivo's solutions-architect work: the plan, the agent map, the loop
specs, and (eventually) the tooling. It is **not** a behavioral clone of Ivo — it does the
mechanical parts so the judgment stays with him.

Two sibling repos under `~/Documents/`:
- **`atlas/`** (this one) — the plans/specs/tooling. Read order: this file → `ENGAGEMENT_PLAN.md` → `README.md`.
- **`engagements/`** — one folder per client engagement, same shape every time. See its `README.md`.
- (`Axion/` still exists — the old junk drawer: `*-usecase/` reference dirs, `tactiq_export/`, playground demos, loose files. A separate cleanup, not blocking anything. `tactiq_export/export.py` is still where the live-transcript fetch reaches.)

## What's been done (as of 2026-05-12)

1. **The agent map** — `AGENT_MAP.html` (v1) and `AGENT_MAP_V2.html` (cleaner redesign: trimmed cards, 3-col grid, impact/effort badges, footnotes section). Built live during Strategy Day Part 2 from the Tactiq transcript. Source transcript: `Strategy Day - Part 2 - AI Driven Development Knowledge Sharing.txt`. **Do not produce PNG/PDF exports** (Ivo's instruction); HTML only.
2. **`ENGAGEMENT_PLAN.md`** — the canonical plan for the engagement-context system. §0 has the decisions; §6 has the two-track build order (A = context system, B = tooling/infra); §7 has the 6 still-open questions; §8 has the AWS/sync architecture.
3. **`engagements/` repo created** (`~/Documents/engagements/`, git-initialised, one commit `fb5ba2a`): `_template/` (the four core files + `1_pre-scoping/`), `/new-engagement <company>` command in `.claude/commands/`, `README.md`, `.gitignore` (keeps client data + credentials out).
   - **Decided structure:** `engagements/<company>/` with `CONTEXT.md` + `STATUS.md` + `SOURCES.md` + `COMMERCIAL.md` at the top; numbered stage folders `1_pre-scoping / 2_scoping / 3_contracting / 4_poc / 5_implementation`, created lazily; `_legacy/` for old flat files; `_briefs/` for auto-briefs (committed); `_pending/` for trigger-staged new engagements awaiting Ivo's promotion.
4. **`atlas/` moved** out of `Axion/_optimize/` to `~/Documents/atlas/` and made its own git repo. Breadcrumb left at `Axion/_optimize/MOVED.md`.

## What's next

**Step A3 — migrate Heineken as the proof.** Move everything from `Axion/scoping/heineken/` into `engagements/heineken/_legacy/`, build clean `CONTEXT / STATUS / SOURCES / COMMERCIAL` at the top + the stage folders for stages it's actually reached (it's a mature RAG-type PoC, wrapping up). Then Ivo reviews and answers the one acceptance question: **"could Alex start the Heineken PoC from these four files cold, without asking me anything?"** If yes → roll out to the other active engagements (SMS, Aumovio, Agrolimen, T&F) + start Track B in parallel. If no → fix the template before touching anything else.

Then, roughly: A4 rollout ‖ B1 (S3 prefix standardisation) ‖ B2 (reusable scoping harness, the biggest hours-saver after the context system). Then A5 (wire Calendar MCP → meeting-prep loop), B3 (EC2 worker), B6 (PoC status dashboard, falls out cheaply once the folders exist). See `ENGAGEMENT_PLAN.md` §6 for the full interleave.

## Still open / things Ivo needs to find out

- Who has **HubSpot admin** (to authorize a read-only HubSpot MCP). Until then the Calendar-only path runs.
- How Jordan **names calendar events** — confirmed inconsistent (company / contact-person / both, no fixed format); the matching has to be defensive. Investigate once the Calendar MCP is wired.
- **EC2 box specifics** — Chandra is GPU-ish, so `t3.small` is likely not enough (`g4dn`, or call a hosted OCR endpoint à la AlexFert's PaddleOCR); region; auth via instance profile + SSM Parameter Store.
- **S3 bucket** — confirm with Ross what he provisioned and whether it's the same bucket the Neuralith upload link writes to.
- **Google Drive** — keep as a one-way git→Drive projection for the tech team, or retire it. Decide once repo-as-source-of-truth is settled.
- **`Axion/` cleanup** — separate exercise; sort `*-usecase/` (reference), `tactiq_export/` (tooling — and move the hardcoded tokens to a secrets store), playground demos, loose files. Not blocking.

## Memory note

This work also has an auto-memory entry under `~/.claude/projects/-Users-iris-Documents-Axion/memory/`
pointing here. A fresh Claude Code session started in `~/Documents/atlas/` or `~/Documents/engagements/`
gets a *different* (empty) auto-memory folder — so the durable memory is **this file + `ENGAGEMENT_PLAN.md`**.
First thing a new session should do here: read `STATE.md` then `ENGAGEMENT_PLAN.md`.
