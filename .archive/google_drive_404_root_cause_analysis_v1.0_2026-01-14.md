# Google Drive 404 Error - Root Cause Analysis

**Date:** 2026-01-14
**Status:** 🔴 CRITICAL - Blocking all workflow executions
**Scope:** Affects Eugene Document Organizer V8 end-to-end pipeline

---

## Executive Summary

**Your Questions Answered:**

1. **Is this a logic error or a bug?**
   → **LOGIC/DESIGN ERROR** in workflow architecture

2. **Is something taking the file too quickly?**
   → **NO** - The file ID itself becomes invalid/non-existent

3. **How critical is this?**
   → **CRITICAL** - 100% failure rate on all Pre-Chunk 0 executions since at least 08:10:40 UTC

---

## What We Know (Facts)

### File Lifecycle Evidence

**Test 11 Execution Timeline:**
```
08:47:41.513Z - File created: ID 1i9VHBasonOffbrgtPzaR3v3M950fW6Sl
               Location: Temp folder
               Size: 53,328 bytes
               Name: 251103_Kaufpreise Schlossberg.pdf
               Status: ✅ SUCCESS

08:47:48.???Z - File moved to _Staging
               Same ID: 1i9VHBasonOffbrgtPzaR3v3M950fW6Sl
               Location: villa_martens/_Staging/
               Status: ✅ SUCCESS (1375ms execution time)

08:47:54.223Z - Chunk 2.5 tries to rename file
               File ID: 1i9VHBasonOffbrgtPzaR3v3M950fW6Sl
               Error: 404 "The resource you are requesting could not be found"
               Status: ❌ FAILURE

NOW (2026-01-14 10:00+) - File verification
               File ID: 1i9VHBasonOffbrgtPzaR3v3M950fW6Sl → NOT FOUND
               Search by name: "251103_Kaufpreise Schlossberg.pdf" → FOUND in _Staging
               File exists: ✅ YES (under different ID)
               Original test file: ❌ DELETED
```

### Critical Discovery

**The file DOES exist in _Staging folder right now**, but under a DIFFERENT file ID than what Test 11 created. This means:

1. ✅ File successfully uploaded
2. ✅ File successfully moved to _Staging
3. ❌ File with original ID was DELETED between move and rename
4. ✅ A different file with same name remains in _Staging (from earlier test)

---

## Systematic Failure Pattern

**ALL Pre-Chunk 0 executions failing:**

| Execution ID | Start Time | Status | Error Location |
|--------------|------------|--------|----------------|
| 2448 | 08:49:40 | ERROR | Execute Chunk 2 (EXISTING) |
| 2444 | 08:47:40 | ERROR | Execute Chunk 2 (EXISTING) |
| 2439 | 08:41:41 | ERROR | Execute Chunk 2 (EXISTING) |
| 2434 | 08:36:40 | ERROR | Execute Chunk 2 (EXISTING) |
| 2429 | 08:30:40 | ERROR | Execute Chunk 2 (EXISTING) |
| 2424 | 08:26:40 | ERROR | Execute Chunk 2 (EXISTING) |
| 2419 | 08:20:40 | ERROR | Execute Chunk 2 (EXISTING) |
| 2414 | 08:17:40 | ERROR | Execute Chunk 2 (EXISTING) |
| 2409 | 08:13:40 | ERROR | Execute Chunk 2 (EXISTING) |
| 2407 | 08:10:40 | ERROR | Execute Chunk 2 (EXISTING) |

**Failure rate:** 100% (10 out of 10 executions)
**Pattern:** Executions trigger every ~3-6 minutes (Gmail polling interval)
**Common error:** Google Drive 404 at "Execute Chunk 2 (EXISTING)" or Chunk 2.5 "Rename File with Confidence"

---

## Root Cause Hypotheses (Ranked by Likelihood)

### Hypothesis 1: File Deleted by Concurrent Process ⭐ MOST LIKELY

**Evidence:**
- File exists after move (confirmed by execution logs)
- File doesn't exist 6 seconds later when rename is attempted
- File with same name exists in _Staging now (from earlier test)
- Pattern suggests automated cleanup

**Possible culprits:**
1. **Another workflow** monitoring _Staging and deleting/processing files
2. **Error recovery workflow** cleaning up failed executions
3. **Chunk 2 or Chunk 2.5** has delete operation on error paths
4. **Manual cleanup** (unlikely - happens too consistently)

**How to test:**
- Check for workflows with Google Drive delete operations
- Monitor _Staging folder during test execution
- Check workflow error handlers for file deletion

### Hypothesis 2: Google Drive API Rate Limiting / Caching Issue

**Evidence:**
- File move reports success
- Immediate read of same file ID fails with 404
- Google Drive APIs have known caching delays

**Possible cause:**
- Move operation returns success before Drive indexes the file
- Subsequent rename operation queries for file before indexing completes
- 404 returned due to eventual consistency delay

**How to test:**
- Add 2-3 second delay between move and rename
- Check Google Drive API quotas and rate limits
- Review Google Drive credential permissions

