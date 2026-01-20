# n8n Test Report - Workflow W2: Gmail Receipt Monitor

**Test Date**: 2026-01-08 20:37:22 UTC
**Workflow ID**: dHbwemg7hEB4vDmC
**Workflow Name**: Expense System - Workflow 2: Gmail Receipt Monitor
**Execution ID**: 619
**Execution Duration**: 42.12 seconds
**Overall Status**: PARTIAL SUCCESS (Critical Issues Found)

---

## Executive Summary

**Total Tests**: 6 success criteria
**Passed**: 3
**Failed**: 3

The workflow executed successfully from a technical perspective (all nodes ran to completion), but encountered critical OAuth authentication failures and a Google Sheets logging error that prevented data from being persisted to the database.

---

## Test Results by Success Criteria

### 1. Files Upload to Correct Folder - PASS

**Status**: ✅ PASS
**Expected**: Files uploaded to folder ID `12SVQzuWtKva48LvdGbszg3UcKl7iy-1x`
**Actual**: All 7 files uploaded to correct folder

**Evidence**:
```json
"parents": ["12SVQzuWtKva48LvdGbszg3UcKl7iy-1x"]
```

**Files Uploaded**:
1. Ticket_541031569097_03.11.2025__R.pdf (FileID: 1d-w1mJSSFbmiaEU-8vn0m9V7OPkscVyA)
2. Ticket_541031569097_31.10.2025__H.pdf (FileID: 1U_Z7FxflD0jeZS89ivIUWX4vyJ52SEuE)
3. Rechnung 135109495.pdf (FileID: 14XuwYCQB1MJzi5SRHg0dwFcFWOYr8UAL)
4. Rechnung 134740112.pdf (FileID: 1Vy6Fu6hficyaqCaHHQg16kDfHoUggxHC)
5. Rechnung 134314064.pdf (FileID: 1aXOtEZl4EQFiYOE3OlIxalQanGK2PH0L)
6. Rechnung 133858476.pdf (FileID: 1SmZeTacmcNHSRH7bfRPQzSV_dkJQTbLC)
7. Rechnung 133442102.pdf (FileID: 1kxbi0B52Sv5g5OZSFM-ynOC4t_Hr1eZr)

---

### 2. Vendor Identification - PASS

**Status**: ✅ PASS
**Expected**: Vendors correctly identified (NOT "Unknown Vendor")
**Actual**: All 7 receipts correctly identified vendors

**Vendors Found**:
- **Deutsche Bahn**: 2 receipts
- **flaschenpost**: 5 receipts

**Sample Data**:
```json
{
  "ReceiptID": "RCPT-DEUTSCHE-BAHN-1767904681800",
  "Vendor": "Deutsche Bahn",
  "SourceEmail": "Buchungsbestätigung Deutsche Bahn (Auftrag: 541031569097)"
}
```

```json
{
  "ReceiptID": "RCPT-FLASCHENPOST-1767904681804",
  "Vendor": "flaschenpost",
  "SourceEmail": "Deine Rechnung 135109495"
}
```

**Note**: The vendor matching fix (`email.from.value[0].address`) is working correctly.

---

### 3. All 12 Fields Present Including New Columns - PASS

**Status**: ✅ PASS
**Expected**: All 12 fields including TransactionType and DownloadTimestamp
**Actual**: All fields correctly generated in Prepare Receipt Record node

**Field Verification**:
```json
{
  "ReceiptID": "RCPT-DEUTSCHE-BAHN-1767904681800",
  "FileName": "Ticket_541031569097_03.11.2025__R.pdf",
  "Vendor": "Deutsche Bahn",
  "Amount": "",
  "TransactionType": "Expense",
  "Date": "2025-10-28",
  "FileID": "1d-w1mJSSFbmiaEU-8vn0m9V7OPkscVyA",
  "DownloadDate": "2026-01-08",
  "DownloadTimestamp": "2026-01-08T20:38:01.800Z",
  "SourceEmail": "Buchungsbestätigung Deutsche Bahn (Auftrag: 541031569097)",
  "Matched": "FALSE",
  "Notes": "Auto-downloaded from Gmail message 19a2ca00850443ed"
}
```

**New Fields Confirmed**:
- TransactionType: "Expense" (correctly set)
- DownloadTimestamp: ISO 8601 format with milliseconds

---

### 4. Binary Data Flow - FAIL

