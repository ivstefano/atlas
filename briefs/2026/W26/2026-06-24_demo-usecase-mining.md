---
date: 2026-06-24
type: analysis
trigger: Jordan demos-feedback call (24 Jun), action #1+#2 — mine customer calls for use cases, rank, map to capability buckets
corpus: 93 external client calls pulled from Tactiq (Dec 2025 - Jun 2026); 70 carried client use-case signal; 266 use-case mentions; 18 clients
method: per-transcript extraction (1 agent each) -> cluster/rank/dedup synthesis. Buckets are Jordan's framing (extraction / data-migration / intelligent-bpa / rag-knowledge-retrieval).
caveat: corpus = calls on Ivo's Tactiq account only. Coverage of reps' own-account recordings not verified.
---

# Demo use-case mining - client-call corpus (Dec 2025 - Jun 2026)

70 external client calls mined. 18 clients. Every use-case mention bucketed into Jordan's 4 capabilities (extraction,
data-migration, intelligent-bpa, rag-knowledge-retrieval).

## TL;DR

- **Most-requested capability: extraction.** It anchors nearly every engagement and shows up across ~16 of 18 clients.
  The repeat pattern: pull structured fields/devices/triples out of messy PDFs, drawings, contracts, specs, with source
  traceability, then trust it.
- **Biggest unserved gap: data-migration, exactly as Jordan flagged, we have NOTHING built.** It is the
  second-most-mentioned capability (cross-system unification, semantic layer, Salesforce-to-HubSpot, ODL over a
  lakehouse) and the highest executive relevance (Basamh, Aramco, Orion, HubSpot, Nielsen all framed it as the
  foundational layer). No demo asset exists. This is the largest frequency-times-value hole in the deck.
- **Clearest aha pattern: "I no longer have to read the document / chase the person."** Whether it is an SMS engineer
  hunting page 6700 of an E-plan, Justyna fielding the same budget question for the hundredth time, or a
  neuro-oncologist staring at 100k glioblastoma papers, the wow moment is always: ask in natural language, get the
  answer back grounded to source, skip the manual dig. Traceability-to-source is the trust unlock that converts the wow
  into a buy.

## Ranked recurring use cases

Clustered near-duplicates into themes. Ranked by frequency x business value (pain severity + executive relevance).

