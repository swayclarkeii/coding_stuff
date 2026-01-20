# n8n Test Report - W2: Gmail Receipt Monitor

**Workflow ID**: dHbwemg7hEB4vDmC
**Test Date**: 2026-01-08 14:58:34 UTC
**Execution ID**: 608
**Date Range Tested**: After October 1, 2025 (updated from "last 7 days")

---

## Summary

- **Overall Status**: FAIL - Workflow found emails but failed to process attachments
- **Total Execution Time**: 21 seconds
- **Emails Found**: 16 total (7 from Account 1, 9 from Account 2)
- **Attachments Processed**: 0 (CRITICAL ISSUE)
- **Files Uploaded to Google Drive**: 0
- **Records Logged to Receipts Sheet**: 0

---

## Test Results by Vendor

### Anthropic
- **Emails Found (Account 1)**: 7
  - All emails had `mimeType: "multipart/mixed"` (indicates attachments present)
  - Emails included:
    - Receipt #2124-7085-4982 (Jan 2026)
    - Receipt #2730-2995-8045 (Dec 2025)
    - Receipt #2763-1795-2113 (Nov 2025)
    - Refund #3660-8865 (Nov 2025)
    - Receipt #2725-6584-7502 (Oct 2025)
    - Plus 2 more
- **Emails Found (Account 2)**: 9
  - All emails had attachments
- **Total Anthropic Emails**: 16
- **Expected Attachments**: 16 PDFs
- **Attachments Actually Processed**: 0

### Other Vendors
- **OpenAI**: 0 emails found
- **AWS**: 0 emails found
- **Stripe**: Not searched (likely in vendor patterns but no results)
- **Other vendors**: Not searched or no results

---

## Workflow Execution Flow

### Successful Nodes

1. **Test Trigger - Webhook**: Executed (1 item)
2. **Load Vendor Patterns**: Executed (13 vendor patterns loaded)
   - Search query format confirmed: `after:2025/10/01` (correct)
3. **Search Gmail for Receipts (Account 1)**: Executed (7 emails found)
4. **Get Email Details (Account 1)**: Executed (7 items processed)
5. **Search Gmail for Receipts (Account 2)**: Executed (9 emails found)
6. **Get Email Details (Account 2)**: Executed (9 items processed)
7. **Combine Both Gmail Accounts**: Executed (16 items combined)

### Failed/Empty Nodes

8. **Extract Attachment Info**: CRITICAL FAILURE
   - **Input**: 16 items (all with attachments)
   - **Output**: 0 items
   - **Status**: Success (but produced no output)
   - **Root Cause**: This Code node failed to extract attachment metadata from the email payload

9. **Download Attachment**: Not executed (0 input items)
10. **Upload to Receipt Pool**: Not executed (0 input items)
11. **Prepare Receipt Record**: Not executed (0 input items)
12. **Log Receipt in Database**: Not executed (0 input items)

---

## Critical Issue: Extract Attachment Info Node

**Problem**: The "Extract Attachment Info" Code node received 16 emails with attachments but output 0 items.

**Impact**:
- No attachments were downloaded
- No files were uploaded to Google Drive
- No records were logged in the Receipts sheet
- The entire downstream workflow (download → upload → log) was skipped

**Likely Causes**:
1. The code is looking for attachment data in the wrong location in the Gmail API response
2. The Gmail "Get Email Details" node may not be fetching attachment metadata (missing `format` parameter)
3. The code may be filtering out all attachments due to incorrect logic
4. The payload structure may have changed and the code expects a different format

**Recommendation**:
- Inspect the "Extract Attachment Info" Code node logic
- Verify the Gmail "Get Email Details" nodes are using `format: "full"` or `format: "metadata"` to include attachment data
- Check if the code is correctly parsing `payload.parts` for attachments

---

## Comparison to Previous Test

### Previous Test (Date Range: "last 7 days" / after 2026-01-01)
- **Emails Found**: Not documented in previous report
- **Issue**: Same problem - Extract Attachment Info produced 0 outputs

### Current Test (Date Range: "after October 1, 2025")
- **Emails Found**: 16 (significant increase due to 4-month date range)
- **Issue**: Same problem persists - Extract Attachment Info still produces 0 outputs

**Conclusion**: Expanding the date range successfully found more emails (as expected), but the core issue with attachment extraction remains unresolved. The problem is NOT with the date range or Gmail search - it's with the attachment processing logic.

---

## Email Breakdown by Date

Based on sample data from execution:

| Date | Vendor | Receipt Number | Account | Status |
|------|--------|---------------|---------|--------|
| 2026-01-04 | Anthropic | #2124-7085-4982 | Account 1 | Found, not processed |
| 2025-12-26 | Anthropic | #2730-2995-8045 | Account 1 | Found, not processed |
| 2025-11-26 | Anthropic | #2763-1795-2113 | Account 1 | Found, not processed |
| 2025-11-26 | Anthropic | Refund #3660-8865 | Account 1 | Found, not processed |
| 2025-10-31 | Anthropic | #2725-6584-7502 | Account 1 | Found, not processed |
| + 11 more emails | Anthropic | Various | Both accounts | Found, not processed |

---

## Test Status: FAIL

**Reason**: While the workflow successfully searched Gmail and found 16 receipts with attachments from October 2025 onwards (as expected), it completely failed to process any attachments. The "Extract Attachment Info" node is broken and outputs 0 items despite receiving 16 emails with attachments.

**Next Steps**:
1. Inspect and fix the "Extract Attachment Info" Code node
2. Verify Gmail "Get Email Details" nodes are fetching full email data including attachment metadata
3. Re-test after fixes to confirm end-to-end flow (find → extract → download → upload → log)

---

## Technical Details

- **n8n Execution ID**: 608
- **Workflow ID**: dHbwemg7hEB4vDmC
- **Execution Mode**: webhook (test trigger)
- **Total Nodes in Workflow**: 13
- **Nodes Executed**: 8
- **Nodes Skipped**: 5 (due to 0 input from Extract Attachment Info)
- **Estimated Data Size**: 1,765 KB (large due to email HTML content)
