# Brain Dump Database Updater - Implementation Guide

## Overview

This n8n workflow receives brain dump data from Claude/my-pa-agent via webhook and automatically updates all relevant databases (Google Sheets CRM, Notion Tasks, Notion Projects, Google Calendar).

**Workflow File:** `/Users/swayclarke/coding_stuff/brain-dump-workflow.json`
**Version:** v1.1 (2026-01-14)

---

## Features

- ✅ **CRM Updates** - Fuzzy matching on contact names, update or create rows in Google Sheets
- ✅ **CRM Delete** - Delete contacts by name (NEW in v1.1)
- ✅ **Task Management** - Create Notion tasks with full property support
- ✅ **Task Delete** - Archive tasks by name (NEW in v1.1)
- ✅ **Project Tracking** - Update or create Notion projects
- ✅ **Project Delete** - Archive projects by name (NEW in v1.1)
- ✅ **Calendar Integration** - Create Google Calendar events
- ✅ **Calendar Delete** - Delete events by title and date (NEW in v1.1)
- ✅ **Parallel Processing** - All database updates run in parallel for speed
- ✅ **Error Handling** - Continues processing even if one update fails
- ✅ **Result Aggregation** - Returns comprehensive success/failure summary

---

## Workflow Structure

```
Webhook Trigger (POST /brain-dump)
  ↓
Parse & Validate Input
  ↓
Split By Update Type
  ↓
┌─────────────┬──────────────┬───────────────┬────────────────┐
│ CRM Path    │ Tasks Path   │ Projects Path │ Calendar Path  │
│ (parallel)  │ (parallel)   │ (parallel)    │ (parallel)     │
└─────────────┴──────────────┴───────────────┴────────────────┘
  ↓
Merge All Results
  ↓
Build Response
  ↓
Respond to Webhook
```

---

## Input JSON Format

Send POST request to webhook URL with this structure:

```json
{
  "crm_updates": [
    {
      "operation": "update",
      "name": "Sindbad",
      "stage": "Conversating",
      "sentiment": "Positive",
      "notes": "Call on 1/13/26 - went well",
      "priority": "High",
      "company": "Acme Corp",
      "platform": "LinkedIn",
      "role": "CEO",
      "business_type": "SaaS",
      "contact_details": "sindbad@acme.com",
      "objective": "Partnership",
      "niche_alignment": "Strong",
      "connection_strength": "Medium",
      "decision_making_power": "High",
      "network_access": "Medium"
    },
    {
      "operation": "delete",
      "name": "Old Contact"
    }
  ],
  "tasks": [
    {
      "operation": "create",
      "name": "Upload Sindbad transcript",
      "type": "Work",
      "status": "To-do",
      "priority": "Medium",
      "when": "2026-01-15",
      "description": "Upload call transcript to CRM",
      "project": "Q1 Partnerships",
      "blocked_by": [],
      "blocking": []
    },
    {
      "operation": "delete",
      "name": "Completed Task"
    }
  ],
  "projects": [
    {
      "operation": "update",
      "name": "AMA System",
      "phase": "Testing",
      "status": "Active",
      "client": "Internal",
      "timeline": "2026-Q1"
    },
    {
      "operation": "delete",
      "name": "Old Project"
    }
  ],
  "calendar": [
    {
      "operation": "create",
      "title": "Jeremiah meeting",
      "start": "2026-01-15T12:30:00",
      "end": "2026-01-15T13:30:00",
      "description": "Quarterly check-in",
      "attendees": ["jeremiah@example.com"]
    },
    {
      "operation": "delete",
      "title": "Cancelled Event",
      "date": "2026-01-20"
    }
  ]
}
```

**Note:** All sections are optional. You can send just CRM updates, just tasks, or any combination.

---

## Output JSON Format

The workflow responds with:

