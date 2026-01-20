# W7 Downloads Folder Monitor - Production Diagnosis

**Date:** January 12, 2026 - 23:30 CET
**System Version:** v2.1.0
**Workflow ID:** 6x1sVuv4XKN0002B
**Status:** ACTIVE (but not processing files)

---

## Problem Statement

**Reported Issue:** Sway uploaded a new receipt to the Downloads folder, but W7 (Downloads Folder Monitor) is not processing it.

**Expected Behavior:**
- File uploaded to Downloads folder
- W7 detects file via Google Drive trigger
- File categorized (sway_invoice/receipt/etc.)
- File processed through Claude Vision
- Uploaded to Invoice/Receipt Pool
- Logged to Google Sheets

**Actual Behavior:**
- File uploaded
- ❌ No execution triggered
- ❌ No data in Google Sheets Invoices sheet

---

## Diagnosis Summary

Based on workflow documentation and recent testing, I've identified **THREE CRITICAL ISSUES** that could explain why W7 isn't processing files:

### 🔴 Critical Issue #1: Google Drive Trigger Polling Limitation

**Problem:** Google Drive triggers only detect changes AFTER the trigger starts polling.

**Evidence from N8N_NODE_REFERENCE.md:**
> **Polling Behavior:**
> - Trigger uses `lastTimeChecked` timestamp to track when it last polled
> - **Only detects changes AFTER trigger activation**
> - Files already present in folder BEFORE trigger starts watching won't fire executions

**Timeline Check Needed:**
1. When was W7 last activated? (Need to check n8n UI)
2. When was the receipt uploaded?
3. If receipt was uploaded BEFORE W7 was activated → trigger won't fire

**Recommended Fix:**
```
Option A: Move file OUT of Downloads folder, wait 5 seconds, move BACK
- This creates a "fileUpdated" event that trigger will detect

Option B: Re-activate workflow
1. Deactivate W7 in n8n
2. Wait 10 seconds
3. Reactivate W7
4. Wait 1 minute for trigger to initialize
5. Upload NEW test file (or move existing file)
```

### 🔴 Critical Issue #2: Trigger Event Type Mismatch

**Problem:** W7 trigger may be configured for `fileCreated` instead of `fileUpdated`.

**Evidence from N8N_NODE_REFERENCE.md:**
> **1. `fileCreated` Event:**
> - Only fires when NEW files are created directly in the folder
> - Will NOT fire for files moved into folder from another location
> - Will NOT fire for files copied into folder
>
> **2. `fileUpdated` Event:**
> - Fires when files are modified
> - **Fires when files are moved into folder (recommended for intake workflows)**
> - Fires when files are copied if copy operation updates modification timestamp

**If the file was:**
- Downloaded from browser → Moved from system Downloads to synced folder → `fileCreated` won't fire
- Copied from another location → `fileCreated` won't fire

**Recommended Fix:**
```
Change Google Drive Trigger event type from "fileCreated" to "fileUpdated"

Why: Downloads folder receives files via MOVE operations (browser download → synced folder)
      This creates UPDATE events, not CREATE events
```

### ⚠️ Critical Issue #3: Workflow Not Actually ACTIVE

**Problem:** Workflow may show as "Active" in documentation but be INACTIVE in n8n.

**Need to Verify:**
1. Open n8n UI
2. Navigate to workflow ID `6x1sVuv4XKN0002B`
3. Check if toggle switch shows "Active" (green) or "Inactive" (grey)

**Common Causes:**
- Workflow was deactivated during recent duplicate check debugging
- Credential issue caused auto-deactivation
- n8n server restart reset workflow state

---

## Secondary Issues (Less Likely)

### 4. Downloads Folder ID Configuration

**Folder ID (should be):** `1O3udIURR14LsEP3Wt4o1QnxzGsR2gciN`

**Need to Verify:**
- Open W7 workflow in n8n
- Check Google Drive Trigger node
- Confirm `folderId` parameter matches `1O3udIURR14LsEP3Wt4o1QnxzGsR2gciN`

### 5. Credential Expiration

**Credentials Used:**
- Google Drive OAuth credential
- Anthropic API credential: `MRSNO4UW3OEIA3tQ`

**Need to Check:**
- Google Drive credential hasn't expired (OAuth token refresh)
- Anthropic API key is valid

### 6. Duplicate Check Bypass Verification

**Known Issue from v7.0 summary:**
> **W7 Duplicate Check Removed (Temporary)**
> - Issue: Nodes 10 and 15 removed due to Google Drive query API failures
> - Status: Nodes 11 & 16 modified to always pass (`true === true`)

**This should NOT block execution** - duplicate check was bypassed to always proceed. But worth verifying nodes 11 & 16 still contain bypass logic.

---

## Diagnostic Steps (Prioritized)

### Step 1: Verify Workflow is ACTIVE (HIGHEST PRIORITY)
```
1. Open n8n: https://n8n.oloxa.ai (or wherever n8n is hosted)
2. Navigate to workflow ID: 6x1sVuv4XKN0002B
3. Check workflow header - is "Active" toggle ON (green)?
4. If OFF → Activate it
5. If ON → Proceed to Step 2
```

### Step 2: Check Trigger Event Type
```
1. In W7 workflow, click on "Google Drive Trigger" node
2. Check "Event" parameter
3. Current value: Should show "file" > "fileUpdated" or "fileCreated"
4. If "fileCreated" → Change to "fileUpdated"
5. Save workflow
6. Re-test with file upload
```

