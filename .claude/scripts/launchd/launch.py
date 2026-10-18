#!/usr/bin/env python3
"""LEGACY launchd entry point. The ai.iris.atlas.* plists no longer use it: every job now runs
through ~/Applications/AtlasAutopilot.app (autopilot/launcher.c), which holds the single Documents grant.
Kept for manual use only. If access is missing it names that same grant.

    launch.py <script.py in atlas/.claude/scripts> [args...]
"""
import datetime as dt
import os
import runpy
import subprocess
import sys

SCRIPTS = os.path.expanduser("~/Documents/atlas/.claude/scripts")
LOG = os.path.expanduser("~/.cache/atlas/autopilot_launch.log")


def note(msg):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"{dt.datetime.now().isoformat(timespec='seconds')}  {msg}\n")


script = sys.argv[1]
path = os.path.join(SCRIPTS, script)
try:
    open(path).close()
except PermissionError:
    msg = (f"{script}: macOS blocks ~/Documents. Run it via the AtlasAutopilot launcher and turn on: "
           "System Settings > Privacy & Security > Files and Folders > AtlasAutopilot > Documents Folder")
    note(msg)
    stamp = os.path.expanduser("~/.cache/atlas/tcc_notified")
    if os.path.exists(stamp) and (dt.datetime.now().timestamp() - os.path.getmtime(stamp)) < 6 * 3600:
        sys.exit(3)          # KeepAlive retries every minute; notify at most every 6h
    open(stamp, "w").close()
    subprocess.run(["/usr/bin/osascript", "-e",
                    f'display notification "{msg}" with title "Atlas autopilot blocked" sound name "Basso"'])
    sys.exit(3)
note(f"start {script} {' '.join(sys.argv[2:])}")
sys.argv = [path] + sys.argv[2:]
sys.path.insert(0, SCRIPTS)
runpy.run_path(path, run_name="__main__")
