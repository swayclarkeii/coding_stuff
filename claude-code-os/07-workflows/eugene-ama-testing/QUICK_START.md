# Eugene Test Harness - Quick Start Guide

**Workflow ID:** `h7TkqhOFpH7OdIHA`
**Workflow URL:** https://n8n.oloxa.ai/workflow/h7TkqhOFpH7OdIHA
**Status:** Ready to configure and test

---

## What This Does

Sends a test email with PDF attachment to swayclarkeii@gmail.com, applies the Eugene label, waits 90 seconds for the Document Organizer V4 workflow to process it, then checks if the workflow executed successfully.

**Result:** PASS/FAIL status in console showing whether the email flow works end-to-end.

---

## Setup (5 Minutes)

### Step 1: Configure n8n API Credential

**Why needed:** The workflow needs to query n8n's API to check if Document Organizer V4 executed.

**How to do it:**

1. **Open n8n UI:**
   - Go to: https://n8n.oloxa.ai/workflow/h7TkqhOFpH7OdIHA

2. **Generate API Key:**
   - Click your profile icon (top right)
   - Settings → API
   - Click "Create API Key"
   - Copy the key (starts with `n8n_api_...`)
   - **IMPORTANT:** Save this key somewhere safe - it won't be shown again

3. **Add Credential to Workflow:**
   - In the workflow, click the "Query Workflow Executions" node
   - Click "Credential to connect with" dropdown
   - Click "+ Add New Credential"
   - Choose "HTTP Header Auth"
   - Configure:
     - **Header Name:** `X-N8N-API-KEY`
     - **Header Value:** {paste your API key from step 2}
   - Click "Save" (credential will be named "HTTP Header Auth account")
   - The node should now show a green checkmark

4. **Save Workflow:**
   - Click "Save" button (top right)
   - Credential is now configured

