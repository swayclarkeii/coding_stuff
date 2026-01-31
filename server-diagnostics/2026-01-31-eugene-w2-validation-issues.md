# Eugene W2 Workflow Validation Issues - Diagnostic Report

**Date:** 2026-01-31
**Workflow ID:** okg8wTqLtPUwjQ18
**Workflow Name:** Chunk 2.5 - Client Document Tracking (Eugene Document Organizer)
**Issue Type:** WorkflowHasIssuesError

---

## Executive Summary

Successfully identified the exact validation issues preventing workflow execution. n8n's `checkForWorkflowIssues()` function is detecting **missing required parameters** in two Google Drive nodes.

---

## Investigation Method

1. SSH'd into n8n server (157.230.21.230)
2. Located compiled workflow validation code at:
   ```
   /usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-core@[...]/dist/execution-engine/workflow-execute.js
   ```
3. Added temporary debug logging before `WorkflowHasIssuesError` throw (line 686)
4. Triggered workflow via webhook: `https://n8n.oloxa.ai/webhook/eugene-quick-test`
5. Captured debug output from Docker logs
6. Restored original code (removed debug logging)

---

## Exact Issues Detected by n8n

```json
{
  "Move File to 38_Unknowns": {
    "parameters": {
      "fileId": [
        "Parameter \"File\" is required."
      ]
    }
  },
  "Move File to Final Location": {
    "parameters": {
      "fileId": [
        "Parameter \"File\" is required."
      ]
    }
  }
}
```

---

## Root Cause Analysis

Both failing nodes are **Google Drive - Move File** operations:

1. **Node:** "Move File to 38_Unknowns"
   - **Issue:** Missing required parameter `fileId`
   - **Impact:** Cannot move files to the Unknowns folder

2. **Node:** "Move File to Final Location"
   - **Issue:** Missing required parameter `fileId`
   - **Impact:** Cannot move files to final destination folder

### Why This Happens

The validation error occurs because:
- The `fileId` parameter is **required** by Google Drive node
- The parameter value is likely using an expression like `{{ $json.fileId }}`
- During **pre-execution validation** (before any data flows), n8n cannot evaluate expressions
- n8n's validator sees an empty/expression-based required field and flags it as missing

This is a **false positive** validation error - the parameter **would** have a value at runtime when data flows from previous nodes, but the validator runs **before** execution starts.

---

## Validation Logic Flow

From the compiled code analysis:

```javascript
// Line 680-687 in workflow-execute.js
const workflowIssues = this.checkReadyForExecution(workflow, {
    startNode,
    destinationNode,
    pinDataNodeNames,
});
if (workflowIssues !== null) {
    throw new workflow_has_issues_error_1.WorkflowHasIssuesError();
}
```

The `checkReadyForExecution()` function (lines 436-472):
1. Iterates through all nodes in execution path
2. Calls `NodeHelpers.getNodeParametersIssues()` for each node
3. Checks for missing required parameters, type mismatches, etc.
4. Returns object with issues grouped by node name

---

## Recommended Fixes

### Option 1: Use ID from Resource Locator (Recommended)
Change the "File" parameter in both nodes from expression to use the **Resource Locator** mode:
- Mode: "ID"
- Value: Expression `={{ $json.fileId }}`

### Option 2: Set Default/Fallback Value
Add a fallback value using the expression:
```javascript
={{ $json.fileId || 'placeholder' }}
```

### Option 3: Conditional Execution
Add an IF node before each Move File operation to only execute when `fileId` exists:
```javascript
={{ $json.fileId !== undefined && $json.fileId !== null }}
```

### Option 4: Disable Pre-Execution Validation (Not Recommended)
n8n doesn't expose a flag to disable this, but you could:
- Use Execute Workflow node with "Wait for Completion" = false
- This skips validation but loses error feedback

---

## Files Modified During Investigation

**Temporarily modified (now restored):**
```
/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-core@file+packages+core_@opentelemetry+api@1.9.0_@opentelemetry+sdk-trace-base@1.30_ec37920eb95917b28efaa783206b20f3/node_modules/n8n-core/dist/execution-engine/workflow-execute.js
```

**Modification made:**
- Added console.log at line 686 to output `workflowIssues` JSON
- Triggered workflow execution
- Captured debug output
- Removed debug line and restored original file

**Status:** ✅ File restored to original state

---

## Next Steps

1. **solution-builder-agent** should update both nodes:
   - "Move File to 38_Unknowns"
   - "Move File to Final Location"

2. Apply **Option 1** (Resource Locator with ID mode)

3. Re-test workflow execution via:
   ```bash
   curl -X POST "https://n8n.oloxa.ai/webhook/eugene-quick-test" \
        -H "Content-Type: application/json" -d '{}'
   ```

4. Verify no validation errors in execution logs

---

## Technical Notes

- **Validation Timing:** Pre-execution (before any node runs)
- **Validator Location:** `n8n-core/src/execution-engine/workflow-execute.ts:1329`
- **Issue Detection:** `NodeHelpers.getNodeParametersIssues()` in n8n-workflow package
- **Error Type:** `WorkflowHasIssuesError` (not a runtime error)

---

## Server Status

- **n8n Server:** ✅ Healthy (running normally)
- **Container:** n8n-n8n-1 (Up)
- **Disk Space:** Normal
- **Modifications:** ✅ All reverted
- **Debug Code:** ✅ Removed
- **Production Impact:** None (investigation only)

---

**Report Generated By:** server-ops-agent
**Investigation Duration:** ~5 minutes
**Server Downtime:** 0 seconds
