# Manual Testing Guide - Document Organizer V4
## Autonomous Testing System Validation

**Created:** 2026-01-08
**Version:** 1.0
**Status:** ⚠️ BLOCKED by critical bug (see Prerequisites)

---

## ⚠️ BEFORE YOU START - CRITICAL BUG FIX REQUIRED

**Testing is BLOCKED until Chunk 2 file lifecycle bug is fixed.**

### The Bug
Chunk 2 tries to download a PDF using a file ID that no longer exists because Pre-Chunk 0 already moved it to staging.

### The Fix (Required Before Testing)

**Step 1: Open Chunk 2 Workflow in n8n**
- URL: https://n8n.oloxa.ai/workflow/g9J5kjVtqaF9GLyc
- Workflow: "AMA Chunk 2 - Document Classification"

**Step 2: Modify "Normalize Input" Node**

Find this code block:
```javascript
const extractedText = item.extractedText || '';
```

Replace with:
```javascript
const extractedText = item.extractedText || '';
const hasExtractedText = extractedText.trim().length > 100;
const skipDownload = hasExtractedText && item.fileId;
```

Then in the return statement, add:
```javascript
return [{
  json: {
    fileId: item.fileId,
    fileName: item.name,
    extractedText: hasExtractedText ? extractedText : null,
    skipDownload: skipDownload,  // NEW FIELD
    // ... rest of existing fields
  }
}];
```

**Step 3: Add IF Node After "Normalize Input"**

Add new IF node:
- Name: "Check Skip Download"
- Condition: `{{ $json.skipDownload }}` equals `true`

**Routing:**
- **TRUE branch** → Connect to "Detect Scan vs Digital" node (skip download)
- **FALSE branch** → Connect to "Download PDF" node (original path)

**Step 4: Update "Download PDF" Node Connections**
- Original: "Normalize Input" → "Download PDF"
- New: "Check Skip Download" (FALSE) → "Download PDF"

**Step 5: Save and Test**
- Click "Save" in n8n
- Send test email to verify fix works

---

## Prerequisites

### 1. Activate Email Sender Workflow
⚠️ **Must be done manually in n8n UI** (API activation failed)

1. Go to: https://n8n.oloxa.ai/workflow/8l1ZxZMZvoWISSkJ
2. Click the toggle switch to **ACTIVE**
3. Verify webhook URL appears: `https://n8n.oloxa.ai/webhook/ama-send-test-email`

### 2. Verify Workflow Status
All workflows should be ACTIVE:
- ✅ Pre-Chunk 0: `YGXWjWcBIk66ArvT` - ACTIVE
- ✅ Chunk 0: `zbxHkXOoD1qaz6OS` - ACTIVE
- ✅ Chunk 2: `g9J5kjVtqaF9GLyc` - ACTIVE (after bug fix)
- ⚠️ Email Sender: `8l1ZxZMZvoWISSkJ` - Must activate manually
- ✅ Test Orchestrator: `nUgGCv8d073VBuP0` - ACTIVE

### 3. Access Test Documents
- **Location:** Google Drive folder `dummy_files`
- **Folder ID:** `1GG_OCKvT1ivR0F-uIVq0b1jhHreWg1Kh`
- **Link:** https://drive.google.com/drive/folders/1GG_OCKvT1ivR0F-uIVq0b1jhHreWg1Kh
- **Clients:** Adolf-Martens-Straße, Propos-Menrad

---

## Test Plan Overview

### Layer 1: Simulated Testing (Fast)
- **Purpose:** Validate chunk logic with simulated data
- **Speed:** 5-10 seconds per test
- **How:** Bypass Gmail trigger, pass data directly to chunk
- **Status:** NOT IMPLEMENTED YET (requires test-runner-agent)

### Layer 2: Real Email Testing (Full Chain)
- **Purpose:** Validate end-to-end flow with real Gmail trigger
- **Speed:** 30-60 seconds per test
- **How:** Send real email with PDF attachment → Pre-Chunk 0 → Chunk 0 → Chunk 2
- **Status:** READY (after bug fix + Email Sender activation)

