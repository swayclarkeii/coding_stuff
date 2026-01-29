# n8n Test Report – Brain Dump Database Updater v1.1

**Workflow ID:** `UkmpBjJeItkYftS9`
**Workflow Name:** Brain Dump Database Updater v1.1
**Test Date:** 2026-01-15
**Tester:** test-runner-agent

---

## Summary

- **Total tests planned:** 3
- **Tests executed:** 0
- **Tests passed:** N/A
- **Tests failed:** N/A
- **Status:** BLOCKED - Workflow activation required

---

## Blocker: Workflow Not Active

### Issue
The workflow is currently **inactive** and cannot receive webhook requests. The `n8n_test_workflow` tool requires workflows to be active before testing webhook-triggered workflows.

### Error Details
```
Workflow must be active to trigger via this method
Hint: Activate the workflow in n8n using n8n_update_partial_workflow with [{type: "activateWorkflow"}]
```

### Limitation
The `test-runner-agent` does not have access to the `n8n_update_partial_workflow` tool needed to activate workflows. This activation must be done in the **main conversation** or by the **solution-builder-agent**.

---

## Workflow Configuration

**Trigger Type:** Webhook
**HTTP Method:** POST
**Webhook Path:** `brain-dump`
**Response Mode:** lastNode (waits for full workflow completion)

**Expected Webhook URL Structure:**
```
https://n8n.oloxa.ai/webhook/brain-dump
```

**Webhook Configuration:**
- Accepts POST requests only
- Expects JSON payload with brain dump data
- Returns aggregated results from all processing branches

---

## Test Cases (Ready to Execute)

### Test 1 - CRM Update

**Purpose:** Test CRM contact update/creation branch

**Payload:**
```json
{
  "crm_updates": [{
    "operation": "update",
    "name": "Test Contact - Claude",
    "stage": "Initial Outreach",
    "sentiment": "Neutral",
    "notes": "Automated test from workflow deployment"
  }],
  "tasks": [],
  "projects": [],
  "calendar": []
}
```

**Expected Behavior:**
1. Workflow routes to CRM branch
2. Checks if "Test Contact - Claude" exists in Google Sheets (Prospects sheet)
3. If exists: Updates the contact with new stage/sentiment/notes
4. If not exists: Creates new row in Google Sheets
5. Returns success message with contact name

**Expected Response:**
```json
{
  "status": "success",
  "summary": {
    "crm": "Updated/Created 1 contacts",
    "tasks": "No tasks created",
    "projects": "No project updates",
    "calendar": "No calendar events"
  },
  "errors": []
}
```

---

### Test 2 - Task Creation

**Purpose:** Test Notion task creation branch

**Payload:**
```json
{
  "crm_updates": [],
  "tasks": [{
    "operation": "create",
    "name": "Test Task - Workflow Deployment",
    "status": "To-do",
    "priority": "Medium",
    "type": "Work"
  }],
  "projects": [],
  "calendar": []
}
```

**Expected Behavior:**
1. Workflow routes to Tasks branch
2. Creates new task in Notion (Tasks database: 39b8b725-0dbd-4ec2-b405-b3bba0c1d97e)
3. Sets Name, Status, Priority, and Type properties
4. Returns success message with task name

**Expected Response:**
```json
{
  "status": "success",
  "summary": {
    "crm": "No CRM updates",
    "tasks": "Created 1 tasks",
    "projects": "No project updates",
    "calendar": "No calendar events"
  },
  "errors": []
}
```

---

### Test 3 - Project Update

**Purpose:** Test Notion project update/creation branch

**Payload:**
```json
{
  "crm_updates": [],
  "tasks": [],
  "projects": [{
    "operation": "update",
    "name": "PA Agent Workflow",
    "phase": "Testing",
    "status": "Active"
  }],
  "calendar": []
}
```

**Expected Behavior:**
1. Workflow routes to Projects branch
2. Searches for "PA Agent Workflow" in Notion Projects database (2d01c288-bb28-81ef-a640-000ba0da69d4)
3. If exists: Updates phase and status
4. If not exists: Creates new project with phase and status
5. Returns success message with project name

