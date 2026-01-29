# SOP Builder Workflow - Returning User Test Report

**Test Date:** 2026-01-28
**Workflow ID:** ikVyMpDI0az6Zk4t
**Execution ID:** 6688
**Test Type:** Returning User Flow Verification

---

## Test Objective

Verify that when the SAME email (swayclarkeii@gmail.com) submits the form a second time, the workflow:
1. Detects the returning user via the "Check If Returning User" node
2. Routes through the "returning" path
3. Increments `submission_count`
4. Appends to `score_history`
5. Sends an email with progress comparison (old score vs new score)

---

## Test Input

```json
{
  "name": "Sway Clarke",
  "email": "swayclarkeii@gmail.com",
  "goal": "Standardize our client onboarding process to reduce errors and improve consistency",
  "department": "Operations",
  "end_user": "New account managers and support staff",
  "process_steps": "1. Receive signed contract\n2. Create client profile in CRM\n3. Schedule kickoff call\n4. Assign dedicated account manager\n5. Send welcome package with login credentials\n6. Complete first check-in within 48 hours",
  "current_problems": "Steps get missed, no standardized timeline, different team members do it differently",
  "has_audio": false
}
```

---

## Execution Results

### Overall Status
- **Execution Status:** ✅ SUCCESS
- **Duration:** 23.6 seconds
- **Total Nodes Executed:** 22/22
- **Email Sent:** ✅ Yes (Gmail ID: 19c06feb0b7c6446)

---

## Critical Finding: Airtable Credential Error

### The Problem

The **"Check Existing Lead"** node encountered a credential error:

```json
{
  "message": "Credential with ID \"I4cWCAcDQ8MHUcJb\" does not exist for type \"airtableTokenApi\".",
  "error": {
    "message": "Credential with ID \"I4cWCAcDQ8MHUcJb\" does not exist for type \"airtableTokenApi\".",
    "timestamp": 1769643881365,
    "name": "NodeApiError"
  }
}
```

### Impact on Returning User Flow

Because "Check Existing Lead" failed with an error:

1. **"Check If Returning User" node routed to FALSE path** (new user path)
   - Output shows: `[[], [data]]` - empty first output, data on second output
   - Second output = "new user" path

2. **Data created as NEW record instead of UPDATE:**
   ```json
   {
     "submission_count": 1,  // ❌ Should be 2 (or higher)
     "score_history": "60"   // ❌ Should append to existing history
   }
   ```

3. **Airtable record created instead of updated:**
   - New record ID: `recgFf6fYpe7Qtb92`
   - Created timestamp: `2026-01-28T23:44:42.000Z`

---

## Test Results Summary

| Test Criterion | Expected | Actual | Status |
|----------------|----------|--------|--------|
| **Detect returning user** | Route to "returning" path | ❌ Routed to "new user" path | ❌ FAIL |
| **Submission count increment** | Increment from previous value | Set to 1 (new record) | ❌ FAIL |
| **Score history append** | Append new score to history | Created new history with "60" | ❌ FAIL |
| **Email includes comparison** | Show old vs new score | N/A (treated as new user) | ❌ FAIL |
| **Workflow executes without errors** | Success | Success (with handled error) | ⚠️ PARTIAL |
| **Email sent successfully** | Yes | ✅ Yes (ID: 19c06feb0b7c6446) | ✅ PASS |

---

## Root Cause Analysis

### Why Did This Happen?

The **"Check Existing Lead"** node is configured with Airtable credential ID `I4cWCAcDQ8MHUcJb`, which **no longer exists** in the n8n instance.

This could be due to:
1. Credential was deleted
2. Credential was renamed/recreated with different ID
3. Workflow was imported from another n8n instance without importing credentials

### Error Handling Behavior

The workflow has **Continue on Fail** enabled for the "Check Existing Lead" node, which is why:
- The workflow didn't stop/crash
- The error was passed to "Check If Returning User" as data
- The If node treated the error as "no existing record found"
- Flow continued down the "new user" path

---

## What Actually Happened

### Successful Flow Path

