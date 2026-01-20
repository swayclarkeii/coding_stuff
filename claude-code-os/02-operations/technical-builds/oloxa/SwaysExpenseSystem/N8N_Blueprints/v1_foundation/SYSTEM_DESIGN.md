# Expense Automation System - Design Document

## Executive Summary

This document describes an automated expense management system for Sway that will:
- Automatically match bank/credit card transactions to receipts
- Organize files into a structured Google Drive folder hierarchy
- Reduce monthly expense management from ~5-6 hours to ~25 minutes

---

## 1. System Overview

### 1.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EXPENSE AUTOMATION SYSTEM                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐        │
│  │  MANUAL INPUTS  │     │   AUTO INPUTS   │     │  EXPENSIFY      │        │
│  │                 │     │                 │     │                 │        │
│  │ Bank Statements │     │ Gmail Receipts  │     │ Monthly Export  │        │
│  │ (PDF upload)    │     │ (auto-monitor)  │     │ (manual upload) │        │
│  └────────┬────────┘     └────────┬────────┘     └────────┬────────┘        │
│           │                       │                       │                  │
│           └───────────────────────┼───────────────────────┘                  │
│                                   ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         n8n WORKFLOW SYSTEM                            │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  WORKFLOW 1: Statement Intake                                    │  │  │
│  │  │  • Watch _Inbox/ folder for new PDFs                            │  │  │
│  │  │  • Parse PDF to extract transactions                            │  │  │
│  │  │  • Store in Transaction Database (Google Sheet)                 │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  WORKFLOW 2: Gmail Receipt Monitor                              │  │  │
│  │  │  • Watch for emails from known vendors                          │  │  │
│  │  │  • Download PDF/image attachments                               │  │  │
│  │  │  • Store in Receipt Pool folder                                 │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  WORKFLOW 3: Transaction-Receipt Matching                       │  │  │
│  │  │  • For each unmatched transaction                               │  │  │
│  │  │  • Search Receipt Pool by vendor + amount + date                │  │  │
│  │  │  • Use AI for fuzzy matching                                    │  │  │
│  │  │  • Link matches in database                                     │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  WORKFLOW 4: File Organization                                  │  │  │
│  │  │  • Move matched receipts to correct month/bank folder           │  │  │
│  │  │  • Move statements to archive                                   │  │  │
│  │  │  • Move unmatched to review queue                               │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  WORKFLOW 5: Monthly Summary                                    │  │  │
│  │  │  • Generate expense summary spreadsheet                         │  │  │
│  │  │  • Send notification when processing complete                   │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                   │                                          │
│                                   ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         GOOGLE DRIVE                                   │  │
│  │  📁 Expenses-System/                                                   │  │
│  │     📁 _Inbox/          (upload zone)                                  │  │
│  │     📁 _Receipt-Pool/   (auto-collected receipts)                      │  │
│  │     📁 _Unmatched/      (review queue)                                 │  │
│  │     📁 2024/            (organized archives)                           │  │
│  │     📁 2025/                                                           │  │
│  │     📁 Income/          (invoices for income)                          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                    TRANSACTION DATABASE (Google Sheet)                 │  │
│  │  • All transactions from all statements                                │  │
│  │  • Match status (matched/unmatched/pending)                           │  │
│  │  • Links to receipt files                                             │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Banks & Cards

| Institution | Type | Folder Name |
|-------------|------|-------------|
| ING | Bank Account | `ING` |
| Deutsche Bank | Bank Account | `Deutsche-Bank` |
| Barclay | Credit Card | `Barclay` |
| Miles & More | Credit Card | `Miles-More` |

### 1.3 Key Assumptions

1. All bank statements are in PDF format
2. Gmail is the primary source for email receipts
3. Expensify exports will be manually uploaded monthly
4. German date format (DD.MM.YYYY) in bank statements
5. Amounts in EUR (€) with comma as decimal separator

---

## 2. Google Drive Folder Structure

### 2.1 Complete Folder Hierarchy

