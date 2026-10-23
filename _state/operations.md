# STATE: operations

_Working memory for this task. Auto-written on session end/compact. Read on session start.
This is NOT the client-facing STATUS.md._

last_session: 2026-10-23T12:00
last_tab: Schneider deep dive

## Now
Live-supported the Schneider Electric India deep dive (2026-10-20, Kiran Vyas) from this
tab: prep brief `briefs/2026/W43/2026-10-20_schneider-deep-dive.md`, layman explainers on
data governance / poisoning / OT, mid-call Tactiq pulls, coverage table vs the
iris-capabilities map (~25% realistic). Opened `engagements/schneider-electric/` (commit
f6f7238). Verdict logged 2026-10-23 in its STATUS: low-value lead, Kiran sold his own
vision (national AI security ops centre), no budget, no owning team, off capability map.

Previous (2026-09-04): Sophia Genetics call support + engagement opened; detail in
`engagements/sophia-genetics/`.

## Next action
Send the written Schneider deal-stopper flag (S2 off capability map, S3 vague ask, no
budget) to Vankata + Steven, owner Ivo, by 2026-10-23. Older: Sophia Genetics pending list
in `engagements/sophia-genetics/ARTEFACTS.md` (unverified whether done).

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
- PRIVATE: Ivo's Oct 2026 personal check of Iris.ai finances lives ONLY in `__finance/` (gitignored) + memory `iris-finance-check`. Never write figures, salaries, loans or fundraising details into this STATE file (it is committed). At most: "personal finance check, see __finance/README.md".
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
- HubSpot MCP wired 2026-10-19 (read-only). Query deals/contacts/notes directly; see _hubspot_mcp_setup.md.