| Rank | Use case theme                                                                                                                 | Capability              | # clients           | Example clients                                                                                                                 | Business pain                                                                                                                                                | Why it excites (aha)                                                                                                                   |
|------|--------------------------------------------------------------------------------------------------------------------------------|-------------------------|---------------------|---------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| 1    | Extract structured fields/devices/values from messy PDFs, drawings, contracts, specs into a clean DB, with source traceability | extraction              | ~16                 | SMS Group, Aumovio, DB InfraGO, GB Foods/Affinity, Taylor & Francis, Alexfert, Stepan, GrantSpider, Shanghai Synocodes, Nielsen | Data locked in unstructured docs; manual read-and-key is the org bottleneck (Aumovio: 112 salespeople hand-typing; GB Foods: ~10k legacy specs)              | "It read the drawing with no fine-tuning" + click-to-source verification. Beats a 100% bar because manual baseline is worse.           |
| 2    | Cross-system data unification / operational data layer / semantic layer over structured + unstructured                         | data-migration          | ~10                 | Aramco, Basamh, Nielsen, Aumovio, SMS Group, FMCG conglomerate, Postbank                                                        | Every AI POC restarts data prep from scratch (Aramco: 2 years to unify; 200+ pending use cases); wrong answers when execs query unstructured-plus-structured | "Revenue by region returns a wrong answer today." Reusable base layer kills the duplication everyone hates. Highest exec relevance.    |
| 3    | Cross-discipline graph/model of a machine, query a device + all its relations in natural language                              | data-migration / rag    | 1 deep (many calls) | SMS Group (15+ calls)                                                                                                           | Machine knowledge only in senior engineers' heads; tags differ per discipline, nothing links; retires with staff (Gerald, autumn)                            | One queryable model: "show me which cylinder this valve controls" without touching the hydraulic sheet. Reuse cuts engineering 70-80%. |
| 4    | Narrative-to-code / spec-to-output consistency checking with flagging + suggestion + traceback                                 | intelligent-bpa         | 3                   | Fresenius, GB Foods/Affinity, Aumovio (code impact)                                                                             | Miscode means missed FDA-reportable event (30-day clock, CAPA in the hundreds of thousands); audit exposure                                                  | "AI corrects this to that, not just flags it" + traceback to canonical source. Regulated-industry auditability.                        |
| 5    | NL chatbot over internal finance/procurement/policy data, answers traceable, human-in-loop on uncertainty                      | rag-knowledge-retrieval | 5                   | Heineken, Postbank, Jordan Ahli Bank, Basamh, Nielsen                                                                           | Knowledge locked in one person (Justyna, Eustina ~2h/request); ~100 teams to consolidate into one unit serving 90k staff                                     | "It answered the same as I would have." Eustina: most exciting thing all year. Self-serve at scale = the business case.                |
| 6    | Auto-extract supplier/customer contract volumes + apply per-OEM business rules + flag discrepancies                            | extraction              | 1 deep (many calls) | Aumovio (8+ calls)                                                                                                              | Annual budget cycle bottleneck; ~5000 contracts; sales 4 months in, ~60-70% done by hand                                                                     | V3 matched expected values per OEM at >85% with no per-file tuning; "19 of 20 contracts come through automatically."                   |
| 7    | Vendor/supplier doc screening: extract then compare against internal specs + checklist, flag risks                             | intelligent-bpa         | 2                   | GB Foods/Affinity, Basamh (CoA)                                                                                                 | Two technicians manually translate + check supplier sheets; slow, costly, error-prone first screening                                                        | Matching went past binary relevant/not into argument-level comparison; pre-Ariba urgency.                                              |
| 8    | Source traceability: every extracted value links to exact page/coordinates for audit                                           | extraction              | 1 deep (many calls) | SMS Group, DB InfraGO, Taylor & Francis, Fresenius                                                                              | Engineers/auditors won't trust a black box                                                                                                                   | Click a cable, see the exact schematic page. Confidence labels (high/med/low/missing). Trust is the currency.                          |
| 9    | Knowledge graph from research literature: claim triples, provenance, cross-article evidence weighting                          | extraction / bpa        | 3                   | Taylor & Francis, NHS (glioblastoma), Shanghai Synocodes                                                                        | 100k+ papers no human can read; trust is the resale currency                                                                                                 | "Megawave effect": one strong study overrides many weak ones. Hypothesis generation, not summarization.                                |
| 10   | Agent drafts action/email, human approves, then it executes (PO checks, cross-charge, claims)                                  | intelligent-bpa         | 3                   | Heineken, Postbank, Orion                                                                                                       | Multi-system checks repeated per PO; tacit rules (100K contract rule) only in one head                                                                       | Approval-gated automation matched expectations; encodes business logic nobody wrote down.                                              |
| 11   | NL analytics agent over warehouse/Salesforce, charts/reports on demand, auto semantic layer                                    | data-migration / rag    | 4                   | Postbank, Nielsen, Basamh, Orascom                                                                                              | People won't open PowerBI; wait on highly-paid analysts, chase 10 people, often get no answer                                                                | "Looks magical." Democratize data access; quantifiable analyst-hours saved = easiest C-suite sell.                                     |
| 12   | Salesforce-to-HubSpot (and Dynamics/SAP) migration: introspect schema, map custom processes, HITL validate                     | data-migration          | 2                   | HubSpot, Postbank                                                                                                               | Migrations manual, slow, error-prone; custom objects + years of process                                                                                      | "Your product is the plumbing." Same engine retargets to Dynamics/SAP.                                                                 |
| 13   | On-prem / sovereign deployment of extraction + AI for regulated/sensitive data                                                 | extraction / bpa        | 4                   | Aramco, Orion (NIS), Jordan Ahli Bank, Basamh                                                                                   | Public-cloud-only vendors get killed late; data residency is table-stakes                                                                                    | Aramco: visibly relieved at on-prem confirmation, prior vendor died on this.                                                           |
| 14   | Reuse / fit-check past machine designs against new project requirements, generate modification tasks                           | rag / bpa               | 1 deep              | SMS Group                                                                                                                       | Reuse needs the right senior engineer or teams design from scratch                                                                                           | "This one fits 80%, here are the steps to 100%." Cuts new engineering work.                                                            |
| 15   | ESG / report auto-generation from ingested operational docs mapped to frameworks                                               | extraction / bpa        | 2                   | Orascom, Nielsen                                                                                                                | Manual consultant-heavy reporting; board mandate to scale without headcount                                                                                  | Boxed starting use case; Orascom asked for a shareable write-up for the CCO.                                                           |

## By capability bucket

### Extraction - ~16 clients. Demo asset: YES (ArcelorMittal).

Strongest example: SMS Group device extraction from E-plan/hydraulic PDFs with click-to-source page references; Aumovio
contract-volume extraction matching expected OEM values at >85% with no per-file tuning. Taylor & Francis called it "
very, very impressive." This is the proven core.
Status: covered. The ArcelorMittal asset transfers well (tables, figures, scanned/handwritten, traceability). Lowest
risk.

### Data-migration - ~10 clients (highest exec relevance). Demo asset: NONE. GAP.

