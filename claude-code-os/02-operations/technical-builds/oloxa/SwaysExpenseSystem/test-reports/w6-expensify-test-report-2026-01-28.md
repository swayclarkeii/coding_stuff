# n8n Test Report - W6 Expensify Table Extractor (SIMPLE)

**Workflow ID:** zFdAi3H5LFFbqusX
**Test Date:** 2026-01-28
**Execution ID:** 6398

---

## Summary

- Total tests: 1
- ❌ Failed: 1
- ✅ Passed: 0

---

## Test Results

### Test: Extract 9 Expensify transactions from November 2025 report

**Status:** ❌ FAIL

**Input:**
```json
{
  "drive_file_id": "1VLswjWt7hvd3kLVJ7CDm6o-FGYpwB9PX",
  "report_month": "November 2025"
}
```

**Execution Status:** error
**Duration:** 1.38 seconds
**HTTP Response:** 200 OK (empty body)

---

## Root Cause

**Critical Error: Missing Anthropic API Credential**

The workflow failed at the "Extract Table with Claude API" HTTP Request node.

**Error Message:**
```
Credential with ID "MRSNO4UW3OEIA3tQ" does not exist for type "httpHeaderAuth".
```

**Failed Node:** `Extract Table with Claude API` (node ID: `call-claude-api`)

**What happened:**
1. ✅ Webhook Trigger received payload successfully
2. ✅ Download PDF from Drive completed (1.37s, retrieved 1.03 MB PDF)
3. ✅ Build Claude Request executed (disabled, but bypassed correctly)
4. ❌ **Extract Table with Claude API failed** - Cannot find credential `MRSNO4UW3OEIA3tQ`

---

## Successful Nodes

### 1. Webhook Trigger
- Status: ✅ Success
- Received POST request with drive_file_id and report_month
- Execution time: 0ms

### 2. Download PDF from Drive
- Status: ✅ Success
- Retrieved: `SwayClarkeNOV2025ExpenseReport[37638].pdf`
- File size: 1.03 MB
- Binary data ID: `filesystem-v2:workflows/zFdAi3H5LFFbqusX/executions/6398/binary_data/7d8ec540-1d33-484f-a340-65813a1b3ed8`
- Execution time: 1,373ms

### 3. Build Claude Request (Disabled)
- Status: ✅ Success (bypassed correctly)
- Workflow flow continues to HTTP Request node
- Execution time: 0ms

---

## Node That Never Ran

The following nodes never executed because the workflow stopped at the credential error:

- Parse Claude Response
- Log Receipts to Database
- Webhook Response

---

## Technical Details

### HTTP Request Node Configuration

**Node:** Extract Table with Claude API
**Type:** n8n-nodes-base.httpRequest v4.2
**Method:** POST
**URL:** https://api.anthropic.com/v1/messages

**Headers:**
- anthropic-version: 2023-06-01

**Credential Reference:**
```json
{
  "credentials": {
    "httpHeaderAuth": {
      "id": "MRSNO4UW3OEIA3tQ",
      "name": "Anthropic API Key"
    }
  }
}
```

**Problem:** This credential ID does not exist in the n8n instance.

---

## Required Fix

**Action for solution-builder-agent:**

1. **Check available Anthropic credentials:**
   - List all httpHeaderAuth credentials in n8n
   - Find the correct "Anthropic API Key" credential ID

2. **Update HTTP Request node:**
   - Replace credential ID `MRSNO4UW3OEIA3tQ` with correct credential ID
   - OR create new Anthropic API credential if none exists

3. **Alternative: Use n8n's native Anthropic node:**
   - Consider replacing HTTP Request with `@n8n/n8n-nodes-langchain.lmChatAnthropic`
   - This may have more reliable credential handling

---

## Expected Behavior (Not Reached)

Once credential is fixed, the workflow should:

1. Extract PDF binary data
2. Send to Claude API with PDF Vision prompt
3. Parse JSON array of transactions
4. Transform to receipt format with ReceiptID
5. Append 9 rows to Google Sheets "Receipts" tab
6. Return success response via webhook

**Expected output:** 9 receipt records in format:
```
ReceiptID: EXP_November 2025_01, EXP_November 2025_02, etc.
Vendor: [merchant name]
Amount: [transaction amount]
Date: [YYYY-MM-DD]
Currency: EUR
Source: Expensify
```

---

## Recommendation

**Immediate action:** Fix the missing Anthropic API credential reference.

**Priority:** HIGH - This blocks all PDF extraction functionality.

**Estimated fix time:** 2-3 minutes (update credential ID in HTTP Request node)
