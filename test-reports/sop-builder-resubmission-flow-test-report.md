# SOP Builder Workflow - Resubmission Flow Test Report

**Workflow ID:** ikVyMpDI0az6Zk4t
**Workflow Name:** SOP Builder Lead Magnet
**Test Date:** 2026-01-29
**Tester:** test-runner-agent

---

## Summary

- **Total Tests:** 2
- **Passed:** 2
- **Failed:** 0

---

## Test 1: Initial Low-Score Submission

**Purpose:** Verify that a minimal SOP submission gets a low score (<85%) and is routed to the improvement email path with a resubmit URL.

### Input Data
```json
{
  "email": "swayclarkeii@gmail.com",
  "name": "Sway Test",
  "goal": "Standardize our client onboarding process to reduce errors",
  "improvement_type": "Documentation",
  "department": "Operations",
  "end_user": "New account managers",
  "process_steps": "Step 1: Get client info. Step 2: Set up account. Step 3: Send welcome email.",
  "input_method": "text"
}
```

### Results

- **Status:** PASS
- **Execution ID:** 6844
- **Final Status:** success
- **Execution Duration:** 25.4 seconds

### Key Findings

1. **Score Calculation**
   - Score: 30/100 (30%)
   - Breakdown: Completeness: 10, Clarity: 10, Usability: 10
   - Automation Ready: false
   - As expected: Score < 85%

2. **Email Routing**
   - Routed to: "Generate Improvement Email (<85%)" (output 1 of Route node)
   - Email sent successfully (Gmail message ID: 19c0999a2d19edf7)
   - Email subject: "Your SOP Analysis - Score: 30%"

3. **Resubmit URL Verification**
   ```
   https://sopbuilder.oloxa.ai?lead=lead_p221tosx7mkzeaqze&email=swayclarkeii%40gmail.com&name=Sway%20Test&score=30&wins=%5B%7B%22title%22%3A%22Add%20Purpose%20Section%22%2C%22action%22%3A%22Clearly%20state%20the%20purpose%20of%20the%20SOP.%22%7D%2C%7B%22title%22%3A%22Expand%20Process%20Steps%22%2C%22action%22%3A%22Use%20specific%20action%20verbs%20and%20measurable%20outcomes%20for%20each%20step.%22%7D%2C%7B%22title%22%3A%22Include%20Document%20Control%22%2C%22action%22%3A%22Add%20details%20for%20document%20versioning%20and%20compliance.%22%7D%5D
   ```
   - Contains: lead_id, email, name, score, and encoded quick wins
   - All parameters present and correctly formatted

4. **Missing Elements Identified**
   - Purpose
   - Preparation
   - Detailed Process Flow
   - Checklist
   - Document Control

5. **Quick Wins Provided**
   1. Add Purpose Section
   2. Expand Process Steps
   3. Include Document Control

---

## Test 2: Detailed Resubmission (High Score Path)

**Purpose:** Verify that a comprehensive SOP submission achieves a high score (>=85%) and is routed to the success email path with Calendly CTA.

### Input Data
```json
{
  "email": "swayclarkeii@gmail.com",
  "name": "Sway Test",
  "goal": "Resubmission - improving existing SOP based on analysis feedback",
  "improvement_type": "quality",
  "department": "operations",
  "end_user": "",
  "lead_id": "test-resubmit-loop",
  "process_steps": "[Comprehensive SOP with Purpose, Preparation, Process Steps, Decision Points, Checklist, and Document Control]"
}
```

### Results

- **Status:** PASS
- **Execution ID:** 6846
- **Final Status:** success
- **Execution Duration:** 21.4 seconds

### Key Findings

1. **Score Calculation**
   - Score: 100/100 (100%)
   - Breakdown: Completeness: 40, Clarity: 30, Usability: 30
   - Automation Ready: true
   - As expected: Score >= 85%

2. **Email Routing**
   - Routed to: "Generate Success Email (>=85%)" (output 0 of Route node)
   - Email sent successfully
   - Email subject: "Congratulations! Your SOP Scored 100%"

3. **Success Email Content**
   - Contains Calendly CTA: "Book Your Free Discovery Call"
   - Calendly URL: https://calendly.com/sway-oloxa/discovery-call
   - Includes full improved SOP template
   - Shows "You are Ready for Automation!" badge

4. **Airtable Resubmission Tracking**
   - Lead lookup successful (found existing lead by email)
   - Detected as returning user
   - Submission count incremented: 9 -> 10
   - Score history updated: "70,55,55,80,35,30,30,40,30,100"
   - Previous score tracked: 30
   - New score: 100
   - Automation ready flag updated: "false" -> "true"

5. **Lead ID Handling**
   - Original lead_id from Test 1: "lead_p221tosx7mkzeaqze"
   - Test 2 provided lead_id: "test-resubmit-loop"
   - System updated the lead_id to the new value (expected behavior for resubmissions)

---

## Verification Checklist

### Test 1 (Low Score)
- [x] Execution succeeds
- [x] Score is <85% (actual: 30%)
- [x] Email routed to improvement path
- [x] Resubmit URL present in email
- [x] Resubmit URL contains all required parameters:
  - [x] lead_id
  - [x] email
  - [x] name
  - [x] score
  - [x] wins (encoded JSON array)

### Test 2 (High Score Resubmission)
- [x] Execution succeeds
- [x] Score is >=85% (actual: 100%)
- [x] Email routed to success path
- [x] Calendly CTA present in email
- [x] Airtable record found by email
- [x] Submission count incremented
- [x] Score history appended
- [x] Previous score tracked
- [x] Automation ready flag updated

---

## Performance Notes

- **Execution Speed:** Both tests completed in ~20-25 seconds
- **LLM Analysis:** Both validations returned detailed scoring and feedback
- **Email Delivery:** All emails sent successfully via Gmail API
- **Airtable Operations:** Lookup and update operations performed correctly

---

## Edge Cases Observed

1. **Lead ID Behavior on Resubmission**
   - When a user resubmits with a different lead_id, the system updates it
   - This could be intentional (allowing lead_id updates) or a bug
   - Recommendation: Clarify if lead_id should be immutable after first submission

2. **Empty end_user Field**
   - Test 2 had an empty end_user field
   - Workflow handled it gracefully
   - No errors or validation issues

3. **Multiple Leads with Same Email**
   - Airtable lookup found 4 records with swayclarkeii@gmail.com
   - System used the first match (most recent: recTk1Ont0IOrLr8U)
   - This is expected behavior but worth noting for data hygiene

---

## Recommendations

1. **Lead ID Persistence:** Consider making lead_id immutable after first creation to prevent accidental overwrites.

2. **Email Deduplication:** The workflow currently allows multiple leads with the same email. Consider adding uniqueness validation if this is not desired.

3. **Score Threshold Visibility:** The 85% threshold is working correctly. Consider surfacing this threshold in the improvement email so users know the target.

4. **Score History Display:** The score_history CSV format works well. Consider adding a visual chart in future iterations.

---

## Overall Assessment

Both tests passed successfully. The resubmission flow is working as designed:

- Low scores (<85%) route to improvement email with resubmit URL
- High scores (>=85%) route to success email with Calendly CTA
- Resubmissions are tracked in Airtable with incremented counts and score history
- All URL parameters are correctly encoded and passed through

The workflow is production-ready for the resubmission loop feature.
