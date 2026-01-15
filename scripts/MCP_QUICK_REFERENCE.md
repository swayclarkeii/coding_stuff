# MCP Mode Quick Reference

**For:** Quickly understanding what to say to Claude Code for MCP management

---

## What You Say vs What Claude Should Do

| What You Say | What Claude Does | Result |
|--------------|------------------|--------|
| "Switch to core-mode" | Runs `/Users/swayclarke/coding_stuff/scripts/mcp-toggle.sh core-mode` | 5 servers enabled in next session |
| "Switch to pa-mode" | Runs `/Users/swayclarke/coding_stuff/scripts/mcp-toggle.sh pa-mode` | 9 servers enabled in next session |
| "Enable all MCP servers" | Runs `/Users/swayclarke/coding_stuff/scripts/mcp-toggle.sh enable-all` | 11 servers enabled in next session |
| "Check MCP status" | Runs `/Users/swayclarke/coding_stuff/scripts/mcp-toggle.sh status` | Shows current config |
| "core-mode" (typed directly) | ❌ Doesn't understand | Claude needs context: "Switch to core-mode" |

---

## Terminal Aliases (For Direct Use)

**Already configured in ~/.zshrc:**

```bash
# Just type these in your terminal (iTerm, Terminal.app, etc.)
core-mode           # Switch to core mode
pa-mode             # Switch to PA mode
mcp-status          # Check current status
mcp-enable-all      # Enable all servers
```

**Usage:**
- Open iTerm or Terminal.app
- Type `core-mode` or `pa-mode`
- Changes take effect in next Claude Code session

---

## Understanding the Modes

### core-mode (5 servers)
**When to use:** Daily automation work
**Servers:** n8n-mcp, playwriter, playwright, google-sheets, google-drive
**Token savings:** ~34,000 tokens per conversation vs enable-all

**Good for:**
- Building n8n workflows
- Browser automation (non-Google sites with Playwriter, Google sites with Playwright)
- Google Sheets work
- File operations

### pa-mode (9 servers)
**When to use:** Personal assistant tasks, CRM, GitHub work
**Servers:** All core servers PLUS notion, google-calendar, fathom, github-mcp

**Good for:**
- CRM updates (Notion database)
- Task management (Notion)
- Calendar event management
- GitHub operations (PRs, issues)
- Analytics (Fathom)

### enable-all (11 servers)
**When to use:** Rarely - only when you need slides or docs
**Servers:** All servers including google-slides, google-docs
**Token cost:** ~51,770 tokens per conversation (HIGH)

**Good for:**
- Creating proposals (needs google-slides)
- Document generation (needs google-docs)

---

## Common Issues

### ❌ "Claude doesn't understand when I type 'core-mode'"
**Fix:** Don't type commands directly in Claude Code. Instead:
- Say: "Switch to core-mode"
- Or run in terminal: `core-mode`

### ❌ "Changes aren't taking effect"
**Fix:** Mode changes only affect NEW Claude Code sessions
- Exit current conversation
- Start new conversation
- New mode will be active

### ❌ "Aliases don't work in terminal"
**Fix:** Source your shell config
```bash
source ~/.zshrc
```

Or restart your terminal application.

---

## How It Works (Technical)

**What the script does:**
1. Directly modifies `~/.claude.json`
2. Updates `projects["/Users/swayclarke/coding_stuff"].disabledMcpServers` array
3. Creates backup at `~/.claude.json.backup`
4. Uses `jq` for JSON manipulation

**Why this approach:**
- `claude mcp enable/disable` CLI commands weren't reliable
- Direct JSON editing ensures persistence
- Clear status output

---

## Full Documentation

**Complete guide:** `/Users/swayclarke/coding_stuff/scripts/MCP_MANAGEMENT.md`

**Script location:** `/Users/swayclarke/coding_stuff/scripts/mcp-toggle.sh`

**Project instructions:** `/Users/swayclarke/coding_stuff/CLAUDE.md` (section: MCP SERVER MODE MANAGEMENT)

---

**Last Updated:** 2026-01-13
**Version:** 1.0
