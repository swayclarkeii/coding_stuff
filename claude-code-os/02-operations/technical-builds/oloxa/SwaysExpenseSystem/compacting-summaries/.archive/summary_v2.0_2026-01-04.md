# Sway's Expense System - Project State

**Last Updated:** January 4, 2026 16:30 CET
**Status:** Testing & Validation Phase - Ready for Agent-Driven Testing

---

## Current To-Do List

### ✅ Completed
- Complete Google Drive infrastructure (96+ folders created)
- Transaction Database with 4 sheets and proper schema
- Workflow 1: PDF Intake & Parsing rebuilt and migrated to OAuth2
- Workflow 2: Gmail Receipt Monitor rebuilt with 4 critical bug fixes (v1.2.3)
- Workflow 3: Transaction-Receipt Matching rebuilt (clean 9-node modular design)
- **Workflow 4: File Organization Blueprint created (v1.2.4)** - Ready for import
- OAuth2 authentication configured for all Google Drive and Sheets nodes
- Anthropic API integration fixed (header + JSON body format)
- Folder IDs hardcoded in workflows (n8n free limitation workaround)
- System design documentation (850+ lines)
- VendorMappings populated with 12 vendor patterns

### ⏳ Pending - Test Phase (Option 3: Test + Build Strategy)
- **Workflow 1 Testing**: test-runner-agent paused, awaiting decision on polling vs manual trigger
  - Agent ID: `a01364b` (ready to resume)
  - Options: (A) Upload test file, wait for 1-min polling, or (B) Manual trigger
- **Workflow 4 Import**: Import blueprint into n8n, test validation workflow
  - Blueprint file: `workflow4_file_organization_v1.2.4.json`
  - Currently only validates/reports, does NOT move files yet
- **Workflow 2 Manual Trigger**: Bypass 6 AM schedule, test immediately
  - No scheduling - all executions manual or immediate
- **Workflow 1 Real Bank Statement Test**: After test-statement-v2.txt validation passes
- **Workflow 3 Testing**: End-to-end transaction-receipt matching validation
- **Verify Database Writes**: Check Transactions, Statements, Receipts sheets for all workflow outputs

### 🚀 Future Enhancements (Not Blocking)
- **Workflow 4 v1.2.5**: Implement actual file moves (currently validation-only)
  - Add folder ID lookup (144 folders or dynamic search)
  - Add Google Drive "Move File" operation
  - Add Google Sheets "Update FilePath" operation
  - Estimated: 2-3 hours
- **Multi-account Gmail support**: Add additional Gmail accounts for vendor receipt monitoring
- **Vendor discovery audit**: Identify all vendors beyond current 12 patterns

### 🔴 Blockers
None currently blocking progress.

### ⚠️ Known Issues
- **Workflow 1**: Playwright MCP server disconnected (prevents browser automation for file uploads)
  - Workaround: Use Google Drive web UI or MCP tools for uploads
