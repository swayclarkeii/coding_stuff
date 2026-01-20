# Autonomous Testing Guide

**Project**: Sway's Expense System
**Created**: December 30, 2025
**Purpose**: Comprehensive testing framework for expense automation workflows

---

## 🎯 Testing Framework Overview

### Infrastructure Created

1. **Test Orchestrator Workflow** (ID: `poBYxyCSaSgXDIhL`)
   - 5 nodes: Webhook Trigger → Parse Test Request → Execute Test Scenario → Log Test Results → Respond to Webhook
   - Supports 20 test scenarios (7 happy paths + 13 edge cases)
   - Tracks results locally in [TEST_RESULTS.md](TEST_RESULTS.md)
   - Status: ⚠️ Built but webhook needs manual UI activation

2. **Test Results Tracking**
   - Local file: [TEST_RESULTS.md](TEST_RESULTS.md)
   - Contains all 20 test scenario definitions
   - Tracks execution status, findings, and fixes

3. **Setup Testing Infrastructure Workflow** (ID: `PamWj7GKFHiUQq3n`)
   - 3 nodes: Webhook Trigger → Create TestResults Sheet → Add Column Headers
   - Purpose: Automate TestResults sheet creation in Google Sheets
   - Status: ⚠️ Built but webhook needs manual UI activation

---

## 📊 Test Scenarios (20 Total)

### Workflow 2: Gmail Receipt Monitor (7 scenarios)

#### Happy Paths
- **HP-01**: Single Vendor Receipt Discovery (OpenAI)
- **HP-02**: Multi-Vendor Receipt Batch (all 7 vendors)

#### Edge Cases
- **EC-01**: No Receipts Found (empty search)
- **EC-02**: Gmail API Rate Limit
- **EC-03**: Attachment Download Failure
- **EC-04**: Duplicate Receipt Detection
- **EC-05**: Large Attachment (>10MB)

### Workflow 1: PDF Statement Parser (6 scenarios)

#### Happy Paths
- **HP-03**: ING Bank Statement (German, 4 pages)
- **HP-04**: Deutsche Bank Statement (German, 2 pages)

#### Edge Cases
- **EC-06**: Corrupted PDF
- **EC-07**: Scanned PDF (image-based)
- **EC-08**: Empty Statement (no transactions)
- **EC-09**: OpenAI API Quota Exceeded

### Workflow 3: Transaction-Receipt Matching (7 scenarios)

#### Happy Paths
- **HP-05**: Perfect Match (date + amount exact)
- **HP-06**: Date +1 Day Match
- **HP-07**: Amount ±€0.50 Match

#### Edge Cases
- **EC-10**: Date +4 Days (outside range)
- **EC-11**: Multiple Possible Matches
- **EC-12**: Unmatched Transaction
- **EC-13**: Unmatched Receipt

---

## 🚀 How to Execute Tests

### Option 1: Manual n8n UI Activation (Recommended)

Since the Test Orchestrator webhook needs manual activation:

1. **Activate Test Orchestrator**:
   - Open n8n: https://n8n.oloxa.ai
   - Navigate to: Workflows → "Test Orchestrator - Autonomous Testing"
   - Click the workflow to open editor
   - Ensure workflow is ACTIVE (toggle in top-right should be green)
   - Save the workflow to register the webhook

2. **Test Individual Scenarios**:
   ```bash
   # Test HP-01 (OpenAI receipt search)
   curl -X POST https://n8n.oloxa.ai/webhook/test-expense-system \
     -H "Content-Type: application/json" \
     -d '{"scenario": "HP-01"}'

   # Test HP-02 (Multi-vendor batch)
   curl -X POST https://n8n.oloxa.ai/webhook/test-expense-system \
     -H "Content-Type: application/json" \
     -d '{"scenario": "HP-02"}'

   # Test EC-01 (No receipts found)
   curl -X POST https://n8n.oloxa.ai/webhook/test-expense-system \
     -H "Content-Type: application/json" \
     -d '{"scenario": "EC-01"}'
   ```

