# Eugene Document Organizer v8 Phase 1 - Backup

**Backup Date:** January 17, 2026
**Backup Time:** 19:46 CET
**Purpose:** Pre-implementation backup before Claude Vision upgrade (v9 Phase 1)

---

## Workflows Included

### 1. Pre-Chunk 0 - REBUILT v1
- **File:** `pre_chunk_0_backup_2026-01-17.json`
- **Workflow ID:** YGXWjWcBIk66ArvT
- **Status:** Active
- **Last Updated:** 2026-01-17 10:30:05 UTC
- **Node Count:** 46 nodes
- **Description:** Main intake workflow - downloads PDFs from Gmail, extracts text with Google Document AI OCR, classifies clients using OpenAI

### 2. Chunk 0 - Folder Initialization
- **File:** `chunk_0_backup_2026-01-17.json`
- **Workflow ID:** zbxHkXOoD1qaz6OS
- **Status:** Active
- **Last Updated:** 2026-01-12 19:19:59 UTC
- **Node Count:** 20 nodes
- **Description:** Creates/initializes Google Drive folder structure for each client

### 3. Chunk 2 - Text Extraction
- **File:** `chunk_2_backup_2026-01-17.json`
- **Workflow ID:** qKyqsL64ReMiKpJ4
- **Status:** Active
- **Last Updated:** 2026-01-12 10:04:46 UTC
- **Node Count:** 11 nodes
- **Description:** Extracts text from PDFs, handles OCR for scanned documents using AWS Textract

### 4. Chunk 2.5 - Client Document Tracking
- **File:** `chunk_2_5_backup_2026-01-17.json`
- **Workflow ID:** okg8wTqLtPUwjQ18
- **Status:** Active
- **Last Updated:** 2026-01-14 14:28:42 UTC
- **Node Count:** 23 nodes
- **Description:** Tracks document metadata in Google Sheets, manages client registry

---

## System State at Backup

### Key Features Working
- ✅ Google Document AI OCR for scanned PDFs
- ✅ OpenAI GPT-4o client classification
- ✅ Street address identification ("Schlossberg 13")
- ✅ Google Drive folder structure automation
- ✅ Google Sheets tracking system
- ✅ Crypto module enabled on n8n server

### Known Issues Fixed
- ✅ "UNKNOWN" classification bug (fixed - was erasing extractedText)
- ✅ Crypto module error (fixed - enabled NODE_FUNCTION_ALLOW_BUILTIN: crypto)
- ✅ Google Document AI authentication (working with JWT)
- ✅ Evaluation Quality node bug (fixed - extractedText vs text field mismatch)

### Current Performance
- **Test Success Rate:** 1/15 documents correctly classified (execution 3612)
  - Successfully identified: "Schlossberg 13"
  - Previously failed: 13/15 labeled as "UNKNOWN" (before fix)
- **Text Extraction:** Working (2300 chars, 273 words from test doc)
- **OCR Quality:** Good (German text extraction working)

---

## Planned Upgrade (v9 Phase 1)

### Phase 2: Claude Vision Implementation
**Goal:** Replace current 3-step process (OCR → Evaluate → AI Classification) with single Claude Vision call

**Current Flow (v8):**
```
Download PDF → Document AI OCR → Parse Response → Evaluate Quality → OpenAI Classification
```

**New Flow (v9):**
```
Download PDF → Convert to Base64 → Claude Vision Extract Identifier → Normalize
```

**Expected Improvements:**
- Single API call instead of 3
- Better German document understanding
- Visual context awareness (maps, Grundbuch diagrams)
- More accurate address extraction
- Simplified pipeline

### Phase 3: Batch Grouping (Future)
**Goal:** Group documents from same email by common identifier
- Extract identifiers from ALL attachments
- Find common patterns (addresses, project names)
- Assign all docs to same project
- Reduce "UNKNOWN" classifications

---

## Credentials & Configuration

### APIs in Use (v8)
1. **Google Document AI**
   - Service Account: n8n-document-ai@n8n-integrations-482020.iam.gserviceaccount.com
   - Authentication: JWT (RS256)
   - Scope: cloud-platform

2. **OpenAI GPT-4o**
   - Model: gpt-4o
   - Operation: Chat Completion (messages)
   - Purpose: Client name extraction from OCR text

3. **AWS Textract**
   - Purpose: OCR for scanned documents
   - Credential: AWS (IAM) account

4. **Google Drive OAuth**
   - Purpose: File download/upload, folder management

5. **Google Sheets**
   - Purpose: Client registry, document tracking

### Server Configuration
- **n8n Server:** Digital Ocean (157.230.21.230)
- **Docker Environment:** NODE_FUNCTION_ALLOW_BUILTIN: crypto

---

## Restoration Instructions

If you need to roll back to v8:

1. **Import workflows:**
   ```bash
   # Use n8n UI: Settings → Import from file
   # Import each JSON file separately
   ```

2. **Verify credentials:**
   - Check Google Document AI credential (JWT format)
   - Check OpenAI API credential
   - Check AWS Textract credential
   - Check Google Drive OAuth

3. **Test execution:**
   - Use Test Helper workflow to send test email
   - Verify Pre-Chunk 0 execution completes
   - Check Google Sheets for tracking entry

4. **Verify crypto module:**
   ```bash
   ssh -i ~/.credentials/n8n-server-ssh.key root@157.230.21.230
   cd /root/n8n
   grep NODE_FUNCTION_ALLOW_BUILTIN docker-compose.yml
   # Should show: NODE_FUNCTION_ALLOW_BUILTIN: crypto
   ```

---

## Related Documentation

- **Credentials:** `/Users/swayclarke/coding_stuff/CREDENTIALS.md`
- **n8n Patterns:** `/Users/swayclarke/coding_stuff/N8N_PATTERNS.md`
- **Project Reference:** `/Users/swayclarke/coding_stuff/PROJECT_REFERENCE.md`
- **Claude Vision Plan:** `/Users/swayclarke/.claude/plans/giggly-cuddling-hartmanis.md`

---

## Changelog

| Date | Version | Change | Reason |
|------|---------|--------|--------|
| Jan 17, 2026 | v8.0 | Backup before Claude Vision | Preserve working state before major upgrade |
| Jan 17, 2026 | v8.0 | Fixed UNKNOWN classification bug | extractedText vs text field mismatch |
| Jan 16, 2026 | v8.0 | Added Google Document AI OCR | Handle scanned PDFs |
| Jan 15, 2026 | v8.0 | Enabled crypto module | Fix JWT signing for Document AI |
| Jan 12, 2026 | v8.0 | Fixed AI prompt | Accept street addresses as identifiers |

---

**Next Steps:**
1. Archive this v8_phase_1 folder
2. Create v9_phase_1 folder
3. Implement Claude Vision upgrade (Phase 2)
4. Test and validate
5. Add batch grouping (Phase 3)
