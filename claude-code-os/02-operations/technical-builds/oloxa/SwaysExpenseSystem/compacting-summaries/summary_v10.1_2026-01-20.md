# Sway's Expense System - Summary

**Version:** v10.1
**Last Updated:** January 20, 2026
**Status:** Backup Complete - Duplicate Detection Implementation Pending

---

## Agent IDs (Resume Work)

**CRITICAL:** Use these agent IDs to resume work in new conversations.

### January 20, 2026 - Current Session (Backup & Prep)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| (main) | main | Created v10.1 summary, n8n workflow backups, v3 foundation plan | ✅ Complete |

### Historical Agent IDs (from CLAUDE.md)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| `a7e6ae4` | solution-builder-agent | W2 critical fixes (Google Sheets + Binary) | ✅ Complete |
| `a7fb5e5` | test-runner-agent | W2 fixes verification | ✅ Complete |
| `a6d0e12` | browser-ops-agent | Gmail OAuth refresh | ✅ Complete |
| `ac6cd25` | test-runner-agent | Gmail Account 1 verification | ✅ Complete |
| `a3b762f` | solution-builder-agent | W3 Merge connection fix attempt | ✅ Complete |
| `a729bd8` | solution-builder-agent | W3 connection syntax fix | ✅ Complete |
| `a8564ae` | browser-ops-agent | W3 execution and connection visual fix | ✅ Complete |
| `a017327` | browser-ops-agent | Google Sheets structure diagnosis | ✅ Complete |

### January 16, 2026 - W7 Architecture Reversion

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| `a277ff0` | solution-builder-agent | Reverted W7 to Google Drive Trigger | ✅ Complete |
| `a70720d` | solution-builder-agent | Verified W9 configuration | ✅ Complete |
| `a17efe2` | test-runner-agent | Checked W7/W9 status | ✅ Complete |

### January 13, 2026 - W7 Critical Fixes

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| `a46683b` | solution-builder-agent | Binary data preservation fix | ✅ Complete |
| `aa7000b` | solution-builder-agent | Google Sheets GID fix | ✅ Complete |
| `adb800e` | solution-builder-agent | Type mismatch bypass | ✅ Complete |

**Usage:** In new conversation: "Resume agent a7e6ae4" or reference this summary

---

## Current To-Do List

### ✅ Completed (This Session)
- [x] Create v10 compact summary of current expense system state
- [x] Archive older versions in the compact summary (v1-v8 moved to .archive/)
- [x] Backup latest n8n workflow JSONs (all 7 workflows backed up to v2_foundation)
- [x] Backup v2 foundations (complete - 7 JSONs in v2_foundation folder)
- [x] Create v3 foundations for next build (BUILD_PLAN.md created)

### ⏳ Pending
- [ ] Cleanup (remove 11 duplicate entries in Receipts sheet rows 12-22)
- [ ] Implement Option 1 duplicate detection in W7
- [ ] Test unknown file path with unrecognized filenames
- [ ] Add PDF handling for unknown path (PDF-to-image conversion)
- [ ] Test W3 (Transaction-Invoice Matching)
- [ ] Activate W8 (G Drive Invoice Collector)

### 🔴 Blockers
- Google Sheets MCP is timing out - OAuth refresh may be needed

### ⚠️ Known Issues
- **CRITICAL:** Skip if Exists nodes are placeholders (`true === true` → always passes)
- 11 duplicate OpenAI receipt entries in Receipts sheet (rows 12-22)
- Claude Vision only accepts JPEG, PNG, GIF, WEBP (not PDF)

---

## Key Decisions Made

### 1. Option 1 for Duplicate Detection (Jan 20, 2026)
**Decision:** Use pre-check via Google Sheets lookup before logging (not appendOrUpdate)
**Rationale:** More foolproof - explicit flow, fails loudly, independent of node behavior
**Impact:** Need to add 2 Google Sheets "Search Rows" nodes and update 2 IF conditions

### 2. Hybrid Classification for W7 (Jan 19, 2026)
**Decision:** Known filename patterns → fast path; Unknown patterns → Claude Vision
**Rationale:** Cost efficiency - no API calls for recognizable files
**Impact:** W7 now has 31 nodes (26 active, 5 disabled)

### 3. Google Sheets GID Configuration (Jan 13, 2026)
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
| W7: Downloads Monitor | `6x1sVuv4XKN0002B` | **Active** | Downloads folder monitor (hybrid) |
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
| v3 Build Plan | `SwaysExpenseSystem/N8N_Blueprints/v3_foundation/BUILD_PLAN.md` | Next build spec |
| Session Summary | `/session-summaries/2026-01-19-w7-hybrid-classification.md` | Jan 19 session |

---

## Technical Architecture

### W7 Architecture (Hybrid Classification)
```
Downloads Folder (1O3udIURR14LsEP3Wt4o1QnxzGsR2gciN)
  ↓
Google Drive Trigger (polls every 60 seconds)
  ↓
Filter Valid Files
  ↓
Categorize by Filename (Voxhaus, SC -, receipt patterns)
  ↓
Skip Unknown Files (IF node)
  ├─ TRUE (known pattern) → Download File → Claude API → Parse Results
  └─ FALSE (unknown) → Download Unknown File → Claude Vision → Parse Unknown
  ↓
Route by Direction (INCOME/EXPENSE/UNKNOWN)
  ↓
Route by Category (invoice vs receipt)
  ├─ Invoice → Skip if Exists → Upload to Invoice Pool → Log to Invoices Sheet
  └─ Receipt → Skip if Exists Receipt → Upload to Receipt Pool → Log to Receipts Sheet
```

**Node Count:** 31 (26 active, 5 disabled)

### Key Patterns
1. **Binary Data Preservation:** `data.binary = $input.item.binary` in Set nodes
2. **Switch Node Expression Mode:** Must evaluate to numeric index (0, 1, 2)
3. **IF Node Branch Connections:** `branch="true"` → main[0], `branch="false"` → main[1]
4. **Google Sheets GID:** Use numeric GID, not string name

---

## Current State Summary

**Version:** v2.2.0 (System) / v10.1 (Summary)
**Phase:** Duplicate Detection Implementation
**Key Metric:** 11 duplicate entries to clean up

**Recent Work:**
- All 7 workflows backed up to v2_foundation (Jan 20)
- v3 foundation BUILD_PLAN.md created (Jan 20)
- Hybrid classification operational (Jan 19)
- Duplicate issue diagnosed (Jan 19)

---

## Next Steps

1. **Fix Google Sheets MCP** - OAuth may need refresh (use browser-ops-agent)
2. **Clean up duplicates** - Remove 11 duplicate entries in Receipts sheet rows 12-22
3. **Implement Option 1** - Add Google Sheets lookup nodes + update IF conditions in W7
4. **Test duplicate prevention** - Drop existing file, verify it's skipped
5. **Test unknown path** - Drop unrecognized filename, verify Claude Vision classification

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
- Previous Summary: `compacting-summaries/summary_v10.0_2026-01-19.md`

---

**Document Version:** v10.1
**Generated:** January 20, 2026 @ 18:57 CET
**Author:** Claude Code (Sway's automation assistant)
**Key Changes:** All workflows backed up, v3 foundation created, Google Sheets MCP issue identified