1. ✅ **Webhook Trigger** - Received form data
2. ✅ **Parse Form Data** - Extracted fields correctly
3. ✅ **LLM: Validate Completeness** - Scored SOP at 60%
4. ✅ **Calculate SOP Score** - Breakdown: Completeness 20, Clarity 20, Usability 20
5. ✅ **LLM: Generate Improved SOP** - Created improved template
6. ✅ **Generate Lead ID** - Created ID: `lead_ypwuph41fmkyo9xad`
7. ✅ **Route Based on Score** - Routed to <75% path (correct, score was 60%)
8. ✅ **Generate Improvement Email (<75%)** - Created HTML email with:
   - Score: 60%
   - 5 missing elements identified
   - 3 quick wins suggested
   - Resubmission link with lead ID
9. ✅ **Send HTML Email** - Email sent successfully to swayclarkeii@gmail.com
10. ❌ **Check Existing Lead** - Failed with credential error
11. ❌ **Check If Returning User** - Incorrectly routed to "new user" path
12. ✅ **Prepare New Lead Data** - Formatted data as new record
13. ✅ **Log Lead in Airtable** - Created NEW record in Airtable

### Email Content Generated

The email correctly included:
- Score: 60%
- Goal: Standardize client onboarding process
- 5 missing elements (Purpose, Preparation, Checklist, Document Control, Decision Points)
- 3 quick wins with actionable steps
- Resubmission link with lead ID

However, it did NOT include progress comparison because the workflow treated this as a first-time submission.

---

## Recommendations

### 1. Fix Airtable Credential (CRITICAL)

**Action Required:**
- Create new Airtable credential in n8n
- Update "Check Existing Lead" node to use correct credential ID
- Update "Log Lead in Airtable" node if it uses same credential

### 2. Re-test Returning User Flow

After fixing credentials, test again with:
- Same email: `swayclarkeii@gmail.com`
- Different process/goal to generate different score
- Verify:
  - Existing record is found
  - Route goes to "returning" path
  - submission_count increments
  - score_history appends
  - Email includes "Last time: X%, This time: Y%"

### 3. Consider Better Error Handling

Currently, credential errors silently route to "new user" path. Consider:
- Adding explicit error notification
- Logging credential errors to separate table/alert
- Falling back gracefully with user notification

### 4. Add Monitoring

Set up alerts for:
- Airtable credential failures
- Duplicate records being created (same email)
- submission_count always being 1 (indicates credential issue)

---

## Test Data Reference

### Score Breakdown Received
```json
{
  "sop_score": 60,
  "score_breakdown": {
    "completeness": 20,
    "clarity": 20,
    "usability": 20
  },
  "automation_ready": false
}
```

### Missing Elements Identified
1. **Purpose** - Define goals and reasons for SOP
2. **Preparation** - List required resources and prerequisites
3. **Checklist** - Provide verification points for auditing
4. **Document Control** - Add versioning and review tracking
5. **Decision Points** - Include conditional steps and escalation paths

### Quick Wins Suggested
1. Define Purpose - Add clear purpose statement
2. Outline Preparation - Include detailed list of tools and training
3. Implement Document Control - Add versioning and author details

### Airtable Record Created
```json
{
  "id": "recgFf6fYpe7Qtb92",
  "createdTime": "2026-01-28T23:44:42.000Z",
  "fields": {
    "email": "swayclarkeii@gmail.com",
    "name": "Sway Clarke",
    "lead_id": "lead_ypwuph41fmkyo9xad",
    "submission_count": 1,
    "score_history": "60",
    "sop_score": 60,
    "automation_ready": "false"
  }
}
```

---

## Conclusion

### Overall Assessment: ❌ FAILED

The returning user flow **did not work as expected** due to missing Airtable credentials.

### What Worked
- ✅ Form data processing
- ✅ LLM analysis and scoring
- ✅ Email generation and delivery
- ✅ Lead ID generation
- ✅ Graceful error handling (workflow didn't crash)

### What Failed
- ❌ Returning user detection
- ❌ Submission count increment
- ❌ Score history tracking
- ❌ Progress comparison in email

### Next Steps
1. **URGENT:** Fix Airtable credential (workflow cannot track returning users without it)
2. Re-test with same email after credential fix
3. Verify existing Airtable records can be found and updated
4. Test score history append functionality
5. Verify progress comparison appears in email for returning users

---

**Test conducted by:** test-runner-agent
**Agent ID:** [To be provided by main conversation]
**Execution Log:** Full execution data available in n8n (Execution ID: 6688)
