# Monday 18 May 2026 — Commercial-call sync brief

**Purpose**: walk into Monday's commercial call with a current, honest picture across all engagements. Per Viktor's directive Fri 15 May: state lives in Asana + HubSpot, not Excel. This doc is the pre-sync; after the call, the deltas below get pushed to HubSpot (deal records) + Asana (tasks). Internal-only.

**Asana tracker (NEW, bootstrapped 2026-05-18)**: https://app.asana.com/1/61830076465436/project/1214855342290138 — `Iris.ai Commercial Engagements`. 13 sections (one per active engagement) + Archive. 12 `[PIPELINE]` summary tasks + 26 next-action tasks. Custom fields pending UI creation (MCP limitation). Iris.ai Product Roadmap (Vankata's) untouched.

---

## TL;DR (verbal first 60 seconds)

- **Agrolimen lost** (closed-lost, internal build). Patricia confirmed 15 May.
- **DB InfraGO landed well**, deliverable hosted, awaiting mid-June engineer eval; Jordan owes proposal mid-June.
- **TandF bundle + recording delivered, NDA sent by Ivana**, Paolo had Drive-access friction (resolved to public-read); Jordan owes proposal week of 19 May.
- **Postbank stakeholder reset** (Svetla → Lina); first call with new champion Tue 19 May 11:30 BG.
- **SMS Group Wed 20 May** is the big one — Gerald presentation, the gating event.
- **Aumovio close target** firmed to first week of June; eval-deliver in flight.
- **Daikin / Finom / Basamh** all in slow/cold drift; not urgent.
- **Welocalize** silent ~13 days — Steven owns.
- **Heineken** running on weekly cadence — Lucy + Justyna call today 15:00.

---

## Active engagements — current state + what to update in HubSpot/Asana

### 🔴 Agrolimen — **CLOSED-LOST 2026-05-15**

- **Deal stage in HubSpot**: move to **closed-lost** (HubSpot deal ID `51829987995`).
- **Amount lost**: ~€40K vendor-onboarding MVP (immediate) + ~€50K spec-extraction PoC (next quarter) + larger implementation upside (~€200-500K depending on full-rollout scope) + S/4HANA migration cross-sell hook.
- **Why**: Patricia Pastoriza emailed Jordan 10:17 UTC: *"not going ahead with any external proposals... an opportunity has emerged to conduct this development internally with a team that is already in charge of other AI initiatives."* Praised the scoping pilot: *"we were impressed with the results... would like to keep you in mind for future opportunities."*
- **Read**: build-vs-buy decision flipped to build. Likely the team is **Marco Sterbizzi's AI-area / AI-governance group** (the original Feb 2026 contact before Patricia took the spec use case forward). The wedding-leave delay framing in the 8 May call retrospectively reads as cover for this decision being prepared.
- **Preserved**: relationship with Patricia + Núria + Lidia is intact; the scoping extractor / 15-table schema / matching pipeline are reusable IP for the next FMCG / spec-digitisation lead.
- **Action**: Jordan to send graceful close-out reply (keep door open if internal hits capability / timeline issues). Mark HubSpot closed-lost. Flag Marco Sterbizzi as a 3-6 month re-engagement target if his internal build runs into trouble.
- **Gmail thread**: `19e2b24945858fba`.

### 🟢 DB InfraGO — scoping demo delivered, awaiting engineer eval

