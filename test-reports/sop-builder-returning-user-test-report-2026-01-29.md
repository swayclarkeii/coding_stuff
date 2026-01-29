# SOP Builder Workflow - Returning User Test Report
**Date**: 2026-01-29
**Workflow ID**: ikVyMpDI0az6Zk4t
**Workflow Name**: SOP Builder Lead Magnet
**Execution ID**: 6696
**Test Status**: ❌ FAILED (Workflow Configuration Error)

---

## Test Summary

- **Total Tests**: 1
- **Passed**: 0
- **Failed**: 1

---

## Test Details

### Test 1: Returning User Flow - swayclarkeii@gmail.com
**Status**: ❌ FAILED
**Reason**: Workflow has configuration errors preventing execution

**Test Input**:
```json
{
  "name": "Sway Clarke",
  "email": "swayclarkeii@gmail.com",
  "goal": "Standardize our client onboarding process with clear timelines and ownership",
  "department": "Operations",
  "end_user": "New account managers",
  "process_steps": "1. Receive signed contract\n2. Create client profile in CRM\n3. Schedule kickoff call within 24 hours\n4. Assign account manager\n5. Send welcome package\n6. First check-in within 48 hours\n7. Weekly follow-ups for first month\n8. 30-day satisfaction survey",
  "current_problems": "Steps get missed, no timeline, inconsistent execution across team",
  "has_audio": false
}
```

**Expected Behavior**:
1. ✅ "Check Existing Lead" searches Airtable for swayclarkeii@gmail.com
2. ✅ "Check If Returning User" evaluates to TRUE (user exists)
3. ✅ Routes to "Prepare Update Data" (RETURNING path)
4. ✅ "Update Lead in Airtable" increments submission_count
5. ✅ Appends new score to score_history

**Actual Result**: Workflow failed to execute

**Error Details**:
- **Error Type**: WorkflowHasIssuesError
- **Message**: "The workflow has issues and cannot be executed for that reason. Please fix them first."
- **Failed Node**: Workflow validation before execution
- **Duration**: 17ms (failed before any nodes ran)

---

## Root Cause Analysis

### Critical Errors Found

#### Error 1: Check Existing Lead - Wrong Operation Type
**Node**: "Check Existing Lead"
**Current Configuration**:
- Operation: `get` (requires Record ID)
- Record ID: Empty
- filterByFormula: Present but ignored in `get` operation

**Problem**: The `get` operation requires a specific Record ID, but we're trying to search by email. This is the wrong operation.

**Fix Required**: Change operation to `search` or `list` with filterByFormula

**Correct Configuration**:
```json
{
  "operation": "search",
  "base": "appvd4nlsNhIWYdbI",
  "table": "tblEHjJlvorWTgptU",
  "filterByFormula": "={email} = 'swayclarkeii@gmail.com'",
  "options": {}
}
```

#### Error 2: Check Existing Lead - Invalid filterByFormula Syntax
**Current Value**: `{email} = '{{ $json["email"] }}'`
**Error**: Missing `=` prefix for expression evaluation

**Problem**: When mixing literal text and expressions, Airtable's filterByFormula requires an `=` prefix.

**Correct Syntax**: `={email} = '{{ $json.email }}'`

---

## Fixes Applied Previously

### Fix 1: Airtable Filter Formula (Partially Applied)
**Status**: ❌ INCOMPLETE
**What Was Fixed**: Removed leading `=` from filterByFormula value
**What Remains Broken**:
- Operation type is still `get` (should be `search`)
- Expression wrapper still needed: `={{ ... }}`
- Record ID field still empty (blocking execution)

### Fix 2: Check If Returning User (Applied Correctly)
**Status**: ✅ VERIFIED
**Fixed Expression**: `={{ $('Check Existing Lead').all().length > 0 }}`
**Current State**: Expression is correct and will work once "Check Existing Lead" is fixed

---

## Required Fixes

### Immediate Actions Required

