# /fix-n8n - Auto-Fix n8n Workflow Errors

Diagnose and fix errors in an n8n workflow. Runs the fix loop until the workflow executes successfully.

## Usage
```
/fix-n8n [workflow-id or name]
/fix-n8n [workflow-id] [specific issue to address]
```

## Examples
```
/fix-n8n sMy4DrgNnGSre6BD
/fix-n8n Eugene W2
/fix-n8n dHbwemg7hEB4vDmC the Google Drive node keeps failing
```

## What This Command Does

1. **Get Current State**
   - Fetch workflow structure
   - Get recent executions (especially errors)

2. **Identify Issues**
   - If recent error execution exists: analyze it
   - If user described issue: focus on that
   - If no errors: run a test to find issues

3. **Fix Loop** (autonomous)
   ```
   While errors exist:
     - Analyze error (node, message, context)
     - Determine fix
     - Apply fix via n8n_update_partial_workflow
     - Re-test
     - If still failing: analyze new error, repeat
   Until: Success OR max iterations (5) OR unfixable blocker
   ```

4. **Document**
   - Log each fix to `directives/n8n/learnings/errors-and-fixes.md`
   - Update N8N_PATTERNS.md if reusable pattern discovered

5. **Report**
   - Summary of all fixes applied
   - Final test result
   - Execution ID for verification

## Arguments

- `$ARGUMENTS` - Workflow ID/name + optional specific issue description

## Instructions for Claude

When this command is invoked:

1. **Identify workflow** (same as /test-n8n)

2. **Get error context**:
   ```
   # Check recent executions
   mcp__n8n-mcp__n8n_executions(
     action: "list",
     workflowId: "[id]",
     status: "error",
     limit: 3
   )

   # Get detailed error for most recent
   mcp__n8n-mcp__n8n_executions(
     action: "get",
     id: "[execution_id]",
     mode: "error"
   )
   ```

3. **If no recent errors**: Run a test first
   ```
   mcp__n8n-mcp__n8n_test_workflow(workflowId: "[id]", ...)
   ```

4. **Analyze error**:
   - `errorInfo.primaryError.nodeName` - which node failed
   - `errorInfo.primaryError.message` - what went wrong
   - `errorInfo.upstreamContext` - what data it received
   - `errorInfo.executionPath` - what succeeded before failure

5. **Determine fix** based on error type:

   | Error Pattern | Fix Approach |
   |---------------|--------------|
   | "Referenced node doesn't exist" | Fix node reference in Code node |
   | "Cannot read property X" | Fix data mapping/expression |
   | "unauthorized" / "token expired" | Refresh credentials (browser-ops-agent) |
   | "not found" (404) | Check resource IDs, paths |
   | "validation failed" | Fix required fields |
   | Node configuration error | Check node parameters |

6. **Apply fix**:
   ```
   mcp__n8n-mcp__n8n_update_partial_workflow(
     id: "[id]",
     operations: [
       {
         type: "updateNode",
         nodeId: "[failed_node_id]",
         updates: { ... }
       }
     ]
   )
   ```

7. **Re-test**:
   ```
   mcp__n8n-mcp__n8n_test_workflow(...)
   ```
   - If success: exit loop
   - If error: analyze new error, repeat (max 5 iterations)

8. **Document fix**:
   ```
   Edit directives/n8n/learnings/errors-and-fixes.md
   Add entry with: date, workflow, node, error, fix, pattern
   ```

9. **Report completion**:
   ```markdown
   ## Fix Complete

   **Workflow**: [Name] (ID: [id])
   **Iterations**: [N]

   **Fixes Applied**:
   1. [Node]: [what was wrong] → [what was fixed]
   2. [Node]: [what was wrong] → [what was fixed]

   **Final Test**: Execution #[id] - Success

   **Patterns Learned**:
   - [Any reusable insights added to learnings]

   Workflow is now operational.
   ```

   Or if unfixable:
   ```markdown
   ## Fix Blocked

   **Workflow**: [Name] (ID: [id])
   **Iterations**: [N]

   **Blocker**: [What couldn't be fixed automatically]
   - [e.g., "Credentials expired - need manual OAuth refresh"]
   - [e.g., "External API returning 500 - service may be down"]

   **Manual Action Required**:
   - [Steps for user to take]
   ```

## Key Rules

- **Max 5 iterations** - Prevents infinite loops
- **Log every fix** - Builds knowledge base
- **Real execution testing** - Every fix is verified with actual run
- **Credential issues** - Route to browser-ops-agent for OAuth refresh
- **Don't give up easily** - Try multiple approaches before declaring blocked