**Expected Response:**
```json
{
  "status": "success",
  "summary": {
    "crm": "No CRM updates",
    "tasks": "No tasks created",
    "projects": "Updated 1 projects",
    "calendar": "No calendar events"
  },
  "errors": []
}
```

---

## Validation Results

**Workflow Validation:** PASSED ✅
- Errors: 0
- Warnings: 0
- All nodes properly configured
- All connections valid

**Credentials:**
- Google Sheets OAuth: `combined-google-oauth` (configured)
- Google Calendar OAuth: `combined-google-oauth` (configured)
- Notion API: `Notion API 2` (ID: Sutx4Kyf49uSMEgO)

---

## Next Steps

### 1. Activate Workflow (REQUIRED)

**Option A - Main Conversation:**
```
Ask main conversation to activate workflow UkmpBjJeItkYftS9
```

**Option B - n8n UI:**
- Open workflow in n8n web interface
- Toggle activation switch to ON

### 2. Re-run Tests

Once activated, re-launch `test-runner-agent` with:
```
Test the Brain Dump Database Updater workflow with sample payloads.
Use the test cases in /Users/swayclarke/coding_stuff/tests/brain-dump-updater-test-report.md
```

### 3. Cleanup Test Data

After successful tests, delete test records:
- Google Sheets: Delete "Test Contact - Claude" from Prospects sheet
- Notion Tasks: Archive "Test Task - Workflow Deployment"
- Notion Projects: Check if "PA Agent Workflow" was created vs updated (only delete if newly created)

---

## Technical Notes

### Workflow Structure
- **53 nodes total** in complex parallel processing architecture
- **4 main branches:** CRM, Tasks, Projects, Calendar
- **Merge node:** Combines all branch results before response
- **Error handling:** Each branch logs results independently

### Key Processing Nodes
1. **Parse & Validate Input** - Validates incoming JSON structure
2. **Split By Update Type** - Creates parallel items for each update type
3. **Route Nodes** - Direct traffic to correct processing branch
4. **Process Nodes** - Extract and prepare data for each branch
5. **Merge All Results** - Combines all branch outputs
6. **Build Response** - Aggregates results into summary

### Credentials Used
- **Google Sheets:** CRM contact management (Prospects sheet)
- **Notion API:** Tasks and Projects databases
- **Google Calendar:** Event creation/deletion

---

## Recommendation

**Activate the workflow immediately** to enable testing. The workflow structure is sound and validation passed with 0 errors. Once active, all three test cases should execute successfully.

**Estimated test execution time:** 5-10 seconds per test (webhook workflows execute synchronously with `responseMode: lastNode`)

---

## Test Execution Commands

Once workflow is active, use these curl commands for manual testing:

**Test 1 - CRM Update:**
```bash
curl -X POST https://n8n.oloxa.ai/webhook/brain-dump \
  -H "Content-Type: application/json" \
  -d '{
    "crm_updates": [{
      "operation": "update",
      "name": "Test Contact - Claude",
      "stage": "Initial Outreach",
      "sentiment": "Neutral",
      "notes": "Automated test from workflow deployment"
    }],
    "tasks": [],
    "projects": [],
    "calendar": []
  }'
```

**Test 2 - Task Creation:**
```bash
curl -X POST https://n8n.oloxa.ai/webhook/brain-dump \
  -H "Content-Type: application/json" \
  -d '{
    "crm_updates": [],
    "tasks": [{
      "operation": "create",
      "name": "Test Task - Workflow Deployment",
      "status": "To-do",
      "priority": "Medium",
      "type": "Work"
    }],
    "projects": [],
    "calendar": []
  }'
```

**Test 3 - Project Update:**
```bash
curl -X POST https://n8n.oloxa.ai/webhook/brain-dump \
  -H "Content-Type: application/json" \
  -d '{
    "crm_updates": [],
    "tasks": [],
    "projects": [{
      "operation": "update",
      "name": "PA Agent Workflow",
      "phase": "Testing",
      "status": "Active"
    }],
    "calendar": []
  }'
```