Strongest example: Aramco (2-year data-unification pain, 200+ pending use cases, "data prep is the only part that
sucks"); Basamh ("build the same ODL concept on our platform"); HubSpot ("your product is the plumbing"). Also the
binding layer under every SMS cross-discipline ask and every Aumovio "join to controlling DB" ask.
Status: **the single biggest hole.** Second-most-mentioned, top in executive framing, zero demo. Jordan's claim holds.
Every discovery call with a CDO/CTO lands here and we have nothing to show.

### Intelligent-BPA - ~9 clients. Demo asset: MOCK-ONLY (SMS / Heineken).

Strongest example: Fresenius narrative-to-code consistency with traceback ("AI corrects this to that, not just flags
it") tied to FDA-reportable miss exposure; Heineken approval-gated PO automation. Stepan computational-chemistry ROI (
33x on test runs).
Status: mock-only is thin for the regulated/high-value asks. Fresenius and Stepan are high-value, high-pain, and a mock
undersells them. Needs a real flagging-plus-suggestion-plus-traceback demo.

### RAG / knowledge-retrieval - ~10 clients. Demo asset: WEAK (Yarrow chatbot).

Strongest example: Heineken finance chatbot (Eustina: "most exciting thing all year," agent answered same as the human);
Nielsen "democratize data access ... game changer." NHS glioblastoma hypothesis engine.
Status: weak asset vs strong, repeated demand. The Heineken/Nielsen NL-over-your-data story is a near-universal opener
and the current Yarrow demo underpowers it. Upgrade priority.

## Best verbatim quotes

- "Perfectly really, really excellent work. That's exactly what I was hoping for and that's the kind of presentation
  that I need to start my discussions with our engineers." - DB InfraGO (extraction)
- "Your product is the plumbing ... the infrastructure, the logic, and then you'll just put a UI on top of it ... the
  same engine retargets to Microsoft Dynamics/SAP." - HubSpot (data-migration)
- "The most amount of work that that project took was unifying data points across the world, and that alone took a good
  two years." - Aramco (data-migration)
- "It looks magical to people actually. And when our analytics folks heard that you can create this layer without heavy
  work on humans, they were very, very interested." - Postbank (data-migration / semantic layer)
- "I mentioned I'm bleeding out but someone misread that as the tubing is bleeding out, so now it doesn't get
  escalated ... there's a timeline for regulatory reportability." - Fresenius (intelligent-bpa)
- "The democratization of access to information ... even the least technically inclined person can just ask the database
  and it spits out accurate answers." - Nielsen (rag)
- "If you were to go to pubmed.gov and put glioblastoma, you get 100,000 papers, no human is going to be able to pass
  those." - NHS (rag / knowledge graph)
- "Now that it's cool. It's a real demo and not a movie." - SMS Group (extraction, live demo)
- "Nobody is extracting the contracts here internally at all ... a salesperson would sit manually and type it by hand in
  an Excel file." - Aumovio (extraction)
- "Yesterday I thought about you and about this assistant because I received so many questions and it took me so much
  time to find those data." - Heineken (rag)
- "They sprang on the fact that they're only on public clouds, and that just shut the whole thing down." - Aramco (
  on-prem, deal-breaker)

## Recommended demo build priority

1. **Data-migration / operational data layer demo (BUILD FIRST).** Second-most-mentioned, highest executive relevance,
   zero asset. Jordan's claim is supported by the data: Aramco, Basamh, HubSpot, Nielsen, Orion, FMCG conglomerate all
   lead here and we walk in empty. Build the "revenue-by-region returns a correct answer over structured + unstructured"
   story plus a Salesforce-to-HubSpot mapping flavor. Biggest gap-to-value ratio in the deck.
2. **Upgrade the RAG / NL-over-your-data demo.** ~10 clients, near-universal opener, current Yarrow asset is weak. The
   Heineken/Nielsen "ask in natural language, get the answer back, traceable, HITL on uncertainty" story converts on
   first contact. Highest frequency among the customer-facing asks.
3. **Real intelligent-BPA flagging-plus-suggestion-plus-traceback demo.** Replace the SMS/Heineken mock. Fresenius (
   FDA-reportable miss) and Stepan (33x ROI) are high-value, high-pain, regulated; a mock undersells them. Reusable
   across Fresenius, GB Foods, Heineken PO automation.
4. **Cross-discipline machine graph demo (SMS-specific, near-ready).** One deep account but 15+ calls and an active POC;
   the queryable graph plus click-to-source is largely built. Package it as a repeatable asset (it doubles as a
   data-migration proof point).
5. **Extraction: maintain, do not rebuild.** ArcelorMittal asset already lands ("real demo not a movie"). Add a
   contract-volume flavor (Aumovio) and a research-triples flavor (Taylor & Francis / NHS) only as targeted variants,
   not net-new build.

## Open questions (for the Vankata + Steven sense-check)

- Data-migration demo: synthetic data or anonymized client data (Basamh/Aramco want it on their own platform)?
- RAG upgrade: ship inside Teams (Heineken, Postbank repeatedly asked) or standalone for the demo?
- BPA demo target vertical first: Fresenius (regulated, highest pain) or Heineken (warmest, fastest)?
