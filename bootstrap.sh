#!/bin/bash

set -euo pipefail

python3 -m venv .venv

if [[ ! -e ".venv/bin/activate" ]]; then
    echo "Failed to create virtualenv"
    exit 1
fi

source ".venv/bin/activate"

.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt


echo '-------------------------------'
echo ''
echo ' please run:'
echo '     source .venv/bin/activate'
echo ''
echo '-------------------------------'
