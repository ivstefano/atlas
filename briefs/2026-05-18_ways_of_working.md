# Monday 18 May 2026 — Ways-of-working proposal

**Purpose**: respond to Steven's Fri 15 May ask ("share ideas on how things could improve... as a team"). Frame: structural fixes that prevent the SMS-deck fire-drill from repeating on the next tier-1 deal. Not a retro on this week.

**Audience**: Steven, Viktor, Vankata, Jordan. Goal is policy-level agreement, not blame allocation.

---

## TL;DR

1. **Deal tiers** with explicit cadence rules. Tier-1 (>€100K ARR potential or multi-year) gets ≥2 calendar weeks between final-alignment meeting and client-facing deliverable. Non-negotiable.
2. **Owner-of-record per deliverable**, written at the point of assignment. Solves "this is from the original Ivo slides" type disputes.
3. **Engagement repo as the visibility layer** (`~/Documents/engagements`). Hook into HubSpot + Asana. Replaces the Google sheet Viktor flagged. Already live for SMS, aumovio, DB.
4. **Champion-meeting invite policy**: lead SO is on every external champion meeting for tier-1 deals; reschedules go through the SO, not direct calendar swaps.
5. **Storyboard-before-slides rule**: for any deck >5 slides going to a client EVP, outline-level sign-off from Vankata + Steven before any PPTX work begins.

---

## Problem statement (one line each, no blame)

- SMS Gerald deck: final alignment Tue → senior review window collapsed to 2 hours Fri morning → multi-year deal at risk on quality.
- Viktor: no mechanism to show current deliverable state, only timeline. Issues like Aumovio invisible.
- Recurring: senior team travel + conference weeks colliding with client deadlines, no buffer.
- Recurring: deck work starts in PPTX before storyboard is agreed → mid-deck rewrites under time pressure.

---

## Proposal 1 — Deal tiers + cadence

| Tier | Definition | Final-align → deliverable | Senior review window |
|------|------------|---------------------------|---------------------|
| T1 | >€100K ARR potential, multi-year, or named-EVP audience | ≥2 calendar weeks | ≥3 working days |
| T2 | €25-100K, single-PoC, technical-champion audience | ≥1 calendar week | ≥1 working day |
| T3 | <€25K, revision/refresh of existing material | ≥3 working days | same-day OK |

Rule: if client timeline forces a shorter window, the deal-owner escalates to Steven *before* committing to the client, not after.

SMS-Gerald and DB-InfraGO-Hannah are T1. Yettel-this-week was T2. Agrolimen would have been T1 (now closed-lost).

---

## Proposal 2 — Owner-of-record

At the point any deliverable is assigned, the assigning person writes one line in the Asana task:

> "Owner: [name]. Reviewers: [names]. Inherits: [link to prior artifact if applicable]."

Eliminates the "but the original was X's slides" deflection. If you inherit material, you own it from the moment you accept the handoff.

---

## Proposal 3 — Engagement repo as visibility layer

What exists today (`~/Documents/engagements`):
- One folder per engagement, four-file shape (CONTEXT / STATUS / SOURCES / COMMERCIAL) + lazy stage folders (1_intro, 2_scoping, 3_contracting, 4_poc, 5_implementation).
- Tactiq transcripts pulled in and digested; STATUS.md is the rolling source of truth.
- AI-agent-readable: any new joiner or SO can point Claude/Cursor at the folder and get a full briefing in seconds (already used to onboard Alex on Aumovio).

What I'm proposing:
- Hook the repo into HubSpot deal records (link field per deal pointing to the engagement STATUS.md).
- Hook into Asana per-engagement section (Monday's bootstrapped tracker already has 13 sections).
- Long-term: expose via MCP server so HubSpot + Asana can pull state directly, no manual sync.

Why this answers Viktor: gives him a one-link view of *current deliverable state*, not just timeline. Independent of any individual being online.

---

## Proposal 4 — Champion-meeting invite policy

For tier-1 deals:
- Lead SO is on every recurring meeting with the technical champion + commercial sponsor.
- Reschedules go via the SO. No direct calendar swaps that drop the SO from the invite.
- If the SO can't attend, they nominate a delegate *and* get the recording + notes within 24h.

Mitigates: "I've only had visibility for 2-3 weeks" gaps that Jordan flagged. Fair point, structural fix.

---

## Proposal 5 — Storyboard before slides

For any deck >5 slides going to a client EVP or board:
1. **Day 0**: outline (slide titles + 1-line thesis per slide) in a doc, not PPTX.
2. **Day 1**: Vankata + Steven sign off on outline.
3. **Day 2+**: PPTX work begins.

McKinsey-equivalent process. Avoids the SMS-deck pattern where 30-40% of slides were structurally wrong on the morning of the send. Vankata flagged this up front on Tue; we should have listened.

---

## Asks for the meeting

1. Agree on the **tier matrix** (Proposal 1) — single biggest lever.
2. Adopt **owner-of-record** wording in Asana templates this week.
3. Bless the **engagement repo → HubSpot/Asana** integration; I'll scope effort by Wed 20 May.
4. Confirm **SO-on-invite** policy for T1; I'll audit current invites Mon afternoon.
5. Adopt **storyboard rule** for the next tier-1 deck (likely DB-InfraGO mid-June proposal).

---

## Unresolved qs

- T1 threshold €100K right number?
- Owner-of-record line: Asana custom field or free-text in description?
- Repo integration: build it or buy HubSpot+Asana native MCP?
- Storyboard sign-off: async (doc comments) or sync (15min call)?
- Who owns enforcement when a cadence rule is breached?
