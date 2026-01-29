# Expense System - Quick Start Guide

## ⚡ TL;DR

Your Expense System has 16 bank statements ready but not processed. W3 has 3 code errors. Here's how to fix it.

---

## 🎯 Goal

1. Get 500+ transactions from 16 PDFs into Transactions sheet
2. Fix W3 errors
3. Match transactions to receipts/invoices

---

## 🛠️ Quick Fix Path (45 minutes)

### Step 1: Fix W3 Errors (15 mins)

**File:** `expense-system-w3-fixes.md`

1. Open W3 workflow in n8n: `http://n8n.oloxa.ai/workflow/CJtdqMreZ17esJAW`
2. Find these 3 nodes:
   - "Match Invoices to Income Transactions"
   - "Prepare Transaction Updates"
   - "Find Unmatched Income Transactions"
3. For each node:
   - Open node
   - Replace entire code with fixed version from `w3-fixes.md`
   - Save
4. Save workflow
5. Validate (should show 0 errors now)

### Step 2: Process 16 PDFs (30 mins)

**SIMPLE METHOD - No new workflow needed:**

For each of these 16 files in Google Drive:
1. Move file OUT of "Bank & CC Statements" folder (to Desktop or any folder)
2. Wait 5 seconds
3. Move file BACK into "Bank & CC Statements" folder
4. W1 will detect the "fileUpdated" event and process it automatically

**Files (in order):**
- ING_OCT2025_Statement.pdf ⭐ START WITH THIS TO TEST
- Barclay_OCT2025_Statement.pdf
- DeutscheBank_OCT2025_Statement.pdf
- Miles&More_Oct2025_Statement.pdf
- (Then do Sep/Nov/Dec for each bank)

**Watch executions:** `http://n8n.oloxa.ai/executions`
- Each file takes ~30 seconds to process
- Check Transactions sheet after first file to verify working

### Step 3: Test W3 Matching (5 mins)

1. Open W3 workflow in n8n
2. Click "Test workflow" button (top right)
3. Wait for execution to complete
4. Check Receipts and Transactions sheets for matched items

---

## 📋 Alternative: Build Batch Processor

**File:** `expense-system-batch-processor-spec.md`

**If you prefer automated batch processing:**
1. Open workflow `y3A3JHocwVaOuMHT` in n8n
2. Follow spec to add remaining 8 nodes
3. Run once to process all 16 files
4. Deactivate workflow

**Time:** 30 mins setup + 5 mins execution

---

## ✅ Success Indicators

**After Step 2 (Process PDFs):**
- Transactions sheet has 500+ rows
- Statements sheet has 16 entries
- Bank & CC Statements folder is empty
- Archive folder has 16 PDFs

**After Step 3 (W3 Matching):**
- Receipts sheet shows transaction_id for matched items
- Transactions sheet shows ReceiptID and InvoiceID for matched items
- Execution shows matching report

---

## 📁 Reference Files

| File | Purpose |
|------|---------|
| `expense-system-build-summary.md` | Complete overview |
| `expense-system-w3-fixes.md` | Copy-paste code fixes |
| `expense-system-batch-processor-spec.md` | Alternative batch method |
| `expense-system-build-log.md` | Detailed analysis |

---

## 🆘 Troubleshooting

**W1 not processing after moving file?**
- Check workflow is Active
- Verify file moved BACK to correct folder ID: `1UYhIP6Nontc2vuE2G1aMvkggaEk6szv8`
- Wait 60 seconds (trigger polls every minute)

**W3 still shows errors after fixes?**
- Make sure you saved the workflow after editing nodes
- Check you replaced ENTIRE code block (not just part)
- Validate again: Should show warnings (OK) but 0 errors (required)

**Transactions not matching?**
- Make sure Transactions sheet has data first (Step 2)
- Check date formats match between transactions and receipts
- Review matching logic in W3 nodes

---

## 📞 Contact

Issues? Questions? Check detailed docs or reach out.

**Agent:** solution-builder-agent
**Date:** 2026-01-28

---

**Ready? Start with Step 1 (Fix W3). Then Step 2 (Process PDFs). Good luck! 🚀**
