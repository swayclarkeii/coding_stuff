# n8n Test Report - W2: Gmail Receipt Monitor (Binary Data Preservation)

## Test Execution Details

- **Workflow ID**: dHbwemg7hEB4vDmC
- **Workflow Name**: Expense System - Workflow 2: Gmail Receipt Monitor
- **Execution ID**: 613
- **Test Date**: 2026-01-08 15:38:27 UTC
- **Trigger Method**: Webhook (POST /test-expense-w2)
- **Duration**: 17.7 seconds
- **Final Status**: Partial Success (error at final node)

---

## Summary

- **Total Tests**: 1 (Full workflow execution)
- **Status**: ❌ FAILED (multiple issues found)
- **Critical Issues**: 3
- **Warnings**: 1

---

## Test Results

### Test 1: Binary Data Preservation Through Combine Node

**Status**: ⚠️ PARTIAL PASS

**n8n Execution Path**:
1. ✅ Test Trigger - Webhook → triggered successfully
2. ✅ Load Vendor Patterns → 13 vendor patterns loaded (17ms)
3. ⚠️ Search Gmail for Receipts (Account 1) → 7 emails found (4.4s)
4. ❌ Search Gmail for Receipts (Account 2) → FAILED (credential error)
5. ✅ Get Email Details (Account 1) → 7 emails retrieved with full data (1.8s)
6. ⚠️ Combine Both Gmail Accounts → 7 items combined (only Account 1, 58ms)
7. ❌ Extract Attachment Info → ERROR: "email.headers?.find is not a function [line 15]"
8. ✅ Download Attachment → 1 file downloaded despite error (1.2s)
9. ✅ Upload to Receipt Pool → 1 file uploaded to Drive (1ms)
10. ❌ Prepare Receipt Record → ERROR: "Cannot read properties of undefined (reading 'replace') [line 3]"
11. ❌ Log Receipt in Database → FAILED (upstream error prevented execution)

---

## Critical Issues Found

### Issue 1: Gmail Account 2 Credential Missing

**Node**: Search Gmail for Receipts (Account 2)
**Error**: `Credential with ID "VdNWQlkZQ0BxcEK2" does not exist for type "googleApi"`
**Impact**: Only 7 emails processed instead of expected 16 (7 Stripe + 9 Anthropic)
**Severity**: HIGH

**Expected**: 16 emails (both accounts)
**Actual**: 7 emails (Account 1 only)

**Root Cause**: The Google API credential assigned to Account 2 Gmail nodes has been deleted or is invalid.

**Recommendation**: Use browser-ops-agent to refresh OAuth credentials for Gmail Account 2.

---

### Issue 2: Extract Attachment Info - Data Structure Mismatch

**Node**: Extract Attachment Info
**Error**: `email.headers?.find is not a function [line 15]`
**Impact**: Failed to extract attachment metadata correctly
**Severity**: HIGH

**Code Issue**:
```javascript
// Line 15 attempts to use .find() on email.headers
const fromHeader = email.headers?.find(h => h.name.toLowerCase() === 'from');
```

**Root Cause**: After the fix to change `email.payload.headers` to `email.headers`, the data structure is different than expected. The `headers` field is likely not an array, or the email object structure changed from Gmail Get operation.

**Data Structure Investigation Needed**:
- The Gmail "Get Email" node returns a different structure than expected
- Need to verify actual output structure from "Get Email Details" node
- The fix assumed `email.headers` would be an array, but it appears to be a different type

**Recommendation**:
1. Check actual data structure from "Get Email Details" node output
2. Update "Extract Attachment Info" code to match actual structure
3. Verify if Gmail API returns headers as array vs object

---

### Issue 3: Prepare Receipt Record - Missing Data

**Node**: Prepare Receipt Record
**Error**: `Cannot read properties of undefined (reading 'replace') [line 3]`
**Impact**: Failed to prepare receipt data for logging
**Severity**: HIGH

