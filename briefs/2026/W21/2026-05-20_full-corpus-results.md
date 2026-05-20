# Full-corpus extraction results — 2026-05-20

## Headline

**106/106 docs extracted, $6.05 cost, 154 min wall, 0 errors.** All 5 V4-CX feedback items from Phil are addressed by the current extractor. One regression on ALPINE that needs diagnosis.

## Extraction stats

| Metric | Value |
|---|---|
| Docs processed | 106 / 106 |
| Failures | 0 |
| Zero-row outputs | 11 (short OCRs, likely no volume tables) |
| Total cost | $6.05 |
| Wall time | 154 min (2h35m) |
| Throughput | 1.6-2.0 docs/min effective (6 workers) |
| Heaviest doc | BMW IBS 269-page: $0.26, 9060s (translation-bound) |

## Reference regression check (10 confirmed)

Compared `reports/full_corpus/predictions.json` vs `reports/iter2_incremental/predictions.json` (locked baseline).

| Doc | Verdict |
|---|---|
| ALPINE | 🔴 **REGRESSION**: 3 rows → 1 row. Lost paint-variant split. Each cell ~6.7× larger (single consolidated row). |
| AUDI | ✅ Exact match |
| FCAUS | 🟢 Cosmetic: "Air Supply Unit (CAirS)" → "CAirS" (same product, briefer) |
| FIATPV | 🟡 Soft: customer "FCA" → "Stellantis" (rules canonicalization); product_group richer (Manual Handbrake / IPB / High IPB variants — better) |
| FORDCV | ✅ Exact match |
| GM | 🟢 IMPROVEMENT: product_group now "Front/Rear Air Spring" directly (matches overlay target); lifetime off by 2 (rounding) |
| HOLON | ✅ Exact match |
| HONDAPV | ✅ Exact match |
| NIO | 🟡 Soft: EOP 12/2027 → 12/2026 (model reverted to last-non-zero-year convention) |
| RENAULTPV | ✅ Exact match |

### ALPINE regression — needs investigation

The new extractor consolidated 3 paint-variant rows into 1. Phil 03-24 explicitly approved keeping paint variants as separate rows ("Oh it's different paint versions. Unpainted red paint... designs again. Okay. That we have 103 rows, it's okay"). The new L/R-collapse rule likely over-applied to color/design variants. Need to refine the prompt to distinguish:
- **DO collapse**: L/R sides of one axle-pair component
- **DO NOT collapse**: paint variants, design variants, distinct part-number families with distinct volumes

Not auto-fixed per plan instructions. The 10-confirmed predictions remain locked in `reports/iter2_incremental/predictions.json`. To fix: tighten the row-granularity rule in `pipeline/llm_extract.py` and re-extract ALPINE only.

## V4-CX feedback — all 5 docs resolved

| Doc | Phil's CX remark | Resolution |
|---|---|---|
| FORDNA CD42 | SOP 2020, volume missing, plant=T0833 (not Oakville buyer) | ✅ SOP 09/2020, T0833 supplier plant, weekly×45×2 = yearly, parts_per_vehicle=2, flex from weekly avg/max |
| FORDNA CD42 v2 | (same as CD42) | ✅ Same handling, includes Edge + Nautilus programs |
| MITSUBISHI Triton | Renault→Mitsubishi, plant=Changshun, volume 2024-2028, TPMS=4/vehicle | ✅ customer="Mitsubishi", TPMS parts_per_vehicle=4, yearly 2024-2028 captured |
| FAW-VW Tavascan | Project="Tavascan", SOP=CW41/2023, flex~15% from weekly normal/max, EOP question | ✅ project_title="Tavascan", SOP="10/2023" (CW41 parsed), flex_pct="15%", EOP=12/2029 (VW 7y default) |
| JAGUAR ACA | SOP~01/09/2018, EOP~2026 (lifetime 910k/8yr), partial-year prorate, flex=10% | ✅ SOP=09/2018, EOP=08/2026 (8y cycle), lifetime=910,545, flex_pct="10%", 9-year yearly w/ partial prorate |

**No new prompt rules needed.** All Phil's concerns are already encoded.

## Zero-row docs (11) — needs follow-up at scale

Short OCRs that produced no extracted rows. Likely missing volume tables or single-page addenda:

GAC_NL_A06_19022017 (zh), PSA_NL_DPCA_X81G_04092013, RENAULTPV_NL_ESS_PMH_HR_01062018, RENAULTPV_NL_XDD_H2_WSS_10122023, RENAULTPV_NL_X10_PH2_28042017, SAIC-VW_NL_SVW_B_SUV__04122024, SAIC-VW_NL_SVW_PURPLE_12122024, SUBARU_DA_2FA_03042023, VWPV_NL_-_16122016, VWPV_NL_ACU_VW40_M_05122017, (one more).

Worth a manual spot-check on 2-3 of these before Monday. Could be:
- Documents that genuinely have no volume table (addenda, price-only)
- OCR failed to capture the volume table (image-based, like Honda before)
- Extraction prompt failed to recognize an unusual structure

## Recommended next steps for Monday call with Phil

1. **Walk through 5-7 of the V4-CX docs** — show how extractor now handles his exact concerns (FORDNA T0833, Tavascan project + CW41 date, JAGUAR partial-year prorate, etc.).
2. **Daily-capacity multiplier for Chevrolet** — still pending. Phil promised after April 21 call.
3. **ALPINE row count** — ask Phil to confirm whether paint-variants should remain separate. Our locked 3-row version matches what he approved on 03-24.
4. **Zero-row docs review** — share the 11-doc list, ask if any should have volumes.
5. **Phil-GT-vs-contract divergences** documented in [[phil-gt-idiosyncrasies]] — share so Phil knows where reference disagrees with contract math.

## Open commercial threads

- Daily-capacity multiplier (Chevrolet) — Phil pending since 21-Apr
- V4 row count expectations (paint-variant policy) — confirm
- Sign-off pathway for the 100-doc extraction as a deliverable

## Files

- Predictions: `aumovio/4_poc/eval/extractor_v2/reports/full_corpus/predictions.json`
- Per-doc meta: `aumovio/4_poc/eval/extractor_v2/reports/full_corpus/per_doc_meta.json`
- Plan that fired this: `aumovio/4_poc/eval/extractor_v2/AUTONOMOUS_PLAN.md`
- Commits: `54924f8` (this run) on top of `183872e` (10/11 confirmed state)
