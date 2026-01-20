# Chunk 2 Workflow Test Report - File Lifecycle Bug Fix

**Workflow:** Chunk 2: Text Extraction (Document Organizer V4)
**Workflow ID:** g9J5kjVtqaF9GLyc
**Test Date:** 2026-01-08
**Tester:** test-runner-agent

---

## Test Summary

- **Total Tests:** 1
- **Passed:** 0
- **Failed:** 1
- **Critical Bugs Found:** 1 (NEW)

---

## Test Case 1: Pre-Chunk 0 Extracted Text Routing

### Test Objective
Validate that Chunk 2 properly handles already-extracted text from Pre-Chunk 0 without attempting to download the file again (file lifecycle bug fix).

### Test Input
```json
{
  "fileId": "1SaAnbMGcyZgLkmYC4KZJyI9gN26N_l7L",
  "name": "ADM10_Exposé.pdf",
  "mimeType": "application/pdf",
  "size": 2044723,
  "client_normalized": "adolf_martens_strasse",
  "staging_folder_id": "18i4O8VhBUczeXXW13pucX3DxpPtIMIkf",
  "extractedText": "This is a sample extracted text from Pre-Chunk 0 that is longer than 100 characters to simulate real PDF content that has already been extracted and should not be downloaded again by Chunk 2.",
  "extractionMethod": "pre_chunk_0_digital"
}
```

### Expected Behavior
1. Normalize Input detects `extractedText.length > 100`
2. Sets `skipDownload = true`
3. Routes through "If Check Skip Download" TRUE branch
4. Goes directly to "Detect Scan vs Digital" without downloading
5. Continues to classification
6. Output includes `chunk2_path: 'direct_from_pre_chunk'`

### Test Status: **FAILED**

### Execution Details
- **Execution ID:** 602 (manual test execution found in logs)
- **Execution Status:** error
- **Started:** 2026-01-08T12:37:56.582Z
- **Stopped:** 2026-01-08T12:37:56.636Z
- **Duration:** 54ms
- **Failed at Node:** If Check Skip Download
- **Error Type:** NodeOperationError

---

## Critical Bug Found

### Bug: Type Validation Error in "If Check Skip Download" Node

**Error Message:**
```
Wrong type: 'false' is a boolean but was expecting a string [condition 0, item 0]
```

**Root Cause:**
The "If Check Skip Download" node is configured to:
- Compare `skipDownload` (boolean) against string `"true"`
- Use strict type validation (`typeValidation: "strict"`)
- Disable loose type conversion (`looseTypeValidation: false`)

**Current Node Configuration:**
```javascript
{
  "conditions": {
    "options": {
      "caseSensitive": true,
      "leftValue": "",
      "typeValidation": "strict",
      "version": 3
    },
    "conditions": [
      {
        "id": "1d9a07d1-bb21-4bb4-b2f7-929dbdb20399",
        "leftValue": "={{ $json.skipDownload }}",
        "rightValue": "true",  // STRING, but skipDownload is BOOLEAN
        "operator": {
          "type": "string",
          "operation": "equals"
        }
      }
    ]
  }
}
```

**Data from Normalize Input:**
```json
{
  "extractedText": null,
  "skipDownload": false,  // BOOLEAN
  "mimeType": "application/pdf",
  "size": 0,
  "clientNormalized": "unknown",
  "textLength": 0,
  "extractionMethod": null,
  "processedAt": "2026-01-08T12:37:56.609Z",
  "needsReExtraction": true,
  "isScanned": null,
  "ocrUsed": false
}
```

**Impact:**
- Workflow ALWAYS fails at the If node, regardless of whether skipDownload is true or false
- File lifecycle bug fix cannot function because the routing logic is broken
- Both paths (skip download and normal download) are unreachable

---

## Recommended Fix

**Option 1: Change Operator to Boolean (RECOMMENDED)**
- Change operator from `type: "string"` to `type: "boolean"`
- Keep rightValue as boolean `true` (not string "true")

**Option 2: Enable Loose Type Validation**
- Set `looseTypeValidation: true` in node options
- This allows n8n to convert boolean to string automatically

**Option 3: Convert in Expression**
- Change leftValue to: `={{ $json.skipDownload.toString() }}`
- Keep rightValue as string `"true"`

---

## Execution Path Analysis

### Nodes Executed:
1. Execute Workflow Trigger (success)
2. Normalize Input (success) - output: skipDownload = false (boolean)
3. If Check Skip Download (ERROR) - type mismatch

### Nodes NOT Reached:
- Download PDF1
- Extract PDF Text1
- Detect Scan vs Digital1
- IF Needs OCR1
- AWS Textract OCR1
- Process OCR Result1
- Normalize Output1

---

## Test Result: CANNOT VALIDATE

The file lifecycle bug fix **cannot be tested** until the type validation error in "If Check Skip Download" is resolved. The workflow fails before reaching the logic that was intended to be tested.

---

## Next Steps

1. **IMMEDIATE:** Fix the type validation error in "If Check Skip Download" node
2. **AFTER FIX:** Re-run this test with the same input data
3. **VALIDATE:** Confirm skipDownload=true path works correctly
4. **VALIDATE:** Confirm skipDownload=false path still works for normal files
5. **INTEGRATION TEST:** Test full pipeline from Pre-Chunk 0 → Chunk 2

---

## Notes

- **Testing Method:** Could not use `n8n_test_workflow` API because Chunk 2 uses Execute Workflow Trigger (only callable from other workflows)
- **Data Source:** Found recent manual test execution (ID: 602) in execution logs
- **Input in Test 602:** Manual test was run without the `extractedText` field, so skipDownload=false (which also triggered the type error)
- **Simulated Test:** The provided test input would have triggered skipDownload=true, but would fail with the same type error

---

## Test Execution Metadata

- **Test Runner:** test-runner-agent
- **Execution Method:** Analysis of existing execution logs (API testing not possible for Execute Workflow Trigger)
- **Report Generated:** 2026-01-08T12:38:00Z
- **Report Location:** `/Users/swayclarke/coding_stuff/test-reports/chunk2-lifecycle-bug-test-report.md`
