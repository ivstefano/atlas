# MCPs (Model Context Protocol servers)

What's wired, what's not, how to set up each on a fresh machine.

## Status as of 2026-05-26

| MCP | Status | Auth method | Used for |
|---|---|---|---|
| **Google Calendar** | ✅ wired | OAuth (claude.ai-hosted) | Morning brief, scheduling, meeting prep. |
| **Gmail** | ✅ wired | OAuth (claude.ai-hosted) | `_gmail_digest_protocol.md`, finding emails from contacts. |
| **Google Drive** | ✅ wired | OAuth (claude.ai-hosted) | Reading client docs, finding shared files. **Note**: prefer the local Drive sync mount for bulk file ops (faster, no base64 bloat). See [memory/drive-sync-mount.md](../memory/drive-sync-mount.md). |
| **Slack** | ✅ wired | OAuth | Channel history, DM search, transcript pulls. |
| **Asana** | ✅ wired | OAuth (self-registering, v1 `/sse`) | Reading Iris Commercial Engagements + Product Roadmap projects. Setup + troubleshooting: [_asana_mcp_setup.md](../_asana_mcp_setup.md). |
| **HubSpot** | ❌ blocked | OAuth | Pipeline/deal state. Blocked: no admin authorisation yet (`NEXT_PRIORITIES.md` OQ-1). |
| **Canva** | ✅ wired | OAuth | Decks, brand templates. Used rarely; pull deck templates. |
| **claude-mem** | ✅ (plugin, not MCP) | n/a | Memory search across sessions. |

## What's NOT wired (intentional)

- **Tactiq** — no MCP exists. Transcripts pulled via `_live/fetch_current.py` instead. See [memory/tactiq-transcript-fetch.md](../memory/tactiq-transcript-fetch.md).
- **Bitbucket** — `gh` CLI handles GitHub; Bitbucket interactions are manual via `git` + Atlassian web. Iris uses Bitbucket for `iris-culture`, `engagements`, `extractor-v2` repos.
- **Linear** — not used by Iris.
- **Notion** — not used by Iris.

## Setup on a new machine / new Claude account

### claude.ai-hosted MCPs (Calendar, Gmail, Drive, Slack)

These connect via OAuth in the Claude Code UI:

1. Open Claude Code.
2. Settings → MCP → enable the server.
3. Claude opens an OAuth flow in browser; sign in with `ivo@iris.ai`.
4. Authorise the requested scopes.

For the personal account this is already done. For the Iris-issued account, redo the OAuth per server.

### Asana (self-registering OAuth)

```
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

Then `/mcp` → asana → Authenticate. No manual app needed.

Use the **v1 `/sse`** endpoint, not `v2/mcp`. v2 delegates OAuth to `app.asana.com`, which publishes no `registration_endpoint`, so Claude Code can't self-register and fails with "does not support dynamic client registration". Full root cause, diagnostics, and cleanup steps: [_asana_mcp_setup.md](../_asana_mcp_setup.md).

### HubSpot

Blocked — need admin auth from Iris HubSpot owner. Not a per-machine setup.

## Key Asana IDs (so you don't have to look them up)

- `Iris.ai Commercial Engagements` project: `1214855342290138` — section per engagement, phase tasks, next-actions. Emoji status: ✅ ⏳ 📅 ❌. See [memory/asana-commercial-tracker.md](../memory/asana-commercial-tracker.md).
- `Iris.ai Product Roadmap` > `Scoping Demo Automation` section: `1214888380737527` — Ivo's automation board. See [memory/sa-automations-board.md](../memory/sa-automations-board.md).

## Drive sync mount path

```
/Users/iris/Library/CloudStorage/GoogleDrive-ivo@iris.ai/.shortcut-targets-by-id/0B1Dd1wWV_2fRLXFaV2ppdTBqMzA/Iris.ai - Everyone
```

Set `$IRIS_EVERYONE` in `~/.zshrc` to this path. The `engagements/CLAUDE.md` convention references it.

## Why these particular MCPs

The set is built around the **morning-brief loop** + **engagement reconstruction**:

- Calendar tells the brief what calls are today.
- Gmail/Drive/Slack find the source-of-truth for what was said/sent.
- Asana holds the commercial state (post-Viktor 2026-05-15 directive).
- HubSpot would close the loop on deal-stage; gated.
- Canva is light usage, deck templates.

For client work, Drive is canonical. For internal state, Asana is canonical. For political/comms state, Slack is canonical. Each MCP maps to one of those.
