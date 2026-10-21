# Iris.ai <> Ulstein next steps, Wed 21 Oct 14:00
Ulstein PLM design data migration, scoping stage (Axion extraction). Join: https://meet.google.com/dvz-sono-qhg (14:00-15:00 EEST).

## Who is on the call
- Jose Jorge Agis, Ulstein: client technical contact. Raised the PLM-vendor constraint and gave the volume estimates. Accepted the invite. Exact title unknown.
- Anita Schjøll Abildgaard, Iris.ai: founder, relationship owner, organizer.
- Ivo Stefanov, Iris.ai: solutions architect, tech lead.
- Ivan Tsenov (Vankata), Iris.ai: CPO, senior technical voice. Invite shows needsAction.
- Victor (Viktor Botev), Iris.ai: CTO. Invite shows needsAction.
- New faces: none.
- Not on the invite: Tore Ulstein (Chair, PLM budget holder, decision-maker) and Johannes (critical in procurement). Neither is listed as attending, so confirm with Jose whether either joins later.
- Away: Jordan Ryken is away 19 Oct to 9 Nov. Eric Frances covers by default.

## Last touchpoints
- 2026-10-14: Ivo emailed Jose and Tore the demo link and access code. Cc Anita, Vankata, Steven. No reply in Gmail.
- 2026-10-09: Invite for this call sent by Anita.
- 2026-10-09: Scoping call "PLM migration review and follow-up" (Anita, Vankata, Jose). Ivo was sick and Vankata presented the demo. No transcript was recorded.
  - Anita's follow-up email to Jose, in Norwegian, said Jose would clarify three things internally: which stakeholders to involve, where the documents are stored, and whether Ulstein wants its own SQL database for the metadata or direct PLM integration.
  - Jose's estimates: about 50 ships a year, 5-10 documents per design, about 10 years of documentation.
- 2026-10-07: Demo built and hosted. All 5 samples extracted, 23,304 values.
  - 1,759 of 1,768 values were confirmed by all six readings.
  - 967 of 970 highlighted values were confirmed.
  - 38 of 39 arithmetic checks passed (T279 is not on the drawing).
  - The PLM vendor is Cadmatic Wave, on CONTACT Elements, with no public schema.
- 2026-10-05: Engagement opened.

## HubSpot
HubSpot: not available. From COMMERCIAL.md only: deal "Ulstein - PLM Design Data Migration POC", amount EUR 50,000 (placeholder), close date 2026-12-20. Live deal stage and next step are unknown.
Calls he was not on: HubSpot: not available. The 9 Oct call was the one Ivo missed, and it is summarized above.

## Open threads
- Jose's answers on stakeholders, document location and storage option (own SQL database vs direct PLM integration). Owner: Jose. No date. This is the current blocker.
- Wave data model and import format. Blocked on this since 7 Oct. It was to be asked on the 9 Oct call, and the status log has no answer. Owner: Jose or the Ulstein side. Ask today.
- Commercial draft from Jose's volume estimates. Owner: Anita, Vankata and Ivo. Due 2026-10-21, today. No evidence in the sources that it exists.
- Demo feedback: no reply since the 14 Oct access email. Unknown whether Jose or Tore opened it.
- Pilot proposal after the technical session. Owner: Anita, with Eric as commercial cover.

## Goal for this call
Leave with Jose's answers on the three open questions and a named route into the Wave import format. Then agree a date to send the pilot scope, so Anita can take the commercial draft to Tore. Decider on scope and budget: Tore, via Anita. Target: answers on the call, pilot scope agreed this week.

## Questions to ask
1. What does Wave accept for import (file format, API, staging tables)? Who at Ulstein or Cadmatic can share the data model?
2. Own SQL database for the metadata, or direct integration into the PLM? Which does Ulstein prefer?
3. Where do the ~10 years of documents live (local drives, SharePoint)? Can we get a representative batch, including original PDFs with the yellow highlights?
4. Which stakeholders should be involved, and does Johannes see the method and accuracy evidence before procurement?
5. Did you and Tore open the demo? Which doc types should a pilot cover first?

## Risks
- Wave schema and import format unknown. Handle: ask directly, and state the gap plainly (line B6 below). Do not promise zero vendor-side change.
- Johannes, the procurement critic, may see this as "simple under the hood". Handle: lead with the method per doc type and the cross-check evidence from the demo.
- Ivo missed the 9 Oct call and there is no transcript. Handle: open by asking Jose to recap what he took from it. Do not re-ask what Vankata already covered.
- Commercial draft due today may not exist. Handle: say it follows once Jose's volume and storage answers are in. Anita owns the timing.
- Pricing questions. Handle: nothing has been discussed with the client, so pass it to Anita and Eric (D line below).

## Pocket lines
- If they ask whether the output fits Wave with no vendor-side change: B4 "That's a known item, it gets solved in phase 1 of implementation, not in the POC." (only once the Wave format is known). Otherwise B6 "I'd rather be straight with you: that part isn't built yet. Here's what is, and here's the plan for the rest."
- If they ask about accuracy on messy scans: B7 "There's about 10-15% of cases that still need work. That's expected at this stage, and it closes in 1-2 iterations." Use it only if the demo evidence supports it.
- If they ask for a firm number, price or timeline: D13 "Good question. I don't want to guess, I'll get you the real answer by [day]."
- If they ask for a rough sense: D14 "I can give you a rough sense now, and the exact figure by [day]. Which do you want?"

## Figures he may be asked about
No figure is approved. Do not quote any of the figures below. If asked, use D12 "Let me confirm the exact number and come back to you, I'd rather be precise than fast."
- Extraction accuracy, cost reduction, migration time saved, faster data preparation, documents processed, connector count, years in production: do not quote.
- Demo-specific counts (1,759 of 1,768, 967 of 970) come from the engagement log, not from Cognion. Treat them as demo results on 5 samples, not general accuracy claims.

## Jordan owns
Away until 9 Nov. Flag only, no drafts. Covered by Eric Frances:
- For Eric (cover): pricing and the pilot proposal commercial terms, SoW and NDA send, any reschedules.
- For Jordan when back: HubSpot deal ownership. He is listed as co-owner of the Ulstein deal.

---
_Autopilot brief, generated 2026-10-21 13:55. Live sidekick: http://127.0.0.1:8095/live/2026-10-21_1400_iris-ai-ulstein-next-steps_
