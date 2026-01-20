# W4 Filter Fix - Visual Comparison

## Before Fix (v2.0) - 404 Errors

```
Read Statements Sheet
         ↓
Process Statements ──────→ Outputs both:
         ↓                  - Valid items (with fileId)
         ↓                  - Errored items (skipped: true, error: "Missing Bank")
         ↓
Move Statement Files ─────→ ❌ 404 ERROR!
         ↓                   (Tries to move items without fileId)
         ↓
Update Statements FilePath
```

```
Read Receipts Sheet
         ↓
Process Receipts ────────→ Outputs both:
         ↓                  - Valid items (with fileId)
         ↓                  - Errored items (skipped: true, error: "No transaction_id")
         ↓
Move Receipt Files ───────→ ❌ 404 ERROR!
         ↓                   (Tries to move items without fileId)
         ↓
Update Receipts FilePath
```

---

## After Fix (v2.1) - No Errors

```
Read Statements Sheet
         ↓
Process Statements ──────→ Outputs both:
         ↓                  - Valid items (with fileId)
         ↓                  - Errored items (skipped: true, error: "Missing Bank")
         ↓
Filter Valid Statements ──→ ✅ FILTERS OUT errored items
         ↓                   Only passes: fileId exists, skipped != true, error is empty
         ↓
Move Statement Files ─────→ ✅ SUCCESS!
         ↓                   (Only processes valid items)
         ↓
Update Statements FilePath
```

```
Read Receipts Sheet
         ↓
Process Receipts ────────→ Outputs both:
         ↓                  - Valid items (with fileId)
         ↓                  - Errored items (skipped: true, error: "No transaction_id")
         ↓
Filter Valid Receipts ────→ ✅ FILTERS OUT errored items
         ↓                   Only passes: fileId exists, skipped != true, error is empty
         ↓
Move Receipt Files ───────→ ✅ SUCCESS!
         ↓                   (Only processes valid items)
         ↓
Update Receipts FilePath
```

---

## Filter Logic (Both Filters Use Same Logic)

```
ALL of these conditions must be TRUE:
  1. $json.skipped !== true       (Item is not marked as skipped)
  2. $json.error is empty          (No error message present)
  3. $json.fileId is not empty     (Valid file ID exists)
```

---

## Example Data Flow

### Valid Statement (Passes Filter)
```json
{
  "statementId": "S001",
  "fileId": "1abc123xyz",
  "bank": "ING Diba",
  "targetFolderId": "1xyz789abc",
  "month": "September",
  "year": "2025"
}
```
**Result:** ✅ Passes filter → Moves file successfully

### Invalid Statement (Blocked by Filter)
```json
{
  "statementId": "S002",
  "error": "Missing Bank or FileID",
  "skipped": true
}
```
**Result:** ❌ Blocked by filter → No move attempted → No 404 error

---

## Summary Report Handling

The "Generate Summary Report" node still sees ALL items from "Process Statements" and "Process Receipts" (including skipped ones), so it can accurately report:

```json
{
  "statistics": {
    "statements_organized": 3,    ← Only successfully moved
    "statements_skipped": 2,       ← Filtered out (not moved)
    "receipts_organized": 5,
    "receipts_skipped": 1,
    "total_files_moved": 8,
    "errors_count": 3
  },
  "errors": [
    "Statement: Missing Bank or FileID",
    "Statement: Missing Bank or FileID",
    "Receipt: No transaction_id"
  ]
}
```

---

## Technical Implementation

### Filter Node Configuration

**Node Type:** `n8n-nodes-base.filter` v2

**Parameters:**
```json
{
  "conditions": {
    "options": {
      "caseSensitive": true,
      "typeValidation": "strict"
    },
    "conditions": [
      {
        "id": "skip-check",
        "leftValue": "={{ $json.skipped }}",
        "rightValue": true,
        "operator": {
          "type": "boolean",
          "operation": "notEquals"
        }
      },
      {
        "id": "error-check",
        "leftValue": "={{ $json.error }}",
        "rightValue": "",
        "operator": {
          "type": "string",
          "operation": "isEmpty"
        }
      },
      {
        "id": "fileid-check",
        "leftValue": "={{ $json.fileId }}",
        "rightValue": "",
        "operator": {
          "type": "string",
          "operation": "notEmpty"
        }
      }
    ],
    "combinator": "and"
  }
}
```

---

## Testing Scenarios

### Scenario 1: All Valid
**Input:** 5 statements, all have Bank + FileID
**Filter Output:** 5 items passed
**Move Result:** 5 files moved
**Summary:** `statements_organized: 5, statements_skipped: 0`

### Scenario 2: Mixed Valid/Invalid
**Input:** 5 statements, 2 missing Bank
**Filter Output:** 3 items passed, 2 blocked
**Move Result:** 3 files moved
**Summary:** `statements_organized: 3, statements_skipped: 2`

### Scenario 3: All Invalid
**Input:** 5 statements, all missing FileID
**Filter Output:** 0 items passed, 5 blocked
**Move Result:** No moves attempted
**Summary:** `statements_organized: 0, statements_skipped: 5`

---

## Benefits of This Approach

1. **Zero False Positives:** Only truly valid items proceed to Move operations
2. **Clear Error Reporting:** Summary report still shows all skipped items and reasons
3. **No Side Effects:** Existing valid items continue processing exactly as before
4. **Defensive Programming:** Triple-check (skipped, error, fileId) ensures safety
5. **Easy to Debug:** Filter conditions are explicit and visible in n8n UI
6. **Performance:** Negligible impact, filter operations are very fast
7. **Maintainable:** Logic is simple and self-documenting

---

## Node Positions in Canvas

```
Statements Path (y=100):
  Process Statements [2440, 100]
          ↓
  Filter Valid Statements [2560, 100] ← NEW
          ↓
  Move Statement Files [2760, 100] (shifted right by 100px)
          ↓
  Update Statements FilePath [2980, 100] (shifted right by 100px)

Receipts Path (y=300):
  Process Receipts [2440, 300]
          ↓
  Filter Valid Receipts [2560, 300] ← NEW
          ↓
  Move Receipt Files [2760, 300] (shifted right by 100px)
          ↓
  Update Receipts FilePath [2980, 300] (shifted right by 100px)
```