**Code Issue**:
```javascript
// Line 3 attempts to call .replace() on an undefined property
// Likely trying to process vendor name or email address
```

**Root Cause**: Upstream error from "Extract Attachment Info" caused incomplete data to be passed downstream. The code expects certain fields (likely vendor name, email, or date) that are undefined due to the extraction error.

**Cascading Effect**: This error prevented "Log Receipt in Database" from executing.

**Recommendation**: Fix "Extract Attachment Info" first, then retest to see if this issue resolves.

---

### Issue 4: Binary Data Preservation Status

**Status**: ⚠️ UNABLE TO VERIFY FULLY

**What We Know**:
- ✅ "Combine Both Gmail Accounts" executed successfully (58ms)
- ✅ "Download Attachment" successfully downloaded 1 file (1.2s)
- ✅ "Upload to Receipt Pool" successfully uploaded 1 file to Google Drive
- ❌ Cannot verify if binary data was properly preserved through combine node due to extraction error

**Partial Success Indicators**:
1. The workflow did not crash at the combine node
2. At least 1 attachment was downloaded and uploaded
3. Binary data appeared to flow through the pipeline

**Concerns**:
- Only 1 attachment processed (expected 20-30)
- The single successful attachment might be coincidental
- Need to fix extraction logic and retest with correct data structure

---

## Attachment Processing Analysis

### Expected Results (from test plan):
- **Emails**: 16 total (7 Stripe + 9 Anthropic)
- **Attachments**: 20-30 PDF/image files
- **Drive Upload**: Files in folder 12SVQzuWtKva48LvdGbszg3UcKl7iy-1x
- **Sheet Logging**: Entries in Receipts sheet

### Actual Results:
- **Emails Found**: 7 (Account 1 only, Account 2 failed)
- **Attachments Extracted**: 1 (extraction error occurred)
- **Files Downloaded**: 1
- **Files Uploaded**: 1 (to correct Drive folder)
- **Sheet Entries**: 0 (logging failed)

### Processing Rate:
- **Expected**: ~2 attachments per email average
- **Actual**: 0.14 attachments per email (1 out of 7)
- **Success Rate**: 7% (critically low)

---

## Binary Data Preservation Test

### Fix Applied:
Changed "Combine Both Gmail Accounts" code to include:
```javascript
binary: item.binary || {}
```

### Test Result:
- ⚠️ **INCONCLUSIVE** - Cannot verify binary preservation due to extraction error
- The combine node did execute successfully
- Need to fix extraction logic and retest

### Next Steps for Verification:
1. Fix Gmail Account 2 credential issue
2. Fix "Extract Attachment Info" data structure handling
3. Rerun test to verify all 16 emails process correctly
4. Verify 20-30 attachments are found and processed
5. Verify binary data flows through all nodes
6. Verify Drive uploads complete
7. Verify Sheet logging succeeds

---

## Execution Timeline

| Node | Duration | Items In | Items Out | Status |
|------|----------|----------|-----------|--------|
| Test Trigger - Webhook | 0ms | - | 1 | ✅ Success |
| Load Vendor Patterns | 17ms | 1 | 13 | ✅ Success |
| Search Gmail (Account 1) | 4,371ms | 13 | 7 | ✅ Success |
| Search Gmail (Account 2) | - | 13 | 0 | ❌ Credential Error |
| Get Email Details (Acc 1) | 1,833ms | 7 | 7 | ✅ Success |
| Get Email Details (Acc 2) | - | 0 | 0 | ⚠️ Skipped |
| Combine Both Accounts | 58ms | 7 | 7 | ✅ Success |
| Extract Attachment Info | 32ms | 7 | 1 | ❌ Code Error |
| Download Attachment | 1,171ms | 1 | 1 | ✅ Success |
| Upload to Receipt Pool | 1ms | 1 | 1 | ✅ Success |
| Prepare Receipt Record | 22ms | 1 | 1 | ❌ Code Error |
| Log Receipt in Database | 3ms | 1 | 0 | ❌ Failed |

