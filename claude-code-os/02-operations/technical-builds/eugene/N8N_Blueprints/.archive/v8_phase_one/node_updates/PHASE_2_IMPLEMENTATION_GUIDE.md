# Phase 2 Implementation Guide
## Ready-to-Apply Node Modifications

**Date:** 2026-01-12 22:20 CET
**Workflow:** Chunk 2.5 (ID: okg8wTqLtPUwjQ18)
**Phase:** 2 of 4 (Modify Existing Nodes)

---

## Prerequisites

✅ Backup exists: `.backups/chunk_2.5_v8.0_BEFORE_PHASE2_20260112.json`
✅ Node code prepared in `/node_updates/` folder
✅ Specification validated: `V8_IMPLEMENTATION_SPEC.md`

---

## Implementation Steps

### Step 1: Modify code-1 Node

**Node Name:** `Build AI Classification Prompt`
**Node ID:** `code-1`
**Type:** Code (JavaScript)

**Source File:** `/node_updates/code-1_tier1_prompt.js`

**MCP Operation:**
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow(
  workflowId: "okg8wTqLtPUwjQ18",
  operations: [{
    op: "updateNode",
    nodeName: "Build AI Classification Prompt",
    updates: {
      parameters: {
        jsCode: `// [INSERT CONTENT OF code-1_tier1_prompt.js HERE]`
      }
    }
  }]
)
```

**Validation After:**
```javascript
mcp__n8n-mcp__n8n_validate_workflow(
  workflowId: "okg8wTqLtPUwjQ18"
)
```

**Expected Changes:**
- Old: Single-tier classification prompt
- New: Tier 1 category-only prompt (4 categories)
- Output adds: `tier1Prompt` field

---

### Step 2: Modify code-2 Node

**Node Name:** `Parse Classification Result`
**Node ID:** `code-2`
**Type:** Code (JavaScript)

**Source File:** `/node_updates/code-2_tier1_parse_tier2_builder.js`

**MCP Operation:**
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow(
  workflowId: "okg8wTqLtPUwjQ18",
  operations: [{
    op: "updateNode",
    nodeName: "Parse Classification Result",
    updates: {
      parameters: {
        jsCode: `// [INSERT CONTENT OF code-2_tier1_parse_tier2_builder.js HERE]`
      }
    }
  }]
)
```

**Validation After:**
```javascript
mcp__n8n-mcp__n8n_validate_workflow(
  workflowId: "okg8wTqLtPUwjQ18"
)
```

**Expected Changes:**
- Old: Parse single classification result
- New: Parse Tier 1 result + Build dynamic Tier 2 prompt based on category
- Outputs: `tier1Category`, `tier1Confidence`, `tier1Reasoning`, `tier2Prompt`
- Adds threshold check: Tier 1 confidence >= 60%
- Adds low confidence flag if threshold not met

---

### Step 3: Create Backup After Phase 2

**Export workflow and save:**

```bash
Filename: .backups/chunk_2.5_v8.0_AFTER_PHASE2_20260112_[HH:MM].json
Timestamp format: 24-hour (e.g., 22:20)
```

**How to export:**
```javascript
mcp__n8n-mcp__n8n_get_workflow(
  workflowId: "okg8wTqLtPUwjQ18",
  mode: "full"
)
```

Then save the JSON response to the backup file.

---

## Verification Checklist

After completing Phase 2, verify:

- [ ] code-1 modified successfully
- [ ] code-2 modified successfully
- [ ] Workflow validates without errors
- [ ] Backup created with timestamp
- [ ] V8_CHANGELOG.md updated with Phase 2 completion

---

## Expected Workflow State After Phase 2

**Modified Nodes:** 2
**Added Nodes:** 0
**Total Nodes:** 18 (unchanged)

**Data Flow Changes:**
```
OLD: code-1 → http-openai-1 → code-2 (single-tier classification)
NEW: code-1 → http-openai-1 → code-2 (Tier 1 category + Tier 2 prompt ready)
```

**New Fields Available:**
- `tier1Prompt` (from code-1)
- `tier1Category` (from code-2)
- `tier1Confidence` (from code-2)
- `tier1Reasoning` (from code-2)
- `tier2Prompt` (from code-2)
- `lowConfidence` (from code-2, if threshold not met)
- `confidenceFailureStage` (from code-2, if threshold not met)

---

## Next Phase Preview

**Phase 3 will add:**
1. `http-openai-2` node (calls GPT-4 with tier2Prompt)
2. `code-tier2-parse` node (parses Tier 2 result)
3. Connections between new nodes

**Phase 3 requires:**
- Phase 2 successfully completed
- Workflow validated
- Backup created

---

## Troubleshooting

### If code-1 modification fails:
- Check node name matches exactly: "Build AI Classification Prompt"
- Verify jsCode parameter path
- Check for JavaScript syntax errors in source file

### If code-2 modification fails:
- Check node name matches exactly: "Parse Classification Result"
- Verify jsCode parameter path
- Check for JavaScript syntax errors in source file

### If validation fails:
- Review error message from n8n_validate_workflow
- Check if connections were accidentally broken
- Verify all required parameters are present

---

## Files Reference

**Node Code:**
- `/node_updates/code-1_tier1_prompt.js`
- `/node_updates/code-2_tier1_parse_tier2_builder.js`

**Specification:**
- `V8_IMPLEMENTATION_SPEC.md` (lines 85-159, 166-537)

**Backup:**
- `.backups/chunk_2.5_v8.0_BEFORE_PHASE2_20260112.json` (existing)
- `.backups/chunk_2.5_v8.0_AFTER_PHASE2_20260112_[HH:MM].json` (to be created)

---

**Status:** Ready for main conversation MCP execution
**Prepared by:** solution-builder-agent
**Date:** 2026-01-12 22:20 CET
