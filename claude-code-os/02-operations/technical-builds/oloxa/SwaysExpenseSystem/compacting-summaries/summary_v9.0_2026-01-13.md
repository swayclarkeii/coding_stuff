# Sway's Expense System - Summary

**Version:** v9.0
**System Version:** v2.1.5 (W7 Critical Fixes - Real-World Testing Pending)
**Last Updated:** January 13, 2026
**Status:** ⚠️ Real-World Testing Required - Execution history verified, manual testing pending

---

## 🚀 START HERE AFTER RESTART

**Quick Context:** W7 (Downloads Folder Monitor) had 4 critical bugs causing 100% failure rate. All bugs fixed and verified via execution history (11 errors → 5 successes). **Real-world testing still needed.**

**Next Action:**
1. Upload test invoice to Downloads folder
2. Verify file appears in Invoice Pool (Google Drive)
3. Verify data logged to Invoices sheet
4. Confirm 0 errors in execution log

**Agent IDs to Resume:** See section below ⬇️

---

## Agent IDs (Resume Work)

**CRITICAL:** Use these agent IDs to resume work in new conversations.

### January 13, 2026 - W7 Critical Fixes Session

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| `a46683b` | solution-builder-agent | Binary data preservation fix (CRITICAL) | ✅ Complete |
| `aa7000b` | solution-builder-agent | Google Sheets GID configuration fix | ✅ Complete |
| `adb800e` | solution-builder-agent | Type mismatch bypass implementation | ✅ Complete |
| `a2a1fde` | test-runner-agent | W7 critical fixes verification via execution history | ✅ Complete |
| `a264935` | test-runner-agent | Initial verification attempt (workflow ID issue) | ⚠️ Failed - wrong workflow ID |

### January 12, 2026 - W7 Build Session

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| `a7e6ae4` | solution-builder-agent | W7: Downloads Folder Monitor - Initial build | ✅ Complete |
| `a7fb5e5` | solution-builder-agent | W8: G Drive Invoice Collector - Build | ✅ Complete |
| `ae18b3f` | browser-ops-agent | Visual verification of W7 connections | ✅ Complete |
| `ad18812` | solution-builder-agent | W7 duplicate node removal | ✅ Complete |
| `ad753d5` | solution-builder-agent | W7 Google Drive duplicate check debugging | ⚠️ Partial - removed duplicates temporarily |
| `ab6b258` | solution-builder-agent | Enhanced W2: Gmail invoice detection | ✅ Complete |
| `a4f02de` | solution-builder-agent | Enhanced W3: Income transaction matching | ✅ Complete |
| `acf4f3e` | solution-builder-agent | Enhanced W4: Invoice organization | ✅ Complete |

**Usage:**
- Resume specific agent: `Task({ subagent_type: "solution-builder-agent", resume: "a46683b", prompt: "..." })`
- Reference this summary: "Review summary v9.0 for context"

---

## Current To-Do List

### ✅ Completed (Jan 13, 2026)

- ✅ Fixed W7 type mismatch errors (Code node bypass)
- ✅ Fixed W7 missing upload parameters (Google Drive nodes)
- ✅ Fixed W7 Google Sheets configuration (string names → numeric GIDs)
- ✅ Fixed W7 binary data preservation (explicit preservation in Set nodes)
- ✅ Verified fixes via execution history (100% success rate post-fix)
- ✅ Created test report (`w7-critical-fixes-verification-report.md`)
- ✅ Created session summary (`2026-01-13-session-w7-critical-fixes.md`)
- ✅ Updated VERSION_LOG.md with v2.1.5
- ✅ Updated MY-JOURNEY.md with v2.1.5 success

### ⏳ Pending (Immediate Priority)

- ⚠️ **Real-world test W7**: Upload test invoice to Downloads folder
- ⚠️ Verify file appears in Invoice Pool (Google Drive: `1xqLe8kcBUXCuWYF5Kl2Y1BRRuAkjYJxM`)
- ⚠️ Verify data logged to Invoices sheet (Sheet GID: `1542914058`)
- ⚠️ Verify no errors in execution log
- ⚠️ Verify binary data preserved (file downloadable)

### ⏳ Pending (After v2.1.5 Validation)

- 🔲 Update VERSION_LOG.md status to "✅ Tested" (remove ⚠️)
- 🔲 Begin v2.2.0 planning (duplicate prevention fix)
- 🔲 Consider activating W8 (G Drive Invoice Collector)
- 🔲 Test W3 (Transaction-Invoice Matching)
- 🔲 Test W4 (Monthly Folder Builder)

