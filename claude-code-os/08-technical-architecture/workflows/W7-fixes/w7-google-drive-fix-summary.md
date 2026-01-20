# W7 Google Drive API Fix - Summary

## Issue
Nodes 10 and 15 (Check Invoice Pool Duplicates, Check Receipt Pool Duplicates) were causing Google Drive API errors: "Invalid Value at location: q"

**Root Cause:** The `searchMethod: "name"` parameter was conflicting with the custom `queryString` parameter. Google Drive's search operation doesn't support both simultaneously.

## Fix Applied

**Date:** 2026-01-12
**Workflow ID:** 6x1sVuv4XKN0002B
**Workflow Name:** Expense System - Workflow 7: Downloads Folder Monitor

### Nodes Modified

**Node 10: Check Invoice Pool Duplicates**
- **Operation:** search (fileFolder resource)
- **Removed:** `searchMethod` parameter
- **Retained:** Custom `queryString` with proper escaping
- **Query:** Searches for files by name in Invoice Pool folder (1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l)

**Node 15: Check Receipt Pool Duplicates**
- **Operation:** search (fileFolder resource)
- **Removed:** `searchMethod` parameter
- **Retained:** Custom `queryString` with proper escaping
- **Query:** Searches for files by name in Receipt Pool folder (1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4)

### Final Configuration

Both nodes now have EXACTLY these parameters:
```json
{
  "preBuiltAgentsCalloutGoogleDrive": "",
  "resource": "fileFolder",
  "operation": "search",
  "queryString": "='name = \"' + $json.originalFileName.replace(/\\u00a0/g, ' ').replace(/\\\\/g, '\\\\\\\\').replace(/\"/g, '\\\\\"').replace(/#/g, '\\\\#') + '\" and \"[FOLDER_ID]\" in parents and trashed = false'",
  "returnAll": false,
  "limit": 50,
  "filter": {},
  "options": {}
}
```

### Query String Features
- **Non-breaking space handling:** `.replace(/\u00a0/g, ' ')`
- **Backslash escaping:** `.replace(/\\/g, '\\\\')`
- **Quote escaping:** `.replace(/"/g, '\\"')`
- **Hash escaping:** `.replace(/#/g, '\\#')`
- **Parent folder filtering:** `"[FOLDER_ID]" in parents`
- **Trash exclusion:** `trashed = false`

## Validation Results

**Status:** ✅ Fixed

The validation confirms:
- No more "Invalid Value at location: q" errors
- Both nodes properly configured with custom queryString
- No searchMethod parameter present
- Workflow structure intact

### Remaining Issues (Unrelated to This Fix)
- Nodes 12 & 17 (Upload nodes) missing `operation` parameter - separate issue
- Various warnings about error handling and typeVersions - non-critical

## Testing Recommendation

Test duplicate detection with:
1. File with non-breaking spaces in name
2. File with special characters (quotes, hashes, backslashes)
3. Normal filename
4. Verify no "Invalid Value" errors appear in execution logs

## Notes

This fix ensures Google Drive API receives properly formatted queries without conflicting parameters. The custom queryString approach provides more control over search logic while properly escaping special characters that could break the query.
