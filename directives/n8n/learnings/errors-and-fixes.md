# n8n Errors and Fixes Log

This document captures errors encountered during agentic building and their fixes.
The system learns from each fix to avoid repeating mistakes.

---

## Format

```
### [Date] - [Error Type]
**Workflow**: [Name/ID]
**Node**: [Node name]
**Error**: [Error message]
**Root Cause**: [Why it happened]
**Fix**: [What fixed it]
**Pattern**: [Reusable lesson]
```

---

## Log

### 2026-01-27 - Referenced Node Doesn't Exist
**Workflow**: Agentic Loop Test - POC v2 (sMy4DrgNnGSre6BD)
**Node**: Process Data (Code node)
**Error**: `Referenced node doesn't exist` when using `$("Missing Node")`
**Root Cause**: Code node tried to reference a node name that doesn't exist in the workflow
**Fix**: Changed `$("Missing Node").first().json` to `$input.first().json.body`
**Pattern**: In Code nodes, use `$input` to reference the previous node's output, or use exact node names that exist in the workflow.

### 2026-01-27 - Webhook Not Registered
**Workflow**: Agentic Loop Test - POC (fkNxdiPz5oJWoU5U)
**Node**: Webhook
**Error**: `The requested webhook "POST agentic-test" is not registered`
**Root Cause**: Workflow created via API but missing `webhookId` field; database activation doesn't register webhook listeners
**Fix**:
1. Add `webhookId` to webhook node via `n8n_update_partial_workflow`
2. Deactivate then activate via API (not database)
3. Or restart n8n after proper API activation
**Pattern**: Webhooks need `webhookId` field and must be activated via n8n API (not database UPDATE) for listeners to register.

---

## Common Patterns

### Webhook Workflows
- Always include `webhookId` (UUID) in webhook nodes
- Activate via API `/api/v1/workflows/{id}/activate`, not database
- Test with `n8n_test_workflow` after activation

### Code Nodes
- Use `$input.first().json` for previous node data
- Use `$("Exact Node Name")` only for named nodes that exist
- Webhook data is in `$input.first().json.body`

### OAuth/Credentials
- Credential errors show as "unauthorized" or "token expired"
- Use browser-ops-agent to refresh OAuth
- Credential names are case-sensitive

---

## Statistics
- Total errors logged: 2
- Most common: [To be updated as patterns emerge]
