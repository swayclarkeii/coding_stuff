# Eugene Document Classification - Session Summary v12.0
**Date:** 2026-01-31
**Session:** Production fixes + verification batch
**Status:** Production-ready, 6/6 verification tests passed (100%)

---

## Current State

### Production Verification Results
- **Tests fired:** 6 (1 initial + 5 batch)
- **Successful:** 6 (100%)
- **Failed:** 0
- **Execution IDs:** #7362, #7374, #7379, #7383, #7386, #7388
- **Avg execution time:** ~4.4 minutes per test
- **Tracker confirmed:** villa_martens row has checkmarks across multiple document types

### Dokumenten_Tracker State
- `villa_martens`: Active, last updated 2026-01-30T19:31:44, checkmarks on 14 document types
- `wilhelmsmuehlenweg_3`: Row exists, no checkmarks yet

---

## Bugs Fixed This Session

### 1. WorkflowHasIssuesError (CRITICAL BLOCKER)
- **Error:** "The workflow has issues and cannot be executed for that reason"
- **Root cause:** n8n's runtime `checkForWorkflowIssues()` validates ALL nodes before execution, including resource locator format
- **Diagnosis:** SSH'd into server, patched n8n source to log the exact issues JSON
- **Actual issues found:**
  ```json
  {
    "Move File to 38_Unknowns": {"parameters": {"fileId": ["Parameter \"File\" is required."]}},
    "Move File to Final Location": {"parameters": {"fileId": ["Parameter \"File\" is required."]}}
  }
  ```
- **Root cause detail:** solution-builder-agent stripped fileId/folderId params when changing operation from copy to move

### 2. Drive Node fileId Format (3 nodes)
- **Nodes:** drive-1 (Move File to Final Location), drive-2 (Move File to 38_Unknowns), drive-download-1 (Download PDF)
- **Problem:** Plain string `"fileId": "={{ $json.fileId }}"` instead of resource locator format
- **Fix:** Changed all to `{"__rl": true, "value": "={{ $json.fileId }}", "mode": "id"}`

### 3. Drive Nodes Missing Parameters
- **Nodes:** drive-1, drive-2
- **Problem:** Only had `"operation": "move"` — no fileId or driveId at all
- **Fix:** Added `fileId` (resource locator) and `driveId` (resource locator with destination folder expression)

### 4. Code Node Multiple Returns (code-3)
- **Node:** Find Client Row and Validate
- **Problem:** Multiple early `return` statements + `.find()` callback with `return true/false` triggered "Cannot return primitive values" validator error
- **Fix:** Restructured to single `return [{ json: resultJson }]` at end, replaced `.find()` with `for` loop

### 5. Gmail Node Version Mismatch (gmail-1)
- **Node:** Send Error Notification Email
- **Problem:** typeVersion 2.1 (may not support emailFormat "html"), malformed credential ID
- **Fix:** Upgraded to typeVersion 2.2, changed credential to `{"id": "aYzk7sZF8ZVyfOan", "name": "Gmail account"}`

### 6. Disabled GPT-4 Nodes Invalid Credentials
- **Nodes:** Classify Document with GPT-4 (http-openai-1), Tier 2 GPT-4 API Call
- **Problem:** Used `openAiApi` credential type on httpRequest nodes (invalid combo), n8n validates even disabled nodes
- **Fix:** Changed authentication to "none", cleared credentials

### 7. IF Node Combinator (from previous session, confirmed fixed)
- **Node:** Check Dual Classification (if-dual-classification)
- **Fix:** combinator moved from inside `options` to root of `conditions` object

---

## Workflows Modified

### Chunk 2.5 - Client Document Tracking (okg8wTqLtPUwjQ18)
- **drive-1** (Move File to Final Location): Added fileId + driveId as resource locators
- **drive-2** (Move File to 38_Unknowns): Added fileId + driveId as resource locators
- **drive-download-1** (Download PDF for Classification): fileId converted to resource locator
- **code-3** (Find Client Row and Validate): Restructured to single return, for loop
- **gmail-1** (Send Error Notification Email): typeVersion 2.1→2.2, credential ID fixed
- **http-openai-1** (Classify Document with GPT-4): auth→none (disabled node)
- **3732e080** (Tier 2 GPT-4 API Call): auth→none (disabled node)
- **if-dual-classification** (Check Dual Classification): combinator fix confirmed
- **code-1** (Build AI Classification Prompt): field names fixed (from prev session)
- **gmail-dual-classification**: re-enabled, HTML formatting (from prev session)

