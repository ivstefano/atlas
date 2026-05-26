# Pyloth deliverable pattern catalog

**Discovery date:** 2026-05-19
**Source:** ~/Documents/engagements/

## Method

Surveyed all 17 active and paused engagements in `/Users/iris/Documents/engagements/` (excluding 4 pure tombstones: alexfert, cetin, shanghai-synocodes, stepan). Read CONTEXT.md, STATUS.md, ARTEFACTS.md, SOURCES.md for each. Examined 2_scoping/ folders for concrete deliverable artifacts (HTML, JSON, PDFs, markdown). Patterns identified via evidence of actual use across 2+ engagements or clear reusability within a single engagement's output.

## Pattern index (19 patterns)

| # | Pattern ID | What it shows | Used by |
|---|---|---|---|
| 1 | `extraction-results-showcase` | Interactive HTML demo of structured outputs | DB, Garrett, Welocalize, Agrolimen, T&F, SMS Group |
| 2 | `extraction-json-bundle` | Structured JSON (findings, claims, entities, evidence) | T&F, DB, Agrolimen, Fresenius |
| 3 | `before-after-visual-comparison` | Source PDF vs extracted output (sliders, BBox overlays) | Welocalize, Garrett, DB, Agrolimen, SMS Group |
| 4 | `confidence-matrix` | Quality bands per doc/field (qualitative narrative) | Welocalize, Aumovio, T&F |
| 5 | `extraction-schema-json` | Canonical field definitions and ontology | DB, Agrolimen, Aumovio, T&F |
| 6 | `evidence-and-source-traceability` | Page refs + BBox + verbatim quote per fact | DB, Welocalize, T&F, Agrolimen, Fresenius |
| 7 | `multilingual-extraction` | Same schema regardless of source language | Garrett, Welocalize, Agrolimen, Aumovio |
| 8 | `relational-database-output` | Normalized queryable tables (with FKs) | DB, Agrolimen, Aumovio, T&F, Heineken |
| 9 | `accuracy-metrics` | F1/precision/recall, hallucination rate, batch curves | Aumovio, Welocalize, T&F |
| 10 | `domain-terminology-mapping` | Client-provided synonyms, aliases, multilingual variants | Fresenius, SMS Group, Aumovio |
| 11 | `multi-format-output` | HTML + Markdown + JSON + DOCX + CSV of same extraction | Welocalize, others |
| 12 | `form-and-table-preservation` | Checkboxes, strike-throughs, dense grids preserved | Welocalize, Aumovio |
| 13 | `document-classification` | Detect doc type (spec/invoice/contract) before extraction | Agrolimen, Aumovio |
| 14 | `cross-document-entity-linking` | Same entity across multiple docs with different IDs | SMS Group, Aumovio, Heineken, DB |
| 15 | `qa-report` | Failure-mode audit, coverage analysis, SoW gates | Welocalize, Agrolimen, Aumovio |
| 16 | `domain-prompts-and-rules` | Custom LLM instructions per domain (rules, validation) | All scoping engagements |
| 17 | `agent-query-interface` | NL → SQL + tree navigation + locate-on-PDF | SMS Group, Postbank, Heineken |
| 18 | `figure-classification` | Diagram/chart/table/photo/schematic detection | Garrett, DB |
| 19 | `cost-breakdown` | Token burn, compute time, per-doc cost | Fresenius, Heineken, Postbank |

## Pattern library (ranked by recurrence and clarity)

### `extraction-results-showcase` — Interactive HTML demo of structured outputs

**What it shows:** A self-contained, browser-viewable single-page app showcasing extraction results from a sample of client documents. Typically tabbed or scrollable, showing before/after (source PDF + extracted structured output side-by-side), with filterable tables, BBox overlays, or document-specific detail views.

**Inputs needed:** 
- Extraction pipeline outputs (JSON, CSV, markdown per document)
- Sample PDFs or images from the source corpus
- Schema/field definitions
- Page-level metadata (page numbers, section names, confidence scores)

**Engagements that used it:** Deutschebahn (showcase.html, S3-hosted, 84MB embedded), Garrett (garrett_showcase_v2/v3.html, 5-10MB, multiple iterations), Welocalize (welocalize_ocr_demo.html, 20MB, multi-page form comparisons), Agrolimen (standalone.html in 2_scoping, embeds PDFs + extraction data), T&F (HTML viewer in deliverable/, page-by-page JSON viewer), SMS Group (planned for May 20 demo, tree-view + locate-on-PDF UI)

**Canonical example:** `/Users/iris/Documents/engagements/deutschebahn/2_scoping/extraction/data/output/showcase.html` (S3 deploy reference; local build gitignored). Walkthrough script: `STORY.md`.

**Eligibility rule:** 
- Extraction is visual/document-heavy (PDFs, scanned forms, technical drawings, patents).
- Client needs to evaluate coverage (is every page processed?) and accuracy (does the output match the source visually?).
- Sample size is manageable enough to embed (20-100 documents; larger corpora require filtering or pagination).

**Notes:** 
- Often paired with a STORY.md walkthrough script and a DEMO_RECAP for the presentation.
- Can be single-page or tabbed (Garrett = 5 tabs; Deutschebahn = buckets + relational + summary tabs; Welocalize = per-doc before/after sliders).
- S3 hosting for large files (>20MB) is common; git-gitignore smaller ones.
- Requires custom CSS/JS per use case (no universal template yet).

---

### `extraction-json-bundle` — Structured JSON outputs (findings, claims, entities, evidence)

**What it shows:** Machine-readable extraction outputs in JSON format, organized by document, entity type, or relationship. Typically includes document metadata, extracted records/triples/tuples, confidence scores, evidence citations (with page/bbox references), and aggregated views.

**Inputs needed:**
- Extraction pipeline JSON outputs (per-document extractions)
- Schema definition (field names, types, required/optional)
- Evidence citations with source page/bbox/quote
- Document metadata (source file, language, processing date)

**Engagements that used it:** 
- T&F: `findings_pdf.json` (4,491 grounded findings from 50 articles; structured RankedClaims + URI linking), `ranked_claims.json` (~4.8MB, cross-document aggregated triples)
- Deutschebahn: `buckets.json` (46KB, confidence-bucketed extraction), `relational_db.json` (395KB, per-field relational output), `evidence_bbox.json` (203KB, page+bbox citations)
- Agrolimen: relational_db.json per document, match reports
- Fresenius: `.iris.json` per paper (title/authors/journal/chunks with Q&A-prefixed retrieval text + RAG context), `metadata.json` (study type, patient count, devices, parameters measured)

**Canonical example:** `/Users/iris/Documents/engagements/tandf/2_scoping/deliverable/ranked_claims.json` (URI-linked knowledge graph triples). `/Users/iris/Documents/engagements/deutschebahn/2_scoping/extraction/data/output/relational_db.json` (database-normalized per-field extraction).

**Eligibility rule:**
- Structured data extraction (not OCR text blobs).
- Client has a defined schema or wants one derived from the data.
- Evidence traceability is important (client may want to verify by re-reading source).

**Notes:**
- T&F extends the input schema: adds `magnitude` (raw_text / treatment_value / control_value / unit / p_value), `strength_score` (0-1 Bayesian blend of evidence volume + rigor + consistency).
- Deutschebahn uses buckets to group extraction confidence: "confidently_extractable" / "needs_poc_discovery" / "cannot_extract" + evidence samples.
- Fresenius wraps extracted chunks with `Q: ...? Q: ...?` prefixes to bias downstream RAG retrieval.
- Large files (>50MB) live in Drive; smaller ones can live in repo.

---

### `before-after-visual-comparison` — Side-by-side document source vs extracted output

**What it shows:** Rendered comparison of a source PDF/document and its extracted/structured form (HTML table, CSV, database record, diagram annotation). May include BBox overlays on the source highlighting extracted regions, or sliders to toggle between source and output.

**Inputs needed:**
- Source document images/PDFs (page renders, screenshots, or low-res pages)
- Extracted output (HTML table, CSV row, JSON record, annotated diagram)
- Document-level or page-level alignment (which output row came from which page)
- Optional: BBox coordinates for visualization

**Engagements that used it:**
- Welocalize: before/after sliders on form pages (ZH bilingual form hero: preserved strike-through on date), per-document before/after PDFs
- Garrett: combined_showcase (BBox overlays on catalog pages showing detected elements: tables, figures, diagrams, text blocks), page-by-page side-by-side renders
- Deutschebahn: layout-detected BBox overlays (showcase embeds bbox-annotated page PNGs)
- Agrolimen: Document Explorer in standalone.html (three wildly different source PDFs → identical English schema output)
- SMS Group: tree-view interface showing device in context, "locate on PDF" button to jump to the drawing

**Canonical example:** `/Users/iris/Documents/engagements/welocalize/2_scoping/TALKING_SCRIPT.md` (demo walkthrough of slider interface showing before/after for the ZH form).

**Eligibility rule:**
- Client evaluates extraction by visual inspection (does it match the source page-by-page?).
- Document layout / visual structure is load-bearing (forms, diagrams, tables, multilingual text preservation).
- Sample size is small enough to render (5-50 pages; larger = paginated viewer or summary samples).

**Notes:**
- Welocalize's hero use case is the ZH bilingual form with the preserved strike-through on the overwritten date field (shows that structure-aware OCR + correction-tracking works).
- Garrett uses this to show "full catalog coverage" — every page processed, nothing hand-labelled, all blocks classified.
- SMS Group uses "locate on PDF" as a search feature: NL query → device found in tree → show me where on the original drawing (jumps to page + highlights).
- BBox overlays require normalized coordinates (0-1000 per axis; Garrett uses this; so does Deutschebahn).

---

### `confidence-matrix` — Multi-dimensional assessment of extraction quality per document/parameter

