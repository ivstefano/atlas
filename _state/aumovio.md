# STATE: aumovio

_Working memory for this task. Auto-written on session end/compact. Read on session start.
This is NOT the client-facing STATUS.md._

last_session: 2026-06-01T (commercial Fast Start + review-session setup)
last_tab: A: Operations

## Now
100/100 corpus reviewed + hand-fixed for correct flagging, SENT to Norbert + Phil 28 May (two files: combined extractions from the PoC + latest-results-only). Viktor agreed (Tue 26 May, w/ Petar) to SHOW Bedrock + Opus results for now, improve Qwen results in Full Implementation later. Petar happy with the results. On 1 Jun Fast Start call, Jordan asked directly whether improved results hit Aumovio's acceptance criteria — I confirmed yes (everything they asked for, uncertainty flagged). Jordan's directive: stop leaving it to async email, set up a proper live REVIEW SESSION with Norbert + Phil. Jordan leans aggressive on booking time.

BOOKED 1 Jun: Aumovio results-review call Wed 3 Jun 12:15-13:15 CET. Calendar invite sent (Meet meet.google.com/btw-sucv-cta, event id a76sjqgrn4f9ibs898jm9q276g). Attendees: Norbert + Phil (external), Jordan, Vankata, Petar required, Victor optional. Confirmation email SENT into the MoveIT thread same day.

## Next action
Prep the Wed 3 Jun 12:15 CET review: walk Norbert + Phil through results vs their acceptance criteria, flagging confident vs uncertain cells. Still pending separately: overlay.yaml reconciliation against Phil's GT once remaining GT lands; resolve the 7 known Phil-GT quirks via overlay, not by editing predictions.

## Open threads
- Convergence pitch: port my prompts INTO Martin's deployment shell (my pipeline 99.6% F1 vs Martin's 62.7% on same docs). Blocked on Viktor, who pushed Alex toward Martin's. Note: Viktor's "Bedrock+Opus now, Qwen later" call partly sidesteps this for the deliverable.
- 16 corrupt docs re-OCR'd 2026-05-28, may need re-judge.
- 2 service contracts correctly 0-row, keep flagged so they aren't treated as misses.

## Don't re-explain
- Extractor V2 (OCR-first) at engagements-worktrees/extractor-v2/, branch extractor-v2 on bitbucket, commit a9d39c6.
- Qwen 27B host: 54.76.91.34 (Rosen-hosted, 192K ctx). Hybrid prompt Rules A-E. qwen_iterate.py 3-phase loop.
- Chandra OCR GPU: instance i-06aa73900ca43c1e9 eu-central-1 ("DeepSeek OCR Experiment" misnomer). SSH key ~/Documents/vpn/test_instances.pem. SSM SendCommand denied.
- Phil GT has 7 quirks (SPR vs Contracted cols, blanks, rounding drift, unreliable lifetime). v4_cx_expected.yaml + Ontology sheet. Phil only deep-reviewed volumes; other V4 cells unreviewed pre-fills.
- Per-OEM business rules: VW group 48 weeks/yr, shared EOP across variants, Planvolumen-sum, German flex phrasings.
- Client-facing naming: never expose Chandra/vLLM/GPT/run IDs. Map to Axion / Neuralith / Iris.ai models.
