# Chunk 2 → Chunk 2.5 Compatibility Analysis

**Date:** 2026-01-09 11:41 AM CET
**Status:** ⚠️ CRITICAL FIELD NAME MISMATCH FOUND

---

## Executive Summary

**CRITICAL ISSUE:** Field name incompatibility detected between Chunk 2 output and Chunk 2.5 input.

- **Chunk 2 outputs:** `client_normalized` (snake_case with underscore)
- **Chunk 2.5 expects:** `clientNormalized` (camelCase, no underscore)

**Impact:** Chunk 2.5 will fail to find clients in Client_Tracker because it cannot read the client identifier.

**Fix Required:** Update Chunk 2's Normalize Output1 node to output `clientNormalized` instead of `client_normalized`.

---

## Data Contract Comparison

### Chunk 2.5 Expected Input (from Execute Workflow Trigger schema)

```javascript
{
  fileId: string,              // ✅ Chunk 2 provides
  fileName: string,            // ✅ Chunk 2 provides
  mimeType: string,            // ⚠️ Chunk 2 doesn't pass through (from Pre-Chunk 0)
  clientNormalized: string,    // ❌ CRITICAL: Chunk 2 outputs "client_normalized" (with underscore)
  stagingFolderId: string,     // ⚠️ Chunk 2 doesn't output (not critical)
  extractedText: string,       // ✅ Chunk 2 provides
  textLength: number,          // ✅ Chunk 2 provides
  isScanned: boolean,          // ⚠️ Chunk 2 detects but doesn't output (not critical)
  ocrUsed: boolean,            // ✅ Chunk 2 provides
  extractionMethod: string     // ✅ Chunk 2 provides
}
```

### Chunk 2 Actual Output (from Normalize Output1)

Based on SESSION_COMPLETE documentation and fix history:

```javascript
{
  fileId: "...",
  fileName: "...",
  client_name: "...",          // ⚠️ Might not be used by Chunk 2.5
  client_normalized: "...",    // ❌ WRONG: Should be "clientNormalized"
  extractedText: "[full text]",
  extractionMethod: "digital_pre_chunk" | "digital" | "ocr_textract",
  chunk2_path: "direct_from_pre_chunk" | "digital_extraction" | "ocr_extraction",
  ocrUsed: true | false,
  textLength: 4678
}
```

---

## Critical Issues

### Issue 1: Field Name Mismatch (CRITICAL)

**Problem:**
- Chunk 2 outputs: `client_normalized`
- Chunk 2.5 reads: `clientNormalized`

**Where Chunk 2.5 Uses It:**

1. **Build AI Classification Prompt (code-1):**
   - Doesn't use clientNormalized directly, only extractedText and fileName ✅

2. **Parse Classification Result (code-2):**
   - Passes through all inputData, including clientNormalized

3. **Find Client Row and Validate (code-3):**
   ```javascript
   const clientNormalized = mainData.clientNormalized || '';  // ⚠️ Will be empty!
   ```
   - **CRITICAL:** Uses clientNormalized to find client in Client_Tracker
   - **Result:** Will always fail with "Client not found" error

4. **Get Destination Folder ID (code-4):**
   ```javascript
   const clientNormalized = mainData.clientNormalized || '';  // ⚠️ Will be empty!
   ```
   - **CRITICAL:** Uses clientNormalized to find client in AMA_Folder_IDs
   - **Result:** Will always fail with "Client not found" error

**Impact Severity:** 🔴 **CRITICAL - Workflow will fail 100% of the time**

**Fix Required:** Update Chunk 2's Normalize Output1 node to use `clientNormalized` (camelCase) instead of `client_normalized` (snake_case).

---

### Issue 2: Missing mimeType (LOW PRIORITY)

**Problem:** Chunk 2 doesn't pass through mimeType from Pre-Chunk 0

**Impact:** Low - Chunk 2.5 doesn't use mimeType in any logic

**Fix Required:** Optional - Add mimeType to Chunk 2's Normalize Output1 for completeness

---

### Issue 3: Missing stagingFolderId (LOW PRIORITY)

**Problem:** Chunk 2 doesn't pass through stagingFolderId

**Impact:** Low - Chunk 2.5 doesn't use stagingFolderId in any logic

**Fix Required:** Optional - Add if needed for future features

