if [[ -n $CODESPACE_NAME && -n $GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN ]]; then
    export LOCALSTACK_ENDPOINT="https://${CODESPACE_NAME}-4566.${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN}"
fi
