# Pre-Chunk 0 Workflow - Manual Import Instructions

**Date**: 2026-01-06
**Status**: Ready for import
**File**: `/Users/swayclarke/coding_stuff/PRE_CHUNK_0_IMPORT.json`

---

## Quick Start

**Your solution**: "how about you just give me the json and i manually upload it?" ✅

The JSON is ready. Follow these 6 steps to import and activate the workflow.

---

## Step-by-Step Import

### 1. Open n8n UI
Navigate to: https://n8n.oloxa.ai

---

### 2. Import Workflow

**Option A - Import from File** (Recommended):
1. Click "+" button in top right corner
2. Select "Import from File"
3. Browse to `/Users/swayclarke/coding_stuff/PRE_CHUNK_0_IMPORT.json`
4. Click "Import"

**Option B - Paste JSON**:
1. Create new workflow
2. Click "..." menu → "Import from URL"
3. Or open workflow code editor and paste JSON content

---

### 3. Re-link Credentials

n8n will prompt you to connect credentials for these nodes:

**Gmail OAuth2** (2 nodes):
- "Gmail Trigger - Unread with Attachments"
- "Send Email - Processing Failure"

**Google Drive OAuth2** (4 nodes):
- "Upload PDF to Temp Folder"
- "Download Original PDF"
- "Move to 38_Unknowns Folder"
- "Move File to Client Folder"

**Google Sheets OAuth2** (2 nodes):
- "Lookup Client Registry"
- "Lookup Client Folder IDs"

**OpenAI API** (1 node):
- "AI Extract Client Name"

**To re-link**:
- Click node with red credential warning
- Select existing credential OR create new one
- Save node

---

### 4. Verify Workflow Structure

**Check these components exist**:

✅ **29 nodes total**, including:
- Gmail Trigger (polls every minute)
- Extract Text from PDF
- AI Extract Client Name (OpenAI)
- Check Client Exists
- Normalize Client Name
- Lookup Folder IDs
- Filter Staging Folder ID
- **Error handling nodes** (Check Routing Decision, Prepare Missing Folder Error)
- Execute Chunk 0 (for new clients)
- Execute Chunk 1 (for existing clients)
- Move to 38_Unknowns (for unknown clients)
- **Evaluate Extraction Quality** (Phase 1 modification - adds extractedText fields)

✅ **30 connections** between nodes

✅ **Settings**: Execution order = v1

---

### 5. Save Workflow

1. Click "Save" button in top right
2. Name: **"AMA Pre-Chunk 0: Intake & Client Identification"**
3. Confirm save

---

### 6. Activate Workflow

1. Toggle "Active" switch in top right (OFF → ON)
2. Verify switch turns green
3. Gmail trigger should start polling within 1 minute

**What activation does**:
- Enables Gmail polling every minute
- Checks for unread emails with attachments
- Filters by label: "AMA Property Docs"
- Processes PDFs automatically

---

## Testing the Workflow

### Send Test Email

**To**: Your monitored Gmail account (the one with n8n access)
**Subject**: Test - Phase 2 Verification
**Attachment**: Any PDF document (real estate document preferred)
**From**: Any email address

### Expected Behavior

**Within 1-2 minutes**:
1. Gmail trigger detects new email
2. Workflow extracts PDF text
3. AI identifies client name from PDF content
4. Workflow normalizes name and checks registry

**Successful execution should**:
- Identify client from PDF (e.g., "CASADA" → "casada")
- Route to appropriate path:
  - **NEW client** → Execute Chunk 0 (create folders)
  - **EXISTING client** → Execute Chunk 1 (move to staging)
  - **UNKNOWN client** → Move to 38_Unknowns folder
  - **Missing staging folder** → Move to 38_Unknowns (graceful error handling)

### Check Execution Results

