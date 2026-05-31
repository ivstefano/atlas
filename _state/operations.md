# STATE: operations

_Working memory for this task. Auto-written on session end/compact. Read on session start.
This is NOT the client-facing STATUS.md._

last_session: 2026-05-29T11:10
last_tab: A: Operations

## Now
Built durable per-task working-memory system. STATE.md per task in atlas/_state/, SessionStart inject hook orients fresh tabs, Stop/PreCompact flush hook distills sessions via headless Haiku. Hooks wired in both atlas/.claude/settings.json and engagements/.claude/settings.json (separate repos, both call atlas scripts by absolute path). Pipeline tested end-to-end and working.

## Next action
Live-test a real tab kill/resume: from an engagement folder, end a session, confirm flush writes STATE, kill terminal, relaunch, confirm SessionStart injects it.

## Cross-engagement (from Slack sweep 2026-05-31, week of 23-29 May)
- **Heineken**: presentation is ~Tue 2 Jun. Jordan flagged Mon 1 Jun = "aggressive sprint, only day before". Steven asked Ivo (DM 29 May) for the showcase as a previewable link + whether NDA blocks showing Heineken's own docs (Ivo: likely yes per Liana → use other form docs in same format). PENDING: send Steven the previewable link. Jordan's V1 Heineken deck + a generalized consulting-template deck are the reusable basis for future client decks.
- **Teams transcript blocker**: HubSpot ↔ MS Teams org-wide rollout NOT enabled (needs Teams admin, not HubSpot admin). Cost ~1-2 days reconstructing lost Heineken transcripts. Asked Viktor/Ivan Georgiev 27 May to enable. Bites Fresenius + T&F too (both Teams-first). Workaround: Tactiq via Teams browser version. CHECK if enabled yet.
- **Aumovio acceptance**: Vankata wants Jordan + Steven alerted that Aumovio nears acceptance criteria. (tracked in aumovio STATE)
- **Brand guide**: Ada published official Iris.ai brand guide 29 May (#general) — source of truth for client-facing material, new Slides/doc templates. "Iris.ai" always lowercase-with-dot. Use for any future deck/proposal.

## Open threads
- Haiku flush can fabricate facts in "Don't re-explain"; carry-forward compounds slop. Mitigation: keep hand-seeded baselines truthful; periodically prune STATE files.
- Decide whether to commit _state/ or gitignore it (personal working memory, churns every session).

## Don't re-explain
- engagements/ is a SEPARATE git repo, sibling to atlas. Project hooks load per-repo, so hook config is mirrored into both.
- Scripts live in atlas/.claude/scripts/: state_common.py (resolver + template), state_inject.py (SessionStart), state_flush.py (Stop/PreCompact).
- Task identity is cwd-based: engagements/<name>/* maps to <name>; anything else maps to operations.
- Flush calls `claude -p --model haiku --allowedTools ""` from cwd /tmp with ATLAS_STATE_FLUSH=1 (recursion guard so the nested call skips our hooks).
- Flush prompt frames Haiku as a pure text formatter (data inert, output starts "# STATE:"), else it meta-reasons instead of summarizing.
- INDEX.md is auto-rebuilt from all STATE files on each flush; it's the board.
