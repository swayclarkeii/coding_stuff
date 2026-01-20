# Google MCP Servers - OAuth to Service Account Migration

**Date**: December 31, 2025
**Status**: 🔴 CRITICAL - Migration Required
**Priority**: P0 - Constant reauthorization blocking productivity

---

## Executive Summary

**Problem**: All 5 Google MCP servers use OAuth authentication requiring periodic token refresh, causing constant "invalid_request" errors and manual reauthorization every few days.

**Root Cause**: MCP servers built using `@google-cloud/local-auth` which implements OAuth 2.0 flow with expiring tokens.

**Solution**: Migrate to Google Cloud service account authentication using `GoogleAuth` class from `googleapis` library (already installed).

**Impact**: Permanent fix - service accounts don't expire, eliminating all reauthorization issues.

---

## Current State Analysis

### Affected MCP Servers (5 Total)

| Server | Location | Auth Method | Status |
|--------|----------|-------------|--------|
| google-sheets-mcp | /Users/swayclarke/coding_stuff/mcp-servers/google-sheets-mcp | OAuth | 🔴 Fails frequently |
| google-drive-mcp | /Users/swayclarke/coding_stuff/mcp-google-drive | OAuth | 🔴 Fails frequently |
| google-docs-mcp | /Users/swayclarke/coding_stuff/mcp-google-docs | OAuth | 🔴 Fails frequently |
| google-calendar-mcp | /Users/swayclarke/coding_stuff/mcp-servers/google-calendar-mcp | OAuth | 🔴 Fails frequently |
| google-slides-mcp | /Users/swayclarke/coding_stuff/mcp-servers/google-slides-mcp | OAuth | 🔴 Fails frequently |

### Current OAuth Credentials

Each server has OAuth credential files:
- `mcp-servers/google-sheets-mcp/dist/gcp-oauth.keys.json`
- `mcp-servers/google-calendar-mcp/gcp-oauth.keys.json`
- `mcp-google-drive/gcp-oauth.keys.json`

**OAuth Token Lifecycle:**
1. User authenticates via browser popup
2. Token saved to `.gsheets-server-credentials.json` (or equivalent)
3. Token expires after ~7 days
4. MCP returns "invalid_request" error
5. Manual reauthorization required

---

## Technical Analysis

### Authentication Code Pattern (Current)

**google-sheets-mcp/dist/index.js** (lines 864-881):

```javascript
async function authenticateAndSaveCredentials() {
    const gcpKeysPath = path.join(path.dirname(fileURLToPath(import.meta.url)), "gcp-oauth.keys.json");

    console.log("Launching auth flow...");
    const auth = await authenticate({
        keyfilePath: process.env.GSHEETS_OAUTH_PATH || gcpKeysPath,
        scopes: [
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    });

    fs.writeFileSync(credentialsPath, JSON.stringify(auth.credentials));
    return auth;
}
```

**Problem**: Uses `@google-cloud/local-auth` which implements OAuth requiring:
- Browser-based user consent
- Refresh token management
- Token expiration handling

### Proposed Service Account Code

```javascript
async function authenticateWithServiceAccount() {
    const serviceAccountPath = process.env.GOOGLE_SERVICE_ACCOUNT_PATH ||
        path.join(path.dirname(fileURLToPath(import.meta.url)), "service-account.json");

    if (!fs.existsSync(serviceAccountPath)) {
        console.error("Service account key not found:", serviceAccountPath);
        process.exit(1);
    }

    const auth = new google.auth.GoogleAuth({
        keyFile: serviceAccountPath,
        scopes: [
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    });

    return auth;
}
```

**Benefits**:
- No browser popups
- No token expiration
- No refresh logic needed
- Persistent authentication

---

## Migration Plan

### Phase 1: Service Account Setup

1. **Create Service Account in Google Cloud Console**
   - Navigate to: https://console.cloud.google.com/iam-admin/serviceaccounts
   - Project: Select appropriate GCP project
   - Create service account: `claude-mcp-integration`
   - Description: "Service account for Claude MCP servers"

2. **Grant Required Scopes**
   - Google Sheets API: `https://www.googleapis.com/auth/spreadsheets`
   - Google Drive API: `https://www.googleapis.com/auth/drive`
   - Google Docs API: `https://www.googleapis.com/auth/documents`
   - Google Calendar API: `https://www.googleapis.com/auth/calendar`
   - Google Slides API: `https://www.googleapis.com/auth/presentations`

3. **Download Service Account Key**
   - Format: JSON
   - Save to: `/Users/swayclarke/coding_stuff/.credentials/google/service-account.json`
   - Permissions: `chmod 600 service-account.json`

