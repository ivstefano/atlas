# Onboarding: Vasko

Welcome. This gets you up to speed on how IRIS.ai turns customer problems into delivered work, and how that feeds the
product. Read end-to-end before your first week.

It's weighted toward delivery and product: what we build, how engagements run, who does what, and what's live right now.
The commercial machinery appears here as context, because delivery constraints and pipeline reality drive product
decisions, but Jordan and Steven own customer commercials.

---

## 1. Products

Both are **in active development**, not GA. PoCs are delivered on top of the current build; expect shifting internals.

- **Axion**: data layer. Extracts, standardizes and indexes structured + unstructured data into a common format (**ODL
  **). Most PoCs exist because 85–91% of customer data lives here. Good Axion use case = extracting images, charts,
  tables, or consolidating data into one standard the customer can plug into internal systems.
- **Neuralith**: agentic orchestration on top of Axion. In practice **RAG with tools**, plus pipelines. Tools
  differentiate use cases:
    - *Yettel*: Neuralith calls a database to extract info.
    - *Heineken*: Neuralith pulls from Excel tables used like database tables to answer scenario questions.
    - Direction: pipelines of separate agents that gather, structure and answer. SQL-in-ingestion in progress so RAG can
      query structured data directly.
- **Platform / Playground**: being built now, and the most likely place you'll contribute product work. Today it bridges
  a gap: a link lets customers upload files, someone runs scoping with internal pipelines, results get presented back.
  Not automated end to end yet. That's the direction.

**RSpace**: earlier product, ≈150M research documents, R&D use cases. Neuralith is RSpace with a B2B interface over it.
Marketing is not pushing RSpace; don't position it to customers. Still shows up in older docs.

Positioning word: **"contextualization"** (replaced "unification").

### Demo environments (read carefully, this trips people up)

- **`neuralith-dev.iris.ai`**: current demo surface for Axion + Neuralith. This is what you show customers.
- **`axion-dev.iris.ai`**: legacy. Hardcoded RSpace copy built for a one-off presentation. Not dynamically generated,
  not maintained. Do not build on it.
- **Demo content** loads from a S3 in a specific format. Artifacts (PDFs, extracted tables, CSVs, images, charts) go in
  a `_artifacts` subfolder. Until content is loaded that way the demo looks like "a PDF viewer that highlights things."
- Access: ask Vova in `#neuralith`. Claude Teams account: ask Victor.

---

## 2. Product work in flight

### 2.1 Playground / Projects hierarchy

Agreed 23 Jul with Vankata + Michael (Dezea Studios). The object model:

```
Project
├── Dataset
│   └── File
│       └── Artifact        (per-file derived view)
└── Output / ODL            (ONE table across the whole dataset)
```

A Project holds a Dataset of Files; each File yields an Artifact. The **Output (ODL) hangs off the Project, not off any
File**: one table for the whole dataset, each File contributing one or more rows.

Downstream of the ODL there are two consumers today and one planned:

- **Client delivery**: full table, all columns, fed into their analytics
- **Playground view**: curated subset that tells a story
- **Reconstructed document** (future): text output rather than a table

Constraints from Vankata:

- Playground ODL view is a **showcase, not a tool**. No column manipulation. Wow moment on first screen.
- ODL schema is per-client. UI must be generic; columns/values surfaced per dataset are picked by hand.
- ODL preview reuses the **same component** as the existing artifact preview, different artifact type.
- Project request is one-time in V1. Editing means propagating changes mid-scoping, deferred.
- Playground -> Create Project is gated on payment; button may be hidden for unpaid users.

### 2.2 The two-pass onboarding upload flow

Being designed now. Pass 2 is a question set that sits next to the customer's uploaded files. Group A is factual (
languages, layout consistency, volume beyond the sample, where documents live today, where the project runs, what needs
clearing legally, whether the files are real or samples, whether a target schema exists). Group B is about the real job
rather than the ideal one (last manual instance, correct answer for one named uploaded file, hidden rules not printed on
the page, contradiction-resolution, who reviews and what counts as a mistake, whether ground truth exists anywhere, who
owns budget).
Why it matters to you: these are the questions that stall delivery when they surface three calls late. Pairing them with
uploaded files makes the customer discover their own gaps up front. If you build delivery tooling, build it assuming
these answers exist.

