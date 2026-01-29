# W4 and W2 Test Report - 2026-01-29

## Summary
- Total workflows tested: 2
- Failed: 2
- Passed: 0
- Test date: 2026-01-29 19:20 UTC

---

## W4 Filing (nASL6hxNQGrNBTV4)

### Test 1: Default Webhook Test
- **Status**: FAIL
- **Execution ID**: 6924
- **Execution status**: error
- **Duration**: 39ms
- **Started**: 2026-01-29T19:16:20.037Z
- **Stopped**: 2026-01-29T19:16:20.076Z

### Error Details
- **Failed node**: Check if VAT Folder Exists
- **Node type**: n8n-nodes-base.googleDrive (v2)
- **Error type**: TypeError
- **Error message**: Cannot read properties of undefined (reading 'execute')

### Execution Path
1. Webhook Trigger (Manual) - SUCCESS (1 item, 1ms)
2. Parse Month/Year Input - SUCCESS (1 item, 28ms)
3. Check if VAT Folder Exists - ERROR (0 items, 3ms)

### Upstream Context
Previous node "Parse Month/Year Input" successfully output:
```json
{
  "month": "December",
  "year": "2025",
  "folder_name": "VAT December 2025",
  "base_folder_id": "1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15"
}
```

### Root Cause Analysis
**STRUCTURAL ERROR - Configuration Issue**

The error `Cannot read properties of undefined (reading 'execute')` at `router.ts:29:60` indicates that the Google Drive node is missing a required configuration parameter. This is an internal n8n router error, meaning the node cannot determine which operation to execute.

**Likely cause**: The recent fix added `resource` parameter to Google Drive nodes, but the value may be incorrect or the `operation` parameter is missing/incompatible with the `resource` value.

**Error stack trace shows**:
```
at ExecuteContext.router (/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-nodes-base@file+packages+nodes-base_@aws-sdk+credential-providers@3.808.0_asn1.js@5_8da18263ca0574b0db58d4fefd8173ce/node_modules/n8n-nodes-base/nodes/Google/Drive/v2/actions/router.ts:29:60)
```

This is the n8n internal router trying to dispatch to the correct operation handler and failing because the configuration is invalid.

**Required fix**: Review the "Check if VAT Folder Exists" node configuration:
1. Verify `resource` parameter is set correctly (likely should be "folder" or "file")
2. Verify `operation` parameter matches the resource type
3. Check Google Drive v2 node documentation for valid resource/operation combinations

---

## W2 Gmail Monitor (dHbwemg7hEB4vDmC)

### Test 1: Default Webhook Test
- **Status**: FAIL (but workflow mostly worked)
- **Execution ID**: 6933
- **Execution status**: error
- **Duration**: 16,652ms (16.6 seconds)
- **Started**: 2026-01-29T19:20:30.812Z
- **Stopped**: 2026-01-29T19:20:47.464Z

### Error Details
- **Failed node**: Trigger W6 Workflow
- **Node type**: n8n-nodes-base.httpRequest
- **Error type**: NodeApiError
- **Error message**: The resource you are requesting could not be found
- **HTTP code**: 404

### Execution Path (10 nodes executed successfully before error)
1. Daily Receipt Check - SKIPPED
2. Load Vendor Patterns - SUCCESS (13 items, 20ms)
3. Search Gmail for Receipts - SUCCESS (12 items, 8,330ms)
4. Get Email Details - SUCCESS (12 items, 4,999ms)
5. Combine Both Gmail Accounts - SUCCESS (12 items, 85ms)
6. Hybrid Pre-Filter - SUCCESS (12 items, 65ms)
7. Detect Expensify Email - SUCCESS (3 items, 7ms)
8. Detect Invoice or Receipt - SKIPPED
9. Extract Expensify PDF - SUCCESS (1 item, 27ms)
10. Upload to Expensify Reports Folder - SUCCESS (1 item, 3,045ms)
11. Trigger W6 Workflow - ERROR (0 items, 62ms)

### Upstream Context
Previous node "Upload to Expensify Reports Folder" successfully uploaded file:
```json
{
  "id": "1rA7YIsmnP7KVQIAh3XRJBId7LhOcRyKk",
  "name": "SwayClarkeNOV2025ExpenseReport.pdf",
  "mimeType": "application/pdf",
  "parents": ["1X_1fczizk4_Tl_T6U1x3J7iwVyaRHoBW"],
  "webViewLink": "https://drive.google.com/file/d/1rA7YIsmnP7KVQIAh3XRJBId7LhOcRyKk/view?usp=drivesdk"
}
```

### Root Cause Analysis
**ENVIRONMENTAL ERROR - External Dependency**

The workflow successfully:
- Loaded vendor patterns from Google Sheets
- Searched Gmail for receipts (12 emails found)
- Downloaded email details
- Filtered for Expensify emails (3 found)
- Extracted PDF attachment (1 PDF)
- Uploaded PDF to Google Drive (SUCCESS)

The error occurred when trying to trigger W6 workflow via webhook:
- Target webhook: `https://n8n.oloxa.ai/webhook/90e50d17-7e01-43a7-8876-e11fb7e7ab4e`
- HTTP response: 404 - "The requested webhook 'POST 90e50d17-7e01-43a7-8876-e11fb7e7ab4e' is not registered"
- Hint from n8n: "The workflow must be active for a production URL to run successfully"

**This is NOT a W2 error.** W2 worked perfectly. The W6 workflow (Expensify Report Processor) either:
1. Is not active/enabled in n8n
2. Does not exist
3. Has a different webhook ID
4. Does not have a webhook trigger configured

**Impact on W2**: This error is at the END of the workflow, after all critical work is done. The file was successfully uploaded to Google Drive. The only failure is the optional downstream trigger.

**Required fix**: Check W6 workflow (ID unknown) to ensure:
1. It exists and is active
2. It has a webhook trigger with path `90e50d17-7e01-43a7-8876-e11fb7e7ab4e`
3. If W6 doesn't exist yet, this trigger should be removed or made conditional

---

## Overall Assessment

### W4 Filing
- **Status**: BROKEN
- **Severity**: HIGH - workflow cannot execute past node 2
- **Type**: STRUCTURAL (configuration error)
- **Next steps**: Fix Google Drive node resource/operation parameters

### W2 Gmail Monitor
- **Status**: MOSTLY WORKING
- **Severity**: LOW - only optional downstream trigger fails
- **Type**: ENVIRONMENTAL (external workflow dependency)
- **Core functionality**: OPERATIONAL (file extraction and upload works)
- **Next steps**: Verify W6 workflow exists and is active, or remove trigger

### Credentials Status
- Google Sheets: WORKING (W2 loaded vendor patterns successfully)
- Gmail: WORKING (W2 searched and downloaded emails successfully)
- Google Drive: WORKING (W2 uploaded file successfully)
- Google Drive (W4): MISCONFIGURED (node configuration error, not credential error)

---

## Recommendations

### Immediate Actions
1. **W4**: Review "Check if VAT Folder Exists" node configuration in workflow editor
   - Check resource parameter value
   - Check operation parameter value
   - Verify against Google Drive v2 node documentation

2. **W2**: Check if W6 workflow exists and is active
   - If W6 doesn't exist yet, remove the "Trigger W6 Workflow" node temporarily
   - If W6 exists but inactive, activate it
   - If W6 has different webhook ID, update the HTTP Request URL

### Testing Priority
1. Fix W4 first (complete failure)
2. Verify W2 can run end-to-end after W6 is resolved (already 91% functional)
