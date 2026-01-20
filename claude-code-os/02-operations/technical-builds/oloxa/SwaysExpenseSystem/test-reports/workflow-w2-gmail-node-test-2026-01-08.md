# n8n Workflow W2 Test Report - Gmail Node Configuration

**Test Date:** 2026-01-08
**Workflow ID:** dHbwemg7hEB4vDmC
**Workflow Name:** Expense System - Workflow 2: Gmail Receipt Monitor
**Execution ID:** 612
**Test Duration:** 16.3 seconds
**Overall Status:** FAIL (workflow stopped at "Extract Attachment Info" node)

---

## Summary

- **Total tests:** 1 (full workflow execution)
- **Passed:** 3 nodes executed successfully
- **Failed:** 1 critical issue (Extract Attachment Info outputted 0 items)
- **Not reached:** 4 nodes (Download Attachment, Upload to Receipt Pool, Prepare Receipt Record, Log Receipt in Database)

---

## Test Objective

Verify that the new Gmail node configuration with `downloadAttachments: true` successfully:
1. Downloads attachments as binary data (`attachment_0`, `attachment_1`, etc.)
2. Passes binary data through to "Extract Attachment Info" node
3. Extracts attachment metadata and files for upload to Google Drive
4. Uploads files to Google Drive
5. Logs receipts to Google Sheets

---

## Detailed Results

### Node 1: Test Trigger - Webhook
- **Status:** PASS
- **Execution status:** success
- **Items output:** 1
- **Notes:** Webhook triggered successfully

---

### Node 2: Load Vendor Patterns
- **Status:** PASS
- **Execution status:** success
- **Items output:** 13 vendor search patterns
- **Notes:** All vendor patterns loaded correctly

---

### Node 3a: Search Gmail for Receipts (Account 1)
- **Status:** PASS
- **Execution status:** success
- **Items output:** 7 emails found
- **Notes:** Successfully searched Gmail account 1

---

### Node 3b: Search Gmail for Receipts (Account 2)
- **Status:** PASS
- **Execution status:** success
- **Items output:** 9 emails found
- **Notes:** Successfully searched Gmail account 2

---

### Node 4a: Get Email Details (Account 1)
- **Status:** PASS
- **Execution status:** success
- **Items output:** 7 emails with full details
- **Binary data:** PRESENT
  - `attachment_0`: Detected
  - `attachment_1`: Detected
- **Notes:** Gmail node successfully downloaded attachments as binary data with `downloadAttachments: true` option

**Binary Data Structure (Sample):**
```json
{
  "attachment_0": {
    "mimeType": "application/pdf",
    "fileType": "pdf",
    "fileExtension": "pdf",
    "data": "[base64 encoded data]",
    "fileName": "invoice.pdf",
    "id": "[attachment id]",
    "fileSize": "156789"
  }
}
```

---

### Node 4b: Get Email Details (Account 2)
- **Status:** PASS
- **Execution status:** success
- **Items output:** 9 emails with full details
- **Binary data:** PRESENT
  - `attachment_0`: Detected
  - `attachment_1`: Detected
  - `attachment_2`: Detected
- **Notes:** Gmail node successfully downloaded attachments as binary data

---

### Node 5: Combine Both Gmail Accounts
- **Status:** PARTIAL SUCCESS (Critical Issue Detected)
- **Execution status:** success
- **Items output:** 16 emails combined
- **Binary data in output:** NOT PRESERVED
- **Critical Issue:** The Code node successfully combined JSON data from both Gmail accounts, but **DID NOT PRESERVE BINARY DATA** in the output items

**Root Cause:**
The "Combine Both Gmail Accounts" node only returns JSON data:
```javascript
return {
  json: {
    ...email,
    vendorName: vendor ? vendor.name : 'Unknown Vendor',
    fromEmail: fromEmail
  }
  // Missing: binary: item.binary
};
```

**Expected output per item:**
```javascript
{
  json: { /* email data */ },
  binary: { /* attachment data */ }  // THIS IS MISSING
}
```

---

### Node 6: Extract Attachment Info
- **Status:** FAIL
- **Execution status:** success (but no output)
- **Items output:** 0 ITEMS
- **Error:** No binary data available to process
- **Expected:** 10-20 attachment items (estimated based on 16 emails with attachments)

**Root Cause Analysis:**

1. **Binary data was not passed from "Combine Both Gmail Accounts"**
   - The Code node only returned JSON data
   - Binary attachments were dropped during the combine operation

2. **Secondary issue in Extract Attachment Info code:**
   The code looks for `email.payload.headers`, but Gmail node returns `email.headers` directly:
   ```javascript
   // Current (incorrect):
   const dateHeader = email.payload?.headers?.find(h => h.name === 'Date');
   const subjectHeader = email.payload?.headers?.find(h => h.name === 'Subject');

   // Should be:
   const dateHeader = email.headers?.find(h => h.name === 'Date');
   const subjectHeader = email.headers?.find(h => h.name === 'Subject');
   ```

**Workflow stopped here** - subsequent nodes were not executed because there were 0 items to process.

---

### Nodes Not Executed (Due to 0 Items from Extract Attachment Info)

#### Node 7: Download Attachment
- **Status:** NOT EXECUTED
- **Expected:** Download attachments from Gmail
- **Notes:** Skipped due to 0 input items

#### Node 8: Upload to Receipt Pool
- **Status:** NOT EXECUTED
- **Expected:** Upload files to Google Drive folder
- **Notes:** Skipped due to 0 input items

