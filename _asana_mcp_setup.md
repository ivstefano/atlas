# Asana MCP — setup state

**Last touched:** 2026-08-06
**Status:** ✅ connected and verified

Current config (project scope, atlas):

```
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

Then `/mcp` → asana → Authenticate. No manual app, no client_id, no fixed callback port. Verified by reading `Iris.ai Commercial Engagements` (15 sections returned).

---

## The problem we fixed

Symptom: `/mcp` showed `✘ Failed to connect — Incompatible auth server: does not support dynamic client registration`. Re-authenticating didn't help; the browser said "Authentication successful" while Claude Code still reported "not authenticated".

### Root cause

Asana runs **two MCP endpoints with different OAuth setups**:

| Endpoint | Auth server | `registration_endpoint`? | Self-registers? |
|---|---|---|---|
| `https://mcp.asana.com/v2/mcp` | `https://app.asana.com` | ❌ absent | No — needs a manual app |
| `https://mcp.asana.com/sse` (v1) | `https://mcp.asana.com` | ✅ present | Yes |

We were on **v2**. It delegates OAuth to `app.asana.com`, which publishes no `registration_endpoint`, so Claude Code cannot dynamically register a client. That is the error, verbatim.

This is **not** an account, plan, or permission limitation — it's a property of the endpoint. Earlier notes claimed "Asana stopped supporting dynamic client registration" account-wide; that was wrong.

The old hardcoded `clientId 1215193037432916` ("Atlas MCP" app) in the config was a manual workaround for exactly this. It had been revoked on Asana's side, and because v2 can't self-register, there was no automatic recovery path — hence the loop.

### Fix

Switch to the v1 `/sse` endpoint, which is its own auth server and supports DCR. Then clear the stale state (below) and restart.

---

## Diagnostic method (reusable for any MCP OAuth failure)

Don't guess at credentials. Interrogate the server's OAuth metadata directly.

**1. Does the auth server advertise dynamic registration?**
```bash
curl -s https://mcp.asana.com/.well-known/oauth-authorization-server | python3 -m json.tool | grep registration_endpoint   # present
curl -s https://app.asana.com/.well-known/oauth-authorization-server | python3 -m json.tool | grep registration_endpoint   # absent
```

**2. Which auth server does the resource delegate to?** This is the step that cracked it — the endpoint and its auth server can differ.
```bash
curl -s https://mcp.asana.com/.well-known/oauth-protected-resource      # v1 → authorization_servers: mcp.asana.com
curl -s https://mcp.asana.com/.well-known/oauth-protected-resource/v2   # v2 → authorization_servers: app.asana.com
```

**3. Read the 401 challenge** — it names the exact metadata URL the client will follow:
```bash
curl -s -D- -o /dev/null https://mcp.asana.com/sse | grep -iE "^(HTTP|www-authenticate)"
```

**4. Prove registration works** before blaming local state (201 = server is fine, problem is yours):
```bash
curl -s -o /dev/null -w "HTTP %{http_code}\n" -X POST https://mcp.asana.com/register \
  -H "Content-Type: application/json" \
  -d '{"client_name":"Claude Code","redirect_uris":["http://localhost:8888/callback"],"token_endpoint_auth_method":"none"}'
```

If a sibling endpoint self-registers, prefer it over registering an app by hand.

---

## Cleanup: `claude mcp remove` is not enough

It only clears #1. Cached OAuth state survives in three places, and leftovers cause "authenticated but not connected":

1. **Config** — `~/.claude.json` → `projects."/Users/iris/Documents/atlas".mcpServers.asana`
2. **macOS keychain** — service `Claude Code-credentials`, key `mcpOAuth`, entries `asana|<hash>`. Holds cached `authorizationServerUrl`, `clientId`, `redirectUri`.
3. **Auth cache** — `~/.claude/mcp-needs-auth-cache.json`

Surgical keychain edit (back up first; preserve `claudeAiOauth` = your Claude login, and other servers):

```bash
security find-generic-password -s "Claude Code-credentials" -w > creds-backup.json
python3 -c "
import json
d=json.load(open('creds-backup.json'))
for k in [k for k in d['mcpOAuth'] if k.startswith('asana')]: d['mcpOAuth'].pop(k)
open('creds-new.json','w').write(json.dumps(d))
"
security add-generic-password -U -s "Claude Code-credentials" -a "$USER" -w "$(cat creds-new.json)"
```

Inspect entries without dumping secrets:
```bash
security find-generic-password -s "Claude Code-credentials" -w | python3 -c "
import sys,json; d=json.load(sys.stdin)
for k,v in d['mcpOAuth'].items(): print(k, v.get('serverUrl'), 'token:', bool(v.get('accessToken')))"
```

---

## Failure modes

- **Config edits appear to do nothing; `/mcp` shows the old URL** → the running session loaded `mcpServers` at startup and holds it in memory. **Restart Claude Code.** Tell: the browser callback URL contains the *old* client_id or port. This cost us a full round-trip — the browser reported success while the token was bound to the revoked legacy client.
- **`accessToken` empty after a "successful" login** → token was issued to a stale client, or the callback port didn't match the registered `redirectUri`. Clear keychain entry, restart, re-auth.
- **Auth completes but tools don't appear** → restart the session.
- **Port conflict** (only when pinning a port; unnecessary on v1) → `lsof -ti:8888 -sTCP:LISTEN`.

---

## Generalises to other MCPs

Same error, same shape as **HubSpot** (see [_hubspot_mcp_setup.md](_hubspot_mcp_setup.md)) — but a different cause, so don't pattern-match blindly:

- **Asana** — endpoint-specific. A sibling endpoint self-registers. Fixed by switching endpoints.
- **HubSpot** — genuinely needs a pre-registered app; blocked on developer-tools permission from the account admin, not on anything local.

Order of attack for "does not support dynamic client registration": check for an alternate endpoint first (free), then clear stale local state, and only then register an app by hand.

## Fallback if v1 is deprecated

Asana documents v1 as the older endpoint. If retired, go back to the manual app: create an **MCP-type** app at https://app.asana.com/0/my-apps, redirect URL `http://localhost:8888/callback`, then:

```
claude mcp add --transport http --client-id <id> --client-secret --callback-port 8888 asana https://mcp.asana.com/v2/mcp
```

Don't tick "native or command-line app" (switches to `urn:ietf:wg:oauth:2.0:oob`, breaks localhost redirects). Don't use API app type — MCP app type is correct for v2.

## Related

- [memory/asana-mcp-oauth-setup.md](../.claude/projects/-Users-iris-Documents-atlas/memory/asana-mcp-oauth-setup.md) — short version
- [_config/mcps.md](_config/mcps.md) — full MCP roster
- Key IDs: `Iris.ai Commercial Engagements` `1214855342290138`; `Product Roadmap > Scoping Demo Automation` `1214888380737527`
