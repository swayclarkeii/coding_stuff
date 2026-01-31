# n8n Test Report – Fathom AI Analysis v2 - Multi-Call

**Test Date:** 2026-01-30
**Workflow ID:** QTmNH1MWW5mGBTdW
**Workflow Name:** Fathom AI Analysis v2 - Multi-Call

## Summary
- Total tests: 1
- ✅ Passed: 0
- ❌ Failed: 1

---

## Test Details

### Test: Ambush TV Discovery Call

**Status:** ❌ FAIL

**Execution Status:** 404 Not Found (webhook not registered)

**Execution ID:** Not created (webhook request rejected)

**Error Details:**
- **Error message:** "The requested webhook 'POST fathom-ai-analysis-v2' is not registered."
- **HTTP status:** 404
- **Workflow ID:** QTmNH1MWW5mGBTdW
- **Workflow active status:** true (but webhook not initialized)
- **Webhook path:** fathom-ai-analysis-v2
- **HTTP method:** POST

**Root Cause:**

The workflow shows as "active: true" in n8n's database, but the webhook trigger hasn't been properly registered with the n8n webhook server. This is a known n8n issue when workflows are created or modified via the API - the webhook doesn't initialize until the workflow is manually toggled in the UI.

**Expected Behavior:**

1. Workflow accepts POST requests to webhook path "fathom-ai-analysis-v2"
2. Processes meeting transcript through 4 parallel AI calls:
   - AI Call 1 - Discovery (summary, key_insights, pain_points, action_items)
   - AI Call 2 - Opportunity (quick_wins, pricing_strategy)
   - AI Call 3 - Technical (complexity_assessment, requirements)
   - AI Call 4 - Strategic (roadmap, client_journey_map)
3. Parses all 4 JSON responses
4. Merges results using append mode
5. Combines all fields into single output object
6. Returns combined output with all 10 fields plus company

**Test Input Data:**

```json
{
  "combined_transcript": "Meeting between Sway Clarke from Oloxa and Sindbad Farahmand from Ambush TV / Bold Move Media. Discussion about freelancer payment management, rate synchronization across Google Sheets, and invoice validation. Sindbad mentioned spending 5-6 hours weekly on invoice review. They have 150,000 euros outstanding from clients, with 100,000 overdue more than 30 days. Admin team member Leonor handles rate updates across 3 Google Sheets. Key pain points include manual rate syncing, delayed invoicing, and error-prone payment reconciliation. Sindbad hourly rate is 50 euros. Admin team rate is 20 euros per hour. They discussed automating the rate synchronization as a quick win, estimated at 1-2 weeks implementation. The invoice validation system would be a larger project at 6-8 weeks. Sindbad expressed interest in a phased approach starting with quick wins. Budget range discussed was 2-3K initially for quick wins, with openness to more for the full admin chain automation. Bold Move TV is a separate entity handling media production, currently at 10 percent of revenue. Ambush TV is the main production company at 90 percent of revenue.",
  "contact_email": "sindbad@boldmove.tv",
  "contact_name": "Sindbad Farahmand",
  "title": "Discovery Call - Ambush TV Admin Automation"
}
```

**Expected Output:**

```json
{
  "company": "Boldmove",
  "summary": "[500-1000 word executive summary]",
  "key_insights": "[500-800 word analysis]",
  "pain_points": "[500-800 word categorized analysis]",
  "action_items": "[300-600 word structured list]",
  "quick_wins": "[500-800 word opportunity matrix]",
  "pricing_strategy": "[500-800 word value-based pricing analysis]",
  "complexity_assessment": "[500-800 word technical scoring]",
  "requirements": "[500-800 word structured requirements]",
  "roadmap": "[500-800 word phased implementation plan]",
  "client_journey_map": "[500-800 word journey analysis]"
}
```

**Workflow Structure (Verified):**

- **13 nodes total**
- **12 connections**
- **Webhook trigger:** POST, path "fathom-ai-analysis-v2", responseMode: "responseNode"
- **Extract Company node:** Code node extracts company from email domain
- **4 parallel OpenAI calls:** All using GPT-4o model
  - AI Call 1 - Discovery (returns 4 fields)
  - AI Call 2 - Opportunity (returns 2 fields)
  - AI Call 3 - Technical (returns 2 fields)
  - AI Call 4 - Strategic (returns 2 fields)
- **4 parsing nodes:** Clean JSON responses from AI calls
- **Merge node:** Append mode with 4 inputs
- **Combine Output node:** Merges all fields into single object, adds company
- **Respond to Webhook node:** Returns combined result

**Credentials:** All AI nodes use "openai-main" credential (OpenAI account)

---

## Next Steps Required

### Immediate Action (Manual)

1. **Toggle workflow OFF and ON in n8n UI:**
   - Go to https://n8n.oloxa.ai
   - Find workflow "Fathom AI Analysis v2 - Multi-Call" (ID: QTmNH1MWW5mGBTdU)
   - Click the toggle to deactivate
   - Wait 2-3 seconds
   - Click the toggle to reactivate
   - This will properly register the webhook with the n8n server

### After Webhook Registration

2. **Re-run this test** with the same test data
3. **Verify execution results:**
   - All 4 AI calls execute successfully
   - Execution duration: 60-120 seconds (expected for 4 GPT-4o calls)
   - No errors in parsing nodes
   - Merge node receives all 4 inputs
   - Final output contains all 10 expected fields
   - Company field = "Boldmove" (extracted from "boldmove.tv")

### Validation Checklist

- [ ] Webhook responds with 200 OK
- [ ] All 4 AI nodes execute
- [ ] All 4 parsing nodes succeed
- [ ] Merge node receives 4 items
- [ ] Output contains all 10 fields
- [ ] Company = "Boldmove"
- [ ] No errors in execution log

---

## Technical Notes

**Why webhook didn't register:**
- n8n workflows created/modified via API don't always auto-register webhooks
- The workflow's `active: true` flag is set in the database
- But the webhook listener process hasn't initialized the route
- Manual toggle forces re-initialization

**Workflow last updated:** 2026-01-30T20:49:10.479Z
**Workflow version:** v7 (versionId: c5bb1bd4-722b-477c-8108-2db40949715f)
**Last publish event:** Activated at 2026-01-30T20:49:24.430Z

---

## Test Configuration

- **Test method:** `n8n_test_workflow` MCP tool
- **Trigger type:** webhook
- **HTTP method:** POST
- **Wait for response:** true
- **Timeout:** 300000ms (5 minutes)
- **Webhook path:** fathom-ai-analysis-v2

---

**Report generated by:** test-runner-agent
**Report timestamp:** 2026-01-30T20:51:27Z
