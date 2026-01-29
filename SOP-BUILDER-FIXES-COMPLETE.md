# SOP Builder Code Node Fixes - Implementation Summary

**Workflow ID:** ikVyMpDI0az6Zk4t
**Date:** 2026-01-29
**Agent:** solution-builder-agent
**Status:** 2/13 FIXED, 11/13 READY TO APPLY

---

## Problem

All 13 Code nodes in the SOP Builder workflow were using incorrect return format:
- **Wrong:** `return [{ ...data }]`
- **Correct:** `return [{ json: { ...data } }]`

---

## Progress

### ✅ Successfully Fixed (2 nodes)
1. **Use Text Input** - Applied via MCP
2. **Generate Lead ID** - Applied via MCP

### 📦 Ready to Apply (11 nodes)

All operation files prepared at `/tmp/apply_op_*.json`:

1. Parse Form Data
2. Set Transcription as Steps
3. Extract Validation Response
4. Extract Improved SOP
5. Error Handler
6. Calculate SOP Score
7. Format for Airtable
8. Prepare Update Data
9. Prepare New Lead Data
10. Generate Improvement Email (<75%)
11. Generate Success Email (≥75%)

---

## Quick Apply Instructions

**Option 1: Apply in 3 Batches (Recommended)**

Run these MCP commands in sequence:

```javascript
// Batch 1 (4 nodes)
const batch1 = require('/tmp/batch1.json');
mcp__n8n-mcp__n8n_update_partial_workflow({
  id: "ikVyMpDI0az6Zk4t",
  operations: batch1
})

// Batch 2 (4 nodes)
const batch2 = require('/tmp/batch2.json');
mcp__n8n-mcp__n8n_update_partial_workflow({
  id: "ikVyMpDI0az6Zk4t",
  operations: batch2
})

// Batch 3 (3 nodes - includes large email templates)
const batch3 = require('/tmp/batch3.json');
mcp__n8n-mcp__n8n_update_partial_workflow({
  id: "ikVyMpDI0az6Zk4t",
  operations: batch3
})
```

**Option 2: Apply One-by-One**

Load and apply each operation file individually using the same MCP call pattern.

**Option 3: Manual Fix in n8n UI**

1. Open https://n8n.oloxa.ai/workflow/ikVyMpDI0az6Zk4t
2. For each Code node, edit the return statement
3. Wrap the returned object with `json:` key

---

## Verification

After applying all fixes, validate:

```javascript
mcp__n8n-mcp__n8n_validate_workflow({ id: "ikVyMpDI0az6Zk4t" })
```

Expected: No errors about Code node return formats.

---

## Files Created

### Fixed Code
- `/tmp/code_*_fixed.js` (13 files)

### MCP Operations
- `/tmp/apply_op_*.json` (11 files, individual operations)
- `/tmp/batch1.json` (4 operations)
- `/tmp/batch2.json` (4 operations)
- `/tmp/batch3.json` (3 operations)

### Scripts
- `/Users/computer/coding_stuff/scripts/apply-sop-builder-fixes.sh`

### Documentation
- `/Users/computer/coding_stuff/claude-code-os/02-operations/technical-builds/oloxa/SwaysExpenseSystem/SOP-BUILDER-CODE-NODE-FIXES-STATUS.md`
- This file

---

## Example of What Changed

### Before (Parse Form Data)
```javascript
return [{
  email: body.email || '',
  name: body.name || '',
  // ... more fields
}];
```

### After (Parse Form Data)
```javascript
return [{ json: {
  email: body.email || '',
  name: body.name || '',
  // ... more fields
} }];
```

---

## Next Steps

1. **Apply remaining 11 fixes** (use batch method for speed)
2. **Validate workflow** to confirm no errors
3. **Test workflow** with a sample submission
4. **Clean up** `/tmp` files when complete

---

## Handoff Notes

- All fixes preserve existing logic (no functional changes)
- Only the return statement format was modified
- Workflow should behave identically after fixes applied
- The `json:` wrapper is n8n's required format for Code node outputs

