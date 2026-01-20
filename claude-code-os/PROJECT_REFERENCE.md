# Project Reference - Sway's Configuration & Details

This file contains project-specific configuration, IDs, and rules. Referenced by CLAUDE.md.

---

## User Contact Information

**Name:** Sway

**Email Address:** swayclarkeii@gmail.com
- Used for all Gmail integrations
- Used in n8n workflows
- Used for testing automations

---

## Notion Integration

### Tasks Database

When referencing "to-do list", "tasks", or "my tasks", use this Notion database:

- **Database ID (legacy):** `889fff97-1c29-490b-a57c-322c0736e90a`
- **Data Source ID (new API):** `39b8b725-0dbd-4ec2-b405-b3bba0c1d97e`
- **URL:** https://www.notion.so/889fff971c29490ba57c322c0736e90a

### Oloxa Projects Database

Client and project tracking database:

- **Database ID (legacy):** `2d01c288-bb28-81f6-a1be-e57188992200`
- **Data Source ID (new API):** `2d01c288-bb28-81ef-a640-000ba0da69d4`
- **URL:** https://www.notion.so/2d01c288bb2881f6a1bee57188992200

### Notion API 2025-09-03 Changes

The Notion API changed significantly on 2025-09-03. Key changes:
- **Databases vs Data Sources**: Now separate concepts - databases are containers, data sources hold the schema/content
- **Page creation**: Requires `data_source_id` instead of `database_id` in parent
- **Querying**: Use `mcp__notion__API-query-data-source` with data_source_id

**Old format (deprecated):**
```json
{"parent": {"type": "database_id", "database_id": "889fff97..."}}
```

**New format (2025-09-03+):**
```json
{"parent": {"type": "data_source_id", "data_source_id": "39b8b725..."}}
```

### Notion MCP Configuration

✅ **Status: Fully working - Both databases accessible (as of Jan 8, 2026)**

**Current Configuration (~/.claude.json):**
```json
"notion": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@notionhq/notion-mcp-server"],
  "env": {
    "NOTION_TOKEN": "ntn_J75587080087TBhkjcxsZBYMUajbCtySV0xnp1xgPH57SC"
  }
}
```

**Environment Variable Requirements:**
- Official package (`@notionhq/notion-mcp-server`) requires `NOTION_TOKEN` (NOT `NOTION_API_KEY`)
- Alternative package (`@suekou/mcp-notion-server`) uses `NOTION_API_KEY`

**Integration Token:**
- Name: "Claude Code MCP"
- Token: `ntn_I755870800881mojWR2QcilFkl0VLOc0UMGTJrmuBw78BZ`

### Known MCP Server Bug

⚠️ **NOTE**: The official Notion MCP server (`@notionhq/notion-mcp-server`) had a known bug where object parameters like `parent` get double-stringified. This causes page creation to fail with:
```
body.parent should be an object or undefined, instead was "{\"type\":...
```

**Current Status (Jan 8, 2026):**
- ✅ Server connection: Working
- ✅ Reading/querying data: Working
- ⚠️ Creating pages: Not tested yet (bug may still exist)

**If page creation fails:**
1. Add tasks/pages directly in Notion UI
2. Check bug status: https://github.com/makenotion/notion-mcp-server/issues/82

### Efficient Querying

Use `mcp__notion__API-query-data-source` with the data_source_id:

```
data_source_id: "39b8b725-0dbd-4ec2-b405-b3bba0c1d97e"
filter: { "property": "Complete", "checkbox": { "equals": false } }
page_size: 20
```

### Key Properties in Tasks Database

- **Name** (title): Task name
- **Complete** (checkbox): Whether task is done
- **Status** (status): Current state (To-do, Doing, Done)
- **When** (date): Due date
- **Priority** (select): Task priority
- **Project** (relation): Related project
- **Area** (relation): Life area

### Task Status Management Rules

**CRITICAL**: When updating Notion tasks, ALWAYS update BOTH the "Complete" checkbox AND the "Status" field together:

1. **When user is working on a task:**
   - Set Status to "Doing": `{"Status": {"status": {"name": "Doing"}}}`
   - Keep Complete as false: `{"Complete": {"checkbox": false}}`

2. **When task is complete/done:**
   - Set Status to "Done": `{"Status": {"status": {"name": "Done"}}}`
   - Set Complete to true: `{"Complete": {"checkbox": true}}`

3. **Default behavior:**
   - When user says "mark as done" or "complete": Update BOTH Status to "Done" AND Complete to true
   - When user says "I'm working on": Update Status to "Doing"
   - This ensures tasks move correctly in the Kanban board