### Hypothesis 3: Workflow Routing Logic Error

**Evidence:**
- Error occurs at "Execute Chunk 2 (EXISTING)" node
- There are TWO execution paths: NEW vs EXISTING clients
- Decision gate routes to "EXISTING" path

**Possible cause:**
- EXISTING path assumes file already in _Staging with different workflow
- NEW path properly stages file then triggers Chunk 2
- Routing logic incorrectly classifies Villa Martens as EXISTING

**How to test:**
- Check "Decision Gate" node logic
- Verify Villa Martens classification (should it be NEW or EXISTING?)
- Compare NEW vs EXISTING execution paths

### Hypothesis 4: File ID Mutation on Move

**Evidence:**
- Upload returns file ID: `1i9VHBasonOffbrgtPzaR3v3M950fW6Sl`
- Move operation claims same ID
- File with that ID doesn't exist

**Possible cause:**
- Google Drive assigns NEW file ID when moving between folders
- n8n Google Drive node doesn't update fileId after move
- Workflow uses stale file ID for subsequent operations

**How to test:**
- Manually move a file in Google Drive and check if ID changes
- Compare file ID before and after move operation
- Check n8n Google Drive node documentation

---

## Execution Flow Analysis

### Pre-Chunk 0 → Chunk 2 → Chunk 2.5 Flow

```
Pre-Chunk 0 (YGXWjWcBIk66ArvT):
  1. Gmail Trigger ✅
  2. Upload PDF to Temp Folder ✅ (creates file ID)
  3. Extract File ID & Metadata ✅
  4. Move PDF to _Staging (EXISTING) ✅ (file ID should stay same)
  5. Prepare for Chunk 2 (EXISTING) ✅
  6. Execute Chunk 2 (EXISTING) ❌ → 404 ERROR
     ↓
Chunk 2 (qKyqsL64ReMiKpJ4):
  1. Execute Workflow Trigger ⚠️ (receives fileId from Pre-Chunk 0)
  2. Normalize Input → Extract Text → Detect Scan
  3. Execute Chunk 2.5 ❌ → passes fileId to Chunk 2.5
     ↓
Chunk 2.5 (okg8wTqLtPUwjQ18):
  1. Execute Workflow Trigger ⚠️
  2. Build AI Classification Prompt → GPT-4 → Parse Results ✅
  3. Rename File with Confidence ❌ → 404 ERROR (fileId not found)
```

### Where File ID Becomes Invalid

**The 404 error occurs at TWO places:**

1. **Pre-Chunk 0 "Execute Chunk 2 (EXISTING)"** - When calling Chunk 2 workflow
2. **Chunk 2.5 "Rename File with Confidence"** - When trying to rename file

Both errors reference the SAME file ID, suggesting the file is deleted/invalid BEFORE Chunk 2 even starts.

---

## Critical Questions to Answer

### 1. Is there a workflow deleting files from _Staging?

**Check:**
- List all active workflows
- Search for Google Drive delete/trash operations
- Check error handlers with cleanup logic

**Command:**
```javascript
// Search all workflows for delete operations
search_nodes(query: "delete")
search_nodes(query: "trash")
```

### 2. What is the ACTUAL file ID in _Staging right now?

**Check:**
- Open Google Drive manually
- Navigate to villa_martens/_Staging/
- Find "251103_Kaufpreise Schlossberg.pdf"
- Get file ID from share link or URL

**If different ID:**
- Confirms file was re-uploaded by different test
- Original Test 11 file was deleted

### 3. Does Google Drive change file IDs when moving?

**Test:**
- Upload test file to Google Drive
- Note file ID
- Move file to different folder
- Check if file ID changed

**Expected:** File ID should STAY THE SAME when moving within Google Drive

### 4. Is Villa Martens being routed to NEW or EXISTING path?

**Check Pre-Chunk 0 execution #2444:**
- "Decision Gate" node output
- Which path did it take? (Output 0 = UNKNOWN, Output 1 = NEW, Output 2 = EXISTING)
- "Check Client Exists" node - what did it return?

**If EXISTING:**
- Lookup Client Registry found villa_martens in spreadsheet
- Routed to EXISTING client path
- This may be incorrect if Villa Martens folders don't exist yet

---

## Recommended Diagnostic Steps

### Step 1: Check for File Deletion Workflows (5 minutes)

1. List all active workflows
2. Search each for Google Drive delete/trash operations
3. Check if any monitor _Staging folder
4. Review error handlers for cleanup logic

### Step 2: Monitor _Staging Folder During Test (10 minutes)

1. Manually trigger Test Email Sender
2. Open Google Drive _Staging folder in browser
3. Watch for file to appear
4. Watch if file disappears before rename
5. Time how long file exists

### Step 3: Add Diagnostic Logging (15 minutes)

Add Code nodes to track file ID through pipeline:

**After "Move PDF to _Staging":**
```javascript
console.log('File moved to staging:');
console.log('- File ID:', $json.fileId);
console.log('- Timestamp:', new Date().toISOString());
return [$input.all()];
```

