# W7 Downloads Monitor - Manual Connection Fix Instructions

## Problem Summary

The IF nodes "Route Expensify to W6" and "Check if Sway Invoice" have incorrect connection formats that prevent items from flowing through the FALSE output.

**Current structure (WRONG - both outputs in same array):**
```json
"Route Expensify to W6": {
  "main": [
    [
      {"node": "Prepare W6 Input", "type": "main", "index": 0},
      {"node": "Check if Sway Invoice", "type": "main", "index": 0}
    ]
  ]
}
```

**Correct structure (separate arrays for TRUE and FALSE):**
```json
"Route Expensify to W6": {
  "main": [
    [{"node": "Prepare W6 Input", "type": "main", "index": 0}],  // TRUE output
    [{"node": "Check if Sway Invoice", "type": "main", "index": 0}]  // FALSE output
  ]
}
```

## Manual Fix Steps (In n8n UI)

### Fix "Route Expensify to W6" Node

1. Open W7 Downloads Folder Monitor workflow in n8n UI
2. Find "Route Expensify to W6" IF node (should be at position X: 1168, Y: 0)
3. Delete both output connections (to "Prepare W6 Input" and "Check if Sway Invoice")
4. Reconnect properly:
   - **TRUE output (green dot)** → Connect to "Prepare W6 Input"
   - **FALSE output (red dot)** → Connect to "Check if Sway Invoice"

### Fix "Check if Sway Invoice" Node

1. Find "Check if Sway Invoice" IF node (position X: 1392, Y: 312)
2. Delete both output connections (to "Download Sway Invoice" and "Download File")
3. Reconnect properly:
   - **TRUE output (green dot)** → Connect to "Download Sway Invoice"
   - **FALSE output (red dot)** → Connect to "Download File"

### Verify Connections

After fixing:
1. Save the workflow
2. Check execution #7209 (or run a new test)
3. Verify that items flow through:
   - Route Expensify FALSE output → Check if Sway Invoice receives items
   - Check if Sway Invoice FALSE output → Download File receives items

## Root Cause

The n8n MCP tool's `addConnection` operation with `sourceOutputIndex: 0` and `sourceOutputIndex: 1` is merging both connections into a single array instead of creating separate arrays for TRUE (index 0) and FALSE (index 1) outputs. This appears to be a bug in how the MCP tool handles IF node connections.

## Alternative: Browser-Ops-Agent Fix

If manual fix is tedious, browser-ops-agent can be used to:
1. Navigate to W7 workflow in n8n UI
2. Click on each IF node
3. Delete wrong connections
4. Re-add connections by dragging from correct output dots to target nodes

## Expected Result

After fix, items should flow:
- Expensify files → Route Expensify TRUE → Prepare W6 Input → W6
- Non-expensify files → Route Expensify FALSE → Check if Sway Invoice
- Sway invoices → Check if Sway Invoice TRUE → Download Sway Invoice → Invoice Pool
- Other files → Check if Sway Invoice FALSE → Download File → Anthropic extraction