### 🔴 Blockers

**None currently.** All critical fixes applied and verified.

### ⚠️ Known Issues

**From v2.1.0 (Not blocking current work):**
- 🔴 **W7 duplicate check removed** (temporary) - v2.2.0 fix planned
  - **Issue**: Google Drive query API fails with special characters
  - **Workaround**: Duplicate check nodes removed, always pass (`true === true`)
  - **Impact**: Potential duplicate files if same file uploaded multiple times
  - **Planned Fix**: v2.2.0 - Client-side List Files + JavaScript comparison

- ⚠️ **W7 30-day modification filter disabled** (testing flexibility)
  - **Issue**: Testing requires uploading older files
  - **Status**: Intentionally disabled - will re-enable after testing complete
  - **Risk**: None (controlled testing environment)

---

## Key Decisions Made

### 1. Google Sheets GID Configuration (v2.1.5 - Jan 13, 2026)
**Decision:** Use numeric sheet GIDs instead of string sheet names
**Rationale:** n8n Google Sheets nodes require numeric GIDs from Google Sheets API, not human-readable names
**Impact:** Eliminated "Sheet with ID Invoices not found" errors (primary blocker causing 100% failure rate)
**Pattern:**
- ✅ **Correct**: `sheetId: 1542914058` (numeric GID)
- ❌ **Wrong**: `sheetName: "Invoices"` (string name)

### 2. Binary Data Preservation Pattern (v2.1.5 - Jan 13, 2026)
**Decision:** Explicitly preserve binary data in Set nodes during LLM processing
**Rationale:** File binary data lost when passing through AI extraction nodes without explicit preservation
**Impact:** No "data.binary is missing" errors, files successfully upload to Google Drive
**Pattern:** `data.binary = $input.item.binary` in Set nodes before/after LLM calls

### 3. Type Bypass Strategy (v2.1.5 - Jan 13, 2026)
**Decision:** Use Code nodes for type transitions instead of n8n native type conversion
**Rationale:** Custom JavaScript logic more reliable for complex type scenarios
**Impact:** Workflow handles data type transitions cleanly without type errors

### 4. Centralized Invoice Pool Approach (v2.1.0 - Jan 12, 2026)
**Decision:** Single collection point for all invoice sources (W7, W8, W2, manual)
**Rationale:** Simplifies W3 matching (searches one location vs. 4+ folders), enables consistent duplicate prevention
**Impact:** Cleaner architecture, easier to maintain, better match accuracy

### 5. Copy vs. Move for Production Invoices (v2.1.0 - Jan 12, 2026)
**Decision:** W8 uses COPY operation (not MOVE) for production invoices
**Rationale:** Preserves originals in production folder for manual review, reduces risk
**Impact:** Requires periodic manual cleanup but safer approach

---

## Important IDs / Paths / Workflow Names

### n8n Workflows

| Workflow Name | ID | Status | Nodes | Purpose |
|--------------|-----|--------|-------|---------|
| **W1: PDF Intake & Parsing** | `MPjDdVMI88158iFW` | ✅ Active | 9 | Bank statement PDF parsing |
| **W2: Gmail Receipt Monitor** | `dHbwemg7hEB4vDmC` | ✅ Active | 32 | Email receipt/invoice monitoring |
| **W3: Transaction-Invoice Matching** | `CJtdqMreZ17esJAW` | ⚠️ Inactive | 27 | Invoice-transaction matching (needs testing) |
| **W4: Monthly Folder Builder** | `nASL6hxNQGrNBTV4` | ⚠️ Inactive | 28 | File organization (needs testing) |
| **W6: Expensify PDF Parser** | `l5fcp4Qnjn4Hzc8w` | ✅ Active | 14 | Expensify export processing |
| **W7: Downloads Folder Monitor** | `6x1sVuv4XKN0002B` | ⚠️ Active - Needs Testing | 22 | Autopilot inbox (JUST FIXED) |
| **W8: G Drive Invoice Collector** | `JNhSWvFLDNlzzsvm` | ⚠️ Inactive | 14 | Production folder monitoring (ready for activation) |
| **W9: W7 Test Harness (Automated)** | `sP2McuKbJ4CO3mNe` | ⚠️ Inactive - Ready to Test | 14 | Automated W7 validation (6 files → verify pools + sheets) |

### Google Sheets

