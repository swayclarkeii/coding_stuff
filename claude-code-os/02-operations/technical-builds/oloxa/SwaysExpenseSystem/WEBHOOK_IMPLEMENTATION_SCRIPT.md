# Webhook Implementation Script

**Date**: January 3, 2026
**Purpose**: Step-by-step commands to add webhook test triggers to all 3 expense workflows
**Status**: Ready for execution

---

## Pre-Implementation Checklist

- [ ] Confirm n8n instance is accessible
- [ ] Verify n8n MCP server is connected
- [ ] Backup current workflows (automatic in n8n version history)
- [ ] Review VERSION_LOG.md current state (v1.2.3)

---

## Implementation Commands

### Step 1: Add Webhook to Workflow 1 (PDF Intake & Parsing)

**Workflow ID**: `MPjDdVMI88158iFW`

**Command**: Use n8n MCP `n8n_update_partial_workflow` tool

**Operations**:
```json
{
  "id": "MPjDdVMI88158iFW",
  "operations": [
    {
      "type": "addNode",
      "node": {
        "name": "Manual Test Trigger",
        "type": "n8n-nodes-base.webhook",
        "typeVersion": 2,
        "position": [250, 100],
        "parameters": {
          "path": "test-expense-w1",
          "httpMethod": "POST",
          "responseMode": "lastNode",
          "options": {}
        },
        "id": "webhook-test-1"
      }
    },
    {
      "type": "addNode",
      "node": {
        "name": "Prepare File Data",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [400, 100],
        "parameters": {
          "jsCode": "// Transform webhook payload to match Google Drive trigger output\nconst fileId = $json.fileId || $json.body?.fileId;\n\nif (!fileId) {\n  throw new Error('Missing fileId in webhook payload. Send: {\"fileId\": \"your-google-drive-file-id\"}');\n}\n\nreturn {\n  json: {\n    id: fileId,\n    testMode: true\n  }\n};"
        },
        "id": "code-prepare-file-1"
      }
    },
    {
      "type": "addConnection",
      "source": "Manual Test Trigger",
      "sourceOutput": "main",
      "target": "Prepare File Data",
      "targetInput": "main"
    },
    {
      "type": "addConnection",
      "source": "Prepare File Data",
      "sourceOutput": "main",
      "target": "Download PDF",
      "targetInput": "main"
    }
  ]
}
```

**Expected Result**:
- 2 new nodes added
- 2 new connections created
- Existing Google Drive trigger unchanged
- Webhook available at `/webhook/test-expense-w1`

---

### Step 2: Add Webhook to Workflow 2 (Gmail Receipt Monitor)

**Workflow ID**: `dHbwemg7hEB4vDmC`

**Command**: Use n8n MCP `n8n_update_partial_workflow` tool

**Operations**:
```json
{
  "id": "dHbwemg7hEB4vDmC",
  "operations": [
    {
      "type": "addNode",
      "node": {
        "name": "Manual Test Trigger",
        "type": "n8n-nodes-base.webhook",
        "typeVersion": 2,
        "position": [250, 100],
        "parameters": {
          "path": "test-expense-w2",
          "httpMethod": "POST",
          "responseMode": "lastNode",
          "options": {}
        },
        "id": "webhook-test-2"
      }
    },
    {
      "type": "addConnection",
      "source": "Manual Test Trigger",
      "sourceOutput": "main",
      "target": "Load Vendor Patterns",
      "targetInput": "main"
    }
  ]
}
```

**Expected Result**:
- 1 new node added
- 1 new connection created
- Existing Schedule trigger unchanged
- Webhook available at `/webhook/test-expense-w2`

---

### Step 3: Add Webhook to Workflow 3 (Transaction-Receipt Matching)

**Workflow ID**: `waPA94G2GXawDlCa`

**Command**: Use n8n MCP `n8n_update_partial_workflow` tool

**Operations**:
```json
{
  "id": "waPA94G2GXawDlCa",
  "operations": [
    {
      "type": "addNode",
      "node": {
        "name": "Manual Test Trigger",
        "type": "n8n-nodes-base.webhook",
        "typeVersion": 2,
        "position": [250, 100],
        "parameters": {
          "path": "test-expense-w3",
          "httpMethod": "POST",
          "responseMode": "lastNode",
          "options": {}
        },
        "id": "webhook-test-3"
      }
    },
    {
      "type": "addConnection",
      "source": "Manual Test Trigger",
      "sourceOutput": "main",
      "target": "Get Unmatched Transactions",
      "targetInput": "main"
    },
    {
      "type": "addConnection",
      "source": "Manual Test Trigger",
      "sourceOutput": "main",
      "target": "Get Unmatched Receipts",
      "targetInput": "main"
    }
  ]
}
```

