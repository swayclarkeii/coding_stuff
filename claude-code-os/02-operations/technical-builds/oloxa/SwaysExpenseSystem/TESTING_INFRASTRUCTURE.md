# Expense System - Testing Infrastructure

**Project**: Sway's Expense System
**Purpose**: Enable rapid test-iterate cycles with manual webhook triggers
**Date Created**: January 3, 2026
**Status**: Implementation in progress

---

## Problem Statement

The current expense system has a critical testing bottleneck:

- **Workflow 1** (PDF Intake & Parsing): Google Drive trigger only - can't test on demand
- **Workflow 2** (Gmail Receipt Monitor): Schedule trigger (daily at 6 AM) - can't test until tomorrow
- **Workflow 3** (Transaction-Receipt Matching): Schedule trigger (daily) - can't test immediately

**Impact**: Unable to test → validate → iterate rapidly. Must wait hours or days between tests.

---

## Solution: Webhook Test Triggers

Add **parallel webhook triggers** to all 3 workflows that coexist with production triggers:

### Architecture Principle
- **Production triggers** remain active (Google Drive, Schedule)
- **Test webhooks** provide manual on-demand execution
- Both paths merge into the same workflow logic
- No production impact - webhooks are separate entry points

---

## Implementation Plan

### Workflow 1: PDF Intake & Parsing (MPjDdVMI88158iFW)

**New Nodes Added:**
1. **Manual Test Trigger** (Webhook)
   - Path: `/test-expense-w1`
   - Method: POST
   - Payload: `{"fileId": "Google Drive file ID"}`
   - Position: [250, 100]

2. **Prepare File Data** (Code node)
   - Transforms webhook payload to match Google Drive trigger output
   - Validates fileId exists
   - Position: [400, 100]

**Connections:**
- Webhook → Prepare File Data → Download PDF (existing node)
- Google Drive Trigger → Download PDF (existing, unchanged)

**Test Usage:**
```bash
curl -X POST https://your-n8n-instance.com/webhook/test-expense-w1 \
  -H "Content-Type: application/json" \
  -d '{"fileId": "1abc123xyz"}'
```

---

### Workflow 2: Gmail Receipt Monitor (dHbwemg7hEB4vDmC)

**New Nodes Added:**
1. **Manual Test Trigger** (Webhook)
   - Path: `/test-expense-w2`
   - Method: POST
   - Payload: `{"testMode": true}` (optional searchQuery override)
   - Position: [250, 100]

**Connections:**
- Webhook → Load Vendor Patterns (existing node)
- Schedule Trigger → Load Vendor Patterns (existing, unchanged)

**Test Usage:**
```bash
curl -X POST https://your-n8n-instance.com/webhook/test-expense-w2 \
  -H "Content-Type: application/json" \
  -d '{"testMode": true}'
```

---

### Workflow 3: Transaction-Receipt Matching (waPA94G2GXawDlCa)

**New Nodes Added:**
1. **Manual Test Trigger** (Webhook)
   - Path: `/test-expense-w3`
   - Method: POST
   - Payload: `{"testMode": true}`
   - Position: [250, 100]

**Connections:**
- Webhook → Get Unmatched Transactions (existing node)
- Webhook → Get Unmatched Receipts (existing node)
- Schedule Trigger → Get Unmatched Transactions (existing, unchanged)
- Schedule Trigger → Get Unmatched Receipts (existing, unchanged)

**Test Usage:**
```bash
curl -X POST https://your-n8n-instance.com/webhook/test-expense-w3 \
  -H "Content-Type: application/json" \
  -d '{"testMode": true}'
```

---

## Testing Workflow

### Standard Test Cycle

1. **Prepare Test Data**
   - Upload test PDF to Google Drive (for W1)
   - Send test receipt email (for W2)
   - Ensure unmatched transactions/receipts exist (for W3)

2. **Trigger Webhook**
   - Use curl or n8n MCP `n8n_test_workflow` tool
   - Pass required payload

3. **Validate Results**
   - Check n8n execution logs
   - Verify database entries (Google Sheets)
   - Confirm file movements in Google Drive

4. **Iterate**
   - Fix issues
   - Re-trigger immediately
   - No waiting for schedules

---

## Webhook URLs

Once deployed, webhooks will be available at:

- **Workflow 1 (PDF Intake)**: `https://[n8n-instance]/webhook/test-expense-w1`
- **Workflow 2 (Gmail Monitor)**: `https://[n8n-instance]/webhook/test-expense-w2`
- **Workflow 3 (Matching)**: `https://[n8n-instance]/webhook/test-expense-w3`

**Note**: Replace `[n8n-instance]` with actual n8n deployment URL.

---

## Test Payloads Reference

### Workflow 1: PDF Intake
```json
{
  "fileId": "1abc123xyz_your_google_drive_file_id"
}
```

**How to get fileId:**
1. Upload PDF to Google Drive
2. Right-click → Get Link
3. Extract ID from URL: `https://drive.google.com/file/d/[THIS_IS_THE_FILE_ID]/view`

### Workflow 2: Gmail Receipt Monitor
```json
{
  "testMode": true
}
```

**Optional custom search:**
```json
{
  "testMode": true,
  "searchQuery": "from:billing@anthropic.com has:attachment"
}
```

### Workflow 3: Transaction-Receipt Matching
```json
{
  "testMode": true
}
```

---

## Implementation Status

| Workflow | Webhook Added | Tested | Status |
|----------|---------------|--------|--------|
| W1: PDF Intake | ⏳ Pending | ❌ | Not started |
| W2: Gmail Monitor | ⏳ Pending | ❌ | Not started |
| W3: Matching | ⏳ Pending | ❌ | Not started |

---

## Next Steps

1. ✅ Design webhook architecture
2. ⏳ Apply `n8n_update_partial_workflow` to W1
3. ⏳ Apply `n8n_update_partial_workflow` to W2
4. ⏳ Apply `n8n_update_partial_workflow` to W3
5. ⏳ Test each webhook with sample data
6. ⏳ Document webhook URLs
7. ⏳ Update VERSION_LOG.md with v1.2.4

---

## Rollback Plan

If webhooks cause issues:

1. Use n8n UI to delete webhook nodes
2. Reconnect original triggers directly to their target nodes
3. All production logic remains intact

**Risk Level**: Low - webhooks are additive, not replacing existing triggers

---

## Benefits

1. **Instant Testing**: No waiting for schedules
2. **Rapid Iteration**: Fix → test → fix in minutes
3. **Isolated Testing**: Test without affecting production data
4. **Development Speed**: 10x faster debugging and validation
5. **Confidence**: Thoroughly test before relying on scheduled runs

---

## Notes

- Webhooks are **unauthenticated** by default in n8n
- For production, consider adding authentication headers
- Test mode flag can be used to add safety checks in workflow logic
- Consider rate limiting if exposing publicly

---

## Related Documentation

- Main VERSION_LOG: `/N8N_Blueprints/v1_foundation/VERSION_LOG.md`
- Workflow Blueprints: `/N8N_Blueprints/v1_foundation/workflow*.json`
- Testing Guide: `/TESTING_GUIDE.md`
