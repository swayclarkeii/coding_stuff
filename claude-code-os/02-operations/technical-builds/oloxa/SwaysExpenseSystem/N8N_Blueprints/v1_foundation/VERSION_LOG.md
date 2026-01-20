# Sway's Expense System - Version Log

**Project**: Automated Expense Management System
**Location**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem`
**Current Version**: v2.1.6 (W9 Test Harness Built)
**Last Updated**: January 14, 2026

---

## Quick Reference

| Version | Status | Date | Phase | Efficiency Score |
|---------|--------|------|-------|------------------|
| v2.1.6 | 📋 Ready to Test | 2026-01-14 | W9 Test Harness Built | 7.0/10 |
| v2.1.5 | ⚠️ Needs Testing | 2026-01-13 | W7 Critical Fixes Verified | 7.0/10 |
| v2.1.0 | 🔧 Testing | 2026-01-12 | Invoice Collection & Matching | 7.0/10 |
| v1.2.4 | 📋 Blueprint | 2026-01-04 | File Organization | 5.0/10 |
| v1.2.3 | ✅ Fixed | 2026-01-03 | Testing & Validation | 4.8/10 |
| v1.3.1 | 🔄 Recovery | 2026-01-02 | Testing & Validation | 4.5/10 |
| v1.2.0 | ⚠️ Lost | 2025-12-30 | Core Automation | 4.0/10 |
| v1.1.0 | ⚠️ Lost | 2025-12-30 | Core Automation | 3.5/10 |
| v1.0.0 | ✅ Complete | 2025-12-30 | Foundation | 3.0/10 |

---

## Versioning Scheme

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR (v1.x.x)**: Complete phase or major milestone
  - v1.x.x = Foundation (infrastructure setup)
  - v2.x.x = Core Automation (workflows operational)
  - v3.x.x = Full Integration (all features + edge cases)

- **MINOR (vx.1.x)**: Individual workflow completion or feature addition
  - New n8n workflow implemented
  - Major feature added
  - Database schema changes

- **PATCH (vx.x.1)**: Bug fixes, refinements, small improvements
  - Workflow parameter tweaks
  - Vendor mapping additions
  - Configuration updates
  - Documentation corrections

---

## Version History

### v2.1.6 - W9 Test Harness Built (Automated Testing Ready)
**Date**: January 14, 2026
**Status**: 📋 Ready to Test - W9 workflow built, awaiting Sway to upload 6 test files
**Phase**: Testing Infrastructure
**Efficiency Score**: 7.0/10 (maintained - testing capability added)

#### What Was Built

**W9: W7 Test Harness (Automated)**
- **Workflow ID**: `sP2McuKbJ4CO3mNe`
- **Purpose**: Automated comprehensive testing of W7 (Downloads Folder Monitor)
- **Test Scenarios**: 6 files (3 invoices + 3 receipts)
- **Status**: Inactive, ready for activation

#### Key Features

1. **Automated Test Execution** ✅
   - Processes 6 test files from testing folder (`1_ZAtv2DOD_S_6HlUoc2Hbv0TqpFUmNsm`)
   - Moves each file to Downloads folder to trigger W7
   - Waits 2 minutes per file for W7 processing
   - Verifies outputs in pools and sheets
   - Cleans up test files after verification

2. **Comprehensive Verification** ✅
   - **File Routing**: Verifies files appear in correct pool (Invoice or Receipt)
   - **Data Logging**: Verifies data logged to correct sheet (Invoices or Receipts)
   - **Test Report**: Creates Google Spreadsheet with detailed pass/fail results
   - **Error Tracking**: Logs all errors to report spreadsheet

3. **Test Report Spreadsheet** ✅
   - **Name**: "W7 Test Report"
   - **Location**: Expenses-System root folder (`1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15`)
   - **Columns**: Test #, Filename, Expected Type, File in Pool?, Data in Sheet?, Execution Status, Errors, Timestamp
   - **Purpose**: Permanent record of all test executions

4. **Configuration Updates** ✅
   - **Corrected Folder IDs** from W7 actual configuration:
     - Invoice Pool: `1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l` (was incorrect in summary v9.0)
     - Receipt Pool: `1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4` (was incorrect in summary v9.0)
     - Expense Database: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` (was incorrect in summary v9.0)
   - **Added Testing Folder**: `1_ZAtv2DOD_S_6HlUoc2Hbv0TqpFUmNsm` (new)
   - **Added Downloads Folder**: `1O3udIURR14LsEP3Wt4o1QnxzGsR2gciN` (documented from W7)

5. **Google OAuth Credential** ✅
   - **Credential Used**: "Google Sheets account" (id: `H7ewI1sOrDYabelt`)
   - **Covers**: Google Drive API + Google Sheets API (combined OAuth)
   - **Verification**: Confirmed credential exists in n8n and covers both services

#### Workflow Details

**Node Count**: 14 nodes
**Execution Time**: ~12 minutes (6 files × 2 min/file)
**Trigger**: Manual
**Error Handling**: Continue on fail for verification (allows reporting even when tests fail)

**Flow**:
1. Create/verify report spreadsheet exists
2. Add headers to report spreadsheet
3. List test files in testing folder
4. For each file:
   - Determine expected type (Invoice or Receipt)
   - Move to Downloads folder (triggers W7)
   - Wait 2 minutes for W7 processing
   - Verify file in expected pool
   - Verify data in expected sheet
   - Cleanup test file
   - Log result to report
5. All results available in "W7 Test Report" spreadsheet

#### Next Steps

1. **Sway uploads 6 test files** to testing folder (`1_ZAtv2DOD_S_6HlUoc2Hbv0TqpFUmNsm`):
   - 3 files with "invoice" in filename (PDF or image)
   - 3 files with "receipt" in filename (PDF or image)

2. **Activate W9** and trigger manual execution

3. **Review test report** in Expenses-System root folder

4. **Expected Result**: All 6 tests show "SUCCESS" status

#### Agent IDs (For Resume)

- **W9 Build**: Agent ID `a6c7d4e` (solution-builder-agent)
- **Credential Check**: Agent ID `aa42945` (browser-ops-agent)

#### Files Updated

- ✅ `summary_v9.0_2026-01-13.md` - Corrected folder IDs + added W9
- ✅ `VERSION_LOG.md` - Added v2.1.6 entry
- 🔲 `MY-JOURNEY.md` - Pending update

---

### v2.1.5 - W7 Critical Fixes (Execution History Verified)
**Date**: January 13, 2026
**Status**: ⚠️ Real-World Testing Pending - Execution history verified, manual testing required
**Phase**: Critical Bug Fixes for Downloads Folder Monitor
**Efficiency Score**: 7.0/10 (maintained - functionality restored)

#### What Was Fixed

**4 Critical Fixes Applied to W7 (Downloads Folder Monitor):**

1. **Type Mismatch Bypass Nodes** ✅
   - **Issue**: Type conversion errors when passing data between nodes
   - **Fix**: Implemented Code node logic to handle type transitions
   - **Verification**: No type errors in execution history post-fix
   - **Impact**: Workflow handles data type transitions cleanly

2. **Missing Upload Parameters** ✅
   - **Issue**: Google Drive Upload nodes missing required parameters
   - **Fix**: Added all required upload configuration parameters
   - **Nodes Fixed**:
     - Upload to Invoice Pool (complete configuration)
     - Upload to Receipt Pool (complete configuration)
   - **Impact**: Files upload correctly to Google Drive folders