```
📁 Expenses-System/
│
├── 📁 _Inbox/                          # Upload zone (monitored)
│   ├── 📁 Bank-Statements/             # Drop bank PDFs here
│   ├── 📁 Credit-Card-Statements/      # Drop credit card PDFs here
│   └── 📁 Expensify-Exports/           # Drop Expensify exports here
│
├── 📁 _Receipt-Pool/                   # Auto-collected receipts (staging)
│   ├── 📁 Gmail/                       # Downloaded from email
│   └── 📁 Manual/                      # Manually added receipts
│
├── 📁 _Unmatched/                      # Review queue
│   ├── 📁 Transactions/                # Transactions without receipts
│   └── 📁 Receipts/                    # Receipts without transactions
│
├── 📁 _Archive/                        # Processed statements
│   └── 📁 Statements/
│       ├── 📁 ING/
│       ├── 📁 Deutsche-Bank/
│       ├── 📁 Barclay/
│       └── 📁 Miles-More/
│
├── 📁 2024/                            # Year folders
│   ├── 📁 01-January/
│   │   ├── 📁 ING/
│   │   │   ├── 📁 Statements/          # Bank statement PDF
│   │   │   └── 📁 Receipts/            # Matched expense receipts
│   │   ├── 📁 Deutsche-Bank/
│   │   │   ├── 📁 Statements/
│   │   │   └── 📁 Receipts/
│   │   ├── 📁 Barclay/
│   │   │   ├── 📁 Statements/
│   │   │   └── 📁 Receipts/
│   │   └── 📁 Miles-More/
│   │       ├── 📁 Statements/
│   │       └── 📁 Receipts/
│   ├── 📁 02-February/
│   │   └── ... (same structure)
│   └── ... (all 12 months)
│
├── 📁 2025/                            # Current year
│   └── ... (same structure as 2024)
│
├── 📁 Income/                          # Income tracking
│   ├── 📁 2024/
│   │   └── 📁 Invoices/                # Matched income invoices
│   └── 📁 2025/
│       └── 📁 Invoices/
│
├── 📁 _Reports/                        # Generated summaries
│   ├── 📁 2024/
│   └── 📁 2025/
│
└── 📄 Expense-Database.gsheet          # Transaction database
```

### 2.2 Folder Creation Strategy

**Initial Setup (One-time, during Phase 1):**
```
I will create the following structure using Google Drive MCP tools:

📁 Expenses-System/               ← Root folder (created first)
│
├── 📁 _Inbox/                    ← You upload statements here
│   ├── 📁 Bank-Statements/
│   ├── 📁 Credit-Card-Statements/
│   └── 📁 Expensify-Exports/
│
├── 📁 2025/                      ← Current year (all 12 months pre-created)
│   ├── 📁 01-January/
│   │   ├── 📁 ING/
│   │   │   ├── 📁 Statements/
│   │   │   └── 📁 Receipts/
│   │   ├── 📁 Deutsche-Bank/
│   │   │   ├── 📁 Statements/
│   │   │   └── 📁 Receipts/
│   │   ├── 📁 Barclay/
│   │   │   ├── 📁 Statements/
│   │   │   └── 📁 Receipts/
│   │   └── 📁 Miles-More/
│   │       ├── 📁 Statements/
│   │       └── 📁 Receipts/
│   ├── 📁 02-February/
│   │   └── ... (same structure)
│   └── ... (all 12 months)
│
└── (other folders: _Receipt-Pool, _Unmatched, Income, _Reports)
```

**Automatic Creation (Ongoing):**
- n8n Workflow 4 (File Organization) includes folder creation logic
- Before moving a file, it checks if the target folder exists
- If not, it creates the folder automatically
- Example: When January 2026 arrives, system creates `2026/01-January/` structure

**Local Access Option:**
- Install "Google Drive for Desktop" app
- Select `Expenses-System` folder to sync locally
- Changes sync in both directions automatically

### 2.3 Naming Conventions

**Statement Files:**
```
{BANK}_{YYYY-MM}_Statement.pdf
Example: ING_2025-01_Statement.pdf
```

**Receipt Files:**
```
{YYYY-MM-DD}_{VENDOR}_{AMOUNT}.pdf
Example: 2025-01-15_OpenAI_20.00.pdf
```

**Summary Reports:**
```
{YYYY-MM}_Monthly-Summary.xlsx
Example: 2025-01_Monthly-Summary.xlsx
```

