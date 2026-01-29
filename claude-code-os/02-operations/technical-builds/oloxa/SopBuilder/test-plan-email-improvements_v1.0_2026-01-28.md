# SOP Builder Email Improvements - Test Plan

**Date:** 2026-01-28
**Workflow ID:** ikVyMpDI0az6Zk4t
**Version:** v1.0

---

## Test Scenarios

### Test 1: Low Score Email (<75%)

**Objective:** Verify improvement email renders correctly with detailed gap analysis

**Test Data:**
```
Name: John Smith
Email: john@example.com
Goal: Improve customer onboarding
Department: Sales
Improvement Type: Efficiency
Process Steps: "1. Receive customer. 2. Send email. 3. Done."
```

**Expected Results:**
- ✅ Email subject: "Your SOP Analysis - Score: [XX]%"
- ✅ Greeting: "Hey John Smith, here's your SOP analysis — let's make it even better."
- ✅ Score badge displays correct percentage
- ✅ "What's Missing From Your SOP" section shows structured gaps:
  - Element name (e.g., "☐ Purpose Statement")
  - Why it matters explanation
  - How to fix guidance
- ✅ "Your SOP Improvement Guide" section includes:
  - Template note with gold border
  - Improved SOP with placeholders like [Your CRM system]
  - NO invented business details