**Example updates:**
```
# Marking task as done:
{"Complete": {"checkbox": true}, "Status": {"status": {"name": "Done"}}}

# Starting work on task:
{"Status": {"status": {"name": "Doing"}}}
```

---

## Eugene AMA Document Organizer Workflows

**Project:** Document organization system for AMA Capital real estate deals

### Active n8n Workflows

| Workflow Name | ID | Status | Purpose |
|--------------|-----|--------|---------|
| Pre-Chunk 0 - REBUILT v1 | `YGXWjWcBIk66ArvT` | ✅ ACTIVE | Gmail trigger → PDF extraction → Client name identification |
| Chunk 0: Folder Initialization (V4 - Parameterized) | `zbxHkXOoD1qaz6OS` | ✅ ACTIVE | Create 37-folder client structure in Google Drive |
| Chunk 2: Text Extraction | `qKyqsL64ReMiKpJ4` | ✅ ACTIVE | Extract text from PDFs using GPT-4 Vision |
| Chunk 2.5: Client Document Tracking | `okg8wTqLtPUwjQ18` | ✅ ACTIVE | Classify documents, route to correct folders |
| Test Email Sender - swayfromthehook to swayclarkeii | `RZyOIeBy7o3Agffa` | ✅ ACTIVE | Send test emails with PDF attachments |
| Autonomous Test Runner - Chunk Integration | `K1kYeyvokVHtOhoE` | ✅ ACTIVE | Automated testing for workflow integration |

### Google Sheets

| Sheet Name | Spreadsheet ID | Purpose |
|-----------|----------------|---------|
| Client_Registry | `1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI` | Master client data registry |
| AMA_Folder_IDs | `1-CPnCr3locAORVX5tUEoh6r0i-x3tQ_ROTN0VXatOAU` | Folder ID mappings |
| Test Results | `1af9ZsSm5IDVWIYb5IMX8ys8a5SUUnQcb77xi9tJQVo8` | Automated test outcomes tracking |

### Google Drive Folders

| Folder Name | Folder ID | Purpose |
|-------------|-----------|---------|
| Client Root (Parent) | `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm` | Container for all client folder structures |
| dummy_files | `1GG_OCKvT1ivR0F-uIVq0b1jhHreWg1Kh` | Test PDF files for workflow testing |

### Gmail Configuration

**Test Account:** swayfromthehook@gmail.com
- Used for: Sending test emails with PDF attachments
- Credential ID (Gmail): `g2ksaYkLXWtfDWAh`
- Credential ID (Google Drive): `PGGNF2ZKD2XqDhe0`

**Production Account:** swayclarkeii@gmail.com
- Used for: Receiving emails from Eugene's team
- Trigger for Pre-Chunk 0 workflow

### Known Issues

**⚠️ CRITICAL - PDFs Not Going to _Staging Folder:**
- **Problem:** PDFs being uploaded to wrong folder (not client `_Staging` folder)
- **Current behavior:** Files going to "N8 and underscore testing folder"
- **Expected behavior:** Files should go to client-specific `_Staging` subfolder
- **Status:** Active investigation (Jan 4, 2026)

**⚠️ Webhook Trigger Not Working:**
- **Workflow:** Test Email Sender (RZyOIeBy7o3Agffa)
- **Webhook URL:** `https://n8n.oloxa.ai/webhook/0743d128-ce67-4a01-9d8f-37b369708d48`
- **Status:** Workflow active, but webhook doesn't trigger execution
- **Workaround:** Manual execution from n8n UI

### Project Documentation