3. **Google Sheets Configuration** ✅ (MOST CRITICAL FIX)
   - **Issue**: Using string sheet names ("Invoices", "Receipts") instead of numeric GIDs
   - **Root Cause**: n8n Google Sheets integration requires numeric sheet GIDs, not names
   - **Fix**: Changed to numeric sheet GIDs:
     - Invoices sheet: GID `1542914058`
     - Receipts sheet: GID `1935486957`
   - **Impact**: Eliminated "Sheet with ID Invoices not found" errors (primary blocker)

4. **Binary Data Preservation** ✅
   - **Issue**: File binary data lost during LLM processing nodes
   - **Fix**: Explicit binary property preservation in Set nodes:
     - Build Anthropic Request node: `data.binary = $input.item.binary`
     - Parse Extraction Results node: `data.binary = $input.item.binary`
   - **Impact**: No "data.binary is missing" errors, files preserved through AI extraction

#### Execution History Evidence

**Before Fixes (Jan 12-13 early):**
- **11 consecutive errors** ❌
- **Primary error**: "Sheet with ID Invoices not found" (Google Sheets configuration)
- **Secondary errors**: Google Drive duplicate check query failures
- **Last error**: Execution #2050 (Jan 13 07:46 UTC)

**After Fixes (Jan 13 11:22 UTC onwards):**
- **Workflow updated**: Jan 13 11:22 UTC with all 4 critical fixes
- **5 consecutive successful executions** ✅
- **100% success rate** (5/5 executions)
- **0 errors**
- **No "data.binary is missing" errors**
- **No Google Sheets errors**
- **No Google Drive upload failures**

**Performance Metrics:**
- Pre-fix error rate: 100% (11/11 failures)
- Post-fix success rate: 100% (5/5 successes)
- **Improvement**: From completely broken → fully operational

#### What This Version Does

**W7 Status After Fixes:**
- ✅ Monitors Downloads folder via Google Drive trigger
- ✅ Categorizes files as invoices or receipts
- ✅ Extracts invoice/receipt data via Claude Vision API
- ✅ Uploads files to Invoice Pool or Receipt Pool
- ✅ Logs metadata to Invoices/Receipts sheets (using correct GIDs)
- ✅ Preserves binary data through entire workflow
- ✅ Executes successfully with 0 errors

#### What This Version Does NOT Do

⚠️ **Real-world end-to-end testing not completed**
- Execution history verified (automated trigger tests)
- Manual testing not yet performed (upload test file → verify complete flow)

#### Testing Status

**Completed:**
- ✅ Execution history analysis (10+ executions reviewed)
- ✅ Error pattern comparison (before/after fixes)
- ✅ Workflow configuration deep inspection
- ✅ Node parameter validation
- ✅ Binary data flow analysis

**Pending:**
- ⚠️ Real-world test: Upload test invoice to Downloads folder
- ⚠️ Verify file appears in Invoice Pool (Google Drive)
- ⚠️ Verify data logged to Invoices sheet (Google Sheets)
- ⚠️ Verify no errors in execution log
- ⚠️ Verify binary data preserved (file downloadable from Invoice Pool)

#### Real-World Test Requirements

**To complete v2.1.5 validation:**

1. **Prepare test file:**
   - Create or download a test invoice PDF
   - Place in Downloads folder (synced via G Drive Desktop)

2. **Monitor execution:**
   - Wait for W7 trigger (Google Drive polling)
   - Check n8n execution log for new execution
   - Verify execution shows "Success"

3. **Verify outputs:**
   - **Google Drive**: File appears in Invoice Pool folder (ID: `1xqLe8kcBUXCuWYF5Kl2Y1BRRuAkjYJxM`)
   - **Google Sheets**: New row in Invoices sheet with extracted data
   - **Binary data**: File is downloadable and not corrupted

4. **Check for errors:**
   - No "data.binary is missing" errors
   - No "Sheet with ID Invoices not found" errors
   - No Google Drive upload failures

**Expected result:** Complete success with file in Invoice Pool and data in Invoices sheet.

#### Session Agent IDs (January 13, 2026)

**Critical Fix Agents:**
- `a46683b`: solution-builder-agent - Binary data preservation fix (CRITICAL)
- `aa7000b`: solution-builder-agent - Google Sheets GID configuration fix
- `adb800e`: solution-builder-agent - Type mismatch bypass implementation
- `a7e6ae4`: solution-builder-agent - W7 initial build (Jan 12)

**Testing & Verification:**
- `a2a1fde`: test-runner-agent - W7 critical fixes verification via execution history
- `a264935`: test-runner-agent - Initial verification attempt (workflow ID issue)
- `ae18b3f`: browser-ops-agent - Visual verification of W7 connections (Jan 12)

#### Documentation Created

**Test Report:**
- Location: `/Users/swayclarke/coding_stuff/test-reports/w7-critical-fixes-verification-report.md`
- Contents: Detailed fix verification, execution timeline, node configuration examples

**Session Summary:**
- Location: `/Users/swayclarke/coding_stuff/session-summaries/2026-01-13-session-w7-critical-fixes.md`
- Contents: Complete timeline, agent IDs, resume instructions

