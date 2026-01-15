# MCP Server Management Guide

## Quick Reference

**Location:** `/Users/swayclarke/coding_stuff/scripts/mcp-toggle.sh`

**Requirements:** `jq` (install with `brew install jq` if not present)

## Common Commands

**Shell Aliases (recommended - already configured in ~/.zshrc):**
```bash
core-mode           # Daily work mode - SAVES ~34K TOKENS
pa-mode             # Personal assistant work
mcp-status          # Show current status
mcp-enable-all      # Enable everything (high token cost)
```

**Direct Script Calls (if aliases not available):**
```bash
./scripts/mcp-toggle.sh status
./scripts/mcp-toggle.sh core-mode
./scripts/mcp-toggle.sh pa-mode
./scripts/mcp-toggle.sh enable-all
./scripts/mcp-toggle.sh list
```

**In Claude Code conversations:**
- Just ask: "Switch to core-mode" or "Run pa-mode"
- Claude will execute the script for you
- Don't type the command directly - Claude Code won't recognize it as a skill

## Token Costs Per Conversation

| Mode | Active Servers | Token Cost | Use Case |
|------|----------------|------------|----------|
| **minimal** | n8n only | ~6,575 | Testing/minimal operations |
| **core-mode** | n8n, playwriter, playwright, sheets, drive | ~28K-32K | Daily automation work |
| **pa-mode** | calendar, github, sheets, notion | ~34K-38K | PA tasks, CRM, GitHub work |
| **enable-all** | All 11 servers | ~52K | Full feature access |

## Server Breakdown

### Core Servers (core-mode)
- **n8n-mcp** - Automation backbone
- **playwriter** - Browser automation (Playwriter extension)
- **playwright** - Browser automation (legacy/Google sites)
- **google-sheets** - Spreadsheet operations
- **google-drive** - File operations

### PA Mode Servers (pa-mode)
- **google-calendar** - Calendar operations (~8,700 tokens)
- **github-mcp** - GitHub operations (~5,201 tokens)
- **google-sheets** - Spreadsheet operations (~8K-10K tokens)
- **notion** - Task management, CRM (~20,388 tokens)

### Optional (Enable Manually When Needed)
- **google-slides** - Presentation generation
- **google-docs** - Document operations

## Recommended Usage

### Daily Automation Work
```bash
./scripts/mcp-toggle.sh core-mode
```
**Why:** Core essentials only - n8n, browser automation, sheets, drive.

### Personal Assistant Tasks
```bash
./scripts/mcp-toggle.sh pa-mode
```
**Why:** Adds Notion, Calendar, Fathom, GitHub to core servers.

### GitHub Work
```bash
# GitHub is included in pa-mode
./scripts/mcp-toggle.sh pa-mode
```

### Presentation/Docs Work
```bash
# Enable slides/docs manually
claude mcp enable google-slides -s local
claude mcp enable google-docs -s local

# Or switch to enable-all
./scripts/mcp-toggle.sh enable-all
```

## Manual MCP Commands

```bash
# Enable specific server
claude mcp enable <server-name> -s local

# Disable specific server
claude mcp disable <server-name> -s local

# List all servers
claude mcp list

# Check server status
./scripts/mcp-toggle.sh status
```

## When to Use Each Mode

| Scenario | Command | Reason |
|----------|---------|--------|
| Daily automation work | `core-mode` | n8n + browser automation + sheets + drive |
| Building n8n workflows | `core-mode` | n8n + browser automation |
| PA tasks, CRM, task management | `pa-mode` | Calendar + GitHub + Sheets + Notion |
| GitHub work | `pa-mode` | Includes GitHub MCP |
| Creating proposals | Manual enable or `enable-all` | Need google-slides |
| Document operations | Manual enable or `enable-all` | Need google-docs |
| Full feature access | `enable-all` | All integrations available |

## Best Practices

1. **Default to core-mode** for daily automation work
2. **Switch to pa-mode** when doing PA tasks, CRM, or GitHub work
3. **Enable-all temporarily** only when you need slides/docs
4. **Check status** after switching: `./scripts/mcp-toggle.sh status`

## Troubleshooting

### Script not working?
```bash
# Make sure it's executable
chmod +x /Users/swayclarke/coding_stuff/scripts/mcp-toggle.sh

# Run with full path
/Users/swayclarke/coding_stuff/scripts/mcp-toggle.sh status
```

### Server not found?
```bash
# List all available servers
claude mcp list

# Check if server name matches exactly
```

### Changes not taking effect?
```bash
# Restart Claude Code session
# Changes only apply to NEW conversations
```

## Examples

### Morning Setup (Start of Day)
```bash
# Enable core servers for automation work
./scripts/mcp-toggle.sh core-mode

# Check status
./scripts/mcp-toggle.sh status
```

### Switching to PA/GitHub Work
```bash
# Enable PA mode (Calendar + GitHub + Sheets + Notion)
./scripts/mcp-toggle.sh pa-mode

# Work on tasks, CRM, calendar, GitHub
# Note: No n8n or file operations in PA mode
# ...

# Switch back to core when done with PA tasks
./scripts/mcp-toggle.sh core-mode
```

## Cost Savings Example

**Scenario:** 10 conversations per day

**Simple Setup:**
- **core-mode** for daily automation work (5 servers: n8n, playwriter, playwright, sheets, drive)
- **pa-mode** for PA tasks (4 servers: calendar, github, sheets, notion)
- **enable-all** rarely needed (11 servers)

**Key Insight:**
PA mode is now more focused and lighter than core mode. Switch between them based on task type:
- Automation/workflows → core-mode
- Personal tasks/CRM → pa-mode

---

## How It Works

**Technical Details:**
- Script directly modifies `/Users/swayclarke/.claude.json`
- Updates `projects["/Users/swayclarke/coding_stuff"].disabledMcpServers` array
- Creates backup at `~/.claude.json.backup` before each change
- Uses `jq` for JSON manipulation

**Why Direct JSON Modification:**
- `claude mcp enable/disable` CLI commands weren't reliably updating the config
- Direct JSON editing ensures configuration changes persist correctly
- Provides clearer status output showing exactly which servers are enabled/disabled

---

**Last Updated:** 2026-01-13
**Version:** 1.1 (Fixed: Direct JSON modification instead of CLI commands)