**Location:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/compacting-summaries/`

**Key Files:**
- `PROJECT_STATE_v1.3_20260104.md` - Current status and completed fixes
- `VERSION_LOG.md` - Complete version history
- `N8N_Blueprints/` - Exported workflow JSON files

---

## Daily Updates & Progress Tracking

### CRITICAL DISTINCTION: Tasks vs Updates

**Tasks** → Notion Tasks Database (889fff97-1c29-490b-a57c-322c0736e90a):
- Action items with due dates
- Things that need to be completed
- Personal todos (shoes to return, books to read, etc.)
- Examples: "Upload coach feedback", "Return shoes", "Schedule call"

**Updates** → MY-JOURNEY.md (/Users/swayclarke/coding_stuff/claude-code-os/00-progress-advisor/MY-JOURNEY.md):
- All client and project progress
- Business learnings and insights
- Call summaries and key takeaways
- Milestones achieved
- Strategy decisions made
- System improvements built
- Examples: "Lombok Task 2 V4 approved", "Jennifer call insights", "Built Google Slides automation"

### Automatic Update Rules

When the user provides ANY update about:
- Client progress (Eugene, Lombok Capital, Jennifer & Fernandez, etc.)
- Project status changes
- Calls completed or insights gained
- Systems or automation built
- Business learnings or realizations

**AUTOMATICALLY do BOTH:**
1. Add relevant tasks to Notion (if there are action items)
2. Document the update in MY-JOURNEY.md in the appropriate section:
   - Add to "Milestones Log" (date + brief summary)
   - Create/update detailed entry in "Notes & Insights" section
   - Add key learnings to "What I'm Learning" section

**DO NOT wait for the user to ask** - proactively update MY-JOURNEY.md whenever they share progress.

### MY-JOURNEY.md Structure to Update

1. **Milestones Log**: Add date + brief entry (one line)
2. **What I'm Learning**: Add any new insights or lessons (bullet points)
3. **Notes & Insights**: Add dated section with detailed breakdown of:
   - Client/project progress
   - Key decisions made
   - Systems built
   - Learnings extracted
   - Next actions identified

Use the current date in "Month Day, Year" format (e.g., "January 4, 2026") for all entries.

---

## Global Versioning System

### CRITICAL: Automatic Versioning for All New Projects

When building ANY new system, automation, agent, workflow, or significant documentation:

**AUTOMATICALLY create a VERSION_LOG.md** in the project folder using the template at:
`/Users/swayclarke/coding_stuff/claude-code-os/VERSION_TEMPLATE.md`

**DO NOT wait for Sway to ask** - proactively create version tracking for all builds.

### What Requires a VERSION_LOG.md

**Always create VERSION_LOG.md for:**
- n8n workflows and automation systems
- New client projects (Eugene, Lombok, etc.)
- Agent prompt templates and skills
- Integration systems (Google, Notion, etc.)
- Any multi-component build with blueprints/exports
- Documentation systems with multiple versions

**When to create it:**
- At project initialization (v0.0.0 draft state)
- BEFORE building the first component
- As part of project setup, not after completion

### Semantic Versioning Rules

**MAJOR.MINOR.PATCH format:**
- **MAJOR (v1.0.0)**: Breaking changes, complete rewrites, major milestones
- **MINOR (v1.1.0)**: New features, enhancements, backward compatible
- **PATCH (v1.0.1)**: Bug fixes, small improvements, refinements

**When to increment:**
- New n8n workflow added = MINOR version
- Workflow node parameter change = PATCH version
- Complete system rewrite = MAJOR version
- Blueprint export at milestone = Document in current version

### VERSION_LOG.md Requirements

**Every VERSION_LOG.md MUST include:**
1. **Quick Reference Table** - Current version, status, date
2. **Versioning Scheme** - MAJOR.MINOR.PATCH definitions
3. **Complete Version History** - All versions with:
   - Components created/modified
   - What works / What doesn't work
   - Known issues and blockers
   - Rollback instructions
   - Files & resources (IDs, URLs, paths)
4. **Component Inventory** - All Google Drive IDs, n8n workflow IDs, Sheet IDs
5. **Rollback Procedures** - Step-by-step for each component type
6. **Blueprint Naming Convention** - How to name exported files

### Blueprint File Naming

**Standard format:** `{component}_v{version}_{date}.json`

**Examples:**
- `chunk0_v1.2_parameterized_20251230.json`
- `test_orchestrator_v1.0_20251230.json`

**Archived files:** `_archived/{component}_v{version}_{date}_ARCHIVED.json`

### Version Update Workflow

**At each milestone:**
1. Export all n8n workflows as JSON to `N8N_Blueprints/v{major}_{phase}/` folder
2. Update VERSION_LOG.md with new version entry
3. Archive old blueprint files to `_archived/` folder
4. Update component inventory with new IDs
5. Document rollback procedures for the new version
6. Test that rollback to previous version works

### Decentralized Architecture

- Each project manages its own VERSION_LOG.md
- No global version index (doesn't scale)
- Use `Glob **/VERSION_LOG.md` to discover all versioned projects
- Generate on-demand reports when Sway asks "show me all versioned projects"

### Integration with MY-JOURNEY.md

When reaching major milestones (v1.0, v2.0, etc.):
- Update VERSION_LOG.md with technical details
- Update MY-JOURNEY.md with business context and learnings
- VERSION_LOG.md = technical rollback and component tracking
- MY-JOURNEY.md = business progress and insights
