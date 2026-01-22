# Sway's Expense System - Project State

**Last Updated:** January 4, 2026
**Status:** Testing & Validation Phase

---

## Current To-Do List

### ✅ Completed
- Complete Google Drive infrastructure (96+ folders created)
- Transaction Database with 4 sheets and proper schema
- Workflow 1: PDF Intake & Parsing rebuilt and migrated to OAuth2
- Workflow 2: Gmail Receipt Monitor rebuilt with 4 critical bug fixes
- Workflow 3: Transaction-Receipt Matching rebuilt (clean 9-node modular design)
- OAuth2 authentication configured for all Google Drive and Sheets nodes
- Anthropic API integration fixed (header + JSON body format)
- Folder IDs hardcoded in workflows (n8n free limitation workaround)
- System design documentation (850+ lines)
- VendorMappings populated with 12 vendor patterns

### ⏳ Pending
- **Workflow 1 Testing**: Upload test file to trigger execution and validate Anthropic API fix
- **Workflow 1 Database Validation**: Verify transaction records written to Google Sheets
- **Workflow 2 Activation**: Activate and test Gmail receipt monitoring (next scheduled: daily 6:00 AM CET)
- **Workflow 3 Testing**: End-to-end transaction-receipt matching validation
- **Workflow 4**: File organization automation (not built yet)
- **Multi-account Gmail support**: Add additional Gmail accounts for vendor receipt monitoring
- **Vendor discovery audit**: Identify all vendors beyond current 12 patterns

### 🔴 Blockers
None currently blocking progress.

