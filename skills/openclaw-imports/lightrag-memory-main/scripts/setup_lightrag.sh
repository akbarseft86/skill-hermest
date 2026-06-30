#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="${HOME}/lightrag"
VENV_DIR="$BASE_DIR/.venv"
PORT="${LIGHTRAG_PORT:-9621}"

mkdir -p "$BASE_DIR"
cd "$BASE_DIR"

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
pip -q install --upgrade pip
pip -q install "lightrag-hku[api]"

if [[ ! -f "$BASE_DIR/.env" ]]; then
  cat > "$BASE_DIR/.env" <<'EOF'
# Minimal LightRAG env
HOST=0.0.0.0
PORT=9621
OPENAI_API_KEY=
# Set provider/model configs as needed for your deployment.
EOF
fi

if pgrep -f "lightrag-server" >/dev/null 2>&1; then
  echo "lightrag-server already running"
else
  nohup lightrag-server > "$BASE_DIR/server.log" 2>&1 &
  sleep 3
fi

echo "LightRAG setup done. Check: http://127.0.0.1:${PORT}"
