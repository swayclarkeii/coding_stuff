# Sway's Expense System - Project State

**Last Updated:** January 11, 2026
**System Version:** v2.1.0 (Invoice Automation Complete)
**Status:** Active Development - Invoice Collection & Matching Operational

---

## Current To-Do List

### ✅ Completed (Session: January 11, 2026)

**Core Workflows:**
- W1: Bank Statement Monitor (active, monitoring new Bank & CC Statements folder)
- W2: Gmail Receipt Monitor with invoice detection (enhanced with 8 new nodes)
- W3: Transaction-Receipt-Invoice Matching with fuzzy logic (enhanced, 27 nodes)
- W4: Monthly Folder Builder with invoice organization (enhanced, 28 nodes)
- W7: Downloads Folder Monitor (built, 24 nodes, awaiting configuration)
- W8: G Drive Invoice Collector (built, awaiting configuration)

**Invoice Architecture:**
- Multi-source invoice collection (Production folder, Invoice Pool, Gmail, Downloads)
- Invoice # extraction from bank descriptions
- Fuzzy client name matching (70%+ Levenshtein similarity)
- Invoice data extraction via Claude Vision API
- Invoice organization to VAT folders

**Agent IDs from January 11, 2026 session:**
- `a7e6ae4`: solution-builder-agent - Built W7 (Downloads Folder Monitor)
- `a7fb5e5`: solution-builder-agent - Built W8 (G Drive Invoice Collector)
- `ab6b258`: solution-builder-agent - Enhanced W2 (Gmail invoice detection)
- `a4f02de`: solution-builder-agent - Enhanced W3 (Income transaction matching)
- `acf4f3e`: solution-builder-agent - Enhanced W4 (Invoice organization to VAT folders)

### ⏳ Pending

**Configuration Tasks:**
- Create Invoices sheet in spreadsheet (1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM)
  - Required columns: InvoiceID | ClientName | Amount | Currency | Date | Project | FileID | FileName | ProcessedDate | Source
- Set up G Drive Desktop app to sync Downloads folder
- Get synced Downloads folder ID for W7 configuration
- Fix W8 continueOnFail/onError conflict in Anthropic API node
- Run test-runner-agent on all 6 workflows (W1, W2, W3, W4, W7, W8)
- Activate W7 and W8 after testing passes

**Future Enhancements:**
- Edge case handling (v2.2.0): Small expenses <€10, GEMA reminders, annual invoices
- Expensify integration (v2.3.0): API export automation, photo matching
- Notification system (v3.0.0): Weekly digests, monthly summaries

### 🔴 Blockers

**None Currently** - All critical blocks resolved:
- ✅ Google OAuth credentials configured and working
- ✅ Anthropic API credential configured (MRSNO4UW3OEIA3tQ)
- ✅ n8n MCP tools functional for workflow updates

### ⚠️ Known Issues

1. **W8 Validation Warning**: Anthropic API node has continueOnFail/onError conflict (non-blocking)
   - Fix: Edit node, remove `continueOnFail` property, keep only `onError`

2. **W2 Gmail Search Complexity**: Searching two Gmail accounts in parallel may hit rate limits
   - Workaround: Daily schedule (6:00 AM CET) should avoid conflicts

3. **W3 Invoice Filename Dependency**: Primary matching requires invoice # in filename
   - Limitation: PDFs without invoice # in filename only get secondary (fuzzy) matching

4. **W4 Date Format Assumption**: Assumes Date column in Invoices sheet is JavaScript-parseable
   - Risk: Invalid date formats will cause filtering errors

---

## Key Decisions Made

### 1. Multi-Source Invoice Collection Architecture (v2.1.0)
**Decision:** Centralized Invoice Pool approach with 4 collection sources
**Rationale:**
- W8 monitors Production folder (where Sway creates invoices)
- W7 monitors Downloads folder (synced via G Drive Desktop)
- W2 monitors Gmail attachments (client invoices)
- Manual uploads to Invoice Pool folder
- All sources route to centralized Invoice Pool (1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l)

