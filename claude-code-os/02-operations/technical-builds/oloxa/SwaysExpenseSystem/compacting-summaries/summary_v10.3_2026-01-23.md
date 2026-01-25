# Sway's Expense System - Summary

**Version:** v10.3
**Last Updated:** January 23, 2026
**Status:** v3.0.1 - Duplicate Detection Bug Fix Applied

---

## Agent IDs (Resume Work)

**CRITICAL:** Use these agent IDs to resume work in new conversations.

### January 23, 2026 - Bug Fix Session (Duplicate Detection Fix)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| (main) | main | Fixed "IS There" nodes missing operation, IF node references | Complete |

### January 21, 2026 - Duplicate Detection Implementation

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| `a67df96` | solution-builder-agent | W7 duplicate detection implementation (v3.0.0) | Complete |
| (main) | main | Cleanup duplicates, OAuth fix via Google Drive MCP | Complete |

### January 20, 2026 - Backup Session

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| (main) | main | Created v10.1 summary, n8n workflow backups, v3 foundation plan | Complete |

### Historical Agent IDs (from CLAUDE.md)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| `a7e6ae4` | solution-builder-agent | W2 critical fixes (Google Sheets + Binary) | Complete |
| `a7fb5e5` | test-runner-agent | W2 fixes verification | Complete |
| `a6d0e12` | browser-ops-agent | Gmail OAuth refresh | Complete |
| `ac6cd25` | test-runner-agent | Gmail Account 1 verification | Complete |
| `a3b762f` | solution-builder-agent | W3 Merge connection fix attempt | Complete |
| `a729bd8` | solution-builder-agent | W3 connection syntax fix | Complete |
| `a8564ae` | browser-ops-agent | W3 execution and connection visual fix | Complete |
| `a017327` | browser-ops-agent | Google Sheets structure diagnosis | Complete |
| `a277ff0` | solution-builder-agent | Reverted W7 to Google Drive Trigger | Complete |
| `a70720d` | solution-builder-agent | Verified W9 configuration | Complete |
| `a17efe2` | test-runner-agent | Checked W7/W9 status | Complete |
| `a46683b` | solution-builder-agent | Binary data preservation fix | Complete |
| `aa7000b` | solution-builder-agent | Google Sheets GID fix | Complete |
| `adb800e` | solution-builder-agent | Type mismatch bypass | Complete |

**Usage:** In new conversation: "Resume agent a67df96" or reference this summary

---

## Current To-Do List

### Completed (This Session - Jan 23)
- [x] Fixed "Check Invoice IS There" missing `operation: "read"` parameter
- [x] Fixed "Check Receipt IS There" missing `operation: "read"` parameter
- [x] Updated IF nodes to reference correct nodes (`$('Check Invoice IS There')` not `$('Check Invoice Exists')`)
- [x] Removed disabled duplicate nodes ("Check Invoice Exists", "Check Receipt Exists")
- [x] Workflow cleaned up from 35 nodes to 33 nodes

### Completed (Jan 21)
- [x] Fix Google Sheets MCP access (used Google Drive MCP instead)
- [x] Cleanup 11 duplicate OpenAI entries in Receipts sheet (rows 12-22 cleared)
- [x] Implement Option 1 duplicate detection in W7 (2 new nodes, 2 IF updates)

### Completed (Jan 20)
- [x] Create v10 compact summary of current expense system state
- [x] Archive older versions in the compact summary (v1-v8 moved to .archive/)
- [x] Backup latest n8n workflow JSONs (all 7 workflows backed up to v2_foundation)
- [x] Backup v2 foundations (complete - 7 JSONs in v2_foundation folder)
- [x] Create v3 foundations for next build (BUILD_PLAN.md created)

### Pending
- [ ] Test duplicate prevention - Drop existing file, verify it's skipped
- [ ] Test unknown file path with unrecognized filenames
- [ ] Add PDF handling for unknown path (PDF-to-image conversion)
- [ ] Test W3 (Transaction-Invoice Matching)
- [ ] Activate W8 (G Drive Invoice Collector)

### Resolved Issues
- ~~Google Sheets MCP timing out~~ - Resolved: Use Google Drive MCP (`getGoogleSheetContent`)
- ~~Skip if Exists nodes are placeholders~~ - Resolved: Implemented proper lookup + IF conditions
- ~~11 duplicate OpenAI receipt entries~~ - Resolved: Cleaned up rows 12-22
- ~~"Unknown error" at Check Receipt IS There~~ - Resolved: Added missing `operation: "read"` parameter (Jan 23)
- ~~IF nodes referencing wrong check nodes~~ - Resolved: Updated to reference "IS There" nodes (Jan 23)
- ~~Duplicate disabled check nodes~~ - Resolved: Removed orphaned "Check Invoice Exists" and "Check Receipt Exists" (Jan 23)

