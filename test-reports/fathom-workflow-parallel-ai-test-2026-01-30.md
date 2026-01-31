# Fathom Workflow - Parallel AI Calls Test Report

**Date:** 2026-01-30
**Workflow ID:** cMGbzpq1RXpL0OHY
**Workflow Name:** Fathom Transcript Workflow Final_22.01.26
**Test Type:** Parallel AI execution verification

---

## Test Summary

- **Total AI Calls Expected:** 4 parallel calls
- **AI Calls Executed:** 1 (Discovery Analysis only)
- **Execution Status:** ERROR
- **Execution ID:** 7290
- **Duration:** 227,678ms (3m 47s)

---

## Critical Finding: Only 1 of 4 AI Calls Executed

### Expected Parallel Execution

From "Enhanced AI Analysis" node, 4 AI calls should execute in parallel:

1. Call AI: Discovery Analysis
2. Call AI: Opportunity Analysis
3. Call AI: Technical Analysis
4. Call AI: Strategic Analysis

### Actual Execution

**ONLY executed:**
- Call AI: Discovery Analysis (72,033ms execution time)

**NOT executed:**
- Call AI: Opportunity Analysis - MISSING
- Call AI: Technical Analysis - MISSING
- Call AI: Strategic Analysis - MISSING

---

## Execution Path Analysis

The workflow executed these nodes successfully:

1. Manual Trigger (skipped)
2. Route: Webhook or API (success, 32ms)
3. IF: Webhook or API?1 (success, 3ms)
4. Process Webhook Meeting (skipped)
5. Enhanced AI Analysis (success, 47ms, 3 items output)
6. **Call AI: Discovery Analysis** (success, 72,033ms) ✅
7. Parse Discovery Response (success, 65ms)
8. Merge All Analysis (success, 1,946ms, 1 item received)
9. Build Performance Prompt (success, 34ms)
10. Call AI for Performance (success, 9,066ms)
11. Parse Performance Response (success, 21ms)
12. Merge Performance Data (success, 5ms)
13. Prepare Performance Data (success, 29ms)
14. Save Performance to Airtable (success, 610ms)
15. **Build Slack Blocks** (ERROR, 1,892ms) ❌

---

## Merge All Analysis - Data Received

The "Merge All Analysis" node received **only 1 item** (from Discovery Analysis).

It should have received **4 items** (one from each AI call).

### Field Population Status

From the single item received:

**Populated fields (from Discovery Analysis):**
- summary ✅
- key_insights ✅
- pain_points ✅
- action_items ✅
- meeting_title ✅
- meeting_date ✅
- contact_name ✅
- contact_email ✅

**Empty fields (missing from other AI calls):**
- quick_wins ❌ (should come from Opportunity Analysis)
- pricing_strategy ❌ (should come from Strategic Analysis)
- complexity_assessment ❌ (should come from Technical Analysis)
- requirements ❌ (should come from Technical Analysis)
- roadmap ❌ (should come from Strategic Analysis)
- client_journey_map ❌ (should come from Opportunity Analysis)
- company_name ❌ (empty string)

**Result:** 8 of 13 fields populated (61.5%), but this is misleading because only 1 of 4 AI analyses ran.

---

## Error Details

**Failed Node:** Build Slack Blocks
**Error Type:** TypeError
**Error Message:**
```
Cannot assign to read only property 'name' of object 'Error: Referenced node doesn't exist'
```

**Stack Trace:**
```
TypeError: Cannot assign to read only property 'name' of object 'Error: Referenced node doesn't exist'
    at new ExecutionBaseError (/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-workflow@file+packages+workflow/node_modules/n8n-workflow/dist/cjs/errors/abstract/execution-base.error.js:24:23)
    at new ExpressionError (/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-workflow@file+packages+workflow/node_modules/n8n-workflow/dist/cjs/errors/expression.error.js:19:13)
```

**Note:** This error is downstream from the AI calls and not related to why the 3 AI calls didn't execute.

---

## Root Cause Analysis

### Why Only 1 AI Call Executed

Looking at the execution data:
- Enhanced AI Analysis output: 3 items
- Call AI: Discovery Analysis received 3 items and processed them
- The other 3 AI calls (Opportunity, Technical, Strategic) received NO items

**Hypothesis:** The parallel split from "Enhanced AI Analysis" is not distributing data correctly to all 4 AI call nodes. Only the first connection is receiving data.

### Workflow Structure

From the structure analysis:
```
Enhanced AI Analysis → [
  Call AI: Discovery Analysis,
  Call AI: Opportunity Analysis,
  Call AI: Technical Analysis,
  Call AI: Strategic Analysis
]
```

All 4 connections exist in the workflow definition, but only the first one received data during execution.

---

## Recommendations

### Immediate Fix Required

1. **Check Enhanced AI Analysis node configuration**
   - Verify it's set to send data to ALL 4 outputs
   - Check if there's a condition or filter preventing data flow

2. **Check connection configuration**
   - Verify all 4 connections from Enhanced AI Analysis are properly configured
   - Check if connections specify output index correctly

3. **Test with minimal workflow**
   - Create a simple test with just the parallel split to isolate the issue

4. **Review recent changes**
   - Check if the connection refresh affected the parallel execution logic
   - Review any recent workflow modifications

---

## Test Data

**Trigger payload:**
```json
{
  "test": true,
  "timestamp": "2026-01-30T19:50:00+01:00"
}
```

**Execution started:** 2026-01-30T19:39:36.484Z
**Execution stopped:** 2026-01-30T19:43:24.162Z
**Duration:** 227,678ms (3m 47.7s)

---

## Next Steps

1. Investigate why Enhanced AI Analysis node only sends data to first output
2. Fix parallel execution issue
3. Re-test with same payload
4. Verify all 4 AI calls execute and Merge receives 4 items
5. Verify all 13 fields are populated correctly
6. Fix Build Slack Blocks error (likely referencing missing data)

---

## Status

❌ **TEST FAILED**

**Critical Issue:** Only 1 of 4 parallel AI calls executed. Workflow cannot provide complete analysis until parallel execution is fixed.
