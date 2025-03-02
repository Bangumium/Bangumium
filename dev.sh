#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/frontend" || exit
npm run dev &
vitepid=$!
cd "$SCRIPT_DIR" || exit
sleep 2
python3 ./main.py --dev-mode
trap 'kill $vitepid; wait $vitepid; exit' EXIT
