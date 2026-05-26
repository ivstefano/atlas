# Atlas workstation config

Everything needed to rebuild Ivo's Claude Code workstation from scratch on a new machine or a different Claude account (e.g. switching from personal `claude.ai` to Iris-issued Claude account).

Atlas itself is the command center. This folder documents the wider environment Atlas runs inside.

## Quick rebuild order

1. Install Claude Code (whichever variant: personal `claude.ai`, Iris-issued, or Copilot CLI).
2. Clone atlas to `~/Documents/atlas/` (path matters — see [memory.md](memory.md)).
3. Apply global config: copy `global-CLAUDE.md.example` to `~/.claude/CLAUDE.md`, copy `settings.json.example` to `~/.claude/settings.json`.
4. Install plugins per [plugins.md](plugins.md).
5. Wire MCPs per [mcps.md](mcps.md). The ones with OAuth flows (Asana, HubSpot, Slack via OAuth, Drive via OAuth) need manual auth.
6. Verify memory loads: open a new session in `~/Documents/atlas/`, the `MEMORY.md` index should appear in the system reminder at session start.
7. Skills + commands: project-level ones live in `atlas/.claude/`, global ones in `~/.claude/`. See [skills-and-commands.md](skills-and-commands.md).

## Files in this folder

- [plugins.md](plugins.md) — the 6 enabled plugins, install commands, what each does.
- [mcps.md](mcps.md) — Calendar, Gmail, Drive, Slack, HubSpot, Asana wiring.
- [settings.json.example](settings.json.example) — global Claude settings template.
- [global-CLAUDE.md.example](global-CLAUDE.md.example) — global instructions template (House Style, prompt-clarification protocol).
- [skills-and-commands.md](skills-and-commands.md) — inventory of custom skills + slash commands.
- [memory.md](memory.md) — how the hand-written `memory/*.md` files work across accounts + machines.

## What this is NOT

- Not a backup of memory content (that lives at `~/.claude/projects/-Users-iris-Documents-atlas/memory/`, see [memory.md](memory.md) for why it's not committed to atlas).
- Not a backup of claude-mem's database (PM2-managed, account-local, starts fresh on a new install).
- Not a backup of session transcripts (`~/.claude/projects/.../.jsonl` files are ephemeral).
