# Expense System - Summary v15.0

**Date:** 2026-01-31
**Status:** Gathr local folder system built, W1v2 + W7v2 webhook workflows operational, moving off Google Drive polling

---

## What Was Done This Session

### 1. W1v2 Transactions Fix (COMPLETE)
- **Problem:** All W1v2 executions showed SUCCESS but Transactions sheet was empty
- **Root Cause:** "Read Existing Transactions" (Google Sheets) returned 0 items from empty sheet, which replaced incoming transaction data. Downstream nodes (Filter Non-Duplicates, Write Transactions) never executed because they received 0 items.
- **Fix:** Converted "Read Existing Transactions" from Google Sheets node to Code node that always outputs at least 1 item (`{_isEmpty: true}` dummy). Updated "Filter Non-Duplicates" to handle dummy items.
- **Result:** 97 transactions written on first successful test (Miles & More Oct 2025)

### 2. Gathr Folder System (COMPLETE)
- Created `/Users/swayclarke/gathr/` as the product folder with:
  - `bank_statements/` (+ processed/, errors/)
  - `receipts_invoices/` (+ processed/, errors/)
- Moved all existing bank statements from `/Users/swayclarke/bank_statements/` to gathr
- Built unified watcher script: `scripts/gathr-watcher.py`
  - Watches both folders simultaneously
  - 300s upload timeout (up from 180s)
  - Sequential queue processing with 10s between files
  - 3 retries with 30s delay
  - `--once` mode and `--folders` flag for selective processing

### 3. W7v2 Receipts & Invoices Webhook (COMPLETE)
- **Workflow ID:** `qSuG0gwuJByd2hGJ`
- **Webhook:** `https://n8n.oloxa.ai/webhook/expense-receipts-upload`
- Uses Anthropic Vision (Claude Sonnet 4.5) to classify files as receipt/invoice/expensify/unknown
- Routes to correct Google Sheets tab + Google Drive folder:
  - receipt → Receipts sheet + Receipt Pool folder
  - sway_invoice → Invoices sheet + Invoice Pool folder
  - expensify → Receipts sheet (Source=Expensify) + Receipt Pool
  - unknown → Downloads folder (no sheet write)
- Uploads files to Google Drive with FilePath tracking

### 4. W7v2 JSON Parse Fix (COMPLETE)
- **Problem:** Parse Classification node crashed when Anthropic returned JSON wrapped in markdown code fences
- **Fix:** 4-level robust JSON extraction: direct parse → strip fences → regex extract → first-{-to-last-} extraction
- All 27 receipt/invoice files processed after fix

### 5. Batch Processing Results
**Bank Statements (8 files):**
- 7/8 succeeded via watcher
- 1 persistent failure: Miles&More Nov 2025 (connection timeout on client side, but n8n processes it successfully — PDF too large)

**Receipts & Invoices (27 files):**
- 25/27 succeeded on first attempt
- 2 failed before JSON parse fix, succeeded after fix
- Classification accuracy: receipts, invoices (SC files), and unknown correctly identified
- Note: Expensify report classified as "unknown" instead of "expensify" — classification prompt needs tuning

### 6. Known Issues
- **Miles&More Nov PDF:** Consistently times out on watcher side (>60s for Vision API). n8n processes it fine. The watcher's 300s timeout isn't the issue — the remote server closes the connection before responding.
- **Webhook registration:** Workflows created via API/MCP don't register webhooks until saved + toggled in n8n UI. One-time issue per workflow.
- **Expensify classification:** SwayClarkeNOV2025ExpenseReport.pdf classified as "unknown" — needs prompt tuning to recognize Expensify reports.

---

## Current System Status

| Flow | Status | Notes |
|------|--------|-------|
| W1v2 Bank Statements (Webhook) | WORKING | Local folder → watcher → webhook → Vision → Sheets |
| W7v2 Receipts/Invoices (Webhook) | WORKING | Local folder → watcher → webhook → classify → Sheets + Drive |
| W1 Bank Statements (Drive poll) | WORKING (backup) | Original, can be deactivated |
| W7 Downloads Monitor (Drive poll) | WORKING (backup) | Original, can be deactivated |
| W2 Gmail Monitor | WORKING | Next to migrate off Google Drive polling |
| W3 Matching | WORKING | Date/amount matching |
| W4 Monthly Folder Builder | WORKING | Creates folder structure |
| W6 Expensify Parser | WORKING | Parses Expensify PDFs |
| W0 Master Orchestrator | WORKING | Slack buttons |

### Gathr Folder Structure
```
/Users/swayclarke/gathr/
├── bank_statements/
│   ├── processed/    (8 files)
│   └── errors/       (Miles&More Nov)
└── receipts_invoices/
    ├── processed/    (27 files)
    └── errors/       (empty)
```

