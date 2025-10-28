#!/usr/bin/env bash
set -e

FLASK_PORT="${FLASK_RUN_PORT:-5000}"
DEBUG_PORT="${DEBUG_PORT:-5678}"
HOST_OPTS=(--host=0.0.0.0 --port="${FLASK_PORT}")

if [[ "${FLASK_DEBUG_MODE:-0}" == "1" ]]; then
    echo "Starting Flask under debugpy on port ${DEBUG_PORT}"
    exec python -Xfrozen_modules=off -m debugpy \
      --listen "0.0.0.0:${DEBUG_PORT}" \
      --log-to-stderr \
      run.py
else
    echo "Starting Flask normally on port ${FLASK_PORT}"
    exec flask run "${HOST_OPTS[@]}"
fi

