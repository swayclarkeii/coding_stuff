# n8n Test Report – SOP Builder Lead Magnet

**Workflow ID:** ikVyMpDI0az6Zk4t
**Test Date:** 2026-01-29
**Tester:** test-runner-agent

---

## Summary

**Status:** FAILED - Workflow cannot execute due to critical structural errors

- Total tests: 1
- PASSED: 0
- FAILED: 1

---

## Test Details

### Test: Comprehensive SOP Input (Score ≥85%)

**Status:** FAIL

**Input Data:**
```json
{
  "email": "swayclarkeii@gmail.com",
  "name": "Sway Clarke",
  "goal": "Standardize employee onboarding to ensure consistency across all departments",
  "improvement_type": "quality",
  "department": "Human Resources",
  "end_user": "HR managers and team leads",
  "input_method": "text",
  "process_steps": "[comprehensive 8-step process with preparation, verification, and document control]"
}
```

**Execution ID:** Not applicable (workflow failed before execution)

**Final Status:** ERROR - Workflow validation failed

---

## Root Cause Analysis

### Critical Errors (4)

The workflow has 4 critical configuration errors that prevent execution:

#### 1. **LLM: Generate Improved SOP** - Missing Required URL
- **Error:** "Required property 'URL' cannot be empty"
- **Impact:** Critical - HTTP Request node cannot proceed without endpoint
- **Fix needed:** Add the Claude API URL or model endpoint

#### 2. **Send HTML Email** - Invalid Operation
- **Error:** "Invalid value for 'operation'. Must be one of: addLabels, delete, get, getAll, markAsRead, markAsUnread, removeLabels, reply, send, sendAndWait"
- **Impact:** Critical - Gmail operation misconfigured
- **Fix needed:** Change operation to one of the valid values (likely "send" for sending email)

#### 3. **Generate Success Email (≥85%)** - Cannot Return Primitive Values
- **Error:** "Cannot return primitive values directly"
- **Impact:** Critical - Code node configured incorrectly
- **Fix needed:** Wrap output in an object structure (e.g., `{body: "..."}, {json: {...}}`)

#### 4. **Generate PDF HTML** - Cannot Return Primitive Values
- **Error:** "Cannot return primitive values directly"
- **Impact:** Critical - Code node configured incorrectly
- **Fix needed:** Wrap HTML output in proper object structure

### Warnings (58 total)

Major warnings include:
- **Outdated typeVersions** on 6 nodes (Check Audio File, Transcribe with Whisper, Merge nodes, HTTP nodes)
- **Invalid $ usage** in 5 Code nodes (Invalid expression syntax)
- **Missing error handling** on 11 nodes (no `onError` property defined)
- **Primitive return values** in multiple Code nodes
- **Long linear chain** (23 sequential nodes) - should be refactored into sub-workflows

---

## Workflow Execution Attempt

**Execution ID:** 6885 (error trigger)

**Status:** Failed immediately

**Error Message:**
```
WorkflowHasIssuesError: The workflow has issues and cannot be executed for that reason.
Please fix them first.
```

The workflow did not proceed past the Error Trigger node because n8n's validation engine detected the critical configuration issues and prevented execution.

---

## PDF Generation Status

**Convert HTML to PDF node:** Not executed (workflow failed before reaching this node)

**Status:** UNKNOWN - Cannot verify if PDF generation works until critical errors are fixed

---

## Email Sending Status

**Send HTML Email node:** Not executed (workflow failed before reaching this node)

**Status:** FAILED - Gmail operation is incorrectly configured (wrong operation type)

---

## Validation Summary

**Workflow Validity:** Invalid

**Total Nodes:** 35
**Valid Connections:** 38
**Invalid Connections:** 0
**Error Count:** 4 (CRITICAL)
**Warning Count:** 58 (MODERATE)

---

## What Needs to Be Fixed (Priority Order)

### CRITICAL (Must Fix to Execute)

1. **LLM: Generate Improved SOP node**
   - Add URL: Specify the Claude API endpoint or model URL
   - Current: Empty URL field
   - Required: Valid API endpoint

2. **Send HTML Email node**
   - Change operation from current value to: `send`
   - Update any required fields for Gmail send operation

3. **Generate Success Email (≥85%) node**
   - Wrap return value in proper object structure
   - Change: `return messageText;`
   - To: `return [{json: {body: messageText}}];`

4. **Generate PDF HTML node**
   - Wrap HTML output in proper object structure
   - Change: `return htmlString;`
   - To: `return [{json: {html: htmlString}}];`

### IMPORTANT (Should Fix)

5. Update outdated node typeVersions (6 nodes affected)
6. Fix invalid $ usage in Code nodes (5 instances)
7. Add error handling (`onError` property) to all HTTP and database nodes
8. Refactor 23-node linear chain into sub-workflows

### NICE-TO-HAVE

9. Add webhook response handling (currently missing)
10. Review all Code nodes for error handling

---

## Next Steps

**Recommendation:** This workflow requires fixes by the solution-builder-agent or engineering team before testing can proceed.

**To resume testing after fixes:**
1. Fix the 4 critical configuration errors
2. Run validation again: `n8n_validate_workflow` with ID `ikVyMpDI0az6Zk4t`
3. Once validation passes, re-run this test with the same test data

**Estimated SOP Score:** Unknown (workflow could not execute to calculate score)

---

## Conclusion

The SOP Builder workflow is currently non-functional due to critical configuration errors in 4 nodes. The test data could not be processed. Once these errors are resolved, the workflow should be tested again to determine if the SOP scores 85% or higher.
