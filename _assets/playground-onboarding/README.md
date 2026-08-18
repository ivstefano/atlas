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

## Client evidence

[CLIENT-EVIDENCE.md](CLIENT-EVIDENCE.md) ranks what clients actually ask for when they look at
extracted data, by how many distinct accounts raised each theme. Read from every client transcript
on file: 26 accounts, 41 meeting sets, ~1.15M words.

Headline: the top four themes are all served by showing the finished table rather than a count of
artifacts. Seeing where each value came from ranks fifth on frequency but first on function, since
checking, trust and accuracy all depend on it.

The four-client block at the top of `odl-example.html` is the earlier, narrower version of the same
argument.

## Numbers — source of truth

Verified per document against `manifest.json`, the source the platform ingests:

| Artifact | Count |
|---|---|
| Tables | 126 |
| Figures | 95 |
| Charts | 54 |
| Connected findings | 52 |
| Page marks / branding | 10 |
| **Total** | **337** |

Corpus (**v2 set**): 14 patents · 376 pages (range 7–59) · 6 languages, 5 scripts ·
7 patent authorities · 2012–2025 · **157 pages (42%) scanned images with no text layer**.

Read from `manifest.json`, the same source the platform ingests.

**The old 8-document set is retired.** It was 8 docs of which 3 were academic journal papers,
not patents, and its counts (Tables 103 / Charts 70 / Images 31 / total 239) are wrong even for
itself. Anything quoting 8 patents, 178 pages or 2 languages is stale.

**Do not re-derive these from pipeline `out/` directories.** Those hold intermediates (JSON
sidecars, `_semantic.png` overlays); counting them overstates figures and understates tables.
Read `manifest.json`, or the product's Extracted Artifacts panel.

**No accuracy figure is cleared for this corpus.** No ground truth was built and no benchmark
run. The 97% figure comes from other engagements and must not appear on this page. Same for any
time-saving or person-hours multiplier. Source:
`engagements/_internal/platform-product/artefacts/onboarding-flow/liana-answers-manufacturing.md`.

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
