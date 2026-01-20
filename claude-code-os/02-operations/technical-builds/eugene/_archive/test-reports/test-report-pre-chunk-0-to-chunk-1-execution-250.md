# n8n Test Report - Pre-Chunk 0 to Chunk 1 File Movement (Execution #250)

## Summary
- Total tests: 6
- PASSED: 2
- FAILED: 4
- **OVERALL VERDICT: FAIL - File movement workflow is broken**

---

## Critical Findings

### BLOCKER ISSUE: Wrong Workflow Called as "Chunk 1"
The workflow configured as "Execute Chunk 1" is calling the **folder creation workflow** (zbxHkXOoD1qaz6OS) instead of a file movement workflow. This is a fundamental configuration error.

**Evidence:**
- Chunk 1 execution #251 created entire folder structure (OBJEKTUNTERLAGEN, WIRTSCHAFTLICHE_UNTERLAGEN, etc.)
- No "Move File to Staging" node exists in the executed workflow
- Workflow ID zbxHkXOoD1qaz6OS is the folder creation workflow, not file movement

### BLOCKER ISSUE: file_id Not Passed to Chunk 1
The file_id from "Upload PDF to Temp Folder" is NOT being passed to "Execute Chunk 1".

**Evidence:**
- Pre-Chunk 0 uploaded file successfully with file_id: `1EaF5vVYsSerNlAAMgV1tF-wlrBxWgKKk`
- Execute Chunk 1 output contains: `emailId`, `threadId`, `from`, `subject`, `client_normalized`, `staging_folder_id`
- Execute Chunk 1 output MISSING: `file_id`, `file_name`, or any reference to the uploaded PDF

---

## Detailed Test Results

### Test 1: Pre-Chunk 0 - Upload PDF to Temp Folder
- **Status:** PASS
- **Execution ID:** 250
- **Execution Status:** success
- **Node:** Upload PDF to Temp Folder
- **File Details:**
  - File ID: `1EaF5vVYsSerNlAAMgV1tF-wlrBxWgKKk`
  - File Name: `OCP-Anfrage-AM10.pdf`
  - File Size: 1,949,265 bytes
  - Upload Location: Temp folder `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm`
  - Upload Time: 2026-01-04T14:28:06.171Z
- **Notes:** File upload succeeded perfectly. PDF is in temp folder.

---

### Test 2: Pre-Chunk 0 - Execute Chunk 1 Passes file_id
- **Status:** FAIL
- **Execution ID:** 250
- **Execution Status:** success (but wrong data passed)
- **Node:** Execute Chunk 1
- **Expected:** file_id (`1EaF5vVYsSerNlAAMgV1tF-wlrBxWgKKk`) passed to Chunk 1
- **Actual:** Only email metadata passed:
  ```json
  {
    "emailId": "19b8967c0bb78e9e",
    "client_normalized": "villa_martens",
    "staging_folder_id": "1HdqcfWMNIhapjvm3-gPBybL5Tp064Yjm"
  }
  ```
- **Error:** file_id is missing from the data passed to Chunk 1
- **Impact:** Chunk 1 cannot move a file it doesn't know about
- **Failing Node Logic:** "Filter Staging Folder ID" or "Execute Chunk 1" node is not including file_id in the payload

---

### Test 3: Chunk 1 - Move File to Staging Executed
- **Status:** FAIL
- **Execution ID:** 251, 253
- **Execution Status:** success (but wrong workflow)
- **Expected Node:** "Move File to Staging"
- **Actual Nodes Executed:**
  - Create Root Folder
  - Prepare Parent Folders
  - Loop Parents
  - Create Parent Folder
  - Prepare Subfolders
  - Loop Subfolders
  - Create Subfolder
  - List All Folders
  - Collect Folder IDs
  - Write Folder IDs to Sheet
  - Write to Client Registry
- **Error:** Executed workflow is "Chunk 0: Create Folder Structure" (zbxHkXOoD1qaz6OS), NOT a file movement workflow
- **Impact:** File never moved from temp to staging
- **Root Cause:** "Execute Chunk 1" node is configured to call the wrong workflow ID

---

### Test 4: Google Drive - PDF in Staging Folder
- **Status:** FAIL
- **Expected:** PDF `OCP-Anfrage-AM10.pdf` should be in staging folder `1HdqcfWMNIhapjvm3-gPBybL5Tp064Yjm`
- **Actual:** File was never moved (wrong workflow executed)
- **Staging Folder ID:** `1HdqcfWMNIhapjvm3-gPBybL5Tp064Yjm` (from Chunk 1 output)
- **Error:** File not in staging because move operation never happened
- **Impact:** File stuck in temp folder

