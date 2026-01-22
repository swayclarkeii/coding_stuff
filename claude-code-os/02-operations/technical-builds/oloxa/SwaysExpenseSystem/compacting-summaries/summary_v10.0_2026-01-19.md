# Sway's Expense System - Compact Summary

**Version:** v10.0
**System Version:** v2.2.0 (W7 Hybrid Classification + Duplicate Detection Pending)
**Last Updated:** January 19, 2026
**Status:** W7 Operational - Duplicate Detection Implementation Pending

---

## START HERE AFTER RESTART

**Quick Context:** W7 (Downloads Folder Monitor) now has hybrid classification working:
- Known filename patterns → Fast path (filename-based classification)
- Unknown filename patterns → Claude Vision API classification

**Critical Issue Found:** Skip if Exists nodes are **placeholders** (`true === true`). This causes duplicate entries in sheets. 11 duplicate OpenAI receipts found in Receipts sheet.

**Next Action:** Implement Option 1 duplicate detection (pre-check via Google Sheets lookup before logging).

---

## Active Workflows

| Workflow | ID | Status | Purpose |
|----------|-----|--------|---------|
| **W1** | `MPjDdVMI88158iFW` | Active | Bank PDF parsing |
| **W2** | `dHbwemg7hEB4vDmC` | Active | Gmail receipt/invoice monitoring |
| **W3** | `CJtdqMreZ17esJAW` | Inactive | Invoice-transaction matching |
| **W4** | `nASL6hxNQGrNBTV4` | Inactive | Monthly folder organization |
| **W6** | `l5fcp4Qnjn4Hzc8w` | Active | Expensify PDF processing |
| **W7** | `6x1sVuv4XKN0002B` | **Active** | Downloads folder monitor (hybrid classification) |
| **W8** | `JNhSWvFLDNlzzsvm` | Inactive | Production folder monitoring |
| **W9** | `hhY1QgHmOyUEYZyY` | Inactive | Manual downloads scan |

---

## W7 Architecture (v10.0 - Hybrid Classification)

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

---

## Critical IDs

### Google Sheets
| Sheet | Spreadsheet ID | GID |
|-------|---------------|-----|
| Expense-Database | `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` | - |
| Invoices | (same) | `1542914058` |
| Receipts | (same) | `1935486957` |
| Unknown | (same) | `284306066` |

### Google Drive Folders
| Folder | ID |
|--------|-----|
| Expenses-System Root | `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15` |
| Downloads Folder | `1O3udIURR14LsEP3Wt4o1QnxzGsR2gciN` |
| Invoice Pool | `1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l` |
| Receipt Pool | `1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4` |

### n8n Credentials
| Name | ID |
|------|-----|
| Google Drive account | `a4m50EefR3DJoU0R` |
| Google Sheets account | `H7ewI1sOrDYabelt` |
| Anthropic account | `MRSNO4UW3OEIA3tQ` |

---

## Known Issues

### CRITICAL: Duplicate Detection Not Working

**Problem:** Skip if Exists nodes are placeholders:
```javascript
leftValue: "={{ true }}"
rightValue: "={{ true }}"
// Always passes - no actual duplicate check
```

**Impact:** 11 duplicate OpenAI receipt entries in Receipts sheet (rows 12-22).

**Fix Planned:** Option 1 - Pre-check via Google Sheets lookup before logging:
1. Add Google Sheets "Search Rows" node before each Skip if Exists
2. Check if FileID already exists in target sheet
3. If exists → route to skip branch (don't log)
4. If not exists → continue to logging

### Claude Vision Limitations

**Accepted formats:** JPEG, PNG, GIF, WEBP
**NOT accepted:** PDF (requires conversion)

**Implication:** Unknown path works for images only. PDFs need separate handling.

---

## Recent Session Agent IDs

### January 19, 2026 - W7 Hybrid Classification

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| (session) | solution-builder-agent | Built hybrid classification path | Complete |
| (session) | main | Diagnosed duplicate issue | Complete |

### January 16, 2026 - W7 Architecture Reversion

| Agent ID | Type | Task |
|----------|------|------|
| `a277ff0` | solution-builder-agent | Reverted W7 to Google Drive Trigger |
| `a70720d` | solution-builder-agent | Verified W9 configuration |
| `a17efe2` | test-runner-agent | Checked W7/W9 status |

### January 13, 2026 - W7 Critical Fixes

| Agent ID | Type | Task |
|----------|------|------|
| `a46683b` | solution-builder-agent | Binary data preservation fix |
| `aa7000b` | solution-builder-agent | Google Sheets GID fix |
| `adb800e` | solution-builder-agent | Type mismatch bypass |

---

## Key Learnings (Patterns)

### 1. Google Sheets GID Configuration
- **Correct:** `sheetId: 1542914058` (numeric GID)
- **Wrong:** `sheetName: "Invoices"` (string name)

### 2. Binary Data Preservation
Pattern: `data.binary = $input.item.binary` in Set nodes during LLM processing.

### 3. Switch Node Expression Mode
Expression must evaluate to numeric index:
```javascript
={{ $json.extractedData.documentType === 'invoice' ? 0 : $json.extractedData.documentType === 'receipt' ? 1 : 2 }}
```

### 4. IF Node Branch Connections
- `branch="true"` → TRUE path (main[0])
- `branch="false"` → FALSE path (main[1])

---

## To-Do List

### Immediate
- [ ] Implement Option 1 duplicate detection in W7
- [ ] Clean up 11 duplicate entries in Receipts sheet (rows 12-21)
- [ ] Test unknown file path with unrecognized filenames

### After Duplicate Fix
- [ ] Add PDF handling for unknown path (PDF-to-image conversion)
- [ ] Test W3 (Transaction-Invoice Matching)
- [ ] Activate W8 (G Drive Invoice Collector)

---

## Archived Versions

Previous summaries archived in this folder:
- v9.1 (Jan 16) - W7 architecture reversion
- v9.0 (Jan 14) - W9 test harness
- v8.0 (Jan 13) - W7 critical fixes
- v7.0 (Jan 12) - W7/W8 build
- v6.0 (Jan 12) - Invoice collection system
- v5.0 (Jan 6) - W4 implementation
- v4.0 (Jan 5) - W3 matching
- v3.0 (Jan 5) - W2 enhancements
- v2.0 (Jan 4) - Initial summary format
- v1.0 (Jan 4) - Foundation

---

## Quick Links

- **n8n Instance:** https://n8n.oloxa.ai
- **W7 Workflow:** https://n8n.oloxa.ai/workflow/6x1sVuv4XKN0002B
- **Expense Database:** https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM
- **Google Drive Root:** https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15
- **VERSION_LOG:** `SwaysExpenseSystem/N8N_Blueprints/v1_foundation/VERSION_LOG.md`
- **Session Summary (Jan 19):** `/Users/swayclarke/coding_stuff/session-summaries/2026-01-19-w7-hybrid-classification.md`

---

**Document Version:** v10.0
**Generated:** January 19, 2026
**Key Change:** W7 hybrid classification operational, duplicate detection implementation pending
