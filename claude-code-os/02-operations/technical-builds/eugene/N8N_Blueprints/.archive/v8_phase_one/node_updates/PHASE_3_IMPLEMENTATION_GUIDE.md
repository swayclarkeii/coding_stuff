# Phase 3 Implementation Guide
## Add Tier 2 Processing Nodes

**Date:** 2026-01-12 22:25 CET
**Workflow:** Chunk 2.5 (ID: okg8wTqLtPUwjQ18)
**Phase:** 3 of 4 (Add New Nodes)

---

## Prerequisites

✅ Phase 2 completed successfully
✅ Workflow validated after Phase 2
✅ Backup exists: `.backups/chunk_2.5_v8.0_AFTER_PHASE2_[timestamp].json`

---

## Implementation Steps

### Step 1: Add http-openai-2 Node

**Node Name:** `Tier 2 GPT-4 API Call`
**Node Type:** HTTP Request
**Position:** [1264, 320] (between code-2 and sheets-1)

**Configuration File:** `/node_updates/http-openai-2_config.json`

**MCP Operation:**
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow(
  workflowId: "okg8wTqLtPUwjQ18",
  operations: [{
    op: "addNode",
    node: {
      name: "Tier 2 GPT-4 API Call",
      type: "n8n-nodes-base.httpRequest",
      position: [1264, 320],
      parameters: {
        url: "https://api.openai.com/v1/chat/completions",
        authentication: "predefinedCredentialType",
        nodeCredentialType: "openAiApi",
        method: "POST",
        sendBody: true,
        contentType: "application/json",
        jsonBody: JSON.stringify({
          model: "gpt-4",
          messages: [
            {
              role: "user",
              content: "={{ $json.tier2Prompt }}"
            }
          ],
          temperature: 0.3,
          max_tokens: 300
        }),
        options: {
          response: {
            response: {
              responseFormat: "json"
            }
          }
        }
      },
      credentials: {
        openAiApi: {
          id: "[USE EXISTING OpenAI credential ID]",
          name: "OpenAI API (Sway)"
        }
      }
    }
  }]
)
```

**Purpose:**
- Takes `tier2Prompt` from code-2
- Calls GPT-4 to classify into specific document type (38 types)
- Returns Tier 2 classification result

---

### Step 2: Add code-tier2-parse Node

**Node Name:** `Parse Tier 2 Result`
**Node Type:** Code (JavaScript)
**Position:** [1488, 320] (after http-openai-2)

**Source File:** `/node_updates/code-tier2-parse.js`

**MCP Operation:**
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow(
  workflowId: "okg8wTqLtPUwjQ18",
  operations: [{
    op: "addNode",
    node: {
      name: "Parse Tier 2 Result",
      type: "n8n-nodes-base.code",
      position: [1488, 320],
      parameters: {
        jsCode: `// [INSERT CONTENT OF code-tier2-parse.js HERE]`
      }
    }
  }]
)
```

**Purpose:**
- Parses GPT-4 Tier 2 response
- Extracts: `documentType`, `tier2Confidence`, `germanName`, `englishName`, `isCoreType`
- Validates Tier 2 confidence >= 70%
- Calculates combined confidence (Tier 1 + Tier 2) / 2
- Sets `lowConfidence` flag if threshold not met

---

### Step 3: Connect New Nodes

**Update workflow connections:**

**OLD:**
```
code-2 → sheets-1
```

**NEW:**
```
code-2 → http-openai-2 → code-tier2-parse → [continue to existing flow]
```

**Connection 1:** code-2 → http-openai-2
```javascript
{
  source: "Parse Classification Result",
  target: "Tier 2 GPT-4 API Call",
  sourceOutput: "main"
}
```

**Connection 2:** http-openai-2 → code-tier2-parse
```javascript
{
  source: "Tier 2 GPT-4 API Call",
  target: "Parse Tier 2 Result",
  sourceOutput: "main"
}
```

**Connection 3:** code-tier2-parse → [existing next node]
- Will be determined in Phase 4 when we add code-action-mapper
- Temporarily can connect to sheets-1 for testing

---

### Step 4: Validate Workflow

```javascript
mcp__n8n-mcp__n8n_validate_workflow(
  workflowId: "okg8wTqLtPUwjQ18"
)
```

**Expected validation results:**
- ✅ All nodes connected properly
- ✅ No orphaned nodes
- ✅ JavaScript syntax valid in code-tier2-parse
- ✅ HTTP Request configuration valid

---

### Step 5: Create Backup After Phase 3

**Export and save:**

```bash
Filename: .backups/chunk_2.5_v8.0_AFTER_PHASE3_20260112_[HH:MM].json
```

---

## Verification Checklist

After completing Phase 3:

- [ ] http-openai-2 added successfully
- [ ] code-tier2-parse added successfully
- [ ] Connections established: code-2 → http-openai-2 → code-tier2-parse
- [ ] Workflow validates without errors
- [ ] Backup created with timestamp
- [ ] V8_CHANGELOG.md updated with Phase 3 completion

---

## Expected Workflow State After Phase 3

**Modified Nodes:** 0 (from Phase 3 only)
**Added Nodes:** 2
**Total Nodes:** 20 (was 18, now 20)

**Data Flow:**
```
code-1 → http-openai-1 → code-2 → http-openai-2 → code-tier2-parse → sheets-1
(Tier 1)                  (Tier 1  (Tier 2)         (Tier 2 parse)
                           parse +
                           Tier 2
                           builder)
