# Expense System Test Report
**Date:** 2026-01-28
**Tester:** test-runner-agent

## Summary

### STATUS: BLOCKED - New Error Found

**Test Round 2 Results:**
- Download PDF fix: ✅ WORKING (files downloading successfully)
- Extract File Metadata: ❌ FAILING (line 7: cannot read 'match' on undefined)
- **All 15 executions failed at Extract File Metadata node**

### BLOCKER ISSUE

**W1 "Extract File Metadata" Node - Data Structure Mismatch**
- Node expects Google Drive trigger data structure
- Webhook provides different data structure
- Error: `Cannot read properties of undefined (reading 'match') [line 7]`
- **Fix required:** Update Extract File Metadata to handle webhook binary data structure

---

## Test Results by Phase

### Phase 1: W3 Baseline Test
- **Workflow:** CJtdqMreZ17esJAW (W3 - Transaction-Receipt-Invoice Matching)
- **Status:** ✅ FIXED (rate limit resolved by reducing from 5 to 3 Google Sheets reads)
- **Execution ID:** 6136 (first failed attempt)
- **Original Error:** Quota exceeded (60 read requests/minute limit)
- **Fix Applied:** Reduced Google Sheets read operations

### Phase 2: Bank Statement Processing (W1)
**Workflow:** MPjDdVMI88158iFW (W1 - PDF Intake & Parsing)
**Target:** Process 15 bank statement PDFs

**Test Round 1 (00:13-00:14 UTC):**
- ❌ All 15 failed at Download PDF (404 errors)
- Issue: Webhook data at `$json.body.id`, node expected `$json.id`
- Executions: 6137-6151

**Test Round 2 (00:20-00:21 UTC):**
- ✅ Download PDF now working (fix applied)
- ❌ All 15 failed at Extract File Metadata (line 7 error)
- Issue: Code expects Google Drive trigger fields, webhook provides binary data
- Executions: 6153-6167

**Current Blocker:**
```
Error: Cannot read properties of undefined (reading 'match') [line 7]
Node: Extract File Metadata
```

The node is trying to access a field that doesn't exist in the webhook data structure.

| # | File Name | File ID | Round 1 | Round 2 | Status |
|---|-----------|---------|---------|---------|--------|
| SKIP | ING_OCT2025_Statement.pdf | 1ot_IUE13xg07gHs_GxZnJNtCPDtmx5Ej | - | - | Already processed (69 txns) |
| 1 | Barclay - Sep 2025.pdf | 1ugUGr6m4uDPgHPLjE7VpmilTGglDU5B6 | 6137 (404) | 6153 (line 7) | FAILED |
| 2 | Barclay_DEC2025_Statement.pdf | 1i_6RzSiMxFS9YiZTzaSirKbq7V6zJdo7 | 6138 (404) | 6154 (line 7) | FAILED |
| 3 | Barclay_NOV2025_Statement.pdf | 1GxwPLi63PKv4lEHuMtxXxk0DHHUBsRwf | 6139 (404) | 6155 (line 7) | FAILED |
| 4 | Barclay_OCT2025_Statement.pdf | 1w841SKNCteXYA0sFpINQQT9ZRGcYVIWh | 6140 (404) | 6156 (line 7) | FAILED |
| 5 | Deutsche bank - Sep 2025.pdf | 1nX8IMz01SKOKa3APk2N9lzQYIFAD5Fux | 6141 (404) | 6157 (line 7) | FAILED |
| 6 | DeutscheBank_DEC2025_Statement.pdf | 1iPsDruy5Uw0urwkVtWNkqLSCJ48gq3ze | 6142 (404) | 6158 (line 7) | FAILED |
| 7 | DeutscheBank_NOV2025_Statement.pdf | 1z7veuzrnWNIB0Fxxlzb2VhPhUldElYmH | 6143 (404) | 6159 (line 7) | FAILED |
| 8 | DeutscheBank_OCT2025_Statement.pdf | 1a6at9z3HGIw4fLXyW2TtAE4ZA79Fuehx | 6144 (404) | 6160 (line 7) | FAILED |
| 9 | ING - Sep 2025.pdf | 1KezxQRuVz5QsmHYVJzJ-rHF6JFyU-REz | 6145 (404) | 6161 (line 7) | FAILED |
| 10 | ING_DEC2025_Statement.pdf | 1CHaP2JXk_YpZnwjr3r4D5OJ_xF7s_COb | 6146 (404) | 6162 (line 7) | FAILED |
| 11 | ING_NOV2025_Statement.pdf | 12ea0DNglkKCXAM0eKpNm-qVLehrrTxuu | 6147 (404) | 6163 (line 7) | FAILED |
| 12 | Miles&More_Dec2025_Statement.pdf | 14_xZo5eIebcaxBi1Gn7wnhoy_ZUSbI8S | 6148 (404) | 6164 (line 7) | FAILED |
| 13 | Miles&More_Nov2025_Statement.pdf | 1-C_pjBUz9LXTx6N9M7sBJ2sDKkOCPfde | 6149 (404) | 6165 (line 7) | FAILED |
| 14 | Miles&More_Oct2025_Statement.pdf | 1m6v9ldfJICeEHfzcYMemUIUuw5-OnXRh | 6150 (404) | 6166 (line 7) | FAILED |
| 15 | MilesMore - Sep 2025.pdf | 1dX3uD7HGWseD50W-D9GaCULGzwqYpm_Y | 6151 (404) | 6167 (line 7) | FAILED |

