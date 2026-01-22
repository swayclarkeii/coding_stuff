# v3 Foundation - Build Plan

**Version:** v3.0.0 (Planned)
**Created:** January 20, 2026
**Previous Version:** v2.2.0 (Hybrid Classification)
**Status:** Planning

---

## Primary Objective: Duplicate Detection Fix

**Issue:** W7 Skip if Exists nodes are placeholders (`true === true` → always passes)

**Impact:** 11 duplicate OpenAI receipt entries found in Receipts sheet (rows 12-22)

**Solution:** Option 1 - Pre-check via Google Sheets lookup before logging

---

## Implementation Plan

### W7 Modifications Required

**Add 2 new nodes before each logging path:**

1. **Check Invoice Exists** (Google Sheets - Search Rows)
   - Position: Before "Log to Invoices Sheet"
   - Operation: Search rows where FileID matches current file
   - Sheet: Invoices (GID: 1542914058)

2. **Check Receipt Exists** (Google Sheets - Search Rows)
   - Position: Before "Log to Receipts Sheet"
   - Operation: Search rows where FileID matches current file
   - Sheet: Receipts (GID: 1935486957)

**Modify existing Skip if Exists nodes:**

3. **Skip if Exists** (IF node - Update condition)
   - Old: `true === true` (placeholder)
   - New: `={{ $('Check Invoice Exists').first().json.row_count === 0 }}`

4. **Skip if Exists Receipt** (IF node - Update condition)
   - Old: `true === true` (placeholder)
   - New: `={{ $('Check Receipt Exists').first().json.row_count === 0 }}`

---

## Workflow Architecture (v3 Target)

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
  ├─ Invoice → **Check Invoice Exists** → Skip if Exists → Upload to Invoice Pool → Log to Invoices Sheet
  └─ Receipt → **Check Receipt Exists** → Skip if Exists Receipt → Upload to Receipt Pool → Log to Receipts Sheet
```

---

## Critical IDs Reference

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
| Downloads Folder | `1O3udIURR14LsEP3Wt4o1QnxzGsR2gciN` |
| Invoice Pool | `1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l` |
| Receipt Pool | `1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4` |

### n8n Workflow
| Workflow | ID |
|----------|-----|
| W7 Downloads Monitor | `6x1sVuv4XKN0002B` |

### n8n Credentials
| Name | ID |
|------|-----|
| Google Drive account | `a4m50EefR3DJoU0R` |
| Google Sheets account | `H7ewI1sOrDYabelt` |
| Anthropic account | `MRSNO4UW3OEIA3tQ` |

---

## Pre-Implementation Checklist

- [ ] Clean up 11 duplicate entries in Receipts sheet (rows 12-22)
- [ ] Verify FileID column exists in both Invoices and Receipts sheets
- [ ] Back up current W7 JSON to v2_foundation (DONE)
- [ ] Implement duplicate detection nodes
- [ ] Test with known duplicate file
- [ ] Verify no duplicate entries created

---

## Testing Plan

1. **Test 1: New file (no duplicate)**
   - Drop new receipt in Downloads folder
   - Expected: File processed and logged normally

2. **Test 2: Existing file (duplicate)**
   - Drop file that already exists in Receipts sheet
   - Expected: File skipped, NOT logged again

3. **Test 3: Invoice path**
   - Drop Voxhaus invoice that already exists
   - Expected: File skipped, NOT logged again

---

## Rollback Plan

If v3 breaks, restore from v2_foundation:
- W7 backup: `W7_Downloads_Folder_Monitor_v2.2.0_2026-01-19.json`
- Use n8n MCP to import or manually restore nodes

---

**Version:** v3.0.0-PLAN
**Author:** Claude Code
**Date:** January 20, 2026
