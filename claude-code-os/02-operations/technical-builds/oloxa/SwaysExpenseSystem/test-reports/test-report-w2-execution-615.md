# n8n Test Report - Workflow W2 (Expense Automation)

## Summary
- Workflow ID: dHbwemg7hEB4vDmC
- Execution ID: 615
- Overall Status: SUCCESS (workflow completed without crashing)
- Total tests: 1 execution test
- Duration: 21.1 seconds
- Executed nodes: 4 of 12 nodes
- Total items processed: 62

## Test Result: FAILED - Binary Data Not Passed Through

The workflow executed successfully but the binary data handling is BROKEN.

---

## Detailed Analysis

### Node 1: Extract Attachment Info
- Status: SUCCESS
- Items output: 20 attachments
- Execution time: 26ms
- Binary structure: CORRECT

**Binary Data Structure (Correct):**
```json
{
  "json": {
    "messageId": "19b8b1062555e3aa",
    "vendorName": "Unknown Vendor",
    "emailDate": "2026-01-04",
    "emailSubject": "Your receipt from Anthropic, PBC #2124-7085-4982",
    "filename": "Invoice-3B639A71-0013.pdf",
    "mimeType": "application/pdf"
  },
  "binary": {
    "data": {
      "mimeType": "application/pdf",
      "fileType": "pdf",
      "fileExtension": "pdf",
      "data": "filesystem-v2",
      "fileName": "Invoice-3B639A71-0013.pdf",
      "id": "filesystem-v2:workflows/dHbwemg7hEB4vDmC/executions/615/binary_data/c47a4de8-6b72-4178-98c3-0946add46e12",
      "fileSize": "31.6 kB"
    }
  }
}
```

**Verdict:** This node is working correctly. Binary data structure is valid.

---

### Node 2: Download Attachment (Gmail node)
- Status: SUCCESS (but not doing what we expect)
- Items output: 20
- Execution time: 4.88 seconds
- Binary data: MISSING

**Problem:** The "Download Attachment" node is NOT downloading attachments. It's passing through the Gmail message JSON metadata without the binary data.

**Output Structure (Missing binary):**
```json
{
  "json": {
    "id": "19b8b1062555e3aa",
    "threadId": "19b8b1062555e3aa",
    "snippet": "Your receipt from Anthropic, PBC #2124-7085-4982...",
    "payload": {
      "mimeType": "multipart/mixed"
    },
    "sizeEstimate": 150716,
    "historyId": "11673046",
    "internalDate": "1767564665000",
    "labels": [...],
    "From": "\"Anthropic, PBC\" <invoice+statements@mail.anthropic.com>",
    "To": "swayclarkeii@gmail.com",
    "Subject": "Your receipt from Anthropic, PBC #2124-7085-4982"
  }
  // NO binary property!
}
```

**Verdict:** The binary data from "Extract Attachment Info" is being LOST. The Gmail "Download Attachment" node is not functioning correctly.

---

### Node 3: Upload to Receipt Pool (Google Drive Upload)
- Status: FAILED (as expected)
- Items output: 20 error messages
- Execution time: 3ms

**Error (all 20 items):**
```
"This operation expects the node's input data to contain a binary file 'data', but none was found [item 0]"
```

**Root Cause:** No binary data available because the previous node ("Download Attachment") didn't pass it through.

**Verdict:** This node is configured correctly. It's failing because upstream node is not providing binary data.

---

### Node 4: Log Receipt in Database (Google Sheets)
- Status: FAILED (credential issue)
- Items output: 2 error messages
- Execution time: 3ms

**Error:**
```
"Credential with ID \"VdNWQlkZQ0BxcEK2\" does not exist for type \"googleApi\"."
```

**Verdict:** Cannot test this node until credential is fixed. This is a known issue.

---

## Root Cause Analysis

The core issue is in the **"Download Attachment" node (Gmail node)**:

1. The "Extract Attachment Info" Code node correctly creates items with:
   - JSON metadata (messageId, vendorName, emailDate, etc.)
   - Binary data structure: `binary: { data: attachment }`

2. The "Download Attachment" Gmail node is configured to:
   - Operation: "Download Attachment"
   - Input data from previous node

3. **BUT**: The Gmail node is NOT preserving or downloading the binary data. Instead, it's:
   - Making a fresh Gmail API call to get message details
   - Returning only the message JSON metadata
   - Completely discarding the binary data from the previous node

4. This means the "Upload to Receipt Pool" node receives items with NO binary data, causing the error.

---

## Recommendation

The "Download Attachment" node needs to be reconfigured or replaced. Two possible solutions:

**Option A: Fix the Gmail node configuration**
- Check if the Gmail node has a setting to "preserve binary data" or "pass through input"
- Verify the Gmail node is actually downloading attachments, not just fetching message metadata

**Option B: Remove the Gmail node entirely**
- The "Extract Attachment Info" Code node already has the binary data
- We may not need a separate "Download Attachment" step
- The binary data is already available as `binary.data` with filesystem-v2 reference
- Try connecting "Extract Attachment Info" directly to "Upload to Receipt Pool"

**Option C: Different Gmail operation**
- Use Gmail "Get Attachment" operation instead of "Download Attachment"
- Provide the attachment ID from the previous node's output

---

## Next Steps

1. Investigate Gmail node configuration options
2. Check if Gmail node can preserve input binary data
3. Consider removing the Gmail "Download Attachment" node entirely
4. Test connecting "Extract Attachment Info" directly to "Upload to Receipt Pool"
5. Fix credential issue for "Log Receipt in Database" node

---

## Files Affected
- Workflow: W2 (dHbwemg7hEB4vDmC)
- Node: "Download Attachment" (Gmail node)
- Test report: /Users/swayclarke/coding_stuff/test-report-w2-execution-615.md