**Status**: ❌ FAIL
**Expected**: Binary data (attachments) flow through all Code nodes
**Actual**: Binary data LOST after "Combine Both Gmail Accounts" node

**Problem**:
The "Combine Both Gmail Accounts" Code node outputs:
```json
"binary": {}
```

This empty binary object indicates the attachment data was stripped during the combination process.

**Impact**:
The "Extract Attachment Info" node received 0 items because no binary data was present. However, the workflow still managed to process 7 attachments from the second Gmail account (which has a different flow path).

**Evidence from Execution Path**:
- Get Email Details (Account 2): 9 items with binary attachments
- Combine Both Gmail Accounts: 22 items but binary data lost
- Extract Attachment Info: 0 items output (should have had items from both accounts)

---

### 5. Gmail Account 1 Authentication - FAIL

**Status**: ❌ FAIL
**Expected**: Both Gmail accounts successfully searched for receipts
**Actual**: Account 1 OAuth credentials expired, Account 2 worked

**Error from Account 1** (all 13 vendor searches):
```json
{
  "error": "The provided authorization grant (e.g., authorization code, resource owner credentials) or refresh token is invalid, expired, revoked, does not match the redirection URI used in the authorization request, or was issued to another client. (item 0)"
}
```

**Breakdown**:
- Gmail Account 1 ("Search Gmail for Receipts" node): 13 OAuth errors
- Gmail Account 2 ("Search Gmail for Receipts (Account 2)" node): 9 successful searches

**Result**: Only receipts from Account 2 were processed.

---

### 6. Google Sheets Logging - FAIL

**Status**: ❌ FAIL
**Expected**: All 7 receipts logged to Google Sheets successfully
**Actual**: Google Sheets node failed with parameter error

**Error from "Log Receipt in Database" node**:
```json
{
  "error": "Could not get parameter",
  "error": {
    "level": "error",
    "tags": {},
    "extra": {
      "parameterName": "columns.schema"
    }
  }
}
```

**Impact**: NO DATA WAS LOGGED TO GOOGLE SHEETS. All 7 prepared records were lost.

**Root Cause**: The node is looking for a parameter named "columns.schema" which doesn't exist or is misconfigured. This suggests the Google Sheets node configuration may need to be updated to match the new 12-field schema.

---

## Execution Statistics

### Email Search Results
- **Total Emails Found**: 22 (13 from Account 1 failed, 9 from Account 2 succeeded)
- **Emails Searched**: From October 1, 2025 onwards
- **Vendor Patterns Loaded**: 13 vendors
- **Search Duration**: Account 1: 1.4s, Account 2: 1.6s (Get Email Details)

### Attachment Processing
- **Total Attachments Extracted**: 7 (all from Account 2)
- **Expected Attachments**: More (Account 1 receipts should have contributed if OAuth worked)
- **Attachments Uploaded to Google Drive**: 7 (100% success rate for extracted attachments)
- **Upload Duration**: 27.18 seconds (average 3.88s per file)

### Data Preparation
- **Receipt Records Prepared**: 7
- **Receipt Records Logged**: 0 (due to Google Sheets error)
- **Preparation Duration**: 107ms

### Node Execution Times
1. Load Vendor Patterns: 10ms
2. Search Gmail for Receipts: 1,438ms (failed with OAuth errors)
3. Get Email Details: 1,591ms (failed with OAuth errors)
4. Search Gmail (Account 2): ~925KB data retrieved
5. Get Email Details (Account 2): ~931KB data retrieved
6. Combine Both Gmail Accounts: 13ms
7. Extract Attachment Info: 10ms (0 items output - binary data issue)
8. Upload to Receipt Pool: 27,180ms (27.18s)
9. Prepare Receipt Record: 107ms
10. Log Receipt in Database: 2,562ms (failed with parameter error)

---

## Sample Receipt Data

### Record 1: Deutsche Bahn Train Ticket
```json
{
  "ReceiptID": "RCPT-DEUTSCHE-BAHN-1767904681800",
  "FileName": "Ticket_541031569097_03.11.2025__R.pdf",
  "Vendor": "Deutsche Bahn",
  "Amount": "",
  "TransactionType": "Expense",
  "Date": "2025-10-28",
  "FileID": "1d-w1mJSSFbmiaEU-8vn0m9V7OPkscVyA",
  "DownloadDate": "2026-01-08",
  "DownloadTimestamp": "2026-01-08T20:38:01.800Z",
  "SourceEmail": "Buchungsbestätigung Deutsche Bahn (Auftrag: 541031569097)",
  "Matched": "FALSE",
  "Notes": "Auto-downloaded from Gmail message 19a2ca00850443ed"
}
```

