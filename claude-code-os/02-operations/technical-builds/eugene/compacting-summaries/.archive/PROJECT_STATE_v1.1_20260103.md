# Eugene Email Compacting Summaries - Project State

**Last Updated:** January 3, 2026 23:00 CET
**Status:** 🔴 CRITICAL ISSUES FOUND - Binary Data Handling + Deprecated Syntax

---

## Current To-Do List

### ✅ Completed

1. **Pre-Chunk 0: Binary data handling fix applied**
   - Fixed "Filter PDF/ZIP Attachments" node to read from `item.binary` instead of `item.json.attachments`
   - **VERIFIED:** Filter now outputs 2 items (was 0 before fix)
   - **VERIFIED:** PDFs successfully extracted from Gmail binary data
   - Workflow progressed from node 2 → node 4 (was stuck at node 2)

2. **Pre-Chunk 0: Binary data fix validated with test-runner-agent**
   - Test execution #121 confirmed binary data extraction works
   - 2 PDFs processed from single email
   - Binary data correctly passed to downstream nodes
   - Test report: `pre-chunk-0_post-fix-validation_20260103.md`

### 🔴 Critical Blockers

1. **Pre-Chunk 0: Deprecated n8n v1.x syntax blocking workflow (5 nodes affected)**
   - Node 5: "Evaluate Extraction Quality" - uses `$input.item(0)` ❌
   - Node 7: "Normalize Client Name" - uses `$input.item(0)` ❌
   - Node 8: "Check Client Exists" - uses `$('Node').item` ❌
   - Node 11: "Handle Unidentified Client" - uses `$input.item(0)` ❌
   - Node 12: "Prepare for Chunk 3" - uses `$input.item(0)` ❌
   - **IMPACT:** Workflow stops at node 5 with error: `$input.item is not a function`
   - **FIX PROVIDED:** All 5 code snippets ready for manual application