---

### Test 5: Google Drive - PDF Removed from Temp Folder
- **Status:** FAIL
- **Expected:** PDF `OCP-Anfrage-AM10.pdf` should be GONE from temp folder `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm`
- **Actual:** File still in temp folder (because move never happened)
- **Temp Folder ID:** `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm`
- **File ID:** `1EaF5vVYsSerNlAAMgV1tF-wlrBxWgKKk`
- **Error:** Move operation never executed
- **Impact:** Temp folder will accumulate PDFs indefinitely

---

### Test 6: Complete Pre-Chunk 0 to Chunk 1 Workflow Chain
- **Status:** FAIL
- **Expected Flow:**
  1. Pre-Chunk 0: Upload PDF to temp → get file_id
  2. Pre-Chunk 0: Pass file_id to Chunk 1
  3. Chunk 1: Move file from temp to staging
  4. Result: PDF in staging, removed from temp
- **Actual Flow:**
  1. Pre-Chunk 0: Upload PDF to temp → get file_id ✅
  2. Pre-Chunk 0: Execute Chunk 1 WITHOUT file_id ❌
  3. Chunk 1: Created NEW folder structure (wrong workflow) ❌
  4. Result: PDF still in temp, NOT in staging ❌
- **Error:** Workflow chain is completely broken
- **Impact:** File movement system is non-functional

---

## Root Cause Analysis

### Issue 1: Wrong Workflow ID in "Execute Chunk 1" Node
**Location:** Pre-Chunk 0 workflow (70n97A6OmYCsHMmV) → "Execute Chunk 1" node

**Problem:** The "Execute Chunk 1" node is configured to call workflow ID `zbxHkXOoD1qaz6OS`, which is the "Chunk 0: Create Folder Structure" workflow.

**Evidence:**
- Execution #251 and #253 show Chunk 1 workflow ID as `zbxHkXOoD1qaz6OS`
- This workflow creates folders, not moves files
- No "Move File to Staging" node exists in this workflow

**Fix Required:** Update "Execute Chunk 1" node to call the correct file movement workflow (likely "Chunk 2: File Movement" or create a new "Chunk 1: File Movement" workflow)

### Issue 2: file_id Not Included in Chunk 1 Payload
**Location:** Pre-Chunk 0 workflow → "Filter Staging Folder ID" or "Execute Chunk 1" node

**Problem:** The data passed to "Execute Chunk 1" only includes email metadata and staging_folder_id, but NOT the file_id from "Upload PDF to Temp Folder".

**Evidence:**
- "Upload PDF to Temp Folder" output has: `id: "1EaF5vVYsSerNlAAMgV1tF-wlrBxWgKKk"`
- "Execute Chunk 1" input/output has: `emailId`, `client_normalized`, `staging_folder_id`
- No file_id anywhere in the Chunk 1 execution

**Fix Required:**
1. In "Filter Staging Folder ID" node: Include `file_id: $('Upload PDF to Temp Folder').first().json.id` in the output
2. In "Execute Chunk 1" node: Ensure file_id is passed in the workflow trigger payload

---

## Execution Timeline

| Time (UTC) | Node/Workflow | Action | Result |
|------------|---------------|--------|--------|
| 14:28:04 | Pre-Chunk 0 | Started | - |
| 14:28:06 | Upload PDF to Temp Folder | Uploaded PDF | File ID: 1EaF5vVYsSerNlAAMgV1tF-wlrBxWgKKk |
| 14:29:16 | Execute Chunk 1 | Called wrong workflow | Triggered zbxHkXOoD1qaz6OS (folder creation) |
| 14:28:11 | Chunk 1 #251 | Created folders | Created villa_martens_Documents structure |
| 14:29:17 | Chunk 1 #253 | Created folders AGAIN | Created DUPLICATE folder structure |
| 14:30:21 | Pre-Chunk 0 | Finished | SUCCESS (but file not moved) |

---

## Key Metrics

