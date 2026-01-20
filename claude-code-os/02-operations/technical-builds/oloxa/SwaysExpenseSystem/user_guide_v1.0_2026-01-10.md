# Expense System - User Guide

**Version**: 1.0
**Date**: 2026-01-10
**For**: Sway Clarke

---

## 📂 Google Drive Folder Structure Explained

### Your Current Setup

```
Expenses-System/
│
├── 📥 INBOX/
│   ├── Bank-Statements/
│   │   ├── ING/          ← Put ING bank statements here
│   │   └── Deutsche Bank/ ← Put Deutsche Bank statements here
│   ├── Credit-Card-Statements/
│   │   ├── Miles/        ← Put Miles credit card statements here
│   │   └── Barclays/     ← Put Barclays statements here
│   └── Expensify-Exports/ ← Put Expensify PDFs here
│
├── 📄 Expensify PDFs/    ← **TRIGGERS W6** (see below)
├── 📄 Invoices/          ← For income invoices (manual upload)
├── 📨 Receipt Pool/      ← **AUTO-FILLED BY W2** (Gmail receipts)
├── 📋 Unmatched/         ← **AUTO-FILLED BY W3** (unmatched items)
├── 🗄️ Archive/           ← **MANUAL USE** (old files you want to keep)
├── 💼 Transaction Database/ ← **DEPRECATED** (no longer used)
└── 🗂️ VAT 2025/          ← **AUTO-CREATED BY W4** (organized monthly folders)
    ├── VAT January 2025/
    ├── VAT February 2025/
    └── ...
```

---

## 🚀 How to Use Each Folder

### 1. INBOX Folders (Manual Upload + Manual Processing)

**Purpose**: Temporary storage - you manually organize from here

**What to do:**
1. **Upload your files to the appropriate INBOX subfolder:**
   - ING bank statements → `INBOX/Bank-Statements/ING/`
   - Deutsche Bank statements → `INBOX/Bank-Statements/Deutsche Bank/`
   - Miles credit card → `INBOX/Credit-Card-Statements/Miles/`
   - Barclays credit card → `INBOX/Credit-Card-Statements/Barclays/`
   - Expensify PDFs → `INBOX/Expensify-Exports/`

2. **Then YOU manually move them:**
   - Bank/credit statements → Move to **"Bank-Statements"** root folder to trigger W1
   - Expensify PDFs → Move to **"Expensify PDFs"** root folder to trigger W6

**Does dropping files here trigger workflows?**
- ❌ **NO** - INBOX is NOT watched by any workflows
- You must manually move files from INBOX to the trigger folders (see below)

**Why use INBOX?**
- Organized upload location (you know where to drop files by bank/card type)
- Gives you a chance to review before processing
- Keeps root folders clean

---

### 2. Bank-Statements Folder (W1 Trigger)

**Folder**: `Bank-Statements/` (root level, NOT in INBOX)
**Workflow**: W1 - Bank Statement Monitor
**Trigger**: ✅ **AUTOMATIC** (Google Drive trigger)

**What happens:**
1. You drop a PDF here (from INBOX or directly)
2. W1 triggers automatically (usually within 1-5 minutes)
3. Claude Sonnet 4.5 extracts transactions from PDF
4. Transactions logged to Google Sheets "Transactions" tab
5. Statement info logged to Google Sheets "Statements" tab

**What to upload:**
- Bank statements (ING, Deutsche Bank, etc.)
- Credit card statements (Miles, Barclays, etc.)
- Any PDF with transaction table

**File naming tip:**
- Use descriptive names: `ING_December_2025.pdf`
- System doesn't care about filename, but helps you track

---

### 3. Expensify PDFs Folder (W6 Trigger)

**Folder**: `Expensify PDFs/` (root level)
**Workflow**: W6 - Expensify PDF Parser v1.1
**Trigger**: ✅ **AUTOMATIC** (Google Drive trigger)

**What happens:**
1. You drop an Expensify export PDF here
2. W6 triggers automatically (within 1-5 minutes)
3. Claude Sonnet 4.5 extracts transaction table from PDF
4. Creates transaction rows in "Transactions" sheet
5. Creates receipt rows in "Receipts" sheet (with FilePath link)

**What to upload:**
- Expensify expense report PDFs only
- Should have transaction table with: Date, Merchant, Amount, Category

**Note about INBOX/Expensify-Exports:**
- This is just temporary storage
- You must manually move PDFs from `INBOX/Expensify-Exports/` to `Expensify PDFs/` root
- Only the root `Expensify PDFs/` folder triggers W6

