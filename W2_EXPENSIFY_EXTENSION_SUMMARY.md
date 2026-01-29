# Implementation Complete – W2 Expensify Extension

## 1. Overview
- **Platform:** n8n
- **Workflow ID:** dHbwemg7hEB4vDmC
- **Workflow Name:** Expense System - Workflow 2: Gmail Receipt Monitor
- **Status:** Built - **Needs Configuration**
- **Files modified:** Workflow W2 (added 3 new nodes)

## 2. Workflow Structure

### New Expensify Branch Added

**Trigger Path:**
```
Daily Receipt Check / Webhook
↓
Load Vendor Patterns (already includes Expensify)
↓
Search Gmail (both accounts)
↓
Get Email Details
↓
Combine Both Gmail Accounts
↓
**NEW: Detect Expensify Email (IF node)**
├─ Output 0 (TRUE - Expensify email): **NEW - Expensify reports path**
│   ↓
│   Extract Expensify PDF
│   ↓
│   Upload to Expensify Reports Folder
│   ↓
│   Trigger W6 Workflow
│
└─ Output 1 (FALSE - Not Expensify): → Detect Invoice or Receipt (IF node)
    ├─ Output 0: Regular receipts path (existing)
    ├─ Output 1: Apple receipts path (existing)
    └─ Output 2: Invoices path (existing)
```

### New Nodes Added

1. **Detect Expensify Email** (IF node - Position: 1000, -112)
   - Inserted BEFORE "Detect Invoice or Receipt"
   - Checks two conditions (AND logic):
     - Condition 1: `fromEmail` equals "concierge@expensify.com"
     - Condition 2: `subject` contains "sent you their"
   - Output 0 (TRUE): Routes to Expensify processing path
   - Output 1 (FALSE): Routes to existing invoice/receipt detection logic

2. **Extract Expensify PDF** (Code node - Position: 1344, -592)
   - Parses report month from subject line
   - Expected format: "Sway Clarke sent you their [Month YYYY] report"
   - Converts to YYYY-MM format (e.g., "January 2026" → "2026-01")
   - Extracts PDF attachment from email
   - Preserves binary data for upload

3. **Upload to Expensify Reports Folder** (Google Drive node - Position: 1568, -592)
   - Uploads PDF to Google Drive
   - **⚠️ NEEDS CONFIGURATION:**
     - Current folder ID: `1BmZqF9X_TODO_REPLACE_WITH_REAL_FOLDER_ID`
     - **Action Required:** Replace with actual "Expensify-Reports" folder ID
   - Uses Sway Google Account credentials (ID: 80)
   - Filename: Uses original PDF filename from Expensify

4. **Trigger W6 Workflow** (HTTP Request node - Position: 1792, -592)
   - Sends webhook to W6 workflow
   - **⚠️ NEEDS CONFIGURATION:**
     - Current URL: `https://n8n.oloxa.ai/webhook/w6-expensify-intake-TODO`
     - **Action Required:** Replace with actual W6 webhook URL
   - Payload sent to W6:
     ```json
     {
       "drive_file_id": "<uploaded file ID>",
       "report_month": "<YYYY-MM>",
       "file_name": "<original filename>",
       "received_date": "<ISO timestamp>"
     }
     ```

## 3. Configuration Notes

### ⚠️ Required Manual Configuration

#### 1. Create/Locate Google Drive Folder
```
Action: Create "Expensify-Reports" folder in Google Drive OR locate existing folder
Steps:
  1. Navigate to Google Drive
  2. Find or create "Expensify-Reports" folder
  3. Get folder ID from URL (e.g., https://drive.google.com/drive/folders/[FOLDER_ID])
  4. Update node "Upload to Expensify Reports Folder":
     - Change folderId parameter from `1BmZqF9X_TODO_REPLACE_WITH_REAL_FOLDER_ID`
     - To actual folder ID
```

#### 2. Verify/Create W6 Workflow
```
Status: Unknown - need to check if W6 exists
Action: Check if "Workflow 6: Expensify Table Processor" exists

If W6 exists:
  - Get webhook URL from W6's webhook trigger node
  - Update "Trigger W6 Workflow" node URL

If W6 doesn't exist:
  - Need to build W6 workflow first
  - W6 should:
    1. Receive webhook with drive_file_id + report_month
    2. Download PDF from Drive
    3. Parse Expensify table data
    4. Process expense records
```

#### 3. ✅ Routing Logic Implemented (COMPLETE)
```
✅ IMPLEMENTED: Nested IF node approach (Option B from original plan)

Structure:
  1. "Detect Expensify Email" IF node (NEW)
     - Checks: fromEmail = "concierge@expensify.com" AND subject contains "sent you their"
     - Output 0 (TRUE): Routes to Expensify path
     - Output 1 (FALSE): Routes to "Detect Invoice or Receipt"

  2. "Detect Invoice or Receipt" IF node (EXISTING - unchanged)
     - Checks: subject contains invoice keywords OR filename contains vendor names
     - Handles receipts, Apple emails, and invoices

This approach:
  ✅ Cleanly separates Expensify emails before other detection
  ✅ Preserves all existing invoice/receipt logic
  ✅ Uses standard IF node behavior (2 outputs per node)
  ✅ Easy to understand and debug
```

### Credentials Used
- **Google Drive**: Sway Google Account (credential ID: 80)
- **W6 Webhook**: No authentication configured (assumes internal n8n webhook)

### Important Mappings
- **Report Month Parsing:**
  - Input: "Sway Clarke sent you their January 2026 report"
  - Output: "2026-01"
  - Regex: `/their\s+([A-Za-z]+\s+\d{4})\s+report/i`

