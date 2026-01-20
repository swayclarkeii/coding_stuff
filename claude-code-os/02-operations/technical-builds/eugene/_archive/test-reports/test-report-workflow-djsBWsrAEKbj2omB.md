# n8n Test Report - Chunk 1: Email to Staging (Document Organizer V4)

**Workflow ID:** djsBWsrAEKbj2omB
**Execution ID:** 171
**Test Date:** 2026-01-04
**Status:** FAILED

---

## Summary

- Total tests: 1 (trigger execution with 3 PDF attachments)
- FAILED: splitInBatches loop not working in trigger mode
- Passed: ✅ NONE
- Failed: ❌ 1

---

## Root Cause Analysis

### The Problem

**splitInBatches node "Sequential Processing" outputs 0 items on Output 0 (empty branch), but the workflow execution stops after processing only the first item.**

### What Should Happen

1. Filter Supported Files outputs **3 items** (3 PDF attachments)
2. Sequential Processing should:
   - **First iteration:** Output 1 item on Output 1 (loop branch) → process → loop back via Normalize Output
   - **Second iteration:** Output 1 item on Output 1 → process → loop back
   - **Third iteration:** Output 1 item on Output 1 → process → loop back
   - **After all iterations:** Output 3 items on Output 0 (done/empty branch)

### What Actually Happened (Execution #171)

1. Filter Supported Files outputs **3 items** ✅
2. Sequential Processing:
   - **First iteration:** Outputs 1 item on Output 1 (loop branch) ✅
   - Item goes to IF ZIP File → Merge File Streams
   - **CRASH at Merge File Streams** with error:
     ```
     Cannot assign to read only property 'name' of object
     'Error: Node 'Normalize ZIP Contents' hasn't been executed'
     ```
3. **Loop never completes** - no items ever reach Output 0
4. **Workflow stops** - items 2 and 3 never processed

---

## Detailed Execution Flow (Execution #171)

### Nodes Before splitInBatches (Working Correctly)

| Node | Items In | Items Out | Status | Notes |
|------|----------|-----------|--------|-------|
| Gmail Trigger | 0 | 1 | ✅ Success | Email with 3 PDF attachments |
| Normalize Email Data | 1 | 1 | ✅ Success | Correctly counted 3 attachments |
| IF Has Attachments | 1 | 1 | ✅ Success | hasAttachments: true |
| Extract Attachments | 1 | 3 | ✅ Success | Split into 3 PDF items |
| Filter Supported Files | 3 | 3 | ✅ Success | All 3 PDFs supported |

### splitInBatches Node (BROKEN)

| Node | Items In | Items Out (Output 0) | Items Out (Output 1) | Status | Issue |
|------|----------|----------------------|----------------------|--------|-------|
| Sequential Processing | 3 | **0** ❌ | 1 (first item only) | ⚠️ Partial | Loop never completes due to downstream crash |

**Expected behavior:**
- Output 0 (empty/done): Should output **3 items** after all iterations complete
- Output 1 (loop): Should output **1 item per iteration** (3 iterations total)

**Actual behavior:**
- Output 0 (empty/done): **0 items** (never reached)
- Output 1 (loop): **1 item** (first iteration only, then crashed)

### Nodes Inside Loop (CRASH)

| Node | Items In | Items Out | Status | Notes |
|------|----------|-----------|--------|-------|
| IF ZIP File | 1 | 1 (not ZIP, goes to Output 1) | ✅ Success | isZip: false, routes to direct PDF path |
| Merge File Streams | 1 | 0 | ❌ **CRASHED** | Error: References unexecuted node "Normalize ZIP Contents" |

**Error Message:**
```
Cannot assign to read only property 'name' of object 'Error: Node 'Normalize ZIP Contents' hasn't been executed'
```

**The Bug:**
The "Merge File Streams" Code node contains this logic:
```javascript
// V4: Merge ZIP and direct PDF items
const directPdf = $('IF ZIP File').first();
const zipContents = $('Normalize ZIP Contents').all();  // ❌ THIS LINE CRASHES

// If this is a direct PDF (not ZIP), pass through
if (!directPdf.json.isZip) {
  return [directPdf];
}

// Otherwise, return extracted PDFs from ZIP
return zipContents;
```

