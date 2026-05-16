# Axion audit: tandf

## Summary
- Total size: 1.2 GB
- File count: 4400
- Categories breakdown: data 150 / code 23 / output 1351 / other 2876
- Category sizes: data 437.9 MB / code 195.5 KB / output 95.7 MB / other 678.0 MB
- Drive coverage: 32.0% of files have a Drive equivalent by filename
- Orphan count (data files NOT in Drive): 0
- Excluded from audit (.venv/node_modules/.git/etc): 6 files, 52.6 KB

## Files (grouped by subfolder; >500MB engagement)

| Subfolder | Files | Size | data | code | output | other | Drive cov | Orphan data |
|---|---|---|---|---|---|---|---|---|
| `_extractor` | 3078 | 620.7 MB | 0 | 23 | 1337 | 1718 | 3% | 0 |
| `shared` | 202 | 304.1 MB | 100 | 0 | 1 | 101 | 99% | 0 |
| `deliverable` | 1111 | 285.3 MB | 50 | 0 | 13 | 1048 | 99% | 0 |
| `notes` | 7 | 1.6 MB | 0 | 0 | 0 | 7 | 86% | 0 |
| `<root>` | 2 | 47.2 KB | 0 | 0 | 0 | 2 | 0% | 0 |

## Drill: code files

### `_extractor/`

| Path | Size | In Drive? |
|---|---|---|
| _extractor/aggregate_findings.py | 11.8 KB | no |
| _extractor/aggregate_with_uris.py | 5.9 KB | no |
| _extractor/backfill_section_types.py | 3.4 KB | no |
| _extractor/bench_models.py | 3.0 KB | no |
| _extractor/build_deliverable.py | 18.8 KB | no |
| _extractor/build_doc_from_chandra.py | 14.1 KB | no |
| _extractor/build_viewer_assets.py | 18.2 KB | no |
| _extractor/chandra_extract.py | 10.1 KB | no |
| _extractor/corpus_summary.py | 6.9 KB | no |
| _extractor/curate_ontology_gaps.py | 7.6 KB | no |
| _extractor/detect_cross_section.py | 6.7 KB | no |
| _extractor/detect_ontology_gaps.py | 9.5 KB | no |
| _extractor/extract_findings.py | 19.6 KB | no |
| _extractor/extract_table_findings.py | 11.5 KB | no |
| _extractor/inspect_findings.py | 1.8 KB | no |
| _extractor/keep_best_findings.py | 5.5 KB | no |
| _extractor/match_pdf_to_xml.py | 4.9 KB | no |
| _extractor/ontologies.py | 4.0 KB | no |
| _extractor/parse_jats.py | 10.8 KB | no |
| _extractor/rename_to_originals.py | 7.8 KB | no |
| _extractor/requirements.txt | 48.0 B | no |
| _extractor/split_xmls.py | 2.0 KB | no |
| _extractor/uri_linking.py | 11.5 KB | no |

## Findings

- No data orphans: every client-document filename has a Drive match.

- Code files to move into engagements/tandf/<stage>/: 23 files (195.5 KB)
- Output files to move to Drive iris-outputs/ or S3: 1351 files (95.7 MB)

## Migration recommendation

- Delete-after-Drive-verified: 3026 files, 1.1 GB (data already in Drive + noise/notes/images)
- Move to repo: 23 files, 195.5 KB
- Upload to Drive first (orphans): 0 files
