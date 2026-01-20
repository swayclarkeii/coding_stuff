# v6 Phase 1 - Production Test Instructions

**Date:** 2026-01-09 16:35 CET
**Status:** Ready for manual workflow execution

---

## Quick Start (5 minutes)

**You need to do ONE manual action:**

1. Open: https://n8n.oloxa.ai/workflow/dZrBgt7W4j15zPRt
2. Click "Test workflow" button (top right)
3. Wait 10 seconds for execution to complete
4. Tell me "done" - I'll handle the rest autonomously

---

## What This Test Does

**Test Workflow:** v6 Autonomous Test Email Sender (ID: dZrBgt7W4j15zPRt)

**Execution Flow:**
1. Webhook Trigger (or Manual Trigger)
2. Prepare Test File IDs (generates 3 PDF file IDs)
3. Download PDF Files (downloads OCP-Anfrage-AM10.pdf from Google Drive 3 times)
4. Prepare Email Body (merges 3 PDF attachments into one email)
5. Send Test Email with PDFs (sends to swayclarkeii@gmail.com)

**What Happens Next:**
- Email arrives at swayclarkeii@gmail.com with 3 PDF attachments
- Gmail trigger on Pre-Chunk 0 detects email (5-60 min polling delay)
- Pre-Chunk 0 executes → calls Chunk 2 (with all 4 fixes applied)
- Chunk 2 executes → processes PDFs → calls Chunk 2.5
- Chunk 2.5 executes → AI classification → moves files to final location

---

## Automated Validation (I Handle This)

Once you say "done", I will:

### Step 1: Verify Test Email Sent
- Check execution #745+ for success
- Verify all 5 nodes completed (green checkmarks)
- Confirm email sent to swayclarkeii@gmail.com
- **Expected:** ✅ Success within 10 seconds

### Step 2: Monitor Pre-Chunk 0 Execution
- Poll for new execution (ID > #666)
- Check Gmail trigger fired
- Verify email processing started
- **Expected:** New execution within 5-60 minutes

### Step 3: Verify Chunk 2 Execution with All 4 Fixes
- Monitor Chunk 2 workflow (qKyqsL64ReMiKpJ4)
- Validate Fix #1: skipDownload logic (webhook body wrapper + Boolean())
- Validate Fix #2: Normalize Output syntax (safe text length calculation)
- Validate Fix #3: Execute Workflow Trigger (not webhook)
- Validate Fix #4: Field name output (clientNormalized for Chunk 2.5)
- **Expected:** ✅ All fixes working, no errors

### Step 4: Verify Chunk 2.5 Execution
- Monitor Chunk 2.5 workflow (okg8wTqLtPUwjQ18)
- Check AI classification ran successfully
- Verify file moved to final location
- Validate Client_Tracker sheet updated
- **Expected:** ✅ End-to-end success

### Step 5: Production Readiness Report
- Document all execution IDs
- Summarize success/failure for each stage
- List any errors or warnings encountered
- Provide production deployment recommendations

---

## Known Configuration

### Test Workflow Details
- **ID:** dZrBgt7W4j15zPRt
- **Name:** v6 Autonomous Test Email Sender
- **Status:** Inactive (manual trigger only)
- **Nodes:** 6 (Webhook Trigger, Manual Trigger, Prepare File IDs, Download PDFs, Prepare Email, Send Email)
- **PDF File ID:** 1k6X7V_JiAnOAXB5TP1MzveQEVv2em90V (OCP-Anfrage-AM10.pdf)
- **Attachments:** 3 copies of the same PDF (tests multi-attachment handling)

### Active v6 Phase 1 Workflows
| Workflow | ID | Status | Purpose |
|----------|-----|--------|---------|
| Pre-Chunk 0 | YGXWjWcBIk66ArvT | ✅ Active | Email intake & client detection |
| Chunk 0 | zbxHkXOoD1qaz6OS | ✅ Active | Folder initialization (new clients) |
| Chunk 2 | qKyqsL64ReMiKpJ4 | ✅ Active | Text extraction (with 4 fixes) |
| Chunk 2.5 | okg8wTqLtPUwjQ18 | ✅ Active | AI classification & file movement |

### Chunk 2 Fixes Applied
1. **skipDownload logic:** Handles webhook body wrapper, Boolean() type conversion
2. **Normalize Output syntax:** Safe text length calculation (no null.length errors)
3. **Execute Workflow Trigger:** Correct trigger type (not webhook)
4. **Field name compatibility:** Outputs clientNormalized (camelCase) for Chunk 2.5

---

## Expected Timeline

| Event | Time | Status Check |
|-------|------|--------------|
| Manual execution | T+0 min | You click "Test workflow" |
| Email sent | T+0 to T+2 min | I verify execution success |
| Gmail polling | T+5 to T+60 min | I monitor for Pre-Chunk 0 trigger |
| Pre-Chunk 0 execution | T+5 to T+61 min | I verify email processing |
| Chunk 2 execution | T+5 to T+62 min | I validate all 4 fixes |
| Chunk 2.5 execution | T+5 to T+63 min | I verify AI classification |
| Production report | T+65 min | I provide final readiness assessment |

---

## Fallback Options

### If Gmail Trigger Delays
Gmail polling can take up to 60 minutes. If no execution after 60 min:
- I'll check Gmail inbox directly to verify email arrived
- I'll check n8n logs for trigger polling status
- I'll recommend manual trigger of Pre-Chunk 0 with test data

### If Chunk 2 Fails
- I'll analyze error messages
- I'll check which of the 4 fixes failed
- I'll provide specific fix recommendations
- I'll test in isolation if needed

### If Chunk 2.5 Fails
- I'll check data contract compatibility
- I'll verify clientNormalized field is present
- I'll analyze AI classification errors
- I'll check Google Drive permissions

---

## Success Criteria

**Test passes when:**
- ✅ Email sent with 3 PDF attachments
- ✅ Pre-Chunk 0 processes email successfully
- ✅ Chunk 2 extracts text (skipDownload optimization working)
- ✅ Chunk 2 outputs clientNormalized (camelCase)
- ✅ Chunk 2.5 classifies and moves document
- ✅ No errors in any workflow stage
- ✅ All 4 Chunk 2 fixes validated

**Production ready when:**
- All success criteria met
- Execution times acceptable (< 2 min per stage)
- No manual intervention required
- Documentation complete

---

## Files Created This Session

| File | Purpose |
|------|---------|
| `WORKFLOW_REGISTRY.md` | Central workflow ID registry |
| `SESSION_COMPLETE_2026-01-09.md` | Complete session documentation (4 fixes) |
| `CHUNK2_CHUNK2.5_COMPATIBILITY_2026-01-09.md` | Field name compatibility analysis |
| `CHUNK2_FIELD_NAME_FIX_2026-01-09.md` | Fix #4 documentation |
| `PRODUCTION_TEST_INSTRUCTIONS_2026-01-09.md` | This file |

---

## What You Need to Do

1. Open: https://n8n.oloxa.ai/workflow/dZrBgt7W4j15zPRt
2. Click "Test workflow"
3. Tell me "done"

I'll handle everything else and report back when production-ready.

---

**Last Updated:** 2026-01-09 16:35 CET
**Next Action:** Awaiting your manual workflow execution
