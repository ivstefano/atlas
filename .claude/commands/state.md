---
description: Show the task-state board, or checkpoint the current task's working memory now.
argument-hint: "" (show board) | board | save | <task>
---

# Task state

Durable per-task working memory. Each tab's task is resolved from cwd
(engagements/<name>/* -> <name>; anything else -> operations). State lives in
`atlas/_state/<task>.md`, auto-written on session end/compact, auto-read on
session start. This command is for manual control.

Argument: `$ARGUMENTS`

## Behavior

- **empty or `board`**: Read and display `atlas/_state/INDEX.md`. That is the board:
  every task, last session, tab, next action. If a task row interests Ivo, offer to
  open its `_state/<task>.md`.

- **`save`**: Checkpoint the CURRENT task now (don't wait for session end). Resolve the
  task from cwd. Then update `atlas/_state/<task>.md` yourself, in this session, from
  what you actually did this conversation. Keep the exact section structure
  (`## Now`, `## Next action`, `## Open threads`, `## Don't re-explain`), set
  `last_session` to now and `last_tab` appropriately. You have full context, so this is
  higher quality than the headless Haiku flush. After writing, rebuild the board:
  `python3 .claude/scripts/state_flush.py` is for the hook path; instead just run
  `python3 -c "import sys; sys.path.insert(0,'.claude/scripts'); import state_flush; state_flush.refresh_index()"`.

- **`<task>` (a name)**: Read and display `atlas/_state/<task>.md` for that task.

## Notes

- Never invent durable facts. Only record what's grounded in this session or the prior STATE.
- `_state/<task>.md` is YOUR working memory, distinct from the engagement's client-facing STATUS.md. Don't conflate them.