---

## Manual Test Execution

### Test 1: End-to-End Email Test (Recommended First Test)

**What This Tests:**
- Pre-Chunk 0: Email receipt, PDF upload, text extraction, client identification
- Chunk 0: Client folder creation (or existing client detection)
- Chunk 2: Document classification with extracted text (no re-download)

**Test Case:** TC_CHUNK2_EXPOSE_ADM10
- **File:** `ADM10_Exposé.pdf`
- **File ID:** `1SaAnbMGcyZgLkmYC4KZJyI9gN26N_l7L`
- **Expected Classification:** `01_PROJEKTBESCHREIBUNG`
- **Expected Confidence:** >= 0.9
- **Client:** `adolf_martens_strasse`

**Steps:**

1. **Download Test PDF from Drive:**
   - Navigate to: https://drive.google.com/file/d/1SaAnbMGcyZgLkmYC4KZJyI9gN26N_l7L/view
   - Download `ADM10_Exposé.pdf` to your computer

2. **Send Email with Attachment:**
   - **From:** swayfromthehook@gmail.com (your Gmail)
   - **To:** swayclarkeii@gmail.com (target Gmail)
   - **Subject:** `Test Exposé Adolf-Martens-Straße`
   - **Body:** Any text (e.g., "Testing document classification")
   - **Attachment:** `ADM10_Exposé.pdf`
   - **IMPORTANT:** Email must be sent to Gmail account monitored by n8n

3. **Wait for Processing:**
   - Expected time: 30-60 seconds
   - n8n will:
     - Detect new email
     - Download PDF attachment
     - Upload to temp folder in Drive
     - Extract text from PDF
     - Identify client name using AI
     - Execute Chunk 0 (create/verify folder structure)
     - Move PDF to staging folder
     - Execute Chunk 2 (classify document)
     - Mark email as read

4. **Check Execution Results:**

   **Option A: n8n UI (Visual)**
   - Go to: https://n8n.oloxa.ai/workflow/YGXWjWcBIk66ArvT
   - Click "Executions" tab
   - Find most recent execution (should be within last minute)
   - Click to expand
   - Check each node for success/failure:
     - ✅ "Gmail Trigger" - Email received
     - ✅ "Upload to Temp Folder" - PDF uploaded
     - ✅ "Extract Text from PDF" - Text extracted
     - ✅ "Identify Client Name" - AI identified client
     - ✅ "Execute Chunk 0" - Folder structure created
     - ✅ "Move PDF to Staging" - File moved
     - ✅ "Execute Chunk 2" - Document classified
     - ✅ "Mark Email as Read" - Email processed

   **Option B: API Query**
   ```bash
   # Get latest execution
   curl -s "https://n8n.oloxa.ai/api/v1/executions?limit=1&workflowId=YGXWjWcBIk66ArvT" \
     -H "X-N8N-API-KEY: n8n_api_5efc21c88cdcb87a341f3d02e47ae265f2a7092c0fa74b1f0dfe632bf89ac9ba" \
     | jq '.[0]'
   ```

5. **Validate Chunk 2 Output:**

   Look for Chunk 2 output in execution data:
   ```json
   {
     "documentType": "01_PROJEKTBESCHREIBUNG",
     "confidence": 0.95,
     "extractionMethod": "digital",
     "reasoning": "Exposé contains project description..."
   }
   ```

   **Expected Values:**
   - `documentType`: `01_PROJEKTBESCHREIBUNG`
   - `confidence`: >= 0.9
   - `extractionMethod`: `digital`

   **✅ PASS Criteria:**
   - All nodes executed successfully
   - Chunk 2 classified correctly
   - Confidence >= 0.9
   - No errors in execution log

   **❌ FAIL Scenarios:**
   - Chunk 2 returns 404 error → Bug fix not applied correctly
   - Wrong documentType → Classification logic issue
   - Low confidence (<0.9) → Prompt engineering issue
   - Execution stopped early → Check error node output

