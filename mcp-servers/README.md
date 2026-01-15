# MCP Servers

Universal MCP (Model Context Protocol) servers directory accessible by all projects in `coding_stuff/`.

---

## Purpose

This folder contains **only custom-built MCP servers** that need a physical location. These can be accessed by any project in `coding_stuff/`.

**NPM-based servers** (installed via `npx`) do NOT need to be in this folder - they're configured in `.claude.json` and run directly from npm.

---

## Complete MCP Server Inventory

### 🔧 Custom-Built Servers (In This Folder)

These are servers you built and need to be stored somewhere:

| Server | Status | Purpose | Location |
|--------|--------|---------|----------|
| [google-calendar-mcp](google-calendar-mcp/) | ✓ Connected | Google Calendar integration | This folder |
| [google-sheets-mcp](google-sheets-mcp/) | ✓ Connected | Google Sheets integration | This folder |
| [trello-mcp-server](trello-mcp-server/) | ⚠ Needs Fix | Trello integration | This folder |
| [playwright-mcp](playwright-mcp/) | Not used | Local Playwright (unused, npx version preferred) | This folder |

### 📦 NPM-Based Servers (User-Level Config)

Configured in `~/.claude.json` at user level:

| Server | Status | Purpose | Installation |
|--------|--------|---------|--------------|
| **n8n-mcp** | ✓ Connected | N8N workflow automation | `npx n8n-mcp` |
| **notion** | ✓ Connected | Notion API integration | `npx @notionhq/notion-mcp-server` |

### 📦 NPM-Based Servers (Project-Level Config)

Configured in `~/.claude.json` for `/Users/swayclarke/coding_stuff`:

| Server | Status | Purpose | Installation |
|--------|--------|---------|--------------|
| **playwright** | ✓ Connected | Browser automation (npx version) | `npx @playwright/mcp@latest` |
| **make** | ⚠ Needs Auth | Make.com automation | SSE: `https://mcp.make.com/sse` |
| **canva-dev** | ✓ Connected | Canva development tools | `npx @canva/cli@latest mcp` |
| **figma-context** | ✓ Connected | Figma design integration | `npx figma-developer-mcp` |
| **github-mcp** | ✓ Connected | GitHub integration | `npx @modelcontextprotocol/server-github` |
| **m365-cli** | ✓ Connected | Microsoft 365 CLI | `npx @pnp/cli-microsoft365-mcp-server@latest` |
| **youtube** | ✓ Connected | YouTube API | `npx @sfiorini/youtube-mcp` |
| **oura** | ✓ Connected | Oura Ring health data | `uvx oura-mcp-server` |

---

## Why Two Types?

### Custom-Built Servers Need This Folder
When you build your own MCP server (like the Google Calendar or Trello integrations), the code needs to live somewhere. That's what this `mcp-servers/` folder is for.

### NPM-Based Servers Don't Need This Folder
Servers installed via `npx` are automatically fetched from npm when needed. They don't need a physical folder in your project.

---

## Configuration

MCP servers are configured in `/Users/swayclarke/.claude.json`

Current paths for custom servers:
```json
{
  "google-calendar": {
    "command": "node /Users/swayclarke/coding_stuff/mcp-servers/google-calendar-mcp/build/index.js",
    "env": {
      "GOOGLE_OAUTH_CREDENTIALS": "/Users/swayclarke/coding_stuff/mcp-servers/google-calendar-mcp/gcp-oauth.keys.json"
    }
  },
  "google-sheets": {
    "command": "node /Users/swayclarke/coding_stuff/mcp-servers/google-sheets-mcp/dist/index.js",
    "env": {
      "GOOGLE_OAUTH_CREDENTIALS": "/Users/swayclarke/coding_stuff/mcp-servers/google-sheets-mcp/dist/gcp-oauth.keys.json"
    }
  },
  "trello": {
    "command": "node /Users/swayclarke/coding_stuff/mcp-servers/trello-mcp-server/dist/index.js"
  }
}
```

---

## Adding New MCP Servers

When building a new custom MCP server:

1. Create it in this folder: `/Users/swayclarke/coding_stuff/mcp-servers/your-server-name/`
2. Build and test it
3. Add to Claude Code configuration:
   ```bash
   claude mcp add your-server --transport stdio -- node /Users/swayclarke/coding_stuff/mcp-servers/your-server-name/dist/index.js
   ```

---

## Troubleshooting

### Check server health
```bash
claude mcp list
```

### Remove and re-add a server
```bash
claude mcp remove server-name
claude mcp add server-name --transport stdio -- node /path/to/server/index.js
```

### Check server logs
Most servers log to console. Run the command directly to see errors:
```bash
node /Users/swayclarke/coding_stuff/mcp-servers/google-calendar-mcp/build/index.js
```

---

## Credentials

Credential files are stored within each MCP server folder:
- Google Calendar: `google-calendar-mcp/gcp-oauth.keys.json`
- Google Sheets: `google-sheets-mcp/dist/gcp-oauth.keys.json`
- Trello: Check `trello-mcp-server/` for API key configuration

**Never commit credential files to git!**
