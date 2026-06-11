# STATE: fresenius-complaint-coding

_Working memory for this task. Auto-written on session end/compact. Read on session start.
This is NOT the client-facing STATUS.md._

last_session: 2026-06-03T (first scoping call, live-copilot)
last_tab: A: Operations

## Now
First scoping call done 3 Jun (Gregor / Beth / Brian / Mark). Use case = AI verifies complaint codes match the narrative, flags mismatches with reasoning, human decides. Own engagement, split out of fresenius-cmc 2026-06-04 (different stakeholders + use case from the CMC pilot, which stays in fresenius-cmc). Full detail in this engagement's STATUS.md 2026-06-03 entry.

## Next action
Wait for Jordan to book next session (week of 9 Jun, same slot ~09:00-10:00 ET; Jordan at London Tech Week then Viva Tech). Deliverables + IQVIA data request agreed there, NOT before. NO email owed: Jordan parked the data ask to next session. If accelerating, flag the IQVIA-sample idea to Jordan internally; do not email the client. Owner: Jordan (invite); Ivo prep.

## Open threads
- Open Qs for next session: code taxonomy size + fixed list? are reviewer corrections captured (original vs corrected) or overwritten? can Brian pull 30-50 IQVIA complaints (narrative + codes, incl. corrected)?
- Success metric still qualitative ("workable program"); make objective next session (recall on known mismatches at acceptable FP rate).
- Confirm with Jordan: is this a separate HubSpot deal or part of the SQR EUR 300K line? NDA coverage for this pilot's data before sharing.
- Teams-first client (Tactiq via Teams browser is the transcript workaround).
- No Drive folder yet for this engagement.

## Don't re-explain
- Jordan owns commercial + cadence. Two FME pilots: CMC (fresenius-cmc) + complaint-coding (this). EUR 25k/pilot client commitment, $25k/pilot AWS POC cash sought (Jordan's).
- **People:** Linda Gelbert = exec sponsor (owns coding-consistency concern, not on calls). Gregor Felsner = facilitator/sponsor. Beth St Germain = Director Global Complaint Mgmt (business owner). Brian Cerusuolo = analyst, the data/systems + IQVIA-export contact. Mark Samples = CIU/post-market, coding SME (US Pacific). Michelle Helton = reportability expert.
- **System facts:** narrative enters at Tech Services into Salesforce; system of record is IQVIA; pilot = manual IQVIA extract, no integration. Codes = product + failure mode + cause + action. Build for RECALL (false positives >> false negatives, per Mark). MDR clock 3/5/30 days = a speed requirement. Each miss ~ CAPA "hundreds of thousands" + possible FDA penalty. >100k files/yr.
- **Two priority capabilities:** (1) catch missed reportable escalations (compliance/MDR/483 risk, the headline value); (2) coding-consistency check (trending integrity, the measurable core). Third: product-code mislabeling at intake.
- **Design requirements:** explainability (trace to source) + suggest-not-auto-correct. Mark's target = 3-column dashboard: coding / regulatory / needs-clarification.
- Acronyms: CIU = Complaint Investigation Unit; MDR = Medical Device Report; CAPA = corrective/preventive action; 483 = FDA observation; FAR = field action request.