6. **Verify Google Drive Structure:**

   Navigate to Drive:
   - **Folder:** `Adolf-Martens-Straße` (or `adolf_martens_strasse`)
   - **Subfolder:** `_Staging`
   - **File:** `ADM10_Exposé.pdf` should be present

   **Expected structure:**
   ```
   AMA_Capital_Pipeline/
   └── Adolf-Martens-Straße/
       └── _Staging/
           └── ADM10_Exposé.pdf
   ```

---

### Test 2: Email Sender Workflow Test (Layer 2)

**What This Tests:**
- Programmatic email sending via webhook
- Email delivery to Gmail
- Workflow execution monitoring
- Result validation and logging

**Note:** This test bypasses Pre-Chunk 0 and tests Chunk 2 directly using Email Sender workflow.

**Steps:**

1. **Trigger Email Sender via Webhook:**

   ```bash
   curl -X POST "https://n8n.oloxa.ai/webhook/ama-send-test-email" \
     -H "Content-Type: application/json" \
     -d '{
       "test_case_id": "TC_CHUNK2_EXPOSE_ADM10",
       "pdf_file_id": "1SaAnbMGcyZgLkmYC4KZJyI9gN26N_l7L",
       "pdf_file_name": "ADM10_Exposé.pdf",
       "target_chunk": "2"
     }'
   ```

2. **What Happens:**
   - Email Sender downloads PDF from Drive
   - Sends email to swayclarkeii@gmail.com with PDF attached
   - Waits 15 seconds for Pre-Chunk 0 to process
   - Queries n8n API for execution results
   - Validates Chunk 2 output against expected values
   - Logs results to `Layer_2_Tests` sheet

3. **Check Results:**

   **Option A: Google Sheets**
   - Open Status Tracker: https://docs.google.com/spreadsheets/d/1af9ZsSm5IDVWIYb5IMX8ys8a5SUUnQcb77xi9tJQVo8
   - Go to "Layer_2_Tests" tab
   - Check most recent row for test results

   **Option B: n8n UI**
   - Go to: https://n8n.oloxa.ai/workflow/8l1ZxZMZvoWISSkJ
   - Check "Executions" tab
   - View validation results in "Validate Chunk Output" node

4. **Expected Result:**
   ```json
   {
     "test_case_id": "TC_CHUNK2_EXPOSE_ADM10",
     "target_chunk": "2",
     "passed": true,
     "validations": {
       "hasDocumentType": true,
       "hasConfidence": true,
       "confidenceThreshold": true
     },
     "output": {
       "documentType": "01_PROJEKTBESCHREIBUNG",
       "confidence": 0.95
     }
   }
   ```

---

### Test 3: Additional Test Cases

Once Test 1 passes, run these additional test cases to validate different document types:

#### Test Case 2: Building Description (Baubeschreibung)
- **File ID:** `1gr8b69ZbRtyB1JB4xk9qlH_cNV7hzZm4`
- **File Name:** `Baubeschreibung Regelgeschoss.pdf`
- **Expected Type:** `14_BAU_AUSSTATTUNGSBESCHREIBUNG`
- **Client:** `adolf_martens_strasse`

#### Test Case 3: Cost Calculation (Kalkulation)
- **File ID:** `1BRz-SaE8gSW1BqeLOh4e4tsg9iG94xvC`
- **File Name:** `251103_Kalkulation Schlossberg.pdf`
- **Expected Type:** `10_BAUTRAEGERKALKULATION_DIN276`
- **Client:** `propos_menrad`

#### Test Case 4: Sales Prices (Kaufpreise)
- **File ID:** `1km2a6MU7mLI9NfeJQGvGujKkEEnI8G5B`
- **File Name:** `251103_Kaufpreise Schlossberg.pdf`
- **Expected Type:** `11_VERKAUFSPREISE`
- **Client:** `propos_menrad`

