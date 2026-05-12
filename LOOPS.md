# Layer 3 — AI loops

Recurring jobs that do the information-processing so I can stay on direction and judgment.

**Policy: local `/loop` first** (I trigger / it self-paces in this session), then iteratively
work out which loops are stable and valuable enough to outsource to cloud `/schedule` remote
agents. Nothing goes to cloud `/schedule` until it's proven locally.

All loops read Layer 1 files (`CONTEXT.md` / `STATUS.md` / `SOURCES.md`) and, once wired,
Layer 2 MCPs. All outward-facing output is a **draft**; I send. SoW/NDA-grade output always
goes through my review (see README §3).

Every loop's actions are tagged for the Layer 4 gate (`MOBILE_APPROVAL.md`): **auto-run** /
**notify-me** / **needs-my-approval** / **needs-escalation**. The tag column appears per loop
below. "needs-my-approval" and higher reach my phone and never proceed on a timeout.

---

## 1. Daily morning brief
- **What**: reads Calendar for today's meetings, pulls each meeting's `CONTEXT.md` + recent
  `STATUS.md`, and (once wired) recent Slack in that engagement's channel. Outputs:
  "Today: N calls. <Client> 10:00 — last action was X, blocked on Y (owner Z). <Client> 14:00
  — <demo>, engineer status: …".
- **Why**: replaces reconstructing context per meeting.
- **Mechanism**: local `/loop` triggered each morning (or `/schedule` later). Inputs: Calendar
  MCP, Layer 1 files. Output: a brief printed to me (later: a `_optimize/briefs/YYYY-MM-DD.md`).
- **Layer 4 tag**: read-only generation = **auto-run**; the "brief is ready" ping = **notify-me**.
- **Build**: step 2 in the sequence (right after Calendar + Drive MCP auth).

## 2. Post-meeting digest
- **What**: new transcript appears in `tactiq_export/` or `scoping/*/notes/` → summarize into
  the right engagement's `STATUS.md` (newest on top), extract action items + owners + dates,
  draft the follow-up email and the Slack update. I review and send.
- **Why**: turns raw transcripts into live state automatically; transcripts stop being sediment.
- **Mechanism**: local `/loop` watching the transcript dirs, or manual trigger after a call.
  Inputs: transcript, `CONTEXT.md`. Output: `STATUS.md` update (commit-worthy) + draft email +
  draft Slack message (for my review).
- **Layer 4 tag**: `STATUS.md` update = **auto-run** (it's internal); "digest written" = **notify-me**;
  the email send and the Slack post = **needs-my-approval** (phone).
- **Build**: step 3.

## 3. Weekly cross-engagement rollup
- **What**: across all `scoping/*` folders — what moved this week, what's blocked and on whom,
  what needs a decision from me, which SoWs are pending review/signature. The report I'd walk
  into the Monday product sync with.
- **Why**: Karpathy's "knowledge base" projection — a new view over data that didn't exist before.
- **Mechanism**: `/schedule` weekly (Friday) once stable; starts as a local `/loop` I run Friday.
  Inputs: all `STATUS.md` files, Slack, Calendar, auto-memory `product_sync_meeting.md`.
  Output: `_optimize/rollups/YYYY-WW.md`.
- **Layer 4 tag**: generation = **auto-run**; "rollup ready" = **notify-me**.
- **Build**: step 6.

## 4. Stale-engagement watchdog
- **What**: any `scoping/*` folder whose `STATUS.md` hasn't changed in N days while the
  engagement is "active" (per `CONTEXT.md` phase) → flag it. Cross-check: meeting on the
  calendar but `STATUS.md` untouched.
- **Why**: engagements die from neglect, not rejection.
- **Mechanism**: weekly `/loop` (later `/schedule`). Inputs: `STATUS.md` mtimes + `CONTEXT.md`
  phase + Calendar. Output: a short flag list appended to the weekly rollup.
- **Layer 4 tag**: **notify-me** (it's a flag list, no action taken).
- **Build**: alongside step 6.

## 5. SoW drafter (on demand, not a loop)
- **What**: "draft the <Client> PoC SoW" → agent reads `CONTEXT.md`, the closest prior SoW
  (Agrolimen templated on SMS, SMS on Aumovio — that lineage), and the standard legal language
  → produces a first draft.
- **Why**: the scaffolding (structure, numbers, dates, scope tables) is verifiable; I do the
  judgment parts.
- **Mechanism**: a slash-command-like prompt I run when needed. **Mandatory human-in-the-loop**:
  the draft does not leave and is not final without my review. A second "judge" agent checks the
  draft against the source docs before it reaches me.
- **Layer 4 tag**: **needs-escalation / contract-grade** — phone notification, high-priority,
  never auto-proceeds. (NDAs same.)
- **Build**: any time after Layer 1 exists for that engagement; not gated on the loops.

---

## Migration to cloud `/schedule`

A loop graduates from local `/loop` to cloud `/schedule` remote agent when:
- it's run reliably locally for a couple of weeks,
- its output is genuinely useful (I act on it, not skim and discard),
- it doesn't need an interactive decision mid-run (or that decision can be deferred to a draft).

First candidates to graduate: the **daily morning brief** and the **weekly rollup** (read-mostly,
predictable, no mid-run decisions). The post-meeting digest stays local longer (it touches Slack
drafts and `STATUS.md` commits).

---

## Build order recap (from README §4)

1. Layer 1 on Heineken / Aumovio / SMS → roll out.
2. Calendar + Drive MCP auth → **morning brief** loop (local).
3. **Post-meeting digest** loop (local) against transcript dirs.
4. Slack MCP → client-update + colleague-reply drafts.
5. **Mobile-in-the-loop approval** (Layer 4) — wire the phone notification + approve path
   (`MOBILE_APPROVAL.md`). Pull earlier if morning brief / digest already needs it.
6. **Weekly rollup** + **stale-engagement watchdog** (local → then `/schedule`).
7. Optional `wiki/` synthesizer view if still manually answering "state of everything."
8. Graduate stable loops to cloud `/schedule` (Layer 4 becomes mandatory at this point).
