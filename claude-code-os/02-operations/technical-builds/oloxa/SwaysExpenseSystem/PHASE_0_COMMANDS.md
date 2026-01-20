# Phase 0: Quick Command Reference

**Use these commands in the main Claude Code session (NOT the agent)**

---

## Step 1: Add Webhook to W2

```
Use the n8n-mcp tool to update workflow dHbwemg7hEB4vDmC with these operations:

1. Add a webhook node named "Test Trigger - Webhook" with:
   - Path: test-expense-w2
   - HTTP method: POST
   - Response mode: lastNode
   - Position: [0, -200]
   - Type version: 2

2. Add a connection from "Test Trigger - Webhook" (main output) to "Load Vendor Patterns" (main input)
```

---

## Step 2: Add Webhook to W3

```
Use the n8n-mcp tool to update workflow waPA94G2GXawDlCa with these operations:

1. Add a webhook node named "Test Trigger - Webhook" with:
   - Path: test-expense-w3
   - HTTP method: POST
   - Response mode: lastNode
   - Position: [240, 100]
   - Type version: 2

2. Add a connection from "Test Trigger - Webhook" (main output) to "Get Unmatched Transactions" (main input)
```

---

## Step 3: Test W2

```
Use the n8n_test_workflow tool to test workflow dHbwemg7hEB4vDmC with test data: {"testMode": true}
```

Then verify:
```
Check the last execution of workflow dHbwemg7hEB4vDmC
```

---

## Step 4: Test W3

```
Use the n8n_test_workflow tool to test workflow waPA94G2GXawDlCa with test data: {"testMode": true}
```

Then verify:
```
Check the last execution of workflow waPA94G2GXawDlCa
```

---

## Step 5: Update VERSION_LOG.md

```
Update the VERSION_LOG.md file to add v1.2.4 entry with:
- Webhook additions to W2 and W3
- Test execution results
- Updated timestamp
```

---

## Verification

```
Get workflow dHbwemg7hEB4vDmC to verify webhook node exists and is connected correctly
```

```
Get workflow waPA94G2GXawDlCa to verify webhook node exists and is connected correctly
```

---

## Rollback (if needed)

```
Delete node "Test Trigger - Webhook" from workflow dHbwemg7hEB4vDmC
```

```
Delete node "Test Trigger - Webhook" from workflow waPA94G2GXawDlCa
```