**Why it crashes:**
- When the file is a direct PDF (not ZIP), the "Normalize ZIP Contents" node never executes
- n8n tries to evaluate `$('Normalize ZIP Contents').all()` **before** the if-statement
- This throws an error because the node hasn't been executed in this branch
- **n8n evaluates ALL expressions before code execution**, even inside if-statements

---

## Comparison: Manual vs Trigger Execution

### Manual "Execute Step" (Works)

- User clicks "Execute step" on Sequential Processing
- n8n processes nodes one-by-one synchronously
- Expression errors might be handled differently in manual mode
- Loop completes successfully

### Trigger Execution (Fails)

- Gmail Trigger fires automatically
- n8n processes workflow asynchronously
- Strict expression evaluation crashes on unexecuted node references
- Loop stops on first iteration

---

## Test Case Details

### Test 1: Process 3 PDF Attachments

**Input:**
- Email with 3 PDF attachments:
  1. OCP-Anfrage-AM10.pdf (1.95 MB)
  2. ADM10_Expose.pdf (1.59 MB)
  3. GBA_Schoneberg_Lichterfelde_15787.pdf (1.09 MB)

**Expected:**
- Sequential Processing outputs 3 items on Output 0 (after all iterations)
- All 3 PDFs uploaded to Google Drive Staging folder
- Workflow completes successfully

**Actual:**
- Sequential Processing outputs **0 items** on Output 0
- **0 PDFs uploaded** (workflow crashed before upload)
- Workflow status: **error**
- Failed at node: **Merge File Streams**

**Status:** ❌ **FAIL**

---

## Recommended Fix

### Option 1: Conditional Node Reference (Preferred)

Replace the "Merge File Streams" Code node with this safe logic:

```javascript
// V4: Merge ZIP and direct PDF items
const directPdf = $('IF ZIP File').first();

// Check if this is a direct PDF (not ZIP)
if (!directPdf.json.isZip) {
  return [directPdf];  // ✅ Exit early, never reference Normalize ZIP Contents
}

// Only reference zipContents if we know the ZIP path was executed
const zipContents = $('Normalize ZIP Contents').all();
return zipContents;
```

**Why this works:**
- Early return prevents evaluating `$('Normalize ZIP Contents').all()` when the node hasn't run
- n8n only evaluates expressions in code paths that actually execute

### Option 2: Try-Catch Guard (Alternative)

```javascript
// V4: Merge ZIP and direct PDF items
const directPdf = $('IF ZIP File').first();

// If this is a direct PDF (not ZIP), pass through
if (!directPdf.json.isZip) {
  return [directPdf];
}

// Otherwise, try to get extracted PDFs from ZIP
try {
  const zipContents = $('Normalize ZIP Contents').all();
  return zipContents;
} catch (error) {
  // Fallback if node hasn't executed
  return [directPdf];
}
```

### Option 3: Use IF Node Instead of Code (Most Robust)

Replace "Merge File Streams" Code node with an IF node:
- Condition: `{{ $json.extractedFromZip }}` equals `true`
- Output 0 (false): Connect to "Upload to Staging" (direct PDFs)
- Output 1 (true): Pull from "Normalize ZIP Contents" → "Upload to Staging"

This avoids Code node expression evaluation issues entirely.

---

## Additional Observations

### Binary Data Handling (Working Correctly)

The workflow correctly:
- Reads binary attachments from Gmail Trigger
- Passes binary data through Normalize Email Data
- Splits binary attachments in Extract Attachments
- Preserves binary data through splitInBatches loop
- Binary format: `filesystem-v2` with proper file metadata

### splitInBatches Configuration

- Node type: `n8n-nodes-base.splitInBatches` v3
- Batch size: Default (1 item per batch)
- Options: Default
- Connections:
  - Input: Filter Supported Files (3 items)
  - Output 0 (empty/done): None (should go to next workflow chunk)
  - Output 1 (loop): IF ZIP File → ... → Normalize Output → loops back to Sequential Processing

**The splitInBatches node configuration is CORRECT.** The issue is downstream in the Code node.

---

## Files Generated

- Test report: `/Users/swayclarke/coding_stuff/test-report-workflow-djsBWsrAEKbj2omB.md`

---

## Next Steps

1. Apply **Option 1 fix** to "Merge File Streams" Code node
2. Re-run execution with same test email (or similar 3-PDF email)
3. Verify all 3 PDFs upload to Staging folder
4. Verify Sequential Processing outputs 3 items on Output 0 after completion
5. Consider adding error handling/logging to track loop iterations
