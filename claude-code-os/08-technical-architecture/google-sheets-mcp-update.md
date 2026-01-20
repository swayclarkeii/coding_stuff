# Google Sheets MCP - Service Account Migration COMPLETE ✅

**Date**: December 31, 2025
**Status**: ✅ CODE MODIFIED - Ready for config update and testing

---

## What Was Done

### 1. Service Account Verified ✅

**Existing Service Account Found:**
- Location: `/Users/swayclarke/coding_stuff/claude-code-os/.credentials/claude-automation-service-account.json`
- Email: `claude-automation@n8n-integrations-482020.iam.gserviceaccount.com`
- Project: `n8n-integrations-482020`
- Status: **Working** - tested successfully with googleapis library

### 2. Code Modified ✅

**File**: `/Users/swayclarke/coding_stuff/mcp-servers/google-sheets-mcp/dist/index.js`

**Backup Created**: `dist/index.js.oauth-backup`

**Changes Made:**
- Removed `@google-cloud/local-auth` OAuth dependency
- Replaced `authenticateAndSaveCredentials()` with `authenticateWithServiceAccount()`
- Updated authentication to use `google.auth.GoogleAuth` with service account
- Added support for `GOOGLE_SERVICE_ACCOUNT_PATH` environment variable

**Server Tested:** ✅ Starts successfully with service account authentication

---

## Next Step: Update Claude Code MCP Configuration

**You need to update the environment variable for google-sheets-mcp in Claude Code.**

### Option 1: Via Command Line (Recommended)

```bash
# Re-configure the google-sheets MCP server with new environment variable
claude mcp add google-sheets
```

When prompted for environment variables, set:
```
GOOGLE_SERVICE_ACCOUNT_PATH=/Users/swayclarke/coding_stuff/claude-code-os/.credentials/claude-automation-service-account.json
```

### Option 2: Manual Config Edit

If Claude Code stores MCP config in a JSON file you can edit:

**Find config location:**
```bash
claude mcp list --verbose  # Should show config file path
```

**Update google-sheets entry:**
```json
{
  "google-sheets": {
    "command": "node",
    "args": ["/Users/swayclarke/coding_stuff/mcp-servers/google-sheets-mcp/dist/index.js"],
    "env": {
      "GOOGLE_SERVICE_ACCOUNT_PATH": "/Users/swayclarke/coding_stuff/claude-code-os/.credentials/claude-automation-service-account.json"
    }
  }
}
```

**Remove old OAuth environment variables:**
- Delete: `GOOGLE_OAUTH_CREDENTIALS`
- Delete: `GSHEETS_OAUTH_PATH`
- Delete: `GSHEETS_CREDENTIALS_PATH`

---

## Testing the Migration

After updating the config:

1. **Restart VS Code** (to reload Claude Code extension and MCP servers)

2. **Test google-sheets-mcp:**
   ```
   Try using any Google Sheets operation, like:
   - mcp__google-sheets__list_sheets
   - mcp__google-sheets__read_all_from_sheet
   ```

3. **Expected Result:**
   - ✅ No "invalid_request" errors
   - ✅ No OAuth prompts
   - ✅ Operations work immediately without authentication

4. **Monitor for 24 hours:**
   - Service account should NEVER expire
   - No reauthorization required
   - Stable authentication permanently

---

## If Testing Succeeds

Apply same changes to remaining 4 Google MCP servers:

1. **google-drive-mcp**
   - Location: `/Users/swayclarke/coding_stuff/mcp-google-drive/dist/index.js`
   - Same modifications as google-sheets-mcp

2. **google-docs-mcp**
   - Location: `/Users/swayclarke/coding_stuff/mcp-google-docs/dist/server.js`
   - Same modifications as google-sheets-mcp

3. **google-calendar-mcp**
   - Location: `/Users/swayclarke/coding_stuff/mcp-servers/google-calendar-mcp/build/index.js`
   - Same modifications as google-sheets-mcp

4. **google-slides-mcp**
   - Location: `/Users/swayclarke/coding_stuff/mcp-servers/google-slides-mcp/build/index.js`
   - Same modifications as google-sheets-mcp

**All servers can use the SAME service account file** - just set `GOOGLE_SERVICE_ACCOUNT_PATH` environment variable for each.

---

## Rollback If Needed

If service account migration fails:

1. **Restore original OAuth code:**
   ```bash
   cp /Users/swayclarke/coding_stuff/mcp-servers/google-sheets-mcp/dist/index.js.oauth-backup \
      /Users/swayclarke/coding_stuff/mcp-servers/google-sheets-mcp/dist/index.js
   ```

2. **Revert Claude Code MCP config** to use OAuth environment variables

3. **Restart VS Code**

4. **Re-authorize OAuth** if needed

---

## Summary of Benefits

**Before (OAuth):**
- ❌ Tokens expire every ~7 days
- ❌ Requires manual browser reauthorization
- ❌ Frequent "invalid_request" errors
- ❌ Constant interruptions

**After (Service Account):**
- ✅ Never expires
- ✅ No browser popups
- ✅ No reauthorization needed
- ✅ Permanent fix

---

## Files Modified

| File | Status | Backup Location |
|------|--------|-----------------|
| google-sheets-mcp/dist/index.js | ✅ Modified | index.js.oauth-backup |

---

## Next Actions (Sway)

- [ ] Update Claude Code MCP config with new environment variable
- [ ] Restart VS Code
- [ ] Test google-sheets-mcp operations
- [ ] Verify no authentication errors for 24 hours
- [ ] If successful, notify Claude to update remaining 4 servers

---

**Last Updated**: December 31, 2025 at 15:50 CET