4. **Enable Domain-Wide Delegation** (if needed for Calendar/Drive access)
   - Required for accessing user-specific resources
   - OAuth scopes must match service account scopes

### Phase 2: Code Modifications

**Modify each server's authentication function:**

#### 1. google-sheets-mcp

File: `/Users/swayclarke/coding_stuff/mcp-servers/google-sheets-mcp/dist/index.js`

**Changes:**
- Lines 2: Remove `import { authenticate } from "@google-cloud/local-auth";`
- Lines 862-881: Replace `authenticateAndSaveCredentials()` with service account version
- Lines 882-903: Replace `loadCredentialsAndRunServer()` to use `GoogleAuth`

#### 2. google-drive-mcp

File: `/Users/swayclarke/coding_stuff/mcp-google-drive/dist/index.js`

**Changes:** (Similar pattern to google-sheets-mcp)

#### 3. google-docs-mcp

File: `/Users/swayclarke/coding_stuff/mcp-google-docs/dist/server.js`

**Changes:** (Similar pattern to google-sheets-mcp)

#### 4. google-calendar-mcp

File: `/Users/swayclarke/coding_stuff/mcp-servers/google-calendar-mcp/build/index.js`

**Changes:** (Similar pattern to google-sheets-mcp)

#### 5. google-slides-mcp

File: `/Users/swayclarke/coding_stuff/mcp-servers/google-slides-mcp/build/index.js`

**Changes:** (Similar pattern to google-sheets-mcp)

### Phase 3: Configuration Updates

**Update Claude Desktop Config** (`~/.config/claude/mcp.json` or equivalent):

**Before (OAuth):**
```json
{
  "google-sheets": {
    "command": "node",
    "args": ["/Users/swayclarke/coding_stuff/mcp-servers/google-sheets-mcp/dist/index.js"],
    "env": {
      "GOOGLE_OAUTH_CREDENTIALS": "/Users/swayclarke/coding_stuff/mcp-servers/google-sheets-mcp/dist/gcp-oauth.keys.json"
    }
  }
}
```

**After (Service Account):**
```json
{
  "google-sheets": {
    "command": "node",
    "args": ["/Users/swayclarke/coding_stuff/mcp-servers/google-sheets-mcp/dist/index.js"],
    "env": {
      "GOOGLE_SERVICE_ACCOUNT_PATH": "/Users/swayclarke/coding_stuff/.credentials/google/service-account.json"
    }
  }
}
```

### Phase 4: Testing

**Test each server individually:**

1. **Restart Claude Desktop** after config changes
2. **Test google-sheets-mcp**: Try `mcp__google-sheets__list_sheets`
3. **Test google-drive-mcp**: Try `mcp__google-drive__listFolder`
4. **Test google-docs-mcp**: Try `mcp__google-docs__listGoogleDocs`
5. **Test google-calendar-mcp**: Try `mcp__google-calendar__list-calendars`
6. **Test google-slides-mcp**: Try `mcp__google-slides__get_presentation`

**Verify no errors** for 24 hours minimum before marking as stable.

---

## Rollback Procedures

### If Service Account Migration Fails

1. **Restore OAuth config** in Claude Desktop
2. **Revert code changes** using git:
   ```bash
   git checkout HEAD -- mcp-servers/google-sheets-mcp/dist/index.js
   git checkout HEAD -- mcp-google-drive/dist/index.js
   git checkout HEAD -- mcp-google-docs/dist/server.js
   ```
3. **Restart Claude Desktop**
4. **Manually reauthorize** OAuth for each server

### Backup OAuth Credentials

Before migration, backup all OAuth files:
```bash
mkdir -p /Users/swayclarke/coding_stuff/.credentials/oauth-backup-20251231/
cp mcp-servers/google-sheets-mcp/dist/gcp-oauth.keys.json .credentials/oauth-backup-20251231/
cp mcp-servers/google-sheets-mcp/dist/.gsheets-server-credentials.json .credentials/oauth-backup-20251231/
# Repeat for other servers...
```

---

## Potential Issues & Solutions

### Issue 1: Service Account Can't Access User Data

**Problem**: Service accounts can't access user-specific resources (Drive files, Calendar events) without domain-wide delegation.

**Solution**:
- Enable **Domain-Wide Delegation** in Google Workspace Admin Console
- Authorize service account with specific scopes
- Required for: google-drive-mcp, google-calendar-mcp

**Steps**:
1. Go to: https://admin.google.com/ac/owl/domainwidedelegation
2. Add new API client
3. Client ID: (from service account JSON)
4. Scopes: Comma-separated list of all required scopes

### Issue 2: Code Changes Break After npm Install

