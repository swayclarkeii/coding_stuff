# Manual Rebuild Guide: Pre-Chunk 0 Workflow

**Target URL**: https://n8n.oloxa.ai/workflow/6MPoDSf8t0u8qXQq
**Date**: 2026-01-06
**Total nodes**: 29 nodes
**Total connections**: 30 connections

---

## Overview

This guide walks you through rebuilding the "AMA Pre-Chunk 0: Intake & Client Identification" workflow node-by-node in the n8n UI.

**Estimated time**: 2-3 hours (29 nodes with full configuration)

**Strategy**: Build nodes in execution order, connect as you go

---

## Part 1: Gmail Trigger & PDF Processing (Nodes 1-5)

### Node 1: Gmail Trigger - Unread with Attachments

**Type**: Gmail Trigger (n8n-nodes-base.gmailTrigger)
**Position**: Start of workflow (top left)

**Parameters**:
```json
{
  "pollTimes": {
    "item": [
      {
        "mode": "everyMinute"
      }
    ]
  },
  "filters": {
    "labelIds": ["INBOX", "UNREAD", "Label_8011160688574026773"],
    "q": "has:attachment"
  }
}
```

**Credentials**: Gmail OAuth2 (select your existing credential or create new)

**Notes**:
- Polls every minute for unread emails with attachments
- Label `Label_8011160688574026773` = "AMA Property Docs"
- If label ID is wrong, update to your actual "AMA Property Docs" label ID

---

### Node 2: Extract Text from PDF

**Type**: Code (n8n-nodes-base.code)
**Connect from**: Gmail Trigger

**Code**:
```javascript
// Extract text from PDF attachments using n8n's extractFromFile helper
const items = $input.all();
const results = [];

for (const item of items) {
  const emailId = item.json.id;
  const emailDate = item.json.internalDate;
  const emailFrom = item.json.headers?.from || 'unknown';

  // Process each attachment
  if (item.json.attachments && item.json.attachments.length > 0) {
    for (const attachment of item.json.attachments) {
      const filename = attachment.filename || 'unknown.pdf';

      // Only process PDFs
      if (filename.toLowerCase().endsWith('.pdf')) {
        const attachmentData = attachment.data;

        // Extract text from PDF
        const text = await this.helpers.extractFromFile(
          Buffer.from(attachmentData, 'base64'),
          'application/pdf'
        );

        results.push({
          json: {
            emailId: emailId,
            emailDate: emailDate,
            emailFrom: emailFrom,
            filename: filename,
            attachmentData: attachmentData,
            text: text || '',
            mimeType: 'application/pdf'
          }
        });
      }
    }
  }
}

return results;
```

---

### Node 3: Evaluate Extraction Quality ⚠️ CRITICAL - Phase 1 Modification

**Type**: Code (n8n-nodes-base.code)
**Connect from**: Extract Text from PDF

**Code**:
```javascript
// V4: Evaluate extraction quality for each PDF
const items = $input.all();
const results = [];

for (const item of items) {
  const extractedText = item.json.text || '';
  const wordCount = extractedText.trim().split(/\s+/).length;

  results.push({
    json: {
      ...item.json,
      wordCount: wordCount,
      needsOCR: wordCount < 10,
      extractionQuality: wordCount < 10 ? 'poor' : 'good',

      // 🚨 CRITICAL: Phase 1 modification - Keep extracted text for downstream use
      extractedText: extractedText,
      textLength: extractedText.trim().length,
      extractionMethod: 'digital_pre_chunk'
    },
    binary: item.binary  // ✅ Pass through binary data
  });
}

return results;
```

**Notes**: The 3 new fields (extractedText, textLength, extractionMethod) are CRITICAL for Phase 2 integration.

---

### Node 4: AI Extract Client Name

**Type**: OpenAI (n8n-nodes-base.openAi)
**Connect from**: Evaluate Extraction Quality

