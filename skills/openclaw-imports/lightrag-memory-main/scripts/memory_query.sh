#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"query text\""
  exit 1
fi

BASE_URL="${LIGHTRAG_BASE_URL:-http://127.0.0.1:9621}"
QUERY="$*"

curl -sS -X POST "$BASE_URL/query" \
  -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg q "$QUERY" '{query:$q, mode:"mix"}')"
