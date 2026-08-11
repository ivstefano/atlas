# STATE: platform-product

_Working memory for this task. Auto-written on session end/compact. Read on session start.
This is NOT the client-facing STATUS.md._

last_session: 2026-07-31T16:30
last_tab: A: Operations

## Now

Playground onboarding funnel (marketing → website → platform demo). Two calls this week settled the flow: 2026-07-28 Playground Sync (Liana/Vankata/Victor/Michael) agreed the four funnel decisions; 2026-07-31 Platform Next Steps (Vankata/Vasco/Vova, 86 min) briefed Vova, escalated front-end analytics into a platform-wide epic, and hit contested ground on the Projects & Applications epic.

Both transcripts filed to `engagements/_internal/platform-product/meetings/`. STATUS.md written and committed (0ee2d0e). **Repo side is done — nothing to sync.**

## Next action

**Resolve the 6 open questions below.** Top priority: #4 (tell Liana the numbers will undercount) — she has not been told, and if she builds expectations on the first campaign report and later learns the figures were systematically low, that is a credibility problem created by omission.

## Open questions — unresolved, no owner

Drafted 2026-07-31, none sent. Each is one message.

**1. To Vankata/Victor — who builds the magic link?**
> Who owns generating the temporary access token for the playground magic link, and does Victor or someone from the Neuralith backend need to be in that conversation?

Vova asked this verbatim at the end of the 07-31 call ("with whom to generate this temporary link… do we need Victor or someone from the backend side at least?"). Vankata's answer was "maybe we can make a quick story on that… maybe during the Neuralith planning" — not an assignment. Vova is ready to build the front end; token generation is unassigned.

**2. To Liana — confirm the two definitions Ivo set unilaterally.**
> Activation = first step where you see real output (document/artifact/chart opening), not just advancing the tour, otherwise it only measures clicking next. Button clicks = artifacts, document opens, charts, tables, CTAs — not every element on the page, so this doesn't become a heatmap project.

Both are recorded in STATUS as "Ivo set, not yet confirmed by Liana."

**3. To Liana — retract the session-video commitment.**
> Floated it too quickly in the Slack thread. Needs Victor's sign-off as security officer, GDPR questions since these are inbound EU leads. Event analytics committable; video not yet.

**4. To Liana — the undercount nobody has told her about. HIGHEST PRIORITY.**
> Any tracker, including self-hosted, gets partially blocked by browsers and DNS filters. Vova tested this live on the 07-31 call (his own DNS resolver blocked posthog.com). Numbers will undercount by an unknown margin. Fine for comparing campaigns against each other; not fine as absolute conversion figures.

**5. To Vankata/Vasco — who owns the analytics requirements?**
Vasco volunteered to write the front-end analytics epic. Ivo has been negotiating the metric list directly with Liana. Vankata's stated position on the call: **product consumes the data first** and hands marketing a specific content ask; he was explicit that Liana can't diagnose a landing page. These cut against each other. Reconcile before the epic gets written twice.

**6. To Vankata — expiry landing page (raise on its own merits).**
An expired magic link currently dumps the user on a bare sign-in screen with no explanation = lead lost silently. Small fix.
**Do NOT reopen the token decision.** 1-day TTL and the forgot-password second visit were both decided deliberately on 07-31, not by omission. Earlier session drafted a 4-point architecture proposal (7-day token, persist campaign, email-first sign-in, expiry page); the full transcript closed the first two. Only the expiry page and possibly email-first sign-in are still live, and both stand alone.

## Also unverified

- Commit 0ee2d0e ("correct project object hierarchy after Ivo confirmation", 16:15) landed ~10 min after the STATUS entry recording **Vova contesting exactly that model** — that Projects was originally an RSpace collaboration construct, that organization already covers it, that Neuralith barely uses organization context today. If `artefacts/onboarding-flow/projects-hierarchy.md` was corrected from the epic as written, it may assert a model the 07-31 call left open. **Check before treating it as settled.**

## Don't re-explain

- **Terminology (Vankata, fixed 07-28)**: playground = many demos; **one demo = one dataset**; campaign = the marketing push into a demo. One landing page **per demo, not per campaign**.
- **Naming split (Michael raised it)**: *marketing landing page* (HubSpot, the Iris story) vs *onboarding page* (in-product, pre-demo, "what results you'll get"). Intro personalized per demo; **outro/CTA identical across all demos**.
- **Magic link needs no campaign tag.** The signed link points straight at the demo page, so no user tagging and no playground-side routing. The *analytics layer* still needs attribution; where that lives is undecided. These are compatible — don't re-derive them as a conflict.
- **Analytics constraints are settled**: no external SaaS (Vankata, ISO), self-hosted open source acceptable, hashed/anonymized (session hash + abstract user, no email/IP/location), internal AI models only, Victor gates it as security officer.
- **Analytics does not block playground launch** (Vankata). Backend request logs cover the very beginning.
- **Vova** = front-end lead / tech lead, both website and product; first employee, 10 years. Architectural decisions route through him. In Ukraine.
- **Vasco** (Vasil Shivachev) = new, customer success, mature-phase customer relations vs Ivo on experimental/scoping. Boundary with Ivo **not yet discussed with Vankata**.
- Transcripts: pull with `atlas/.claude/scripts/tactiq_pull.py`. **It skips if the file exists** — `rm` first when re-pulling a call that was still processing. The 07-31 transcript was first pulled at 23 min of an 86-min call and the partial version was materially misleading.
