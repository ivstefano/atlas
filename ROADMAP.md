# atlas — strategic roadmap + founding thesis

Long-term thinking about what atlas is becoming. Counterpart to `NEXT_PRIORITIES.md` (which is the tactical build queue).

This was the original `README.md` when atlas was still called `_optimize` (early May 2026). It pre-dates a lot of what's been built since then. Some layers are now built, some are still pending. Use this as the **frame**, use `NEXT_PRIORITIES.md` as the **current queue**.

Last updated context: 2026-05-26. Status notes inline mark what's built vs. pending vs. dropped.

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

## 2. The system — four layers

Build in this order. Each layer is useful on its own.

### Layer 1 — Uniform per-engagement context (foundation) — **BUILT ✅**
Every `engagements/<client>/` gets the same five files: `CONTEXT.md`, `STATUS.md`,
`COMMERCIAL.md`, `SOURCES.md`, `ARTEFACTS.md`. These are the inputs every other automation reads.

Status as of 2026-05-26: 9 active engagements all migrated. `_template/` holds the spec. `/new-engagement` slash command scaffolds new ones in <30 sec.

### Layer 2 — MCP connectors (the multiplier) — **MOSTLY BUILT ✅**
Karpathy's "sensors and actuators." Give agents reach into Google Drive, Slack, Google
Calendar (Calendar/Gmail/Drive/Slack/Asana/Canva wired; HubSpot blocked on admin auth).
Drafts only for anything outward-facing; I send. See `_config/mcps.md` for status.

### Layer 3 — AI loops in Claude Code (the leverage) — **PARTIAL ⏳**
Recurring jobs: morning brief, post-meeting digest, weekly cross-engagement rollup,
stale-engagement watchdog, SoW drafter. **Local `/loop` first** (I trigger), then iteratively
work out what to outsource to cloud `/schedule` remote agents.

Status: morning brief works (auto + hand-written variants); post-meeting digest is the next-biggest toil-removal target in `NEXT_PRIORITIES.md`; weekly rollup not built; SoW drafter not built.

### Layer 4 — Mobile-in-the-loop approval (decouple the person from the desk) — **NOT STARTED**
Claude sessions (loops, drafts, agent actions) pause at their decision points and reach me on
my phone: a notification with the context and what's being asked, and I approve / edit / reject
from there. Same for Victor, Vankata, Steven on the tech side. The agent does the surfacing
("this action is high-risk", "this SoW draft is ready for review"); I do the deciding, from
wherever I am.

Status: not built. Becomes necessary when cloud `/schedule` remote agents come online.

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

The atlas-side enforcement of this rule lives in `~/.claude/projects/-Users-iris-Documents-atlas/memory/outward-facing-actions.md`.

---

## 4. Build order (the original sequencing)

This was the original plan. Some steps are done, some are reordered in `NEXT_PRIORITIES.md`.

1. **Layer 1 on Heineken, Aumovio, SMS** ✅ — done. Rolled out to all 9 active engagements.
2. **Wire Calendar + Drive MCPs** ✅ + **daily morning brief** ✅ — done.
3. **Post-meeting digest** loop against transcripts — ⏳ pending. This is `A8` in `NEXT_PRIORITIES.md`, the highest toil-per-build-day item still in the queue.
4. **Slack MCP** ✅ wired + weekly client-update drafts ⏳ pending.
5. **Mobile-in-the-loop approval (Layer 4)** — not started. Becomes urgent when cloud loops come online.
6. **Weekly cross-engagement rollup** — ⏳ this is `A9` in `NEXT_PRIORITIES.md`. Feeds the Monday Steven commercial call + becomes the CFO-brief feeder.
7. **Synthesizer view (wiki/)** — deprioritised. Asana now holds engagement state (Viktor 2026-05-15 directive); Asana Gantt + HubSpot pipeline view cover what a synthesizer would have done.
8. **Migrate stable loops to cloud `/schedule`** — gated on `B3` (EC2 controller box) in `NEXT_PRIORITIES.md`.

---

## 5. What's changed since the original thesis (2026-05-26 reflection)

What this doc didn't anticipate:

- **The product-surface reframe (2026-05-18)**: what started as "deliverable HTML generator" became a small web product for Solutions Architects (`B4` in NEXT_PRIORITIES). The Karpathy thesis still applies, just at one layer up — the *context pack* is now the input to a UI that other SAs (Matyo, Petar) will also use.
- **Pyloth**: a deployment-side companion to atlas. Atlas runs locally on Ivo's box; Pyloth handles the cloud-side / EC2 / S3 self-serve. Originally everything was "atlas does it all"; now there's a clean local/cloud split.
- **Internal threads also need the 5-file structure**: Liana demos, Neuralith design system, culture-site, SA-position artefacts — these are stakeholder threads too, not just client engagements. `engagements/_internal/` will be a sibling carve-out.
- **The leverage question**: this doc treated atlas as a tool. Living with it for 2 weeks shows it's actually Ivo's *command center* and personal leverage — what makes him faster than peers. That changes where it should be hosted (private GitHub on `ivstefano`, not Iris-org) and what stays private vs. what becomes published patterns.
- **Memory as the durable layer**: the original plan focused on per-engagement context files. Real leverage came from the cross-engagement *memory index* (38 entries as of 2026-05-26). Memory is what makes pre-call reconstruction cheap.

---

## 6. Files that were promised by this doc but never built (status as of 2026-05-26)

- `LAYER1_CONTEXT_TEMPLATE.md` — never made it as a single doc. The convention is encoded in `engagements/_template/` instead.
- `MCP_SETUP.md` — superseded by `_config/mcps.md`.
- `LOOPS.md` — partially in `_config/` (skills-and-commands.md), but the loops themselves are documented inside their `.claude/commands/*.md` files.
- `MOBILE_APPROVAL.md` — Layer 4 not started; no spec exists yet.
- `OPEN_QUESTIONS.md` — questions get logged inside individual briefs and NEXT_PRIORITIES instead.

Don't recreate these as separate docs unless the current pattern stops working.

---

## 7. How to read this doc going forward

- **First-time landing on atlas as a fresh Claude / new SA / future-Ivo**: read this for the *why*.
- **Working on what to build next**: read `NEXT_PRIORITIES.md`. This doc is the *frame*; that one is the *queue*.
- **Quarterly review (every ~3 months)**: revisit this. Has the thesis changed? Is Layer 4 still worth building? Has the product-surface reframe (B4) absorbed Layer 3?
