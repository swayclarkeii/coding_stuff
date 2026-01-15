# Workflow Backup Manifest

**Backup Date**: 2026-01-06T10:28:42+01:00
**Reason**: Pre-Phase 2 testing backup - all workflows production ready
**Created By**: Claude Code (automated backup)

---

## Backup Files Created

### 1. Pre-Chunk 0: Intake & Client Identification
- **File**: `backup_pre_chunk_0_2026-01-06.json`
- **Workflow ID**: `6MPoDSf8t0u8qXQq`
- **Status**: INACTIVE (ready to activate for testing)
- **Nodes**: 28
- **Connections**: 24
- **Version**: 18
- **Last Updated**: 2026-01-06T09:18:55.587Z
- **Production Readiness**: 92% (validated, zero blocking errors)

**Key Features**:
- Gmail trigger with PDF attachment detection
- AI client name extraction (OpenAI)
- Client Registry lookup (Google Sheets)
- Three execution paths: NEW, EXISTING, UNKNOWN
- Execute Chunk 0 for NEW clients
- Execute Chunk 1 for EXISTING clients
- Move to 38_Unknowns for UNKNOWN clients

---

### 2. Chunk 0: Folder Initialization
- **File**: `backup_chunk_0_2026-01-06.json`
- **Workflow ID**: `zbxHkXOoD1qaz6OS`
- **Status**: ACTIVE
- **Nodes**: 17
- **Connections**: 16
- **Version**: 78
- **Last Updated**: 2025-12-28T14:41:49.949Z

**Key Features**:
- Creates client folder structure in Google Drive
- Subfolder creation: 38_Unknowns, 01_Staging
- Client Registry updates (Google Sheets)
- Email notifications for new clients
- Returns folder IDs to Pre-Chunk 0

---

### 3. Chunk 1: Move to Staging
- **File**: `backup_chunk_1_2026-01-06.json`
- **Workflow ID**: `djsBWsrAEKbj2omB`
- **Status**: ACTIVE
- **Nodes**: 11 (5 disabled ZIP extraction nodes)
- **Connections**: 10
- **Version**: 114
- **Last Updated**: 2026-01-04T20:50:17.535Z

**Key Features**:
- Moves file to staging folder (Google Drive)
- Email notification on successful move
- Prepares output for Chunk 2
- ZIP extraction nodes DISABLED (Phase 1 doesn't support ZIP)

---

### 4. Chunk 2: Text Extraction
- **File**: `backup_chunk_2_2026-01-06.json`
- **Workflow ID**: `g9J5kjVtqaF9GLyc`
- **Status**: INACTIVE (to be activated in Phase 2)
- **Nodes**: 8
- **Connections**: 7
- **Version**: 6
- **Last Updated**: 2025-12-24T11:00:42.969Z

**Key Features**:
- Downloads PDF from staging folder
- Extracts text using n8n extractFromFile
- Detects scanned documents (<100 chars)
- AWS Textract OCR for scanned PDFs
- Outputs normalized text for Chunk 2.5

---

## Backup Validation

✅ All 4 workflows backed up successfully
✅ Full workflow JSON preserved (nodes, connections, settings)
✅ Metadata captured (version IDs, node counts, status)
✅ Backup reason documented
✅ Timestamped for version tracking

---

## Restore Instructions

**To restore a workflow**:

1. Navigate to n8n workflow: `https://n8n.oloxa.ai/workflow/{workflow_id}`
2. Click "..." menu → "Import from File" or "Replace workflow"
3. Browse to backup file: `/Users/swayclarke/coding_stuff/backups/backup_*_2026-01-06.json`
4. Extract `workflow_data` field from JSON
5. Import the workflow_data object
6. Re-link credentials (Gmail, Google Drive, Google Sheets, OpenAI)
7. Save and activate

**Alternative - Use MCP tool**:
```javascript
mcp__n8n-mcp__n8n_update_full_workflow({
  id: "WORKFLOW_ID",
  nodes: backup.workflow_data.nodes,
  connections: backup.workflow_data.connections,
  settings: backup.workflow_data.settings
})
```

---

## Next Steps

**Phase 2 Ready**: All workflows backed up before Phase 2 testing begins.

**Proceed with**:
1. ✅ **Backups Complete** - All 4 workflows preserved
2. ⏳ **Phase 2** - Test Chunk 1 → Chunk 2 integration
   - Activate Chunk 2 workflow
   - Connect Chunk 1 to Chunk 2
   - Test digital PDF text extraction
   - Test scanned PDF OCR (AWS Textract)
3. ⏳ **Phase 3** - Configure AWS Textract OCR
4. ⏳ **Phase 4** - Create Chunk 2.5 (project tracking)
5. ⏳ **Phase 5** - Create webhook test harness
6. ⏳ **Phase 6** - End-to-end integration tests

---

## Backup Retention

**Location**: `/Users/swayclarke/coding_stuff/backups/`
**Retention**: Keep indefinitely for rollback capability
**Versioning**: Date-stamped for tracking multiple backup points

**Recommended**: Create new backup set before each major change phase.

---

**Backup Manifest Created**: 2026-01-06T10:28:42+01:00
**Status**: ✅ ALL BACKUPS COMPLETE
