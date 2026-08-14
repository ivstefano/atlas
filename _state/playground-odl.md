# STATE: playground-odl

_Working memory for the playground onboarding + ODL work. Not client-facing._

last_session: 2026-08-14

## Now

Building the **ODL side-panel mock**: the Axion demo chrome (dark sidebar, file list,
`Close preview` bar) but the preview pane holds the **corpus-wide ODL table** instead of a
single file's table artifact. Target file:
`atlas/_assets/playground-onboarding/odl-example.html` (replacing the current standalone
evidence-drawer page).

Reference screenshot: the existing artifact preview showing FOUND / RECONSTRUCTED side by
side for one file. The ODL replaces that pane, opened from the middle-right panel of the
demo, as the **final beat** after the visitor has browsed files and artifacts.

## Key reasoning (do not re-derive)

- Everything before the ODL is **per document**. The ODL's only job is the realisation
  *"it did that to all of them, and they all line up."* Corpus-level, not document-level.
- The artifact preview already does found-vs-reconstructed brilliantly. The ODL must not
  compete with it.
- **Vankata 2026-07-23**: playground ODL is a *showcase, not a tool*. No column
  manipulation. 4-5 cols, always-visible descriptions, ~10 rows paginated, frozen header.
  **"Expand/collapse fights one-glance comprehension"** — inline evidence drawers were
  parked for the playground (fine for our own exploration page).
- **Vankata**: rejected the count-up animation — *"we're not selling speed, we're selling
  accuracy"*. An **assembly** animation (rows/cells filling once) is different and was the
  agreed idea to stage the moment; must play once per session and be skippable.
- Storage for per-cell evidence is NOT a blocker: hierarchy is Project → Dataset → File →
  Artifact, ODL hangs off the Project, so a row already knows its file. Per-cell evidence
  would be `{value, artifact_id, page}` captured at write time — a schema question for
  Vova, deferred to V2.

## Data (all verified, extraction complete 2026-08-13/14)

- 14 patents · 376 pages · **6 languages** (ZH/JA/AR/KO/FR/EN) · 7 patent offices
- 157 pages (42%) scanned, no text layer: SA518391052B1, SA522432530B1, TWI592499B
- 337 artifacts: 126 tables, 95 figures, 54 charts, 52 connected findings
- 298 data points recovered from 28 charts across 7 docs
- ODL fields in `demos/process-manufacturing-v2/out/odl.json` (10 fields, two-tier:
  7 universal + material fields at 10-11/14)
- **Row order for first screen** (hardest + fully populated first): TWI592499B(ZH,scan),
  CN115595499A(ZH), JP5523373B2, JP6374864B2, JP6794630B2, JPWO2020262063A1(JA),
  KR102297297B1(KO), EP2038445B1(FR), US11203795(EN), then sparse rows below the fold.

## Files

- `atlas/_assets/playground-onboarding/index.html` — 3 A·C hybrid onboarding variants
  (routing / connected / icon circles). Panel 03 has language+scan badges, difficulty order.
- `atlas/_assets/playground-onboarding/odl-example.html` — **being replaced** by the
  side-panel mock.
- `engagements/_internal/platform-product/artefacts/onboarding-flow/liana-answers-manufacturing.md`
  — answers to Liana, complete except the three items below.
- Generators in scratchpad: `build_odl_v2.py`, `odl_extract.py`, `make_odl_page.py`.

## Open, not mine

1. Retention/deletion policy — **Victor** (highest risk item on the public page)
2. Export/share capability — engineering
3. Whether accuracy is measured at all — **Vankata**. 97% CANNOT be published for this dataset.
4. Drop the 2 Saudi oil&gas patents? They're also both Arabic scans = strongest proof.

## Uncommitted

Pipeline concurrency + `_esc()` fixes in the **engagements** repo, on branch
`severity-grader-validation` (unrelated branch — ask before committing).
Atlas commits done: 49e28dd, 774ccab, 8974fd1.
