# /build-n8n - Autonomous n8n Workflow Builder

Build or modify n8n workflows autonomously. Runs the full agentic loop:
Design → Build → Test → Fix → Repeat until success.

## Usage
```
/build-n8n [description of what you want]
```

## Examples
```
/build-n8n webhook that receives form data and saves to Airtable
/build-n8n modify Eugene W2 to also process image attachments
/build-n8n scheduled workflow that checks Slack for unanswered messages daily
```

## What This Command Does

1. **Understand the Goal**
   - Parse your description into a directive
   - Identify: trigger type, inputs, outputs, integrations needed

2. **Design (if new workflow)**
   - Route to idea-architect-agent for solution brief
   - Skip if modifying existing workflow

3. **Build**
   - Route to solution-builder-agent
   - Create/modify workflow via n8n MCP tools
   - Ensure webhook trigger exists for testing

4. **Test**
   - Route to test-runner-agent
   - Execute workflow via `n8n_test_workflow`
   - Retrieve results/errors via `n8n_executions`

5. **Fix (if errors)**
   - Analyze error with `n8n_executions mode="error"`
   - Fix via `n8n_update_partial_workflow`
   - Document fix in `directives/n8n/learnings/errors-and-fixes.md`
   - Go back to step 4

6. **Complete**
   - Report success with execution ID
   - Provide workflow URL for verification
   - Suggest next steps

## Autonomous Behavior

This command runs **without asking for permission** at each step.
It will iterate until:
- Workflow executes successfully, OR
- It hits a blocker it cannot solve (e.g., missing credentials, external API down)

If blocked, it will explain what's needed and stop.

## Arguments

- `$ARGUMENTS` - Your description of what to build/modify

## Instructions for Claude

When this command is invoked:

1. **Parse the request**: Extract what the user wants to build or modify.

2. **Check for existing workflow**: If user mentions a workflow name/ID or project name (like "Eugene"), look up the existing workflow ID.

3. **For NEW workflows**:
   ```
   Task(idea-architect-agent): "Design a solution brief for: [user request]"
   → Get solution brief
   Task(solution-builder-agent): "Build this workflow: [solution brief]. Include webhook trigger for testing."
   → Get workflow ID
   Task(test-runner-agent): "Test workflow [ID] with sample data"
   → If error: continue to fix loop
   → If success: report done
   ```

4. **For EXISTING workflows**:
   ```
   mcp__n8n-mcp__n8n_get_workflow: Get current state
   Task(solution-builder-agent): "Modify workflow [ID]: [user request]"
   Task(test-runner-agent): "Test workflow [ID]"
   → If error: continue to fix loop
   → If success: report done
   ```

5. **Fix loop** (runs automatically):
   ```
   While execution fails:
     - Get error via n8n_executions mode="error"
     - Analyze: which node failed, why
     - Fix via n8n_update_partial_workflow
     - Log fix to directives/n8n/learnings/errors-and-fixes.md
     - Re-test
   ```

6. **Report completion**:
   ```markdown
   ## Build Complete

   **Workflow**: [Name] (ID: [id])
   **URL**: https://n8n.oloxa.ai/workflow/[id]
   **Status**: Active and tested

   **Iterations**: [N] (list any errors fixed)

   **Test Execution**: #[execution_id] - Success

   **What it does**:
   - [Trigger]: [description]
   - [Step 1]: [description]
   - [Step 2]: [description]

   **Next steps**:
   - [Any follow-up suggestions]
   ```

## Key Rules

- **Always add webhook trigger** for new workflows (required for API testing)
- **Always test after building** - never mark complete without successful execution
- **Log every fix** to the learnings file
- **Don't ask permission** - run autonomously until done or blocked
- **Show progress** - update TodoWrite as you work through steps