**Parameters**:
```json
{
  "resource": "text",
  "operation": "message",
  "model": "gpt-4o-mini",
  "text": "={{ $json.extractedText }}",
  "options": {
    "systemMessage": "You are analyzing a German real estate document (Angebot, Mahnung, Rechnung, etc.). Extract ONLY the CLIENT company name (e.g., 'CASADA GmbH', 'Villa Martens'). Return ONLY the company name, nothing else. If unclear, return 'UNKNOWN_CLIENT'.\n\nExamples:\n- Document mentions 'CASADA GmbH' → return 'CASADA GmbH'\n- Document mentions 'Villa Martens' → return 'Villa Martens'\n- Document is unclear → return 'UNKNOWN_CLIENT'"
  }
}
```

**Credentials**: OpenAI API (your API key)

---

### Node 5: Normalize Client Name

**Type**: Code (n8n-nodes-base.code)
**Connect from**: AI Extract Client Name

**Code**:
```javascript
// Extract client name from AI response and normalize for folder matching
const item = $input.first();
const aiResponse = item.json.choices?.[0]?.message?.content || 'UNKNOWN_CLIENT';
const extractedClientName = aiResponse.trim();

// Normalize for folder name matching (German characters + remove legal entities)
function normalizeClientName(clientName) {
  return clientName
    .toLowerCase()
    .trim()
    .replace(/ü/g, 'ue')
    .replace(/ö/g, 'oe')
    .replace(/ä/g, 'ae')
    .replace(/ß/g, 'ss')
    .replace(/\s*(gmbh|ag|kg|e\.v\.|mbh|co\.|&\s*co\.?)\s*/gi, '')
    .replace(/[^a-z0-9]/g, '_')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '');
}

const normalizedName = normalizeClientName(extractedClientName);
const isUnknown = extractedClientName === 'UNKNOWN_CLIENT' || normalizedName === 'unknown_client';

return [{
  json: {
    ...item.json,
    client_name: extractedClientName,
    client_normalized: normalizedName,
    is_unknown_client: isUnknown
  }
}];
```

---

## Part 2: Client Routing (Nodes 6-10)

### Node 6: Check Client Exists

**Type**: Google Sheets (n8n-nodes-base.googleSheets)
**Connect from**: Normalize Client Name

**Parameters**:
```json
{
  "operation": "read",
  "sheetName": "Client Registry",
  "range": "A:E",
  "options": {}
}
```

**Credentials**: Google Sheets OAuth2

**Notes**: Reads Client Registry to check if client exists

---

### Node 7: IF Unknown Client

**Type**: IF (n8n-nodes-base.if)
**Connect from**: Normalize Client Name

**Parameters**:
```json
{
  "conditions": {
    "conditions": [
      {
        "leftValue": "={{ $json.is_unknown_client }}",
        "rightValue": true,
        "operator": {
          "type": "boolean",
          "operation": "true"
        }
      }
    ]
  }
}
```

**Notes**: Routes to 38_Unknowns if client name extraction failed

---

### Node 8: Move to 38_Unknowns Folder (from Unknown path)

**Type**: Google Drive (n8n-nodes-base.googleDrive)
**Connect from**: IF Unknown Client → true output

**Parameters**:
```json
{
  "operation": "move",
  "fileId": {
    "__rl": true,
    "mode": "id",
    "value": "={{ $json.file_id }}"
  },
  "driveId": {
    "__rl": true,
    "mode": "list",
    "value": "My Drive"
  },
  "folderId": {
    "__rl": true,
    "mode": "list",
    "value": "1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm"
  }
}
```

**Credentials**: Google Drive OAuth2

**Notes**: Folder ID `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm` = "38_Unknowns" folder

---

### Node 9: Check If Client in Registry

**Type**: Code (n8n-nodes-base.code)
**Connect from**: Check Client Exists