**What it shows:** A tabular or graphical assessment of extraction readiness across documents and parameters: e.g., confidence scores (% correct per field or per document), difficulty (easy/good/needs-tuning/below-threshold), or feature coverage (what works / what fails / what needs domain tuning).

**Inputs needed:**
- Per-document extraction results
- Ground truth or SME evaluation (if available)
- Grouping variables (document type, parameter type, language, complexity)
- Scoring method (F1 / accuracy / subjective confidence band)

**Engagements that used it:**
- Welocalize: 7-document ranking (ZH ~98%, DE1 ~95%, DE2 ~92%, FR1 "good with caveats" ~84%, TH1/KO1 "need-tuning", TH2 "below-threshold")
- Aumovio: batch-by-batch improvement tracking (V1→V2→V3 showing % correct per priority field; hallucination rates per run; final 10-doc eval set)
- T&F: coverage report (XML vs PDF per-article yield, predicate distribution, diversity-vs-depth note, % findings with structured magnitude)

**Canonical example:** `/Users/iris/Documents/engagements/welocalize/2_scoping/TALKING_SCRIPT.md` (ranking by fidelity; honest about failure modes).

**Eligibility rule:**
- Multiple documents/samples exist in the deliverable.
- Client needs to understand quality variance (which documents work best, which parameters are hard).
- Honesty about failure modes is valued (Welocalize explicitly includes a blurred low-DPI scan that hallucinates; flags it below-threshold).

**Notes:**
- Welocalize's framing: rank by fidelity, show the hard case (TH2 below-threshold), recommend DPI/quality-SLA in any pilot SoW.
- Aumovio's framing: show improvement curve batch-to-batch, curate the eval set for optics ("directional improvement" story).
- Helps manage client expectations and positions extraction as a domain-tuning problem, not a "buy a black box" problem.

---

### `extraction-schema-json` — Canonical field definitions and ontology

**What it shows:** Machine-readable definition of what fields/entities/relationships to extract, their types, required/optional status, constraints, and (often) natural-language descriptions.

**Inputs needed:**
- Client domain knowledge (what fields matter, what the valid values are, business rules)
- Extraction output samples (to infer structure if not pre-defined)
- Multilingual entity names (if applicable)

