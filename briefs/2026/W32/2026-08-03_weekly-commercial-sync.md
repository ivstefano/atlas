# Weekly commercial sync — Mon 2026-08-03
Covering week of Mon 27 Jul – Sun 2 Aug. Sources: engagements repo, atlas repo, filed transcripts.

Three engagements moved. Two dormant ones carry gates that go stale if not touched. Ranked by commercial urgency.

---

## 1. SimLab / Valencia Energy — moved most, biggest new upside

**Stage:** pre-scoping, unpaid POC. Path: unpaid POC → 8-10 wk paid POC → implementation.

**Last week:** second technical call 30 Jul (Tim absent). Manuals folder discovered mid-call, retrieved and assessed same day. Recap email + 12 questions for Tim sent 31 Jul to Marek + Niall (cc Steven).

**Three material corrections to what we thought:**
- **Niall IS the client.** Buyer and internal champion, not adjacent. Previously logged wrong.
- **There is an approver above him: "Mark", Chief Energy Infrastructure.** We are building for Mark's business case, not Niall's sign-off. Surname still not captured.
- **The real deadline driver is an NVIDIA GTC keynote** (Berlin, date still not obtained). Niall places customer stories there. Pilsworth is "number one, mostly complete, all we need is the AI capability on top."

**Two deliverables now, and they must not share an accuracy bar:**

