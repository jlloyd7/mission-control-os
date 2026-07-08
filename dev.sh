#!/usr/bin/env bash
# Mission Control OS - local dev launcher (macOS / Linux)
# SQLite + mock mode: no Docker or API keys needed.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API="$ROOT/apps/api"

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing prerequisite: $1 ($2)"; exit 1; }; }
need pnpm "npm i -g pnpm"
need python3 "install Python 3.12+"

if [ ! -x "$API/.venv/bin/python" ]; then
  echo "Backend venv missing. Set it up first:"
  echo "  cd apps/api && uv venv && uv pip install -e '.[dev]'"
  exit 1
fi

echo "Launching Mission Control OS..."

( cd "$API" && ./.venv/bin/python -m app.seed && \
  ./.venv/bin/python -m uvicorn app.main:app --reload --port 8000 ) &
API_PID=$!

( cd "$ROOT" && pnpm --filter web dev ) &
WEB_PID=$!

cleanup() { kill "$API_PID" "$WEB_PID" 2>/dev/null || true; }
trap cleanup EXIT INT TERM

# Wait for the web server to respond, then open the browser
for _ in $(seq 1 40); do
  curl -sf http://localhost:3000 >/dev/null 2>&1 && break
  sleep 1
done
( command -v open >/dev/null 2>&1 && open http://localhost:3000 ) \
  || ( command -v xdg-open >/dev/null 2>&1 && xdg-open http://localhost:3000 ) || true

echo "  API  ->  http://localhost:8000/docs"
echo "  Web  ->  http://localhost:3000"
wait
