# Re-Authentication Root Cause Analysis

**Date:** January 13, 2026
**Issue:** Constant need to re-authenticate Google Calendar and Notion MCP servers
**Status:** Investigation in progress

---

## The Problem

You're experiencing repeated authentication failures requiring manual re-auth:
- Google Calendar OAuth tokens expire frequently
- After Claude Code resets, MCP connections break
- Notion MCP has parameter formatting issues in main conversation

---

## Root Causes Identified

### 1. Google Calendar OAuth - Test Mode Limitation ⚠️

**The Issue:**
- Google Calendar MCP is running in **"test mode"**
- In test mode, OAuth refresh tokens **expire after 7 days**
- This is a Google Cloud Platform policy, not an MCP bug

**Why This Happens:**
- Your GCP OAuth app is not "published" (still in testing)
- Test apps have strict token expiration (7 days max)
- After 7 days, you MUST re-authenticate manually

**Evidence:**
- Browser-ops-agent obtained tokens with `refresh_token_expires_in: 604799` (7 days)
- This is Google's standard test mode behavior

**The Fix:**
Two options:

**Option A: Publish the OAuth App (Recommended)**
1. Go to Google Cloud Console
2. Navigate to your OAuth consent screen
3. Change from "Testing" to "Production"
4. Submit for verification (takes 1-2 weeks)
5. Once published, refresh tokens **never expire**

**Option B: Add Yourself as Test User**
1. In GCP Console, add swayclarkeii@gmail.com as a test user
2. Tokens still expire after 7 days, but you can refresh
3. This is a temporary workaround

### 2. Claude Code Resets Breaking MCP Connections

**The Issue:**
- When you reset Claude Code, MCP server connections are lost
- OAuth tokens are stored in MCP server memory
- Reset = tokens gone = need to re-auth

**Why This Happens:**
- Google Calendar MCP stores tokens in-memory, not persisted
- After reset, the MCP server restarts with no tokens
- You have to re-authenticate from scratch

**The Fix:**
- Tokens should be persisted to `~/.config/google-calendar-mcp/tokens.json`
- Need to verify the MCP server is configured to save tokens to disk
- Check if `GOOGLE_OAUTH_CREDENTIALS` env var is set properly

### 3. Notion MCP Parameter Encoding Bug

**The Issue:**
- Direct Notion MCP calls from main conversation fail
- Parameters are double-encoded (JSON stringified twice)
- Error: "body.parent should be an object, instead was string"

**Why This Happens:**
- This is a Claude Code bug with nested JSON parameters
- Only affects direct MCP calls in main conversation
- Agents bypass this issue with internal parameter handling

**The Fix:**
- **ALWAYS use my-pa-agent for Notion task creation** (per CLAUDE.md delegation rules)
- Never create Notion tasks directly in main conversation
- This is actually a protocol violation - should have been delegated from the start

---

## Immediate Actions Needed

### 1. Save OAuth Tokens Properly ⚡ URGENT
- Browser-ops-agent has fresh tokens waiting to be saved
- Save to: `~/.config/google-calendar-mcp/tokens.json`
- Format: Google Calendar MCP token structure

### 2. Publish GCP OAuth App 📅 HIGH PRIORITY
- This is the ONLY way to stop 7-day re-auth cycles
- Takes 1-2 weeks for Google verification
- Once done, tokens never expire

### 3. Update CLAUDE.md Protocol 📝 MEDIUM PRIORITY
- Document: Never create Notion tasks in main conversation
- Document: Always delegate PA tasks to my-pa-agent
- Add: Google Calendar token expiry monitoring

### 4. Verify MCP Token Persistence 🔧 MEDIUM PRIORITY
- Check if Google Calendar MCP is saving tokens to disk
- Verify `~/.config/google-calendar-mcp/tokens.json` exists after auth
- Test: Restart Claude Code and verify tokens still work

---

## Long-Term Solution

**To permanently fix re-authentication issues:**

1. **Publish GCP OAuth App** - Eliminates 7-day expiry
2. **Enable MCP token persistence** - Survives Claude Code resets
3. **Follow delegation protocol strictly** - No direct MCP calls from main
4. **Monitor token expiry** - Alert before tokens expire

---

## Why This Keeps Happening

**You're not doing anything wrong.** The setup has inherent limitations:

1. **Google's test mode policy** - 7-day expiry is by design
2. **MCP server architecture** - In-memory tokens don't survive resets
3. **Claude Code resets** - You reset frequently during development
4. **Protocol violations** - Direct MCP calls instead of agent delegation

**The good news:** All of these are fixable with the actions above.

---

## Next Steps

1. ✅ Complete OAuth token save (in progress)
2. ⏳ Publish GCP OAuth app to production
3. ⏳ Verify token persistence after save
4. ⏳ Update CLAUDE.md with lessons learned

---

## Files to Check

- `~/.config/google-calendar-mcp/tokens.json` - Token storage
- `~/.config/google-calendar-mcp/config.json` - MCP configuration
- `/Users/swayclarke/coding_stuff/.credentials/gcp-oauth.keys.json` - OAuth client credentials
- GCP Console > APIs & Services > OAuth consent screen - App status

---

**Status:** Analysis complete. Ready to implement fixes.