---

## 3. Data Model

### 3.1 Transaction Database (Google Sheet)

**Sheet: Transactions**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `transaction_id` | String | Unique ID | `TXN-2025-01-001` |
| `date` | Date | Transaction date | `2025-01-15` |
| `bank` | String | Source bank/card | `Barclay` |
| `description` | String | Raw description | `PAYPAL *OPENAI` |
| `amount` | Number | Transaction amount | `-20.00` |
| `currency` | String | Currency code | `EUR` |
| `type` | Enum | income/expense | `expense` |
| `vendor_normalized` | String | Cleaned vendor | `OpenAI` |
| `category` | String | Expense category | `Software` |
| `match_status` | Enum | matched/unmatched/pending | `matched` |
| `receipt_file_id` | String | Google Drive file ID | `1abc...xyz` |
| `receipt_file_name` | String | Receipt filename | `2025-01-15_OpenAI_20.00.pdf` |
| `statement_id` | String | Source statement ID | `STM-2025-01-ING` |
| `processed_at` | DateTime | When processed | `2025-01-20 14:30:00` |
| `notes` | String | Manual notes | `Annual subscription` |

**Sheet: Statements**

| Column | Type | Description |
|--------|------|-------------|
| `statement_id` | String | Unique ID |
| `bank` | String | Bank/card name |
| `period_start` | Date | Statement start date |
| `period_end` | Date | Statement end date |
| `file_id` | String | Google Drive file ID |
| `transaction_count` | Number | Number of transactions |
| `processed_at` | DateTime | When processed |
| `status` | Enum | pending/processed/error |

**Sheet: Receipts**

| Column | Type | Description |
|--------|------|-------------|
| `receipt_id` | String | Unique ID |
| `source` | Enum | gmail/expensify/manual |
| `vendor` | String | Vendor name |
| `amount` | Number | Receipt amount |
| `date` | Date | Receipt date |
| `file_id` | String | Google Drive file ID |
| `file_name` | String | Filename |
| `matched` | Boolean | Is matched to transaction |
| `transaction_id` | String | Linked transaction ID |

**Sheet: VendorMappings**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `pattern` | String | Regex/text pattern | `PAYPAL.*OPENAI\|PP\*OPENAI` |
| `vendor_name` | String | Normalized name | `OpenAI` |
| `category` | String | Default category | `Software` |
| `receipt_source` | Enum | gmail/expensify/none | `gmail` |
| `gmail_search` | String | Gmail search query | `from:noreply@openai.com` |

---

## 4. n8n Workflow Specifications

### 4.1 Workflow 1: Statement Intake & Parsing

**Trigger:** Google Drive - Watch Folder (`_Inbox/Bank-Statements/` and `_Inbox/Credit-Card-Statements/`)

**Steps:**

```
1. TRIGGER: New file in _Inbox/Bank-Statements/ or Credit-Card-Statements/
   │
2. EXTRACT METADATA
   │ • Get filename
   │ • Determine bank from folder or filename
   │ • Parse date from filename
   │
3. DOWNLOAD PDF
   │ • Download file content
   │
4. PARSE PDF → TRANSACTIONS
   │ • Send to PDF parsing service (options below)
   │ • Extract table data
   │ • Parse each row into transaction
   │
5. NORMALIZE TRANSACTIONS
   │ • For each transaction:
   │   - Parse date (DD.MM.YYYY → YYYY-MM-DD)
   │   - Parse amount (1.234,56 → 1234.56)
   │   - Determine type (negative = expense, positive = income)
   │   - Match vendor using VendorMappings sheet
   │
6. STORE IN DATABASE
   │ • Add rows to Transactions sheet
   │ • Add row to Statements sheet
   │
7. MOVE STATEMENT
   │ • Move PDF to _Archive/Statements/{BANK}/
   │
8. TRIGGER MATCHING
   │ • Call Workflow 3 for new transactions
```

**PDF Parsing Options:**

| Service | Pros | Cons | Cost |
|---------|------|------|------|
| PDF.co | Good table extraction | API limits | ~$0.01/page |
| OpenAI Vision | Handles any format | Slower, more expensive | ~$0.02/page |
| Google Document AI | Best for structured PDFs | Setup complexity | ~$0.015/page |
| Textract (AWS) | Very accurate | AWS complexity | ~$0.015/page |

