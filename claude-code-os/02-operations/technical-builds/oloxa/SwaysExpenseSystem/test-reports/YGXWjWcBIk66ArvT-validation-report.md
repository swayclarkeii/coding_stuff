# Test Report: AMA Pre-Chunk 0 - REBUILT v1 (YGXWjWcBIk66ArvT)

**Date:** 2026-01-07
**Workflow ID:** YGXWjWcBIk66ArvT
**Workflow URL:** https://n8n.oloxa.ai/workflow/YGXWjWcBIk66ArvT
**Status:** NOT TESTED - Gmail trigger workflow requires manual activation

---

## Executive Summary

**CANNOT AUTO-TEST**: This is a Gmail trigger workflow. The test_workflow tool only works with webhook, form, or chat triggers. Manual testing is required.

**Validation Status:** FAILED (1 critical error, 42 warnings)

**Key Blocker:** Incorrect error output configuration in "Check Routing Decision" node prevents proper error handling.

**Credentials Status:** UNKNOWN (cannot validate until workflow runs)

---

## Critical Error (MUST FIX)

### Error 1: Incorrect Error Output Configuration

**Node:** Check Routing Decision (If node)
**Severity:** CRITICAL
**Impact:** Error handlers are in wrong output path, will cause execution failures

**Problem:**
The node "Prepare Missing Folder Error" appears to be an error handler but is connected to main[0] (success output) alongside "Execute Chunk 1". This causes n8n to execute BOTH paths when only one should run.

**Current (INCORRECT) Structure:**
```json
"Check Routing Decision": {
  "main": [
    [  // main[0] has TWO nodes mixed together
      {"node": "Prepare Missing Folder Error", "type": "main", "index": 0},
      {"node": "Execute Chunk 1", "type": "main", "index": 0}
    ]
  ]
}
```

**Required Fix:**
```json
"Check Routing Decision": {
  "main": [
    [  // main[0] = success output
      {"node": "Execute Chunk 1", "type": "main", "index": 0}
    ],
    [  // main[1] = error/false output
      {"node": "Prepare Missing Folder Error", "type": "main", "index": 0}
    ]
  ]
}
```

**Also add to the node:**
```json
"onError": "continueErrorOutput"
```

---

## Warnings (Non-Blocking but Important)

### High Priority Warnings

1. **Missing Error Handling (Multiple Nodes)**
   - All Google Drive, Google Sheets, and OpenAI nodes lack error handling
   - Impact: Any API failure will crash the entire workflow
   - Fix: Add `"onError": "continueErrorOutput"` to critical nodes

2. **Outdated Node Versions**
   - "Check Routing Decision" (If node): typeVersion 2, latest is 2.3
   - "Check If UNKNOWN Path" (If node): typeVersion 2, latest is 2.3
   - "Send Email Notification" (Gmail node): typeVersion 2, latest is 2.2
   - Impact: Missing newer features and bug fixes

3. **Resource Locator Format Issues**
   - "Upload PDF to Temp Folder": Field 'name' should use resource locator format
   - "Move PDF to 38_Unknowns": Fields 'fileId' and 'folderId' should use resource locator format
   - Impact: May cause compatibility issues in future n8n versions

4. **Invalid $ Usage Detected (Multiple Code Nodes)**
   - "Extract File ID & Metadata"
   - "Normalize Client Name"
   - "Check Client Exists"
   - "Extract 38_Unknowns Folder ID"
   - Impact: May cause runtime errors when accessing $json

5. **Google Sheets Range Issues**
   - "Lookup Client Registry": Range may not be in valid A1 notation
   - "Lookup Staging Folder": Range may not be in valid A1 notation
   - Impact: May fail to read registry data

### Lower Priority Warnings

- Long linear chain (24 nodes) - Consider breaking into sub-workflows
- Code nodes can throw errors - Add try/catch blocks
- AI APIs have rate limits - Add retry logic

---

## Workflow Structure Analysis

**Total Nodes:** 28
**Enabled Nodes:** 28
**Trigger Nodes:** 1 (Gmail Trigger)
**Valid Connections:** 29
**Invalid Connections:** 0

**Key Nodes:**
1. Gmail Trigger - Unread with Attachments
2. Upload PDF to Temp Folder (Google Drive)
3. Download PDF from Drive (Google Drive)
4. Extract Text from PDF (OpenAI/extractFromFile)
5. AI Extract Client Name (OpenAI)
6. Lookup Client Registry (Google Sheets)
7. Decision Gate (Switch node with 5 outputs)
8. Execute Chunk 0 - Create Folders (Execute Workflow)
9. Execute Chunk 1 (Execute Workflow)
10. Move PDF to 38_Unknowns (Google Drive)
11. Send Email Notification (Gmail)

---

## Credentials to Validate (Runtime Only)

**Cannot validate until workflow runs. Expected credentials:**

1. **Gmail Account** (ID: aYzk7sZF8ZVyfOan)
   - Used by: Gmail Trigger, Send Email Notification
   - Permissions needed: Read emails, send emails

2. **Google Drive Account** (ID: a4m50EefR3DJoU0R)
   - Used by: Upload PDF to Temp Folder, Download PDF from Drive, Move PDF to 38_Unknowns
   - Permissions needed: Create files, move files, read files

3. **Google Sheets Account** (ID: H7ewI1sOrDYabelt)
   - Used by: Lookup Client Registry, Lookup Staging Folder
   - Permissions needed: Read sheets

4. **OpenAI Account** (ID: xmJ7t6kaKgMwA1ce)
   - Used by: AI Extract Client Name, Extract Text from PDF
   - Permissions needed: API calls for text extraction and completion

---

