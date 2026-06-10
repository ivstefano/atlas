# Fresenius CMC — their problem in plain terms (call primer)

Companion to the working-group prep brief. This one is just: what hurts, why, what we can do about it, what to ask. No jargon unless I define it.

## What Fresenius actually does here

They make drugs and medical devices. Before they can sell one, a regulator (FDA in the US) has to approve it. To get approval they submit a giant dossier proving the product is made consistently, safely, and to spec. That dossier is the "submission."

The part we're working on is called **CMC** — Chemistry, Manufacturing, and Controls. In plain terms: "here is exactly what's in the product, how we make it, and how we prove every batch is correct." It's the manufacturing-evidence half of the application.

The dossier follows a fixed international filing format called **eCTD**, split into numbered modules. We only care about two:
- **Module 3** — the full technical detail (the long, evidence-heavy sections).
- **Module 2.3** — a human-written executive summary of Module 3, called the **QOS** (Quality Overall Summary). Same facts, condensed for the reviewer.

Inside Module 3 the sections are numbered like a filing system:
- **3.2.S** = the drug substance (the active ingredient).
- **3.2.P** = the drug product (the finished thing in the bag/vial). This is the part Fresenius owns and controls, so it's our main target.
- **3.2.R** = regional add-ons (e.g. the actual batch-manufacturing records for a specific market).

## The pain, in one paragraph

Writing one of these submissions takes a person **3 to 6 months**. An author sits with a pile of messy source documents — filled-in batch records, lab certificates, validation reports, supplier specs, some of them scanned PDFs — and by hand turns them into clean, structured, regulator-ready sections. It's slow, it's expensive, and it's error-prone: if a number on page 4 doesn't match the same number on page 40, the FDA sends back a **deficiency query**, which costs weeks and delays the product reaching the market. Sathya is living this right now — he mentioned he had ~60 FDA queries due in a single week.

So there are really two pains stacked on top of each other:
1. **Too slow / too manual.** Months of skilled human time per submission.
2. **Quality leaks.** Inconsistencies slip through, the FDA catches them, and every catch is a delay.

## What they want (their words, translated)

- **Faster time to market.** Same quality, far fewer person-hours. Sanja's vivid version: a draft that takes a person 10 hours should take the system ~10 minutes.
- **Fewer FDA queries.** Catch the self-contradictions *before* submitting, not after the regulator finds them.
- **Human stays in charge.** They don't want the AI to file anything. They want the AI to write the first draft with a visible evidence trail, and a human reviews it. Vankata's framing: creating a document is ~10x the effort of reviewing one, so let the machine create and the human check.

Their three success numbers (from Sanja, 28 May):
1. 10% faster drafting.
2. Fewer than 5 "cardinal" (serious) errors per human review.
3. 25% fewer FDA deficiency queries in production.

## What we can actually do with their documents

They sent us 5 finished sections for one simple product (Cienby — basically a 3-ingredient salt-and-citrate infusion bag). From those we built three things that map straight onto their pain:

1. **We read all 5 PDFs and turned them into one structured, queryable table** — every fact tagged back to the section it came from. This is the raw capability: the system understands the dossier, not just stores it.

2. **We cross-checked every number that appears in more than one section.** All the release-critical numbers agree (good — their dossier is clean). And we surfaced **4 things a reviewer would query** — a particle-limit table with its rows in a different order in two places, two similar numbers (sodium 408 / citrate 136) sitting close enough to be misread, an unlabeled stray digit in a reconciliation table, and one clinical batch that reused a single lot number across two supplier columns. None are show-stoppers. The point: **these are exactly the nitpicks that turn into FDA letters, and we found them in seconds.** That's success-criterion #3 made real.

3. **We auto-drafted the Module 2.3 QOS** (the executive summary) from those 5 sections, with every sentence tagged to its source and anything unsupported auto-flagged. That's the "machine writes the first draft, human verifies" model in miniature. That's success-criterion #1's mechanism.

**The honest line to hold on the call:** this proves the *mechanism* works on real regulated data. It does not yet prove it works at *scale or on the hard stuff* — because the 5 files were the easy ones: one simple product, all clean digital, and all already-finished (the polished output, not the messy input an author actually starts from).

## Why that "easy files" caveat matters (and how to say it without deflating)

Think of every section as a `messy inputs → finished section` arrow. They sent us the right-hand side: the finished sections. To prove we can *save authoring time* (criterion #1), we need to see the left-hand side too — the raw filled-in batch records and lab certs the author wrestles with. With both sides we can show input → output, which is the actual time-saver. With only the output, we can summarize and consistency-check, but we can't prove we replaced the months of authoring.

Say it as: "What you sent proves we understand your dossiers and can catch reviewer issues. To prove we can cut the *drafting* months, we need to see one section's raw inputs and its finished version side by side."

## What to ask on the call (in priority order)

1. **One executed batch record + the finished section it fed into** — the matched input→output pair. This is the single most valuable thing; it unlocks the time-saving proof.
2. **One complete prior submission** — so we know exactly what "finished and accepted" looks like as a target.
3. **The two high-volume sections: 3.2.P.3 (Manufacture) and 3.2.P.8 (Stability)** — these are where the real bulk and complexity live, not a 3-ingredient salt.
4. **One ugly document** — a scan, a non-standard layout. We've only seen clean digital PDFs; we need one hard one to prove the messy-document path.
5. **3.2.S (drug substance)** whenever the restriction clears — Sathya said colleagues were on holiday, update expected "next week."

Plus the four consistency flags: walk Sathya through them and confirm they're real reviewer issues vs. our misread — especially the reused lot number on batch E3LB141.

## One-sentence version if someone asks "so what is this?"

"We take the pile of manufacturing documents an FDA submission is built from, draft the regulator-ready sections automatically with a full evidence trail, and catch the internal contradictions before the FDA does — so a 3-to-6-month manual job gets faster and cleaner, with your reviewer still signing off."
