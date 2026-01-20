# n8n Test Report – Pre-Chunk 0 → Chunk 1 Workflow Chain

**Test Date:** 2026-01-04
**Execution ID:** 262
**Workflow:** V4 Pre-Chunk 0: Intake & Client Identification (70n97A6OmYCsHMmV)
**Test Email Sent:** 2026-01-04 14:59:46 UTC

---

## Summary

- **Total tests:** 1 (Complete workflow chain verification)
- **Status:** ❌ **FAIL**
- **Execution Status:** success (workflow completed without errors)
- **Root Cause:** Empty registry stopped downstream workflow execution

---

## Test Details

### Test: Complete Pre-Chunk 0 → Chunk 1 workflow chain

**Expected Behavior:**
1. Email received and PDF parsed ✅
2. PDF uploaded to temp folder ✅
3. Client identified as "Villa Martens" ✅
4. Registry returns empty result (NEW client scenario) ✅
5. "Check Client Exists" determines client_status = 'NEW' ❌ **NOT EXECUTED**
6. Decision Gate routes to "Execute Chunk 0" ❌ **NOT EXECUTED**
7. Chunk 0 creates folder structure ❌ **NOT EXECUTED**
8. Chunk 1 moves PDF to staging folder ❌ **NOT EXECUTED**
9. Client Registry updated with new entry ❌ **NOT EXECUTED**
10. Temp folder cleaned up ❌ **NOT EXECUTED**

---

## Execution Analysis

### ✅ Stages That Completed Successfully

1. **Gmail Trigger - Unread with Attachments**
   - Status: success
   - Email ID: `19b89859274dca84`
   - Attachment: `OCP-Anfrage-AM10.pdf` (1.95 MB)

2. **Filter PDF/ZIP Attachments**
   - Status: success
   - Filtered 1 PDF attachment

3. **Upload PDF to Temp Folder**
   - Status: success
   - File ID: `1Wpve3TRu4sjoTO3hRU_JTswjPXKH_obI`
   - Location: Temp folder `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm`

4. **Extract File ID & Metadata**
   - Status: success
   - Preserved: `file_id`, `filename`, `emailId`, `emailSubject`, `emailFrom`, `emailDate`

5. **Download PDF from Drive**
   - Status: success
   - Binary data retrieved for text extraction

6. **Extract Text from PDF**
   - Status: success
   - Word count: 729 words
   - Quality: good (no OCR needed)

7. **AI Extract Client Name**
   - Status: success
   - Extracted: `"Villa Martens"`

8. **Normalize Client Name**
   - Status: success
   - Normalized: `"villa_martens"`
   - Parent folder ID: `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm`

9. **Lookup Client Registry**
   - Status: success
   - **Output: 0 items** (empty registry)
   - Execution time: 890ms

---

### ❌ Stages That Did NOT Execute

10. **Check Client Exists** - **NOT EXECUTED**
    - Reason: Received 0 input items from "Lookup Client Registry"
    - Expected behavior: Should have returned `client_status: 'NEW'` even with empty registry
    - Code analysis: Node has logic to handle `registryRows.length === 0`, but never ran

11. **Decision Gate** - **NOT EXECUTED**
    - Reason: No input from "Check Client Exists"

12. **Execute Chunk 0 - Create Folders** - **NOT EXECUTED**
    - Workflow ID: `zbxHkXOoD1qaz6OS`
    - No execution records found

13. **Lookup Staging Folder** - **NOT EXECUTED**

14. **Filter Staging Folder ID** - **NOT EXECUTED**

15. **Execute Chunk 1** - **NOT EXECUTED**
    - Workflow ID: `djsBWsrAEKbj2omB`
    - No execution records found

---

## Root Cause Analysis

### The Problem

When the "Lookup Client Registry" node returns **0 items** (empty registry), n8n does not execute any downstream nodes. This is standard n8n behavior: nodes only execute when they receive at least 1 input item.

### Why This Happened

The Client Registry Google Sheet was completely empty (0 rows, not even a header row). The "Lookup Client Registry" node performed a successful read operation but returned 0 items.

### Code Examination

The "Check Client Exists" node has logic to handle empty registries:

```javascript
// Handle empty registry (0 items or only header row)
if (registryRows.length === 0 || registryRows.length === 1) {
  // Empty registry = new client needs folder creation
  return [{
    json: {
      ...normalizeData,
      client_status: 'NEW',
      root_folder_id: null,
      staging_folder_id: null
    }
  }];
}
```

**However**, this code never ran because the node itself was skipped due to 0 inputs.

---

## Evidence

### File Upload Verification
- **PDF in temp folder:** YES
  - File ID: `1Wpve3TRu4sjoTO3hRU_JTswjPXKH_obI`
  - File name: `OCP-Anfrage-AM10.pdf`
  - Location: `https://drive.google.com/file/d/1Wpve3TRu4sjoTO3hRU_JTswjPXKH_obI/view`

### Client Registry Status
- **Villa Martens entry:** NO (not created)
- **Reason:** Chunk 0 never executed

### Chunk 0 Execution
- **Workflow ID:** `zbxHkXOoD1qaz6OS`
- **Executions:** 0 (never triggered)

### Chunk 1 Execution
- **Workflow ID:** `djsBWsrAEKbj2omB`
- **Executions:** 0 (never triggered)

---

## What Should Have Happened (After Recent Fix)

You mentioned an "empty registry fix" was applied. Based on the workflow code, the fix should have ensured the registry always returns at least a header row so that downstream nodes execute.

However, execution #262 still shows 0 items from the registry lookup, meaning:
1. The fix was not applied before this test ran, OR
2. The fix did not work as expected

---

## Recommended Fix

### Option 1: Always Return at Least 1 Item (Preferred)
Modify the "Lookup Client Registry" node to ALWAYS return at least 1 item, even if the sheet is empty:

```javascript
// After Google Sheets lookup
const registryRows = $input.all();

if (registryRows.length === 0) {
  // Return a dummy header row to ensure downstream execution
  return [{
    json: {
      Client_Name: 'HEADER',
      Root_Folder_ID: '',
      Intake_Folder_ID: ''
    }
  }];
}

return registryRows;
```

### Option 2: Use Code Node After Lookup
Insert a Code node immediately after "Lookup Client Registry" that ensures at least 1 item passes through.

### Option 3: Modify "Check Client Exists" to Run Always
Change the connection so "Check Client Exists" receives input from "Normalize Client Name" instead of "Lookup Client Registry", and have it manually fetch the registry data using `$('Lookup Client Registry').all()`.

---

## Next Steps

1. **Verify the empty registry fix** - Check if header row exists in Client_Registry sheet
2. **Re-run the test** after confirming fix is applied
3. **Monitor Chunk 0 and Chunk 1 executions** to ensure they trigger properly
4. **Verify folder creation** in Google Drive
5. **Verify registry entry** gets added after Chunk 0 completes

---

## Test Result

**VERDICT:** ❌ **FAIL**

The workflow did NOT complete the full Pre-Chunk 0 → Chunk 1 chain. The execution stopped at "Lookup Client Registry" due to 0 items being returned, preventing all downstream folder creation and PDF staging operations.

**Blocker:** Empty registry returns 0 items, causing n8n to skip all downstream nodes.

**Action Required:** Apply the empty registry fix and re-test.
