# Testing Checklist - Fathom CRM Auto-Populate

## Pre-Testing Setup

### Step 1: Configure n8n Credentials

- [ ] **Google Sheets OAuth**
  - Go to n8n.oloxa.ai → Credentials
  - Create/Select Google OAuth2 credential
  - Ensure scopes include: `https://www.googleapis.com/auth/spreadsheets`
  - Connect to these nodes:
    - "Get CRM Data"
    - "Update Existing Contact"
    - "Add New Contact"

- [ ] **Anthropic API**
  - Go to n8n.oloxa.ai → Credentials
  - Create Anthropic API credential
  - Add API key from Anthropic Console
  - Connect to "Anthropic Claude" node

- [ ] **Verify Fathom API Key**
  - Check "Get Fathom Transcript" node has API key in Authorization header
  - Consider moving to credential for better security

### Step 2: Configure Fathom Webhook

- [ ] **Get n8n Webhook URL**
  - Activate workflow in n8n
  - Click "Fathom Webhook" node
  - Copy production webhook URL: `https://n8n.oloxa.ai/webhook/fathom-crm-webhook`

- [ ] **Configure in Fathom**
  - Go to https://app.fathom.video/settings/webhooks
  - Add new webhook:
    - URL: `https://n8n.oloxa.ai/webhook/fathom-crm-webhook`
    - Event: "New meeting content ready"
    - Secret: `whsec_5hR2zWP8KRKjIss3qRLb2z2v+Rh7xc0n`
  - Save and test connection

### Step 3: Prepare Test Data

- [ ] **Clean Test Environment**
  - Open Google Sheets: https://docs.google.com/spreadsheets/d/1PwIqO1nfEeABoRRvTml3dN9q1rUjHIMVXsqOLtouemk
  - Go to "Prospects" tab
  - Note current row count
  - Optionally: Create backup copy before testing

- [ ] **Prepare Test Contacts**
  - Test Contact 1 (New): Use unique email not in CRM
  - Test Contact 2 (Duplicate): Use existing email from CRM

---

## Test Scenarios

### Test 1: New Contact - Complete Flow

**Objective:** Verify workflow can add a completely new contact to CRM.

**Setup:**
- [ ] Ensure test email does NOT exist in CRM
- [ ] Schedule a Fathom call with test participant

**Steps:**
1. [ ] Complete Fathom call (5+ minutes for good transcript)
2. [ ] During call, mention:
   - Full name clearly
   - Email address
   - Company name
   - Role/title
   - What they're looking for (objective)
   - Budget signals (for priority scoring)
3. [ ] Wait for Fathom to process transcript (~2-5 minutes)
4. [ ] Check n8n execution log for workflow run

**Expected Results:**
- [ ] Workflow executes successfully (green checkmark in n8n)
- [ ] New row appears in Google Sheets "Prospects" tab
- [ ] All fields populated correctly:
  - [ ] Full Name matches spoken name
  - [ ] Contact Details contains email
  - [ ] Priority Level is 1-10
  - [ ] Stage is set (In Progress/Follow-up/Closed)
  - [ ] Reply Sentiment is set
  - [ ] Notes has 2-3 sentence summary with date stamp
  - [ ] Objective describes what they want
  - [ ] All scores (1-3) are populated
  - [ ] "Added to CRM" = TRUE
- [ ] Success notification node returns correct message

**Pass/Fail:** ___________

**Notes:**
```
(Record any issues, unexpected behavior, or discrepancies)
```

---

### Test 2: Duplicate Contact - Update Logic

**Objective:** Verify workflow correctly updates existing contact without creating duplicate.

**Setup:**
- [ ] Choose existing contact from CRM
- [ ] Note current values: Priority Level, Connection Strength, Notes
- [ ] Schedule Fathom call using SAME email as existing contact

**Steps:**
1. [ ] Complete Fathom call with existing contact
2. [ ] During call, mention different/updated information:
   - HIGHER priority signals (budget, urgency)
   - New objective or updates
   - Additional context for notes
