# n8n Integration Test Report: Pre-Chunk 0 → Chunk 1

**Test Date**: 2026-01-04
**Test Objective**: Verify complete flow from Pre-Chunk 0 client identification through Chunk 1 PDF upload to dynamic staging folder

---

## Executive Summary

**Integration Status**: FAILED

**Critical Finding**: The integration between Pre-Chunk 0 and Chunk 1 is **broken**. The workflow stops after "Execute Chunk 0 - Create Folders" completes and never reaches "Execute Chunk 1".

**Root Cause**: The "Lookup Staging Folder" node (n8n-nodes-base.googleSheets) is **missing required configuration** (documentId, sheetName, operation), causing workflow execution to halt.

---

## Test Scenarios Executed

### Test 1: New Client Flow (Villa Martens)

**Execution Details**:
- Pre-Chunk 0 Execution ID: `180`
- Status: SUCCESS (partial)
- Workflow ID: `70n97A6OmYCsHMmV`
- Executed: 2026-01-04 00:26:49 - 00:28:51 (121 seconds)
- Email ID: `19b8665d03d49ed9`

**Flow Analysis**:

1. Gmail Trigger - SUCCESS
   - Email received with 3 PDF attachments
   - Files: OCP-Anfrage-AM10.pdf, ADM10_Expose.pdf, GBA_Schoneberg_Lichterfelde_15787.pdf

2. Client Identification - SUCCESS
   - AI extracted client name: "Villa Martens"
   - Normalized: "villa_martens"
   - Registry lookup: NEW client (not found in Client_Registry)

3. Decision Gate - SUCCESS
   - Route: Output 1 ("create_folders")
   - Reason: `folders_exist: false`

4. Execute Chunk 0 - Create Folders - SUCCESS
   - Execution time: 57.5 seconds
   - Created root folder: `1BXXUPJ539jXW4etiFSM3iyQph-edEn_I`
   - Created staging folder (Intake): `1ahpPa6pOLR1xK3tU4q0YOTQJOczr7ZsS`
   - Registered client in both sheets (Client_Registry + AMA_Folder_IDs)
   - Status: ACTIVE

5. **Lookup Staging Folder - FAILED (node did not execute)**
   - Node was NOT in execution results
   - Workflow stopped after Chunk 0 completion
   - No data passed to downstream nodes

6. **Execute Chunk 1 - NOT REACHED**
   - Node never executed
   - No sub-workflow call made
   - Integration broken

---

## Chunk 1 Execution Analysis

**Chunk 1 Execution ID**: `182`
**Status**: SUCCESS (via Gmail Trigger, NOT via Execute Workflow)

**Critical Observation**: Chunk 1 execution #182 shows:
- Triggered by: **Gmail Trigger** (NOT Execute Workflow Trigger)
- Timing: Started at 00:26:59 (10 seconds AFTER Pre-Chunk 0)
- Same email ID: `19b8665d03d49ed9`

This proves:
- Chunk 1 has its own Gmail Trigger still active
- Both workflows triggered independently from the same email
- There was **no parent-child execution relationship**
- Chunk 1 uploaded to **default staging folder** (not dynamic folder from Pre-Chunk 0)

