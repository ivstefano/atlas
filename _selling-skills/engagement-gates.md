# Engagement gates (canonical)

Single source of truth for the engagement phases, the SA's job in each, and the go/no-go gates. The `/call-gates` skill scores calls against this file. The team-facing proposal (`engagement-flow-proposal.md`) copies from here; when the team changes a gate, edit it here first.

**Status: DRAFT v0, 2026-09-25.** Source: Vankata's Miro board (new flow), Vankata/Vasko/Ivo call 2026-09-24, commercial feedback call 2026-09-25 (Viktor, Vankata, Steven, Jordan, Eric). Not yet confirmed by Vankata or approved by Viktor. Items marked OPEN are unresolved.

## Flow

Lead/Qualification (Sales) → Technical Assessment (1-2 wks, SA) → Discovery / Kickstart Program (20k, 4 wks, Vasko) → Proposal → Launchpad License (50-60k, 3-6 months) → Full License (extension)

Removed from the old flow: free scoping/POC, fixed-scope MVP, Bridge Phase.

## Gate states

Every gate takes exactly one state:

- **MET**: a client-side quote or artifact proves it. Cite speaker + timestamp or file.
- **NOT MET**: the client said no, or the evidence contradicts the gate.
- **UNKNOWN**: nobody asked, or only IRIS people spoke to it.

IRIS statements never make a client gate MET. "Jordan said they'll bring an expert" is UNKNOWN until the client names the expert. Gates marked (IRIS) describe something IRIS must tell the client; for those, the IRIS quote is the evidence.

Hard gates (H) block the next phase when NOT MET. Soft gates (S) raise risk but do not block.

## Phase 1: Lead / Qualification

Owner: Sales (Jordan). SA: not required.

| ID | Gate | Type |
|---|---|---|
| L1 | Champion named, with role | H |
| L2 | Pain stated in the client's words | H |
| L3 | Budget range estimated | S |
| L4 | Trigger event known (why now) | S |

## Stoppers (check right after the first deep dive)

Added 2026-10-19 after FINCA (war room: Vankata "this is not what we do… cancel the AWS request", Steven "we don't do non-profit", "it should have been stopped three months ago"). Any one stopper means: no scoping work, no demo, no AWS funding request until Vankata (use case) and Steven (commercial) answer in writing.

| ID | Stopper | Example |
|---|---|---|
| S1 | Non-profit, NGO, or no own budget ("we'll take it to donors / sponsors / funders") | FINCA, 361 raising from donors |
| S2 | Core of the use case is not on the capability map (core-iris) today: photo or image grading, prediction or decisions about people, anything needing a trained model we don't have | FINCA farm photos, credit decisions |
| S3 | Client can't say what they want, or asks for open-ended "AI that figures out what to do" instead of a concrete job | FINCA "malleable AI" |
| S4 | No document or data job at the core (unstructured in, structured out). Vankata's line: we sell Axion extraction, engineering niche | |
| S5 | Use case reframed by IRIS on a call (e.g. "switch to document extraction only") but the client never confirmed the new frame | FINCA, frame from ~3 months earlier never switched |

How to flag, within 24 h of the deep dive, in the engagement's Slack thread, @Vankata @Steven:
> Before I start work on <client>: <stopper in one line, with the client's own words>. Use case as I understand it: <one line>. Not covered by us: <list>. Go or stop?

Their written answer is the paper trail. If Sales overrides a flag, send one written FYI to Steven ("I flagged X, <owner> wants to continue, your call") and stop arguing it. Log the flag and the answer in STATUS.

Don't confirm capabilities live on the call either: "Let me check that with our CPO and come back to you in writing" (pocket-lines Group D).

## Phase 2: Technical Assessment (1-2 weeks)

Owner: SA (Ivo). This is where the SA says no on technical grounds. Input: `scoping-intake-questionnaire.md`.

| ID | Gate | Type |
|---|---|---|
| T1 | Use case fits what the product does today. Anything that needs roadmap is listed as roadmap | H |
| T2 | Data exists and the client can share it (or a mock) within 2 weeks. Sender named | H |
| T3 | Baseline known: how the job is done today, time per unit, error rate or who checks it | H |
| T4 | Success metric stated by the client, with a number | H |
| T5 | Budget owner named, and whether it is the champion | S |
| T6 | Expected-answer set (ground truth) available or planned | S |

SA output: one-page Technical Assessment with GO / NO-GO / GO-WITH-CONDITIONS and the gate table.

## Phase 3: Discovery / Kickstart Program (4 weeks, 20k)

Owner: Vasko. SA: data sizing, demo, requirements to engineers, real-vs-roadmap line. Engineer on the case within 2 weeks (Vankata).

Content (Miro): get data or mock, create demo, discovery of project needs, form Steerco, assess stakeholders, quick demo hosted on platform (front-end engineer), enablement workshops (how to do AI in enterprise), strategic partner plus other partners.

Entry gates, checked before the program starts:

| ID | Gate | Type |
|---|---|---|
| D1 | Client commitment: client pays a share, OR (AWS covers all) client signs that meeting the exit criteria moves them to Launchpad with no further approval gates. OPEN: Viktor wants at least 5k or ~30% from the client; the board shows 20k → AWS | H |
| D2 | Steerco named: people, roles, hours per week | H |
| D3 | Evaluator is a named domain expert, not a proxy | H |
| D4 | (IRIS) IRIS told the client the Launchpad price (50-60k) | H |
| D5 | (IRIS) IRIS told the client the program does not guarantee accuracy | S |
| D6 | Exit criteria written and agreed before start | H |

Exit gates, checked at week 4:

| ID | Gate | Type |
|---|---|---|
| X1 | Named expert evaluated output against the T3 baseline | H |
| X2 | Budget owner and budget line (the "bucket") identified for Launchpad | H |
| X3 | Written decision: proceed to Launchpad, or stop | H |

## Phase 4: Proposal and Launchpad License (50-60k, 3-6 months)

Owner: Jordan (commercial), Vasko (program). SA: defines the 10 baseline agents, SOW data-for-accuracy terms, product feedback.

| ID | Gate | Type |
|---|---|---|
| P1 | SOW lists the data the client provides and the accuracy IRIS commits to on that data | H |
| P2 | Steerco continues, same people as D2 or named replacements | S |
| P3 | No new stakeholders at signature that nobody met in Discovery | S |

## Kill signals (any phase)

Any one of these triggers a HOLD review with Vankata and Viktor:

- Steerco members or the evaluator skip two sessions in a row.
- The evaluator sees results better than their baseline and pushes to stop (Garrett, 2026-09-24).
- The client offers data but no meeting time ("send us data, we'll look", Steven).
- New stakeholders appear at negotiation.
- IRIS offers a discount or free work that the client did not ask for.

## Who decides

- SA can recommend NO-GO at Technical Assessment. OPEN: can the SA stop a deal alone, or only recommend?
- OPEN: one kill-gate at Discovery exit (Jordan) or several (Viktor, Steven).
- Exceptions to D1 need Viktor's approval, per case.
