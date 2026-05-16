# Axion audit — summary

_Generated 2026-05-16T18:49Z._

## Active engagements (will migrate)

| Engagement | Axion size | Files | Drive cov | Orphans | data files | code files | output files | Action |
|---|---|---|---|---|---|---|---|---|
| postbank | 9.7 MB | 34 | 3% | 0 | 1 | 0 | 0 | Phase 2 pilot (small) |
| aumovio | 173.2 MB | 781 | 64% | 8 | 153 | 15 | 458 | Phase 3 |
| heineken | 301.7 MB | 281 | 9% | 26 | 50 | 8 | 175 | Phase 3 |
| welocalize | 242.4 MB | 182 | 85% | 15 | 49 | 1 | 61 | Phase 3 |
| garrett | 478.9 MB | 823 | 2% | 3 | 14 | 10 | 404 | Phase 3 |
| sms-group | 2.6 GB | 8403 | 80% | 16 | 6649 | 60 | 238 | Phase 3 |
| tandf | 1.2 GB | 4400 | 32% | 0 | 150 | 23 | 1351 | Phase 3 |
| agrolimen | 78.4 MB | 332 | 84% | 2 | 96 | 6 | 140 | Phase 3 |
| fresenius | 45.9 MB | 178 | 84% | 0 | 25 | 17 | 103 | Phase 3 |
| deutschebahn | 31.6 MB | 12 | 58% | 1 | 8 | 0 | 0 | Phase 2 pilot (small) |
| nhs | 37.5 KB | 3 | 0% | 0 | 0 | 0 | 0 | Phase 2 pilot (small) |
| daikin | (no Axion folder) | - | - | - | - | - | - | n/a (pre-scoping, never in Axion) |
| finom | (no Axion folder) | - | - | - | - | - | - | n/a (pre-scoping, never in Axion) |

## Halted / declined (will delete in Phase 1)

| Engagement | Axion size | Files | Drive cov | Orphans | Reason | Tombstone in engagements/? |
|---|---|---|---|---|---|---|
| alexfert | 302.0 MB | 5333 | 5% | 24 | war-paused | no |
| shanghai-synocodes | 4.7 MB | 88 | 84% | 4 | lost (price) | no |
| stepan | 46.2 MB | 56 | 12% | 6 | lost (no project) | no |
| aumovio-soft-impact | 847.0 KB | 2 | 0% | 1 | merged into Aumovio main | no |
| hubspot | 265.5 KB | 14 | 0% | 0 | internal IRIS exploration only | no |
| cetin | 3.0 MB | 15 | 0% | 10 | halted / no engagement | no |

## Empty placeholders (will delete)

| Folder | Size | Files | Notes |
|---|---|---|---|
| ahli | 44.0 KB | 1 | meeting-1.md |
| allianz | 52.0 KB | 4 |  |
| aramco | 612.0 KB | 1 | FY2026 Commercial Strategy v4.0.0.pdf |
| basamh | 56.0 KB | 1 | Mohammed (Basamh) _ Jordan (Iris.ai).txt |
| brunela | 68.0 KB | 2 | Notes from NHS.txt + Iris.ai <> Brunela 02-04-2026.txt |
| ciklum | 36.0 KB | 1 | First Meeting Transcription.txt |
| lifescience | 0.0 B | 0 | truly empty |
| orion | 56.0 KB | 1 | Goran (Orion Telekom) _ Jordan (Iris.ai).txt |
| riyadbank | 0.0 B | 0 | truly empty |

## Anomalies (listed as empty in brief, but has content)

| Engagement | Axion size | Files | Drive cov | Orphans | data | code | output | Note |
|---|---|---|---|---|---|---|---|---|
| yettel | 13.6 MB | 535 | 0% | 55 | 55 | 22 | 338 | brief said empty, but contains a RAG pipeline + ~55 client docs; needs disposition decision |

## Axion top-level loose files

| File | Size | Note |
|---|---|---|
| Usage based pricing 2025 - calculator.xlsx | 167.4 KB | top-level, decide per-file |
| bbox_editor.html | 12.4 KB | top-level, decide per-file |

## Cross-engagement findings

- Total Axion size audited: **5.4 GB** across 17 engagements (20937 files).
- Active engagements: 5.1 GB across 15429 files (11 engagements with Axion folders).
- Halted/declined (will delete): 357.0 MB across 5508 files.
- Files needing upload-to-Drive-first (data orphans across all audited): **116** files.
- Total code files to move into engagement repos: **183** files (1.9 MB).
- Total output files (extraction results, deliverables): **3217** files (548.5 MB) — should land in Drive iris-outputs/ or S3.
- Total client data (already-on-Drive + orphans): 3.8 GB — bulk of the Axion footprint.
- Engagement with most code files: **sms-group** (60 files, 648.0 KB).
- Engagement with most data orphans: **heineken** (26 files).

## Phase plan derived from audit

**Phase 1 — delete halted/declined + empty placeholders.** Confirm tombstones exist in `engagements/` for each before deleting. Items where the engagements/ tombstone is `no` need a tombstone written first.

**Phase 2 — pilot migration (postbank).** 34 files, 9.7 MB, 100% non-orphan. Cleanest pilot: validates the migration script and the engagements/<co>/<stage>/extraction/ destination layout.

**Phase 3 — batch migrate the active rest.** Per-engagement, in size order:
- `nhs` — 37.5 KB, 3 files, 0 orphans, 0% drive cov.
- `postbank` — 9.7 MB, 34 files, 0 orphans, 3% drive cov.
- `deutschebahn` — 31.6 MB, 12 files, 1 orphans, 58% drive cov.
- `fresenius` — 45.9 MB, 178 files, 0 orphans, 84% drive cov.
- `agrolimen` — 78.4 MB, 332 files, 2 orphans, 84% drive cov.
- `aumovio` — 173.2 MB, 781 files, 8 orphans, 64% drive cov.
- `welocalize` — 242.4 MB, 182 files, 15 orphans, 85% drive cov.
- `heineken` — 301.7 MB, 281 files, 26 orphans, 9% drive cov.
- `garrett` — 478.9 MB, 823 files, 3 orphans, 2% drive cov.
- `tandf` — 1.2 GB, 4400 files, 0 orphans, 32% drive cov.
- `sms-group` — 2.6 GB, 8403 files, 16 orphans, 80% drive cov.

**Phase 4 — handle Axion loose top-level files** (Usage-based pricing xlsx, bbox_editor.html, root .DS_Store).

## Read the per-engagement audits

- [postbank](./postbank.md)
- [aumovio](./aumovio.md)
- [heineken](./heineken.md)
- [welocalize](./welocalize.md)
- [garrett](./garrett.md)
- [sms-group](./sms-group.md)
- [tandf](./tandf.md)
- [agrolimen](./agrolimen.md)
- [fresenius](./fresenius.md)
- [deutschebahn](./deutschebahn.md)
- [nhs](./nhs.md)
- [alexfert](./alexfert.md)
- [shanghai-synocodes](./shanghai-synocodes.md)
- [stepan](./stepan.md)
- [aumovio-soft-impact](./aumovio-soft-impact.md)
- [hubspot](./hubspot.md)
- [cetin](./cetin.md)
- [yettel](./yettel.md)

