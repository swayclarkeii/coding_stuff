# Phase 0: Automated Test Trigger Implementation

**Project**: Sway's Expense System
**Version**: v1.2.4
**Date**: January 3, 2026
**Status**: Ready for Implementation

---

## Overview

Add webhook triggers to Workflows 2 and 3 to enable Claude Code to execute on-demand tests via the `n8n_test_workflow` MCP tool.

**Current State**: W2 and W3 only have schedule triggers (no programmatic testing capability)
**Target State**: Both workflows have webhook triggers alongside schedule triggers for testing

---

## Implementation Steps

### Step 1: Add Webhook to W2 (Gmail Receipt Monitor)

**Workflow ID**: `dHbwemg7hEB4vDmC`

**Command** (use in main Claude Code session):
```javascript
// Call this MCP tool:
mcp__n8n-mcp__n8n_update_partial_workflow

// With these parameters:
{
  "id": "dHbwemg7hEB4vDmC",
  "operations": [
    {
      "type": "addNode",
      "node": {
        "name": "Test Trigger - Webhook",
        "type": "n8n-nodes-base.webhook",
        "parameters": {
          "path": "test-expense-w2",
          "httpMethod": "POST",
          "responseMode": "lastNode",
          "options": {}
        },
        "position": [0, -200],
        "typeVersion": 2
      }
    },
    {
      "type": "addConnection",
      "source": "Test Trigger - Webhook",
      "sourceOutput": "main",
      "target": "Load Vendor Patterns",
      "targetInput": "main"
    }
  ]
}
```

**Expected Result**:
- New webhook node at position [0, -200] (above schedule trigger)
- Connected to "Load Vendor Patterns" (same as schedule trigger)
- Webhook path: `/test-expense-w2`

---

### Step 2: Add Webhook to W3 (Transaction-Receipt Matching)

**Workflow ID**: `waPA94G2GXawDlCa`

**Command** (use in main Claude Code session):
```javascript
// Call this MCP tool:
mcp__n8n-mcp__n8n_update_partial_workflow

// With these parameters:
{
  "id": "waPA94G2GXawDlCa",
  "operations": [
    {
      "type": "addNode",
      "node": {
        "name": "Test Trigger - Webhook",
        "type": "n8n-nodes-base.webhook",
        "parameters": {
          "path": "test-expense-w3",
          "httpMethod": "POST",
          "responseMode": "lastNode",
          "options": {}
        },
        "position": [240, 100],
        "typeVersion": 2
      }
    },
    {
      "type": "addConnection",
      "source": "Test Trigger - Webhook",
      "sourceOutput": "main",
      "target": "Get Unmatched Transactions",
      "targetInput": "main"
    }
  ]
}
```

**Expected Result**:
- New webhook node at position [240, 100] (above schedule trigger)
- Connected to "Get Unmatched Transactions" (same as schedule trigger)
- Webhook path: `/test-expense-w3`

---

### Step 3: Test W2 Webhook

**Command**:
```javascript
// Call this MCP tool:
mcp__n8n-mcp__n8n_test_workflow

// With these parameters:
{
  "id": "dHbwemg7hEB4vDmC",
  "data": {
    "testMode": true
  }
}
```

**Validation**:
1. Check execution completes successfully
2. Verify no errors in execution logs
3. Confirm workflow reached "Log Receipt in Database" node
4. Note execution ID for reference

**To check execution**:
```javascript
// Call this MCP tool:
mcp__n8n-mcp__n8n_executions

// With these parameters:
{
  "workflowId": "dHbwemg7hEB4vDmC",
  "limit": 1
}
```

---

### Step 4: Test W3 Webhook

**Command**:
```javascript
// Call this MCP tool:
mcp__n8n-mcp__n8n_test_workflow

// With these parameters:
{
  "id": "waPA94G2GXawDlCa",
  "data": {
    "testMode": true
  }
}
```

**Validation**:
1. Check execution completes successfully
2. Verify no errors in execution logs
3. Confirm workflow processes unmatched transactions
4. Note execution ID for reference

**To check execution**:
```javascript
// Call this MCP tool:
mcp__n8n-mcp__n8n_executions

// With these parameters:
{
  "workflowId": "waPA94G2GXawDlCa",
  "limit": 1
}
```

---

## Webhook URLs (After Implementation)

Once webhooks are added, they will be accessible at:

- **W2 (Gmail Monitor)**: `https://[your-n8n-instance]/webhook/test-expense-w2`
- **W3 (Transaction Matching)**: `https://[your-n8n-instance]/webhook/test-expense-w3`

Replace `[your-n8n-instance]` with your actual n8n instance URL.

---

## Troubleshooting

### If Node Addition Fails

**Error**: "Target node 'Load Vendor Patterns' not found"
**Solution**: Verify target node name exactly matches in W2
```javascript
// Get current workflow structure:
mcp__n8n-mcp__n8n_get_workflow({ "id": "dHbwemg7hEB4vDmC" })
// Check node names in response
```

**Error**: "Target node 'Get Unmatched Transactions' not found"
**Solution**: Verify target node name exactly matches in W3
```javascript
// Get current workflow structure:
mcp__n8n-mcp__n8n_get_workflow({ "id": "waPA94G2GXawDlCa" })
// Check node names in response
```

### If Test Execution Fails

**Issue**: Webhook returns 404
**Solution**: Ensure workflow is activated after adding webhook node

**Issue**: Execution starts but errors immediately
**Solution**: Check if workflow has valid credentials configured

**Issue**: Timeout or no response
**Solution**: Check n8n server logs, may be processing slowly

