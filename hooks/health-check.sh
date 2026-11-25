#!/usr/bin/env bash
# Says at session start whether the Metrikia server answers. One request, no
# credential and no data in it: a 401 is the expected answer, the sign-in
# happens in the client. No variable and no command substitution here, the
# plugin directory holds for a reviewer a script that it cannot follow.
set -uo pipefail

if ! command -v curl > /dev/null 2>&1; then
  echo "> **Note:** \`curl\` not found. Metrikia reachability check skipped."
  exit 0
fi

if curl -s -o /dev/null -w "%{http_code}" --max-time 3 "https://mcp.metrikia.io/api/v1/mcp" 2> /dev/null | grep -qxE '2[0-9][0-9]|401'; then
  echo "> **Sign-in:** not connected yet? Run \`/mcp\`, select the Metrikia server, then Authenticate. No API key."
  exit 0
fi

echo "> **Warning:** the Metrikia server does not answer. Its tools may fail. Check the network connection."