3. [ ] Wait for transcript processing
4. [ ] Check n8n execution log

**Expected Results:**
- [ ] Workflow executes successfully
- [ ] NO new row created (row count stays same)
- [ ] Existing row is updated:
  - [ ] Full Name unchanged (kept existing)
  - [ ] Company unchanged (kept existing)
  - [ ] Contact Details unchanged (kept existing)
  - [ ] Priority Level = MAX(old, new)
  - [ ] Notes has NEW entry APPENDED with date stamp
  - [ ] Stage updated to new value
  - [ ] Reply Sentiment updated to new value
  - [ ] Objective updated to new value
  - [ ] Connection Strength = MAX(old, new)
  - [ ] Decision Making Power = MAX(old, new)
  - [ ] Network Access = MAX(old, new)
- [ ] Success notification says "updated" (not "added")

**Pass/Fail:** ___________

**Notes:**
```
(Verify merge logic works correctly, especially MAX comparisons)
```

---

### Test 3: Missing Email - Error Handling

**Objective:** Verify workflow fails gracefully when email is not mentioned in call.

**Setup:**
- [ ] Schedule Fathom call
- [ ] Plan to avoid mentioning email/phone in conversation

**Steps:**
1. [ ] Complete Fathom call WITHOUT mentioning contact details
2. [ ] Mention name, company, but deliberately omit email
3. [ ] Wait for transcript processing
4. [ ] Check n8n execution log

**Expected Results:**
- [ ] Workflow executes but FAILS at "Parse AI Response" node
- [ ] Error message indicates: "Missing required fields: contact_details"
- [ ] NO row added to Google Sheets
- [ ] Execution marked as failed (red X in n8n)
- [ ] Can view full error details in execution log

**Pass/Fail:** ___________

**Notes:**
```
(Verify error message is clear and helpful)
```

---

### Test 4: AI Extraction Accuracy

**Objective:** Verify AI correctly extracts and scores contact information.

**Setup:**
- [ ] Prepare script with specific details to mention in call
- [ ] Record expected extraction values

**Test Script:**
```
"My name is Sarah Johnson, I'm the Chief Technology Officer at
DataFlow Solutions, we're a B2B data analytics company. You can
reach me at sarah.johnson@dataflow.io. We're looking to automate
our client onboarding workflows and have a $50,000 budget approved
for Q1. This is urgent - we need to start by February 1st. I can
introduce you to our CEO and VP of Operations if this moves forward."
```

**Expected Extraction:**
- Full Name: Sarah Johnson
- Role: Chief Technology Officer (or CTO)
- Company: DataFlow Solutions
- Business Type: B2B data analytics (or similar)
- Contact Details: sarah.johnson@dataflow.io
- Priority Level: 8-10 (budget + urgency signals)
- Objective: Automate client onboarding workflows
- Niche Alignment: 3 (perfect fit - automation is core)
- Decision Making Power: 3 (C-level)
- Network Access: 3 (mentioned CEO and VP connections)

**Steps:**
1. [ ] Complete call using test script above
2. [ ] Wait for processing
3. [ ] Check extracted values in Google Sheets

**Actual Results:**
- Full Name: ___________
- Priority Level: ___________
- Decision Making Power: ___________
- Network Access: ___________
- Niche Alignment: ___________

**Pass/Fail:** ___________

**Notes:**
```
(Compare actual vs expected, note any scoring discrepancies)
```

---

### Test 5: Notes Append Logic

**Objective:** Verify notes are appended correctly with date stamps on updates.

**Setup:**
- [ ] Use existing contact from Test 2
- [ ] Note current notes content
- [ ] Schedule 2 additional Fathom calls with same contact

**Steps:**
1. [ ] Complete Call #1 with new information
2. [ ] Wait for processing
3. [ ] Check notes field in Google Sheets
4. [ ] Complete Call #2 with different new information
5. [ ] Wait for processing
6. [ ] Check notes field again

**Expected Results:**
- [ ] After Call #1:
  - Notes contains original entry + new entry
  - New entry has date stamp: `[2026-01-XX]:`
  - Entries separated by double newline
