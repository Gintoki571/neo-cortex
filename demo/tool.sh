#!/usr/bin/env bash
# Call any daemon tool (connect and explore have no `neo` subcommand).  Usage: demo/tool.sh connect '{"a":"INC-03","b":"Chen Wei"}'
. "$(dirname "$0")/env.sh"
curl -fsS -X POST "$NEO_DAEMON_URL/api/$1" -H 'Content-Type: application/json' -d "${2:-{\}}"; echo
