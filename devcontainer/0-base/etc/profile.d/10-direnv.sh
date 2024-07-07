#!/bin/sh

if [ -n "$BASH_VERSION" ]; then
    eval "$(direnv hook bash)"
elif [ -n "$ZSH_VERSION" ]; then
    eval "$(direnv hook zsh)"
fi

# TODO: Other shells (fish, etc.)
