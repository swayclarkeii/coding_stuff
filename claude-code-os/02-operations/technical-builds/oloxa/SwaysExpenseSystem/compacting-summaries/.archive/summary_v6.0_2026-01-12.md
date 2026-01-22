# Sway's Expense System - Project State

**Last Updated:** January 12, 2026 - 19:15 CET
**System Version:** v2.1.0 (Build Complete - Ready for Testing)
**Status:** Active Development - Testing Phase

---

## Current To-Do List

### ✅ Completed (Session: January 12, 2026 - Evening)

**W7 Build Completion:**
- ✅ Removed duplicate check nodes (10 and 15) from W7
- ✅ Fixed Route by Category connections (output 0 → invoices, output 1 → receipts)
- ✅ Verified workflow structure and connections
- ✅ W7 ready for testing (duplicate prevention deferred to v2.2.0)

**Build Verification:**
- ✅ Confirmed Invoices sheet exists with correct columns
- ✅ Validated W8 workflow (no continueOnFail/onError conflicts)
- ✅ All workflows ready for test-runner-agent

**Architecture Decisions:**
- ✅ Decided to skip duplicate checking for now (causing excessive delays)
- ✅ Plan documented to revisit with client-side List Files approach later
- ✅ Understanding clarified: Google Drive DOES create duplicates without prevention

### ⏳ Pending

**Immediate Actions (Next Session):**
- Run test-runner-agent on all 6 workflows (W1, W2, W3, W4, W7, W8)
- Re-enable 30-day modification filter in W7 Filter Valid Files node after testing
- Document W7 changes in VERSION_LOG.md as "KNOWN ISSUE"

**Manual Configuration Tasks:**
- Set up G Drive Desktop app to sync Downloads folder
- Get synced Downloads folder ID for W7 configuration
- Activate W7 and W8 after testing passes

**Duplicate Detection - Future Fix:**
- Implement client-side duplicate prevention (Option A - Recommended):
  - Use Google Drive "List Files" operation to get all files in target folder
  - Compare incoming filename against list in n8n (JavaScript/Code node)
  - If match found: skip upload, log "duplicate skipped"
  - No escaping issues, much simpler than query API
- Alternative: Hash-based deduplication (Option B):
  - Calculate file hash (MD5/SHA256)
  - Store hashes in Google Sheets
  - Check hash before upload (catches renamed duplicates too)

**Future Enhancements:**
- Edge case handling (v2.2.0): Small expenses <€10, GEMA reminders, annual invoices
- Expensify integration (v2.3.0): API export automation, photo matching
- Notification system (v3.0.0): Weekly digests, monthly summaries

### 🔴 Blockers

**Current Blocker (Resolved - Decision Made):**
- ~~Google Drive query API rejects filenames with special characters~~
  - **Resolution**: Skip duplicate checking for now, implement client-side check later
  - **Impact**: W7 can move forward with testing
  - **Risk**: Potential duplicates in Invoice/Receipt pools (acceptable for initial testing)

### ⚠️ Known Issues

1. **W7 Duplicate Check Removed (Temporary)**
   - Issue: Google Drive query API "Invalid Value" error with non-breaking spaces
   - Status: Nodes 10 and 15 to be removed from W7
   - Impact: No duplicate prevention at upload time
   - Consequence: May create duplicate files in pools if same file uploaded twice
   - Planned Fix: Client-side List Files + JavaScript comparison (v2.2.0)

2. **Google Drive Duplicate Behavior**
   - Issue: Google Drive DOES create duplicates when same filename uploaded
   - Impact: Multiple files with same name in same folder (no versioning)
   - Downstream: Multiple rows in Google Sheets, data integrity issues
   - Mitigation: Manual monitoring during initial testing phase

3. **W7 Query String Issues (Historical - For Reference)**
   - Attempted: Double quotes with backslash/quote escaping - Failed
   - Attempted: Single quotes with apostrophe escaping - Failed
   - Attempted: Non-breaking space normalization - Failed
   - Root Cause: Google Drive query API very strict with special character handling
   - Decision: Abandon query approach, use List Files instead (future)

4. **W8 Validation Warning**: Anthropic API node has continueOnFail/onError conflict (non-blocking)
   - Fix: Edit node, remove `continueOnFail` property, keep only `onError`

5. **W2 Gmail Search Complexity**: Searching two Gmail accounts in parallel may hit rate limits
   - Workaround: Daily schedule (6:00 AM CET) should avoid conflicts

6. **W3 Invoice Filename Dependency**: Primary matching requires invoice # in filename
   - Limitation: PDFs without invoice # in filename only get secondary (fuzzy) matching

7. **W4 Date Format Assumption**: Assumes Date column in Invoices sheet is JavaScript-parseable
   - Risk: Invalid date formats will cause filtering errors

---

## Key Decisions Made

