#!/bin/sh
set -eu

cd /app
uvicorn app.main:app --host 127.0.0.1 --port 8000 --timeout-keep-alive 120 &
backend_pid=$!

cd /app/frontend
PORT="${PORT:-3000}" HOSTNAME=0.0.0.0 node server.js &
frontend_pid=$!

terminate() {
    kill "$backend_pid" "$frontend_pid" 2>/dev/null || true
}
trap terminate INT TERM

# The platform only restarts the container when PID 1 exits, so surface a dead
# child instead of serving a half-broken deployment (e.g. API up, frontend down).
while kill -0 "$backend_pid" 2>/dev/null && kill -0 "$frontend_pid" 2>/dev/null; do
    sleep 5
done

if ! kill -0 "$backend_pid" 2>/dev/null; then
    echo "start.sh: backend (uvicorn) exited; shutting down container" >&2
else
    echo "start.sh: frontend (next) exited; shutting down container" >&2
fi

terminate
exit 1