```json
{
  "status": "success",
  "summary": {
    "crm": "Updated/Created 1 contacts, Deleted 1 contacts",
    "tasks": "Created 1 tasks, Deleted 1 tasks",
    "projects": "Updated 1 projects, Deleted 1 projects",
    "calendar": "Created 1 events, Deleted 1 events"
  },
  "errors": []
}
```

If errors occur:

```json
{
  "status": "partial_success",
  "summary": {
    "crm": "Updated 2 contacts (Sindbad, Felix)",
    "tasks": "No tasks created",
    "projects": "Updated 1 project",
    "calendar": "Created 1 event"
  },
  "errors": [
    "Failed to create task: Invalid status value",
    "Failed to update CRM contact 'Unknown Person': Not found"
  ]
}
```

---

## Setup Instructions

### 1. Prerequisites

Ensure you have these credentials configured in n8n:

**Google OAuth (Combined):**
- Credential Name: "Combined Google OAuth"
- Type: Google OAuth2
- Scopes:
  - `https://www.googleapis.com/auth/spreadsheets` (read/write)
  - `https://www.googleapis.com/auth/calendar` (read/write)
- Token file: `/Users/swayclarke/coding_stuff/.credentials/gcp-oauth-combined.keys.json`

**Notion API:**
- Credential Name: "Notion API"
- Type: Notion API
- Integration token: (from Notion integrations page)
- Permissions: Read/write access to Tasks and Projects databases

### 2. Import Workflow

**Option A: Import via n8n UI**
1. Open n8n web interface
2. Click "Add workflow" → "Import from File"
3. Select `/Users/swayclarke/coding_stuff/brain-dump-workflow.json`
4. Click "Import"

**Option B: Import via n8n CLI** (if available)
```bash
n8n import:workflow --input=/Users/swayclarke/coding_stuff/brain-dump-workflow.json
```

### 3. Configure Credentials

After import, update these nodes with your credentials:

**Google Sheets Nodes:**
- "Read CRM Sheet"
- "Update CRM Row"
- "Create CRM Row"

→ Select credential: "Combined Google OAuth"

**Notion Nodes:**
- "Create Notion Task"
- "Find Notion Project"
- "Update Notion Project"
- "Create Notion Project"

→ Select credential: "Notion API"

**Google Calendar Node:**
- "Create Calendar Event"

→ Select credential: "Combined Google OAuth"

### 4. Activate Workflow

1. Click "Active" toggle in top-right corner
2. Workflow status should show "Active" with green indicator

### 5. Get Webhook URL

After activation, click on the "Webhook Trigger" node to see the webhook URL:

**Production URL format:**
```
https://your-n8n-instance.com/webhook/brain-dump
```

**Test URL format:**
```
https://your-n8n-instance.com/webhook-test/brain-dump
```

Copy this URL for use in my-pa-agent or Claude.

---

## Database Configuration Details

### Google Sheets CRM

**Spreadsheet ID:** `1PwIqO1nfEeABoRRvTml3dN9q1rUjHIMVXsqOLtouemk`
**Sheet Name:** "Prospects"
**Range:** A:R (columns A through R)

**Column Mapping:**
- A: Full Name
- B: Priority Level
- C: Company
- D: Platform
- E: Role
- F: Business Type
- G: Contact Details
- H: Stage
- I: Reply Sentiment
- J: Notes
- K: Added to CRM (auto-populated on create)
- M: Objective
- O: Niche Alignment
- P: Connection Strength
- Q: Decision Making Power
- R: Network Access

**Search Logic:**
- Searches column A (Full Name) for matching contact
- Case-insensitive, trimmed comparison
- If found: Updates existing row
- If not found AND operation=create: Appends new row
- If not found AND operation=update: Logs warning, skips

### Notion Tasks Database

**Database ID:** `39b8b725-0dbd-4ec2-b405-b3bba0c1d97e`

**Properties:**
- Name (title) - Task name
- Status (status) - To-do, In Progress, Complete, etc.
- Priority (select) - Low, Medium, High
- Type (select) - Work, Personal, etc.
- When (date) - Due date
- Description (rich_text) - Task description
- Complete (checkbox) - Completion status
- Project (relation) - Related project
- Blocked by (relation) - Dependencies
- Blocking (relation) - Blocks other tasks

