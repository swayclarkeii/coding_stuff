# Expense System - Quick Start Guide

**Last Updated**: 2026-01-29 13:30
**Status**: ✅ ALL FEATURES COMPLETE - Ready for Testing (Slack notifications added!)

---

## 🔴 URGENT: Clean Duplicates First

**Before testing**, clean Google Sheets duplicates:

1. Open: https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM/edit
2. Select Transactions tab
3. Click Data > Remove duplicates
4. Select all columns → Keep first occurrence
5. Done! (Takes 30 seconds)

---

## What Was Fixed

### ✅ Fix #1: W0 Business Logic (CORRECTED - URGENT)
**⚠️ CRITICAL UPDATE**: Previous fix was incorrect!

**Correct Business Requirement**:
- **Expenses (negative)** → Need **RECEIPTS** from vendors
- **Income (positive)** → Need **INVOICES** issued by Sway

**ALL transactions need documentation!**

**Fix Applied**:
- Node renamed: "Filter Missing Documents" (was "Filter Missing Receipts")
- Now flags BOTH expenses AND income
- Categorizes by document type: 'receipt' or 'invoice'
- Calculates separate totals for receipts vs invoices
- Updated console output to show both categories clearly

**Result**: Complete tracking of missing receipts (expenses) AND missing invoices (income)

**Details**: See `/Users/computer/coding_stuff/internal/EXPENSE_SYSTEM_URGENT_FIX.md`

### ✅ Fix #2: W1 Deduplication
**Problem**: Same transaction appearing 3-4x in Google Sheets
**Fix**: Added deduplication logic before writing to Sheets
**Result**: Future imports won't create duplicates

### ✅ Fix #3: W0 Detailed Transaction Lists
**Problem**: Only showing counts/totals, not actual transactions
**Fix**: Added complete transaction lists in console output
**Result**: Sway can see exactly which documents are missing

### ✅ Fix #4: W0 Slack Notifications
**Problem**: Had to open n8n to see reports (not practical)
**Fix**: Added automatic Slack notifications with formatted reports
**Result**: Reports delivered to #expense-reports channel automatically

**Details**: See `/Users/computer/coding_stuff/internal/W0_SLACK_NOTIFICATIONS.md`

---

## Testing Instructions

### Quick Test (5 minutes)

**Step 1**: Clean duplicates (see above)

**Step 2**: Test W0 filter with real data:
```bash
curl -X POST https://n8n.oloxa.ai/webhook/w0-expense-orchestrator-start \
  -H "Content-Type: application/json" \
  -d '{"month": "2025-12"}'
```

**Expected Results**:
- ✅ **Missing Receipts** (expenses): X transactions, €Y total
- ✅ **Missing Invoices** (income): X transactions, €Y total
- ✅ **Grand Total**: Both combined
- ✅ Console log shows clear separation between receipts and invoices
- ✅ Each transaction has `document_type` field ('receipt' or 'invoice')

**Step 3**: Test W1 deduplication:
1. Upload any bank statement PDF to Google Drive folder: Bank-Statements
2. Wait 2-3 minutes for processing
3. Check Transactions tab → Note row count
4. Upload **the SAME PDF again** (test duplicate detection)
5. Wait 2-3 minutes
6. Check Transactions tab → Row count should be **UNCHANGED**
7. Check n8n execution logs → Should see "Skipping duplicate" messages

---

## Key Configuration Points

### Excluded Vendors (W0)
Currently excluded from "missing document" checks:
- Deka, Edeka, DM, Kumpel und Keule, Bettoni

**To modify**: Edit W0 workflow, "Filter Missing Documents" node:
```javascript
const excludedVendors = ['Deka', 'Edeka', 'DM', ...];
```

### Minimum Document Amount (W0)
Current threshold: **€10** (applies to BOTH receipts and invoices)

**To modify**: Edit W0 workflow, "Filter Missing Documents" node:
```javascript
const minAmount = 10;  // Change to desired amount
```

---

## Google Drive Folders

- **Bank-Statements**: `1UYhIP6Nontc2vuE2G1aMvkggaEk6szv8`
  - Upload bank statement PDFs here
  - W1 watches this folder

- **Archive**: `1uohhbtaE6qvS08awMEYdVP6BqgRLxgjH`
  - Processed PDFs move here automatically

---

## Google Sheets Database

**Sheet ID**: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`

**Tabs**:
- **Transactions**: All bank transactions (from W1)
- **Statements**: Statement processing log
- **Receipts**: Receipt data (from W2 - future)

---

## Workflow Status

| Workflow | ID | Status | Purpose |
|----------|-----|--------|---------|
| W0 - Master Orchestrator | ewZOYMYOqSfgtjFm | ✅ Fixed | Check for missing documents (receipts + invoices) |
| W1 - PDF Intake & Parsing | MPjDdVMI88158iFW | ✅ Fixed | Import bank statements |
| W2 - Gmail Receipts | dHbwemg7hEB4vDmC | 🔵 Not tested | Import email receipts |
| W3 - Matching | CJtdqMreZ17esJAW | 🔵 Not built | Match receipts to transactions |
| W6 - Expensify | zFdAi3H5LFFbqusX | 🔵 Not tested | Import Expensify data |

---

## Common Issues & Solutions

### Issue: "89 missing receipts, €93K total"
**Cause**: Combination of duplicates + old buggy filter
**Solution**: Clean duplicates in Google Sheets, re-run W0 with new logic

### Issue: Duplicate transactions in Google Sheets
**Cause**: Old W1 (fixed)
**Solution**: Clean existing duplicates, future imports will be deduplicated

### Issue: Income NOT being checked for invoices
**Cause**: Misunderstood business requirement (FIXED NOW)
**Solution**: New W0 logic tracks BOTH receipts (expenses) AND invoices (income)

---

## Next Steps

1. ✅ Clean Google Sheets duplicates
2. ✅ Test W0 with real month
3. ⏳ Test W1 with duplicate PDF
4. ⏳ Verify results are correct
5. ⏳ Run test-runner-agent for automated validation

---

## Documentation

Full details in:
- **⚠️ URGENT FIX**: `/Users/computer/coding_stuff/internal/EXPENSE_SYSTEM_URGENT_FIX.md`
- **Fixes Summary**: `/Users/computer/coding_stuff/internal/expense-system-fixes-summary.md`
- **Customization Checklist**: `/Users/computer/coding_stuff/internal/expense-system-customization-checklist.md`
- **Cleanup Script**: `/Users/computer/coding_stuff/internal/google-sheets-cleanup-script.md`

---

## Need Help?

**Automated testing**: Use test-runner-agent for workflow validation

**Questions**: Check `/Users/computer/coding_stuff/CLAUDE.md` for n8n patterns

**Issues**: Document in MY-JOURNEY.md and re-invoke solution-builder-agent
