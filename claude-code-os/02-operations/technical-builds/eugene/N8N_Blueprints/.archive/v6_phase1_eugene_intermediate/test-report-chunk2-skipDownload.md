# n8n Test Report - Chunk 2: skipDownload Logic Fix

## Summary
- Total tests: 1
- Status: **FAILED** (Fix did NOT work)
- Execution ID: 734
- Test Date: 2026-01-09T10:24:39.911Z

---

## Test Case: Verify skipDownload: true Takes TRUE Branch

### Input Data
```json
{
  "skipDownload": true,
  "extractedText": "This is test extracted text content from Pre-Chunk 0...",
  "textLength": 287,
  "extractionMethod": "digital_pre_chunk",
  "fileId": "1test123_mock_file_id",
  "fileName": "test-skipDownload-document.pdf",
  "mimeType": "application/pdf",
  "extension": "pdf",
  "client_normalized": "test_client",
  "stagingPath": "test_client/_Staging/test.pdf"
}
```

### Expected Outcome
- "If Check Skip Download" node outputs:
  - TRUE branch: 1 item (skip download path)
  - FALSE branch: 0 items
- "Download PDF1" node: 0 items executed (skipped)
- "Detect Scan vs Digital1" receives data with `chunk2_path: 'direct_from_pre_chunk'`

### Actual Outcome - FAILED

#### Status: FAILED

**Node Execution Results:**

1. **Test Webhook (Temporary)** - SUCCESS
   - Received input correctly
   - body.skipDownload = true (correct)
   - body.extractedText = "This is test..." (correct)

2. **Normalize Input1** - SUCCESS (but incorrect logic)
   - **PROBLEM**: Output shows:
     ```json
     {
       "skipDownload": false,  // WRONG! Should be true
       "extractedText": null,   // WRONG! Should be test text
       "textLength": 0,         // WRONG! Should be 287
       "extractionMethod": null // WRONG! Should be "digital_pre_chunk"
     }
     ```
   - **ROOT CAUSE**: The Normalize Input1 code is NOT reading from the webhook body correctly
   - Code uses `$input.first().json` but the actual data is in `$input.first().json.body`

3. **If Check Skip Download** - SUCCESS (but took wrong branch)
   - Evaluated: `skipDownload === true`
   - Received: `skipDownload = false`
   - Result: TRUE branch = 0 items, FALSE branch = 1 item
   - **This is correct behavior given the wrong input from Normalize Input1**

4. **Download PDF1** - ERROR (expected, took FALSE branch)
   - Attempted to download fileId: (empty/null)
   - Failed with: "Request failed with status code 404"
   - **This proves the FALSE branch was taken**

### Comparison with Execution #733

Both executions show the **SAME BEHAVIOR**:
- Execution #733: IF node TRUE=0, FALSE=1
- Execution #734: IF node TRUE=0, FALSE=1

**The solution-builder-agent fix (a7efb1e) did NOT address the root cause.**

---

## Root Cause Analysis

The Boolean() conversion fix was correct, but **the actual problem is earlier in the chain**.

### The Real Bug

**Normalize Input1** is reading the wrong path:

```javascript
const item = $input.first().json;  // This gets the webhook wrapper
```

But the actual test data is in:
```javascript
const item = $input.first().json.body;  // This is where the data is
```

### Evidence from Execution Data

**Webhook output:**
```json
{
  "json": {
    "headers": {...},
    "params": {},
    "query": {},
    "body": {
      "skipDownload": true,
      "extractedText": "...",
      // ... all test data here
    }
  }
}
```

**Normalize Input1 receives this but reads the wrong level:**
- Reads: `$input.first().json` (gets headers, params, query, body wrapper)
- Should read: `$input.first().json.body` (gets actual data)

---

## Fix Required

**Update Normalize Input1 code:**

Change line:
```javascript
const item = $input.first().json;
```

To:
```javascript
// Handle both webhook body (testing) and direct calls (production)
const item = $input.first().json.body || $input.first().json;
```

This ensures:
- Webhook triggers (testing) read from `body`
- Direct workflow calls (production) read from root `json`

---

## Next Steps

1. Solution-builder-agent should update Normalize Input1 with the correct data path
2. Re-run this test to verify the fix
3. Test with both:
   - Webhook trigger (via test_workflow)
   - Direct Execute Workflow call (production path)

---

## Execution Details

**Execution ID:** 734
**Workflow ID:** qKyqsL64ReMiKpJ4
**Duration:** 462ms
**Final Status:** error (expected - mock fileId)

**Node Execution Path:**
1. Test Webhook (Temporary) - 1ms - SUCCESS
2. Normalize Input1 - 25ms - SUCCESS (but wrong logic)
3. If Check Skip Download - 1ms - SUCCESS (took FALSE branch)
4. Download PDF1 - 357ms - ERROR (404 on mock fileId)

**Failed At:** Download PDF1
**Error:** "The resource you are requesting could not be found"

---

## Test Verdict

**Result:** FAILED

**Reason:** The Boolean() conversion fix was correct, but the root cause is that Normalize Input1 is reading from the wrong data path (`json` instead of `json.body` for webhook triggers).

**Impact:** The skipDownload optimization does not work. All documents will attempt download even when Pre-Chunk 0 provides extracted text.

**Priority:** HIGH - This breaks the core optimization strategy for the V4 pipeline.
