# _optimize — making solutions-architect work scale across many parallel engagements

This folder holds the plan (and, later, the working notes) for optimizing how I run
multiple scoping exercises and PoCs at once: notes, transcripts, Excel sheets, SoWs,
Slack threads with the tech team, Drive uploads, and calendar-driven engagements.

Status: **planning**. Nothing here is built yet. Build order and decisions are below.

---

## 1. The thesis (the Karpathy lens, applied to this job)

From Karpathy's AI Native talk, the parts that are load-bearing for *this* role (not a coder's):

1. **I am the bottleneck, and the bottleneck is *understanding*, not typing.**
   "You can outsource your thinking but you can't outsource your understanding." The job
   is already mostly information-processing (digest a transcript, reconcile it with an
   Excel sheet, decide what the PoC does, write the SoW, brief the engineer). All of that
   is automatable *except* keeping the live state of ~30 engagements in my head so I can
   direct them.

2. **The valuable new artifact is the *context pack I hand to an agent*, not an app.**
   Karpathy's openclaw point: install instructions stopped being a shell script and became
   "text you paste to your agent." My equivalent: a per-engagement context file good enough
   that an agent can draft the next SoW / meeting prep / Slack update *correctly* without me
   re-explaining. Already half-done (`scoping/aumovio/CLAUDE.md`, various `STATUS`/`TIMELINE`
   files, the auto-memory `MEMORY.md`). The leverage is making it **systematic and uniform**
   across all engagement folders.

3. **"LLM knowledge bases" — recompiling my own scattered docs into new projections — is
   the highest-ROI new capability.** Transcripts (`tactiq_export/`, `scoping/*/notes/`),
   Excels, PDFs, SoWs, Slack logs, calendar events: today they're 30 piles of sediment.
   The thing that couldn't exist before is a synthesizer that re-projects all of it on
   demand: "what changed across all engagements this week?", "which PoCs are blocked and
   on whom?", "draft the Heineken weekly update from the last 3 meeting notes + Slack."

4. **Verifiability says where to trust the loop vs. stay hands-on.** SoW numbers, dates,
   deliverable counts, owners: verifiable against source docs, so agents draft and I check.
   Strategic judgment (is this PoC worth doing? what's the commercial gate? how hard do I
   push a stakeholder?): not verifiable, stays with me.

5. **Jaggedness: human in the loop on the *spec*, not the *fill-in*.** An agent will
   confidently merge two engagements' facts the way Karpathy's agent matched a Stripe email
   to a Google email. I own the spec/plan/structure; agents fill blanks; I review the
   top-level categories.

6. **Human attention is the scarce resource — the approval has to come to me, not me to a desk.**
   Cherny's framing: "the doing of things is now easy; *is this a good thing, is this what I
   wanted* is the single most important bottleneck." Two consequences. (a) The right shape of
   the human gate is not "click approve, approve, approve" (humans default-approve, badly) but
   the agent surfacing *which* actions are high-risk / need escalation / are safe to auto-run,
   and me deciding only the ones that matter. (b) That decision has to be reachable from a
   phone. If approving a Claude session means being at a laptop, the bottleneck is the laptop,
   not me. Mobile approval decouples the person from the computer while moving — which is the
   normal state for Victor, Vankata, Steven, and me. This is **Layer 4** below.

7. **Now is a one-time context investment.** Cherny: "you have all these meetings, you didn't
   include the AI; that's not nice to the AI." The models will keep improving on their own; the
   thing that doesn't happen automatically is making sure the AI *has the information in theory
   to solve the problem*. That's exactly what Layer 1 (uniform per-engagement context) and
   Layer 2 (MCP reach into Drive/Slack/Calendar) are. Do this once, well, now.

---

## 2. The system — three layers

Build in this order. Each layer is useful on its own.

### Layer 1 — Uniform per-engagement context (foundation)
Every `scoping/<client>/` gets the same three regenerated files: `CONTEXT.md`, `STATUS.md`,
`SOURCES.md`. These are the inputs every other automation reads. Spec: **`LAYER1_CONTEXT_TEMPLATE.md`**.

> Note: this is *engagement-tracking* context, distinct from the RAG-grounding knowledge-base
> CONTEXT.md that already exists at `scoping/heineken/human-in-the-loop/CONTEXT.md`. Different
> purpose, different file. Don't conflate. Naming to be settled in OPEN_QUESTIONS.

