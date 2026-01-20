# n8n Test Report – V4 Pre-Chunk 0: Intake & Client Identification

**Workflow ID:** 70n97A6OmYCsHMmV
**Test Date:** 2026-01-03
**Tester:** test-runner-agent
**Workflow Status:** Inactive

---

## Summary

- **Total tests analyzed:** 9 executions (IDs: 1-2, 22-28)
- **✅ Passed:** 0
- **❌ Failed:** 9
- **Critical Issue Found:** Workflow stops at "Filter PDF/ZIP Attachments" node

---

## Workflow Structure

### Trigger Mechanism
**Type:** Gmail Trigger (Poll-based)
- Monitors: Inbox for unread emails with attachments
- Filters: `INBOX`, `UNREAD`, `Label_4133960118153091049` (oloxa.ai label)
- Query: `has:attachment`
- Poll interval: Every minute

### Expected Flow
1. **Gmail Trigger** → Receive email with PDF/ZIP attachments
2. **Filter PDF/ZIP Attachments** → Extract only PDF/ZIP files
3. **Download Attachment** → Fetch attachment data
4. **Extract Text from PDF** → Convert PDF to text
5. **Evaluate Extraction Quality** → Check if OCR needed (< 10 words = scanned doc)
6. **AI Extract Client Name** → Use OpenAI to identify client
7. **Normalize Client Name** → Clean and format name (German chars, legal entities)
8. **Lookup Client Registry** → Check Google Sheet for existing client
9. **Check Client Exists** → Parse registry response
10. **Decision Gate** → Route based on:
    - No client identified → Handle Unidentified Client
    - Folders don't exist → Execute Chunk 0 (Create Folders)
    - Folders exist → Prepare for Chunk 3 (Classification)

### Current State
**Workflow is inactive** - Cannot be triggered by Gmail automatically until activated.

---

## Test Results

### Execution #28 (Most Recent Success)
- **Status:** ✅ SUCCESS (but incomplete)
- **Execution ID:** 28
- **Started:** 2026-01-02T19:49:20.548Z
- **Duration:** 27ms
- **Final Status:** success
- **Nodes Executed:** 2 / 13
- **Last Node:** Filter PDF/ZIP Attachments
- **Error:** None (workflow stopped normally with 0 outputs)

**Test Data:**
- Email ID: `19b6b8a02b18850a`
- Subject: "testing"
- From: sway@oloxa.ai
- Attachments detected: 2 PDFs
  - `Gesprächsnotiz zu Wie56 - Herr Owusu.pdf` (111 kB)
  - `2501_Casada_Kalku_Wie56.pdf` (61.4 kB)

**What Happened:**
- Gmail trigger successfully fetched email with attachments
- Attachments were stored in `binary.attachment_0` and `binary.attachment_1`
- Filter node returned 0 items (filtering failed)
- Workflow stopped - no further processing

---

### Execution #27
- **Status:** ❌ FAIL
- **Nodes Executed:** 1 / 13
- **Last Node:** Gmail Trigger
- **Issue:** Same as #28 - filter returned 0 items

---

### Execution #24
- **Status:** ❌ FAIL
- **Nodes Executed:** 2 / 13
- **Last Node:** Filter PDF/ZIP Attachments
- **Issue:** Same filtering problem

---

### Execution #2
- **Status:** ❌ FAIL
- **Nodes Executed:** 2 / 13
- **Test Data:** Email from Mina Beluga (swimming course invoice)
- **Issue:** Same filtering problem - 0 outputs from filter node

---

### Execution #1 (First Test - Failed)
- **Status:** ❌ FAIL (Error)
- **Error:** `Credential with ID "YOUR_GMAIL_CREDENTIAL_ID" does not exist`
- **Node:** Gmail Trigger
- **Root Cause:** Missing/invalid Gmail OAuth2 credentials
- **Notes:** Credentials were fixed after this - subsequent executions succeeded in triggering

---

## Root Cause Analysis

### Critical Bug: "Filter PDF/ZIP Attachments" Node

**Problem:** The filtering logic expects attachments in `item.json.attachments` array, but Gmail Trigger stores them in `binary` object.

**Current Code (Broken):**
```javascript
for (const item of items) {
  if (!item.json.attachments) continue;  // ❌ This field doesn't exist

  for (const attachment of item.json.attachments) {
    const filename = attachment.filename || attachment.name;
    // ...
  }
}
```

**Actual Data Structure:**
```json
{
  "json": {
    "id": "19b6b8a02b18850a",
    "subject": "testing"
    // NO attachments array here!
  },
  "binary": {
    "attachment_0": {
      "mimeType": "application/pdf",
      "fileName": "Gesprächsnotiz zu Wie56 - Herr Owusu.pdf",
      "fileSize": "111 kB"
    },
    "attachment_1": {
      "mimeType": "application/pdf",
      "fileName": "2501_Casada_Kalku_Wie56.pdf",
      "fileSize": "61.4 kB"
    }
  }
}
```

