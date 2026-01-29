# Expense System Customization Checklist

**Purpose**: This document lists all configuration points that need to be customized when deploying this expense tracking system for a new user (e.g., Gurvan, other clients).

---

## 1. Excluded Vendors/Categories

**Location**: W0 - Master Orchestrator, "Filter Missing Receipts" node

```javascript
const excludedVendors = ['Deka', 'Edeka', 'DM', 'Kumpel und Keule', 'Bettoni'];
```

**Customization Questions**:
- Which recurring vendors should be excluded from "missing receipt" checks?
- Examples:
  - Grocery stores (if personal expenses)
  - Rent payments (if monthly invoices handled separately)
  - Insurance providers (if annual invoices handled separately)
  - Specific vendors with guaranteed receipts

**When to ask**: During initial setup interview

**Default behavior**: No exclusions (flag all unmatched expenses)

---

## 2. Minimum Receipt Amount Threshold

**Location**: W0 - Master Orchestrator, "Filter Missing Receipts" node

```javascript
const minAmount = 10;  // €10 minimum
```

**Customization Questions**:
- What's the minimum transaction amount that requires a receipt?
- Legal requirements in their country/region?
- Company policy threshold?

**Common values**:
- Germany: €10-€50
- France: €10
- UK: £10
- US: $75 (IRS threshold)

**Default**: €10 (suitable for most EU countries)

---

## 3. Income vs Expense Classification

**Location**: W0 - Master Orchestrator, "Filter Missing Receipts" node

```javascript
// Only flag EXPENSE transactions (negative amounts)
if (amount >= 0) return false;  // Skip income (positive) and zero amounts
```

**Customization Questions**:
- How are positive/negative amounts represented in their bank statements?
  - Standard: Negative = expense, Positive = income ✅ (current implementation)
  - Reversed: Positive = expense, Negative = income ❌ (needs code change)
- Should income transactions EVER be flagged for receipts?
  - Usually NO
  - Exception: Reimbursements requiring proof

**Note**: Most bank statements use negative for debits (expenses). Verify with sample statement during setup.

---

## 4. Bank Statement Naming Conventions

**Location**: W1 - PDF Intake & Parsing, "Extract File Metadata" node

**Current supported formats**:
```
Format A: BankName_YYYY-MM_Statement.pdf
Example: ING_2025-11_Statement.pdf

Format B: BankName - MonthName YYYY.pdf
Example: Barclay - Sep 2025.pdf

Format C: BankName_MonthYYYY_Statement.pdf
Example: Miles&More_Nov2025_Statement.pdf
```

**Customization Questions**:
- What naming format do their banks use?
- Do they manually rename files or use bank's download format?
- Multiple banks = multiple formats?

**Action**: Add regex patterns for their specific formats if not covered

---

## 5. Bank Names and Identifiers

**Location**: W1 - PDF Intake & Parsing, "Extract File Metadata" node

```javascript
// Parses bank from filename prefix
const bankMatch = fileName.match(/^([A-Za-z&-]+)_/);
```

**Customization Questions**:
- List all banks they use (for filename validation)
- How do they abbreviate bank names?
  - "Deutsche Bank" → "DB" or "DeutscheBank"?
  - "Miles & More Credit Card" → "Miles&More" or "M&M"?

**Action**: Document their bank name conventions for file upload guidelines

---

## 6. Google Drive Folder Structure

**Location**: Multiple workflows reference specific folder IDs

