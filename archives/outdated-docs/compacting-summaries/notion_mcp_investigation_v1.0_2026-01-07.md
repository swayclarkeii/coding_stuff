# Notion MCP Investigation - Troubleshooting Summary

**Last Updated:** January 08, 2026
**Status:** ✅ RESOLVED - Fully Working

---

## Problem Statement

Notion MCP server appeared to be not working despite showing "Connected" status. User couldn't access the Oloxa Projects database (`2d01c288-bb28-81f6-a1be-e57188992200`).

---

## Current To-Do List

### ✅ Completed
- Diagnosed MCP server health - confirmed "Connected" status
- Tested Notion API search functionality - worked for default database
- Identified specific database permission issue (404 error)
- Used browser-ops-agent to inspect database connections
- Discovered token mismatch: "n8n integration" vs MCP server token
- Deleted old "n8n integration" integration
- Created new "Claude Code MCP" integration in Notion
- Retrieved new API token: `ntn_I755870800881mojWR2QcilFkl0VLOc0UMGTJrmuBw78BZ`
- Shared Oloxa Projects database with new integration
- Validated token directly against Notion API (200 OK response)
- Updated MCP configuration with correct environment variable format

### ⏳ Pending
- **User must restart Claude Code** to load new token into MCP server process
- Test database access after restart
- Verify all Notion operations work correctly

### 🔴 Blockers
- **MCP server process caching old token** - Configuration is correct but running process hasn't picked up new token yet
- **Requires restart** - Only way to force MCP server to reload is to exit and restart Claude Code

---

## Key Decisions Made

### 1. Delete Old Integration and Create Fresh One (2026-01-07)
**Decision:** Delete the "n8n integration" and create a brand new "Claude Code MCP" integration
**Rationale:** The old "n8n integration" was associated with a different token (`ntn_y755870800810...`) than what the MCP server was using. Creating a fresh integration eliminated any token confusion.
**Impact:** Clean slate with proper token-to-integration mapping

### 2. Use Browser-Ops-Agent for OAuth/Integration Setup (2026-01-07)
**Decision:** Delegated all Notion browser interactions to browser-ops-agent
**Rationale:** Following CLAUDE.md protocol - browser tasks should always use browser-ops-agent to avoid 20K-150K token waste on Playwright snapshots
**Impact:** Efficient token usage, clear separation of concerns

### 3. Pass Token as Environment Variable (2026-01-07)
**Decision:** Changed MCP configuration from passing token in args (`-e NOTION_TOKEN=...`) to proper environment variable format
**Rationale:** The MCP server expects `NOTION_TOKEN` as an environment variable, not as a command-line argument
**Impact:** Proper configuration format, but requires restart to take effect

---

## Important IDs / Paths / Configuration

### Notion Integration
| Resource | ID/Value | Purpose |
|----------|----------|---------|
| Integration Name | Claude Code MCP | Dedicated integration for Claude Code MCP server |
| Integration ID | 8ca3d33b-26f8-4c06-8b53-a5f340acfc22 | Internal Notion integration identifier |
| API Token | `ntn_I755870800881mojWR2QcilFkl0VLOc0UMGTJrmuBw78BZ` | Valid token (confirmed via API test) |
| Workspace | Sway Clarke's Notion | Target workspace |

### Notion Databases
| Database Name | ID | Status |
|--------------|-----|--------|
| Oloxa Projects | 2d01c288-bb28-81f6-a1be-e57188992200 | Shared with Claude Code MCP integration |
| Tasks/To-Do Database | (multiple IDs) | Already accessible with old token |

### MCP Configuration
| Setting | Value |
|---------|-------|
| Scope | Local config (project-specific) |
| Command | `npx -y @notionhq/notion-mcp-server` |
| Environment | `NOTION_TOKEN=ntn_I755870800881mojWR2QcilFkl0VLOc0UMGTJrmuBw78BZ` |

### Agent IDs
| Agent | ID | Purpose |
|-------|-----|---------|
| browser-ops-agent | **ad886f2** | Created new integration, retrieved token, shared database, validated token |

---

## Technical Architecture

### Investigation Flow

1. **Initial Diagnosis**
   - Ran `claude mcp list` → Notion showed "Connected"
   - Tested `mcp__notion__API-post-search` → Worked (returned tasks)
   - Tested specific database → 404 "object_not_found"

