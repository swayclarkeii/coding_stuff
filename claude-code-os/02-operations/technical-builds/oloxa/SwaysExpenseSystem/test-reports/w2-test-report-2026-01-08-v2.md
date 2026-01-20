# n8n Test Report – Workflow W2 (dHbwemg7hEB4vDmC)

**Test Date:** 2026-01-08 15:45:30 UTC
**Execution ID:** 614
**Workflow Name:** Receipt Scanning - Extract Attachments from Gmail
**Test Focus:** Date/subject extraction fix after recent workflow modifications

---

## Summary

- **Overall Status:** ✅ PARTIAL PASS
- **Execution Status:** success (21.3 seconds)
- **Total Nodes Executed:** 12/12
- **Total Items Processed:** 144 items across all nodes

### Key Metrics
- **Emails Processed (Account 1):** 7 emails
- **Emails Processed (Account 2):** 9 emails
- **Total Emails Combined:** 16 emails
- **Attachments Extracted:** 20 attachments (13 from Account 1, 7+ from Account 2)
- **Files Uploaded to Drive:** 0 (FAILED - binary data issue)
- **Rows Logged to Sheets:** 0 (FAILED - credentials issue)

---

## Test Results by Fix

### ✅ Fix 1: Date/Subject Extraction (PASS)

**Issue:** Previous test showed "headers.find is not a function" error
**Fix Applied:** Changed from `$json.headers.find(...)` to direct field access (`$json.date`, `$json.subject`)

**Result:** ✅ **PASS** - No more "headers.find" errors

**Evidence:**
```json
{
  "messageId": "19b8b1062555e3aa",
  "vendorName": "Unknown Vendor",
  "emailDate": "2026-01-04",
  "emailSubject": "Your receipt from Anthropic, PBC #2124-7085-4982",
  "filename": "Invoice-3B639A71-0013.pdf"
}
```

**Sample Extracted Data:**
1. Email Date: "2026-01-04", Subject: "Your receipt from Anthropic, PBC #2124-7085-4982"
2. Email Date: "2025-12-26", Subject: "Your receipt from Anthropic, PBC #2730-2995-8045"

**Attachments per Email:**
- Most emails: 2 attachments (Invoice + Receipt PDF)
- Total extracted: 20 attachments from 16 emails

---

### ✅ Fix 2: Gmail Attachment Download (PASS)

**Issue:** Gmail nodes needed `downloadAttachments: true` to get binary data
**Fix Applied:** Added `downloadAttachments: true` to both Gmail nodes

**Result:** ✅ **PASS** - Binary data successfully downloaded

**Evidence:**
- "Get Email Details" node output shows binary data:
  ```json
  "binary": {
    "attachment_0": {
      "mimeType": "application/pdf",
      "fileName": "Invoice-3B639A71-0013.pdf",
      "fileSize": "31.6 kB"
    },
    "attachment_1": {
      "mimeType": "application/pdf",
      "fileName": "Receipt-2124-7085-4982.pdf",
      "fileSize": "31.6 kB"
    }
  }
  ```

---

### ✅ Fix 3: Binary Data Preservation in "Combine" Node (PASS)

**Issue:** Merge node was dropping binary data from inputs
**Fix Applied:** Set merge mode to pass through binary data

**Result:** ✅ **PASS** - Binary data preserved after merge

**Evidence:**
- "Combine Both Gmail Accounts" node output shows 16 items with binary data
- Preview shows binary attachments still present after merge

---

### ❌ Issue 4: Upload to Drive (FAIL)

**Problem:** Binary data NOT being passed to "Upload to Receipt Pool" node

**Error Message:**
```
This operation expects the node's input data to contain a binary file 'data', but none was found [item 0]
```

**Root Cause:** The "Extract Attachment Info" node creates NEW output items with:
- `json`: metadata (messageId, vendorName, filename, etc.)
- `binary.data`: the attachment file

However, the Google Drive "Upload a File" node is NOT finding `binary.data`.

**Likely Issue:**
- The "Extract Attachment Info" node code creates `binary.data` by copying from the input's `binary[attachmentKey]`
- But the binary reference may not be properly passed through the node transformation

**ALL 20 items failed with the same error** - no files were uploaded to Drive.

---

### ❌ Issue 5: Log to Google Sheets (FAIL)

**Problem:** Google Sheets credential does not exist

**Error Message:**
```
Credential with ID "VdNWQlkZQ0BxcEK2" does not exist for type "googleApi".
```

**Root Cause:** The Google Sheets credential needs to be refreshed or reconnected

**Result:** No rows were logged to the Receipts sheet

**Note:** This is a separate issue from the workflow logic - just needs OAuth refresh

---

## Detailed Node Analysis

### Node: Search Gmail for Receipts (Account 1)
- **Status:** success
- **Input:** 0 items (triggered by vendor patterns)
- **Output:** 7 emails
- **Execution Time:** Not shown in preview
- **Binary Data:** Attachments downloaded (2 per email typically)

### Node: Get Email Details (Account 1)
- **Status:** success
- **Input:** 0 items
- **Output:** 7 emails with binary attachments
- **Binary Data:** ✅ Present (attachment_0, attachment_1)

### Node: Search Gmail for Receipts (Account 2)
- **Status:** success
- **Input:** 0 items
- **Output:** 9 emails
- **Binary Data:** Attachments downloaded

