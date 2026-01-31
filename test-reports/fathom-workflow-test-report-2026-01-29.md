# n8n Test Report – Fathom Transcript Workflow Final_22.01.26

**Workflow ID:** cMGbzpq1RXpL0OHY
**Test Date:** 2026-01-29 22:49:03 UTC
**Test Runner Agent ID:** [Current session]

---

## Summary

- **Total tests executed:** 1
- **✅ Passed:** 0
- **❌ Failed:** 1
- **⚠️ Blocked:** Workflow has structural issues preventing execution

---

## Test Results

### Test 1: Basic Webhook Trigger Test

**Status:** ❌ FAIL (Blocked by workflow issues)

**Test Details:**
- **Trigger method:** Webhook POST to `fathom-test` path
- **Trigger response:** HTTP 200 "Workflow was started"
- **Execution created:** NO
- **Actual outcome:** No execution record created; workflow cannot execute

**Error Analysis:**

The workflow returned success when triggered, but failed to create an execution record. Investigation revealed:

1. **Latest execution (7010):**
   - Started: 2026-01-29T22:37:00.118Z
   - Stopped: 2026-01-29T22:37:00.137Z (19ms duration)
   - Status: error
   - Error: `WorkflowHasIssuesError`
   - Message: "The workflow has issues and cannot be executed for that reason. Please fix them first."

2. **Validation results:**
   - Structural validation: PASSED (valid: true)
   - Total nodes: 40 (33 enabled, 7 disabled)
   - Trigger nodes: 3 (Webhook, Manual, Schedule)
   - Valid connections: 35
   - Invalid connections: 0
   - Errors: 0
   - **Warnings: 54** (including credential and configuration warnings)

3. **Recent execution pattern:**
   - All recent executions (7010, 7007, 7003, 6997, 6991) show identical error
   - All fail immediately (19ms average)
   - All stopped with `WorkflowHasIssuesError`
   - No nodes executed in any execution

**Root Cause:**

The error `WorkflowHasIssuesError` typically indicates one of:
- Missing or invalid credentials
- Required node parameters not configured
- Expression evaluation failures
- API connection issues

The workflow passes structural validation but fails at execution initialization, suggesting **credential or configuration issues** rather than connection/logic problems.

**Critical Warnings Identified:**

1. **Credential-related:**
   - Multiple nodes use external services (Google Drive, Airtable, OpenAI, Slack)
   - No explicit credential errors in validation, but execution fails before any node runs

2. **Configuration issues:**
   - "Create or Get Date Folder" has expression format warning for resource locator
   - Multiple Code nodes have "Invalid $ usage detected"
   - Webhook node lacks proper error handling

3. **Deprecated patterns:**
   - 9 nodes use deprecated `continueOnFail: true` (should use `onError`)
   - 2 OpenAI nodes use outdated typeVersion (1.8 → 2.1 required)
   - Webhook Trigger uses outdated typeVersion (2 → 2.1 required)

---

## Next Steps

### Immediate Actions Required

1. **Check credentials in n8n UI:**
   - Google Drive OAuth credentials
   - Airtable API credentials
   - OpenAI API credentials
   - Slack OAuth credentials
   - Fathom API credentials

2. **Fix resource locator format:**
   - Node: "Create or Get Date Folder"
   - Field: `name`
   - Current: `"name": "={{ $json.date_folder_name }}"`
   - Required: Use resource locator format with `__rl` structure

3. **Update deprecated nodes:**
   - Replace `continueOnFail: true` with `onError: 'continueRegularOutput'` (9 nodes)
   - Update OpenAI nodes to typeVersion 2.1 (2 nodes)
   - Update Webhook Trigger to typeVersion 2.1

4. **Fix Code node issues:**
   - "Combine Meeting + Transcript1": Invalid $ usage, doesn't reference input data
   - "Match Meetings to Folders": Invalid $ usage, doesn't reference input data
   - "Build Slack Blocks": Invalid $ usage, doesn't reference input data
   - "Prepare Airtable Data": Invalid $ usage

### Testing Strategy

Once issues are resolved:
1. Test webhook trigger with empty payload
2. Test manual trigger with API data
3. Verify credential connections for each service
4. Test individual node execution in n8n UI
5. Run full workflow with test Fathom data

---

## Execution Timeline

| Time (UTC) | Event | Status |
|------------|-------|--------|
| 22:37:00 | Execution 7010 started | Error (19ms) |
| 22:49:03 | Test trigger sent | HTTP 200 returned |
| 22:49:03 | Polling started | No execution created |
| 22:50:00+ | Multiple polls | No new execution found |

---

## Technical Details

**Workflow Structure:**
- 40 total nodes
- 33 enabled nodes
- 7 disabled nodes (impromptu meeting AI analysis path)
- 35 valid connections
- 38 total connections (3 connections to disabled nodes)

**Trigger Configuration:**
- Webhook path: `fathom-test`
- HTTP method: POST
- Response mode: Not configured (warning: should always send response)

**Execution Environment:**
- n8n instance: n8n.oloxa.ai
- Workflow last updated: 2026-01-29T22:48:07.215Z
- Workflow created: 2026-01-20T22:27:32.419Z

---

## Conclusion

**Test Result:** FAIL - Workflow is non-functional due to configuration or credential issues.

**Confidence:** HIGH - The error is consistent and reproducible across all recent executions.

**Recommended Owner:** Sway should:
1. Open n8n.oloxa.ai
2. Check execution 7010 for detailed error message
3. Verify all credential connections
4. Fix resource locator format issue
5. Re-test manually in n8n UI before automated testing

**Agent Recommendation:** Workflow requires **solution-builder-agent** intervention to fix structural issues, not just test execution.

---

**Report generated by:** test-runner-agent
**Report saved to:** /Users/swayclarke/coding_stuff/test-reports/fathom-workflow-test-report-2026-01-29.md
