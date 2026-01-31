# n8n Workflow Activation Error Report

## Issue Details
- **Workflow ID**: JFzIwurZQCf2zui7
- **Error**: "Could not find property option"
- **Date**: 2026-01-30
- **Server**: n8n.oloxa.ai (157.230.21.230)

## Error Stack Trace

```
Error: Could not find property option
    at getNodeParameters (/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-workflow@file+packages+workflow/node_modules/n8n-workflow/src/node-helpers.ts:900:14)
    at /usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-workflow@file+packages+workflow/node_modules/n8n-workflow/src/telemetry-helpers.ts:461:46
    at Array.forEach (<anonymous>)
    at Object.generateNodesGraph (/usr/local/lib/node_modules/n8n/node_modules/.pnpm/n8n-workflow@file+packages+workflow/node_modules/n8n-workflow/src/telemetry-helpers.ts:236:13)
    at TelemetryEventRelay.workflowSaved (/usr/local/lib/node_modules/n8n/src/events/relays/telemetry.event-relay.ts:633:42)
    at workflow-saved (/usr/local/lib/node_modules/n8n/src/events/relays/telemetry.event-relay.ts:91:50)
    at EventService.<anonymous> (/usr/local/lib/node_modules/n8n/src/events/relays/event-relay.ts:19:11)
    at EventService.emit (node:events:531:35)
    at EventService.emit (/usr/local/lib/node_modules/n8n/src/typed-emitter.ts:38:16)
    at WorkflowService.update (/usr/local/lib/node_modules/n8n/src/workflows/workflow.service.ts:419:21)
```

## Root Cause Analysis

### Location
The error occurs in n8n's telemetry/analytics system, specifically:
- **File**: `n8n-workflow/src/node-helpers.ts` line 900
- **Function**: `getNodeParameters()`
- **Trigger**: When workflow is saved (event: `workflow-saved`)
- **Process**: `TelemetryEventRelay.workflowSaved()` -> `generateNodesGraph()`

### What's Happening
1. When you save or activate a workflow, n8n tries to generate telemetry data
2. The `generateNodesGraph()` function iterates through all nodes
3. For each node, it calls `getNodeParameters()` to extract parameter info
4. `getNodeParameters()` tries to find a "property option" that doesn't exist
5. This crashes the telemetry process and blocks the workflow save/activation

### Why This Happens
The error "Could not find property option" typically means:
- **A node has a parameter configuration that references a non-existent option**
- **A dropdown/select parameter is referencing an invalid value**
- **A node property definition is malformed or missing**

### Critical Detail
This error happens during **telemetry generation**, NOT during workflow execution. This means:
- The workflow might actually be valid and executable
- The telemetry system is choking on a specific node's parameter structure
- This is preventing the workflow from being saved/activated

## Evidence from Logs

The error appears multiple times in the logs:
- Occurs on **workflow-saved** events (when activating or updating)
- Also occurs on **workflow-created** events (when creating new workflows)
- Pattern shows this affects multiple workflows, not just one

Other log entries show:
```
Disabled MCP access for deactivated workflow
Problem with execution 7039: The workflow has issues and cannot be executed for that reason. Please fix them first.
```

This suggests the workflow validation system is correctly detecting the issue and blocking execution.

## Recommended Fix

### Option 1: Find the Problematic Node (Recommended)
The error is in `getNodeParameters()` which processes node parameters. Look for:
1. **Dropdown/select fields with invalid values**
2. **Resource/operation pairs where the operation doesn't exist for that resource**
3. **Node parameters that reference deleted or renamed options**

### Option 2: Check Recent Node Changes
Since this is workflow JFzIwurZQCf2zui7, check:
- What nodes were recently added or modified?
- Were any node parameters changed via API (MCP tools)?
- Are there any custom/community nodes that might have configuration issues?

### Option 3: Disable Telemetry (Workaround)
If the workflow is functionally correct, this might be a telemetry-only issue. However, disabling telemetry is not recommended as it's a system-wide change.

## Next Steps

1. **Review the workflow structure** - Identify which node is causing the telemetry error
2. **Check node parameters** - Look for dropdown values that don't match available options
3. **Validate node configuration** - Ensure all required fields are properly set
4. **Test fix** - Try re-saving the workflow after fixing the problematic parameter

## Server Health
- **n8n Container**: Running
- **PostgreSQL**: Running
- **Caddy**: Running
- **Overall Status**: Healthy (other workflows working)

## Additional Observations

The logs also show:
- Multiple "Task rejected by Runner" errors (unrelated to this issue - likely AI task runner timeouts)
- UptimeRobot health checks being blocked (expected behavior)
- Unknown webhook "fathom-test" request (separate test issue)

---

**Report Generated**: 2026-01-30
**Server**: n8n.oloxa.ai
**Investigated By**: server-ops-agent