**Current folder IDs** (Sway's setup):
- Bank-Statements: `1UYhIP6Nontc2vuE2G1aMvkggaEk6szv8`
- Archive: `1uohhbtaE6qvS08awMEYdVP6BqgRLxgjH`

**Customization Actions**:
1. Create folder structure in their Google Drive:
   ```
   Expense Tracking/
   ├── Bank-Statements/     (intake folder for PDFs)
   ├── Receipt-Pool/        (intake folder for receipts)
   ├── Archive/             (processed bank statements)
   └── Matched-Receipts/    (matched receipts from W3)
   ```

2. Update folder IDs in workflows:
   - W1: Watch Bank Statements Folder
   - W1: Move PDF to Archive
   - W2: Watch Receipt Pool Folder
   - W3: Move Receipt to Matched folder

---

## 7. Google Sheets Database

**Location**: All workflows reference Google Sheets ID

**Current sheet**: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`

**Customization Actions**:
1. Create new Google Sheet with exact column structure:
   - **Transactions** tab:
     - TransactionID, Date, Bank, Amount, Currency, Description
     - Vendor, Category, ReceiptID, StatementID
     - MatchStatus, MatchConfidence, Notes, Tags, Type, AnnualInvoiceID

   - **Statements** tab:
     - StatementID, Bank, Month, Year, FileID, FilePath, ProcessedDate, TransactionCount

   - **Receipts** tab:
     - ReceiptID, Date, Vendor, Amount, Currency, Description
     - FileID, FilePath, ProcessedDate, MatchedTransactionID, Tags, Notes

2. Share sheet with n8n service account (edit permissions)

3. Update sheet ID in ALL workflows:
   - W0: Read Transactions Sheet
   - W1: Write Transactions to Database
   - W1: Log Statement Record
   - W2: Write Receipts to Database
   - W3: Match transactions and receipts

---

## 8. Currency and Locale

**Current setup**: EUR (€), German locale

**Customization Questions**:
- Primary currency?
- Handle multi-currency transactions?
- Date format preference:
  - DD.MM.YYYY (German/EU)
  - MM/DD/YYYY (US)
  - YYYY-MM-DD (ISO)

**Action**: Update Anthropic parsing prompts if non-EUR currency

---

## 9. Tax Year vs Calendar Year

**Current setup**: Monthly processing, calendar year assumed

**Customization Questions**:
- Tax year = calendar year? (Jan-Dec)
- Or fiscal year? (e.g., Apr-Mar in UK)
- Processing frequency:
  - Monthly (current)
  - Quarterly
  - Annually (tax season)

**Action**: Adjust period parameters in W0 webhook if needed

---

## 10. Receipt File Types

**Location**: W2 - Gmail Receipt Intake

**Current supported**: PDF, PNG, JPEG attachments from Gmail

**Customization Questions**:
- Do they receive receipts via:
  - Email? (Gmail integration) ✅
  - Direct file uploads? (need manual Google Drive upload workflow)
  - Mobile app scans? (need mobile integration)
- Acceptable file formats?
  - PDF ✅
  - Images (PNG, JPEG, HEIC) ✅
  - Scanned documents
  - Excel exports (for bulk receipts)

---

## 11. OAuth and Credentials

**Required credentials**:
1. **Google Sheets OAuth2**
   - Scopes: `https://www.googleapis.com/auth/spreadsheets`
   - Access: Read + Write

2. **Google Drive OAuth2**
   - Scopes: `https://www.googleapis.com/auth/drive.file`
   - Access: Read + Write + Move files

3. **Gmail OAuth2** (if using W2)
   - Scopes: `https://www.googleapis.com/auth/gmail.readonly`
   - Access: Read emails and attachments

4. **Anthropic API Key**
   - For Claude Sonnet 4.5 (PDF parsing)
   - Estimate: €1-3 per bank statement PDF
   - Monthly cost: €10-50 depending on transaction volume

**Setup Actions**:
1. Create Google Cloud Project
2. Enable APIs (Sheets, Drive, Gmail)
3. Create OAuth credentials
4. Connect credentials in n8n
5. Test each credential with sample data

---

## 12. Error Handling Preferences

**Customization Questions**:
- Who gets notified on errors?
  - User email?
  - Accountant email?
  - No notifications (check manually)?

- What errors require immediate attention?
  - PDF parsing failures
  - Duplicate transaction detection
  - Google Sheets write errors
  - Missing folder IDs

- Error recovery preference:
  - Auto-retry (current: none)
  - Manual intervention
  - Skip and log

**Action**: Add error notification nodes if needed

---

## 13. Matching Algorithm Preferences

**Location**: W3 - Matching Engine (future workflow)

**Customization Questions**:
- Matching strictness:
  - Strict: Exact amount + date within 3 days
  - Moderate: Amount ±€1 + date within 7 days
  - Loose: Amount ±€5 + date within 14 days

- Multi-currency handling:
  - Convert all to base currency?
  - Match in original currency?

- Duplicate receipt handling:
  - Flag for manual review (safest)
  - Auto-keep highest resolution
  - Keep all copies

---

## 14. Accountant Handoff Format

**Customization Questions**:
- Preferred output format:
  - Google Sheets (current) ✅
  - Excel export
  - DATEV export (Germany)
  - QuickBooks import
  - CSV files

- Folder structure for accountant:
  - Organized by month?
  - Organized by vendor?
  - Organized by category?
  - Flat structure with naming convention?

- Naming conventions for matched receipts:
  - `YYYY-MM-DD_VendorName_Amount.pdf` (current)
  - `TransactionID_ReceiptID.pdf`
  - Custom format?

---

## Setup Questionnaire Template

Use this during onboarding call:

### Basic Information
1. Name:
2. Country/Tax Region:
3. Primary Currency:
4. Number of bank accounts:
5. Banks used:

### Processing Preferences
6. Processing frequency: [ ] Monthly [ ] Quarterly [ ] Annually
7. Tax year: [ ] Calendar (Jan-Dec) [ ] Fiscal (specify: ______)
8. Minimum receipt amount threshold: € ______

### Vendor Exclusions
9. List vendors to exclude from "missing receipt" checks:
   - _________________________ (reason: _______________)
   - _________________________ (reason: _______________)
   - _________________________ (reason: _______________)

### File Naming
10. How do you name bank statement files?
    Example filename: _________________________________

11. How do you name receipt files?
    Example filename: _________________________________

### Integration Details
12. Receipt sources:
    - [ ] Gmail (provide email: _______________)
    - [ ] Manual Google Drive upload
    - [ ] Other: _____________________

13. Accountant contact:
    - Name: _____________________
    - Email: _____________________
    - Preferred export format: _____________________

### Google Drive Setup
14. Google Drive folder structure created? [ ] Yes [ ] No
15. Google Sheets template created? [ ] Yes [ ] No
16. OAuth credentials connected? [ ] Yes [ ] No

---

## Post-Setup Verification

After customization, test with sample data:

1. ✅ Upload 1 sample bank statement PDF → Verify parsing
2. ✅ Upload 1 sample receipt PDF → Verify extraction
3. ✅ Run W0 with test data → Verify filtering logic
4. ✅ Check Google Sheets → Verify all data written correctly
5. ✅ Test duplicate detection → Upload same PDF twice
6. ✅ Verify excluded vendors are actually excluded
7. ✅ Verify income transactions are NOT flagged

**Estimated setup time**: 2-3 hours per new user

---

## Future Customization Points (Not Yet Implemented)

- W3: Matching confidence thresholds
- W4: Folder builder preferences
- W5: Accountant email templates
- Multi-user support (separate folders per client)
- Category auto-tagging rules
- Vendor normalization rules (e.g., "AMZN MKTP" → "Amazon")

---

**Last Updated**: 2026-01-29
**Version**: 1.0
**Author**: Claude Code (solution-builder-agent)
