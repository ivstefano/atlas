# STATE: aumovio

_Working memory for this task. Auto-written on session end/compact. Read on session start.
This is NOT the client-facing STATUS.md._

last_session: 2026-05-28T11:17
last_tab: A: Aumovio

## Now
100/100 corpus OCR'd + extracted. Reference + corpus predictions merged into unified dataset, exported to Phil's V4 template (100-doc, three sections). CJK text sanitized in export. 83 docs Opus-judged (27 High / 52 Med / 1 Low).

## Next action
Run overlay.yaml reconciliation against Phil's GT once remaining GT lands; resolve the 7 known Phil-GT quirks via the overlay rather than editing predictions.

## Open threads
- Convergence pitch: port my prompts INTO Martin's deployment shell (my pipeline 99.6% F1 vs Martin's 62.7% on same docs). Blocked on Viktor, who pushed Alex toward Martin's.
- 16 corrupt docs re-OCR'd 2026-05-28, may need re-judge.
- 2 service contracts correctly 0-row, keep flagged so they aren't treated as misses.

## Don't re-explain
- Extractor V2 (OCR-first) at engagements-worktrees/extractor-v2/, branch extractor-v2 on bitbucket, commit a9d39c6.
- Qwen 27B host: 54.76.91.34 (Rosen-hosted, 192K ctx). Hybrid prompt Rules A-E. qwen_iterate.py 3-phase loop.
- Chandra OCR GPU: instance i-06aa73900ca43c1e9 eu-central-1 ("DeepSeek OCR Experiment" misnomer). SSH key ~/Documents/vpn/test_instances.pem. SSM SendCommand denied.
- Phil GT has 7 quirks (SPR vs Contracted cols, blanks, rounding drift, unreliable lifetime). v4_cx_expected.yaml + Ontology sheet. Phil only deep-reviewed volumes; other V4 cells unreviewed pre-fills.
- Per-OEM business rules: VW group 48 weeks/yr, shared EOP across variants, Planvolumen-sum, German flex phrasings.
- Client-facing naming: never expose Chandra/vLLM/GPT/run IDs. Map to Axion / Neuralith / Iris.ai models.
