# Notion MCP Integration Fix - January 3, 2026

## Problem Identified

The Notion MCP integration in Cursor was failing with 401 "API token is invalid" errors, even though the token worked with direct curl tests.

## Root Cause

**Environment Variable Mismatch:**
- The official `@notionhq/notion-mcp-server` package requires `NOTION_TOKEN`
- The config at `~/.cursor/mcp.json` was using `NOTION_API_KEY`
- This caused the MCP server to start without the token, resulting in 401 errors

## Changes Made

### 1. Updated `~/.cursor/mcp.json`

**Before:**
```json
"notion": {
  "command": "npx",
  "args": ["-y", "@suekou/mcp-notion-server"],
  "env": {
    "NOTION_API_KEY": "ntn_z7558708008939B4mm5n0EiLw0yqD4qHrVQVxwnqc4Z1VJ"
  }
}
```

**After:**
```json
"notion": {
  "command": "npx",
  "args": ["-y", "@notionhq/notion-mcp-server"],
  "env": {
    "NOTION_TOKEN": "ntn_z7558708008939B4mm5n0EiLw0yqD4qHrVQVxwnqc4Z1VJ"
  }
}
```

**Changes:**
1. Switched to official package `@notionhq/notion-mcp-server` (was `@suekou/mcp-notion-server`)
2. Changed environment variable from `NOTION_API_KEY` to `NOTION_TOKEN`

### 2. Cleaned up stale processes

- Killed 30+ orphaned `notion-mcp-server` processes
- Cleared npx cache to ensure fresh package installation

## Next Steps for User

1. **Restart Cursor completely** (Quit and reopen)
2. Try using Notion MCP tools in Cursor
3. Test with the Tasks database (ID: `39b8b725-0dbd-4ec2-b405-b3bba0c1d97e`)

## Test Script

Created `/Users/swayclarke/coding_stuff/test-notion-mcp.sh` to verify the MCP server can start with the correct token.

Run with:
```bash
/Users/swayclarke/coding_stuff/test-notion-mcp.sh
```

## Database IDs for Testing

- **Tasks:** `39b8b725-0dbd-4ec2-b405-b3bba0c1d97e`
- **Projects:** `2d01c288bb2881f6a1bee57188992200`

## Integration Token

- **Name:** Claude Code MCP 2
- **Token:** `ntn_z7558708008939B4mm5n0EiLw0yqD4qHrVQVxwnqc4Z1VJ`
- **Verified working:** Yes (via curl test to `https://api.notion.com/v1/users/me`)

## Status

✅ Config fixed
✅ Stale processes cleared
✅ Package cache cleared
⏳ Waiting for Cursor restart to test

## References

- Official docs: [Notion MCP Server README](https://www.npmjs.com/package/@notionhq/notion-mcp-server)
- Environment variable requirement: `NOTION_TOKEN` (not `NOTION_API_KEY`)
- Config location: `~/.cursor/mcp.json`
