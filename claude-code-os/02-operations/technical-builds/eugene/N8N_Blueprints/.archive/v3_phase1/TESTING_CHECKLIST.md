> ⚠️ **SUPERSEDED BY V4** - This document is for reference only.
> For the latest testing checklist, the V4 workflow has been thoroughly tested.
> See: `../v4_phase1/WORKFLOW_V4_SUMMARY.md` for V4 details.

---

# Document Organizer V3.5 Phase 1 - Testing Checklist

**Version:** 3.5 (Phase 1 with Project Tracking)
**Status:** SUPERSEDED - Use V4
**Created:** 2025-12-21
**Last Updated:** 2025-12-22
**For:** Eugene

---

## Overview

This checklist guides you through testing each component of the Document Organizer workflow. Complete each section in order before moving to the next.

**Testing Philosophy:** Test small, fix fast, build confidence.

**V3.5 New Tests:**
- Chunk 0: Folder Initialization (one-time setup)
- Chunk 2.5: Project Tracking across email batches
- Timestamp verification in filenames (HH:MM:SS)
- Project completion status tracking (2/4, 3/4, 4/4)
- Enhanced email notifications with project status

---

## Pre-Testing Setup

### Documents to Prepare

Collect these 8 test documents before starting:

| # | Document Type | Description | Source |
|---|---------------|-------------|--------|
| 1 | Exposé | Property description/teaser | Any project |
| 2 | Grundbuch | Land register extract | Any property |
| 3 | DIN 276 Calculation | Cost breakdown spreadsheet | Any project |
| 4 | Exit Strategy | Liquidation/exit plan | Any project |
| 5 | Other (identifiable) | Baugenehmigung OR BWA OR Kaufvertrag | Any |
| 6 | Unknown (unclear) | Poor scan OR foreign language doc | Test file |
| 7 | ZIP archive | ZIP containing 2-3 PDFs | Create test |
| 8 | Scanned PDF | Image-based PDF (not digital) | Scan a doc |

### Create Gmail Test Label

1. Open Gmail
2. Create label: `Bautraeger_Docs_TEST`
3. Update workflow to use test label during testing
4. Switch back to `Bautraeger_Docs` when going live

---

## Chunk 0: Folder Initialization (One-Time Setup)

**IMPORTANT:** Test Chunk 0 FIRST before all other chunks. This is a one-time setup that creates all folders.

### Test 0.1: Initial Folder Creation

**Action:**
1. Import `chunk0_folder_initialization.json`
2. Configure Google Drive and Gmail credentials
3. Execute workflow manually (click "Execute Workflow" button)

**Expected Results:**
- [ ] Workflow executes successfully
- [ ] Root folder `Bautraeger_Documents` created in Google Drive
- [ ] 4 parent folders created (OBJEKTUNTERLAGEN, WIRTSCHAFTLICHE, RECHTLICHE, SONSTIGES)
- [ ] All 37 subfolders created under parent folders
- [ ] `_Staging` folder created
- [ ] Confirmation email received with folder IDs

**Google Drive Structure:**
```
Bautraeger_Documents/
├── OBJEKTUNTERLAGEN/
│   ├── 01_Projektbeschreibung/
│   ├── 02_Kaufvertrag/
│   ├── 03_Grundbuchauszug/
│   └── ... (22 total)
├── WIRTSCHAFTLICHE/
│   └── ... (6 folders)
├── RECHTLICHE/
│   └── ... (6 folders)
├── SONSTIGES/
│   ├── 36_Exit_Strategie/
│   ├── 37_Others/
│   └── 38_Unknowns/
└── _Staging/
```

**Folder Count Verification:**
- [ ] 1 root folder
- [ ] 4 parent folders
- [ ] 37 subfolders
- [ ] 1 staging folder
- [ ] **Total: 43 folders**

**Pass/Fail:** ___________

### Test 0.2: Variable Auto-Setting

**Action:**
1. After Chunk 0 execution, go to Settings → Variables
2. Verify all folder ID variables are set

