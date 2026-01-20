# Temporary Test Trigger Workflow

## Overview
- **Workflow Name:** TEMP - Autonomous Test Trigger
- **Workflow ID:** HwRADmf15MY3Ala2
- **Platform:** n8n
- **Status:** Built and validated (inactive)
- **Purpose:** One-shot workflow to trigger autonomous testing system by sending test email with PDF attachment

## Workflow Structure

### 1. Webhook Trigger
- **Node Type:** n8n-nodes-base.webhook (v2.1)
- **Purpose:** API-triggered execution via POST endpoint
- **Configuration:**
  - HTTP Method: POST
  - Path: `trigger-test-chunk2`
  - Response Mode: When Last Node Finishes
  - Response Data: First Entry JSON
- **Webhook URL:** `https://n8n.sway.so/webhook-test/trigger-test-chunk2`
- **Position:** Entry point

### 2. Download ADM10 PDF
- **Node Type:** n8n-nodes-base.googleDrive (v3)
- **Resource:** File
- **Operation:** Download
- **Configuration:**
  - File ID: `1SaAnbMGcyZgLkmYC4KZJyI9gN26N_l7L`
  - Credentials: Google Drive OAuth (g2ksaYkLXWtfDWAh)
  - Output: Binary data stored in `data` property
- **Purpose:** Fetch ADM10_Exposé.pdf from Google Drive

### 3. Send Test Email
- **Node Type:** n8n-nodes-base.gmail (v2.2)
- **Resource:** Message
- **Operation:** Send
- **Configuration:**
  - From: swayfromthehook@gmail.com (via OAuth)
  - To: swayclarkeii@gmail.com
  - Subject: "Test Chunk 2 Fix - ADM10 Exposé"
  - Body: "Autonomous test - validating file lifecycle bug fix"
  - Attachment: Binary data from previous node
  - Credentials: Gmail OAuth (g2ksaYkLXWtfDWAh)
- **Purpose:** Send email that triggers Pre-Chunk 0 → Chunk 2 execution

### 4. Return Success
- **Node Type:** n8n-nodes-base.code (v2)
- **Purpose:** Return confirmation JSON
- **Output:**
```json
{
  "success": true,
  "message": "Test email sent successfully",
  "timestamp": "<ISO timestamp>",
  "emailTo": "swayclarkeii@gmail.com",
  "subject": "Test Chunk 2 Fix - ADM10 Exposé"
}
```

## Workflow Flow

```
Webhook Trigger (POST /webhook-test/trigger-test-chunk2)
    ↓
Download ADM10 PDF (from Google Drive)
    ↓
Send Test Email (with PDF attachment)
    ↓
Return Success (confirmation → webhook response)
```

## Validation Results

- **Status:** ✅ Valid
- **Total Nodes:** 4
- **Connections:** 3 (all valid)
- **Errors:** 0
- **Warnings:** 6 (non-critical)
  - Code node doesn't reference input data (expected behavior)
  - Webhook should send response on error (handled by responseMode)
  - Consider error handling (not critical for one-shot test)

## Execution Instructions

### Option 1: Webhook Trigger (Recommended for Programmatic Use)
The workflow must be **activated** first, then triggered via webhook:

```bash
# Step 1: Activate the workflow (if not already active)
curl -X PATCH https://n8n.sway.so/api/v1/workflows/HwRADmf15MY3Ala2 \
  -H "X-N8N-API-KEY: <api-key>" \
  -H "Content-Type: application/json" \
  -d '{"active": true}'

# Step 2: Trigger via webhook
curl -X POST https://n8n.sway.so/webhook-test/trigger-test-chunk2 \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Response:** The webhook will return the success JSON from the "Return Success" node after all nodes complete.

### Option 2: Manual Execution via n8n UI
1. Navigate to workflow ID: `HwRADmf15MY3Ala2`
2. Click "Execute Workflow" button (tests the flow without activating webhook)
3. Monitor execution progress
4. Verify email sent successfully

## Expected Test Flow

1. **This workflow executes** → Sends email with ADM10 PDF
2. **Pre-Chunk 0 receives email** → Extracts attachment
3. **Pre-Chunk 0 calls Chunk 2** → Uploads to Google Drive
4. **Chunk 2 returns file ID** → Validates bug fix
5. **Pre-Chunk 0 continues** → Completes processing

## Success Criteria

- Email successfully sent to swayclarkeii@gmail.com
- PDF attachment included (ADM10_Exposé.pdf)
- Pre-Chunk 0 triggers and processes the email
- Chunk 2 executes without file lifecycle errors
- File appears in Google Drive with valid ID

## Cleanup Instructions

After successful test execution:

1. **Verify test results** in Pre-Chunk 0 and Chunk 2 logs
2. **Delete this workflow:**
   - Via n8n UI: Navigate to workflow → Delete
   - Via API: `DELETE /api/v1/workflows/HwRADmf15MY3Ala2`
3. **Clean up test email** from swayclarkeii@gmail.com inbox (optional)

## Credentials Used

- **Google Drive OAuth:** g2ksaYkLXWtfDWAh
- **Gmail OAuth:** g2ksaYkLXWtfDWAh
- Both use swayfromthehook@gmail.com account

## Notes

- Workflow is currently **inactive** (must be activated for webhook to work)
- Webhook path: `/webhook-test/trigger-test-chunk2`
- Full webhook URL: `https://n8n.sway.so/webhook-test/trigger-test-chunk2`
- Webhook response mode: Returns final node output when workflow completes
- No error handling added (intentional for simplicity)
- Workflow settings: Save all executions for debugging
- Delete after use to avoid clutter

## File Locations

- **Workflow ID:** HwRADmf15MY3Ala2
- **Summary Document:** `/Users/swayclarke/coding_stuff/workflows/temp-test-trigger-summary.md`
- **Test File:** Google Drive file ID `1SaAnbMGcyZgLkmYC4KZJyI9gN26N_l7L`

## Next Steps

1. Execute this workflow via n8n UI or API
2. Monitor Pre-Chunk 0 execution logs
3. Verify Chunk 2 receives correct file lifecycle data
4. Confirm file appears in Google Drive with valid ID
5. Delete this temporary workflow after successful test