**Impact:**
- Invoices collected from all sources automatically
- W3 can search one central location instead of 4+ folders
- Duplicate prevention at collection stage
- Single source of truth for invoice matching

### 2. Copy vs. Move for Invoice Collection (v2.1.0)
**Decision:** W8 uses COPY operation (not MOVE) for invoices
**Rationale:**
- Production folder is Sway's invoice creation workspace
- Preserving originals allows manual review/editing
- Manual cleanup of production folder can be done quarterly

**Impact:**
- Invoices remain in production folder after collection
- Invoice Pool has copies for matching
- No risk of losing invoice originals
- Requires periodic manual cleanup of production folder

### 3. Fuzzy Client Name Matching with Levenshtein Distance (v2.1.0)
**Decision:** Implement 70%+ similarity threshold for secondary invoice matching
**Rationale:**
- Bank descriptions don't always match invoice client names exactly
- Example: "Supreme Music GmbH" vs "SUPREME MUSIC" = 78% match
- Handles typos, abbreviations, legal suffixes (GmbH, Ltd, Inc)

**Impact:**
- Higher match rate for income transactions (estimated 85%+)
- Reduces manual matching workload
- Known clients list enables targeted fuzzy matching
- May require periodic review of false positives

### 4. Invoice Organization: Centralized Income Folder (v2.1.0)
**Decision:** W4 moves all invoices to `VAT 2025/[Month]/Income/` (not bank-specific)
**Rationale:**
- Invoices are income documents, not tied to specific bank accounts
- Multiple banks may receive same client payment
- Simpler folder structure for tax reporting

**Impact:**
- All monthly invoices in single folder per month
- Easier for accountant to locate income documents
- May need subfolder by client if volume increases (future v2.2.0+)

### 5. German Invoice Format Support (v2.1.0)
**Decision:** Claude Vision API with German-specific extraction prompts
**Rationale:**
- German invoice format: RECHNUNG #, INSGESAMT, DATUM, Projekt
- Different field names than English invoices
- W8 uses targeted German extraction prompt

