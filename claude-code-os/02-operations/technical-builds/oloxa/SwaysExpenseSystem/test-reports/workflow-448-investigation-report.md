# Workflow Execution 448 Investigation Report
## Villa Martens File Movement Issue

**Date:** 2026-01-06
**Workflow:** AMA Pre-Chunk 0: Intake & Client Identification (6MPoDSf8t0u8qXQq)
**Execution ID:** 448
**Timestamp:** 19:29:26 - 19:29:35 (9 seconds duration)
**Status:** Success (but incomplete)

---

## Executive Summary

**Problem:** Villa Martens PDF file was not moved to the staging folder despite successful workflow execution.

**Root Cause:** The workflow execution STOPPED prematurely at the "Route by Client Status" node (node 12 of 28). The NEW path was identified correctly, but **no downstream nodes after the routing switch executed**.

**Critical Finding:** The "Lookup Client Registry" node returned an **empty result** ({}), causing the workflow to treat Villa Martens as a NEW client instead of EXISTING, even though the client was previously in the registry (as evidenced by execution 446).

---

## Detailed Findings

### 1. Path Determination

**Execution 448:**
- Client Name Extracted: "Villa Martens"
- Client Normalized: "villa_martens"
- Registry Lookup Result: **EMPTY ({})**
- Client Status Determined: **NEW**
- Routing Decision: NEW path (output 0)

**Execution 446 (previous run):**
- Client Name Extracted: "Villa Martens"
- Client Normalized: "villa_martens"
- Registry Lookup Result: **FOUND**
- Client Status Determined: **EXISTING**
- Staging Folder ID: 1-Vhtms-hGinDYAEuVLzSLrBQFWVJ6I1H

### 2. Workflow Execution Flow

**Nodes That Executed (12 total):**
1. Gmail Trigger - Unread with Attachments
2. Filter PDF/ZIP Attachments
3. Upload PDF to Temp Folder
4. Extract File ID & Metadata
5. Download PDF from Drive
6. Extract Text from PDF
7. Evaluate Extraction Quality
8. AI Extract Client Name
9. Normalize Client Name
10. Lookup Client Registry ← **RETURNED EMPTY**
11. Check Client Exists ← **Set status to NEW**
12. Route by Client Status ← **EXECUTION STOPPED HERE**

**Nodes That DID NOT Execute:**
- Merge File + Client Data (NEW)
- Execute Chunk 0 - Create Folders
- Send Email - New Client Notification
- Mark Email as Read (NEW)
- Lookup Staging Folder
- Execute Chunk 1 - Move to Staging (NEW)
- (All subsequent NEW path nodes)

### 3. File Information

**File Details:**
- File ID: 1PM9ZoTbFq0LTWcSSmJwiHjIFb_6jLX_-
- Filename: OCP-Anfrage-AM10.pdf
- Location: 1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm (Temp folder)
- Size: 1.95 MB
- Email ID: 19b94c8320ba19c0

**File Status:** The file is still in the temp folder and was **NOT moved** to any staging or client folder.

### 4. Client Registry Lookup Issue

**"Lookup Client Registry" Node Configuration:**
```json
{
  "documentId": "1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI",
  "sheetName": 762792134 (Client_Registry),
  "options": {},
  "alwaysOutputData": true
}
```

**Result:** Empty object `{}`

**Possible Causes:**
1. Villa Martens entry was **deleted from the Client Registry** between execution 446 and 448
2. The Google Sheets lookup failed silently
3. The Client_Normalized field value changed in the registry
4. The registry sheet structure changed

---

## Why the Workflow Stopped at the Switch Node

**Expected Behavior:**
When the Switch node routes to NEW output, the "Merge File + Client Data (NEW)" node should execute next.

**Actual Behavior:**
The workflow marked itself as "success" but stopped after 12 nodes, leaving 16 nodes unexecuted.

**Likely Causes:**
1. **n8n Switch Node Behavior**: When trigger-based workflows have connections to named outputs (NEW, EXISTING, UNKNOWN), n8n may not continue execution if there's an issue with node availability or activation state
2. **Workflow Validation Issue**: One of the downstream nodes may have had a configuration error that prevented execution
3. **n8n Internal Issue**: The workflow engine may have encountered an error but marked the execution as "success" anyway
4. **Timing Issue**: The workflow may have been deactivated/reactivated during execution

**Evidence:**
- Execution status: "success"
- Execution finished: true
- Duration: 8471ms (normal)
- No error messages in any node
- All 12 executed nodes completed successfully

---

## Impact Assessment

### What Happened:
1. File uploaded to temp folder: **SUCCESS**
2. Client identified as "Villa Martens": **SUCCESS**
3. Registry lookup: **FAILED (empty result)**
4. Routed to NEW path: **SUCCESS**
5. NEW path execution: **FAILED (nodes never ran)**
6. File moved to staging: **FAILED (never attempted)**

### What Should Have Happened (NEW Path):
1. Merge File + Client Data (NEW)
2. Execute Chunk 0 - Create Folders (workflow zbxHkXOoD1qaz6OS)
3. Send Email - New Client Notification
4. Mark Email as Read (NEW)
5. Lookup Staging Folder
6. Execute Chunk 1 - Move to Staging (NEW) (workflow djsBWsrAEKbj2omB)

### What Should Have Happened (EXISTING Path - if registry had worked):
1. Merge File + Client Data (EXISTING)
2. Send Email - Existing Client
3. Mark Email as Read (EXISTING)
4. Execute Chunk 1 - Move to Staging (EXISTING) (workflow djsBWsrAEKbj2omB)

---

## Recommendations

### Immediate Actions:

1. **Check Client Registry**
   - Open spreadsheet: `1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI`
   - Verify Villa Martens entry exists in Client_Registry sheet
   - Confirm Client_Normalized field = "villa_martens"
   - Confirm Staging_Folder_ID field = "1-Vhtms-hGinDYAEuVLzSLrBQFWVJ6I1H"

2. **Manually Move the File**
   - File ID: 1PM9ZoTbFq0LTWcSSmJwiHjIFb_6jLX_-
   - Destination: Villa Martens staging folder (1-Vhtms-hGinDYAEuVLzSLrBQFWVJ6I1H)

3. **Test the Workflow Again**
   - Send another test email with a Villa Martens PDF
   - Monitor execution to see if it completes all nodes
   - Check if NEW path nodes execute this time

### Root Cause Investigation:

1. **Debug the Switch Node Issue**
   - Check if there are any validation errors in downstream nodes
   - Verify all downstream nodes are properly connected
   - Test the workflow in n8n's UI manually to see if it completes

2. **Debug the Registry Lookup**
   - Test the "Lookup Client Registry" node in isolation
   - Verify Google Sheets API connection is working
   - Check if the sheet permissions are correct

3. **Consider Workflow Architecture Change**
   - The current behavior (stopping at Switch node) is problematic
   - Consider adding error handling after the Switch node
   - Add logging nodes to track execution flow

---

## Next Steps for Sway

1. Open the Client Registry Google Sheet and verify Villa Martens entry exists
2. Manually move file 1PM9ZoTbFq0LTWcSSmJwiHjIFb_6jLX_- to the staging folder
3. Check if the NEW path nodes have any configuration errors in n8n UI
4. Run another test to see if the issue reproduces

---

## Key Takeaway

**The file is not in the staging folder because the workflow execution stopped prematurely at the routing node, before any file movement nodes could execute. This appears to be an n8n workflow engine issue rather than a logic problem, since the execution was marked as "success" despite only running 12 of 28 nodes.**
