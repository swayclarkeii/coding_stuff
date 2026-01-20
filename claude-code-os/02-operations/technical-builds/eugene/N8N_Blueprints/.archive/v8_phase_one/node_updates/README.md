# V8 Implementation - Node Updates Directory

This directory contains all the code, configurations, and guides needed to implement V8 into the live Chunk 2.5 workflow.

---

## Quick Start

**If using main conversation with n8n MCP tools:**
1. Read `PHASE_2_IMPLEMENTATION_GUIDE.md` first
2. Execute Phase 2 MCP operations
3. Read `PHASE_3_IMPLEMENTATION_GUIDE.md`
4. Execute Phase 3 MCP operations
5. Read `PHASE_4_IMPLEMENTATION_GUIDE.md`
6. Execute Phase 4 MCP operations

**If using n8n UI manually:**
1. Open Chunk 2.5 workflow in n8n
2. For each node, copy code from corresponding `.js` file
3. Follow the guides for connections and validations

---

## File Index

### Phase 2 Files (Modify Existing Nodes)

**Nodes to modify:** 2
**Files:**
- `code-1_tier1_prompt.js` - Code for "Build AI Classification Prompt" node
- `code-2_tier1_parse_tier2_builder.js` - Code for "Parse Classification Result" node
- `PHASE_2_IMPLEMENTATION_GUIDE.md` - Step-by-step instructions

**What it does:**
- Tier 1: Classify into 4 broad categories (OBJEKTUNTERLAGEN, WIRTSCHAFTLICHE, RECHTLICHE, SONSTIGES)
- Build dynamic Tier 2 prompt based on Tier 1 result
- Add confidence threshold check (>= 60%)

---

### Phase 3 Files (Add New Nodes)

**Nodes to add:** 2
**Files:**
- `http-openai-2_config.json` - Configuration for "Tier 2 GPT-4 API Call" node (HTTP Request)
- `code-tier2-parse.js` - Code for "Parse Tier 2 Result" node
- `PHASE_3_IMPLEMENTATION_GUIDE.md` - Step-by-step instructions

**What it does:**
- Tier 2: Classify into specific document type (38 types total)
- Parse Tier 2 GPT-4 response
- Validate Tier 2 confidence (>= 70%)
- Calculate combined confidence ((Tier 1 + Tier 2) / 2)

**Connections:**
- code-2 → http-openai-2 → code-tier2-parse → [continue to Phase 4 nodes]

---

### Phase 4 Files (Action Mapping + Routing)

**Nodes to add:** 2
**Nodes to modify:** 3
**Files:**
- `code-action-mapper.js` - Code for "Determine Action Type" node (NEW)
- `drive-rename_expression.txt` - Expression for "Rename File with Confidence" node (NEW - Google Drive)
- `code-4_extended_folder_mapping.js` - Code for "Get Destination Folder ID" node (MODIFY)
- `code-8_conditional_tracker.js` - Code for "Prepare Tracker Update Data" node (MODIFY)
- `if-1_conditions.json` - Configuration for "Check Status" node (MODIFY)
- `PHASE_4_IMPLEMENTATION_GUIDE.md` - Step-by-step instructions

**What it does:**
- Determine routing: CORE (4 types) / SECONDARY (34 types) / LOW_CONFIDENCE
- Rename file to include confidence score: `type_client_89pct.pdf`
- Map 38 document types to correct folders:
  - CORE → 4 specific folders + tracker update
  - SECONDARY → 4 holding folders + NO tracker
  - LOW_CONFIDENCE → 38_Unknowns + email
- Add skipTrackerUpdate routing (SECONDARY bypasses tracker)

---

## Implementation Guides

### PHASE_2_IMPLEMENTATION_GUIDE.md
**Purpose:** Modify code-1 and code-2 nodes (Tier 1 classification)
**Contains:**
- MCP commands for both modifications
- Expected changes summary
- Validation checklist
- Backup instructions

