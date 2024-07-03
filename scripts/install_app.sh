#!/usr/bin/env bash

# Run from the root of the project
cd $(dirname ${BASH_SOURCE[0]})/..

install_target=${INSTALL_TARGET:-"/Applications"}
cp -r -P dist/ollama-bar.app $install_target/