### Scripts
- `scripts/gathr-watcher.py` — unified watcher for both folders
- `scripts/bank-statement-watcher.py` — original (superseded by gathr-watcher)
- `scripts/com.oloxa.bank-statement-watcher.plist` — launchd plist (needs update for gathr-watcher)

---

## Pending / Next Steps

1. **Migrate Gmail (W2) off Google Drive polling** — Use IMAP/SMTP or HTTP approach instead of Drive trigger
2. **Local-first filing strategy** — Two options to plan:
   - Option A: Create VAT folder structure locally, upload final result to Google Drive
   - Option B: Do everything locally, bulk upload to Google Drive when done
3. **Expensify classification** — Tune W7v2 prompt to correctly identify Expensify reports
4. **Miles&More timeout** — Investigate: possibly increase n8n webhook timeout, or split large PDFs
5. **Deactivate old workflows** — Once confident, deactivate W1 (Drive poll) and W7 (Downloads Monitor)
6. **Update launchd plist** — Point to gathr-watcher.py instead of bank-statement-watcher.py

---

## Key IDs

| Resource | ID |
|----------|-----|
| W0 Master Orchestrator | `ewZOYMYOqSfgtjFm` |
| W1 PDF Intake & Parsing | `MPjDdVMI88158iFW` |
| W1v2 Bank Statement Webhook | `Is8zl1TpWhIzspto` |
| W2 Gmail Monitor | `dHbwemg7hEB4vDmC` |
| W3 Matching (v2.1) | `CJtdqMreZ17esJAW` |
| W4 Monthly Folder Builder | `nASL6hxNQGrNBTV4` |
| W6 Expensify Parser | `zFdAi3H5LFFbqusX` |
| W7 Downloads Monitor | `6x1sVuv4XKN0002B` |
| W7v2 Receipts Webhook | `qSuG0gwuJByd2hGJ` |
| Google Sheets | `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` |
| Expense System folder | `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15` |
| Receipt Pool | `1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4` |
| Invoice Pool | `1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l` |
| Downloads folder | `1f4HP_6JEtePXjEmNqvdRNQ9vB_CcdQ3x` |

---

## Agent IDs from This Session (2026-01-31)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| a879da3 | solution-builder | W1 rate limit fix (60s wait + continueOnFail) | Complete |
| a9402d7 | solution-builder | W1 Wait node removal | Complete |
| a5444e4 | Bash | Workflow JSON backups (2026-01-30) | Complete |
| a4e3524 | solution-builder | W1v2 webhook build | Complete |
| a0c4f47 | solution-builder | W1v2 fix/test | Complete |
| abb5aeb | general-purpose | Bank statement watcher script | Complete |
| a3d5c0f | solution-builder | W1v2 transactions fix (dedup chain) | Complete |
| ae05a35 | solution-builder | W7v2 receipts webhook build | Complete |
| aebe09c | solution-builder | W7v2 JSON parse fix | Complete |
| a86dafb | test-runner | W1v2 + W7v2 test iteration | Running |
| ae15f78 | Bash | Workflow JSON backups (2026-01-31) | Running |

### Previous Session Agents (from v14.0)
| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| a947286 | test-runner | W7 verification | Complete |
| a44c654 | solution-builder | W7 IF node connection fix | Complete |
| a9fae4e | solution-builder | W1 retry fix | Complete |

---

## Architecture

```
GATHR LOCAL INTAKE:
  /Users/swayclarke/gathr/
  ├── bank_statements/ → gathr-watcher.py → W1v2 webhook
  │   └─ Anthropic Vision → Extract transactions → Dedup → Sheets (Transactions + Statements)
  └── receipts_invoices/ → gathr-watcher.py → W7v2 webhook
      └─ Anthropic Vision → Classify (receipt/invoice/expensify/unknown)
          ├─ Receipt → Receipts sheet + Receipt Pool (Drive)
          ├─ Invoice → Invoices sheet + Invoice Pool (Drive)
          ├─ Expensify → Receipts sheet (Source=Expensify) + Receipt Pool
          └─ Unknown → Downloads folder (Drive)

GMAIL INTAKE (still on Drive polling):
  Gmail → W2 (hybrid filter + classify)
    ├─ Receipt PDF → Receipt Pool (Gmail) + Sheets
    └─ Expensify PDF → Upload to Drive + Trigger W6

MATCHING:
  W3 → normalized date/amount matching → update Sheets

ORCHESTRATION:
  W0 → read Sheets → Slack notification with buttons
    ├─ [Re-match Now] → W3
    ├─ [Execute Filing] → W4
    └─ [Send to Accountant] → Gmail

FILING:
  W4 → create VAT folder structure → move files → update Sheets
```