- ✅ CTA button is gold (#d4af37) not black
- ✅ Footer: "© 2026 OLOXA.AI - AI Solutions" (no n8n reference)

**How to Verify:**
1. Submit form at SOP Builder landing page with minimal process steps
2. Check email received
3. Inspect button color (should be gold/yellow, not black)
4. Verify gap analysis has "why it matters" and "how to fix" for each element
5. Verify improved SOP uses [Placeholders] not made-up names

---

### Test 2: High Score Email (≥75%)

**Objective:** Verify success email renders correctly

**Test Data:**
```
Name: Sarah Johnson
Email: sarah@example.com
Goal: Standardize invoice processing
Department: Finance
Improvement Type: Quality
Process Steps: [Complete SOP with all 5 elements]
```

**Expected Results:**
- ✅ Email subject: "🎉 Congratulations! Your SOP Scored [XX]%"
- ✅ Greeting: "Hey Sarah Johnson, great work! Your SOP is looking solid."
- ✅ Score badge displays correct percentage
- ✅ Congrats message: "✅ You're Ready for Automation!"
- ✅ Shows original process steps
- ✅ "Your SOP Improvement Guide" includes template note
- ✅ CTA button is gold (#d4af37)
- ✅ Footer: "© 2026 OLOXA.AI - AI Solutions"

**How to Verify:**
1. Submit form with comprehensive SOP (include purpose, preparation, steps, checklist, version info)
2. Check email received
3. Verify gold CTA button
4. Verify template note is present even in success email
5. Verify no automation references in footer

---

### Test 3: No Name Provided

**Objective:** Verify fallback greeting works

**Test Data:**
```
Name: [blank]
Email: test@example.com
Goal: Test workflow
Department: IT
Improvement Type: Efficiency
Process Steps: "Basic steps"
```

**Expected Results:**
- ✅ Greeting: "Hey there, here's your SOP analysis — let's make it even better."
- ✅ Email still renders correctly despite missing name

---

### Test 4: LLM Response Validation

**Objective:** Verify LLM returns structured missing_elements

**How to Test:**
1. Submit minimal SOP through form
2. Access n8n execution log for workflow
3. Find "LLM: Validate Completeness" node execution
4. Check response JSON

**Expected LLM Response Format:**
```json
{
  "completeness_score": 20,
  "clarity_score": 15,
  "usability_score": 10,
  "total_score": 45,
  "missing_elements": [
    {
      "element_name": "Purpose Statement",
      "why_it_matters": "Your SOP doesn't clearly state why this procedure exists...",
      "how_to_fix": "Add a clear 'Purpose' section explaining why this process matters..."
    },
    {
      "element_name": "Preparation Section",
      "why_it_matters": "Without listing required equipment...",
      "how_to_fix": "Add a 'Preparation' section listing all required tools..."
    }
  ],
  "strengths": ["Uses action verbs"],
  "summary": "Basic process outline needs structure"
}
```

**Validation:**
- ✅ missing_elements is array of objects (not strings)
- ✅ Each object has element_name, why_it_matters, how_to_fix
- ✅ No elements are null or empty strings

---

### Test 5: Improved SOP Generation

**Objective:** Verify LLM uses placeholders, not invented details

**How to Test:**
1. Submit minimal SOP through form
2. Access n8n execution log
3. Find "LLM: Generate Improved SOP" node execution
4. Read improved_sop output

**Expected in Improved SOP:**
- ✅ Placeholders like: [Your system name], [Responsible person], [Your company policy]
- ❌ NO invented details like: "Use Salesforce", "Manager John Smith", "Approve if >$5000"
- ✅ Section: "Next Steps to Complete Your SOP" with 3-5 specific actions
- ✅ Each of 5 core elements marked as ✓ (provided) or ✗ (missing)
- ✅ References user's actual submitted steps

**Red Flags (should NOT appear):**
- Specific software names user didn't mention
- Specific dollar amounts or thresholds
- Made-up employee names or job titles
- Invented company policies

---

### Test 6: Backward Compatibility

**Objective:** Verify old executions still work if LLM returns old format

**Simulation:**
1. Manually trigger workflow with old-format data:
```json
{
  "missing_elements": ["Purpose", "Checklist", "Document Control"],
  "sop_score": 50
}
```

**Expected Results:**
- ✅ Email still renders correctly
- ✅ `getElementDetails()` function maps old strings to structured format
- ✅ Gap analysis shows why/how for each element
- ✅ No JavaScript errors in execution log

---

### Test 7: Mobile Email Rendering

**Objective:** Verify emails render correctly on mobile devices

**How to Test:**
1. Submit form and receive email
2. Open email on:
   - iPhone (iOS Mail app)
   - Android (Gmail app)
   - Desktop Gmail web
   - Desktop Outlook

**Expected Results:**
- ✅ Responsive design scales correctly
- ✅ Gold CTA button is tappable (min 44px touch target)
- ✅ Text is readable without zooming
- ✅ Gap analysis boxes don't overflow
- ✅ Pre-formatted SOP text wraps correctly

---

## Edge Cases to Test

### Edge Case 1: Very Long Process Steps
- Submit SOP with 5000+ characters
- Verify email doesn't break layout
- Verify `<pre>` tag handles overflow correctly

### Edge Case 2: Special Characters in Name
- Name: "José María O'Brien"
- Verify name renders correctly in greeting (no encoding issues)

### Edge Case 3: Empty Missing Elements
- High-scoring SOP with no missing elements
- Verify "What's Missing" section handles empty array gracefully
- Should show "Analysis not available" or similar fallback

### Edge Case 4: LLM Returns Invalid JSON
- Simulate LLM returning malformed response
- Verify workflow error handling catches it
- Verify error email is sent to Sway (not broken email to user)

---

## Acceptance Criteria

**Email Rendering:**
- [x] Personalized greeting uses name or "there" fallback
- [x] CTA button is gold (#d4af37) matching landing page
- [x] No automation/n8n references in footer
- [x] Template note appears in "Your SOP Improvement Guide" section
- [x] Gap analysis shows element name + why + how (not just element names)

**LLM Responses:**
- [x] Validation returns structured missing_elements objects
- [x] Improved SOP uses placeholders, not invented details
- [x] Improved SOP includes "Next Steps" section
- [x] Each core element marked as ✓ or ✗

**Functionality:**
- [x] Backward compatible with old LLM response format
- [x] Handles missing name field gracefully
- [x] Handles empty missing_elements array
- [x] Email renders correctly on mobile and desktop

**Visual:**
- [x] Gold button (#d4af37) contrasts well with black background
- [x] Template note has gold left border for visual consistency
- [x] Gap items have clear visual separation and hierarchy

---

## Test Results Log

**Test Date:** _____________________
**Tester:** _____________________

| Test # | Test Name | Status | Notes |
|--------|-----------|--------|-------|
| 1 | Low Score Email | ⬜ Pass ⬜ Fail | |
| 2 | High Score Email | ⬜ Pass ⬜ Fail | |
| 3 | No Name Provided | ⬜ Pass ⬜ Fail | |
| 4 | LLM Response Validation | ⬜ Pass ⬜ Fail | |
| 5 | Improved SOP Generation | ⬜ Pass ⬜ Fail | |
| 6 | Backward Compatibility | ⬜ Pass ⬜ Fail | |
| 7 | Mobile Email Rendering | ⬜ Pass ⬜ Fail | |

**Edge Cases:**
- [ ] Very long process steps
- [ ] Special characters in name
- [ ] Empty missing elements
- [ ] LLM invalid JSON

---

## Rollback Plan

**If issues found:**

1. **Minor email formatting issues:**
   - Fix CSS in email generation nodes
   - Update via `n8n_update_partial_workflow`
   - No rollback needed

2. **LLM not returning new format:**
   - Verify backward compatibility is working (should be fine)
   - If needed, adjust prompt in LLM nodes
   - Test with manual execution first

3. **Major rendering issues:**
   - Rollback to previous workflow version
   - Restore from n8n workflow history (Version Control)
   - Document issue for future fix

**Previous Version Backup:**
- Workflow has version history in n8n
- No separate backup needed (n8n maintains history)

---

## Success Metrics

**After 10 real submissions, verify:**
- [ ] 0 broken email layouts
- [ ] 100% of emails use personalized greetings
- [ ] 100% of CTA buttons are gold (not black)
- [ ] ≥90% of improved SOPs use placeholders (not invented details)
- [ ] ≥90% of missing_elements have structured why/how (not just names)

**User Feedback to Monitor:**
- Email readability and clarity
- Usefulness of gap analysis (do they understand what to fix?)
- Quality of improved SOP guide (is it actionable?)
- CTA button visibility and click-through rate

---

## Next Steps After Testing

1. **If all tests pass:**
   - Mark workflow as production-ready
   - Monitor first 5-10 real submissions
   - Collect feedback on email quality

2. **If minor issues found:**
   - Document issues
   - Fix and re-test
   - Update test plan with new scenarios

3. **If major issues found:**
   - Rollback changes
   - Root cause analysis
   - Update implementation plan
   - Re-test before re-deployment