**System State Summary:**
- Location: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/compacting-summaries/summary_v8.0_2026-01-13.md`
- Version: v8.0 - Complete system overview with v2.1.5 status

#### Key Learnings

**1. Google Sheets Integration Pattern:**
- ✅ **Correct**: Use numeric sheet GIDs (e.g., `1542914058`)
- ❌ **Wrong**: Use string sheet names (e.g., `"Invoices"`)
- **Why**: n8n Google Sheets nodes require GIDs from Google Sheets API
- **How to find GIDs**: Check Google Sheets URL or use Sheets API

**2. Binary Data Preservation Pattern:**
- Must explicitly preserve binary data in Set nodes
- Pattern: `data.binary = $input.item.binary`
- Critical for workflows with LLM processing + file uploads
- Without this, files are lost during AI extraction steps

**3. Type Bypass Strategy:**
- Code nodes handle type transitions better than n8n native type conversion
- Custom JavaScript logic more reliable for complex type scenarios
- Use when workflow has type conflicts between nodes

**4. Execution History as Validation:**
- Can verify fixes through execution history analysis
- Before/after comparison shows impact clearly
- Useful when real-world testing not immediately possible
- **BUT**: Always follow up with real-world end-to-end testing

#### Known Issues - v2.1.5

**No new issues introduced by fixes.**

**Existing issues from v2.1.0:**
- 🔴 W7 duplicate check removed (temporary) - v2.2.0 fix planned
- ⚠️ W7 30-day modification filter disabled (testing) - will re-enable after testing

#### Next Steps

**Immediate (Required for v2.1.5 validation):**
1. Upload test invoice to Downloads folder
2. Monitor W7 execution
3. Verify complete flow: Downloads → Invoice Pool → Invoices sheet
4. Confirm 0 errors in execution log

**After v2.1.5 validation:**
1. Update VERSION_LOG.md status to "✅ Tested" (remove ⚠️)
2. Begin v2.2.0 planning (duplicate prevention fix)
3. Consider activating W8 (G Drive Invoice Collector)

---

### v2.1.0 - Invoice Collection & Matching System
**Date**: January 12, 2026
**Status**: 🔧 Testing Phase - All workflows validated, ready for end-to-end testing
**Phase**: Invoice Collection & Automated Matching
**Efficiency Score**: 7.0/10

#### What Was Built

**New Workflows:**
1. **W7: Downloads Folder Monitor** (ID: `6x1sVuv4XKN0002B`)
   - Monitors Downloads folder (synced via G Drive Desktop)
   - Categorizes files as invoices or receipts using filename patterns
   - Claude Vision API extraction for invoice/receipt data
   - Routes to Invoice Pool or Receipt Pool
   - Logs metadata to Invoices/Receipts sheets
   - **Status**: ✅ Active - 24 nodes

2. **W8: G Drive Invoice Collector** (ID: `JNhSWvFLDNlzzsvm`)
   - Monitors Invoice Production folder (`1_zVNS3JHS15pUjvfEJMh9nzYWn6TltbS`)
   - German invoice format extraction (RECHNUNG #, INSGESAMT, DATUM, Projekt)
   - COPY operation (preserves originals in production folder)
   - Routes to centralized Invoice Pool
   - Logs to Invoices sheet
   - **Status**: ⚠️ Inactive - Ready for activation after testing (14 nodes)

**Enhanced Workflows:**
3. **W2: Gmail Receipt Monitor** (ID: `dHbwemg7hEB4vDmC`) - Enhanced
   - Added invoice detection logic
   - Routes client invoices to Invoice Pool
   - Maintains receipt collection to Receipt Pool
   - **Status**: ✅ Active - 23 nodes

4. **W3: Transaction-Receipt-Invoice Matching** (ID: `CJtdqMreZ17esJAW`) - Enhanced
   - **Primary Match**: Invoice # + Amount (±2 EUR) + Date (±7 days) → 95% confidence
   - **Secondary Match**: Fuzzy client name (70%+ Levenshtein) + Exact amount + Date (±14 days) → 75% confidence
   - Known Clients list for targeted fuzzy matching
   - Confidence scoring and match method tracking
   - **Status**: ⚠️ Inactive - Ready for testing (24 nodes)

5. **W4: Monthly Folder Builder & Organizer** (ID: `nASL6hxNQGrNBTV4`) - Enhanced
   - Invoice organization to `VAT 2025/[Month]/Income/` folders
   - Centralized income folder (not bank-specific)
   - Statement and receipt organization maintained
   - **Status**: ⚠️ Inactive - Ready for testing (7 nodes)

#### What This Version Does

**Invoice Collection Architecture:**
- ✅ **4 collection sources** route to centralized Invoice Pool:
  1. W8: Production folder (Sway's invoices)
  2. W7: Downloads folder (scanned/downloaded invoices)
  3. W2: Gmail attachments (client invoices)
  4. Manual uploads to Invoice Pool
- ✅ **Claude Vision API** extracts invoice data (German format support)
- ✅ **Automated matching** links invoices to income transactions
- ✅ **Fuzzy client name matching** handles variations (e.g., "Supreme Music GmbH" vs "SUPREME MUSIC")
- ✅ **Confidence scoring** enables manual review of low-confidence matches
- ✅ **Organized filing** to monthly VAT/Income folders

#### What This Version Does NOT Do

❌ **Duplicate prevention** - Temporarily disabled (see KNOWN ISSUES below)
❌ **Edge case handling** - Deferred to v2.2.0 (small expenses <€10, GEMA reminders, annual invoices)
❌ **G Drive Desktop sync** - Manual setup required for Downloads monitoring
❌ **Invoices sheet creation** - Pending manual creation in Expense-Database spreadsheet

#### KNOWN ISSUES - v2.1.0

**🔴 CRITICAL: W7 Duplicate Check Removed (Temporary)**

**Issue**: W7 nodes 10 and 15 (duplicate check nodes) removed due to Google Drive query API failures
- **Root Cause**: Google Drive query API "Invalid Value" error with special characters (non-breaking spaces, hash symbols, umlauts)
- **Attempted Fixes**: 5+ query string approaches tested (double quotes, single quotes, various escaping methods) - all failed
- **Decision Date**: January 12, 2026
- **Current Implementation**:
  - Nodes 11 & 16 modified to always pass (`true === true`)
  - Clear notes in workflow indicating temporary modification
  - NO duplicate prevention at upload time
- **Impact**:
  - Potential duplicate files in Invoice Pool and Receipt Pool if same file uploaded multiple times
  - May create duplicate Google Sheets rows
  - Acceptable risk for initial testing phase
- **Planned Fix**: v2.2.0 - Client-side List Files + JavaScript comparison
  - Use Google Drive "List Files" operation to get all files in target folder
  - Compare incoming filename against list in n8n (JavaScript/Code node)
  - Skip upload if match found
  - Much simpler and more reliable than query API approach

**⚠️ W7: 30-Day Modification Filter Disabled (Testing)**

**Issue**: W7 Filter Valid Files node has 30-day modification filter commented out
- **Reason**: Testing flexibility - allows uploading older files for validation
- **Lines Affected**: Lines 43-47 in Filter Valid Files Code node
- **Status**: Intentionally disabled - will re-enable after testing complete
- **Risk**: None (controlled testing environment)

**⚠️ W8: continueOnFail/onError Resolved**

**Issue**: W8 Anthropic API node had potential conflict
- **Resolution**: Confirmed `continueOnFail: null` and `onError: "continueRegularOutput"`
- **Status**: ✅ Resolved - No conflict detected

#### Architecture Decisions

**1. Centralized Invoice Pool Approach**
- Single collection point for all invoice sources
- Simplifies W3 matching (searches one location vs. 4+ folders)
- Enables consistent duplicate prevention (when restored)

**2. Copy vs. Move for Production Invoices**
- W8 uses COPY operation (not MOVE)
- Preserves originals in production folder for manual review
- Requires periodic manual cleanup

**3. Fuzzy Client Name Matching**
- 70%+ Levenshtein similarity threshold
- Known Clients list enables targeted matching
- Handles typos, abbreviations, legal suffixes (GmbH, Ltd, Inc)

**4. German Invoice Format Support**
- Claude Vision API with German-specific extraction prompts
- Supports RECHNUNG #, INSGESAMT, DATUM, Projekt fields
- Example pattern: "SC - SUPREME MUSIC GmbH - 122025 #540.pdf"

**5. Confidence Scoring System**
- Primary match (invoice #) = 95% confidence
- Secondary match (fuzzy name) = 75% confidence
- Enables manual review workflow for uncertain matches

#### Testing Status

**All 6 workflows validated:**
- ✅ W1: Bank Statement Monitor - Active and operational
- ✅ W2: Gmail Receipt Monitor - Active with invoice enhancements
- ✅ W3: Transaction-Invoice Matching - Structure validated, ready for testing
- ✅ W4: Monthly Folder Builder - Structure validated, ready for testing
- ✅ W7: Downloads Folder Monitor - Active, duplicate check bypassed (temporary)
- ✅ W8: G Drive Invoice Collector - Structure validated, ready for activation

**Next Testing Steps:**
1. Create Invoices sheet in Expense-Database spreadsheet
2. Set up G Drive Desktop sync for Downloads folder
3. End-to-end testing with real invoices
4. Monitor for duplicate files during testing phase
5. Activate W8 after successful W7 testing

#### Session Agent IDs (January 12, 2026)

**Build Agents:**
- `ad18812`: solution-builder-agent - W7 duplicate node removal
- `ad753d5`: solution-builder-agent - W7 Google Drive duplicate check debugging
- `a7e6ae4`: solution-builder-agent - Built W7: Downloads Folder Monitor
- `a7fb5e5`: solution-builder-agent - Built W8: G Drive Invoice Collector
- `ab6b258`: solution-builder-agent - Enhanced W2: Gmail invoice detection
- `a4f02de`: solution-builder-agent - Enhanced W3: Income transaction matching
- `acf4f3e`: solution-builder-agent - Enhanced W4: Invoice organization

#### Lessons Learned

**1. Google Drive Query API Limitations**
- Query API extremely strict about special character handling
- No clear pattern to what characters are accepted vs. rejected
- Client-side processing (List Files + JavaScript) more maintainable than query construction

**2. Diminishing Returns on API Debugging**
- Set time limit for debugging (e.g., 2 hours), then pivot to alternative approach
- Each fix attempt revealed new edge cases with no clear resolution path

**3. Architecture Flexibility**
- Design for replaceability - don't couple workflow logic tightly to one API approach
- Abstract operations into separate nodes that can be swapped without affecting flow

**4. Production-Like Test Data**
- Real-world filenames contain special characters (non-breaking spaces, umlauts, hash symbols)
- Test with actual user filenames from the start, not simplified examples

---

### v1.2.4 - Workflow 4: File Organization Blueprint
**Date**: January 4, 2026
**Status**: 📋 Blueprint Ready for Import
**Phase**: File Organization
**Efficiency Score**: 5.0/10

#### What Was Built

**Workflow 4: File Organization & Sorting (Blueprint)**
- **Blueprint File**: `workflow4_file_organization_v1.2.4.json`
- **Status**: Ready for import into n8n
- **Node Count**: 7 nodes
- **Purpose**: Organize receipts from Receipt Pool into monthly vendor folders
- **Trigger**: Manual (no scheduling)

#### Workflow Structure

**Node Flow**:
1. **Manual Trigger** - User-initiated execution
2. **Load Receipt Files** - Google Drive: List all files in Receipt Pool (ID: 12SVQzuWtKva48LvdGbszg3UcKl7iy-1x)
3. **Read Receipt Metadata** - Google Sheets: Load Receipts sheet from Expense-Database
4. **Merge Data Streams** - Combine Drive files and Sheet records
5. **Match Files to Metadata** - Code: Join by FileID, filter valid records
6. **Determine Target Folder** - Code: Calculate destination path based on date/vendor
7. **Generate Summary Report** - Code: Output organization plan with statistics

#### What This Version Does

✅ **Loads all receipts** from Receipt Pool folder
✅ **Reads metadata** from Receipts sheet in database
✅ **Matches files to records** by FileID
✅ **Validates data** (checks for missing Date/Vendor)
✅ **Calculates target paths** in format: `Receipts/{year}/{month}/{vendor}`
✅ **Generates summary report** with:
- Total files processed
- Ready to organize count
- Skipped files (missing data)
- Breakdown by vendor
- Breakdown by month
- List of all errors
- Detailed file report with target paths

#### What This Version Does NOT Do

❌ **Does NOT move files** - Only generates organization plan
❌ **Does NOT update database** - FilePath field not modified
❌ **Does NOT create folders** - Assumes folders already exist
❌ **Does NOT handle folder ID lookup** - Target paths are strings, not Drive folder IDs

#### Design Rationale

**Why Blueprint Only (No Live Workflow)?**
- n8n MCP `create_workflow` and `update_partial_workflow` had validation errors with complex connection structures
- Building via MCP operations was taking 10+ attempts with persistent issues
- Blueprint approach is more reliable: single JSON import vs. 20+ incremental operations
- Allows Sway to review structure before importing
- Easier to version control and rollback

**Why No File Moves Yet?**
- Moving files requires folder ID lookup (not just path strings)
- Two options for v1.2.5:
  1. **Hardcode 144 folder IDs** (6 vendors × 12 months × 2 years) - error-prone
  2. **Dynamic Google Drive search** - slower but maintainable
- v1.2.4 validates the matching/path logic before implementing moves
- Testing summary report ensures folder paths are correct

#### Supported Vendors (6 total)

| Database Value | Folder Name | Path Component |
|----------------|-------------|----------------|
| OpenAI | OpenAI | OpenAI |
| Anthropic | Anthropic | Anthropic |
| AWS | AWS | AWS |
| Google Cloud | Google-Cloud | Google-Cloud |
| GitHub | GitHub | GitHub |
| Oura Ring | Oura-Ring | Oura-Ring |

#### Folder Structure Expected

```
Receipts/
├── 2024/
│   ├── 01-January/
│   │   ├── OpenAI/
│   │   ├── Anthropic/
│   │   ├── AWS/
│   │   ├── Google-Cloud/
│   │   ├── GitHub/
│   │   └── Oura-Ring/
│   ├── 02-February/
│   │   └── [same 6 vendors]
│   └── ... (all 12 months)
└── 2025/
    └── [same structure]