---

### Issue 4: Missing isScanned (LOW PRIORITY)

**Problem:** Chunk 2 detects scan vs digital in "Detect Scan vs Digital1" node but doesn't output isScanned in Normalize Output1

**Impact:** Low - Chunk 2.5 doesn't use isScanned in any logic

**Fix Required:** Optional - Add for completeness and future debugging

---

## Required Fixes

### Priority 1: CRITICAL - Field Name Fix

**Node:** Chunk 2 (qKyqsL64ReMiKpJ4) → Normalize Output1

**Current Code (BROKEN):**
```javascript
return [{
  json: {
    // ... other fields
    client_normalized: json.client_normalized || json.clientNormalized || '',  // Wrong field name
    // ... other fields
  }
}];
```

**Fixed Code (REQUIRED):**
```javascript
return [{
  json: {
    // ... other fields
    clientNormalized: json.client_normalized || json.clientNormalized || '',  // camelCase for Chunk 2.5
    // ... other fields
  }
}];
```

**Why This Works:**
- Reads from both `client_normalized` (Pre-Chunk 0) and `clientNormalized` (if already camelCase)
- Outputs as `clientNormalized` (camelCase) to match Chunk 2.5 expectations
- Backward compatible with Pre-Chunk 0 output

---

### Priority 2: OPTIONAL - Add Missing Fields

**Node:** Chunk 2 (qKyqsL64ReMiKpJ4) → Normalize Output1

**Enhanced Output (OPTIONAL):**
```javascript
return [{
  json: {
    fileId: json.fileId || '',
    fileName: json.fileName || '',
    mimeType: json.mimeType || 'application/pdf',  // Add from input
    clientNormalized: json.client_normalized || json.clientNormalized || '',  // Fixed
    stagingFolderId: json.stagingFolderId || '',  // Add from input
    extractedText: extractedText,
    textLength: textLength,
    isScanned: json.isScanned || false,  // Add from detection logic
    ocrUsed: json.ocrUsed || false,
    extractionMethod: json.extractionMethod || 'unknown',
    chunk2_path: json.chunk2_path || 'unknown',
    processedAt: new Date().toISOString()
  }
}];
```

---

## Testing Plan

### After Fix 1 (Critical Field Name)

1. **Test with Pre-Chunk 0 → Chunk 2 → Chunk 2.5:**
   - Send test email with PDF
   - Verify Chunk 2 execution success
   - Verify Chunk 2.5 receives `clientNormalized` (camelCase)
   - Verify Chunk 2.5 finds client in Client_Tracker
   - Verify Chunk 2.5 classifies and moves document

2. **Validation Points:**
   - Chunk 2.5 execution #XXX: Check "Find Client Row and Validate" output
   - Should show: `clientNormalized: "villa_martens"` (not empty)
   - Should show: `chunk2_5_status: "success"` (not error_client_not_found)

---

## Downstream Impact Analysis

### Will This Break Pre-Chunk 0?

**NO** - Pre-Chunk 0 doesn't read Chunk 2's output, it only calls Chunk 2 and proceeds to Chunk 2.5.

### Will This Break Chunk 2 Internal Logic?

**NO** - Chunk 2 internal nodes don't use `client_normalized` after Normalize Input1. The Normalize Output1 node is the final step before calling Chunk 2.5.

### Will This Break Future Chunks?

**NO** - Future chunks should use camelCase field names consistently (following Chunk 2.5 pattern).

---

## Recommendation

**Proceed with Priority 1 fix immediately:**
- Use solution-builder-agent to update Normalize Output1 node
- Change `client_normalized` to `clientNormalized` in output
- Test with test-runner-agent
- Validate end-to-end when Gmail trigger fires

**Defer Priority 2 (optional fields):**
- Not blocking Chunk 2.5 functionality
- Can add later if needed

---

## Files Referenced

- Chunk 2 workflow: qKyqsL64ReMiKpJ4
- Chunk 2.5 workflow: okg8wTqLtPUwjQ18
- Previous session: SESSION_COMPLETE_2026-01-09.md
- Fix documentation: SKIPDOWNLOAD_FIX_2026-01-09.md

---

**Status:** Ready to apply fix autonomously per user instructions.

**Next Action:** Launch solution-builder-agent to fix Normalize Output1 field name.