1. Go to n8n executions tab
2. Find latest execution (should appear within 2 minutes of sending email)
3. Click execution to see node-by-node results
4. **Verify Phase 1 fields exist**:
   - `extractedText`: Full PDF text content
   - `textLength`: Character count
   - `extractionMethod`: "digital_pre_chunk"

---

## What's Included in This Import

### Phase 1 Modifications ✅
**Node**: "Evaluate Extraction Quality"
**Added**: 3 lines to keep extracted text for downstream reuse
```javascript
extractedText: extractedText,
textLength: extractedText.trim().length,
extractionMethod: 'digital_pre_chunk'
```

### Error Handling Fixes ✅
**Node**: "Filter Staging Folder ID"
**Changed**: Returns error flags instead of throwing errors
**Added nodes**:
- "Check Routing Decision" (IF node)
- "Prepare Missing Folder Error" (Code node)

**Graceful handling**: Files with missing staging folders route to 38_Unknowns instead of blocking execution

### All Workflow Logic ✅
- Client name extraction (AI with regex fallback)
- German text normalization (ä→ae, ö→oe, ü→ue, ß→ss)
- Client registry lookup
- Folder ID lookup
- NEW/EXISTING/UNKNOWN routing
- Error recovery paths
- Chunk 0 execution (folder creation)
- Chunk 1 execution (file staging)

---

## Troubleshooting

### Import Fails
**Error**: "Invalid workflow JSON"
- Verify file downloaded completely
- Check JSON syntax (should start with `{` and end with `}`)
- Try Option B (paste JSON manually)

### Credentials Won't Link
**Error**: "OAuth credentials invalid"
- Go to n8n Settings → Credentials
- Create new credentials for the service
- Re-authenticate OAuth flow
- Return to workflow and select new credential

### Workflow Won't Activate
**Error**: "Workflow cannot be activated"
- Check all nodes have credentials linked (no red warnings)
- Verify Gmail trigger has valid OAuth2 connection
- Check executions tab for validation errors

### No Execution After Test Email
**Possible causes**:
1. **Workflow not active** → Check toggle is green
2. **Email label missing** → Add "AMA Property Docs" label to test email
3. **Email already read** → Trigger only fires on UNREAD emails
4. **No PDF attachment** → Trigger requires PDF attachment
5. **Gmail polling delay** → Wait 2-3 minutes for poll cycle

---

## Next Steps After Successful Import

### Immediate
1. ✅ Verify workflow accessible in n8n UI
2. ✅ Activate workflow
3. ✅ Send test email
4. ✅ Confirm execution appears

### Phase 2 Testing
Once Pre-Chunk 0 is active and processing emails:
1. Test Chunk 1 → Chunk 2 integration
2. Verify pass-through fields (extractedText, textLength, extractionMethod)
3. Verify error handling (missing staging folders route to 38_Unknowns)
4. Proceed to Phase 3 (AWS Textract OCR configuration)

---

## Why Manual Import Works

**Problem**: n8n v2.1.4 API/UI compatibility bug
- Workflows modified via API can't be rendered in UI
- JavaScript error: "propertyValues[itemName] is not iterable"

**Solution**: Import in UI bypasses API entirely
- UI creates workflow with compatible parameter structures
- No JavaScript rendering errors
- Guaranteed to be accessible after import
- n8n assigns fresh workflow ID automatically

**This workaround is faster and simpler than recreating 29 nodes manually!**

---

## Files Referenced

- **Import JSON**: `/Users/swayclarke/coding_stuff/PRE_CHUNK_0_IMPORT.json`
- **Critical Blocker Summary**: `/Users/swayclarke/coding_stuff/CRITICAL_BLOCKER_SUMMARY.md`
- **Phase 2 Status**: `/Users/swayclarke/coding_stuff/tests/phase-2-status.md`
- **Implementation Plan**: `/Users/swayclarke/.claude/plans/fuzzy-watching-muffin.md`

---

**Last Updated**: 2026-01-06T00:24:30+01:00
**Status**: Ready for import
**Next Action**: Sway imports and activates workflow