**Alternative (if HTTP Header Auth doesn't work):**

Use the built-in n8n API credential type instead:
1. In "Query Workflow Executions" node settings
2. Change "Authentication" from "Generic Credential Type" to "Predefined Credential Type"
3. Select "n8n API"
4. Click "+ Add New Credential"
5. Add your API key
6. Save

---

### Step 2: Verify Prerequisites

Before running the test, make sure:

- [ ] **Document Organizer V4 is ACTIVE**
  - Go to: https://n8n.oloxa.ai/workflow/j1B7fy24Jftmksmg
  - Toggle should be ON (blue)
  - If not, click toggle to activate

- [ ] **Gmail credentials are working**
  - Already configured (no action needed)
  - Test harness uses swayfromthehook@gmail.com to send
  - Sends to swayclarkeii@gmail.com

- [ ] **Test PDF file exists**
  - Path: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/projects/eugene/dummy_files/Checkliste Investor-Bauträger.pdf`
  - Should exist (no action needed)

---

## Run First Test (2 Minutes)

### Step 1: Execute Workflow

1. Open workflow: https://n8n.oloxa.ai/workflow/h7TkqhOFpH7OdIHA
2. Click "Execute Workflow" button (top right)
3. Workflow will run automatically - you'll see progress through each node
4. **Wait ~95 seconds** for completion (90s wait + 5s processing)

### Step 2: Check Results

1. **In n8n UI:**
   - Scroll to the last node "Output Results"
   - Click on the node to see output
   - Look for console log showing PASS/FAIL status

2. **Expected PASS Output:**
   ```
   ============================================================
   EUGENE TEST HARNESS - RESULTS
   ============================================================
   Test Run: 2026-01-03T17:00:00.000Z
   Status: PASS
   Message: ✅ Test PASSED - Workflow executed successfully (ID: abc123)

   Verification Steps:
     ✓ Test email sent: true
     ✓ Eugene label applied: true
     ✓ Workflow triggered: true

   Recent Executions Found: 3
   Wait Time: 90 seconds

   Execution Details:
     - Execution ID: abc123
     - Started: 2026-01-03T17:01:30.000Z
     - Finished: 2026-01-03T17:02:15.000Z
     - Status: success
   ============================================================
   ```

3. **Expected FAIL Output (if Document Organizer V4 didn't run):**
   ```
   ============================================================
   EUGENE TEST HARNESS - RESULTS
   ============================================================
   Status: FAIL
   Message: ❌ Test FAILED - No workflow execution detected in last 2 minutes
   ...
   ============================================================
   ```

### Step 3: Verify in Gmail (Optional)

1. Log in to Gmail: swayclarkeii@gmail.com
2. Check inbox for email with subject starting with "TEST: Eugene Document"
3. Verify email has "Eugene" label
4. Verify PDF is attached

---

## Troubleshooting

### Test Shows FAIL but Email Was Sent

**Possible Causes:**
1. Document Organizer V4 is inactive
2. Workflow took longer than 2 minutes to execute
3. n8n API credential not working

**Solutions:**
1. Check Document Organizer V4 status: https://n8n.oloxa.ai/workflow/j1B7fy24Jftmksmg
2. Check execution history manually (Executions tab in n8n)
3. Re-configure n8n API credential

### Node "Query Workflow Executions" Fails

**Error Message:** "Unauthorized" or "Invalid credentials"

**Solution:**
1. Re-generate n8n API key in Settings → API
2. Update credential in "Query Workflow Executions" node
3. Save workflow and re-run test

### Email Not Sent

**Error in "Send Test Email" Node**

**Solutions:**
1. Check Gmail OAuth credential is active
2. Re-authorize Gmail if needed (click credential → Reconnect)
3. Check Gmail API quota in Google Cloud Console

---

## What to Do After First Successful Test

### Immediate Actions

1. **Export Blueprint:**
   - In workflow UI, click "..." menu (top right)
   - Select "Download"
   - Save as: `test_harness_v1.0_20260103.json`
   - Store in project folder

2. **Document Results:**
   - Take screenshot of PASS output
   - Note execution ID and duration
   - Update VERSION_LOG.md if needed

3. **Share Success:**
   - Update MY-JOURNEY.md with milestone
   - Consider this test harness for other projects

### Optional Enhancements

**Add Slack Notification (v1.1):**
- Add Slack node after "Output Results"
- Send PASS/FAIL status to #eugene-testing channel

**Test Multiple Workflows (v1.2):**
- Modify "Parse Results" to check for Pre-Chunk 0 + Chunk 0
- Verify complete end-to-end flow

**Automate Daily Testing (v1.3):**
- Integrate with Test Orchestrator
- Schedule daily at 9am to verify workflows still work

---

## File Locations

**Workflow:** https://n8n.oloxa.ai/workflow/h7TkqhOFpH7OdIHA

**Documentation:**
- Quick Start: `/Users/swayclarke/coding_stuff/claude-code-os/07-workflows/eugene-ama-testing/QUICK_START.md` (this file)
- Full Documentation: `/Users/swayclarke/coding_stuff/claude-code-os/07-workflows/eugene-ama-testing/TEST_HARNESS_v1.0_2026-01-03.md`
- Version Log: `/Users/swayclarke/coding_stuff/claude-code-os/07-workflows/eugene-ama-testing/VERSION_LOG.md`
- Implementation Summary: `/Users/swayclarke/coding_stuff/claude-code-os/07-workflows/eugene-ama-testing/IMPLEMENTATION_SUMMARY.md`

**Test PDF:**
- Current: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/projects/eugene/dummy_files/Checkliste Investor-Bauträger.pdf`
- More test files: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/projects/eugene/dummy_files/`

---

## Support

**Questions or Issues:**
- Check VERSION_LOG.md for known issues
- Review TEST_HARNESS_v1.0_2026-01-03.md for detailed troubleshooting
- Inspect n8n execution logs for error details

**Built By:** solution-builder-agent (Claude Code)
**Date:** 2026-01-03
**Version:** v1.0
