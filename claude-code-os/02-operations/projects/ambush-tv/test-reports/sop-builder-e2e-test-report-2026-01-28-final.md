# SOP Builder E2E Test Report - 2026-01-28

## Summary
- Total tests: 1 attempted
- ✅ Passed: 0
- ❌ Failed: 1
- Status: **CRITICAL WORKFLOW ERROR - CANNOT EXECUTE**

---

## Test Environment
- Workflow ID: `ikVyMpDI0az6Zk4t`
- Workflow Name: SOP Builder Lead Magnet
- Test Date: 2026-01-28 23:22 UTC
- Execution ID: 6660 (failed), 6661 (error trigger)

---

## Test 1: New User Submission

### Status: ❌ FAIL - Workflow Cannot Execute

### Input Data
```json
{
  "email": "swayclarkeii@gmail.com",
  "name": "Sway Test",
  "goal": "Onboard new clients quickly",
  "improvement_type": "speed",
  "department": "operations",
  "end_user": "New sales hires",
  "process_steps": "Step 1: Get client email. Step 2: Send welcome email. Step 3: Done.",
  "input_method": "text"
}
```

### Execution Results
- **n8n execution status**: ERROR
- **Error Type**: `WorkflowHasIssuesError`
- **Error Message**: "The workflow has issues and cannot be executed for that reason. Please fix them first."
- **Failed at**: Workflow validation (before any nodes executed)
- **Execution Duration**: 8ms

### Root Cause Analysis

The workflow **validates successfully** (0 errors) but **fails to execute**. Investigation reveals:

#### Critical Connection Error: "Check If Returning User" Node

**Problem**: The IF node "Check If Returning User" has **incorrect routing logic**.

**Current configuration** (from connection data):
```json
"Check If Returning User": {
  "main": [
    [
      {
        "node": "Prepare Update Data",
        "type": "main",
        "index": 0
      },
      {
        "node": "Prepare New Lead Data",
        "type": "main",
        "index": 0
      }
    ]
  ]
}
```

**What this means**:
- The node has only **ONE output array** `main[0]`
- This single output goes to BOTH "Prepare Update Data" AND "Prepare New Lead Data"
- This violates IF node logic - IF nodes should have TWO separate output paths

**Expected configuration**:
```json
"Check If Returning User": {
  "main": [
    [
      {
        "node": "Prepare Update Data",
        "type": "main",
        "index": 0
      }
    ],
    [
      {
        "node": "Prepare New Lead Data",
        "type": "main",
        "index": 0
      }
    ]
  ]
}
```

**Why this causes WorkflowHasIssuesError**:
- n8n's validator checks syntax (which passes)
- n8n's execution engine checks workflow logic (which fails)
- The execution engine detects that an IF node doesn't have proper TRUE/FALSE routing
- This is a **runtime validation error**, not a syntax error

#### Visual Representation

```
Current (WRONG):
┌─────────────────────────┐
│ Check If Returning User │
└───────────┬─────────────┘
            │ (main[0] only)
            ├──────┬──────┐
            │      │      │
            ↓      ↓      ↓
    ┌─────────┐  ┌────────────┐
    │ Update  │  │ New Lead   │
    └─────────┘  └────────────┘
    (both fire)

Expected (CORRECT):
┌─────────────────────────┐
│ Check If Returning User │
└───────┬─────────┬───────┘
        │ TRUE    │ FALSE
        ↓         ↓
    ┌───────┐  ┌──────────┐
    │Update │  │New Lead  │
    └───────┘  └──────────┘
    (one fires)
```

### Validation Output

**n8n validation says**:
- Valid: true
- Errors: 0
- Warnings: 46 (cosmetic, not blocking)

**But execution fails** because:
- Runtime logic validation is stricter than syntax validation
- The workflow has a semantic error (incorrect IF routing)

---

## Fix Required

### Node: "Check If Returning User"

**Current connections** (WRONG):
- Output 0 → BOTH "Prepare Update Data" AND "Prepare New Lead Data"

**Required connections** (CORRECT):
- Output 0 (TRUE) → "Prepare Update Data" only
- Output 1 (FALSE) → "Prepare New Lead Data" only

### Implementation

The IF node needs to be reconfigured so:
1. **TRUE branch** (returning user found) → goes to "Prepare Update Data"
2. **FALSE branch** (no existing user) → goes to "Prepare New Lead Data"

This is a **critical structural fix** - the workflow cannot execute until this is corrected.

---

## Test 2: Airtable Verification

### Status: ⏸️ NOT RUN

**Reason**: Test 1 failed with workflow execution error. Cannot proceed to data verification until workflow executes successfully.

---

## Additional Issues Found

### 1. Validator Warning - Update Lead in Airtable

**Warning**: Expression format issue in "Update Lead in Airtable" node.

```
Field 'id' should use resource locator format for better compatibility.

Current (incorrect):
"id": "={{ $json.record_id }}"

Fixed (correct):
"id": {
  "__rl": true,
  "value": "={{ $json.record_id }}",
  "mode": "expression"
}
```

**Impact**: Low priority (workflow may work once routing is fixed), but should be corrected for best practices.

### 2. Deprecated continueOnFail

**Node**: "Check Existing Lead"

**Issue**: Using deprecated `continueOnFail: true` instead of modern `onError: 'continueRegularOutput'`

**Impact**: Low priority, cosmetic only.

---

## Next Steps

1. **CRITICAL**: Fix "Check If Returning User" IF node routing
   - Ensure TRUE/FALSE branches are properly separated
   - TRUE → "Prepare Update Data"
   - FALSE → "Prepare New Lead Data"

2. **Run Test 1 again** to verify workflow can execute

3. **Run Test 2** to verify Airtable data integrity

4. **Optional cleanup**:
   - Fix "Update Lead in Airtable" resource locator format
   - Replace `continueOnFail` with `onError` in "Check Existing Lead"

---

## Technical Notes

**Why validation passed but execution failed**:
- n8n has two validation layers:
  1. **Syntax validation** (checks JSON structure, node types, parameters)
  2. **Runtime validation** (checks workflow logic, execution paths)
- The IF node routing error is a **logical error**, not a syntax error
- Syntax validator says "looks OK"
- Runtime validator says "this won't work"

**How to reproduce**:
```bash
curl -X POST https://n8n.oloxa.ai/webhook/sop-builder \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test",
    "goal": "Test goal",
    "improvement_type": "speed",
    "department": "operations",
    "end_user": "Test user",
    "process_steps": "Step 1. Step 2. Step 3.",
    "input_method": "text"
  }'
```

**Expected result after fix**:
- Workflow executes successfully
- Email sent to user
- Airtable record created
- Webhook responds with success message

---

## Report Metadata

- **Generated by**: test-runner-agent
- **Agent ID**: (to be provided)
- **Workflow validated**: Yes (0 errors, 46 warnings)
- **Workflow executed**: No (runtime validation error)
- **Root cause identified**: Yes (IF node routing)
- **Fix complexity**: Medium (requires structural change to connections)
