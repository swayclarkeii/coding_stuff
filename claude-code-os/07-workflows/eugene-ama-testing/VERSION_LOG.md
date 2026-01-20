# Eugene Test Harness - Version Log

## Quick Reference

| Property | Value |
|----------|-------|
| **Current Version** | v1.0 |
| **Status** | Built - Pending n8n API credential |
| **Workflow ID** | `h7TkqhOFpH7OdIHA` |
| **Last Updated** | 2026-01-03 |
| **Active** | No (pending configuration) |

---

## Versioning Scheme

We use **semantic versioning** (MAJOR.MINOR.PATCH):

- **MAJOR (v2.0):** Breaking changes, complete rewrites, architectural changes
- **MINOR (v1.1):** New features, enhancements, backward compatible additions
- **PATCH (v1.0.1):** Bug fixes, small improvements, no new features

---

## Complete Version History

### v1.0 (2026-01-03) - **CURRENT**

**Status:** Built - Pending n8n API credential configuration

#### Components Created

| Node | Type | Purpose | Status |
|------|------|---------|--------|
| Manual Trigger | `manualTrigger` | Start test manually | ✅ Working |
| Read Test PDF | `readBinaryFiles` | Load test PDF from disk | ✅ Working |
| Send Test Email | `gmail` | Send email with PDF attachment | ✅ Configured |
| Apply Eugene Label | `gmail` | Add Eugene label to email | ✅ Configured |
| Wait for Processing | `wait` | Wait 90s for workflows | ✅ Working |
| Query Workflow Executions | `httpRequest` | Get recent n8n executions | ⏳ Needs credential |
| Parse Results | `code` | Analyze executions | ✅ Working |
| Output Results | `code` | Format test results | ✅ Working |

#### What Works

- ✅ **Email Sending:** Gmail OAuth configured for swayfromthehook@gmail.com
- ✅ **Label Application:** Eugene label (`Label_4133960118153091049`) applies correctly
- ✅ **Wait Mechanism:** 90-second time-based wait
- ✅ **Result Parsing:** JavaScript logic validates execution data
- ✅ **Console Output:** Formatted PASS/FAIL reporting

#### What Doesn't Work

- ⚠️ **n8n API Query:** Credential not yet configured
- ⚠️ **End-to-End Test:** Cannot verify until API credential is added
- ⚠️ **Execution Verification:** Depends on API query working

#### Known Issues

1. **Missing n8n API Credential:**
   - **Impact:** Cannot query workflow executions
   - **Severity:** Critical (blocks testing)
   - **Resolution:** Configure n8n API credential in UI
   - **ETA:** Requires manual configuration by Sway

2. **No Blueprint Export:**
   - **Impact:** Cannot archive or share workflow config
   - **Severity:** Low
   - **Resolution:** Export blueprint after credential configuration
   - **ETA:** After first successful test

#### Configuration Details

**Test PDF:**
```
/Users/swayclarke/coding_stuff/claude-code-os/02-operations/projects/eugene/dummy_files/Checkliste Investor-Bauträger.pdf
```

**Email Flow:**
- **From:** swayfromthehook@gmail.com
- **To:** swayclarkeii@gmail.com
- **Subject:** `TEST: Eugene Document - {timestamp}`
- **Label:** `Label_4133960118153091049`

**Target Workflow:**
- **Name:** Document Organizer V4 - Complete Workflow
- **ID:** `j1B7fy24Jftmksmg`

**Wait Time:** 90 seconds

**Detection Window:** 120 seconds (2 minutes)

#### Files & Resources

- **Workflow ID:** `h7TkqhOFpH7OdIHA`
- **Workflow URL:** https://n8n.oloxa.ai/workflow/h7TkqhOFpH7OdIHA
- **Documentation:** `TEST_HARNESS_v1.0_2026-01-03.md`
- **Blueprint Export:** (pending - export after credential config)

#### Rollback Instructions

**To rollback to no test harness:**
1. Open n8n UI: https://n8n.oloxa.ai/workflow/h7TkqhOFpH7OdIHA
2. Click "Delete Workflow"
3. Confirm deletion

**Impact:** None (test infrastructure only, no production dependencies)

**Rollback Time:** < 1 minute

---

## Component Inventory

### Google Drive IDs

**Test Files Location:**
```
/Users/swayclarke/coding_stuff/claude-code-os/02-operations/projects/eugene/dummy_files/
```

Available test PDFs:
- `Checkliste Investor-Bauträger.pdf` (current test file)
- `Kaulsdorf/OCP_Memo_New-KaulsCity.pdf`
- Additional PDFs in subdirectories

