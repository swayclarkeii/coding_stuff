---
name: n8n Patterns
description: Technical reference for n8n MCP operations, token efficiency guidelines, and workflow patterns
---

# n8n Patterns & Technical Reference

Technical reference for n8n MCP operations. Referenced by CLAUDE.md.

---

## Token Efficiency Guidelines

### n8n_get_workflow Mode Costs

| Mode | Token Cost | Use When |
|------|------------|----------|
| `minimal` | ~200 tokens | Check if workflow exists, is active, or get basic metadata |
| `details` | ~500 tokens | Get metadata + execution stats |
| `structure` | ~2,000 tokens | See node names and connection topology only |
| `full` | ~13,000 tokens | Need complete node parameters for building/debugging |

### Best Practices (Follow These Always)

1. ✅ **Ask user first** - If user likely knows the answer, ask instead of calling MCP
2. ✅ **Start with minimal mode** - Use `mode: "minimal"` to check workflow status
3. ✅ **Use structure for topology** - Only when you need to see workflow flow
4. ✅ **Reserve full mode** - Only for building/debugging node configurations
5. ✅ **One call per task** - Don't call structure then full; go straight to what you need

### Anti-Patterns (Never Do These)

- ❌ Calling `mode: "structure"` then `mode: "full"` in same conversation
- ❌ Using `mode: "full"` just to check if workflow is active
- ❌ Using `mode: "full"` to verify a single parameter value
- ❌ Getting workflow data when user can answer the question
- ❌ Calling MCP to check something visible in previous conversation context

### Examples

**❌ WASTEFUL (15,000+ tokens):**
```javascript
// Just to check Gmail Trigger labels
mcp__n8n-mcp__n8n_get_workflow({ id: "...", mode: "structure" })  // 2,000 tokens
mcp__n8n-mcp__n8n_get_workflow({ id: "...", mode: "full" })       // 13,000 tokens
```

**✅ EFFICIENT:**
```javascript
// Ask user: "Which labels does the Gmail Trigger monitor?"
// OR if you must verify:
mcp__n8n-mcp__n8n_get_workflow({ id: "...", mode: "minimal" })    // 200 tokens
```

**When to use each mode:**
- **minimal**: "Is this workflow active?" "Does this workflow exist?"
- **details**: "How many times has this run?" "When was it last updated?"
- **structure**: "Which nodes connect to which?" "What's the workflow flow?"
- **full**: "What are the exact parameters for this Gmail node?" "I need to copy node config"

---

## n8n_update_partial_workflow Syntax

### Common Mistakes to AVOID

- ❌ Using `sourceNode` and `targetNode` (WRONG)
- ❌ Using `sourceOutput: 0` as number (WRONG)
- ❌ Guessing parameter names instead of checking docs

### Correct Syntax

- ✅ Use `source` and `target` for node names
- ✅ Use `sourceOutput: "main"` as string
- ✅ Use exact node names (case-sensitive)

### Operation Types

#### Adding a Node
```javascript
{
  "type": "addNode",
  "node": {
    "name": "List All Folders",
    "type": "n8n-nodes-base.googleDrive",
    "parameters": {
      "resource": "folder",
      "operation": "getAll",
      "driveId": {"__rl": true, "mode": "list", "value": "My Drive"},
      "folderId": {"__rl": true, "value": "={{$('Create Root Folder').first().json.id}}", "mode": "id"},
      "options": {"recursive": true}
    },
    "position": [1000, 500]
  }
}
```

#### Adding a Connection
```javascript
{
  "type": "addConnection",
  "source": "Loop Subfolders",          // Exact source node name
  "sourceOutput": "done",               // Output name (string)
  "target": "List All Folders",         // Exact target node name
  "targetInput": "main"                 // Input name (string, usually "main")
}
```

#### Updating Node Code
```javascript
{
  "type": "updateNode",
  "nodeName": "Collect Folder IDs",
  "updates": {
    "parameters": {
      "jsCode": "// Updated JavaScript code here"
    }
  }
}
```