Document found here:
[https://docs.google.com/document/d/1qau1msrXFc_GyBFitic2eWv6qh3eDYYV](https://docs.google.com/document/d/1qau1msrXFc_GyBFitic2eWv6qh3eDYYV)

---

## 3. Engagement model of MVPs (formerly called PoC's)

The standard de-risked flow.

1. **Free scoping**: 1–2 weeks, 20–50 sample docs.
2. **Paid PoC**: 4–10 weeks, €25–50K, near-cost pricing.
3. **Full Implementation**: consumption-based.

PoC pricing = fixed setup (schema/config) + per-page/per-doc consumption. Compute is 90–95% of our cost, which is why
efficiency work in the pipeline is commercially real, not just engineering hygiene.

### What a scoping exercise is

Short, free, using the customer's real documents, to show concrete output: "here's what Axion extracts, here's what
Neuralith answers about it." The point is not abstract capability. It's a specific artifact that makes them say yes to a
paid PoC. The PoC is the door; scoping opens it.

Shape: intake (20–50 docs, confirm target output format first) -> pipeline run (OCR, table extraction, schema-driven
extraction, sometimes LLM Q&A) -> analysis (pick interesting extractions, note edge cases, measure approximate accuracy,
find one or two "wow" artifacts) -> presentation (their documents, side-by-side image/extracted views, proposed PoC
shape) -> handoff.

What it is **not**: not a free PoC (no production-grade accuracy or fine-tuning, say explicitly that fine-tuning happens
in the paid stage), not a product demo (they've seen the demo, this is *their* data), not exhaustive (showcase the best
files, you don't need to process everything they sent).

### What must exist before scoping starts

Sample documents (20-50, spanning messy edge cases), target output format, ground truth (how do we know it's right), a
named domain SME who answers within a week, a use case owner who can sign off scope.

If any are missing, flag it at kickoff. Don't silently work around it. That's how accounts die quietly.

### What makes a good IRIS-fit use case

Yes: unstructured data where manual effort is measurable in FTEs, schema can be defined, named internal owner exists,
regulated or high-volume industry, ROI framable as FTE-hours saved or risk reduced.

Push back: "magic" use cases with no schema or ground truth, no domain SME (dies in validation), customer wants a
product not a PoC, pure chat/search over already-clean structured data (not our edge), long legal cycles with no
technical champion.

---

## 4. Team

### Leadership

- **Victor Botev**: co-founder, CTO. Drops into senior customer calls. NDA signatory on some contracts.
- **Vankata**: CPO. Runs Product Sync. **Your main counterpart.** Senior technical voice on client calls; owns product
  direction and technical scope gating. Note: in transcripts "Vankata"/"Wanka"/"Venkata" is always Ivan Tsenov.

### Commercial (context, not your lane)

- **Jordan Ryken**: Principal Commercial Director. Runs discovery/qualification, owns customer commercials.
- **Steven Fung**: CRO, UK. Runs the weekly commercial call, "so what commercially" lens.
- **Liana Hakobyan**: Marketing lead, demo production.
- **Ada Kretkowska**: marketing comms; owns the official Iris.ai brand guide (source of truth for client-facing
  material; "Iris.ai" always lowercase-with-dot).

### Extract team

Builds the extraction pipeline behind Axion: OCR, text, tables, schema-driven extraction from complex documents. Core
engine most PoCs rely on.

- **Petar Ivanov**: team lead
- **Martin Kondov**: Aumovio parts extraction
- **Aleksandar Georgiev "Aleks"**: SMS Group extraction
- **Rosen Krumov**: extract / translation; also hosts the Qwen inference box
- **William Le Roux**, **Georgi**, **Irina**
- **Matyo**: ML scientist; ran the Chandra-2 / DocLayout-YOLO / vision extraction work

### RAG / Neuralith team

Agentic and retrieval layer: chat interfaces, scenario agents, retrieval over extracted data. Heineken is the flagship.

- **Borislava "Bobi" Bagaliyska**, **Nikolay "Niki"**, **Martina "Marti"**, **Ross** (QA)

### Platform team

Axion / Neuralith product surfaces, playground, marketplace. **The team your product work touches most.**

- **Yovcho**, **Vladi**, **Zhenya**, **Romek**, **Denis**
- **Vova (Volodymyr Krekhovetskyi)**: frontend / playground
- **Michael (Dezea Studio)**: external design agency on Playground + website

### Also

- **Ivo Stefanov**: solutions architect; runs the engagements. Your handover counterpart on delivery context.

**Main counterparts on delivery and product work:** Vankata (product direction), Petar (extract delivery), Bobi (RAG
delivery), Vova + dezea (Playground surfaces).

---

## 5. Cadences

| Meeting                      | When              | Who runs                         |
|------------------------------|-------------------|----------------------------------|
| Tech weekly sync             | Mon 10:00 - 10:30 | Rotation                         |
| Platform Design Sync         | Mon 10:30 - 11:30 | Vankata / Ivo                    |
| Weekly Commercial Fast Start | Mon 12:30 - 14:00 | Steven                           |
| Website Planning             | Mon 14:00 - 15:00 | Liana / Michael                  |
| Neuralith Sprint Planning    | Mon 16:00 - 17:00 | Yovcho                           |
| Weekly Product Sync          | Wed ~11:00        | Vankata / Ivo / secondary person |
| Extract Tool Sync            | weekly            | Someone from extract team        |
| Neuralith Sync               | daily             | Bobi / Marti / Yovcho            |
| All Hands                    | Friday            | Sara / Viktor / Others           |

---

## 6. Current pipeline (as of late Jul 2026)

Delivery-relevant view. Commercial detail lives in HubSpot and the pipeline tracker.

### Won / in delivery

| Account                            | State                                                   | Delivery notes                                                                                                                                                                                                                                                                                            |
|------------------------------------|---------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **SMS Group**                      | **WON ~3 Jul**, moving to full implementation           | Hydraulic schematic extraction, staged S1–S4. Aleks built; Petar leads. Vankata owns the deliverable, not Ivo. Gerald Mayr retires autumn 2026, Matthias Tarnow is continuity owner. Wed calls on Teams.                                                                                                  |
| **Aumovio** (Continental spin-off) | PoC delivered, near acceptance, awaiting their go/no-go | 100/100 corpus reviewed and sent 28 May. Phil declared PoC done his side. Extractor V2 (OCR-first) hit 99.6% F1 vs the older pipeline's 62.7% on the same docs. Decision was to show Bedrock + Opus results now, improve Qwen later.                                                                      |
| **Heineken**                       | PoC validated, production gate is price + IT access     | RAG build, 6 scenarios; Bobi, Niki, Marti, Ross QA. 11 Jun demo brought in two new senior stakeholders. Production needs real integrations (data changes multiple times/day, manual snapshots won't do). Proposal ~95–160k: integration one-time 5 sources at ~10–20k each, plus 45k/yr platform license. |

### Live scoping / pre-PoC

| Account                           | State                                                                                                                                                                                                                                                                                                   |
|-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Fresenius CMC**                 | Scoping, no PoC contracted. Regulatory submissions (eCTD Module 3). Demo + readiness dashboard built 11 Jun. Test is reconstruct-and-diff, not column counting. Weekly working session Wed 09:00 ET. Waiting on 3.2.S data.                                                                             |
| **Fresenius complaint-coding**    | Scoping. Second session 12 Jun locked three deliverables. Reframed by Vankata as ontology-from-examples then classify + spot-check, **not** extraction. Gate is the data handover (~100 input/output pairs, codes doc, remediation reports). ~8,000 complaints/mo NA, >100k files/yr. Build for recall. |
| **Garrett**                       | Pilot structure accepted 12 Jun. Design-reuse search over millions of drawings + design-standard compliance. Co-funded 6–10wk. Their in-house extraction is stuck ~70%, engineers need ~100%; our 95%+ is the whole justification. Awaiting NDA then real sample drawings.                              |
| **Deutsche Bahn (InfraGO)**       | Proposal delivered 15 Jun, engineer feedback positive, awaiting go/no-go. Interim sync 10 Jul.                                                                                                                                                                                                          |
| **SPIE**                          | Pre-scoping. Degraded-document preprocessing (perspective distortion, low contrast, stains) then OCR then agentic Q&A with source links. 100% Microsoft/Azure stack.                                                                                                                                    |
| **Heyne Tillett Steel**           | Intro / use-case call 10 Jul.                                                                                                                                                                                                                                                                           |
| **SimLab / Valencia Energy**      | Sync 24 Jul. Data-center end client.                                                                                                                                                                                                                                                                    |
| **Basamh**, **FedEx**, **Aramco** | Early, active.                                                                                                                                                                                                                                                                                          |

### Paused / waiting

**T&F (Taylor & Francis)** deferred to Sept 2026, client-side, not dead, **Nielsen** paused, summer resumption expected,
**Postbank** parked pending their internal reorg, **Daikin** intro no-show, reschedule pending, **Yettel** B2B chatbot
in production, cloud migration PoC in internal planning.

### Dead / lost

| Account                 | Reason                     | Lesson                                                  |
|-------------------------|----------------------------|---------------------------------------------------------|
| Agrolimen / GB Foods    | Went internal (15 May)     | Capable internal team + easy schema = they copy the PoC |
| GrantSpider             | Internal build             | Same pattern                                            |
| Orion Telekom           | Closed-lost                | Never showed up                                         |
| AlexFert (Egypt)        | Iran war, AI deprioritized | Don't over-invest in single-threaded accounts           |
| Aumovio Software Impact | Canceled internally        | Multi-workstream deals can lose the smaller track       |
| Shanghai Synocodes      | CCP investigation          | Geopolitical exposure is real                           |
| Stepan                  | Chose a competitor         | Miss their evaluation window, lose                      |

The delivery takeaway across the dead list: fast time-to-value in scoping, hard schemas customers can't trivially copy,
and SME relationships that survive political shifts.

---

## 7. Tools

- **Asana**: internal task tracking. Product work sits in `Iris.ai Product Roadmap`.
- **HubSpot**: source of truth for customer records, meetings, notes, files.
- **Tactiq**: auto-transcribes calls; transcripts land in each engagement's `transcripts/`.
- **IRIS AI Notetaker bot**: joins customer calls.
- **GDrive** (`Iris.ai - Everyone`): customer files, SoWs, proposals, demo content. Canonical source for engagement
  material.
- **Miro**: e.g. the Heineken board.
- **Slack**: `#neuralith` for demo/platform access, per-engagement Slack Connect channels with active PoC customers.

Repo layout you'll inherit context from: engagement content lives in `~/Documents/engagements/` (one folder per client:
CONTEXT / STATUS / COMMERCIAL / SOURCES / ARTEFACTS, with numbered stage folders). Operations, briefs and protocols live
in `~/Documents/atlas/`.

