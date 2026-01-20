# Expense System Session Summary v5.0

**Date:** January 6, 2026
**Session Focus:** Architecture Redesign for Monthly Accountant Handoff
**Status:** Planning Phase - Ready for Implementation

---

## Summary of Changes from v4.0

### Architecture Evolution

**Previous Plan (v4.0):**
- W4 would create 12 months of folders upfront
- Organization by: `Receipts/{year}/{month}/{vendor}/`
- Receipts sourced only from Gmail

**New Plan (v5.0):**
- **Monthly folder creation** (dynamic, on-demand at month-end)
- **New folder structure:** `VAT {Month} {Year}/{Bank}/{Statements|Receipts}/`
- **Multi-source receipt collection:** Gmail + Google Drive + Mac Downloads folder
- **OCR support** for photos and scanned receipts (via Anthropic API)
- **Income folder** for invoices and payment confirmations

### Key Business Driver

**Problem:** Sway needs to hand off a complete, organized folder to his accountant at the end of every month.

**Solution:** A single folder (e.g., "VAT September 2025") containing all bank statements and receipts organized by bank, ready to send.

---

## Google Drive Folder Structure

### Folder IDs Reference

| Folder | ID | Purpose |
|--------|----|---------|
| **Inbox** | `1iY6SL4SmIaPHwY4Ps45BhAvuJq-dG5w5` | Manually downloaded statements + special documents |
| **expense_system** | `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15` | Base folder for monthly VAT folders |
| **Invoices** | `1_zVNS3JHS15pUjvfEJMh9nzYWn6TltbS` | Outgoing invoices (VO/invoices) |

### Monthly Folder Structure (Created Dynamically)

**Created by W4 at month-end:**

```
expense_system/
└── VAT September 2025/
    ├── ING Diba/
    │   ├── Statements/
    │   │   └── [bank statement PDF]
    │   └── Receipts/
    │       └── [all receipts for ING transactions]
    ├── Deutsche Bank/
    │   ├── Statements/
    │   └── Receipts/
    ├── Barclays/
    │   ├── Statements/
    │   └── Receipts/
    ├── Mastercard/
    │   ├── Statements/
    │   └── Receipts/
    └── Income/
        ├── [outgoing invoices from VO/invoices]
        └── [payment confirmations from Gmail/Drive]
```

**Banks:** 4 total
1. ING Diba
2. Deutsche Bank
3. Barclays
4. Mastercard (includes Miles-More)

---

## Revised Workflow Architecture

### W1: Statement Intake & Parsing ✅

**Status:** Working (per v4.0)
**Workflow ID:** `MPjDdVMI88158iFW`

**Input:**
- Sway manually downloads bank statements → uploads to **Inbox** folder (`1iY6SL4SmIaPHwY4Ps45BhAvuJq-dG5w5`)

**Process:**
1. Watch Inbox folder for new PDFs
2. Parse PDF via Anthropic API (Claude Sonnet 4.5)
3. Extract transactions: Date, Bank, Amount, Currency, Description, Vendor

**Output:**
- Transactions written to **Transactions** sheet
- Statement metadata written to **Statements** sheet

**Current Issues:**
- ⚠️ Statements sheet is currently empty
- Minor archival issue (not critical)

---

### W2 v2.0: Multi-Source Receipt Collection 🔧

**Status:** Built but needs expansion
**Workflow ID:** `dHbwemg7hEB4vDmC`
**Last Updated:** Jan 5, 2026 (20 hours ago)

**Current Capabilities:**
- ✅ Gmail attachment scanning
- ✅ Receipt download to Google Drive
- ✅ Amount/Currency extraction
- ✅ Metadata logging to Receipts sheet

**Needs Expansion:**

**Input Sources (3 total):**
1. **Gmail attachments** ✅ (working)
2. **Google Drive folders** ❌ (not implemented)
   - Downloads folder (synced from Mac via Google Drive Desktop)
   - Any other designated folders
3. **Inbox folder** ❌ (not implemented)
   - Manual uploads by Sway

