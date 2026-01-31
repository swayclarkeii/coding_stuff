# W1v2: Webhook-Based Bank Statement Intake - Implementation Complete

**Agent:** solution-builder-agent
**Date:** 2026-01-30
**Workflow ID:** `Is8zl1TpWhIzspto`
**Status:** Built (inactive) - Ready for testing

---

## Overview

Created **W1v2** as a webhook-based alternative to W1 (Google Drive polling). This workflow accepts bank statement PDFs directly via POST request instead of monitoring a Google Drive folder.

**Key difference:** Local folder watcher script will POST files to this webhook, enabling faster processing and eliminating Google Drive API polling overhead.

---

## Workflow Structure

### Trigger
- **Node:** Webhook Upload Trigger
- **Type:** POST webhook
- **Path:** `expense-bank-statement-upload`
- **Full URL:** `https://n8n.oloxa.ai/webhook/expense-bank-statement-upload`
- **Accepts:** `multipart/form-data` (binary file upload)
- **Response mode:** `lastNode` (caller gets confirmation when processing completes)

### Processing Pipeline

```
Webhook Upload Trigger (POST multipart/form-data)
  ↓
Extract File Metadata (parse filename, generate IDs)
  ↓
Build Anthropic API Request (convert PDF to base64)
  ↓
Parse PDF with Anthropic Vision (extract transactions via Claude)
  ↓
Parse Anthropic Response (convert JSON to transaction records)
  ↓ (splits to two paths)
  ├─→ Prepare Statement Log → Log Statement Record (Statements sheet)
  └─→ Check for Duplicates → Read Existing Transactions → Filter Non-Duplicates → Write Transactions to Database (Transactions sheet)
```

### Nodes Removed from W1

1. ❌ **"Watch Bank Statements Folder"** (Google Drive trigger) - not needed for webhook approach
2. ❌ **"Download PDF"** (Google Drive download) - binary comes directly from webhook
3. ❌ **"Move PDF to Archive"** (Google Drive move) - local watcher handles file management

### Nodes Modified from W1

**"Extract File Metadata":**
- Updated to handle webhook binary input (instead of Google Drive JSON)
- Generates unique file ID: `webhook-{timestamp}`
- Still supports all three filename formats:
  - `ING_2025-01_Statement.pdf` (YYYY-MM)
  - `Miles&More_Nov2025_Statement.pdf` (TextMonth+YYYY)
  - `Barclay - Sep 2025.pdf` (TextMonth YYYY)

### Nodes Kept Identical from W1

- ✅ Build Anthropic API Request (uses `this.helpers.getBinaryDataBuffer()` for n8n 2.1.4 filesystem mode)
- ✅ Parse PDF with Anthropic Vision (Claude Sonnet 4.5 extraction)
- ✅ Parse Anthropic Response (JSON → transaction records)
- ✅ Prepare Statement Log (metadata for Statements sheet)
- ✅ Check for Duplicates (pass-through)
- ✅ Log Statement Record (write to Statements sheet)
- ✅ Read Existing Transactions (fetch from Transactions sheet)
- ✅ Filter Non-Duplicates (dedupe logic)
- ✅ Write Transactions to Database (append to Transactions sheet)

---

## Configuration

### Credentials Used

| Node | Credential | ID |
|------|-----------|-----|
| Parse PDF with Anthropic Vision | Anthropic API | `MRSNO4UW3OEIA3tQ` |
| Parse PDF with Anthropic Vision | HTTP Header Auth (Anthropic) | `vfoYopBRX35Znmq6` |
| Log Statement Record | Google Sheets | `H7ewI1sOrDYabelt` |
| Read Existing Transactions | Google Sheets | `H7ewI1sOrDYabelt` |
| Write Transactions to Database | Google Sheets | `H7ewI1sOrDYabelt` |

### Google Sheets Database

- **Sheet ID:** `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
- **Sheets:**
  - `Transactions` - individual transaction records
  - `Statements` - statement metadata log

---

## Validation Results

✅ **Valid workflow** (no errors)
⚠️ **23 warnings** (mostly style suggestions, not blockers):
- Expression format suggestions (low-confidence warnings from validator)
- Error handling recommendations (inherited from W1)
- TypeVersion suggestions (non-critical)

**All critical functionality intact** - workflow ready for testing.

---

## Testing Plan

### 1. Happy-Path Test

**Input:**
- POST to `https://n8n.oloxa.ai/webhook/expense-bank-statement-upload`
- Multipart form data with PDF file
- Example filename: `ING_2025-01_Statement.pdf`

**Expected Output:**
- Transactions extracted and written to Transactions sheet
- Statement metadata logged in Statements sheet
- Duplicates filtered out
- Webhook returns success confirmation

### 2. Local Folder Watcher Integration

**Next step:** Create folder watcher script that:
1. Monitors local directory (e.g., `~/Documents/Bank Statements/`)
2. Detects new PDF files
3. POSTs each file to webhook URL
4. Logs success/failure
5. Optionally moves processed files to archive folder

**Example curl command:**
```bash
curl -X POST \
  https://n8n.oloxa.ai/webhook/expense-bank-statement-upload \
  -F "data=@/path/to/ING_2025-01_Statement.pdf"
```

### 3. Error Scenarios

- Test invalid filename format (should fallback to current date)
- Test duplicate file upload (should skip duplicate transactions)
- Test malformed PDF (should fail gracefully at Anthropic Vision step)

---

## Handoff Notes

### How to Activate

1. Open workflow in n8n UI: `https://n8n.oloxa.ai/workflow/Is8zl1TpWhIzspto`
2. Toggle "Active" switch in top-right corner
3. Webhook URL becomes live: `https://n8n.oloxa.ai/webhook/expense-bank-statement-upload`

### How to Monitor

- **Executions:** Check n8n UI > Executions tab to see real-time processing
- **Errors:** Any node failures will appear in execution logs
- **Logs:** Google Sheets "Statements" tab shows processed files
- **Duplicates:** Check execution logs for "Skipping duplicate" messages

### Known Limitations

1. **No archive functionality** - local watcher script must handle file archiving (W1v2 doesn't move files in Google Drive)
2. **FileID is timestamp-based** - not tied to actual Google Drive file ID (since files don't come from Drive)
3. **Response mode:** Webhook waits for entire processing pipeline to complete before responding (can take 10-30 seconds for large PDFs)

### Comparison to W1

| Feature | W1 (Google Drive Polling) | W1v2 (Webhook Upload) |
|---------|--------------------------|----------------------|
| Trigger | Polls Drive every minute | Instant webhook POST |
| Latency | Up to 60 seconds | Immediate |
| File source | Google Drive folder | Local filesystem via POST |
| Archive handling | Moves to Drive archive | Local watcher handles |
| Integration | Google Drive sync required | Works with any folder watcher |

---

## Suggested Next Steps

1. ✅ **Test with single PDF** - Use curl or Postman to POST a test file
2. ⏳ **Build folder watcher script** - Python/Node.js script to monitor local directory
3. ⏳ **Add error notifications** - Slack/email alerts for failed processing
4. ⏳ **Performance test** - Test with multiple simultaneous uploads
5. ⏳ **Consider async mode** - If processing takes too long, respond immediately and process async

---

## Files Created/Modified

- **Workflow created:** `Is8zl1TpWhIzspto` (W1v2)
- **Documentation:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/projects/oloxa/SwaysExpenseSystem/W1v2_WEBHOOK_IMPLEMENTATION.md`