**Expected Result**:
- 1 new node added
- 2 new connections created (split to both read nodes)
- Existing Schedule trigger unchanged
- Webhook available at `/webhook/test-expense-w3`

---

## Validation Steps

After each workflow update:

### 1. Verify Workflow Structure
Use `n8n_get_workflow` to confirm new nodes exist:
```json
{
  "id": "MPjDdVMI88158iFW"
}
```

Check for:
- [ ] "Manual Test Trigger" node exists
- [ ] Connections to workflow logic are correct
- [ ] Original triggers still connected

### 2. Test Webhook Activation
Use `n8n_validate_workflow` to check for errors:
```json
{
  "id": "MPjDdVMI88158iFW"
}
```

### 3. Get Webhook URLs
Navigate to n8n UI or use n8n API to retrieve full webhook URLs:
- Production URL format: `https://[n8n-instance]/webhook/test-expense-w1`
- Test URL format: `https://[n8n-instance]/webhook-test/test-expense-w1`

---

## Test Execution

### Test Workflow 1
```bash
# Get a test PDF file ID from Google Drive
FILE_ID="your_test_pdf_file_id"

# Trigger webhook
curl -X POST https://[n8n-instance]/webhook/test-expense-w1 \
  -H "Content-Type: application/json" \
  -d "{\"fileId\": \"$FILE_ID\"}"
```

**Expected behavior**:
1. Webhook receives fileId
2. Prepare File Data transforms it
3. Download PDF executes
4. Full workflow processes the PDF
5. Database entries created
6. PDF moved to archive

### Test Workflow 2
```bash
# Trigger webhook (no parameters needed)
curl -X POST https://[n8n-instance]/webhook/test-expense-w2 \
  -H "Content-Type: application/json" \
  -d '{"testMode": true}'
```

**Expected behavior**:
1. Webhook triggers
2. Load Vendor Patterns executes
3. Gmail search runs for all 6 vendors
4. Receipts downloaded and logged
5. Database entries created

### Test Workflow 3
```bash
# Trigger webhook (no parameters needed)
curl -X POST https://[n8n-instance]/webhook/test-expense-w3 \
  -H "Content-Type: application/json" \
  -d '{"testMode": true}'
```

**Expected behavior**:
1. Webhook triggers
2. Both "Get Unmatched" nodes execute
3. Matching algorithm runs
4. Database updated
5. Receipts moved to organized folders

---

## Post-Implementation Tasks

- [ ] Export updated workflow JSONs to `/N8N_Blueprints/v1_foundation/`
- [ ] Update VERSION_LOG.md to v1.2.4 (Testing Infrastructure)
- [ ] Document webhook URLs in TESTING_INFRASTRUCTURE.md
- [ ] Add test payloads to documentation
- [ ] Run end-to-end test of all 3 workflows
- [ ] Update efficiency score if testing speed improves

---

## Rollback Procedure

If webhooks cause issues:

1. **Via n8n UI**:
   - Open workflow
   - Delete "Manual Test Trigger" node
   - Delete "Prepare File Data" node (W1 only)
   - Save workflow

2. **Via n8n MCP**:
   ```json
   {
     "id": "MPjDdVMI88158iFW",
     "operations": [
       {
         "type": "removeNode",
         "nodeName": "Manual Test Trigger"
       },
       {
         "type": "removeNode",
         "nodeName": "Prepare File Data"
       }
     ]
   }
   ```

3. **Via Version History**:
   - n8n UI → Workflow → ... menu → Versions
   - Select version before webhook addition
   - Click Restore

---

## Success Criteria

Testing infrastructure is complete when:

- [ ] All 3 workflows have webhook triggers
- [ ] Webhooks can be triggered independently
- [ ] Production triggers remain functional
- [ ] Test executions complete successfully
- [ ] Webhook URLs documented
- [ ] Test payloads documented
- [ ] Rollback tested and verified
- [ ] VERSION_LOG.md updated to v1.2.4

---

## Notes

- Webhooks are parallel entry points - they don't replace existing triggers
- Test mode flag can be used in workflow logic for conditional behavior
- Consider adding authentication to webhooks in production
- Webhook URLs persist across n8n restarts
- Each workflow activation creates a new webhook instance

---

## References

- n8n Webhook Node Docs: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/
- n8n MCP Documentation: See CLAUDE.md for tool usage
- Workflow Blueprints: `/N8N_Blueprints/v1_foundation/`
- Testing Guide: `/TESTING_GUIDE.md`
