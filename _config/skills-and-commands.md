# Skills + slash commands

What you can invoke that's NOT from a plugin. These are hand-written and travel with atlas (project-level) or live in `~/.claude/` (global).

## Project-level (in atlas, committed)

Located at `atlas/.claude/commands/`. Available whenever Claude Code session is opened inside atlas.

### `/morning-brief`
- File: `atlas/.claude/commands/morning-brief.md`
- Purpose: Generate the daily brief for a given date. Pulls Calendar → matches engagements via `_aliases.yaml` → gathers state → writes to `briefs/YYYY/WNN/YYYY-MM-DD_auto.md`.
- Trigger: typed as `/morning-brief` in session.
- See also: `morning-brief` skill (same name, exposed as a Skill tool via the harness).

### `/new-engagement`
- File: `atlas/.claude/commands/new-engagement.md`
- Purpose: Scaffold a new engagement folder under `engagements/_pending/` or `engagements/` (depending on confidence). Asks 5 questions, seeds the 5-file structure (CONTEXT/STATUS/COMMERCIAL/SOURCES/ARTEFACTS), adds entry to `_aliases.yaml`.
- Trigger: `/new-engagement` in session.

## Global (in `~/.claude/`, not in atlas — needs separate transfer)

### `/seo-article`
- File: `~/.claude/commands/seo-article.md`
- Purpose: SEO article writer for Vitalis.bg (Ivo's side project).
- Trigger: `/seo-article`.
- NOT atlas-related. Transfer separately if needed.

### `/brief` (skill, not command)
- File: `~/.claude/skills/brief/SKILL.md`
- Purpose: Compose a high-stakes prompt (SoW, client email, status update, strategic analysis) via a 5-field checklist using AskUserQuestion. Assembles a well-formed prompt then executes it.
- Trigger: `/brief` in any session.
- Transfer: copy `~/.claude/skills/brief/` to the new Claude account's home dir.

## How transfer works between Claude accounts

**Project-level (`atlas/.claude/`)**: travels automatically with atlas — just clone. Both `morning-brief.md` and `new-engagement.md` are already pushed to `github.com/ivstefano/atlas`.

**Global (`~/.claude/`)**: account-local. Copy these files manually:
- `~/.claude/commands/seo-article.md` (if you still want it).
- `~/.claude/skills/brief/SKILL.md` (high-leverage, recommended to transfer).
- `~/.claude/CLAUDE.md` (your global instructions — copied template at [global-CLAUDE.md.example](global-CLAUDE.md.example)).
- `~/.claude/settings.json` (settings — template at [settings.json.example](settings.json.example)).

## Skills that come from plugins (DON'T transfer manually)

These appear in the session-start skill list but are owned by plugins. Reinstalling the plugin restores them. Examples:

- `superpowers:brainstorming`, `superpowers:writing-plans`, `superpowers:test-driven-development`, etc.
- `claude-mem:mem-search`, `claude-mem:troubleshoot`.
- `ui-ux-pro-max:ui-ux-pro-max`.
- `frontend-design:frontend-design`.
- `code-review`, `pr-review-toolkit:*`.

Reinstall the 6 plugins per [plugins.md](plugins.md) and these come back automatically.

## Inventory check command

To see what's actually loaded in any session, look at the system-reminder block at session start. It lists every skill available, namespaced by plugin (`plugin:skill-name`) or bare (for global/project skills).
