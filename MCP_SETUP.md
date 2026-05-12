# Layer 2 — MCP connectors (sensors and actuators)

Karpathy: agents need "sensors over the world, actuators over the world." Right now Claude
Code only sees the local repo. These MCPs give agents reach into the surfaces where the
engagement state actually lives.

**Hard rule for all of these: agents draft, I send.** Anything outward-facing (Slack message
to a colleague, email to a client, Drive overwrite of a shared doc) is prepared as a draft and
does not leave without me. Contract-grade docs (SoW, NDA) additionally require my review even
as drafts (see README §3).

---

## Priority 1 — Google Drive

**Why**: the canonical SoW / Excel / proposal often lives in Drive; local copies go stale.
Closes the "string up the deployment / go to the settings menu" friction Karpathy complained
about.

**Unlocks**:
- Pull the live SoW/Excel/proposal instead of a stale local copy when drafting.
- Push generated artifacts back to the right Drive folder (with my confirmation).
- "Is the local `SOURCES.md` pointer still valid?" checks against Drive.

**Status**: `mcp__claude_ai_Google_Drive__*` tools are present in this environment; needs
`authenticate` / `complete_authentication`. See auto-memory `iris_gdrive_location.md` for the
existing GDrive mount path and key folders.

**Guardrail**: read freely; write only on confirmation; never overwrite a shared SoW/NDA
without the human-in-the-loop step.

---

## Priority 1 — Slack

**Why**: a lot of engagement state currently exists *only* in Slack threads with the tech
team (and in `SLACK.md` paste-in exports). We want a **live Slack MCP**, not paste-ins.

**Unlocks**:
- Read the per-engagement tech-team channel → auto-draft the weekly client update.
- When an engineer asks a question in Slack, draft (not send) my reply with the full
  engagement context (`CONTEXT.md` + recent `STATUS.md`) attached.
- Feed Slack activity into the weekly cross-engagement rollup.

**Status**: not yet connected. **Action item: find/stand up a Slack MCP server and wire it.**
Options to evaluate: the official/community Slack MCP servers (bot token + channel scopes), or
a self-hosted one. Decide scopes: read messages in the engagement channels + post as me/bot
(post = draft-and-confirm only).

**Guardrail**: never auto-post to a client-facing or company-wide channel. Posting to internal
tech channels still goes through a confirm step.

---

## Priority 2 — Google Calendar

**Why**: engagements are driven from the calendar. "What has a meeting this week, and is its
`STATUS.md` current?" is the prep queue generator.

**Unlocks**:
- Daily morning brief: today's meetings → matching `CONTEXT.md`/`STATUS.md` → prep summary.
- Meeting created/updated → trigger a prep doc from `CONTEXT.md` + recent `STATUS.md`.
- Stale-engagement watchdog cross-checks: meeting scheduled but `STATUS.md` untouched.

**Status**: `mcp__claude_ai_Google_Calendar__*` present; needs `authenticate` /
`complete_authentication`.

**Guardrail**: read-only to start. Creating/moving events later, on confirmation only.

---

## Maybe later — Gmail

`mcp__claude_ai_Gmail__*` is present. Useful for drafting follow-up emails after meetings and
for pulling client email threads into `STATUS.md`. Same draft-not-send rule. Lower priority
than Drive/Slack/Calendar; revisit after Layer 3 loops are running.

---

## Setup checklist

- [ ] Authenticate Google Drive MCP; confirm it can list the engagement folders.
- [ ] Authenticate Google Calendar MCP; confirm it lists this week's meetings.
- [ ] Choose and stand up a Slack MCP; configure scopes (read engagement channels + draft-post).
- [ ] Confirm the draft-not-send behavior holds for each (test: ask it to "send" something,
      verify it stops and asks).
- [ ] (later) Gmail MCP, if the email-drafting loop proves worth it.
