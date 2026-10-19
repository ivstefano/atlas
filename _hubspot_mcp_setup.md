# HubSpot MCP — setup state

**Last touched:** 2026-10-19
**Status:** connected, read-only

## Config
- Server `https://mcp.hubspot.com` (streamable-http), user scope, name `hubspot`.
- Own MCP auth app in Iris.ai HubSpot (Hub 2048671): app id 57707799, client id `d9329141-2a37-41d0-9971-77b45f1c5d0d`.
- Redirect `http://localhost:8092/callback`, `--callback-port 8092`.
- Client secret: `~/.config/hubspot-mcp/client_secret` (chmod 600). Never in repo or `~/.claude.json`.
- Scopes: "View-only" preset on the consent screen. All write ops return REQUIRES_REAUTHORIZATION by design.

## Re-register (new machine / broken auth)
```
claude mcp remove hubspot --scope user
MCP_CLIENT_SECRET=$(cat ~/.config/hubspot-mcp/client_secret) claude mcp add --transport http --scope user \
  --client-id d9329141-2a37-41d0-9971-77b45f1c5d0d --client-secret --callback-port 8092 \
  hubspot https://mcp.hubspot.com
```
Restart Claude Code, `/mcp` → hubspot → Authenticate, pick View-only.

## Adding write access later
Re-run `/mcp` Authenticate and tick the needed write scopes (e.g. notes) on the consent screen.

## History
- 2026-05-17: blocked, `ivo@iris.ai` lacked developer tools permission; dynamic client registration unsupported, so a pre-registered app is required.
- 2026-10-19: developer access granted, app created, connected. Verified: get_user_details + deal search (1362 deals).

## References
- https://developers.hubspot.com/docs/apps/developer-platform/build-apps/integrate-with-the-remote-hubspot-mcp-server