**Receipt Types:**
- Digital PDFs ✅ (working)
- **Photos** ❌ (needs OCR via Anthropic API)
- **Scanned PDFs** ❌ (needs OCR via Anthropic API)

**Output:**
- All receipts logged in **Receipts** sheet
- Fields: ReceiptID, Source, Vendor, Date, Amount, Currency, FileID, FilePath, ProcessedDate, Matched, transaction_id

**Schema Changes Since v4.0:**
- ✅ Added: Amount, Currency, FilePath, ProcessedDate, Source
- ❌ Removed: FileName, DownloadDate, SourceEmail, Notes

---

### W3: Transaction-Receipt Matching ⚠️

**Status:** Built but has wrong organization logic
**Workflow ID:** `waPA94G2GXawDlCa`
**Last Updated:** Jan 3, 2026

**Process:**
1. Get unmatched transactions from Transactions sheet
2. Get unmatched receipts from Receipts sheet
3. Fuzzy matching algorithm:
   - Vendor similarity (Levenshtein distance)
   - Amount tolerance (±€0.50)
   - Date tolerance (±3 days)
4. Update both sheets with match status and confidence
5. ⚠️ **INCORRECT:** Tries to organize receipts into old folder structure

**Current Organization Logic (WRONG):**
```javascript
// W3 currently tries to create this structure:
const folderPath = `${year}/${month}-${monthName}/${bankFolder}/Receipts`;
// Example: "2025/09-September/ING/Receipts"
```

**Problem:**
- This is NOT the new "VAT {Month} {Year}" structure
- Hardcoded to move files to `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15` (empty folder)
- Will fail because folder structure doesn't exist

**Fix Needed:**
- **Option A:** Disable organization nodes in W3, let W4 handle it
- **Option B:** Update W3 to use new structure (but W4 should own this)

**Recommendation:** Disable W3's organization logic. W4 v2.0 should be the single source of truth for file organization.

---

### W4 v2.0: Monthly Folder Builder & Organizer ❌

**Status:** NOT BUILT (stub only)
**Workflow ID:** `nASL6hxNQGrNBTV4`

**This is the CRITICAL missing piece.**

**Trigger:** Manual (Sway runs at month-end)

**Process Flow (Proposed):**

```
1. Manual Trigger (Sway clicks "Execute")
   ↓
2. Prompt for Month/Year (e.g., "September 2025")
   ↓
3. Create Monthly Folder Structure
   - Create "VAT {Month} {Year}" folder
   - Create 4 bank subfolders (ING, Deutsche, Barclays, Mastercard)
   - Create Statements + Receipts subfolders for each bank
   - Create Income folder
   ↓
4. Read Statements Sheet (filter by Month/Year)
   ↓
5. Read Receipts Sheet (Matched=TRUE only, filter by Month/Year)
   ↓
6. Read Transactions Sheet (for bank lookup)
   ↓
7. Organize Statements
   - Move each statement PDF to: VAT {Month}/{Bank}/Statements/
   - Update Statements sheet FilePath column
   ↓
8. Organize Receipts
   - Lookup transaction_id → get Bank
   - Move receipt to: VAT {Month}/{Bank}/Receipts/
   - Update Receipts sheet FilePath column
   ↓
9. Organize Income Documents
   - Copy outgoing invoices from VO/invoices folder (1_zVNS3JHS15pUjvfEJMh9nzYWn6TltbS)
   - Move payment confirmations from Gmail/Drive
   - Place all in: VAT {Month}/Income/
   ↓
10. Generate Summary Report
   - Count: Statements organized, Receipts organized, Unmatched receipts skipped
   - Log any errors or warnings
```

**Nodes Estimate:** 15-18 nodes

**Critical Design Decisions:**

