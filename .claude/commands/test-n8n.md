# /test-n8n - Test n8n Workflow Execution

Execute an n8n workflow and report results. Quick way to verify a workflow works.

## Usage
```
/test-n8n [workflow-id or name]
/test-n8n [workflow-id] with [test data description]
```

## Examples
```
/test-n8n sMy4DrgNnGSre6BD
/test-n8n Eugene W2
/test-n8n dHbwemg7hEB4vDmC with sample receipt email
```

## What This Command Does

1. **Identify Workflow**
   - Get workflow by ID or search by name
   - Verify it exists and has a webhook trigger

2. **Prepare Test Data**
   - If user provided test data description, generate appropriate payload
   - If not, use minimal valid payload for the webhook

3. **Execute**
   - Ensure workflow is active
   - Trigger via `n8n_test_workflow`
   - Wait for completion

4. **Report Results**
   - Success: Show execution ID, output data, nodes executed
   - Error: Show failed node, error message, execution path

## Arguments

- `$ARGUMENTS` - Workflow ID, name, or project reference + optional test data

## Instructions for Claude

When this command is invoked:

1. **Parse the workflow reference**:
   - If looks like ID (alphanumeric, ~16 chars): use directly
   - If name/project: search with `n8n_list_workflows` or check known projects

2. **Get workflow details**:
   ```
   mcp__n8n-mcp__n8n_get_workflow(id, mode="structure")
   ```
   - Verify it has webhook/form/chat trigger
   - If no executable trigger: report "Cannot test - no webhook trigger"

3. **Ensure active**:
   - If not active, activate via API

4. **Prepare test data**:
   - Default: `{"test": true, "timestamp": "[current time]"}`
   - If user described data, generate appropriate JSON

5. **Execute**:
   ```
   mcp__n8n-mcp__n8n_test_workflow(
     workflowId: "[id]",
     triggerType: "webhook",
     data: [test payload],
     waitForResponse: true
   )
   ```

6. **Report results**:

   **On Success**:
   ```markdown
   ## Test Passed

   **Workflow**: [Name] (ID: [id])
   **Execution**: #[execution_id]
   **Status**: Success
   **Duration**: [X]ms

   **Output**:
   ```json
   [response data]
   ```

   **Nodes Executed**: [list]
   ```

   **On Error**:
   ```markdown
   ## Test Failed

   **Workflow**: [Name] (ID: [id])
   **Execution**: #[execution_id]
   **Status**: Error

   **Failed Node**: [node name]
   **Error**: [message]

   **Execution Path**:
   1. [Node] - Success
   2. [Node] - Success
   3. [Node] - ERROR

   **Upstream Data** (what the failed node received):
   ```json
   [sample items]
   ```

   **Suggested Fix**: [If obvious from error]

   Run `/fix-n8n [id]` to auto-fix this error.
   ```

## Key Rules

- **Real execution** - This triggers actual workflow execution on n8n server
- **Visible in n8n** - User can watch execution in n8n.oloxa.ai Executions tab
- **Quick feedback** - Just tests once, doesn't loop/fix (use /fix-n8n for that)
