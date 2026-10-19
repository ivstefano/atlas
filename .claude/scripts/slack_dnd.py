#!/usr/bin/env python3
"""Set / clear Slack DND. Token from macOS Keychain (service: slack-dnd-token).

Usage:
    slack_dnd.py status
    slack_dnd.py snooze <minutes>
    slack_dnd.py off
"""
import json
import subprocess
import sys
import urllib.parse
import urllib.request

KEYCHAIN_SERVICE = "slack-dnd-token"
API = "https://slack.com/api/"


def token() -> str:
    return subprocess.run(
        ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-w"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def call(method: str, **params) -> dict:
    data = urllib.parse.urlencode(params).encode() if params else None
    req = urllib.request.Request(
        API + method,
        data=data,
        headers={
            "Authorization": f"Bearer {token()}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd = sys.argv[1]

    if cmd == "status":
        res = call("dnd.info")
    elif cmd == "snooze":
        if len(sys.argv) < 3:
            print("snooze needs minutes")
            return 2
        res = call("dnd.setSnooze", num_minutes=int(sys.argv[2]))
    elif cmd == "off":
        res = call("dnd.endSnooze")
    else:
        print(__doc__)
        return 2

    print(json.dumps(res, indent=2))
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
