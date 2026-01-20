# V4 Phase 1: Pre-Chunk 0 Architecture Plan

**Version**: 1.0
**Created**: December 25, 2025
**Status**: Planning
**Author**: Sway + Claude

---

## Version History

| Version | Date | Changes | Status |
|---------|------|---------|--------|
| 1.0 | 2025-12-25 | Initial plan - architecture and implementation steps | Planning |

---

## Problem Statement

**The chicken-and-egg issue**: Chunk 0 (Folder Initialization) needs to know the client name to create client-specific folders, but we can only extract the client name AFTER processing the documents.

**Current broken flow**:
```
Chunk 0 (Manual, hardcoded "AMA_Documents") ← Runs first, but doesn't know client
  → Chunk 1 (Email)
  → Chunk 2 (Text Extract)
  → Chunk 2.5 (ID Client) ← Too late! Folders already created
```

---

## Architecture Decision

**Selected**: Option B - Separate Workflows with Execute Workflow

```
┌─────────────────────────────────────────┐
│  WORKFLOW 1: V4_PreChunk0_Intake        │
│  (NEW - Email trigger)                  │
│                                         │
│  Email → Extract → ID Client → Lookup   │
│                      ↓                  │
│              Decision Gate              │
│                  ↓                      │
│         [Execute Workflow] ────────────────┐
└─────────────────────────────────────────┘  │
                                             │
┌─────────────────────────────────────────┐  │
│  WORKFLOW 2: V4_Chunk0_FolderInit       │←─┘
│  (REFACTORED - Execute Workflow trigger)│
│                                         │
│  Receives: client_name                  │
│  Creates: 47 folders (nested per client)│
│  Returns: folder_ids                    │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  WORKFLOW 3: V4_Main_Flow               │
│  (Chunks 3-5)                           │
│                                         │
│  Classification → File Ops → Cleanup    │
└─────────────────────────────────────────┘
```

**Why Option B**:
- Chunk 0 stays mostly intact (minimal changes)
- Can test each workflow independently
- Execute Workflow is synchronous (waits for folder creation)
- Can still manually test Chunk 0

---

## Confirmed Parameters

| Parameter | Value |
|-----------|-------|
| Root Folder ID | `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm` |
| Folder Structure | NESTED (per client) |
| Scope | Eugene/AMA clients only |
| Live Chunk 0 Workflow ID | `Ui2rQFpMu9G1RTE1` |

---

## Implementation Phases

### Phase 0: Safety Backup (DO FIRST)

**Goal**: Create backup of working Chunk 0 before any changes

**n8n Steps**:
1. Open workflow `Ui2rQFpMu9G1RTE1` (current Chunk 0)
2. Click three dots menu → "Duplicate"
3. Rename to: `Chunk 0 - BACKUP v8 - DO NOT TOUCH`
4. Keep this workflow INACTIVE
5. Note the new workflow ID: `_______________` (fill in after creating)

**Local Backup**:
1. Current JSON file is already saved at:
   `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/N8N_Blueprints/v4_phase1/chunk 0_ Folder Initialization (V4 - Google Sheets) v8_24122025_FINAL Version.json`
2. This serves as version control

---

### Phase 1: Create Master Client Registry

**Goal**: Create Google Sheet to track clients and their folder IDs

**Steps**:

1. **Create Google Sheet**
   - Location: Root folder `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm`
   - Name: `AMA_Client_Registry`

2. **Sheet Structure** (Sheet 1: "Clients")
   | Column | Header | Type | Purpose |
   |--------|--------|------|---------|
   | A | client_name_raw | Text | Original client name from document |
   | B | client_normalized | Text | Normalized (lombok_capital) |
   | C | root_folder_id | Text | Client's root folder ID |
   | D | subfolder_ids_json | Text | JSON object with all folder IDs |
   | E | created_date | Date | When client was added |
   | F | last_updated | Date | Last document processed |
   | G | status | Text | active / inactive |

3. **Pre-populate with existing client** (if Lombok Capital folders exist):
   - Query existing "AMA - Folder ID Spreadsheet" for current folder IDs
   - Add row for Lombok Capital

4. **Store Sheet ID**:
   - Note the spreadsheet ID: `_______________` (fill in after creating)
   - Store in n8n credentials or as static workflow data