**Recommendation:** Start with OpenAI Vision for flexibility, optimize later if needed.

---

### 4.2 Workflow 2: Gmail Receipt Monitor

**Trigger:** Schedule - Every 15 minutes OR Gmail webhook

**Steps:**

```
1. TRIGGER: Every 15 minutes
   │
2. SEARCH GMAIL
   │ • For each vendor in VendorMappings where receipt_source = 'gmail':
   │   - Search: "{gmail_search} after:{last_check_date} has:attachment"
   │
3. FOR EACH EMAIL FOUND
   │
4. │ DOWNLOAD ATTACHMENTS
   │ │ • Download PDF/image attachments
   │ │
5. │ EXTRACT RECEIPT DATA
   │ │ • Parse vendor name from email
   │ │ • Parse amount from email body or filename
   │ │ • Parse date from email
   │ │
6. │ RENAME FILE
   │ │ • Rename to: {YYYY-MM-DD}_{VENDOR}_{AMOUNT}.pdf
   │ │
7. │ UPLOAD TO RECEIPT POOL
   │ │ • Upload to _Receipt-Pool/Gmail/
   │ │
8. │ ADD TO DATABASE
   │   • Add row to Receipts sheet
   │
9. UPDATE LAST CHECK TIME
   │
10. TRIGGER MATCHING
    • Call Workflow 3 for new receipts
```

**Known Vendor Gmail Patterns:**

| Vendor | Gmail Search Query | Attachment Type |
|--------|-------------------|-----------------|
| OpenAI | `from:noreply@openai.com` | PDF |
| AWS | `from:aws-billing@amazon.com` | PDF |
| Google Cloud | `from:billing-noreply@google.com` | PDF |
| Amazon | `from:auto-confirm@amazon.de` | - (no attachment) |
| Anthropic | `from:billing@anthropic.com` | PDF |
| GitHub | `from:billing@github.com` | PDF |
| Oura | `from:hello@ouraring.com subject:receipt` | PDF |

---

### 4.3 Workflow 3: Transaction-Receipt Matching

**Trigger:** Called by Workflow 1 or 2, OR scheduled daily

**Steps:**

```
1. TRIGGER: Called with new transactions OR receipts
   │
2. GET UNMATCHED TRANSACTIONS
   │ • Query Transactions sheet where match_status = 'unmatched'
   │
3. GET UNMATCHED RECEIPTS
   │ • Query Receipts sheet where matched = false
   │
4. FOR EACH UNMATCHED TRANSACTION
   │
5. │ SEARCH RECEIPTS
   │ │ • Search by:
   │ │   - Vendor name (exact or fuzzy)
   │ │   - Amount (exact match with tolerance ±0.01)
   │ │   - Date (within ±5 days)
   │ │
6. │ IF EXACT MATCH FOUND
   │ │ │
7. │ │ LINK TRANSACTION TO RECEIPT
   │ │ │ • Update Transactions.receipt_file_id
   │ │ │ • Update Transactions.match_status = 'matched'
   │ │ │ • Update Receipts.matched = true
   │ │ │ • Update Receipts.transaction_id
   │ │
8. │ ELSE IF FUZZY MATCH CANDIDATES
   │ │ │
9. │ │ SEND TO AI FOR VERIFICATION
   │ │ │ • Send transaction + candidates to OpenAI
   │ │ │ • Ask: "Is this a match?"
   │ │ │ • If yes → Link
   │ │ │ • If no → Continue searching
   │ │
10.│ ELSE (NO MATCH)
   │ │
11.│ │ SEARCH GMAIL DIRECTLY
   │   │ • Search Gmail for vendor + amount
   │   │ • If found → Download and add to pool
   │   │ • If not → Mark transaction as 'unmatched'
   │
12. REPORT RESULTS
    • Log match statistics
    • Flag problematic transactions
```

**Matching Algorithm:**