**Code**:
```javascript
// Check if normalized client name exists in registry
const normalizedClient = $('Normalize Client Name').first().json.client_normalized;
const registryRows = $input.all();

const clientExists = registryRows.some(row => {
  const registryClientName = row.json['Client_Normalized_Name'] || '';
  return registryClientName.toLowerCase().trim() === normalizedClient;
});

return [{
  json: {
    ...$('Normalize Client Name').first().json,
    client_exists: clientExists,
    client_status: clientExists ? 'EXISTING' : 'NEW'
  }
}];
```

---

### Node 10: IF New vs Existing Client

**Type**: IF (n8n-nodes-base.if)
**Connect from**: Check If Client in Registry

**Parameters**:
```json
{
  "conditions": {
    "conditions": [
      {
        "leftValue": "={{ $json.client_status }}",
        "rightValue": "NEW",
        "operator": {
          "type": "string",
          "operation": "equals"
        }
      }
    ]
  }
}
```

---

## Part 3: New Client Path (Nodes 11-13)

### Node 11: Upload PDF to Temp Folder (New Client)

**Type**: Google Drive (n8n-nodes-base.googleDrive)
**Connect from**: IF New vs Existing Client → true output

**Parameters**:
```json
{
  "operation": "upload",
  "name": "={{ $json.filename }}",
  "driveId": {
    "__rl": true,
    "mode": "list",
    "value": "My Drive"
  },
  "folderId": {
    "__rl": true,
    "mode": "list",
    "value": "1NvqT3XkXINJ4HN0wJ2woGlZPYSfXa1Hj"
  },
  "binaryData": true,
  "binaryPropertyName": "data",
  "options": {
    "mimeType": "application/pdf"
  }
}
```

**Credentials**: Google Drive OAuth2

**Notes**: Folder ID `1NvqT3XkXINJ4HN0wJ2woGlZPYSfXa1Hj` = temp folder for new clients

---

### Node 12: Extract File ID & Metadata (New Client)

**Type**: Code (n8n-nodes-base.code)
**Connect from**: Upload PDF to Temp Folder

**Code**:
```javascript
// Extract file ID from upload result
const uploadResult = $input.first().json;
const originalItem = $('Normalize Client Name').first().json;

return [{
  json: {
    file_id: uploadResult.id,
    filename: uploadResult.name,
    client_name: originalItem.client_name,
    client_normalized: originalItem.client_normalized,
    email_id: originalItem.emailId,
    parent_folder_id: uploadResult.parents?.[0] || '1NvqT3XkXINJ4HN0wJ2woGlZPYSfXa1Hj',
    client_status: 'NEW'
  }
}];
```

---

### Node 13: Execute Chunk 0

**Type**: Execute Workflow (n8n-nodes-base.executeWorkflow)
**Connect from**: Extract File ID & Metadata (New Client)

**Parameters**:
```json
{
  "workflowId": {
    "__rl": true,
    "mode": "list",
    "value": "zbxHkXOoD1qaz6OS"
  },
  "waitForSubWorkflow": true
}
```

**Notes**: Workflow ID `zbxHkXOoD1qaz6OS` = Chunk 0 (folder creation)

---

## Part 4: Existing Client Path (Nodes 14-20)

### Node 14: Upload PDF to Temp Folder (Existing Client)

**Type**: Google Drive (n8n-nodes-base.googleDrive)
**Connect from**: IF New vs Existing Client → false output

**Parameters**: Same as Node 11 (Upload PDF to Temp Folder for New Client)

---

### Node 15: Extract File ID & Metadata (Existing Client)

**Type**: Code (n8n-nodes-base.code)
**Connect from**: Upload PDF to Temp Folder (Existing Client)

**Code**: Same as Node 12

---

### Node 16: Lookup Client Folder IDs

**Type**: Google Sheets (n8n-nodes-base.googleSheets)
**Connect from**: Extract File ID & Metadata (Existing Client)

**Parameters**:
```json
{
  "operation": "read",
  "sheetName": "Folder IDs",
  "range": "A:M",
  "options": {}
}
```