**Engagements that used it:**
- Deutschebahn: `schema.json` (CTMS ontology: 14-15 data objects + possible attributes per object)
- Agrolimen: `schema.json` (Patricia's 14-table relational design: specification_identity, identity_sensory, technical_properties, etc.)
- Aumovio: `schema.json` (fields: final customer, project title, product group, SOP/EOP dates, flex %, lifetime volume, yearly volumes, plus unit-conversion logic)
- SMS Group: `Devices.xlsx` device-type ontology, `PCM.xlsx` Plant Breakdown Structure (hierarchical codes, WBS mapping)

**Canonical example:** `/Users/iris/Documents/engagements/deutschebahn/2_scoping/extraction/schema.json`.

**Eligibility rule:**
- Extraction targets a well-defined domain (rail operations, food specs, automotive contracts, steel plants).
- Client has existing database/schema or will provide one.
- Field-level accuracy is measurable (F1, precision/recall, "is this value correct?").

**Notes:**
- Deutschebahn's schema is "not very exact, the result of a research meeting" — subject to refinement during PoC.
- Agrolimen: "the schema is the contract" — Patricia explicitly wants the database normalized to her design, not a generic CSV.
- Aumovio: business rules embedded in schema (unit conversions, parts-per-vehicle multipliers, which table row is source of truth).
- Typically JSON or Excel; v1 often hand-written by the client, v2+ refined from extracted data.

---

### `evidence-and-source-traceability` — Page references, BBox coordinates, quotes for every extracted fact

**What it shows:** For every extracted value/claim/finding, the source page number, bounding-box coordinates, and verbatim quote from the source document.

**Inputs needed:**
- PDF or document with page structure (page numbers, geometry)
- Extracted value + source location (page, bbox, character offsets)
- Verbatim quote verification (LLM judge: "is this quote a substring of the source text?")

**Engagements that used it:**
- Deutschebahn: `evidence_bbox.json` (per-extraction page+bbox citations, 96.6% value-in-source LLM-judge audit n=815)
- T&F: every triple has `evidence` fields (source document, section, verbatim quote; LLM validates that quote is a substring)
- Welocalize: HTML output carries `data-bbox` region coordinates and `data-label` block types for QA reviewers to spot-check
- Aumovio: final extraction row includes source-doc reference so Phil can verify
- SMS Group: tree-view UI shows device on the hydraulic schematic + mechanical drawing; "locate on PDF" jumps to that page

**Canonical example:** `/Users/iris/Documents/engagements/deutschebahn/2_scoping/extraction/data/output/evidence_bbox.json` (203KB, per-field bbox + page citations).

**Eligibility rule:**
- Client needs to audit extraction accuracy (especially in regulated industries: healthcare, finance, pharma, food safety).
- Source documents are visual (PDFs, scans, technical drawings) where position matters.
- Hallucination risk is high (LLM-based extraction without grounding).

**Notes:**
- Deutschebahn's groundedness audit found 96.6% of extracted values are verifiable in source (3.4% false positives, valuable for risk assessment).
- T&F's "no ungrounded outputs" rule: every triple validated as a verbatim quote or dropped.
- Welocalize's HTML + bboxes allow QA reviewers who don't read the language to see what was extracted from where.
- Coordinates can be normalized (0-1000 per axis, Garrett style) or absolute (pixel offsets, Deutschebahn style).

---

### `multilingual-extraction` — Same schema output across languages

**What it shows:** A single, language-agnostic schema applied to documents in multiple languages (German, French, Spanish, Chinese, Thai, Korean), with the output structurally identical regardless of source language.

**Inputs needed:**
- Multilingual source documents (PDFs, forms, patents, contracts in 2+ languages)
- Schema definition (language-independent field names and types)
- Translation or language-aware NLP (for proper noun / medical term handling)
- Per-language model or unified multimodal model

**Engagements that used it:**
- Garrett: multilingual patents (French, German, Spanish originals → identical English output structure, figure numbers + reference numerals + dimensions preserved)
- Welocalize: 5-language adverse-event forms (DE, FR, KO, TH, ZH) → same HTML/Markdown/JSON structure per page, with English-translation tooltip for QA reviewers
- Agrolimen: supplier specs in ES/IT/FR/DE + internal specs in EN → all normalized to English schema
- Aumovio: ~9 Chinese-OEM contracts through translation pre-step (V5 includes one Chinese contract end-to-end)

**Canonical example:** `/Users/iris/Documents/engagements/garrett/2_scoping/_axion_archive/patent-extractions/{DE69827504T2_DE,EP1301689B1_FR,ES2320343T3_ES}/translated/` (per-patent translated English outputs, identical JSON to the original-language runs).

**Eligibility rule:**
- Client has multilingual documents as a routine operational challenge.
- No per-language fine-tuning or hand-labelling is acceptable (must be generic + guided).
- Language is not the barrier; the *structure* (tables, forms, diagrams) is consistent across languages.

**Notes:**
- Garrett: "language is no longer a wall between your incoming spec and your component library" is the headline pitch.
- Welocalize: same pipeline for all 7 docs, 5 languages, no per-language model. Adding a 6th language = "hours not weeks" (sample for validation).
- Agrolimen: format normalization (different section orders, old vs new internal formats, external supplier chaos) + language normalization in one pass.
- Multi-language is often a *stretch goal* in MVP (Aumovio positioned it as a later translation phase; SMS Group English-only for the PoC).
- **Mechanism varies by engagement:** Garrett used Chandra 2 vLLM (extract in original language) + GPT-4.1 translation as a second pass, preserving figure numbers and reference numerals. Welocalize extracted in original language + added English-translation tooltip for QA (not translating the form itself). Agrolimen normalized to English schema in one pass. Aumovio puts translation on the critical path for Chinese OEMs (COMET ≥ 0.80 PoC metric).
- **COMET** (Conditional On Matching Entity Types) is the metric to use for translation quality where domain terms matter — BLEU/ROUGE miss whether technical terms stay correct.

---

### `relational-database-output` — Normalized, queryable table structure (CSV or JSON)

**What it shows:** Extraction results normalized into database tables (one row per record, columns = fields, proper join keys across tables).

**Inputs needed:**
- Extraction schema with relationships (one-to-many: e.g., a machine has many devices)
- Extracted records per document
- Join keys (IDs that link records across tables)
- Denormalized-vs-normalized trade-off decision

**Engagements that used it:**
- Deutschebahn: `relational_db.json` (per-document, per-object, per-attribute; relational shape)
- Aumovio: contract-volumes table (one row per project × product × part-number, yearly volumes 2018-2034, business-rule-converted units)
- Agrolimen: 14-15 tables (specification_identity, technical_properties, allergens, etc.) matching Patricia's schema
- T&F: `findings.json` + `ranked_claims.json` (both quasi-relational: Findings = rows with article/section/practice/outcome; RankedClaims = aggregated cross-document triples with strength scores)
- Heineken: Excel workbooks (MAIN, Tracker, Zycus, PO Dump, MEC reports) unified into a queryable DB for the agent

**Canonical example:** `/Users/iris/Documents/engagements/deutschebahn/2_scoping/extraction/data/output/relational_db.json`.

**Eligibility rule:**
- Output needs to be queryable or joined with other tables.
- Client has a relational database or Excel workflow downstream.
- One-to-many relationships exist (e.g., a machine has N devices, each device has M properties).

**Notes:**
- Deutschebahn: normalized to allow querying "which electrified tracks use train-control PZB90?"
- Aumovio: business rules in the schema (unit conversions, vehicle→parts multipliers, weeks-per-year per OEM).
- Agrolimen: "the schema is the contract" — structure is contractually binding; Patricia validates every field.
- Denormalization trade-off: T&F's `ranked_claims.json` keeps cross-document aggregated rows flat (not normalized) for easy RAG retrieval.

---

### `accuracy-metrics` — Per-field F1/precision/recall, hallucination rates, coverage

**What it shows:** Quantitative assessment of extraction quality: F1 scores or precision/recall per field, hallucination rate (% false values), coverage (% of documents/fields extracted vs missing), and per-batch improvement curves.

**Inputs needed:**
- Ground truth (SME-validated reference extraction on a sample)
- Extraction output on the same sample
- Per-field scoring (is the value correct? partially correct? hallucinated?)
- Batch-to-batch comparison (showing improvement over iterations)

**Engagements that used it:**
- Aumovio: target metrics (F1 ≥ 0.92 priority fields / 0.88 others; table-row recall ≥ 0.95; OCR WER ≤ 7%; ODL-mapping ≥ 0.90). Actual: V1→V2→V3 showing % correct per batch, hallucination rate per run, improvement curve.
- Deutschebahn: 96.6% value-in-source (LLM-judge audit n=815); 815 extracted values, 3.4% false positives.
- Garrett: No explicit F1 metrics in the deliverable (Liviu says "we never ran the benchmark"), but figure-classification counts are reported.
- T&F: No labeled data yet (precision/recall to be measured in the PoC with SME spot-check + labeled ground truth).
- Welocalize: no formal metrics, but per-doc confidence bands (ZH ~98%, FR1 ~84%) and concrete failure examples (TH2 blurred = below-threshold).

**Canonical example:** `/Users/iris/Documents/engagements/aumovio/4_poc/eval/week-reports/week5-V5_VS_V6_FINAL_REPORT.md` (per-field improvement, hallucination postprocessor recommendation).

**Eligibility rule:**
- Quality gates exist (client has explicit acceptance criteria: "must hit 90% F1").
- PoC or MVP phase (need to measure progress across iterations).
- Procurement evaluation (client will hold extraction against stated quality targets).

**Notes:**
- Aumovio: metrics are IRIS-originated from the Sept 2025 proposal (not in the signed Nov 2025 SoW), so procurement may hold them. Internal bar: "directional improvement + credible path to implementation".
- Welocalize: honesty about failure modes is the pitch ("this TH2 scan is below-threshold; we recommend >=300 DPI hard gate").
- Metrics can be curated (choose the 10 best documents for the eval-deliver to hit the numbers) — Aumovio does this.
- For Axion-heavy engagements (Deutschebahn, Aumovio, Agrolimen), F1 per-field is standard. For RAG/hybrid (Heineken, Postbank), metrics are "does the agent answer the question correctly" (more subjective).

---

### `domain-terminology-mapping` — Custom lexicons for implicit knowledge (drug names, OEM codes, abbreviations)

**What it shows:** Structured mappings of synonymous terms, abbreviations, brand names ↔ generic names, legacy codes ↔ new codes, so extraction can handle terminology variance without per-language fine-tuning.

**Inputs needed:**
- Domain abbreviations and synonyms (GLP-1-RA / Mounjaro / semaglutide / tirzepatide; ESA / EPO; RRT / dialysis; YVH code / PE## tag)
- Client-provided equivalence lists or inferred from the corpus
- Personalization rules (different researcher, different subset of papers, different terminology preference)

**Engagements that used it:**
- Fresenius: `SYNONYMS` map in config (HDF/HD/ESA/TSAT/CKD/ESKD/GLP-1-RA expansions); Andreas flagged "can the system handle synonymous expressions and add a personalized 'dictionary'".
- Aumovio: OEM-specific weeks-per-year table (Ford 42 avg / 45 max; varies by OEM and region), product → segment/product-group → parts-per-vehicle mapping.
- SMS Group: old/legacy tag + new IEC 81346 PE## tag on every device; yVH codes ↔ PE## tag mapping; normalized tag separator convention.
- Garrett: figure-type classification vocabulary (compressor map, spec table, dimensional drawing, performance chart, product photo, cutaway, ...).
- Heineken: implicit L-code join (universal join key linking MAIN / Tracker / Zycus / PO Dump); vendor-name fuzzy matching ("Elucidat" in MAIN = "Insight Enterprises Netherlands B.V." in MEC).

**Canonical example:** `/Users/iris/Documents/engagements/fresenius/2_scoping/extraction/config.py` (`SYNONYMS` map). `/Users/iris/Documents/engagements/sms-group/2_scoping/_axion_archive/SMS_GROUP_EXTRACTION_TEMPLATE.md` (legacy-to-new tag mapping).

**Eligibility rule:**
- Domain has high terminology variance (multiple names for the same thing, legacy vs new naming schemes).
- Client cannot afford per-instance hand-labelling.
- Implicit knowledge (brand name → active ingredient, abbreviation → full term) is important for downstream use.

**Notes:**
- Fresenius: wants a personalized "dictionary" so different researchers can have different terminology preferences.
- Aumovio: weeks-per-year is client-supplied (Phil's hand-curated table); parts-per-vehicle is a product-type lookup.
- SMS Group: device-type ontology in `Devices.xlsx` (MuK code → tag prefix → RoleClass path).
- Synonyms are often domain-specific rules (not generalizable across industries) and need client input to define.

---

### `multi-format-output` — Multiple serializations of the same extraction (HTML, Markdown, JSON, DOCX, CSV)

**What it shows:** The same extraction delivered in multiple formats for different downstream uses: HTML (web display), Markdown (versioning + diffing), JSON (programmatic + RAG), DOCX (human review), CSV (Excel).

**Inputs needed:**
- Unified extraction in an interchange format (JSON or intermediate representation)
- Format-specific serializers (HTML builder, Markdown renderer, DOCX templater, CSV exporter)
- Per-page and per-document aggregation (single files per document, plus a global index)

**Engagements that used it:**
- Welocalize: per-doc extraction (HTML, Markdown, JSON, DOCX, TXT) + per-page versions in all 5 formats; XTM ingestion requires HTML/DOCX, so both are built
- Agrolimen: per-doc relational_db.json + summary.csv + match report
- T&F: per-article + aggregate JSON (findings_xml.json / findings_pdf.json + ranked_claims.json) + HTML viewer; PDF XML mapping for matching
- Deutschebahn: buckets.json + relational_db.json + summary.csv + evidence_bbox.json (all queryable views of the same extraction)
- Fresenius: per-paper .iris.json (title/authors/journal/chunks) + metadata.json (study type / patient count / devices / parameters) + all_questions.json / extracted_entities.json (aggregated)

**Canonical example:** `/Users/iris/Documents/engagements/welocalize/2_scoping/extraction/sample-extraction-output/` (Markdown samples showing the output shape).

**Eligibility rule:**
- Output needs to be used in multiple workflows (web UI, batch processing, human review, system ingestion).
- Downstream systems have different input requirements (XTM wants HTML/DOCX; Excel wants CSV; vector DB wants JSON).
- Serialization complexity is acceptable (multi-format pipelines add engineering effort).

**Notes:**
- Welocalize: the multi-format output *plus* a usable human-in-the-loop editor wired into XTM is the differentiator, not just the OCR.
- Deutschebahn: buckets (confidence grouping) is a useful grouping for downstream tools; relational_db is the full normalized form; summary.csv is for quick spot-checks.
- T&F: per-article JSON is the archival form; aggregate JSON is for cross-document queries; HTML viewer is for stakeholder review.
- Format-specific: Welocalize needs DOCX for human review in Word; T&F's viewers need HTML; Aumovio needs Excel; all need JSON for programmatic use.

---

_(merged with `multilingual-extraction` above — both describe the same multilingual pattern, the former being the "outcome" framing and the latter the "mechanism." The pipeline details (translate-then-extract vs extract-in-English) and the COMET metric are absorbed into the canonical pattern's Notes.)_

---

### `form-and-table-preservation` — Detect form structure, preserve checkboxes, strike-throughs, dense grids

**What it shows:** Extraction that recognizes form layouts (checkboxes, radio buttons, text fields, dense multi-column grids), captures checkbox states, preserves corrections (strike-through + corrected value), and outputs as structured HTML with semantic block labels.

**Inputs needed:**
- Scanned forms or form PDFs (often handwritten, low DPI, faded photocopies)
- OCR + layout detection (pdfplumber, Chandra, DocLayout-YOLO, or similar)
- Checkbox and correction-state detection (model-specific or rule-based)
- HTML/Markdown output with `data-label` block types (Form, Header, Footer, Footnote)

**Engagements that used it:**
- Welocalize: adverse-event / biovigilance forms (DE veterinary form with 3-column layout + checkbox states; ZH bilingual form with overwritten date showing both struck and corrected value in output)
- Heineken: Excel workbooks with cell comments (institutional memory captured as metadata)
- SMS Group: Dense multi-column outcome/severity matrices on Thai + Korean forms (table-alignment drift flagged as "needs per-template tuning")

**Canonical example:** `/Users/iris/Documents/engagements/welocalize/2_scoping/extraction/sample-extraction-output/` (Markdown outputs with `data-bbox` + `data-label` showing extracted structure). Welocalize TALKING_SCRIPT.md (ZH hero: "the struck-through date shows structure-aware OCR + correction tracking").

**Eligibility rule:**
- Source documents are scanned forms or handwritten content (not machine-printed clean PDFs).
- Form structure (checkboxes, tables, grids) carries semantic meaning that must be preserved.
- Client audits extraction visually (can spot a mis-mapped checkbox or a strike-through that wasn't captured).
- High fidelity is a regulatory requirement (pharmacovigilance, medical records).

**Notes:**
- Welocalize's hero: ZH form with strike-through date (overwritten correction) shows extraction captured both values. Score ~98%.
- Checkbox states must be extracted (checked / unchecked / partially filled), not just the field name.
- Dense-grid alignment drift is a known hard problem (TH1/KO1 forms in Welocalize need per-template tuning; SMS Group's outcome matrices need cell-splitting logic).
- Low DPI is a data-quality problem, not an extraction problem (Welocalize recommends >=300 DPI hard gate; TH2 below-threshold is the concrete case).

---

### `document-classification` — Detect document type (spec vs invoice vs contract) before extraction

**What it shows:** A classification step that identifies document type before extraction, routing to the right schema/rules. E.g., "this PDF is an internal spec in the new format" vs "this is a legacy spec in Spanish" vs "this is an external supplier TDS".

**Inputs needed:**
- Sample documents labeled by type (training set, even small)
- Feature extraction (text, layout, metadata)
- Classification model (LLM-based or ML classifier)
- Per-type extraction rules/schemas

**Engagements that used it:**
- Agrolimen: `step2_classify_extract.py` classifies each PDF as GB Foods internal master spec (old or new format) vs supplier TDS; routes to the right extraction schema
- SMS Group: classification to internal-spec vs vendor-doc (files pre-named by type, but system still learns to classify)
- Heineken: implicit classification of Excel sheets by role (MAIN = master file, Tracker = operational tracker, Zycus = contracts register, etc.)
- Fresenius: implicit classification of papers by study type (RCT / observational / review / case report) — extracted in metadata.json

**Canonical example:** `/Users/iris/Documents/engagements/agrolimen/2_scoping/extraction/step2_classify_extract.py`.

**Eligibility rule:**
- Multiple document types exist in the corpus (not all the same schema).
- Document type determines schema / extraction rules (different fields per type).
- Type can be inferred from content/layout (not always pre-labeled by the client).

**Notes:**
- Agrolimen: classification is step 1 of the pipeline (classify → extract-with-right-rules → match-to-master-spec).
- SMS Group: pre-classification by filename, but system learns to classify for robustness.
- Fresenius: study-type classification embedded in the metadata extraction (same LLM call extracts both).
- Classification quality feeds downstream extraction quality (misclassify a supplier spec as internal → extraction fails or uses wrong schema).

---

### `cross-document-entity-linking` — Link same device/entity across multiple documents with different identifiers

**What it shows:** A deduplication + linking step that recognizes the same physical entity (device, supplier, contract) appearing under different names/codes in different documents, and unifies them under a canonical ID.

**Inputs needed:**
- Extracted entities from multiple documents (each with local identifiers)
- Similarity scoring (string distance, semantic, context-based)
- Canonical identifier strategy (pick one source, generate new)
- Confidence scoring (is this link certain or uncertain?)

**Engagements that used it:**
- SMS Group: same hydraulic valve appears as MuK tag in functional view, YVH code in hydraulic schematics, PLC address tag in electrical docs; system links all three to the same device node. Cross-discipline linking without explicit mapping is the "core gotcha".
- Aumovio: same OEM contract referenced by HNK number (Zycus), project name (Tracker), and SAP order (PO Dump); joins are partial both ways (some services have no Zycus contract, some Zycus contracts not in MAIN).
- Deutschebahn: same operating point documented in BeBu, Streckenbuch, and ESTW; extraction matches fields (track attributes, electrification, etc.) to the right ontology entities.
- Heineken: vendor name fuzzy matching ("Elucidat" in MAIN = "Insight Enterprises Netherlands B.V." in MEC).

**Canonical example:** `/Users/iris/Documents/engagements/sms-group/2_scoping/_axion_archive/SMS_GROUP_EXTRACTION_TEMPLATE.md` (cross-discipline linking challenge in brief). `/Users/iris/Documents/engagements/sms-group/4_poc/SHARED_FILES_LEGEND.md` (file legend + cross-linking rules).

**Eligibility rule:**
- Multiple document sources exist (not a single unified export).
- Same entity appears with different identifiers across sources (no explicit join key provided by the client).
- Deterministic linking is possible (strong context clues, or client can pre-label a sample).

**Notes:**
- SMS Group: legacy data with no cross-document identifiers is explicitly *out of scope*. PoC uses newer data with PE## + SAP codes.
- Aumovio: partial join keys (HNK appears on multiple contract amendments; matching is fuzzy on vendor name).
- Fallback for hard cases: suggest matches + human confirmation (SMS Group approach for cases where automatic linking fails).
- Linking confidence can be scored and flagged for review.

---

### `qa-report` — Extraction quality audit, failure modes, coverage analysis

**What it shows:** A narrative report (Markdown or PDF) summarizing the scoping/PoC results: what works, what fails, what needs domain tuning, what's out of scope, and honest limitations.

**Inputs needed:**
- Extraction results on a sample
- SME feedback or ground truth (if available)
- Failure-mode analysis (which documents/fields are hard, why?)
- Coverage analysis (% of corpus processed, % of fields extracted)

**Engagements that used it:**
- Welocalize: TALKING_SCRIPT.md (per-doc talking points, failure modes, >=300 DPI recommendation, next-steps asks)
- Aumovio: `week-reports/week5-V5_VS_V6_FINAL_REPORT.md` (per-field improvement, hallucination postprocessor recommendation, V5 fix-list)
- T&F: `corpus_summary.md` (per-journal yield, predicate distribution, quality signals, diversity-vs-depth note), `ontology_gaps.md`, `coverage_report.md`
- Deutschebahn: `DEMO_RECAP_2026-05-15.md` (recap of the May 15 demo to Hannah), `email_to_hannah_2026-05-15.md` (deliverable email with key findings)
- SMS Group: `POC_WRAPPING.md` (locked remaining scope for the final weeks + items needed from client)

**Canonical example:** `/Users/iris/Documents/engagements/welocalize/2_scoping/TALKING_SCRIPT.md` (the honesty is the pitch: TH2 is below-threshold; we recommend >=300 DPI).

**Eligibility rule:**
- Scoping or PoC phase (not just a finished product demo).
- Client wants to understand failure modes and next steps (not "here's the finished thing, ship it").
- Regulatory/compliance context (client's team reviews quality with accountability).

**Notes:**
- Welocalize: honesty about the blurred low-DPI scan (hallucinations, below-threshold) is trust-building, not trust-destroying.
- Aumovio: directional improvement narrative (V1→V2→V3 shows learning curve; extrapolate to full implementation).
- The QA report is often the main deliverable in scoping; the extraction outputs are secondary.

---

### `domain-prompts-and-rules` — Custom LLM instructions per domain (extraction rules, field definitions, validation rules)

**What it shows:** Detailed prompts and system rules that guide the extraction model to focus on domain-specific constraints: field definitions, business logic, forbidden values, citation requirements, etc.

**Inputs needed:**
- Domain expertise (what the fields mean, what values are valid, what the business rules are)
- Extraction schema (field names, types, constraints)
- Error cases (examples of what NOT to extract)
- LLM model choice (GPT-4o, GPT-4.1, Gemma-4, etc.)

**Engagements that used it:**
- Aumovio: "business rules, in Bulgarian" in week-reports (unit conversions, parts-per-vehicle multipliers, which table row is source of truth, what to ignore)
- Fresenius: medical-domain extraction checklist (forces exact copying of patient counts, parameter values with units, stats, treatment parameters, device/dialyzer names)
- T&F: "no ungrounded outputs" rule (every triple must be a verbatim quote or dropped); strength_score calibration (Bayesian blend of evidence volume, rigor, consistency)
- Deutschebahn: "80% solution with no hallucinations" framing (confidence bucketing: confidently_extractable / needs_poc_discovery / cannot_extract)

**Canonical example:** `/Users/iris/Documents/engagements/aumovio/4_poc/eval/QUESTIONS.md` (the full scoping-question list with Phil's answers = the de-facto ODL spec / business rules).

**Eligibility rule:**
- Extraction targets a well-defined domain with specific rules (not free-form text summarization).
- Field definitions are clear and enforceable (can be written as LLM instructions).
- Hallucination risk is high (client needs explicit "don't guess" rules).

**Notes:**
- Aumovio: business rules evolve during the PoC; V1 rules are refined based on Phil's feedback.
- Fresenius: medical-domain synonyms + forced-exact-copy rules for numbers/units are baked into `config.py`.
- T&F: "no ungrounded outputs" is enforced via an LLM judge that validates every triple as a substring.
- Rules are often domain-specific and not reusable across industries (unlike the schema pattern itself).

---

### `agent-query-interface` — Natural-language question answering + SQL generation + tree-view navigation

**What it shows:** A user-facing agent or app that lets users ask questions in natural language ("which devices need power?", "show me all valves on the hydraulic circuit", "which contracts cover remote installation?") and returns structured answers (table, tree, SQL query, or JSON).

**Inputs needed:**
- Structured data layer (relational DB, knowledge graph, or vector DB + retriever)
- Agent framework (Claude, LangChain, MCP, etc.)
- Question-answering rules specific to the domain
- UI/UX (chat, tree-view, forms, etc.)

**Engagements that used it:**
- Heineken: Neuralith RAG agent (`heineken-dev.iris.ai`, Justyna got a login Apr 24) answering vendor PO lookups, contract status, budget-vs-actuals, missing-invoice detection; human-in-the-loop email-draft demo planned
- SMS Group: Claude-Code-style agent (tree-view + NL query interface + "locate on PDF") for the May 20 demo; user asks in plain language, agent returns filterable table + Excel export + "show me on the drawing"
- Postbank: Neuralith unified-demo app (synthetic SFMC dataset, custom ingestion agents, test cases, SFMC workflow for "Campaign Triage & Segment Builder")
- T&F: (not delivered yet; HTML viewer is the deliverable; real agent query interface is future)

**Canonical example:** `/Users/iris/Documents/engagements/heineken/4_poc/datastore-context/` (human-readable datastore description + glossary + agent guidelines). SMS Group demo (May 20, locked; tree-view + NL queries + locate-on-PDF).

**Eligibility rule:**
- End users need to ask ad-hoc questions against structured data.
- Questions vary in complexity (simple lookups, cross-source joins, aggregations, math).
- Deterministic answers are required (no hallucinations; "proof result, not like ChatGPT").

**Notes:**
- Heineken: the three named capabilities are (1) cross-source data ingestion, (2) human-in-the-loop learning (agent improves from corrections), (3) auditability (trace which data informed each conclusion).
- SMS Group: "deterministic, verifiable answers, presented like magic" — user doesn't see the plumbing, just the result.
- Postbank: two output modes (business-user = graph+table+explanation+verification; Campaign Ops = copy-paste-ready SQL query).
- Agent is often the client's first experience with a "working" system; UX/trust matters as much as accuracy.

---

### `figure-classification` — Detect figure types (diagram, chart, table, photo, schematic, drawing) and extract semantics

**What it shows:** Classification and extraction that recognizes figures in documents (compressor maps, dimensional drawings, wiring schematics, organ system diagrams, etc.) and extracts structured data from them (x/y axis values, component IDs, connections, measurements).

**Inputs needed:**
- Labeled examples of figure types in the domain
- Figure-specific extraction rules (how to read a compressor map vs a wiring diagram)
- Multimodal model (e.g., GPT-4o vision, Chandra, or DocLayout-YOLO)
- Domain ontology for figure types

**Engagements that used it:**
- Garrett: 739 figure crops classified into turbo-specific types (compressor map, spec table, dimensional drawing, performance chart, product photo, cutaway, ...). Compressor-map reading: structured numerical fields (model, HP range, peak efficiency %, max mass flow, etc.) pulled from chart imagery itself, not surrounding text.
- SMS Group: hydraulic schematics (detect valves/cylinders/pressure instruments, their IDs, connections between them, link IDs back to MuK tags); EPLAN electrical pages (which device IDs appear on which pages)
- T&F: charts extracted with "semantic understanding"; image-derived content is low-priority (prone to hallucination)
- Welocalize: (not explicitly; forms have diagrams but extraction is structure-focused, not figure-semantic)

**Canonical example:** `/Users/iris/Documents/engagements/garrett/2_scoping/_axion_archive/catalog-extraction/showcase/layout_results.json` (DocLayout-YOLO + GPT-4o-vision figure classification).

**Eligibility rule:**
- Technical documents with figures that carry semantic meaning (not just illustrations).
- Figure extraction is load-bearing for downstream use (client needs the compressor-map numbers, not just the photo).
- Figure types are domain-specific and need custom rules (can't use a generic chart reader).

**Notes:**
- Garrett: "row in a database out of an image, not a vector out of an image" is the pitch.
- SMS Group: hydraulic schematic parsing requires understanding connection patterns (pressure line, tank line, pilot line) — standard vision models don't do this without domain guidance.
- T&F: image-derived content is a known hard problem; recommended as out of scope for MVP.
- Requires multimodal LLM or specialized vision model (Chandra, DocLayout-YOLO, or GPT-4o vision).

---

### `cost-breakdown` — Pricing transparency (token burn, compute time, margin)

**What it shows:** A detailed cost model showing how much it costs to extract/query per document, per query, or per batch, broken down by model (GPT-4o vs Gemma), compute (GPU, inference time), and storage.

**Inputs needed:**
- Token counts (input tokens per doc, output tokens per extraction)
- Model pricing (GPT-4o $/1K tokens, etc.)
- Compute costs (GPU hours, inference latency)
- Batch size (economies of scale as corpus grows)

**Engagements that used it:**
- Fresenius: cost-per-document figure extrapolatable to 1000-2000 papers and ~500-SOP deployment; Gerome wants "no surprises" for the leadership-team pitch
- T&F: "cost at cost" (~€25-75k co-funded PoC depending on scope); Jordan guesses ~€50k
- Heineken: token spend vs manual FTE cost (Lucy needs the math to work)
- Postbank: ~€40k co-funded PoC (IRIS co-funding makes net-negative on PoC — Viktor signed off contingent on clear expansion path)

**Canonical example:** `/Users/iris/Documents/engagements/fresenius/2_scoping/PLAN.md` (cost estimate ~$2–10 on gpt-4o-mini per document).

**Eligibility rule:**
- Client has a cost sensitivity or ROI check (especially if they're evaluating IRIS vs building internally).
- Economies of scale matter (cost per doc drops with volume; Postbank scales from retail banking to enterprise data warehouse).
- Budget approval is contingent on price transparency.

**Notes:**
- Fresenius: Gerome's ROI math is "doing them in-house is positive because labour is cheap; shifting to IRIS only works if setup isn't per-use-case".
- Heineken: token spend must be <FTE cost for the deal to work (Justyna's salary is the hurdle rate).
- Postbank: co-funding a PoC makes it net-negative; the expansion story must show path to profitability.
- Costs should be transparent, not hidden in a vendor contract ("no surprises" for Fresenius, "trustworthy answers in audit context" for Postbank).

---

## Engagement appendix

### deutschebahn

**Source types:**
- German rail operational documents (Betriebsstellenbuch / route books / ESTW documents) in Word/PDF
- ~7 sample documents (BeBu, Streckenbuch, ESTW) provided for scoping extraction
- German, single company, consistent terminology across regions (though regional authors have individual styles)

**Promised extraction:**
Extract operationally relevant facts (track attributes, electrification, signalling/train-control standards, platform lengths, weight/gauge restrictions, gradients, mileage points, switch/track topology) from BeBu/Streckenbuch documents into a structured database for routing/dispatching algorithms. 80-90% coverage acceptable (missing/uncertain 20% flagged, not hallucinated).

**Artifacts found:**
- `2_scoping/extraction/data/output/showcase.html` (S3-hosted, 84MB, embedded page renders + extraction results)
- `2_scoping/extraction/data/output/buckets.json` (46KB, confidence-bucketed extraction: confidently_extractable / needs_poc_discovery / cannot_extract)
- `2_scoping/extraction/data/output/relational_db.json` (395KB, per-field relational extraction)
- `2_scoping/extraction/data/output/summary.csv` (2.7KB, per-doc summary)
- `2_scoping/extraction/data/output/evidence_bbox.json` (203KB, page+bbox citations for 815 extracted values, 96.6% LLM-judge validation)
- `2_scoping/STORY.md`, `DEMO_RECAP_2026-05-15.md`, `email_to_hannah_2026-05-15.md` (walkthrough + recap)

**Patterns used:**
- extraction-results-showcase (showcase.html, S3-hosted)
- extraction-json-bundle (buckets.json, relational_db.json, evidence_bbox.json)
- relational-database-output (structured per-field output)
- evidence-and-source-traceability (page+bbox+quote validation at 96.6%)
- extraction-schema-json (CTMS ontology, ~14-15 data objects)
- accuracy-metrics (LLM-judge audit n=815, 96.6% value-in-source)
- qa-report (DEMO_RECAP, email summary)

**Specific things worth noting:**
- "80% with no hallucinations" is the acceptance bar (safety-first for rail operations).
- Demo was 2026-05-15; results sent 2026-05-16 via S3 hosted link (code `DBInfraGO-Axion-2026`).
- CTMS ontology is "not very exact" — refinement expected during PoC.
- Soft-rule sections (control-system config, shunting rules) are natural-language fields, not fully structured.
- Signed NDA (DocuSign, Hannah Richta, ~2026-04-21); CTO's inbox only, not yet uploaded to Drive.

---

### garrett

**Source types:**
- 144-page public Garrett Performance Catalog 2025 (PDF, 26MB)
- 3 multilingual patents (French, German, Spanish; public)
- ~10 other public demo PDFs (Garrett/Honeywell patents, BorgWarner guide, Turbosmart schematics; curated for relevance)

**Promised extraction:**
Demonstrate full-document-understanding pipeline (layout detection, table extraction, chart/diagram comprehension, multilingual text) on technical PDFs to show extraction quality superior to Garrett's own internal 97% matcher on broader use cases (cross-document reasoning, semantic linking, multilingual invariance). Not expected to beat the narrow matcher on its own benchmarks.

**Artifacts found:**
- `2_scoping/STORY_v3.md`, `STORY.md` (walkthrough scripts for v2 and v3 showcases)
- `2_scoping/PLAN.md` (6-phase pipeline: doc selection → chandra extraction → docLayout-YOLO → figures → combined showcase)
- `2_scoping/demo-documents.md` (per-document "why Garrett" rationale)
- `2_scoping/_axion_archive/catalog-extraction/` (Chandra 2 .txt + .xml per doc, table extractions, combined-showcase BBox PDFs — binaries gitignored)
- `2_scoping/_axion_archive/patent-extractions/{DE,FR,ES}/` (per-patent Chandra + translated outputs)
- Drive: `garrett_showcase_v2.html` (v2, 10MB), `garrett_showcase_v3.html` (v3, 5MB + 5-tab layout)

**Patterns used:**
- extraction-results-showcase (garrett_showcase_v3.html, 5-tab, 20MB for full delivery including multilingual patents)
- before-after-visual-comparison (BBox overlays on pages, side-by-side catalog pages + extracted elements)
- multilingual-extraction (French/German/Spanish patents → identical English structure)
- multilingual-extraction-translation-pipeline (per-patent translation, figure numbers + reference numerals preserved)
- figure-classification (compressor maps, spec tables, dimensional drawings, performance charts, product photos, cutaways — 739 figure crops)
- qa-report (STORY_v3.md as the demo script, demo-documents.md as the rationale)

**Specific things worth noting:**
- Liviu said "increased their trust" post-demo; mildly disappointed there was no turbo-schematic / 2D-drawing demo (that's MVP-stage work).
- Showcase was presented 2026-05-07; next call 2026-05-19 for commercial discussion.
- Honesty framing is critical: "we didn't run your 97% benchmark, don't claim to beat it, this is different capability (semantic linking, multilingual invariance)."
- Chandra 2 vLLM run was on AWS GPU (g5.2xlarge, eu-central-1); stopped after extraction.
- Multilingual patents used for hero demo; full Garrett catalog was the breadth case (all 144 pages processed).

---

### welocalize

**Source types:**
- 7 scanned adverse-event / biovigilance forms in 5 languages (DE x2, FR, KO, TH x2, ZH bilingual)
- 9 pages total, handwritten, checkboxes, dense grids, strike-throughs, faded photocopies
- Fabricated with fake data by Welo's Gerard Alseda on real Bayer-style templates

**Promised extraction:**
Structure-aware extraction (preserving form tables, checkbox states, strike-throughs + corrected values) + translation, output in multiple formats (HTML, Markdown, JSON, DOCX, plain text) per page and per document. Demonstrate multilingual handling with no per-language tuning.

**Artifacts found:**
- `2_scoping/welocalize_ocr_demo.html` (20MB self-contained HTML demo, kept in Axion per client request)
- `2_scoping/extraction/build.py` (demo builder; DOCS list at top has per-doc scores, issues, file mappings)
- `2_scoping/TALKING_SCRIPT.md` (20-25 min walkthrough: framing, per-doc points, next-steps asks, anticipated Q&A)
- `2_scoping/extraction/sample-extraction-output/` (Markdown samples showing output shape)
- Drive: `Welocalize - Scoping Results/` folder (output zip with full HTML demo)

**Patterns used:**
- extraction-results-showcase (welocalize_ocr_demo.html, hero before/after sliders on ZH form with strike-through)
- before-after-visual-comparison (per-doc before/after PDFs showing extracted structure)
- form-and-table-preservation (checkbox states, strike-throughs with both values, dense grids)
- multilingual-extraction (same pipeline for all 7 docs, 5 languages, no per-language tuning)
- extraction-json-bundle (per-page HTML/JSON/MD outputs with data-bbox + data-label)
- confidence-matrix (7-doc ranking: ZH ~98%, DE1 ~95%, FR1 ~84%, TH2 below-threshold)
- qa-report (TALKING_SCRIPT.md: honesty about TH2, >=300 DPI recommendation)
- multi-format-output (5 formats per page: HTML, Markdown, JSON, DOCX, TXT)

**Specific things worth noting:**
- Scoping results presented 2026-04-30; Welo reaction: "looks very promising."
- Output files sent 2026-05-05 (while Ivo on PTO, Vankata sent by Vankata).
- Awaiting Welo's next-steps decision since 2026-05-05 (~8 days at migration date).
- Hero case is ZH form: bilingual EN/ZH, handwriting throughout, overwritten/corrected year on signature date, preserved in extraction.
- TH2 (blurred low-DPI) is flagged below-threshold; used as concrete case for >=300 DPI SLA recommendation in any pilot.
- Downstream workflow: output into XTM (ingests HTML/DOCX) for their CAT tool; multi-format output critical because XTM ≠ JSON.
- Multi-user editor wired into XTM (edits flow back for retraining) is the differentiator in a paid pilot, not just OCR layer.

---

### aumovio

**Source types:**
- ~100 OEM contracts (nomination letters, sourcing agreements, purchase contracts, quotes) from diverse OEMs (BMW, Ford, PSA/Stellantis, Renault, VW/Audi, GM, Honda, Hyundai, Volvo, Chinese OEMs, Cummins, etc.)
- Predominantly English + German, ~9 Chinese-OEM docs (later translation phase)
- Machine-printed PDFs (fine for OCR) + some image-only / scanned pages + dense embedded image tables (Honda volume table = image on page 1)
- Organized by product segment: ASC (air suspension), WBS (brakes), PSS (sensors)

**Promised extraction:**
Extract contracted parts-volume data (which OEM, which vehicle program, which part, how many parts/year, production window, flex range) into a harmonised Aumovio template, with unit conversions (weekly→annual per OEM weeks/year factors) and parts-per-vehicle multipliers baked in. Output: one row per project × product × part-number with final customer, project title, product group, SOP/EOP dates, flex %, lifetime volume, yearly volumes.

**Artifacts found:**
- `4_poc/eval/extractor/schema.json` (field definitions, business rules)
- `4_poc/eval/week-reports/` (week-by-week eval reports; week5 = final comparison V6 baseline + V5 fix-list)
- `4_poc/eval/QUESTIONS.md` (full scoping-question list with Phil's answers = de-facto ODL spec)
- `3_contracting/contracts/Aumovio SOW.md` (signed Nov 2025 SoW; numeric metrics in Sept 2025 proposal, not SoW)
- Drive: extraction-week4/5/6/7 (outputs + comparison sheets)

**Patterns used:**
- relational-database-output (contract-volumes table, rows = project × product × part)
- extraction-schema-json (field definitions + business rules in schema.json)
- accuracy-metrics (target: F1 ≥0.92 priority / 0.88 others; table-row recall ≥0.95; actual: V1~30%→V2~90%, batch improvement curve)
- domain-terminology-mapping (OEM-specific weeks/year, parts-per-vehicle multipliers, unit conversions)
- document-classification (NL / VFax / VED / eNA / F1 / F3 / CPA / PC prefixes route to right extraction rules)
- cross-document-entity-linking (same contract / OEM / project ID appearing across nomination letters, POs, quotes; partial join keys on HNK number)
- qa-report (week-reports, POC_WRAPPING.md with locked scope + items needed from Phil)
- domain-prompts-and-rules ("business rules, in Bulgarian"; unit conversions, parts-per-vehicle, source-of-truth rules)

**Specific things worth noting:**
- PoC running long (10 weeks nominally, ~17 actual as of mid-May); extension agreed late April.
- Phil's manual 11-doc ground-truth review arrived morning of May 13 call; blue (might be wrong) / yellow (wrong) markups drove V5 fix-list.
- V5 fixes: multi-pass self-check, caliper/TPMS mapping, partial-year + EOP-from-lifetime, CW-notation date parsing, flex-rate extraction.
- Close target: first week of June 2026 (eval-deliver + commercial next steps).
- File exchange via MOVEit (friction: Norbert relay, 30-day auto-expiry, no Phil access); May 13 decision to move off MoveIT to S3 / secure Aumovio account post-PoC.
- Procurement will check SoW's explicit requirements (signed Nov 2025 SoW doesn't have numeric thresholds — those are IRIS Sept 2025 proposal, so metrics are IRIS-originated, not client-imposed).
- Metrics are curated for optics (batch 1 ~30%→~90%; batch 2 starting at X, improving same way; extrapolate to full implementation).

---

### tandf

**Source types:**
- 50 academic articles (publisher PDFs) in pharma (25, journals: IDDI, IDMR, KCAM, KCBT, KCCY) and agri/food (25, journals: CFAI, GAGS, LJFP, TJLS, WSFR)
- 50 JATS XML equivalents of the same articles
- Open-access content (scoping use case only; not reusable beyond pilot testing)
- 2-column scientific layout, figures, tables, chemical formulas, image-derived content

**Promised extraction:**
Predicate-triple extraction (practice → effect → outcome) with ontology linking (SNOMED-CT, MeSH, NCIt), strength-of-evidence scoring (0-1 Bayesian), evidence citation validation (verbatim quote or dropped), cross-document aggregation by concept URIs. Demonstrate PDF extraction at XML quality.

**Artifacts found:**
- `2_scoping/PLAN.md` (full 16-phase implementation plan and run log)
- `2_scoping/deliverable/README.md`, `STORY.md` (demo script), `coverage_report.md`, `corpus_summary.md` (per-journal yield, predicate distribution)
- `2_scoping/deliverable/schema_extension_spec.md` (what IRIS added to Paolo's Finding model), `ontology_gaps.md`
- `2_scoping/deliverable/*.json` (cross_section_summary, ontology_gaps, pdf_xml_mapping, aggregation_stats_uri)
- Large JSON (findings, ranked_claims, uri_cache) + HTML viewer in Axion
- `2_scoping/extraction/` (~25 Python files: parse_jats, chandra_extract, uri_linking, aggregate_findings, build_viewer, etc.)

**Patterns used:**
- extraction-results-showcase (HTML viewer for 50 articles, page-by-page JSON viewer)
- extraction-json-bundle (findings_xml.json ~12MB, findings_pdf.json ~8.6MB, ranked_claims.json ~4.8MB, uri_cache.json ~2MB)
- evidence-and-source-traceability (every triple has verbatim quote, LLM-validated as substring of source)
- accuracy-metrics (no labeled data yet; recall-tuned; 4,491 findings from XML, 3,718 from PDF; PDF/XML ratio ~0.83)
- figure-classification (figures extracted with "semantic understanding"; image-derived = low-priority)
- qa-report (coverage_report.md, ontology_gaps.md, open_questions_email.md)
- confidence-matrix (per-journal yield, predicate distribution, ~23% unique terms mapped to ontology)

**Specific things worth noting:**
- Scoping presented 2026-05-12; Paolo's reaction: "increased trust"; moved straight to scoping a paid PoC.
- Recall-first framing ("false negative > false positive"); on 05-12 call Paolo caught a case where a p-value was picked up 3 sentences away (may not be related) — magnitude-field structure added to separate effect-size from significance.
- Table findings cited from citations ("Martin et al...") are excluded (not the paper's own finding).
- Cross-section evidence (methods↔results) on ~60% of XML findings; diversity not depth (only 1 practice recurs across articles).
- T&F already building internally, so IRIS's pitch is "different capability" (semantic linking, multilingual invariance, documented evidence) not "faster" or "better on your 97% matcher."
- Ontology bootstrapped from 12 pharma relations (UMLS Semantic Network) + FoodOn for agri; real run needs T&F's official lists (SNOMED-CT, MeSH, NCIt).

---

### agrolimen

**Source types:**
- 47 PDFs (scoping batch): 38 Test + 9 Train
- Mix: GB Foods internal master specs (15 fixed sections, current format; legacy format in Spanish) + external supplier technical sheets from dozens of suppliers in EN/IT/ES/FR/DE
- Three heterogeneous document types; no standard layout across suppliers
- ~4,000–6,000 internal raw-material specs in production (raw materials only, not packaging)

**Promised extraction:**
Classify each document (internal master vs legacy vs supplier), extract all fields into 14-15 table relational schema (normalised to English), match supplier specs to GB Foods internal masters (same base ingredient in multiple processing states: fresh / frozen / chopped / dehydrated / powder / grilled). Output: PLM-ready, queryable relational database.

**Artifacts found:**
- `2_scoping/SCOPING_PRESENTATION.md` (Apr 7 results-presentation script)
- `2_scoping/AIM.md` (document-type analysis from Mar 27 call + 26 screenshots)
- `2_scoping/extraction/schema.json` (14 tables, Patricia's relational design)
- `2_scoping/_axion_archive/standalone.html` (Document Explorer with embedded PDFs + extraction data; left in Axion)
- Drive: "Scoping pilot" folder (original client files)
- Axion: `_extractor/presentation/standalone.html` (the deliverable), `_extractor/data/ocr/extracted/matched/output/` (extraction outputs, binaries deleted after migration)

**Patterns used:**
- extraction-results-showcase (standalone.html in Document Explorer format, shows three wildly different source PDFs → identical English schema output as hero)
- before-after-visual-comparison (AIM.md document-type analysis with screenshots, Normalization Story)
- document-classification (classify internal master vs legacy vs supplier → apply right schema)
- cross-document-entity-linking (supplier spec → GB Foods internal master via matching, basil test case with near-misses)
- relational-database-output (14-15 table relational schema, Patricia's design)
- extraction-schema-json (Patricia's 14-table schema, field definitions, allergen/contaminant lists)
- extraction-json-bundle (extracted records per document, match reports)
- qa-report (SCOPING_PRESENTATION.md, AIM.md with challenges + matching confidence thresholds)
- accuracy-metrics (Patricia: 75–80% confidence threshold for matching, HIGH/MEDIUM/LOW/NO-MATCH bands, adjustable in evaluation)

**Specific things worth noting:**
- Scoping pilot ran end of March 2026 (47 PDFs, ~147 pages); results presented Apr 7 to Patricia + Núria.
- Two workstreams: (1) spec-extraction PoC ("Digitization MVP", 10w / 100 docs / 50K EUR), (2) vendor-onboarding MVP (scoping in progress, ~40K, 14w, success-based phase-gate).
- Apr 24: Patricia narrowed MVP scope to internal specs only (defer external/supplier specs to later project).
- May 8: Patricia floated simplifying the schema for vendor-onboarding MVP.
- **CLOSED-LOST 2026-05-15**: Patricia emailed Jordan going internal with a team already running other AI initiatives.
- NDA in place (mutual, Agrolimen template, signed before scoping); SAP→S/4HANA migration change freeze makes large extract awkward.
- Compliance is high-stakes (label claims, allergen declarations legally binding).
- Patricia: "prefer to prioritize quality… we're not in a hurry" — two-to-three months to launch PoC is fine.

---

### sms-group

**Source types:**
- Side Trimmer engineering documentation (a motorised steel-strip-edge-cutting machine):
  - **Functional**: MuK master component list (Excel, 8.5MB; ~2,300+ device rows for entire PLTCM plant, Side Trimmer rows ~2,300+; both old/legacy + new IEC 81346 PE## tags)
  - **Mechanical**: BOM (Excel + PDF), ~11 engineering drawings (.dwg + .pdf), bilingual DE/EN
  - **Hydraulic**: BOM (Excel + PDF), ~150 circuit drawings (.pdf + .dwg), valve schematics with old tagging system (YVH codes)
  - **Pneumatic**: BOM + schematics (similar structure)
  - **Electrical**: Full EPLAN documentation (280MB ~7,500 pages total plant; Side Trimmer extract ~1.2MB), Excel exports (parts list, interconnect diagram, signal list), PLC I/O mapping
  - **Functional descriptions**: Word documents (operational behaviour, strip-width adjustment, safety measures)
  - **3D CAD**: Creo XML export (full assembly tree)
  - **Ontology**: `Devices.xlsx` (device-type → RoleClass mapping), `PCM.xlsx` (Plant Breakdown Structure), `GraphSchema_FunctionalModel.vsdx`

**Promised extraction:**
Transform heterogeneous engineering docs into a single queryable description of the Side Trimmer: list devices, cross-reference across disciplines (MuK tag ↔ hydraulic YVH code ↔ EPLAN PLC address), parse hydraulic schematics + EPLAN pages, expose through tree-view UI + NL query interface + "locate on PDF" feature.

**Artifacts found:**
- `4_poc/POC_WRAPPING.md` (May 7 wrap-up, locked remaining scope)
- `4_poc/SHARED_FILES_LEGEND.md` (file legend, cross-linking rules)
- `2_scoping/_axion_archive/` (scoping outputs, table-extractor pipeline code)
- `_legacy/POC_SCOPING_PROPOSAL.md`, `SMS_GROUP_EXTRACTION_TEMPLATE.md`, `SMS_AIM_ACHIEVABILITY_AND_TBD.md`
- Drive: `Commercial/Account Management /SMS Group/PoC/Shared Files/` (all source documents, binaries)
- Demo (locked May 20 2026, 09:30 to Gerald + Matthias): tree-view, NL queries, Excel export, locate-on-PDF

**Patterns used:**
- extraction-results-showcase (tree-view UI + NL query interface + locate-on-PDF demo May 20)
- before-after-visual-comparison (locate-on-PDF: device found in tree → show on original drawing)
- relational-database-output (one graph database, one common data pool, every object once, multiple views)
- cross-document-entity-linking (same device = MuK tag + old YVH code + EPLAN PLC address; linking without explicit mapping, core gotcha)
- figure-classification (hydraulic schematics: detect valves/cylinders/pressure instruments + connections, link IDs back to MuK)
- agent-query-interface (Claude-Code-style agent: NL questions → tree-view + filterable table + Excel export)
- extraction-schema-json (`Devices.xlsx` device-type ontology, `PCM.xlsx` Plant Breakdown Structure)
- qa-report (POC_WRAPPING.md, AIM_ACHIEVABILITY_AND_TBD.md flagging legacy-data limits)
- domain-prompts-and-rules (ontology definition, device-type RoleClass paths, naming conventions)

**Specific things worth noting:**
- PoC ~12 weeks, started end of Feb 2026, in final stretch as of mid-May (May 20 locked demo to Gerald + Matthias).
- Demo goal: "wow factor" ("you ask and the answer appears, no exposed plumbing"), but honest about limitations ("platform requires adaptation, not plug-and-play").
- Thorsten (SME): "definition of data model is very important… if we go the wrong way, we can extract data but can't use it."
- SMS moving slowly on procurement; expect weeks for next commercial step.
- Reference quote wanted (Jordan willing to co-fund part of implementation in exchange).
- Cross-discipline linking challenge: legacy data with no cross-document identifiers explicitly out of scope. PoC uses newer data with PE## + SAP codes.
- Hydraulic-chains currently extracted to separate JSON, not yet connected to device ontology (Victor flagged for Phase-2 refactor).

---

### heineken

**Source types:**
- Excel workbooks (MAIN Applications & Services Financials, Financial Tracker, Zycus contracts, PO Dump, MEC closing reports)
- SharePoint-hosted (IRIS.ai x Heineken site; shared as external Teams channel)
- ~160 IT services tracked across 4-5 Excel workbooks with no integrated system
- Universal join key: L-code (L.0226 = MyHR, L.0290 = Ironclad, L.0215 = HeiPort, etc.)
- Cell comments are institutional memory (~354 across files)
- Formulas encode business logic (=(9600/12)*8 = 8 months of a €9,600/yr contract)

**Promised extraction:**
Build RAG / SQL-agent over the financial files, ingesting them into a database (values, cell comments, formulas, column metadata) and answering cross-source questions (vendor PO lookups, contract-status checks, budget-vs-actuals gaps, missing-invoice detection). Human-in-the-loop demo (agent drafts email, budget owner approves/edits).

**Artifacts found:**
- `4_poc/datastore-context/` (human-readable datastore description + glossary + agent guidelines)
- `4_poc/Heineken POC Alignment 2026-04-16.docx` (scenarios/data/process validation doc)
- `_legacy/BRIEFING.md`, `_legacy/KICK_OFF.md` (data walkthrough, Excel→DB+RAG job spec)
- `4_poc/_axion_archive/_rag_extracted/` (~102 MB, per-sheet .txt extractions + cell-comments / manifest JSONs)
- `https://heineken-dev.iris.ai` (the agent itself; Justyna got login Apr 24)

**Patterns used:**
- agent-query-interface (Heineken Assistant RAG agent at heineken-dev.iris.ai; six scenarios: vendor count, vendor PO lookup, missing-invoice, MEC monthly-split, budget-vs-actuals, invoice status)
- relational-database-output (unified data layer from 5 Excel sources via L-code join key)
- extraction-json-bundle (per-sheet .txt + metadata JSONs, formulas + cell comments captured)
- domain-terminology-mapping (vendor-name fuzzy matching, L-code mappings, HNK contract number, PO# linkage)
- cross-document-entity-linking (HNK number partial join across Zycus / Tracker / MAIN; vendor fuzzy match Elucidat ↔ Insight Enterprises)
- domain-prompts-and-rules (datastore-context + glossary tell the agent how files connect, what cells mean, business rules)
- qa-report (Heineken POC Alignment doc; Monika self-testing scenarios)

**Specific things worth noting:**
- PoC since Mar 23 2026 contract, originally ending ~May 18 (Week 8); as of mid-May: single-source scenarios done, cross-source landing, human-in-the-loop email-draft demo being built.
- Justyna's three capabilities to prove: (1) data ingestion across 5 sources without hard-coded rules, (2) human-in-the-loop learning (agent improves from corrections), (3) observability/auditability.
- Justyna stays in control (nothing leaves without her approval). Answers must carry budget context (AP26 budget vs PO vs actual, contract status via status field not expiry date).
- Lucy (manager) wants to see Justyna as human-in-the-loop approver (draft PO-request email, she approves/edits/rejects, not just Q&A).
- Continuous-learning loop is open question (not demonstrable next Wednesday, needs scope discussion with Lucy).
- Token-spend economics: cost must be <Justyna's salary for the deal to work.

---

### postbank

**Source types:**
- Salesforce Marketing Cloud (SFMC) Data Extensions (their term for views/tables), populated by SFMC SQL Query Activities
- No real data shared yet (pre-NDA; would only share after NDA signed)
- Demo uses synthetic SFMC dataset (10 Data Extensions, ~150 rows each, 5 hand-authored SFMC SQL Query Activities, glossary docs)
- Bulgarian-flavour names, English-only labels
- Multibank campaign data (Send-Cohort, Segments, Campaign performance, Conversions, Pipeline, etc.)

**Promised extraction:**
Data-unification layer (auto-generated semantic layer from schema + code + sample rows) + analytics agent on top. Demonstrate on synthetic data first; real data after NDA. Two output modes: business-user (graph+table+explanation+verification) and Campaign Ops (copy-paste-ready SFMC SQL query).

**Artifacts found:**
- `2_scoping/demo-build/SCOPING_DEMO.md` (scoping-demo spec: what Postbank wants, sheet 1 answers, synthetic dataset, three-act demo structure)
- `2_scoping/demo-build/PLAN.md` (engineering build plan for 28 Apr demo)
- `1_pre-scoping/transcripts/Postbank (Svetla) <> Iris.ai 2026-04-08 Discovery (Viktor).txt` (discovery/qualification call)
- Neuralith unified-demo app (synthetic `postbank-sfmc` dataset registered, custom ingestion agents, test cases, chat-on-deploy script, SFMC workflow)

**Patterns used:**
- agent-query-interface (analytics agent over SFMC Data Extensions, business-user + Campaign Ops SQL output modes)
- extraction-json-bundle (synthetic Data Extensions as structured fixtures, 5 SFMC SQL Query Activities)
- domain-terminology-mapping (segment codes ∈ {SME, RETAIL, PRIVATE, MORTGAGE}; "active customer" definition; conversion attribution window)
- relational-database-output (10 SFMC Data Extensions with schema, per-DE sample rows ~150 each)
- qa-report (SCOPING_DEMO.md framing the demo, differentiator vs Solid AI, NDA close)
- domain-prompts-and-rules (semantic layer auto-built from code + docs + sample rows; every relationship traceable to source)

**Specific things worth noting:**
- **CRITICAL: Svetla departed 2026-05-14** (final week at Postbank); handed off to Lina Varbanova (new primary contact, brand new to the engagement).
- Lena (VP-style, Svetla's boss on this topic) decides whether/when MNDA gets sent; holds budget first-line approval.
- NDA not yet sent (Svetla declined to commit on 8 May, said Lena would decide); synthetic-data-only path still holds.
- 28 Apr Sofia F2F (in-person) happened; no transcript on file, but 8 May call references it positively.
- Scoped pilot: retail-banking campaign analysis, few SFMC Data Extensions, ~€40k with IRIS co-funding.
- Viktor signed off on co-funding "contingent on clear expansion path" (enterprise data-warehouse is aspirational follow-on).
- Two output modes (business-user report + Campaign Ops SQL) are judgment criteria, not three escalating-complexity questions.
- Hard for Postbank = administrative (security, GDPR, EU AI Act, procurement, CEO sign-off for NDA), not technical.

---

## Recurring themes / cross-cutting observations

1. **"Scoping" is the consistent phase** where Pyloth deliverables are built. All 17 engagements ran a scoping exercise (or are in pre-scoping / intro for fresh ones). Scoping outputs include showcase HTML, extraction results JSON, demo walkthrough scripts (STORY.md), QA reports, and confidence matrices. The scoping exercise is the "prove capability before paid PoC" step.

2. **Self-contained HTML showcases are the currency of demo** — Almost every engagement that reached scoping (Deutschebahn, Garrett, Welocalize, Agrolimen, T&F demo viewer, SMS Group planned) delivered an interactive HTML app. These are the artifacts clients actually interact with; they show extraction coverage (every page processed), accuracy samples, and (often) before/after comparisons.

3. **Evidence traceability is table-stakes in regulated industries** — Deutschebahn (rail operations), Welocalize (pharmacovigilance), T&F (scientific claims), Agrolimen (food safety/compliance) all require page number + BBox + verbatim quote on every extracted fact. Hallucination risk is high; honesty about confidence / failure modes is trust-building.

4. **Multilingual = business problem, not just a data problem** — Garrett (OEM specs in multiple languages → component library), Welocalize (adverse-event forms in 5 languages), Agrolimen (supplier specs in EN/IT/ES/FR/DE) all use multilingual extraction to *solve a customer problem* (no human can read everything, language is a wall). The pattern: same schema output regardless of source language, no per-language fine-tuning.

5. **Cross-document entity linking is hard and unique per industry** — SMS Group (MuK tag ↔ hydraulic YVH code ↔ EPLAN PLC address), Aumovio (HNK number across Zycus / Tracker / PO Dump, vendor fuzzy match), Heineken (L-code universal join key). There's no universal pattern here; each domain has its own linkage challenge. Legacy data with no cross-document identifiers is out of scope (SMS Group flagged this honestly).

6. **Business rules are domain-specific and live in the extraction pipeline, not a separate "config"** — Aumovio (weekly→annual unit conversions, parts-per-vehicle multipliers, which table row is source of truth), Heineken (L-code join logic, formula interpretation), Agrolimen (supplier→master matching rules). These are not post-extraction; they're baked into the extraction schema and prompts. The schema is the contract.

7. **Quality gates are often IRIS-originated, not client-imposed** — Aumovio's procurement will check the signed SoW's explicit requirements (it doesn't have numeric thresholds) — the specific F1/recall/ODL-mapping targets came from IRIS's Sept 2025 proposal, not Aumovio. This is a risk (client can hold you to your own targets), so metrics must be justified (not arbitrary) and curated for evaluation (batch-by-batch improvement narrative).

8. **Cost-per-document transparency is a deal-gate** — Fresenius (wants extrapolatable cost to 1000-2000 papers + 500-SOP deployment), Heineken (token spend vs Justyna's FTE cost), Postbank (€40k co-funded, needs expansion path to profitability). Clients want to evaluate IRIS vs building internally; cost is the comparison point.

9. **Honesty about failure modes is a differentiator** — Welocalize (TH2 blurred scan below-threshold, recommend >=300 DPI SLA), Aumovio (batch improvement curves showing learning, not claiming 95% on day 1), Garrett (didn't claim to beat your 97% matcher, this is different capability). This lands better than overselling.

10. **Deliverable artifacts cluster into a few canonical shapes** — (a) interactive HTML showcase with before/after or tab-driven navigation, (b) extraction JSON bundles (per-document + aggregated), (c) confidence matrices / per-doc quality bands, (d) STORY.md walkthrough script, (e) QA report (AIM.md / SCOPING_PRESENTATION / POC_WRAPPING). These patterns are reusable; no engagement invented a wholly new deliverable shape.

11. **The "human-in-the-loop" demo matters for trust and adoption** — Heineken (Justyna approves/edits draft email before send), SMS Group (tree-view NL query → locate on drawing), Postbank (Campaign Ops gets copy-paste SQL to review). It's not Q&A; it's "the system drafts, the person approves."

12. **Schema = contract, not a derivation** — Agrolimen ("Patricia explicitly asked for a relational database matching her schema, not a generic CSV"), Aumovio (template_contracted_volumes_rev2, business rules per field), Deutschebahn (CTMS ontology, 14-15 data objects). The client's schema (or their expectation of one) is binding. IRIS doesn't invent structure; it extracts to an agreed schema.

13. **Closed-lost engagements still inform the pattern catalog** — Agrolimen (closed-lost 2026-05-15 mid-scoping, but the Scoping Presentation, AIM.md, and Document Explorer are all reusable patterns). Patterns are about the *shape of the deliverable*, not the deal outcome.

14. **Terminology mapping is domain-specific and client-provided** — Fresenius (GLP-1-RA = Mounjaro = semaglutide = tirzepatide; ESA = EPO; RRT = dialysis), SMS Group (MuK + YVH + PE## + PLC address = same device), Aumovio (OEM-specific weeks/year, product-type parts-per-vehicle). Synonyms are baked into extraction schema or config; not post-processed.

15. **Scoping demo scripts (STORY.md) are underrated assets** — Almost every scoping engagement documented a STORY or TALKING_SCRIPT (Garrett, Welocalize, Agrolimen, SMS Group, Heineken). These are walk-throughs for the presentation. They're not just narration; they document what the demo is trying to prove and what the client should pay attention to.

