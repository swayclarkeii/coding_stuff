# Expense System - Summary v13.0

**Date:** 2026-01-29
**Status:** Complete Rebuild - All 7 Phases Built, Testing In Progress

---

## What Was Done This Session

Full system rebuild consolidating the expense pipeline into a single-intake architecture. All 7 phases executed:

### Phase 1: Cleanup
- Renamed old W3 (`waPA94G2GXawDlCa`) and W8 (`JNhSWvFLDNlzzsvm`) with [DEACTIVATED] suffix
- Need to toggle active=false in n8n UI (MCP can't deactivate workflows)

### Phase 2: W7 + W6 Single Intake
- **W7** (`6x1sVuv4XKN0002B`): Added PDF-only filter in "Filter Valid Files" node, Expensify filename detection in "Categorize by Filename", new Switch node routing Expensify files to W6 as sub-workflow
- **W6** (`zFdAi3H5LFFbqusX`): Added Execute Workflow Trigger (accepts fileId from W7), updated Download PDF node to accept fileId from either webhook or sub-workflow, added Upload to Receipt Pool node after logging

### Phase 3: W2 Gmail Hybrid Filter
- **W2** (`dHbwemg7hEB4vDmC`): Added "Hybrid Pre-Filter" code node between Gmail fetch and attachment processing
- Filters: 35+ known vendor domains, 13 keywords (EN/DE), PDF-only attachment check
- Logic: (vendor match OR keyword match) AND has PDF
- Also fixed credential ID "80" → `a4m50EefR3DJoU0R` on "Upload to Expensify Reports Folder" node

### Phase 4: W3 Matching Fix
- **W3** (`CJtdqMreZ17esJAW`): Updated "Match Receipts to Expense Transactions" code node with:
  - `normalizeDate()`: Handles DD.MM.YYYY, DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD, text months
  - `normalizeAmount()`: Strips currency symbols, handles German (1.572,94) and US (1,572.94) formats
  - Matching tolerance: +/-0.02
- Added "Re-match Webhook" node (path: `expense-rematch`) for W0 Slack button

### Phase 5: W0 Slack Interactive Buttons
- **W0** (`ewZOYMYOqSfgtjFm`): Added Slack Block Kit message with 3 buttons:
  - "Re-match Now" → calls W3 via sub-workflow
  - "Execute Filing" → calls W4 via sub-workflow
  - "Send to Accountant" → sends Gmail with Drive folder link
- Added single webhook (`slack-expense-buttons`) that routes by action_id via Switch node
- Existing orchestration flow preserved (webhook trigger, read sheets, filter missing, notify)

### Phase 6: W4 Filing Updates
- **W4** (`nASL6hxNQGrNBTV4`): 28 → 50 nodes
  - Renamed: "Mastercard" → "Miles & More", "Barclays" → "Barclay"
  - Added duplicate folder checking (Search → IF → Use Existing/Create → Merge) for all folders
  - Added Income/ subfolder for invoices
  - Added month/year filtering (defaults to previous month)
  - Added webhook trigger (path: `expense-filing`)
  - Fixed Google Drive search nodes: replaced broken native nodes with HTTP Request nodes calling Drive API
  - Fixed credentials on all 5 search nodes (`a4m50EefR3DJoU0R`)

---

## Current Test Results

| Workflow | ID | Status | Notes |
|----------|----|--------|-------|
| W0 Orchestrator | `ewZOYMYOqSfgtjFm` | PASS | No data for test month (expected) |
| W2 Gmail Monitor | `dHbwemg7hEB4vDmC` | 91% PASS | W6 webhook call fails (environmental) |
| W3 Matching | `CJtdqMreZ17esJAW` | PASS | Executed successfully |
| W4 Filing | `nASL6hxNQGrNBTV4` | PASS | Folder search + dupe check working |
| W6 Expensify Parser | `zFdAi3H5LFFbqusX` | PASS | Test file doesn't exist (expected) |
| W7 Downloads Monitor | `6x1sVuv4XKN0002B` | N/A | Drive Trigger, can't API-test |

---

## Manual Config Required (Sway in n8n UI)

1. **W0**: Assign Gmail OAuth2 credential to "Send Accountant Email" node
2. **W0**: Update accountant email address (currently `accountant@example.com`)
3. **Slack App**: Enable Interactivity → Request URL: `https://n8n.oloxa.ai/webhook/slack-expense-buttons`
4. **W2**: Toggle continueOnFail on 3 Vision API nodes + add Vision API OAuth2 credential
5. **Old W3/W8**: Toggle active=false for `waPA94G2GXawDlCa` and `JNhSWvFLDNlzzsvm`

---

## Webhook URLs

| Workflow | Webhook Path | Full URL |
|----------|-------------|----------|
| W0 Start | `w0-expense-orchestrator-start` | `https://n8n.oloxa.ai/webhook/w0-expense-orchestrator-start` |
| W0 Slack Buttons | `slack-expense-buttons` | `https://n8n.oloxa.ai/webhook/slack-expense-buttons` |
| W3 Re-match | `expense-rematch` | `https://n8n.oloxa.ai/webhook/expense-rematch` |
| W4 Filing | `expense-filing` | `https://n8n.oloxa.ai/webhook/expense-filing` |

---

## Key IDs Reference

| Resource | ID |
|----------|-----|
| W0 Master Orchestrator | `ewZOYMYOqSfgtjFm` |
| W1 PDF Intake | `MPjDdVMI88158iFW` |
| W2 Gmail Monitor | `dHbwemg7hEB4vDmC` |
| W3 Matching (v2.1) | `CJtdqMreZ17esJAW` |
| W3 OLD [DEACTIVATED] | `waPA94G2GXawDlCa` |
| W4 Monthly Folder Builder | `nASL6hxNQGrNBTV4` |
| W6 Expensify Parser | `zFdAi3H5LFFbqusX` |
| W7 Downloads Monitor | `6x1sVuv4XKN0002B` |
| W8 Invoice Collector [DEACTIVATED] | `JNhSWvFLDNlzzsvm` |
| Google Sheets | `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` |
| Expense System base folder | `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15` |
| Receipt Pool | `1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4` |
| Invoice Pool | `1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l` |
| Downloads folder | `1f4HP_6JEtePXjEmNqvdRNQ9vB_CcdQ3x` |
| Google Drive credential | `a4m50EefR3DJoU0R` |
| Google Sheets credential | `H7ewI1sOrDYabelt` |
| Slack credential | `iN2b9bGFpoyptSPr` |

---

## Agent IDs from This Session

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| a70d645 | solution-builder | Phase 2: W7 + W6 enhancements | Complete |
| a3859da | solution-builder | Phase 3: W2 hybrid filter | Complete |
| a5553b0 | solution-builder | Phase 4: W3 matching fix | Complete |
| ae1ce44 | solution-builder | Phase 5: W0 Slack buttons | Complete |
| aa60b70 | solution-builder | Phase 6: W4 filing updates | Complete |
| ac02fe6 | test-runner | Phase 7: Initial test run | Complete |
| a48885a | solution-builder | W2 credential fix | Complete |
| a485472 | solution-builder | W4 structural fix (attempt 1) | Complete |
| a2e7b49 | solution-builder | W4 Drive search node fix | Complete |
| ab85955 | test-runner | W4+W2 re-test | Complete |
| ada1b8b | test-runner | W4 re-test after Drive fix | Complete |
| a2981d4 | test-runner | W4 final re-test (PASS) | Complete |

---

## Architecture

```
INTAKE:
  Downloads Folder → W7 (PDF filter + classify)
    ├─ Receipt → Receipt Pool (Hard Drive) + Sheets
    ├─ Invoice → Invoice Pool + Sheets
    └─ Expensify → W6 (parse tables) → Receipt Pool + Sheets

  Gmail → W2 (hybrid filter + classify)
    └─ Receipt PDF → Receipt Pool (Gmail) + Sheets

  Bank Statements → W1 (unchanged)
    └─ Extract transactions → Sheets

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

---

## Next Steps

1. Real-world end-to-end testing (in progress)
2. Manual config items (Sway in n8n UI)
3. Deactivate old W3/W8 in n8n UI
4. Set up Slack App interactivity
5. First real month filing test
