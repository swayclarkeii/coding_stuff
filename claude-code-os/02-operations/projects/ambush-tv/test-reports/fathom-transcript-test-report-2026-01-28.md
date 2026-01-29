# Fathom Transcript Workflow Test Report

**Date:** 2026-01-28
**Workflow ID:** cMGbzpq1RXpL0OHY
**Workflow Name:** Fathom Transcript Workflow Final_22.01.26
**Execution ID:** 6409

---

## Summary

- **Total tests attempted:** 1
- ❌ **Failed:** 1 (Cannot execute - validation errors)
- **Execution status:** error (WorkflowHasIssuesError)
- **Duration:** 11ms

---

## Test Result

### Test: Verify Batch Size & Airtable Field Fixes

**Status:** ❌ BLOCKED - Cannot Execute

**Expected to verify:**
1. OpenAI rate limit fix (batch size reduced from 5 to 3)
2. Airtable field mapping fix ("Call Type" → "call_type")
3. Retry logic on AI nodes (3 retries, 30s wait)

**Actual result:**
- Workflow has 6 critical validation errors that prevent execution
- Execution failed immediately with: "The workflow has issues and cannot be executed"
- Cannot test the applied fixes until structural errors are resolved

---

## Critical Errors Found (6)

### 1. Route: Webhook or API - Expression Format Error

**Node:** Route: Webhook or API
**Error:** Unmatched expression brackets: 0 opening, 3 closing
**Impact:** Workflow cannot route between webhook/API modes

**Details:**
```
Field 'jsCode' Unmatched expression brackets: 0 opening, 3 closing
```

The code contains optional chaining operators (`?.`) which may be confusing n8n's bracket parser.

---

### 2. Save to Airtable - Missing Record ID

**Node:** Save to Airtable
**Error:** Required property 'Record ID' cannot be empty
**Impact:** Cannot save call metadata to Airtable

**Root cause:** Node is configured for "Update" operation but needs to be "Create" (or "Upsert")

**This blocks testing of the "call_type" field fix.**

---

### 3. Save Transcript to Drive - Invalid Operation

**Node:** Save Transcript to Drive
**Error:** Invalid value for 'operation'. Must be one of: copy, createFromText, deleteFile, download, move, share, update, upload
**Impact:** Cannot save transcripts to Google Drive

**Root cause:** Operation field has an invalid value (not in the allowed list)

---

### 4. Process Each Meeting - Cannot Return Primitives

**Node:** Process Each Meeting
**Error:** Cannot return primitive values directly
**Impact:** Processing logic breaks

**Fix needed:** Code must return array of objects with `json` property:
```javascript
return [{ json: { ...data } }];
// NOT: return data;
```

---

### 5. Prepare Airtable Data - Cannot Return Primitives

**Node:** Prepare Airtable Data
**Error:** Cannot return primitive values directly
**Impact:** Airtable data preparation fails

**Fix needed:** Same as #4 - must return array of objects with `json` property

---

### 6. Process Webhook Meeting - Cannot Return Primitives

**Node:** Process Webhook Meeting
**Error:** Cannot return primitive values directly
**Impact:** Webhook-triggered executions fail

**Fix needed:** Same as #4 - must return array of objects with `json` property

---

## Additional Warnings (56 total)

**Most critical:**
- 6 nodes using deprecated `continueOnFail: true` (should use `onError: 'continueRegularOutput'`)
- 3 OpenAI nodes on outdated typeVersion (1.8, should be 2.1)
- Multiple nodes missing error handling
- Connections to disabled nodes (Impromptu name extraction flow)

---

## Next Steps

**Before re-testing the batch size and Airtable field fixes:**

1. **Fix "Save to Airtable" node** - Change operation to "Create" or "Upsert"
2. **Fix "Route: Webhook or API" code** - Resolve bracket parsing issue
3. **Fix "Save Transcript to Drive"** - Set valid operation value
4. **Fix 3 Code nodes** - Update return statements to proper format:
   - Process Each Meeting
   - Prepare Airtable Data
   - Process Webhook Meeting

**Recommended approach:**
- Launch **solution-builder-agent** to fix all 6 critical errors
- Then re-run **test-runner-agent** to verify:
  - No OpenAI rate limit (batch size 3 works)
  - Airtable save succeeds with "call_type" field
  - Slack notification sent with 5 decision buttons

---

## Technical Details

**Validation Profile:** runtime
**Nodes in workflow:** 39 total (33 enabled)
**Connections:** 35 valid, 0 invalid
**Expressions validated:** 41

**Error breakdown:**
- Node configuration errors: 6
- Warnings: 56
- Invalid connections: 0

---

## Conclusion

The workflow has critical structural errors that prevent execution. The fixes previously applied (batch size reduction, retry logic, Airtable field mapping) **cannot be tested** until these 6 blocking errors are resolved.

**Recommendation:** Use solution-builder-agent to fix the 6 critical errors, then re-run this test.

**Agent ID:** [to be populated after agent completes]
**Type:** test-runner-agent
**Status:** Test blocked - validation errors found
