# Phase 4 Implementation Guide
## Action Mapping, File Rename, and Routing

**Date:** 2026-01-12 22:30 CET
**Workflow:** Chunk 2.5 (ID: okg8wTqLtPUwjQ18)
**Phase:** 4 of 4 (Action Mapping and Final Routing)

---

## Prerequisites

✅ Phase 3 completed successfully
✅ Workflow validated after Phase 3
✅ Backup exists: `.backups/chunk_2.5_v8.0_AFTER_PHASE3_[timestamp].json`
✅ Tier 2 classification working (code-tier2-parse outputs all required fields)

---

## Overview

Phase 4 completes the V8 implementation by:
1. Adding action mapper (CORE/SECONDARY/LOW_CONFIDENCE routing)
2. Adding file rename (confidence score in filename)
3. Extending folder mapping (38 types + 4 holding folders)
4. Making tracker updates conditional (CORE only)
5. Updating routing logic (skip tracker for SECONDARY)

**Total changes:** 2 new nodes + 3 modified nodes

---

## Implementation Steps

### Step 1: Add code-action-mapper Node

**Node Name:** `Determine Action Type`
**Node Type:** Code (JavaScript)
**Position:** [1712, 320] (after code-tier2-parse)

**Source File:** `/node_updates/code-action-mapper.js`