- [ ] After Call #2:
  - Notes contains ALL three entries (original + call 1 + call 2)
  - Each has its own date stamp
  - Chronological order maintained

**Pass/Fail:** ___________

**Notes:**
```
(Verify formatting, date stamps, and preservation of old notes)
```

---

### Test 6: Retry Logic on API Failure

**Objective:** Verify HTTP Request retries work correctly.

**Setup:**
- [ ] Temporarily modify "Get Fathom Transcript" node
- [ ] Add invalid/non-existent meeting_id for testing
- [ ] OR disable Fathom API credentials temporarily

**Steps:**
1. [ ] Trigger webhook with invalid meeting_id
2. [ ] Watch execution log in real-time
3. [ ] Observe retry attempts

**Expected Results:**
- [ ] HTTP Request node attempts 3 times
- [ ] 5 second delay between retries visible in execution timeline
- [ ] After 3 failures, workflow stops with error
- [ ] Error message indicates API failure
- [ ] NO row added to Google Sheets

**Pass/Fail:** ___________

**Notes:**
```
(Verify retry count and delay timing)
```

---

## Post-Testing Validation

### Data Integrity Check
- [ ] Open Google Sheets "Prospects" tab
- [ ] Verify no duplicate rows created
- [ ] Check all "Added to CRM" fields = TRUE
- [ ] Verify no empty/null values in critical fields
- [ ] Confirm Notes formatting is clean (no corruption)

### Execution Log Review
- [ ] Go to n8n.oloxa.ai → Executions
- [ ] Review all test workflow runs
- [ ] Verify success rate matches expected
- [ ] Check execution times (should be <30 seconds typically)
- [ ] Look for any warnings or unexpected patterns

### Webhook Configuration
- [ ] In Fathom settings, check webhook delivery log
- [ ] Verify all events were delivered successfully
- [ ] Check for any failed deliveries or errors

---

## Known Issues & Workarounds

### Issue 1: Validation Warning on Update Node
**Symptom:** Validator shows "Values are required for update operation"
**Impact:** None - workflow functions correctly despite warning
**Workaround:** Ignore this warning, using autoMapInputData mode bypasses this check
**Status:** Non-blocking, cosmetic issue

### Issue 2: Platform Field Always "Unknown"
**Symptom:** Platform column always shows "Unknown" for new contacts
**Impact:** Minor - field not currently extracted by AI
**Workaround:** Manually update after import, or enhance AI prompt to extract platform
**Status:** Expected behavior, enhancement opportunity

### Issue 3: Scores Outside Valid Ranges
**Symptom:** AI occasionally returns scores like 4 (when max is 3)
**Impact:** Data integrity issue
**Workaround:** Add validation/clamping in "Parse AI Response" node
**Status:** Should be fixed before production

---

## Success Criteria

**Workflow is considered production-ready when:**

- [ ] All 6 test scenarios pass
- [ ] No data corruption in Google Sheets
- [ ] Duplicate detection works 100% of the time
- [ ] AI extraction accuracy ≥80% for critical fields
- [ ] Execution time consistently <30 seconds
- [ ] Error handling prevents bad data from entering CRM
- [ ] Notes append logic preserves all historical data
- [ ] Retry logic handles transient failures

---

## Next Steps After Testing

1. [ ] **If tests pass:**
   - Activate workflow for production use
   - Monitor first 10 real executions
   - Document any edge cases discovered
   - Consider test-runner-agent for ongoing automated testing

2. [ ] **If tests fail:**
   - Document specific failures
   - Create issue list with priority levels
   - Use solution-builder-agent to fix issues
   - Re-test after fixes

3. [ ] **Enhancement opportunities:**
   - Add webhook signature verification
   - Move Fathom API key to credential
   - Add score range validation
   - Implement notes truncation (keep last N)
   - Extract Platform field from call context

---

**Testing Completed By:** ___________
**Date:** ___________
**Overall Result:** PASS / FAIL (circle one)
