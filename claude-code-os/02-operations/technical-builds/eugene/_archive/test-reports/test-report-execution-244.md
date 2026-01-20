# n8n Test Report - Pre-Chunk 0 Execution #244

## Summary
- Total tests: 3
- PASS: 0
- FAIL: 3

## Test Execution Details

### Test 1: Merge Binary + Metadata Node Combines Data
- Status: FAIL
- Execution ID: 244
- Workflow: V4 Pre-Chunk 0: Intake & Client Identification (70n97A6OmYCsHMmV)
- Final status: success
- Failed at node: Merge Binary + Metadata
- Expected: Node should combine binary PDF data from "Filter PDF/ZIP Attachments" with metadata from "Filter Staging Folder ID"
- Actual: Node did NOT execute in this workflow run (appears in structure but not in execution data)

**Evidence:**
- "Filter PDF/ZIP Attachments" output contained binary data:
  - `binary.data.fileName`: "OCP-Anfrage-AM10.pdf"
  - `binary.data.fileSize`: "1.95 MB"
  - `binary.data.mimeType`: "application/pdf"
- "Filter Staging Folder ID" output contained metadata:
  - `client_normalized`: "villa_martens"
  - `staging_folder_id`: "1HdqcfWMNIhapjvm3-gPBybL5Tp064Yjm"
- "Merge Binary + Metadata" node shows 0 items executed in execution #244

---

### Test 2: Execute Chunk 1 Receives Binary + JSON Data
- Status: FAIL
- Execution ID: 244 (Pre-Chunk 0) → 248 (Chunk 1)
- Workflow: Chunk 1: Email to Staging (Document Organizer V4) (djsBWsrAEKbj2omB)
- Final status: success
- Failed at node: Execute Chunk 1 / IF Has Attachments
- Expected: Execute Chunk 1 should receive both binary PDF data AND JSON metadata (client_normalized, staging_folder_id)
- Actual: Execute Chunk 1 received ONLY JSON metadata, NO binary data

**Evidence from Chunk 1 Execution #248:**
- Input to "IF Has Attachments" node:
  - `hasAttachments`: false (WRONG - should be true)
  - `attachmentCount`: 0 (WRONG - should be 1)
  - `binary`: {} (EMPTY - should contain PDF data)
  - `client_normalized`: "villa_martens" (CORRECT)
  - `staging_folder_id`: "1HdqcfWMNIhapjvm3-gPBybL5Tp064Yjm" (CORRECT)

**Root Cause:**
The "Merge Binary + Metadata" node in Pre-Chunk 0 is configured but appears to NOT be executing or NOT properly passing binary data through to the Execute Workflow node.

---

### Test 3: PDF Uploaded to Staging Folder (Google Drive)
- Status: FAIL
- Execution ID: 248
- Workflow: Chunk 1: Email to Staging (Document Organizer V4)
- Expected Google Drive Folder ID: 1HdqcfWMNIhapjvm3-gPBybL5Tp064Yjm (Villa Martens staging)
- Expected: PDF "OCP-Anfrage-AM10.pdf" should be uploaded to staging folder
- Actual: NO UPLOAD occurred because workflow took the "no attachments" branch

**Evidence:**
- "IF Has Attachments" node output went to output[1] (false branch)
- No execution of "Upload to Staging" node in execution #248
- Workflow completed successfully but skipped all file upload logic

---

## Workflow Chain Analysis

**Complete execution chain for #244:**

1. **Pre-Chunk 0 (70n97A6OmYCsHMmV) - Execution #244**
   - Started: 2026-01-04T14:12:40.756Z
   - Stopped: 2026-01-04T14:14:53.261Z
   - Duration: 132505ms (2.2 minutes)
   - Status: success

2. **Chunk 0 (zbxHkXOoD1qaz6OS) - Execution #245**
   - Started: 2026-01-04T14:12:43.727Z
   - Stopped: 2026-01-04T14:13:47.112Z
   - Duration: 63385ms (1 minute)
   - Status: success
   - Purpose: Created folder structure for new client

3. **Chunk 1 (djsBWsrAEKbj2omB) - Execution #246**
   - Started: 2026-01-04T14:13:48.198Z
   - Stopped: 2026-01-04T14:13:48.582Z
   - Duration: 384ms
   - Status: success
   - Result: Skipped attachment upload (hasAttachments: false)