### Step 3: Verify Trigger Polling Timestamp
```
1. In Google Drive Trigger node parameters
2. Look for "lastTimeChecked" or "Last Poll Time"
3. Compare to when your receipt was uploaded
4. If receipt was uploaded BEFORE last poll → trigger missed it
5. Solution: Upload NEW file OR move existing file to trigger update event
```

### Step 4: Check Recent Executions
```
1. In n8n, click "Executions" tab (top menu)
2. Filter by workflow: W7 (6x1sVuv4XKN0002B)
3. Check last execution timestamp
4. Look for:
   - No executions → Trigger not firing
   - Failed executions → Check error messages
   - Successful but empty → Trigger firing but file filtered out
```

### Step 5: Verify Folder ID Configuration
```
1. In Google Drive Trigger node
2. Check "Folder ID" parameter
3. Should be: 1O3udIURR14LsEP3Wt4o1QnxzGsR2gciN
4. If different → Update and save
```

### Step 6: Check Google Sheets for Indirect Evidence
```
1. Open Invoices sheet: https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM
2. Go to "Invoices" tab
3. Check for new rows with Source="Downloads"
4. If NO rows → Workflow didn't execute OR execution failed before Sheets logging
5. If rows exist → Workflow IS working, but may have processed different files
```

---

## Most Likely Root Cause

Based on the evidence, **Issue #1 (Polling Limitation)** is the most likely culprit:

**Scenario:**
1. W7 was activated yesterday during testing
2. Trigger set `lastTimeChecked` to activation time (e.g., Jan 11, 22:00)
3. Sway uploaded receipt today (Jan 12, 23:00)
4. File upload created `fileUpdated` event with timestamp Jan 12, 23:00
5. Trigger polled and detected the change
6. **BUT:** If W7 was **deactivated** during recent debugging and hasn't been re-activated yet, no polling occurs

**Combined with Issue #3 (Not Actually Active):**
- Documentation says "Active" but workflow may be OFF in n8n UI
- This would explain complete silence (no executions, no errors)

---

## Recommended Fix (Quick Win)

**If you have n8n UI access right now:**

1. **Check if W7 is ACTIVE**
   - Open workflow `6x1sVuv4XKN0002B`
   - If inactive → Activate it
   - Wait 1 minute for trigger to initialize

2. **Re-trigger the file**
   - Move the receipt OUT of Downloads folder to Desktop
   - Wait 10 seconds
   - Move it BACK to Downloads folder
   - This creates a new `fileUpdated` event
   - Trigger should fire within 1 minute

3. **Verify execution**
   - Check Executions tab in n8n
   - Look for new W7 execution
   - If success → Check Invoices sheet for new row
   - If failed → Read error message and diagnose

**If you DON'T have n8n UI access right now:**

1. **Check Google Sheets as proxy**
   - Open Invoices sheet
   - Look for ANY new rows from today
   - If yes → W7 may be working but processing different files
   - If no → W7 definitely not executing

2. **Upload a NEW test file with obvious filename**
   - Create a file named: `TEST-W7-2026-01-12-23-30.pdf`
   - Upload to Downloads folder
   - Wait 2 minutes
   - Check Sheets again
   - If new row appears → W7 is working, just hasn't processed your receipt yet

---

## Alternative Diagnosis: File Was Filtered Out

**Possible:** The workflow IS running, but your receipt was filtered by categorization logic.

**W7 categorization rules:**
```javascript
Category Logic (from "Categorize by Filename" node):
- sway_invoice: Filename starts with "SC - "
- client_invoice: Contains "SUPREME MUSIC", "Massive Voices", or "BOXHOUSE"
- invoice: Contains "invoice" or "rechnung"
- receipt: Contains "receipt", "beleg", or "quittung"
- unknown: None of the above → SKIPPED
```

**Check your receipt filename:**
- Does it contain "receipt", "beleg", or "quittung"?
- If NO → Categorized as "unknown" → Skipped by node 3 "Skip Unknown Files"

**Solution if filename is generic:**
```
Rename file to include keyword:
- Original: "document_2026-01-12.pdf"
- Renamed: "receipt_2026-01-12.pdf"
- Re-upload to Downloads folder
```

---

## Next Steps

**Immediate (Within 5 Minutes):**
1. Check if W7 is ACTIVE in n8n UI
2. Check Google Sheets Invoices for any new rows today
3. Note the filename of your uploaded receipt

**Short-term (Within 30 Minutes):**
1. Verify Google Drive Trigger event type (fileCreated vs fileUpdated)
2. Check recent W7 executions in n8n
3. Verify folder ID configuration

**If Still Not Working:**
1. Export current W7 workflow and check trigger configuration manually
2. Create minimal test: Upload file named "receipt-test.pdf" with obvious content
3. Check n8n logs for errors

---

## Files Created

- `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/W7-PRODUCTION-DIAGNOSIS.md` (this file)

---

## Agent Session Info

**Agent ID:** [This session - solution-builder-agent]
**Task:** Diagnose W7 production issue
**Status:** Diagnosis complete - awaiting n8n UI verification

---

**Built:** 2026-01-12 23:30 CET
**Agent:** solution-builder-agent