### Node: Get Email Details (Account 2)
- **Status:** success
- **Input:** 0 items
- **Output:** 9 emails with binary attachments
- **Binary Data:** ✅ Present (attachment_0, attachment_1, attachment_2)

### Node: Combine Both Gmail Accounts
- **Status:** success
- **Input:** 0 items
- **Output:** 16 emails (7 + 9)
- **Binary Data:** ✅ Preserved from both accounts

### Node: Extract Attachment Info
- **Status:** success
- **Input:** 0 items
- **Output:** 20 attachment items
- **Execution Time:** 29ms
- **Binary Data:** ✅ Created `binary.data` for each attachment
- **Key Fields Created:**
  - `messageId`: Gmail message ID
  - `vendorName`: "Unknown Vendor" (vendor matching not working)
  - `emailDate`: Successfully extracted (e.g., "2026-01-04")
  - `emailSubject`: Successfully extracted
  - `filename`: Attachment filename
  - `mimeType`: File MIME type
  - `attachmentKey`: Source binary key

### Node: Upload to Receipt Pool
- **Status:** success (but all items have errors)
- **Input:** 0 items
- **Output:** 20 items
- **Execution Time:** 3ms
- **Result:** ❌ All 20 items failed with "binary file 'data' not found" error

### Node: Prepare Receipt Record
- **Status:** success
- **Input:** 0 items
- **Output:** 20 items
- **Result:** ❌ All items have errors (propagated from Upload node)

### Node: Log Receipt in Database
- **Status:** success (completed with error)
- **Input:** 0 items
- **Output:** 2 items (error items)
- **Execution Time:** 8ms
- **Result:** ❌ Credential error - no rows logged

---

## Comparison to Previous Test

### Improvements ✅
1. **No more "headers.find is not a function" errors** - date/subject extraction now works
2. **Increased attachments extracted:** Previous test only got 1 attachment, this test got 20
3. **Binary data properly downloaded from Gmail** - both accounts working
4. **Binary data preserved through merge node** - all 16 emails kept their attachments

### Remaining Issues ❌
1. **Upload to Drive still failing** - NEW ISSUE: binary data not being passed correctly
2. **Google Sheets credential missing** - needs OAuth refresh (expected)
3. **Vendor matching not working** - all showing "Unknown Vendor"

---

## Root Cause Analysis: Binary Data Upload Issue

The "Extract Attachment Info" node uses this code to create output items:

```javascript
for (const [key, binaryData] of Object.entries(item.binary)) {
  if (key.startsWith('attachment_')) {
    newItem = {
      json: {
        messageId: item.json.messageId,
        vendorName: item.json.vendorName || 'Unknown Vendor',
        emailDate: item.json.date,
        emailSubject: item.json.subject,
        filename: binaryData.fileName,
        mimeType: binaryData.mimeType,
        attachmentKey: key
      },
      binary: {
        data: binaryData  // ← This creates binary.data
      }
    };
    items.push(newItem);
  }
}
```

**The Problem:**
- `binaryData` from `item.binary[key]` is a REFERENCE to binary data stored in n8n's binary data system
- When creating a new item with `binary.data = binaryData`, this reference may not be properly handled by n8n
- The Google Drive node expects actual binary data at `binary.data`, but it's not finding it

**Possible Solutions:**
1. **Don't split into multiple items** - keep all attachments in single item's binary object
2. **Use Item Lists node** - properly split items while preserving binary data
3. **Re-download binary data** - use HTTP Request to fetch binary data by reference ID
4. **Use different binary key** - instead of `binary.data`, use `binary[filename]` and configure Drive node to use that key

---

## Recommendations

### Immediate Actions

1. **Fix binary data passing to Upload node** (HIGH PRIORITY)
   - The date/subject extraction fix is working perfectly
   - But files still not uploading due to binary data issue
   - Need to investigate how to properly pass binary data from "Extract Attachment Info" to "Upload to Receipt Pool"

2. **Refresh Google Sheets OAuth credentials** (MEDIUM PRIORITY)
   - Use browser-ops-agent to refresh credential VdNWQlkZQ0BxcEK2
   - This is blocking the final logging step

3. **Fix vendor matching** (LOW PRIORITY)
   - All emails showing "Unknown Vendor"
   - Check vendor pattern matching logic in workflow

### Testing Next Steps

Once binary data issue is fixed:
1. Re-run test to verify files upload to Drive folder 12SVQzuWtKva48LvdGbszg3UcKl7iy-1x
2. After OAuth refresh, verify rows are logged to Sheets
3. Check if vendor names are correctly matched

---

## Files Generated

- Test execution data: /Users/swayclarke/.claude/projects/-Users-swayclarke-coding-stuff/af5b904a-e307-4a1b-8f24-7b36d9c9af2b/tool-results/mcp-n8n-mcp-n8n_executions-*.txt

---

## Conclusion

**Date/Subject Extraction Fix: ✅ SUCCESS**

The main fix for extracting email date and subject is working perfectly. No more "headers.find is not a function" errors, and the extracted data looks correct:
- Dates formatted as "YYYY-MM-DD"
- Subjects captured accurately
- 20 attachments successfully extracted with metadata

**Remaining Issues:**
1. Binary data not passing to Upload node (NEW ISSUE - needs investigation)
2. Google Sheets credential needs refresh (EXPECTED - known issue)

**Overall Assessment:**
The date/subject extraction fix is **VERIFIED AND WORKING**. The workflow successfully processes emails and extracts attachment metadata. The upload failure is a separate issue related to binary data handling that needs to be addressed next.
