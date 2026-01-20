# V6 Phase 1 - Workflow Registry
**Backup Date:** January 11, 2026 11:40 CET
**Status:** All workflows active and operational

## Workflow IDs and Status

| Workflow | ID | Status | Version Counter | Last Updated | Blueprint File |
|----------|-----|--------|-----------------|--------------|----------------|
| **Pre-Chunk 0 - REBUILT v1** | YGXWjWcBIk66ArvT | ✅ ACTIVE | 42 | 2026-01-09 09:56 | pre_chunk_0_v6.0_20260111.json (129KB) |
| **Chunk 0: Folder Initialization** | zbxHkXOoD1qaz6OS | ✅ ACTIVE | 108 | 2026-01-11 10:08 | chunk_0_v6.0_20260111.json (72KB) |
| **Chunk 2: Text Extraction** | qKyqsL64ReMiKpJ4 | ✅ ACTIVE | 63 | 2026-01-11 10:25 | Full workflow available in n8n |
| **Chunk 2.5: Client Document Tracking** | okg8wTqLtPUwjQ18 | ✅ ACTIVE | 103 | 2026-01-11 10:25 | Full workflow available in n8n |
| **Test Email Sender** | RZyOIeBy7o3Agffa | ✅ ACTIVE | 98 | 2026-01-11 10:00 | Full workflow available in n8n |

## Key Changes Since v6.0 (Jan 9, 2026)

### Chunk 0 - Client_Tracker Initialization ⭐ NEW
**Added nodes:**
- **"Prepare Client_Tracker Row"** (Code node) - Normalizes client name and maps all 37 folder IDs to Client_Tracker columns
- **"Write to Client_Tracker"** (Google Sheets node) - Appends initialized client row to Client_Tracker sheet

**Purpose:** Automatically populates Client_Tracker when creating new client folder structures, enabling Chunk 2.5 to find clients without "client not found" errors.

**Spreadsheet:** Client_Tracker (12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I)

### Chunk 2 - GPT-4 Turbo Model
**Changed:** HTTP Request node now uses `gpt-4-turbo` model (was `gpt-3.5-turbo`)

**Purpose:** Improved text extraction accuracy for scanned documents

### Chunk 2.5 - GPT-4 Turbo Classification
**Changed:** HTTP Request node now uses `gpt-4-turbo` model with JSON mode

**Purpose:** More accurate document classification (Exposé, Grundbuch, Calculation, Exit_Strategy, Other)

## Testing Status

**Clean Slate Test Pending:**
- Google Sheets cleaned (Client_Registry, AMA_Folder_IDs, Client_Tracker)
- Google Drive cleaned (all client folders removed)
- Ready for end-to-end validation test

## Rollback Instructions

To rollback to Jan 9, 2026 version:
1. Stop all workflows
2. Import from `_archive/` folder:
   - `pre_chunk_0_v6.0_20260109.json`
   - `chunk_0_v6.0_20260109.json`
   - `chunk_2_v6.0_20260109.json`
3. Reactivate workflows
4. Remove Client_Tracker initialization (if needed)

## Notes

- Pre-Chunk 0 and Chunk 0 have complete blueprint JSONs saved
- Chunk 2, 2.5, and Test Email Sender are fully available in n8n (can be exported via UI if needed)
- All workflows validated via n8n MCP API on Jan 11, 2026