3. **Run All 20 Tests**:
   ```bash
   # Loop through all scenarios
   for scenario in HP-01 HP-02 EC-01 EC-02 EC-03 EC-04 EC-05 HP-03 HP-04 EC-06 EC-07 EC-08 EC-09 HP-05 HP-06 HP-07 EC-10 EC-11 EC-12 EC-13; do
     curl -X POST https://n8n.oloxa.ai/webhook/test-expense-system \
       -H "Content-Type: application/json" \
       -d "{\"scenario\": \"$scenario\"}" \
       -w "\n"
     sleep 2  # Pause between tests
   done
   ```

### Option 2: Direct Workflow Testing

Test Workflow 2 (Gmail Receipt Monitor) directly:

1. **Open Workflow 2 in n8n**:
   - Workflow ID: `2CA0zQTsdHA8bZKF`
   - Name: "Gmail Receipt Monitor"

2. **Manual Execution**:
   - Click "Test workflow" button in n8n UI
   - Watch execution progress through all 9 nodes
   - Check execution results for errors

3. **Validation Checklist**:
   - [ ] Gmail searches executed for all 7 vendors
   - [ ] Attachments downloaded successfully
   - [ ] Files uploaded to Receipt Pool folder
   - [ ] Receipts logged in Receipts sheet
   - [ ] No errors in execution log

### Option 3: Real Data Testing

Use 2025 receipts as test data:

1. **Trigger Workflow 2** to pull December 2025 receipts
2. **Verify downloads** in `_Receipt-Pool/` folder
3. **Check database** in Receipts sheet for new entries
4. **Test Workflow 3** (when built) to match receipts to transactions

---

## 🔍 Validation Criteria

### Workflow 2 Success Criteria

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Email search success | 100% | All vendor searches return results (if emails exist) |
| Attachment download | 100% | All found emails have attachments downloaded |
| File upload | 100% | All attachments uploaded to Receipt Pool |
| Receipt ID format | 100% | Check ReceiptID column matches `RCPT-{VENDOR}-{timestamp}` |
| Database logging | 100% | All receipts logged in Receipts sheet |
| Vendor identification | 100% | Vendor column populated correctly |

### Workflow 1 Success Criteria

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Parsing accuracy | 95%+ | Manual count: transactions in PDF vs database |
| Transaction ID format | 100% | Check TransactionID column matches pattern |
| Date format | 100% | No ISO dates in database (must be DD.MM.YYYY) |
| Vendor extraction | 80%+ | Vendor column populated (not "Unknown") |
| File archiving | 100% | PDF moved from _Inbox to _Archive |
| Database logging | 100% | Statement record in Statements sheet |

### Workflow 3 Success Criteria

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Match accuracy | 90%+ | Manual verification of matches |
| False positives | <5% | Check MatchConfidence <0.8 for incorrect matches |
| File organization | 100% | All matched receipts moved to correct year/month/bank folder |
| Database updates | 100% | Both Transactions and Receipts sheets updated |
| Unmatched handling | 100% | Transactions without receipts remain "unmatched" |

---

## 📝 Logging Test Results

### Manual Logging Template

For each test scenario, document in [TEST_RESULTS.md](TEST_RESULTS.md):

```markdown
#### Scenario: HP-01
- **Execution Date**: YYYY-MM-DD HH:MM
- **Status**: ✅ Passed / ❌ Failed / ⏳ Pending / ⚠️ Partial
- **Workflow Executed**: Yes/No
- **Receipts Processed**: X
- **Errors Found**: None / List errors
- **Expected Behavior**: [Description]
- **Actual Behavior**: [Description]
- **Notes**: [Any observations]
```

### Automated Logging (If Webhook Works)

