# W2 Gmail Receipt Monitor - Test Execution Report

**Workflow ID:** dHbwemg7hEB4vDmC
**Workflow Name:** Expense System - Workflow 2: Gmail Receipt Monitor
**Test Date:** 2026-01-07
**Test Method:** Analyzed recent scheduled executions (last 5 runs)
**Status:** CRITICAL ISSUES FOUND

---

## Executive Summary

- **Total Tests:** 5 recent executions analyzed
- **Passed:** 4 (no emails found, so no further processing)
- **Failed:** 1 (execution #32 on Jan 2, 2026)
- **Critical Issues:** 3 blocking problems identified

---

## Test Results

### Execution #481 (Jan 6, 2026) - PASS (Empty Result)
- **Status:** Success
- **Duration:** 1.2 seconds
- **Emails Found:** 0
- **Vendors Searched:** 6 (OLD vendor list, not 25)
- **Notes:** Workflow stopped after Gmail search found no matching emails

### Execution #436 (Jan 5, 2026) - PASS (Empty Result)
- **Status:** Success
- **Emails Found:** 0
- **Vendors Searched:** 6

### Execution #299 (Jan 4, 2026) - PASS (Empty Result)
- **Status:** Success
- **Emails Found:** 0
- **Vendors Searched:** 6

### Execution #152 (Jan 3, 2026) - PASS (Empty Result)
- **Status:** Success
- **Emails Found:** 0
- **Vendors Searched:** 6

### Execution #32 (Jan 2, 2026) - FAIL
- **Status:** Error
- **Duration:** 1.2 seconds
- **Failed Node:** "Get Email Details"
- **Error Message:** "Bad request - please check your parameters (item 0)"
- **Root Cause:** Invalid id value - Gmail API received empty/invalid message ID
- **Emails Found by Search:** 6 emails matched
- **Upstream Node:** "Search Gmail for Receipts" output had invalid structure
- **Notes:** This is the ONLY execution that found emails, and it crashed

---

## Critical Issues Identified

### 1. BROKEN VENDOR LIST (CRITICAL)

**Problem:** Workflow is using OLD vendor list with only 6 vendors instead of the updated 25 vendors.

**Evidence:**
- Execution logs show only 6 items output from "Load Vendor Patterns"
- Current code in workflow contains 25 vendors
- But active version shows search queries for only 6: OpenAI, Anthropic, AWS, Google Cloud, GitHub, Oura Ring

**Impact:**
- Missing 19 vendors: Spotify, Audible, NYT, NinjaTrader, ScoreApp, WebinarJam, AAA Accelerator, Kling AI, Amazon, Wolt, Coffee Circle, Flaschenpost, MILES Mobility, Deutsche Bahn, Facebook Ads, Telefonica, Continentale, Barmenia
- No receipts captured from these vendors

**Root Cause:** The workflow's active version is out of sync with the current code version. The code shows 25 vendors, but the ACTIVE version being executed only has 6.

---

### 2. MISSING SEARCH QUERY FIELD (CRITICAL)

**Problem:** "Load Vendor Patterns" node outputs `emailPattern` and `searchParams`, but "Search Gmail for Receipts" expects `searchQuery`.

**Evidence from execution #481:**
```json
{
  "vendorName": "OpenAI",
  "searchQuery": "from:noreply@openai.com has:attachment after:2025/12/30 before:2026/01/06",
  "startDate": "2025/12/30",
  "endDate": "2026/01/06"
}
```

**Current code in workflow:**
```javascript
return vendors.map(vendor => ({
  json: {
    vendorName: vendor.name,
    emailPattern: vendor.emailPattern,  // Wrong field name!
    searchParams: searchParams           // Wrong structure!
  }
}));
```

**Should be:**
```javascript
const startDate = new Date(Date.now() - (7 * 24 * 60 * 60 * 1000));
const endDate = new Date();

return vendors.map(vendor => ({
  json: {
    vendorName: vendor.name,
    searchQuery: `${vendor.emailPattern} has:attachment after:${formatDate(startDate)} before:${formatDate(endDate)}`,
    startDate: formatDate(startDate),
    endDate: formatDate(endDate)
  }
}));
```

**Impact:** When search returns results, the workflow cannot process them properly.

---

### 3. SECOND GMAIL ACCOUNT NOT CONFIGURED (CRITICAL)

**Problem:** The workflow has placeholder credentials for the second Gmail account.

**Evidence:**
```json
"credentials": {
  "gmailOAuth2": {
    "id": "TBD_SWAYFROMTHEHOOK",
    "name": "Gmail account (swayfromthehook)"
  }
}
```

**Impact:**
- Only searching swayclarke@gmail.com
- NOT searching swayfromthehook@gmail.com
- Missing 50% of potential receipts

**Required Action:** Set up OAuth credentials for swayfromthehook@gmail.com account.

---

### 4. INVALID MESSAGE ID ERROR (MEDIUM)

**Problem:** When "Search Gmail for Receipts" returns results, "Get Email Details" receives invalid/empty message IDs.

**Evidence from execution #32:**
- Search found 6 emails
- Output structure: `{"pairedItem": {"item": 0}}` (no actual email data)
- "Get Email Details" tried to access `$json.id` but got empty/invalid value
- Gmail API rejected with "Invalid id value"

**Root Cause:** "Search Gmail for Receipts" is configured incorrectly - likely using wrong output mode or missing required fields.

**Current Configuration:**
```json
{
  "operation": "getAll",
  "simple": false,
  "filters": {
    "q": "={{$json.searchQuery}}"
  }
}
```

**Issue:** The node returned items but without message data (only `pairedItem` metadata).

---

## What Actually Happens (Real-World Behavior)

### Current State:
1. Workflow runs daily at 11pm UTC (midnight Berlin time)
2. Loads only 6 vendor patterns (not 25)
3. Searches ONLY swayclarke@gmail.com (not both accounts)
4. Uses broken search query format
5. Past 4 days: Found 0 emails (possibly due to search query issues)
6. Jan 2: Found 6 emails but crashed with "Invalid id" error
7. **Zero receipts successfully downloaded**
8. **Zero files uploaded to Google Drive**
9. **Zero records added to Google Sheets**

### Expected vs Actual:

| Expected | Actual |
|----------|--------|
| 25 vendors monitored | 6 vendors monitored |
| 2 Gmail accounts searched | 1 Gmail account searched |
| Daily receipt downloads | 0 receipts downloaded (ever) |
| Files in "_Receipt-Pool" folder | 0 files |
| Records in "Receipts" sheet | 0 records |

---

## Questions Answered

### 1. Does it actually search both Gmail accounts?
**NO** - Only searches swayclarke@gmail.com. Second account has placeholder credentials.

### 2. How many emails does it find from the 25 vendors?
**UNKNOWN** - Only searching 6 vendors, and search query is malformed. Jan 2 found 6 emails but crashed.

### 3. How many attachments does it successfully download?
**ZERO** - Workflow has never successfully completed the download process.

### 4. What errors occur?
- **Invalid id value** - When search finds emails, the message ID is not properly passed to "Get Email Details"
- **Missing credentials** - Second Gmail account not configured
- **Malformed search query** - "Load Vendor Patterns" outputs wrong field names

### 5. What gets uploaded to Google Drive "_Receipt-Pool"?
**NOTHING** - Workflow has never reached the upload stage.

### 6. What gets logged in Google Sheets "Receipts" tab?
**NOTHING** - Workflow has never reached the logging stage.

### Critical Question: Are there vendors that send links instead of attachments (like Miles)?
**CANNOT DETERMINE** - Workflow has never successfully processed emails. Need to fix bugs first, then re-test.

---

## Recommended Actions (Priority Order)

### Immediate (Blocking Issues):

1. **Fix "Load Vendor Patterns" code** - Output correct `searchQuery` format instead of `emailPattern` + `searchParams`

2. **Set up second Gmail account OAuth** - Configure credentials for swayfromthehook@gmail.com

3. **Fix "Search Gmail for Receipts" configuration** - Ensure it returns message IDs properly

4. **Re-activate workflow** - After code changes, the workflow needs to be saved and re-activated to use the new active version with 25 vendors

### After Fixes:

5. **Run manual test** - Trigger webhook or schedule to verify all 25 vendors are searched

6. **Verify dual-account search** - Confirm both Gmail accounts are queried

7. **Test with known receipts** - Send test emails from monitored vendors to confirm download/upload/logging works end-to-end

8. **Monitor for link-based receipts** - Check if vendors like MILES send links instead of attachments (may need separate handling)

---

## Test Conclusion

**Overall Status:** FAIL - Workflow is non-functional

**Root Cause:** Multiple critical bugs preventing successful execution:
- Using outdated vendor list (6 instead of 25)
- Malformed search query structure
- Second Gmail account not configured
- Invalid message ID handling

**Next Steps:** Fix the 4 critical issues above before re-testing. Current workflow has never successfully downloaded a single receipt.

---

## Execution Evidence

**Recent Execution IDs (for reference):**
- #481 (Jan 6) - https://n8n.oloxa.ai/execution/481
- #436 (Jan 5) - https://n8n.oloxa.ai/execution/436
- #299 (Jan 4) - https://n8n.oloxa.ai/execution/299
- #152 (Jan 3) - https://n8n.oloxa.ai/execution/152
- #32 (Jan 2) - https://n8n.oloxa.ai/execution/32 (ERROR - only execution with emails found)
