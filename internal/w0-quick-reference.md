# W0 Master Orchestrator - Quick Reference

## Workflow Details
- **ID:** `ewZOYMYOqSfgtjFm`
- **URL:** `https://n8n.oloxa.ai/workflow/ewZOYMYOqSfgtjFm`
- **Status:** Phase 0 (Quick Win) - Ready for testing

---

## How to Run

### Trigger Monthly Close
```bash
curl -X POST https://n8n.oloxa.ai/webhook/w0-expense-orchestrator-start \
  -H "Content-Type: application/json" \
  -d '{"month": "2025-02"}'
```

### Trigger Quarterly Close
```bash
curl -X POST https://n8n.oloxa.ai/webhook/w0-expense-orchestrator-start \
  -H "Content-Type: application/json" \
  -d '{"quarter": "Q1-2025"}'
```

---

## What It Does

1. **Executes workflows in order:**
   - W1 (Bank Statements)
   - W2 (Gmail Receipts)
   - W6 (Expensify)
   - W3 (Matching)

2. **Checks for missing receipts:**
   - Reads Transactions sheet
   - Filters unmatched transactions
   - Excludes: Deka, Edeka, DM, Kumpel und Keule, Bettoni
   - Minimum: €10

3. **Reports results:**
   - Console log with missing receipts list OR success message
   - Check in n8n Executions tab

---

## What to Check

### View Results
1. Go to `https://n8n.oloxa.ai/executions`
2. Find latest W0 execution
3. Check "Log Missing Receipts" or "Log Success" node

### If Missing Receipts Found
1. Open Google Sheets: `https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM/edit`
2. Upload receipts to Receipt Pool folder
3. Re-run W3: `https://n8n.oloxa.ai/workflow/CJtdqMreZ17esJAW`
4. Re-run W0 to verify

### If All Matched ✅
1. Run W4 (Folder Builder): `https://n8n.oloxa.ai/workflow/nASL6hxNQGrNBTV4`
2. Send folder to Maud
3. Done!

---

## Phase 0 Limitations
- ❌ No Slack notifications (console only)
- ❌ No automatic Missing Receipts sheet tab
- ❌ No interactive buttons
- ❌ No error handling
- ❌ Manual W4 trigger required

**Phase 1 will add Slack, sheets, and automation.**

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Webhook 404 | Activate workflow in n8n |
| Sub-workflow fails | Check W1/W2/W3/W6 are active |
| No results | Check Transactions sheet columns |
| Can't see logs | Check n8n Executions tab |

---

**Built:** 2026-01-29
**Agent:** solution-builder-agent