2. **Chunk 1: Email to Staging has SAME binary data bug**
   - Node 2: "Normalize Email Data" - checks `email.attachments` (doesn't exist) ❌
   - Node 4: "Extract Attachments" - iterates over `emailData.attachments` (doesn't exist) ❌
   - **IMPACT:** `hasAttachments` always FALSE → workflow stops at "IF Has Attachments" node
   - **STATUS:** No documents ever get processed in Chunk 1
   - **FIX DESIGNED:** Not yet applied (waiting for Pre-Chunk 0 validation)

### ⏳ Pending

1. **Apply all 5 deprecated syntax fixes to Pre-Chunk 0**
   - Sway will manually update nodes 5, 7, 8, 11, 12
   - Re-test with test-runner-agent to confirm end-to-end flow

2. **Apply binary data fixes to Chunk 1**
   - Fix "Normalize Email Data" node
   - Fix "Extract Attachments" node
   - Test with real email

3. **Scan remaining workflows for similar issues**
   - Chunk 2: Text Extraction
   - Chunk 3: AI Classification
   - Any other Gmail-triggered workflows

---

## Key Decisions Made

### 1. Binary Data Handling Pattern (Session 3 - Jan 3, 2026)

**Decision:** Gmail Trigger stores attachments in `item.binary`, NOT `item.json.attachments`

**Correct pattern:**
```javascript
// ✅ CORRECT - Read from binary
const inputItem = $input.first();
const binary = inputItem.binary || {};

for (const [key, attachment] of Object.entries(binary)) {
  const filename = attachment.fileName;  // Note: fileName not filename
  const size = attachment.fileSize;      // Note: fileSize not size
  const mimeType = attachment.mimeType;
  // ...
}
```

**Incorrect pattern:**
```javascript
// ❌ WRONG - This doesn't exist in Gmail Trigger
const attachments = email.attachments;
for (const att of attachments) { ... }
```

**Rationale:** Gmail Trigger node downloads attachments as binary data with keys like `attachment_0`, `attachment_1`. The `json.attachments` array doesn't exist.

**Impact:** This issue affects:
- Pre-Chunk 0: Filter PDF/ZIP node (FIXED)
- Chunk 1: Normalize Email + Extract Attachments nodes (NOT YET FIXED)

---

### 2. n8n v2.x Syntax Migration (Session 3 - Jan 3, 2026)

**Decision:** Replace deprecated `$input.item(0)` with `$input.all()` for v2.x compatibility

**Correct pattern:**
```javascript
// ✅ CORRECT - n8n v2.x
const items = $input.all();
for (const item of items) {
  // Process each item
  results.push({ json: {...}, binary: item.binary });
}
return results;
```

**Incorrect pattern:**
```javascript
// ❌ DEPRECATED - n8n v1.x only
const item = $input.item(0);
return [{ json: {...} }];
```

**Rationale:** n8n v2.x deprecated the `.item()` accessor. Using `$input.all()` also handles multiple items correctly (e.g., 2 PDFs from one email).

**Impact:** Pre-Chunk 0 has 5 nodes using deprecated syntax - workflow stops at node 5 until fixed.

---

### 3. Binary Data Pass-Through (Session 3 - Jan 3, 2026)

**Decision:** Always preserve `binary` property when transforming items in code nodes

**Pattern:**
```javascript
results.push({
  json: {
    // ... transformed JSON data
  },
  binary: item.binary  // ✅ Pass through binary data
});
```

**Rationale:** Downstream nodes (Extract Text from PDF, etc.) need access to the binary attachment data. If you only return `json`, binary data is lost.

---

## Important IDs / Paths / Workflow Names

### n8n Workflows

| Workflow Name | ID | Purpose | Status |
|--------------|-----|---------|--------|
| V4 Pre-Chunk 0: Intake & Client Identification | `70n97A6OmYCsHMmV` | Gmail → PDF filter → Client extraction | 🔴 Blocked at node 5 (deprecated syntax) |
| Chunk 1: Email to Staging | `djsBWsrAEKbj2omB` | Email attachments → Google Drive staging | 🔴 Binary data bug (never processes docs) |
| Chunk 0: Folder Initialization | `zbxHkXOoD1qaz6OS` | Create client folder structure | ✅ Working (production-ready) |
| Test Orchestrator | `K1kYeyvokVHtOhoE` | Automated test runner | ✅ All 5 tests passing |

### Google Sheets

| Spreadsheet Name | ID | Purpose |
|-----------------|-----|---------|
| Client_Registry | `1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI` | Master client data registry |
| Test Results | `1af9ZsSm5IDVWIYb5IMX8ys8a5SUUnQcb77xi9tJQVo8` | Automated test outcomes tracking |

### Google Drive

| Folder Name | ID | Purpose |
|-------------|-----|---------|
| Client Root (Parent) | `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm` | Container for all client folder structures |

### File Paths

| File | Location | Purpose |
|------|----------|---------|
| Pre-Chunk 0 Test Report | `test-reports/pre-chunk-0_test-report_20260103.md` | Initial test analysis (found binary bug) |
| Pre-Chunk 0 Fix Report | `fix-reports/pre-chunk-0_attachment-filter-fix_20260103.md` | Binary data fix implementation |
| Pre-Chunk 0 Validation | `test-reports/pre-chunk-0_post-fix-validation_20260103.md` | Test results after binary fix (found syntax bug) |
| Project State (this doc) | `PROJECT_STATE_v1.1_20260103.md` | Current document |

---

## Technical Architecture

### Pre-Chunk 0 Workflow Flow

```
Gmail Trigger (receives email with PDFs)
  ↓ (outputs item with binary.attachment_0, binary.attachment_1)
Filter PDF/ZIP Attachments (node 2) ✅ FIXED
  ↓ (extracts PDFs from binary, outputs 2 items)
Download Attachment (node 3) [DISABLED - not needed]
  ↓
Extract Text from PDF (node 4) ✅ WORKING
  ↓ (2 items with extracted text)
Evaluate Extraction Quality (node 5) 🔴 BLOCKED - deprecated syntax
  ↓ [STOPS HERE - needs $input.all() fix]
AI Extract Client Name (node 6)
  ↓
Normalize Client Name (node 7) 🔴 Deprecated syntax
  ↓
Lookup Client Registry (node 8)
  ↓
Check Client Exists (node 9) 🔴 Deprecated syntax
  ↓
Decision Gate (node 10)
  ├→ Execute Chunk 0 (create folders)
  ├→ Prepare for Chunk 3 (existing client) 🔴 Deprecated syntax
  └→ Handle Unidentified Client (error) 🔴 Deprecated syntax
```

### Chunk 1 Workflow Flow

```
Gmail Trigger (receives email)
  ↓ (outputs item with binary.attachment_0, binary.attachment_1)
Normalize Email Data (node 2) 🔴 BROKEN
  ↓ (checks email.attachments - DOESN'T EXIST)
  ↓ (sets hasAttachments: false - ALWAYS FALSE)
IF Has Attachments (node 3) 🔴 BLOCKS HERE
  ↓ [STOPS - condition always fails]
Extract Attachments (node 4) 🔴 BROKEN (never reached)
  ...
```

---

## Known Issues & Fixes

### Issue #1: Pre-Chunk 0 Binary Data Handling ✅ FIXED

**Problem:** "Filter PDF/ZIP Attachments" tried to read `item.json.attachments` which doesn't exist in Gmail Trigger output.

**Status:** ✅ Fixed on Jan 3, 2026
**Verification:** Test execution #121 - Filter outputs 2 items (was 0 before)
**Fix Report:** `fix-reports/pre-chunk-0_attachment-filter-fix_20260103.md`

---

### Issue #2: Pre-Chunk 0 Deprecated n8n Syntax 🔴 BLOCKING

**Problem:** 5 nodes use `$input.item(0)` which is deprecated in n8n v2.x

**Affected Nodes:**
1. Node 5: "Evaluate Extraction Quality"
2. Node 7: "Normalize Client Name"
3. Node 8: "Check Client Exists" (uses `$('Node').item`)
4. Node 11: "Handle Unidentified Client"
5. Node 12: "Prepare for Chunk 3"

**Current Impact:**
- Workflow stops at node 5 with error: `$input.item is not a function`
- Cannot test client name extraction
- Cannot validate end-to-end flow

**Fix Status:** Code provided to Sway for manual application
**Test Plan:** Re-run test-runner-agent after all 5 nodes updated

---

### Issue #3: Chunk 1 Binary Data Handling 🔴 CRITICAL

**Problem:** Same binary data issue as Pre-Chunk 0, but affects TWO nodes

**Node 2: "Normalize Email Data"**
```javascript
// ❌ WRONG
const email = $input.first().json;
const hasAttachments = email.attachments?.length > 0 || false;  // Always FALSE
const attachments = email.attachments || [];  // Always []
```

**Node 4: "Extract Attachments"**
```javascript
// ❌ WRONG
const attachments = emailData.attachments;  // Doesn't exist
for (let i = 0; i < attachments.length; i++) { ... }  // Never runs
```

**Current Impact:**
- Workflow NEVER processes any emails with attachments
- `hasAttachments` always evaluates to FALSE
- "IF Has Attachments" condition fails immediately
- No documents reach staging folder

**Fix Status:** Designed but not yet applied
**Waiting For:** Pre-Chunk 0 validation to confirm pattern works

---

## Test Results Summary

### Pre-Chunk 0 Post-Fix Validation (Execution #121)

| Node # | Node Name | Status | Output Items | Notes |
|--------|-----------|--------|--------------|-------|
| 1 | Gmail Trigger | ✅ | 1 item | Email with 2 PDFs |
| 2 | Filter PDF/ZIP | ✅ | 2 items | Binary fix WORKING |
| 3 | Download Attachment | ⏭️ | (disabled) | Not needed |
| 4 | Extract Text from PDF | ✅ | 2 items | Both PDFs processed |
| 5 | Evaluate Extraction Quality | ❌ | Error | `$input.item is not a function` |

**Progress:** 31% complete (4/13 nodes executed)
**Improvement:** +16% from before binary fix (was 15%)
**Next Blocker:** Node 5 deprecated syntax

---

## Next Steps (Priority Order)

### Immediate (Today)

1. **Apply 5 syntax fixes to Pre-Chunk 0** (Sway manual task)
   - Update nodes 5, 7, 8, 11, 12 with provided code
   - Save workflow

2. **Re-test Pre-Chunk 0 end-to-end**
   - Run test-runner-agent with execution #28 pinned data
   - Verify workflow reaches final nodes
   - Confirm client name extraction works

### High Priority (Next Session)

3. **Fix Chunk 1 binary data handling**
   - Update "Normalize Email Data" node
   - Update "Extract Attachments" node
   - Test with real email

4. **Scan all workflows for similar patterns**
   - Check Chunk 2, Chunk 3 for deprecated syntax
   - Check for other Gmail-triggered workflows
   - Create comprehensive pattern guide

### Medium Priority

5. **Create binary data handling documentation**
   - Patterns to use vs patterns to avoid
   - Gmail Trigger specific gotchas
   - n8n v2.x migration guide

---

## Pattern Guide: Binary Data + Modern n8n Syntax

### ✅ Correct: Reading Gmail Attachments

```javascript
// Get input with binary data
const inputItem = $input.first();
const email = inputItem.json;
const binary = inputItem.binary || {};

// Count attachments
const attachmentKeys = Object.keys(binary);
const attachmentCount = attachmentKeys.length;

// Check if has attachments
const hasAttachments = attachmentCount > 0;

// Iterate over attachments
for (const [key, attachment] of Object.entries(binary)) {
  const filename = attachment.fileName;    // ✅ fileName (camelCase)
  const size = attachment.fileSize;        // ✅ fileSize (not size)
  const mimeType = attachment.mimeType;
  // ...
}
```

### ❌ Incorrect: Assuming JSON Attachments

```javascript
// ❌ This doesn't exist in Gmail Trigger
const attachments = email.attachments;
const hasAttachments = attachments?.length > 0;
```

### ✅ Correct: Processing Multiple Items (n8n v2.x)

```javascript
const items = $input.all();
const results = [];

for (const item of items) {
  results.push({
    json: {
      // ... transformed data
    },
    binary: item.binary  // ✅ Pass through binary
  });
}

return results;
```

### ❌ Incorrect: Using Deprecated Syntax (n8n v1.x)

```javascript
// ❌ Deprecated - will error in v2.x
const item = $input.item(0);
const otherNodeData = $('Other Node').item.json;
```

---

## References

### Test Reports

- Pre-Chunk 0 initial test: `test-reports/pre-chunk-0_test-report_20260103.md`
- Pre-Chunk 0 fix implementation: `fix-reports/pre-chunk-0_attachment-filter-fix_20260103.md`
- Pre-Chunk 0 post-fix validation: `test-reports/pre-chunk-0_post-fix-validation_20260103.md`

### MCP Tools Used

- `mcp__n8n-mcp__n8n_get_workflow` - Retrieve workflow structure
- `mcp__n8n-mcp__n8n_update_partial_workflow` - Apply targeted fixes
- `mcp__n8n-mcp__n8n_test_workflow` - Execute test scenarios
- `mcp__n8n-mcp__n8n_executions` - Retrieve execution details

### Key Learnings

1. **Gmail Trigger stores attachments in `binary` not `json`**
   - Field names: `fileName`, `fileSize`, `mimeType` (not `filename`, `size`)
   - Keys: `attachment_0`, `attachment_1`, etc.

2. **n8n v2.x deprecated `.item()` accessor**
   - Use `$input.all()` instead of `$input.item(0)`
   - Use `$('Node Name').first()` instead of `$('Node Name').item`

3. **Always pass through `binary` property in code nodes**
   - Downstream nodes need binary data for file processing
   - Include `binary: item.binary` in output items

4. **Test with real data early**
   - Pinned test data reveals data structure mismatches
   - Don't assume field names - verify with actual execution

---

**Document Version:** 1.1
**Generated:** January 3, 2026 23:00 CET
**Author:** Claude Code (Sway's automation assistant)
**Previous Version:** PROJECT_STATE_v1.0_20260103.md (client onboarding system - different project)