### PHASE_3_IMPLEMENTATION_GUIDE.md
**Purpose:** Add http-openai-2 and code-tier2-parse nodes (Tier 2 classification)
**Contains:**
- MCP commands for adding nodes
- Connection instructions
- Validation checklist
- Backup instructions

### PHASE_4_IMPLEMENTATION_GUIDE.md
**Purpose:** Add action mapper, file rename, and modify routing
**Contains:**
- MCP commands for 5 changes (2 add + 3 modify)
- Complete routing logic
- Validation checklist
- Final backup instructions
- Testing scenarios

---

## Additional Documentation

### IMPLEMENTATION_STATUS.md
**Purpose:** Explains why solution-builder-agent couldn't execute directly
**Contains:**
- Blocker identified (sub-agent MCP access)
- What was prepared vs what remains
- Options for completing implementation

---

## Code Quality

All code files have been:
- ✅ Extracted from V8_IMPLEMENTATION_SPEC.md
- ✅ JavaScript syntax validated
- ✅ Logic verified against specification
- ✅ Ready for direct copy-paste (no editing needed)

---

## Node Mapping Reference

| File | Node Name | Type | Change |
|------|-----------|------|--------|
| `code-1_tier1_prompt.js` | Build AI Classification Prompt | Code | MODIFY |
| `code-2_tier1_parse_tier2_builder.js` | Parse Classification Result | Code | MODIFY |
| `http-openai-2_config.json` | Tier 2 GPT-4 API Call | HTTP Request | ADD |
| `code-tier2-parse.js` | Parse Tier 2 Result | Code | ADD |
| `code-action-mapper.js` | Determine Action Type | Code | ADD |
| `drive-rename_expression.txt` | Rename File with Confidence | Google Drive | ADD |
| `code-4_extended_folder_mapping.js` | Get Destination Folder ID | Code | MODIFY |
| `code-8_conditional_tracker.js` | Prepare Tracker Update Data | Code | MODIFY |
| `if-1_conditions.json` | Check Status | IF | MODIFY |

**Total changes:** 9 nodes (5 add + 4 modify)

---

## Safety Protocol

**Before starting:**
- ✅ Backup exists: `.backups/chunk_2.5_v8.0_BEFORE_PHASE2_20260112.json`

**After each phase:**
- Create backup: `.backups/chunk_2.5_v8.0_AFTER_PHASE[N]_[timestamp].json`
- Validate workflow: `mcp__n8n-mcp__n8n_validate_workflow`

**Rollback if needed:**
- All backups available in `.backups/` folder
- Can restore to any phase checkpoint

---

## Estimated Implementation Time

**Using n8n MCP tools:**
- Phase 2: 15-20 minutes
- Phase 3: 20-25 minutes
- Phase 4: 30-40 minutes
- **Total: 65-85 minutes**

**Using n8n UI manually:**
- Phase 2: 30-40 minutes
- Phase 3: 40-50 minutes
- Phase 4: 60-80 minutes
- **Total: 130-170 minutes (2-3 hours)**

---

## Testing After Implementation

**Use test-runner-agent or manual testing:**

1. **CORE document** (e.g., filename with "Projektbeschreibung")
   - Expected: 01_Expose folder + Status_Expose = ✓

2. **SECONDARY document** (e.g., filename with "Kaufvertrag")
   - Expected: _Holding_Property folder + NO tracker update

3. **LOW_CONFIDENCE document** (ambiguous filename)
   - Expected: 38_Unknowns folder + email notification

**Test scenarios included in Phase 4 guide.**

---

## Questions or Issues?

All guides include:
- Clear step-by-step instructions
- MCP command syntax examples
- Validation checklists
- Troubleshooting sections
- Expected results

**Start with:** `PHASE_2_IMPLEMENTATION_GUIDE.md`

---

**Created by:** solution-builder-agent
**Date:** 2026-01-12 22:40 CET
**Status:** Ready for implementation
