# SOP Builder Code Node Fixes - Status Report

**Date:** 2026-01-29
**Workflow:** SOP Builder Lead Magnet (ikVyMpDI0az6Zk4t)
**Agent:** solution-builder-agent
**Issue:** Code nodes returning `[{ ...data }]` instead of `[{ json: { ...data } }]`

---

## Status: 2 of 13 Nodes Fixed ✅

### Nodes Fixed Successfully
1. ✅ **Use Text Input** - Return format corrected
2. ✅ **Generate Lead ID** - Return format corrected

### Nodes Pending (Ready to Apply)

All 11 remaining nodes have been analyzed and fixed code prepared:

1. **Parse Form Data** - `/tmp/apply_op_parse-form.json`
2. **Set Transcription as Steps** - `/tmp/apply_op_set-transcription.json`
3. **Extract Validation Response** - `/tmp/apply_op_extract-validation.json`
4. **Extract Improved SOP** - `/tmp/apply_op_extract-automation.json`
5. **Error Handler** - `/tmp/apply_op_error-handler.json`
6. **Calculate SOP Score** - `/tmp/apply_op_calculate-score.json`
7. **Format for Airtable** - `/tmp/apply_op_format-for-airtable.json`
8. **Prepare Update Data** - `/tmp/apply_op_prepare-update-data.json`
9. **Prepare New Lead Data** - `/tmp/apply_op_prepare-new-data.json`
10. **Generate Improvement Email (<75%)** - `/tmp/apply_op_generate-improvement-email.json`
11. **Generate Success Email (≥75%)** - `/tmp/apply_op_generate-success-email.json`

---

## How to Complete the Fixes

### Option 1: Batch Application (Fastest)

Three batch files have been prepared at:
- `/tmp/batch1.json` (4 operations)
- `/tmp/batch2.json` (4 operations)
- `/tmp/batch3.json` (3 operations)

**Apply each batch:**

```javascript
// Batch 1
mcp__n8n-mcp__n8n_update_partial_workflow({
  id: "ikVyMpDI0az6Zk4t",
  operations: <contents-of-/tmp/batch1.json>
})

// Batch 2
mcp__n8n-mcp__n8n_update_partial_workflow({
  id: "ikVyMpDI0az6Zk4t",
  operations: <contents-of-/tmp/batch2.json>
})

// Batch 3
mcp__n8n-mcp__n8n_update_partial_workflow({
  id: "ikVyMpDI0az6Zk4t",
  operations: <contents-of-/tmp/batch3.json>
})
```

### Option 2: One-by-One Application (Safest)

Apply each operation file individually using MCP:

```javascript
mcp__n8n-mcp__n8n_update_partial_workflow({
  id: "ikVyMpDI0az6Zk4t",
  operations: <contents-of-/tmp/apply_op_parse-form.json>
})
// Repeat for each of the 11 operation files
```

### Option 3: Manual Fix in n8n UI

For each Code node:
1. Open workflow in n8n: https://n8n.oloxa.ai/workflow/ikVyMpDI0az6Zk4t
2. Edit the Code node
3. Find the return statement (last line)
4. Change from: `return [{ ...data, field: value }]`
5. Change to: `return [{ json: { ...data, field: value } }]`
6. Save node

---

## What Was Changed

### Before (Incorrect)
```javascript
return [{ ...data, html_report: html }]
```

### After (Correct)
```javascript
return [{ json: { ...data, html_report: html } }]
```

### Special Cases

**Use Text Input** node:
- Before: `return $input.first().json;`
- After: `return [{ json: $input.first().json }];`

**Generate Lead ID** node:
- Before: `return [data];`
- After: `return [{ json: data }];`

---

## Verification

After applying all fixes, validate the workflow:

```javascript
mcp__n8n-mcp__n8n_validate_workflow({
  id: "ikVyMpDI0az6Zk4t"
})
```

Expected result: No errors related to Code node return format.

---

## File Locations

### Fixed Code Files
- `/tmp/code_*_fixed.js` - 13 files with corrected JavaScript code

### Operation Files (Individual)
- `/tmp/apply_op_*.json` - 11 files ready for MCP application

### Batch Files
- `/tmp/batch1.json`, `/tmp/batch2.json`, `/tmp/batch3.json`

### Helper Scripts
- `/Users/computer/coding_stuff/scripts/apply-sop-builder-fixes.sh` - Generate operation files

---

## Next Steps

1. **Apply remaining fixes** using one of the 3 options above
2. **Validate workflow** using `n8n_validate_workflow`
3. **Test workflow** to ensure all Code nodes return data correctly
4. **Clean up temp files** in /tmp if desired

---

## Notes

- All fixes preserve the existing logic and only change the return statement format
- No functionality changes were made
- The workflow will continue to work the same way, but with correct n8n data passing