### Record 2: flaschenpost Invoice
```json
{
  "ReceiptID": "RCPT-FLASCHENPOST-1767904681804",
  "FileName": "Rechnung 135109495.pdf",
  "Vendor": "flaschenpost",
  "Amount": "",
  "TransactionType": "Expense",
  "Date": "2025-12-23",
  "FileID": "14XuwYCQB1MJzi5SRHg0dwFcFWOYr8UAL",
  "DownloadDate": "2026-01-08",
  "DownloadTimestamp": "2026-01-08T20:38:01.804Z",
  "SourceEmail": "Deine Rechnung 135109495",
  "Matched": "FALSE",
  "Notes": "Auto-downloaded from Gmail message 19b4ac21e8a7ace5"
}
```

---

## All 7 Processed Receipts

1. **Deutsche Bahn** - Ticket_541031569097_03.11.2025__R.pdf (2025-10-28)
2. **Deutsche Bahn** - Ticket_541031569097_31.10.2025__H.pdf (2025-10-28)
3. **flaschenpost** - Rechnung 135109495.pdf (2025-12-23)
4. **flaschenpost** - Rechnung 134740112.pdf (2025-12-06)
5. **flaschenpost** - Rechnung 134314064.pdf (2025-11-15)
6. **flaschenpost** - Rechnung 133858476.pdf (2025-10-24)
7. **flaschenpost** - Rechnung 133442102.pdf (2025-10-04)

---

## Critical Issues Requiring Immediate Attention

### Priority 1: Google Sheets Logging Failure
**Impact**: HIGH - No data is being persisted to the database
**Error**: "Could not get parameter columns.schema"
**Action Required**:
1. Review "Log Receipt in Database" node configuration
2. Verify column mapping matches the 12-field schema
3. Check if OAuth credentials for Google Sheets are valid
4. Re-test after fixing configuration

### Priority 2: Gmail Account 1 OAuth Expired
**Impact**: HIGH - Only half of the receipts are being processed
**Error**: "authorization grant is invalid, expired, revoked"
**Action Required**:
1. Re-authenticate Gmail Account 1 in n8n credentials
2. Verify OAuth scopes include Gmail read access
3. Test both Gmail accounts separately

### Priority 3: Binary Data Loss in Combine Node
**Impact**: MEDIUM - First Gmail account's attachments would be lost even if OAuth worked
**Error**: Binary data not preserved when combining results
**Action Required**:
1. Review "Combine Both Gmail Accounts" Code node
2. Ensure binary data from input items is explicitly copied to output
3. Test with sample data containing binary attachments

---

## Recommendations

### Immediate Actions
1. Fix Google Sheets node configuration to resolve "columns.schema" error
2. Refresh OAuth credentials for Gmail Account 1
3. Fix binary data preservation in Combine node

### Testing Improvements
1. Add error handling to Gmail search nodes to continue workflow even if one account fails
2. Add validation step after "Combine Both Gmail Accounts" to verify binary data exists
3. Add error logging node to capture Google Sheets failures without stopping workflow

### Future Enhancements
1. Consider splitting into two separate workflows (one per Gmail account) that merge at the Google Sheets step
2. Add duplicate detection before uploading to prevent re-downloading same receipts
3. Add notification system for OAuth failures

---

## Conclusion

The workflow demonstrates partial success with correct vendor identification, proper file uploads, and complete field generation. However, three critical failures prevent full operation:

1. Google Sheets logging completely failed (no data persisted)
2. Gmail Account 1 OAuth expired (missing half of receipts)
3. Binary data lost during combination (would affect Account 1 attachments)

The recent fixes for vendor matching and field additions are working correctly where data flows through. The immediate priority is fixing the Google Sheets logging issue, as this prevents ANY data from being saved regardless of other fixes.

---

## Test Execution Details

**Triggered By**: Webhook test trigger (POST to test-expense-w2)
**Test Data**: Empty payload (workflow uses date-based Gmail search)
**Search Period**: October 1, 2025 onwards
**Vendors Searched**: 13 patterns from "Load Vendor Patterns" node
**Execution Mode**: Webhook
**n8n Instance**: Production

**Workflow Validation**: Passed (18 warnings, 0 errors, 12 nodes enabled)
