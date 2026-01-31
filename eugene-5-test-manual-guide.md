# Eugene Quick Test Runner - 5 Test Manual Execution Guide

## Overview
This guide walks through executing 5 tests against the Eugene Quick Test Runner workflow to verify production changes.

## Workflow Details
- **Test Runner ID:** fIqmtfEDuYM7gbE9
- **Chunk 2.5 ID:** okg8wTqLtPUwjQ18
- **Webhook URL:** https://n8n.oloxa.ai/webhook/eugene-quick-test

## Current Status
- **Latest execution before tests:** #7361 (completed 2026-01-31 00:17:49 UTC)

## Test Execution Process

### For Each Test (Repeat 5 Times)

1. **Fire the webhook:**
   ```bash
   curl -X POST "https://n8n.oloxa.ai/webhook/eugene-quick-test" \
     -H "Content-Type: application/json" \
     -d '{}' \
     --silent \
     --max-time 15
   ```

2. **Wait 30 seconds** (let the execution register)

3. **Check n8n UI for new executions:**
   - Test Runner: https://n8n.oloxa.ai/workflow/fIqmtfEDuYM7gbE9
   - Chunk 2.5: https://n8n.oloxa.ai/workflow/okg8wTqLtPUwjQ18

4. **Poll every 60 seconds** until both complete (max 12 minutes)

5. **Record results** in the test log below

## Test Results

### Test 1 of 5
- **Webhook fired:** [ ] Yes [ ] No
- **Time started:** _____________
- **Test Runner execution ID:** _____________
- **Test Runner status:** [ ] Success [ ] Error [ ] Timeout
- **Chunk 2.5 execution ID:** _____________
- **Chunk 2.5 status:** [ ] Success [ ] Error [ ] Timeout
- **Time completed:** _____________
- **Duration:** _____________
- **Notes:** _____________

### Test 2 of 5
- **Webhook fired:** [ ] Yes [ ] No
- **Time started:** _____________
- **Test Runner execution ID:** _____________
- **Test Runner status:** [ ] Success [ ] Error [ ] Timeout
- **Chunk 2.5 execution ID:** _____________
- **Chunk 2.5 status:** [ ] Success [ ] Error [ ] Timeout
- **Time completed:** _____________
- **Duration:** _____________
- **Notes:** _____________

### Test 3 of 5
- **Webhook fired:** [ ] Yes [ ] No
- **Time started:** _____________
- **Test Runner execution ID:** _____________
- **Test Runner status:** [ ] Success [ ] Error [ ] Timeout
- **Chunk 2.5 execution ID:** _____________
- **Chunk 2.5 status:** [ ] Success [ ] Error [ ] Timeout
- **Time completed:** _____________
- **Duration:** _____________
- **Notes:** _____________

### Test 4 of 5
- **Webhook fired:** [ ] Yes [ ] No
- **Time started:** _____________
- **Test Runner execution ID:** _____________
- **Test Runner status:** [ ] Success [ ] Error [ ] Timeout
- **Chunk 2.5 execution ID:** _____________
- **Chunk 2.5 status:** [ ] Success [ ] Error [ ] Timeout
- **Time completed:** _____________
- **Duration:** _____________
- **Notes:** _____________

### Test 5 of 5
- **Webhook fired:** [ ] Yes [ ] No
- **Time started:** _____________
- **Test Runner execution ID:** _____________
- **Test Runner status:** [ ] Success [ ] Error [ ] Timeout
- **Chunk 2.5 execution ID:** _____________
- **Chunk 2.5 status:** [ ] Success [ ] Error [ ] Timeout
- **Time completed:** _____________
- **Duration:** _____________
- **Notes:** _____________

## Summary

### Overall Results
- **Total tests:** 5
- **Passed:** _____ / 5
- **Failed:** _____ / 5
- **Timeouts:** _____ / 5

### Known Issues Encountered
- [ ] 250814_Schloßberg 13.pdf auto-skip
- [ ] JSON parse errors from Claude
- [ ] Other: _____________

### Verification Points
- [ ] Files are being moved (not copied)
- [ ] Tracker is being updated correctly
- [ ] No WorkflowHasIssuesError
- [ ] Consistent success rate

### Recommendations
_____________

---

## Quick Reference

**Check latest Test Runner execution:**
- n8n UI: https://n8n.oloxa.ai/workflow/fIqmtfEDuYM7gbE9
- Or via agent: `n8n_executions(action: "list", workflowId: "fIqmtfEDuYM7gbE9", limit: 1)`

**Check latest Chunk 2.5 execution:**
- n8n UI: https://n8n.oloxa.ai/workflow/okg8wTqLtPUwjQ18
- Or via agent: `n8n_executions(action: "list", workflowId: "okg8wTqLtPUwjQ18", limit: 1)`

**Expected timing:**
- Each test: ~4-5 minutes
- Total for 5 tests: ~20-25 minutes
