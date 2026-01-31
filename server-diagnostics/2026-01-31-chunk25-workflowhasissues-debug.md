# Debug Log Analysis - Chunk 2.5 WorkflowHasIssuesError

## Date
2026-01-31

## Issue
Workflow okg8wTqLtPUwjQ18 (Chunk 2.5) fails with "WorkflowHasIssuesError" when executed via Execute Workflow node.

## Investigation Steps Performed

1. **Enabled debug logging**: Set N8N_LOG_LEVEL=debug in docker-compose.yml
2. **Restarted n8n**: Full restart to apply debug logging
3. **Triggered test**: Executed webhook eugene-quick-test
4. **Captured logs**: Searched for issue/error/validation messages

## Key Log Findings

### Error Stack Trace
```
WorkflowHasIssuesError: The workflow has issues and cannot be executed for that reason. Please fix them first.
    at WorkflowExecute.checkForWorkflowIssues (/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-core@file+packages+core_@opentelemetry+api@1.9.0_@opentelemetry+sdk-trace-base@1.30_ec37920eb95917b28efaa783206b20f3/node_modules/n8n-core/src/execution-engine/workflow-execute.ts:1328:10)
    at WorkflowExecute.processRunExecutionData (/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-core@file+packages+core_@opentelemetry+api@1.9.0_@opentelemetry+sdk-trace-base@1.30_ec37920eb95917b28efaa783206b20f3/node_modules/n8n-core/src/execution-engine/workflow-execute.ts:1407:8)
```

### Execution Timeline (Execution ID: 7348)
```
2026-01-31T00:03:21.303Z | debug | Start executing node "Execute Chunk 2.5" {"node":"Execute Chunk 2.5","workflowId":"fIqmtfEDuYM7gbE9"}
2026-01-31T00:03:21.304Z | debug | Running node "Execute Chunk 2.5" started {"node":"Execute Chunk 2.5","workflowId":"fIqmtfEDuYM7gbE9"}
2026-01-31T00:03:21.333Z | debug | Execution added {"executionId":"7348"}
2026-01-31T00:03:21.347Z | debug | Workflow execution started {"workflowId":"okg8wTqLtPUwjQ18"}
2026-01-31T00:03:21.393Z | debug | Execution finalized {"executionId":"7348"}
2026-01-31T00:03:21.394Z | debug | Execution removed {"executionId":"7348"}
2026-01-31T00:03:21.414Z | error | The workflow has issues and cannot be executed for that reason. Please fix them first.
2026-01-31T00:03:21.415Z | debug | Running node "Execute Chunk 2.5" finished with error {"node":"Execute Chunk 2.5","workflowId":"fIqmtfEDuYM7gbE9"}
```

### Workflow Activation Logs
```
2026-01-31T00:02:55.467Z | debug | Added triggers and pollers for workflow "Chunk 2.5 - Client Document Tracking (Eugene Document Organizer)" (ID: okg8wTqLtPUwjQ18) {"scopes":["workflow-activation"]}
2026-01-31T00:02:55.475Z | info  | Activated workflow "Chunk 2.5 - Client Document Tracking (Eugene Document Organizer)" (ID: okg8wTqLtPUwjQ18) {"scopes":["workflow-activation"]}
```

## Critical Observations

1. **Workflow activated successfully** - The workflow okg8wTqLtPUwjQ18 activates without errors during n8n startup
2. **Execution starts** - Workflow execution ID 7348 is created and starts
3. **Immediate failure** - Execution is finalized and removed within 61ms (7348 added at .333, removed at .394)
4. **No specific node/issue logged** - Debug logging does NOT reveal which node or what specific issue triggered the error
5. **checkForWorkflowIssues at line 1328** - The error is thrown from workflow-execute.ts:1328 during the workflow validation phase

## What Debug Logging Did NOT Show

**CRITICAL**: Despite debug logging being enabled, the logs do NOT contain:
- Which specific node has the issue
- What type of issue (missing parameter, invalid expression, etc.)
- Any validation error details
- The workflow's `issues` object contents

This suggests the error is thrown in `checkForWorkflowIssues()` but the details are not logged at debug level.

## Next Investigation Steps

Since debug logging didn't reveal the specific issue, recommend:

1. **Direct workflow inspection**: Use n8n_validate_workflow MCP tool to get detailed validation results
2. **Check workflow structure**: Get full workflow JSON and examine each node's configuration
3. **Compare with working workflow**: Check if Chunk 2.5 has different node types or configurations than working sub-workflows
4. **Source code review**: The checkForWorkflowIssues function throws the error but doesn't log details - may need to add custom logging or check the workflow's `issues` property directly via MCP

## Hypothesis

Based on the immediate failure (61ms) and lack of specific error details:
- This is a **validation/configuration issue**, not an execution issue
- The workflow likely has a node with missing required parameters or invalid configuration
- The issue is detected during the pre-execution validation phase (`checkForWorkflowIssues`)
- The n8n UI may show the issue visually (red error indicators on nodes)

## Status

- Debug logging enabled: ✅ Complete
- Test execution triggered: ✅ Complete
- Logs captured: ✅ Complete
- Log level restored: ✅ Complete
- Specific issue identified: ❌ **Not found in logs**

## Recommendation

Use **n8n_validate_workflow** MCP tool to get structured validation results that should reveal the specific node and issue type.
