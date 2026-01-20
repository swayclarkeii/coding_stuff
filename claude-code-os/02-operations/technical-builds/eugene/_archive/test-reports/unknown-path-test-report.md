# n8n Test Report – V4 Pre-Chunk 0: Intake & Client Identification

## Summary
- **Workflow ID:** `70n97A6OmYCsHMmV`
- **Test Execution ID:** `369`
- **Execution Status:** ❌ **FAILED** (ended with error)
- **Test Result:** ❌ **FAIL**
- **Path Taken:** NEW client path (incorrect - should have been UNKNOWN)

---

## Test Details

### Execution Information
- **Execution ID:** 369
- **Started:** 2026-01-05 10:38:01 UTC
- **Stopped:** 2026-01-05 10:38:59 UTC
- **Duration:** 58.6 seconds
- **Final Status:** error
- **Failed Node:** Execute Chunk 1

### Input Data (from email trigger)
- **Email ID:** `19b8dbbdb7993823`
- **Attachment:** `sop-template.pdf`
- **File ID:** `1eQWFYfYZFlBLP-HQ9-Soy9zd7mjDNmeV`

---

## Root Cause Analysis

### Problem 1: Wrong Path Selection

**AI Extraction Result:**
```
"Unable to extract client company name from the provided text."
```

**Normalized Client Name:**
```
"unable_to_extract_client_company_name_from_the_provided_text"
```

**Expected Behavior:**
- "Check Client Exists" node should detect this as UNKNOWN
- Set `client_status = "UNKNOWN"`
- Decision Gate routes to Output 0 (UNKNOWN path)

**Actual Behavior:**
- "Check Client Exists" node set `client_status = "NEW"`
- Decision Gate routed to Output 1 (NEW client path)
- Workflow attempted to create staging folder for a non-existent client
- Failed at "Execute Chunk 1" with error

### Problem 2: "Check Client Exists" Node Logic Bug

The "Check Client Exists" node is **not detecting extraction failures**. It needs to check if the normalized client name matches the pattern:
- `"unable_to_extract_*"`
- `"error_extracting_*"`
- Or any other AI extraction failure pattern

**Current logic appears to be:**
```javascript
// Pseudocode of current logic
if (registry_has_client) {
  client_status = "EXISTING"
} else {
  client_status = "NEW"  // ❌ BUG: Should check for extraction failures first
}
```

**Correct logic should be:**
```javascript
// Correct logic
if (client_name matches "unable_to_extract_*" or "error_extracting_*") {
  client_status = "UNKNOWN"  // ✅ Route to UNKNOWN path
} else if (registry_has_client) {
  client_status = "EXISTING"
} else {
  client_status = "NEW"
}
```

---

## Execution Path Analysis

### Nodes Executed (11 nodes before failure):

1. ✅ **Extract Text from PDF** - Success (77ms)
2. ✅ **Evaluate Extraction Quality** - Success (16ms)
3. ✅ **AI Extract Client Name** - Success (935ms)
   - Output: "Unable to extract client company name from the provided text."
4. ✅ **Normalize Client Name** - Success (19ms)
   - Output: `"unable_to_extract_client_company_name_from_the_provided_text"`
5. ✅ **Lookup Client Registry** - Success (785ms)
6. ✅ **Check Client Exists** - Success (16ms)
   - ❌ **BUG:** Set `client_status = "NEW"` (should be "UNKNOWN")
7. ✅ **Decision Gate** - Success (11ms)
   - ❌ **Wrong path:** Routed to Output 1 (NEW) instead of Output 0 (UNKNOWN)
8. ✅ **Lookup Staging Folder** - Success (407ms)
9. ✅ **Filter Staging Folder ID** - Success (16ms)
10. ❌ **Execute Chunk 1** - **FAILED** (1833ms)
    - Error: "Unknown error"

### UNKNOWN Path Nodes (not executed):
- ❌ Prepare UNKNOWN Client Data
- ❌ Execute Chunk 0 - Create Folders (UNKNOWN variant)
- ❌ Check If UNKNOWN Path
- ❌ Extract 38_Unknowns Folder ID
- ❌ Validate Folder IDs
- ❌ Move PDF to 38_Unknowns
- ❌ Prepare Email Notification Data
- ❌ Build Email HTML Body
- ❌ Send Email Notification

**None of the 8 new UNKNOWN nodes executed because the Decision Gate routed to the wrong path.**

---

## Test Verdict

### ❌ **FAIL**

**Reason:** The UNKNOWN client handling flow was not triggered. The workflow incorrectly routed extraction failures to the NEW client path, causing a downstream error.

---

## Recommendations

### Fix Required: Update "Check Client Exists" Node

**Location:** Node `check-exists-001` (Check Client Exists)

**Required Change:** Add UNKNOWN detection logic before checking registry:

```javascript
// Add at the start of the node code:
const clientNormalized = $input.item.json.client_normalized;

// Check for extraction failure patterns
if (
  clientNormalized.startsWith('unable_to_extract_') ||
  clientNormalized.startsWith('error_extracting_') ||
  clientNormalized.includes('unable to extract') ||
  clientNormalized === 'unknown_client'
) {
  return {
    ...existingData,
    client_status: 'UNKNOWN',
    root_folder_id: null,
    staging_folder_id: null
  };
}

// Then continue with existing NEW/EXISTING logic
```

### Testing After Fix

After updating the "Check Client Exists" node:

1. **Re-trigger workflow** with the same test email (or similar image-only email)
2. **Verify Decision Gate** routes to Output 0 (UNKNOWN)
3. **Verify all 8 UNKNOWN nodes execute:**
   - Prepare UNKNOWN Client Data
   - Execute Chunk 0 - Create Folders
   - Check If UNKNOWN Path (TRUE branch)
   - Extract 38_Unknowns Folder ID
   - Validate Folder IDs
   - Move PDF to 38_Unknowns
   - Prepare Email Notification Data
   - Build Email HTML Body
   - Send Email Notification
4. **Verify email sent** to swayclarkeii@gmail.com
5. **Verify Google Drive:**
   - Timestamp folder created (e.g., `unknown_2026-01-05_1141_Documents`)
   - 37-folder structure + 38_Unknowns created
   - PDF moved to 38_Unknowns folder

---

## Additional Notes

**Execution #356 (earlier error):**
- Status: error
- Time: 2026-01-05 10:05:33 UTC
- This may have been another test attempt that also failed

**Recommendation:** After fixing "Check Client Exists", Sway should send another test email (image-only, no client name) to fully validate the UNKNOWN path end-to-end.

---

**Generated:** 2026-01-05
**Agent:** test-runner-agent
