# Fresenius CMC — Working Group Session prep
**Today 10 Jun, 16:00-17:00 BG (Google Meet). Jordan organizing.**

## Who's on
- **Fresenius:** Sathya Upendran (Manager Reg Affairs Pharma, the SME + data owner), Sanja Matern (coordinates, reviewer-perspective, owns the medical-device parallel use case), Gerome Fischer (champion/anchor, tentative/optional today).
- **IRIS:** you, Jordan (commercial lead), Vankata/Ivan Tsenov (CPO, technical).
- Calendar title is "Kick-off Pharma CMC / Working Group Session" — this is the next scoping session promised on the 2 Jun call, where IRIS shows what it built from the uploaded data.

## Where we actually are (the real state, not the stale STATE files)
- We are **scoping**, not in PoC. No PoC contracted yet.
- Sathya uploaded **5 files on 5 Jun** via Vankata's secure Neuralith link. They're in `1_pre-scoping/data/Fresenius CMC 08-06-2026/`.
- **Yesterday (9 Jun) we extracted them.** Three artifacts in `1_pre-scoping/extraction/`: `cienby_extraction.json`, `consistency_audit.md`, `QOS_2.3.P_draft.md`.

## What the 5 files are
All five are **finished, authored dossier sections** for one product — Cienby (trisodium citrate dihydrate, a 3-ingredient salt-water infusion, 1,500 mL bag). All clean digital PDFs, no scans. ~16 pages total. eCTD sections: 3.2.P.1, 3.2.P.2 (partial), 3.2.P.5.1, 3.2.P.5.4, 3.2.R.1.P.

Key nuance to keep straight on the call: **they're inputs to us, but outputs of Fresenius's authoring process** — the polished right-hand side of the messy-source → finished-section arrow. We have not seen the raw feedstock (executed batch records, CoAs, validation reports) the author actually starts from.

## What we built (and can show)
1. **Structured extraction** — 5 PDFs → one eCTD-keyed table, every record tagged to its source section. Proof-of-mechanism on a simple product.
2. **Cross-section consistency audit** — the strong demo. Every value appearing in >1 section, checked. All release-critical numerics reconcile. Surfaced **4 reviewer-grade flags** (particle-limit row order flips between 3.2.P.5.4 and 3.2.R.1.P; sodium 408 vs citrate 136 sit close enough to misread; unlabeled trailing digit in reconciliation "288 / 2"; clinical batch E3LB141 reuses one DS lot number across Merck + Fresenius columns — confirm vs transcription). None release-blocking. Pitch: "the 4 things a reviewer queries, found in seconds, not in an FDA deficiency letter."
3. **Auto-drafted Module 2.3 QOS** — overview summary grounded in the 5 sections, every sentence tagged to source, untagged claims auto-flag. The "draft generation, human verifies" North Star in miniature.

## How it maps to their success criteria (Sanja's, from 28 May)
- **#2 (<5 cardinal errors/review):** consistency engine pre-finds candidate errors — done, demonstrated.
- **#3 (25% fewer FDA queries):** cross-section disagreement is a top query source, removed pre-submission — done, demonstrated.
- **#1 (10% faster drafting):** QOS draft shows the mechanism, but **not yet provable** — needs the raw input side.

## The honest framing (lead with this, don't oversell)
"We extracted everything in the 5 files, confirmed your numbers reconcile, found 4 reviewer-grade flags, and auto-drafted the 2.3 overview. But this is one **simple** product in **finished** form — it's proof-of-mechanism, not proof-of-scale. To scope the PoC accurately we need representative variety and the messy input side."

## The ask back to Fresenius (this is a SCOPING ask — variety, not volume)
Sanja already asked for representative variety incl. complex/scanned docs; this aligns. Priority order:
1. **Executed batch records** (the raw filled-in MX-R-BPR041 sections 1-10) — the messy input; unlocks the drafting-time case (#1).
2. **One complete prior submission** — the format/output target, to show input→output not just tidy-the-output.
3. **3.2.P.3 (Manufacture) + 3.2.P.8 (Stability)** — the high-volume sections; prove scale/complexity, not a 3-ingredient salt.
4. **One complex/scanned/non-standard doc** — we've only seen clean digital; need one ugly one to prove the OCR/messy path.
5. **3.2.S sections** when the restriction clears (Sathya: colleagues on holiday, update "next week" per his 5 Jun email).

## Coverage reality (for your own read, don't necessarily volunteer the number)
~15% of one product's Module 3 by structure; ~5-10% by extraction value (they sent the easy, finished sections). The volume + authoring effort lives in the missing sections. For scoping this is fine — we just need the hard examples next, not the whole dossier.

## Process / governance threads live from 2 Jun
- **Steering committee** being formed: Gerome + Sanja + Sathya + Stepan + Renee (Fresenius side); Jordan + Vankata (IRIS). Monthly. Sathya to send names + emails + titles.
- **Project group**: weekly/async; delivers the work. Sanja observing (optional invite).
- **IT/data contact**: Sanja to check with Gerome whether to involve ITS business partner now vs at PoC stage. Useful to surface environment constraints early in regulated context.
- **Data handling**: secure portal (24-48hr link), SA-only access, all data deleted post-PoC (GDPR — confirmed to Sanja). Real-state would integrate SharePoint/RIMS.
- **Sathya's urgency**: "as soon as possible," wants it running — but no hard external deadline ("nothing to present to anybody right now").

## Likely agenda today
Show the extraction + consistency + QOS artifacts (proof of mechanism on real data), get their reaction/alignment that this is what good looks like, then make the variety ask so the next data drop lets us scope effort + price. Next step after this would be a more formal proposal/SoW (Vankata's 2 Jun framing).

## Open questions to resolve on the call
- Confirm the 4 consistency flags with Sathya — real issues or our misread? (especially the E3LB141 lot-number reuse).
- Which output section do they want the PoC to generate (they need to define this)?
- Can Sathya send one executed batch record + one prior submission as the matched input→output pair?
- Format of raw inputs (PDF / Word / system export)?