### 1. Skip Duplicate Checking in W7 (v2.1.0 - Jan 12, 2026)
**Decision:** Remove duplicate check nodes (10 and 15) from W7, proceed without duplication prevention
**Rationale:**
- Google Drive query API repeatedly failed with "Invalid Value" error
- Tried 5+ different query string approaches (double quotes, single quotes, various escaping)
- Non-breaking spaces (U+00A0), hash symbols, and other special characters causing issues
- Blocking W7 testing for hours with no clear resolution path
- Simple client-side approach (List Files) is more reliable and maintainable

**Impact:**
- W7 can proceed to end-to-end testing immediately
- Potential duplicate files in Invoice Pool and Receipt Pool during testing
- Acceptable risk for initial testing phase
- Must revisit with proper client-side duplicate check in v2.2.0
- Documents "KNOWN ISSUE" in VERSION_LOG.md

**Alternative Considered:**
- Continue debugging query API approach - Rejected (diminishing returns, unclear if solvable)
- Use hash-based deduplication - Deferred to v2.2.0 (more complex, overkill for MVP)

**User Requirement:**
- User explicitly stated: "I don't want to take shortcuts and rely on Google Drive to sort it out"
- User understanding: Google Drive DOES create duplicates without prevention
- User acceptance: Remove for now, but MUST revisit properly later
- User concern: Avoid data integrity issues downstream (multiple Sheets rows, cluttered folders)

### 2. Multi-Source Invoice Collection Architecture (v2.1.0)
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
- Duplicate prevention at collection stage (when working)
- Single source of truth for invoice matching

### 3. Copy vs. Move for Invoice Collection (v2.1.0)
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

### 4. Fuzzy Client Name Matching with Levenshtein Distance (v2.1.0)
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

### 5. Invoice Organization: Centralized Income Folder (v2.1.0)
**Decision:** W4 moves all invoices to `VAT 2025/[Month]/Income/` (not bank-specific)
**Rationale:**
- Invoices are income documents, not tied to specific bank accounts
- Multiple banks may receive same client payment
- Simpler folder structure for tax reporting

**Impact:**
- All monthly invoices in single folder per month
- Easier for accountant to locate income documents
- May need subfolder by client if volume increases (future v2.2.0+)

### 6. German Invoice Format Support (v2.1.0)
**Decision:** Claude Vision API with German-specific extraction prompts
**Rationale:**
- German invoice format: RECHNUNG #, INSGESAMT, DATUM, Projekt
- Different field names than English invoices
- W8 uses targeted German extraction prompt

