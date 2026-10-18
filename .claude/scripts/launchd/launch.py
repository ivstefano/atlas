#!/usr/bin/env python3
"""launchd entry point for the atlas autopilot jobs. Lives OUTSIDE ~/Documents on purpose:
launchd processes cannot read ~/Documents unless this interpreter has Full Disk Access (macOS TCC).
If access is missing, show a notification saying exactly what to grant, instead of failing silently.

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
    py = os.path.realpath(sys.executable)
    msg = f"{script}: macOS blocks ~/Documents. Grant Full Disk Access to {py}"
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
