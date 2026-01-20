# Eugene Test Harness - End-to-End Email Flow Testing

**Version:** v1.0
**Created:** 2026-01-03
**Workflow ID:** `h7TkqhOFpH7OdIHA`
**Status:** Built - Pending credential configuration

---

## Overview

This test harness enables **live end-to-end testing** of Eugene's document processing workflows by simulating the complete email flow from sender to Gmail inbox to workflow trigger.

### What It Does

1. Reads a test PDF file from disk
2. Sends email from **swayfromthehook@gmail.com** to **swayclarkeii@gmail.com**
3. Applies the "Eugene" Gmail label (`Label_4133960118153091049`)
4. Waits 90 seconds for polling workflows to detect and process the email
5. Queries n8n API for recent workflow executions
6. Parses execution data and reports PASS/FAIL status
7. Outputs detailed test results to console

---

## Workflow Structure

### Nodes

| # | Node Name | Type | Purpose |
|---|-----------|------|---------|
| 1 | Manual Trigger | `manualTrigger` | Start test manually |
| 2 | Read Test PDF | `readBinaryFiles` | Load test PDF from disk |
| 3 | Send Test Email | `gmail` | Send email with PDF attachment |
| 4 | Apply Eugene Label | `gmail` | Add Eugene label to email |
| 5 | Wait for Processing | `wait` | Wait 90s for workflows to run |
| 6 | Query Workflow Executions | `httpRequest` | Get recent n8n executions |
| 7 | Parse Results | `code` | Analyze executions and determine PASS/FAIL |
| 8 | Output Results | `code` | Format and display test results |

### Data Flow

```
Manual Trigger
    ↓
Read Test PDF (local file)
    ↓
Send Test Email (Gmail API)
    ↓
Apply Eugene Label (Gmail API)
    ↓
Wait for Processing (90 seconds)
    ↓
Query Workflow Executions (n8n API)
    ↓
Parse Results (JavaScript)
    ↓
Output Results (Console)
```

---

## Configuration

### Test PDF File

**Current Path:**
```
/Users/swayclarke/coding_stuff/claude-code-os/02-operations/projects/eugene/dummy_files/Checkliste Investor-Bauträger.pdf
```

**To Change Test File:**
Update the `Read Test PDF` node's `fileSelector` parameter.

### Email Configuration

- **From:** swayfromthehook@gmail.com (via Gmail OAuth)
- **To:** swayclarkeii@gmail.com
- **Subject:** `TEST: Eugene Document - {timestamp}`
- **Label:** `Label_4133960118153091049` (Eugene label)

### Target Workflow

The test currently checks for executions of:
- **Document Organizer V4** (ID: `j1B7fy24Jftmksmg`)

**To test different workflows:**
Modify the `Parse Results` node's `jsCode` to check for different `workflowId` values.

### Wait Time

**Default:** 90 seconds

Gmail polling workflows typically check every 60 seconds. The 90-second wait ensures:
- Polling workflow detects new email
- Target workflow completes processing
- Execution data is available via API

**To adjust:** Update `Wait for Processing` node's `amount` parameter.

---

## Credentials Required

### 1. Gmail OAuth2 ✅

**Status:** Configured
**Credential ID:** `o11Tv2e4SgGDcVpo`
**Account:** swayfromthehook@gmail.com
**Used By:**
- Send Test Email node
- Apply Eugene Label node

### 2. n8n API ⚠️

**Status:** Needs Configuration
**Current:** Placeholder credential ID
**Required Permissions:** Read executions

**To configure:**
1. Open n8n UI: https://n8n.oloxa.ai/workflow/h7TkqhOFpH7OdIHA
2. Click on "Query Workflow Executions" node
3. Add n8n API credential:
   - **API Key:** Your n8n API key
   - **Base URL:** https://n8n.oloxa.ai
4. Save workflow

**Alternative:** Update `Query Workflow Executions` node to use HTTP Header Auth with manual API key.

---

## Usage

### Running a Test

1. **Prerequisites:**
   - Document Organizer V4 workflow is ACTIVE
   - Gmail polling is enabled
   - n8n API credential is configured

2. **Execute Test:**
   - Open workflow in n8n UI
   - Click "Execute Workflow" button
   - Wait ~95 seconds for completion