**Credentials**: Google Sheets OAuth2

---

### Node 17: Filter Staging Folder ID ⚠️ CRITICAL - Error Handling Fix

**Type**: Code (n8n-nodes-base.code)
**Connect from**: Lookup Client Folder IDs

**Code**:
```javascript
// V5: GRACEFUL ERROR HANDLING - No errors thrown, route to 38_Unknowns if missing
const clientNormalized = $('Check If Client in Registry').first().json.client_normalized;
const sheetRows = $input.all();
const fileData = $('Extract File ID & Metadata (Existing Client)').first().json;

// Find matching row
const matchingRow = sheetRows.find(row => {
  const clientName = row.json.Client_Name || '';
  const normalizedName = clientName
    .toLowerCase().trim()
    .replace(/ü/g, 'ue').replace(/ö/g, 'oe').replace(/ä/g, 'ae').replace(/ß/g, 'ss')
    .replace(/\s*(gmbh|ag|kg|e\.v\.|mbh|co\.|&\s*co\.?)\s*/gi, '')
    .replace(/[^a-z0-9]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
  return normalizedName === clientNormalized;
});

// 🚨 CRITICAL: GRACEFUL HANDLING - Route to 38_Unknowns if no matching row
if (!matchingRow) {
  return [{
    json: {
      ...fileData,
      client_normalized: clientNormalized,
      error: `No staging folder found for client: ${clientNormalized}`,
      routeTo38Unknowns: true,
      errorType: 'missing_client_in_registry',
      skipChunk1: true
    }
  }];
}

const stagingFolderId = matchingRow.json.Staging_Folder_ID || matchingRow.json['01_Staging'];

// 🚨 CRITICAL: GRACEFUL HANDLING - Route to 38_Unknowns if staging folder ID is empty
if (!stagingFolderId) {
  return [{
    json: {
      ...fileData,
      client_normalized: clientNormalized,
      error: `Staging_Folder_ID is empty for client: ${clientNormalized}`,
      routeTo38Unknowns: true,
      errorType: 'missing_staging_folder',
      skipChunk1: true
    }
  }];
}

// SUCCESS PATH: Continue with staging folder ID
return [{
  json: {
    client_normalized: clientNormalized,
    staging_folder_id: stagingFolderId,
    email_id: fileData.email_id,
    file_id: fileData.file_id,
    filename: fileData.filename,
    routeTo38Unknowns: false
  }
}];
```

**Notes**: This graceful error handling fixes the villa_martens bug.

---

### Node 18: Check Routing Decision (NEW - Error Handling)

**Type**: IF (n8n-nodes-base.if)
**Connect from**: Filter Staging Folder ID

**Parameters**:
```json
{
  "conditions": {
    "conditions": [
      {
        "leftValue": "={{ $json.routeTo38Unknowns }}",
        "rightValue": true,
        "operator": {
          "type": "boolean",
          "operation": "true"
        }
      }
    ]
  }
}
```

**Notes**: Routes files with missing staging folders to 38_Unknowns

---

### Node 19: Prepare Missing Folder Error (NEW - Error Handling)

**Type**: Code (n8n-nodes-base.code)
**Connect from**: Check Routing Decision → true output

**Code**:
```javascript
// Prepare data for routing to 38_Unknowns when staging folder is missing
const item = $input.first().json;

// Create UNKNOWN_CLIENT structure to match existing unknowns path
return [{
  json: {
    client_name: 'UNKNOWN_CLIENT',
    client_normalized: 'unknown_client',
    parent_folder_id: '1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm',
    client_status: 'UNKNOWN',
    is_unknown_client: true,
    error_reason: item.error || 'Missing staging folder',
    error_type: item.errorType || 'missing_staging_folder',
    file_id: item.file_id,
    filename: item.filename,
    email_id: item.email_id,
    unknown_timestamp: new Date().toISOString()
  }
}];
```

