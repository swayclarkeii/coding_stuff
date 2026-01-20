# n8n Test Report – Expense System Workflow 1: PDF Intake & Parsing

**Workflow ID:** MPjDdVMI88158iFW
**Test Date:** 2026-01-03
**Status:** CANNOT COMPLETE - Blocker Identified

---

## Summary

Unable to execute full end-to-end test due to workflow architecture constraints. The workflow uses a Google Drive Trigger (polling-based), which cannot be manually triggered externally. This is by design for production workflows but prevents traditional test execution.

---

## Findings

### Workflow Architecture Analysis

**Trigger Type:** Google Drive Folder Trigger (polling-based)
- Watches folder ID: `1stmB5nWmoViQKKuQqpkWICPrfPQ_GDN1`
- Poll interval: Every 1 minute
- Event: File creation
- Authentication: Google Service Account

**Pipeline Steps:**
1. Watch Bank Statements Folder (trigger)
2. Download PDF (Google Drive)
3. Extract File Metadata (JavaScript code)
4. Parse PDF with OpenAI Vision (HTTP request to Anthropic API)
5. Parse OpenAI Response (JavaScript code transformation)
6. Write Transactions to Database (Google Sheets append)
7. Log Statement Record (Google Sheets append - Statements sheet)
8. Move PDF to Archive (Google Drive)