1. **Month/Year Input:** Manual prompt at start (prevents accidental runs)
2. **Folder Creation:** Dynamic, not all 12 months upfront
3. **Receipt-to-Bank Matching:** Uses W3's transaction_id linkage
4. **Unmatched Receipts:** Skipped (stays in original location)
5. **Income Folder:** Copies invoices (doesn't move originals)

---

## Google Sheets Structure

**Spreadsheet ID:** `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`

### Transactions Sheet

**Columns:** TransactionID, Date, Bank, Amount, Currency, Description, Vendor, Category, ReceiptID, StatementID, MatchStatus, MatchConfidence, Notes, Tags, Type, AnnualInvoiceID

**Current Data:**
- 5 transactions from ING, September 2025
- All currently "unmatched"

**Populated by:** W1 (PDF parsing)

---

### Receipts Sheet

**Columns (NEW SCHEMA):**
- ReceiptID
- **Source** (gmail, drive, inbox)
- Vendor
- Date
- **Amount** (NEW)
- **Currency** (NEW)
- FileID
- **FilePath** (NEW)
- **ProcessedDate** (NEW)
- Matched (TRUE/FALSE)
- **transaction_id** (links to Transactions sheet)

**Current Data:**
- 3 test receipts
- All Matched = FALSE
- All transaction_id = empty

**Populated by:** W2 (receipt collection)

---

### Statements Sheet

**Columns:** StatementID, Bank, Month, Year, FileID, FilePath, ProcessedDate, TransactionCount

**Current Data:**
- ⚠️ **EMPTY** - No statements logged yet

**Populated by:** W1 (when statements are parsed)

---

## Receipt Collection Strategy

### Source 1: Gmail Attachments ✅
**Status:** Working (W2 v2.0)
**Search Pattern:** Vendor email patterns (configured in W2)
**File Types:** PDF attachments

### Source 2: Google Drive Sync 🔧
**Status:** Needs implementation
**Setup:**
1. Install **Google Drive Desktop** app on Sway's Mac
2. Configure sync: `~/Downloads` → Google Drive folder (e.g., `Downloads-Sync/`)
3. W2 scans this folder for new receipts
4. Move processed files to archive subfolder

**Recommended Folder Structure:**
```
My Drive/
└── Expense-Downloads-Sync/
    ├── New/          ← W2 scans this folder
    └── Processed/    ← W2 moves files here after logging
```

### Source 3: Inbox Folder 🔧
**Status:** Needs implementation
**Folder ID:** `1iY6SL4SmIaPHwY4Ps45BhAvuJq-dG5w5`
**Use Case:** Special documents that Sway manually downloads and uploads

---

## OCR Implementation

### Use Case
- Photos of receipts (from phone camera)
- Scanned PDFs without text layer
- Physical receipts captured via scanner

### Technology Choice: Anthropic API (Claude Sonnet 4.5)

**Why Anthropic over AWS Textract:**
- ✅ Already using Anthropic API in W1 (same credentials)
- ✅ Same code patterns (minimal new code)
- ✅ Supports both documents AND images
- ✅ Cost: ~$0.001 per image (negligible)

**Implementation:**
- Detect if file is image (JPEG, PNG, HEIC) or scanned PDF
- Send to Anthropic with prompt: "Extract vendor, date, amount, currency from this receipt"
- Parse JSON response
- Continue normal W2 flow

**File Types Supported:**
- PDF (with text) → Direct text extraction
- PDF (scanned) → OCR via Anthropic
- JPEG/PNG/HEIC → OCR via Anthropic

---

## Income Folder Logic

### Outgoing Invoices

**Source:** VO/invoices folder (`1_zVNS3JHS15pUjvfEJMh9nzYWn6TltbS`)

**W4 Logic:**
1. Filter invoices by month/year (from filename or creation date)
2. **Copy** (don't move) to `VAT {Month} {Year}/Income/`
3. Preserve originals in VO/invoices

### Payment Confirmations (Incoming)

**Sources:**
- Gmail attachments (payment receipts from clients)
- Downloads folder (bank transfer confirmations)

**W2 Logic:**
- Tag receipt as "income" if:
  - Vendor matches known clients, OR
  - Amount is positive (credit/deposit), OR
  - Keywords: "payment received", "invoice paid", etc.
- Store in Receipts sheet with Type = "income"

**W4 Logic:**
- Filter Receipts sheet for Type = "income"
- Move to `VAT {Month} {Year}/Income/`

---

## Current System Status

### ✅ Working
1. **W1 (PDF Intake & Parsing)** - Extracts transactions from bank statements

### 🔧 Partially Working (Needs Updates)
2. **W2 v2.0 (Gmail Receipt Monitor)** - Works for Gmail, needs expansion for Drive/Inbox + OCR
3. **W3 (Transaction Matching)** - Matching logic works, organization logic is WRONG

### ❌ Not Built
4. **W4 v2.0 (Monthly Folder Builder)** - Complete redesign needed

---

## Implementation Plan

### Phase 1: Fix W3 Organization Logic (1 hour)
**Goal:** Stop W3 from breaking when it tries to organize files

**Tasks:**
1. Disable "Determine Target Folder" node in W3
2. Disable "Move Receipt to Organized Folder" node in W3
3. Test W3 matching-only (without organization)

**Agent:** Main conversation (simple node disabling)

---

### Phase 2: Expand W2 for Multi-Source Collection (4-6 hours)
**Goal:** Collect receipts from Gmail + Google Drive + Inbox

**Tasks:**
1. Add Google Drive folder scanning (Downloads-Sync/New/)
2. Add Inbox folder scanning (`1iY6SL4SmIaPHwY4Ps45BhAvuJq-dG5w5`)
3. Implement OCR for images/scanned PDFs (Anthropic API)
4. Add "income" tagging logic
5. Test with sample files

**Agent:** solution-builder-agent (4+ node additions)

---

### Phase 3: Build W4 v2.0 Monthly Folder Builder (8-12 hours)
**Goal:** Create complete monthly folder organization system

**Tasks:**
1. Manual trigger with Month/Year prompt
2. Dynamic folder structure creation (VAT folders + subfolders)
3. Statement organization logic
4. Receipt organization logic (via transaction_id → bank lookup)
5. Income folder logic (copy invoices + move payment confirmations)
6. FilePath column updates in Sheets
7. Summary report generation
8. Error handling (missing folders, failed moves, etc.)

**Agent:** solution-builder-agent (15-18 nodes)

---

### Phase 4: Google Drive Desktop Setup (15 minutes)
**Goal:** Sync Mac Downloads folder to Google Drive

**Tasks:**
1. Install Google Drive Desktop app on Sway's Mac
2. Create `Expense-Downloads-Sync/` folder in Google Drive
3. Configure selective sync: `~/Downloads` → `Expense-Downloads-Sync/New/`
4. Test: Drop a receipt in Downloads, verify it appears in Drive

**Agent:** None (manual setup by Sway)

---

### Phase 5: End-to-End Testing (3-4 hours)
**Goal:** Validate entire system with real data

**Test Scenarios:**
1. **Statement Processing:**
   - Upload Sept 2025 statement to Inbox
   - Verify W1 extracts transactions
   - Verify Transactions + Statements sheets populated

2. **Receipt Collection:**
   - Place 3 receipts in Downloads folder (PDF, JPEG, scanned PDF)
   - Verify W2 finds them, extracts data, logs to Receipts sheet
   - Verify OCR works on photo receipts

3. **Transaction Matching:**
   - Run W3
   - Verify receipts matched to transactions
   - Verify transaction_id populated in Receipts sheet

4. **Monthly Organization:**
   - Run W4 for "September 2025"
   - Verify "VAT September 2025" folder created
   - Verify all bank subfolders created
   - Verify statements moved to correct folders
   - Verify receipts moved to correct folders
   - Verify Income folder populated
   - Verify FilePath columns updated

5. **Edge Cases:**
   - Unmatched receipts (verify they're skipped)
   - Missing data (verify error handling)
   - Duplicate files (verify handling)

**Agent:** test-runner-agent

---

### Phase 6: Documentation & Handoff (1 hour)
**Goal:** Document final state for future reference

**Tasks:**
1. Update VERSION_LOG.md with all folder IDs
2. Create user guide for Sway (how to run monthly process)
3. Archive old blueprints (W4 v1.x)
4. Save new W4 v2.0 blueprint

**Agent:** Main conversation

---

## Total Estimated Effort

| Phase | Hours | Calendar Time |
|-------|-------|---------------|
| Phase 1: Fix W3 | 1 | 0.25 days |
| Phase 2: Expand W2 | 4-6 | 1-1.5 days |
| Phase 3: Build W4 v2.0 | 8-12 | 2-3 days |
| Phase 4: Drive Setup | 0.25 | 0 days (Sway) |
| Phase 5: Testing | 3-4 | 1 day |
| Phase 6: Documentation | 1 | 0.25 days |
| **TOTAL** | **17-24 hours** | **5-7 days** |

**At 4 hours/day:** 5-7 calendar days
**Classification:** Small-to-Medium Project

---

## Success Criteria

### For W1 (Already Working)
- ✅ Statements parsed by Anthropic API
- ✅ Transactions extracted to Sheets
- ⚠️ Statements sheet needs to be populated (currently empty)

### For W2 v2.0
- [ ] Receipts collected from Gmail ✅ (already working)
- [ ] Receipts collected from Google Drive sync folder
- [ ] Receipts collected from Inbox folder
- [ ] OCR extracts data from photos and scanned PDFs
- [ ] Income receipts tagged correctly
- [ ] All receipts logged to Receipts sheet with Amount/Currency

### For W3
- [ ] Organization logic disabled (or removed)
- [ ] Matching logic works correctly
- [ ] transaction_id populated in Receipts sheet
- [ ] MatchStatus and MatchConfidence accurate

### For W4 v2.0
- [ ] Manual trigger prompts for Month/Year
- [ ] "VAT {Month} {Year}" folder created dynamically
- [ ] All 4 bank subfolders created (ING, Deutsche, Barclays, Mastercard)
- [ ] Statements + Receipts subfolders created for each bank
- [ ] Income folder created
- [ ] All statements moved to correct bank Statement folders
- [ ] All matched receipts moved to correct bank Receipt folders
- [ ] Outgoing invoices copied to Income folder
- [ ] Payment confirmations moved to Income folder
- [ ] FilePath columns updated in Statements and Receipts sheets
- [ ] Unmatched receipts skipped gracefully
- [ ] Summary report shows counts and any errors
- [ ] **Month-end:** Sway can share single "VAT September 2025" folder with accountant

---

## Open Questions & Next Steps

### Immediate Questions for Sway
1. ✅ Downloads folder approach → **Answered: Option B (Google Drive sync)**
2. ✅ OCR implementation → **Answered: Use Anthropic API (like AMA workflows)**
3. ✅ VO/invoices location → **Answered: Folder ID provided**
4. ✅ Statement inbox → **Answered: Use existing Inbox folder**

### Immediate Actions
1. **Fix W3 organization logic** (Phase 1) - Should I proceed?
2. **Set up Google Drive Desktop** (Phase 4) - Sway needs to do this
3. **Build W4 v2.0** (Phase 3) - Biggest task, use solution-builder-agent

---

## Technical Environment

- **n8n Version:** 2.1.4 Self Hosted (Digital Ocean)
- **Binary Mode:** filesystem-v2
- **Anthropic Model:** claude-sonnet-4-5
- **Google Sheets:** 1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM

---

## Critical Files & Folders

### Google Drive
- **Inbox:** 1iY6SL4SmIaPHwY4Ps45BhAvuJq-dG5w5
- **expense_system:** 1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15
- **VO/invoices:** 1_zVNS3JHS15pUjvfEJMh9nzYWn6TltbS

### n8n Workflows
- **W1:** MPjDdVMI88158iFW (working)
- **W2:** dHbwemg7hEB4vDmC (needs expansion)
- **W3:** waPA94G2GXawDlCa (needs organization fix)
- **W4:** nASL6hxNQGrNBTV4 (stub, needs rebuild)

---

## Resume Instructions

**To continue this work in a new chat:**

1. Reference this summary: `summary_v5.0_2026-01-06.md`
2. Start with: "Continue from summary v5.0, beginning with [Phase #]"
3. Key decision: Architecture redesigned for monthly accountant handoff
4. Next step: Fix W3 organization logic (Phase 1)

---

**End of Summary v5.0**