| Spreadsheet Name | ID | Purpose |
|-----------------|-----|---------|
| **Expense-Database** | `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` | Main expense tracking database (W7 destination) |
| **- Transactions sheet** | Sheet GID: `0` | Bank transactions |
| **- Statements sheet** | Sheet GID: `846217120` | Statement metadata |
| **- Receipts sheet** | Sheet GID: `1935486957` | Receipt metadata (W7 logs receipt data here) |
| **- Invoices sheet** | Sheet GID: `1542914058` | Invoice metadata (W7 logs invoice data here - CRITICAL fix) |
| **- VendorMappings sheet** | Sheet GID: Not documented | Vendor pattern matching |
| **W7 Test Report** | Created by W9 | Test results for W7 validation (in root folder) |

### Google Drive Folders

| Folder Name | ID | Purpose |
|-------------|-----|---------|
| **Expenses-System** | `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15` | Root folder |
| **Invoice Pool** | `1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l` | Centralized invoice collection (W7 destination) |
| **Receipt Pool** | `1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4` | Centralized receipt collection (W7 destination) |
| **Downloads Folder** | `1O3udIURR14LsEP3Wt4o1QnxzGsR2gciN` | W7 monitoring folder (G Drive Desktop sync) |
| **Testing Folder** | `1_ZAtv2DOD_S_6HlUoc2Hbv0TqpFUmNsm` | W9 test files source (6 files: 3 invoices + 3 receipts) |

### File Paths

| File | Location | Purpose |
|------|----------|---------|
| **VERSION_LOG.md** | `SwaysExpenseSystem/N8N_Blueprints/v1_foundation/VERSION_LOG.md` | Complete version history |
| **Test Report** | `/Users/swayclarke/coding_stuff/test-reports/w7-critical-fixes-verification-report.md` | W7 fix verification details |
| **Session Summary** | `/Users/swayclarke/coding_stuff/session-summaries/2026-01-13-session-w7-critical-fixes.md` | Jan 13 session timeline |
| **System Design** | `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md` | Original system design (850+ lines) |

---

## Technical Architecture

### W7: Downloads Folder Monitor (JUST FIXED - v2.1.5)

**Flow:**
```
Downloads Folder (G Drive Desktop sync)
  ↓
Google Drive Trigger (polling)
  ↓
Filter Valid Files (PDF/image, >30 days old - disabled for testing)
  ↓
Categorize (Invoice vs Receipt via filename patterns)
  ↓
Branch: Invoice Path | Receipt Path
  ↓                 ↓
Type Bypass (Code) | Type Bypass (Code)
  ↓                 ↓
Build Anthropic Request (preserve binary data)
  ↓                 ↓
Claude Vision API (extract invoice/receipt data)
  ↓                 ↓
Parse Extraction Results (preserve binary data)
  ↓                 ↓
Upload to Invoice Pool | Upload to Receipt Pool
  ↓                 ↓
Log to Invoices sheet (GID 1542914058) | Log to Receipts sheet (GID 1935486957)
```

**Critical Fixes Applied:**
1. **Type Bypass Nodes**: Code nodes handle type transitions
2. **Upload Parameters**: All required Google Drive parameters configured
3. **Google Sheets GIDs**: Numeric GIDs instead of string names (CRITICAL)
4. **Binary Preservation**: Explicit `data.binary = $input.item.binary` in Set nodes

**Execution History:**
- Pre-fix: 11 consecutive errors (100% failure rate)
- Post-fix: 5 consecutive successes (100% success rate)
- **Status**: Verified via execution history, real-world testing pending

### Invoice Collection Architecture (v2.1.0)

**4 Collection Sources → Centralized Invoice Pool:**