**Target Google Sheet:** `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
- Transactions sheet: Stores parsed transactions with 16 columns
- Statements sheet: Logs statement metadata and transaction counts

---

## Test Execution Attempt

### Test Case 1: PDF Upload & Processing
- **Objective:** Verify workflow triggers on PDF upload and processes data end-to-end
- **Attempt:** Manual test via webhook trigger
- **Result:** FAILED - Workflow does not support external webhook triggers
- **Root Cause:** Workflow is production-configured with polling trigger, not webhook

### Test Case 2: Folder Access Verification
- **Objective:** Confirm trigger folder is accessible and monitored
- **Attempt:** List folder contents at ID `1stmB5nWmoViQKKuQqpkWICPrfPQ_GDN1`
- **Result:** BLOCKED - Folder is empty or inaccessible
- **Implication:** Trigger folder may not exist, may be in different Drive, or permissions are insufficient

### Previous Execution Analysis
- **Execution ID:** 21
- **Status:** Error
- **Error Message:** "No data with the current filter could be found"
- **Failed Node:** Watch Bank Statements Folder
- **Error Type:** NodeApiError
- **Timestamp:** 2026-01-02 19:29:15 UTC
- **Implication:** Trigger node cannot access the configured folder

---

## Blockers & Issues

| Issue | Severity | Details |
|-------|----------|---------|
| Trigger Folder Inaccessible | CRITICAL | Folder ID `1stmB5nWmoViQKKuQqpkWICPrfPQ_GDN1` returns "No data" error. May not exist or permissions insufficient. |
| No External Trigger | CRITICAL | Workflow uses polling trigger (not webhook). Cannot be manually triggered for testing without actual file upload. |
| Service Account Permissions | HIGH | Workflow depends on Google Service Account credentials. Need to verify: Can list folder? Can download files? Can write to Sheet? Can move files? |
| PDF Parser Setup | UNKNOWN | Workflow calls Anthropic Claude Vision API. Configuration assumes valid credentials and model availability. |
| Archive Folder | UNKNOWN | Workflow uses env variable `$env.ARCHIVE_STATEMENTS_FOLDER_ID` to archive PDFs. This may not be configured. |

---

## Recommended Test Strategy

To fully test this workflow, you have two options:

### Option 1: Verify Folder Setup (Fastest)
1. Confirm the trigger folder ID `1stmB5nWmoViQKKuQqpkWICPrfPQ_GDN1` exists in your Google Drive
2. Verify Google Service Account has:
   - Read access to trigger folder
   - Read/download access to PDF files within it
   - Read/write access to Sheets (`1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`)
   - Write access to archive folder (referenced by `$env.ARCHIVE_STATEMENTS_FOLDER_ID`)
3. Once verified, manually upload a test PDF to the trigger folder
4. Wait 1-2 minutes for polling trigger to detect the file
5. Monitor execution in n8n UI
6. Verify data appears in Transactions and Statements sheets

### Option 2: Create a Webhook Wrapper (Most Testable)
1. Create a new workflow with a Webhook trigger
2. This webhook accepts file metadata and binary data
3. Pass data to the existing PDF parsing nodes (skip Google Drive Download)
4. This allows external triggering via HTTP POST
5. Test via HTTP client or cURL

### Option 3: Use n8n Manual Trigger (Partial)
1. Add a Manual Trigger node alongside the Google Drive trigger
2. Configure it to pass file metadata
3. Allows testing parsing logic without actual file upload
4. Note: Workflow must be in "Test" mode or trigger won't execute

---

## Environmental Dependencies

**Required Credentials (Currently Configured):**
- Google Service Account (ID: VdNWQlkZQ0BxcEK2) - for Drive & Sheets operations
- Anthropic API (ID: MRSNO4UW3OEIA3tQ) - for PDF parsing via Claude Vision
- OpenAI API (ID: xmJ7t6kaKgMwA1ce) - available but not used (Parse PDF node uses Anthropic)

**Environment Variables Required:**
- `ARCHIVE_STATEMENTS_FOLDER_ID` - Google Drive folder ID for archiving processed PDFs
  - Status: UNKNOWN if configured

**Google Sheet Requirements:**
- Sheet ID: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
- Must have two sheets: "Transactions" and "Statements"
- Transactions sheet: Columns for TransactionID, Date, Bank, Amount, Currency, Description, Vendor, Category, ReceiptID, StatementID, MatchStatus, MatchConfidence, Notes, Tags, Type, AnnualInvoiceID
- Statements sheet: Columns for StatementID, Bank, Month, Year, FileID, FilePath, ProcessedDate, TransactionCount

---

## Data Flow Example (When Working)

**Input:** PDF file uploaded to trigger folder (e.g., `ING_2025-01_Statement.pdf`)

**Processing:**
```
File: ING_2025-01_Statement.pdf
├─ Extracted metadata:
│  ├─ Bank: ING
│  ├─ Month: 01
│  ├─ Year: 2025
│  ├─ StatementID: STMT-ING-202501-{timestamp}
│  └─ FileID: {Google Drive ID}
│
├─ Claude Vision parses transactions from PDF:
│  ├─ Date: DD.MM.YYYY format
│  ├─ Description: Transaction details
│  ├─ Amount: -/+ number (EUR)
│  └─ Currency: EUR (default)
│
├─ Transform to standard format:
│  └─ Generate TransactionID for each
│
├─ Write to Google Sheets:
│  ├─ Transactions sheet: One row per transaction
│  └─ Statements sheet: One metadata row per statement
│
└─ Archive: Move PDF to folder structure:
   └─ {ARCHIVE_FOLDER}/ING/{original filename}
```

**Output:**
- Transactions sheet has new rows with parsed transaction data
- Statements sheet has new row with statement metadata
- Original PDF moved to archive folder by bank

---

## Conclusion

**Test Status:** INCONCLUSIVE - Blocked by infrastructure issues

The workflow itself appears **correctly built** based on code review:
- Node configuration is valid
- Data mappings are proper
- Sheet column schema matches expected output
- API credentials are configured
- Error handling is basic but present

**However, testing is blocked until:**
1. Trigger folder (`1stmB5nWmoViQKKuQqpkWICPrfPQ_GDN1`) is confirmed to exist and is accessible
2. Google Service Account permissions are verified for all required operations
3. Environment variable `ARCHIVE_STATEMENTS_FOLDER_ID` is configured
4. A test PDF is manually uploaded to trigger folder

**Next Steps (For Sway):**
1. Verify the trigger folder ID in your Google Drive
2. Confirm all Google Service Account permissions
3. Set up the archive folder and configure the env variable
4. Upload a test PDF and monitor the execution
5. Once successful, the workflow is production-ready for automated statement processing
