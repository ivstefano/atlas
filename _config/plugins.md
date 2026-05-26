# Plugins

6 plugins enabled as of 2026-05-26. Install via `/plugin install <name>` in Claude Code, or by editing `~/.claude/settings.json`'s `enabledPlugins` block + adding marketplaces.

## The list

| Plugin | Source | Purpose |
|---|---|---|
| **claude-mem** | thedotmack (community) | Cross-session memory. The `#NNNN` observation IDs + the "recent context" summary at session start. Highest-leverage. |
| **superpowers** | claude-plugins-official | The skill framework: brainstorming, writing-plans, TDD, debugging, verification-before-completion, etc. Most `/<skill>` invocations land here. |
| **code-review** | claude-plugins-official | `/code-review` slash command for the current diff. |
| **pr-review-toolkit** | claude-plugins-official | PR review agents: code-reviewer, comment-analyzer, pr-test-analyzer, silent-failure-hunter, type-design-analyzer, code-simplifier. |
| **ui-ux-pro-max** | github: nextlevelbuilder/ui-ux-pro-max-skill | UI/UX design patterns, color palettes, font pairings, component styles. |
| **frontend-design** | claude-plugins-official | Frontend code generation skill. |

## Install commands

Most are from the official marketplace (auto-discovered). `ui-ux-pro-max` is from a separate GitHub marketplace and needs to be added first.

```bash
# Add the third-party marketplace for ui-ux-pro-max:
# (in Claude Code session)
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill

# Install everything:
/plugin install claude-mem
/plugin install superpowers
/plugin install code-review
/plugin install pr-review-toolkit
/plugin install ui-ux-pro-max
/plugin install frontend-design
```

Or set them all enabled at once in `settings.json` (see [settings.json.example](settings.json.example)). Claude Code will install on next launch.

## Per-plugin notes

### claude-mem

- Backend: PM2-managed worker + SQLite DB, lives in plugin install dir.
- Auto-summarises sessions, builds the recent-context index.
- DB does NOT migrate across accounts/machines — starts fresh. The hand-written `memory/*.md` is the durable knowledge.
- Slash commands: `/claude-mem:mem-search` (search), `/claude-mem:troubleshoot` (fix PM2/DB issues).

### superpowers

- Skill collection. Skills are *rigid* by default — follow them exactly when invoked.
- The framework injects a `using-superpowers` skill at session start that forces you to check for relevant skills before responding.
- Key skills:
  - `brainstorming` — for any creative/design task.
  - `writing-plans` / `executing-plans` — for multi-step implementations.
  - `test-driven-development` — TDD discipline.
  - `systematic-debugging` — for any bug or unexpected behavior.
  - `verification-before-completion` — run-the-command before claiming done.

### code-review + pr-review-toolkit

- `code-review` is the lighter inline tool.
- `pr-review-toolkit` is multi-agent — spawns specialised reviewers (silent-failure-hunter, type-design-analyzer, etc).
- Both useful before pushing engagement-side code (extractor pipelines, Pyloth, culture).

### ui-ux-pro-max + frontend-design

- Used when generating client-facing visualisations (Garrett dashboards, scoping showcases, Heineken demo HTML).
- ui-ux-pro-max has the design libraries (colors, fonts, patterns).
- frontend-design generates the actual code.

## What's NOT installed (and why)

- **Code execution sandboxes** — not needed; Claude Code has Bash.
- **GitHub plugin** — `gh` CLI does the job.
- **Slack/Asana write plugins** — only read MCPs are wired; write actions go through Ivo manually per the [outward-facing-actions](../memory/outward-facing-actions.md) rule.
