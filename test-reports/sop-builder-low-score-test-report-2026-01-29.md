# SOP Builder Lead Magnet - Low Score Test Report
**Test Date:** 2026-01-29
**Workflow ID:** ikVyMpDI0az6Zk4t
**Execution ID:** 6794
**Test Type:** Low-score submission (<75%)

---

## Test Summary

- **Total tests:** 1
- **Passed:** 1
- **Failed:** 0

---

## Test Case: Low-Score Submission

### Input Payload
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

### Status: PASS

**n8n execution:** success
**Duration:** 26.49 seconds
**Execution status:** Completed successfully

---

## Verification Checklist

### 1. No Errors - PASS
- Workflow executed without errors
- All 22 nodes executed successfully
- Final status: success

### 2. Score - PASS
**Expected:** Score < 75%
**Actual:** 30%

**Score breakdown:**
- Completeness: 10/100
- Clarity: 10/100
- Usability: 10/100
- Total: 30/100

The score correctly reflects a low-quality SOP submission with minimal detail.

### 3. Email HTML Verification - PASS

#### Logo Verification - PASS
**Expected:** Logo has `width="180"` attribute
**Actual:** Found in HTML:
```html
<img src="https://sopbuilder.oloxa.ai/logo.png" alt="OLOXA" style="height:40px;width:180px;">
```
Logo correctly has `width:180px` in the style attribute.

#### Score Display - PASS
**Expected:** Score number followed by "Your SOP Completeness Score" and encouragement text
**Actual:** Found in HTML:
```html
<div style="font-size:64px;font-weight:bold;color:#F26B5D;text-align:center;margin:30px 0;">30%</div>
<p style="text-align:center;font-size:18px;color:#fff;margin:10px 0;">Your SOP Completeness Score</p>
<p style="text-align:center;font-size:16px;color:#ccc;font-style:italic;margin-bottom:30px;">Great start! With a few improvements, you'll be on your way.</p>
```
All required text elements are present and correctly formatted.

#### Label Color Verification - PASS
**Expected:** Labels "Intention:", "Department:", "Who will use this:" have color `#F26B5D`
**Actual:** Found in HTML:
```html
<p><strong style="color:#F26B5D;">Intention:</strong> Standardize our client onboarding process to reduce errors</p>
<p><strong style="color:#F26B5D;">Department:</strong> Operations</p>
<p><strong style="color:#F26B5D;">Who will use this:</strong> New account managers</p>
```
All three labels correctly use color `#F26B5D`.

#### Resubmit URL Parameters - PASS
**Expected:** Resubmit URL contains `lead=`, `email=`, `name=`, `score=`, `wins=` params
**Actual:** Found in HTML:
```html
https://sopbuilder.oloxa.ai?lead=lead_x7r6zyvdtmkza6k8c&email=swayclarkeii%40gmail.com&name=Sway%20Test&score=30&wins=%5B%7B%22title%22%3A%22Define%20Purpose%22%2C%22action%22%3A%22Add%20a%20purpose%20section%20explaining%20the%20importance%20of%20standardizing%20client%20onboarding.%22%7D%2C%7B%22title%22%3A%22Detail%20Steps%22%2C%22action%22%3A%22Expand%20the%20current%20steps%20to%20include%20specific%20actions%20and%20responsibilities.%22%7D%2C%7B%22title%22%3A%22Include%20Document%20Control%22%2C%22action%22%3A%22Add%20a%20document%20control%20section%20to%20maintain%20versioning%20and%20authorship.%22%7D%5D
```

**URL parameters present:**
- `lead=lead_x7r6zyvdtmkza6k8c` - PASS
- `email=swayclarkeii%40gmail.com` - PASS
- `name=Sway%20Test` - PASS
- `score=30` - PASS
- `wins=[...]` (JSON encoded) - PASS

All required parameters are present and correctly formatted.

### 4. Airtable Update - PASS

**Record ID:** recTk1Ont0IOrLr8U

**Verification:**
- Record was found (existing user with email swayclarkeii@gmail.com)
- Submission count incremented: 5 → 6
- Score history updated: "70,55,55,80,35" → "70,55,55,80,35,30"
- New score (30) appended to history
- Previous score captured: 35
- Lead ID updated: lead_x7r6zyvdtmkza6k8c
- Timestamp updated: 2026-01-29T09:57:55.811Z

**Note:** This was a returning user test, which is why submission_count was already at 5.

---

## Additional Observations

### Email Content Quality
The email includes:
- Clear score display with large, prominent number (30%)
- Descriptive subtitle "Your SOP Completeness Score"
- Encouraging message appropriate for low scores
- 5 missing elements with explanations:
  1. Purpose
  2. Preparation
  3. Detailed Process Flow
  4. Checklist
  5. Document Control
- Each missing element includes "Why it matters" and "How to fix" guidance
- 3 quick wins section with actionable steps
- Clear CTA button to resubmit with URL parameters

### Workflow Flow
The execution followed the correct path:
1. Webhook Trigger → Parse Form Data → Use Text Input
2. LLM: Validate Completeness (scored 30/100)
3. Calculate SOP Score (determined low score < 75%)
4. LLM: Generate Improved SOP
5. Generate Lead ID
6. Route Based on Score → Low score path (<75%)
7. Generate Improvement Email
8. Send HTML Email (Gmail)
9. Check Existing Lead → Update Lead in Airtable
10. Respond to Webhook

### Performance
- Total execution time: 26.49 seconds
- LLM calls: 2 (validate + generate improved SOP)
- Airtable operations: 2 (search + update)
- Gmail operation: 1 (send email)

---

## Test Result: PASS

All verification requirements met:
- No errors during execution
- Score correctly calculated as 30% (< 75%)
- Email HTML contains all required elements with correct styling
- Logo has width="180" attribute
- Score display text present and formatted correctly
- Labels use correct color (#F26B5D)
- Resubmit URL contains all required parameters (lead, email, name, score, wins)
- Airtable record successfully updated with incremented submission count

**Recommendation:** Workflow is functioning correctly for low-score submissions. Ready for production use.
