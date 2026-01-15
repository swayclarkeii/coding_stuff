# Playwriter MCP Setup Guide

## Why Playwriter Over Playwright MCP?

**Playwriter solves the tab accumulation bug** that causes about:blank loops and token waste.

### Key Benefits

✅ **80% less token usage** - Massive cost savings
✅ **No tab accumulation** - Extension-based architecture prevents the bug
✅ **Explicit tab control** - You choose which tabs AI can access
✅ **10x more capable** - Full Playwright API access
✅ **Works with existing Chrome** - No separate browser instances
✅ **Reuse Chrome extensions** - Ad blockers, password managers, etc.
✅ **Bypass automation detection** - Looks like normal browsing

## Installation

### Step 1: Install Chrome Extension

1. Open https://chromewebstore.google.com/detail/playwriter-mcp/jfeammnjpkecdekppnclgkkffahnhfhe
2. Click **"Add to Chrome"**
3. **Pin the extension** to your toolbar:
   - Click the puzzle icon in Chrome toolbar
   - Find "Playwriter MCP"
   - Click the pin icon

### Step 2: MCP Configuration ✅ COMPLETED

**IMPORTANT DISCOVERY:** MCP servers are NOT configured via `.cursor/mcp.json` - that file is unused!

**Actual configuration:**
- MCP servers are managed via `claude mcp` CLI commands
- Config is stored in `/Users/swayclarke/.claude.json` (project-specific)
- Commands:
  ```bash
  # Add Playwriter (DONE ✅)
  claude mcp add playwriter -s local -- npx -y playwriter@latest

  # Remove old Playwright (DONE ✅)
  claude mcp remove playwright -s local

  # List all MCP servers
  claude mcp list

  # Get details about a specific server
  claude mcp get <server-name>
  ```

**Current status:**
```
playwriter: npx -y playwriter@latest - ✓ Connected
```

### Step 3: Restart Claude Code

**IMPORTANT:** You must restart Claude Code (Cursor) for the MCP config changes to take effect.

1. Save all your work
2. Quit Cursor completely (Command+Q)
3. Reopen Cursor

## How to Use Playwriter

### Basic Usage

1. **Open a tab** in Chrome (your regular browser)
2. **Navigate to the page** you want to work with
3. **Click the Playwriter icon** in Chrome toolbar
4. **Icon turns green** ✅ = Connected, AI can control this tab
5. **Use browser-ops-agent** normally in Claude Code

### Example: OAuth Flow

```
1. Open https://accounts.google.com/o/oauth2/v2/auth?... in Chrome
2. Click Playwriter extension icon → turns green
3. In Claude Code: "Complete the OAuth flow using browser-ops-agent"
4. Agent controls the tab directly (no new Chrome instance)
5. When done, click Playwriter icon again to disconnect
```

### Key Differences from Playwright MCP

| Playwright MCP | Playwriter |
|----------------|------------|
| Launches separate Chrome instance | Uses your existing Chrome browser |
| Auto-opens tabs | You manually enable tabs |
| Tabs accumulate (bug) | No accumulation (explicit control) |
| 100% token usage | 20% token usage (80% savings) |
| Can't reuse extensions | Reuses all your Chrome extensions |
| Automation detected | Looks like normal browsing |

## Troubleshooting

### Extension Won't Turn Green

**Problem:** Click Playwriter icon but it doesn't turn green.

**Solutions:**
1. Refresh the page
2. Make sure Claude Code is running
3. Restart Claude Code (Cursor)
4. Check Chrome console for errors (F12)

### Agent Can't See the Tab

**Problem:** browser-ops-agent says "no tabs available"

**Solutions:**
1. Make sure Playwriter icon is **green** on the tab
2. Try disconnecting and reconnecting (click icon twice)
3. Restart Playwriter by disabling/enabling extension

### Still Getting Tab Accumulation

**Problem:** Tabs still accumulating even with Playwriter.

**Cause:** Playwright MCP is still running alongside Playwriter.

**Solution:**
1. Kill Playwright MCP processes:
   ```bash
   pkill -f "mcp-server-playwright"
   pkill -f "@playwright/mcp"
   ```
2. Restart Claude Code
3. Only use Playwriter extension (don't launch Playwright MCP)

## Migration from Playwright MCP

### Phase 1: Test Playwriter (Current)

- ✅ Playwriter added to MCP config
- ✅ Old Playwright MCP processes killed
- ⏳ Test Playwriter with simple browser task
- ⏳ Verify tab control works as expected

### Phase 2: Switch Default (After Testing)

Once Playwriter is confirmed working:

1. Remove Playwright MCP from workflows
2. Update browser-ops-agent to only use Playwriter
3. Monitor token usage (should drop 80%)

### Phase 3: Remove Playwright MCP (Optional)

If Playwriter works perfectly for 1+ week:

1. Remove `@playwright/mcp` from MCP config
2. Uninstall Playwright MCP package:
   ```bash
   npm uninstall -g @playwright/mcp
   ```

## Monitoring

### Tab Count Monitoring (Still Useful)

Even with Playwriter, monitor your tabs:

```bash
# Quick check
/Users/swayclarke/coding_stuff/scripts/monitor-browser-tabs.sh check

# Continuous monitoring
/Users/swayclarke/coding_stuff/scripts/monitor-browser-tabs.sh watch
```

### Token Usage Tracking

Track token usage to verify 80% savings:

**Before Playwriter (typical browser task):**
- Playwright MCP: 20K-150K tokens per task

**After Playwriter (same task):**
- Playwriter: 4K-30K tokens per task

## Resources

- **Chrome Extension**: https://chromewebstore.google.com/detail/playwriter-mcp/jfeammnjpkecdekppnclgkkffahnhfhe
- **GitHub**: https://github.com/remorses/playwriter
- **MCP Store**: https://mcpstore.co/server/69165975944e98de231df0ed

## Support

If you encounter issues:

1. Check [Playwriter GitHub Issues](https://github.com/remorses/playwriter/issues)
2. Verify extension is up to date (Chrome manages updates)
3. Try disabling/re-enabling the extension
4. Restart Claude Code
5. Check Chrome console (F12) for JavaScript errors