3. **Review Results:**
   - Check console output for PASS/FAIL status
   - Review execution details in final node output

### Expected Output

#### Successful Test (PASS)
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

#### Failed Test (FAIL)
```
============================================================
EUGENE TEST HARNESS - RESULTS
============================================================
Test Run: 2026-01-03T17:00:00.000Z
Status: FAIL
Message: ❌ Test FAILED - No workflow execution detected in last 2 minutes

Verification Steps:
  ✓ Test email sent: true
  ✓ Eugene label applied: true
  ✗ Workflow triggered: false

Recent Executions Found: 0
Wait Time: 90 seconds
============================================================
```

---

## Test Scenarios

### Happy Path - Document Organizer V4
**Description:** Test complete email-to-processing flow
**Expected Result:** PASS
**Verification:**
- Email arrives in inbox
- Eugene label is applied
- Document Organizer V4 executes
- Execution completes successfully

### Edge Case - Workflow Not Active
**Description:** Test when target workflow is inactive
**Expected Result:** FAIL
**Message:** "No workflow execution detected"

### Edge Case - Polling Delay
**Description:** Test with longer-than-expected polling interval
**Expected Result:** May FAIL if wait time too short
**Solution:** Increase wait time to 120 seconds

---

## Troubleshooting

### Test Reports FAIL but Workflow Actually Ran

**Cause:** Execution completed outside 2-minute detection window
**Solutions:**
1. Increase detection window in `Parse Results` node (line 6: `timeDiff < 120`)
2. Increase wait time to 120 seconds
3. Check n8n execution history manually

### Email Sent but Not Processed

**Possible Causes:**
1. Document Organizer V4 is inactive
2. Gmail label filter incorrect
3. Polling workflow not running
4. Gmail API rate limiting

**Debugging:**
1. Check Document Organizer V4 status
2. Verify email has "Eugene" label in Gmail
3. Check polling workflow execution history
4. Review Gmail API quota usage

### n8n API Query Fails

**Possible Causes:**
1. n8n API credential not configured
2. API key expired or invalid
3. Network connectivity issue

**Solutions:**
1. Configure n8n API credential properly
2. Generate new API key in n8n settings
3. Test API endpoint with curl:
   ```bash
   curl -H "X-N8N-API-KEY: your_key" https://n8n.oloxa.ai/api/v1/executions?limit=5
   ```

---

## Customization

### Testing Different Workflows

Modify `Parse Results` node JavaScript (line 15):

```javascript
// Original (Document Organizer V4)
const docOrganizerExecution = recentExecutions.find(exec =>
  exec.json.workflowId === 'j1B7fy24Jftmksmg'
);

// Example: Test Chunk 0 workflow
const chunk0Execution = recentExecutions.find(exec =>
  exec.json.workflowId === 'Ui2rQFpMu9G1RTE1'
);
```

### Testing Multiple PDFs

Modify `Read Test PDF` node to use glob pattern:

```javascript
// Single file (current)
fileSelector: "/path/to/single.pdf"

// Multiple files (glob pattern)
fileSelector: "/path/to/test-files/*.pdf"
```

Update downstream logic to handle multiple files.

### Custom Test Email Content

Modify `Send Test Email` node parameters:

```javascript
// Add custom metadata to subject
subject: "TEST: Eugene Document - CLIENT_NAME - {{ $now.toFormat('yyyy-MM-dd HH:mm:ss') }}"

// Add specific test scenario to message
message: "Test Scenario: Happy Path - Standard PDF\n\nClient: Test Client GmbH\n..."
```

---

## Integration with Automated Testing

### Test Orchestrator Integration

This test harness can be called from the existing **Test Orchestrator** workflow for automated regression testing:

**Steps:**
1. Add Execute Workflow node in Test Orchestrator
2. Point to this test harness (ID: `h7TkqhOFpH7OdIHA`)
3. Parse PASS/FAIL status in Test Orchestrator
4. Include in automated test suite

**Benefit:** Daily or scheduled testing of complete email flow

---

## Files & Resources

