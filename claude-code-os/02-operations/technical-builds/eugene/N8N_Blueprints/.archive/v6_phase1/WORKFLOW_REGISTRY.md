# Eugene Document Organizer - Workflow Registry (v6 Phase 1)

**Date:** 2026-01-09
**Status:** Active Production Workflows

---

## Active Workflows

| Workflow Name | ID | Status | Last Updated |
|--------------|-----|--------|--------------|
| Pre-Chunk 0: Email Intake & Client Detection | YGXWjWcBIk66ArvT | ✅ Active | 2026-01-08 |
| Chunk 0: Folder Initialization | zbxHkXOoD1qaz6OS | ✅ Active | 2026-01-07 |
| Chunk 2: Text Extraction | **qKyqsL64ReMiKpJ4** | ✅ Active | 2026-01-09 |
| Chunk 2.5: Client Document Tracking | okg8wTqLtPUwjQ18 | ⏳ Active | 2026-01-09 |

---

## Workflow Details

### Pre-Chunk 0: Email Intake & Client Detection
- **ID:** YGXWjWcBIk66ArvT
- **URL:** https://n8n.oloxa.ai/workflow/YGXWjWcBIk66ArvT
- **Trigger:** Gmail (swayclarkeii@gmail.com)
- **Purpose:** Detects incoming emails, extracts PDFs, identifies clients, and routes to Chunk 0 or Chunk 2
- **Backup:** `pre_chunk_0_v6.0_20260109.json`

### Chunk 0: Folder Initialization
- **ID:** zbxHkXOoD1qaz6OS
- **URL:** https://n8n.oloxa.ai/workflow/zbxHkXOoD1qaz6OS
- **Trigger:** Execute Workflow (called by Pre-Chunk 0)
- **Purpose:** Creates Google Drive folder structure for new clients
- **Backup:** `chunk_0_v6.0_20260109.json`

### Chunk 2: Text Extraction
- **ID:** qKyqsL64ReMiKpJ4 ⚠️ **NEW (replaced g9J5kjVtqaF9GLyc)**
- **URL:** https://n8n.oloxa.ai/workflow/qKyqsL64ReMiKpJ4
- **Trigger:** Execute Workflow (called by Pre-Chunk 0)
- **Purpose:** Extracts text from PDFs, handles OCR for scanned documents, optimizes by skipping downloads when text is already extracted
- **Backup:** `chunk_2_v6.0_20260109.json`
- **Changes:**
  - Fixed configuration errors that prevented UI loading
  - Re-imported from clean JSON backup
  - Activated successfully on 2026-01-09

### Chunk 2.5: Client Document Tracking
- **ID:** okg8wTqLtPUwjQ18
- **URL:** https://n8n.oloxa.ai/workflow/okg8wTqLtPUwjQ18
- **Trigger:** Execute Workflow (called by Chunk 2)
- **Purpose:** Classifies documents using AI, moves files to final locations, updates Client_Tracker sheet
- **Status:** Not yet tested in v6 phase 1

---

## Deleted/Deprecated Workflows

| Workflow Name | Old ID | Deleted Date | Reason |
|--------------|---------|--------------|--------|
| Chunk 2: Text Extraction (OLD) | g9J5kjVtqaF9GLyc | 2026-01-09 | UI loading error - replaced with clean import |

---

## Workflow Execution Flow

```
Email arrives → Pre-Chunk 0 (YGXWjWcBIk66ArvT)
                      ↓
                [Check if client exists]
                      ↓
            ┌─────────┴─────────┐
            │                   │
       NEW CLIENT          EXISTING CLIENT
            │                   │
            ↓                   ↓
    Chunk 0                  Chunk 2
(zbxHkXOoD1qaz6OS)    (qKyqsL64ReMiKpJ4)
    Create folders         Extract text
            │                   │
            └─────────┬─────────┘
                      ↓
                  Chunk 2.5
              (okg8wTqLtPUwjQ18)
              Classify & Move
```

---

## Testing Status

| Flow | Last Tested | Status | Notes |
|------|-------------|--------|-------|
| Pre-Chunk 0 → Chunk 0 (NEW) | 2026-01-08 | ✅ Pass | Folder creation working |
| Pre-Chunk 0 → Chunk 2 (EXISTING) | 2026-01-09 | ⏳ Pending | New Chunk 2 needs testing |
| Chunk 2 → Chunk 2.5 | TBD | ⏳ Pending | End-to-end test needed |

---

## Credentials Used

| Service | Credential ID | Used By |
|---------|---------------|---------|
| Google Drive | a4m50EefR3DJoU0R | Pre-Chunk 0, Chunk 0, Chunk 2 |
| AWS Textract | G6y6PdRQ94Y85Jar | Chunk 2 (OCR fallback) |
| OpenAI GPT-4 | TBD | Chunk 2.5 (AI classification) |

---

## Quick Links

- **n8n Instance:** https://n8n.oloxa.ai
- **Workflow List:** https://n8n.oloxa.ai/home/workflows
- **Executions:** https://n8n.oloxa.ai/executions
- **v6 Phase 1 Folder:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/N8N_Blueprints/v6_phase1/`

---

## Version History

- **v6.0 (2026-01-09):** Clean slate - re-imported all workflows with fixes applied
- **v5.0 (2026-01-05):** Previous version with configuration issues
- **v4.0:** Initial production deployment