```javascript
function findMatch(transaction, receipts) {
  // Exact match
  const exactMatch = receipts.find(r =>
    r.vendor === transaction.vendor_normalized &&
    Math.abs(r.amount - Math.abs(transaction.amount)) < 0.02 &&
    daysBetween(r.date, transaction.date) <= 3
  );
  if (exactMatch) return { match: exactMatch, confidence: 1.0 };

  // Fuzzy match
  const fuzzyMatches = receipts.filter(r =>
    fuzzyVendorMatch(r.vendor, transaction.vendor_normalized) > 0.8 &&
    Math.abs(r.amount - Math.abs(transaction.amount)) < 0.02 &&
    daysBetween(r.date, transaction.date) <= 7
  );
  if (fuzzyMatches.length === 1) return { match: fuzzyMatches[0], confidence: 0.9 };
  if (fuzzyMatches.length > 1) return { candidates: fuzzyMatches, confidence: 0.7 };

  // Amount-only match (for common amounts like subscriptions)
  const amountMatches = receipts.filter(r =>
    Math.abs(r.amount - Math.abs(transaction.amount)) < 0.02 &&
    daysBetween(r.date, transaction.date) <= 5
  );
  if (amountMatches.length === 1) return { match: amountMatches[0], confidence: 0.6 };

  return null;
}
```

---

### 4.4 Workflow 4: File Organization

**Trigger:** Called after matching complete OR scheduled hourly

**Steps:**

```
1. TRIGGER: After Workflow 3 OR scheduled
   │
2. GET MATCHED TRANSACTIONS
   │ • Query where match_status = 'matched' AND receipt not yet filed
   │
3. FOR EACH MATCHED TRANSACTION
   │
4. │ DETERMINE DESTINATION
   │ │ • Year: from transaction.date
   │ │ • Month: from transaction.date
   │ │ • Bank: from transaction.bank
   │ │ • Path: /{YEAR}/{MM-MONTH}/{BANK}/Receipts/
   │ │
5. │ CREATE FOLDERS IF NEEDED
   │ │ • Check if path exists
   │ │ • Create missing folders
   │ │
6. │ MOVE RECEIPT FILE
   │ │ • Move from _Receipt-Pool/ to destination
   │ │
7. │ UPDATE DATABASE
   │   • Mark as filed
   │
8. MOVE STATEMENTS
   │ • For each processed statement in _Archive/
   │ • Move to correct /{YEAR}/{MM-MONTH}/{BANK}/Statements/
   │
9. HANDLE UNMATCHED
   │ • Move unmatched transactions list to _Unmatched/Transactions/
   │ • Create summary document
   │
10. NOTIFY COMPLETION
    • Send notification (email/Slack) with summary
```

---

### 4.5 Workflow 5: Monthly Summary

**Trigger:** Scheduled - 1st of each month, OR manual trigger

**Steps:**

```
1. TRIGGER: Monthly schedule or manual
   │
2. QUERY TRANSACTION DATA
   │ • Get all transactions for previous month
   │ • Group by category
   │ • Calculate totals
   │
3. GENERATE SUMMARY SPREADSHEET
   │ • Create new Google Sheet
   │ • Add sheets:
   │   - Overview (totals by category)
   │   - Income (all income transactions)
   │   - Expenses by Category
   │   - Expenses by Bank
   │   - Unmatched Transactions
   │
4. CREATE CHARTS
   │ • Pie chart: Expenses by category
   │ • Bar chart: Monthly trend
   │
5. SAVE TO REPORTS FOLDER
   │ • Save as: {YYYY-MM}_Monthly-Summary
   │ • Move to _Reports/{YEAR}/
   │
6. SEND NOTIFICATION
   │ • Email with summary stats
   │ • Link to full report
```

---

## 5. Vendor Mapping Database

Initial vendor mappings to configure:

