# Slack DND ↔ client meetings

Silences Slack automatically during client calls on `ivo@iris.ai`'s calendar.

**2026-10-19: Slack snoozing is OFF** (`SNOOZE_SLACK = False` in `dnd_sync.py`). Ivo needs DMs mid-call;
screen-share banners are handled by macOS "Allow notifications when mirroring or sharing the display" = off.
The job still runs and writes `~/.cache/atlas/meetings_now.json` (all calls in the next 6h, `dnd_rules.is_meeting`),
which `notify_hook.py` (Claude Code notification hook) reads to stay quiet during calls.

## Pieces

| File | Role |
|---|---|
| `slack_dnd.py` | Slack API wrapper: `status` / `snooze <min>` / `off`. Token from Keychain (`slack-dnd-token`). |
| `dnd_rules.py` | `classify(event) -> (is_client, reason)`. The heuristic. |
| `dnd_sync.py` | launchd entrypoint. Reads calendar, snoozes for the event's remaining time. |

## Rule (calibrated on 97 real events, 2026-08-25..09-07)

External attendee = client. In order:
1. non-`default` eventType (out-of-office etc) → no
2. title has `[internal]` → no
3. all external domains deny-listed → no
4. any external domain left → **CLIENT**
5. all-internal / solo → no

`DENY_DOMAINS` = gmail.com (team + contractor personal accounts), growth-mojo.com,
marketstar.com, dezea.digital (partners/vendors). `@group.calendar.google.com`
attendees are shared calendars, not people, so they're ignored.

Result on the sample: 20/97 flagged, no false positives or negatives.

Deliberately NOT a rule: client name in the title. Ivo's call — internal prep
calls about a client (e.g. "Garrett MVP Scoping Discussion") stay unsilenced.

**Known blind spot:** a client emailing from a personal Gmail address is missed,
since gmail.com is deny-listed. Nothing like that in the sample. If it happens,
add an allow-list exception.

## Runtime layout

launchd cannot read `~/Documents` (TCC restriction), so the live copies run from
`~/.local/share/atlas-dnd/`. **This directory is the source of record; after
editing here, re-copy:**

    cp .claude/scripts/{slack_dnd,dnd_rules,dnd_sync}.py ~/.local/share/atlas-dnd/

Calendar auth piggybacks on gcalcli's cached OAuth credentials
(`~/Library/Application Support/gcalcli/oauth`, pickled, has a refresh token) and
calls the Calendar API directly via gcalcli's venv interpreter. gcalcli itself was
installed with `uv tool install gcalcli`; its 4.x releases need your own Google
Cloud OAuth client (Desktop app type).

## Job

`~/Library/LaunchAgents/ai.iris.slack-dnd-sync.plist`, every 300s.

    launchctl list | grep slack-dnd      # 2nd column is last exit code, want 0
    tail -f ~/.cache/atlas/dnd_sync.log
    launchctl unload ~/Library/LaunchAgents/ai.iris.slack-dnd-sync.plist   # disable
    launchctl load   ~/Library/LaunchAgents/ai.iris.slack-dnd-sync.plist   # enable

Only clears a snooze it set itself (tracked in `~/.cache/atlas/dnd_sync.json`), so
a manual `/dnd` is never overridden. No pre-meeting buffer: DND starts at the
event's start time, so a call cancelled 10 min out doesn't silence you early.

## Gotcha

Calendar API returns `eventType: "default"` (lowercase); the Claude Calendar MCP
returns `"DEFAULT"`. `classify()` lowercases before comparing — don't undo that or
every event silently reclassifies as non-client.