4. **Chunk 1 (djsBWsrAEKbj2omB) - Execution #248**
   - Started: 2026-01-04T14:14:52.863Z
   - Stopped: 2026-01-04T14:14:53.246Z
   - Duration: 383ms
   - Status: success
   - Result: Skipped attachment upload (hasAttachments: false)

---

## Critical Issue Identified

**Problem:** The "Merge Binary + Metadata" node is NOT passing binary data to the Execute Workflow node.

**Workflow Connection Issue:**
Looking at Pre-Chunk 0 workflow structure:
- "Filter PDF/ZIP Attachments" → "Merge Binary + Metadata" (input 1)
- "Filter Staging Folder ID" → "Merge Binary + Metadata" (input 2)
- "Merge Binary + Metadata" → "Execute Chunk 1"

**Hypothesis:**
The Merge node may be configured incorrectly, OR the Execute Workflow node may not support binary data passthrough in n8n.

**Node Configuration:**
- Merge node type: `n8n-nodes-base.merge`
- Mode: `combine`
- Combine by: `combineByPosition`

**Possible Root Causes:**
1. Merge node's "combineByPosition" may not preserve binary data from input 1
2. Execute Workflow node may strip binary data when passing to sub-workflow
3. Timing issue - binary data from "Filter PDF/ZIP Attachments" may not be available when Merge executes (different execution path)

**Critical Path Issue:**
Looking at the workflow structure, there's a MAJOR routing problem:
- "Filter PDF/ZIP Attachments" runs EARLY in the workflow (position 336, 480)
- "Filter Staging Folder ID" runs LATE in the workflow (position 2800, 384)
- The binary data from early in the workflow may be LOST by the time it reaches the Merge node

The workflow routes like this:
1. Gmail Trigger → Filter PDF/ZIP Attachments (binary data created here)
2. Filter PDF/ZIP → Extract Text from PDF → ... → Decision Gate → Lookup Staging Folder → Filter Staging Folder ID
3. Filter Staging Folder ID → Merge Binary + Metadata

By the time execution reaches "Merge Binary + Metadata", the binary data from "Filter PDF/ZIP Attachments" is no longer in the execution context because it went through the text extraction path, NOT directly to the merge node.

---

## Recommended Fix

The workflow needs to PRESERVE binary data throughout the execution path. Options:

1. **Pass binary data alongside text extraction:**
   - Modify "Extract Text from PDF" and subsequent nodes to preserve `item.binary` in their outputs
   - Ensure all Code nodes in the chain include `binary: item.binary` in their return statements

2. **Parallel path for binary data:**
   - Keep binary data in a separate parallel branch
   - Use Merge node AFTER both paths complete

3. **Store binary in staging earlier:**
   - Upload PDF to staging folder immediately after "Filter PDF/ZIP Attachments"
   - Pass only the Google Drive file ID to Chunk 1
   - Chunk 1 retrieves the file from staging by ID

**Most Reliable Solution:** Option 3 - Upload PDF to staging in Pre-Chunk 0, pass file ID to Chunk 1.

---

## Test Files & Resources

**Workflows Tested:**
- Pre-Chunk 0: V4 Pre-Chunk 0: Intake & Client Identification (70n97A6OmYCsHMmV)
- Chunk 0: Chunk 0: Folder Initialization (V4 - Parameterized) (zbxHkXOoD1qaz6OS)
- Chunk 1: Chunk 1: Email to Staging (Document Organizer V4) (djsBWsrAEKbj2omB)

**Test Email:**
- From: swayfromthehook@gmail.com
- Subject: Test Email from AMA with PDF Attachment - Document Organizer V4
- Email ID: 19b895a37235af7b
- Attachment: OCP-Anfrage-AM10.pdf (1.95 MB)

**Client Identified:**
- Raw name: Villa Martens (or similar)
- Normalized: villa_martens
- Status: EXISTING client
- Staging folder ID: 1HdqcfWMNIhapjvm3-gPBybL5Tp064Yjm

**Google Drive Staging Folder:**
- Expected folder ID: 1HdqcfWMNIhapjvm3-gPBybL5Tp064Yjm
- Status: NOT CHECKED (cannot verify upload because upload never occurred)

---

## Final Verdict

**COMPLETE WORKFLOW CHAIN: FAIL**

All three test conditions failed:
1. Merge Binary + Metadata - FAIL (binary data not preserved)
2. Execute Chunk 1 receives binary + json - FAIL (only json received)
3. PDF uploaded to staging - FAIL (no upload occurred)

The workflow successfully identified the client and created folder structure, but the core functionality of uploading the PDF attachment completely failed due to binary data loss in the execution chain.