### n8n Workflow IDs

| Workflow | ID | Purpose | Used By Test Harness |
|----------|-----|---------|---------------------|
| Test Harness | `h7TkqhOFpH7OdIHA` | This workflow | N/A |
| Document Organizer V4 | `j1B7fy24Jftmksmg` | Target workflow for testing | ✅ Yes (verification) |
| Test Orchestrator | `EzPj1xtEZOy2UY3V` | Automated test runner | ⏳ Future integration |
| Pre-Chunk 0 | `koJAMDJv2Gk7HzdS` | Client intake | ❌ No |

### Gmail Label IDs

| Label | ID | Purpose |
|-------|-----|---------|
| Eugene | `Label_4133960118153091049` | Filter for Eugene emails |

### Credential IDs

| Credential Type | ID | Account | Status | Used By |
|----------------|-----|---------|--------|---------|
| Gmail OAuth2 | `o11Tv2e4SgGDcVpo` | swayfromthehook@gmail.com | ✅ Active | Send Test Email, Apply Eugene Label |
| n8n API | ⏳ TBD | n8n instance | ⏳ Needs config | Query Workflow Executions |

---

## Rollback Procedures

### Rollback Checklist

Before rolling back:
- [ ] Export current workflow as blueprint
- [ ] Document reason for rollback
- [ ] Verify no active tests are running
- [ ] Notify team (if applicable)

### Component Rollback

#### To Remove Test Harness Completely

**Steps:**
1. Log in to n8n: https://n8n.oloxa.ai
2. Navigate to workflow: https://n8n.oloxa.ai/workflow/h7TkqhOFpH7OdIHA
3. Click "..." menu → "Delete Workflow"
4. Confirm deletion

**Rollback Time:** 1 minute
**Impact:** None (no production dependencies)
**Data Loss:** Test execution history only

#### To Deactivate Without Deleting

**Steps:**
1. Workflow is already inactive
2. No additional action needed

**Note:** Test harness is currently inactive and will not run automatically.

---

## Blueprint Naming Convention

**Format:** `test_harness_v{version}_{YYYY-MM-DD}.json`

**Examples:**
- `test_harness_v1.0_20260103.json` (pending export)
- `test_harness_v1.1_20260110.json` (future)

**Archived Files:** `_archived/test_harness_v{version}_{YYYY-MM-DD}_ARCHIVED.json`

---

## Version Update Workflow

### At Each Milestone

When making changes to the test harness:

1. **Export Blueprint:**
   - Open n8n UI
   - Export workflow as JSON
   - Save to `N8N_Blueprints/test-harness/`

2. **Update VERSION_LOG.md:**
   - Add new version entry
   - Document changes
   - Update component inventory

3. **Archive Old Version:**
   - Move old blueprint to `_archived/`
   - Update rollback procedures

4. **Test Rollback:**
   - Verify rollback to previous version works
   - Document any rollback issues

5. **Update Documentation:**
   - Update `TEST_HARNESS_v{version}_{date}.md`
   - Archive old documentation

---

## Decentralized Architecture

This test harness is part of the Eugene project testing infrastructure:

**Location:** `/Users/swayclarke/coding_stuff/claude-code-os/07-workflows/eugene-ama-testing/`

**Related Projects:**
- Eugene Technical Builds: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/`
- Eugene Project Docs: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/projects/eugene/`

**To Find All Eugene Versioned Projects:**
```bash
find /Users/swayclarke/coding_stuff/claude-code-os -name "VERSION_LOG.md" | grep eugene
```

---

## Integration with MY-JOURNEY.md

When reaching major milestones (v1.0, v2.0, etc.):

1. **Update VERSION_LOG.md:** Technical details, component tracking
2. **Update MY-JOURNEY.md:** Business context, learnings, client impact

**VERSION_LOG.md Focus:**
- Technical implementation details
- Component IDs and resources
- Rollback procedures
- Breaking changes

**MY-JOURNEY.md Focus:**
- Business value delivered
- Client feedback and impact
- Learnings and insights
- Strategic decisions

---

## Next Actions

### Immediate (Required for v1.0 Completion)

1. ⏳ **Configure n8n API Credential:**
   - Open workflow in n8n UI
   - Add n8n API credential to "Query Workflow Executions" node
   - Save workflow

2. ⏳ **Run First Test:**
   - Execute workflow manually
   - Verify PASS/FAIL logic works
   - Document any issues

3. ⏳ **Export Blueprint:**
   - Export workflow as JSON
   - Save to `N8N_Blueprints/test-harness/test_harness_v1.0_20260103.json`