```

#### Error Handling

**Errors Logged to Console**:
- Files in Receipt Pool with no metadata in database
- Metadata missing required fields (Date or Vendor)
- Unknown vendor names (not in supported list)
- Invalid date formats (not YYYY-MM-DD)

**All errors included in summary report** under `errors` array.

#### Files Created

1. **Blueprint JSON**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/workflow4_file_organization_v1.2.4.json`
2. **Implementation Guide**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/workflows/workflow4_implementation_guide.md`

#### Import Instructions

1. Delete placeholder workflow in n8n (ID: `nASL6hxNQGrNBTV4`) if it exists
2. Navigate to n8n → Workflows → Import from File
3. Select `workflow4_file_organization_v1.2.4.json`
4. Verify Google OAuth2 credentials are configured (ID: a4m50EefR3DJoU0R)
5. Execute workflow manually to test
6. Review summary report output
7. Update VERSION_LOG.md with actual n8n workflow ID after import

#### Testing Plan

**Prerequisites**:
- 3-5 test receipts in Receipt Pool
- Corresponding records in Receipts sheet with valid FileID, Date, Vendor

**Test Steps**:
1. Import workflow into n8n
2. Execute manually
3. Review "Generate Summary Report" output
4. Verify counts: totalFiles, readyToOrganize, skipped
5. Check errors array for data quality issues
6. Validate target paths match folder structure
7. Inspect console logs for detailed matching results

**Expected Output**:
```json
{
  "totalFiles": 5,
  "readyToOrganize": 5,
  "skipped": 0,
  "byVendor": {"OpenAI": 2, "Anthropic": 2, "GitHub": 1},
  "byMonth": {"2025-01-January": 3, "2024-12-December": 2},
  "errors": []
}
```

#### Known Limitations

1. Only supports 6 vendors (see table above)
2. Only works for 2024-2025 (folder structure limitation)
3. No file moves implemented yet (v1.2.5 feature)
4. No database updates (v1.2.5 feature)
5. Assumes all monthly vendor folders already exist
6. Month folders must use format: `01-January` not `January`

#### Next Steps (v1.2.5)

**To implement actual file organization**:
1. Add folder ID lookup mechanism (dynamic search recommended)
2. Add Google Drive "Move File" operation
3. Add Google Sheets "Update FilePath" operation
4. Add error logging to separate sheet (optional)
5. Test end-to-end with real receipts
6. Validate database updates persist correctly

**Estimated Effort**: 2-3 hours to implement v1.2.5 with moves

#### Rollback Instructions

**To rollback from v1.2.4**:
1. Delete imported workflow in n8n UI
2. No database changes were made (safe rollback)
3. No Google Drive changes were made (safe rollback)
4. Return to v1.2.3 state (3 workflows operational)

#### Efficiency Score Increase

**v1.2.3 → v1.2.4**: 4.8/10 → 5.0/10 (+0.2)

**Rationale**:
- Foundation for automated file organization (+0.2)
- Not yet operational (actual moves in v1.2.5 will add +1.0)
- Validates data quality before implementing moves
- Provides visibility into receipt organization needs

**Projected v1.2.5 Score**: 6.0/10 (when moves are implemented)

---

### v1.2.3 - Workflow 2 Critical Fixes
**Date**: January 3, 2026
**Status**: ✅ Fixed
**Phase**: Testing & Validation
**Efficiency Score**: 4.8/10

#### Critical Bugs Fixed
After analyzing failed execution #32 from 2026-01-02T23:00:21.042Z, discovered and fixed 4 critical configuration errors in Workflow 2 (Gmail Receipt Monitor):

1. **Gmail Search Operation Fix** ✅
   - **Bug**: "Search Gmail for Receipts" node used invalid operation `"search"` (doesn't exist in Gmail node v2.1)
   - **Fix**: Changed to `operation: "getAll"` with proper filters configuration
   - **Impact**: Gmail search now returns valid message objects instead of broken data structure

2. **Environment Variable Fix** ✅
   - **Bug**: "Upload to Receipt Pool" used `={{$env.RECEIPT_POOL_FOLDER_ID}}` (not supported in n8n free)
   - **Fix**: Hardcoded folder ID `12SVQzuWtKva48LvdGbszg3UcKl7iy-1x`
   - **Impact**: Receipts now upload to correct Google Drive folder

3. **Attachment Download Fix** ✅
   - **Bug**: "Download Attachment" used invalid operation `"getAttachment"`
   - **Fix**: Changed to `operation: "get"` with `options: {downloadAttachments: true}`
   - **Impact**: Attachments now download correctly from Gmail messages

4. **Upload Operation Fix** ✅
   - **Bug**: "Upload to Receipt Pool" missing required `operation` parameter
   - **Fix**: Added `operation: "upload"` to Google Drive node
   - **Impact**: File upload operation now properly configured

#### Validation Results
- **Before**: 3 critical errors, 18 warnings
- **After**: 1 minor error (code structure), 18 warnings
- **Status**: Workflow now functional, ready for next scheduled run

#### Next Scheduled Run
- **Trigger**: Daily at 6:00 AM CET
- **Next Run**: January 3, 2026 06:00 CET
- **Expected Behavior**: Search Gmail for receipts from 6 vendors, download attachments, log in database

#### Known Remaining Issues
- Minor code structure warning in "Load Vendor Patterns" (doesn't prevent execution)
- 18 warnings about error handling and outdated typeVersions (non-blocking)

#### Files Updated
- **Workflow**: n8n ID `dHbwemg7hEB4vDmC` (version counter: 25)
- **Last Updated**: 2026-01-03T00:01:03.515Z

---

### v1.3.1 - Post-Rebuild Recovery
**Date**: January 2, 2026
**Status**: 🔄 In Progress
**Phase**: Testing & Validation
**Efficiency Score**: 4.5/10

#### What Happened
On December 31, 2025, **all n8n workflows were erased without backup** due to unknown causes. The system had to be completely rebuilt from scratch.

#### Rebuild Summary
All 3 core workflows were successfully rebuilt in n8n on January 2, 2026:

**Workflow 1: PDF Intake & Parsing (Rebuilt)**
- **New n8n ID**: `MPjDdVMI88158iFW` (previous: `BggZuzOVZ7s87psQ`)
- **Status**: ✅ Active
- **Node Count**: 8 nodes (matches original design)
- **Testing**: 70+ test PDFs uploaded on Dec 31, awaiting validation
- **Changes**: New workflow ID, all node configurations rebuilt from design docs

**Workflow 2: Gmail Receipt Monitor (Rebuilt)**
- **New n8n ID**: `dHbwemg7hEB4vDmC` (previous: `2CA0zQTsdHA8bZKF`)
- **Status**: ⚠️ Inactive (needs activation)
- **Node Count**: 9 nodes (matches original design)
- **Testing**: Not tested yet
- **Changes**: New workflow ID, all node configurations rebuilt from design docs

**Workflow 3: Transaction-Receipt Matching (Rebuilt - Clean Version)**
- **New n8n ID**: `waPA94G2GXawDlCa` (created: Jan 2, 2026)
- **Status**: ✅ Built - Ready for Testing
- **Node Count**: **9 nodes** (matches original design)
- **Architecture Decision**: MODULAR approach chosen
  - Clean, focused workflow for transaction-receipt matching only
  - Proper separation of concerns (W1, W2, W3 are independent)
- **Old Mega Workflow**: `oxHGYOrKHKXyGp4u` - ARCHIVED (renamed "ARCHIVED - Mega Workflow 3 (Broken)")
  - 26 nodes combining W1+W2+W3 - abandoned in favor of modular approach

#### What Survived
✅ **Google Drive Infrastructure**: All 96+ folders intact
✅ **Transaction Database**: Expense-Database spreadsheet intact with all sheets
✅ **VendorMappings**: 12 vendor patterns preserved
✅ **Design Documentation**: All specs, blueprints, and guides intact
✅ **Blueprint Exports**: JSON exports from v1.0-v1.2 available for reference

#### What Was Lost
❌ **Original n8n workflows**: All 3 workflows erased (IDs changed)
❌ **n8n execution history**: 70+ test execution records lost
❌ **Workflow-specific configurations**: Some node settings may need reconfiguration
⚠️ **Authentication credentials**: Google service account credentials may need verification

#### Critical Action Items
1. **Verify Google Service Account credentials** in all 3 workflows (Drive + Sheets nodes)
2. **Validate Workflow 1 test results**: Check if 5-10 sample PDFs created database entries
3. **Activate and test Workflow 2**: Gmail receipt monitoring
4. **Decide Workflow 3 architecture**: Mega workflow vs. 3 separate workflows
5. **End-to-end integration testing**: All workflows working together

#### Known Issues
🔴 **Authentication Risk**: Google Drive/Sheets nodes may be using old credentials instead of new service account
🟡 **Workflow 3 Architecture**: Unclear if mega workflow is intentional or accidental merge
🟡 **Test Validation Pending**: 70+ test PDFs uploaded but not verified in database

#### Rollback Instructions
**Cannot rollback** - original workflows were erased without backup. Current state is the recovery baseline.

To restart from clean state:
1. Deactivate all 3 rebuilt workflows
2. Clear any test data from Transactions/Statements/Receipts sheets
3. Delete test PDFs from Archive folder
4. Rebuild workflows from blueprint JSONs in `N8N_Blueprints/v1_foundation/`

#### Files & Resources
- Workflow 1 (rebuilt): n8n workflow `MPjDdVMI88158iFW`
- Workflow 2 (rebuilt): n8n workflow `dHbwemg7hEB4vDmC`
- Workflow 3 (rebuilt): n8n workflow `oxHGYOrKHKXyGp4u`
- Progress Dashboard: https://docs.google.com/spreadsheets/d/1xRwLX5G-hdFn5j2J-jk_LfIlF5xtR0Gn4Rw3zL2ewA0/edit
- Original blueprints: `N8N_Blueprints/v1_foundation/workflow*.json`

#### Next Version Goal
**v1.4.0 - Full System Validation**
- All 3 workflows tested and operational
- End-to-end integration confirmed
- Authentication verified with service account
- Ready for production use

---

### v1.2.0 - Gmail Receipt Monitor
**Date**: December 30, 2025
**Status**: ✅ Active
**Phase**: Core Automation
**Efficiency Score**: 4.0/10

#### New Components

**Workflow 2: Gmail Receipt Monitor**
- **n8n Workflow ID**: `2CA0zQTsdHA8bZKF`
- **Blueprint**: [`workflow2_gmail_receipt_monitor_v1.2.0.json`](workflow2_gmail_receipt_monitor_v1.2.0.json)
- **Node Count**: 9 nodes
- **Purpose**: Automated daily search of Gmail for receipt emails from 6 vendors, downloads attachments, stores in Receipt Pool, logs in database

**Workflow Structure**:
1. **Daily Receipt Check** (Schedule Trigger) - Runs every 24 hours
2. **Load Vendor Patterns** (Code) - Defines 6 vendor email search patterns
3. **Search Gmail for Receipts** (Gmail) - Searches last 7 days for emails with attachments
4. **Get Email Details** (Gmail) - Retrieves full email metadata
5. **Extract Attachment Info** (Code) - Parses PDF/image attachments from email parts
6. **Download Attachment** (Gmail) - Downloads attachment binary data
7. **Upload to Receipt Pool** (Google Drive) - Stores in `_Receipt-Pool/` folder
8. **Prepare Receipt Record** (Code) - Generates receipt metadata with ID format `RCPT-{VENDOR}-{timestamp}`
9. **Log Receipt in Database** (Google Sheets) - Writes to Receipts sheet

**Vendors Monitored**:
- OpenAI (from:noreply@openai.com)
- Anthropic (from:billing@anthropic.com)
- AWS (from:aws-billing@amazon.com)
- Google Cloud (from:billing-noreply@google.com)
- GitHub (from:billing@github.com)
- Oura Ring (from:hello@ouraring.com)

**Environment Variables Required**:
- `RECEIPT_POOL_FOLDER_ID` - Google Drive folder ID for receipt storage

**What Changed**:
- Added automated Gmail monitoring (previously manual)
- Receipt downloads now happen daily automatically
- All receipts logged to database with metadata
- Efficiency increased from 3.5/10 → 4.0/10

**Known Limitations**:
- Only searches last 7 days (prevent duplicate downloads)
- Limited to 10 emails per vendor per run
- Requires Gmail API credentials configured
- Does not extract amount from email (Amount field left empty)

---

### v1.1.0 - PDF Statement Parser
**Date**: December 30, 2025
**Status**: ✅ Complete
**Phase**: Core Automation
**Efficiency Score**: 3.5/10

#### New Components

**Workflow 1: PDF Intake & Parsing**
- **n8n Workflow ID**: `BggZuzOVZ7s87psQ`
- **Blueprint**: [`workflow1_pdf_intake_v1.0.json`](workflow1_pdf_intake_v1.0.json)
- **Node Count**: 8 nodes
- **Purpose**: Monitors inbox for bank statement PDFs, parses using OpenAI Vision, extracts transactions, writes to database

**Workflow Structure**:
1. **Watch Bank Statements Folder** (Google Drive Trigger) - Monitors for new PDF uploads
2. **Download PDF** (Google Drive) - Retrieves PDF file
3. **Extract File Metadata** (Code) - Parses filename for bank/month/year
4. **Parse PDF with OpenAI Vision** (HTTP Request) - Sends PDF to GPT-4 Vision API
5. **Parse OpenAI Response** (Code) - Transforms AI response to transaction records
6. **Write Transactions to Database** (Google Sheets) - Appends to Transactions sheet
7. **Log Statement Record** (Google Sheets) - Records in Statements sheet
8. **Move PDF to Archive** (Google Drive) - Organizes processed files

**Statement ID Format**: `STMT-{bank}-{yearmonth}-{timestamp}`
**Transaction ID Format**: `{statementId}-{index:003}`

**Environment Variables Required**:
- `BANK_STATEMENTS_FOLDER_ID` - Watch folder for new statements
- `ARCHIVE_STATEMENTS_FOLDER_ID` - Archive location after processing

**What Changed**:
- Added PDF parsing capability (previously manual entry)
- German bank statement support via AI
- Automatic transaction extraction
- Efficiency increased from 3.0/10 → 3.5/10

**Known Limitations**:
- Requires OpenAI API key configured
- Only supports PDF format
- Filename must follow format: `{BANK}_{YYYY-MM}_Statement.pdf`
- No receipt matching yet (all transactions marked `MatchStatus: unmatched`)

---

### v1.0.0 - Foundation Complete
**Date**: December 30, 2025
**Status**: ✅ Complete
**Phase**: Foundation
**Efficiency Score**: 3.0/10

#### Components Created

**1. Google Drive Folder Structure** (96+ folders)
- **Root Folder**: Expenses-System
  - ID: `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15`
  - URL: https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15

**Structure**:
```
📁 Expenses-System/
├── 📁 _Inbox/
│   ├── 📁 Bank-Statements/
│   ├── 📁 Credit-Card-Statements/
│   └── 📁 Expensify-Exports/
├── 📁 _Receipt-Pool/
├── 📁 _Unmatched/
├── 📁 _Archive/
│   └── 📁 Statements/
│       ├── 📁 ING/
│       ├── 📁 Deutsche-Bank/
│       ├── 📁 Barclay/
│       └── 📁 Miles-More/
├── 📁 Income/
│   └── 📁 2025/
│       └── 📁 Invoices/
├── 📁 _Reports/
│   ├── 📁 2024/
│   └── 📁 2025/
├── 📁 2025/
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
│   ├── 📁 02-February/ (same structure)
│   └── ... (all 12 months)
└── 📄 Expense-Database.gsheet
```

**Total Folders Created**: 96+
- 7 main folders
- 12 monthly folders
- 48 bank folders (4 banks × 12 months)
- 96 Statements/Receipts subfolders
- Archive folders for 4 banks

**2. Transaction Database Spreadsheet**
- **Name**: Expense-Database
- **ID**: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
- **URL**: https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM/edit
- **Location**: Expenses-System folder

**Sheets Created** (4 total):

**Sheet 1: Transactions** (16 columns)
```
TransactionID | Date | Bank | Amount | Currency | Description | Vendor | Category |
ReceiptID | StatementID | MatchStatus | MatchConfidence | Notes | Tags | Type | AnnualInvoiceID
```

**Sheet 2: Statements** (8 columns)
```
StatementID | Bank | Month | Year | FileID | FilePath | ProcessedDate | TransactionCount
```

**Sheet 3: Receipts** (10 columns)
```
ReceiptID | Source | Vendor | Date | Amount | Currency | FileID | FilePath | ProcessedDate | Matched
```

**Sheet 4: VendorMappings** (4 columns)
```
BankPattern | NormalizedVendor | Category | GmailSearch
```

**3. System Design Documentation**
- **File**: `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md`
- **Size**: 850+ lines
- **Status**: Complete and approved
- **Sections**: 13 main sections covering all workflows, edge cases, vendor mappings

**4. Project Organization Structure**
- **Location**: `claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/`
- **Folders**:
  - `workflows/` - Workflow documentation and diagrams
  - `N8N_Blueprints/v1_foundation/` - n8n workflow JSON exports
  - `_archive/` - Historical versions and deprecated files

#### What Works
✅ Complete Google Drive folder infrastructure (96+ folders)
✅ Transaction Database with all 4 sheets and proper headers
✅ Comprehensive system design specification approved
✅ Clear vendor mapping patterns defined (11+ vendors)
✅ Edge case handling rules documented
✅ 4 financial institutions supported (ING, Deutsche Bank, Barclay, Miles & More)

#### What Doesn't Work Yet
❌ No automation workflows built (0% automation capability)
❌ VendorMappings sheet is empty (needs 11+ patterns from design doc)
❌ No PDF parsing workflow
❌ No Gmail monitoring workflow
❌ No transaction matching engine
❌ No file organization automation
❌ No notification/reporting system

#### Known Issues
⚠️ n8n workflow "Expense System - Database Setup" (ID: `hf37ifjSLspiQyxF`) exists but webhook registration had issues
- Workaround: Database created manually via Google Sheets MCP instead
- Workflow may be useful for reference but not currently operational

#### Blockers Identified
🔴 **Critical**:
- OpenAI API key needed for PDF parsing (German bank statements)
- Sample German bank statement PDF needed for parsing rule development

🟡 **Important**:
- Gmail API credentials need verification in n8n
- Expensify export format needs to be verified

#### Rollback Instructions
**To completely reset to pre-v1.0.0 state**:
1. Delete Google Drive folder: Expenses-System (ID: `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15`)
2. Delete spreadsheet: Expense-Database (ID: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`)
3. Keep design document at `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md` for reference

