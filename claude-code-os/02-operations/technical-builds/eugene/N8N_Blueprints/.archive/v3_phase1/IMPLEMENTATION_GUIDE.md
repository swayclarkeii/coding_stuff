> ⚠️ **SUPERSEDED BY V4** - This document is for reference only.
> For the latest implementation, see: `../v4_phase1/WORKFLOW_V4_SUMMARY.md`
> V4 includes critical fixes for fuzzy matching, sequential processing, and confidence scoring.

---

# Document Organizer V3.5 Phase 1 - Implementation Guide

**Version:** 3.5 (Phase 1 with Project Tracking)
**Status:** SUPERSEDED - Use V4
**Created:** 2025-12-21
**Total Nodes:** 52 (main workflow) + 26 (folder initialization) + 14 (error handling)
**Estimated Setup Time:** 3-4 hours

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Import Strategy](#2-import-strategy)
3. [Credential Setup](#3-credential-setup)
4. [Variable Configuration](#4-variable-configuration)
5. [Google Sheets Setup](#5-google-sheets-setup)
6. [Chunk-by-Chunk Import](#6-chunk-by-chunk-import)
7. [Testing Each Chunk](#7-testing-each-chunk)
8. [Troubleshooting](#8-troubleshooting)
9. [Go-Live Checklist](#9-go-live-checklist)

---

## 1. Prerequisites

### Required Accounts & Access

| Service | Required For | Setup Link |
|---------|--------------|------------|
| Google Workspace | Gmail, Drive, Sheets | Already configured |
| OpenAI API | Document classification | https://platform.openai.com/api-keys |
| AWS Account | Textract OCR | https://aws.amazon.com/textract/ |
| n8n Instance | Workflow automation | Self-hosted or n8n Cloud |

### Minimum n8n Version
- **Required:** n8n v1.20.0 or higher
- **Recommended:** Latest stable version

### API Rate Limits to Know
| Service | Limit | Impact |
|---------|-------|--------|
| Gmail API | 250 quota units/second | 1 email read = 5 units |
| Google Drive | 1000 requests/100 seconds | Move/rename = 1 request each |
| OpenAI GPT-4o-mini | 10,000 TPM | ~50 docs/minute capacity |
| AWS Textract | 1 sync request/second | OCR bottleneck for scans |

---

## 2. Import Strategy

### Recommended: Incremental Chunk Import

Build and test the workflow in stages:

```
Setup:    Chunk 0 (Folder Initialization) → One-time setup, creates all 37 folders
Day 1:    Chunk 1 (Email → Staging) → Test email ingestion + ZIP extraction
Day 2:    Chunk 2 (Text Extraction) + Chunk 2.5 (Project Tracking) → Test OCR + project extraction
Day 3:    Chunk 3 (AI Classification) → Test document routing with timestamps
Day 4:    Chunk 4 (File Ops + Project Update) → Test end-to-end flow + project status
Day 5:    Chunk 5 (Error Handling) → Test failure scenarios + retry logic
```

### Alternative: Full Import

If you prefer to import everything at once, use:
- `document_organizer_v3.5_complete.json`

**Warning:** Debugging 52 nodes at once is harder. Recommended only for experienced n8n users.

### V3.5 New Features in This Guide

- **Chunk 0:** Automated folder creation with existence checks (replaces manual setup)
- **Chunk 2.5:** AI-powered project tracking across email batches
- **Timestamp filenames:** HH:MM:SS added to prevent duplicate confusion
- **Enhanced notifications:** Email shows project completion status (2/4, 3/4, 4/4)

---

## 3. Credential Setup

### 3.1 Gmail OAuth2

1. Go to **Settings → Credentials → Add Credential**
2. Search for **Gmail OAuth2**
3. Click **Sign in with Google**
4. Select the Google account with access to Bauträger emails
5. Grant required permissions:
   - Read emails
   - Manage labels
   - Send emails (for notifications)
6. Save credential

**Credential Name:** `Gmail OAuth2`
**Used By:** Gmail Trigger, Email Eugene Summary

### 3.2 Google Drive OAuth2

1. **Settings → Credentials → Add Credential**
2. Search for **Google Drive OAuth2 API**
3. Sign in with the same Google account
4. Grant permissions:
   - View and manage all Drive files
5. Save credential

**Credential Name:** `Google Drive`
**Used By:** Upload to Staging, Move to Target Folder, Rename File

### 3.3 Google Sheets OAuth2

1. **Settings → Credentials → Add Credential**
2. Search for **Google Sheets OAuth2 API**
3. Sign in (same account)
4. Grant permissions for Sheets access
5. Save credential

**Credential Name:** `Google Sheets`
**Used By:** Log to Main Sheet, Log Error to Sheet, Update Error Status

### 3.4 OpenAI API

1. Go to https://platform.openai.com/api-keys
2. Create new API key
3. In n8n: **Settings → Credentials → Add Credential**
4. Search for **OpenAI**
5. Paste API key
6. Save credential

**Credential Name:** `OpenAI`
**Used By:** AI Level 1 Classification, AI Level 2 Classification, Project Name Extraction

**Cost Estimate (V3.5 with Project Tracking):**
- Model: gpt-4o-mini
- Cost per document: ~$0.006-0.012 (3 API calls: 2 classification + 1 project extraction)
- 100 documents/month: ~$1.15
- 500 documents/month: ~$6.00
- 1000 documents/month: ~$12.00

### 3.5 AWS Credentials (for Textract OCR)

1. Log into AWS Console
2. Go to IAM → Users → Add User
3. Create user `n8n-textract` with programmatic access
4. Attach policy: `AmazonTextractFullAccess`
5. Copy Access Key ID and Secret Access Key
6. In n8n: **Settings → Credentials → Add Credential**
7. Search for **AWS**
8. Enter:
   - Access Key ID
   - Secret Access Key
   - Region: `eu-central-1` (Frankfurt - GDPR compliant)
9. Save credential

**Credential Name:** `AWS`
**Used By:** AWS Textract OCR (German)

---

## 4. Variable Configuration

### Setting Up n8n Variables

Go to **Settings → Variables** and create:

### 4.1 Client Configuration

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `CLIENT_NAME` | `Eugene` | Client name for file prefixes |
| `EUGENE_EMAIL` | `eugene@example.com` | Notification email address |
| `AWS_REGION` | `eu-central-1` | AWS region for Textract |

### 4.2 Google Sheets IDs

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `MAIN_LOG_SHEET_ID` | `1abc...xyz` | Main processing log spreadsheet |
| `PROJECT_TRACKER_SHEET_ID` | `1ghi...jkl` | **NEW V3.5:** Project completion tracking sheet |
| `ERROR_LOG_SHEET_ID` | `1def...uvw` | Error tracking spreadsheet |

### 4.3 Folder IDs (Phase 1 Active Folders)

**NEW IN V3.5:** These variables are **automatically set by Chunk 0** (Folder Initialization workflow). You don't need to create these manually!

These 6 folders are actively used in Phase 1:

| Variable Name | Description | Auto-Created by Chunk 0 |
|---------------|-------------|------------------------|
| `STAGING_FOLDER_ID` | Incoming documents staging | ✅ Yes |
| `FOLDER_01_PROJEKTBESCHREIBUNG` | Exposé documents | ✅ Yes |
| `FOLDER_03_GRUNDBUCHAUSZUG` | Grundbuch documents | ✅ Yes |
| `FOLDER_10_BAUTRAEGERKALKULATION` | DIN 276 calculations | ✅ Yes |
| `FOLDER_36_EXIT_STRATEGIE` | Exit strategy documents | ✅ Yes |
| `FOLDER_37_OTHERS` | Other identifiable docs | ✅ Yes |
| `FOLDER_38_UNKNOWNS` | Unclassifiable docs | ✅ Yes |

### 4.4 Full Folder Variable List (All 37 for Phase 2)

Create all these variables now (even if not used in Phase 1):

```
FOLDER_01_PROJEKTBESCHREIBUNG
FOLDER_02_KAUFVERTRAG
FOLDER_03_GRUNDBUCHAUSZUG
FOLDER_04_EINTRAGUNGSBEWILLIGUNGEN
FOLDER_05_BODENRICHTWERT
FOLDER_06_BAULASTENVERZEICHNIS
FOLDER_07_ALTLASTENKATASTER
FOLDER_08_BAUGRUNDGUTACHTEN
FOLDER_09_LAGEPLAN
FOLDER_10_BAUTRAEGERKALKULATION
FOLDER_11_VERKAUFSPREISE
FOLDER_12_BAUZEITENPLAN
FOLDER_13_VERTRIEBSWEG
FOLDER_14_AUSSTATTUNGSBESCHREIBUNG
FOLDER_15_FLAECHENBERECHNUNG
FOLDER_16_GU_WERKVERTRAEGE
FOLDER_17_BAUZEICHNUNGEN
FOLDER_18_BAUGENEHMIGUNG
FOLDER_19_TEILUNGSERKLAERUNG
FOLDER_20_VERSICHERUNGEN
FOLDER_21_MUSTER_VERKAUFSVERTRAG
FOLDER_22_GUTACHTERAUFTRAG
FOLDER_23_JAHRESABSCHLUSS
FOLDER_24_BWA
FOLDER_25_STEUERNUMMER
FOLDER_26_SCHUFA
FOLDER_27_EINKOMMENSTEUERBESCHEID
FOLDER_28_VERMOEGENUEBERSICHT
FOLDER_29_HANDELSREGISTER
FOLDER_30_GESELLSCHAFTSVERTRAG
FOLDER_31_34C_GEWO
FOLDER_32_PERSONALAUSWEIS
FOLDER_33_KREDITZUSAGE
FOLDER_34_SICHERHEITEN
FOLDER_35_PROJEKTHISTORIE
FOLDER_36_EXIT_STRATEGIE
FOLDER_37_OTHERS
FOLDER_38_UNKNOWNS
```

---

## 5. Google Sheets Setup

### 5.1 Main Processing Log

1. Create new Google Spreadsheet
2. Name: `Document Organizer - Processing Log`
3. First sheet name: `Processing Log`
4. Add headers in Row 1:

| A | B | C | D | E | F | G | H | I | J | K | L | M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Timestamp | Date | Time | Original Filename | New Filename | Document Type | Category | Target Folder | Confidence | Client | File ID | Status | Error |

5. Copy the Spreadsheet ID from URL:
   `https://docs.google.com/spreadsheets/d/`**`1abc...xyz`**`/edit`
6. Set variable `MAIN_LOG_SHEET_ID` to this ID

### 5.2 Project Tracker Sheet (NEW IN V3.5)

**Purpose:** Track project-level document completion status across email batches.

1. Create new Google Spreadsheet (or add tab to existing Processing Log)
2. Name: `Document Organizer - Project Tracker` (or tab name: `Project Tracker`)
3. Add headers in Row 1:

| A | B | C | D | E | F | G | H | I |
|---|---|---|---|---|---|---|---|---|
| Project Name | Exposé | Grundbuch | Calculation | Exit Strategy | Total Complete | Status | Last Updated | Notes |

4. **Column Formulas:**
   - **Column F (Total Complete):** `=COUNTIF(B2:E2, TRUE)` (counts checked boxes)
   - **Column G (Status):**
     ```
     =IF(F2=4,"COMPLETE",IF(F2=0,"NEW","IN PROGRESS ("&F2&"/4)"))
     ```

5. **Format Columns B-E as Checkboxes:**
   - Select columns B through E
   - Format → Number → Checkbox

6. Copy Spreadsheet ID and set `PROJECT_TRACKER_SHEET_ID`

**Example Data:**

| Project Name | Exposé | Grundbuch | Calculation | Exit | Total | Status | Last Updated |
|--------------|--------|-----------|-------------|------|-------|--------|--------------|
| Müller Apartment Building | ✓ | ✓ | ✓ | ✓ | 4 | COMPLETE | 2025-12-21 |
| Schmidt Office Complex | ✓ | ✓ |  |  | 2 | IN PROGRESS (2/4) | 2025-12-21 |
| Unknown Project |  | ✓ |  |  | 1 | IN PROGRESS (1/4) | 2025-12-21 |

### 5.3 Error Log

1. Create new Google Spreadsheet
2. Name: `Document Organizer - Error Log`
3. First sheet name: `Errors`
4. Add headers in Row 1:

| A | B | C | D | E | F | G | H | I | J | K | L | M | N | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Error ID | Timestamp | Date | Time | Error Message | Node Name | Node Type | Execution ID | Retry Count | Can Retry | Document Name | Severity | Status | Resolved At | Resolution |

5. Copy Spreadsheet ID and set `ERROR_LOG_SHEET_ID`

---

## 6. Chunk-by-Chunk Import

### IMPORTANT: Start with Chunk 0 (One-Time Setup)

**Chunk 0 (Folder Initialization) automatically creates all 37 folders and sets all folder ID variables. Run this FIRST before importing the main workflow!**

### 6.0 Import Chunk 0: Folder Initialization (Run Once)

1. **Import JSON:**
   - Go to **Workflows → Import from File**
   - Select `chunk0_folder_initialization.json`
   - Click Import

2. **Configure Credentials:**
   - Open all Google Drive nodes → Select Google Drive OAuth2 credential
   - Open "Send Confirmation Email" node → Select Gmail OAuth2 credential

3. **Set Root Folder Name (Optional):**
   - Default: Creates `Bautraeger_Documents` folder in Drive root
   - To customize: Edit "Set Root Folder Name" node

4. **Execute Workflow (Manual Trigger):**
   - Click "Execute Workflow" button
   - Workflow will:
     - Create root folder `Bautraeger_Documents`
     - Create 4 parent folders (OBJEKTUNTERLAGEN, WIRTSCHAFTLICHE, RECHTLICHE, SONSTIGES)
     - Create all 37 subfolders
     - Create `_Staging` folder
     - Set all folder ID variables automatically
     - Send confirmation email with folder IDs

5. **Verify Completion:**
   - Check your Drive for new folder structure
   - Check your email for confirmation
   - Go to **Settings → Variables** - all folder variables should be set

**Folder Structure Created:**

```
📁 Bautraeger_Documents/
├── 📁 _Staging/                    (auto-set: STAGING_FOLDER_ID)
├── 📁 OBJEKTUNTERLAGEN/ (22 subfolders)
│   ├── 📁 01_Projektbeschreibung/  (auto-set: FOLDER_01_PROJEKTBESCHREIBUNG)
│   ├── 📁 03_Grundbuchauszug/      (auto-set: FOLDER_03_GRUNDBUCHAUSZUG)
│   ├── 📁 10_Bautraegerkalkulation_DIN276/ (auto-set: FOLDER_10_BAUTRAEGERKALKULATION)
│   └── ... (19 more folders)
├── 📁 WIRTSCHAFTLICHE/ (6 subfolders)
├── 📁 RECHTLICHE/ (4 subfolders)
└── 📁 SONSTIGES/ (5 subfolders)
    ├── 📁 36_Exit_Strategie/      (auto-set: FOLDER_36_EXIT_STRATEGIE)
    ├── 📁 37_Others/              (auto-set: FOLDER_37_OTHERS)
    └── 📁 38_Unknowns/            (auto-set: FOLDER_38_UNKNOWNS)
```

**Important Notes:**
- Chunk 0 is **idempotent** - safe to re-run if interrupted
- It checks if folders exist before creating (won't duplicate)
- All 37 folder ID variables are automatically set
- This is a **ONE-TIME setup** - deactivate after successful run

### Gmail Label Setup

Before importing the main workflow chunks, create the Gmail label:

1. Open Gmail
2. Create label: `Bautraeger_Docs`
3. Create filter to auto-label incoming Bauträger emails
4. Or manually label emails to trigger processing

---

### 6.1 Import Chunk 1: Email → Staging

1. **Import JSON:**
   - Go to **Workflows → Import from File**
   - Select `chunk1_email_staging.json`
   - Click Import

2. **Configure Credentials:**
   - Open "Gmail Trigger" node → Select Gmail OAuth2 credential
   - Open "Download Attachments" node → Select Gmail OAuth2 credential
   - Open "Upload to Staging" node → Select Google Drive credential

3. **Update Placeholder Values:**
   - In credential references, replace `{{GMAIL_CREDENTIAL_ID}}` with actual credential
   - In credential references, replace `{{GOOGLE_DRIVE_CREDENTIAL_ID}}` with actual credential

4. **Test:**
   - Click "Execute Workflow"
   - Send test email with PDF attachment to Gmail
   - Verify file appears in Staging folder
   - **V3.5 Test:** Send email with ZIP file containing PDFs → Verify all PDFs extracted

### 6.2 Import Chunk 2: Text Extraction

1. **Import JSON:** `chunk2_text_extraction.json`

2. **Configure Credentials:**
   - Open "AWS Textract OCR (German)" node → Select AWS credential

3. **Connect to Chunk 1:**
   - Connect "Upload to Staging" output → "Input: File from Staging" input

4. **Test:**
   - Execute with a digital PDF → Should skip OCR
   - Execute with scanned PDF → Should use Textract

### 6.3 Import Chunk 2.5: Project Tracking (NEW IN V3.5)

1. **Import JSON:** `chunk2.5_project_tracking.json`

2. **Configure Credentials:**
   - Open "OpenAI: Extract Project Name" node → Select OpenAI credential
   - Open all Google Sheets nodes → Select Google Sheets credential

3. **Configure Project Tracker Sheet ID:**
   - Ensure `PROJECT_TRACKER_SHEET_ID` variable is set (from Section 5.2)

4. **Connect to Chunk 2:**
   - Connect "Prepare Text for AI" output → "Input: Extracted Text" input

5. **Test:**
   - Execute with sample document
   - Verify project name extracted correctly
   - Check Project Tracker sheet for new row or updated row
   - Verify completion status calculated

### 6.4 Import Chunk 3: AI Classification

1. **Import JSON:** `chunk3_ai_classification.json`

2. **Configure Credentials:**
   - Open all OpenAI nodes → Select OpenAI credential

3. **Connect to Chunk 2.5:**
   - Connect "Output: Project Data" output → "Input: Text + Project" input

4. **Test with sample documents:**
   - Exposé → Should route to "Set Expose Filename"
   - Grundbuch → Should route to "Set Grundbuch Filename"
   - DIN 276 Calculation → Should route to "Set Calculation Filename"
   - Exit Strategy → Should route to "Set Exit Filename"
   - Baugenehmigung → Should route to "Set Others Filename"
   - Gibberish → Should route to "Set Unknown Filename"
   - **V3.5 Test:** Verify all filenames include HH:MM:SS timestamp

### 6.5 Import Chunk 4: File Operations + Logging + Project Update (UPDATED IN V3.5)

1. **Import JSON:** `chunk4_file_ops_logging.json`

2. **Configure Credentials:**
   - Open "Move to Target Folder" → Select Google Drive credential
   - Open "Rename File" → Select Google Drive credential
   - Open "Log to Main Sheet" → Select Google Sheets credential
   - Open "Update Project Tracker" node → Select Google Sheets credential
   - Open "Email Eugene Summary" → Select Gmail OAuth2 credential

3. **Connect to Chunk 3:**
   - Connect "Merge All Classified" output → "Move to Target Folder" input

4. **Test:**
   - Execute full workflow
   - Verify file moved to correct folder
   - Verify file renamed with timestamp
   - Verify log entry in Google Sheet
   - **V3.5 Test:** Verify Project Tracker sheet updated (document marked as ✓)
   - **V3.5 Test:** Verify email shows project status (2/4, 3/4, or COMPLETE)
   - Verify Eugene receives email with enhanced project information

### 6.6 Import Chunk 5: Error Handling

1. **Import JSON:** `chunk5_error_handling.json`

2. **Configure Credentials:**
   - Open "Log Error to Sheet" → Select Google Sheets credential
   - Open all "Alert" nodes → Select Gmail OAuth2 credential
   - Open "Update Error Status" nodes → Select Google Sheets credential

3. **Note:** This chunk is independent - triggered by workflow errors

4. **Test:**
   - Temporarily break a node (invalid credential)
   - Execute workflow
   - Verify error logged to Error Sheet
   - Verify retry logic triggers (3 attempts with exponential backoff)
   - Verify alert email sent

---

## 7. Testing Each Chunk

### Test Documents Needed

Prepare these 6 test documents:

| Type | Example | Expected Outcome |
|------|---------|------------------|
| Exposé | Project description PDF | → 01_Projektbeschreibung, prefix: EXPOSE |
| Grundbuch | Land register extract | → 03_Grundbuchauszug, prefix: GRUNDBUCH |
| Calculation | DIN 276 cost breakdown | → 10_Bautraegerkalkulation, prefix: KALK276 |
| Exit Strategy | Liquidation plan | → 36_Exit_Strategie, prefix: EXIT |
| Other | Baugenehmigung or BWA | → 37_Others, prefix: OTHERS |
| Unknown | Random/illegible scan | → 38_Unknowns, prefix: UNKNOWN |

### Test Scenarios

| Scenario | Input | Expected Result |
|----------|-------|-----------------|
| Digital PDF | Clear text PDF | Text extracted, no OCR |
| Scanned PDF | Image-based PDF | OCR triggered, German text |
| ZIP with PDFs | Archive with 3 PDFs | All 3 extracted and processed |
| Mixed ZIP | PDF + DOCX + JPG | Only PDF/DOCX processed |
| Large file | 50-page PDF | Truncated to 3000 chars for AI |
| Rate limit | 20 emails at once | Queued processing, no errors |

### V3.5 Project Tracking Test Scenarios (NEW)

**Test Case 1: New Project - Single Email with 2 Documents**
- **Input:** Email with Exposé + Grundbuch for "Müller Apartment Building"
- **Expected:**
  - New row created in Project Tracker: "Müller Apartment Building"
  - Exposé checkbox: ✓
  - Grundbuch checkbox: ✓
  - Status: "IN PROGRESS (2/4)"
  - Email shows: "2/4 Priority Documents" + "Missing: Calculation, Exit Strategy"

**Test Case 2: Same Project - Second Email with Missing Documents**
- **Input:** Email with Calculation + Exit Strategy for "Müller Apartment Building" (3 days later)
- **Expected:**
  - SAME row updated in Project Tracker (not new row)
  - Calculation checkbox: ✓
  - Exit Strategy checkbox: ✓
  - Status: "COMPLETE"
  - Email shows: "🎉 4/4 Priority Documents - COMPLETE"

**Test Case 3: Different Project - Partial Documents**
- **Input:** Email with only Exposé for "Schmidt Office Complex"
- **Expected:**
  - New row created: "Schmidt Office Complex"
  - Only Exposé checkbox: ✓
  - Status: "IN PROGRESS (1/4)"
  - Email shows: "1/4 Priority Documents" + "Missing: Grundbuch, Calculation, Exit Strategy"

**Test Case 4: Unknown Project Name**
- **Input:** Email with Grundbuch but AI can't extract project name
- **Expected:**
  - Row created: "Unknown Project"
  - Grundbuch checkbox: ✓
  - Status: "IN PROGRESS (1/4)"
  - Still tracked, can be renamed manually later

**Test Case 5: Timestamp Uniqueness**
- **Input:** Two identical Exposé files processed in same minute
- **Expected:**
  - Both files saved with different timestamps (seconds differ)
  - Example: `EXPOSE_Eugene_20251221_143052.pdf` and `EXPOSE_Eugene_20251221_143053.pdf`
  - No filename collision in Google Drive

---

## 9. Troubleshooting

### Common Issues

#### "Gmail Trigger not firing"
- Check label filter matches exactly: `Bautraeger_Docs`
- Verify OAuth2 scopes include read access
- Check poll interval (default: every minute)

#### "AWS Textract returns empty"
- Verify region matches variable: `eu-central-1`
- Check IAM policy includes `textract:DetectDocumentText`
- Ensure file is < 5MB (Textract limit)

#### "AI classification returns wrong type"
- Check extracted text quality (view in execution)
- For scanned docs, verify OCR worked
- Confidence threshold may need adjustment

#### "File not moving to folder"
- Verify folder ID in variable is correct
- Check Drive permissions for service account
- Ensure no special characters in folder name

#### "Google Sheets append fails"
- Verify sheet name matches exactly: `Processing Log`
- Check column headers match node configuration
- Ensure spreadsheet ID is correct

#### "Email notifications not sending"
- Verify Gmail OAuth2 has send permission
- Check EUGENE_EMAIL variable is valid
- Review Gmail sending limits (500/day)

### V3.5-Specific Issues

#### "Chunk 0 folder creation fails"
- **Symptom:** Folders not created in Google Drive
- **Causes:**
  - Google Drive OAuth2 missing `drive.file` scope
  - Drive API quota exceeded (750 requests/minute)
  - Parent folder name conflict (folder already exists)
- **Solution:**
  - Re-authenticate Google Drive credential with full scopes
  - Add delay between folder creation calls (1-2 seconds)
  - Check Drive root for existing `Bautraeger_Documents` folder

#### "Folder ID variables not set"
- **Symptom:** Variables missing after Chunk 0 execution
- **Causes:**
  - Workflow execution failed mid-way
  - Variable name typo in Set node
  - Insufficient n8n permissions
- **Solution:**
  - Check Chunk 0 execution log for errors
  - Verify "Set Variable" nodes completed successfully
  - Re-run Chunk 0 (safe to re-run)

#### "Project name not extracting correctly"
- **Symptom:** All projects show "Unknown Project"
- **Causes:**
  - OpenAI API key invalid or quota exceeded
  - Document text too short or unclear
  - German language not detected properly
- **Solution:**
  - Verify OpenAI credential and API key
  - Check extracted text includes property/project mentions
  - Review "Extract Project Name" prompt - may need tuning for specific document format
  - Check OpenAI usage dashboard for errors

#### "Project Tracker sheet not updating"
- **Symptom:** New documents processed but sheet doesn't update
- **Causes:**
  - PROJECT_TRACKER_SHEET_ID variable not set
  - Google Sheets credential missing write permission
  - Sheet name mismatch (expected: `Project Tracker`)
- **Solution:**
  - Verify PROJECT_TRACKER_SHEET_ID is set (Section 5.2)
  - Re-authenticate Google Sheets with full edit permissions
  - Check exact sheet/tab name matches `Project Tracker`
  - Verify columns B-E are formatted as checkboxes

#### "Email doesn't show project status"
- **Symptom:** Notification email missing project completion info
- **Causes:**
  - Chunk 2.5 (Project Tracking) not connected
  - Project data not passed through workflow
  - Email template node using old V3 format
- **Solution:**
  - Verify Chunk 2.5 output is connected to Chunk 3 input
  - Check workflow execution - project data should be in JSON throughout
  - Update "Build Email Summary" node to use V3.5 template (includes project status)

#### "Timestamp not appearing in filename"
- **Symptom:** Filenames lack HH:MM:SS suffix
- **Causes:**
  - Still using V3 "Set Filename" nodes (old format)
  - Date/time variable not configured
- **Solution:**
  - Verify Chunk 3 nodes use V3.5 format: `{{PREFIX}}_{{CLIENT}}_{{$now.format('YYYYMMDD_HHmmss')}}.{{ext}}`
  - Check n8n's `$now` variable is available
  - Re-import `chunk3_ai_classification.json` (V3.5 version)

#### "Duplicate project rows created"
- **Symptom:** Same project appears multiple times in Project Tracker
- **Causes:**
  - Project name extraction inconsistent (e.g., "Müller Building" vs "Müller Apartment Building")
  - Search logic case-sensitive
  - Typos in project name
- **Solution:**
  - Review project names in tracker - merge duplicates manually
  - Consider adding fuzzy matching logic (Phase 2 enhancement)
  - Standardize AI extraction prompt for consistency

### Debug Mode

Enable verbose logging:
1. **Settings → Workflow Settings**
2. Enable "Save Execution Progress"
3. Enable "Save Data Success Execution: All"

---

## 10. Go-Live Checklist

### Pre-Launch Verification

**Chunk 0 Setup (One-Time):**
- [ ] Chunk 0 (Folder Initialization) imported and executed successfully
- [ ] All 37 folders created in Google Drive under `Bautraeger_Documents/`
- [ ] `_Staging` folder created
- [ ] All folder ID variables automatically set (verify in Settings → Variables)
- [ ] Confirmation email received with folder IDs
- [ ] Chunk 0 workflow deactivated (one-time use only)

**Credentials & API Access:**
- [ ] All 5 credentials configured and tested (Gmail, Drive, Sheets, OpenAI, AWS)
- [ ] Google Drive OAuth2 has `drive.file` scope
- [ ] Google Sheets OAuth2 has edit permissions
- [ ] OpenAI API key valid with sufficient quota
- [ ] AWS credentials configured for `eu-central-1` region

**Variables Configuration:**
- [ ] `CLIENT_NAME` set (default: "Eugene")
- [ ] `EUGENE_EMAIL` set for notifications
- [ ] `MAIN_LOG_SHEET_ID` set
- [ ] `PROJECT_TRACKER_SHEET_ID` set (NEW V3.5)
- [ ] `ERROR_LOG_SHEET_ID` set
- [ ] All folder variables set by Chunk 0 (37 folders + staging)

**Google Sheets Setup:**
- [ ] Main Processing Log created with correct headers
- [ ] **Project Tracker sheet created** (NEW V3.5)
  - [ ] Headers: Project Name | Exposé | Grundbuch | Calculation | Exit Strategy | Total Complete | Status | Last Updated | Notes
  - [ ] Columns B-E formatted as checkboxes
  - [ ] Column F formula: `=COUNTIF(B2:E2, TRUE)`
  - [ ] Column G formula: `=IF(F2=4,"COMPLETE",IF(F2=0,"NEW","IN PROGRESS ("&F2&"/4)"))`
- [ ] Error Log sheet created with correct headers

**Gmail Configuration:**
- [ ] Gmail label created (e.g., `Bautraeger_Docs`)
- [ ] Label filtering configured correctly
- [ ] Test email with label successfully triggers workflow

**Workflow Testing:**
- [ ] Test email with single PDF processed successfully
- [ ] Test email with ZIP file extracted correctly
- [ ] All 6 document types tested (Exposé, Grundbuch, Calculation, Exit, Others, Unknown)
- [ ] **Project tracking tested** (NEW V3.5):
  - [ ] New project created in tracker
  - [ ] Second batch updates same project (not creates duplicate)
  - [ ] Completion status calculated correctly (2/4, 3/4, 4/4)
  - [ ] Email notification shows project status
- [ ] Timestamp appears in filenames (HH:MM:SS format)
- [ ] Files moved to correct folders
- [ ] Eugene receives notification email with **project completion status** (NEW V3.5)
- [ ] Error handling triggers correctly on simulated failure
- [ ] Retry logic tested (exponential backoff: 5s → 15s → 45s)

### Activation Steps

1. **Activate Workflow:**
   - Click "Active" toggle in top right
   - Workflow will now run on schedule

2. **Monitor First Day:**
   - Check executions every hour
   - Review error log for issues
   - Verify files in correct folders

3. **Adjust as Needed:**
   - Tune AI prompts if misclassifications occur
   - Adjust retry delays if rate limits hit
   - Update email template based on feedback

### Support Contact

For issues during implementation:
- Check n8n community forum
- Review this guide's troubleshooting section
- Document any new issues for V3.1 improvements

---

## Appendix: Credential ID Placeholders

Replace these placeholders in JSON files before import:

| Placeholder | Replace With |
|-------------|--------------|
| `{{GMAIL_CREDENTIAL_ID}}` | Your Gmail OAuth2 credential ID |
| `{{GOOGLE_DRIVE_CREDENTIAL_ID}}` | Your Google Drive credential ID |
| `{{GOOGLE_SHEETS_CREDENTIAL_ID}}` | Your Google Sheets credential ID |
| `{{OPENAI_CREDENTIAL_ID}}` | Your OpenAI credential ID |
| `{{AWS_CREDENTIAL_ID}}` | Your AWS credential ID |

**How to find credential ID:**
1. Go to Settings → Credentials
2. Click on credential
3. ID is in URL: `/credentials/`**`123`**

---

*Document Organizer V3.5 Phase 1 - Implementation Guide*
*Created: 2025-12-21*
*Last Updated: 2025-12-22*