The Test Orchestrator automatically logs to:
- Google Sheets: TestResults sheet (when created)
- Response JSON: Returns test result immediately

Example response:
```json
{
  "success": true,
  "testId": "TEST-1735557600000",
  "status": "manual_validation_required",
  "message": "Test HP-01: Would search Gmail for OpenAI receipts..."
}
```

---

## 🔧 Troubleshooting

### Test Orchestrator Webhook Not Working

**Issue**: 404 error when calling webhook
**Cause**: Webhook not registered in n8n
**Fix**:
1. Open workflow in n8n UI
2. Click "Save" button (forces webhook registration)
3. Verify workflow is ACTIVE
4. Try webhook call again

### Gmail OAuth Not Configured

**Issue**: Workflow 2 fails with authentication error
**Cause**: Gmail credentials not set up
**Fix**: See [ENVIRONMENT_SETUP.md](N8N_Blueprints/v1_foundation/ENVIRONMENT_SETUP.md) section "Gmail OAuth2"

### OpenAI API Insufficient Credits

**Issue**: Workflow 1 fails with quota error
**Cause**: Not enough OpenAI credits
**Fix**:
1. Check balance: https://platform.openai.com/account/billing/overview
2. Add credits: minimum $5 recommended
3. Verify API key in n8n credentials

### Google Sheets API Errors

**Issue**: "invalid_request" when logging results
**Cause**: Authentication expired or quota exceeded
**Fix**:
1. Refresh Google Sheets OAuth credentials in n8n
2. Check API quota: https://console.cloud.google.com/apis/dashboard
3. Fallback: Use local [TEST_RESULTS.md](TEST_RESULTS.md) for tracking

---

## 📈 Testing Progress Tracking

### Current Status

**Total Scenarios**: 20
- ✅ Passed: 0
- ❌ Failed: 0
- ⏳ Pending: 20
- ⚠️ Blocked: 7 (Workflow 3 scenarios - workflow not yet built)

**Workflows Ready for Testing**:
- ✅ Workflow 2 (Gmail Receipt Monitor) - 7 scenarios
- ✅ Workflow 1 (PDF Statement Parser) - 6 scenarios
- ❌ Workflow 3 (Transaction Matching) - 7 scenarios (blocked - not built)

**Prerequisites**:
- [ ] Gmail OAuth2 configured
- [ ] OpenAI API key configured with $5+ credits
- [ ] Test Orchestrator webhook activated in n8n UI
- [ ] TestResults sheet created in Expense-Database

---

## 🎯 Recommended Testing Order

1. **Start with Workflow 2** (lowest risk):
   - Scenarios: HP-01, HP-02, EC-01
   - Requires: Gmail OAuth only
   - Duration: ~10 minutes
   - Data: Uses real 2025 receipts

2. **Progress to Workflow 1** (higher cost):
   - Scenarios: HP-03, HP-04, EC-06
   - Requires: OpenAI API credits
   - Duration: ~20 minutes
   - Data: Upload sample German bank statements

3. **Build and Test Workflow 3** (not yet implemented):
   - Scenarios: HP-05, HP-06, HP-07, EC-10, EC-11, EC-12, EC-13
   - Requires: Workflow 3 built first
   - Duration: ~30 minutes
   - Data: Uses results from Workflows 1 & 2

---

## 📊 Final Deliverable

After all testing complete:

1. **Update [TEST_RESULTS.md](TEST_RESULTS.md)** with all execution results
2. **Generate summary report** with:
   - Total scenarios passed/failed
   - Issues discovered and fixed
   - Efficiency score calculation
   - Readiness assessment for production use
3. **Document any system improvements** made during testing
4. **Update [VERSION_LOG.md](N8N_Blueprints/v1_foundation/VERSION_LOG.md)** with testing milestone

---

**Last Updated**: December 30, 2025 at 12:53 CET
**Testing Framework Status**: ✅ Built, ⚠️ Awaiting Manual Activation
