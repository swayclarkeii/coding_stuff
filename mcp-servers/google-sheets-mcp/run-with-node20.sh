#!/bin/bash
# Wrapper script to run google-sheets-mcp with Node 20 (for Node 25 compatibility issues)

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"

nvm use 20 > /dev/null 2>&1

exec node /Users/computer/coding_stuff/mcp-servers/google-sheets-mcp/dist/index.js