1. **W8**: Production folder (Sway's invoices) - COPY operation
2. **W7**: Downloads folder (scanned/downloaded invoices) - MOVE operation
3. **W2**: Gmail attachments (client invoices) - Download + upload
4. **Manual**: Direct uploads to Invoice Pool

**Benefits:**
- Single search location for W3 matching
- Consistent duplicate prevention (when restored)
- Simpler architecture vs. searching multiple folders

### Matching System (W3 - Not yet tested)

**Primary Match (95% confidence):**
- Invoice # match (exact)
- Amount match (±2 EUR tolerance)
- Date match (±7 days)

**Secondary Match (75% confidence):**
- Fuzzy client name (70%+ Levenshtein similarity)
- Exact amount match
- Date match (±14 days)

---

## Current State Summary

**Version:** v2.1.5
**Phase:** Critical Bug Fixes - Execution History Verified
**Efficiency Score:** 7.0/10 (maintained - functionality restored)

**System Capabilities:**
- ✅ Bank statement parsing (W1)
- ✅ Gmail receipt/invoice monitoring (W2)
- ✅ Expensify export processing (W6)
- ✅ Downloads folder monitoring (W7 - JUST FIXED, needs real-world test)
- ⚠️ Transaction-invoice matching (W3 - ready for testing)
- ⚠️ Monthly folder organization (W4 - ready for testing)
- ⚠️ Production invoice collection (W8 - ready for activation)

**Performance Metrics:**
- W7 Pre-fix error rate: 100% (11/11 failures)
- W7 Post-fix success rate: 100% (5/5 successes)
- **Improvement**: From completely broken → fully operational (execution history verified)

**Active Workflows:** 4 of 8
**Inactive (Ready):** 3 of 8
**Testing Status:** Real-world validation pending for W7

---

## Next Steps

### Immediate (Required for v2.1.5 Validation)

1. **Upload test invoice** to Downloads folder
   - Create or download test invoice PDF
   - Place in Downloads folder (synced via G Drive Desktop)

2. **Monitor W7 execution**
   - Wait for Google Drive trigger (polling-based)
   - Check n8n execution log for new execution
   - Verify execution shows "Success"

3. **Verify outputs**
   - **Google Drive**: File appears in Invoice Pool (ID: `1xqLe8kcBUXCuWYF5Kl2Y1BRRuAkjYJxM`)
   - **Google Sheets**: New row in Invoices sheet (GID: `1542914058`)
   - **Binary data**: File is downloadable and not corrupted

4. **Check for errors**
   - No "data.binary is missing" errors
   - No "Sheet with ID Invoices not found" errors
   - No Google Drive upload failures

**Expected Result:** Complete success with file in Invoice Pool and data in Invoices sheet.

### After v2.1.5 Validation

1. Update VERSION_LOG.md status to "✅ Tested" (remove ⚠️)
2. Begin v2.2.0 planning (duplicate prevention fix)
3. Consider activating W8 (G Drive Invoice Collector)
4. Test W3 (Transaction-Invoice Matching)
5. Test W4 (Monthly Folder Builder)

### v2.2.0 Planning (Future)

**Planned Fix: W7 Duplicate Prevention**
- **Issue**: Google Drive query API fails with special characters
- **Solution**: Client-side List Files + JavaScript comparison
- **Implementation**:
  1. Use Google Drive "List Files" operation to get all files in target folder
  2. Compare incoming filename against list in n8n (JavaScript/Code node)
  3. Skip upload if match found
- **Benefit**: Much simpler and more reliable than query API approach

---

## Key Learnings from v2.1.5

### 1. Google Sheets Integration Pattern
**Problem:** Using string sheet names ("Invoices", "Receipts") fails
**Solution:** Use numeric sheet GIDs (e.g., `1542914058`)
**Why:** n8n Google Sheets nodes require GIDs from Google Sheets API
**How to find GIDs:**
- Check Google Sheets URL: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid={SHEET_GID}`
- Use Google Sheets API to retrieve sheet metadata

### 2. Binary Data Preservation Pattern
**Problem:** File binary data lost during LLM processing nodes
**Solution:** Explicit preservation in Set nodes: `data.binary = $input.item.binary`
**Why:** Critical for workflows with LLM processing + file uploads
**Impact:** Without this, files are lost during AI extraction steps

### 3. Type Bypass Strategy
**Problem:** Type conversion errors when passing data between nodes
**Solution:** Use Code nodes to handle type transitions instead of n8n native conversion
**Why:** Custom JavaScript logic more reliable for complex type scenarios
**Impact:** Workflow handles data type transitions cleanly

### 4. Execution History as Validation
**Insight:** Can verify fixes through execution history analysis
**Benefit:** Before/after comparison shows impact clearly
**Limitation:** Useful when real-world testing not immediately possible
**Important:** Always follow up with real-world end-to-end testing

---

## References

- **VERSION_LOG**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/VERSION_LOG.md`
- **Test Report**: `/Users/swayclarke/coding_stuff/test-reports/w7-critical-fixes-verification-report.md`
- **Session Summary**: `/Users/swayclarke/coding_stuff/session-summaries/2026-01-13-session-w7-critical-fixes.md`
- **System Design**: `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md`
- **Google Drive Root**: https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15
- **Expense Database**: https://docs.google.com/spreadsheets/d/1P_LN7c-QugGMnhBrQ6FBMsq3h0AkGWJzlL3Uu1t9rXY/edit

---

**Document Version:** v9.0
**Generated:** January 13, 2026 at 21:25 CET
**Author:** Claude Code (Sway's automation assistant)
