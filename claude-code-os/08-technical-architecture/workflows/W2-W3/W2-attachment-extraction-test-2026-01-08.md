# W2 Attachment Extraction Test Report
**Date:** 2026-01-08
**Workflow ID:** dHbwemg7hEB4vDmC
**Workflow Name:** Expense System - Workflow 2: Gmail Receipt Monitor
**Execution ID:** 611

---

## Summary

- **Total tests:** 1 (single execution test)
- **Result:** FAIL (Critical blocker: Credentials not found)
- **Execution status:** success (workflow completed but with errors)
- **Duration:** 11.2 seconds

---

## Test: HTTP Request Attachment Extraction

### Status: FAIL

### Execution Details

**Trigger:** Webhook (POST)
**Started:** 2026-01-08T15:25:25.897Z
**Stopped:** 2026-01-08T15:25:37.146Z
**Total nodes executed:** 8 of 13

### Node-by-Node Results

#### 1. Test Trigger - Webhook
- **Status:** SUCCESS
- **Items output:** 1
- **Notes:** Successfully triggered workflow

#### 2. Load Vendor Patterns
- **Status:** SUCCESS
- **Items output:** 13
- **Notes:** Loaded vendor search patterns correctly

#### 3. Search Gmail for Receipts (Account 1)
- **Status:** SUCCESS
- **Items output:** 7 emails found
- **Notes:** Successfully found Stripe emails in Account 1

#### 4. Get Email Details (Account 1)
- **Status:** FAIL (returned error objects, but node didn't fail)
- **Items output:** 7 items (all errors)
- **Error message:** "Credentials not found"
- **Error type:** NodeOperationError
- **Failed at:** All 7 email detail requests

**Sample error output:**
```json
{
  "error": {
    "message": "Credentials not found",
    "timestamp": 1767885930525,
    "name": "NodeOperationError",
    "context": {}
  }
}
```

#### 5. Search Gmail for Receipts (Account 2)
- **Status:** SUCCESS
- **Items output:** 9 emails found
- **Notes:** Successfully found Anthropic emails in Account 2

#### 6. Get Email Details (Account 2)
- **Status:** FAIL (returned error objects, but node didn't fail)
- **Items output:** 9 items (all errors)
- **Error message:** "Credentials not found"
- **Error type:** NodeOperationError
- **Failed at:** All 9 email detail requests

**Sample error output:**
```json
{
  "error": {
    "message": "Credentials not found",
    "timestamp": 1767885937100,
    "name": "NodeOperationError",
    "context": {}
  }
}
```

#### 7. Combine Both Gmail Accounts
- **Status:** SUCCESS (but combined error objects)
- **Items output:** 16 items (all errors)
- **Notes:** Successfully merged outputs from both accounts, but all items contain error objects

#### 8. Extract Attachment Info
- **Status:** SUCCESS (but no items to extract)
- **Items input:** 16 error objects
- **Items output:** 0 attachments
- **Notes:** Code node filtered out all error objects, resulting in zero attachments

#### 9. Download Attachment
- **Status:** NOT EXECUTED
- **Reason:** No items from Extract Attachment Info

#### 10. Upload to Receipt Pool
- **Status:** NOT EXECUTED
- **Reason:** Downstream from failed extraction

#### 11. Prepare Receipt Record
- **Status:** NOT EXECUTED
- **Reason:** Downstream from failed extraction

#### 12. Log Receipt in Database
- **Status:** NOT EXECUTED
- **Reason:** Downstream from failed extraction

---

## Root Cause Analysis

### Critical Issue: Credentials Not Found

Both HTTP Request nodes (`Get Email Details` and `Get Email Details (Account 2)`) are failing with **"Credentials not found"** errors.

**What this means:**
- The HTTP Request nodes are configured to use OAuth2 credentials
- The credential IDs referenced in the nodes do not exist or are not accessible
- The nodes are trying to authenticate with Gmail API but cannot find the OAuth tokens

**Why this happened:**
- When we replaced Gmail nodes with HTTP Request nodes, we likely:
  1. Created new credential configurations in HTTP Request nodes
  2. Referenced credentials that don't exist in n8n's credential store
  3. OR the credential IDs were not properly saved/linked

**Impact:**
- Zero email details fetched (0 of 16 emails)
- Zero attachments extracted (expected: unknown, actual: 0)
- Zero downloads, uploads, or database entries
- Entire workflow blocked at HTTP Request step

---

## Expected vs Actual Results

### Expected Results:
1. Search Gmail: Find 16 emails (Stripe + Anthropic)
2. Get Email Details: Return 200 status with `payload.parts[]` array
3. Extract Attachment Info: Output >0 attachment items
4. Download: Successfully download PDF files
5. Upload: Upload to Google Drive Receipt Pool
6. Log: Create entries in Receipts sheet

### Actual Results:
1. Search Gmail: PASS - Found 16 emails (7 Stripe + 9 Anthropic)
2. Get Email Details: FAIL - All requests returned "Credentials not found" error
3. Extract Attachment Info: FAIL - 0 attachments extracted (filtered out errors)
4. Download: NOT EXECUTED (no attachments)
5. Upload: NOT EXECUTED (no downloads)
6. Log: NOT EXECUTED (no uploads)

---

## Critical Blocker

**The HTTP Request nodes cannot authenticate with Gmail API.**

### What needs to happen next:

1. **Verify OAuth2 credentials exist in n8n**
   - Check n8n credentials page
   - Ensure OAuth2 credentials are properly configured for Gmail API
   - Verify both Account 1 and Account 2 have valid credentials

2. **Update HTTP Request node configurations**
   - Open workflow in n8n UI
   - Edit "Get Email Details" node
   - Set credential field to valid OAuth2 credential
   - Repeat for "Get Email Details (Account 2)"
   - Save workflow

3. **Alternative: Revert to Gmail nodes**
   - If HTTP Request approach is too complex
   - Gmail nodes have built-in credential handling
   - Consider using Gmail nodes with "Get Email" operation

4. **Re-test after fixing credentials**
   - Run this test again
   - Verify HTTP Request nodes return 200 status
   - Check that `payload.parts[]` array is present
   - Confirm attachments are extracted

---

## Test Execution Metrics

- **Emails searched:** 16 (7 + 9 across both accounts)
- **Email details fetched:** 0 (all failed with credentials error)
- **Attachments extracted:** 0
- **Attachments downloaded:** 0
- **Files uploaded to Drive:** 0
- **Database entries created:** 0

---

## Conclusion

**The test FAILED due to a critical blocker: missing OAuth2 credentials.**

The HTTP Request approach is theoretically sound, but the nodes are not properly configured with valid Gmail API credentials. Until this is resolved, the workflow cannot fetch email details or extract attachments.

**Next Steps:**
1. Fix OAuth2 credential configuration in HTTP Request nodes
2. Re-run this test to verify attachment extraction works
3. If credentials cannot be configured, consider reverting to Gmail nodes

---

## Test Environment

- **n8n Instance:** https://n8n.swayclarke.com
- **Workflow Version:** Latest (modified 2026-01-08)
- **Test Method:** Webhook trigger (POST)
- **Execution Mode:** production