| Bank Pattern | Normalized Vendor | Category | Gmail Search |
|--------------|------------------|----------|--------------|
| `PAYPAL.*OPENAI`, `PP\*OPENAI` | OpenAI | AI Services | `from:noreply@openai.com` |
| `ANTHROPIC` | Anthropic | AI Services | `from:billing@anthropic.com` |
| `AWS`, `AMAZON WEB SERVICE` | AWS | Cloud & Hosting | `from:aws-billing@amazon.com` |
| `GOOGLE.*CLOUD`, `GOOGLE\*SERVICES` | Google Cloud | Cloud & Hosting | `from:billing-noreply@google.com` |
| `GITHUB` | GitHub | Software & Subscriptions | `from:billing@github.com` |
| `AMAZON\.DE`, `AMZN` | Amazon | Shopping & Supplies | - |
| `EDEKA`, `EDEKA SCHECK` | Edeka | Food & Groceries | - (Expensify) |
| `DM.DROGERIE`, `DM-MARKT` | DM | Food & Groceries | - (Expensify) |
| `OURA` | Oura Ring | Health & Wellness | `from:hello@ouraring.com` |
| `VODAFONE`, `O2`, `TELEKOM` | Phone Bill | Communication & Phone | - |
| `MIETVERTRAG`, `MIETE` | Rent | Housing & Rent | - |

### 5.1 Expense Categories (Detailed)

| Category | Description | Examples |
|----------|-------------|----------|
| AI Services | AI and ML tools | OpenAI, Anthropic, Midjourney |
| Cloud & Hosting | Infrastructure | AWS, Google Cloud, Vercel |
| Software & Subscriptions | SaaS tools | GitHub, Notion, Slack, Zoom |
| Communication & Phone | Telecom | Phone bills, internet |
| Housing & Rent | Living/workspace | Rent, studio rent |
| Utilities | Basic services | Electricity, water, heating |
| Insurance | Coverage | Health, liability, equipment |
| Food & Groceries | Consumables | Edeka, DM, restaurants |
| Travel & Transport | Movement | Flights, trains, taxis, fuel |
| Health & Wellness | Self-care | Oura, gym, medical |
| Shopping & Supplies | General purchases | Amazon, office supplies |
| Education & Learning | Courses, books | Courses, conferences |
| Entertainment | Leisure | Streaming, events |
| Banking & Fees | Financial | Bank fees, currency conversion |
| Other | Uncategorized | Anything else |

---

## 6. Error Handling

### 6.1 Common Errors & Recovery

| Error | Detection | Recovery Action |
|-------|-----------|-----------------|
| PDF parsing failed | No transactions extracted | Move to _Inbox/Failed/, notify user |
| Duplicate statement | Statement ID already exists | Skip processing, notify user |
| Gmail API rate limit | 429 response | Exponential backoff, retry |
| Receipt download failed | Empty file or error | Retry 3x, then flag for manual |
| Multiple match candidates | Confidence < 0.8 | Move to _Unmatched/ for review |
| Folder creation failed | Drive API error | Retry, then notify user |

### 6.2 Notification Channels

- **Email:** Summary and errors
- **Slack (optional):** Real-time errors
- **Daily digest:** Unmatched items needing review

---

## 7. Manual Processes

### 7.1 Monthly Tasks (User)

| Task | Frequency | Time Estimate |
|------|-----------|---------------|
| Upload bank statements to `_Inbox/Bank-Statements/` | Monthly | 5 min |
| Upload credit card statements to `_Inbox/Credit-Card-Statements/` | Monthly | 3 min |
| Export Expensify and upload to `_Inbox/Expensify-Exports/` | Monthly | 2 min |
| Review `_Unmatched/` folder | Monthly | 10-15 min |
| Verify monthly summary | Monthly | 5 min |

**Total: ~25-30 minutes/month** (vs. 5-6 hours currently)

### 7.2 Quarterly Tasks

- Review and update vendor mappings
- Archive old years to separate folder
- Check for missed recurring expenses

---

## 8. Implementation Phases

### Phase 1: Foundation
- [ ] **Create Google Drive folder structure** (see Section 2)
  - Base folders: `Expenses-System/`, `_Inbox/`, `_Receipt-Pool/`, etc.
  - Year folders: `2025/` with all 12 months
  - Bank subfolders within each month: ING, Deutsche-Bank, Barclay, Miles-More
  - Each bank has: `Statements/` and `Receipts/` subfolders
- [ ] Create Transaction Database spreadsheet (Google Sheet)
- [ ] Create Vendor Mappings sheet
- [ ] Set up n8n with Google Drive & Gmail connections