#### Node 9: Prepare Receipt Record
- **Status:** NOT EXECUTED
- **Expected:** Format data for Google Sheets
- **Notes:** Skipped due to 0 input items

#### Node 10: Log Receipt in Database
- **Status:** NOT EXECUTED
- **Expected:** Append rows to Google Sheets
- **Notes:** Skipped due to 0 input items

---

## Test Results vs Expectations

| Test Checkpoint | Expected | Actual | Status |
|----------------|----------|--------|--------|
| Gmail nodes execute successfully | Yes | Yes | PASS |
| Binary data includes `attachment_0`, `attachment_1` keys | Yes | Yes | PASS |
| Binary data preserved through "Combine Both Gmail Accounts" | Yes | No | FAIL |
| Extract Attachment Info outputs >0 items | Yes | No (0 items) | FAIL |
| Attachments uploaded to Google Drive | Yes | Not reached | FAIL |
| Receipts logged to Google Sheets | Yes | Not reached | FAIL |

---

## Key Findings

### What Worked
1. Gmail nodes successfully fetched email lists from both accounts
2. Gmail "Get Email Details" nodes with `downloadAttachments: true` successfully downloaded attachments as binary data
3. Binary data structure is correct: `attachment_0`, `attachment_1`, `attachment_2`, etc.
4. No credential errors or API failures

### What Failed
1. **"Combine Both Gmail Accounts" Code node does not preserve binary data**
   - Only JSON data is passed through
   - Binary attachments are lost in the combine operation

2. **"Extract Attachment Info" received 0 items with binary data**
   - Could not process any attachments
   - Workflow stopped here

3. **Secondary code issues in "Extract Attachment Info"**
   - Incorrect path to headers (`email.payload.headers` should be `email.headers`)
   - Would have caused failures even if binary data was present

---

## Required Fixes

### Priority 1: Fix "Combine Both Gmail Accounts" Node

**Current code (incorrect):**
```javascript
return {
  json: {
    ...email,
    vendorName: vendor ? vendor.name : 'Unknown Vendor',
    fromEmail: fromEmail
  }
};
```

**Fixed code:**
```javascript
return {
  json: {
    ...email,
    vendorName: vendor ? vendor.name : 'Unknown Vendor',
    fromEmail: fromEmail
  },
  binary: item.binary || {}  // PRESERVE BINARY DATA
};
```

### Priority 2: Fix "Extract Attachment Info" Node

**Current code (incorrect):**
```javascript
// Get email metadata
const dateHeader = email.payload?.headers?.find(h => h.name === 'Date');
const emailDate = dateHeader ? new Date(dateHeader.value) : new Date();

const subjectHeader = email.payload?.headers?.find(h => h.name === 'Subject');
const subject = subjectHeader ? subjectHeader.value : 'No Subject';
```

**Fixed code:**
```javascript
// Get email metadata - headers are at root level, not in payload
const dateHeader = email.headers?.find(h => h.name === 'Date');
const emailDate = dateHeader ? new Date(dateHeader.value) : new Date();

const subjectHeader = email.headers?.find(h => h.name === 'Subject');
const subject = subjectHeader ? subjectHeader.value : 'No Subject';
```

---

## Next Steps

1. **Update "Combine Both Gmail Accounts" node** to preserve binary data in return statement
2. **Update "Extract Attachment Info" node** to use correct header path (`email.headers` not `email.payload.headers`)
3. **Re-test workflow** after fixes to verify:
   - Binary data flows through combine operation
   - Attachments are extracted (expecting 10-20 items)
   - Files upload to Google Drive successfully
   - Receipt records are logged to Google Sheets
4. **Verify file count** in Google Drive Receipt Pool folder
5. **Verify row count** in Google Sheets Receipts tab

---

## Attachments Detected (But Not Processed)

Based on execution preview data:
- **Account 1:** 7 emails, estimated 10-14 attachments (2 attachment keys detected per sample)
- **Account 2:** 9 emails, estimated 12-18 attachments (3 attachment keys detected per sample)
- **Total estimated attachments:** 20-30 PDF/image files

None of these were processed due to the binary data preservation issue.

---

## Execution Performance

- **Workflow duration:** 16.3 seconds
- **Total nodes executed:** 8 of 13 nodes
- **Data processed:** 16 emails with attachments
- **Estimated data size:** 5.2 MB (5,157 KB)
- **Final status:** success (n8n perspective, but workflow incomplete)

---

## Recommendations

1. **Always preserve binary data in Code nodes** when working with attachments
2. **Add debug logging** to "Combine Both Gmail Accounts" to show binary data presence
3. **Add validation** in "Extract Attachment Info" to check if binary data exists before processing
4. **Consider splitting** "Combine Both Gmail Accounts" into two steps:
   - Step 1: Merge JSON data
   - Step 2: Preserve binary data in separate operation
5. **Add error handling** if no attachments are found (return empty array with warning)

---

## Conclusion

The Gmail node configuration with `downloadAttachments: true` is working correctly and successfully downloading attachments as binary data. However, the workflow fails at the "Combine Both Gmail Accounts" node because it does not preserve binary data when combining items from both accounts.

**Status:** FAIL - Critical issue prevents attachment processing

**Fix complexity:** Low - Single line change to preserve binary data, plus header path fix

**Estimated time to fix:** 5 minutes

**Retest required:** Yes - Full workflow execution after fixes applied
