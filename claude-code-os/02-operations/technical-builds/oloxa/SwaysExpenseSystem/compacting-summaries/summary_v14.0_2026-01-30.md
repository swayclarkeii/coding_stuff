# Expense System - Summary v14.0

**Date:** 2026-01-30
**Status:** W7 Invoice Routing Fixed, W1 Rate Limit Fix Applied, W1 Needs Re-test

---

## What Was Done This Session

### 1. W7 Invoice Routing Fix (COMPLETE)
- **Problem:** SC invoices were correctly categorized as `sway_invoice` but the Check if Sway Invoice node received 0 items — broken IF node connections
- **Root Cause:** n8n MCP tool and REST API both merge IF node TRUE/FALSE outputs into a single array (`main[1]` with 2 items) instead of separate arrays (`main[2]`)
- **Fix:** Sway manually reconnected 3 IF nodes in n8n UI:
  - Skip Unknown Files: TRUE→Route Expensify, FALSE→Download Unknown
  - Route Expensify to W6: TRUE→Prepare W6 Input, FALSE→Check if Sway Invoice
  - Check if Sway Invoice: TRUE→Download Sway Invoice, FALSE→Download File
- **Result:** Manual scan (exec #7209) processed 52 files, 4 SC invoices correctly written to Invoices sheet

### 2. Invoice Duplicate Cleanup (COMPLETE)
- Invoices sheet had 8 rows (4 unique + 4 duplicates from duplicate files in Downloads)
- Cleaned to 4 unique rows:
  - #506 antoni Holding GmbH - EUR 535.50
  - #451 Not A Machine GmbH - EUR 1,190.00
  - #442 SUPREME MUSIC GmbH - EUR 535.50
  - #454 acc rekorder GmbH - EUR 1,428.00

### 3. W7 Webhook Rescan Trigger (ADDED)
- Added webhook-rescan node (path: `expense-w7-rescan`) for manual file reprocessing
- Needed because Google Drive trigger only fires on NEW files
- Note: Requires saving in n8n UI to register the webhook path

### 4. W1 Rate Limit Fix (APPLIED, NEEDS RE-TEST)
- **Problem:** "Read Existing Transactions" node fails with Google Sheets 429 (60 reads/min/user shared across all workflows)
- **Fix applied by agent a879da3:**
  - Added "Wait 60s (Rate Limit Buffer)" node before Sheets read
  - Set `onError: continueRegularOutput` — if read fails, continues with empty data (writes all transactions)
  - Set retry: 5 attempts, 15s between tries
- **Status:** W1 trigger hasn't fired a new execution yet — Drive trigger may have already consumed the file. Needs manual re-trigger.

### 5. n8n IF Node Connection Bug (DOCUMENTED)
- **Critical finding:** Both `n8n_update_partial_workflow` MCP tool AND the n8n REST API PUT normalize IF node connections, merging TRUE/FALSE outputs into a single array
- **Workaround:** IF node connections must be set manually in n8n UI editor
- This affects all IF nodes across all workflows

---

## Current System Status

| Flow | Status | Notes |
|------|--------|-------|
| Receipts (W7 → Sheets) | WORKING | Drop PDFs in Downloads folder → auto-logged |
| Invoices (W7 → Sheets) | WORKING | SC invoices detected and logged (verified) |
| Expensify (W7 → W6 → Sheets) | WORKING | Expensify PDFs parsed and logged |
| Gmail receipts (W2 → Sheets) | WORKING | Email receipts auto-detected |
| Bank statements (W1 → Sheets) | NEEDS RE-TEST | Rate limit fix applied, awaiting successful run |
| Matching (W3) | WORKING | Date/amount matching with tolerance |
| Filing (W4) | WORKING | Creates folder structure, moves files |

### Google Sheets Data

| Sheet | Rows | Status |
|-------|------|--------|
| Receipts | 16 | 9 Expensify + 7 Hard Drive |
| Invoices | 4 | 4 unique SC invoices |
| Transactions | 0 (headers only) | W1 hasn't succeeded yet |
| Statements | 0 (headers only) | W1 hasn't succeeded yet |

---

## Pending / Next Steps

1. **W1 re-test** — Trigger W1 manually (Watch Bank Statements Folder may need a new file). Verify the 60s wait + continueOnFail handles the rate limit.
2. **Receipts sheet cleanup** — Rows 2-10 (Expensify) are missing FileName/FileID/FilePath from before W6 output format was fixed. Those old rows have incomplete data.
3. **Manual config still needed** (from v13.1):
   - W0: Assign Gmail OAuth2 credential to "Send Accountant Email" node
   - W0: Update accountant email (currently `accountant@example.com`)
   - Slack App: Enable Interactivity → `https://n8n.oloxa.ai/webhook/slack-expense-buttons`
   - W2: Toggle continueOnFail on 3 Vision API nodes + Vision API OAuth2 credential
   - Old W3/W8: Toggle active=false for `waPA94G2GXawDlCa` and `JNhSWvFLDNlzzsvm`

---

## Productization Notes (from this session)

Sway asked about alternatives to Google Drive polling for selling the system:

1. **Local folder watcher + webhook** — Lightweight script watches local folder, POSTs to n8n webhook. Most universal.
2. **Dropbox / OneDrive / S3** — Swap trigger node per client's cloud storage.
3. **Upload portal (web form)** — n8n form trigger, client gets URL to drag-and-drop files. Cleanest for product — no cloud storage dependency.

**Recommendation:** Upload portal for product, local folder watcher for power users.

---

## Key IDs

| Resource | ID |
|----------|-----|
| W0 Master Orchestrator | `ewZOYMYOqSfgtjFm` |
| W1 PDF Intake & Parsing | `MPjDdVMI88158iFW` |
| W2 Gmail Monitor | `dHbwemg7hEB4vDmC` |
| W3 Matching (v2.1) | `CJtdqMreZ17esJAW` |
| W4 Monthly Folder Builder | `nASL6hxNQGrNBTV4` |
| W6 Expensify Parser | `zFdAi3H5LFFbqusX` |
| W7 Downloads Monitor | `6x1sVuv4XKN0002B` |
| Google Sheets | `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` |
| Expense System folder | `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15` |
| Receipt Pool | `1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4` |
| Invoice Pool | `1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l` |
| Downloads folder | `1f4HP_6JEtePXjEmNqvdRNQ9vB_CcdQ3x` |
| Google Drive credential | `a4m50EefR3DJoU0R` |
| Google Sheets credential | `H7ewI1sOrDYabelt` |
| Slack credential | `iN2b9bGFpoyptSPr` |

---

## Agent IDs from This Session (2026-01-30)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| a947286 | test-runner | W7 verification | Complete |
| a44c654 | solution-builder | W7 IF node connection fix (MCP limitation found) | Complete |
| a9fae4e | solution-builder | W1 retry fix (5s delay) | Complete |
| a879da3 | solution-builder | W1 rate limit fix (60s wait + continueOnFail) | Complete |

### Previous Session Agents (from v13.1)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| a70d645 | solution-builder | Phase 2: W7 + W6 enhancements | Complete |
| a3859da | solution-builder | Phase 3: W2 hybrid filter | Complete |
| a5553b0 | solution-builder | Phase 4: W3 matching fix | Complete |
| ae1ce44 | solution-builder | Phase 5: W0 Slack buttons | Complete |
| aa60b70 | solution-builder | Phase 6: W4 filing updates | Complete |

---

## Architecture

```
INTAKE:
  Downloads Folder → W7 (PDF filter + classify)
    ├─ Receipt → Receipt Pool (Hard Drive) + Sheets
    ├─ Invoice → Invoice Pool + Sheets
    └─ Expensify → W6 (parse tables) → Receipt Pool + Sheets

  Gmail → W2 (hybrid filter + classify)
    ├─ Receipt PDF → Receipt Pool (Gmail) + Sheets
    └─ Expensify PDF → Upload to Drive + Trigger W6

  Bank Statements → W1 (parse via Anthropic Vision)
    └─ Extract transactions → [Wait 60s] → Dedup → Sheets

MATCHING:
  W3 → normalized date/amount matching → update Sheets

ORCHESTRATION:
  W0 → read Sheets → Slack notification with buttons
    ├─ [Re-match Now] → W3
    ├─ [Execute Filing] → W4
    └─ [Send to Accountant] → Gmail

FILING:
  W4 → create VAT folder structure → move files → update Sheets
    ├─ ING Diba/ (Statements/ + Receipts/)
    ├─ Deutsche Bank/ (Statements/ + Receipts/)
    ├─ Barclay/ (Statements/ + Receipts/)
    ├─ Miles & More/ (Statements/ + Receipts/)
    └─ Income/ (invoices)
```