**Fix Required:**
The filter node must iterate over `item.binary` keys instead of `item.json.attachments`:

```javascript
for (const item of items) {
  if (!item.binary) continue;

  for (const [key, attachment] of Object.entries(item.binary)) {
    const filename = attachment.fileName;
    const ext = filename.toLowerCase().split('.').pop();

    if (['pdf', 'zip'].includes(ext)) {
      filtered.push({
        json: {
          emailId: item.json.id,
          emailSubject: item.json.Subject || item.json.subject,
          emailFrom: item.json.From || item.json.from,
          emailDate: item.json.date,
          attachmentKey: key,
          filename: filename,
          mimeType: attachment.mimeType,
          size: attachment.fileSize
        },
        binary: {
          data: attachment
        }
      });
    }
  }
}
```

---

## What Works

✅ **Gmail Trigger Configuration**
- Successfully polls Gmail inbox
- Correctly filters by labels (INBOX, UNREAD, oloxa.ai)
- Downloads attachments as binary data
- Handles authentication (after credentials were fixed)

✅ **Workflow Structure**
- Logical flow is well-designed
- Proper decision gates for routing
- Good separation of concerns (intake → identify → route)

✅ **Node Configuration**
- AI extraction node properly configured with OpenAI
- Client normalization handles German characters
- Registry lookup connected to correct Google Sheet

---

## What Doesn't Work

❌ **Critical: Attachment Filtering**
- Filter node incompatible with Gmail trigger's data structure
- Blocks entire workflow - nothing past node 2 can execute

❌ **Workflow Not Active**
- Cannot automatically process incoming emails
- Requires manual testing in n8n UI

❌ **Cannot Test End-to-End**
- Unable to verify client name extraction
- Cannot confirm folder creation trigger
- Cannot validate registry lookup/update

---

## Recommendations

### Immediate Fixes Required

1. **Fix Filter Node** (CRITICAL - Priority 1)
   - Update "Filter PDF/ZIP Attachments" code to read from `binary` object
   - Test with real email data to confirm attachments are extracted

2. **Update Download Attachment Node** (Priority 2)
   - Currently expects `attachmentId` from filtered data
   - May need adjustment to work with binary data already in payload

3. **Activate Workflow** (Priority 3)
   - Once filter is fixed, activate workflow for automatic processing
   - Monitor first few real executions

### Testing Strategy

**After Filter Fix:**
1. **Manual Test with Pinned Data**
   - Use execution #28's email data
   - Pin it to Gmail trigger node
   - Execute workflow manually
   - Verify it reaches "AI Extract Client Name" node

2. **End-to-End Test with Real Email**
   - Send test email with known PDF (e.g., test client "ACME GmbH")
   - Monitor execution through all nodes
   - Verify:
     - Client name extracted correctly
     - Registry lookup works
     - Correct routing (create folders vs. existing client)

3. **Edge Case Tests**
   - Scanned PDF (requires OCR)
   - No client name found
   - Existing client in registry

---

## Data Flow to Chunk 0

**Expected Output (when working):**
```json
{
  "client_name": "ACME Immobilien GmbH",
  "client_normalized": "acme_immobilien",
  "parent_folder_id": "1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm"
}
```

**Current Output:** None (workflow stops at node 2)

---

## Configuration Details

### Gmail Credentials
- **Status:** ✅ Working (after initial fix)
- **Credential ID:** `aYzk7sZF8ZVyfOan`
- **Name:** "Gmail account"

### OpenAI Credentials
- **Status:** Unknown (not tested - workflow doesn't reach this node)
- **Credential ID:** `xmJ7t6kaKgMwA1ce`
- **Name:** "OpenAi account"

### Google Sheets Registry
- **Document ID:** `1T-jL-jLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI`
- **Sheet:** "Sheet1"
- **Credential ID:** `VdNWQlkZQ0BxcEK2` (Google Service Account)

### Parent Folder for Clients
- **Google Drive Folder ID:** `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm`

---

## Conclusion

**Workflow Status:** ❌ NOT FUNCTIONAL

The V4 Pre-Chunk 0 workflow is well-designed but **cannot process any emails** due to a critical bug in the attachment filtering node. The node expects attachments in a JSON array structure that doesn't match the Gmail trigger's actual output format (binary data).

**To make this workflow operational:**
1. Fix the filter node to read from `item.binary`
2. Test with pinned data to verify fix
3. Activate workflow for automatic processing

Until the filter is fixed, the workflow cannot:
- Extract client names from PDFs
- Create folder structures
- Route documents to Chunk 0 or Chunk 3

**Next Steps:**
- Apply the fix outlined in "Root Cause Analysis"
- Re-run tests with execution #28's data
- Validate full workflow end-to-end