---

### 4. Receipt Pool (AUTO-FILLED - Don't Touch)

**Folder**: `Receipt Pool/`
**Workflow**: W2 - Gmail Receipt Monitor (fills this automatically)
**Your Action**: ❌ **DO NOT manually add files here**

**What happens automatically:**
1. W2 runs daily (or on webhook trigger)
2. Scans your Gmail accounts for receipt emails
3. Downloads attachments
4. Uploads to Receipt Pool
5. Logs receipt info to Google Sheets "Receipts" tab

**When W4 runs:**
- Files in Receipt Pool get moved to monthly VAT folders
- Receipt Pool should be empty after W4 runs

**Apple Store receipts:**
- W2 detects Apple email receipts (HTML format)
- Converts to PDF automatically
- Uploads to Receipt Pool like other receipts

---

### 5. Invoices Folder (Manual Upload for Income)

**Folder**: `Invoices/`
**Workflow**: W3 - Transaction-Receipt-Invoice Matching (reads from here)
**Your Action**: ✅ **Manually upload income invoices here**

**What to do:**
1. When you receive an invoice for income (client payment, etc.)
2. Upload PDF to `Invoices/` folder
3. Add row to Google Sheets "Receipts" tab:
   - Store/Vendor: Client name
   - Amount: Invoice amount
   - ReceiptDate: Invoice date
   - FilePath: Link to invoice PDF in Drive
4. Add income transaction to "Transactions" tab:
   - Type: "income"
   - Amount: Same as invoice
   - Date: Payment date

**Then run W3 manually:**
- W3 will match the invoice to the income transaction
- Updates "Transactions" sheet with InvoiceID
- Updates "Receipts" sheet with TransactionID

**Example:**
- You invoice a client €5,000
- Upload invoice PDF to `Invoices/` folder
- Add to Sheets, run W3, invoice gets matched

---

### 6. Unmatched Folder (AUTO-FILLED)

**Folder**: `Unmatched/`
**Workflow**: W3 - Transaction-Receipt-Invoice Matching (writes here)
**Your Action**: ⚠️ **Review periodically, manually match**

**What happens automatically:**
1. W3 runs (manual trigger)
2. Tries to match receipts → expense transactions
3. Tries to match invoices → income transactions
4. Items with confidence < 0.7 go to "Unmatched" folder

**What you do:**
1. Open `Unmatched/` folder
2. Review unmatched receipts/invoices
3. Manually update Google Sheets to link them:
   - Add ReceiptID to Transaction row
   - Add TransactionID to Receipt row

**Why items don't match:**
- Date mismatch (receipt date ≠ transaction date by >7 days)
- Amount mismatch (different by >$5 or >10%)
- Vendor name too different

---

### 7. Archive Folder (Manual Storage)

**Folder**: `Archive/`
**Workflow**: None - manual use only
**Your Action**: ✅ **Use for old files you want to keep but not process**

**What to use it for:**
- Old statements from previous years
- Duplicate files
- Files you want to keep but not include in current VAT tracking
- Reference documents

**System doesn't touch this folder** - it's entirely for your own organization.

---

### 8. Transaction Database Folder (DEPRECATED)

**Folder**: `Transaction Database/`
**Status**: ❌ **NO LONGER USED**
**Your Action**: ❌ **Ignore this folder**

**Why it exists:**
- From older version of expense system
- Replaced by Google Sheets integration
- Can be deleted or kept for historical reference

**Current system uses:**
- Google Sheets for transaction/receipt database
- No longer writes to this folder

---

### 9. VAT 2025 Folder (AUTO-CREATED)

**Folder**: `VAT 2025/`
**Workflow**: W4 - Monthly Folder Builder & Organizer
**Trigger**: ⏰ **MANUAL** (webhook trigger)
**Your Action**: ⚠️ **Trigger W4 when you want to organize files**

