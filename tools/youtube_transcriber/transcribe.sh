#!/bin/bash
# Wrapper script to run YouTube transcriber with virtual environment

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Use the virtual environment's Python
./venv/bin/python3 youtube_transcriber.py "$@"
