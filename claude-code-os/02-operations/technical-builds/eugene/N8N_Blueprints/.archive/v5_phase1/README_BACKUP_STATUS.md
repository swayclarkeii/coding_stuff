# Eugene Document Organizer - Backup Status

**Date:** 2026-01-09
**Status:** ⚠️ Pending - n8n database temporarily unavailable

---

## Current Situation

The n8n database is temporarily unavailable, preventing workflow export via API. This is a temporary infrastructure issue (database restart/maintenance).

### Latest Valid Backups

| File | Date | Size | Status |
|------|------|------|--------|
| `PRE_CHUNK_0_IMPORT.json` | Jan 6 | 41K | ✅ Valid |
| `pre_chunk_0_v1.4_20260105.json` | Jan 5 | 84K | ✅ Valid |

**Note:** These backups are from BEFORE the fixes applied on Jan 9, 2026.

---

## Changes Made Today (Jan 9) - Not Yet Backed Up

All changes were applied successfully via n8n API and are live in the workflows. They just need to be exported once the database is available:

### Pre-Chunk 0 (YGXWjWcBIk66ArvT)
- ✅ Fixed JavaScript syntax errors in "Execute Chunk 2" nodes
- ✅ Removed `||` operators from field expressions
- ✅ Updated type conversion settings

### Chunk 2 (g9J5kjVtqaF9GLyc)
- ✅ Fixed Chunk 2.5 Execute Workflow Trigger schema (added 10 fields)
- ✅ Fixed Execute Chunk 2.5 node schema
- ✅ Fixed IF Needs OCR1 duplicate options field

### Chunk 2.5 (okg8wTqLtPUwjQ18)
- ✅ Added Execute Workflow Trigger schema for 10 input fields

---

## How to Backup When Database is Available

### Option 1: Run the Backup Script

```bash
cd /Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/N8N_Blueprints/v5_phase1
./backup_workflows.sh
```

The script will:
1. Check if database is available
2. Backup all 3 workflows with today's date
3. Create files: `pre-chunk-0_v5.0_YYYYMMDD.json`, `chunk-2_v5.0_YYYYMMDD.json`, `chunk-2.5_v5.0_YYYYMMDD.json`

### Option 2: Manual Backup via n8n UI

1. Open https://n8n.oloxa.ai/
2. Navigate to each workflow
3. Click "..." menu → "Download"
4. Save to this folder with naming: `[workflow-name]_v5.0_20260109.json`

---

## Workflow IDs

| Workflow | ID |
|----------|-----|
| Pre-Chunk 0: Email Intake & Client Detection | `YGXWjWcBIk66ArvT` |
| Chunk 2: Text Extraction | `g9J5kjVtqaF9GLyc` |
| Chunk 2.5: Client Document Tracking | `okg8wTqLtPUwjQ18` |

---

## Next Steps

1. **Wait for n8n database to become available** (usually a few minutes)
2. **Run backup script** or manually download workflows
3. **Verify backups** are > 1KB (valid JSON)
4. **Archive old versions** to `.archive/` folder if needed

---

## Verification

Once backups are created, verify they contain today's fixes:

**Pre-Chunk 0:**
- Search for: `"convertFieldsToString": false`
- Should NOT contain: `|| 0` or `|| false` in Execute Chunk 2 nodes

**Chunk 2:**
- Execute Chunk 2.5 node should have full `schema` array with 10 fields
- IF Needs OCR1 node should NOT have duplicate `options` field

**Chunk 2.5:**
- Execute Workflow Trigger should have `schema` array with 10 fields

---

## Contact

If database remains unavailable for > 1 hour, check:
- n8n instance health: https://n8n.oloxa.ai/healthz
- Database logs
- Restart n8n instance if needed
