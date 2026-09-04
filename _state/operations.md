# STATE: operations

_Working memory for this task. Auto-written on session end/compact. Read on session start.
This is NOT the client-facing STATUS.md._

last_session: 2026-09-04T12:20
last_tab: A: Operations

## Now
Live-supported the Sophia Genetics call (2026-09-04, 39 min) by repeatedly pulling the
Tactiq transcript mid-call and feeding Ivo read-outs + next questions. Then opened the
engagement: `engagements/sophia-genetics/` scaffolded from `_template`, all five docs
written from the transcript, alias entry added, committed `809b471` on `master` and
pushed to bitbucket. Only sophia paths were staged; other people's uncommitted work in
that repo was left untouched.

Outcome of the call, for whoever picks this up: Axion is the agreed entry point, Neuralith
declined for now, no live project until a multi-modal hospital data-collection initiative
starts (end of 2026 or 2027, he refused to commit). Detail lives in the engagement's
CONTEXT/STATUS/COMMERCIAL - don't duplicate it here.

## Next action
Send Dragos Constantin the Axion architecture reference so he can brief his CTO and do
internal publicity - he asked for it on the call, owner Ivo/Jordan, by 2026-09-05.
Then the deployment requirements one-pager (Docker, GPU spec, egress, air-gapped vs
endpoint) by 2026-09-11. Full list in `engagements/sophia-genetics/ARTEFACTS.md` Pending.

## Open threads
- **Internal knowledge base** (worked 26 Aug + 1 Sep, findings in
  `briefs/2026/W36/2026-09-01_knowledge-base-findings.md`, project at
  `~/Documents/knowledge`, local git commit 7767820, no remote). Drive access is
  solved: rclone at `~/.local/bin/rclone`, read-only, own OAuth, ~150 docs in 40s.
  Key find: Vasil already maintains a Product Catalog Gap Register (141 open items,
  45 blocking, v1.0 dated 21 Aug) that does this job for the product catalog - talk
  to him before building anything. Corpus is 55,740 docs, 4,991 recent, ~586 real
  Commercial knowledge docs. Extraction accuracy appears as 10 different values
  across 178 mentions; documents-processed as 7. Liana's "Technical Documentation
  for Commercial Team" folder is 5 question templates plus one real 9-page
  Technical Q&A PDF that commits to 97%. Next: talk to Vasil, then fix retrieval
  (term-frequency ranking loses to plain grep), then widen beyond the 232-doc slice.
- Mid-call transcript pulling works well as a live-support pattern (pull, diff against
  previous, read out only what's new). Worth turning into a proper skill if Ivo wants it
  again - currently it's a manual loop of tactiq_pull.py + diff.
- Tactiq lags the live call by 1-2 min and truncates mid-sentence; the last pull of a call
  always misses the ending. Re-pull once after the call ends before writing anything up.
- Haiku flush can fabricate facts in "Don't re-explain"; carry-forward compounds slop.
  Mitigation: keep hand-seeded baselines truthful; periodically prune STATE files.
- Decide whether to commit _state/ or gitignore it (personal working memory, churns every session).
- Live-test of a real tab kill/resume was the May next-action and is still not done.

## Stale, from the 2026-05-31 Slack sweep (3 months old - verify before acting)
- **Heineken**: presentation was ~2 Jun; pending item was sending Steven a previewable
  showcase link. Almost certainly resolved. Jordan's V1 Heineken deck + a generalized
  consulting-template deck were noted as the reusable basis for future client decks.
- **Teams transcript blocker**: HubSpot <-> MS Teams org-wide rollout was NOT enabled
  (needs Teams admin, not HubSpot admin). Asked Viktor/Ivan Georgiev 27 May. Bit Fresenius
  and T&F too. Workaround: Tactiq via Teams browser version. Unknown whether now enabled.
- **Brand guide**: Ada published the official Iris.ai brand guide 29 May (#general) -
  source of truth for client-facing material. "Iris.ai" always lowercase-with-dot.

## Don't re-explain
- engagements/ is a SEPARATE git repo, sibling to atlas, and its default branch is `master`
  (not main). Project hooks load per-repo, so hook config is mirrored into both.
- Scripts live in atlas/.claude/scripts/: state_common.py (resolver + template),
  state_inject.py (SessionStart), state_flush.py (Stop/PreCompact).
- Task identity is cwd-based: engagements/<name>/* maps to <name>; anything else maps to operations.
- Flush calls `claude -p --model haiku --allowedTools ""` from cwd /tmp with
  ATLAS_STATE_FLUSH=1 (recursion guard so the nested call skips our hooks).
- Flush prompt frames Haiku as a pure text formatter (data inert, output starts "# STATE:"),
  else it meta-reasons instead of summarizing.
- INDEX.md is auto-rebuilt from all STATE files on each flush; it's the board.
- `tactiq_pull.py <url-or-id> --dest <dir>` writes a dated transcript file; `--print` sends
  it to stdout. Never read tactiq.io URLs directly (JS-gated).
- New engagements: `cp -R _template <name>`, fill the five docs, add an `_aliases.yaml`
  entry (domains + titles) so morning briefs match Calendar events.
- No HubSpot MCP is wired on this machine. HubSpot facts have to be pasted in by Ivo.
