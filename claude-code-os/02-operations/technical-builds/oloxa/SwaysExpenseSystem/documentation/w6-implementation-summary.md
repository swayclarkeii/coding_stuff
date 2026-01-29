# W6 Implementation Summary

## Status: ⚠️ Partially Complete - Manual Completion Required

**Workflow ID**: `qt1CzTCkjUQaRd5n`
**Name**: Expense System - Workflow 6: PDF Bank Statement Processor

---

## What Was Built

### Current State
- ✅ Workflow created with webhook trigger
- ⚠️ Needs remaining 7 nodes added manually in n8n UI
- ❌ Not yet active (requires complete node chain)

### Issue Encountered
The MCP `n8n_update_partial_workflow` function has a bug where the `target` parameter appears empty in error messages, preventing automated node updates. Multiple approaches were attempted:
1. Updating by node ID
2. Updating by node name
3. Using autofix
4. Direct API calls

All resulted in the same "Node not found" error despite nodes existing in the workflow.

---

## Complete W6 Design (Copy from W2 Structure)

### Node Chain

```
1. Webhook Trigger
   ↓
2. Read PDF File (readBinaryFile)
   ↓
3. Prepare Metadata (Code)
   ↓
4. Upload PDF to Drive (googleDrive)
   ↓
5. Build Vision API Request (Code)
   ↓
6. Extract Text with Vision API (httpRequest - Anthropic)
   ↓
7. Parse Claude Response (Code)
   ↓
8. Log to Bank Statements Sheet (googleSheets)
```

---

## Node Configurations (Ready to Copy)

### 1. ✅ Webhook Trigger
**Already configured in workflow**
- Type: `n8n-nodes-base.webhook`
- Path: `bank-statement-pdf`
- Method: POST
- Response Mode: On Received
- Webhook ID: `99f8a9b0-c1d2-4e3f-a4b5-6c7d8e9f0999`

---

### 2. Read PDF File
**Type**: `n8n-nodes-base.readBinaryFile`
**Parameters**:
```json
{
  "filePath": "={{ $json.body.pdf_path }}"
}
```

---

### 3. Prepare Metadata
**Type**: `n8n-nodes-base.code`
**Code**:
```javascript
const inputData = $input.first();
const webhookData = $('Webhook Trigger').first().json.body;
const binaryData = inputData.binary.data;

return {
  json: {
    file_name: binaryData.fileName || webhookData.file_name || 'bank_statement.pdf',
    file_path: webhookData.pdf_path,
    mime_type: binaryData.mimeType || 'application/pdf',
    timestamp: new Date().toISOString()
  },
  binary: inputData.binary
};
```

---

### 4. Upload PDF to Drive
**Type**: `n8n-nodes-base.googleDrive`
**Credential**: `google-drive-swaybot99`
**Parameters**:
```json
{
  "resource": "file",
  "operation": "upload",
  "folderId": {
    "__rl": true,
    "mode": "id",
    "value": "1ahpPa6pOLR1xK3tU4q0YOTQJOczr7ZsS"
  }
}
```

**Note**: Folder ID `1ahpPa6pOLR1xK3tU4q0YOTQJOczr7ZsS` is the Gmail folder from W2.

---

### 5. Build Vision API Request
**Type**: `n8n-nodes-base.code`
**Code**:
```javascript
const item = $input.first();
const binaryData = item.binary.data;
const base64Data = binaryData.toBase64();
const fileName = item.json.file_name || 'bank_statement.pdf';

const requestBody = {
  model: 'claude-3-5-sonnet-20241022',
  max_tokens: 4096,
  messages: [
    {
      role: 'user',
      content: [
        {
          type: 'text',
          text: `Extract all bank transactions from this PDF bank statement. Return ONLY valid JSON with this structure:
{
  "bank_name": "string",
  "account_number": "string (last 4 digits)",
  "statement_period": "string",
  "transactions": [
    {
      "date": "YYYY-MM-DD",
      "description": "string",
      "amount": number,
      "balance": number
    }
  ]
}

Rules:
- Return ONLY the JSON object, no markdown
- Use negative amounts for debits
- Extract ALL visible transactions
- If balance not visible, use null`
        },
        {
          type: 'image',
          source: {
            type: 'base64',
            media_type: 'application/pdf',
            data: base64Data
          }
        }
      ]
    }
  ]
};

return {
  json: {
    requestBody: requestBody,
    file_name: fileName,
    file_id: item.json.id
  },
  binary: item.binary
};
```

---

### 6. Extract Text with Vision API
**Type**: `n8n-nodes-base.httpRequest`
**Credential**: `anthropic-claude-api`
**Parameters**:
```json
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "anthropicApi",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "anthropic-version",
        "value": "2023-06-01"
      }
    ]
  },
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "={{ $json.requestBody }}"
}
```

**CRITICAL**: This is the EXACT configuration from W2's working "Extract Text with Vision API" node. Copy all settings exactly.

---

### 7. Parse Claude Response
**Type**: `n8n-nodes-base.code`
**Code**:
```javascript
const response = $input.first().json;
const textContent = response.content[0].text;

let jsonText = textContent.trim();
if (jsonText.startsWith('```')) {
  jsonText = jsonText.replace(/```json\n?/g, '').replace(/```/g, '').trim();
}