- **Pre-Chunk 0 Duration:** 137 seconds
- **Upload to Temp Duration:** 2.7 seconds
- **Execute Chunk 1 Call Duration:** 0.4 seconds
- **Chunk 1 Execution Duration:** 63 seconds (both #251 and #253)
- **Total Workflow Time:** ~138 seconds
- **Files Moved:** 0 (expected: 1)
- **Folders Created:** 88 (42 subfolders × 2 executions = 84 + 4 parents = 88)

---

## Required Fixes

### Priority 1: BLOCKER - Fix Workflow Configuration
1. **Identify or create the correct file movement workflow**
   - This workflow should have a "Move File to Staging" node
   - Should accept: `file_id`, `staging_folder_id`, `client_normalized`
   - Should output: `success`, `moved_file_id`, `new_location`

2. **Update "Execute Chunk 1" node in Pre-Chunk 0**
   - Change workflow ID from `zbxHkXOoD1qaz6OS` to the correct file movement workflow ID
   - Ensure it's configured to pass the right payload

### Priority 2: BLOCKER - Pass file_id to Chunk 1
1. **Update "Filter Staging Folder ID" node** (or create new node before "Execute Chunk 1"):
   ```javascript
   return {
     json: {
       file_id: $('Upload PDF to Temp Folder').first().json.id,
       file_name: $('Upload PDF to Temp Folder').first().json.name,
       staging_folder_id: <staging_folder_id>,
       client_normalized: <client_normalized>,
       temp_folder_id: '1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm'
     }
   };
   ```

2. **Verify "Execute Chunk 1" node payload includes**:
   - `file_id`
   - `staging_folder_id`
   - `temp_folder_id` (optional, but useful)
   - `client_normalized`

### Priority 3: Test and Validate
1. **Create/verify Chunk 1 file movement workflow** with:
   - Execute Workflow Trigger (receives file_id, staging_folder_id)
   - Get File Metadata (optional validation step)
   - Move File to Staging (Google Drive: Update File)
   - Return Success Status

2. **Test complete chain**:
   - Send test email with PDF
   - Verify file uploaded to temp
   - Verify file_id passed to Chunk 1
   - Verify file moved to staging
   - Verify file removed from temp

---

## Workflow Structure Issues

### Current (BROKEN) Flow:
```
Pre-Chunk 0
  └─ Upload PDF to Temp ✅
  └─ Extract File ID ✅
  └─ Execute Chunk 1 ❌ (calls WRONG workflow, passes WRONG data)
       └─ zbxHkXOoD1qaz6OS (Folder Creation) ❌
            └─ Creates 42 folders ❌
            └─ NO file movement ❌
```

### Expected (CORRECT) Flow:
```
Pre-Chunk 0
  └─ Upload PDF to Temp ✅
  └─ Extract File ID ✅
  └─ Prepare Chunk 1 Payload (file_id + staging_folder_id)
  └─ Execute Chunk 1 (calls FILE MOVEMENT workflow)
       └─ Chunk 1: File Movement
            └─ Move File to Staging ✅
            └─ Return Success ✅
```

---

## Test Conclusion

The Pre-Chunk 0 → Chunk 1 workflow chain is **COMPLETELY BROKEN** for file movement:

1. ❌ Wrong workflow called (folder creation instead of file movement)
2. ❌ file_id not passed to Chunk 1
3. ❌ File never moved from temp to staging
4. ❌ Temp folder accumulating files
5. ❌ Duplicate folder structures being created (executions #251 and #253 both created folders)

**RECOMMENDATION:**
1. Stop using Pre-Chunk 0 workflow until fixes are implemented
2. Create proper Chunk 1 file movement workflow
3. Fix "Execute Chunk 1" node to call correct workflow with correct payload
4. Re-test complete chain
5. Clean up duplicate folders created by incorrect executions

---

## Files & Resources

**Test Execution:**
- Pre-Chunk 0 Workflow ID: `70n97A6OmYCsHMmV`
- Pre-Chunk 0 Execution ID: `250`
- Chunk 1 (WRONG) Workflow ID: `zbxHkXOoD1qaz6OS`
- Chunk 1 Execution IDs: `251`, `253`

**Google Drive:**
- Temp Folder ID: `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm`
- Staging Folder ID: `1HdqcfWMNIhapjvm3-gPBybL5Tp064Yjm`
- Uploaded File ID: `1EaF5vVYsSerNlAAMgV1tF-wlrBxWgKKk`
- File Name: `OCP-Anfrage-AM10.pdf`
- File Size: 1.9 MB

**Test Report File:**
- Path: `/Users/swayclarke/coding_stuff/test-report-pre-chunk-0-to-chunk-1-execution-250.md`
- Generated: 2026-01-04

---

*Report generated by test-runner-agent*
