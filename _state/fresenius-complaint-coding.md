# STATE: fresenius-complaint-coding

_Working memory for this task. Auto-written on session end/compact. Read on session start.
This is NOT the client-facing STATUS.md._

last_session: 2026-06-12T (second scoping session, live-copilot)
last_tab: A: Operations

## Now
Second scoping session done 12 Jun. THREE deliverables locked (Mark): (1) narrative→code alignment at intake (right area + right specific code), (2) reportability conditions at intake, (3) investigation→coding alignment late-stage (consistency across products/sites/over-time). Gregor unified it as ONE early-stage correctness check, not separate products. POC reframed by Vankata: NOT extraction — phase 1 = define ontology FROM examples ("data retrospection agent") → SME-review → phase 2 = classify + spot-check mismatches → produces the error-rate baseline FME can't get manually. Deployment = batch export from CHS → IRIS → dashboard (no live integration; FME lockdowns). Full detail STATUS.md 2026-06-12 + 1_pre-scoping/2026-06-12_pilot-scope-wip.md.

## Next action
Send FME the data request (3 artifacts, Vankata's list): (1) input→output pairs — narrative + assigned codes, ~100 records; (2) codes/ontology doc (Brian has it); (3) issue/remediation reports (reviewer write-ups = documented known-errors / recall benchmark). Ask de-identification path + owner + date. Likely puller: Brian; release authority: Gregor. Owner: Ivo/Jordan. Also: schedule recurring SteerCo+project-group; identify "Jerome/Gerome".

## Open threads
- Data handover NOT committed in-call (owners/de-ID/dates) — close async. This is the gate on everything.
- Ground truth is imperfect: existing CHS codes are baseline but "not 100% true" (Gregor). Success = surfaced mismatches are REAL on spot-check, not raw agreement with existing codes.
- Ontology partly UNWRITTEN: code list exists, when-to-apply rules are tacit medical expertise. Work via examples + model's medical knowledge + Mark SME time.
- Metrics deferred (correct): premature until data seen; requirements doc is "living", fully defined after ~2 wks scoping on real data.
- Scale ~8,000 complaints/mo NA. Pain: ~3-5 clarifications/day to Tech Services + regulatory audit exposure.
- Beth may have accidentally declined the invite — ensure she's on next.
- Shared Google Doc (Jordan's "Core Requirements"): 1Tj_mrD-f2xJNM3Tz-FuBJ0YXh34tA7TPPh1aye_RFjM.
- Confirm with Jordan: separate HubSpot deal or part of SQR line? NDA coverage before data sharing. Teams-first (Tactiq via browser). No Drive folder yet.

## Don't re-explain
- Jordan owns commercial + cadence. Two FME pilots: CMC (fresenius-cmc) + complaint-coding (this). EUR 25k/pilot client commitment, $25k/pilot AWS POC cash sought (Jordan's).
- **People:** Linda Gelbert = exec sponsor (owns coding-consistency concern, not on calls). Gregor Felsner = facilitator/sponsor. Beth St Germain = Director Global Complaint Mgmt (business owner). Brian Cerusuolo = analyst, the data/systems + IQVIA-export contact. Mark Samples = CIU/post-market, coding SME (US Pacific). Michelle Helton = reportability expert.
- **System facts:** narrative enters at Tech Services into Salesforce; system of record is IQVIA; pilot = manual IQVIA extract, no integration. Codes = product + failure mode + cause + action. Build for RECALL (false positives >> false negatives, per Mark). MDR clock 3/5/30 days = a speed requirement. Each miss ~ CAPA "hundreds of thousands" + possible FDA penalty. >100k files/yr.
- **Two priority capabilities:** (1) catch missed reportable escalations (compliance/MDR/483 risk, the headline value); (2) coding-consistency check (trending integrity, the measurable core). Third: product-code mislabeling at intake.
- **Design requirements:** explainability (trace to source) + suggest-not-auto-correct. Mark's target = 3-column dashboard: coding / regulatory / needs-clarification.
- Acronyms: CIU = Complaint Investigation Unit; MDR = Medical Device Report; CAPA = corrective/preventive action; 483 = FDA observation; FAR = field action request.