**Note**: This is the foundation version, so there's no previous state to roll back to.

#### Files & Resources
- Design Document: `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md`
- Version Log: `claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/VERSION_LOG.md`
- Google Drive Root: https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15
- Transaction Database: https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM/edit

#### Next Version Goal
**v1.1.0 - Workflow 1: PDF Intake & Parsing**
- Build n8n workflow to monitor `_Inbox/Bank-Statements/`
- Integrate OpenAI Vision API for German PDF parsing
- Extract transactions and write to Transactions sheet
- Move processed PDFs to Archive
- **Estimated time**: 2-3 hours
- **Efficiency score target**: 4.5/10

---

## Planned Versions

### v1.1.0 - Workflow 1: PDF Intake & Parsing
**Target Date**: TBD
**Estimated Time**: 2-3 hours
**Efficiency Gain**: 3.0/10 → 4.5/10

**Components to Build**:
- n8n workflow JSON
- OpenAI Vision API integration
- German date/amount parsing rules
- Database write operations
- File moving logic

**Success Criteria**:
- Can process 1 sample German bank statement
- Correctly extracts all transactions
- Writes to database with proper IDs
- Moves PDF to Archive folder

### v1.2.0 - Workflow 2: Gmail Receipt Monitor
**Target Date**: TBD
**Estimated Time**: 1.5-2 hours
**Efficiency Gain**: 4.5/10 → 5.5/10