### Workflow Files
- **Workflow ID:** `h7TkqhOFpH7OdIHA`
- **Workflow URL:** https://n8n.oloxa.ai/workflow/h7TkqhOFpH7OdIHA
- **Blueprint Export:** (pending - export after credential config)

### Test Data
- **Test PDF Location:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/projects/eugene/dummy_files/`
- **Additional PDFs Available:**
  - `Checkliste Investor-Bauträger.pdf` (current)
  - `Kaulsdorf/OCP_Memo_New-KaulsCity.pdf`
  - Various other sample documents in subdirectories

### Related Workflows
- **Document Organizer V4:** `j1B7fy24Jftmksmg`
- **Test Orchestrator:** `EzPj1xtEZOy2UY3V`
- **Pre-Chunk 0:** `koJAMDJv2Gk7HzdS`

---

## Next Steps

### Immediate (Required for Testing)
1. ✅ Workflow structure built
2. ⏳ **Configure n8n API credential** (required)
3. ⏳ Test single execution manually
4. ⏳ Verify PASS/FAIL logic works correctly

### Short Term (Enhancements)
5. Export blueprint after successful test
6. Add support for multiple target workflows
7. Create test scenarios for different PDF types
8. Integrate with Test Orchestrator for automation

### Future (Advanced Features)
9. Add Slack/email notifications for test results
10. Support for batch testing (multiple PDFs)
11. Detailed execution log parsing (node-by-node verification)
12. Performance benchmarking (execution duration tracking)

---

## Version History

### v1.0 (2026-01-03) - Initial Build
**Created By:** solution-builder-agent
**Status:** Built - Pending credential configuration

**Components Created:**
- ✅ 8-node workflow structure
- ✅ Gmail send and label automation
- ✅ 90-second wait period
- ✅ n8n API query logic
- ✅ PASS/FAIL result parsing
- ✅ Console output formatting

**Known Issues:**
- n8n API credential needs configuration
- Not yet tested end-to-end
- No blueprint export yet (pending credential config)

**What Works:**
- Email sending (Gmail OAuth configured)
- Label application (Gmail OAuth configured)
- Wait mechanism (time-based)
- Result parsing logic (JavaScript)

**What Doesn't Work Yet:**
- n8n API execution query (credential missing)
- End-to-end test verification (pending test run)

---

## Technical Notes

### API Query Format

The workflow queries n8n's REST API:

**Endpoint:** `GET /api/v1/executions`
**Parameters:**
- `limit=20` (fetch recent executions)
- Optional: `status=success` (filter by status)

**Response Format:**
```json
{
  "data": [
    {
      "id": "execution-id",
      "workflowId": "workflow-id",
      "startedAt": "2026-01-03T17:00:00.000Z",
      "stoppedAt": "2026-01-03T17:02:00.000Z",
      "status": "success"
    }
  ]
}
```

### Time Window Logic

The test uses a **2-minute detection window** (120 seconds):
- 90 seconds wait time
- 30 seconds buffer for processing
- Total: 120 seconds from test start to verification

**Rationale:**
- Gmail polling interval: ~60s
- Workflow processing time: 15-45s
- Safety buffer: 15-30s

### Gmail OAuth Scope

**Required Scopes:**
- `https://www.googleapis.com/auth/gmail.send` (send emails)
- `https://www.googleapis.com/auth/gmail.modify` (apply labels)

Currently configured credential includes these scopes.

---

## Support & Maintenance

### Ownership
- **Created By:** solution-builder-agent (Claude Code)
- **Maintained By:** Sway Clarke
- **Project:** Eugene AMA Capital

### Rollback Procedure

If test harness causes issues:
1. Deactivate workflow in n8n UI
2. Delete workflow if needed
3. No production impact (test infrastructure only)

### Update Protocol

When modifying this test harness:
1. Export current version as blueprint
2. Archive to `_archived/` folder
3. Update this documentation
4. Increment version number
5. Test thoroughly before deployment

---

## Conclusion

This test harness provides **reusable, automated end-to-end testing** for Eugene workflows. Once the n8n API credential is configured, it will enable:

- ✅ Quick verification of email flow
- ✅ Regression testing after changes
- ✅ Performance monitoring
- ✅ Confidence in production deployments

**Next Action:** Configure n8n API credential and run first test.
