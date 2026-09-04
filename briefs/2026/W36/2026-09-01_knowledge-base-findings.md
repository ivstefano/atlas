# Internal knowledge base: what the Drive actually contains

Worked 2026-08-26 and 2026-09-01, following the 25 Aug call
"Iris.ai Internal Knowledge Repository" (Vankata, Viktor, Jordan, Steven,
Vasil, Ivo). Transcript: app.tactiq.io/transcripts/BlyCMOLx4hxW1OBIfevx

Project lives at `~/Documents/knowledge` (local git, no remote, not pushed).

## The headline

Vasil is already doing this work, formally. `Product/Knowledge base/
Platfotm-draft/00-gap-register.docx` is the **Product Catalog Gap Register
v1.0**, owner Vasil Shivachev, generated 21 August 2026: 141 open items
(45 blocking, 92 material, 4 minor), tracked by ID, with severity, owner and
resolution notes. Twenty-three closed in the last round.

Vasil was in the 25 Aug call. The room discussed building a knowledge
repository while one participant was five days into maintaining the artefact
that work would produce. Nobody connected the two.

**Talk to Vasil before building anything.** Highest-value move available and
it costs nothing.

## Access is solved

rclone at `~/.local/bin/rclone`, read-only scope, own OAuth, no admin needed.
Installed standalone: Homebrew on this machine is owned by user `ivstefano`
while Ivo runs as `iris`, so `brew install` fails on permissions and chasing
it is a dead end.

Bulk export runs at ~150 documents in 40 seconds. Text extraction, seconds.

The `.gdoc` stub problem that looked like the blocker applies to under a tenth
of the corpus: of 4,991 documents modified in the last year, only 440 are
native Google files. The other 4,551 are real `.docx`/`.pptx`/`.xlsx`/`.pdf`
that were readable from the mount all along.

## Corpus size

Whole Drive, counting real binaries as well as native Google files:
**55,740 documents**, not the 6,902 from the first pass.

| Bucket | Count |
|---|---|
| stale (>1yr) | 43,475 |
| recent (<=1yr) | 4,991 |
| archived | 3,364 |
| sensitive: investor/board | 1,625 |
| junk (untitled, copy of) | 874 |
| sensitive: personal/HR | 693 |
| sensitive: contracts/NDA | 618 |
| noise (transcripts, notes) | 100 |

Recent by area: Commercial 2,906, Product 1,407, Finance 577, Operations 81,
Research 20.

Filtering Commercial down: 1,014 documents, minus sensitive and meeting noise
= 805, minus client payload (DXF, scoping data) = **586 real knowledge docs**,
of which **150 carry outward-facing claims**. The ~100 estimate from the first
pass holds up.

## Contradictions found

From my scan plus Vasil's register.

**Product count.** Brand guide lists three products; July onboarding says do
not position RSpace. Vasil's ruling: RSpace is a use case, not a product
(Axion data with a Neuralith interface). Closed five gaps. He calls it "the
longest-running conflict in the catalog."

**Positioning word.** "Contextualisation" replaced "unification" in July 2026,
but the brand guide, the stated source of truth for customer-facing material,
still carries "Unified Data Readiness Layer".

**Extraction accuracy: 10 distinct values, 178 mentions.** The same
"outperforms human experts at X% accuracy" slide appears as 94%+, 95%+, 96%+,
97%+ and 98%. `AWS Summit Warsaw v2.pptx` says 96% on its title slide and
95%+ on a later slide. `Iris.ai Context Control AI Foundation.pptx` carries
>95%, 97% and 80%.

**Documents processed: 7 distinct values.** 330M+ (12 docs), 160M+ (6),
150M+ (8). `level-1-neuralith.docx` says 350M and labels it honestly as
"architectural capability, not a delivered instance". The Technical Q&A PDF
says 300M+, scoped to research articles and patents. These may be counting
different things, which is the actual problem: a Claims sheet needs a
definition column, not just a value column.

**Evaluation metrics: 20, 22, 27 or 3.** The Axion battlecard alone says 22
in one answer and 27 in another.

**Unsourced figures Vasil has flagged:** "more than 50 connectors" (press
coverage and brand guide; engineering demonstrates five sources), 50-60%
regulatory translation speed, 50% cloud-migration figures attached to a
solution rated Early with no PoC finished, 80% GTM acceleration ("cannot be
defended without a definition"), and 96%/35% escalation figures that come
from an awards submission rather than a delivery record.

**Consistent:** 68 languages (42 docs) and 10+ years. Vasil notes 68 is
extraction coverage and does not transfer to translation, which is a
language-pair problem.

## Liana's folder is not a source of truth

`Commercial/Technical Documentation for Commercial Team/` looked like an
existing canonical set: six documents, all updated 16 Jul 2026, topics
matching exactly what Vankata asked for.

Five of the six are **79-95 words each and contain only questions**. They are
interview templates by Liana (CMO), marketing wanting consistent positioning.
Example, from the accuracy document: "The 97%+ extraction accuracy figure:
what exactly does it measure, on what dataset, and how was it evaluated?"

The sixth, `Technical Q&A_ Iris.ai Knowledge Layer.pdf`, is real: 9 pages of
substantive argument on how the knowledge layer differs from RAG, why a
foundation model will not subsume it, where accuracy degrades and the four
failure modes. It commits to **97%** with a derivation ("not a benchmark
artifact... a production measurement across deployed systems") and states
**300M+ research articles and patents in 68 languages**.

So the answer document exists, says 97%, and the sales decks say 94-98%.
Caveat: the 97% is asserted but not sourced, which is exactly what Liana's
template asks for.

## Question test

232 documents, 625k words. Five questions a salesperson would ask.

Answerable: is customer data used for training (unambiguous, "Client data is
never used for model training"); deployment options (`level-0-platform.docx`
gives four models with who each is for, better than any deck); which
connectors are real (five demonstrated, each with proof); what is the price
(eight pricing documents, which is itself the answer).

Not answerable: what accuracy figure to quote. Ten values, no document ranks
above the others. A missing decision, not a missing feature.

## What this changes

The 25 Aug room assumed no source of truth exists and one must be built.
Two partial ones already do: Liana's positioning folder and Vasil's gap
register. Neither is connected to the other, or to the sales decks where the
wrong numbers keep getting used, and nobody in that meeting mentioned either.

At ~600 documents the corpus fits grep-plus-reading. No vector store, no
graph, no embeddings needed for v1. The bottleneck is deciding the numbers,
and no retrieval architecture substitutes for that.

## Open questions

- Do Vankata, Liana and Vasil know about each other's work?
- Who decides the accuracy figure, and what does each volume number count?
- Is the Drive still in a personal account? Viktor said so on 25 Aug and
  nobody picked it up; it blocks every shared-drive integration discussed.