**Upload Destination (Chunk 1 #182)**:
- Folder ID: `0ADu2vODw7d18Uk9PVA` (from execution data)
- This is **NOT** the villa_martens staging folder (`1ahpPa6pOLR1xK3tU4q0YOTQJOczr7ZsS`)
- Files uploaded to wrong location (not client-specific)

---

## Root Cause Analysis

### Primary Issue: Incomplete "Lookup Staging Folder" Node

The "Lookup Staging Folder" node (Google Sheets) has **incomplete configuration**:

**Current Configuration**:
```json
{
  "name": "Lookup Staging Folder",
  "type": "n8n-nodes-base.googleSheets",
  "parameters": {
    "options": {
      "range": "A:Z"
    }
  },
  "credentials": {
    "googleApi": {
      "id": "VdNWQlkZQ0BxcEK2"
    }
  }
}
```

**Missing Required Fields**:
1. `operation` - Should be "Read Rows" or "getAll"
2. `documentId` - Google Sheet ID (likely `1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI`)
3. `sheetName` - Tab name (likely "AMA_Folder_IDs" based on Filter code)

**Expected Configuration** (based on similar nodes in workflow):
```json
{
  "operation": "getAll",  // or equivalent "Read" operation
  "authentication": "serviceAccount",
  "documentId": {
    "__rl": true,
    "value": "1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI",
    "mode": "id"
  },
  "sheetName": {
    "__rl": true,
    "value": "AMA_Folder_IDs",  // or gid number
    "mode": "list"
  },
  "options": {
    "range": "A:Z"
  }
}
```

### Secondary Issue: Chunk 1 Has Competing Gmail Trigger

Chunk 1 workflow (`djsBWsrAEKbj2omB`) has:
- Gmail Trigger: **ENABLED** (still active)
- Execute Workflow Trigger: **ENABLED** (should be primary)

This creates race condition:
- Both triggers fire independently
- Chunk 1 processes emails without Pre-Chunk 0 parameters
- Files upload to wrong folder

---

## Integration Test Results

### Test 1: New Client (villa_martens)

| Checkpoint | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Pre-Chunk 0 identifies client | villa_martens | villa_martens | PASS |
| Decision Gate routes to create_folders | Output 1 | Output 1 | PASS |
| Execute Chunk 0 creates folders | SUCCESS | SUCCESS | PASS |
| Chunk 0 returns staging_folder_id | 1ahpPa6pOLR1xK3tU4q0YOTQJOczr7ZsS | 1ahpPa6pOLR1xK3tU4q0YOTQJOczr7ZsS | PASS |
| Lookup Staging Folder queries sheet | SUCCESS | NOT EXECUTED | **FAIL** |
| Filter Staging Folder ID extracts ID | Extract staging_folder_id | NOT EXECUTED | **FAIL** |
| Execute Chunk 1 called with params | Call with 3 params | NOT EXECUTED | **FAIL** |
| Chunk 1 uploads to villa_martens folder | 1ahpPa6pOLR1xK3tU4q0YOTQJOczr7ZsS | 0ADu2vODw7d18Uk9PVA (wrong) | **FAIL** |

**Overall Result**: FAILED (4/8 checkpoints passed)

### Test 2: Existing Client

**Status**: NOT TESTED (no recent executions with existing client scenario)

**Note**: Based on workflow structure, this would also fail at "Lookup Staging Folder" node.

---

## Critical Failures Identified

### 1. Broken Workflow Chain
- **Node**: "Lookup Staging Folder"
- **Issue**: Missing operation, documentId, sheetName parameters
- **Impact**: Workflow stops, never reaches Chunk 1
- **Severity**: CRITICAL - Breaks entire integration

### 2. Parameter Passing Not Tested
- **Issue**: Execute Chunk 1 never executes, so parameter passing is untested
- **Expected Parameters**:
  - `client_normalized`: "villa_martens"
  - `staging_folder_id`: "1ahpPa6pOLR1xK3tU4q0YOTQJOczr7ZsS"
  - `email_id`: "19b8665d03d49ed9"
- **Actual**: N/A (node not reached)

### 3. Chunk 1 Dual Trigger Issue
- **Issue**: Gmail Trigger still active in Chunk 1, competing with Execute Workflow Trigger
- **Impact**: Chunk 1 runs independently, uploads to wrong folder
- **Severity**: HIGH - Defeats purpose of dynamic staging folders

### 4. No Error Handling
- **Issue**: Workflow fails silently when Lookup Staging Folder returns no data
- **Expected**: Error notification or fallback
- **Actual**: Execution shows SUCCESS but stops mid-flow

---

## Recommendations

### Immediate Fixes (Priority 1)

1. **Fix "Lookup Staging Folder" Node**:
   ```javascript
   // Required configuration
   {
     "operation": "getAll",
     "authentication": "serviceAccount",
     "documentId": {
       "__rl": true,
       "value": "1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI",
       "mode": "id"
     },
     "sheetName": {
       "__rl": true,
       "value": "AMA_Folder_IDs",  // or gid number
       "mode": "list"
     },
     "options": {
       "range": "A:Z"
     }
   }
   ```

2. **Disable Chunk 1 Gmail Trigger**:
   - Keep only Execute Workflow Trigger active
   - Prevents duplicate/competing execution
   - Ensures dynamic parameters are used

3. **Add Error Handling After Lookup Staging Folder**:
   - Add IF node to check if staging_folder_id exists
   - Route errors to notification/fallback queue
   - Prevent silent failures

### Testing Requirements (Priority 2)

After fixes are applied, retest:

1. **New Client Flow**:
   - Send test email with PDF
   - Verify Pre-Chunk 0 → Chunk 0 → Lookup → Chunk 1 chain
   - Confirm PDFs upload to new client's staging folder
   - Check execution shows parent-child relationship

2. **Existing Client Flow**:
   - Send test email for existing client (e.g., eugene)
   - Verify Decision Gate routes to output 2 ("folders_exist")
   - Skip Chunk 0, go directly to Lookup → Chunk 1
   - Confirm PDFs upload to existing client's staging folder

3. **Parameter Passing**:
   - Inspect Chunk 1 execution logs
   - Verify all 3 parameters received correctly
   - Check "Merge Parameters" node preserves binary data

### Workflow Improvements (Priority 3)

1. **Add "Merge Chunk 0 Result" Node**:
   - Combine Chunk 0 output with original client data
   - Preserve context through workflow chain

2. **Simplify Decision Gate Output 0**:
   - Remove extra connection to "Lookup Staging Folder"
   - Prevents unidentified clients from attempting folder lookup

3. **Add Execution Logging**:
   - Log each major checkpoint (client identified, folders created, Chunk 1 called)
   - Use Code node to append to Google Sheet for audit trail

---

## Files & Resources

### Workflows Tested
- **Pre-Chunk 0**: `70n97A6OmYCsHMmV` (V4 Pre-Chunk 0: Intake & Client Identification)
- **Chunk 1**: `djsBWsrAEKbj2omB` (Chunk 1: Email to Staging)
- **Chunk 0**: `zbxHkXOoD1qaz6OS` (Chunk 0: Folder Initialization V4)

### Executions Analyzed
- Pre-Chunk 0: #180, #177, #172, #167, #164
- Chunk 1: #182 (triggered independently via Gmail)

### Google Sheets
- Client Registry: `1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI` (tab: Client_Registry)
- AMA Folder IDs: Same sheet, tab: AMA_Folder_IDs

### Test Email
- Email ID: `19b8665d03d49ed9`
- Subject: "FW: Damn... really... I'm still looking for yet another investor? Oloxa.ai"
- Attachments: 3 PDFs (OCP-Anfrage-AM10.pdf, ADM10_Expose.pdf, GBA_Schoneberg_Lichterfelde_15787.pdf)
- Client Identified: Villa Martens

### Folders Created (Chunk 0 Output)
- Root Folder: `1BXXUPJ539jXW4etiFSM3iyQph-edEn_I`
- Staging Folder (correct target): `1ahpPa6pOLR1xK3tU4q0YOTQJOczr7ZsS`
- Actual Upload Folder (wrong): `0ADu2vODw7d18Uk9PVA`

---

## Conclusion

The Pre-Chunk 0 → Chunk 1 integration is **currently non-functional** due to incomplete configuration of the "Lookup Staging Folder" node. While individual components work (client identification, folder creation, PDF upload), the workflow chain breaks before reaching Chunk 1, defeating the purpose of dynamic staging folder routing.

**Next Steps**:
1. Fix "Lookup Staging Folder" node configuration (add operation, documentId, sheetName)
2. Disable Chunk 1 Gmail Trigger (keep only Execute Workflow Trigger)
3. Retest with both new and existing client scenarios
4. Validate parameter passing and dynamic folder upload
5. Add error handling for failed lookups

**Estimated Fix Time**: 15-30 minutes
**Retest Required**: Yes (critical fix)

---

**Report Generated**: 2026-01-04
**Tested By**: test-runner-agent
**Report Path**: `/Users/swayclarke/coding_stuff/eugene-lombok/tests/pre-chunk0-chunk1-integration-test-report.md`
