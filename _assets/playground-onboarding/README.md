# Playground demo — onboarding intro screen mockups

Design alternatives for the **Process Manufacturing demo onboarding page** (the in-product
screen a magic-link lead lands on before the guided tour starts).

Open `index.html` in a browser. No build step, no server needed.

## Why these exist

Michael (Dezea) shipped a first design on 2026-08-12 (`IRIS-Platform-Playground-14-Onboarding-Intro`).
Vasko raised the open question in `#ux_platform`: *"is this the best in the perspective of UX?
What to put on the upper part of that page: numbers, graph or anything else?"*

The diagnosis: the kicker promises **"This is the finished output"** but the hero shows a tally
of artifact counts. Counts say how much came out; they don't show what it looks like or why
you'd want it. The UI design database independently recommends **Before-After Transformation**
for this exact job ("visual proof of value, 45% higher conversion").

These five options explore what should carry the claim instead.

## The options

| | Approach | Notes |
|---|---|---|
| **A** | Before/after split | Raw CN filing (desaturated) → structured table (full colour). The recommended pattern. Has a real output table, so Liana's "the table above" line is literally true. |
| **B** | Output first | No "before" at all. Real table as hero, fading at the bottom edge; source filings as mono pills above. Cheapest to build if a table crop exists. |
| **C** | Three-stage funnel | Stages are the hero, flow line running through the middle of the row. Answers Michael's "learn the steps" purpose. |
| **C·E** | C reduced by Maeda's laws | Same content, ~90 words instead of ~250. Section headers gone, stage prose hidden behind hover, time promise promoted. See caveat below. |
| **D** | Artifact proof grid | Keeps the counts but each shows its own artifact (sparkline, rows, thumbnails). Smallest change from Michael's current design. |

## Copy

All five carry **Liana's marketing copy verbatim** (Iris-Playground-Landing-Copy_Product.docx).
The only typographic liberty is "search in English" set in iris-violet.

Two exceptions, both structural labels the copy doc doesn't cover because it wasn't written
for those layouts — **these need copy from Liana**:
- Option A pane labels: "What you upload" / "What you get"
- Option B source row: "Read from"

## Numbers — source of truth

Taken from the **Neuralith Extracted Artifacts panel**, not from the pipeline output directories:

| Artifact | Count |
|---|---|
| Tables | 103 |
| Charts | 70 |
| Images | 31 |
| Brands | 8 |
| Cross-references | 27 |
| **Total** | **239** |

Corpus: 8 patents · 178 pages (range 9–47) · 2 languages (EN + ZH).

**Do not re-derive these from `engagements/_demo-builder/demos/process-manufacturing/out/`.**
Those directories contain pipeline intermediates (JSON sidecars, `_semantic.png` overlays) and
counting them overstates images ~3x and understates tables ~2x. The platform applies its own
filtering. Read the product panel.

## Design system

Built on `atlas/Neuralith Design System/` — Saira (UI) / Poppins (body) / Aber Mono (code),
navy `#1c2550` + iris-violet `#3e4cd5`, hairline borders `#07074f @ 15%`, one accent glow on the
primary CTA. `colors_and_type.css` and `fonts/` are copied in so the file opens standalone.

**The stat-strip icons are hand-drawn stand-ins.** In production use the real app sprite:
`nlf-icon-document-patent`, `-document-pdf`, `-document-chart`, `-document-table`,
`-document-image`. They exist in `assets/icons/svg-sprite.svg` but are nested `<svg>` in
`<defs>` with hardcoded fills, so `<use href>` won't recolor them for hover states.

## Open issues to resolve before build

1. **"The table above"** — Liana's copy says the tour ends at "the table above". True in A and B
   (both show a table); false in C, C·E and D. Either pick A/B or Liana adjusts the line.
2. **Figures vs Images** — the copy says "Figures carrying detail the body text never states";
   the product panel says **Images**. Vocabulary mismatch visible one click apart.
3. **Scroll vs one screen** — Michael's brief was "no scrolling". With the full copy, all three
   stage paragraphs and a chart, one viewport isn't achievable. Cutting copy is Liana's call.
4. **C·E hover** — hiding stage prose behind hover means touch users never see
   "every value traceable to a page and a paragraph", one of the strongest lines. Cards are
   keyboard-focusable, but tablets get the short version. Use tap-to-expand if tablet traffic matters.
5. **Numbers are provisional** if the corpus is expanded. Drive the stat block from Figma
   variables so it doesn't force a redesign.

## Recommendation

**A** for the full version, **D** if the Wednesday deadline is tight (smallest change from what
Michael built). **B** is strongest if a real table crop can be pulled from the demo bundle.

From C·E, two changes are pure gain with no information loss and are worth taking into whichever
option ships: merge the caption line into the stat strip, and promote "About 8 minutes" from grey
small-caps to a stated promise next to the button.
