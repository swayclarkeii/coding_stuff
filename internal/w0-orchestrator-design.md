# W0 Expense System Master Orchestrator - Design

## Phase 0 Implementation (Quick Win)

### Workflow Overview

**Purpose:** Automate monthly/quarterly expense processing by orchestrating existing workflows (W1-W8) and detecting missing receipts.

**Trigger:** Manual webhook or n8n form

**Main Flow:**
1. Manual trigger with month/quarter input
2. Sequential execution: W1 → W2 → W6 → W3
3. Query transactions for missing receipts
4. Generate missing receipts report in Google Sheets
5. Send Slack notification with summary

---

## Node Structure

### 1. Webhook Trigger (Manual Start)
- **Type:** `n8n-nodes-base.webhook`
- **Purpose:** Allow Sway to manually trigger monthly close process
- **Parameters:**
  - Path: `/webhook/w0-expense-orchestrator-start`
  - Method: POST
  - Expected body:
    ```json
    {
      "month": "2025-01",
      "quarter": "Q1-2025"
    }
    ```

### 2. Extract Input Parameters
- **Type:** `n8n-nodes-base.code`
- **Purpose:** Parse and validate input parameters
- **Logic:**
  ```javascript
  const month = $json.month || '';
  const quarter = $json.quarter || '';
  const processDate = new Date().toISOString();

  if (!month && !quarter) {
    throw new Error('Must provide either month or quarter parameter');
  }

  return [{
    json: {
      processing_period: month || quarter,
      process_date: processDate,
      status: 'STARTED'
    }
  }];
  ```

### 3. Execute W1 (Bank Statements)
- **Type:** `n8n-nodes-base.executeWorkflow`
- **Purpose:** Process bank statement PDFs
- **Parameters:**
  - Workflow ID: `[W1_WORKFLOW_ID]`
  - Wait for completion: `true`

### 4. Execute W2 (Gmail Receipts)
- **Type:** `n8n-nodes-base.executeWorkflow`
- **Purpose:** Collect receipts from Gmail
- **Parameters:**
  - Workflow ID: `[W2_WORKFLOW_ID]`
  - Wait for completion: `true`

### 5. Execute W6 (Expensify)
- **Type:** `n8n-nodes-base.executeWorkflow`
- **Purpose:** Process Expensify reports
- **Parameters:**
  - Workflow ID: `[W6_WORKFLOW_ID]`
  - Wait for completion: `true`

### 6. Execute W3 (Matching)
- **Type:** `n8n-nodes-base.executeWorkflow`
- **Purpose:** Match transactions with receipts/invoices
- **Parameters:**
  - Workflow ID: `[W3_WORKFLOW_ID]`
  - Wait for completion: `true`

### 7. Read Transactions Sheet
- **Type:** `n8n-nodes-base.googleSheets`
- **Purpose:** Get all transactions to check for missing receipts
- **Parameters:**
  - Spreadsheet ID: `[EXPENSE_SHEETS_ID]`
  - Sheet name: `Transactions`
  - Operation: `Get Row(s)`
  - Return all: `true`

### 8. Filter Missing Receipts
- **Type:** `n8n-nodes-base.code`
- **Purpose:** Filter unmatched transactions based on criteria
- **Logic:**
  ```javascript
  const transactions = $input.all();
  const excludedVendors = ['Deka', 'Edeka', 'DM', 'Kumpel und Keule', 'Bettoni'];
  const minAmount = 10;

  const missingReceipts = transactions.filter(item => {
    const amount = parseFloat(item.json.Amount) || 0;
    const vendor = item.json.Vendor || '';
    const matchStatus = item.json.MatchStatus || '';

    // Apply filters
    if (amount < minAmount) return false;
    if (excludedVendors.includes(vendor)) return false;
    if (matchStatus === 'matched') return false;

    return true;
  });

  return missingReceipts.map(item => ({
    json: {
      transaction_date: item.json.Date,
      vendor: item.json.Vendor,
      amount_eur: item.json.Amount,
      category: item.json.Category,
      description: item.json.Description,
      transaction_id: item.json.ID
    }
  }));
  ```

### 9. Check if Missing Receipts Exist
- **Type:** `n8n-nodes-base.if`
- **Purpose:** Branch based on whether missing receipts were found
- **Conditions:**
  - If items count > 0 → Write to sheet + notify
  - If items count = 0 → Send success notification

### 10a. Clear Missing Receipts Sheet (if items found)
- **Type:** `n8n-nodes-base.googleSheets`
- **Purpose:** Clear previous missing receipts before writing new ones
- **Parameters:**
  - Spreadsheet ID: `[EXPENSE_SHEETS_ID]`
  - Sheet name: `Missing Receipts`
  - Operation: `Clear`
  - Range: `A2:F1000` (preserve headers)

### 10b. Write Missing Receipts to Sheet
- **Type:** `n8n-nodes-base.googleSheets`
- **Purpose:** Write missing receipts to dedicated sheet tab
- **Parameters:**
  - Spreadsheet ID: `[EXPENSE_SHEETS_ID]`
  - Sheet name: `Missing Receipts`
  - Operation: `Append Row`
  - Data mode: `Auto-Map Columns`
  - Columns:
    - Transaction Date
    - Vendor
    - Amount (EUR)
    - Category
    - Description
    - Transaction ID