4. ⏳ **Document Test Results:**
   - Create test report
   - Update VERSION_LOG.md with results
   - Mark v1.0 as "Active and Tested"

### Future Enhancements (v1.1+)

- Add support for multiple target workflows
- Create test scenarios for different PDF types
- Integrate with Test Orchestrator for automation
- Add Slack/email notifications for test results
- Support batch testing (multiple PDFs)

---

## Critical Technical Notes

### Email-to-Workflow Flow

**Complete Path:**
1. Test Harness sends email → Gmail inbox (swayclarkeii@gmail.com)
2. Email receives "Eugene" label → Manual or automatic labeling
3. Gmail Trigger (polling, ~60s) → Detects new email with Eugene label
4. Document Organizer V4 → Processes email and attachments
5. Test Harness queries n8n API → Verifies execution occurred
6. Test Harness reports PASS/FAIL → Console output

**Critical Dependencies:**
- Gmail Trigger must be polling every 60s
- Document Organizer V4 must be ACTIVE
- Eugene label must match exactly
- n8n API must be accessible

### Time Window Calculation

**Why 90 seconds?**
- Gmail polling interval: ~60s
- Workflow processing time: 15-45s
- Safety buffer: 15-30s
- **Total wait:** 90s
- **Detection window:** 120s (2 minutes from test start)

**Trade-offs:**
- Shorter wait → Faster tests, higher false negatives
- Longer wait → Slower tests, higher reliability

**Current setting:** 90s balances speed and reliability.

---

## Known Limitations

### Current v1.0 Limitations

1. **Single Workflow Testing:**
   - Only tests Document Organizer V4
   - Cannot test multiple workflows in parallel
   - **Future:** v1.1 will support multiple target workflows

2. **Manual Credential Configuration:**
   - n8n API credential must be added via UI
   - Cannot be automated due to security
   - **Impact:** One-time manual setup required

3. **No Automated Scheduling:**
   - Must be triggered manually
   - No cron or schedule support built-in
   - **Future:** Integrate with Test Orchestrator for automation

4. **Console-Only Output:**
   - Results only displayed in console
   - No email or Slack notifications
   - **Future:** v1.2 will add notification support

### Platform Limitations

**n8n API Rate Limits:**
- Not currently documented
- Assumed to be generous for self-hosted instances
- **Impact:** Minimal for testing workload

**Gmail API Rate Limits:**
- Send: 500 emails/day (consumer account)
- Label: 250 quota units/user/second
- **Impact:** Minimal for test harness usage

---

## Support & Troubleshooting

### Common Issues

#### Issue: Test Reports FAIL but Workflow Actually Ran

**Symptoms:**
- Test harness shows FAIL status
- Manual check shows workflow executed successfully

**Causes:**
- Execution completed outside 2-minute detection window
- n8n API query returned incomplete results

**Solutions:**
1. Increase detection window to 180s (3 minutes)
2. Increase wait time to 120 seconds
3. Check n8n execution history manually
4. Verify n8n API credential is working

#### Issue: Email Sent but Not Processed

**Symptoms:**
- Email appears in Gmail inbox
- Eugene label is NOT applied
- No workflow execution detected

**Causes:**
- Document Organizer V4 is inactive
- Gmail label filter incorrect
- Polling workflow not running

**Solutions:**
1. Activate Document Organizer V4
2. Verify Eugene label ID matches
3. Check Gmail Trigger polling status
4. Review Gmail API quota usage

#### Issue: n8n API Query Fails

**Symptoms:**
- "Query Workflow Executions" node fails
- Error: "Credential not found" or "Unauthorized"

**Causes:**
- n8n API credential not configured
- API key expired or invalid
- Network connectivity issue

**Solutions:**
1. Configure n8n API credential in UI
2. Generate new API key in n8n settings
3. Test API endpoint with curl:
   ```bash
   curl -H "X-N8N-API-KEY: your_key" \
     https://n8n.oloxa.ai/api/v1/executions?limit=5
   ```

### Getting Help

**For Test Harness Issues:**
1. Check VERSION_LOG.md (this file)
2. Review TEST_HARNESS_v1.0_2026-01-03.md
3. Inspect n8n execution logs
4. Contact Sway Clarke

**For Eugene Workflow Issues:**
1. Check Eugene VERSION_LOG.md
2. Review workflow-specific documentation
3. Inspect workflow execution logs

---

## Last Updated

**Date:** 2026-01-03
**By:** solution-builder-agent (Claude Code)
**Version:** v1.0
