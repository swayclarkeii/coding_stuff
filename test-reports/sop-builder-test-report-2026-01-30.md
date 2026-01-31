# SOP Builder Lead Magnet - Test Report

**Test Date:** 2026-01-30
**Workflow ID:** ikVyMpDI0az6Zk4t
**Workflow Name:** SOP Builder Lead Magnet
**Execution ID:** 7096 (main), 7097 (error handler)

---

## Summary

- **Test Status:** FAIL
- **SOP Score Achieved:** 80%
- **Target Score:** ≥85% (for PDF generation)
- **Duration:** 34.3 seconds
- **Execution Status:** Error

---

## Test Input

Comprehensive SOP submission designed to score ≥85%:

```json
{
  "name": "Sway Clarke",
  "email": "swayclarkeii@gmail.com",
  "processName": "Client Onboarding Process",
  "goal": "Streamline new client onboarding to ensure consistent delivery, clear expectations, and a professional experience within the first 7 days of engagement",
  "department": "Operations",
  "audience": "Project managers and account leads",
  "processSteps": "1. Initial Welcome: Send personalized welcome email within 2 hours of signed contract. Include project timeline, team introductions, and access credentials.\n\n2. Kickoff Meeting: Schedule 30-minute video call within 48 hours. Cover project scope, communication preferences, tool access (Slack, Notion, Drive), and milestone dates.\n\n3. Account Setup: Create client workspace in Notion with project tracker, shared Drive folder with naming conventions, and Slack channel. Assign project manager and backup contact.\n\n4. Requirements Gathering: Send structured intake form covering brand guidelines, existing assets, technical requirements, and success metrics. Review responses within 24 hours.\n\n5. Project Plan Delivery: Create detailed project plan with phases, milestones, deliverables, and review cycles. Share via Notion and walk through in second call.\n\n6. First Deliverable: Complete and deliver first milestone within 5 business days. Include revision process explanation and feedback template.\n\n7. Check-in & Feedback: Schedule weekly 15-minute check-in. Send satisfaction survey after first deliverable. Document all feedback in project tracker.\n\n8. Handoff to Ongoing: After onboarding complete, transition to regular project cadence. Archive onboarding docs, update CRM status, send summary report to client."
}
```

---

## Execution Flow

### Successful Steps (15 nodes executed)

1. **Webhook Trigger** - Received POST request (0ms)
2. **Parse Form Data** - Parsed JSON payload (62ms)
3. **Check Audio File** - Detected no audio (6ms)
4. **Use Text Input** - Proceeded with text path
5. **Merge Audio and Text Paths** - Combined data (1ms)
6. **LLM: Validate Completeness** - OpenAI analysis (12.3s)
7. **Extract Validation Response** - Parsed AI feedback (19ms)
8. **Calculate SOP Score** - Computed 80% score (38ms)
9. **Prepare LLM Request** - Built improved SOP request (26ms)
10. **LLM: Generate Improved SOP** - Created enhanced version (21.8s)
11. **Extract Improved SOP** - Extracted markdown (22ms)
12. **Generate Lead ID** - Created unique ID (19ms)
13. **Route Based on Score** - Routed to improvement path (80% < 85%)
14. **Generate Improvement Email (<85%)** - Built HTML email (28ms)
15. **Send HTML Email** - FAILED (5ms)

---

## Error Details

### Primary Error

**Node:** Send HTML Email
**Type:** NodeOperationError
**Message:** This operation expects the node's input data to contain a binary file 'data', but none was found

### Root Cause Analysis

The workflow has two score-based paths:

1. **Score ≥85%** (SUCCESS PATH):
   - Generate Success Email (≥85%)
   - **Generate PDF HTML** → **Convert HTML to PDF** → Send HTML Email
   - This path generates the binary PDF attachment

2. **Score <85%** (IMPROVEMENT PATH):
   - Generate Improvement Email (<85%)
   - Send HTML Email **DIRECTLY** (no PDF generation)
   - Gmail node is still configured to expect PDF attachment

**The Issue:** The test submission scored 80%, triggering the improvement path. However, the "Send HTML Email" node is configured with:

```json
"options": {
  "attachmentsUi": {
    "attachmentsBinary": [
      {
        "property": "data"
      }
    ]
  }
}
```

This configuration expects a binary file called 'data' but the improvement path does not generate a PDF, causing the error.

---

## Score Breakdown

### Actual Score: 80%

- **Completeness:** 30/40 points
- **Clarity:** 25/30 points
- **Usability:** 25/30 points

### Missing Elements Identified by AI

1. **Purpose Statement**
   - Why: Establishes rationale for the SOP
   - Fix: Add a section clearly stating the purpose

2. **Checklist/Verification**
   - Why: Key verification points to ensure nothing is overlooked
   - Fix: Include a checklist of key tasks

3. **Document Control**
   - Why: Ensures proper versioning and accountability
   - Fix: Add version, author, review date

### Quick Wins Suggested