**Before "Rename File with Confidence":**
```javascript
console.log('About to rename file:');
console.log('- File ID:', $json.fileId);
console.log('- Timestamp:', new Date().toISOString());
return [$input.all()];
```

### Step 4: Test Google Drive File ID Persistence (5 minutes)

1. Manually upload a PDF to Google Drive
2. Note the file ID from the share link
3. Move the file to a different folder
4. Check if the file ID changed

### Step 5: Review Routing Logic (10 minutes)

1. Get Pre-Chunk 0 execution #2444 full data
2. Check "Decision Gate" output
3. Verify "Check Client Exists" logic
4. Confirm Villa Martens should route to EXISTING path

---

## Potential Solutions (Based on Root Cause)

### If Hypothesis 1 (Concurrent Deletion):

**Solution:** Identify and disable/fix the deleting workflow

**Steps:**
1. Find workflow deleting files from _Staging
2. Check if it's an error cleanup workflow
3. Either disable it or fix its logic to not delete files still being processed
4. Add file locking mechanism if needed

### If Hypothesis 2 (API Caching):

**Solution:** Add delay between move and rename operations

**Steps:**
1. Add Wait node (2-3 seconds) after "Move PDF to _Staging"
2. Test if delay resolves 404 errors
3. If successful, document as workaround for Google Drive eventual consistency

### If Hypothesis 3 (Routing Logic):

**Solution:** Fix NEW vs EXISTING routing logic

**Steps:**
1. Review "Check Client Exists" node logic
2. Verify Client_Registry spreadsheet data for villa_martens
3. Update routing decision to correctly classify clients
4. Ensure _Staging folder exists before routing to EXISTING path

### If Hypothesis 4 (File ID Mutation):

**Solution:** Re-fetch file ID after move operation

**Steps:**
1. After "Move PDF to _Staging", add Google Drive "Get File" operation
2. Use new file ID from Get File response
3. Pass updated file ID to Chunk 2
4. Update all downstream nodes to use refreshed file ID

---

## Impact Assessment

### Current State

**Workflows Affected:**
- ✅ V8 Classification Pipeline - WORKING (Tests 3-11 validated)
- ❌ File Rename/Move Operations - BLOCKED
- ❌ End-to-End Automation - BLOCKED

**Failure Rate:**
- 100% of Pre-Chunk 0 executions failing
- No successful document processing since at least 08:10:40 UTC
- ~10+ failed attempts in past 2 hours

**User Impact:**
- Eugene cannot use automated document organizer
- All incoming emails with PDFs are not being processed
- Manual intervention required for every document

### Business Impact

**If Not Fixed:**
- Eugene Document Organizer V8 cannot launch to production
- Manual document processing required (defeats automation purpose)
- Client confidence in automation solution at risk

**Urgency:** 🔴 CRITICAL - Must be resolved before V8 production launch

---

## Next Steps

### Immediate Actions (Today)

1. **Execute Step 1:** Check for file deletion workflows
2. **Execute Step 5:** Review routing logic for villa_martens
3. **Execute Step 4:** Test Google Drive file ID persistence

### Short-Term (This Week)

1. Implement solution based on root cause identified
2. Run Test 12 to validate fix
3. Monitor 5-10 successful executions
4. Document fix in VERSION_LOG.md

### Medium-Term (Post-Launch)

1. Add file existence validation before rename operations
2. Implement better error handling for 404 errors
3. Add retry logic with exponential backoff
4. Create monitoring alerts for systematic failures

---

## Appendix: Technical Details

### File ID from Test 11

```json
{
  "fileId": "1i9VHBasonOffbrgtPzaR3v3M950fW6Sl",
  "fileName": "251103_Kaufpreise Schlossberg.pdf",
  "size": 53328,
  "created": "2026-01-14T08:47:41.513Z",
  "modified": "2026-01-14T08:47:42.412Z",
  "owner": "swayclarkeii@gmail.com",
  "status": "File created successfully, moved to _Staging, then DELETED"
}
```

### Google Drive Credential

```json
{
  "credentialId": "a4m50EefR3DJoU0R",
  "credentialName": "Google Drive account",
  "credentialType": "googleDriveOAuth2Api",
  "usedBy": [
    "Pre-Chunk 0: Upload, Move, Download operations",
    "Chunk 2: Download PDF operation",
    "Chunk 2.5: Rename File operation"
  ]
}
```

### Error Stack Trace

```
NodeApiError: The resource you are requesting could not be found
  at ExecuteContext.httpRequestWithAuthentication (request-helper-functions.ts:1391:9)
  at ExecuteContext.googleApiRequest (transport/index.ts:54:11)
  at ExecuteContext.execute (file/update.operation.ts:266:23)
  HTTP Status: 404
  Workflow: okg8wTqLtPUwjQ18 (Chunk 2.5)
  Node: Rename File with Confidence
  File ID: 1i9VHBasonOffbrgtPzaR3v3M950fW6Sl
```

---

**Analysis Version:** v1.0
**Date:** 2026-01-14
**Analyst:** Claude Code (Sonnet 4.5)
**Review Status:** Ready for investigation
