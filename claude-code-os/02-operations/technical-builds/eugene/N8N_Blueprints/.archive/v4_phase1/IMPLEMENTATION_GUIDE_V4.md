# Document Organizer V4 - Implementation Guide

**Date:** December 22, 2025
**Version:** 4.0 (Phase 1 MVP with Archive Feature)
**Status:** READY FOR DEPLOYMENT

---

## Table of Contents

1. [Implementation Status Matrix](#implementation-status-matrix)
2. [Prerequisites](#prerequisites)
3. [API Credentials Setup](#api-credentials-setup)
4. [Google Sheets Configuration](#google-sheets-configuration)
5. [Step-by-Step Implementation](#step-by-step-implementation)
6. [Testing Procedures](#testing-procedures)
7. [Confidence Score Explanation](#confidence-score-explanation)
8. [Archive Folder Implementation](#archive-folder-implementation)
9. [Known Limitations](#known-limitations)
10. [Troubleshooting](#troubleshooting)

---

## Implementation Status Matrix

### V4 Features: What's Implemented vs Documented

| Feature | Status | Details | Evidence |
|---------|--------|---------|----------|
| **1. Confidence in Filename** | ✅ FULLY IMPLEMENTED | AI confidence visible as `_97%.pdf` | chunk3, lines 61-88 |
| **2. Document Versioning** | ✅ FULLY IMPLEMENTED | Detection, filename, tracker, AND archiving | chunk4 + archive nodes |
| **2a. Version Detection** | ✅ Implemented | Queries Processing Log, increments version | chunk4, lines 56-65 |
| **2b. Version in Filename** | ✅ Implemented | `_v2_` inserted before confidence | chunk4, lines 75-88 |
| **2c. Version in Tracker** | ✅ Implemented | Updates "Exposé Version" to "v2" | chunk4, lines 224-237 |
| **2d. Archive Old Versions** | ✅ IMPLEMENTED | Moves old versions to _Archive subfolders | chunk4 (archive nodes) |
| **3. Fuzzy Project Matching** | ✅ FULLY IMPLEMENTED | Levenshtein with German normalization | chunk2.5, lines 49-96 |
| **4. Sequential Processing** | ✅ FULLY IMPLEMENTED | SplitInBatches with batch size = 1 | chunk1 |
| **5. Automated Variables** | ✅ FULLY IMPLEMENTED | n8n Variables API batch update | chunk0, lines 149-169 |
| **6. Failed Docs → Unknown** | ✅ FULLY IMPLEMENTED | Catch-all with email notification | chunk5, all nodes |
| **7. German Char Normalization** | ✅ FULLY IMPLEMENTED | ü→u, ö→o, ä→a, ß→ss | chunk2.5, lines 49-58 |
| **8. Field Name Consistency** | ✅ FULLY IMPLEMENTED | Normalization nodes at chunk boundaries | All chunks |
| **9. Timestamp Milliseconds** | ✅ FULLY IMPLEMENTED | HHMMSSsss format | chunk3, line 61 |
| **10. Confidence Thresholds** | ⚠️ DOCUMENTED ONLY | Interpretive guidelines, not enforced | See section below |

### Critical Fixes: All Implemented

| Fix | Status | Evidence |
|-----|--------|----------|
| **Fix #1: Fuzzy Matching** | ✅ Implemented | chunk2.5, lines 49-96 |
| **Fix #2: Tracker Update Logic** | ✅ Implemented | chunk4, lines 169-178 |
| **Fix #3: Variable API** | ✅ Implemented | chunk0, lines 149-169 |
| **Fix #4: Field Consistency** | ✅ Implemented | Normalization nodes in all chunks |
| **Fix #5: Sequential Processing** | ✅ Implemented | chunk1 design |
| **Fix #6: Milliseconds** | ✅ Implemented | chunk3 filename function |

---

## Prerequisites

### 1. n8n Installation Verified
- n8n installed and running
- Access to n8n UI (typically http://localhost:5678)
- Admin access to create workflows and configure credentials

### 2. Required API Keys

You'll need to obtain the following API credentials **before** starting implementation:

#### A. n8n API Key
- **Purpose:** Allows chunk 0 to set folder ID variables automatically
- **How to get:**
  1. In n8n UI: Settings → API
  2. Generate new API key
  3. Copy the key (you won't see it again)
- **Where to use:** Set as n8n environment variable `N8N_API_KEY`

#### B. OpenAI API Key
- **Purpose:** GPT-4o-mini for document classification
- **How to get:**
  1. Go to https://platform.openai.com/api-keys
  2. Create new secret key
  3. Copy the key (starts with `sk-`)
- **Cost:** ~$0.006-0.010 per document
- **Where to use:** Configure as credential in n8n

#### C. Google OAuth2 Credentials (3 APIs)
- **Purpose:** Gmail, Google Drive, Google Sheets access
- **How to get:**
  1. Go to https://console.cloud.google.com/
  2. Create new project (or select existing)
  3. Enable APIs:
     - Gmail API
     - Google Drive API
     - Google Sheets API
  4. Create OAuth 2.0 credentials:
     - Application type: Desktop app
     - Download JSON credentials
  5. Configure OAuth consent screen
- **Where to use:** Configure as credentials in n8n (separate for each)

#### D. AWS Credentials (for Textract)
- **Purpose:** OCR for scanned German documents
- **How to get:**
  1. Go to AWS IAM console
  2. Create new user with programmatic access
  3. Attach policy: `AmazonTextractFullAccess`
  4. Save Access Key ID and Secret Access Key
- **Cost:** ~$0.0015 per scanned page
- **Where to use:** Configure as credential in n8n

### 3. n8n Environment Variables

**Required Variables (set BEFORE running chunk 0):**

| Variable | Purpose | Example Value |
|----------|---------|---------------|
| `N8N_API_KEY` | Automated variable setting | `n8n_api_1234567890abcdef` |
| `N8N_BASE_URL` | Your n8n instance URL | `http://localhost:5678` |
| `CLIENT_NAME` | Used in filenames | `Eugene` |
| `NOTIFICATION_EMAIL` | Alert email address | `eugene@example.com` |

**How to set in n8n:**
1. Go to n8n UI → Settings → Variables
2. Click "Add Variable"
3. Enter Key and Value
4. Click Save

**Variables Set Automatically by Chunk 0:**
- `FOLDER_ROOT`
- `FOLDER_STAGING`
- `FOLDER_01_PROJEKTBESCHREIBUNG` through `FOLDER_38_UNKNOWNS`
- `FOLDER_01_ARCHIVE`, `FOLDER_03_ARCHIVE`, `FOLDER_10_ARCHIVE`, `FOLDER_36_ARCHIVE`
- **Total:** 41 folder ID variables (no manual intervention required)

---

## API Credentials Setup

### Step 1: Configure n8n Credentials (30-45 minutes)

#### A. OpenAI API Credential
1. In n8n: Credentials → Add Credential → OpenAI
2. Enter API key (starts with `sk-`)
3. Name it "OpenAI"
4. Save

#### B. Google OAuth2 Credentials (do 3 times)

**Gmail:**
1. Credentials → Add Credential → Gmail OAuth2
2. Upload JSON credentials file (from Google Cloud Console)
3. Authorize with your Google account
4. Name it "Gmail"
5. Save

**Google Drive:**
1. Credentials → Add Credential → Google Drive OAuth2
2. Upload JSON credentials file
3. Authorize with your Google account
4. Name it "Google Drive"
5. Save

**Google Sheets:**
1. Credentials → Add Credential → Google Sheets OAuth2
2. Upload JSON credentials file
3. Authorize with your Google account
4. Name it "Google Sheets"
5. Save

#### C. AWS Textract Credential
1. Credentials → Add Credential → AWS
2. Enter Access Key ID
3. Enter Secret Access Key
4. Select region: `us-east-1` (or your preferred region)
5. Name it "AWS"
6. Save

---

## Google Sheets Configuration

### Create Project Tracker Spreadsheet

**Method 1: Manual Creation**
1. Go to Google Sheets
2. Create new spreadsheet named "Eugene Document Tracker"
3. Create 3 sheets (tabs):

#### Sheet A: Processing Log
Columns (in this order):
```
Timestamp | Project Name | Document Type | Filename | Confidence | Version | Folder Path | File ID | Status | Email From | Email Subject | OCR Used | Scanned | From ZIP
```

#### Sheet B: Projects
Columns (in this order):
```
Project Name | Normalized Name | Exposé | Exposé Version | Grundbuch | Grundbuch Version | Calculation | Calculation Version | Exit Strategy | Exit Version | Total Complete | Status | Last Updated | Created From Email | Source
```

#### Sheet C: Error Log
Columns (in this order):
```
Timestamp | Error Type | Node Name | Error Message | Severity | File Name | Project Name | Document Type | Execution ID | Resolution Status
```

4. Copy the spreadsheet ID from URL:
   ```
   https://docs.google.com/spreadsheets/d/[THIS_IS_THE_ID]/edit
   ```
5. Set as n8n variable: `PROJECT_TRACKER_SHEET_ID`

### Gmail Label Setup

**Create Gmail Label for Document Emails:**
1. In Gmail: Settings → Labels
2. Create new label: `AMA_Documents`
3. Get label ID:
   - Method A: Use Gmail API Explorer
   - Method B: Check label URL when selected in Gmail
4. Set as n8n variable: `GMAIL_LABEL_ID`

---

## Step-by-Step Implementation

### Step 1: Import and Test Chunk 0 (15 minutes)

**A. Import Chunk 0 Workflow**
1. In n8n: Workflows → Import from File
2. Select [chunk0_folder_initialization_v4.json](chunk0_folder_initialization_v4.json)
3. Workflow opens in editor

**B. Update Credential References**
The JSON has placeholders like `{{GOOGLE_DRIVE_CREDENTIAL_ID}}`. Replace these:
1. Click on "Create Root Folder" node
2. In Credential dropdown, select "Google Drive"
3. Repeat for all Google Drive nodes
4. Click on "Send Confirmation Email" node
5. Select "Gmail" credential
6. Save workflow

**C. Verify Variables Are Set**
- Go to Settings → Variables
- Confirm `N8N_API_KEY` exists
- Confirm `N8N_BASE_URL` exists
- Confirm `CLIENT_NAME` exists
- Confirm `NOTIFICATION_EMAIL` exists

**D. Execute Chunk 0**
1. Click "Execute Workflow" button
2. Workflow runs (takes 2-3 minutes)
3. Watch for:
   - "Create Root Folder" → Creates Eugene_Documents
   - "Loop Parents" → Creates 5 parent folders
   - "Loop Subfolders" → Creates 41 subfolders (includes _Archive folders)
   - "Set All Variables" → Sets 41 n8n variables
   - "Send Confirmation Email" → Sends success email

**E. Verify Folder Creation**
1. Open Google Drive
2. Check for "Eugene_Documents" folder
3. Check for 4 parent folders:
   - OBJEKTUNTERLAGEN
   - WIRTSCHAFTLICHE_UNTERLAGEN
   - RECHTLICHE_UNTERLAGEN
   - SONSTIGES
4. Check for _Staging folder
5. Check for _Archive subfolders in:
   - `01_Projektbeschreibung/_Archive`
   - `03_Grundbuchauszug/_Archive`
   - `10_Bautraegerkalkulation_DIN276/_Archive`
   - `36_Exit_Strategie/_Archive`

**F. Verify Variables Were Set**
1. Go to Settings → Variables
2. Check for new variables (41 total):
   - `FOLDER_ROOT`
   - `FOLDER_STAGING`
   - `FOLDER_01_PROJEKTBESCHREIBUNG` through `FOLDER_38_UNKNOWNS`
   - `FOLDER_01_ARCHIVE`, `FOLDER_03_ARCHIVE`, `FOLDER_10_ARCHIVE`, `FOLDER_36_ARCHIVE`

### Step 2: Import Main Workflow (30 minutes)

**Option A: Import Combined Workflow** (Recommended)
1. Workflows → Import from File
2. Select [document_organizer_v4_complete.json](document_organizer_v4_complete.json)
3. All chunks imported as one workflow

**Option B: Import Individual Chunks**
1. Import chunk1_email_staging_v4.json
2. Import chunk2_text_extraction_v4.json
3. Import chunk2.5_project_tracking_v4.json
4. Import chunk3_ai_classification_v4.json
5. Import chunk4_file_ops_logging_v4.json
6. Import chunk5_error_handling_v4.json

### Step 3: Configure Workflow Credentials (20 minutes)

For each node that requires credentials, click the node and select the appropriate credential:

**Gmail Nodes:**
- "Gmail Trigger" → Select "Gmail"
- "Alert Email" (chunk 5) → Select "Gmail"

**Google Drive Nodes:**
- All "Google Drive" nodes → Select "Google Drive"

**Google Sheets Nodes:**
- All "Google Sheets" nodes → Select "Google Sheets"

**OpenAI Nodes:**
- "Extract Project Name" → Select "OpenAI"
- "AI Classification" → Select "OpenAI"

**AWS Textract Nodes:**
- "OCR Scanned Document" → Select "AWS"

**Save the workflow.**

### Step 4: Configure Gmail Trigger (10 minutes)

1. Click on "Gmail Trigger" node (first node in chunk 1)
2. Configure:
   - **Event**: "Message Received"
   - **Label**: Select "AMA_Documents"
   - **Simple**: Enable
   - **Download Attachments**: Enable
3. Test connection: Click "Test Step"
4. If successful, you'll see recent emails

---

## Testing Procedures

### Test 1: Basic Document Processing (30 minutes)

**Prepare Test Documents:**
- 1 Exposé (PDF)
- 1 Grundbuch (PDF)
- 1 Calculation DIN 276 (PDF)
- 1 Exit Strategy (PDF)
- 1 scanned document (to test OCR)
- 1 unknown document
- 1 ZIP file containing 2-3 documents

**Test Procedure:**
1. Send email to yourself with test documents attached
2. Apply "AMA_Documents" label to email
3. Watch workflow execution in n8n
4. Verify:
   - Documents appear in _Staging
   - AI classification runs
   - Documents move to correct folders
   - Filenames include confidence: `EXPOSE_Eugene_20251222_143052_97%.pdf`
   - Processing Log sheet is updated
   - Project Tracker sheet is updated

**Expected Processing Time:**
- Digital PDF: 10-20 seconds per document
- Scanned PDF (OCR): 30-45 seconds per document

**Verification Checklist:**
- [ ] Documents moved from _Staging to target folders
- [ ] Filenames include confidence percentage
- [ ] Processing Log has entries
- [ ] Project Tracker shows project with checkboxes
- [ ] Unknown folder has unclassifiable documents
- [ ] No errors in Error Log sheet

### Test 2: Document Versioning with Archive (15 minutes)

**Test Scenario 1: First Version**
1. Send email with Exposé for "Test Project A"
2. Verify file saved as: `EXPOSE_TestProjectA_[date]_[time]_v1_97%.pdf`
3. Check Project Tracker: "Exposé Version" = "v1"
4. Verify: NO archive operation (no previous version)

**Test Scenario 2: Second Version (Archive Triggered)**
1. Send email with UPDATED Exposé for same "Test Project A"
2. Expected Results:
   - New file: `EXPOSE_TestProjectA_[date]_[time]_v2_98%.pdf` in main folder
   - Old v1 file MOVED to `01_Projektbeschreibung/_Archive/`
   - Project Tracker: "Exposé Version" = "v2"
3. Verification:
   - Main folder: Only v2 file present
   - _Archive folder: v1 file present
   - Project Tracker updated

**Test Scenario 3: Third Version (Multiple Archives)**
1. Send email with ANOTHER updated Exposé for "Test Project A"
2. Expected Results:
   - New file: `EXPOSE_TestProjectA_[date]_[time]_v3_95%.pdf` in main folder
   - Old v2 file MOVED to _Archive
   - Project Tracker: "Exposé Version" = "v3"
3. Verification:
   - Main folder: Only v3 file
   - _Archive folder: v1 AND v2 files

### Step 5: Activate Workflow

1. In workflow editor, toggle "Inactive" → "Active"
2. Workflow now runs automatically when emails arrive
3. Monitor execution history for errors

---

## Confidence Score Explanation

### How Confidence Scores Work

**IMPORTANT:** There is NO pre-defined rubric for confidence scores.

The confidence percentage you see in filenames (e.g., `_97%.pdf`) is **AI-generated** by GPT-4o-mini during document classification.

#### How It Works:

1. **AI Analyzes Document:**
   - The AI reads the first 3000 characters of extracted text
   - It looks for German real estate keywords (Exposé, Grundbuch, DIN 276, Exit-Strategie)
   - It determines document type AND its own confidence level

2. **AI Returns Confidence:**
   ```javascript
   // AI response format:
   {
     "classification": "expose",
     "confidence": 0.97,  // AI's self-assessed confidence (0.0 to 1.0)
     "reason": "Document contains Projektbeschreibung and property details"
   }
   ```

3. **Workflow Captures and Displays:**
   - Workflow converts 0.97 → 97%
   - Adds to filename: `EXPOSE_Eugene_20251222_143052_97%.pdf`

#### What the Percentages Mean:

| Range | Interpretation | What to Do |
|-------|---------------|------------|
| 90-100% | High confidence | AI is very certain of classification |
| 70-89% | Medium confidence | Spot check recommended |
| 50-69% | Low confidence | Manual review recommended |
| <50% | Very low confidence | Likely misclassified, review required |

**These are interpretive guidelines only** - the workflow does NOT automatically block or quarantine low-confidence files.

#### Key Points:

- **All documents are processed** regardless of confidence score
- Low confidence files (e.g., 45%) are still saved to their classified folder
- The confidence percentage is a **visual indicator** for you to prioritize manual review
- You should manually check files with <70% confidence by looking at the filename

#### No Automated Filtering:

There is NO code that blocks documents based on confidence. For example:
```javascript
// This code DOES NOT EXIST in the workflow:
if (confidence < 0.7) {
  moveToReviewQueue();  // ❌ NOT IMPLEMENTED
}
```

All documents flow through to their classified folders. You decide which to review based on the confidence in the filename.

---

## Archive Folder Implementation

### How Archive Folders Work

When a client sends an updated version of a document (e.g., revised Exposé), the workflow:

1. **Detects Existing Version:**
   - Queries Processing Log sheet
   - Searches for same project + same document type
   - If found, increments version number

2. **Archives Old Version:**
   - Checks if previous version exists
   - Maps document type to archive folder:
     - Exposé → `01_Projektbeschreibung/_Archive`
     - Grundbuch → `03_Grundbuchauszug/_Archive`
     - Calculation → `10_Bautraegerkalkulation_DIN276/_Archive`
     - Exit → `36_Exit_Strategie/_Archive`
   - Moves old file to _Archive folder

3. **Saves New Version:**
   - Saves new file with incremented version in main folder
   - Updates Project Tracker with new version number

### Example Flow:

**Monday:**
- Client sends Exposé for "Müller Building"
- Saved as: `EXPOSE_MullerBuilding_20251222_143052_v1_97%.pdf`
- Location: `01_Projektbeschreibung/`
- Project Tracker: Exposé = v1

**Thursday:**
- Client sends UPDATED Exposé for "Müller Building"
- Workflow detects existing v1
- Moves v1 to: `01_Projektbeschreibung/_Archive/`
- Saves v2 as: `EXPOSE_MullerBuilding_20251225_091530_v2_98%.pdf`
- Location: `01_Projektbeschreibung/`
- Project Tracker: Exposé = v2

**Result:**
- Main folder: Only latest version (v2)
- _Archive folder: All previous versions (v1)
- Clean folder structure maintained automatically

### Which Document Types Get Archived?

Only the 4 priority document types have archive folders:
- Exposé
- Grundbuch
- Calculation
- Exit Strategy

**Others and Unknown documents:**
- Do NOT have archive folders
- Multiple versions will accumulate in main folder
- These are typically one-off documents that don't need versioning

---

## Known Limitations

### 1. Confidence Thresholds Are Not Enforced

**What This Means:**
- The workflow does NOT automatically quarantine low-confidence documents
- All documents are processed and saved, regardless of confidence score
- You must manually review low-confidence files by checking filenames

**Why This Design:**
- Low-volume system (~30 clients/year = ~120 documents/year)
- Manual review is feasible
- Avoids false positives where correct classifications are blocked

**How to Handle:**
- Weekly: Review filenames in each folder
- Check any file with <70% confidence
- Move misclassified files manually if needed

### 2. Others/Unknown Versioning Not Supported

**What This Means:**
- "Others" and "Unknown" document types do NOT have archive folders
- Multiple versions will accumulate in the same folder
- No automatic archiving for these types

**Why This Design:**
- These are typically one-off documents (contracts, invoices, misc)
- Versioning is less critical for non-standardized documents
- Keeps archive folder structure focused on 4 priority types

**How to Handle:**
- Manually archive Others/Unknown documents if needed
- Consider moving to project-specific subfolders

### 3. Concurrent Email Processing

**What This Means:**
- Emails are processed sequentially (one at a time)
- If two emails arrive simultaneously, second waits for first to complete

**Why This Design:**
- Prevents race conditions in Project Tracker updates
- Low-volume system doesn't require parallel processing
- Simpler error handling

**Impact:**
- Processing time: 10-20 seconds per document
- If 5 documents arrive simultaneously, total time: ~1-2 minutes
- Acceptable for low-volume use case

### 4. Email Summary Optimization Deferred

**What This Means:**
- Email summary after processing is ~150 lines of code
- Could be optimized to ~50 lines

**Why Deferred:**
- Phase 2 optimization
- Current version is functional
- Not critical for MVP

---

## Troubleshooting

### Issue: Chunk 0 fails with "N8N_API_KEY not set"
**Solution:**
- Go to Settings → Variables
- Add `N8N_API_KEY` with your n8n API key

### Issue: Gmail Trigger doesn't fire
**Solution:**
- Check `GMAIL_LABEL_ID` variable is correct
- Verify Gmail OAuth2 authorization is active
- Test: Apply label to existing email manually

### Issue: Documents stuck in _Staging
**Solution:**
- Check Error Log sheet for error details
- Verify all credentials are configured
- Check OpenAI API key is valid and has credits

### Issue: AI Classification returns "unknown" for all documents
**Solution:**
- Check OpenAI credential configuration
- Verify API key is valid: https://platform.openai.com/api-keys
- Check OpenAI account has available credits
- Check quota limits on OpenAI account

### Issue: OCR fails on scanned documents
**Solution:**
- Check AWS credential configuration
- Verify Textract permissions in IAM:
  - Policy: `AmazonTextractFullAccess`
- Check AWS region is set correctly (us-east-1)
- Verify AWS account has Textract enabled

### Issue: Project Tracker not updating
**Solution:**
- Check `PROJECT_TRACKER_SHEET_ID` variable is correct
- Verify Google Sheets OAuth2 authorization
- Check sheet names match exactly:
  - "Processing Log"
  - "Projects"
  - "Error Log"
- Verify column headers match exactly (case-sensitive)

### Issue: Archive folder not working
**Solution:**
- Verify _Archive folders were created by chunk 0
- Check _Archive folder variables exist:
  - `FOLDER_01_ARCHIVE`
  - `FOLDER_03_ARCHIVE`
  - `FOLDER_10_ARCHIVE`
  - `FOLDER_36_ARCHIVE`
- Check "IF Previous Version Exists" node is connected
- Verify "Move Old Version to Archive" node has Google Drive credential

### Issue: Versions not incrementing (always v1)
**Solution:**
- Check Processing Log sheet has data
- Verify "Check Existing Version" node is querying correctly
- Check Project Tracker "Projects" sheet has project names
- Verify project name fuzzy matching is working

---

## Post-Setup Maintenance

### Daily:
- Check Error Log sheet for failures
- Review Unknown folder for misclassified documents

### Weekly:
- Review low-confidence files (<80%) in each folder
- Manually sort "Others" folder contents
- Check _Archive folders aren't accumulating duplicates

### Monthly:
- Review OpenAI and AWS costs
- Archive old logs if Processing Log exceeds 10,000 rows
- Review and merge duplicate projects in Project Tracker

---

## Support and Updates

**Documentation:**
- Main summary: [WORKFLOW_V4_SUMMARY.md](WORKFLOW_V4_SUMMARY.md)
- Missing features: [IMPROVEMENTS_AND_MISSING_FEATURES.md](IMPROVEMENTS_AND_MISSING_FEATURES.md)
- Plan file: `/Users/swayclarke/.claude/plans/humming-giggling-sunbeam.md`

**Version History:**
- V1: Initial implementation (deprecated)
- V2: Added project tracking (deprecated)
- V3: Added fuzzy matching (deprecated)
- V3.5: Chunk architecture (superseded)
- **V4: Current version** (confidence in filename, versioning with archive, all critical fixes)

---

**Last Updated:** December 22, 2025
**Next Review:** After Phase 1 deployment testing