**What happens when you trigger W4:**
1. W4 creates monthly folder structure (if doesn't exist):
   ```
   VAT [Month] 2025/
   ├── Receipts/
   └── Statements/
   ```

2. Moves files from Receipt Pool to appropriate monthly folder
3. Moves statement files based on date
4. Updates Google Sheets with new file paths

**Answering your questions:**

**Q: If I drop a November bank statement now, will it create "VAT November 2025"?**
- ❌ **NO** - Bank statements in `Bank-Statements/` trigger W1 (not W4)
- W1 extracts transactions but doesn't move files
- You must trigger W4 separately to create monthly folders

**Q: If I submit something for January, will it create "VAT January 2025"?**
- ✅ **YES** - If you trigger W4 with January data, it creates "VAT January 2025"
- W4 looks at dates in Google Sheets to determine which month

**Q: If I submit multiple items at once (credit cards + bank statements), will it process everything?**
- ✅ **YES** - W1 processes all PDFs in `Bank-Statements/` folder
- Each PDF triggers separately (usually processes within minutes of each other)
- All transactions get logged to Google Sheets

**Q: If I submit one bank statement today and another tomorrow, will it keep creating folders?**
- W1: Processes each statement, logs transactions (no folders created)
- W4: Checks if monthly folder exists before creating
  - If "VAT January 2025" exists → uses existing folder
  - If doesn't exist → creates new folder
  - **No duplicates created**

**How to trigger W4:**
- Method 1: In n8n, open W4 workflow, click "Test Workflow"
- Method 2: Use webhook URL (if you have one set up)
- Method 3: Ask me to trigger it for you

**When to trigger W4:**
- End of month (organize all receipts/statements from that month)
- Before VAT filing deadline
- Anytime you want to organize accumulated files

---

## 🔄 Complete Workflow Sequence

### Daily/Weekly (Automatic)

**W1: Bank Statement Monitor**
1. You: Drop bank/credit card PDF in `Bank-Statements/`
2. System: Auto-triggers W1 (within 1-5 min)
3. System: Extracts transactions → Google Sheets
4. Result: Transactions logged, PDF stays in folder

**W2: Gmail Receipt Monitor**
1. System: Runs daily at configured time
2. System: Scans Gmail for receipt emails
3. System: Downloads attachments → `Receipt Pool/`
4. System: OCR extracts amounts → Google Sheets
5. Result: Receipts in Receipt Pool, ready for W4

**W6: Expensify PDF Parser**
1. You: Drop Expensify PDF in `Expensify PDFs/`
2. System: Auto-triggers W6 (within 1-5 min)
3. System: Extracts transactions + receipts → Google Sheets
4. Result: Both transactions and receipt records created

### Monthly (Manual Trigger)

**W3: Transaction-Receipt-Invoice Matching**
1. You: Trigger W3 in n8n (or ask me)
2. System: Matches receipts → expenses, invoices → income
3. System: Updates Google Sheets with IDs
4. System: Moves unmatched items to `Unmatched/`
5. Result: Matched items linked, unmatched flagged

**W4: Monthly Folder Builder**
1. You: Trigger W4 in n8n (or ask me)
2. System: Creates "VAT [Month] 2025/" folder (if needed)
3. System: Moves files from Receipt Pool → monthly folder
4. System: Updates Google Sheets with new file paths
5. Result: Organized monthly structure, Sheets updated

---

## 📊 Google Sheets Structure

Your Google Sheet has these tabs:

### Transactions
**Columns:**
- TransactionID (UUID)
- Date
- Description
- Amount
- Type (expense / income)
- StatementID (links to Statements tab)
- ReceiptID (links to Receipts tab - for expenses)
- InvoiceID (links to Receipts tab - for income) ← NEW in v2.1
- Source (Bank / Expensify / Manual)
- ExpensifyNumber (optional - if from Expensify)
- ReportID (optional - if from Expensify)

### Receipts
**Columns:**
- ReceiptID (UUID)
- ReceiptDate
- Store/Vendor
- Amount
- FilePath (Google Drive link)
- Source (Gmail / Expensify / Manual)
- TransactionID (links back to Transactions tab)
- ExpensifyNumber (optional - if from Expensify)
- ReportID (optional - if from Expensify)

### Statements
**Columns:**
- StatementID (UUID)
- StatementDate
- FilePath (Google Drive link to PDF)
- UploadDate
- Bank/Institution

---

## ⚙️ Workflow Triggers Summary

| Workflow | Trigger Type | How to Trigger | Frequency |
|----------|-------------|----------------|-----------|
| **W1: Bank Statement Monitor** | Automatic (Drive) | Drop PDF in `Bank-Statements/` | Instant (1-5 min) |
| **W2: Gmail Receipt Monitor** | Scheduled | Runs automatically daily | Daily |
| **W3: Transaction Matching** | Manual | Click "Execute" in n8n | On demand |
| **W4: Monthly Folder Builder** | Manual (Webhook) | Trigger webhook or in n8n | Monthly recommended |
| **W6: Expensify PDF Parser** | Automatic (Drive) | Drop PDF in `Expensify PDFs/` | Instant (1-5 min) |

---

## 🎯 Common Use Cases

### Use Case 1: Process Bank Statement

**What you do:**
1. Download bank statement PDF from bank website
2. Optional: Upload to `INBOX/Bank-Statements/ING/` first (for organization)
3. Move or upload directly to `Bank-Statements/` folder

**What happens automatically:**
- W1 triggers within 1-5 minutes
- Extracts all transactions
- Logs to Google Sheets "Transactions" tab
- Logs statement info to "Statements" tab

**When to check:**
- Open Google Sheets after 5 minutes
- Verify transactions appear
- Check amounts match your statement

---

### Use Case 2: Process Expensify Report

**What you do:**
1. Export Expensify report as PDF
2. Optional: Upload to `INBOX/Expensify-Exports/` first
3. Move or upload directly to `Expensify PDFs/` folder

**What happens automatically:**
- W6 triggers within 1-5 minutes
- Extracts transaction table
- Creates transaction rows (with Source="Expensify")
- Creates receipt rows (with FilePath to PDF)

**When to check:**
- Open Google Sheets after 5 minutes
- Verify transactions + receipts created
- Check ReportID matches your Expensify export date

---

### Use Case 3: Match Receipts to Transactions

**What you do:**
1. Wait until you have several unmatched transactions + receipts
2. Trigger W3 manually in n8n
3. Or ask me: "Run W3 to match receipts"

**What happens:**
- W3 runs fuzzy matching logic
- Matches receipts → expenses (by date, amount, vendor)
- Matches invoices → income
- Updates ReceiptID / InvoiceID columns
- Moves unmatched items to `Unmatched/` folder

**When to check:**
- Open Google Sheets
- Look for ReceiptID / InvoiceID filled in
- Check `Unmatched/` folder for items that didn't match
- Manually link unmatched items if needed

---

### Use Case 4: Organize Monthly Files

**What you do:**
1. At end of month (or before VAT filing)
2. Trigger W4 manually in n8n
3. Or ask me: "Run W4 to organize December files"

**What happens:**
- W4 creates "VAT December 2025/" folder (if doesn't exist)
- Moves files from Receipt Pool → monthly folder
- Organizes into Receipts/ and Statements/ subfolders
- Updates FilePath in Google Sheets

**When to check:**
- Open `VAT 2025/` folder
- Verify monthly folder created
- Check files moved from Receipt Pool
- Open Google Sheets, verify FilePath updated

---

## 🚨 Common Mistakes to Avoid

❌ **Don't drop files directly in Receipt Pool**
- This folder is auto-filled by W2
- Manually added files may get overwritten or cause errors

❌ **Don't expect INBOX to trigger workflows**
- INBOX is manual staging area only
- You must move files to trigger folders (Bank-Statements, Expensify PDFs)

❌ **Don't delete "Unmatched" folder**
- W3 needs this to store unmatched items
- Review it periodically and manually match items

❌ **Don't use Transaction Database folder**
- Deprecated from old system
- Use Google Sheets instead

❌ **Don't forget to trigger W3 and W4 manually**
- W3 and W4 don't run automatically
- You must trigger them when ready

---

## 📞 When to Ask for Help

**Ask me to trigger workflows:**
- "Run W3 to match receipts"
- "Run W4 to organize December files"
- "Trigger monthly folder builder"

**Ask me to check status:**
- "Did W1 process my bank statement?"
- "Why didn't my Expensify PDF get processed?"
- "How many unmatched receipts do I have?"

**Ask me to fix issues:**
- "W1 didn't extract transactions correctly"
- "Receipt amounts are wrong in Google Sheets"
- "Monthly folder not created"

---

## 🎓 Tips for Success

1. **Use INBOX as staging area**
   - Upload files to INBOX first
   - Review/rename if needed
   - Then move to trigger folders

2. **Process statements regularly**
   - Don't wait until year-end
   - Process each month's statements as they arrive

3. **Run W3 weekly or bi-weekly**
   - More frequent matching = easier to track
   - Don't let unmatched items pile up

4. **Run W4 at month-end**
   - Creates clean monthly organization
   - Makes VAT filing easier

5. **Check Google Sheets regularly**
   - Verify transactions logged correctly
   - Spot errors early

6. **Review Unmatched folder monthly**
   - Manually link items that fuzzy matching missed
   - Update Google Sheets to connect them

---

**Version**: 1.0
**Last Updated**: 2026-01-10
**Questions?** Ask me anytime!