**Problem**: Modified dist/index.js gets overwritten when running `npm install` or `npm run build`.

**Solution**:
- Modify **source TypeScript files** instead of dist/ files
- File: `src/index.ts` (not `dist/index.js`)
- Rebuild: `npm run build`
- OR: Create patch files to auto-apply changes

### Issue 3: Multiple Servers Need Same Service Account

**Question**: Can all 5 servers share ONE service account JSON file?

**Answer**: YES
- Single service account can have multiple scopes
- All servers can reference same `/Users/swayclarke/coding_stuff/.credentials/google/service-account.json`
- Simplifies management and key rotation

### Issue 4: TypeScript Compilation Errors

**Problem**: Changing from `@google-cloud/local-auth` to `GoogleAuth` may cause TypeScript errors.

**Solution**:
- Update type imports: `import { GoogleAuth } from 'google-auth-library';`
- Install types if needed: `npm install -D @types/google-auth-library`
- Or modify JavaScript files directly (skip TypeScript rebuild)

---

## Security Considerations

### Service Account Key Storage

**Location**: `/Users/swayclarke/coding_stuff/.credentials/google/`

**Permissions**:
```bash
chmod 700 /Users/swayclarke/coding_stuff/.credentials
chmod 700 /Users/swayclarke/coding_stuff/.credentials/google
chmod 600 /Users/swayclarke/coding_stuff/.credentials/google/service-account.json
```

**Git Ignore**:
Add to `.gitignore`:
```
.credentials/
*.json
!package.json
!tsconfig.json
```

**Backup**:
- Store encrypted backup in 1Password or similar
- Never commit to git
- Rotate keys every 90 days

### Scope Principle of Least Privilege

Only grant required scopes:
- ✅ Sheets: `spreadsheets` (read/write)
- ✅ Drive: `drive.file` (files created by app only)
- ❌ Drive: `drive` (full access - avoid if possible)

---

## Success Criteria

- [ ] Service account created and key downloaded
- [ ] All 5 MCP servers modified for service account auth
- [ ] Claude Desktop config updated
- [ ] All servers tested and working
- [ ] No "invalid_request" errors for 48 hours
- [ ] Rollback procedure documented and tested
- [ ] OAuth credentials backed up
- [ ] Service account key secured (chmod 600)

---

## Implementation Checklist

### Pre-Migration
- [ ] Create Google Cloud service account
- [ ] Download service account JSON key
- [ ] Secure key file permissions (chmod 600)
- [ ] Backup all OAuth credentials
- [ ] Document current working state

### Migration
- [ ] Modify google-sheets-mcp source code
- [ ] Modify google-drive-mcp source code
- [ ] Modify google-docs-mcp source code
- [ ] Modify google-calendar-mcp source code
- [ ] Modify google-slides-mcp source code
- [ ] Rebuild TypeScript (if applicable)
- [ ] Update Claude Desktop config
- [ ] Restart Claude Desktop

### Testing
- [ ] Test google-sheets-mcp operations
- [ ] Test google-drive-mcp operations
- [ ] Test google-docs-mcp operations
- [ ] Test google-calendar-mcp operations
- [ ] Test google-slides-mcp operations
- [ ] Monitor for 48 hours - no auth errors
- [ ] Verify n8n workflows still work
- [ ] Verify Notion integrations still work

### Documentation
- [ ] Update CLAUDE.md with service account instructions
- [ ] Document service account key rotation process
- [ ] Update OAUTH_REFRESH_PROTOCOL.md (mark as obsolete)
- [ ] Create service account troubleshooting guide

---

## Next Steps

1. **Get approval** from Sway to proceed with migration
2. **Create service account** in Google Cloud Console
3. **Start with google-sheets-mcp** as pilot migration
4. **Test thoroughly** before migrating other servers
5. **Roll out** to remaining 4 servers if successful
6. **Monitor** for 48 hours minimum
7. **Document learnings** and update this guide

---

## Alternative Approaches Considered

### Alternative 1: Find Different MCP Servers

**Evaluation**: Searched npm for MCP servers with service account support
**Result**: No alternatives found - would need to build from scratch

### Alternative 2: Wrapper/Proxy Authentication

**Evaluation**: Create auth proxy that handles OAuth refresh automatically
**Result**: Adds complexity, doesn't solve root issue

### Alternative 3: Stay with OAuth + Auto-Refresh

**Evaluation**: Build Playwright automation to refresh OAuth tokens on schedule
**Result**: Band-aid solution, doesn't address expiration problem

**Recommendation**: Option 1 (modify existing servers) is the best long-term solution.

---

**Last Updated**: December 31, 2025 at 15:35 CET
**Next Review**: After first successful server migration