**Note:** As of January 2025, ALL expense files will be stored in Google Drive. The n8n workflows automatically create any missing folders (e.g., new year `2026/` when needed). If local access is desired, use Google Drive for Desktop to sync the `Expenses-System` folder to your computer.

### Phase 2: Statement Processing
- [ ] Build Workflow 1 (Statement Intake)
- [ ] Configure PDF parsing service
- [ ] Test with 1-2 sample statements
- [ ] Refine parsing rules for German format

### Phase 3: Receipt Collection
- [ ] Build Workflow 2 (Gmail Monitor)
- [ ] Configure vendor Gmail patterns
- [ ] Test receipt extraction
- [ ] Handle Expensify exports

### Phase 4: Matching Engine
- [ ] Build Workflow 3 (Matching)
- [ ] Implement matching algorithm
- [ ] Configure AI-assisted matching
- [ ] Test with real data

### Phase 5: Organization & Reporting
- [ ] Build Workflow 4 (File Organization)
- [ ] Build Workflow 5 (Monthly Summary)
- [ ] Create summary templates
- [ ] Set up notifications

### Phase 6: Production
- [ ] Process backlog (2024 data)
- [ ] Monitor and refine
- [ ] Document edge cases
- [ ] Train system on missed patterns

---

## 9. Technical Requirements

### 9.1 Services & APIs

| Service | Purpose | Authentication |
|---------|---------|----------------|
| Google Drive | File storage & organization | OAuth 2.0 |
| Gmail | Receipt monitoring | OAuth 2.0 |
| Google Sheets | Transaction database | OAuth 2.0 |
| n8n | Workflow automation | Self-hosted or Cloud |
| OpenAI | PDF parsing, fuzzy matching | API Key |
| PDF.co (optional) | PDF parsing | API Key |

### 9.2 n8n Credentials Needed

1. Google OAuth (Drive, Sheets, Gmail)
2. OpenAI API key
3. PDF parsing service (if not using OpenAI)

### 9.3 Expected Costs

| Service | Usage | Monthly Cost |
|---------|-------|--------------|
| n8n Cloud | ~500 executions/month | ~$20/month |
| OpenAI | ~50 API calls/month | ~$2/month |
| Google Workspace | Existing | $0 |
| PDF.co (optional) | ~50 pages/month | ~$5/month |

**Total: ~$22-27/month** (or less with self-hosted n8n)

---

## 10. Edge Cases & Special Handling

### 10.1 Transaction Types & Rules

| Transaction Type | Detection | Handling | Receipt Required? |
|------------------|-----------|----------|-------------------|
| **Expense < €10** | amount < 10 | Auto-mark "Below threshold" | No - tracked but not flagged |
| **Expense ≥ €10** | amount >= 10 | Normal matching flow | Yes - alert if unmatched |
| **ATM Withdrawal** | Contains "GELDAUTOMAT", "ATM" | Auto-tag "Cash Withdrawal" | No |
| **Bank Fee** | Contains "GEBÜHR", "FEE", "ENTGELT" | Auto-tag "Bank Fee" | No |
| **Own-Account Transfer** | Matches your own account numbers | Auto-exclude from expenses | No |
| **Refund/Credit** | Positive amount in expense context | Link to original transaction | No (inherits from original) |
| **Foreign Currency** | Non-EUR indicator | Store original + EUR conversion | Yes |

### 10.2 Subscription & Annual Invoice Handling

**Problem:** Some subscriptions send one annual invoice but charge monthly.

**Solution:** "Annual Invoice Coverage" Feature

```
Database: AnnualInvoices
| vendor       | annual_amount | covers_months | invoice_file_id |
|--------------|---------------|---------------|-----------------|
| GitHub Pro   | €48.00        | Jan-Dec 2025  | abc123...       |
| Domain Reg   | €24.00        | Mar 2025-Feb 2026 | def456...   |

When matching:
1. Check if vendor has annual invoice covering this month
2. If yes → Link transaction to annual invoice
3. Mark as "Covered by annual invoice [filename]"
4. No alert needed
```

### 10.3 Portal Download Reminders (GEMA)

**Problem:** GEMA income doesn't send email; requires manual portal download.