---

### Phase 2: Build Pre-Chunk 0 Workflow

**Goal**: New workflow that handles email intake, text extraction, and client identification

**Workflow Name**: `V4_PreChunk0_Intake`

**Node-by-Node Implementation**:

#### Node 1: Gmail Trigger
```
Type: n8n-nodes-base.gmailTrigger
Name: "Email Trigger - AMA Documents"
Parameters:
  - Polling: Every 1 minute
  - Label: [Create "AMA_PENDING" label in Gmail]
  - Simple: false (get full email data)
  - Download Attachments: true
```

#### Node 2: Filter - Has Attachments
```
Type: n8n-nodes-base.filter
Name: "Filter - Has PDF Attachments"
Conditions:
  - {{ $json.attachments.length > 0 }}
  - {{ $json.attachments.some(a => a.mimeType === 'application/pdf') }}
```

#### Node 3: Split Out Attachments
```
Type: n8n-nodes-base.splitOut
Name: "Split Out Attachments"
Field: attachments
```

#### Node 4: Filter PDF Only
```
Type: n8n-nodes-base.filter
Name: "Filter PDF Only"
Conditions:
  - {{ $json.mimeType === 'application/pdf' }}
```

#### Node 5: Upload to Staging
```
Type: n8n-nodes-base.googleDrive
Name: "Upload to Staging"
Operation: Upload
Parameters:
  - File Data: {{ $json.data }} (base64)
  - Name: {{ $json.filename }}
  - Parent Folder: [STAGING folder ID from registry]
```

#### Node 6: Extract Text (Digital PDF)
```
Type: n8n-nodes-base.extractFromFile
Name: "Extract Text - Digital PDF"
Operation: Extract from PDF
Input: Binary from previous node
```

#### Node 7: Check Text Length
```
Type: n8n-nodes-base.if
Name: "Is Scanned PDF?"
Conditions:
  - {{ $json.text.length < 100 }} → Yes (needs OCR)
  - Otherwise → No (digital PDF, proceed)
```

#### Node 8a: OCR Branch (if scanned)
```
Type: n8n-nodes-base.awsTextract (or OpenAI Vision)
Name: "OCR - Scanned PDF"
[Configure based on existing Chunk 2 OCR logic]
```

#### Node 8b: Merge Text Results
```
Type: n8n-nodes-base.merge
Name: "Merge Text Results"
Combines digital extraction and OCR paths
```

#### Node 9: AI - Extract Client Name
```
Type: n8n-nodes-base.openAi
Name: "AI - Extract Client Name"
Operation: Message a Model
Model: gpt-4o-mini
System Prompt:
  "You are a document analyzer. Extract the client/company name from the following document text.
   Return ONLY a JSON object: {\"client_name\": \"...\", \"confidence\": 0.0-1.0}
   If you cannot determine the client name, return {\"client_name\": null, \"confidence\": 0}"
User Message: {{ $json.extractedText.substring(0, 3000) }}
```

#### Node 10: Normalize Client Name
```
Type: n8n-nodes-base.code
Name: "Normalize Client Name"
Code:
  function normalizeClientName(rawName) {
    if (!rawName) return null;
    return rawName
      .toLowerCase()
      .trim()
      .replace(/ä/g, 'ae')
      .replace(/ö/g, 'oe')
      .replace(/ü/g, 'ue')
      .replace(/ß/g, 'ss')
      .replace(/\s*(gmbh|ag|kg|e\.v\.|mbh|co\.|&\s*co\.?)\s*/gi, '')
      .replace(/[^a-z0-9]/g, '_')
      .replace(/_+/g, '_')
      .replace(/^_|_$/g, '');
  }

  const aiResponse = JSON.parse($input.first().json.message.content);
  return [{
    json: {
      client_name_raw: aiResponse.client_name,
      client_normalized: normalizeClientName(aiResponse.client_name),
      confidence: aiResponse.confidence,
      // Pass through other data
      stagingFileId: $('Upload to Staging').first().json.id,
      extractedText: $('Merge Text Results').first().json.text,
      emailId: $('Email Trigger').first().json.id,
      emailFrom: $('Email Trigger').first().json.from
    }
  }];
```