- **W6 Payload Fields:**
  - `drive_file_id`: Google Drive file ID (from upload response)
  - `report_month`: Formatted as YYYY-MM
  - `file_name`: Original PDF filename from Expensify
  - `received_date`: ISO timestamp when email was received

## 4. Testing

### Manual Testing Plan

**Test 1: Expensify Email Detection**
1. Trigger workflow manually via webhook: `POST https://n8n.oloxa.ai/webhook/[webhook-id]`
2. Or wait for scheduled trigger
3. Verify "Combine Both Gmail Accounts" enriches Expensify email with `vendorName: "Expensify"`
4. Check if "Detect Expensify Email" IF node routes to Output 0 (Expensify branch)
5. Verify non-Expensify emails route to Output 1 (existing logic)

**Test 2: Report Month Parsing**
1. Send test email with subject: "Sway Clarke sent you their December 2025 report"
2. Expected output: `reportMonth: "2025-12"`
3. Verify regex captures month name and year correctly

**Test 3: PDF Upload**
1. After fixing folder ID configuration
2. Verify PDF uploads to correct Drive folder
3. Check that file ID is captured in JSON output

**Test 4: W6 Trigger**
1. After configuring W6 webhook URL
2. Verify HTTP request succeeds
3. Check W6 receives correct payload format
4. Monitor W6 execution for processing

### Expected Test Data
- **Sender:** concierge@expensify.com
- **Subject:** "Sway Clarke sent you their [Month YYYY] report"
- **Attachment:** PDF file (any .pdf extension)

### Success Criteria
- ✅ Expensify emails route to separate branch (not mixed with invoices/receipts)
- ✅ Report month parsed correctly (YYYY-MM format)
- ✅ PDF uploaded to correct Drive folder
- ✅ W6 webhook triggered with all required fields
- ✅ Existing invoice/receipt logic unaffected

## 5. Handoff

### How to Modify
1. **Change folder location:**
   - Edit "Upload to Expensify Reports Folder" node
   - Update `folderId` parameter

2. **Change W6 webhook URL:**
   - Edit "Trigger W6 Workflow" node
   - Update `url` parameter

3. **Adjust month parsing logic:**
   - Edit "Extract Expensify PDF" node
   - Modify regex in `jsCode` parameter
   - Update `monthMap` object for different date formats

### Known Limitations
- Month parsing only supports English month names
- Assumes PDF is always the first .pdf attachment found
- No retry logic if W6 webhook fails
- No error handling if Drive folder doesn't exist
- Requires manual configuration before production use

### Suggested Next Steps
1. **Immediate (Required):**
   - [ ] Configure Google Drive folder ID
   - [ ] Test Expensify email detection routing (should work with nested IF approach)

2. **Before Production:**
   - [ ] Verify/Build W6 workflow
   - [ ] Configure W6 webhook URL
   - [ ] Test end-to-end with real Expensify email
   - [ ] Add error handling (catch Drive upload failures)
   - [ ] Add error handling (catch W6 webhook failures)

3. **Optional Enhancements:**
   - [ ] Run test-runner-agent to validate workflow
   - [ ] Run workflow-optimizer-agent if costs become an issue
   - [ ] Add email notification on Expensify processing completion
   - [ ] Add logging to track Expensify reports processed

## 6. Current Status

**✅ Completed:**
- New "Detect Expensify Email" IF node inserted before existing logic
- Extract Expensify PDF node created (with month parsing)
- Google Drive upload node created
- W6 trigger node created
- All nodes connected in workflow
- Workflow validates successfully (0 errors, 59 warnings)
- Routing logic uses nested IF approach (clean separation)

**⚠️ Pending Configuration:**
- Google Drive folder ID (placeholder value)
- W6 webhook URL (placeholder value)

**⚠️ Blocker:**
- Cannot test until folder ID and W6 URL are configured

## 7. Technical Notes

### Vendor Patterns Already Include Expensify
The "Load Vendor Patterns" node already includes Expensify:
```javascript
{ name: 'Expensify', email: 'concierge@expensify.com' }
```

This means "Combine Both Gmail Accounts" will enrich Expensify emails with:
```json
{
  "vendorName": "Expensify",
  "fromEmail": "concierge@expensify.com"
}
```

### IF Node Routing Strategy
The workflow now uses **nested IF nodes** for clean separation:

**1. "Detect Expensify Email" (NEW IF node - first check)**
- Output 0 (TRUE): Expensify emails (fromEmail = "concierge@expensify.com" AND subject contains "sent you their")
- Output 1 (FALSE): All other emails → routes to "Detect Invoice or Receipt"

**2. "Detect Invoice or Receipt" (EXISTING IF node - unchanged)**
- Output 0: Regular receipts
- Output 1: Apple emails (no attachments)
- Output 2: Invoices (subject contains "invoice,rechnung,faktura")

**Why this works:**
- ✅ Standard IF node behavior (2 outputs: true/false)
- ✅ No complex multi-branch routing needed
- ✅ Expensify detected first, bypassing other logic
- ✅ All existing logic preserved and unmodified

### Binary Data Preservation
The "Extract Expensify PDF" node explicitly preserves binary data:
```javascript
return {
  json: { ...metadata },
  binary: { data: pdfAttachment }
};
```

This ensures the PDF can be uploaded to Drive in the next node.

---

**Implementation Date:** 2026-01-29
**Agent:** solution-builder-agent (Agent ID: will be provided in main conversation)
**Workflow Version:** Latest (36 nodes, 33 connections)
**Validation Status:** ✅ Valid (0 errors, 59 warnings)
**Approach:** Nested IF nodes (clean separation strategy)
