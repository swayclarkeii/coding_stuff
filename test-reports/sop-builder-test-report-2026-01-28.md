# n8n Test Report – SOP Builder Lead Magnet

**Workflow ID:** ikVyMpDI0az6Zk4t
**Workflow Name:** SOP Builder Lead Magnet
**Test Date:** 2026-01-28
**Tested By:** test-runner-agent

---

## Summary
- Total tests: 1
- ✅ Passed: 0
- ❌ Failed: 1

---

## Test Details

### Test 1: Basic SOP Submission (Text Input)

**Status:** ❌ FAIL

**Test Input:**
```json
{
  "email": "swayclarkeii@gmail.com",
  "name": "Sway Test",
  "goal": "Onboard new clients quickly",
  "improvement_type": "speed",
  "department": "operations",
  "end_user": "New sales hires",
  "process_steps": "Step 1: Get client email. Step 2: Send welcome email. Step 3: Done.",
  "input_method": "text"
}
```

**Execution ID:** 6648
**Final Status:** error
**Duration:** 13ms
**Failed at:** Workflow validation (before execution)

**Primary Error:**
```
WorkflowHasIssuesError: The workflow has issues and cannot be executed for that reason. Please fix them first.
```

**Root Cause:**
The workflow has a **critical error** in the `Generate Improvement Email (<75%)` node (Code node).

**Error Details from Validation:**
```
Node: Generate Improvement Email (<75%)
Message: Cannot return primitive values directly
```

**What This Means:**
The Code node is attempting to return a JavaScript value directly instead of wrapping it in the proper n8n item structure. Code nodes in n8n must return an array of objects with a `json` property.

**Example of incorrect vs correct return:**

❌ **Incorrect (current):**
```javascript
return [{ ...data, html_report: html, email_subject: subject }]
```

✅ **Correct:**
```javascript
return [{
  json: { ...data, html_report: html, email_subject: subject }
}];
```

---

## Validation Report

**Workflow Validity:** ❌ Invalid
**Total Nodes:** 32
**Errors:** 1 (critical)
**Warnings:** 46 (non-blocking)

### Critical Error (Blocks Execution)

1. **Generate Improvement Email (<75%)**
   - **Error:** "Cannot return primitive values directly"
   - **Impact:** Workflow cannot execute at all
   - **Fix Required:** Wrap return value in `{ json: {...} }` structure

### Additional Warnings (Non-Critical)

The workflow has 46 warnings including:
- Multiple outdated node typeVersions (can be upgraded but not critical)
- Missing error handling on HTTP Request nodes
- Invalid `$` usage in some Code nodes (should use `$input` or named node references)
- Deprecated `continueOnFail: true` (should use `onError: 'continueRegularOutput'`)
- Long linear chain (23 nodes) - consider breaking into sub-workflows

These warnings don't block execution but indicate areas for improvement.

---

## Recommended Fixes

### Priority 1 (Critical - Blocks Execution)

**Fix the "Generate Improvement Email (<75%)" node:**

The current code ends with:
```javascript
const subject = `Your SOP Analysis - Score: ${score}%`;

return [{ ...data, html_report: html, email_subject: subject }]
```

Change the last line to:
```javascript
return [{
  json: { ...data, html_report: html, email_subject: subject }
}];
```

### Priority 2 (High - Best Practice)

**Fix Invalid $ Usage in Code Nodes:**

Several nodes use deprecated `$` syntax. Update:
- `Set Transcription as Steps`
- `Extract Validation Response`
- `Extract Improved SOP`
- `Error Handler`
- `Prepare Update Data`
- `Prepare New Lead Data`

Replace `$(nodeName)` with `$('nodeName')` (add quotes).

### Priority 3 (Medium - Reliability)

**Add Error Handling to HTTP Nodes:**

Add to LLM API call nodes:
```json
"onError": "continueRegularOutput",
"retryOnFail": true,
"maxTries": 3
```

**Replace deprecated continueOnFail:**

In "Check Existing Lead" node, replace:
```json
"continueOnFail": true
```

With:
```json
"onError": "continueRegularOutput"
```

---

## Next Steps

1. **Immediate:** Fix the `Generate Improvement Email (<75%)` return statement
2. **Before Re-testing:** Fix invalid `$` usage in Code nodes
3. **Re-test:** Run the same test payload after fixes
4. **Post-Success:** Consider implementing Priority 3 fixes for production reliability

---

## Notes

- The Error Trigger (node: error-trigger) **did** fire, which is good - error handling path is connected
- The workflow sent an error notification to sway@oloxa.ai (execution 6649)
- The basic structure and connections are valid (34 connections validated)
- This is a structure/syntax issue, not a logic issue

---

## Test Command Used

```javascript
mcp__n8n-mcp__n8n_test_workflow({
  workflowId: "ikVyMpDI0az6Zk4t",
  data: {
    email: "swayclarkeii@gmail.com",
    name: "Sway Test",
    goal: "Onboard new clients quickly",
    improvement_type: "speed",
    department: "operations",
    end_user: "New sales hires",
    process_steps: "Step 1: Get client email. Step 2: Send welcome email. Step 3: Done.",
    input_method: "text"
  },
  triggerType: "webhook",
  httpMethod: "POST",
  waitForResponse: true
})
```

**Webhook URL:** https://n8n.oloxa.ai/webhook/sop-builder

---

## Agent Information

**Agent Type:** test-runner-agent
**Session Date:** 2026-01-28
**Tools Used:**
- n8n_test_workflow (execution)
- n8n_executions (error retrieval)
- n8n_validate_workflow (validation analysis)