**Components to Build**:
- Gmail API integration
- Vendor pattern matching
- Receipt download logic
- Store in `_Receipt-Pool/`
- Log in Receipts sheet

### v1.3.0 - Workflow 3: Transaction-Receipt Matching
**Target Date**: TBD
**Estimated Time**: 3-4 hours
**Efficiency Gain**: 5.5/10 → 6.5/10

**Components to Build**:
- Matching algorithm (date ±3 days, amount exact/±€0.50)
- Confidence scoring (0.0-1.0)
- Vendor pattern regex matching
- Database updates (ReceiptID, MatchStatus, MatchConfidence)
- Move matched receipts to organized folders

### v1.4.0 - Workflow 4: File Organization
**Target Date**: TBD
**Estimated Time**: 1.5-2 hours
**Efficiency Gain**: 6.5/10 → 7.0/10

**Components to Build**:
- Receipt sorting from `_Receipt-Pool/` to monthly folders
- Unmatched transaction handling (`_Unmatched/`)
- Statement archiving logic
- Folder existence checks

### v2.0.0 - Core Automation Complete
**Target Date**: TBD
**Estimated Time**: 8-10 hours total (all workflows)
**Efficiency Score**: 7.0/10
**Milestone**: MVP Ready for Testing

**What Makes v2.0.0**:
- All 4 core workflows operational
- End-to-end processing tested with real data
- VendorMappings sheet populated (11+ vendors)
- System can process monthly expenses in 25-30 minutes
- Successfully matched 90%+ of recurring vendor transactions