### Layer 2 — MCP connectors (the multiplier)
Karpathy's "sensors and actuators." Give agents reach into Google Drive, Slack, Google
Calendar (Calendar/Gmail already available in this environment; Slack and richer Drive are
the adds). Drafts only for anything outward-facing; I send. Spec: **`MCP_SETUP.md`**.

### Layer 3 — AI loops in Claude Code (the leverage)
Recurring jobs: morning brief, post-meeting digest, weekly cross-engagement rollup,
stale-engagement watchdog, SoW drafter. **Local `/loop` first** (I trigger), then iteratively
work out what to outsource to cloud `/schedule` remote agents. Spec: **`LOOPS.md`**.

### Layer 4 — Mobile-in-the-loop approval (decouple the person from the desk)
Claude sessions (loops, drafts, agent actions) pause at their decision points and reach me on
my phone: a notification with the context and what's being asked, and I approve / edit / reject
from there. Same for Victor, Vankata, Steven on the tech side. The agent does the surfacing
("this action is high-risk", "this SoW draft is ready for review"); I do the deciding, from
wherever I am. Spec: **`MOBILE_APPROVAL.md`**.

---

## 3. What stays mine (do not automate, not even as a draft without me)

- Whether a PoC is commercially worth doing, and the real value driver.
- How hard to push a stakeholder; reading the room on a call.
- The **send** of anything outward-facing — Slack to colleagues, email to clients, Drive overwrites.
- **SoWs, NDAs, and other contract-grade documents**: generated and reviewed *with me in the
  loop*. Agents may prepare a draft, but it does not leave, and is not treated as final, without
  my review. (Per decision, nothing is forbidden from being drafted; these just carry a mandatory
  human gate.)

Safety net for the draftable stuff: a second agent ("council of LLM judges") sanity-checks a
generated SoW or client update against the source docs before it reaches me — cheap, catches
the email-merge-style hallucinations.

The mechanics of the gate (Cherny): not "approve / approve / approve" (humans default-approve).
The agent classifies each action — auto-run / notify-me / needs-my-approval / needs-escalation
— and only the last two reach me, ideally on my phone (Layer 4).

---

## 4. Build order (sequencing)

1. **Layer 1 on Heineken, Aumovio, SMS** (confirmed prototype set). Prove the
   `CONTEXT.md` / `STATUS.md` / `SOURCES.md` template earns its keep — mostly reorganizing
   what already exists — then roll out to all engagement folders.
2. **Wire Calendar + Drive MCPs** (already available, just auth) → build the **daily morning
   brief** as a local `/loop`. Smallest thing that changes the daily routine.
3. **Post-meeting digest** loop against `tactiq_export/` (and `scoping/*/notes/`).
4. **Slack MCP** → weekly client-update drafts + colleague-reply drafts.
5. **Mobile-in-the-loop approval** (Layer 4) — once there are loops/drafts worth approving,
   wire the notification + approve-from-phone path. Pull it earlier if the morning brief or
   digest already needs it. Rolls out to Victor / Vankata / Steven too.
6. **Weekly cross-engagement rollup** feeding the Monday product sync (see auto-memory
   `product_sync_meeting.md`).
7. Once all the above is load-bearing: consider a small **synthesizer view** (a `wiki/` that
   recompiles all engagements — Karpathy's LLM-knowledge-base move) if I'm still manually
   answering "what's the state of everything."
8. **Iteratively migrate** the loops that prove stable + valuable from local `/loop` to cloud
   `/schedule` remote agents. (Cloud loops make Layer 4 mandatory, not optional — a remote
   agent with no phone gate is just unsupervised.)

---

## 5. Files in this folder

- `README.md` — this file: thesis, system overview, build order.
- `LAYER1_CONTEXT_TEMPLATE.md` — the per-engagement `CONTEXT.md` / `STATUS.md` / `SOURCES.md` spec.
- `MCP_SETUP.md` — which MCPs, what each unlocks, auth notes, the draft-not-send rule.
- `LOOPS.md` — the recurring jobs, `/loop` vs `/schedule`, triggers, inputs/outputs.
- `MOBILE_APPROVAL.md` — Layer 4: approve/edit/reject Claude sessions from a phone; action
  classification; rollout to the tech-side folks.
- `OPEN_QUESTIONS.md` — decisions still pending, and decisions already made (logged).
