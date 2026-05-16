# Axion audit: alexfert

## Summary
- Total size: 302.0 MB
- File count: 5333
- Categories breakdown: data 90 / code 39 / output 247 / other 4957
- Category sizes: data 230.3 MB / code 371.1 KB / output 8.6 MB / other 62.8 MB
- Drive coverage: 5.0% of files have a Drive equivalent by filename
- Orphan count (data files NOT in Drive): 24
- Excluded from audit (.venv/node_modules/.git/etc): 5459 files, 83.1 MB

## Files (grouped by subfolder; >500MB engagement)

| Subfolder | Files | Size | data | code | output | other | Drive cov | Orphan data |
|---|---|---|---|---|---|---|---|---|
| `agent` | 5190 | 225.2 MB | 69 | 25 | 207 | 4889 | 5% | 3 |
| `presentation` | 62 | 60.8 MB | 7 | 3 | 3 | 49 | 0% | 7 |
| `results` | 22 | 4.3 MB | 0 | 0 | 22 | 0 | 0% | 0 |
| `<root>` | 8 | 4.0 MB | 2 | 0 | 0 | 6 | 0% | 2 |
| `raw-data` | 9 | 3.4 MB | 1 | 0 | 1 | 7 | 0% | 1 |
| `extraction` | 9 | 2.0 MB | 7 | 0 | 2 | 0 | 0% | 7 |
| `docs` | 4 | 1.9 MB | 4 | 0 | 0 | 0 | 0% | 4 |
| `notes` | 6 | 210.0 KB | 0 | 0 | 0 | 6 | 0% | 0 |
| `app` | 11 | 144.1 KB | 0 | 11 | 0 | 0 | 0% | 0 |
| `results-llm` | 12 | 27.4 KB | 0 | 0 | 12 | 0 | 0% | 0 |

## Drill: code files

### `agent/`

| Path | Size | In Drive? |
|---|---|---|
| agent/chunker/chunk_papers.py | 11.7 KB | no |
| agent/chunker/chunk_papers_v1.py | 0.0 B | no |
| agent/chunker/chunk_papers_v2.py | 11.7 KB | no |
| agent/extractor/config.py | 900.0 B | no |
| agent/extractor/run_pipeline.sh | 3.1 KB | no |
| agent/extractor/step1_extract_papers.py | 10.2 KB | no |
| agent/extractor/step2_chunk_content.py | 12.5 KB | no |
| agent/extractor/step3_generate_indices.py | 5.2 KB | no |
| agent/extractor/step4_build_opensearch.py | 16.1 KB | no |
| agent/extractor/step4_build_vector_db.py | 8.2 KB | no |
| agent/output-800-tokens/59_capex_opex_evaluation_of_blue_ammonia_process_configuration_for_higher_co2_recov.iris.json | 27.4 KB | yes (2x, Commercial/Playground & Demo/Axion Demo Datasets/AlexFert Demo/59_capex_opex_eva) |
| agent/output-mechanically-reduced/59_capex_opex_evaluation_of_blue_ammonia_process_configuration_for_higher_co2_recov.iris.json | 26.4 KB | yes (2x, Commercial/Playground & Demo/Axion Demo Datasets/AlexFert Demo/59_capex_opex_eva) |
| agent/split_pdf_bookmarks.py | 5.4 KB | no |
| agent/split_pdf_by_topics.py | 7.1 KB | no |
| agent/split_pdf_contextual.py | 6.0 KB | no |
| agent/split_pdf_v2.py | 8.0 KB | no |
| agent/split_pdf_v3.py | 6.0 KB | no |
| agent/split_pdf_v3_test.py | 2.3 KB | no |
| agent/tester/.neuralith_config.json | 769.0 B | no |
| agent/tester/demo_queries.py | 2.5 KB | no |
| agent/tester/neuralith_client.py | 8.8 KB | no |
| agent/tester/optimal_demo_queries.py | 3.2 KB | no |
| agent/tester/query_consistency.py | 2.4 KB | no |
| agent/tester/query_variations.py | 2.4 KB | no |
| agent/tester/run_comparison.py | 3.1 KB | no |

### `app/`

| Path | Size | In Drive? |
|---|---|---|
| app/extract_to_schema.py | 12.1 KB | no |
| app/extract_vision_llm.py | 10.7 KB | no |
| app/generate_bbox_editor.py | 35.1 KB | no |
| app/generate_excel.py | 14.4 KB | no |
| app/generate_gpt_bbox_editor.py | 23.2 KB | no |
| app/generate_pdf.py | 28.9 KB | no |
| app/gpt-vision-extract.py | 2.5 KB | no |
| app/schema.py | 7.6 KB | no |
| app/test_ocr.py | 1.8 KB | no |
| app/visualize_llm_extraction.py | 5.1 KB | no |
| app/visualize_ocr.py | 2.7 KB | no |

### `presentation/`

| Path | Size | In Drive? |
|---|---|---|
| presentation/create_intro_slides.py | 15.2 KB | no |
| presentation/create_presentation.py | 14.9 KB | no |
| presentation/create_trusted_by_slide.py | 5.6 KB | no |

## Findings

- 24 data file(s) NOT in Drive (orphans, need upload-before-delete):
  - `AlexFert Scoping Results.pptx.pdf`
  - `Usage based pricing 2025 - calculator.xlsx`
  - `raw-data/target-output.pdf`
  - `agent/nitrogen_syngas_2024_technical_preprints-7d8d2c.pdf`
  - `agent/chunks/20_compact_urea_plant_for_green_hydrogen_and_co2_valorization_luca_edoardo_viganò_m.pdf`
  - `agent/chunks/24_-_refurbishing_an_aging_urea_reactor.pdf`
  - `docs/Commercial Proposal AlexFert.docx`
  - `docs/AlexFert SOW February 2026 bak.docx`
  - `docs/_Blank NDA Iris - AlexFert.docx`
  - `docs/AlexFert SOW February 2026.docx`
  - `extraction/plants_daily_activities.pdf`
  - `extraction/AS_production_ocr_visualization.pdf`
  - `extraction/plants_daily_activities.xlsx`
  - `extraction/UREA_REP1 Daily Production Report - screenshot_ocr_visualization.pdf`
  - `extraction/Ammonia daily report - photo print and handwritten_ocr_visualization.pdf`
  - `extraction/amm_rep1 daily production report - photo print_ocr_visualization.pdf`
  - `extraction/Production Daily Report - handwriting_gpt_ocr_visualization.pdf`
  - `presentation/AlexFert Scoping Results.pdf`
  - `presentation/Trusted_By.pptx`
  - `presentation/AlexFert AI Assesment Presentation.pdf`
  - `presentation/Iris_Intro_CaseStudies.pptx`
  - `presentation/Company Introduction_Master Deck .pdf`
  - `presentation/Company Introduction_Master Deck .pptx`
  - `presentation/AlexFert Scoping Results.pptx`

- Code files to move into engagements/alexfert/<stage>/: 39 files (371.1 KB)
- Output files to move to Drive iris-outputs/ or S3: 247 files (8.6 MB)

## Migration recommendation

- Delete-after-Drive-verified: 5047 files, 293.0 MB (data already in Drive + noise/notes/images)
- Move to repo: 39 files, 371.1 KB
- Upload to Drive first (orphans): 24 files
