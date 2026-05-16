# Axion audit: garrett

## Summary
- Total size: 478.9 MB
- File count: 823
- Categories breakdown: data 14 / code 10 / output 404 / other 395
- Category sizes: data 49.9 MB / code 193.7 KB / output 272.2 MB / other 156.7 MB
- Drive coverage: 1.6% of files have a Drive equivalent by filename
- Orphan count (data files NOT in Drive): 3

## Files (grouped by subfolder; >500MB engagement)

| Subfolder | Files | Size | data | code | output | other | Drive cov | Orphan data |
|---|---|---|---|---|---|---|---|---|
| `04_Garrett_performance-catalog-2025` | 638 | 416.9 MB | 1 | 0 | 332 | 305 | 0% | 0 |
| `scoping` | 13 | 49.9 MB | 13 | 0 | 0 | 0 | 77% | 3 |
| `DE69827504T2_DE` | 51 | 4.2 MB | 0 | 0 | 24 | 27 | 0% | 0 |
| `EP1301689B1_FR` | 62 | 4.2 MB | 0 | 0 | 28 | 34 | 0% | 0 |
| `ES2320343T3_ES` | 42 | 3.4 MB | 0 | 0 | 20 | 22 | 0% | 0 |
| `<root>` | 15 | 241.3 KB | 0 | 10 | 0 | 5 | 0% | 0 |
| `notes` | 2 | 17.6 KB | 0 | 0 | 0 | 2 | 0% | 0 |

## Drill: code files

### `<root>/`

| Path | Size | In Drive? |
|---|---|---|
| build_combined_showcase.py | 25.2 KB | no |
| build_combined_showcase_v3.py | 48.1 KB | no |
| build_showcase.py | 15.6 KB | no |
| build_showcase_v2.py | 17.5 KB | no |
| garrett_showcase.py | 29.2 KB | no |
| inject_data.py | 8.4 KB | no |
| step1_chandra_full.py | 11.0 KB | no |
| step1_chandra_patents.py | 8.0 KB | no |
| step2_translate_patents.py | 7.2 KB | no |
| step3_build_multilingual_showcase.py | 23.6 KB | no |

## Findings

- 3 data file(s) NOT in Drive (orphans, need upload-before-delete):
  - `scoping/13_ES2320343T3_turbocompresor-system_ES.pdf`
  - `scoping/11_EP1301689B1_sliding-vanes_FR.pdf`
  - `scoping/12_DE69827504T2_two-axis-adjustable-vanes_DE.pdf`

- Code files to move into engagements/garrett/<stage>/: 10 files (193.7 KB)
- Output files to move to Drive iris-outputs/ or S3: 404 files (272.2 MB)

## Migration recommendation

- Delete-after-Drive-verified: 409 files, 206.5 MB (data already in Drive + noise/notes/images)
- Move to repo: 10 files, 193.7 KB
- Upload to Drive first (orphans): 3 files