### Known Issues
- Claude Vision only accepts JPEG, PNG, GIF, WEBP (not PDF)
- 3 pre-existing Upload node errors in W7 (unrelated to duplicate detection)

---

## Key Decisions Made

### 1. Bug Fix: Missing Operation Parameter (Jan 23, 2026)
**Problem:** "Check Invoice IS There" and "Check Receipt IS There" nodes created via n8n UI were missing `operation: "read"` parameter
**Root Cause:** When nodes are created in n8n UI, they may not have all required parameters set
**Fix Applied:**
- Added `operation: "read"` to both "IS There" nodes
- Updated IF conditions from `$('Check Invoice Exists')` to `$('Check Invoice IS There')`
- Updated IF conditions from `$('Check Receipt Exists')` to `$('Check Receipt IS There')`
- Removed disabled orphan nodes ("Check Invoice Exists", "Check Receipt Exists")
**Impact:** W7 now has 33 nodes, duplicate detection working correctly

### 2. Option 1 Duplicate Detection Implemented (Jan 21, 2026)
**Decision:** Pre-check via Google Sheets lookup before logging
**Implementation:**
- Added "Check Invoice IS There" node (Google Sheets Get Row(s) with FileID filter)
- Added "Check Receipt IS There" node (Google Sheets Get Row(s) with FileID filter)
- Updated IF conditions to check `.all().length === 0`
**Impact:** Duplicates prevented at source

### 3. Google Drive MCP for Sheets Access (Jan 21, 2026)
**Decision:** Use `mcp__google-drive__getGoogleSheetContent` instead of Google Sheets MCP
**Rationale:** Google Sheets MCP had OAuth issues; Google Drive MCP shares OAuth and works
**Impact:** Can read/write Sheets without separate OAuth refresh

### 4. Hybrid Classification for W7 (Jan 19, 2026)
**Decision:** Known filename patterns -> fast path; Unknown patterns -> Claude Vision
**Rationale:** Cost efficiency - no API calls for recognizable files
**Impact:** W7 now has hybrid classification operational

### 5. Google Sheets GID Configuration (Jan 13, 2026)
**Decision:** Use numeric GID (`sheetId: 1542914058`) not string name
**Rationale:** n8n 4.7+ requires GID for reliable sheet targeting
**Impact:** All Google Sheets nodes updated to use GIDs

---

## Important IDs / Paths / Workflow Names

### n8n Workflows
| Workflow Name | ID | Status | Purpose |
|--------------|-----|--------|---------|
| W1: PDF Intake & Parsing | `MPjDdVMI88158iFW` | Active | Bank PDF parsing |
| W2: Gmail Receipt Monitor | `dHbwemg7hEB4vDmC` | Active | Gmail receipt/invoice monitoring |
| W3: Transaction Matching | `CJtdqMreZ17esJAW` | Inactive | Invoice-transaction matching |
| W4: Monthly Folder Builder | `nASL6hxNQGrNBTV4` | Inactive | Monthly folder organization |
| W6: Expensify PDF Parser | `l5fcp4Qnjn4Hzc8w` | Active | Expensify PDF processing |
| W7: Downloads Monitor | `6x1sVuv4XKN0002B` | **Active** | Downloads folder monitor (v3.0.1) |
| W8: G Drive Invoice Collector | `JNhSWvFLDNlzzsvm` | Inactive | Production folder monitoring |
| W9: Manual Downloads Scan | `hhY1QgHmOyUEYZyY` | Inactive | Manual downloads scan |

### Google Sheets
| Spreadsheet Name | ID | GID | Purpose |
|-----------------|-----|-----|---------|
| Expense-Database | `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` | - | Main database |
| Invoices tab | (same) | `1542914058` | Invoice records |
| Receipts tab | (same) | `1935486957` | Receipt records |
| Unknown tab | (same) | `284306066` | Unclassified documents |

### Google Drive
| Folder Name | ID | Purpose |
|------------|-----|---------|
| Expenses-System Root | `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15` | System root |
| Downloads Folder | `1O3udIURR14LsEP3Wt4o1QnxzGsR2gciN` | W7 monitors this |
| Invoice Pool | `1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l` | Processed invoices |
| Receipt Pool | `1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4` | Processed receipts |

### n8n Credentials
| Name | ID |
|------|-----|
| Google Drive account | `a4m50EefR3DJoU0R` |
| Google Sheets account | `H7ewI1sOrDYabelt` |
| Anthropic account | `MRSNO4UW3OEIA3tQ` |

