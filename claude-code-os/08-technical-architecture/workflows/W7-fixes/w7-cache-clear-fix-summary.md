# W7 Cache Clear Fix - Complete Node Rebuild

## Date
2026-01-12

## Problem
The `searchMethod` parameter was persisting in nodes 10 and 15 despite previous updates, causing Google Drive API errors: "Invalid Value at location: q"

**Root Cause:** n8n caching issue - parameter updates weren't clearing cached values.

## Solution
**Complete node deletion and recreation** to force n8n to clear its cache.

## Changes Applied

### Operations Performed
1. **Deleted nodes 10 and 15 entirely**
2. **Recreated both nodes from scratch** with clean parameters
3. **Reconnected all node relationships**

### Node 10: Check Invoice Pool Duplicates
- **Type:** n8n-nodes-base.googleDrive (typeVersion 3)
- **Position:** [2224, 112]
- **Parameters:**
  - `resource: "fileFolder"`
  - `operation: "search"`
  - `queryString: "='name = \"' + $json.originalFileName.replace(/\u00a0/g, ' ').replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/#/g, '\\#') + '\" and \"1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l\" in parents and trashed = false'"`
  - `returnAll: false`
  - `limit: 50`
  - `filter: {}`
  - `options: {}`
  - ❌ **NO searchMethod parameter**
- **Credentials:** googleDriveOAuth2Api (id: a4m50EefR3DJoU0R)
- **Connections:**
  - Input: Route by Category (output 0)
  - Output: Skip if Exists (input 0)

### Node 15: Check Receipt Pool Duplicates
- **Type:** n8n-nodes-base.googleDrive (typeVersion 3)
- **Position:** [2224, 304]
- **Parameters:**
  - `resource: "fileFolder"`
  - `operation: "search"`
  - `queryString: "='name = \"' + $json.originalFileName.replace(/\u00a0/g, ' ').replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/#/g, '\\#') + '\" and \"1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4\" in parents and trashed = false'"`
  - `returnAll: false`
  - `limit: 50`
  - `filter: {}`
  - `options: {}`
  - ❌ **NO searchMethod parameter**
- **Credentials:** googleDriveOAuth2Api (id: a4m50EefR3DJoU0R)
- **Connections:**
  - Input: Route by Category (output 1)
  - Output: Skip if Exists Receipt (input 0)

## Verification

### Validation Results
✅ **6 operations applied successfully:**
- 2 node deletions
- 2 node creations
- 4 connection recreations

✅ **Workflow structure intact:**
- 24 total nodes
- 17 connections
- All connections properly restored

✅ **Parameter confirmation:**
- Both nodes use custom `queryString` with special character escaping
- No `searchMethod` parameter exists in either node
- Folder IDs correctly set (Invoice Pool: 1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l, Receipt Pool: 1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4)

## Testing Instructions

Test with files containing special characters:

1. **Non-breaking space test:**
   - File: "Invoice 540.pdf" (with \u00a0 character)
   - Expected: Query properly escapes non-breaking space to regular space

2. **Special character test:**
   - File: 'SC - SUPREME MUSIC GmbH - 122025 #540.pdf'
   - Expected: Query properly escapes quotes, hashes, backslashes

3. **Normal filename test:**
   - File: "receipt.pdf"
   - Expected: Standard query execution

4. **Execution log verification:**
   - Check node 10 execution log - should show NO "searchMethod" in parameters
   - Check node 15 execution log - should show NO "searchMethod" in parameters
   - Verify NO "Invalid Value at location: q" errors

## Status
✅ **Fix complete - nodes rebuilt from scratch**
🔄 **Ready for execution testing**

## Next Steps
1. Run workflow with test files
2. Verify execution logs show clean Google Drive API queries
3. Confirm duplicate detection works correctly
4. Monitor for any API errors

## Notes
- This fix demonstrates that sometimes parameter updates aren't sufficient
- Complete node recreation is the most reliable way to clear n8n cache
- All connections were preserved and restored correctly