#### Test Case 5: Ground Assessment (Baugrund)
- **File ID:** `1xx0rJEk5h1vAx757rcNPZainf_kYvfyi`
- **File Name:** `Baugrund_und_Gründungsgutachten.pdf`
- **Expected Type:** `08_BAUGRUNDGUTACHTEN`
- **Client:** `propos_menrad`

**For each test case:**
1. Download PDF from Drive
2. Send email with attachment
3. Wait 30-60 seconds
4. Check execution results
5. Verify classification matches expected type
6. Verify confidence >= 0.9

**See `test_cases.json` for complete list of 10 test cases with expected outputs.**

---

## Test Orchestrator Validation

**Purpose:** Validate autonomous build-test-fix loop (future chunks)

**Status:** ACTIVE but not yet tested

**How to Test:**

1. **Trigger Orchestrator Manually:**
   - Go to: https://n8n.oloxa.ai/workflow/nUgGCv8d073VBuP0
   - Click "Execute Workflow" button
   - Monitor execution progress

2. **What Orchestrator Does:**
   - Reads `Chunk_Status` sheet
   - Determines next chunk to build (2.5, 3, 4, or 5)
   - Calls idea-architect-agent for design
   - Calls architecture-feasibility-agent for validation
   - Calls solution-builder-agent for implementation
   - Runs Layer 1 test (simulated data)
   - Triggers Layer 2 test (real email via Email Sender)
   - Validates results
   - Creates workflow backup if tests pass
   - Updates Status Tracker

3. **Expected Behavior:**
   - First run: Should build Chunk 2.5 (Completeness Validation)
   - If build succeeds + tests pass → Status updated to "completed"
   - If build fails or tests fail → Retry up to 3 times
   - After 3 failures → Status updated to "failed", manual intervention needed

4. **Check Status Tracker:**
   - Open: https://docs.google.com/spreadsheets/d/1af9ZsSm5IDVWIYb5IMX8ys8a5SUUnQcb77xi9tJQVo8
   - Go to "Chunk_Status" tab
   - Verify Chunk 2.5 row updated with:
     - Status: "in_progress" → "completed" or "failed"
     - Agent_ID: (agent that built it)
     - Attempt_Count: Number of build attempts
     - Last_Updated: Timestamp

**Note:** Orchestrator runs every 1 hour on schedule trigger. Disable schedule if you want manual control only.

---

## Troubleshooting

### Issue: Email Not Processed

**Symptoms:**
- Email received but no execution in n8n
- Gmail shows email as unread

**Possible Causes:**
1. **Pre-Chunk 0 workflow inactive**
   - Check: https://n8n.oloxa.ai/workflow/YGXWjWcBIk66ArvT
   - Verify toggle is ACTIVE

2. **Gmail credentials expired**
   - Check n8n credentials: Gmail OAuth (g2ksaYkLXWtfDWAh)
   - Re-authenticate if needed

3. **Email doesn't match trigger conditions**
   - Must have attachment
   - Must be sent to monitored Gmail account
   - Must be unread

**Fix:**
- Verify workflow is active
- Check credentials
- Resend email with attachment

---

### Issue: Chunk 2 Returns 404 Error

**Symptoms:**
- Execution reaches Chunk 2
- "Download PDF" node fails with "resource could not be found"

**Cause:**
Bug fix not applied (see Prerequisites section)

**Fix:**
Apply the skip-download logic to Chunk 2 (see Prerequisites)

---

### Issue: Wrong Document Classification

**Symptoms:**
- Chunk 2 completes successfully
- `documentType` is incorrect (e.g., classified as UNKNOWNS)

**Possible Causes:**
1. **Prompt engineering issue** - AI classifier needs tuning
2. **Document ambiguity** - Document genuinely unclear
3. **Low confidence** - Confidence <0.9 indicates uncertainty

**Diagnostics:**
- Check Chunk 2 output:
  - `confidence` score
  - `reasoning` field (explains why AI chose this type)
  - `extractedText` (first 500 chars) - verify text quality

**Fix:**
- If confidence <0.9 → Expected behavior, flag for review
- If confidence >=0.9 but wrong → Prompt engineering needed
- Check execution logs for AI classifier reasoning