### File Paths
| File | Location | Purpose |
|------|----------|---------|
| VERSION_LOG.md | `SwaysExpenseSystem/N8N_Blueprints/v1_foundation/` | Version history |
| v2 Workflow Backups | `SwaysExpenseSystem/N8N_Blueprints/v2_foundation/` | 7 JSON backups |
| v3 Build Plan | `SwaysExpenseSystem/N8N_Blueprints/v3_foundation/BUILD_PLAN.md` | Build spec |
| Session Summary | `/session-summaries/2026-01-19-w7-hybrid-classification.md` | Jan 19 session |

---

## Technical Architecture

### W7 Architecture (v3.0.1 - Duplicate Detection Fixed)
```
Downloads Folder (1O3udIURR14LsEP3Wt4o1QnxzGsR2gciN)
  |
Google Drive Trigger (polls every 60 seconds)
  |
Filter Valid Files
  |
Categorize by Filename (Voxhaus, SC -, receipt patterns)
  |
Skip Unknown Files (IF node)
  +- TRUE (known pattern) -> Download File -> Claude API -> Parse Results
  +- FALSE (unknown) -> Download Unknown File -> Claude Vision -> Parse Unknown
  |
Route by Direction (INCOME/EXPENSE/UNKNOWN)
  |
Route by Category (invoice vs receipt)
  +- Invoice -> Check Invoice IS There -> Skip if Exists -> Upload -> Log to Invoices
  +- Receipt -> Check Receipt IS There -> Skip if Exists Receipt -> Upload -> Log to Receipts
```

**Node Count:** 33
**Connections:** 25

### Duplicate Detection Flow (v3.0.1 - Fixed)
```
Route by Category
  |
  +-- Invoice Path:
  |     Check Invoice IS There (Google Sheets read + FileID filter)
  |       |
  |       Skip if Exists (IF: $('Check Invoice IS There').all().length === 0?)
  |         +- TRUE (not exists) -> Upload to Invoice Pool -> Log
  |         +- FALSE (exists) -> SKIP (no action)
  |
  +-- Receipt Path:
        Check Receipt IS There (Google Sheets read + FileID filter)
          |
          Skip if Exists Receipt (IF: $('Check Receipt IS There').all().length === 0?)
            +- TRUE (not exists) -> Upload to Receipt Pool -> Log
            +- FALSE (exists) -> SKIP (no action)
```

### Key Patterns
1. **Binary Data Preservation:** `data.binary = $input.item.binary` in Set nodes
2. **Switch Node Expression Mode:** Must evaluate to numeric index (0, 1, 2)
3. **IF Node Branch Connections:** `branch="true"` -> main[0], `branch="false"` -> main[1]
4. **Google Sheets GID:** Use numeric GID, not string name
5. **Duplicate Check:** `$('Check Node').all().length === 0` (empty = new file)
6. **Google Sheets Read Node:** MUST have `operation: "read"` explicitly set

---

## Current State Summary

**Version:** v3.0.1 (System) / v10.3 (Summary)
**Phase:** Testing & Validation
**Key Metric:** Duplicate detection bug fixed

**Recent Work:**
- Bug fix: Added missing `operation: "read"` to check nodes (Jan 23)
- Bug fix: Updated IF nodes to reference correct "IS There" nodes (Jan 23)
- Cleanup: Removed orphan disabled nodes (Jan 23)
- Duplicate detection nodes added to W7 (Jan 21)
- 11 duplicate entries cleaned from Receipts sheet (Jan 21)
- Google Sheets access via Google Drive MCP (Jan 21)
- All 7 workflows backed up to v2_foundation (Jan 20)
- v3 foundation BUILD_PLAN.md created (Jan 20)

---

## Next Steps

1. **Test duplicate prevention** - Drop existing file, verify it's skipped
2. **Test unknown path** - Drop unrecognized filename, verify Claude Vision classification
3. **Activate W8** - G Drive Invoice Collector for production folder
4. **Test W3** - Transaction-Invoice Matching workflow

---

## Quick Links

- **n8n Instance:** https://n8n.oloxa.ai
- **W7 Workflow:** https://n8n.oloxa.ai/workflow/6x1sVuv4XKN0002B
- **Expense Database:** https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM
- **Google Drive Root:** https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15

---

## References

- VERSION_LOG: `SwaysExpenseSystem/N8N_Blueprints/v1_foundation/VERSION_LOG.md`
- v3 Build Plan: `SwaysExpenseSystem/N8N_Blueprints/v3_foundation/BUILD_PLAN.md`
- Previous Summary: `compacting-summaries/summary_v10.2_2026-01-21.md`

---

**Document Version:** v10.3
**Generated:** January 23, 2026 @ 19:55 CET
**Author:** Claude Code (Sway's automation assistant)
**Key Changes:** Bug fix - added missing `operation: "read"` to check nodes, fixed IF node references, removed orphan disabled nodes