#### Node 11: Lookup Client Registry
```
Type: n8n-nodes-base.googleSheets
Name: "Lookup Client Registry"
Operation: Read Rows
Spreadsheet: [AMA_Client_Registry ID]
Sheet: Clients
Filters:
  - client_normalized = {{ $json.client_normalized }}
```

#### Node 12: Decision Gate
```
Type: n8n-nodes-base.switch
Name: "Decision Gate"
Rules:
  1. "Unknown Client" - {{ $json.client_normalized === null || $json.confidence < 0.7 }}
  2. "Create Folders" - {{ $('Lookup Client Registry').first().json.length === 0 }}
  3. "Proceed" - Default (client exists)
```

#### Node 13a: Unknown Client Branch
```
Type: n8n-nodes-base.googleDrive
Name: "Move to Unknown Queue"
Operation: Move
Destination: UNKNOWN_CLIENT_QUEUE folder
[Then send Slack notification]
```

#### Node 13b: Create Folders Branch
```
Type: n8n-nodes-base.executeWorkflow
Name: "Execute Chunk 0"
Workflow: [Chunk 0 workflow ID]
Input Data:
  {
    "client_name": "{{ $json.client_name_raw }}",
    "client_normalized": "{{ $json.client_normalized }}",
    "parent_folder_id": "1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm"
  }
Wait for completion: true
```

#### Node 13c: Proceed Branch
```
Type: n8n-nodes-base.set
Name: "Set Folder IDs from Registry"
[Parse subfolder_ids_json from registry lookup]
```

#### Node 14: Continue to Classification
```
[Pass data to Chunk 3 - either via Execute Workflow or continue in same workflow]
```

---

### Phase 3: Refactor Chunk 0

**Goal**: Minimal changes to accept parameters instead of hardcoded values

**Changes to existing Chunk 0**:

#### Change 1: Replace Trigger
```
REMOVE: Manual Trigger node

ADD: Execute Workflow Trigger
Type: n8n-nodes-base.executeWorkflowTrigger
Name: "Workflow Trigger - Receive Client"
```

#### Change 2: Read Input Parameters
```
ADD after trigger:
Type: n8n-nodes-base.code
Name: "Read Input Parameters"
Code:
  const input = $input.first().json;

  // Validate input
  if (!input.client_name || !input.client_normalized) {
    throw new Error('Missing required input: client_name');
  }

  return [{
    json: {
      clientName: input.client_name,
      clientNormalized: input.client_normalized,
      parentFolderId: input.parent_folder_id || '1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm',
      rootFolderName: `${input.client_normalized}_Documents`
    }
  }];
```

#### Change 3: Update "Define Folder Structure"
```
CHANGE: Hardcoded 'AMA_Documents'
TO: {{ $('Read Input Parameters').first().json.rootFolderName }}

The folder config array stays the same - just the root name changes
```

#### Change 4: Update "Create Root Folder"
```
CHANGE: name parameter
FROM: "AMA_Documents"
TO: "={{ $('Read Input Parameters').first().json.rootFolderName }}"

KEEP: folderId (parent) = "1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm"
```

#### Change 5: Add Registry Update (at end)
```
ADD after "Write Folder IDs to Sheet":
Type: n8n-nodes-base.googleSheets
Name: "Update Client Registry"
Operation: Append Row
Spreadsheet: [AMA_Client_Registry ID]
Sheet: Clients
Values:
  - client_name_raw: {{ $('Read Input Parameters').first().json.clientName }}
  - client_normalized: {{ $('Read Input Parameters').first().json.clientNormalized }}
  - root_folder_id: {{ $('Create Root Folder').first().json.id }}
  - subfolder_ids_json: {{ JSON.stringify(folderIdsObject) }}
  - created_date: {{ new Date().toISOString() }}
  - last_updated: {{ new Date().toISOString() }}
  - status: "active"
```

#### Change 6: Return Data
```
ADD at end:
Type: n8n-nodes-base.respondToWebhook (or just let Execute Workflow return last node data)
Return:
  {
    "success": true,
    "client_name": "...",
    "root_folder_id": "...",
    "subfolder_ids": { ... }
  }
```

---

### Phase 4: Integration & Testing

