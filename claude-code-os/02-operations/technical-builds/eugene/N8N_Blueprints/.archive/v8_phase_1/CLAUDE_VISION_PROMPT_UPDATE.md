# Claude Vision Prompt Priority Update

**Date:** 2026-01-18
**Workflow:** AMA Pre-Chunk 0 - REBUILT v1 (YGXWjWcBIk66ArvT)
**Node:** Claude Vision Extract Identifier
**Agent:** solution-builder-agent

---

## Summary

Updated the Claude Vision prompt in Pre-Chunk 0 to **prioritize PROJECT NAMES over street addresses**, aligning with Eugene's business logic.

---

## Changes Made

### Before (WRONG Priority Order)
```
Look for (in priority order):
1. Street address (e.g., 'Schloßbergstraße 13' → 'Schlossberg 13')
2. Project code (e.g., 'BV Propos' → 'Propos')
3. Property name (e.g., 'Villa Martens')
4. Company name (e.g., 'Propos GmbH' → 'Propos')
```

### After (CORRECT Priority Order) ✅
```
Look for (in priority order):
1. Project code or name (e.g., 'BV Propos' → 'Propos', 'Villa Martens', 'Projekt Schlossberg')
2. Company or client name (e.g., 'VAH Immobilien' → 'VAH', 'Propos GmbH' → 'Propos')
3. Street address ONLY as last resort (e.g., 'Adolf-Martens-Straße 10' → 'Adolf-Martens 10')
```

---

## Full Updated Prompt

```
Extract the PROJECT or PROPERTY IDENTIFIER from this German real estate document.

Look for (in priority order):
1. Project code or name (e.g., 'BV Propos' → 'Propos', 'Villa Martens', 'Projekt Schlossberg')
2. Company or client name (e.g., 'VAH Immobilien' → 'VAH', 'Propos GmbH' → 'Propos')
3. Street address ONLY as last resort (e.g., 'Adolf-Martens-Straße 10' → 'Adolf-Martens 10')

Rules:
- Normalize German: ß→ss, ä→ae, ö→oe, ü→ue
- Remove common suffixes: 'GmbH', 'AG', 'KG', 'straße/str.'
- Return ONLY the identifier, nothing else
- Prefer project/company names over addresses
- If no identifier found, return: UNKNOWN

CRITICAL: Return ONLY the normalized identifier. NO explanations. NO formatting. NO bullet points. Just the identifier text.

Examples of CORRECT responses:
- Propos
- Villa Martens
- VAH
- Schlossberg 13
- UNKNOWN

Examples of INCORRECT responses:
- "The project name is Propos" (has explanation)
- "1. Project: Propos" (has numbering)
- "Propos (normalized from...)" (has parenthetical)
```

---

## Business Logic Rationale

**Why project names come first:**
- Eugene's business is project-based (e.g., "BV Propos", "Villa Martens")
- Projects often span multiple addresses
- Clients may use the same address for multiple projects
- Street addresses are generic fallbacks only when no project/client name exists

**Example scenarios:**
- Document says "BV Propos, Schloßbergstraße 13" → Extract "Propos" (NOT "Schlossberg 13")
- Document says "VAH Immobilien GmbH" → Extract "VAH" (NOT an address)
- Document says only "Adolf-Martens-Straße 10" → Extract "Adolf-Martens 10" (last resort)

---

## Technical Implementation

**Node Type:** HTTP Request (Claude API)
**Model:** claude-sonnet-4-20250514
**Max Tokens:** 50

**Update Method:**
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow({
  id: "YGXWjWcBIk66ArvT",
  operations: [{
    type: "updateNode",
    nodeName: "Claude Vision Extract Identifier",
    updates: {
      "parameters.body": "={\n  \"model\": \"claude-sonnet-4-20250514\",\n  \"max_tokens\": 50,\n  \"messages\": [...]\n}"
    }
  }]
})
```

---

## Verification

**Status:** ✅ Successfully applied
**Operations Applied:** 1
**Workflow Active:** Yes

**Verified via:**
```bash
cat workflow.json | jq '.data.nodes[] | select(.name == "Claude Vision Extract Identifier") | .parameters.body'
```

**Result:** Prompt text matches the updated priority order exactly.

---

## Next Steps

1. **Test with real invoices** - Use test-runner-agent to verify extraction behavior
2. **Monitor 38_Unknowns folder** - Check if project names are now correctly extracted
3. **Compare with old behavior** - Document any changes in routing decisions

---

## Related Workflows

- **Pre-Chunk 0** (YGXWjWcBIk66ArvT) - Updated ✅
- **Client Registry** (Google Sheets) - No changes needed
- **Chunk 2.5** - Downstream consumer (no changes needed)

---

**Update completed by:** solution-builder-agent
**Verification:** Prompt text matches expected format and priority order