**Total Execution Time**: 17.7 seconds

---

## Required Fixes

### Priority 1: Gmail Account 2 Credentials
- **Action**: Refresh OAuth credentials for Gmail Account 2
- **Tool**: browser-ops-agent
- **Impact**: Will restore access to 9 Anthropic emails

### Priority 2: Fix Extract Attachment Info Data Structure
- **Action**: Investigate actual data structure from "Get Email Details" output
- **Action**: Update code to correctly parse headers (not as array)
- **Impact**: Will enable proper attachment extraction

### Priority 3: Test Prepare Receipt Record After Fix
- **Action**: Retest after fixing extraction logic
- **Action**: Verify all required fields are present
- **Impact**: Will enable Sheet logging

---

## Recommendations

1. **Immediate**: Fix Gmail Account 2 credential (use browser-ops-agent for OAuth refresh)
2. **Immediate**: Inspect actual output structure from "Get Email Details" node
3. **Immediate**: Update "Extract Attachment Info" to handle correct data structure
4. **After Fix**: Rerun full test to verify:
   - All 16 emails are found
   - 20-30 attachments are extracted
   - Binary data is preserved through combine
   - Files upload to Drive successfully
   - Sheet logging completes
5. **Future**: Add error handling in "Extract Attachment Info" to gracefully handle missing headers
6. **Future**: Add logging/debugging output to track binary data preservation explicitly

---

## Test Verdict

**OVERALL: ❌ FAILED**

### What Worked:
- ✅ Webhook trigger functioning
- ✅ Vendor pattern loading
- ✅ Gmail Account 1 search and retrieval
- ✅ Combine node executed without crashing
- ✅ At least 1 attachment downloaded and uploaded
- ✅ Drive upload target folder correct

### What Failed:
- ❌ Gmail Account 2 credential missing (50% of emails lost)
- ❌ Extract Attachment Info data structure mismatch (extraction failed)
- ❌ Prepare Receipt Record missing data (cascading error)
- ❌ Sheet logging prevented by upstream errors
- ❌ Only 1 of expected 20-30 attachments processed (7% success rate)

### Binary Data Preservation:
- ⚠️ **INCONCLUSIVE** - Cannot verify due to extraction errors
- The fix was applied, but testing blocked by other issues

---

## Next Test Requirements

Before declaring binary preservation fix successful, must verify:

1. ✅ Gmail Account 2 credentials restored
2. ✅ Extract Attachment Info correctly parses email structure
3. ✅ All 16 emails found (7 Stripe + 9 Anthropic)
4. ✅ 20-30 attachments extracted from emails
5. ✅ Binary data preserved through combine node
6. ✅ All attachments successfully downloaded
7. ✅ All files uploaded to Drive folder 12SVQzuWtKva48LvdGbszg3UcKl7iy-1x
8. ✅ All receipt entries logged to Google Sheets
9. ✅ Zero errors in execution
10. ✅ Manual verification of files in Drive
11. ✅ Manual verification of rows in Sheets

---

## Files Generated

- **Test Report**: `/Users/swayclarke/coding_stuff/tests/W2-binary-preservation-test-report.md`
- **Execution ID**: 613 (available in n8n UI for manual inspection)

---

## Appendix: Error Messages

### Extract Attachment Info Error
```
email.headers?.find is not a function [line 15]
```

### Prepare Receipt Record Error
```
Cannot read properties of undefined (reading 'replace') [line 3]
```

### Gmail Account 2 Credential Error
```
Credential with ID "VdNWQlkZQ0BxcEK2" does not exist for type "googleApi"
```

---

**Test Completed**: 2026-01-08 15:38:45 UTC
**Report Generated**: 2026-01-08 (test-runner-agent)
**Execution ID**: 613
**Workflow ID**: dHbwemg7hEB4vDmC