**Step 1: Test Chunk 0 in isolation**
1. Activate refactored Chunk 0
2. Use n8n's "Test Workflow" with manual input:
   ```json
   {
     "client_name": "Test Client",
     "client_normalized": "test_client",
     "parent_folder_id": "1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm"
   }
   ```
3. Verify folders created correctly
4. Verify registry updated
5. Delete test folders after verification

**Step 2: Test Pre-Chunk 0 in isolation**
1. Send test email with PDF attachment to monitored inbox
2. Verify email is picked up
3. Verify text extraction works
4. Verify client name extraction works
5. Verify registry lookup works
6. Verify decision gate routes correctly

**Step 3: Integration test**
1. Connect Pre-Chunk 0 → Chunk 0 via Execute Workflow
2. Send test email with NEW client document
3. Verify full flow:
   - Email received
   - Client identified
   - Folders created (new client)
   - Document classified
   - Document filed

**Step 4: Test existing client flow**
1. Send another document for same client
2. Verify folders NOT re-created
3. Verify document filed to existing folders

---

### Phase 5: Fallback & Monitoring

**Create UNKNOWN_CLIENT_QUEUE folder**
- Location: Root folder
- Purpose: Documents where client couldn't be identified

**Slack Notifications**
- On unknown client: Alert with document link for manual review
- On error: Alert with error details

**Email Lifecycle Labels**
- AMA_PENDING → AMA_PROCESSING → AMA_PROCESSED
- AMA_FAILED for errors

---

## Files Reference

| File | Location | Purpose |
|------|----------|---------|
| Current Chunk 0 JSON | `v4_phase1/chunk 0_ Folder Initialization (V4 - Google Sheets) v8_24122025_FINAL Version.json` | Backup reference |
| This Plan | `v4_phase1/PLAN_PreChunk0_Architecture_v1.0.md` | Implementation guide |
| Chunk 1 (reference) | `v4_phase1/chunk1_email_staging_v4.json` | Email logic reference |
| Chunk 2 (reference) | `v4_phase1/chunk2_text_extraction_v4.json` | Extraction logic reference |
| Chunk 2.5 (reference) | `v4_phase1/chunk2.5_project_tracking_v4.json` | Client ID logic reference |

---

## Checklist

### Phase 0: Backup
- [ ] Duplicate Chunk 0 workflow in n8n
- [ ] Name backup workflow correctly
- [ ] Note backup workflow ID: `_______________`

### Phase 1: Registry
- [ ] Create AMA_Client_Registry Google Sheet
- [ ] Set up column headers
- [ ] Pre-populate existing client (if any)
- [ ] Note sheet ID: `_______________`

### Phase 2: Pre-Chunk 0
- [ ] Create new workflow in n8n
- [ ] Implement email trigger
- [ ] Implement text extraction
- [ ] Implement client ID extraction
- [ ] Implement registry lookup
- [ ] Implement decision gate
- [ ] Test in isolation

### Phase 3: Refactor Chunk 0
- [ ] Change trigger to Execute Workflow Trigger
- [ ] Add input parameter handling
- [ ] Update folder naming to use parameter
- [ ] Add registry update at end
- [ ] Add return data
- [ ] Test in isolation

### Phase 4: Integration
- [ ] Connect Pre-Chunk 0 → Chunk 0
- [ ] Test new client flow
- [ ] Test existing client flow
- [ ] Test unknown client fallback

### Phase 5: Monitoring
- [ ] Create UNKNOWN_CLIENT_QUEUE folder
- [ ] Set up Slack notifications
- [ ] Set up email labels

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking working Chunk 0 | Phase 0 backup - can revert instantly |
| Registry out of sync | Weekly reconciliation, validation checks |
| OCR extraction fails | Falls back to unknown queue for manual review |
| Client name ambiguous | Confidence threshold (0.7) + manual queue |

---

## Next Steps

1. **Approve this plan** - Review and confirm approach
2. **Execute Phase 0** - Create backup (5 minutes)
3. **Execute Phase 1** - Create registry sheet (15 minutes)
4. **Execute Phase 2** - Build Pre-Chunk 0 (1-2 hours)
5. **Execute Phase 3** - Refactor Chunk 0 (30 minutes)
6. **Execute Phase 4** - Integration testing (30 minutes)