### 11a. Calculate Missing Receipts Summary
- **Type:** `n8n-nodes-base.code`
- **Purpose:** Calculate totals for Slack notification
- **Logic:**
  ```javascript
  const missingItems = $input.all();
  const totalCount = missingItems.length;
  const totalAmount = missingItems.reduce((sum, item) => {
    return sum + parseFloat(item.json.amount_eur || 0);
  }, 0);

  return [{
    json: {
      has_missing: true,
      missing_count: totalCount,
      missing_total_eur: totalAmount.toFixed(2),
      processing_period: $('Extract Input Parameters').first().json.processing_period,
      sheet_url: `https://docs.google.com/spreadsheets/d/[EXPENSE_SHEETS_ID]/edit#gid=[MISSING_RECEIPTS_GID]`
    }
  }];
  ```

### 11b. Send Slack Notification (Missing Items)
- **Type:** `n8n-nodes-base.slack`
- **Purpose:** Notify Sway about missing receipts
- **Parameters:**
  - Channel: `[SLACK_CHANNEL_ID or #test-channel]`
  - Operation: `Post message`
  - Message:
    ```
    📋 Missing Receipts Detected

    Month/Quarter: {{ $json.processing_period }}
    Total missing: {{ $json.missing_count }} transactions (€{{ $json.missing_total_eur }})

    📊 View details: {{ $json.sheet_url }}
    📁 Upload files to: Receipt Pool folder

    Re-run W3 matching after uploading missing receipts.
    ```

### 12a. Calculate Success Summary (if all matched)
- **Type:** `n8n-nodes-base.code`
- **Purpose:** Calculate totals for success notification
- **Logic:**
  ```javascript
  const allTransactions = $('Read Transactions Sheet').all();
  const totalCount = allTransactions.length;
  const totalAmount = allTransactions.reduce((sum, item) => {
    return sum + parseFloat(item.json.Amount || 0);
  }, 0);

  return [{
    json: {
      has_missing: false,
      total_count: totalCount,
      total_amount_eur: totalAmount.toFixed(2),
      processing_period: $('Extract Input Parameters').first().json.processing_period
    }
  }];
  ```

### 12b. Send Slack Notification (All Matched)
- **Type:** `n8n-nodes-base.slack`
- **Purpose:** Notify Sway that all receipts matched
- **Parameters:**
  - Channel: `[SLACK_CHANNEL_ID or #test-channel]`
  - Operation: `Post message`
  - Message:
    ```
    ✅ All Receipts Matched

    Month/Quarter: {{ $json.processing_period }}
    Total transactions: {{ $json.total_count }} (€{{ $json.total_amount_eur }})

    Ready for manual folder organization (W4) and accountant handoff.
    ```

---

## Connections

```
Webhook Trigger
  ↓
Extract Input Parameters
  ↓
Execute W1
  ↓
Execute W2
  ↓
Execute W6
  ↓
Execute W3
  ↓
Read Transactions Sheet
  ↓
Filter Missing Receipts
  ↓
Check if Missing (IF node)
  ├─ TRUE (has missing) → Clear Sheet → Write Missing → Calculate Summary → Slack Notify (Missing)
  └─ FALSE (all matched) → Calculate Success → Slack Notify (Success)
```

---

## Configuration Needed from Sway

1. **Workflow IDs:**
   - W1 (Bank Statements): `[NEEDED]`
   - W2 (Gmail Receipts): `[NEEDED]`
   - W3 (Matching): `[NEEDED]`
   - W6 (Expensify): `[NEEDED]`

2. **Google Sheets:**
   - Spreadsheet ID: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` (from brief)
   - Sheet names:
     - `Transactions` (existing)
     - `Missing Receipts` (needs to be created)
   - Missing Receipts GID: `[NEEDED after sheet created]`

3. **Slack:**
   - Channel ID or name: `[NEEDED]` (or use test logging for now)

4. **Excluded Vendors List:**
   - Current: Deka, Edeka, DM, Kumpel und Keule, Bettoni
   - Confirm if this is accurate

5. **Minimum Transaction Amount:**
   - Current: €10
   - Confirm if this threshold is correct

---

## Testing Plan

### Test Scenario 1: Happy Path (All Matched)
1. Trigger workflow with `{"month": "2025-01-TEST"}`
2. Verify W1, W2, W6, W3 execute in sequence
3. Verify Transactions sheet is read
4. Verify all transactions show `MatchStatus: matched`
5. Verify success Slack notification sent

### Test Scenario 2: Missing Receipts
1. Manually set some test transactions to `MatchStatus: unmatched`
2. Trigger workflow with `{"month": "2025-01-TEST"}`
3. Verify missing receipts are filtered correctly
4. Verify Missing Receipts sheet is cleared and updated
5. Verify missing receipts Slack notification with correct counts

### Test Scenario 3: Excluded Vendors
1. Add test transaction with vendor "Edeka"
2. Verify it's excluded from missing receipts report

### Test Scenario 4: Minimum Amount Threshold
1. Add test transaction with amount €5
2. Verify it's excluded from missing receipts report

---

## Phase 1 Enhancements (Future)

After Phase 0 is working:
1. Add interactive webhook buttons for re-matching
2. Add W4 (Folder Builder) trigger webhook
3. Add accountant notification with Yes/No buttons
4. Add Processing Status tracking sheet
5. Add error handling and retry logic
6. Add duplicate month/quarter detection

---

## Notes

- Phase 0 skips interactive buttons (manual workflow triggers used instead)
- Slack notifications use simple text format (no Block Kit yet)
- No accountant email automation yet (manual email for now)
- Background monitors W7 and W8 run independently (not called by W0)
- For testing, use 2025 historical data to avoid production conflicts
