# Test Orchestrator Fixes - Ready to Apply

## Summary

Two critical fixes ready for Test Orchestrator workflow (ID: K1kYeyvokVHtOhoE):

1. **HP-02 Idempotency**: Prevent duplicate folder creation for existing clients
2. **EC-08 Special Characters**: Fix Google Sheets lookup to handle apostrophes

## Detailed Changes

### Fix 1: Route to Chunk 0 Node

**Current Code:**
```javascript
const data = $input.first().json;

if (data.simulateError) {
  return [];
} else {
  return { json: data };
}
```

**New Code:**
```javascript
const data = $input.first().json;

if (data.simulateError || data.clientExists) {
  // Skip Chunk 0 for errors AND existing clients
  return [];
} else {
  // Only run Chunk 0 for new clients
  return { json: data };
}
```

**Impact:**
- HP-02 test will now skip Chunk 0 entirely when clientExists=true
- No more duplicate folder creation for existing clients
- Chunk 0 still runs normally for new clients (HP-01)

### Fix 2: Google Sheets Lookup Refactor

**Current Setup:**
- "Check Client Registry" node uses Google Sheets filter
- Filter: `lookupColumn: "Client_Name"`, `lookupValue: "={{ ... }}"`
- **Problem:** Fails with special characters like apostrophes

**New Setup:**

**Step 1:** Update "Check Client Registry" node
- Change operation from "read" (with filter) to "readRows" (read all rows)
- Remove filter parameters
- Keep same document and sheet references

**Step 2:** Add new "Find Matching Client" JavaScript node
- Type: Code node (n8n-nodes-base.code)
- Position: Between "Check Client Registry" and "Merge All Results"
- Code:
```javascript
// Filter the registry rows to find matching client
const allRows = $input.all();
const targetClientName = $('Prepare Test Data').first().json.clientName;

// Find matching row (case-sensitive exact match)
const matchingRow = allRows.find(item => {
  const row = item.json;
  return row.Client_Name === targetClientName;
});

// Return the matching row or empty object if not found
return matchingRow ? { json: matchingRow.json } : { json: {} };
```

**Step 3:** Rewire connections
- Remove: "Check Client Registry" → "Merge All Results"
- Add: "Check Client Registry" → "Find Matching Client"
- Add: "Find Matching Client" → "Merge All Results"

**Impact:**
- EC-08 test will now successfully find "O'Brien Muller GmbH"
- All other client lookups continue working
- JavaScript string comparison handles special characters correctly

## Operations to Execute

Using `mcp__n8n-mcp__n8n_update_partial_workflow`:

```json
{
  "id": "K1kYeyvokVHtOhoE",
  "operations": [
    {
      "type": "updateNode",
      "nodeName": "Route to Chunk 0",
      "updates": {
        "parameters": {
          "jsCode": "..."
        }
      }
    },
    {
      "type": "updateNode",
      "nodeName": "Check Client Registry",
      "updates": {
        "parameters": {
          "operation": "readRows",
          "options": {}
        }
      }
    },
    {
      "type": "addNode",
      "node": {
        "name": "Find Matching Client",
        "type": "n8n-nodes-base.code",
        "parameters": {...}
      }
    },
    {
      "type": "removeConnection",
      "source": "Check Client Registry",
      "target": "Merge All Results"
    },
    {
      "type": "addConnection",
      "source": "Check Client Registry",
      "target": "Find Matching Client"
    },
    {
      "type": "addConnection",
      "source": "Find Matching Client",
      "target": "Merge All Results"
    }
  ]
}
```

## Testing Plan

### After applying fixes:

1. **Test HP-02 (Existing Client)**
   - Run with clientExists=true
   - Verify Chunk 0 is skipped
   - Verify no duplicate folders created
   - Verify Chunk 1 and Chunk 2 run normally

2. **Test EC-08 (Special Characters)**
   - Run with clientName="O'Brien Muller GmbH"
   - Verify "Find Matching Client" returns correct registry row
   - Verify no errors from apostrophe in name
   - Verify workflow completes successfully

3. **Regression Test HP-01 (New Client)**
   - Run with clientExists=false
   - Verify Chunk 0 still runs normally
   - Verify new client folders are created
   - Ensure fix 1 doesn't break new client flow

## Rollback Plan

If issues occur after applying:

1. Export current workflow as `test_orchestrator_v1.3_BACKUP_[datetime].json`
2. Apply fixes
3. If problems occur:
   - Revert "Route to Chunk 0" code to original
   - Remove "Find Matching Client" node
   - Restore "Check Client Registry" to filter operation
   - Reconnect "Check Client Registry" → "Merge All Results"

## Files

- Fix documentation: `/Users/swayclarke/coding_stuff/test_orchestrator_fixes.md`
- Operations JSON: `/Users/swayclarke/coding_stuff/workflow_update_operations.json`
- This file: `/Users/swayclarke/coding_stuff/FIXES_READY_TO_APPLY.md`

## Ready to Apply?

All operations are prepared and validated. Ready to execute when you confirm.
