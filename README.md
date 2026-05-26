# atlas

Ivo's operations layer: daily briefs, persistent memory index, engagement coordination, MCP wiring, automation strategy. The command center for running ~15 active client engagements + internal product threads + commercial cadence.

## What's here

| Folder / file | Purpose |
|---|---|
| `briefs/YYYY/WNN/` | Daily prep briefs (`_auto.md`) + call-specific briefs (`_<topic>.md`). |
| `_config/` | Workstation setup: plugins, MCPs, settings, skills, memory — everything needed to rebuild a Claude Code environment from scratch. **Start here on a new machine.** |
| `NEXT_PRIORITIES.md` | Build queue, framed by toil-removed-per-build-day. Updated as priorities shift. |
| `SESSION_LOG.md` | Narrative log of multi-day sessions. |
| `CLAUDE.md` | Operating instructions for Claude when working inside atlas. Loaded automatically. |
| `.claude/commands/` | Project-level slash commands (`/morning-brief`, `/new-engagement`). |
| `_assets/` | Published artefacts (Pyloth logo, SA-position dashboards). |
| `_live/` | Scratch / in-flight transcripts. Gitignored where sensitive. |
| `sessions/` | Cross-session handoff docs. |

## Sibling things (NOT in this repo)

| Path | Purpose |
|---|---|
| `~/Documents/engagements/` | One folder per client (CONTEXT/STATUS/COMMERCIAL/SOURCES/ARTEFACTS). Sibling repo. |
| `~/.claude/projects/-Users-iris-Documents-atlas/memory/` | Hand-written memory (38 entries). Path-derived from atlas's filesystem location. Not committed — see [_config/memory.md](_config/memory.md) for why. |
| `~/Documents/culture/` | Sara HR companion site (iris-culture, Bitbucket). |
| `~/Documents/pyloth/` | SA-clone deployment scaffolding. |
| `Iris.ai - Everyone/` (Google Drive) | Shared org drive: canonical source for client docs + deliverables. |

## Rebuilding the workstation (new machine or new Claude account)

Open Claude Code inside `~/Documents/atlas/` and read `_config/README.md`. It has the 6-step rebuild order (settings → global instructions → plugins → MCPs → memory verify → skills).

Short version of the first prompt to give a fresh Claude:

> Read `_config/README.md` and follow the rebuild order. This is my workstation.
> Tell me what's missing on this machine vs. what `_config/` describes, then fix it.

## House style for working in here

See `~/.claude/CLAUDE.md` (template at [_config/global-CLAUDE.md.example](_config/global-CLAUDE.md.example)) for the durable rules. The atlas-specific conventions live in [CLAUDE.md](CLAUDE.md).
