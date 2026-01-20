# n8n Test Report - Expense System Workflow 4

**Workflow ID**: nASL6hxNQGrNBTV4
**Workflow Name**: Expense System - Workflow 4: Monthly Folder Builder & Organizer v2.0
**Test Date**: 2026-01-08 23:16:19 UTC
**Execution ID**: 658

---

## Summary

- Total tests: 1
- FAIL: 1
- PASS: 0

---

## Test Details

### Test: Process receipts for December 2025 with empty transaction_id fields

**Status**: FAIL

**Input**:
```json
{
  "month_year": "December 2025"
}
```

**Expected Behavior**:
1. Create folder structure for December 2025
2. Skip statements (0 records in database)
3. Process 7 receipts from Receipts sheet
4. Move receipts to appropriate bank folders
5. Update Receipts sheet with new FilePath values
6. Generate summary report

**Actual Result**:

**Execution Status**: error
**Duration**: 14.6 seconds
**Failed at Node**: Process Receipts

**Error Message**:
```
Cannot assign to read only property 'name' of object 'Error: Node 'Read Transactions Sheet' hasn't been executed'
```

**What Happened**:

The workflow successfully completed these steps:
1. Created Year Folder (VAT 2025)
2. Created Main VAT Folder (VAT December 2025)
3. Created 4 bank folders (ING Diba, Deutsche Bank, Barclays, Mastercard)
4. Created Statements and Receipts subfolders for each bank
5. Created Income folder
6. Read Statements Sheet (0 records - correctly skipped)
7. Read Receipts Sheet (7 records found)
8. Read Transactions Sheet (parallel branch)

**Failure occurred at**: Process Receipts node

**Root Cause**:

The "Process Receipts" Code node attempts to reference data from "Read Transactions Sheet" using:
```javascript
const transactions = $('Read Transactions Sheet').all();
```

However, the three sheet-reading nodes (Statements, Receipts, Transactions) run in **parallel branches** from "Create Income Folder". The "Process Receipts" node runs immediately after "Read Receipts Sheet" completes, but "Read Transactions Sheet" may not have completed yet (or at all if it encounters issues).

**Additional Issue - Data Validation**:

Even if the parallel execution issue were resolved, **all 7 receipts would have been skipped** because:
- Each receipt has an **empty `transaction_id` field** in the Receipts sheet
- The "Process Receipts" node requires `transaction_id` to match receipts to banks via the Transactions sheet
- Without a valid `transaction_id`, receipts cannot be assigned to the correct bank folder

**Receipts Data from Execution**:
```json
{
  "row_number": 2,
  "ReceiptID": "RCPT-DEUTSCHE-BAHN-1767905303682",
  "FileName": "Ticket_541031569097_03.11.2025__R.pdf",
  "Vendor": "Deutsche Bahn",
  "transaction_id": ""  // EMPTY
}
```

All 7 receipts have `transaction_id: ""`.

**Nodes Successfully Executed**:
1. Webhook Trigger (Manual) - 1 item
2. Parse Month/Year Input - 1 item
3. Create Year Folder - 1 item
4. Create Main VAT Folder - 1 item
5. Prepare Bank Folders - 4 items
6. Create Bank Folder - 4 items
7. Create Statements Subfolder - 4 items
8. Create Receipts Subfolder - 4 items
9. Wait for Subfolders - merge completed
10. Get Main Folder Data - 1 item
11. Create Income Folder - 1 item
12. Read Receipts Sheet - 7 items

**Nodes Not Executed**:
- Process Receipts (failed)
- Move Receipt Files (not reached)
- Update Receipts FilePath (not reached)
- Wait for Processing (not reached)
- Generate Summary Report (not reached)
- Respond to Webhook (not reached)

---

## Issues Identified

### 1. Workflow Design Issue: Parallel Branch Data Dependency

**Problem**: The "Process Receipts" node depends on data from "Read Transactions Sheet", but these run in separate parallel branches. n8n does not guarantee that "Read Transactions Sheet" will complete before "Process Receipts" executes.

**Impact**: Execution error preventing workflow completion.

**Recommended Fix**: Restructure the workflow to ensure "Read Transactions Sheet" completes before "Process Receipts" runs. Options:
- Use a Merge node to wait for all three sheet reads to complete before processing
- Chain the sheet reads sequentially if parallel execution is not required
- Use a Wait node or conditional logic to ensure data availability

### 2. Data Issue: Empty transaction_id Fields

**Problem**: All 7 receipts in the Receipts sheet have empty `transaction_id` fields.

**Impact**: Even if the workflow executes without errors, all receipts would be skipped with "No transaction_id" errors.

**Expected Behavior**: Each receipt should have a valid `transaction_id` that matches a record in the Transactions sheet to determine which bank folder to use.

**Recommended Fix**:
- Populate `transaction_id` fields in the Receipts sheet with valid transaction IDs
- OR modify the workflow to use vendor-based routing (e.g., use the "Vendor" field to determine bank folder)
- OR add fallback logic to handle receipts without transaction IDs

### 3. Alternative Approach: Vendor-Based Routing

The Receipts sheet already contains a "Vendor" field (e.g., "Deutsche Bahn", "flaschenpost"). If vendor-to-bank mapping is predictable, the workflow could route receipts based on vendor instead of requiring transaction matching.

---

## Test Verdict

**FAIL - Workflow cannot complete due to design and data issues**

**Blockers**:
1. Parallel branch data dependency causes execution error
2. Empty `transaction_id` fields would prevent receipt processing even if error is fixed

**Next Steps**:
1. Fix workflow structure to resolve parallel branch dependency
2. Either populate transaction_id fields OR implement vendor-based routing
3. Re-test with corrected workflow and data

---

## Execution Timeline

- Start: 2026-01-08 23:16:19.483Z
- Stop: 2026-01-08 23:16:34.088Z
- Duration: 14.605 seconds
- Final Status: error

---

## Files Processed

**Statements**: 0 (sheet empty - correctly skipped)
**Receipts**: 7 found, 0 processed (failed before processing)

**Receipt Files Identified**:
1. Ticket_541031569097_03.11.2025__R.pdf (Deutsche Bahn)
2. Ticket_541031569097_31.10.2025__H.pdf (Deutsche Bahn)
3. (5 additional flaschenpost receipts)

**Folders Created**:
- VAT 2025/
  - VAT December 2025/
    - ING Diba/
      - Statements/
      - Receipts/
    - Deutsche Bank/
      - Statements/
      - Receipts/
    - Barclays/
      - Statements/
      - Receipts/
    - Mastercard/
      - Statements/
      - Receipts/
    - Income/

---

## Recommendations

1. **Immediate**: Fix the parallel branch dependency in the workflow structure
2. **Data**: Populate transaction_id fields in Receipts sheet OR implement vendor-based routing
3. **Testing**: Add error handling for empty transaction_id cases
4. **Validation**: Add workflow validation to check for data dependencies before processing