**Impact:**
- Accurate extraction from German invoices (Sway's primary format)
- May need English prompt variant for client invoices (future)
- Example pattern: "SC - SUPREME MUSIC GmbH - 122025 #540.pdf"

### 7. Primary vs. Secondary Matching Strategy (v2.1.0)
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

| Workflow Name | ID | Status | Purpose | Latest Agent ID |
|--------------|-----|--------|---------|-----------------|
| W1: Bank Statement Monitor | MPjDdVMI88158iFW | ✅ Active | Monitors new Bank & CC Statements folder, processes PDFs | - |
| W2: Gmail Receipt Monitor | dHbwemg7hEB4vDmC | ✅ Active | Monitors Gmail for receipts + invoices (enhanced) | ab6b258 |
| W3: Transaction-Receipt-Invoice Matching | CJtdqMreZ17esJAW | ⚠️ Inactive | Matches transactions to receipts/invoices with fuzzy logic | a4f02de |
| W4: Monthly Folder Builder & Organizer | nASL6hxNQGrNBTV4 | ✅ Active | Creates VAT folders, organizes statements/receipts/invoices | acf4f3e |
| W7: Downloads Folder Monitor | 6x1sVuv4XKN0002B | 🔧 Debugging | Monitors Downloads, categorizes receipts/invoices | **ad753d5** (Jan 12) |
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

### W7 Specific Node IDs (For Reference)

| Node Name | Node ID | Status | Notes |
|-----------|---------|--------|-------|
| Check Invoice Pool Duplicates | a8c7f2d1-node10-new | ⚠️ To be removed | Repeated "Invalid Value" errors |
| Check Receipt Pool Duplicates | b9d8e3f2-node15-new | ⚠️ To be removed | Same query issues as node 10 |
| Route by Category | - | ✅ Working | IF node routing invoices/receipts |
| Upload to Invoice Pool | - | ⏳ Pending test | Will connect directly after removal |
| Upload to Receipt Pool | - | ⏳ Pending test | Will connect directly after removal |

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

### W7 Debugging Timeline (January 12, 2026)

**Problem**: Google Drive duplicate check query failing with "Invalid Value" error

**Attempts Made:**
1. **Attempt 1**: Double-quoted query with backslash/quote escaping
   - Query: `name = "filename" and "folderID" in parents`
   - Result: Invalid Value error
   - Issue: Non-breaking space (U+00A0) in filename

2. **Attempt 2**: Added non-breaking space normalization
   - Query: `.replace(/\u00a0/g, ' ')` before building query
   - Result: Still Invalid Value error
   - Issue: Hash symbol (#) or other special characters

3. **Attempt 3**: Removed hash escaping
   - Rationale: Hash doesn't need escaping in Google Drive queries
   - Result: Still Invalid Value error
   - Issue: Query syntax itself problematic

4. **Attempt 4**: Single-quoted query with apostrophe escaping
   - Query: `name = 'filename' and 'folderID' in parents`
   - Rationale: Single quotes more permissive with special characters
   - Result: Still Invalid Value error
   - Issue: Non-breaking space still causes problems

5. **Attempt 5**: Single quotes + non-breaking space normalization
   - Query: `.replace(/\u00A0/g, ' ').replace(/'/g, "\\'")`
   - Result: Still Invalid Value error
   - Issue: Unknown - possibly query API limitation

**Test File Used:**
- Filename: `SC - zweisekundenstille Tonstudios GmbH - 122025 #520.pdf`
- Contains: Non-breaking space (U+00A0) between "zweisekundenstille" and "Tonstudios"
- Contains: Hash symbol (#) in invoice number
- Google Drive normalized name: Same format with regular space

**Executions Analyzed:**
- Execution 1777: Node corruption (upload operation instead of search)
- Execution 1780: Invalid Value error after fixing node parameters
- Execution 1794: Invalid Value error after single-quote fix
- Execution 1796: Invalid Value error after non-breaking space normalization

**Root Cause Analysis:**
- Google Drive query API is extremely strict about special character handling
- Non-breaking spaces (U+00A0) seem to be rejected even when normalized
- Hash symbols may be interpreted as special characters in some contexts
- Query string construction with expression evaluation may have hidden issues
- No clear pattern to what characters are accepted vs. rejected

**Decision**: Abandon query approach, remove duplicate check nodes, implement client-side check later

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
         │      NO DUPLICATE │  NO DUPLICATE      │  NO DUPLICATE
         │      CHECK (v6.0) │  CHECK (v6.0)      │  CHECK (v6.0)
         │                   │                    │
         └────────────┬──────┴────────────────────┘
                      │
              ┌───────▼────────┐
              │  INVOICE POOL  │
              │  (May have     │
              │   duplicates)  │
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
│   └── ⚠️ MAY CONTAIN DUPLICATES (v6.0 - no prevention)
├── _Invoice-Pool/ (ID: 1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l)
│   └── ⚠️ MAY CONTAIN DUPLICATES (v6.0 - no prevention)
├── _Production-Invoices/ (ID: 1_zVNS3JHS15pUjvfEJMh9nzYWn6TltbS)
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
│   │   └── Income/ (for invoices)
│   └── ... (all 12 months)
└── Expense-Database.gsheet
```

---

## Current State Summary

**System Version:** v2.1.0 (W7 Debugging - Duplicate Check Issues)
**Phase:** Invoice Collection & Matching / W7 Troubleshooting
**Efficiency Score:** 7.0/10 (estimated - reduced from 7.5 due to W7 blocking issue)

**What's Working:**
- ✅ Bank statement monitoring (W1) - Active
- ✅ Gmail receipt + invoice monitoring (W2) - Active with enhancements
- ✅ Multi-source invoice collection architecture - Built
- ✅ Invoice matching with fuzzy logic (W3) - Enhanced, ready for testing
- ✅ File organization including invoices (W4) - Enhanced, active
- ✅ Claude Vision API integration for German invoices - Working

**What's Blocked:**
- 🔴 W7 duplicate check - Google Drive query API failures (DECISION: Remove nodes)
- 🔴 W7 end-to-end testing - Blocked by duplicate check issues (UNBLOCKING NOW)

**What's Pending:**
- ⏳ W7 activation (needs duplicate nodes removed first)
- ⏳ W8 activation (needs configuration)
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
- ⚠️ **NO duplicate prevention** (temporary - v6.0 state)

**Known Client Names (for fuzzy matching):**
- SUPREME MUSIC
- Massive Voices
- BOXHOUSE
- zweisekundenstille

---

## Next Steps

### Immediate (Right Now - January 12)

1. **Remove W7 Duplicate Check Nodes**
   - Delete node 10 (Check Invoice Pool Duplicates)
   - Delete node 15 (Check Receipt Pool Duplicates)
   - Connect Route by Category directly to Upload nodes
   - Export updated W7 workflow JSON
   - Document removal in VERSION_LOG.md as "KNOWN ISSUE"

2. **Test W7 End-to-End**
   - Upload test invoice and receipt files to Downloads
   - Verify categorization works (Route by Category)
   - Verify uploads to Invoice Pool and Receipt Pool
   - Verify logging to Invoices/Receipts sheets
   - Accept that duplicates may occur if same file uploaded twice

3. **Re-enable 30-Day Modification Filter**
   - W7 Filter Valid Files node currently has filter disabled for testing
   - After successful test, restore: `modifiedTime >= [30 days ago]`

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

1. **Implement Proper Duplicate Prevention (v2.2.0)**
   - Use Google Drive "List Files" operation
   - Compare filenames in JavaScript Code node
   - Skip upload if match found
   - Log "duplicate skipped" to console
   - **CRITICAL**: Don't rely on Google Drive to prevent duplicates

2. **End-to-End Invoice Flow Testing**
   - Upload test invoice to production folder → W8 processes
   - Upload test invoice to Downloads → W7 processes
   - Send test invoice via Gmail → W2 processes
   - Create test income transaction → W3 matches
   - Run W4 for test month → Verify organization

3. **Monitor Initial Executions**
   - Watch W2 next scheduled run (6:00 AM CET)
   - Review execution logs for errors
   - Verify Invoices sheet updates correctly
   - **Monitor for duplicate files** in pools

4. **Populate Historical Invoices**
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
   - Add duplicate prevention guide

---

## References

- **VERSION_LOG**: [N8N_Blueprints/v1_foundation/VERSION_LOG.md](../N8N_Blueprints/v1_foundation/VERSION_LOG.md)
- **System Design**: `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md`
- **W7 Implementation**: [WORKFLOW_7_IMPLEMENTATION.md](../WORKFLOW_7_IMPLEMENTATION.md)
- **W8 Handoff**: [workflows/W8-HANDOFF.md](../workflows/W8-HANDOFF.md)
- **W3 Enhancements**: `/Users/swayclarke/coding_stuff/expense-system/docs/W3-ENHANCEMENTS-v2.1.md`
- **W4 Implementation**: `/Users/swayclarke/coding_stuff/W4-invoice-organization-implementation.md`

---

## Session Agent IDs (January 12, 2026 - Evening)

**CRITICAL: These agent IDs can be resumed to continue work if needed**

| Agent ID | Agent Type | Task | Status | Notes |
|----------|-----------|------|--------|-------|
| ad18812 | solution-builder-agent | W7 duplicate node removal | ✅ Complete | Removed nodes 10 & 15, reconnected workflow flow |
| ad753d5 | solution-builder-agent | W7 Google Drive duplicate check debugging | ✅ Complete | Multiple query attempts, decision to remove nodes |

**Previous Session Agent IDs (January 11, 2026):**

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
  resume: "ad753d5",  // Use agent ID from table above
  prompt: "Continue W7 duplicate check work or implement removal"
})
```

---

## Lessons Learned (January 12, 2026)

### 1. Google Drive Query API Limitations
**Issue**: Query API extremely strict about special character handling
**Discovery**: 5+ hours debugging query string with no clear resolution
**Learning**: Client-side List Files + JavaScript comparison is simpler and more maintainable
**Application**: Always consider client-side processing before complex API query construction

### 2. Diminishing Returns on API Debugging
**Issue**: Each fix attempt revealed new edge cases (non-breaking spaces, hash symbols, etc.)
**Discovery**: No clear pattern to what characters Google Drive query API accepts
**Learning**: Know when to abandon an approach and try fundamentally different solution
**Application**: Set time limit for debugging (e.g., 2 hours), then pivot to alternative approach

### 3. User Communication on Technical Blockers
**Issue**: Initial attempts to debug without explaining full implications of skipping duplicate check
**Discovery**: User needs to understand risks (duplicates in pools, data integrity issues) to make informed decision
**Learning**: Be transparent about trade-offs, consequences, and future fix plans
**Application**: Explain both short-term workaround AND long-term proper solution when proposing compromise

### 4. Test File Characteristics Matter
**Issue**: Test file had multiple special characters (non-breaking space, hash symbol, umlauts)
**Discovery**: Real-world filenames are complex and edge cases are common
**Learning**: Use production-like test data from the start, not simplified examples
**Application**: Always test with actual user filenames that contain special characters

### 5. Architecture Flexibility
**Issue**: Initially designed duplicate check as query-based API approach
**Discovery**: Multiple valid solutions exist (query API, List Files, hash-based)
**Learning**: Design for replaceability - don't couple workflow logic tightly to one API approach
**Application**: Abstract duplicate check into separate nodes that can be swapped without affecting flow

---

**Document Version:** v6.0
**Generated:** January 12, 2026 at 11:45 CET
**Author:** Claude Code (Sway's automation assistant)
**Next Summary Due:** February 12, 2026 (30 days) or when v3.0.0 released
**Session Focus:** W7 Debugging & Duplicate Check Architecture Decision