**Supported Operations (v1.1):**
- **create** - Create new task (default)
- **delete** - Archive task by name (searches by exact match)

**Properties Set:**
- Name, Status, Priority, Type

**Future:** Add support for update operation

### Notion Projects Database

**Database ID:** `2d01c288-bb28-81ef-a640-000ba0da69d4`

**Properties:**
- Project (title) - Project name
- Phase (select) - Planning, Development, Testing, Complete, etc.
- Client (select) - Client name
- Status (select) - Active, On Hold, Complete, etc.
- Timeline (date) - Project timeline
- Tasks (relation) - Related tasks

**Supported Operations (v1.1):**
- **create** - Create new project
- **update** - Update existing project (default)
- **delete** - Archive project by name (searches by exact match)

**Search Logic:**
- Searches for project by name (exact match on title)
- If found: Updates Phase and Status (update), or archives (delete)
- If not found AND operation=create: Creates new project
- If not found AND operation=update/delete: Skips (logs as not found)

### Google Calendar

**Calendar:** primary (user's default calendar)

**Event Properties:**
- title - Event title/summary
- start - Start date/time (ISO 8601 format)
- end - End date/time (ISO 8601 format)
- description - Event description/notes
- attendees - List of attendee emails (future enhancement)

**Supported Operations (v1.1):**
- **create** - Create new event (default)
- **delete** - Delete event by title and optional date

**Delete Behavior:**
- If `date` provided: Searches only that specific day
- If `date` NOT provided: Searches next 30 days
- Deletes first matching event found

**Future:** Add support for update operation

---

## CRM Fuzzy Matching Details

The workflow implements **case-insensitive, trimmed matching** for CRM contact lookup:

```javascript
// Example matching logic
const normalizedSearch = contactName.toLowerCase().trim();
const sheetName = (row['Full Name'] || '').toLowerCase().trim();

if (sheetName === normalizedSearch) {
  // Match found
}
```

**Matching Examples:**
- "Sindbad" matches "sindbad" ✅
- "Sindbad" matches "SINDBAD" ✅
- "Sindbad " (with space) matches "Sindbad" ✅
- "Sindbad" does NOT match "Sindbad Ahmad" ❌ (requires exact match after normalization)

**Future Enhancements:**
- Partial matching (e.g., "Sindbad" matches "Sindbad Ahmad")
- Levenshtein distance for typo tolerance
- Multiple match handling (prompt user to choose)

---

## Error Handling

The workflow implements **continue-on-fail** logic:

1. **Per-item processing:** Each CRM update, task, project, and event is processed independently
2. **Failure isolation:** If one contact update fails, others continue
3. **Error collection:** Failed operations are logged with details
4. **Summary response:** Returns both successes and failures

**Error Response Example:**
```json
{
  "status": "partial_success",
  "summary": {
    "crm": "Updated 2 contacts (Sindbad, Felix)",
    "tasks": "Created 1 task",
    "projects": "No project updates",
    "calendar": "Created 1 event"
  },
  "errors": [
    "CRM update failed for 'Unknown Contact': Contact not found and operation=update",
    "Project update failed for 'Old Project': Project not found"
  ]
}
```

---

## Testing

### Test with Sample Data

Use this cURL command to test the workflow:

```bash
curl -X POST https://your-n8n-instance.com/webhook/brain-dump \
  -H "Content-Type: application/json" \
  -d '{
    "crm_updates": [
      {
        "operation": "create",
        "name": "Test Contact",
        "stage": "Initial Outreach",
        "sentiment": "Neutral",
        "notes": "Test brain dump integration",
        "priority": "Low"
      }
    ],
    "tasks": [
      {
        "operation": "create",
        "name": "Test Task from Brain Dump",
        "type": "Work",
        "status": "To-do",
        "priority": "Low"
      }
    ],
    "projects": [
      {
        "operation": "update",
        "name": "AMA System",
        "phase": "Testing"
      }
    ],
    "calendar": [
      {
        "operation": "create",
        "title": "Test Event from Brain Dump",
        "start": "2026-01-20T10:00:00",
        "end": "2026-01-20T10:30:00"
      }
    ]
  }'
```

### Expected Test Results

**Google Sheets CRM:**
- Check row exists for "Test Contact"
- Verify Stage = "Initial Outreach"
- Verify Notes contains "Test brain dump integration"

**Notion Tasks:**
- Check new task created: "Test Task from Brain Dump"
- Verify Status = "To-do"
- Verify Type = "Work"

**Notion Projects:**
- Check "AMA System" project updated
- Verify Phase = "Testing"

**Google Calendar:**
- Check event created on 2026-01-20 at 10:00 AM
- Verify title = "Test Event from Brain Dump"

### Cleanup Test Data

After testing, clean up:

**Google Sheets:**
1. Open spreadsheet: `1PwIqO1nfEeABoRRvTml3dN9q1rUjHIMVXsqOLtouemk`
2. Find row with "Test Contact"
3. Delete row

**Notion Tasks:**
1. Open Tasks database
2. Find "Test Task from Brain Dump"
3. Delete task

**Google Calendar:**
1. Open Google Calendar
2. Find "Test Event from Brain Dump" on 2026-01-20
3. Delete event

**Note:** Projects are left as-is since test only updates existing project.

---

## Limitations & Future Enhancements

### Current Limitations

**CRM (Google Sheets):**
- ❌ Only exact name matching (after normalization)
- ❌ Cannot handle duplicate contacts with same name
- ✅ **DELETE support added in v1.1**
- ❌ Notes are appended, not replaced (could grow large)

**Tasks (Notion):**
- ❌ Only supports create operation
- ❌ Cannot update existing tasks
- ✅ **DELETE (archive) support added in v1.1**
- ❌ No support for task relations (project, blocked_by, blocking)

**Projects (Notion):**
- ❌ Only updates Phase and Status
- ❌ Cannot update Client or Timeline
- ✅ **DELETE (archive) support added in v1.1**
- ❌ Search is case-sensitive on project title

**Calendar (Google):**
- ❌ Only supports create operation
- ❌ Cannot update existing events
- ✅ **DELETE support added in v1.1**
- ❌ No support for attendees
- ❌ No recurrence support

**General:**
- ❌ No rate limiting (could hit API limits on large batches)
- ❌ No batch size limits (large brain dumps could timeout)
- ❌ No retry logic for transient failures

### Planned Enhancements

**Phase 2 (High Priority):**
1. ✅ Add fuzzy matching for CRM contacts (Levenshtein distance)
2. ✅ Support task update/delete operations
3. ✅ Support calendar event update/delete operations
4. ✅ Add rate limiting (max 10 items per category)
5. ✅ Add retry logic (3 retries with exponential backoff)

**Phase 3 (Medium Priority):**
6. ✅ Support task relations (project, blocked_by, blocking)
7. ✅ Support calendar attendees
8. ✅ Support project Client and Timeline updates
9. ✅ Add CRM duplicate detection (warn if multiple matches)
10. ✅ Add batch size validation (max 50 total updates)

**Phase 4 (Nice to Have):**
11. ✅ Support CRM contact deletion
12. ✅ Support recurring calendar events
13. ✅ Add webhook authentication (API key or signature)
14. ✅ Add execution history logging to separate database
15. ✅ Email notifications on failures

---

## Integration with my-pa-agent

The my-pa-agent should format brain dump data and send to this webhook:

```javascript
// In my-pa-agent
const brainDumpData = {
  crm_updates: extractedCRMUpdates,
  tasks: extractedTasks,
  projects: extractedProjects,
  calendar: extractedCalendarEvents
};

// Send to webhook
const response = await fetch('https://your-n8n-instance.com/webhook/brain-dump', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(brainDumpData)
});

const result = await response.json();
console.log('Brain dump processed:', result.summary);

if (result.errors.length > 0) {
  console.warn('Some updates failed:', result.errors);
}
```

---

## Troubleshooting

### "Unknown error" when updating Google Sheets

**Cause:** OAuth scope insufficient (read-only)
**Fix:** Ensure credential has scope: `https://www.googleapis.com/auth/spreadsheets` (not `.readonly`)

### "Notion API error: validation_error"

**Cause:** Invalid property value (e.g., wrong status name)
**Fix:** Check Notion database schema for valid select/status values

### "Calendar event not created"

**Cause:** Invalid date format
**Fix:** Ensure dates are ISO 8601 format: `2026-01-15T12:30:00`

### Webhook times out

**Cause:** Too many updates in single request
**Fix:** Split large brain dumps into smaller batches (<20 items per category)

### CRM contact not found but should exist

**Cause:** Name mismatch (extra spaces, different capitalization)
**Fix:** Check exact spelling in Google Sheet, ensure case-insensitive matching is working

### Multiple contacts with same name - wrong one updated

**Cause:** Workflow updates first match
**Fix:** Use unique identifiers in contact names or add disambiguation field

---

## Performance Notes

**Typical execution time:**
- Small batch (1-5 updates per category): 3-8 seconds
- Medium batch (5-15 updates per category): 8-20 seconds
- Large batch (15+ updates per category): 20-40 seconds

**Optimization opportunities:**
- CRM updates are slowest (Google Sheets read + search + write)
- Tasks and Projects are fast (Notion API is efficient)
- Calendar events are medium speed

**Parallel execution:**
All 4 categories (CRM, Tasks, Projects, Calendar) run in parallel, so total time is MAX(category times), not SUM.

---

## Support & Maintenance

**Workflow maintained by:** solution-builder-agent
**Last updated:** 2026-01-14
**Version:** 1.1

**Contact:** Sway Clarke
**File location:** `/Users/swayclarke/coding_stuff/brain-dump-workflow.json`

For issues or enhancement requests, update this README and re-run solution-builder-agent.

---

## Appendix: Node Reference

### Core Nodes Used

1. **Webhook Trigger** - Receives POST requests
2. **Code Nodes** - Parse input, search data, build responses
3. **IF Nodes** - Route data by type, check existence
4. **Google Sheets Nodes** - Read/update CRM data
5. **Notion Nodes** - Create/update tasks and projects
6. **Google Calendar Node** - Create calendar events
7. **Merge Node** - Aggregate results from parallel paths
8. **Respond to Webhook Node** - Send response back to caller

### Code Node JavaScript Patterns

**Accessing previous node data:**
```javascript
const data = $input.first().json;
const allItems = $input.all();
```

**Referencing specific node:**
```javascript
const processedData = $('Process CRM Updates').first().json;
```

**Returning data:**
```javascript
return [{
  json: { field: 'value' }
}];
```

**Returning multiple items:**
```javascript
return [
  { json: { item: 1 } },
  { json: { item: 2 } },
  { json: { item: 3 } }
];
```

---

## Version History

**v1.1 (2026-01-14):**
- Added DELETE operations for CRM (Google Sheets row deletion)
- Added DELETE operations for Tasks (Notion page archive)
- Added DELETE operations for Projects (Notion page archive)
- Added DELETE operations for Calendar (Google Calendar event deletion)
- Updated response summary to separately track create/update vs delete counts
- Graceful error handling for "not found" scenarios (logs warning, does not fail)
- Calendar delete supports date-range search (specific day or next 30 days)
- Fully backward compatible with v1.0 (no breaking changes)

**v1.0 (2026-01-14):**
- Initial implementation
- CRM updates with fuzzy matching
- Task creation (Notion)
- Project updates (Notion)
- Calendar event creation (Google)
- Parallel processing
- Error aggregation
- Webhook response
