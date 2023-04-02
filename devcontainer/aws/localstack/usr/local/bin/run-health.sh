#!/usr/bin/env bash
set -Eeo pipefail

function _intercept {
    echo "Stopping health ($child)"
    kill -INT $child
    exit 0
}

trap _intercept SIGTERM
trap _intercept SIGINT
trap _intercept SIGQUIT
trap _intercept EXIT

/usr/local/bin/uvicorn health:app \
    --host 0.0.0.0 \
    --port 9000 \
    --log-level critical \
    & child=$!

wait "$child"