**MCP Operation:**
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow(
  workflowId: "okg8wTqLtPUwjQ18",
  operations: [{
    op: "addNode",
    node: {
      name: "Determine Action Type",
      type: "n8n-nodes-base.code",
      position: [1712, 320],
      parameters: {
        jsCode: `// [INSERT CONTENT OF code-action-mapper.js HERE]`
      }
    }
  }]
)
```

**Connection:**
```javascript
{
  source: "Parse Tier 2 Result",
  target: "Determine Action Type",
  sourceOutput: "main"
}
```

**Purpose:**
- Checks `lowConfidence` flag → "LOW_CONFIDENCE" action
- Checks `isCoreType === true` → "CORE" action
- Otherwise → "SECONDARY" action
- Sets `trackerUpdate` flag (true only for CORE)
- Sets `sendNotification` flag (true only for LOW_CONFIDENCE)

---

### Step 2: Add drive-rename Node

**Node Name:** `Rename File with Confidence`
**Node Type:** Google Drive (Update a File operation)
**Position:** [1936, 320] (after code-action-mapper)

**Expression File:** `/node_updates/drive-rename_expression.txt`

**MCP Operation:**
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow(
  workflowId: "okg8wTqLtPUwjQ18",
  operations: [{
    op: "addNode",
    node: {
      name: "Rename File with Confidence",
      type: "n8n-nodes-base.googleDrive",
      position: [1936, 320],
      parameters: {
        operation: "update",
        fileId: "={{ $json.fileId }}",
        updateFields: {
          name: `// [INSERT CONTENT OF drive-rename_expression.txt HERE]`
        }
      },
      credentials: {
        googleDriveOAuth2Api: {
          id: "[USE EXISTING Google Drive credential ID]",
          name: "Google Drive (Sway)"
        }
      }
    }
  }]
)
```

**Connection:**
```javascript
{
  source: "Determine Action Type",
  target: "Rename File with Confidence",
  sourceOutput: "main"
}
```

**Purpose:**
- Renames file to: `{typeCode}_{clientName}_{confidence}pct.{ext}`
- Example: `CORE_expose_villa_martens_89pct.pdf`
- Maps all 38 document types to English snake_case codes
- Includes confidence percentage in filename

---

### Step 3: Modify code-4 Node (Extended Folder Mapping)

**Node Name:** `Get Destination Folder ID` (EXISTING)
**Source File:** `/node_updates/code-4_extended_folder_mapping.js`

**MCP Operation:**
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow(
  workflowId: "okg8wTqLtPUwjQ18",
  operations: [{
    op: "updateNode",
    nodeName: "Get Destination Folder ID",
    updates: {
      parameters: {
        jsCode: `// [INSERT CONTENT OF code-4_extended_folder_mapping.js HERE]`
      }
    }
  }]
)
```

**Changes:**
- OLD: Mapped 4 CORE types only to specific folders
- NEW: Maps 4 CORE types + 34 SECONDARY types + LOW_CONFIDENCE
  - CORE → 4 specific folders (01_Expose, 02_Grundbuch, 03_Calculation, 04_Exit_Strategy)
  - SECONDARY → 4 holding folders based on Tier 1 category:
    - OBJEKTUNTERLAGEN → _Holding_Property
    - WIRTSCHAFTLICHE_UNTERLAGEN → _Holding_Financial
    - RECHTLICHE_UNTERLAGEN → _Holding_Legal
    - SONSTIGES → _Holding_Misc
  - LOW_CONFIDENCE → 38_Unknowns

**Folder IDs Required in AMA_Folder_IDs Sheet:**
- FOLDER_01_Expose (existing)
- FOLDER_02_Grundbuch (existing)
- FOLDER_03_Calculation (existing)
- FOLDER_04_Exit_Strategy (existing)
- FOLDER_38_Unknowns (existing)
- FOLDER_HOLDING_PROPERTY (NEW - must exist)
- FOLDER_HOLDING_FINANCIAL (NEW - must exist)
- FOLDER_HOLDING_LEGAL (NEW - must exist)
- FOLDER_HOLDING_MISC (NEW - must exist)

---

### Step 4: Modify code-8 Node (Conditional Tracker Update)

**Node Name:** `Prepare Tracker Update Data` (EXISTING)
**Source File:** `/node_updates/code-8_conditional_tracker.js`

**MCP Operation:**
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow(
  workflowId: "okg8wTqLtPUwjQ18",
  operations: [{
    op: "updateNode",
    nodeName: "Prepare Tracker Update Data",
    updates: {
      parameters: {
        jsCode: `// [INSERT CONTENT OF code-8_conditional_tracker.js HERE]`
      }
    }
  }]
)
```

**Changes:**
- OLD: Always prepared tracker update data
- NEW: Checks `trackerUpdate` flag first
  - If `trackerUpdate !== true` → Returns `skipTrackerUpdate: true` and skips all tracker logic
  - If `trackerUpdate === true` → Prepares tracker data as before (CORE types only)

**Purpose:**
- CORE documents: Prepare tracker update (Status_Expose, Status_Grundbuch, etc.)
- SECONDARY + LOW_CONFIDENCE: Skip tracker entirely, go straight to folder move

---

### Step 5: Modify if-1 Node (Add Skip Tracker Condition)

**Node Name:** `Check Status` (EXISTING)
**Configuration File:** `/node_updates/if-1_conditions.json`

**MCP Operation:**
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow(
  workflowId: "okg8wTqLtPUwjQ18",
  operations: [{
    op: "updateNode",
    nodeName: "Check Status",
    updates: {
      parameters: {
        conditions: {
          options: {
            conditions: [
              {
                id: "condition-1",
                name: "Update Tracker (CORE types)",
                leftValue: "={{ $json.skipTrackerUpdate }}",
                operation: "equal",
                rightValue: false,
                outputKey: "update_tracker"
              },
              {
                id: "condition-2",
                name: "Skip Tracker (SECONDARY + LOW_CONFIDENCE)",
                leftValue: "={{ $json.skipTrackerUpdate }}",
                operation: "equal",
                rightValue: true,
                outputKey: "skip_tracker"
              },
              {
                id: "condition-3",
                name: "Client Not Found",
                leftValue: "={{ $json.clientFound }}",
                operation: "equal",
                rightValue: false,
                outputKey: "error"
              }
            ]
          }
        }
      }
    }
  }]
)
```

**New Routing:**
- Condition 1 (skipTrackerUpdate === false): → code-8 → sheets-2 → sheets-3 → code-4 → drive-1 → code-5
- Condition 2 (skipTrackerUpdate === true): → sheets-3 → code-4 → drive-1 → code-5 (SKIPS sheets-2)
- Condition 3 (clientFound === false): → sheets-4 → error flow (UNCHANGED)

---

### Step 6: Update Connections

**Connect new nodes to existing flow:**

1. **code-tier2-parse → code-action-mapper** (NEW)
2. **code-action-mapper → drive-rename** (NEW)
3. **drive-rename → sheets-1** (replaces old code-2 → sheets-1)

**Disconnect old connection:**
- OLD: code-2 → sheets-1
- NEW: code-2 → http-openai-2 (already done in Phase 3)

