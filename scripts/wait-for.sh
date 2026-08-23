#!/usr/bin/env sh
# Usage: ./scripts/wait-for.sh HOST PORT [TIMEOUT_SECONDS]
set -eu
HOST="${1:?host required}"
PORT="${2:?port required}"
TIMEOUT="${3:-60}"
i=0
while [ "$i" -lt "$TIMEOUT" ]; do
  if nc -z "$HOST" "$PORT" 2>/dev/null || (echo >/dev/tcp/"$HOST"/"$PORT") 2>/dev/null; then
    echo "$HOST:$PORT is available"
    exit 0
  fi
  i=$((i + 1))
  sleep 1
done
echo "timeout waiting for $HOST:$PORT" >&2
exit 1
