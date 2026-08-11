# Iris.ai Product Team board — task seed
2026-08-03. Window: 27 Jul – 3 Aug. Source: `engagements/_internal/platform-product`.

Granularity matches the board: `Workstream: deliverable`, one owner. Small action items live in task comments, not as tasks.

**Already on the board — don't duplicate:**
- Platform analytics and user-session tracking (Vasco, ready)
- Data Set Outputs (ODL): Table presentation (Michael, backlog)
- Customer Onboarding: Scoping exercise file upload and questionnaire (Michael, backlog)
- Data Set Outputs (ODL): Produce real data table for Process Manufacturing (Ivo, ready → move to in-progress)
- Customer Onboarding: File Upload and questionnaire specification (Ivo, completed)

---

## ROADMAP

**Projects & Applications: epic alignment** — Vankata
The 29 Jul epic isn't aligned, which blocks handoff to Neuralith for technical requirements. Needs the phase-1 short list (projects with datasets, one application per project), the application data-model spec, and a session with the backend team plus Victor. Vova is contesting whether Projects is the right abstraction at all — he owes an abstraction diagram (users → orgs → projects → applications) and that's what's blocking him. Shtiliyan asked twice for concrete requirements and wasn't convinced by the end of the 29 Jul session.
*Comments: where applications get hosted (outside the Neuralith deployment?); SMS Group auth boundaries unverified; workflows have no exposed API; nobody has reviewed how projects work in the backend today.*

**Platform analytics: technical design and tooling** — Vova
Sub-deliverable of the existing analytics task, but it's the engineers' call and distinct from Vasco's product epic. Self-hosted only, no external SaaS (ISO). PostHog vs a simple internal event system. Requirement is session-level end-to-end journeys structured for AI analysis, with events carrying element state, not just identity. Needs Victor's security/GDPR sign-off: hashed and anonymized, internal models only.

---

## DESIGN

**Customer Onboarding: upload and Pass 2 wireframes** — Michael
85-90% done, interaction tested, digitalisation and tweaks left. Two corrections needed before delivery: file cap is ~50 files / ~20MB each / **≤1GB per customer** (Michael said "2 gigs" on the 3 Aug call), and file editing is **add yes, delete no, submit is the commit point** (his last word was still "add and delete" after Yevhenii ruled delete out). Both went uncorrected on the call and are going into wireframes this week.

**Customer Onboarding: in-product onboarding page** — Michael
Pre-demo page, "what results you'll get + steps to get them". Prioritised above results/outputs work. Intro personalized per demo, outro/CTA identical across all demos. Liana's dark wireframe doesn't match playground styling, hence Michael rather than reuse.

**Playground: magic-link re-entry experience** — Michael
An expired link currently drops the user on a bare sign-in with no explanation, so the lead is lost silently. Two drivers now: that, plus partial-state persistence (Pass 1 answers and uploads must survive a session, which is useless if re-entry fails). Needs Vankata's go-ahead on the expiry page; the 1-day TTL itself was decided deliberately and isn't being reopened.

---

## PRODUCT OPERATIONS

**Playground: launch readiness** — Ivo
Vankata's stated immediate priority: demo landing pages + magic-link logic. Covers giving the commercial team access so they stop re-reporting known bugs, choosing the demo dataset (Aumovio vs ArcelorMittal — the latter is harder to make impressive at a glance), and supplying the real figures for the `[N]` placeholders in Liana's landing copy. Analytics explicitly does not block launch.

**Playground: analytics scope agreement with marketing** — Ivo
Six metrics agreed with Liana in Slack on 31 Jul. Three things still owed to her, none sent: the numbers will undercount by an unknown margin (every tracker is partially blocked; Vova demonstrated it live), the session-video commitment needs retracting (GDPR, needs Victor's sign-off), and two definitions were set unilaterally and need confirming — activation means real output rendered, not advancing the tour; element clicks means a defined set, not every element. Also unresolved: Vankata's position is that product consumes this data first and hands marketing a specific ask, which cuts against Ivo negotiating requirements directly with Liana.

**Customer Onboarding: flow specification, v2** — Ivo
The consolidated spec exists; Vankata wants it circulated rather than discussed further. Additions since: partial-state persistence and the re-onboarding email (new on 3 Aug, in neither document), plus more context around the line naming Michael and the animation, which reads cold as if Dezea underdelivered when the requirement was absent from the source spec.

**Playground: content and walkthrough handoff to marketing** — Ivo
Owed to Liana since 28 Jul, into her Playground content improvements doc, for the funnel visual the commercial team works from: the post-registration user-action list and the ~10 walkthrough steps with their text. Vankata also needs to confirm whether Liana's landing-page structure still stands, since nobody has seen updates from her.

**Product operations: board and status-doc ownership** — Vankata
Vankata committed on 3 Aug to writing up this board, with Michael getting access. Unresolved: how it relates to Ivo's existing `Scoping Demo Automation` section and to the playground status doc Vankata asked Ivo to maintain on 29 Jul, where ownership was never confirmed. Three boards is the risk. Rotating meeting lead also proposed so it isn't always Vankata or Vasco.

---

## BACKLOG

**Neuralith: generic conversation backend** — unassigned
Current chat backend judged too custom on 29 Jul. Needed for anything chat-like.

**Onboarding: registration edge cases** — unassigned
Meta lead-form → backend webhook feasibility (Vankata assumes it exists, never verified) and the duplicate-email case. Both open since 27 Jul.

**Onboarding: pricing the scoping exercise** — Vankata, parked
Ivo floated ~€50 and argued a payment gate raises willingness to answer the deeper questions. Vankata deferred: "we're not on that user story yet, that's coming from sales." Logged so it isn't lost, not to be reopened now.

**Onboarding: question-structure iteration** — Vankata, parked
Deprioritised on 3 Aug: put it in front of clients and the commercial team, iterate, expect a lot of restructuring. Michael explicitly clarified he was not asking to cut questions; his concern was 30-40% Pass 2 drop-off and securing Pass 1 first. Validating the project-goal preset set (extraction / search-Q&A / classification / comparison / summarization, currently inferred) belongs here too.
