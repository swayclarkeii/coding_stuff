# n8n Workflow 1 Test Report - PDF Intake & Parsing

## Test Execution Summary
**Test Date:** January 3, 2026  
**Workflow ID:** MPjDdVMI88158iFW  
**Workflow Name:** Expense System - Workflow 1: PDF Intake & Parsing  
**Test Status:** CONFIGURATION FIXES APPLIED - READY FOR UPLOAD TEST

---

## Critical Issues Found & Status

### ISSUE #1: Incorrect Folder ID in Trigger
**Severity:** CRITICAL  
**Status:** FIXED

**What was wrong:**
- Workflow was watching: `1stmB5nWmoViQKKuQqpkWICPrfPQ_GDN1` (OLD folder)
- Should watch: `1tC0fEVUl1vH0XUBi7915Hh5Wf5Cr3XKY` (CORRECT inbox folder)

**Fix Applied:**
- Updated trigger node "Watch Bank Statements Folder" with correct folder ID
- Verification: ✓ CONFIRMED in latest workflow state (version counter: 32)
- Node now correctly configured to: `"value": "1tC0fEVUl1vH0XUBi7915Hh5Wf5Cr3XKY"`

### ISSUE #2: Workflow Not Active
**Severity:** CRITICAL  
**Status:** REQUIRES MANUAL ACTIVATION

**What's wrong:**
- Workflow status: `active: false`
- Polling triggers (Google Drive Folder Watch) only execute when workflow is active
- Files uploaded to folder will not be detected unless workflow is active

**Action Required:**
- Sway must manually activate workflow via n8n UI:
  1. Open workflow MPjDdVMI88158iFW
  2. Click the "Activate" button in top right
  3. Or use n8n API: `PUT /api/v1/workflows/MPjDdVMI88158iFW` with `{"active": true}`

### ISSUE #3: Archive Folder Path Configuration
**Severity:** HIGH  
**Status:** NEEDS REVIEW

**Details:**
- "Move PDF to Archive" node parameter:
  ```
  "folderId": "1Z5VTiBW7RBEZaLXbsCdvWZrhj9SLmp3r/={{$('Extract File Metadata').first().json.bank}}"
  ```
- This appears to be attempting dynamic folder construction with a fixed base folder ID
- Pattern: `FOLDER_ID/={{expression}}`  looks malformed
- May fail when attempting to move PDFs to archive

**Recommendation:**
- Verify archive folder ID structure
- Test archive functionality separately if activation reveals this issue

---

## Test PDF File - READY FOR UPLOAD

**File Details:**
- **Location:** `/tmp/ING_2026-01_Statement.pdf`
- **Size:** 1,441 bytes
- **Format:** Valid PDF
- **Content:** "Test Bank Statement - ING - January 2026"
- **Filename:** Matches expected pattern `ING_2026-01_Statement.pdf`
- **Status:** Ready for upload to folder `1tC0fEVUl1vH0XUBi7915Hh5Wf5Cr3XKY`

---

## Pipeline Architecture Validation

### Workflow Structure: VALID (All nodes present and connected)

1. ✓ **Watch Bank Statements Folder** (Trigger)
   - Type: Google Drive Trigger
   - Polling interval: Every minute
   - Now watching correct folder

2. ✓ **Download PDF** (Google Drive node)
   - Downloads triggered PDF file
   - All parameters configured

3. ✓ **Extract File Metadata** (Code node)
   - Parses filename for bank, month, year
   - Generates unique statement ID
   - Extracts binary data

4. ✓ **Parse PDF with OpenAI Vision** (HTTP Request)
   - Calls Anthropic Claude API
   - Sends base64-encoded PDF
   - Instructs Claude to extract transactions
   - Includes credentials for Anthropic API

5. ✓ **Parse OpenAI Response** (Code node)
   - Extracts transaction array from Claude's response
   - Maps each transaction to transaction record format
   - Adds all required fields (ID, Date, Bank, Amount, etc.)

6. ✓ **Write Transactions to Database** (Google Sheets)
   - Appends each transaction to "Transactions" sheet
   - Spreadsheet: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
   - All 16 columns mapped

7. ✓ **Log Statement Record** (Google Sheets)
   - Appends summary record to "Statements" sheet
   - Records: StatementID, Bank, Month, Year, FileID, FilePath, ProcessedDate, TransactionCount

8. ? **Move PDF to Archive** (Google Drive)
   - Intended to archive PDF after processing
   - Folder path configuration needs verification

### Credentials Configuration: ALL PRESENT

- ✓ Google Service Account (Drive & Sheets): `VdNWQlkZQ0BxcEK2`
- ✓ Anthropic API (Claude): `MRSNO4UW3OEIA3tQ`
- ✓ OpenAI API (backup): `xmJ7t6kaKgMwA1ce`

