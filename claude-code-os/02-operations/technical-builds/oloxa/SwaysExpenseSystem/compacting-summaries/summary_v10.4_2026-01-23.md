# Sway's Expense System - Summary

**Version:** v10.4
**Last Updated:** January 23, 2026
**Status:** v3.0.2 - Core Fixes Complete, Duplicate Detection STILL FAILING

---

## CRITICAL ISSUE: Duplicate Detection Not Working

**Problem:** Despite all configuration fixes, duplicate detection still causes workflow to stop/error when enabled.

**What We Tried:**
1. Added `operation: "read"` to Check nodes
2. Added `range: "A:Z"` parameter
3. Changed typeVersion from 4.7 to 4.5
4. Fixed IF node references to correct node names
5. Enabled all 4 duplicate detection nodes
6. Rewired connections properly

**Current State:** Duplicate detection nodes are DISABLED to allow workflow to function. Files process correctly but duplicates are not prevented.

**Needs Investigation:**
- Why does Google Sheets read with filter cause workflow to stop?
- Is it a credential issue? OAuth scope issue?
- Is the FileID filter expression wrong?
- Alternative approaches needed

---

## Agent IDs (Resume Work)

**CRITICAL:** Use these agent IDs to resume work in new conversations.

### January 23, 2026 - Evening Session (Multiple Fixes)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| (main) | main | Binary bug fix, Direction routing, Source/Date fixes, Duplicate attempts | Complete |

### January 23, 2026 - Earlier Session (Duplicate Detection Fix Attempt)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| (main) | main | Fixed "IS There" nodes missing operation, IF node references | Complete |

### January 21, 2026 - Duplicate Detection Implementation

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| `a67df96` | solution-builder-agent | W7 duplicate detection implementation (v3.0.0) | Complete |
| (main) | main | Cleanup duplicates, OAuth fix via Google Drive MCP | Complete |

### Historical Agent IDs

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| `a7e6ae4` | solution-builder-agent | W2 critical fixes (Google Sheets + Binary) | Complete |
| `a46683b` | solution-builder-agent | Binary data preservation fix | Complete |
| `aa7000b` | solution-builder-agent | Google Sheets GID fix | Complete |

---

## Current To-Do List

### Completed (This Session - Jan 23 Evening)
- [x] Fixed binary data bug: `getBinaryDataBuffer(0,...)` → `getBinaryDataBuffer($itemIndex,...)`
- [x] Changed routing from Category to Direction (INCOME→Invoices, EXPENSE→Receipts)
- [x] Updated Receipt Pool upload to Hard Drive folder (`1Qbqx9uiGiODsLE9TVEFG5NRysRJCFMnY`)
- [x] Fixed ProcessedDate format: ISO → "Jan 23, 2026, 9:45 PM"
- [x] Fixed Source field: "Downloads" → "Hard Drive"
- [x] Added FileName to sheet data preparation
- [x] Backed up workflow JSON to v3_foundation

### Completed (Jan 23 Earlier)
- [x] Fixed "Check Invoice IS There" missing `operation: "read"` parameter
- [x] Fixed "Check Receipt IS There" missing `operation: "read"` parameter
- [x] Updated IF nodes to reference correct nodes
- [x] Removed disabled duplicate nodes ("Check Invoice Exists", "Check Receipt Exists")

### BLOCKED - Needs Alternative Approach
- [ ] **Duplicate detection** - Google Sheets lookup approach not working

### Pending
- [ ] Test unknown file path with unrecognized filenames
- [ ] Add PDF handling for unknown path (PDF-to-image conversion)
- [ ] Test W3 (Transaction-Invoice Matching)
- [ ] Activate W8 (G Drive Invoice Collector)

---

## Key Fixes Applied This Session