### Eugene Quick Test Runner (fIqmtfEDuYM7gbE9)
- No changes this session (still points to Test_Results_Iterationt5 tab)

---

## Workflow JSON Backups

Saved to `/claude-code-os/02-operations/technical-builds/eugene/n8n-workflows/`:
- `chunk-2-5-production-2026-01-31.json` — Chunk 2.5 full export after all fixes

---

## Post-Testing TODO (for email test run)

1. **Clean Dokumenten_Tracker tab** — Clear all checkmarks and timestamps from test data
2. **Clean Google Drive folders** — Remove files that were moved during testing from client folders
3. **Run real email test** — Trigger Pre-Chunk 0 from actual email to verify full chain
4. **Note:** Test runner currently writes to `Test_Results_Iterationt5` — may want new tab for email tests
5. **Note:** Drive operations are now MOVE (production mode) — test files WILL be moved out of test folder

---

## Key Architecture Notes

- **Test folder:** `1GQcFD61eaWgHwXZGxfzY2h_-boyG6IHa` (161 files currently)
- **Results spreadsheet:** `12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I`
- **AMA_Folder_IDs sheet:** `1-CPnCr3locAORVX5tUEoh6r0i-x3tQ_ROTN0VXatOAU`
- **Webhook:** `https://n8n.oloxa.ai/webhook/eugene-quick-test`
- **n8n server:** 157.230.21.230 (SSH key: `.credentials/n8n-server-ssh.key`)
- **N8N_LOG_LEVEL:** info (debug removed)

---

## Key Learnings

### n8n Resource Locator Format
Google Drive v3 nodes require resource locator objects for fileId:
```json
{
  "__rl": true,
  "value": "={{ $json.fileId }}",
  "mode": "id"
}
```
Plain strings like `"={{ $json.fileId }}"` pass the MCP validator but fail n8n's runtime `checkForWorkflowIssues()`.

### n8n Validates Disabled Nodes
Disabled nodes with invalid credential types still get validated at runtime. Must either remove credentials or set authentication to "none".

### MCP Validator vs Runtime Validator
The MCP `n8n_validate_workflow` tool and n8n's runtime `checkForWorkflowIssues()` check different things. MCP validator can report `valid: true` while runtime still rejects. For definitive diagnosis, SSH into server and patch the source to log the issues object.

### Code Node Return Validation
n8n flags "Cannot return primitive values" on Code nodes with:
- Multiple `return` statements in conditional blocks
- `.find()` callbacks containing `return true/false`
Solution: Single return at end, use `for` loops with `break` instead of `.find()`.

---

## Iteration Accuracy Comparison

| Iteration | Tests | Passed | Failed | Accuracy |
|-----------|-------|--------|--------|----------|
| 4 | 44* | ~42 | ~2 | ~95% |
| 5 | 50 | 49 | 1 | **98%** |
| Production verify | 6 | 6 | 0 | **100%** |

---

## Agent IDs from This Session

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| a5f9fed | Explore | Map Eugene chunk architecture | Completed |
| a6bf6ef | solution-builder-agent | Production changes to Chunk 2.5 | Completed |
| ade4bcb | server-ops-agent | Disable debug logging on server | Completed |
| aa54c6a | server-ops-agent | Debug log investigation (no detail found) | Completed |
| a4f3cfe | server-ops-agent | SSH exact issues capture (FOUND ROOT CAUSE) | Completed |
| a06c027 | test-runner-agent | Test attempt (can't fire webhooks) | Completed |

### Previously tracked agents (from v11.0):
- a3a9f9b: test-runner-agent - Run iteration 4 tests
- a9021c3: test-runner-agent - Run iteration 4 tests 6-50
- ad3bd43: server-ops-agent - Diagnose webhook registration
- ac42b19: server-ops-agent - Fix webhook listener + restart n8n