try {
  const parsedData = JSON.parse(jsonText);
  const buildNode = $('Build Vision API Request').first().json;

  return {
    json: {
      bank_name: parsedData.bank_name || 'Unknown',
      account_number: parsedData.account_number || 'N/A',
      statement_period: parsedData.statement_period || 'N/A',
      transaction_count: parsedData.transactions?.length || 0,
      file_name: buildNode.file_name,
      file_id: buildNode.file_id,
      extraction_timestamp: new Date().toISOString()
    }
  };
} catch (error) {
  const buildNode = $('Build Vision API Request').first().json;
  return {
    json: {
      error: 'Failed to parse',
      error_message: error.message,
      file_name: buildNode.file_name
    }
  };
}
```

---

### 8. Log to Bank Statements Sheet
**Type**: `n8n-nodes-base.googleSheets`
**Credential**: `google-sheets-swaybot99`
**Parameters**:
```json
{
  "resource": "sheet",
  "operation": "append",
  "documentId": {
    "__rl": true,
    "mode": "id",
    "value": "1KvVY9BdA6-wVNR_4rHjvEyGkp3ILe3W3zQQVbH5LRa4"
  },
  "sheetName": {
    "__rl": true,
    "mode": "name",
    "value": "Bank_Statements"
  },
  "dataMode": "autoMapInputData"
}
```

**Note**: Sheet ID is from the expense tracking spreadsheet.

---

## Manual Completion Steps

### In n8n UI (http://n8n.oloxa.ai)

1. **Open W6 workflow** (ID: `qt1CzTCkjUQaRd5n`)

2. **Add each node** by clicking the "+" button after "Webhook Trigger"

3. **For each node**:
   - Select the correct node type from the list above
   - Copy/paste the parameters or code exactly as shown
   - Connect to the previous node
   - Select the correct credentials (already exist in n8n)

4. **Verify connections**:
   - Each node should connect sequentially (webhook → read → prepare → upload → build → extract → parse → log)

5. **Activate workflow**:
   - Click "Active" toggle in top right
   - Verify webhook URL is generated

6. **Test webhook**:
   ```bash
   curl -X POST "http://n8n.oloxa.ai/webhook/bank-statement-pdf" \
     -H "Content-Type: application/json" \
     -d '{"pdf_path": "/path/to/test.pdf", "file_name": "test_statement.pdf"}'
   ```

---

## Why This Approach Works

### Copied from W2's Success
- W2 successfully uses Claude Vision API for PDFs
- HTTP Request node configuration is PROVEN to work
- Same Anthropic API credentials
- Same base64 conversion pattern

### Key Differences from W2
1. **Input**: Webhook with PDF path (not Gmail trigger)
2. **Output**: Bank statements sheet (not receipts sheet)
3. **Parsing**: Bank transactions (not receipt amounts)
4. **No duplicate checking**: Each request processes fresh PDF

---

## Testing Plan

### Test Data Required
- Sample PDF bank statement
- Place in accessible file path
- Note the full absolute path

### Test Execution
1. Send webhook with PDF path
2. Watch execution in n8n UI
3. Verify:
   - PDF loads
   - Uploads to Drive
   - Vision API extracts data
   - Parses to JSON
   - Logs to sheet

### Expected Output
Google Sheet "Bank_Statements" should have new row with:
- Bank name
- Account number
- Statement period
- Transaction count
- File name
- File ID
- Extraction timestamp

---

## Alternative Completion: Copy from W2 in UI

### Even Faster Approach
1. Open W2 (dHbwemg7hEB4vDmC) in n8n UI
2. **Copy these specific nodes**:
   - "Upload to Receipt Pool" → Rename to "Upload PDF to Drive"
   - "Build Vision API Request" → Keep name
   - "Extract Text with Vision API" → Keep name (THIS IS CRITICAL - exact copy)
   - "Parse Amount from OCR Text" → Rename to "Parse Claude Response" (modify code)
   - "Log Receipt in Database" → Rename to "Log to Bank Statements Sheet"

3. **Paste into W6** after the webhook

4. **Modify only**:
   - Parse code (use bank transaction structure)
   - Sheet operation (point to Bank_Statements sheet)
   - Code references (adjust node names)

---

## Blockers Resolved for Future

### Bug Documented
The `mcp__n8n-mcp__n8n_update_partial_workflow` `target` parameter bug has been documented. When this is fixed, automated workflow building will work smoothly.

### Learnings Captured
- Resource locator format is required for Google nodes (`__rl: true`)
- Webhook activation requires complete node chain
- Direct API calls have same validation requirements as MCP
- Manual UI completion is fastest when MCP has bugs

---

## Next Agent Handoff

Once W6 is manually completed in UI:
1. **test-runner-agent** can test execution
2. **workflow-optimizer-agent** can optimize token usage
3. **solution-builder-agent** can integrate with other workflows

---

## Files Created
- `/Users/computer/coding_stuff/temp_w6_workflow.json` - Complete workflow JSON (can be imported)
- `/Users/computer/coding_stuff/workflows/w6-implementation-summary.md` - This file

---

**Status**: ⚠️ Awaiting manual node addition in n8n UI
**Estimated Time**: 10-15 minutes to add 7 nodes
**Complexity**: Low (copy/paste configurations)