**Expected Results:**
- [ ] `STAGING_FOLDER_ID` variable set
- [ ] `FOLDER_01_PROJEKTBESCHREIBUNG` variable set
- [ ] `FOLDER_03_GRUNDBUCHAUSZUG` variable set
- [ ] `FOLDER_10_BAUTRAEGERKALKULATION_DIN276` variable set
- [ ] `FOLDER_36_EXIT_STRATEGIE` variable set
- [ ] `FOLDER_37_OTHERS` variable set
- [ ] `FOLDER_38_UNKNOWNS` variable set
- [ ] All other folder variables (31 more) set

**Sample Variable Value (should be Drive folder ID):**
```
FOLDER_01_PROJEKTBESCHREIBUNG = ________________________
```

**Pass/Fail:** ___________

### Test 0.3: Idempotent Re-Run

**Action:**
1. Execute Chunk 0 workflow AGAIN (second time)
2. Check execution log

**Expected Results:**
- [ ] Workflow executes without errors
- [ ] No duplicate folders created
- [ ] Existing folders detected and IDs reused
- [ ] Variables updated with same IDs
- [ ] Confirmation email shows "Folders already exist, reusing IDs"

**Pass/Fail:** ___________

### Test 0.4: Deactivate Chunk 0

**Action:**
1. After successful execution, deactivate Chunk 0 workflow
2. Verify it won't run automatically

**Expected Results:**
- [ ] Workflow toggle set to "Inactive"
- [ ] Workflow won't execute on schedule
- [ ] Can still be run manually if needed later

**Pass/Fail:** ___________

---

## Chunk 1: Email → Staging

### Test 1.1: Single PDF Email

**Action:**
1. Send email to yourself with single PDF attached
2. Apply label `Bautraeger_Docs_TEST`
3. Wait 1-2 minutes for trigger

**Expected Results:**
- [ ] Workflow triggers automatically
- [ ] Attachment downloaded
- [ ] File uploaded to Staging folder
- [ ] Original filename preserved in metadata

**Pass/Fail:** ___________

### Test 1.2: Multiple Attachments

**Action:**
1. Send email with 3 PDFs attached
2. Apply label

**Expected Results:**
- [ ] All 3 files processed
- [ ] Each file uploaded separately
- [ ] No files missed

**Pass/Fail:** ___________

### Test 1.3: ZIP File Extraction

**Action:**
1. Create ZIP with 2 PDFs inside
2. Send email with ZIP attached
3. Apply label

**Expected Results:**
- [ ] ZIP detected by IF node
- [ ] Contents extracted
- [ ] Both PDFs uploaded to Staging
- [ ] Original ZIP filename logged

**Pass/Fail:** ___________

### Test 1.4: Mixed File Types

**Action:**
1. Send email with: PDF + DOCX + JPG + XLSX
2. Apply label

**Expected Results:**
- [ ] PDF processed
- [ ] DOCX processed
- [ ] JPG filtered out (not processed)
- [ ] XLSX filtered out (not processed)

**Pass/Fail:** ___________

### Test 1.5: No Attachments

**Action:**
1. Send email with no attachments
2. Apply label

**Expected Results:**
- [ ] Workflow triggers
- [ ] Gracefully handles empty attachment list
- [ ] No errors thrown

**Pass/Fail:** ___________

---

## Chunk 2: Text Extraction + OCR

### Test 2.1: Digital PDF Text Extraction

**Action:**
1. Use a digitally-created PDF (not scanned)
2. Run workflow

**Expected Results:**
- [ ] "Detect Scan vs Digital" identifies as digital
- [ ] Routes to "Extract Text (Digital PDF)" node
- [ ] Text extracted successfully
- [ ] German characters preserved (ä, ö, ü, ß)

**Extracted Text Sample (first 100 chars):**
```
________________________________________
________________________________________
```

**Pass/Fail:** ___________

### Test 2.2: Scanned PDF OCR

**Action:**
1. Use a scanned/image-based PDF
2. Run workflow