| | Keynote snippet | Valencia POC |
|---|---|---|
| Bar | "doesn't need to be 100%" (Niall's words) | real precision/recall |
| Data | what we hold | needs SCADA |
| Timing | GTC Berlin, TBC | 8-10 wk paid |

Risk to manage in the sync: do not let "doesn't need to be accurate" leak into the paid POC scope.

**Commercial upside, unowned:** Niall offered co-marketing through NVIDIA and HPE channels, an MoU, and floated a white-label digital-twin product with HPE opening doors ("Shell and the big companies"). Offered unprompted. **No owner, no date.** Steven's to run. This is the largest un-actioned item in the whole portfolio.

**Blocker:** SCADA sensor history still not delivered. Tim claims he sent it twice; the SharePoint folder is empty. Two chasers on it.

**Honest finding worth surfacing:** we tested whether delivered data can predict future events. **It cannot.** VIR207 has 9 dated readings against 153 breakdowns; median breakdown's nearest reading is 102 days old. Supports multi-year wear assessment, not event prediction. Apparent time-clustering (79%) collapses to 1.13x random under a null model — **do not present the 79% figure.** Framing for Niall: retrospective proof now, predictive proof when sensor data lands.

**Offsetting good news:** manuals carry ~1,565 coded Jenbacher alarms plus in-document thresholds. Fault normalisation becomes a mapping job against an existing OEM vocabulary rather than a taxonomy we invent — buildable with zero SCADA.

**Next action:** await Tim. If nothing by ~7 Aug, chase is 30 min with Tim directly, not a resend. Nobody else can answer these. Steven out last week.

---

## 2. Barentz — new engagement, scope narrowed hard, director gate still unresolved

**Stage:** intro → pre-scoping. **EUR 50K** POC default (25-75K band). Commercial owner: Jordan.

**Last week:** deep-dive scoping call 30 Jul (Jordan + Ivo + Jurek, ~27 min, Ivo's first direct contact). Engagement folder scaffolded. Data-request email sent same day with upload link.

**Scope narrowed materially vs the May note.** Jurek: "let's focus only on products, don't touch suppliers and customers at all." ~1,500 products. The 800-package-types framing from May was his illustrative example, not the job.

**Where the work actually is:** step 1, identifying which Czech products already exist in the Barentz master. Jurek: "this is the tricky part, this is the magic part." Splits into a deterministic half (supplier + product ID present → key match, "we don't need any AI") and a hard slice where only an 8-digit CN code or a product name remains. Field mapping (step 3) is **already solved** — he cut Ivo off on it. Do not pitch it.

**Unexplored lead worth a follow-up:** they resolve hard cases today by "opening certificates, comparing." Nobody followed up on the call. If those documents carry CAS/grade/concentration, this becomes extraction-plus-matching (Axion territory) rather than fuzzy name matching. Flagged as the key hypothesis in the email.

**Commercial gate, unchanged since May and still the single unknown:** Jurek's director must approve. "I provided the details presentation. I didn't receive the clear answer, but I believe we can start with a small POC." His own position: "in my opinion, we should start anyway." Deal stage logged Stage 3 SQL as of 28 May, **not verified since — assume stale.**

**Two timing constraints:** Jurek's SME colleague is off from 31 Jul for two weeks; Jurek himself goes away shortly. Next call 25 Aug.

**Next action:** chase the two extracts before Jurek leaves — Ivo, by 18 Aug. Nothing can run until they arrive. Worth asking Jordan in the sync whether the director gate gets pushed or left to drift to 25 Aug.

---

## 3. Platform-product (internal) — repo done, six decisions unsent

**Last week:** two calls settled the playground onboarding funnel — 28 Jul Playground Sync (four funnel decisions agreed) and 31 Jul Platform Next Steps (86 min; briefed Vova, escalated front-end analytics to a platform-wide epic, hit contested ground on the Projects & Applications epic). May–July meeting history backfilled. STATUS committed. **Repo side is done.**

**Six open questions drafted 31 Jul, none sent.** Each is one message. Highest priority:

- **Tell Liana the analytics will undercount.** Any tracker, self-hosted included, gets partially blocked by browsers and DNS filters — Vova demonstrated this live on the call. Fine for comparing campaigns against each other, not fine as absolute conversion figures. She has not been told. If she builds expectations on the first campaign report and later learns the figures were systematically low, that is a credibility problem created by omission.
- **Retract the session-video commitment** to Liana. Floated too quickly in Slack; needs Victor's security sign-off and has GDPR exposure (inbound EU leads). Event analytics is committable, video is not.
- **Who builds the magic-link token?** Vova asked verbatim and got "maybe we can make a quick story on that" — not an assignment. Vova is ready to build the front end; token generation is unowned.
- **Who owns the analytics requirements?** Vasco volunteered to write the epic; Ivo has been negotiating the metric list directly with Liana; Vankata's position is that product consumes the data first. These cut against each other — reconcile before the epic gets written twice.
- Plus: confirm the two activation/click definitions Ivo set unilaterally, and the expired-magic-link landing page (currently dumps users on a bare sign-in screen, lead lost silently).

**One thing to verify, not assume:** commit 0ee2d0e corrected the project object hierarchy ~10 min after the STATUS entry recording Vova contesting exactly that model. It may assert a model the 31 Jul call left open. Check before treating as settled.

---

## Dormant but gated — no movement last week

| Engagement | Last touched | Gate | Risk of drift |
|---|---|---|---|
| **Fresenius CMC** | 22 Jul | Two clean template-filled pairs ready (P.1 9/7/1, P.5.1 11/10/0). Weekly Wed 09:00 ET working session. Still owed by Sathya: particle-row-swap verification, P.5.4-vs-S.4.4 title confirm. €300K HubSpot deal, close 2026-09-30 | **Two weeks quiet on a Sept close.** Worth confirming the Wednesday cadence is still running |
| **Heyne Tillett Steel** | 10 Jul | HTS to pick one project and export its data. ETA was "end of next week or week after" — that window has passed | Free scoping PoC can't start. Chase Jonathan |
| **FedEx** | 15 Jul | Jordan owed Andrzej the presentation. Andrzej owed us the beachhead vertical | Both sides quiet three weeks after a call that ended well |

---

## Agenda candidates, ranked

1. **SimLab co-marketing / MoU / white-label with NVIDIA + HPE** — offered unprompted, no owner, no date. Needs Steven. Biggest unrealised item on the board.
2. **Barentz director gate** — unresolved since May, and the window closes as Jurek and his SME both go away. Jordan's call whether to force it.
3. **Fresenius CMC cadence** — €300K, Sept close, two weeks silent.
4. **Liana undercount disclosure** — internal, but a credibility problem that grows the longer it waits.
5. **HTS + FedEx chases** — both overdue, both cheap to restart.

## Unresolved

- GTC Berlin date — still not obtained. Everything about the keynote deliverable's timing depends on it.
- "Mark" (Valencia Chief Energy Infrastructure) — surname unknown, and he is the actual approver.
- Barentz HubSpot stage — logged 28 May, unverified since.
- Whether the Wed 09:00 ET Fresenius session ran on 29 Jul.
