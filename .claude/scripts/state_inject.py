#!/usr/bin/env python3
"""SessionStart hook: orient a fresh Claude to where this tab's task left off.

Resolves the task from cwd, reads atlas/_state/<task>.md, prints it so the
harness injects it as additional context. Silent (no output) if no STATE file
yet, so new tasks don't error.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from state_common import read_hook_input, cwd_from_hook, resolve_task, state_path  # noqa: E402


def main() -> None:
    import os
    if os.environ.get("ATLAS_STATE_FLUSH") == "1":
        return  # nested headless flush call; do not inject
    data = read_hook_input()
    task = resolve_task(cwd_from_hook(data))
    sp = state_path(task)
    if not sp.exists():
        return
    body = sp.read_text().strip()
    if not body:
        return
    print(f"# Where you left off on this task ({task})\n")
    print("Resuming task state from a prior session. Trust this for "
          "'where was I' / 'next action'; verify file/flag references "
          "against the repo before acting.\n")
    print(body)


if __name__ == "__main__":
    main()