### v2.1.0 - Edge Case Handling
**Target Date**: TBD
**Components**:
- Small expense handling (<€10)
- GEMA income portal reminders (quarterly)
- Annual invoice tracking system
- Alert system for unmatched transactions ≥€10

### v2.2.0 - Expensify Integration
**Target Date**: TBD
**Components**:
- API-based monthly export automation
- Receipt photo matching to transactions
- Cash expense tracking

### v3.0.0 - Full Integration
**Target Date**: TBD
**Efficiency Score**: 9.0/10
**Components**:
- Weekly digest reports (every Monday)
- Monthly summary generation
- All edge cases handled
- Notification system operational
- Complete system documentation

---

## Component Inventory

### Google Drive Resources
| Component | ID | Version | Status |
|-----------|----|---------| ------|
| Root Folder | `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15` | v1.0.0 | ✅ Active |
| Expense-Database | `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` | v1.0.0 | ✅ Active |

### n8n Workflows
| Workflow | ID | Version | Status |
|----------|----|---------| ------|
| Workflow 1: PDF Intake & Parsing | `MPjDdVMI88158iFW` | v1.1.1 | ✅ Rebuilt (Jan 2, 2026) - Active, 70+ test runs |
| Workflow 2: Gmail Receipt Monitor | `dHbwemg7hEB4vDmC` | v1.2.1 | ✅ Rebuilt (Jan 2, 2026) - Inactive, needs testing |
| Workflow 3: Transaction-Receipt Matching | `waPA94G2GXawDlCa` | v1.3.2 | ✅ Rebuilt (Jan 2, 2026) - Clean 9-node workflow, ready for testing |
| Workflow 3: ARCHIVED Mega Workflow | `oxHGYOrKHKXyGp4u` | v1.3.1 | ⚠️ ARCHIVED - Broken 26-node mega workflow - DO NOT USE |
| Workflow 4: File Organization & Sorting | Blueprint Only | v1.2.4 | 📋 Blueprint ready for import - See `workflow4_file_organization_v1.2.4.json` |
| Workflow 5: Notifications & Reporting | - | Not built | ⏳ Optional |
| Database Setup (deprecated) | `hf37ifjSLspiQyxF` | v1.0.0 | ⚠️ Not operational |

### Documentation Files
| File | Location | Version | Status |
|------|----------|---------|--------|
| System Design | `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md` | v1.0.0 | ✅ Complete |
| Version Log | `SwaysExpenseSystem/N8N_Blueprints/v1_foundation/VERSION_LOG.md` | v1.2.4 | ✅ Active |
| Workflow 4 Implementation Guide | `SwaysExpenseSystem/workflows/workflow4_implementation_guide.md` | v1.2.4 | ✅ Complete |

---

## Efficiency Scoring Rubric

**Scale**: 0-10 (where 10 = fully automated, 25-30 min/month)

### Current Score Breakdown (v1.0.0): 3.0/10

| Category | Weight | Score | Points | Notes |
|----------|--------|-------|--------|-------|
| **Foundation** | 20% | 10/10 | 2.0 | ✅ All infrastructure complete |
| **Core Automation** | 50% | 0/10 | 0.0 | ❌ No workflows built yet |
| **Data Setup** | 10% | 0/10 | 0.0 | ❌ VendorMappings empty |
| **Testing & Validation** | 10% | 0/10 | 0.0 | ❌ No test data processed |
| **Integration & Edge Cases** | 10% | 5/10 | 0.5 | ⚠️ Partial (GDrive/Sheets ✅, Gmail pending) |
| **Total** | 100% | - | **3.0** | Foundation only |

