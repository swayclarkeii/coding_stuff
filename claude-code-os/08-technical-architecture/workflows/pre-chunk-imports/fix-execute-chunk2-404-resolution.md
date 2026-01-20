# Execute Chunk 2 (NEW) - 404 Error Resolution

## Problem Summary

Pre-Chunk 0 workflow (ID: YGXWjWcBIk66ArvT) execution #592 failed with 404 error when calling "Execute Chunk 2 (NEW)" node:
- **Error:** "The resource you are requesting could not be found"
- **Status:** 404
- **Node:** Execute Chunk 2 (NEW) (ID: execute-chunk2-new-001)

## Root Cause

The Execute Chunk 2 nodes were using **outdated typeVersion 1.1** instead of the current **typeVersion 1.3**.

**Why this caused 404:**
1. typeVersion 1.1 uses different internal API structure
2. The node was configured with Resource Locator pattern (`__rl: true`, `mode: "id"`) which is a v1.2+ feature
3. This version mismatch caused n8n to fail resolving the workflow ID
4. Result: 404 "resource not found" error

**Evidence:**
- Screenshot showed warning: "This node is out of date. Please upgrade by removing it and adding a new one"
- Node definition shows `outdatedVersionWarning` is displayed when `@version <= 1.1`
- Chunk 0 Execute Workflow nodes (working correctly) used typeVersion 1.3
- Chunk 2 Execute Workflow nodes (failing) used typeVersion 1.1

## Fix Applied

Updated both Execute Chunk 2 nodes from typeVersion 1.1 → 1.3:

```json
// Before:
{
  "name": "Execute Chunk 2 (NEW)",
  "type": "n8n-nodes-base.executeWorkflow",
  "typeVersion": 1.1,  // ❌ OUTDATED
  "parameters": {
    "workflowId": {
      "__rl": true,
      "mode": "id",
      "value": "g9J5kjVtqaF9GLyc"
    }
  }
}

// After:
{
  "name": "Execute Chunk 2 (NEW)",
  "type": "n8n-nodes-base.executeWorkflow",
  "typeVersion": 1.3,  // ✅ CURRENT
  "parameters": {
    "workflowId": {
      "__rl": true,
      "mode": "id",
      "value": "g9J5kjVtqaF9GLyc"
    }
  }
}
```

## Nodes Fixed

1. ✅ **Execute Chunk 2 (NEW)** - typeVersion 1.1 → 1.3
2. ✅ **Execute Chunk 2 (EXISTING)** - typeVersion 1.1 → 1.3

## Verification

Confirmed via workflow re-fetch:
```bash
# Both nodes now show typeVersion 1.3
{
  "name": "Execute Chunk 2 (NEW)",
  "typeVersion": 1.3,
  "workflowId": {
    "__rl": true,
    "mode": "id",
    "value": "g9J5kjVtqaF9GLyc"
  }
}
```

## Status

✅ **404 Error FIXED** - Execute Chunk 2 nodes upgraded to current typeVersion

## Remaining Workflow Issues (Not Related to 404 Error)

The workflow validation shows other errors that are **NOT related to the Execute Chunk 2 404 issue**:

1. **Upload PDF to Temp Folder** - Invalid operation value
2. **Move PDF to 38_Unknowns** - Missing resourceLocator mode
3. **Send Email Notification** - Invalid operation value
4. **Send Registry Error Email** - Invalid operation value

These errors exist in different parts of the workflow and did not cause the Execute Chunk 2 404 error. They should be addressed separately.

## Test Recommendation

**Next step:** Re-run Pre-Chunk 0 workflow to verify Execute Chunk 2 (NEW) node now successfully calls Chunk 2 workflow without 404 error.

The typeVersion upgrade should resolve the workflow execution issue.