**Final connection from drive-rename:**
```javascript
{
  source: "Rename File with Confidence",
  target: "Lookup Client in Client_Tracker",
  sourceOutput: "main"
}
```

---

### Step 7: Validate Workflow

```javascript
mcp__n8n-mcp__n8n_validate_workflow(
  workflowId: "okg8wTqLtPUwjQ18"
)
```

**Expected validation results:**
- ✅ All nodes connected properly
- ✅ No orphaned nodes
- ✅ All JavaScript syntax valid
- ✅ All Google Drive operations configured
- ✅ Routing logic correctly split (CORE vs SECONDARY vs ERROR)

---

### Step 8: Create Final Backup

**Export and save:**

```bash
Filename: .backups/chunk_2.5_v8.0_AFTER_PHASE4_20260112_[HH:MM].json
```

This is the FINAL V8 implementation backup.

---

## Verification Checklist

After completing Phase 4:

- [ ] code-action-mapper added successfully
- [ ] drive-rename added successfully
- [ ] code-4 modified (extended folder mapping)
- [ ] code-8 modified (conditional tracker)
- [ ] if-1 modified (skip tracker condition)
- [ ] All connections established correctly
- [ ] Workflow validates without errors
- [ ] Final backup created with timestamp
- [ ] V8_CHANGELOG.md updated with Phase 4 completion

---

## Expected Final Workflow State

**Modified Nodes (Phase 4):** 3 (code-4, code-8, if-1)
**Added Nodes (Phase 4):** 2 (code-action-mapper, drive-rename)
**Total Added Nodes (All Phases):** 5 (http-openai-2, code-tier2-parse, code-action-mapper, drive-rename, + routing)
**Total Modified Nodes (All Phases):** 4 (code-1, code-2, code-4, code-8, if-1)
**Final Node Count:** 23 nodes (was 18, now 23)

**Complete Data Flow:**
```
trigger-1
  → code-1 (Tier 1 prompt builder)
  → http-openai-1 (Tier 1 GPT-4 call)
  → code-2 (Tier 1 parse + Tier 2 prompt builder)
  → http-openai-2 (Tier 2 GPT-4 call) ← NEW
  → code-tier2-parse (Tier 2 parse) ← NEW
  → code-action-mapper (Determine CORE/SECONDARY/LOW_CONFIDENCE) ← NEW
  → drive-rename (Add confidence to filename) ← NEW
  → sheets-1 (Lookup Client in Client_Tracker)
  → code-3 (Find Client Row and Validate)
  → if-1 (Check Status - MODIFIED with skipTrackerUpdate)
    ├─ [CORE: skipTrackerUpdate === false]
    │   → code-8 (Prepare Tracker Update - MODIFIED conditional)
    │   → sheets-2 (Update Client_Tracker Row)
    │   → sheets-3 (Lookup Client in AMA_Folder_IDs)
    │   → code-4 (Get Destination Folder ID - MODIFIED extended mapping)
    │   → drive-1 (Move File to Final Location)
    │   → code-5 (Prepare Success Output)
    │
    ├─ [SECONDARY: skipTrackerUpdate === true]
    │   → sheets-3 (Lookup Client in AMA_Folder_IDs) ← SKIPS sheets-2
    │   → code-4 (Get Destination Folder ID - MODIFIED extended mapping)
    │   → drive-1 (Move File to Final Location)
    │   → code-5 (Prepare Success Output)
    │
    └─ [ERROR: clientFound === false]
        → sheets-4 (Lookup 38_Unknowns Folder)
        → code-6 (Get 38_Unknowns Folder ID)
        → drive-2 (Move File to 38_Unknowns)
        → code-7 (Prepare Error Email Body)
        → gmail-1 (Send Error Notification Email)
```

---

## Complete Feature Set After V8

### 2-Tier Classification
✅ **Tier 1:** 4 broad categories (OBJEKTUNTERLAGEN, WIRTSCHAFTLICHE, RECHTLICHE, SONSTIGES)
✅ **Tier 2:** 38 specific document types (4 CORE + 34 SECONDARY)

### Confidence Scoring
✅ **Tier 1 threshold:** >= 60%
✅ **Tier 2 threshold:** >= 70%
✅ **Combined confidence:** (Tier 1 + Tier 2) / 2
✅ **Confidence in filename:** `type_client_89pct.pdf`