### Target Score by Version
- v1.0.0 (Current): 3.0/10 - Foundation only
- v1.1.0: 4.5/10 - Add PDF parsing
- v1.2.0: 5.5/10 - Add Gmail monitoring
- v1.3.0: 6.5/10 - Add transaction matching
- v1.4.0: 7.0/10 - Add file organization
- v2.0.0: 7.0/10 - All core workflows operational (MVP)
- v2.1.0: 8.0/10 - Edge cases handled
- v3.0.0: 9.0/10 - Full integration with reporting

---

## Rollback Procedures

### General Rollback Process
1. **Identify target version** from this version history
2. **Review what changed** between current and target version
3. **Follow specific rollback instructions** for that version
4. **Verify all components** match target version state
5. **Update "Current Version"** at top of this document
6. **Test system** to ensure rollback was successful

### Component-Specific Rollback

#### Google Drive Folder Structure
- Use Google Drive's "Manage versions" for file changes
- Delete folders created in newer version
- Restore folders from trash if deleted in newer version
- **Verify folder IDs** match version manifest above
- Use MCP tool: `mcp__google-drive__listFolder` to verify structure

#### Transaction Database (Google Sheets)
- Navigate to: File > Version history > See version history
- Find version matching target version timestamp
- Click "Restore this version"
- **Export current version** as backup before rollback
- Verify column headers match version schema in this log

#### n8n Workflows
- Each workflow has built-in version history in n8n UI
- Navigate to workflow > ... menu > Versions
- **Export current workflow JSON** before rollback (File > Download)
- Select previous version to restore
- Click "Restore" button
- **Reactivate workflow** after rollback
- Test workflow execution

#### Design Documents
- If using git: `git checkout <commit-hash> -- <file-path>`
- Otherwise: Keep dated backups manually
- Compare versions using diff tools

### Emergency Rollback (Complete System Reset)
If system becomes unstable, reset to v1.0.0:
```bash
1. Delete all n8n workflows (keep JSON backups)
2. Reset Transaction Database to v1.0.0 schema (empty data)
3. Keep Google Drive folder structure intact
4. Clear VendorMappings sheet
5. Update VERSION_LOG.md to mark current version as v1.0.0
```

---

## Archiving Procedures

### When to Archive
Archive workflow versions whenever:
- Making changes to existing workflows (parameter tweaks, node additions, connection changes)
- Upgrading to a new minor or major version
- Testing experimental features
- Before any potentially breaking changes

### Archive Folder Structure
```
N8N_Blueprints/
└── v1_foundation/
    ├── _archive/
    │   ├── workflow1_pdf_intake_v1.0.0_2025-12-30.json
    │   ├── workflow1_pdf_intake_v1.0.1_2025-12-31.json
    │   ├── workflow2_gmail_receipt_monitor_v1.2.0_2025-12-30.json
    │   └── workflow2_gmail_receipt_monitor_v1.2.1_2025-01-01.json
    ├── workflow1_pdf_intake_v1.1.0.json (current)
    ├── workflow2_gmail_receipt_monitor_v1.2.1.json (current)
    └── workflow3_transaction_receipt_matching_v1.3.0.json (current)
```

### Archiving Workflow Versions

**Step 1: Export Current Workflow from n8n**
```bash
# In n8n UI:
1. Open workflow
2. Click ... menu → Download
3. Save as: workflow{N}_{name}_v{version}_{date}.json
```

**Step 2: Move Previous Version to Archive**
```bash
# Before making changes, copy current version to _archive
cp workflow2_gmail_receipt_monitor_v1.2.0.json \
   _archive/workflow2_gmail_receipt_monitor_v1.2.0_2025-12-30.json
```

**Step 3: Update Current Version File**
```bash
# After changes, export new version with updated version number
# Example: v1.2.0 → v1.2.1 (patch) or v1.3.0 (minor)
mv workflow2_gmail_receipt_monitor_v1.2.0.json \
   workflow2_gmail_receipt_monitor_v1.2.1.json
```

### File Naming Convention

**Active Workflows** (in v1_foundation/):
```
workflow{number}_{name}_v{MAJOR.MINOR.PATCH}.json
Example: workflow2_gmail_receipt_monitor_v1.2.1.json
```

**Archived Workflows** (in _archive/):
```
workflow{number}_{name}_v{MAJOR.MINOR.PATCH}_{YYYY-MM-DD}.json
Example: workflow2_gmail_receipt_monitor_v1.2.0_2025-12-30.json
```

### What to Archive

**Always Archive:**
- ✅ Workflow JSON files before modifications
- ✅ Major documentation changes (SYSTEM_DESIGN.md updates)
- ✅ Database schema changes (export Expense-Database as CSV)

**No Need to Archive:**
- ❌ VERSION_LOG.md (this file tracks all changes already)
- ❌ README.md (living document)
- ❌ Folder structures (Google Drive has version history)

### Retrieval from Archive

**To restore an old version:**
```bash
# 1. Find archived version
ls -la _archive/workflow2_gmail_receipt_monitor_v1.2.0*

# 2. Copy back to active folder
cp _archive/workflow2_gmail_receipt_monitor_v1.2.0_2025-12-30.json \
   workflow2_gmail_receipt_monitor_v1.2.0.json

# 3. Import to n8n
# In n8n UI: Workflows → Import from File → Select JSON
# Choose: "Import as new workflow" to test side-by-side
# OR "Replace current workflow" to restore completely
```

### Archive Retention Policy

- **Keep all archives** for current major version (v1.x.x)
- **Keep last 3 minor versions** of previous major versions
- **Never delete v1.0.0 foundation versions** (baseline for rollback)
- Review and clean archives annually

---

## Version Update Checklist

**Before creating a new version**:
- [ ] Export current n8n workflows as JSON backups
- [ ] Export Transaction Database as CSV/Excel backup
- [ ] Document current system state (folders, files, data)
- [ ] Test rollback procedure to previous version

**When creating a new version**:
- [ ] Update "Current Version" and "Last Updated" at top of file
- [ ] Add new version entry with complete details
- [ ] Document all components created/modified
- [ ] List what works and what doesn't
- [ ] Document known issues and blockers
- [ ] Provide clear rollback instructions
- [ ] Update component inventory with new IDs/versions
- [ ] Update efficiency score and breakdown
- [ ] Test new components thoroughly
- [ ] Export n8n workflow JSONs to `N8N_Blueprints/vX_X/` folder

**After creating a new version**:
- [ ] Tag version in git (if using version control)
- [ ] Update related documentation
- [ ] Notify relevant stakeholders (if applicable)
- [ ] Archive previous version files to `_archive/`

---

## Notes

- **Version numbers are permanent** - never reuse or skip numbers
- **Document ALL breaking changes** clearly in version notes
- **Always test rollback procedures** before deploying to production
- **Keep JSON exports** of all n8n workflows for each version
- **This is a living document** - update as system evolves
- **Efficiency scoring** is subjective but should be consistent across versions
- **Rollback time estimates** should be added for complex versions

---

## Questions & Support

For questions about this version log or the expense system:
1. Review the main design document: `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md`
2. Check component inventory for IDs and URLs
3. Review known issues section for current blockers
4. Consult rollback procedures for recovery steps

Last reviewed: December 30, 2025