---

### Node 20: Move to 38_Unknowns (Error Path)

**Type**: Google Drive (n8n-nodes-base.googleDrive)
**Connect from**: Prepare Missing Folder Error

**Parameters**: Same as Node 8 (Move to 38_Unknowns Folder)

---

### Node 21: Execute Chunk 1

**Type**: Execute Workflow (n8n-nodes-base.executeWorkflow)
**Connect from**: Check Routing Decision → false output

**Parameters**:
```json
{
  "workflowId": {
    "__rl": true,
    "mode": "list",
    "value": "djsBWsrAEKbj2omB"
  },
  "waitForSubWorkflow": true
}
```

**Notes**: Workflow ID `djsBWsrAEKbj2omB` = Chunk 1 (file staging)

---

## Part 5: Download & Move Operations (Nodes 22-25)

### Node 22: Download Original PDF (for Move to Client Folder)

**Type**: Google Drive (n8n-nodes-base.googleDrive)
**Connect from**: Execute Chunk 0

**Parameters**:
```json
{
  "operation": "download",
  "fileId": {
    "__rl": true,
    "mode": "id",
    "value": "={{ $json.file_id }}"
  }
}
```

**Credentials**: Google Drive OAuth2

---

### Node 23: Move File to Client Folder

**Type**: Google Drive (n8n-nodes-base.googleDrive)
**Connect from**: Download Original PDF

**Parameters**:
```json
{
  "operation": "move",
  "fileId": {
    "__rl": true,
    "mode": "id",
    "value": "={{ $json.file_id }}"
  },
  "driveId": {
    "__rl": true,
    "mode": "list",
    "value": "My Drive"
  },
  "folderId": {
    "__rl": true,
    "mode": "id",
    "value": "={{ $json.parent_folder_id }}"
  }
}
```

**Credentials**: Google Drive OAuth2

---

### Node 24: Send Email - New Client Notification

**Type**: Gmail (n8n-nodes-base.gmail)
**Connect from**: Move File to Client Folder

**Parameters**:
```json
{
  "operation": "send",
  "sendTo": "swayclarkeii@gmail.com",
  "subject": "New Client Detected: {{ $json.client_name }}",
  "message": "A new client has been detected and their folder structure has been created.\n\nClient Name: {{ $json.client_name }}\nNormalized Name: {{ $json.client_normalized }}\nDocument: {{ $json.filename }}\n\nThe document has been moved to their intake folder."
}
```

**Credentials**: Gmail OAuth2

---

### Node 25: Mark Email as Read

**Type**: Gmail (n8n-nodes-base.gmail)
**Connect from**: Send Email - New Client Notification

**Parameters**:
```json
{
  "operation": "markAsRead",
  "messageId": "={{ $json.email_id }}"
}
```

**Credentials**: Gmail OAuth2

---

## Part 6: Error Handling & Notifications (Nodes 26-29)

### Node 26: Download PDF for Unknown (Error Path)

**Type**: Google Drive (n8n-nodes-base.googleDrive)
**Connect from**: Move to 38_Unknowns (from Unknown Client path)

**Parameters**: Same as Node 22

---

### Node 27: Send Email - Unknown Client

**Type**: Gmail (n8n-nodes-base.gmail)
**Connect from**: Download PDF for Unknown

**Parameters**:
```json
{
  "operation": "send",
  "sendTo": "swayclarkeii@gmail.com",
  "subject": "Unknown Client Detected - Manual Review Required",
  "message": "An email with a PDF attachment was received, but the client could not be identified.\n\nDocument: {{ $json.filename }}\nFrom: {{ $json.emailFrom }}\n\nThe document has been moved to the 38_Unknowns folder for manual review."
}
```

**Credentials**: Gmail OAuth2

---

### Node 28: Send Email - Processing Failure

**Type**: Gmail (n8n-nodes-base.gmail)
**Connect from**: Move to 38_Unknowns (from Error Path)