```

**New Fields Available After code-tier2-parse:**
- `documentType` (e.g., "01_Projektbeschreibung")
- `tier2Confidence` (0-100)
- `combinedConfidence` ((tier1 + tier2) / 2)
- `germanName` (e.g., "Projektbeschreibung")
- `englishName` (e.g., "Exposé/Project Description")
- `isCoreType` (true/false)
- `tier2Reasoning` (explanation)
- `lowConfidence` (true if either tier < threshold)
- `confidenceFailureStage` ('tier1', 'tier2', or 'tier2_parse_error')

---

## Next Phase Preview

**Phase 4 will add/modify:**
1. `code-action-mapper` node (NEW - determines CORE/SECONDARY/LOW_CONFIDENCE)
2. `drive-rename` node (NEW - adds confidence to filename)
3. `code-4` node (MODIFY - extended folder mapping for 38 types + 4 holding folders)
4. `code-8` node (MODIFY - conditional tracker updates)
5. `if-1` node (MODIFY - add skipTrackerUpdate routing)

**Phase 4 requires:**
- Phase 3 successfully completed
- Workflow validated
- Backup created

---

## Troubleshooting

### If http-openai-2 fails to add:
- Verify OpenAI credential exists and name matches
- Check URL is correct: `https://api.openai.com/v1/chat/completions`
- Verify body structure matches OpenAI API v1 format

### If code-tier2-parse fails to add:
- Check JavaScript syntax in source file
- Verify node name is unique
- Check position coordinates don't overlap existing nodes

### If connections fail:
- Verify node names match exactly (case-sensitive)
- Check sourceOutput is "main" (not "0" or other)
- Ensure target nodes exist before creating connections

### If validation fails:
- Review error message details
- Check if tier2Prompt field exists from code-2 output
- Verify all parameter paths are correct

---

## Testing After Phase 3

**Optional manual test (if Phase 4 not ready):**

1. Temporarily connect code-tier2-parse → sheets-1
2. Execute workflow with test document
3. Check execution log for:
   - Tier 1 category correctly identified
   - Tier 2 prompt dynamically built
   - Tier 2 API call succeeds
   - Tier 2 result correctly parsed
   - Combined confidence calculated
   - All fields passed through

**Expected output from code-tier2-parse:**
```json
{
  "tier1Category": "OBJEKTUNTERLAGEN",
  "tier1Confidence": 85,
  "tier1Reasoning": "...",
  "documentType": "01_Projektbeschreibung",
  "tier2Confidence": 92,
  "combinedConfidence": 89,
  "germanName": "Projektbeschreibung",
  "englishName": "Exposé/Project Description",
  "isCoreType": true,
  "tier2Reasoning": "...",
  "filename": "...",
  "clientEmail": "...",
  ...
}
```

---

## Files Reference

**Node Code:**
- `/node_updates/http-openai-2_config.json`
- `/node_updates/code-tier2-parse.js`

**Specification:**
- `V8_IMPLEMENTATION_SPEC.md` (lines 549-658)

**Backups:**
- `.backups/chunk_2.5_v8.0_AFTER_PHASE2_[timestamp].json` (input)
- `.backups/chunk_2.5_v8.0_AFTER_PHASE3_[timestamp].json` (to be created)

---

**Status:** Ready for implementation after Phase 2 completion
**Prepared by:** solution-builder-agent
**Date:** 2026-01-12 22:25 CET
