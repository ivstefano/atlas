# Call brief — Fresenius Complaint Coding, Weekly Project Group

**When:** Fri 26 Jun, 17:00-18:00 Sofia / 15:00-16:00 BST / 10:00-11:00 ET (1h)
**Organizer:** Jordan. You accepted. (Earlier declined a duplicate invite by mistake, re-accepted; Jordan asked who'd cover, resolved.)
**Cadence:** recurring weekly. This is the FIRST project group since 12 Jun — 19 Jun was skipped (US holiday, Danielle flagged).

## Attendees (calendar)
- IRIS: Ivo (lead SA), Jordan (organizer), Ivan Tsenov / Vankata (CPO, needsAction), Steven (optional)
- FME core: Mark Samples (coding SME), Brian Cerasuolo (data/systems), Danielle Fleckner (PMS mgr)
- FME optional: Beth St Germain (business owner, tentative — was OOO 18-22 Jun), Gregor Felsner (sponsor, accepted), Gerome Fischer (innovation/AI, tentative), Om Gaikwad (accepted, new face)

## The one thing this call must close: the data handover
The data request — the gate on everything — was agreed 12 Jun but **never sent**. No complaint-coding data email exists in Gmail (only meeting invites + the separate CMC thread). Two weeks gone. Walk in ready to either hand FME the ask live or, better, have the email out before/at the call.

Three artifacts (Vankata's list):
1. Narrative + assigned codes, ~100 records (input→output pairs)
2. Code list / ontology doc (Brian has it)
3. Issue / remediation reports — reviewer write-ups of coding problems = documented known-errors, the recall benchmark, the most valuable input

Still open from 12 Jun (close them live):
- **Owner** to pull (likely Brian) + **release authority** (likely Gregor)
- **De-identification path** — who, how, by when
- **NDA coverage** before any data leaves FME — confirm with Jordan it's in place
- **Delivery channel:** secure upload link (same Neuralith pattern Vankata used for CMC: neuralith-dev.iris.ai/upload-file/...). Offer to send one.

## Talking points / where scope stands
- Core requirements doc drafted (18 Jun) and shared as `core-requirements.md` — one capability (does the data match the code?) at three lifecycle checks. If not yet sent to FME, this call is the moment to walk them through it for inline comment. Lives in Jordan's shared Google Doc `1Tj_mrD-f2xJNM3Tz-FuBJ0YXh34tA7TPPh1aye_RFjM`.
- The three checks: (1) narrative→code area-level, (2) right specific code within area, (3) reportability at intake (highest-priority output). Open question to raise: the 4th check (investigation→coding agreement) — in pilot or later phase?
- Reinforce the value framing: FME has no coding-error-rate baseline today; running the validated AI over the corpus *produces* that baseline — a deliverable in itself. Manual route = "year-long project."
- Metrics stay deferred (correct): targets set after ~2 wks on real data. Don't let Beth pull you into SMART numbers before data is seen.
- Deployment settled: batch, not live. Export from CHS → IRIS → dashboard. No live intake integration in pilot.

## Method reminder (so you speak it confidently)
POC is NOT extraction. Phase 1 = define the ontology FROM examples ("data retrospection agent"), because when-to-apply rules are tacit medical expertise → SME-review with Mark → Phase 2 = classify, surface mismatches, spot-check. Success = surfaced mismatches are REAL on spot-check, not raw agreement with existing (imperfect) codes.

## Other opens
- New deck shared 10 Jun: "Fresenius - CMC and Complaint Coding Initiatives" (Jordan's). Skim if it comes up.
- Commercial: confirm with Jordan whether this is a separate HubSpot deal or part of the SQR line. EUR 25k/pilot client + $25k/pilot AWS POC cash sought.
- Mark's dashboard target: 3 columns — coding / regulatory / needs-clarification.

## Your asks into the room (proposed)
1. Confirm data owners + de-ID path + a date. Get a name and a deadline before the call ends.
2. Offer the secure upload link now; remove the channel as an excuse.
3. Walk the core-requirements doc, request inline comments by next session.
4. Confirm NDA covers the data transfer (check with Jordan first).
