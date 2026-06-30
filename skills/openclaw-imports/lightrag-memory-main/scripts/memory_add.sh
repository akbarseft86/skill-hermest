#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"text to store\""
  exit 1
fi

BASE_URL="${LIGHTRAG_BASE_URL:-http://127.0.0.1:9621}"
TEXT="$*"

curl -sS -X POST "$BASE_URL/documents/text" \
  -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg text "$TEXT" '{text:$text}')"
