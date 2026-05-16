# atlas — operating instructions for Claude / Kiro

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
- **_live/** — in-flight working state (call notes during meetings, scratch).
- **_iris_people.md** — name ↔ nickname ↔ role decoder for transcripts.
- **_migration_protocol.md**, **_digest_protocol.md**, **_gmail_digest_protocol.md** — reusable procedures.

## Memory

Persistent memory lives at `~/.claude/projects/-Users-iris-Documents-atlas/memory/`. Index in `MEMORY.md` loaded each session. See that file for the catalog.

## When in doubt

- Engagement content questions → `engagements/CLAUDE.md`
- Drive / artefact resolution → `engagements/CLAUDE.md` "Path conventions" + "$IRIS_EVERYONE"
- Memory questions → `MEMORY.md` index, then the linked memory file
- Outward-facing action (email, calendar invite) → draft, get Ivo approval, then create. Never auto-send.
