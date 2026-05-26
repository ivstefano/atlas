# HubSpot MCP — setup state

**Last touched:** 2026-05-17
**Status:** blocked, waiting on Ivan Georgiev (CFO) to grant developer tools permission

## Where we are

Goal: connect HubSpot's remote MCP server (`https://mcp.hubspot.com`) to Claude Code so HubSpot CRM (deals, contacts, companies, pipeline) is queryable from atlas / engagements sessions.

### Done
1. Confirmed HubSpot MCP server details from official docs: `https://mcp.hubspot.com`, transport `streamable-http`, auth OAuth 2.0 + PKCE.
2. Registered server at user scope: `claude mcp add --transport http --scope user hubspot https://mcp.hubspot.com`. Lives in `~/.claude.json` top-level `mcpServers`.
3. Verified it shows in `/mcp` after Claude Code restart.

### Blocked
4. OAuth flow fails with: `SDK auth failed: Incompatible auth server: does not support dynamic client registration`.
5. Both Claude Code's built-in /mcp Authenticate flow AND the server-exposed `mcp__hubspot__authenticate` tool return this error.
6. Means: HubSpot's auth server requires a pre-registered OAuth client. Need to create an MCP auth app in Iris.ai's HubSpot developer portal and pass `--client-id` / `--client-secret` to `claude mcp add`.

### Blocker root cause
- `ivo@iris.ai` is bound to Iris.ai HubSpot account (Hub ID 2048671).
- User role on that account lacks "developer tools" permission → can't access developer portal to create the MCP auth app.
- This is a Super Admin permission. Ivan Georgiev (CFO) owns Iris.ai HubSpot account admin.

### Action sent
- 2026-05-17: Slack DM to Ivan in Bulgarian asking for developer tools permission on my user.
- Expected response: tomorrow (2026-05-18) or shortly after.

## When Ivan grants access — next steps

1. Log into https://developers.hubspot.com with `ivo@iris.ai`, select Iris.ai account (Hub ID 2048671).
2. Developer portal → Apps → Create MCP auth app.
3. Set redirect URL to `http://localhost:8765/callback` (port arbitrary, must match `--callback-port` below).
4. Copy Client ID + Client Secret.
5. Re-register the MCP server with the credentials:
   ```
   claude mcp remove hubspot --scope user
   claude mcp add --transport http --scope user \
     --client-id <CLIENT_ID> \
     --client-secret \
     --callback-port 8765 \
     hubspot https://mcp.hubspot.com
   ```
   (`--client-secret` flag prompts interactively, doesn't put secret on command line.)
6. Restart Claude Code, run `/mcp` → select hubspot → Authenticate. Browser opens, approve, redirects back.
7. Verify with `claude mcp list` — should show `hubspot: ... - ✓ Connected`.
8. Update memory: flip `mcp-and-sources.md` "HubSpot no" line to confirmed connected.

## References
- HubSpot remote MCP docs: https://developers.hubspot.com/docs/apps/developer-platform/build-apps/integrate-with-the-remote-hubspot-mcp-server
- Current registration: `~/.claude.json` top-level `mcpServers.hubspot` (left in place, will be removed in step 5 above)
- Precedent (working OAuth MCP via same pattern): Asana — `claude mcp list` shows it connected
