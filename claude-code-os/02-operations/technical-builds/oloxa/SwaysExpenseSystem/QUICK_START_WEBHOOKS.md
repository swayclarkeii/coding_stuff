# Quick Start - Webhook Testing

**3-Minute Guide to Testing Expense Workflows**

---

## Setup (One Time - 10 minutes)

### 1. Apply Webhooks to n8n

Use n8n MCP `n8n_update_partial_workflow` with these files:

```
webhook_operations/workflow1_add_webhook.json → W1 (MPjDdVMI88158iFW)
webhook_operations/workflow2_add_webhook.json → W2 (dHbwemg7hEB4vDmC)
webhook_operations/workflow3_add_webhook.json → W3 (waPA94G2GXawDlCa)
```

### 2. Get Webhook URLs

In n8n UI, click each "Manual Test Trigger" node → Copy webhook URL

---

## Testing (Instant)

### Test Workflow 1 (PDF Processing)

**Payload**:
```json
{"fileId": "YOUR_GOOGLE_DRIVE_PDF_FILE_ID"}
```

**How to get fileId**:
1. Upload PDF to Google Drive
2. Right-click → Get Link
3. Extract ID from: `https://drive.google.com/file/d/[ID_HERE]/view`

**Trigger**:
```bash
curl -X POST [YOUR_WEBHOOK_URL] \
  -H "Content-Type: application/json" \
  -d '{"fileId": "1abc123xyz"}'
```

**Validate**:
- [ ] Check n8n execution logs
- [ ] Verify new transactions in Google Sheets
- [ ] Confirm PDF moved to Archive

---

### Test Workflow 2 (Gmail Receipts)

**Payload**:
```json
{"testMode": true}
```

**Trigger**:
```bash
curl -X POST [YOUR_WEBHOOK_URL] \
  -H "Content-Type: application/json" \
  -d '{"testMode": true}'
```

**Validate**:
- [ ] Check n8n execution logs
- [ ] Verify receipts in Receipt Pool (Google Drive)
- [ ] Confirm receipt records in Google Sheets

---

### Test Workflow 3 (Matching)

**Payload**:
```json
{"testMode": true}
```

**Trigger**:
```bash
curl -X POST [YOUR_WEBHOOK_URL] \
  -H "Content-Type: application/json" \
  -d '{"testMode": true}'
```

**Validate**:
- [ ] Check n8n execution logs
- [ ] Verify ReceiptID populated in Transactions sheet
- [ ] Confirm receipts moved to organized folders

---

## Webhook URLs

After setup, document your URLs here:

- **W1 (PDF Intake)**: `_______________________________`
- **W2 (Gmail Monitor)**: `_______________________________`
- **W3 (Matching)**: `_______________________________`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 404 Not Found | Verify webhook path is correct (`/test-expense-w1`) |
| Missing fileId error | Include fileId in W1 payload |
| No execution logs | Check workflow is active |
| Empty results | Verify test data exists (unmatched transactions, etc.) |

---

## Full Documentation

- **Complete Guide**: TESTING_INFRASTRUCTURE.md
- **Implementation Steps**: WEBHOOK_IMPLEMENTATION_SCRIPT.md
- **Build Summary**: TESTING_INFRASTRUCTURE_BUILD_SUMMARY.md
- **Handoff**: HANDOFF_TESTING_INFRASTRUCTURE.md

---

**Time to first test**: 10 minutes setup → Instant testing forever ✅