1. **Fix "Check Existing Lead" node**:
   ```json
   {
     "operation": "search",  // Changed from "get"
     "base": {
       "__rl": true,
       "value": "appvd4nlsNhIWYdbI",
       "mode": "list"
     },
     "table": {
       "__rl": true,
       "value": "tblEHjJlvorWTgptU",
       "mode": "id"
     },
     "options": {
       "filterByFormula": "={{ '{email} = \"' + $json.email + '\"' }}"
     }
   }
   ```

2. **Remove Record ID requirement** (only needed for `get` operation)

3. **Verify Airtable has existing records** for swayclarkeii@gmail.com (prerequisite)

---

## Flow Validation (Once Fixed)

### Expected Execution Path for Returning User

```
Webhook Trigger
  ↓
Parse Form Data
  ↓
Check Audio File (FALSE path - no audio)
  ↓
Use Text Input
  ↓
Merge Audio and Text Paths
  ↓
LLM: Validate Completeness
  ↓
Extract Validation Response
  ↓
Calculate SOP Score
  ↓
LLM: Generate Improved SOP
  ↓
Extract Improved SOP
  ↓
Generate Lead ID
  ↓
Route Based on Score
  ↓
Generate Email (Success or Improvement)
  ↓
Send HTML Email
  ↓
Format for Airtable
  ↓
Check Existing Lead (SEARCH returns records)  ← CURRENTLY BROKEN HERE
  ↓
Check If Returning User (TRUE - records found)
  ↓
Prepare Update Data (RETURNING path)
  ↓
Merge Airtable Paths
  ↓
Route Create or Update (TRUE - is_returning)
  ↓
Update Lead in Airtable
  ↓
Respond to Webhook
```

---

## Additional Issues Identified

### Warning: Other Nodes May Not Run Correctly

1. **"Prepare Update Data" and "Prepare New Lead Data"**:
   - Both reference `$('Format for Airtable').first().json`
   - This will work as long as "Format for Airtable" runs before them ✅

2. **"Route Create or Update" node**:
   - Checks `$json.is_returning` property
   - This property must be added by "Prepare Update Data" or "Prepare New Lead Data"
   - **Currently**: Neither code node adds `is_returning` property
   - **Fix**: Add `is_returning: true` in "Prepare Update Data" and `is_returning: false` in "Prepare New Lead Data"

---

## Next Steps

1. **Fix "Check Existing Lead" node**:
   - Change operation to `search`
   - Remove Record ID requirement
   - Fix filterByFormula expression wrapper

2. **Add is_returning flag**:
   - Update "Prepare Update Data" to include `is_returning: true`
   - Update "Prepare New Lead Data" to include `is_returning: false`

3. **Re-test with same payload** after fixes applied

4. **Verify in Airtable**:
   - Check if swayclarkeii@gmail.com exists
   - Verify submission_count increments
   - Verify score_history appends

---

## Test Execution Details

**Execution Timeline**:
- Started: 2026-01-28T23:53:42.459Z
- Stopped: 2026-01-28T23:53:42.476Z
- Duration: 17ms
- Status: Error (validation failure)

**Nodes Executed**: 0 (failed before any nodes ran)

**Validation Summary**:
- Total Nodes: 32
- Enabled Nodes: 32
- Trigger Nodes: 2
- Valid Connections: 34
- Invalid Connections: 0
- **Error Count**: 2 (both in "Check Existing Lead")
- **Warning Count**: 47

---

## Conclusion

The returning user flow **cannot be tested** until the "Check Existing Lead" node is properly configured. The fixes applied in the previous session were incomplete:

1. ✅ **IF node expression fixed correctly**
2. ❌ **Airtable node operation type incorrect** (still `get` instead of `search`)
3. ❌ **Airtable filterByFormula syntax still invalid**
4. ❌ **Missing is_returning flag** in prepare nodes

**Priority**: Fix "Check Existing Lead" node configuration before re-testing.

---

**Report Generated**: 2026-01-29
**Agent**: test-runner-agent
**Agent ID**: [Will be displayed after completion]