### Phase 3: W3 Full Data Test
- **Status:** BLOCKED - Cannot proceed until Phase 2 completes
- **Wait for:** All 15 bank statements processed successfully
- **Expected:** 500+ transactions to match

---

## Detailed Error Analysis

### Round 2: Extract File Metadata Error (Execution 6167)

**Success so far:**
- ✅ Webhook trigger received file ID correctly
- ✅ Download PDF node successfully downloaded the file (162 kB PDF)
- ✅ Binary data available with filename: "MilesMore - Sep 2025.pdf"

**Failure point:**
- ❌ Extract File Metadata node (Code node, line 7)
- Error: `Cannot read properties of undefined (reading 'match')`

**Data available at failure:**
```json
{
  "json": {
    "headers": {...},
    "body": {"id": "1dX3uD7HGWseD50W-D9GaCULGzwqYpm_Y"},
    "webhookUrl": "https://n8n.oloxa.ai/webhook/process-bank-statement"
  },
  "binary": {
    "data": {
      "fileName": "MilesMore - Sep 2025.pdf",
      "mimeType": "application/pdf",
      "fileSize": "162 kB"
    }
  }
}
```

**Root Cause:**
The Extract File Metadata code node expects fields from Google Drive trigger (like `$json.name` or `$json.path`), but when triggered via webhook:
- File metadata is in `$binary.data.fileName`
- There is no `$json.name` or similar trigger fields

**Required Fix:**
Update Extract File Metadata code to detect trigger source and extract metadata from the correct location:
- **Webhook trigger:** Use `$binary.data.fileName`
- **Google Drive trigger:** Use `$json.name` or `$json.path`

The code should check which fields exist and adapt accordingly.

---

## Execution Timeline

**Round 1: First Attempt**
- **00:11:10** - Triggered W3 baseline test (execution 6136) - Rate limit error
- **00:13:31-00:14:39** - Triggered all 15 bank statements via W1 webhook
- **00:13:32-00:14:39** - All 15 executions failed at Download PDF (404 errors)
- **Root cause:** Download PDF expected `$json.id`, webhook provided `$json.body.id`

**Fixes Applied:**
- ✅ W1 Download PDF node updated to handle `$json.body?.id || $json.id`
- ✅ W3 Google Sheets operations reduced from 5 to 3

**Round 2: After Fix**
- **00:20:46-00:21:33** - Re-triggered all 15 bank statements via W1 webhook
- **00:20:47-00:21:35** - All 15 executions failed at Extract File Metadata (line 7 error)
- **Root cause:** Extract File Metadata expects Google Drive trigger fields, webhook provides binary data

---

## Recommendations

### Immediate Action Required

**Fix W1 Extract File Metadata Node:**

The code needs to handle both trigger types. Suggested approach:

```javascript
// Detect trigger source and extract filename accordingly
const fileName = $binary.data?.fileName || $json.name || $json.path?.split('/').pop();

if (!fileName) {
  throw new Error('Could not extract filename from trigger data');
}

// Continue with existing logic using fileName variable
const fileNameMatch = fileName.match(/...pattern.../);
// ... rest of code
```

This will:
1. Try binary data first (webhook trigger)
2. Fall back to JSON fields (Google Drive trigger)
3. Throw clear error if neither exists

### Testing Steps After Fix

1. **Verify fix in n8n UI** - Check Extract File Metadata code
2. **Test with 1 file first** - Use Barclay - Sep 2025.pdf (1ugUGr6m4uDPgHPLjE7VpmilTGglDU5B6)
3. **If successful, process remaining 14 files**
4. **Monitor for Anthropic Vision API errors** (could still fail at parsing step)
5. **Verify transaction extraction** - Check Google Sheets for new rows
6. **Test W3 matching** with full dataset

---

## Next Steps

**BLOCKED ON:** W1 Extract File Metadata node fix (solution-builder-agent required)

**Cannot proceed with testing until:**
1. Extract File Metadata node updated to handle webhook binary data structure
2. Workflow validated and re-deployed

**After fix:**
1. Re-trigger all 15 bank statements (3rd attempt)
2. Monitor for success/failure at each node
3. Track transaction counts in Google Sheets
4. Test W3 with full dataset (500+ transactions expected)

---

## Progress Summary

**Fixes Completed:**
- ✅ W3 rate limit (reduced Google Sheets reads)
- ✅ W1 Download PDF (now handles webhook data)

**Fixes Needed:**
- ❌ W1 Extract File Metadata (needs webhook data handling)

**Files Processed:**
- 0/15 new files (all blocked at Extract File Metadata)
- 1/16 total (ING_OCT2025 already processed before testing)