### 1. Binary Data Bug (CRITICAL FIX)
**Problem:** All files got same extraction data (always first file's data)
**Root Cause:** `getBinaryDataBuffer(0, binaryPropertyName)` - hardcoded index 0
**Fix:** Changed to `getBinaryDataBuffer($itemIndex, binaryPropertyName)` in both:
- Build Anthropic Request
- Build Anthropic Request (Unknown)

### 2. Direction-Based Routing
**Before:** Category-based (invoice vs receipt by documentType)
**After:** Direction-based:
- INCOME → Invoices sheet
- EXPENSE → Receipts sheet
- UNKNOWN → Unknown sheet

### 3. Receipt Pool Folder Update
**Before:** Gmail folder (for email receipts)
**After:** Hard Drive folder (`1Qbqx9uiGiODsLE9TVEFG5NRysRJCFMnY`) for computer files

### 4. Sheet Data Improvements
- ProcessedDate: Now readable format "Jan 23, 2026, 9:45 PM"
- Source: Changed from "Downloads" to "Hard Drive"
- FileName: Now being populated (was missing before)

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
| W7: Downloads Monitor | `6x1sVuv4XKN0002B` | **Active** | Downloads folder monitor (v3.0.2) |
| W8: G Drive Invoice Collector | `JNhSWvFLDNlzzsvm` | Inactive | Production folder monitoring |
| W9: Manual Downloads Scan | `hhY1QgHmOyUEYZyY` | Inactive | Manual downloads scan |

### Google Sheets
| Spreadsheet Name | ID | GID | Purpose |
|-----------------|-----|-----|---------|
| Expense-Database | `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` | - | Main database |
| Invoices tab | (same) | `1542914058` | Invoice records |
| Receipts tab | (same) | `1935486957` | Receipt records |
| Unknown tab | (same) | `284306066` | Unclassified documents |

### Google Drive Folders
| Folder Name | ID | Purpose |
|------------|-----|---------|
| Expenses-System Root | `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15` | System root |
| Downloads Folder | `1O3udIURR14LsEP3Wt4o1QnxzGsR2gciN` | W7 monitors this |
| Invoice Pool | `1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l` | Processed invoices |
| Receipt Pool (Gmail) | `1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4` | Gmail receipts |
| Receipt Pool (Hard Drive) | `1Qbqx9uiGiODsLE9TVEFG5NRysRJCFMnY` | Computer receipts |

### Sheet Column Names (Must Match Exactly)
**Receipts:** ReceiptID, FileName, Vendor, Amount, TransactionType, Date, FileID, DownloadDate, DownloadTimestamp, SourceEmail, Matched, Notes, transaction_id, ExpensifyNumber, ReportID, Currency, FilePath, ProcessedDate, Source, Direction

**Invoices:** InvoiceID, ClientName, Amount, Currency, Date, Project, FileID, FileName, ProcessedDate, Source, FilePath, Direction, DocumentType, DirectionReason

---

## Technical Architecture

### W7 Architecture (v3.0.2 - Working Without Duplicate Detection)
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
Route by Direction (INCOME?)
  +- TRUE (INCOME) -> Upload to Invoice Pool -> Log to Invoices
  +- FALSE -> Route EXPENSE vs UNKNOWN (EXPENSE?)
               +- TRUE (EXPENSE) -> Upload to Receipt Pool (Hard Drive) -> Log to Receipts
               +- FALSE (UNKNOWN) -> Upload to Unknown Pool -> Log to Unknown
```

**Node Count:** 33
**Duplicate Detection:** DISABLED (4 nodes disabled)

### Duplicate Detection Nodes (Currently Disabled)
```
Check Invoice IS There (id: 76f4877a-8507-4419-98a5-d4d655c60c1d) - DISABLED
Check Receipt IS There (id: e51416c3-f00e-4ad1-8d0e-b1994ee07743) - DISABLED
Skip if Exists (id: 11) - DISABLED
Skip if Exists Receipt (id: 16) - DISABLED
```

---

## Backup Files

### v3_foundation Backups
| File | Date | Description |
|------|------|-------------|
| W7_Downloads_Monitor_v3.0.2_2026-01-23.json | Jan 23, 2026 | Current state with all fixes |
| BUILD_PLAN.md | Jan 20, 2026 | v3 build specification |

### v2_foundation Backups
All 7 workflows backed up (Jan 20, 2026)

---

## Alternative Approaches for Duplicate Detection

**Options to Consider:**

1. **Code Node Approach**
   - Replace Google Sheets lookup with HTTP Request to Sheets API
   - More control over error handling
   - Can return empty array instead of erroring

2. **Different Trigger Point**
   - Check for duplicates at trigger level (before processing)
   - Use Google Drive file metadata instead of sheet lookup

3. **Post-Processing Cleanup**
   - Allow duplicates to be logged
   - Run separate cleanup workflow periodically
   - Simpler but less elegant

4. **Unique Constraint in Sheet**
   - Use Google Apps Script to reject duplicate FileIDs
   - Requires additional setup

5. **File Rename After Processing**
   - Rename processed files to include "PROCESSED_" prefix
   - Filter trigger to ignore files with that prefix

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
- Previous Summary: `compacting-summaries/summary_v10.3_2026-01-23.md`
- Workflow Backup: `N8N_Blueprints/v3_foundation/W7_Downloads_Monitor_v3.0.2_2026-01-23.json`

---

**Document Version:** v10.4
**Generated:** January 23, 2026 @ 22:15 CET
**Author:** Claude Code (Sway's automation assistant)
**Key Changes:** Binary bug fix, Direction routing, Hard Drive folder, ProcessedDate/Source/FileName fixes, Duplicate detection still failing - needs alternative approach