**Expected Results:**
- [ ] "Detect Scan vs Digital" identifies as scanned
- [ ] Routes to "AWS Textract OCR (German)"
- [ ] OCR returns text
- [ ] German text recognized correctly

**OCR Output Sample:**
```
________________________________________
________________________________________
```

**Pass/Fail:** ___________

### Test 2.3: Poor Quality Scan

**Action:**
1. Use a low-quality or partially illegible scan
2. Run workflow

**Expected Results:**
- [ ] OCR attempts extraction
- [ ] textQuality marked as "partial" or "poor"
- [ ] Workflow continues (doesn't crash)

**Pass/Fail:** ___________

### Test 2.4: DOCX File

**Action:**
1. Send email with Word document attached
2. Run workflow

**Expected Results:**
- [ ] File detected as DOCX
- [ ] needsOCR set to false
- [ ] Text extracted from DOCX
- [ ] Continues to AI classification

**Pass/Fail:** ___________

---

## Chunk 2.5: Project Tracking (NEW IN V3.5)

**Purpose:** Test AI extraction of project names and project completion tracking across multiple email batches.

### Test 2.5.1: Project Name Extraction

**Action:**
1. Process an Exposé document that clearly mentions a property name
2. Check "Extract Project Name" node output

**Expected Results:**
- [ ] OpenAI API called successfully
- [ ] Project/property name extracted from document text
- [ ] Example: "Müller Apartment Building" or "Schmidt Office Complex"
- [ ] If unclear, defaults to "Unknown Project"

**Extracted Project Name:** ___________

**Pass/Fail:** ___________

### Test 2.5.2: New Project Creation in Tracker

**Action:**
1. Process first document for a new project (e.g., Exposé for "Test Project Alpha")
2. Check Project Tracker Google Sheet

**Expected Results:**
- [ ] New row created in Project Tracker sheet
- [ ] Project name: "Test Project Alpha"
- [ ] Exposé checkbox: ✓ (checked)
- [ ] Other checkboxes: unchecked
- [ ] Total Complete: 1
- [ ] Status: "IN PROGRESS (1/4)"
- [ ] Last Updated: today's date

**Pass/Fail:** ___________

### Test 2.5.3: Same Project Update (2nd Document)

**Action:**
1. Process second document for same project (e.g., Grundbuch for "Test Project Alpha")
2. Check Project Tracker sheet again

**Expected Results:**
- [ ] SAME row updated (not new row created)
- [ ] Project name: "Test Project Alpha" (unchanged)
- [ ] Exposé checkbox: ✓ (still checked)
- [ ] Grundbuch checkbox: ✓ (now checked)
- [ ] Total Complete: 2
- [ ] Status: "IN PROGRESS (2/4)"
- [ ] Last Updated: updated to current time

**Pass/Fail:** ___________

### Test 2.5.4: Project Completion (4th Document)

**Action:**
1. Process third and fourth documents for same project (Calculation + Exit Strategy for "Test Project Alpha")
2. Check Project Tracker sheet after both

**Expected Results:**
- [ ] All 4 checkboxes: ✓
- [ ] Total Complete: 4
- [ ] Status: "COMPLETE"
- [ ] Email notification shows "🎉 ALL PRIORITY DOCUMENTS COMPLETE!"

**Pass/Fail:** ___________

### Test 2.5.5: Multiple Projects Simultaneously

**Action:**
1. Process 1 doc from Project A (Exposé)
2. Process 1 doc from Project B (Grundbuch)
3. Process another doc from Project A (Calculation)
4. Check Project Tracker sheet

**Expected Results:**
- [ ] Two separate rows in tracker (Project A, Project B)
- [ ] Project A: 2/4 complete (Exposé + Calculation)
- [ ] Project B: 1/4 complete (Grundbuch)
- [ ] Each project tracked independently
- [ ] No cross-contamination

**Pass/Fail:** ___________

### Test 2.5.6: Unknown Project Handling

**Action:**
1. Process a document where project name cannot be extracted
2. Check Project Tracker sheet

**Expected Results:**
- [ ] Row created with project name: "Unknown Project"
- [ ] Document type checkbox still marked
- [ ] Status tracked correctly
- [ ] Can be manually renamed later in sheet

**Pass/Fail:** ___________

---

## Chunk 3: AI Classification

### Test 3.1: Exposé Classification

**Action:**
1. Process an Exposé/Projektbeschreibung document
2. Check AI output

**Expected Results:**
- [ ] Level 1 AI returns: `OBJEKTUNTERLAGEN`
- [ ] Level 2 AI returns: `expose`
- [ ] Routed to "Set Expose Filename"
- [ ] Filename prefix: `EXPOSE_`
- [ ] **V3.5:** Filename includes timestamp: `EXPOSE_Eugene_20251222_143052.pdf` (HH:MM:SS format)
- [ ] Target folder: `01_Projektbeschreibung`

**AI Confidence:** ___________

**Filename Generated:** ___________

**Pass/Fail:** ___________

### Test 3.2: Grundbuch Classification

**Action:**
1. Process a Grundbuchauszug document
2. Check AI output

**Expected Results:**
- [ ] Level 1 AI returns: `OBJEKTUNTERLAGEN`
- [ ] Level 2 AI returns: `grundbuch`
- [ ] Routed to "Set Grundbuch Filename"
- [ ] Filename prefix: `GRUNDBUCH_`
- [ ] Target folder: `03_Grundbuchauszug`

**Pass/Fail:** ___________

### Test 3.3: DIN 276 Calculation Classification

**Action:**
1. Process a Bauträgerkalkulation DIN 276 document
2. Check AI output

**Expected Results:**
- [ ] Level 1 AI returns: `OBJEKTUNTERLAGEN`
- [ ] Level 2 AI returns: `calculation`
- [ ] Routed to "Set Calculation Filename"
- [ ] Filename prefix: `KALK276_`
- [ ] Target folder: `10_Bautraegerkalkulation_DIN276`

**Pass/Fail:** ___________

### Test 3.4: Exit Strategy Classification

**Action:**
1. Process an Exit-Strategie document
2. Check AI output

**Expected Results:**
- [ ] Level 1 AI returns: `SONSTIGES`
- [ ] Level 2 AI returns: `exitstrategie`
- [ ] Routed to "Set Exit Filename"
- [ ] Filename prefix: `EXIT_`
- [ ] Target folder: `36_Exit_Strategie`

**Pass/Fail:** ___________

### Test 3.5: Other Document (Should NOT go to specific folder)

**Action:**
1. Process a Baugenehmigung OR BWA document
2. Check AI output

**Expected Results:**
- [ ] Document identified (not unknown)
- [ ] BUT routed to "Set Others Filename"
- [ ] Filename prefix: `OTHERS_`
- [ ] Target folder: `37_Others` (NOT its specific folder)
- [ ] Original document type logged for Phase 2 training

**Pass/Fail:** ___________

### Test 3.6: Unknown Document

**Action:**
1. Process an illegible or foreign language document
2. Check AI output

**Expected Results:**
- [ ] AI cannot confidently classify
- [ ] Routed to "Set Unknown Filename"
- [ ] Filename prefix: `UNKNOWN_`
- [ ] Target folder: `38_Unknowns`

**Pass/Fail:** ___________

---

## Chunk 4: File Operations + Logging

### Test 4.1: File Move

**Action:**
1. Process an Exposé document end-to-end
2. Check Google Drive

**Expected Results:**
- [ ] File removed from Staging folder
- [ ] File appears in `01_Projektbeschreibung` folder
- [ ] No duplicate files
- [ ] File accessible (not corrupted)

**Pass/Fail:** ___________

### Test 4.2: File Rename (V3.5 with Timestamp)

**Action:**
1. Process a document
2. Check filename after processing

**Expected Results:**
- [ ] **V3.5:** Filename follows pattern: `{PREFIX}_{CLIENT}_{DATE}_{TIME}.{ext}`
- [ ] **V3.5:** Example: `EXPOSE_Eugene_20251222_143052.pdf`
- [ ] Date is today's date (YYYYMMDD format)
- [ ] **V3.5:** Time includes hours, minutes, seconds (HHmmss format)
- [ ] Extension preserved

**New Filename:** ___________

**Pass/Fail:** ___________

### Test 4.2.1: Timestamp Uniqueness (V3.5 NEW)

**Action:**
1. Process two identical documents in rapid succession (< 1 second apart)
2. Check both filenames

**Expected Results:**
- [ ] First file: `EXPOSE_Eugene_20251222_143052.pdf`
- [ ] Second file: `EXPOSE_Eugene_20251222_143053.pdf` (seconds differ)
- [ ] No filename collision in Google Drive
- [ ] Both files accessible

**Pass/Fail:** ___________

### Test 4.3: Log Entry Created

**Action:**
1. Process a document
2. Check Main Processing Log spreadsheet

**Expected Results:**
- [ ] New row added to sheet
- [ ] Timestamp accurate
- [ ] **V3.5:** Project name logged
- [ ] Original filename logged
- [ ] New filename logged (with timestamp)
- [ ] Document type logged
- [ ] Target folder logged
- [ ] Status shows "SUCCESS"

**Pass/Fail:** ___________

### Test 4.3.1: Project Tracker Updated (V3.5 NEW)

**Action:**
1. Process an Exposé document for a new project
2. Check Project Tracker Google Sheet

**Expected Results:**
- [ ] Row for project updated (or created)
- [ ] Exposé checkbox: ✓ (checked)
- [ ] Total Complete count incremented
- [ ] Status updated (e.g., "IN PROGRESS (1/4)" or "COMPLETE")
- [ ] Last Updated timestamp reflects current time

**Pass/Fail:** ___________

### Test 4.4: Eugene Email Notification (V3.5 Enhanced)

**Action:**
1. Process 3 documents from same project (e.g., Exposé, Grundbuch, Calculation)
2. Check Eugene's email

**Expected Results:**
- [ ] Email received within 1 minute
- [ ] **V3.5:** Subject includes project name and completion status
- [ ] **V3.5:** Example: `[Doc Organizer] Test Project Alpha - 3/4 documents complete`
- [ ] **V3.5:** Email body shows PROJECT STATUS section:
  - [ ] Project name
  - [ ] Completion: "3/4 Priority Documents"
  - [ ] Checkmarks for received documents (✓ Exposé, ✓ Grundbuch, ✓ Calculation)
  - [ ] Missing documents listed (✗ Exit Strategy)
- [ ] LATEST BATCH PROCESSED section with document details
- [ ] Link to Google Sheet included

**Email Subject Received:**
```
________________________________________
```

**Email Body Includes Project Status:** [ ] Yes [ ] No

**Pass/Fail:** ___________

### Test 4.5: Batch Processing

**Action:**
1. Send email with 5 PDFs attached
2. Process full batch

**Expected Results:**
- [ ] All 5 files processed
- [ ] Each file moved to correct folder
- [ ] 5 log entries created
- [ ] Single summary email sent (not 5 emails)

**Pass/Fail:** ___________

---

## Chunk 5: Error Handling

### Test 5.1: Simulated API Error

**Action:**
1. Temporarily invalidate OpenAI credential
2. Run workflow with a document
3. Restore credential after test

**Expected Results:**
- [ ] Error caught by Error Trigger
- [ ] Error logged to Error Sheet
- [ ] Error severity classified
- [ ] Alert email sent to Eugene
- [ ] Retry attempted (if configured)

**Error Logged:** ___________

**Pass/Fail:** ___________

### Test 5.2: Error Log Entry

**Action:**
1. After Test 5.1, check Error Log spreadsheet

**Expected Results:**
- [ ] New row created
- [ ] Error ID generated
- [ ] Error message captured
- [ ] Node name logged
- [ ] Severity classified (CRITICAL/HIGH/MEDIUM/LOW)
- [ ] Status shows "NEW"

**Pass/Fail:** ___________

### Test 5.3: Retry Logic

**Action:**
1. Simulate temporary network failure
2. Check retry behavior

**Expected Results:**
- [ ] First retry after ~5 seconds
- [ ] Second retry after ~15 seconds (if still failing)
- [ ] Third retry after ~45 seconds (if still failing)
- [ ] After 3 failures, marked as "FAILED"
- [ ] Failed alert sent

**Pass/Fail:** ___________

---

## End-to-End Full Test

### E2E Test: Complete Flow (V3.5)

**Action:**
1. Send single email with 1 Exposé PDF for a new project
2. Let entire workflow execute
3. Track document through all stages

**Checkpoints:**

| Stage | Timestamp | Status |
|-------|-----------|--------|
| Email received | _______ | [ ] Pass |
| Attachment downloaded | _______ | [ ] Pass |
| Uploaded to Staging | _______ | [ ] Pass |
| Text extracted | _______ | [ ] Pass |
| **V3.5:** Project name extracted | _______ | [ ] Pass |
| **V3.5:** Project Tracker row created | _______ | [ ] Pass |
| AI classified as Exposé | _______ | [ ] Pass |
| Moved to 01_Projektbeschreibung | _______ | [ ] Pass |
| **V3.5:** Renamed with timestamp (HH:MM:SS) | _______ | [ ] Pass |
| Log entry created with project name | _______ | [ ] Pass |
| **V3.5:** Project Tracker updated (1/4) | _______ | [ ] Pass |
| Email notification with project status | _______ | [ ] Pass |

**Total Time (email to complete):** _______ seconds

**Project Name Extracted:** ___________

**Pass/Fail:** ___________

---

## Phase 1 Sign-Off

### Summary (V3.5)

| Chunk | Tests | Passed | Failed |
|-------|-------|--------|--------|
| **0: Folder Initialization (NEW)** | **4** | ___ | ___ |
| 1: Email → Staging | 5 | ___ | ___ |
| 2: Text Extraction | 4 | ___ | ___ |
| **2.5: Project Tracking (NEW)** | **6** | ___ | ___ |
| 3: AI Classification | 6 | ___ | ___ |
| 4: File Ops + Logging | 7 | ___ | ___ |
| 5: Error Handling | 3 | ___ | ___ |
| End-to-End | 1 | ___ | ___ |
| **TOTAL** | **36** | ___ | ___ |

**V3.5 Test Additions:**
- Chunk 0: Folder initialization and idempotent re-run tests
- Chunk 2.5: Project name extraction and completion tracking tests
- Test 4.2.1: Timestamp uniqueness verification
- Test 4.3.1: Project Tracker update verification
- Enhanced E2E with project tracking checkpoints

### Issues Found

| Issue # | Description | Severity | Resolution |
|---------|-------------|----------|------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### Ready for Production?

- [ ] All critical tests passed
- [ ] All high-priority tests passed
- [ ] Known issues documented
- [ ] Eugene comfortable with Others/Unknowns manual sorting

**Approved by:** ___________
**Date:** ___________

---

## Post-Testing: Going Live

### Final Steps

1. [ ] Switch Gmail label from `Bautraeger_Docs_TEST` to `Bautraeger_Docs`
2. [ ] Activate workflow (toggle ON)
3. [ ] Monitor first 24 hours closely
4. [ ] Check Error Log daily for first week
5. [ ] Review Others/Unknowns folders for Phase 2 training data

### Success Metrics (First Week)

| Metric | Target | Actual |
|--------|--------|--------|
| Documents processed | 50+ | ___ |
| Accuracy (priority docs) | 90%+ | ___ |
| Errors | <5% | ___ |
| False positives in Unknowns | <10% | ___ |

---

*Document Organizer V3.5 Phase 1 - Testing Checklist*
*Created: 2025-12-21*
*Last Updated: 2025-12-22*
