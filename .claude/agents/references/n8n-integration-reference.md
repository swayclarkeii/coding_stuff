---
name: n8n Integration Reference
description: Reference guide for n8n service integrations and API connections
---

# n8n Integration Reference

**Purpose**: Quick reference for architecture-feasibility-agent and solution-builder-agent to validate integration capabilities without bloating agent prompts.

**Last Verified**: January 3, 2026
**Verification Method**: All integrations confirmed via `mcp__n8n-mcp__search_nodes` and `mcp__n8n-mcp__get_node`

---

## How to Use This Reference

1. **Quick lookup**: Check if integration exists and basic capabilities
2. **Verify specifics**: Use `mcp__n8n-mcp__get_node` for detailed operations
3. **Stay current**: Update this file as new nodes are discovered

---

## Core Integrations (Verified ✅)

### Google Workspace

**Google Drive** (`n8n-nodes-base.googleDrive`)
- **Operations**: File (copy, delete, download, move, upload, share), Folder (create, delete, list), Shared Drives (create, delete, get, list, update)
- **Authentication**: OAuth2 (recommended) or Service Account
- **Version**: typeVersion 3 (latest)
- **Key Feature**: Resource locator with modes: list, url, id
- **Known Limitation**: Search requires scoping to folder (see CLAUDE.md - don't search 70K+ files)

**Google Sheets** (`n8n-nodes-base.googleSheets`)
- **Operations**: Read, update, write data
- **Authentication**: OAuth2
- **Trigger Available**: Yes (`n8n-nodes-base.googleSheetsTrigger`)
- **Use Case**: Data storage, reporting, automation data source

**Google Docs** (`n8n-nodes-base.googleDocs`)
- **Operations**: Create, read, update documents
- **Authentication**: OAuth2
- **Use Case**: Document generation, content management

**Google Calendar** (`n8n-nodes-base.googleCalendar`)
- **Operations**: Event management, calendar operations
- **Authentication**: OAuth2
- **Trigger Available**: Yes (`n8n-nodes-base.googleCalendarTrigger`)

**Gmail** (`n8n-nodes-base.gmail`)
- **Operations**: Send, read, delete, search emails
- **Authentication**: OAuth2
- **AI Tool Variant**: Yes (`n8n-nodes-base.gmailTool`)
- **Use Case**: Email automation, notifications

**Google Slides** (`n8n-nodes-base.googleSlides`)
- **Operations**: Create, update presentations
- **Authentication**: OAuth2
- **Use Case**: Presentation generation, visual content

### Productivity & Databases

**Notion** (`n8n-nodes-base.notion`)
- **Operations**: Database operations, page operations
- **Authentication**: OAuth2 or API Key
- **Trigger Available**: Yes (`n8n-nodes-base.notionTrigger`)
- **Critical**: Use data_source_id for v2025-09-03+ API (see CLAUDE.md)
- **Use Case**: Task management, knowledge base, CRM

**Airtable** (`n8n-nodes-base.airtable`)
- **Operations**: Read, update, write, delete records
- **Authentication**: OAuth2 or API Key
- **Trigger Available**: Yes (`n8n-nodes-base.airtableTrigger`)
- **Use Case**: Database operations, flexible data storage

**Slack** (`n8n-nodes-base.slack`)
- **Operations**: Message posting, channel management, user operations
- **Authentication**: OAuth2
- **Trigger Available**: Yes (`n8n-nodes-base.slackTrigger`)
- **Use Case**: Team notifications, collaboration

### Core n8n Nodes

**Webhook** (`n8n-nodes-base.webhook`)
- **Type**: Trigger node
- **Purpose**: Starts workflow when HTTP request received
- **Authentication**: Optional (can use header auth, query auth, etc.)
- **Use Case**: External system triggers, form submissions, API endpoints

**Respond to Webhook** (`n8n-nodes-base.respondToWebhook`)
- **Type**: Response node
- **Purpose**: Send HTTP response back to webhook caller
- **Use Case**: API responses, synchronous workflows

**HTTP Request** (`n8n-nodes-base.httpRequest`)
- **Type**: Action node
- **Purpose**: Make HTTP requests to any API
- **Authentication**: Many methods (OAuth2, API Key, Basic Auth, etc.)
- **Use Case**: Custom API integrations, RESTful services

---

## n8n Cloud Tiers (General Reference)

**Starter Tier**:
- Execution limits per month
- Basic integrations
- Community support

**Pro Tier**:
- Higher execution limits
- Advanced integrations
- Priority support

**Enterprise Tier**:
- Custom execution limits
- SSO, advanced security
- Dedicated support
- Custom SLAs

⚠️ **Note**: For exact pricing and limits, use `WebFetch` to check current n8n.io pricing page during feasibility reviews.

---

## Self-Hosted Considerations

**When to Recommend Self-Hosted**:
- Long-running workflows (hours)
- Large file processing (GB+)
- Custom security requirements
- Heavy parallel executions

**When to Recommend Cloud**:
- Quick setup needed
- Standard workflows
- Client doesn't want to manage infrastructure
- Moderate execution volume

**Infrastructure Requirements** (self-hosted):
- Minimum: 1GB RAM, 1 CPU for basic workflows
- Recommended: 2GB+ RAM, 2+ CPU for production
- Database: PostgreSQL (recommended) or SQLite (dev only)
- Storage: Depends on file processing volume

---

## Known n8n Limitations (from CLAUDE.md)

### splitInBatches Loop Issue
**Problem**: `$('NodeName').all()` inside splitInBatches loops only returns the last iteration, not accumulated data.

**Solution**: Use a separate node after the loop completes to fetch all accumulated data.

**Example**:
```
❌ Wrong: Inside splitInBatches loop → Use $('CollectData').all()
✅ Correct: After loop completes → Use separate node to aggregate
```

### Google Drive Search Scoping
**Problem**: Searching entire "My Drive" can scan 70K+ files (slow, hits rate limits).

**Solution**: Always scope searches to specific folders using `folderId` parameter with `recursive: true`.

**Example**:
```javascript
{
  "folderId": {
    "__rl": true,
    "value": "={{$('Create Root Folder').first().json.id}}",
    "mode": "id"
  },
  "options": {
    "recursive": true
  }
}
```

### Expression Format
**Requirement**: All n8n expressions must use `={{...}}` format.

**Examples**:
- ✅ `={{$json.fieldName}}`
- ✅ `={{$('NodeName').first().json.id}}`
- ❌ `$json.fieldName` (missing =)

---

## Common Workflow Patterns

### Pattern 1: Webhook → Transform → Action
```
Webhook (trigger)
  → Code/Function (transform data)
  → Google Sheets/Notion/etc (action)
  → Respond to Webhook (response)
```

### Pattern 2: Scheduled → Fetch → Process → Store
```
Schedule Trigger
  → HTTP Request/API (fetch data)
  → Code/Filter (process)
  → Database/Sheet (store)
```

### Pattern 3: Form → Validate → Branch → Notify
```
Webhook (form submission)
  → Code (validate)
  → IF (branch)
    → Valid: Create record + Send email
    → Invalid: Log error + Send rejection
```

---

## How Agents Should Use This File

### architecture-feasibility-agent:
1. **Read this file first** in Step 2 (Integration check)
2. **Quick lookup**: Check if integration is listed here
3. **If found**: Note capabilities from this file
4. **If unclear**: Use `mcp__n8n-mcp__search_nodes` to search
5. **If need details**: Use `mcp__n8n-mcp__get_node` for full schema
6. **If not in n8n**: Suggest alternative (HTTP Request node, different platform)

### solution-builder-agent:
1. **Read this file** before building workflows
2. **Reference patterns**: Use common workflow patterns section
3. **Check limitations**: Review "Known n8n Limitations" before using splitInBatches or Google Drive
4. **Verify nodes**: Use `mcp__n8n-mcp__search_nodes` if integration not listed
5. **Get schemas**: Use `mcp__n8n-mcp__get_node` for exact parameters

---

## Maintenance Protocol

**When to update this file**:
- New integration discovered via MCP tools
- n8n node version changes (e.g., typeVersion update)
- Known limitation found in production
- Pricing tier changes from n8n.io

**How to update**:
1. Verify with `mcp__n8n-mcp__search_nodes` or `get_node`
2. Update relevant section
3. Add "Last Verified" date at top
4. Document verification method

**Don't include**:
- Unverified integrations (guesses)
- Deprecated nodes without confirmation
- Third-party community nodes (unless explicitly tested)

---

## Quick Reference Table

| Integration | Node Type | Trigger? | AI Tool? | Auth |
|------------|-----------|----------|----------|------|
| Google Drive | `n8n-nodes-base.googleDrive` | No | No | OAuth2/SA |
| Google Sheets | `n8n-nodes-base.googleSheets` | Yes | No | OAuth2 |
| Google Docs | `n8n-nodes-base.googleDocs` | No | Yes | OAuth2 |
| Google Calendar | `n8n-nodes-base.googleCalendar` | Yes | No | OAuth2 |
| Gmail | `n8n-nodes-base.gmail` | No | Yes | OAuth2 |
| Google Slides | `n8n-nodes-base.googleSlides` | No | No | OAuth2 |
| Notion | `n8n-nodes-base.notion` | Yes | No | OAuth2/Key |
| Airtable | `n8n-nodes-base.airtable` | Yes | Yes | OAuth2/Key |
| Slack | `n8n-nodes-base.slack` | Yes | No | OAuth2 |
| Webhook | `n8n-nodes-base.webhook` | Yes | No | Optional |
| HTTP Request | `n8n-nodes-base.httpRequest` | No | No | Various |

**Legend**:
- Trigger: Node has a trigger variant available
- AI Tool: Node has AI agent variant
- SA: Service Account
- Key: API Key authentication

---

## Need More Detail?

For detailed node documentation, operation lists, or exact parameters:

```javascript
// Search for nodes
mcp__n8n-mcp__search_nodes({
  query: "google sheets",
  limit: 10
})

// Get full node details
mcp__n8n-mcp__get_node({
  nodeType: "nodes-base.googleSheets",
  detail: "standard"  // or "full" for everything
})

// Get tool documentation
mcp__n8n-mcp__tools_documentation({
  topic: "get_node",
  depth: "full"
})
```