---

## Verification Checklist

After completing all steps, verify:

- [ ] W2 has "Test Trigger - Webhook" node visible in workflow editor
- [ ] W2 webhook is connected to "Load Vendor Patterns"
- [ ] W2 test execution completes successfully (Step 3)
- [ ] W3 has "Test Trigger - Webhook" node visible in workflow editor
- [ ] W3 webhook is connected to "Get Unmatched Transactions"
- [ ] W3 test execution completes successfully (Step 4)
- [ ] Both webhook URLs are documented
- [ ] Both schedule triggers still active (not replaced)
- [ ] VERSION_LOG.md updated to v1.2.4

---

## Expected Outcomes

**Success Criteria**:
1. Both workflows have dual triggers (schedule + webhook)
2. Webhooks respond within 2-5 seconds when triggered
3. Executions complete without errors
4. Claude Code can now run on-demand tests via MCP tools

**Benefits**:
- No more waiting for scheduled runs (6:00 AM CET)
- Immediate feedback when testing changes
- Ability to test specific scenarios on-demand
- Foundation for automated integration testing

---

## Next Steps (After Phase 0)

Once webhooks are operational:

1. **Phase 1**: Build comprehensive test suite
   - Sample data generators
   - Validation scripts
   - End-to-end test scenarios

2. **Phase 2**: Integration testing framework
   - W1 → W2 → W3 flow testing
   - Error handling validation
   - Edge case coverage

3. **Phase 3**: Automated monitoring
   - Daily health checks via webhooks
   - Alert on execution failures
   - Performance tracking

---

## Files to Update

After successful implementation:

1. **VERSION_LOG.md** → Update to v1.2.4 (see next section)
2. **This file** → Mark as "Complete" in status

---

## VERSION_LOG.md Update

Add this entry to VERSION_LOG.md:

```markdown
### v1.2.4 - Webhook Test Triggers
**Date**: January 3, 2026
**Status**: ✅ Complete
**Phase**: Testing & Validation
**Efficiency Score**: 4.8/10 (unchanged)

#### What Changed
Added webhook triggers to W2 and W3 for programmatic testing via Claude Code MCP tools.

#### Components Modified
1. **Workflow 2 (Gmail Receipt Monitor)** - `dHbwemg7hEB4vDmC`
   - Added "Test Trigger - Webhook" node
   - Path: `/test-expense-w2`
   - Position: [0, -200] (above schedule trigger)
   - Connected to: "Load Vendor Patterns"

2. **Workflow 3 (Transaction-Receipt Matching)** - `waPA94G2GXawDlCa`
   - Added "Test Trigger - Webhook" node
   - Path: `/test-expense-w3`
   - Position: [240, 100] (above schedule trigger)
   - Connected to: "Get Unmatched Transactions"

#### Testing Results
- W2 test execution: [EXECUTION_ID] - ✅ Success
- W3 test execution: [EXECUTION_ID] - ✅ Success
- Average response time: [X] seconds
- No errors encountered

#### What This Enables
- On-demand testing via `mcp__n8n-mcp__n8n_test_workflow` tool
- Immediate feedback during development
- Foundation for automated test suite
- No need to wait for 6:00 AM scheduled runs

#### Known Limitations
- Webhooks are unauthenticated (public URLs)
- No rate limiting configured
- Test mode flag (`testMode: true`) not currently utilized in workflows

#### Files Updated
- Workflow 2: n8n ID `dHbwemg7hEB4vDmC` (version counter: [NEW_COUNT])
- Workflow 3: n8n ID `waPA94G2GXawDlCa` (version counter: [NEW_COUNT])
- Updated: 2026-01-03T[TIME]Z

#### Next Steps
- Phase 1: Build comprehensive test suite with sample data
- Phase 2: Add webhook authentication for security
- Phase 3: Implement automated daily health checks
```

---

## Implementation Notes

**Important**:
- Do NOT remove or modify existing schedule triggers
- Webhooks are ADDITIONAL triggers, not replacements
- Both triggers should coexist in parallel
- Schedule triggers run daily at 6:00 AM CET (production)
- Webhook triggers run on-demand (testing only)

**Design Decisions**:
- `responseMode: "lastNode"` - Webhook waits for workflow to complete before responding
- `httpMethod: "POST"` - Standard for triggering actions
- Position coordinates chosen to avoid overlap with existing nodes

**Security Considerations** (Future):
- Currently webhooks are public (no authentication)
- For production use, consider adding:
  - API key authentication
  - IP whitelisting
  - Rate limiting
- For testing purposes, public webhooks are acceptable

---

## Rollback Instructions

If webhooks cause issues:

1. **Remove webhook from W2**:
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow({
  "id": "dHbwemg7hEB4vDmC",
  "operations": [
    {
      "type": "deleteNode",
      "nodeName": "Test Trigger - Webhook"
    }
  ]
})
```

2. **Remove webhook from W3**:
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow({
  "id": "waPA94G2GXawDlCa",
  "operations": [
    {
      "type": "deleteNode",
      "nodeName": "Test Trigger - Webhook"
    }
  ]
})
```

3. **Revert VERSION_LOG.md** to v1.2.3

---

## Contact & Support

For questions about this implementation:
- Review: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/VERSION_LOG.md`
- Check: n8n workflow editor for visual confirmation
- Test: Use `mcp__n8n-mcp__n8n_validate_workflow` to check structure

**Created**: January 3, 2026
**Owner**: Sway (swayclarkeii@gmail.com)
**Agent**: solution-builder-agent v1.0
