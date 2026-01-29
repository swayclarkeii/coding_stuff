# MCP Configuration Fixes - January 12, 2026

## Summary

Completed comprehensive audit and consolidation of MCP server configurations after folder reorganization in `coding_stuff/`.

## Issues Fixed

### 1. Google Drive MCP Server - Path and Credentials ✅
**Problem:**
- Path pointed to `/Users/swayclarke/coding_stuff/mcp-google-drive/dist/index.js` (didn't exist)
- No credentials configured

**Fixed:**
- Updated path to `/Users/swayclarke/coding_stuff/mcp-servers/google-drive-mcp/dist/index.js`
- Added centralized credentials: `/Users/swayclarke/coding_stuff/.credentials/gcp-oauth.keys.json`

### 2. Google Calendar - Outdated Local Credentials ✅
**Problem:**
- Using local copy from Dec 14 at `mcp-servers/google-calendar-mcp/gcp-oauth.keys.json`

**Fixed:**
- Updated to use centralized credentials: `/Users/swayclarke/coding_stuff/.credentials/gcp-oauth.keys.json` (Jan 8 - newer)

### 3. Google Sheets - Wrong Credentials Path ✅
**Problem:**
- Path pointed to `/Users/swayclarke/coding_stuff/claude-code-os/.credentials/` (didn't exist)

**Fixed:**
- Updated to `/Users/swayclarke/coding_stuff/.credentials/claude-automation-service-account.json`

### 4. n8n MCP Server - Wrong Package and Syntax ✅
**Problem:**
- Configuration used wrong package name `@n8n-mcp/server` (doesn't exist)
- Environment variables passed as CLI args instead of env object

**Fixed:**
- Changed to correct package: `n8n-mcp`
- Moved environment variables to proper `env` field:
  - `N8N_API_URL`: `https://n8n.oloxa.ai`
  - `N8N_API_KEY`: Configured

## Final Configuration Status

### Project-Specific Servers (/Users/swayclarke/coding_stuff)

| Server | Executable | Credentials | Status |
|--------|-----------|-------------|--------|
| **github-mcp** | `npx @modelcontextprotocol/server-github` | None needed | ✅ |
| **google-calendar** | `mcp-servers/google-calendar-mcp/build/index.js` | `.credentials/gcp-oauth.keys.json` | ✅ |
| **google-sheets** | `mcp-servers/google-sheets-mcp/dist/index.js` | `.credentials/claude-automation-service-account.json` | ✅ |
| **notion** | `npx -y @notionhq/notion-mcp-server` | API token in env | ✅ |
| **playwriter** | `npx -y playwriter@latest` | None needed | ✅ |
| **fathom** | `mcp-servers/mcp-fathom-server/dist/index.js` | API key in env | ✅ |
| **playwright** | `npx -y @playwright/mcp@latest` | None needed | ✅ |
| **n8n-mcp** | `npx -y n8n-mcp` | API URL and key in env | ✅ |

### Global Servers

| Server | Executable | Credentials | Status |
|--------|-----------|-------------|--------|
| **google-drive** | `mcp-servers/google-drive-mcp/dist/index.js` | `.credentials/gcp-oauth.keys.json` | ✅ |
| **n8n-mcp** | `npx -y n8n-mcp` | API URL and key in env | ✅ |

## Centralized Credentials Location

All Google OAuth credentials now consolidated in:
```
/Users/swayclarke/coding_stuff/.credentials/
├── claude-automation-service-account.json  # Google Sheets service account
├── gcp-oauth.keys.json                     # Google Calendar & Drive OAuth
├── google-calendar-credentials.json
├── credentials.json
├── n8n-api-key.txt
└── api-keys.md
```

## Verification

All configured paths verified to exist:
- ✅ All MCP server executables found
- ✅ All credential files found
- ✅ All paths point to correct locations

## Next Steps

**RESTART REQUIRED:** Restart Claude Code to load the updated configuration.

After restart, verify connections:
```bash
claude mcp list
```

Expected result: All servers should show "✓ Connected"

## Files Modified

- `/Users/swayclarke/.claude.json` - Updated MCP server configurations
  - Project config: `/Users/swayclarke/coding_stuff`
  - Global config: `mcpServers`
