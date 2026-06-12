@# atlas — operating instructions for Claude / Kiro

This repo is Ivo's operations layer: daily briefs, session logs, MCP wiring, migration protocols, automation strategy. It does NOT hold engagement content — engagements live in `~/Documents/engagements/` (separate repo).

## Sibling repos / contexts

| Path | Purpose | Operating instructions |
|---|---|---|
| `~/Documents/engagements/` | One folder per client engagement (CONTEXT / STATUS / COMMERCIAL / SOURCES / ARTEFACTS) | [engagements/CLAUDE.md](../engagements/CLAUDE.md) |
| `~/Documents/Axion/` | Local IRIS Axion code + transitional copies of some client sources | being phased out for sources — Drive is canonical (see engagements/CLAUDE.md) |
| `Iris.ai - Everyone/` (Google Drive) | Shared org drive: sources, deliverables, contracts | env var `$IRIS_EVERYONE` if locally mounted; Drive MCP otherwise |

## Atlas-internal conventions

- **briefs/** — daily prep briefs (`YYYY-MM-DD.md`) and call briefs (`YYYY-MM-DD_<topic>.md`). Committed.
- **SESSION_LOG.md** — narrative log of multi-day sessions, newest section appended.
- **_iris_people.md** — name ↔ nickname ↔ role decoder for transcripts.
- **_migration_protocol.md**, **_digest_protocol.md**, **_gmail_digest_protocol.md**, **_hubspot_mcp_setup.md** — reusable procedures.
- **.claude/scripts/** — automation primitives: `tactiq_pull.py`, `tactiq_watch.py`, `tactiq_client.py`, `post_meeting_digest.py`, `gap_scan.py`, `state_common.py` / `state_inject.py` / `state_flush.py`.
- **.claude/skills/** + **.claude/commands/** — project-scoped skills and slash commands: `/tactiq-pull`, `/post-meeting-digest`, `/morning-brief`, `/new-engagement`, `/brief`, `/state`.
- **_state/** — durable per-task working memory (see below).

## Task state (cross-session memory per tab)

Each terminal tab is an isolated Claude session that dies on terminal close. To stop re-explaining context after a restart, every task carries a STATE file.

- Task identity is the working directory: launch Claude inside `engagements/<name>/` and the task is `<name>`; anywhere else (atlas root) it's `operations`.
- `_state/<task>.md` is MY working memory for that task: `## Now`, `## Next action`, `## Open threads`, `## Don't re-explain`. Distinct from the engagement's client-facing `STATUS.md`.
- A SessionStart hook injects the task's STATE when a tab opens, so a fresh Claude wakes up oriented. A Stop/PreCompact hook flushes the session back into STATE via a headless Haiku call (runs in background). Hook config lives in both `atlas/.claude/settings.json` and `engagements/.claude/settings.json` because engagements is a separate repo.
- `_state/INDEX.md` is the board: every task, last session, tab, next action. `/state` shows it; `/state save` checkpoints the current task mid-session.
- STATE files are committed (portable across machines); `_state/.flush.log` is gitignored.

## Memory

Persistent memory lives at `~/.claude/projects/-Users-iris-Documents-atlas/memory/`. Two-tier, like briefs: `MEMORY.md` is the **active** index (evergreen rules + work touched ~last 3 weeks), loaded each session. `MEMORY_ARCHIVE.md` holds dormant/closed/absorbed memories, NOT loaded each session — the full `.md` files stay on disk so `[[links]]` resolve. **Lookup order if a fact isn't in MEMORY.md: grep MEMORY_ARCHIVE.md, then the `.md` files in the memory dir, before concluding it doesn't exist.** When a memory goes dormant, move its line from MEMORY.md to MEMORY_ARCHIVE.md; reactivate by moving it back. Portability across machines / Claude accounts: [_config/memory.md](_config/memory.md).

## Workstation rebuild (new machine or new Claude account)

If you're a fresh Claude landing in this repo without prior context, read [_config/README.md](_config/README.md) first. It has the 6-step rebuild order (settings → global instructions → plugins → MCPs → memory verify → skills) and links to per-topic detail pages. Tell Ivo what's missing on this machine vs. what `_config/` describes, then fix it. Don't ask questions about preferences — they're documented in `_config/`.

## When in doubt

- Engagement content questions → `engagements/CLAUDE.md`
- Drive / artefact resolution → `engagements/CLAUDE.md` "Path conventions" + "$IRIS_EVERYONE"
- Memory questions → `MEMORY.md` index, then the linked memory file
- Outward-facing action (email, calendar invite) → draft, get Ivo approval, then create. Never auto-send.
