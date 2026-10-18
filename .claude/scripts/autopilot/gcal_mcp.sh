#!/bin/sh
# Restricted Google Workspace MCP for autopilot headless calls.
#   gcal_mcp.sh readonly  -> gmail+calendar, read-only scopes, write tools disabled
#   gcal_mcp.sh drafts    -> gmail up to "drafts" level (no send tool), used only by `meeting_autopilot.py gmail-draft`
# Secrets are read from ~/.config/workspace-mcp files at runtime, never stored here.
D="$HOME/.config/workspace-mcp"
export GOOGLE_OAUTH_CLIENT_ID="$(cat "$D/client_id")"
export GOOGLE_OAUTH_CLIENT_SECRET="$(cat "$D/client_secret")"
export USER_GOOGLE_EMAIL="ivo@iris.ai"
export WORKSPACE_MCP_CREDENTIALS_DIR="$D/creds"
case "${1:-readonly}" in
  drafts) exec /opt/homebrew/bin/uvx workspace-mcp --single-user --permissions gmail:drafts \
            --disabled-tools send_gmail_message ;;
  *)      exec /opt/homebrew/bin/uvx workspace-mcp --single-user --read-only --tools gmail calendar ;;
esac
