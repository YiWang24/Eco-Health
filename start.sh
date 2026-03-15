#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-all}"
RUN_DIR="$ROOT_DIR/.run"
BACKEND_LOG="$RUN_DIR/backend.log"
FRONTEND_LOG="$RUN_DIR/frontend.log"

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd"
    exit 1
  fi
}

ensure_backend_env() {
  if [[ ! -f "$ROOT_DIR/backend/.env" && -f "$ROOT_DIR/backend/.env.example" ]]; then
    cp "$ROOT_DIR/backend/.env.example" "$ROOT_DIR/backend/.env"
    echo "Created backend/.env from backend/.env.example"
  fi
}

apply_backend_runtime_defaults() {
  export ENV="${ENV:-development}"
  export AUTH_BYPASS_ENABLED="${AUTH_BYPASS_ENABLED:-false}"

  # For local hackathon demo stability: use SQLite by default.
  # Set USE_ENV_DATABASE_URL=1 to allow backend/.env DATABASE_URL to take effect.
  if [[ "${USE_ENV_DATABASE_URL:-0}" != "1" ]]; then
    export DATABASE_URL=""
    export SQLITE_MODE="${SQLITE_MODE:-file}"
  fi
}

start_backend_foreground() {
  require_cmd uv
  ensure_backend_env
  apply_backend_runtime_defaults
  cd "$ROOT_DIR/backend"
  exec uv run uvicorn app.main:app --reload --port 8000
}

start_frontend_foreground() {
  require_cmd npm
  cd "$ROOT_DIR/frontend"
  exec npm run dev
}

wait_for_http() {
  local name="$1"
  local url="$2"
  local attempts="${3:-40}"

  local i=1
  while [[ "$i" -le "$attempts" ]]; do
    if curl -fsS --max-time 1 "$url" >/dev/null 2>&1; then
      return 0
    fi
    sleep 0.5
    i=$((i + 1))
  done
  echo "$name is not healthy at $url"
  return 1
}

start_all_background() {
  require_cmd uv
  require_cmd npm
  require_cmd curl
  ensure_backend_env
  apply_backend_runtime_defaults
  mkdir -p "$RUN_DIR"

  (
    cd "$ROOT_DIR/backend"
    exec uv run uvicorn app.main:app --reload --port 8000
  ) >"$BACKEND_LOG" 2>&1 &
  BACKEND_PID=$!

  (
    cd "$ROOT_DIR/frontend"
    exec npm run dev
  ) >"$FRONTEND_LOG" 2>&1 &
  FRONTEND_PID=$!

  cleanup() {
    kill "$BACKEND_PID" "$FRONTEND_PID" >/dev/null 2>&1 || true
  }
  trap cleanup INT TERM EXIT

  echo "Backend running:  http://localhost:8000  (pid=$BACKEND_PID)"
  echo "Frontend running: http://localhost:3000  (pid=$FRONTEND_PID)"
  echo "Logs:"
  echo "  $BACKEND_LOG"
  echo "  $FRONTEND_LOG"
  echo "Checking service health..."

  if ! wait_for_http "Backend" "http://127.0.0.1:8000/docs" 50; then
    echo "--- backend.log (tail) ---"
    tail -n 80 "$BACKEND_LOG" || true
    exit 1
  fi

  if ! wait_for_http "Frontend" "http://127.0.0.1:3000" 60; then
    echo "--- frontend.log (tail) ---"
    tail -n 80 "$FRONTEND_LOG" || true
    exit 1
  fi

  echo "Both services are healthy. Press Ctrl+C to stop both."

  wait "$BACKEND_PID" "$FRONTEND_PID"
}

usage() {
  cat <<'EOF'
Usage:
  ./start.sh all       # start backend + frontend
  ./start.sh backend   # start backend only
  ./start.sh frontend  # start frontend only
EOF
}

case "$MODE" in
all)
  start_all_background
  ;;
backend)
  start_backend_foreground
  ;;
frontend)
  start_frontend_foreground
  ;;
*)
  usage
  exit 1
  ;;
esac