---

### Issue: Email Sender 404 Error

**Symptoms:**
```json
{
  "code": 404,
  "message": "The requested webhook \"POST ama-send-test-email\" is not registered."
}
```

**Cause:**
Email Sender workflow not activated

**Fix:**
1. Go to: https://n8n.oloxa.ai/workflow/8l1ZxZMZvoWISSkJ
2. Toggle workflow to ACTIVE
3. Verify webhook appears: `https://n8n.oloxa.ai/webhook/ama-send-test-email`
4. Retry webhook call

---

### Issue: Test Orchestrator Stuck

**Symptoms:**
- Orchestrator execution takes >10 minutes
- Agent calls time out
- Status not updating

**Possible Causes:**
1. **Agent service down** - Claude API or agent infrastructure issue
2. **Token limit exceeded** - Agent running out of context
3. **Infinite loop** - Logic error in orchestrator

**Diagnostics:**
- Check n8n execution logs for error messages
- Check agent HTTP request responses
- Verify agent service is accessible

**Fix:**
- Stop execution manually in n8n UI
- Check agent service status
- Review orchestrator logic for infinite loops
- Contact Claude Code support if agent service issue

---

## Success Criteria

### Test 1 (End-to-End Email) - PASS
- ✅ Email processed by Pre-Chunk 0
- ✅ PDF uploaded to Drive
- ✅ Client name identified correctly
- ✅ Chunk 0 created folder structure
- ✅ PDF moved to staging
- ✅ Chunk 2 classified document correctly
- ✅ Confidence >= 0.9
- ✅ Email marked as read
- ✅ No errors in execution log

### Test 2 (Email Sender) - PASS
- ✅ Webhook accepted request
- ✅ PDF downloaded from Drive
- ✅ Email sent successfully
- ✅ Execution monitored via API
- ✅ Results validated against expected output
- ✅ Results logged to Layer_2_Tests sheet

### Test 3 (Additional Cases) - PASS
- ✅ All 10 test cases executed
- ✅ Classification accuracy >= 90% (9/10 correct)
- ✅ Average confidence >= 0.9
- ✅ No critical errors

### Test Orchestrator - PASS
- ✅ Chunk 2.5 built autonomously
- ✅ Layer 1 test passed
- ✅ Layer 2 test passed
- ✅ Workflow backup created
- ✅ Status Tracker updated
- ✅ Ready to build next chunk (Chunk 3)

---

## Next Steps After Testing

Once all tests pass:

1. **Enable Autonomous Loop**
   - Let Test Orchestrator run on 1-hour schedule
   - Monitor Chunk_Status sheet for progress
   - Chunks 2.5, 3, 4, 5 will be built automatically

2. **Monitor Build Progress**
   - Check Status Tracker daily
   - Intervene only if status = "failed" after 3 attempts
   - Review Layer_1_Tests and Layer_2_Tests for validation data

3. **Expand Test Coverage**
   - Add more test cases to `test_cases.json`
   - Test missing document types (see TEST_DATA_REPOSITORY.md)
   - Test edge cases (scanned PDFs, large files, etc.)

4. **Production Readiness**
   - Once Chunks 2-5 complete and tested → Ready for production
   - Disable test emails (remove test trigger)
   - Enable production Gmail monitoring
   - Set up monitoring alerts for failures

---

## Related Files

- **test_cases.json** - Test case definitions and expected outputs
- **TEST_DATA_REPOSITORY.md** - Complete test data documentation
- **SYSTEM_VALIDATION_REPORT_2026-01-08.md** - Current system status and findings
- **AUTONOMOUS_TESTING_SYSTEM_V2.md** - Full testing system design
- **Status Tracker Sheet** - `1af9ZsSm5IDVWIYb5IMX8ys8a5SUUnQcb77xi9tJQVo8`

---

**Last Updated:** 2026-01-08
**Version:** 1.0
**Status:** ⚠️ Ready for testing after bug fix

