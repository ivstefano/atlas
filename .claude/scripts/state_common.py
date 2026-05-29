"""Shared helpers for the task-state system (state_inject / state_flush hooks).

A "task" is one unit of durable working memory. Identity comes from cwd:
  ~/Documents/engagements/<name>/...  -> task "<name>"
  ~/Documents/atlas (or anywhere else) -> task "operations"

STATE files live in atlas/_state/<task>.md. They hold MY working state
(what I was doing, next action, what not to re-explain), distinct from an
engagement's STATUS.md (client-facing project state).
"""

import json
import os
import sys
from pathlib import Path

HOME = Path.home()
ATLAS = HOME / "Documents" / "atlas"
ENGAGEMENTS = HOME / "Documents" / "engagements"
STATE_DIR = ATLAS / "_state"


def resolve_task(cwd: str) -> str:
    """Map a working directory to a task name."""
    try:
        p = Path(cwd).resolve()
    except Exception:
        return "operations"
    try:
        rel = p.relative_to(ENGAGEMENTS)
        parts = rel.parts
        if parts and not parts[0].startswith("_"):
            return parts[0]
    except ValueError:
        pass
    return "operations"


def state_path(task: str) -> Path:
    return STATE_DIR / f"{task}.md"


def read_hook_input() -> dict:
    """Hooks receive a JSON object on stdin. Return {} if absent/garbage."""
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def cwd_from_hook(data: dict) -> str:
    return data.get("cwd") or os.getcwd()


STATE_TEMPLATE = """# STATE: {task}

_Working memory for this task. Auto-written on session end/compact. Read on session start.
This is NOT the client-facing STATUS.md._

last_session: {ts}
last_tab: {tab}

## Now
{now}

## Next action
{next_action}

## Open threads
{open_threads}

## Don't re-explain
{dont_reexplain}
"""
