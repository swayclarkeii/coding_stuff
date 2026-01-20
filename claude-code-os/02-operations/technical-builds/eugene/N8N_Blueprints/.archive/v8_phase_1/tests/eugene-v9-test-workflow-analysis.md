# Eugene V9 Test Workflow Analysis

**Test Workflow ID:** 0nIrDvXnX58VPxWW
**Workflow Name:** Eugene V8 Document Test Runner - Phase 0
**Spreadsheet:** https://docs.google.com/spreadsheets/d/1zbonuRUDIkI5xq8gaLDJZtqf7xVtH7iMjBg8A31svsw/edit
**Analysis Date:** 2026-01-18
**Status:** Needs Updates for v9 Architecture

---

## Executive Summary

The test workflow is still configured for **v8 architecture** and needs 2 critical updates:

1. Remove Chunk 2 from execution checks (now bypassed in v9)
2. Update column header to reflect v9 workflow chain

**Root cause of duplicate rows:** The workflow checks for Chunk 2 executions which no longer run, resulting in "not_found" statuses that trigger the "Mark Failed" path incorrectly.

---

## v9 Architecture Changes

### What Changed

**v8 Flow:**
```
Pre-Chunk 0 → Chunk 2 → Chunk 2.5
```

**v9 Flow:**
```
Pre-Chunk 0 → Chunk 2.5 (Chunk 2 bypassed)
```

### Impact on Test Workflow

The test workflow currently checks **3 workflows**:
- Pre-Chunk 0 ✅ (still active)
- Chunk 2 ❌ (bypassed, no longer runs)
- Chunk 2.5 ✅ (still active)

When testing documents in v9, Chunk 2 will show `status: "not_found"` because it doesn't execute, causing tests to incorrectly fail.

---

## Critical Issues Found

### Issue 1: Hardcoded Chunk 2 Reference

**Node:** "Query n8n Executions" (code-query-executions-1)
**Line 294-303 in workflow:**

```javascript
const workflows = [
  { id: 'YGXWjWcBIk66ArvT', name: 'Pre-Chunk 0' },
  { id: 'qKyqsL64ReMiKpJ4', name: 'Chunk 2' },       // ❌ REMOVE THIS
  { id: 'okg8wTqLtPUwjQ18', name: 'Chunk 2.5' }
];
```

**Fix Required:**

```javascript
// v9 Update: Chunk 2 is bypassed, only check Pre-Chunk 0 and Chunk 2.5
const workflows = [
  { id: 'YGXWjWcBIk66ArvT', name: 'Pre-Chunk 0' },
  { id: 'okg8wTqLtPUwjQ18', name: 'Chunk 2.5' }
];
```

---

### Issue 2: Spreadsheet Column Header Outdated

**Current Header:** "Execution IDs (Pre/C2/C2.5)"
**Should Be:** "Execution IDs (Pre/C2.5)"

This affects **5 nodes** that reference this column:
1. Prepare Initial Row Data (code-prepare-init-1)
2. Update Status to Testing (google-sheets-update-testing-1)
3. Mark Passed (google-sheets-update-passed-1)
4. Mark Failed (google-sheets-update-failed-1)
5. Prepare Testing Status Update (code-prepare-testing-1)
6. Prepare Passed Status Update (code-prepare-passed-1)
7. Prepare Failed Status Update (code-prepare-failed-1)

**Fix Required:** Update all column references from `'Execution IDs (Pre/C2/C2.5)'` to `'Execution IDs (Pre/C2.5)'`

---

### Issue 3: Root Cause of Duplicate/Empty Rows (SOLVED)