## Expected Execution Flow (NEW Client Path)

Based on the workflow structure, here's what SHOULD happen for a NEW client:

1. **Gmail Trigger** - Receives email with PDF attachment
2. **Filter PDF/ZIP Attachments** - Extracts PDF from email
3. **Upload PDF to Temp Folder** - Stores PDF in Google Drive temp location
4. **Extract File ID & Metadata** - Captures Drive file ID
5. **Download PDF from Drive** - Retrieves PDF for processing
6. **Extract Text from PDF** - Uses OpenAI to extract text content
7. **Evaluate Extraction Quality** - Checks if extraction was successful
8. **AI Extract Client Name** - Uses OpenAI to identify client name
9. **Normalize Client Name** - Converts to lowercase, replaces umlauts (ä→ae, ö→oe, ü→ue, ß→ss)
10. **Lookup Client Registry** - Searches Google Sheets for existing client
11. **Check Client Exists** - Determines if client is NEW or EXISTING
12. **Decision Gate** - Routes to NEW path (output 0)
13. **Execute Chunk 0 - Create Folders** - Creates client folder structure in Google Drive
14. **Check If UNKNOWN Path** - Determines if this is an UNKNOWN client (no)
15. **Lookup Staging Folder** - Gets _Staging folder ID from registry
16. **Filter Staging Folder ID** - Extracts folder ID
17. **Check Routing Decision** - Validates folder ID exists
18. **Execute Chunk 1** - Processes PDF in staging folder

---

## Manual Testing Instructions

Since this is a Gmail trigger workflow, Sway must test manually:

### Step 1: Fix Critical Error First

Before testing, FIX the "Check Routing Decision" node error (see Critical Error section above).

### Step 2: Activate Workflow

1. Go to https://n8n.oloxa.ai/workflow/YGXWjWcBIk66ArvT
2. Toggle the workflow to ACTIVE
3. Confirm all credentials are properly connected (green checkmarks)

### Step 3: Send Test Email

**Test Case 1: NEW Client (Happy Path)**

Send an email to the Gmail account (aYzk7sZF8ZVyfOan) with:
- **Subject:** Test - NEW Client Villa Martens
- **Attachment:** A PDF file named "Villa_Martens_Invoice.pdf" or similar
- **Body:** (optional) Any text mentioning "Villa Martens"

**Expected Results:**
- Workflow executes successfully
- New folders created in Google Drive for "villa_martens"
- Client "villa_martens" written to Master Client Registry (Google Sheets)
- PDF moved to _Staging folder under "villa_martens"
- Chunk 0 sub-workflow executes
- Chunk 1 sub-workflow executes

**Test Case 2: UNKNOWN Client Path**

Send an email with:
- **Subject:** Test - UNKNOWN Client
- **Attachment:** A PDF with no clear client name
- **Body:** Ambiguous text without client name

**Expected Results:**
- Workflow executes UNKNOWN path
- PDF moved to "38_Unknowns" folder in Google Drive
- Email notification sent to Sway
- No registry entry created

### Step 4: Monitor Execution

1. Go to n8n UI > Executions tab
2. Find the most recent execution for workflow YGXWjWcBIk66ArvT
3. Click to view execution details
4. Check which nodes succeeded/failed
5. Look for credential errors (red nodes)

### Step 5: Validate Outputs

**For NEW client path:**
- Check Google Drive for new client folder structure
- Check Master Client Registry (Google Sheets) for new entry
- Confirm PDF was moved to _Staging folder
- Check execution logs for Chunk 0 and Chunk 1 sub-workflows

**For UNKNOWN path:**
- Check "38_Unknowns" folder in Google Drive for moved PDF
- Check email inbox for notification
- Confirm no registry entry was created

---

## Recommendations

### Before Testing
1. **FIX the critical error** in "Check Routing Decision" node (error output configuration)
2. **Update node versions** for If and Gmail nodes
3. **Add error handling** to Google Drive, Google Sheets, and OpenAI nodes
4. **Validate Google Sheets ranges** are in correct A1 notation

### During Testing
1. **Start with ONE test email** for NEW client path only
2. **Monitor execution in real-time** in n8n UI
3. **Check credential connections** before activating workflow
4. **Take screenshots** of any errors for debugging

### After Testing
1. **Document actual vs expected outcomes** for each test case
2. **Capture execution IDs** for successful and failed runs
3. **Report credential errors** separately from logic errors
4. **Test UNKNOWN path** separately after NEW path succeeds

---

## Test Status Summary

| Test Type | Status | Notes |
|-----------|--------|-------|
| Auto-test via MCP | NOT POSSIBLE | Gmail trigger workflow |
| Validation check | FAILED | 1 critical error, 42 warnings |
| Credential validation | NOT TESTED | Requires manual activation |
| NEW client path | NOT TESTED | Awaiting manual test |
| EXISTING client path | NOT TESTED | Not requested yet |
| UNKNOWN client path | NOT TESTED | Not requested yet |
| Chunk 0 sub-workflow | NOT TESTED | Dependent on parent workflow |
| Chunk 1 sub-workflow | NOT TESTED | Dependent on parent workflow |

---

## Next Steps

1. **solution-builder-agent** should fix the critical error in "Check Routing Decision" node
2. Sway should activate the workflow in n8n UI
3. Sway should send a test email with a NEW client PDF attachment
4. **test-runner-agent** can analyze the execution results after manual test completes

---

## Notes

- Workflow has NEVER been executed (0 executions in history)
- Workflow is currently INACTIVE (must be activated for testing)
- All 28 nodes are enabled (none disabled)
- No invalid connections detected (topology is correct)
- Error handling is minimal (most nodes will crash on error)