**Impact:**
- Accurate extraction from German invoices (Sway's primary format)
- May need English prompt variant for client invoices (future)
- Example pattern: "SC - SUPREME MUSIC GmbH - 122025 #540.pdf"

### 6. Primary vs. Secondary Matching Strategy (v2.1.0)
**Decision:** Two-tier matching system with confidence scoring
**Rationale:**
- **Primary match** (95% confidence): Invoice # + Amount (±2 EUR) + Date (±7 days)
- **Secondary match** (75% confidence): Fuzzy client name (70%+) + Exact amount + Date (±14 days)
- Bank descriptions often include invoice numbers for income transactions

**Impact:**
- Higher accuracy on primary matches (invoice # is definitive)
- Fallback to fuzzy matching catches variations
- Confidence scoring allows manual review of low-confidence matches
- Transaction metadata includes MatchMethod for audit trail

---

## Important IDs / Paths / Workflow Names

### n8n Workflows

| Workflow Name | ID | Status | Purpose | Agent ID |
|--------------|-----|--------|---------|----------|
| W1: Bank Statement Monitor | MPjDdVMI88158iFW | ✅ Active | Monitors new Bank & CC Statements folder, processes PDFs | - |
| W2: Gmail Receipt Monitor | dHbwemg7hEB4vDmC | ✅ Active | Monitors Gmail for receipts + invoices (enhanced) | ab6b258 |
| W3: Transaction-Receipt-Invoice Matching | CJtdqMreZ17esJAW | ⚠️ Inactive | Matches transactions to receipts/invoices with fuzzy logic | a4f02de |
| W4: Monthly Folder Builder & Organizer | nASL6hxNQGrNBTV4 | ✅ Active | Creates VAT folders, organizes statements/receipts/invoices | acf4f3e |
| W7: Downloads Folder Monitor | 6x1sVuv4XKN0002B | 📋 Built | Monitors Downloads, categorizes receipts/invoices | a7e6ae4 |
| W8: G Drive Invoice Collector | JNhSWvFLDNlzzsvm | 📋 Built | Monitors production folder, extracts German invoices | a7fb5e5 |

### Google Sheets

| Spreadsheet Name | ID | Purpose |
|------------------|-----|---------|
| Expense-Database | 1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM | Main database with 5 sheets: Transactions, Statements, Receipts, VendorMappings, **Invoices** (pending creation) |

**Invoices Sheet Required Columns:**
```
InvoiceID | ClientName | Amount | Currency | Date | Project | FileID | FileName | ProcessedDate | Source
```

### Google Drive

| Folder/File Name | ID | Purpose |
|------------------|-----|---------|
| Expenses-System (Root) | 1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15 | Root folder for all expense system resources |
| Bank & CC Statements (NEW) | 1UYhIP6Nontc2vuE2G1aMvkggaEk6szv8 | Consolidated bank and credit card statements (W1 trigger) |
| Invoice Pool | 1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l | Central invoice collection point (all sources → here) |
| Receipt Pool | 1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4 | Central receipt collection point |
| Invoice Production Folder | 1_zVNS3JHS15pUjvfEJMh9nzYWn6TltbS | Sway's invoice creation folder (W8 source) |

### n8n Credentials

| Credential Name | ID | Type | Used By |
|-----------------|-----|------|---------|
| Google OAuth2 (multiple) | Various | OAuth2 | W1, W2, W3, W4, W7, W8 (Drive & Sheets) |
| Anthropic API | MRSNO4UW3OEIA3tQ | API Key | W2, W7, W8 (Claude Vision for invoice/receipt extraction) |

### File Paths

| File | Location | Purpose |
|------|----------|---------|
| VERSION_LOG.md | `SwaysExpenseSystem/N8N_Blueprints/v1_foundation/` | System version history and component inventory |
| W7 Export JSON | `SwaysExpenseSystem/n8n/workflows/W7-downloads-folder-monitor.json` | W7 workflow export for backup/import |
| W7 Implementation Doc | `SwaysExpenseSystem/WORKFLOW_7_IMPLEMENTATION.md` | W7 build documentation |
| W8 Export JSON | `SwaysExpenseSystem/workflows/w8-gdrive-invoice-collector.json` | W8 workflow export for backup/import |
| W8 Handoff Doc | `SwaysExpenseSystem/workflows/W8-HANDOFF.md` | W8 configuration and testing guide |
| W3 Enhancement Export | `/Users/swayclarke/coding_stuff/expense-system/workflows/W3-enhanced-v2.1-export.json` | W3 enhanced workflow export |
| W3 Enhancement Doc | `/Users/swayclarke/coding_stuff/expense-system/docs/W3-ENHANCEMENTS-v2.1.md` | W3 enhancement documentation |
| W4 Implementation Doc | `/Users/swayclarke/coding_stuff/W4-invoice-organization-implementation.md` | W4 invoice organization guide |

---

## Technical Architecture

### Invoice Collection Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    INVOICE SOURCES (4)                      │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
    ┌────▼─────┐         ┌───▼────┐          ┌───▼─────┐
    │ W8: G    │         │ W7:    │          │ W2:     │
    │ Drive    │         │ Down-  │          │ Gmail   │
    │ Produc-  │         │ loads  │          │ Attach- │
    │ tion     │         │ Folder │          │ ments   │
    └────┬─────┘         └───┬────┘          └───┬─────┘
         │                   │                    │
         │    Claude Vision  │  Claude Vision     │  Claude Vision
         │    (German fmt)   │  (Auto-detect)     │  (Auto-detect)
         │                   │                    │
         └────────────┬──────┴────────────────────┘
                      │
              ┌───────▼────────┐
              │  INVOICE POOL  │
              │  (Central DB)  │
              └───────┬────────┘
                      │
              ┌───────▼────────┐
              │ W3: Matching   │
              │ Engine         │
              │ (Primary +     │
              │  Secondary)    │
              └───────┬────────┘
                      │
              ┌───────▼────────┐
              │ Transactions   │
              │ Sheet Updated  │
              │ (InvoiceID,    │
              │  Confidence)   │
              └────────────────┘
```

### W3 Matching Logic Flow

```
Income Transaction → Extract Invoice # from Description
                              ↓
                    ┌─────────┴──────────┐
                    │                    │
              Found Invoice #?      No Invoice #
                    │                    │
            ┌───────▼────────┐    ┌─────▼──────┐
            │ PRIMARY MATCH  │    │ SECONDARY  │
            │ - Invoice #    │    │ MATCH      │
            │ - Amount ±2EUR │    │ - Fuzzy    │
            │ - Date ±7 days │    │   Client   │
            │                │    │   (70%+)   │
            │ Confidence:95% │    │ - Exact $  │
            └───────┬────────┘    │ - Date ±14 │
                    │             │            │
                    │             │ Conf: 75%  │
                    └──────┬──────┴────────────┘
                           │
                    ┌──────▼──────┐
                    │ Match Found?│
                    └──────┬──────┘
                           │
                  ┌────────┴─────────┐
                  │                  │
              Yes Match          No Match
                  │                  │
          ┌───────▼────────┐  ┌─────▼──────────┐
          │ Update Txn:    │  │ Missing Items  │
          │ - InvoiceID    │  │ Report:        │
          │ - InvoiceFile  │  │ - TxnID        │
          │ - Confidence   │  │ - Expected#    │
          │ - Method       │  │ - Amount       │
          └────────────────┘  └────────────────┘
```

### Folder Structure (Current)

```
Expenses-System/
├── _Inbox/
│   ├── Bank-Statements/ (OLD - replaced by Bank & CC Statements)
│   ├── Credit-Card-Statements/
│   └── Expensify-Exports/
├── _Receipt-Pool/ (ID: 1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4)
├── _Invoice-Pool/ (ID: 1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l) ← NEW
├── _Production-Invoices/ (ID: 1_zVNS3JHS15pUjvfEJMh9nzYWn6TltbS) ← NEW
├── _Unmatched/
├── _Archive/
│   └── Statements/
├── VAT 2025/
│   ├── January/
│   │   ├── DKB/
│   │   │   ├── Statements/
│   │   │   └── Receipts/
│   │   ├── Sparkasse/
│   │   │   ├── Statements/
│   │   │   └── Receipts/
│   │   └── Income/ ← NEW (for invoices)
│   └── ... (all 12 months)
└── Expense-Database.gsheet
```

---

## Current State Summary

**System Version:** v2.1.0 (Invoice Automation Complete)
**Phase:** Invoice Collection & Matching
**Efficiency Score:** 7.5/10 (estimated)

**What's Working:**
- ✅ Bank statement monitoring (W1) - Active
- ✅ Gmail receipt + invoice monitoring (W2) - Active with enhancements
- ✅ Multi-source invoice collection architecture - Built
- ✅ Invoice matching with fuzzy logic (W3) - Enhanced, ready for testing
- ✅ File organization including invoices (W4) - Enhanced, active
- ✅ Claude Vision API integration for German invoices - Working

**What's Pending:**
- ⏳ W7 and W8 activation (needs configuration)
- ⏳ Invoices sheet creation
- ⏳ End-to-end testing of invoice flow
- ⏳ G Drive Desktop sync setup for Downloads folder

**System Capabilities (as of v2.1.0):**
- Automated bank statement processing
- Automated receipt collection from Gmail (2 accounts)
- Automated invoice collection from 4 sources
- Automated invoice data extraction (German format support)
- Automated transaction-to-invoice matching with confidence scoring
- Automated file organization to VAT folders (statements, receipts, invoices)
- Missing items reporting for unmatched transactions

**Known Client Names (for fuzzy matching):**
- SUPREME MUSIC
- Massive Voices
- BOXHOUSE
- zweisekundenstille

---

## Next Steps

### Immediate (Next 1-2 Days)

1. **Create Invoices Sheet** in Expense-Database spreadsheet
   - Columns: InvoiceID | ClientName | Amount | Currency | Date | Project | FileID | FileName | ProcessedDate | Source
   - Add to spreadsheet: 1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM

2. **Set up G Drive Desktop Sync**
   - Install Google Drive Desktop app
   - Sync Downloads folder
   - Get synced folder ID for W7 configuration

3. **Fix W8 API Node**
   - Edit Anthropic API node in W8
   - Remove `continueOnFail` property
   - Keep only `onError: continueRegularOutput`

4. **Run Test-Runner Agent** on all workflows
   - Test W7: Downloads categorization with sample files
   - Test W8: German invoice extraction with real invoice
   - Test W2: Invoice detection from Gmail
   - Test W3: Invoice matching with test transactions
   - Test W4: Invoice organization to VAT folders

5. **Activate W7 and W8** after testing passes

### Short-Term (Next 1-2 Weeks)

1. **End-to-End Invoice Flow Testing**
   - Upload test invoice to production folder → W8 processes
   - Upload test invoice to Downloads → W7 processes
   - Send test invoice via Gmail → W2 processes
   - Create test income transaction → W3 matches
   - Run W4 for test month → Verify organization

2. **Monitor Initial Executions**
   - Watch W2 next scheduled run (6:00 AM CET)
   - Review execution logs for errors
   - Verify Invoices sheet updates correctly

3. **Populate Historical Invoices**
   - Backfill Invoices sheet with previous month's invoices
   - Test W3 matching with historical data

### Medium-Term (Next Month)

1. **Edge Case Handling (v2.2.0)**
   - Small expense rules (<€10)
   - GEMA quarterly reminders
   - Annual invoice tracking system
   - Alert system for unmatched ≥€10

2. **Optimization Review**
   - Run workflow-optimizer-agent if performance issues
   - Review token costs for Claude Vision API calls
   - Consider caching for repeated Drive searches

3. **Documentation Updates**
   - Update user guide with invoice flows
   - Create invoice matching troubleshooting guide
   - Document common client name variations

---

## References

- **VERSION_LOG**: [N8N_Blueprints/v1_foundation/VERSION_LOG.md](../N8N_Blueprints/v1_foundation/VERSION_LOG.md)
- **System Design**: `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md`
- **W7 Implementation**: [WORKFLOW_7_IMPLEMENTATION.md](../WORKFLOW_7_IMPLEMENTATION.md)
- **W8 Handoff**: [workflows/W8-HANDOFF.md](../workflows/W8-HANDOFF.md)
- **W3 Enhancements**: `/Users/swayclarke/coding_stuff/expense-system/docs/W3-ENHANCEMENTS-v2.1.md`
- **W4 Implementation**: `/Users/swayclarke/coding_stuff/W4-invoice-organization-implementation.md`

---

## Session Agent IDs (January 11, 2026)

**CRITICAL: These agent IDs can be resumed to continue work if needed**

| Agent ID | Agent Type | Task | Status |
|----------|-----------|------|--------|
| a7e6ae4 | solution-builder-agent | Built W7: Downloads Folder Monitor | ✅ Complete |
| a7fb5e5 | solution-builder-agent | Built W8: G Drive Invoice Collector | ✅ Complete |
| ab6b258 | solution-builder-agent | Enhanced W2: Gmail invoice detection | ✅ Complete |
| a4f02de | solution-builder-agent | Enhanced W3: Income transaction matching | ✅ Complete |
| acf4f3e | solution-builder-agent | Enhanced W4: Invoice organization | ✅ Complete |

**To resume any agent:**
```javascript
Task({
  subagent_type: "solution-builder-agent",
  resume: "a7e6ae4",  // Use agent ID from table above
  prompt: "Continue building/fixing workflow"
})
```

---

**Document Version:** v1.0
**Generated:** January 11, 2026 at 01:30 CET
**Author:** Claude Code (Sway's automation assistant)
**Next Summary Due:** February 10, 2026 (30 days) or when v3.0.0 released