1. **Add Purpose Section** - Clearly outline the objective
2. **Include a Checklist** - Create task checklist for each step
3. **Establish Document Control** - Provide versioning info

---

## Expected vs Actual

### Expected Behavior

- Score ≥85% → Generate PDF → Attach to email → Send success email
- Score <85% → Send improvement email without PDF attachment

### Actual Behavior

- Score = 80% → Routed to improvement path
- Improvement email generated successfully
- Gmail node attempted to attach PDF that doesn't exist
- Execution failed with binary data error

---

## Test Results

| Test Aspect | Status | Notes |
|-------------|--------|-------|
| Webhook trigger | PASS | Successfully received POST request |
| Form data parsing | PASS | All fields parsed correctly |
| Audio/text routing | PASS | Correctly used text input (no audio) |
| LLM validation | PASS | OpenAI returned valid scoring (12.3s) |
| SOP scoring | PASS | Calculated 80% correctly |
| LLM SOP generation | PASS | Generated improved SOP (21.8s) |
| Score routing | PASS | Correctly routed to <85% path |
| HTML email generation | PASS | Built improvement email with missing elements |
| PDF generation | N/A | Not executed (score <85%) |
| Email delivery | FAIL | Binary attachment expected but missing |
| Airtable logging | N/A | Not reached due to error |
| Webhook response | N/A | Not reached due to error |

---

## Issues Found

### Critical Issue 1: PDF Attachment Configuration

**Severity:** HIGH
**Node:** Send HTML Email

**Problem:** The Gmail node has `attachmentsBinary` configured globally, but only the success path (≥85%) generates a PDF. The improvement path (<85%) does not generate a PDF but still tries to attach it.

**Impact:** Workflow fails for ANY score <85%, preventing users from receiving their analysis email.

**Solution:** Use conditional logic or separate Gmail nodes:

**Option A (Conditional):**
```javascript
"options": {
  "attachmentsUi": {
    "attachmentsBinary": {{ $json.sop_score >= 85 ? [{"property": "data"}] : [] }}
  }
}
```

**Option B (Two Gmail Nodes):**
- "Send Success Email with PDF" (≥85% path) - with attachment
- "Send Improvement Email" (<85% path) - without attachment

---

### Issue 2: Test Data Score Gap

**Severity:** MEDIUM
**Problem:** Test data was designed to be comprehensive but still scored only 80%, falling short of the 85% threshold needed to test PDF generation.

**Missing from Test Data:**
- Explicit purpose statement section
- Verification checklist format
- Document control metadata (version, author, date)

**For Next Test:** Include these elements explicitly:

```json
{
  "goal": "PURPOSE: Ensure consistent client onboarding...",
  "processSteps": "## PURPOSE\n[statement]\n\n## PREPARATION\n[prerequisites]\n\n## PROCESS\n1. Step...\n\n## CHECKLIST\n- [ ] Verify...\n\n## DOCUMENT CONTROL\nVersion: 1.0\nAuthor: Sway\nReview Date: 2026-01-30"
}
```

---

## Recommendations

### Immediate Fix (Critical)

1. **Separate Gmail nodes** for success and improvement paths
   - Success path: Include PDF attachment
   - Improvement path: No attachment

2. **OR use conditional attachment** in single Gmail node (if n8n supports dynamic options)

### Testing Improvements

1. **Create two test cases:**
   - Test Case 1: Comprehensive SOP (target ≥85%) → Test PDF generation
   - Test Case 2: Basic SOP (target <85%) → Test improvement email

2. **Add explicit SOP structure** to test data to ensure ≥85% score:
   - Purpose section
   - Preparation requirements
   - Numbered process steps
   - Verification checklist
   - Document control metadata

### Workflow Enhancements

1. **Add validation before email node:**
   - Check if binary data exists before attempting attachment
   - Log warning if score ≥85% but PDF missing

2. **Error handling improvement:**
   - Catch binary missing error specifically
   - Send email without attachment as fallback
   - Notify admin of PDF generation failure

---

## Performance Metrics

- **Total Duration:** 34.3 seconds
- **LLM Validation:** 12.3s (35.9% of total)
- **LLM SOP Generation:** 21.8s (63.6% of total)
- **Other Processing:** 0.2s (0.5% of total)

**LLM calls dominate execution time (99.5%)**, which is expected for this workflow.

---

## Next Steps

1. Fix the Gmail attachment configuration (solution-builder-agent)
2. Create enhanced test data with explicit SOP structure
3. Re-test both paths:
   - Score ≥85% with PDF
   - Score <85% without PDF
4. Verify Airtable logging works correctly
5. Confirm webhook response returns properly

---

## Files

**Test Data:** See JSON block above
**Execution URL:** https://n8n.oloxa.ai/workflow/ikVyMpDI0az6Zk4t/executions/7096
**Error Execution:** https://n8n.oloxa.ai/workflow/ikVyMpDI0az6Zk4t/executions/7097