**Solution:** Quarterly reminder system

```
Workflow: Portal Download Reminders
Trigger: 1st of each quarter month (Jan, Apr, Jul, Oct)

Action:
1. Send email: "GEMA Statement Reminder"
2. Include: Link to GEMA portal, folder to upload to
3. Track: Mark reminder sent in database

Expected uploads:
- Q1 (Jan-Mar) → Download in April
- Q2 (Apr-Jun) → Download in July
- Q3 (Jul-Sep) → Download in October
- Q4 (Oct-Dec) → Download in January
```

### 10.4 Notification System

**Weekly Digest (Every Monday)**
```
Subject: Expense System Weekly Summary

Unmatched Transactions (≥€10): 3 items
├── Jan 15: OpenAI - €20.00 (no receipt found)
├── Jan 18: Amazon - €45.99 (no receipt found)
└── Jan 20: Unknown Vendor - €12.50 (no receipt found)

Action needed: Find receipts or mark as "No receipt available"

Successfully matched this week: 12 items
Below threshold (no action): 5 items

[View full report in Drive]
```

**Immediate Alert (Within 1 hour)**
- Trigger: Unmatched transaction ≥ €100
- Email: "Large expense needs receipt: [VENDOR] €[AMOUNT]"

**Monthly Summary (1st of month)**
- Complete expense breakdown by category
- All unmatched items for previous month
- Reminder before VAT deadline

### 10.5 Small Expense Handling (< €10)

**Configuration:**
```
Settings:
  small_expense_threshold: 10.00  # EUR
  track_small_expenses: true      # Still record them
  match_small_expenses: false     # Don't try to find receipts
  include_in_reports: true        # Show in monthly summary
```

**Report Section:**
```
Unclaimed Small Expenses (<€10): €47.32
├── Coffee: €23.50 (8 transactions)
├── Parking: €12.00 (3 transactions)
└── Other: €11.82 (5 transactions)

Note: These are tracked but not claimed for VAT purposes.
```

---

## 11. Known Limitations

1. **Bank statements require manual download** - Banks don't offer APIs for individuals
2. **Amazon receipts** - Amazon doesn't email receipts; may need browser extension or manual
3. **Cash expenses** - Only Expensify captures these
4. **Grocery store variations** - EDEKA has many franchise names; may need ongoing mapping updates
5. **Multi-currency** - System designed for EUR; would need adjustment for other currencies
6. **Statement format changes** - Banks may change PDF formats; parsing rules may need updates

---

## 12. Success Criteria

The system is successful when:

1. ✅ 90%+ of recurring vendor transactions are auto-matched
2. ✅ Files are correctly organized within 24 hours of upload
3. ✅ Monthly time spent < 30 minutes
4. ✅ Unmatched queue is < 10 items per month
5. ✅ No receipts are lost or misfiled

---

## 13. Questions for Review

Before implementation, please confirm:

### Confirmed Decisions

| Question | Answer |
|----------|--------|
| Statement Format | Sway will provide sample for testing |
| Income Tracking | Mix of invoices and retainers |
| Categories | Detailed (15 categories - see section 5.1) |
| Notifications | Email |
| Historical Data | 2025 only (going forward, no backfill) |

### Current Folder Structure (Reference)

Sway's existing VAT folder structure (iCloud):
```
.../SCII/Invoices/VAT/
├── VAT 2019/
│   ├── VAT JAN - JUNE 2019/
│   ├── VAT JUL - SEP 2019/
│   └── VAT OCT - DEC 2019/
├── VAT 2020/
│   └── (quarterly folders)
├── VAT 2021/
│   └── (quarterly folders)
└── ...
```

**Note:** The new system on Google Drive will use a different structure (monthly rather than quarterly, organized by bank). This is intentional for better automation. Existing iCloud folders remain unchanged.

### Additional Edge Cases

**Approach:** Start building and discover edge cases during testing. The system will be designed to easily add new rules and mappings as we discover them.

---

## Appendix A: Sample Workflow JSON

*(Will be added during implementation)*

## Appendix B: Vendor Mapping Regex Patterns

*(Will be added during implementation)*

## Appendix C: PDF Parsing Prompts

*(Will be added during implementation)*
