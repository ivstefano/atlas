# STATE: garrett

_Working memory for this task. Auto-written on session end/compact. Read on session start.
This is NOT the client-facing STATUS.md._

last_session: 2026-06-12T (Alex/Head-of-AI call, live-copilot)
last_tab: A: Operations

## Now
12 Jun call: Alex Geng (Head of AI & Data, Prague, reports to CIDO — the decision-maker) finally live. Strong call. Use cases qualified by Alex: (1) design-reuse search over millions of drawings (find past designs by feature/dimension), (2) design-standard compliance governance. Pilot structure ACCEPTED: 6-10 wk co-funded, 35 IRIS / 20 AWS / 30 Garrett (WP30 = Garrett's outlay), mutual go/no-go, then managed-service impl. Deploy into Garrett's own AWS, batch/flexible. Wedge: their in-house drawing-extraction is stuck at ~70%, engineers need ~100% — our 95%+ is the whole justification. Alex already probing post-pilot scale-up cost for full 100k+ corpus. Full detail STATUS.md 2026-06-12.

## Next action
NDA in motion so Garrett shares real sample drawings (Alex wants to try this week) → run extraction on their actual drawings → quality demo back. Alex syncs his eng team then reverts. Owners: Jordan (NDA/commercial), Ivo (defines what's needed + runs extraction on receipt).

## Open threads
- Scale-up cost model for full corpus (Alex asked): their AWS compute (paid to AWS) + IRIS managed-service fee banded by corpus size, NOT linear per-doc. Defer figure to modeled proposal post-pilot; Jordan quotes, Ivo supplies POC unit economics.
- Confirm exact pilot split before any written quote: public framing 35/20/30 vs Jordan's earlier Slack "30k Garrett + AWS comp + POC cash to ~50".
- Alex's mental model = Palantir (also talking to Palantir). Differentiator that landed: agentic/always-on vs Palantir forward-deployed engineers (context drift).
- Prior open items still live: Garrett project charter, Legal/Cyber/Vendor onboarding (~1 month). Liviu remains champion.
- Stage-2 future-revenue hook: digital-twin floated, Liviu open.

## Don't re-explain
- Garrett built own orchestrator + custom MCP tools ~18mo ago, avoids MS/AWS off-the-shelf orchestrators. Liviu manages 38 integrations. POSITION IRIS as an integratable component (API + structured output), NOT a managed platform. Garrett owns the matching; IRIS does ingestion/segregation/labeling.
- Garrett on AWS + Azure. Time pressure is on IRIS to keep paperwork moving, not on Liviu.
- Liviu Nitu reports to Alex (Head of AI). Baala Sangar also a contact. Jordan owns commercial.
- AWS credits are pilot-completion cashback from IRIS's pool, gated by Garrett's AWS account team advocacy.