### ⚠️ Known Issues
- **Workflow 1**: Playwright MCP server disconnected (prevents browser automation for file uploads)
- **Workflow 2**: 18 non-blocking warnings about error handling and outdated typeVersions
- **Workflow 2**: Minor code structure warning in "Load Vendor Patterns" node (doesn't prevent execution)
- **Service Account limitation**: Google Drive MCP uses Service Account (can't upload to personal drive)

---

## Key Decisions Made

### 1. Modular Architecture Over Mega Workflow (v1.3.1, January 2, 2026)
**Decision:** Split Workflow 3 into clean 9-node workflow instead of 26-node mega workflow combining W1+W2+W3
**Rationale:** Proper separation of concerns, easier debugging, independent workflow testing
**Impact:** Archived mega workflow (`oxHGYOrKHKXyGp4u`), created clean modular W3 (`waPA94G2GXawDlCa`)

### 2. OAuth2 Authentication Migration (v1.3.1, January 2-4, 2026)
**Decision:** Migrate all workflows from Service Account to OAuth2 authentication (swayclarkeii@gmail.com)
**Rationale:** Service Accounts can't access personal Gmail Drive folders; OAuth2 required for user-owned resources
**Impact:** All Google Drive and Google Sheets nodes now use OAuth2 credentials (ID: `a4m50EefR3DJoU0R`)

### 3. Hardcoded Folder IDs Instead of Environment Variables (v1.2.0, December 30, 2025)
**Decision:** Hardcode Google Drive folder IDs directly in workflow parameters
**Rationale:** n8n free tier doesn't support environment variables
**Impact:**
- Workflow 1 monitors: `1stmB5nWmoViQKKuQqpkWICPrfPQ_GDN1` (Bank-Statements)
- Workflow 1 archives: `1Z5VTiBW7RBEZaLXbsCdvWZrhj9SLmp3r` (Processed Statements - Test)
- Workflow 2 stores: `12SVQzuWtKva48LvdGbszg3UcKl7iy-1x` (Receipt Pool)

### 4. Anthropic API for PDF Parsing (v1.3.1, January 4, 2026)
**Decision:** Use Anthropic Messages API (Claude 3.5 Sonnet) instead of OpenAI Vision for PDF text extraction
**Rationale:** Better German language support, structured JSON responses, cost-effective
**Impact:** HTTP Request node configured with proper headers (anthropic-version: 2023-06-01) and JSON body format

---

## Important IDs / Paths / Workflow Names

### n8n Workflows
| Workflow Name | ID | Purpose |
|--------------|-----|---------|
| Workflow 1: PDF Intake & Parsing | `MPjDdVMI88158iFW` | Monitor bank statements, parse with Anthropic API, extract transactions |
| Workflow 2: Gmail Receipt Monitor | `dHbwemg7hEB4vDmC` | Daily Gmail search for receipts from 6 vendors, download attachments |
| Workflow 3: Transaction-Receipt Matching | `waPA94G2GXawDlCa` | Match transactions to receipts with confidence scoring |
| Workflow 3: ARCHIVED Mega Workflow | `oxHGYOrKHKXyGp4u` | DO NOT USE - Broken 26-node combined workflow |

### Google Sheets
| Spreadsheet Name | ID | Purpose |
|-----------------|-----|---------|
| Expense-Database | `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` | Master database with 4 sheets: Transactions, Statements, Receipts, VendorMappings |

### Google Drive
| Folder Name | ID | Purpose |
|------------|-----|---------|
| Expenses-System (Root) | `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15` | Main project folder with 96+ subfolders |
| Bank-Statements | `1stmB5nWmoViQKKuQqpkWICPrfPQ_GDN1` | W1 monitors for new PDFs |
| Processed Statements - Test | `1Z5VTiBW7RBEZaLXbsCdvWZrhj9SLmp3r` | W1 archives processed PDFs |
| Receipt Pool | `12SVQzuWtKva48LvdGbszg3UcKl7iy-1x` | W2 stores downloaded receipts |
| Bank Statements Inbox - Test | `1tC0fEVUl1vH0XUBi7915Hh5Wf5Cr3XKY` | Alternative test folder |

### Credentials
| Credential Name | ID | Type | Purpose |
|----------------|-----|------|---------|
| Google Drive account | `a4m50EefR3DJoU0R` | OAuth2 | All Google Drive operations |
| Google Sheets Service Account | `VdNWQlkZQ0BxcEK2` | Service Account | Google Sheets operations (being migrated to OAuth2) |
| Anthropic account | `MRSNO4UW3OEIA3tQ` | API Key | PDF parsing with Claude 3.5 Sonnet |

### File Paths
| File | Location | Purpose |
|------|----------|---------|
| System Design | `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md` | 850+ line complete specification |
| Version Log | `SwaysExpenseSystem/N8N_Blueprints/v1_foundation/VERSION_LOG.md` | Version history & rollback guide |
| README | `SwaysExpenseSystem/README.md` | Project overview & quick start |
| Test File | `/Users/swayclarke/coding_stuff/test-statement-v2.txt` | 211-byte mock bank statement for W1 testing |

---

## Technical Architecture

### Workflow 1: PDF Intake & Parsing (8 nodes)
```
Watch Bank Statements Folder (Google Drive Trigger)
  ↓ fileCreated event (polls every 1 minute)
Download PDF (Google Drive)
  ↓ Binary data
Extract File Metadata (Code)
  ↓ Parse filename: BANK_YYYY-MM_Statement.pdf
Parse PDF with Anthropic Vision (HTTP Request)
  ↓ Anthropic Messages API with base64 PDF
Parse Anthropic Response (Code)
  ↓ Extract transactions array
Write Transactions to Database (Google Sheets)
  ↓ Append to Transactions sheet
Log Statement Record (Google Sheets)
  ↓ Append to Statements sheet
Move PDF to Archive (Google Drive)
  ↓ Organize in Archive folder
```

**Current Status**: Active, OAuth2 configured, Anthropic API fixed (JSON body format), pending test execution

### Workflow 2: Gmail Receipt Monitor (9 nodes)
```
Daily Receipt Check (Schedule Trigger)
  ↓ Every 24 hours at 6:00 AM CET
Load Vendor Patterns (Code)
  ↓ 6 vendor email patterns
Search Gmail for Receipts (Gmail)
  ↓ operation: getAll with filters (last 7 days)
Get Email Details (Gmail)
  ↓ Full message metadata
Extract Attachment Info (Code)
  ↓ Parse PDF/image from email parts
Download Attachment (Gmail)
  ↓ operation: get with downloadAttachments: true
Upload to Receipt Pool (Google Drive)
  ↓ operation: upload to folder 12SVQzuWtKva48LvdGbszg3UcKl7iy-1x
Prepare Receipt Record (Code)
  ↓ Generate RCPT-{VENDOR}-{timestamp}
Log Receipt in Database (Google Sheets)
  ↓ Append to Receipts sheet
```

**Current Status**: Inactive, 4 critical bugs fixed (v1.2.3), next run: January 3, 2026 06:00 CET

**Vendors Monitored**:
1. OpenAI (from:noreply@openai.com)
2. Anthropic (from:billing@anthropic.com)
3. AWS (from:aws-billing@amazon.com)
4. Google Cloud (from:billing-noreply@google.com)
5. GitHub (from:billing@github.com)
6. Oura Ring (from:hello@ouraring.com)

### Workflow 3: Transaction-Receipt Matching (9 nodes, modular)
```
[Trigger TBD]
  ↓
Load Unmatched Transactions
  ↓
Load Available Receipts
  ↓
Match by Date Range (±3 days)
  ↓
Match by Amount (exact or ±€0.50)
  ↓
Match by Vendor Pattern (regex)
  ↓
Calculate Confidence Score (0.0-1.0)
  ↓
Update Transaction Records
  ↓
Move Matched Receipts to Organized Folders
```

**Current Status**: Built but untested, ready for integration testing

### Database Schema

**Transactions Sheet** (16 columns):
```
TransactionID | Date | Bank | Amount | Currency | Description | Vendor | Category |
ReceiptID | StatementID | MatchStatus | MatchConfidence | Notes | Tags | Type | AnnualInvoiceID
```

**Statements Sheet** (8 columns):
```
StatementID | Bank | Month | Year | FileID | FilePath | ProcessedDate | TransactionCount
```

**Receipts Sheet** (10 columns):
```
ReceiptID | Source | Vendor | Date | Amount | Currency | FileID | FilePath | ProcessedDate | Matched
```

**VendorMappings Sheet** (4 columns):
```
BankPattern | NormalizedVendor | Category | GmailSearch
```

---

## Current State Summary

**Version:** v1.2.3 (Workflow 2 Critical Fixes)
**Phase:** Testing & Validation
**Efficiency Score:** 4.8/10

### Recovery Context (December 31, 2025 Incident)
On December 31, 2025, all n8n workflows were erased without backup due to unknown causes. System completely rebuilt on January 2, 2026 from design documentation and blueprint JSONs.

**What Survived:**
- ✅ Google Drive Infrastructure (96+ folders)
- ✅ Transaction Database (all sheets intact)
- ✅ VendorMappings (12 patterns preserved)
- ✅ Design Documentation
- ✅ Blueprint Exports (v1.0-v1.2)

**What Was Lost:**
- ❌ Original n8n workflows (IDs changed)
- ❌ 70+ test execution records
- ❌ Workflow-specific configurations

### Efficiency Breakdown (v1.2.3)
| Category | Weight | Score | Points | Status |
|----------|--------|-------|--------|--------|
| Foundation | 20% | 10/10 | 2.0 | ✅ Complete |
| Core Automation | 50% | 4/10 | 2.0 | ⚠️ Built but untested |
| Data Setup | 10% | 8/10 | 0.8 | ✅ VendorMappings populated |
| Testing & Validation | 10% | 0/10 | 0.0 | ❌ Pending |
| Integration & Edge Cases | 10% | 0/10 | 0.0 | ❌ Not built |
| **Total** | 100% | - | **4.8** | In Progress |

### Financial Institutions Supported
1. **ING Bank** (Checking) - 12 monthly folders ready
2. **Deutsche Bank** (Checking) - 12 monthly folders ready
3. **Barclay** (Credit Card) - 12 monthly folders ready
4. **Miles & More** (Credit Card) - 12 monthly folders ready

---

## Next Steps

### Immediate (Current Session)
1. **Test Workflow 1 Execution** - Upload test file to trigger workflow and validate Anthropic API integration
2. **Verify Database Writes** - Check Transactions and Statements sheets for new records
3. **Validate File Archival** - Confirm test file moved to Archive folder

### Short-Term (Next 1-2 Days)
4. **Activate Workflow 2** - Enable Gmail receipt monitoring, wait for first scheduled run (6:00 AM CET)
5. **Test Workflow 2 Results** - Verify receipts downloaded to Receipt Pool and logged in database
6. **Configure Google Sheets OAuth2** - Migrate remaining Service Account nodes to OAuth2

### Medium-Term (Next Week)
7. **End-to-End Integration Test** - All 3 workflows working together with real data
8. **Workflow 4 Development** - Build file organization automation (receipt sorting from pool to monthly folders)
9. **Multi-Account Gmail Setup** - Add additional Gmail accounts for vendor receipt monitoring
10. **Vendor Discovery Audit** - Identify all vendors beyond current 12 patterns

### Long-Term (Next Month)
11. **Edge Case Handling** - Small expenses (<€10), annual invoices, GEMA reminders
12. **Expensify Integration** - API-based monthly export automation
13. **Reporting System** - Weekly digest and monthly summary generation
14. **Production Readiness** - Full system validation, documentation updates, v2.0.0 milestone

---

## References

- **VERSION_LOG:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/VERSION_LOG.md`
- **System Design:** `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md`
- **README:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/README.md`
- **Google Drive Root:** https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15
- **Transaction Database:** https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM/edit
- **n8n Instance:** https://n8n.oloxa.ai

---

**Document Version:** v1.0
**Generated:** January 4, 2026 at 11:17 CET
**Author:** Claude Code (Sway's automation assistant)
