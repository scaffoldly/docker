#!/usr/bin/env bash
set -Eeo pipefail

function _intercept {
    echo "Stopping proxy ($child)"
    kill -INT $child
    exit 0
}

trap _intercept SIGTERM
trap _intercept SIGINT
trap _intercept SIGQUIT
trap _intercept EXIT

/usr/sbin/nginx \
    -g "daemon off;" \
    & child=$!

wait "$child"
