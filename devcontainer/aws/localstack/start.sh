#!/usr/bin/env bash
set -Eeo pipefail

function _intercept {
    echo "Interrupting supervisord"
    kill -INT $child
    exit 0
}

trap _intercept SIGTERM
trap _intercept SIGINT
trap _intercept SIGQUIT
trap _intercept EXIT

tail -f /var/log/supervisor/services.log &
/usr/bin/supervisord -c /etc/supervisor/supervisord.conf -n -s & child=$!

wait "$child"
