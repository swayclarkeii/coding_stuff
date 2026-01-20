#!/bin/bash
# Test Notion MCP server connection

export NOTION_TOKEN="ntn_z7558708008939B4mm5n0EiLw0yqD4qHrVQVxwnqc4Z1VJ"

echo "Testing Notion MCP server with official package..."
echo "Environment variable NOTION_TOKEN is set: ${NOTION_TOKEN:0:10}..."

# Test that the MCP server can start
timeout 5s npx -y @notionhq/notion-mcp-server 2>&1 | head -20

echo ""
echo "If you see JSON-RPC messages above, the server started successfully."
echo "Now restart Cursor to pick up the updated config at ~/.cursor/mcp.json"
