#!/usr/bin/env bash
set -uo pipefail

if [ -z "${CLAUDE_PLUGIN_ROOT:-}" ]; then
  echo "> **Warning:** CLAUDE_PLUGIN_ROOT is not set. Metrikia health check cannot run."
  exit 0
fi

CONTEXT_FILE="${CLAUDE_PLUGIN_ROOT}/hooks/session-context.md"

if [ ! -r "$CONTEXT_FILE" ]; then
  echo "> **Warning:** Metrikia session-context.md is missing. Plugin may be misconfigured."
  exit 0
fi

# Metrikia authenticates with OAuth 2.1 (no API key to configure). Claude Code
# discovers the authorization server from the MCP endpoint and runs a one-time
# browser sign-in on the first tool call. No METRIKIA_API_KEY is needed.

if ! command -v curl &> /dev/null; then
  cat "$CONTEXT_FILE"
  echo ""
  echo "> **Note:** \`curl\` not found. MCP reachability check skipped."
  exit 0
fi

# Reachability probe (no credentials). A 401 is EXPECTED: it carries the OAuth
# discovery challenge that Claude Code follows. Anything 2xx/401 means the
# server is up; only network/5xx errors warrant a warning.
HTTP_STATUS=$(curl -o /dev/null -s -w "%{http_code}" --max-time 3 \
  "https://mcp.metrikia.io/api/v1/mcp" 2>/dev/null) || HTTP_STATUS="000"

case "$HTTP_STATUS" in
  2*|401)
    cat "$CONTEXT_FILE"
    echo ""
    echo "> **Sign-in:** the first Metrikia tool call opens a browser to connect your account (OAuth). No API key required."
    ;;
  *)
    cat "$CONTEXT_FILE"
    echo ""
    echo "> **Warning:** Metrikia MCP server unreachable (HTTP $HTTP_STATUS). Tools may fail. Check your network connection."
    ;;
esac

exit 0
