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
3. **`engagements/` repo created** (`~/Documents/engagements/`, git-initialised): `_template/` (the four core files + `1_pre-scoping/`), `/new-engagement <company>` command in `.claude/commands/`, `README.md`, `.gitignore` (keeps client data + credentials out: `*.pdf *.zip *.xlsx *.docx *.pptx`, `**/data/* **/raw/ **/processed/ **/results/`, `*credentials* *token* .env *.pem`, `.DS_Store`).
   - **Decided structure:** `engagements/<company>/` with `CONTEXT.md` + `STATUS.md` + `SOURCES.md` + `COMMERCIAL.md` at the top; numbered stage folders `1_pre-scoping / 2_scoping / 3_contracting / 4_poc / 5_implementation`, created lazily; `_legacy/` for old flat files; `_briefs/` for auto-briefs (committed); `_pending/` for trigger-staged new engagements awaiting Ivo's promotion.
4. **`atlas/` moved** out of `Axion/_optimize/` to `~/Documents/atlas/` and made its own git repo. Breadcrumb left at `Axion/_optimize/MOVED.md`.
5. **A3 — Heineken migrated** (`engagements/` commit `6c6c1f0`). `Axion/scoping/heineken/` (flat folder, ~20 transcripts + workbooks + an abandoned `_rag/` exploration) folded into `engagements/heineken/`: clean `CONTEXT/STATUS/SOURCES/COMMERCIAL` written from the transcripts + `BRIEFING.md` + the authored datastore-context doc; old `.md` files → `_legacy/`; transcripts split into `1_pre-scoping/transcripts/` (Feb–Mar use-case deep dives) and `4_poc/transcripts/`; the authored datastore-context (`human-in-the-loop/`) → `4_poc/datastore-context/`; the signed contract PDF → `3_contracting/contracts/`; the `_rag/` *code* → `_legacy/_rag-exploration/`. **Decisions made on the spot** (Ivo declined the upfront question, take as defaults): COPIED not moved (Axion source untouched, reversible — cleanup later); big binaries (workbooks, `heineken-rag-full-extract.zip`, `_rag/chroma_db`, `_rag/extracted/` ~175 files) **left in Axion**, `SOURCES.md` references the `AXION:` paths + future S3; no separate `2_scoping/` stage (went straight from deep dives → contracting → PoC); `5_implementation/` kept as a placeholder (Phase-2 actively being scoped). The `.gitignore` excludes the contract PDF + alignment/glossary `.docx` + `Heineken S3 answers.xlsx` — they sit in the working tree, referenced by path, *not committed* (consistent with "binaries don't go in git"; revisit if Ivo wants the contract tracked). Heineken facts now in `CONTEXT.md`: RAG-type Excel→DB+SQL-agent PoC over the D&T Cost&Value financial files; business owner **Justyna Roczek** (= Justyna Bień, married — both names appear in transcripts); manager/decision-maker **Lucy Todorovska**; procurement SME **Monika Samolej**; ~160 IT services across 4-5 workbooks; L-code is the universal join key; MAIN "In progress" sheet (rows 3-166) is source of truth; 6 scenarios built easiest-first S3→S1→S5→S4→S6→S2; human-in-the-loop demo (email draft, send mocked) + the open "continuous learning loop" question with Lucy; 8-week PoC from the Mar 23 contract HNK282127, ~ending mid/late May; post-PoC commercial+technical meeting + Phase-2 proposal pending.

## What's next

**Ivo reviews the Heineken folder** and answers the acceptance question: **"could a tech person (Alex) start the Heineken PoC from these four files cold, without asking me anything?"** If yes → roll the same fold-down out to the other active engagements (SMS, Aumovio, Agrolimen, T&F) + start Track B in parallel. If no → fix the `_template/` files before touching anything else, then re-migrate Heineken.

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
