# Claude Vision Extract Identifier - BPS Prompt Update

## Update Summary

**Workflow:** AMA Pre-Chunk 0 - REBUILT v1 (YGXWjWcBIk66ArvT)
**Node:** Claude Vision Extract Identifier (claude-vision-extract-001)
**Date:** 2026-01-18
**Status:** ✅ Successfully Updated

---

## What Changed

Replaced the simplified prompt in the Claude Vision API request with the **full BPS-structured prompt** containing:

1. **# Role** - Expert German real estate document analyst definition
2. **# Task** - 5-step extraction sequence (Scan → Prioritize → Normalize → Validate → Return)
3. **# Specifics** - Complete priority hierarchy, normalization rules, output format, and forbidden patterns
4. **# Context** - Eugene's project-based routing system explanation
5. **# Examples** - 5 detailed examples showing correct/incorrect outputs
6. **# Notes** - Critical enforcement rules, guardrails, and edge case handling

---

## Technical Details

**Node Type:** `n8n-nodes-base.httpRequest`
**Method:** POST
**URL:** `https://api.anthropic.com/v1/messages`
**Model:** `claude-sonnet-4-20250514`
**Max Tokens:** 50

**Body Parameter:** Set as EXPRESSION (= prefix)

**Key Expression Fields:**
- `media_type`: `{{ $json.imageData.media_type }}`
- `data`: `{{ $json.imageData.data }}`

---

## Prompt Structure (Full BPS Format)

### Previous Prompt (Simplified)
```
You are an expert German real estate document analyst. Extract the single identifier from this document.

Priority order:
1. Project code/name (e.g., 'BV Propos' → 'Propos')
2. Company name (e.g., 'VAH Immobilien GmbH' → 'VAH')
3. Street address as last resort (e.g., 'Adolf-Martens-Straße 10' → 'Adolf-Martens 10')

Normalization: ß→ss, ä→ae, ö→oe, ü→ue. Remove 'GmbH', 'AG', 'KG', 'straße', 'str.'.

Return ONLY the normalized identifier. No explanations. If none found, return: UNKNOWN
```

### New Prompt (Full BPS Structure)
Now includes:
- **Role definition**: Project identification and entity normalization expertise
- **Task breakdown**: 5-step process (Scan, Prioritize, Normalize, Validate, Return)
- **Specifics**: Detailed priority hierarchy, normalization rules, forbidden output patterns
- **Context**: Eugene's project-based routing system (why this matters)
- **Examples**: 5 detailed scenarios with correct/incorrect outputs
- **Notes**: Critical enforcement, guardrails, edge case handling

**Total prompt length:** ~3,200 characters (vs. ~400 in simplified version)

---

## Validation Results

**Workflow Status:** Active
**Total Nodes:** 49
**Enabled Nodes:** 43
**Operations Applied:** 1

**Node-Specific Warnings:**
- Outdated typeVersion: 4.2 (latest is 4.3) - cosmetic only
- No error handling configured - consider adding for production

**No critical errors** related to the Claude Vision node.

---

## Expected Behavior Changes

With the full BPS prompt, the Claude Vision API should now:

1. **Better project identification**: Clearer hierarchy (project → company → address)
2. **Consistent normalization**: Stricter German character and suffix rules
3. **Cleaner output**: Fewer explanatory responses, more plain identifiers
4. **Improved edge cases**: Better handling of multi-project documents, mixed languages, abbreviations

---

## Testing Recommendations

1. **Test with BV Propos document**: Should return `Propos` (not "BV Propos" or "Bauvorhaben Propos")
2. **Test with company-only document**: Should return `VAH` (not "VAH Immobilien GmbH")
3. **Test with address-only document**: Should return `Adolf-Martens 10` (normalized)
4. **Test with generic document**: Should return `UNKNOWN` (not hallucinated identifiers)
5. **Test with scanned/poor quality**: Should gracefully handle with best-effort or UNKNOWN

---

## Next Steps

1. ✅ **Update complete** - Node now has full BPS prompt
2. ⏳ **Test in production** - Monitor extraction quality on real documents
3. 📊 **Track metrics** - Compare UNKNOWN rate vs. simplified prompt
4. 🔧 **Adjust if needed** - Fine-tune examples/rules based on edge cases

---

## Files Modified

- **Workflow ID:** YGXWjWcBIk66ArvT
- **Node ID:** claude-vision-extract-001
- **Parameter:** `parameters.jsonBody`

**No local files modified** - update applied directly via n8n MCP server.

---

## Rollback Instructions (If Needed)

To revert to the simplified prompt:

```javascript
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 50,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "document",
          "source": {
            "type": "base64",
            "media_type": {{ $json.imageData.media_type }},
            "data": {{ $json.imageData.data }}
          }
        },
        {
          "type": "text",
          "text": "You are an expert German real estate document analyst. Extract the single identifier from this document.\n\nPriority order:\n1. Project code/name (e.g., 'BV Propos' → 'Propos')\n2. Company name (e.g., 'VAH Immobilien GmbH' → 'VAH')\n3. Street address as last resort (e.g., 'Adolf-Martens-Straße 10' → 'Adolf-Martens 10')\n\nNormalization: ß→ss, ä→ae, ö→oe, ü→ue. Remove 'GmbH', 'AG', 'KG', 'straße', 'str.'.\n\nReturn ONLY the normalized identifier. No explanations. If none found, return: UNKNOWN"
        }
      ]
    }
  ]
}
```

Use `mcp__n8n-mcp__n8n_update_partial_workflow` with the same operation structure to revert.
