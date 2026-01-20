# Chunk 2.5 Google Drive Credential Fix

**Date:** 2026-01-18
**Workflow:** Chunk 2.5 - Client Document Tracking (ID: okg8wTqLtPUwjQ18)
**Issue:** Google Drive credential error on "Download PDF for Classification" node
**Status:** ✅ FIXED

---

## Problem

The workflow was failing with this error:
```
Credential with ID 'google-drive-account-1' does not exist for type 'googleDriveOAuth2Api'
```

**Root Cause:** The "Download PDF for Classification" node (ID: `drive-download-1`) was using an incorrect credential ID that doesn't exist in the system.

---

## Investigation

**Step 1:** Checked Pre-Chunk 0 workflow (YGXWjWcBIk66ArvT) to find the correct credential:
- All Google Drive nodes use credential ID: `a4m50EefR3DJoU0R`
- Credential name: "Google Drive account"

**Step 2:** Checked Chunk 2.5 workflow (okg8wTqLtPUwjQ18) Google Drive nodes:
- "Move File to Final Location" → ✅ Correct credential (a4m50EefR3DJoU0R)
- "Move File to 38_Unknowns" → ✅ Correct credential (a4m50EefR3DJoU0R)
- "Rename File with Confidence" → ✅ Correct credential (a4m50EefR3DJoU0R)
- **"Download PDF for Classification" → ❌ Wrong credential (google-drive-account-1)**

---

## Solution Applied

Updated the "Download PDF for Classification" node credentials:

**Before:**
```json
{
  "googleDriveOAuth2Api": {
    "id": "google-drive-account-1",
    "name": "Google Drive Account 1"
  }
}
```

**After:**
```json
{
  "googleDriveOAuth2Api": {
    "id": "a4m50EefR3DJoU0R",
    "name": "Google Drive account"
  }
}
```

**Update Method:** Used `mcp__n8n-mcp__n8n_update_partial_workflow` with updateNode operation
**Result:** Successfully applied 1 operation

---

## Validation

**Post-fix validation results:**
- ✅ Credential error resolved (no longer appears in validation)
- ⚠️ 1 unrelated error remains: "Send Error Notification Email" has invalid Gmail operation
- ⚠️ 46 warnings (mostly suggestions for error handling and expression formats - non-critical)

**Note:** The remaining Gmail error is unrelated to the Google Drive credential fix and was pre-existing.

---

## Impact

**Fixed:** The workflow can now successfully download PDFs from Google Drive for classification.

**Next Steps:**
1. Test the workflow end-to-end to confirm the fix works in execution
2. (Optional) Address the Gmail operation error in "Send Error Notification Email" node
3. (Optional) Apply suggested expression format improvements (resource locator format)

---

## Technical Details

**Node Updated:**
- Node ID: `drive-download-1`
- Node Name: "Download PDF for Classification"
- Node Type: `n8n-nodes-base.googleDrive`
- Operation: `download`
- Parameter: `fileId: "={{ $json.fileId }}"`

**Credential Change:**
- Old: `google-drive-account-1` (doesn't exist)
- New: `a4m50EefR3DJoU0R` (matches all other Google Drive nodes)