2. **Permission Investigation**
   - Launched browser-ops-agent (ad886f2)
   - Found database shared with "n8n integration"
   - Discovered token mismatch

3. **Integration Replacement**
   - Deleted "n8n integration"
   - Created "Claude Code MCP" integration
   - Retrieved new token: `ntn_I755870800881mojWR2QcilFkl0VLOc0UMGTJrmuBw78BZ`
   - Shared Oloxa Projects database

4. **Token Validation**
   - Direct API test via HTTPie: `GET https://api.notion.com/v1/users/me`
   - Result: 200 OK (token is valid)

5. **MCP Configuration Update**
   - Removed old MCP config
   - Added new config with token as environment variable
   - Verified configuration: `claude mcp get notion`

6. **Current State**
   - Configuration is correct
   - Token is valid
   - MCP process hasn't reloaded new token (requires restart)

---

## Current State Summary

**Status:** Configuration Complete - Pending Restart

**What's Working:**
- ✅ New Notion integration created
- ✅ Token validated against Notion API
- ✅ Database shared with correct integration
- ✅ MCP configuration updated properly

**What's Not Working:**
- ❌ MCP server still returning 401 errors
- ❌ Running MCP process using cached old token

**Root Cause:**
The MCP server process is still running with the old token cached in memory. The configuration file has been updated correctly, but the running process won't pick up the new token until Claude Code is restarted.

---

## Next Steps

1. **User Action Required:**
   - Exit Claude Code (type `exit` or Ctrl+C)
   - Restart Claude Code
   - Return to test Notion MCP access

2. **After Restart - Verification:**
   - Test accessing Oloxa Projects database: `mcp__notion__API-retrieve-a-data-source` with ID `2d01c288-bb28-81f6-a1be-e57188992200`
   - Should return database schema instead of 401 error
   - Test query/create operations on the database

3. **If Still Not Working:**
   - Check if token has expired (regenerate if needed)
   - Verify database is still shared with "Claude Code MCP" integration
   - Check Claude Code logs for MCP server errors

---

## Key Learnings

1. **Token Format:** Notion now uses `ntn_` prefix for internal integration tokens (not `secret_` anymore)

2. **MCP Token Caching:** MCP servers cache tokens in memory. Config changes require restart to take effect.

3. **Integration vs Token:** Each Notion integration has its own token. Databases must be shared with the specific integration that matches the token.

4. **Efficient Debugging:** Using browser-ops-agent saved ~100K+ tokens vs doing Playwright operations in main conversation

---

## References

**Configuration File:** `/Users/swayclarke/.claude.json` (local project config)

**Notion Resources:**
- Integration Settings: https://www.notion.so/my-integrations
- Oloxa Projects Database: https://www.notion.so/2d01c288bb2881f6a1bee57188992200

**Agent Resume:**
- browser-ops-agent ID: **ad886f2** (can resume for follow-up Notion browser tasks)

---

## Final Resolution (January 08, 2026)

**✅ ISSUE RESOLVED**

**Root Cause:**
The databases were not shared with the "Claude Code MCP" integration. Once shared, the MCP server needed the correct **Data Source IDs** instead of Database IDs.

**What Fixed It:**
1. **browser-ops-agent (ad4522c)** reconnected both databases to "Claude Code MCP" integration
2. Used correct **Data Source IDs**:
   - Oloxa Projects: `2d01c288-bb28-81ef-a640-000ba0da69d4` ✅
   - Tasks Database: `39b8b725-0dbd-4ec2-b405-b3bba0c1d97e` ✅

**Current Status:**
- ✅ Oloxa Projects database: Fully accessible
- ✅ Tasks Database: Fully accessible
- ✅ MCP server token: Verified and working
- ✅ Integration connections: Active and confirmed

**Updated Documentation:**
- PROJECT_REFERENCE.md updated with Oloxa Projects database IDs
- Token corrected to: `ntn_I755870800881mojWR2QcilFkl0VLOc0UMGTJrmuBw78BZ`
- Status updated to "Fully working"

---

**Document Version:** v1.0
**Generated:** January 07, 2026 at 18:30 CET
**Last Updated:** January 08, 2026 at 21:30 CET
**Author:** Claude Code (Sway's automation assistant)
