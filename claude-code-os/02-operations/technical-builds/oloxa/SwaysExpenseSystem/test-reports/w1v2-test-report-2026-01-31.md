# W1v2 Test Report - Expense System Bank Statement Intake

**Date:** 2026-01-31
**Workflow ID:** Is8zl1TpWhIzspto
**Workflow Name:** Expense System - W1v2: Bank Statement Intake (Webhook)
**Google Sheets ID:** 1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM

---

## Summary

- **Total tests:** 2
- **Passed:** 0
- **Failed:** 2
- **Status:** BLOCKED - Webhook not registered

---

## Issue Identified

### Problem: Webhook Not Registered (404 Error)

**Error Message:**
```
The requested webhook "POST expense-bank-statement-upload" is not registered.
```

**Root Cause:**
The workflow is marked as ACTIVE in n8n, but the webhook trigger is not properly registered with the n8n webhook router. This is a known n8n issue where:
- Activating a workflow doesn't always register the webhook immediately
- Webhooks can fail to register if there's a configuration timing issue
- The webhook path might conflict with another workflow

**Workflow Status:**
- Active: ✅ YES
- Webhook path configured: ✅ expense-bank-statement-upload
- HTTP method: ✅ POST
- Webhook registered: ❌ NO (404 error)

---

## Test Details

### Test 1: Basic Webhook Trigger
- **Status:** ❌ BLOCKED
- **Expected:** Workflow executes successfully
- **Actual:** 404 Not Found - webhook not registered
- **Execution ID:** None (webhook call failed before workflow execution)
- **Error:**
  ```
  {
    "code": 404,
    "message": "The requested webhook \"POST expense-bank-statement-upload\" is not registered.",
    "hint": "The workflow must be active for a production URL to run successfully."
  }
  ```

### Test 2: Webhook with File Metadata
- **Status:** ❌ BLOCKED
- **Test Data:**
  ```json
  {
    "fileName": "ING_2025-11_Statement.pdf",
    "data": {
      "fileName": "ING_2025-11_Statement.pdf",
      "mimeType": "application/pdf",
      "fileSize": 12345
    }
  }
  ```
- **Expected:** Workflow parses filename and triggers successfully
- **Actual:** 404 Not Found - same webhook registration issue
- **Execution ID:** None

---

## Workflow Validation Results

**Validation Status:** ✅ VALID (with warnings)

**Statistics:**
- Total nodes: 11
- Enabled nodes: 11
- Trigger nodes: 1
- Valid connections: 10
- Invalid connections: 0
- Expressions validated: 25
- Error count: 0
- Warning count: 23

**Key Warnings:**
1. Webhook Upload Trigger - Outdated typeVersion (2 vs 2.1)
2. Webhook Upload Trigger - Should always send a response, even on error
3. Multiple Code nodes - Missing error handling
4. HTTP Request node - No retry configuration for transient failures
5. Google Sheets nodes - Expression format warnings (resource locator format)

**Suggestions:**
- Add error handling to all Code nodes
- Update webhook trigger to latest typeVersion
- Add `onError: 'continueRegularOutput'` to webhook trigger
- Add retry logic to HTTP Request node

---

## Required Fix

### Solution: Reactivate Workflow to Register Webhook

**Steps:**
1. Open workflow in n8n UI: https://n8n.oloxa.ai/workflow/Is8zl1TpWhIzspto
2. Click the "Active" toggle to DEACTIVATE the workflow
3. Wait 2-3 seconds
4. Click the "Active" toggle to REACTIVATE the workflow
5. Verify webhook is registered by checking the execution log or testing again

**Alternative Solutions:**
1. **Check for path conflicts:** Search for other workflows using the same webhook path "expense-bank-statement-upload"
2. **Restart n8n service:** If deactivate/reactivate doesn't work, restart the n8n server
3. **Change webhook path:** Temporarily change to a different path (e.g., "expense-bank-v2") to test if path is the issue

---

## Next Steps

1. **IMMEDIATE:** Deactivate and reactivate the workflow in n8n UI
2. **VERIFY:** Test webhook registration after reactivation
3. **RE-TEST:** Run test-runner-agent again once webhook is registered
4. **ENHANCE:** Consider adding error handling to webhook trigger and Code nodes (optional, after testing)

---

## Webhook Details

**Production URL:** https://n8n.oloxa.ai/webhook/expense-bank-statement-upload
**Method:** POST
**Expected Payload:** Binary file upload or JSON with fileName/fileData

**Workflow Flow:**
1. Webhook Upload Trigger → Receives file upload
2. Extract File Metadata → Parses filename for bank/date
3. Build Anthropic API Request → Prepares PDF for Vision API
4. Parse PDF with Anthropic Vision → Extracts transactions via Claude
5. Parse Anthropic Response → Formats transaction data
6. (Split) → Prepare Statement Log + Check for Duplicates
7. Log Statement Record → Writes to Statements sheet
8. Read Existing Transactions → Fetches current data
9. Filter Non-Duplicates → Removes duplicate transactions
10. Write Transactions to Database → Appends new transactions

---

## Agent Information

**Agent ID:** [test-runner-agent]
**Type:** test-runner-agent
**Task:** Execute and validate W1v2 workflow
**Status:** Blocked - awaiting webhook registration fix
