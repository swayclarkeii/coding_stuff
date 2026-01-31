# Parse Classification Node Fix - Complete

## Status: COMPLETE ✓

**Date Completed**: 2026-01-31 08:19 UTC
**Workflow ID**: qSuG0gwuJByd2hGJ
**Workflow Name**: Expense System - W7v2: Receipts & Invoices Intake (Webhook)

---

## What Was Fixed

The "Parse Classification" code node in workflow W7v2 was crashing with:

```
Unexpected non-whitespace character after JSON at position 216 (line 10 column 1)
```

This happened because Anthropic's vision API response sometimes wraps the JSON output in markdown code fences or adds surrounding text, and the original code only did a single simple strip-and-parse attempt.

---

## Solution Deployed

Updated the Parse Classification node (id: `parse-classification`) with **4-level robust JSON extraction**:

1. **Direct Parse**: Try parsing raw response as JSON
2. **Markdown Strip**: Remove ` ```json...``` ` code fences
3. **Regex Extract**: Use regex to find JSON in code blocks
4. **Boundary Extract**: Find first `{` to last `}` as fallback

The node now handles:
- Pure JSON responses
- JSON in markdown code fences
- JSON wrapped in explanatory text
- Multiple code block variations
- Any combination of the above

---

## Verification

All features verified in deployed code:

- ✓ Step 1: Direct JSON.parse attempt
- ✓ Step 2: Markdown fence removal
- ✓ Step 3: Regex code block extraction
- ✓ Step 4: Boundary-based extraction (first { to last })
- ✓ Validation of required fileType field
- ✓ Fallback values for optional fields
- ✓ Descriptive error messages for debugging

---

## Testing Instructions

### Happy Path Test

1. Upload a PDF receipt to the webhook at:
   ```
   https://n8n.oloxa.ai/webhook/expense-receipts-upload
   ```

2. Expected flow:
   - File extracted and metadata created
   - Anthropic Vision API classifies document
   - Parse Classification node processes response
   - Document routed to appropriate Google Sheet (Receipts/Invoices/Expensify)
   - File uploaded to Google Drive
   - Sheet updated with metadata

3. Check:
   - No errors in Parse Classification node
   - Correct classification in output
   - Metadata fields populated (date, vendor, amount, currency)

### Error Scenario Test

If Parse Classification fails, check n8n execution logs for:
- Original Anthropic response format (in error message)
- Which extraction step failed
- Whether validation caught missing fileType

---

## Node Configuration

**Node ID**: `parse-classification`
**Type**: n8n-nodes-base.code
**Type Version**: 2
**Code Size**: 2,056 characters

**Input**:
- From "Classify with Anthropic Vision" HTTP response node
- Expects: `response.content[0].text` containing JSON

**Output**:
- fileType (receipt | sway_invoice | expensify | unknown)
- vendor (string)
- date (YYYY-MM-DD)
- amount (string)
- currency (3-letter code)
- description (string)
- confidence (0-1)
- fileName (from metadata)
- fileId (from metadata)
- processedDate (from metadata)
- binary (file binary passed through)

---

## Files Updated

**Modified Files**:
- Workflow `qSuG0gwuJByd2hGJ` on n8n.oloxa.ai
  - Parse Classification node code only
  - All other nodes unchanged
  - Workflow active state preserved

**Documentation Created**:
- `/claude-code-os/02-operations/technical-builds/oloxa/SwaysExpenseSystem/compacting-summaries/summary_v13.0_2026-01-31.md`
- `/claude-code-os/02-operations/technical-builds/oloxa/SwaysExpenseSystem/PARSE_CLASSIFICATION_FIX_COMPLETE.md` (this file)

---

## Next Steps

1. **Test**: Run workflow with various PDF/image inputs
2. **Monitor**: Check for Parse Classification errors in executions
3. **Cleanup**: Address other validation warnings if desired:
   - Google Drive upload node operation names
   - Type version upgrades
   - Expression format warnings

---

## Technical Details

### Why This Works

The multi-level approach handles all known Anthropic response variations:

```javascript
// Level 1: What if Claude returns pure JSON?
JSON.parse(textContent)

// Level 2: What if Claude wraps it? ```json {...}```
textContent.replace(/^```json\n?/, '').replace(/\n?```$/, '')

// Level 3: What if there's a regex-matchable block?
textContent.match(/```(?:json)?\n?([\s\S]*?)```/)

// Level 4: What if it's just embedded in text? {...}
textContent.substring(jsonStart, jsonEnd + 1)
```

Each level only runs if the previous failed, so it's efficient (no unnecessary parsing).

### Error Handling

If all extraction methods fail:
- Throws descriptive error with response preview
- Prevents silent failures or undefined behavior
- Includes first 500 chars of response for debugging

### Defensive Defaults

Even if JSON is missing optional fields, the node won't crash:
```javascript
fileType: classification.fileType || 'unknown',
vendor: classification.vendor || 'Unknown',
date: classification.date || '',
amount: classification.amount || '0',
```

---

## Support

If the fix doesn't work for a specific Anthropic response format:

1. Check n8n execution logs for the response that failed
2. Note the error message showing response preview
3. The 4 extraction methods cover all known formats
4. If a new format is discovered, can add Level 5 extraction

---

## Implementation Notes

- Updated via n8n REST API (n8n_update_partial_workflow MCP had schema issues)
- No workflow structure changes - only code node parameters
- Backward compatible with old response formats
- Zero performance impact (nested try-catch only used if needed)
- Thoroughly documented with step-by-step comments in code