**Parameters**:
```json
{
  "operation": "send",
  "sendTo": "swayclarkeii@gmail.com",
  "subject": "Document Processing Error - Manual Review Required",
  "message": "An error occurred while processing a document.\n\nClient: {{ $json.client_normalized }}\nDocument: {{ $json.filename }}\nError: {{ $json.error_reason }}\nError Type: {{ $json.error_type }}\n\nThe document has been moved to the 38_Unknowns folder for manual review."
}
```

**Credentials**: Gmail OAuth2

---

### Node 29: Mark Email as Read (Final)

**Type**: Gmail (n8n-nodes-base.gmail)
**Connect from**: Send Email - Processing Failure

**Parameters**: Same as Node 25

---

## Connection Summary

**Total connections**: 30

1. Gmail Trigger → Extract Text from PDF
2. Extract Text from PDF → Evaluate Extraction Quality
3. Evaluate Extraction Quality → AI Extract Client Name
4. AI Extract Client Name → Normalize Client Name
5. Normalize Client Name → Check Client Exists
6. Normalize Client Name → IF Unknown Client
7. IF Unknown Client (true) → Move to 38_Unknowns Folder
8. Check Client Exists → Check If Client in Registry
9. Check If Client in Registry → IF New vs Existing Client
10. IF New vs Existing Client (true) → Upload PDF to Temp Folder (New Client)
11. Upload PDF to Temp Folder (New Client) → Extract File ID & Metadata (New Client)
12. Extract File ID & Metadata (New Client) → Execute Chunk 0
13. IF New vs Existing Client (false) → Upload PDF to Temp Folder (Existing Client)
14. Upload PDF to Temp Folder (Existing Client) → Extract File ID & Metadata (Existing Client)
15. Extract File ID & Metadata (Existing Client) → Lookup Client Folder IDs
16. Lookup Client Folder IDs → Filter Staging Folder ID
17. Filter Staging Folder ID → Check Routing Decision
18. Check Routing Decision (true) → Prepare Missing Folder Error
19. Prepare Missing Folder Error → Move to 38_Unknowns (Error Path)
20. Check Routing Decision (false) → Execute Chunk 1
21. Execute Chunk 0 → Download Original PDF
22. Download Original PDF → Move File to Client Folder
23. Move File to Client Folder → Send Email - New Client Notification
24. Send Email - New Client Notification → Mark Email as Read
25. Move to 38_Unknowns (Unknown Path) → Download PDF for Unknown
26. Download PDF for Unknown → Send Email - Unknown Client
27. Send Email - Unknown Client → Mark Email as Read (Unknown Path)
28. Move to 38_Unknowns (Error Path) → Send Email - Processing Failure
29. Send Email - Processing Failure → Mark Email as Read (Final)
30. Execute Chunk 1 → (ends workflow)

---

## Workflow Settings

After adding all nodes and connections, configure workflow settings:

**Settings** (gear icon in top right):
```json
{
  "executionOrder": "v1"
}
```

---

## Final Steps

1. **Save the workflow**: Click "Save" button
2. **Name**: "AMA Pre-Chunk 0: Intake & Client Identification"
3. **Verify all credentials are linked**: Check for any red warning icons on nodes
4. **DO NOT activate yet**: Keep workflow inactive until you verify it's accessible

---

## Verification Checklist

Before activating:

✅ All 29 nodes added
✅ All 30 connections made
✅ All credentials linked (no red warnings)
✅ "Evaluate Extraction Quality" has 3 Phase 1 fields
✅ "Filter Staging Folder ID" has graceful error handling
✅ Workflow settings: executionOrder = "v1"
✅ Workflow saved successfully
✅ Workflow accessible in UI (can open and edit)

Once verified, activate and test with email.

---

**Estimated time to complete**: 2-3 hours
**Last updated**: 2026-01-06T00:24:45+01:00