**What Happened:**
1. Test workflow sends email with PDF attachment
2. Waits 120 seconds
3. Queries n8n for executions of Pre-Chunk 0, Chunk 2, and Chunk 2.5
4. Chunk 2 returns `status: "not_found"` (because it doesn't run in v9)
5. "Merge Execution Results" sees `allPassed = false`
6. "Check All Passed" routes to "Prepare Failed Status Update"
7. Failed node creates row with error: "Chunk 2: not_found"

**Why "testing" and empty "failed" rows appeared:**
- "testing" rows = workflow started test, marked status as "testing"
- "failed" rows = Chunk 2 not found, incorrectly marked as failed

**Solution:** Remove Chunk 2 from workflow checks (Fix #1 above)

---

## Detailed Fix Instructions

### Fix 1: Update "Query n8n Executions" Node

**Node ID:** code-query-executions-1
**Action:** Replace entire code block

**New Code:**

```javascript
// Split into 2 items (one per workflow to query)
// v9 Update: Only check Pre-Chunk 0 and Chunk 2.5 (Chunk 2 is bypassed)
const testStartTime = $json['Test Start'];
const workflows = [
  { id: 'YGXWjWcBIk66ArvT', name: 'Pre-Chunk 0' },
  { id: 'okg8wTqLtPUwjQ18', name: 'Chunk 2.5' }
];

return workflows.map(wf => ({
  json: {
    workflowId: wf.id,
    workflowName: wf.name,
    testStartTime: testStartTime,
    documentName: $json['Document Name'],
    fileId: $json['File ID']
  }
}));
```

**Changes:**
- Removed Chunk 2 from workflows array
- Updated comment to reflect v9 architecture
- Reduced from 3 HTTP requests to 2 (20% faster)

---

### Fix 2: Update Column References in All Nodes

**Nodes to Update:**

1. **Prepare Initial Row Data** (code-prepare-init-1)
   - Line 241: Change `'Execution IDs (Pre/C2/C2.5)'` to `'Execution IDs (Pre/C2.5)'`

2. **Update Status to Testing** (google-sheets-update-testing-1)
   - Schema line 188: Change `"Execution IDs (Pre/C2/C2.5)"` to `"Execution IDs (Pre/C2.5)"`

3. **Mark Passed** (google-sheets-update-passed-1)
   - Schema line 289: Change `"Execution IDs (Pre/C2/C2.5)"` to `"Execution IDs (Pre/C2.5)"`

4. **Mark Failed** (google-sheets-update-failed-1)
   - Schema line 345: Change `"Execution IDs (Pre/C2/C2.5)"` to `"Execution IDs (Pre/C2.5)"`

5. **Prepare Testing Status Update** (code-prepare-testing-1)
   - Line 383: Change `'Execution IDs (Pre/C2/C2.5)'` to `'Execution IDs (Pre/C2.5)'`

6. **Prepare Passed Status Update** (code-prepare-passed-1)
   - Line 397: Change `'Execution IDs (Pre/C2/C2.5)'` to `'Execution IDs (Pre/C2.5)'`

7. **Prepare Failed Status Update** (code-prepare-failed-1)
   - Line 408: Change `'Execution IDs (Pre/C2/C2.5)'` to `'Execution IDs (Pre/C2.5)'`

**OR** (easier): Update the spreadsheet header itself from "Execution IDs (Pre/C2/C2.5)" to "Execution IDs (Pre/C2.5)" and the workflow will auto-match.

---

## Pre-Test Checklist

Before running v9 tests:

- [ ] Apply Fix 1: Remove Chunk 2 from execution checks
- [ ] Apply Fix 2: Update column header references
- [ ] Clear old test data from spreadsheet (rows with "testing" and "failed" status)
- [ ] Verify Pre-Chunk 0 is active (ID: YGXWjWcBIk66ArvT)
- [ ] Verify Chunk 2.5 is active (ID: okg8wTqLtPUwjQ18)
- [ ] Verify Chunk 2 is INACTIVE (ID: qKyqsL64ReMiKpJ4)
- [ ] Activate test workflow (ID: 0nIrDvXnX58VPxWW)

---

## Expected v9 Test Behavior

### Happy Path

1. Document appears in spreadsheet with status "pending"
2. Test starts, status changes to "testing"
3. Email sent with PDF attachment
4. Pre-Chunk 0 triggers
5. Pre-Chunk 0 calls Chunk 2.5 directly (skips Chunk 2)
6. Both workflows complete successfully
7. Test workflow marks status as "passed"
8. Execution IDs populated: "[pre-chunk-0-id], [chunk-2.5-id]"

### Failure Path

1-4. Same as happy path
5. One of the workflows fails or times out
6. Test workflow marks status as "failed"
7. Error Details shows: "Pre-Chunk 0: error" or "Chunk 2.5: error"
8. Execution IDs show which workflows ran

### No More False Failures

- ❌ Old behavior: "Chunk 2: not_found" incorrectly marked as failed
- ✅ New behavior: Only checks workflows that actually run in v9

---

## Testing Strategy

### Phase 1: Single Document Test

1. Pick 1 PDF from Drive folder
2. Update spreadsheet to only include that document
3. Run test workflow manually
4. Verify:
   - Only 1 row created in spreadsheet
   - Status progresses: pending → testing → passed/failed
   - Execution IDs show 2 values (Pre-Chunk 0 + Chunk 2.5)
   - No "Chunk 2: not_found" errors

### Phase 2: Multi-Document Test

1. Add 3-5 documents to spreadsheet
2. Run test workflow
3. Verify:
   - Each document has exactly 1 row
   - No duplicate rows
   - No empty rows with "failed" status
   - Loop continues until all documents tested

### Phase 3: Error Handling Test

1. Test with a corrupted/invalid PDF
2. Verify:
   - Error is captured correctly
   - Error Details shows meaningful message (not "undefined: not_found")
   - Execution IDs show which workflow failed

---

## Migration Notes

**Workflow Version:** This is version 33 of the workflow (versionCounter: 33)

**After applying fixes:**
- Version will increment to 34
- Old test results (with Chunk 2 references) will still be in spreadsheet
- Recommend clearing spreadsheet before first v9 test run

**Backward Compatibility:**
- Cannot test v8 workflows with this updated test runner
- If v8 testing is needed, create a separate test workflow or revert this one

---

## Questions for Sway

1. **Should we keep old test data?** Or clear the spreadsheet before v9 testing?
2. **Workflow name update?** Change from "Eugene V8 Document Test Runner" to "Eugene V9 Document Test Runner"?
3. **How many documents to test initially?** Recommend starting with 1-2 before full batch.

---

## Next Steps

**Sway's Decision Required:**

**Option A: I fix the workflow now (recommended)**
- Apply both fixes via MCP update
- Clear spreadsheet test data
- Activate workflow
- Run 1 test document to verify

**Option B: Sway delegates to solution-builder-agent**
- More appropriate for complex changes (3+ nodes)
- Can make fixes + add additional improvements
- Would take longer but more thorough

**Option C: Manual fixes in n8n UI**
- Sway makes changes in browser
- I can provide step-by-step instructions

Which approach would you prefer?