- **Deal stage in HubSpot**: scoping → contracting-in-prep (gate is engineer evaluation). Update deal next-step + close-date to **~end of July 2026** per the timeline Hannah confirmed Friday (proposal mid-June → procurement + AI-gov through summer → contract end July → kickoff post-August OOO).
- **Amount in flight**: **~€50K MVP + ~€100K full implementation + annual ontology-support contract** (~€TBD/yr). One-contract structure per Hannah's preference.
- **Demo verdict (2026-05-15)**: Hannah *"really impressed"*; *"excellent material to convince people"*. She read the deliverable correctly and dropped signature-validation + halteplatz from scope live. **Mid-June follow-up call booked: Mon 15 Jun 10:30 BG.**
- **Deliverable**: hosted at `https://iris-db-scoping-showcase.s3.eu-central-1.amazonaws.com/showcase.html`, access code `DBInfraGO-Axion-2026`. Sent to Hannah Sat 16 May with 5 open ontology questions + 7 take-aways.
- **Quality numbers we can quote**: 88% of 32 CTMS fields confidently extractable, 96.6% value-in-source (LLM-judge audit, n=815), 0 confirmed hallucinations. 100% on the 48 verbatim German local rules.
- **Approval chain (Hannah's own framing)**: engineers (technical eval, ~3 wks) → her boss (follows engineer reco) → procurement (supportive not adversarial) → controlling (already cleared — she has budget). **No real veto except engineer eval.**
- **Asana tasks to create**: (1) Jordan — prepare one-contract proposal by mid-June. (2) Ivo — be ready to host 30-min ontology call if Hannah books. (3) Ivo/Jordan — chase Hannah by mid-June if no word.
- **Mon 15 Jun call** in calendar (Jordan booked, all attending).

### 🟡 TandF — bundle delivered, NDA sent, proposal pending

- **Deal stage in HubSpot**: scoping → proposal-pending. **Close date estimate: mid-July 2026** (Paolo flagged ~4-week internal review + budget verification before go/no-go on a paid pilot).
- **Amount in flight**: PoC ~**€50K** (Jordan's guess, IRIS absorbing ~€25K of at-cost ~€75K). Full implementation ~2-3× (~€100-150K). Then managed service on T&F's AWS VPC (recurring).
- **Status**:
  - **15 May 09:17**: Ivo sent the scoping bundle + recording link to Paolo + David, cc Jordan + Victor.
  - **15 May 09:54**: Paolo replied — can't access from corporate email, asked to share with `tandfapis@gmail.com` (T&F team account).
  - **15 May 10:06**: Ivo replied — that email address comes back invalid.
  - **15 May 12:06**: Ivo opened the Drive folder to "anyone with the link can view" and replied to Paolo to try again.
  - **15 May 12:29**: **Ivana sent the MNDA directly to Paolo** (cc Ivan Georgiev / CTO / signatory, Jordan, Ivo). Subject "МNDA Iris.ai - T&F".
  - **Awaiting**: Paolo's confirmation he can access the folder + acknowledgement of MNDA.
- **Paolo's stated requirements on the call**: managed service IS a required pilot output. Wants costing-clarity + latency + performance numbers from the pilot. KPI: very high precision/recall, correct magnitude (not p-values).
- **What Paolo flagged on the call**: p-value vs magnitude bug + citation-sourced finding to exclude. Both PoC discovery items.
- **Asana tasks to create**: (1) Jordan — formal proposal by Tue 19 May (his commitment to Paolo 5 working days = 19 May). (2) Ivo — chase Paolo on Drive access + MNDA ack early next week if no response. (3) Track next call ~2026-06-09 (4 weeks out from 12 May scoping presentation).
- **Risk**: T&F building this internally too — disclosed upfront; positioning is "complementary not competing".

### 🟡 Postbank — stakeholder handover, first call with Lina Tue 19 May 11:30 BG

- **Deal stage in HubSpot**: scoping. **Replace contact**: Svetla Yankova → **Lina Varbanova** (`LVarbanova@postbank.bg`). Add note re: Svetla left Postbank week of 12 May.
- **Amount in flight**: **~€40K co-funded PoC** (IRIS absorbing ~€10K of standard €50K). Full implementation ~2-3×. Then managed service usage-based.
- **Status**:
  - **2026-05-14 06:15 UTC**: Svetla announced her final week, handed conversation to Lina Varbanova on the same Gmail thread.
  - **2026-05-14 14:25 UTC**: Ivo sent Lina welcome reply on the existing thread (Tue 19 May 11:30 BG confirmed).
  - **Mon 18 May EOD**: Ivo sending pre-read pack to Lina (draft ready in chat).
  - **Tue 19 May 11:30 BG**: first call with Lina.
- **Open items Svetla left dangling** (worth flagging to Lina at Tue call):
  - MNDA timing (was Lena's decision)
  - Value quantification (Lena was producing for first committee)
  - Head of Salesforce introduction (Svetla was to invite)
  - Solid AI parallel evaluation status (not discussed on 8 May call)
- **Relationship hook (lost)**: Svetla went to high school with Viktor Botev. With her gone, the warm-relationship anchor is gone. Need to build with Lina cold.
- **Risk**: 5-day-pre-call champion change. Mitigation = robust pre-read + Lina has the existing thread context.
- **Asana tasks**: (1) Ivo — send pre-read pack Mon EOD. (2) Jordan + Ivo — Tue 19 May 11:30 BG call attendance. (3) post-call STATUS.md + HubSpot update.

### 🟢 SMS Group — **WED 20 MAY GERALD PRESENTATION (the big one)**

- **Deal stage in HubSpot**: PoC complete → presenting results. **Stage critical**: Gerald Mayr (EVP, retiring autumn 2026) is the deciding stakeholder.
- **Amount in flight**: per the 13 May Jordan/Vankata/Steven internal sync:
  - **Per full plant cost-to-IRIS**: €400-700K
  - **Target price per full plant**: €600K-€1.1M (margin)
  - **Phased anchor**: €15K × first 10 machines = €150K, then €8K × next 40 = €320K, then €5K × remaining 100 = €500K → **~€950K-€1.3M for 150 machines**
  - **+ 30% discount on second plant, tapering to 50% by plant 4-5**
  - Multi-plant trajectory = multi-€M deal over 3-5 yrs
- **Status**:
  - **20 May session locked** via Thorsten's Teams invite (sent 13 May 08:12 UTC). Attendees: Gerald, Matthias Tarnow, Thorsten, Vankata, Jordan, Ivo, Petar.
  - **Preview package sent** to Thorsten 14 May (demo video + preview deck).
  - **Ivo demoed the showcase** to internal IRIS team; Jordan presents to Gerald.
  - **Cost numbers still need Steven + Victor validation** before they land in any deck (the 13 May internal sync called this out).
- **Pre-Wed prep needed**:
  - Confirm cost-numbers validated by Steven + Victor
  - Demo recording cleanly captured (Vankata recorded before HU travel, but verify)
  - Slide-deck final review with Vankata's story-doc spine
  - Lead with business case (saving even single-digit % of engineering effort on multi-€M plants → €M savings); avoid "digital twin" framing (Victor's 12 May warning re: European labour-replacement perception)
- **Asana tasks**: (1) Ivo — confirm cost-number validation by Steven + Victor (Mon evening). (2) Team alignment for Wed 20 May (Mon evening / Tue morning). (3) Post-call STATUS.md + HubSpot stage update + outcome capture.

### 🟢 Aumovio — close target 1st week of June, V5 plan firm

- **Deal stage in HubSpot**: PoC implementation → eval-deliver. Update **expected close** to **first week of June 2026**.
- **Amount in flight**: V5 PoC at-cost (~€50K range), with full implementation ~2-3× + ongoing.
- **Status (13 May at-scale-extraction sync)**:
  - **Phil's V4 review delivered with column-CX comments via MoveIT** 13 May 11:26 EEST.
  - **Decision**: move OFF MoveIT to S3 / dedicated secure account for file exchange.
  - **Logic fixes**: Daimler lifetime volume sum, Ford SOP relative-date logic, Ford left/right caliper ×2 multiplication regression, plant location → supplier manufacturing location (GSDB codes for Ford).
  - **Plan**: 2 more eval sets → final 10-doc eval (5 reviewed + 5 random unbiased) → soft close 1st week of June.
  - **Next call**: **Fri 22 May** (Norbert to confirm Jordan's proposed time).
- **Open**: Phil's success bar (Norbert + Phil aligning internally week of 18 May). The actual numeric success-criteria number is the single biggest pre-eval-deliver input still missing.
- **Asana tasks**: (1) Ivo — V5 build incl. one Chinese contract through translation pre-step. (2) Ivo + Jordan — Fri 22 May follow-up call. (3) Track Norbert + Phil's internal success-bar alignment week of 18 May.

### 🟡 Garrett — Tue 19 May follow-up, internal answer due

- **Deal stage in HubSpot**: scoping → awaiting client internal decision.
- **Amount in flight**: paid co-funded MVP (~€30-50K range), structure TBD.
- **Status**: Liviu coming back with internal answer on paid co-funded MVP after briefing Alex (Head of AI) / Legal / Cyber / AWS. **Call Tue 19 May 13:30 BG.**
- **Asana tasks**: (1) Tue 19 May call attendance. (2) Post-call STATUS.md + HubSpot stage update.

### 🟢 Heineken — PoC presentation today

- **Deal stage in HubSpot**: PoC eval-deliver → presentation today.
- **Status**: **PoC presentation today Mon 18 May 15:00 BG** to Lucy + Justyna. This is the eval-deliver milestone — IRIS walks the PoC results. Outcome of this call sets the trajectory for the rest of the engagement (extension, full implementation scoping, or close).
- **Recent context**: 13 May Gmail digest confirmed human-in-the-loop = continuous learning interpretation was always Jordan's original Mar 6 ask.
- **Action**: post-call, capture outcome in STATUS.md + HubSpot stage update.

### 🟡 Welocalize — silent ~13 days (since 5 May)

- **Deal stage in HubSpot**: scoping (Yufan follow-up not booked yet).
- **Status**: no contact since 5 May. **Steven owns the relationship.**
- **Action**: flag at the commercial call — does Steven have visibility on why it went cold? Risk of further drift.
- **Asana task**: Steven to chase Yufan if no movement by 22 May.

### 🟡 Daikin — no-show, reschedule pending

- **Deal stage in HubSpot**: intro (cool, not lost).
- **Status**: Haruka Degawa no-showed 13 May intro. Maria Volkova rescheduling ~2-3 weeks out (target ~3 June 2026).
- **Asana task**: Maria — confirm new slot booked by Mon 25 May.

### 🟡 Finom — no-show 14 May

- **Deal stage in HubSpot**: intro (no contact post-decline).
- **Status**: Valeriy Dmitriev declined the 14 May invite; nobody from Finom showed. Engagement is essentially dead unless they re-engage.
- **Asana task**: ping back in 2 weeks if no response? Or close-lost? Decide at commercial call.

### 🟡 Basamh — Stan rescheduled to Tue 3 June

- **Deal stage in HubSpot**: intro. **Engagement folder doesn't exist in repo** — bootstrap pending.
- **Status**: Mohamed Ni handed off to Abdullah Alamoudi (Head of Data & Analytics). Stan Stefanov rescheduled to **Tue 3 June 14:00 Saudi / 13:00 CET**.
- **Asana task**: (1) Stan — Tue 3 June call. (2) Ivo — bootstrap engagements/basamh/ folder if engagement progresses.

### ⚪ NHS — stalled / dormant

- **Deal stage in HubSpot**: should be **closed-lost-no-fit** or **dormant** depending on HubSpot stage taxonomy. Three transcripts digested, engagement marked stalled.
- **Asana task**: confirm closed-status decision at commercial call.

### ⚪ Fresenius — scoping, no recent activity

- **Deal stage in HubSpot**: scoping. Last activity 13 May (folder migration).
- **Asana task**: confirm at commercial call — who owns next touch?

---

## Pipeline summary for the call

| Stage | Engagements | Approx value |
|---|---|---|
| **Closed-won** | — | — |
| **Closed-lost (new)** | Agrolimen | ~€40K + ~€50K + future ~€200-500K lost |
| **PoC / contracting** | DB InfraGO, SMS Group, Aumovio, Heineken, TandF | €50K-€1.3M each, sum 6-figure → low 7-figure |
| **Scoping** | Postbank, Garrett, Welocalize, Fresenius | ~€40-50K each PoC value |
| **Intro / cold** | Daikin, Finom, Basamh | TBD |
| **Dormant** | NHS | n/a |

---

## What to flag verbally at the commercial call

1. **Agrolimen closed-lost** — internal build flipped the decision. Build-vs-buy signal for FMCG.
2. **SMS Wed 20 May** is the make-or-break event of the week. Cost-number validation by Steven + Victor needs to happen Mon evening at latest.
3. **TandF proposal due Tue 19 May** — confirm Jordan is on track. NDA momentum is fresh (Ivana sent Fri).
4. **Postbank champion handover** — Lina is brand new. Tue 19 May 11:30 BG call is high-stakes "rebuild rapport from cold" first contact. Pre-read going out Mon EOD.
5. **Aumovio close target firmed** to first week of June. Phil's internal success bar is the last input.
6. **Welocalize 13-day silence** — Steven, what's the status?
7. **MCPs**: HubSpot + Asana MCPs not wired in atlas yet — sync will be manual today. Worth flagging to Viktor as a 1-2 day eng investment that would let me drive Monday briefs from the repo automatically.

---

## State-sync actions for Monday (post-call)

After the call, push these to HubSpot + Asana:

### HubSpot deal updates
- [ ] Agrolimen `51829987995` → closed-lost, reason "client internal build", lost-reason note + Patricia's email reference
- [ ] DB InfraGO → contracting-in-prep, close ~end July, next-step "mid-June engineer eval"
- [ ] TandF → proposal-pending, close ~mid-July, next-step "Jordan proposal Tue 19 May"
- [ ] Postbank → replace contact Svetla → Lina Varbanova, note re: champion handover
- [ ] SMS → next-step "Wed 20 May Gerald presentation"
- [ ] Aumovio → expected close 1st week June, next-step "Fri 22 May follow-up"
- [ ] Heineken → confirm sub-stage after today's call
- [ ] Daikin → next-step "Maria reschedule by 25 May"
- [ ] Welocalize → escalate to Steven for status
- [ ] NHS → confirm closed-lost / dormant decision

### Asana tasks to create
- [ ] Jordan: Send graceful Agrolimen close-out reply (due Tue 19 May)
- [ ] Jordan: TandF proposal (due Tue 19 May)
- [ ] Jordan: DB proposal (due mid-June)
- [ ] Ivo: Postbank Lina pre-read (due Mon 18 May EOD)
- [ ] Ivo: Confirm SMS cost-numbers validated by Steven + Victor (due Mon evening)
- [ ] Ivo + team: SMS final prep Mon evening / Tue morning
- [ ] Ivo: Aumovio V5 build incl. Chinese-contract translation pre-step (due Fri 22 May)
- [ ] Stan: Basamh Tue 3 June call coordination
- [ ] Maria: Daikin reschedule confirmation by Mon 25 May
- [ ] Steven: Welocalize chase if no movement by 22 May

---

## Open questions for the call

- Marco Sterbizzi as a 3-6 month Agrolimen re-engagement target — yes or shelve?
- Finom — close-lost now or wait 2 weeks?
- NHS — what's the official HubSpot status (closed-lost-no-fit vs dormant)?
- Welocalize — who chases Yufan, and when?
- HubSpot + Asana MCP wiring — is this a Q3 task or worth fast-tracking?