### Real-World Example

**Task**: Add a Google Drive "List All Folders" node between "Loop Subfolders" and "Collect Folder IDs"

**Correct Implementation**:
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow({
  id: "Ui2rQFpMu9G1RTE1",
  operations: [
    {
      type: "addNode",
      node: {
        name: "List All Folders",
        type: "n8n-nodes-base.googleDrive",
        parameters: {
          resource: "folder",
          operation: "getAll",
          driveId: {__rl: true, mode: "list", value: "My Drive"},
          folderId: {__rl: true, value: "={{$('Create Root Folder').first().json.id}}", mode: "id"},
          options: {recursive: true}
        },
        position: [1000, 500]
      }
    },
    {
      type: "addConnection",
      source: "Loop Subfolders",
      sourceOutput: "done",
      target: "List All Folders",
      targetInput: "main"
    },
    {
      type: "addConnection",
      source: "List All Folders",
      sourceOutput: "main",
      target: "Collect Folder IDs",
      targetInput: "main"
    }
  ]
})
```

---

## Important n8n Workflow Patterns

### splitInBatches Loop Limitation

**Problem**: `$('NodeName').all()` DOES NOT work inside splitInBatches loops
- It only returns the **last iteration**, not accumulated data
- **Solution**: Use a separate node to fetch all data after loops complete

**Example**:
```javascript
// ❌ WRONG - Inside splitInBatches loop
const allData = $('Previous Node').all();  // Only gets last iteration

// ✅ CORRECT - After loop completes
{
  type: "addNode",
  node: {
    name: "Collect All Results",
    type: "n8n-nodes-base.code",
    parameters: {
      jsCode: "return $('Previous Node').all();"
    }
  }
}
```

### Google Drive Search Scoping

**Problem**: Unscoped searches scan entire My Drive (70K+ files, performance issue)

**Solution**: ALWAYS scope searches to specific folders using `folderId` parameter

**Example - Scoped Folder Search**:
```javascript
{
  "folderId": {
    "__rl": true,
    "value": "={{$('Create Root Folder').first().json.id}}",  // Scope to specific folder
    "mode": "id"
  },
  "options": {
    "recursive": true  // Get all subfolders within scope
  }
}
```

**Best Practices**:
- Always use `folderId` to limit search scope
- Use `recursive: true` to get all subfolders within scope
- Never search "My Drive" root without folder scoping
- Performance: Scoped search = <1s, Unscoped = 30+ seconds

---

## Common n8n MCP Tools

### Getting Workflow Data
```javascript
mcp__n8n-mcp__n8n_get_workflow({
  id: "workflow_id",
  mode: "minimal"  // or "details", "structure", "full"
})
```

### Updating Workflows
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow({
  id: "workflow_id",
  operations: [/* array of operations */]
})
```

### Validating Workflows
```javascript
mcp__n8n-mcp__n8n_validate_workflow({
  id: "workflow_id",
  options: {
    validateNodes: true,
    validateConnections: true,
    validateExpressions: true
  }
})
```

### Getting Node Information
```javascript
mcp__n8n-mcp__get_node({
  nodeType: "n8n-nodes-base.googleDrive",
  detail: "standard",  // or "minimal", "full"
  mode: "info"  // or "docs", "search_properties"
})
```

### Searching for Nodes
```javascript
mcp__n8n-mcp__search_nodes({
  query: "google drive",
  limit: 20,
  includeExamples: true
})
```

---

## Documentation Reference

**Always check documentation first** when unsure about command syntax:
```javascript
mcp__n8n-mcp__tools_documentation({
  topic: "n8n_update_partial_workflow",
  depth: "full"
})
```

**Available topics**:
- `n8n_update_partial_workflow` - Update workflow operations
- `n8n_get_workflow` - Get workflow data
- `search_nodes` - Find n8n nodes
- `get_node` - Node information
- `validate_workflow` - Workflow validation