- **Workflow 2**: 18 non-blocking warnings about error handling and outdated typeVersions
- **Workflow 2**: Minor code structure warning in "Load Vendor Patterns" node (doesn't prevent execution)
- **Workflow 4**: Blueprint only - needs import into n8n to become operational
- **Workflow 4**: Does NOT move files yet - v1.2.4 is validation-only (summary report generation)

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

### 5. Workflow 4 as Blueprint (v1.2.4, January 4, 2026)
**Decision:** Build Workflow 4 as JSON blueprint instead of live workflow via n8n MCP
**Rationale:** n8n MCP `create_workflow` had persistent validation errors; blueprint = single import, more reliable
**Impact:** Workflow 4 ready for import but requires manual import step via n8n UI

### 6. Validation-Only Workflow 4 v1.2.4 (January 4, 2026)
**Decision:** v1.2.4 generates organization plan only, does NOT move files
**Rationale:** Validate matching/path logic before implementing 144+ folder ID lookups and file moves
**Impact:** Safer testing, confirms target paths are correct, v1.2.5 will add actual moves (2-3 hours)

### 7. No Scheduling - Manual/Immediate Execution Only (January 4, 2026)
**Decision:** Remove all scheduling triggers from workflows; everything runs manually or immediately
**Rationale:** Sway preference for manual control during testing phase; easier debugging without waiting for cron schedules
**Impact:**
- Workflow 1: Still polls Google Drive every 1 minute (Google Drive Trigger limitation)
- Workflow 2: Manual trigger instead of daily 6 AM schedule
- Workflow 4: Manual trigger only (not scheduled monthly)

### 8. Agent Delegation for Testing (January 4, 2026)
**Decision:** Use test-runner-agent and solution-builder-agent instead of direct MCP calls in main conversation
**Rationale:** Token efficiency (agents use 5-10x fewer tokens than Playwright/large MCP operations in main)
**Impact:** Cleaner context window, better delegation of complex multi-step tasks

---

## Important IDs / Paths / Workflow Names

### n8n Workflows
| Workflow Name | ID | Status | Version |
|--------------|-----|--------|---------|
| Workflow 1: PDF Intake & Parsing | `MPjDdVMI88158iFW` | ✅ Active - Ready for testing | v1.1.1 |
| Workflow 2: Gmail Receipt Monitor | `dHbwemg7hEB4vDmC` | ⚠️ Inactive - 4 bugs fixed, ready to activate | v1.2.3 |
| Workflow 3: Transaction-Receipt Matching | `waPA94G2GXawDlCa` | ✅ Built - Ready for testing | v1.3.2 |
| Workflow 3: ARCHIVED Mega Workflow | `oxHGYOrKHKXyGp4u` | ❌ DO NOT USE - Broken 26-node combined workflow | v1.3.1 ARCHIVED |
| Workflow 4: File Organization & Sorting | Blueprint Only | 📋 Blueprint ready for import | v1.2.4 |

### Google Sheets
| Spreadsheet Name | ID | Purpose |
|-----------------|-----|---------|
| Expense-Database | `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` | Master database with 4 sheets: Transactions, Statements, Receipts, VendorMappings |

### Google Drive
| Folder Name | ID | Purpose |
|------------|-----|---------|
| Expenses-System (Root) | `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15` | Main project folder with 96+ subfolders |
| Bank-Statements | `1stmB5nWmoViQKKuQqpkWICPrfPQ_GDN1` | W1 monitors for new PDFs (polling every 1 min) |
| Processed Statements - Test | `1Z5VTiBW7RBEZaLXbsCdvWZrhj9SLmp3r` | W1 archives processed PDFs |
| Receipt Pool | `12SVQzuWtKva48LvdGbszg3UcKl7iy-1x` | W2 stores downloaded receipts |
| Bank Statements Inbox - Test | `1tC0fEVUl1vH0XUBi7915Hh5Wf5Cr3XKY` | Alternative test folder |

### Credentials
| Credential Name | ID | Type | Purpose |
|----------------|-----|------|---------|
| Google Drive account | `a4m50EefR3DJoU0R` | OAuth2 | All Google Drive operations (swayclarkeii@gmail.com) |
| Google Sheets OAuth2 | `a4m50EefR3DJoU0R` | OAuth2 | Google Sheets operations (same as Drive) |
| Anthropic account | `MRSNO4UW3OEIA3tQ` | API Key | PDF parsing with Claude 3.5 Sonnet |

### File Paths
| File | Location | Purpose |
|------|----------|---------|
| System Design | `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md` | 850+ line complete specification |
| Version Log | `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/VERSION_LOG.md` | Complete version history & rollback guide |
| README | `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/README.md` | Project overview & quick start |
| Test File | `/Users/swayclarke/coding_stuff/test-statement-v2.txt` | 211-byte mock bank statement for W1 testing |
| Workflow 4 Blueprint | `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/workflow4_file_organization_v1.2.4.json` | Ready for import into n8n |
| W4 Implementation Guide | `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/workflows/workflow4_implementation_guide.md` | Import instructions and testing plan |

### Agent IDs (Active Session - January 4, 2026)
| Agent Type | ID | Status | Purpose |
|-----------|-----|--------|---------|
| test-runner-agent | `a01364b` | ⏸️ Paused - Awaiting decision | Test Workflow 1 with test file upload |
| solution-builder-agent | `ae617a2` | ✅ Complete | Built Workflow 4 blueprint v1.2.4 |

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

**Current Status**: Active, OAuth2 configured, Anthropic API fixed (JSON body format), ready for testing with test-runner-agent

### Workflow 2: Gmail Receipt Monitor (9 nodes)
```
Manual Trigger (was: Schedule Trigger - Daily 6 AM CET)
  ↓ User-initiated execution
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

**Current Status**: Inactive, 4 critical bugs fixed (v1.2.3), ready for manual trigger testing

**Vendors Monitored**:
1. OpenAI (from:noreply@openai.com)
2. Anthropic (from:billing@anthropic.com)
3. AWS (from:aws-billing@amazon.com)
4. Google Cloud (from:billing-noreply@google.com)
5. GitHub (from:billing@github.com)
6. Oura Ring (from:hello@ouraring.com)

### Workflow 3: Transaction-Receipt Matching (9 nodes, modular)
```
[Trigger TBD - Manual for testing]
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

**Current Status**: Built but untested, ready for integration testing after W1/W2 generate data

### Workflow 4: File Organization & Sorting (7 nodes, validation-only v1.2.4)
```
Manual Trigger
  ↓ User-initiated execution
Load Receipt Files (Google Drive)
  ↓ List all files in Receipt Pool (12SVQzuWtKva48LvdGbszg3UcKl7iy-1x)
Read Receipt Metadata (Google Sheets)
  ↓ Load Receipts sheet from Expense-Database
Merge Data Streams (Code)
  ↓ Combine Drive files and Sheet records
Match Files to Metadata (Code)
  ↓ Join by FileID, filter valid records
Determine Target Folder (Code)
  ↓ Calculate path: Receipts/{year}/{month}/{vendor}
Generate Summary Report (Code)
  ↓ Output organization plan with statistics
```

**Current Status**: Blueprint ready for import, does NOT move files yet (v1.2.5 feature)

**v1.2.4 Outputs**:
- Total files processed
- Ready to organize count
- Skipped files (missing metadata)
- Breakdown by vendor and month
- List of errors (missing Date/Vendor, unknown vendors)
- Detailed file report with calculated target paths

**v1.2.5 Will Add** (2-3 hours):
- Folder ID lookup (dynamic search recommended)
- Google Drive "Move File" operation
- Google Sheets "Update FilePath" operation

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

**Version:** v1.2.4 (Workflow 4 Blueprint)
**Phase:** Testing & Validation
**Efficiency Score:** 5.0/10

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

### Efficiency Breakdown (v1.2.4)
| Category | Weight | Score | Points | Status |
|----------|--------|-------|--------|--------|
| Foundation | 20% | 10/10 | 2.0 | ✅ Complete |
| Core Automation | 50% | 4/10 | 2.0 | ⚠️ Built but untested |
| Data Setup | 10% | 8/10 | 0.8 | ✅ VendorMappings populated |
| Testing & Validation | 10% | 0/10 | 0.0 | ❌ Pending (agents ready) |
| Integration & Edge Cases | 10% | 2/10 | 0.2 | ⚠️ W4 blueprint adds foundation |
| **Total** | 100% | - | **5.0** | In Progress |

**Projected Scores:**
- v1.2.5 (W4 with file moves): 6.0/10
- v1.3.0 (All workflows tested): 7.0/10

### Financial Institutions Supported
1. **ING Bank** (Checking) - 12 monthly folders ready
2. **Deutsche Bank** (Checking) - 12 monthly folders ready
3. **Barclay** (Credit Card) - 12 monthly folders ready
4. **Miles & More** (Credit Card) - 12 monthly folders ready

---

## Next Steps

### Immediate Actions (Current Session - January 4, 2026)

**Awaiting User Decision:**
1. **Workflow 1 Test Method** - Choose testing approach:
   - Option A: Upload test file, wait for 1-min polling (recommended, end-to-end)
   - Option B: Manually trigger workflow with test data (faster, bypasses polling)

2. **Agent Deployment Strategy** - Confirmed: Option 3 (Test + Build)
   - Resume test-runner-agent (ID: `a01364b`) for W1 testing
   - Import W4 blueprint and test validation workflow
   - Manually trigger W2 for immediate testing (no 6 AM wait)

### Short-Term (Next 1-2 Days)
3. **Complete W1 Testing** - Validate Anthropic API integration and database writes
4. **Test W2 Receipt Downloads** - Verify Gmail monitoring works without scheduling
5. **Import W4 Blueprint** - Import into n8n, run validation test, review summary report
6. **Verify Database Writes** - Check all 3 sheets (Transactions, Statements, Receipts) for test data

### Medium-Term (Next Week)
7. **Test W1 with Real Bank Statement** - After test-statement-v2.txt passes
8. **End-to-End Integration Test** - All 3 workflows working together with real data
9. **Build Workflow 4 v1.2.5** - Add actual file moving (2-3 hours with solution-builder-agent)
10. **Test W3 Transaction Matching** - After W1/W2 generate data to match

### Long-Term (Next Month)
11. **Edge Case Handling** - Small expenses (<€10), annual invoices, GEMA reminders
12. **Expensify Integration** - API-based monthly export automation
13. **Reporting System** - Weekly digest and monthly summary generation
14. **Production Readiness** - Full system validation, documentation updates, v2.0.0 milestone

---

## Testing Strategy (Option 3: Test + Build)

### Phase 1: Parallel Testing & Building (In Progress)
**Test-runner-agent (ID: a01364b)** - Test Workflow 1
- Upload test-statement-v2.txt to Bank-Statements folder
- Monitor workflow execution (polling trigger)
- Validate Anthropic API response
- Verify database writes (Transactions + Statements sheets)
- Confirm file archival

**Manual Task** - Import Workflow 4 Blueprint
- Import workflow4_file_organization_v1.2.4.json into n8n
- Execute manually to test validation logic
- Review summary report output
- Verify target path calculations

### Phase 2: Manual Trigger Testing
**Workflow 2 Manual Execution**
- Activate W2 in n8n
- Manually trigger (no 6 AM wait)
- Verify Gmail search returns results
- Check receipt downloads to Receipt Pool
- Validate Receipts sheet writes

### Phase 3: Integration Testing
**End-to-End Flow**
- W1 generates transactions from real bank statement
- W2 downloads receipts from Gmail
- W3 matches transactions to receipts
- W4 organizes matched receipts into monthly folders (v1.2.5)

---

## References

- **VERSION_LOG:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/VERSION_LOG.md`
- **System Design:** `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md`
- **README:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/README.md`
- **Google Drive Root:** https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15
- **Transaction Database:** https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM/edit
- **n8n Instance:** https://n8n.oloxa.ai

---

**Document Version:** v2.0
**Generated:** January 4, 2026 at 16:30 CET
**Author:** Claude Code (Sway's automation assistant)

**Changes from v1.0:**
- Added Workflow 4 blueprint completion (v1.2.4)
- Updated testing strategy to Option 3 (Test + Build)
- Added agent delegation decisions and active agent IDs
- Removed scheduling requirements (all manual/immediate now)
- Added validation-only status for W4 v1.2.4
- Updated efficiency score to 5.0/10
- Added detailed next steps with agent deployment strategy