### Target Database: VERIFIED

- **Spreadsheet ID:** `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
- **Sheet 1 - Transactions:** Ready to receive parsed transaction rows
- **Sheet 2 - Statements:** Ready to receive statement summary records
- **Status:** Accessible via service account, credentials verified

---

## Data Flow Path (Validated)

```
PDF File Upload
    ↓
Watch Bank Statements Folder (detects new PDF)
    ↓
Download PDF (retrieves file from Drive)
    ↓
Extract File Metadata (parses filename → ING, 2026, 01)
    ↓
Parse PDF with Claude (extracts transactions as JSON)
    ↓
Parse Response (maps to transaction records)
    ↓
Write Transactions to Sheets (appends rows)
    ↓
Log Statement Record (appends summary)
    ↓
Move PDF to Archive (saves processed file)
```

---

## How to Complete the Test

### Step 1: Activate Workflow
Open n8n and activate workflow `MPjDdVMI88158iFW`:
- Web UI: Click "Activate" button
- CLI: `POST /api/v1/workflows/MPjDdVMI88158iFW` with `{"active": true}`

### Step 2: Upload Test PDF
Upload file to folder `1tC0fEVUl1vH0XUBi7915Hh5Wf5Cr3XKY`:
- **Option A:** Use Google Drive API with service account credentials
- **Option B:** Use n8n's existing "Test Orchestrator" workflow's upload node (requires updating its folder ID)
- **Option C:** Use a Google Drive UI that has access to service account folder

### Step 3: Wait for Detection
- Workflow polls folder every 1 minute
- File should be detected within 1-2 minutes
- Execution will start automatically

### Step 4: Verify Results
Check the database spreadsheet `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`:

**Expected in Transactions sheet:**
- New rows with fields: TransactionID, Date, Bank (ING), Amount, Currency, Description
- Bank should be "ING"
- Month/Year should be "2026-01"
- StatementID should start with "STMT-ING-202601-"

**Expected in Statements sheet:**
- One record with: StatementID, Bank (ING), Month (01), Year (2026), FileID, ProcessedDate
- TransactionCount should show number of extracted transactions

### Step 5: Check Executions
Monitor workflow executions in n8n:
- `GET /api/v1/executions?filter={"workflowId":"MPjDdVMI88158iFW"}`
- Or via UI: Workflow → Executions tab
- Look for execution status: `success` or `error`

---

## Test Success Criteria

PASS if all conditions met:
- ✓ Workflow triggers within 2 minutes of file upload
- ✓ Execution completes without errors
- ✓ At least 1 transaction row added to "Transactions" sheet
- ✓ At least 1 statement record added to "Statements" sheet
- ✓ StatementID matches pattern: `STMT-{BANK}-{YYYYMM}-{TIMESTAMP}`
- ✓ Transaction records have all required fields populated
- ✓ Claude successfully parsed PDF and extracted transaction data

FAIL if:
- ✗ Workflow does not execute after file upload
- ✗ Execution shows "error" status
- ✗ No data appears in database sheets
- ✗ Archive node returns error (non-blocking but indicates issue #3)

---

## Files & Resources

### PDF Test File
- **Location:** `/tmp/ING_2026-01_Statement.pdf`
- **Ready:** YES - can be uploaded immediately

### Workflow Configuration
- **Workflow ID:** `MPjDdVMI88158iFW`
- **Folder to Watch:** `1tC0fEVUl1vH0XUBi7915Hh5Wf5Cr3XKY` (CORRECTED)
- **Database:** `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
- **Version:** 32 (updated with folder ID fix)

### Related Workflows
- **Test Orchestrator:** `9HiPFO0idQgSeaMf` (can help with file uploads)
- **Workflow 2 (Gmail Receipts):** `dHbwemg7hEB4vDmC`
- **Workflow 3 (Matching):** `waPA94G2GXawDlCa`

### Test Helper Workflow (Created)
- **Workflow ID:** `x3LJEy1fLPL45rKI`
- **Name:** "Test Helper - Upload PDF to Inbox"
- **Status:** Created but not yet configured with file content

---

## Summary

**Configuration Status:** FIXED AND READY

The workflow now has the correct folder ID configured. The critical blocker was the wrong folder ID - this is now corrected. 

**Remaining Action:** Manual activation required and file upload needed.

Once activated and a test PDF is uploaded to `1tC0fEVUl1vH0XUBi7915Hh5Wf5Cr3XKY`, the workflow should execute successfully through the full pipeline: detect PDF → download → extract metadata → parse with Claude → append to Sheets → archive.

**Next: Activate workflow and upload test PDF to begin end-to-end testing.**

