# Claude Vision Prompt Update - Pre-Chunk 0

**Date:** 2026-01-18
**Issue:** Extracting addresses instead of project names
**Root Cause:** Wrong priority order in prompt

---

## The Problem

**Example from execution 4222:**
- Document: "Energiebedarfsausweis Entwurf ADM10.pdf"
- Extracted: **"Adolf-Martens 10"** (street address)
- Expected: Project name or company name (if available)

**Why this happened:**
The prompt prioritized street addresses as #1, so Claude Vision extracted "Adolf-Martens-Straße 10" instead of looking for a project name first.

---

## Business Logic (Eugene's Explanation)

**Eugene's organization hierarchy:**
1. **Project-based** (e.g., "BV Propos", "Villa Martens") ← PRIMARY
2. **Company/client-based** (e.g., "VAH Immobilien", "Propos GmbH") ← FALLBACK
3. **Address-based** (e.g., "Adolf-Martens 10") ← LAST RESORT

**Why projects matter:**
- One project can span multiple addresses
- Documents for "BV Propos" should go to ONE folder: `propos`
- NOT separate folders: `schlossberg_13`, `adolf_martens_10`, etc.

---

## Prompt Changes

### BEFORE (v9.0 - WRONG Priority)

```
Extract the PROJECT or PROPERTY IDENTIFIER from this German real estate document.

Look for (in priority order):
1. Street address (e.g., 'Schloßbergstraße 13' → 'Schlossberg 13')  ← WRONG #1
2. Project code (e.g., 'BV Propos' → 'Propos')
3. Property name (e.g., 'Villa Martens')
4. Company name (e.g., 'Propos GmbH' → 'Propos')

Rules:
- Normalize German: ß→ss, ä→ae, ö→oe, ü→ue
- Remove 'straße/str.' from addresses, keep number
- Return ONLY the identifier, nothing else
- If no identifier found, return: UNKNOWN
```

**Result:** Extracted "Adolf-Martens 10" from document

---

### AFTER (v9.1 - CORRECT Priority)

```
Extract the PROJECT or PROPERTY IDENTIFIER from this German real estate document.

Look for (in priority order):
1. Project code or name (e.g., 'BV Propos' → 'Propos', 'Villa Martens', 'Projekt Schlossberg')  ← CORRECT #1
2. Company or client name (e.g., 'VAH Immobilien' → 'VAH', 'Propos GmbH' → 'Propos')
3. Street address ONLY as last resort (e.g., 'Adolf-Martens-Straße 10' → 'Adolf-Martens 10')

Rules:
- Normalize German: ß→ss, ä→ae, ö→oe, ü→ue
- Remove common suffixes: 'GmbH', 'AG', 'KG', 'straße/str.'
- Return ONLY the identifier, nothing else
- Prefer project/company names over addresses
- If no identifier found, return: UNKNOWN
```

**Expected result:** Extract project name (if present) instead of address

---

## Implementation Details

**Workflow:** Pre-Chunk 0 (YGXWjWcBIk66ArvT)
**Node:** Claude Vision Extract Identifier (claude-vision-extract-001)
**Updated by:** solution-builder-agent (adc3f61)
**Date:** 2026-01-18T21:45:00Z

---

## Test Cases

### Test Case 1: Document with Project Name
**Input:** Invoice for "BV Propos" at "Schloßbergstraße 13"
**Expected extraction:** "Propos"
**Should NOT extract:** "Schlossberg 13"

### Test Case 2: Document with Company Only
**Input:** Invoice from "VAH Immobilien GmbH"
**Expected extraction:** "VAH"
**Should NOT extract:** Address (if present)

### Test Case 3: Document with Address Only
**Input:** Invoice with "Adolf-Martens-Straße 10" but no project/company name
**Expected extraction:** "Adolf-Martens 10"
**Fallback behavior:** Correct

### Test Case 4: Real-world Example
**Input:** "Energiebedarfsausweis Entwurf ADM10.pdf" (from execution 4222)
**Old behavior:** Extracted "Adolf-Martens 10"
**New behavior:** Should extract project name (if document contains one)

---

## Expected Impact

### Positive Changes
1. **Better client grouping** - Documents for same project go to same folder
2. **Fewer unknowns** - More accurate identification reduces `38_Unknowns` routing
3. **Business logic alignment** - Matches how Eugene actually organizes deals

### Potential Edge Cases
1. **Documents with no project name** - Will fallback to company, then address
2. **Multiple projects on one document** - Claude will pick the most prominent one
3. **Ambiguous names** - May require manual review in Client Registry

---

## Monitoring

**Check these metrics after update:**
1. **Extraction accuracy** - Run test workflow, check spreadsheet results
2. **Unknown rate** - Monitor `38_Unknowns` folder (should decrease)
3. **Client Registry matches** - Check "Decision Gate" NEW/EXISTING/UNKNOWN routing

**How to review extraction:**
```sql
-- Check Pre-Chunk 0 executions
SELECT executionId, extractedText, client_name, client_normalized
FROM executions
WHERE workflowId = 'YGXWjWcBIk66ArvT'
  AND startedAt > '2026-01-18T21:45:00Z'
ORDER BY startedAt DESC
LIMIT 20;
```

---

## Version History

| Version | Date | Priority Order | Status |
|---------|------|----------------|--------|
| v9.0 | 2026-01-17 | Address → Project → Company | ❌ Wrong |
| **v9.1** | **2026-01-18** | **Project → Company → Address** | **✅ Correct** |

---

## Next Steps

1. ✅ **Update complete** - Prompt priority fixed
2. ⏳ **Test workflow** - Run with real documents
3. ⏳ **Monitor results** - Check extraction accuracy
4. ⏳ **Adjust if needed** - Refine prompt based on real-world results