### Smart Routing
✅ **CORE types (4):** Specific folder + tracker update
✅ **SECONDARY types (34):** Holding folder (by category) + no tracker
✅ **LOW_CONFIDENCE:** 38_Unknowns folder + email notification

### Folder Organization
✅ **4 CORE folders:** 01_Expose, 02_Grundbuch, 03_Calculation, 04_Exit_Strategy
✅ **4 Holding folders:** _Holding_Property, _Holding_Financial, _Holding_Legal, _Holding_Misc
✅ **1 Unknown folder:** 38_Unknowns

### Tracker Updates
✅ **Conditional updates:** Only for CORE types
✅ **4 tracker columns:** Status_Expose, Status_Grundbuch, Status_Calculation, Status_Exit_Strategy
✅ **Skip for SECONDARY:** No unnecessary tracker writes

---

## Testing After Phase 4

**Recommended test scenarios:**

### Test 1: CORE Document (e.g., Projektbeschreibung)
**Expected:**
- Tier 1: OBJEKTUNTERLAGEN (>= 60% confidence)
- Tier 2: 01_Projektbeschreibung (>= 70% confidence)
- Action: CORE
- File rename: `CORE_expose_client_XXpct.pdf`
- Destination: 01_Expose folder
- Tracker: Status_Expose = ✓

### Test 2: SECONDARY Document (e.g., Kaufvertrag)
**Expected:**
- Tier 1: OBJEKTUNTERLAGEN (>= 60% confidence)
- Tier 2: 02_Kaufvertrag (>= 70% confidence)
- Action: SECONDARY
- File rename: `purchase_agreement_client_XXpct.pdf`
- Destination: _Holding_Property folder
- Tracker: NO UPDATE (skipTrackerUpdate = true)

### Test 3: LOW_CONFIDENCE Document
**Expected:**
- Tier 1 OR Tier 2 confidence < threshold
- Action: LOW_CONFIDENCE
- File rename: `REVIEW_unknown_client_XXpct.pdf`
- Destination: 38_Unknowns folder
- Tracker: NO UPDATE
- Email: Notification sent

### Test 4: All 4 Categories
- OBJEKTUNTERLAGEN → _Holding_Property
- WIRTSCHAFTLICHE_UNTERLAGEN → _Holding_Financial
- RECHTLICHE_UNTERLAGEN → _Holding_Legal
- SONSTIGES → _Holding_Misc

---

## Pre-Implementation Checklist

Before starting Phase 4, verify:

- [ ] **Phase 3 completed** and validated
- [ ] **Holding folders exist** in Google Drive:
  - _Holding_Property
  - _Holding_Financial
  - _Holding_Legal
  - _Holding_Misc
- [ ] **AMA_Folder_IDs sheet updated** with holding folder IDs:
  - FOLDER_HOLDING_PROPERTY
  - FOLDER_HOLDING_FINANCIAL
  - FOLDER_HOLDING_LEGAL
  - FOLDER_HOLDING_MISC
- [ ] **Google Drive credentials** exist and are named correctly
- [ ] **Backup created** after Phase 3

---

## Post-Implementation Checklist

After completing Phase 4:

- [ ] All 5 changes applied (2 add + 3 modify)
- [ ] Workflow validates successfully
- [ ] Final backup created
- [ ] V8_CHANGELOG.md updated
- [ ] Ready for test-runner-agent automated testing
- [ ] Ready for production deployment

---

## Files Reference

**Node Code:**
- `/node_updates/code-action-mapper.js`
- `/node_updates/drive-rename_expression.txt`
- `/node_updates/code-4_extended_folder_mapping.js`
- `/node_updates/code-8_conditional_tracker.js`
- `/node_updates/if-1_conditions.json`

**Specification:**
- `V8_IMPLEMENTATION_SPEC.md` (lines 670-995)

**Backups:**
- `.backups/chunk_2.5_v8.0_AFTER_PHASE3_[timestamp].json` (input)
- `.backups/chunk_2.5_v8.0_AFTER_PHASE4_[timestamp].json` (FINAL - to be created)

---

**Status:** Ready for implementation after Phase 3 completion
**Prepared by:** solution-builder-agent
**Date:** 2026-01-12 22:30 CET
