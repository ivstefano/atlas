# Memory — how it works, how it travels

There are TWO memory systems in play. Don't confuse them.

## 1. Hand-written memory (`memory/*.md`) — the durable one

Lives at `~/.claude/projects/-Users-iris-Documents-atlas/memory/`. **NOT committed to atlas.** Path is derived from the project's filesystem location (`/Users/iris/Documents/atlas/` → URL-encoded slug `-Users-iris-Documents-atlas`).

- 38 hand-curated `.md` files as of 2026-05-26.
- Index: `MEMORY.md` in the same folder, loaded automatically at every session start.
- Content: User profile, feedback rules, project state, references (Asana IDs, Drive paths, etc).
- Maintained by hand (by Claude, with Ivo's approval, via the auto-memory protocol in the system prompt).

### Portability across Claude accounts (same machine)

**Works automatically.** Same project path → same slug → same memory folder. Switching from personal `claude.ai` to Iris-issued Claude on the same macOS user: no action needed.

### Portability across machines

Need atlas to live at the same path on the new machine (`/Users/iris/Documents/atlas/`). Then:
- The `memory/` folder is NOT part of atlas, so you'd start with empty memory on the new machine.
- To restore: `rsync` or manual copy from old machine's `~/.claude/projects/-Users-iris-Documents-atlas/memory/` to new machine's same path.
- No automated sync today.

### Why memory isn't committed to atlas

- Privacy: some entries (commercial state, political dynamics) are honest assessments meant for Ivo only.
- Atlas is on GitHub (private repo on `ivstefano`); even private GitHub means GitHub admins + future-Ivo's potential collaborators see it.
- The path-key derivation is enough — memory loads automatically wherever atlas lives at the right path.

### If you really want a backup

Optional script (not built today, can be added later): `atlas/scripts/sync-memory.sh` would `rsync` from `~/.claude/projects/.../memory/` into `atlas/.memory-backup/` (gitignored) on demand. Provides recovery without committing to GitHub.

## 2. claude-mem database — the cross-session observation index

Plugin-managed (claude-mem@thedotmack). Stores the `#NNNN` observation IDs you see in the "recent context" summary at session start. PM2 worker writes to a SQLite DB inside the plugin install dir.

- **Account-scoped, machine-scoped.** A different Claude account = a different DB.
- **Does NOT migrate** when switching accounts. New account starts with an empty observation history.
- The recent-context summary ("📊 50 observations, 19,852 tokens, 89% reduction from reuse") starts at zero on the new account.

### What you lose on account switch

- The auto-summary of past sessions.
- Search across past sessions via `/claude-mem:mem-search`.

### What you don't lose

- The hand-written memory (#1 above) — that's the durable knowledge.
- Git history of atlas (briefs, NEXT_PRIORITIES, engagement work logs).
- Engagement `STATUS.md` files (in the sibling `engagements/` repo).

The auto-summary is convenience. The hand-written memory + STATUS files are the actual institutional knowledge.

## Quick reference

| Question | Answer |
|---|---|
| Switching Claude accounts on same machine — memory works? | Yes, hand-written memory loads automatically. claude-mem starts fresh. |
| Switching machines — memory works? | Hand-written: rsync the `~/.claude/projects/.../memory/` folder. claude-mem: starts fresh. |
| Where do I add a new memory? | Either ask Claude to add it (it'll use the auto-memory protocol), or write the file by hand under `~/.claude/projects/-Users-iris-Documents-atlas/memory/` and add a line to MEMORY.md. |
| Can I see all my memory? | `cat ~/.claude/projects/-Users-iris-Documents-atlas/memory/MEMORY.md` for the index. |
| What if I move atlas to a different path? | The slug changes, so the project-scoped memory folder changes too. You'd need to rename the slug folder to match the new path, or symlink. Best to keep atlas at `~/Documents/atlas/`. |
