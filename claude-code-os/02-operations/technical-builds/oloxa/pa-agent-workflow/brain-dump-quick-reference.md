# Brain Dump Workflow - Quick Reference

## Files

- **Workflow JSON:** `/Users/swayclarke/coding_stuff/brain-dump-workflow.json`
- **Full Documentation:** `/Users/swayclarke/coding_stuff/brain-dump-workflow-README.md`
- **This Reference:** `/Users/swayclarke/coding_stuff/brain-dump-quick-reference.md`

---

## Import to n8n

1. Open n8n web interface
2. Click "Add workflow" → "Import from File"
3. Select `/Users/swayclarke/coding_stuff/brain-dump-workflow.json`
4. Configure credentials (see below)
5. Activate workflow
6. Copy webhook URL

---

## Credentials Required

**Google OAuth (Combined):**
- Name: "Combined Google OAuth"
- File: `/Users/swayclarke/coding_stuff/.credentials/gcp-oauth-combined.keys.json`
- Scopes: spreadsheets, calendar (read/write)

**Notion API:**
- Name: "Notion API"
- Type: Notion API
- Get token from: https://www.notion.so/my-integrations

---

## Webhook URL

After activation, webhook URL will be:

**Production:**
```
https://your-n8n-instance.com/webhook/brain-dump
```

**Test:**
```
https://your-n8n-instance.com/webhook-test/brain-dump
```

---

## Usage

**Send POST request with JSON body:**

```json
{
  "crm_updates": [
    {"operation": "update", "name": "Sindbad", "stage": "Conversating", "notes": "Call went well"}
  ],
  "tasks": [
    {"operation": "create", "name": "Upload transcript", "type": "Work", "status": "To-do"}
  ],
  "projects": [
    {"operation": "update", "name": "AMA System", "phase": "Testing"}
  ],
  "calendar": [
    {"operation": "create", "title": "Meeting", "start": "2026-01-15T12:30:00", "end": "2026-01-15T13:30:00"}
  ]
}
```

**Response:**

```json
{
  "status": "success",
  "summary": {
    "crm": "Updated 1 contact (Sindbad)",
    "tasks": "Created 1 task",
    "projects": "Updated 1 project",
    "calendar": "Created 1 event"
  },
  "errors": []
}
```

---

## Database IDs

**Google Sheets CRM:**
- Spreadsheet: `1PwIqO1nfEeABoRRvTml3dN9q1rUjHIMVXsqOLtouemk`
- Sheet: "Prospects"

**Notion Tasks:**
- Database: `39b8b725-0dbd-4ec2-b405-b3bba0c1d97e`

**Notion Projects:**
- Database: `2d01c288-bb28-81ef-a640-000ba0da69d4`

**Google Calendar:**
- Calendar: "primary"

---

## Test Command

```bash
curl -X POST https://your-n8n-instance.com/webhook/brain-dump \
  -H "Content-Type: application/json" \
  -d '{
    "crm_updates": [{"operation": "create", "name": "Test Contact", "stage": "Initial", "notes": "Test"}],
    "tasks": [{"operation": "create", "name": "Test Task", "type": "Work", "status": "To-do"}]
  }'
```

---

## Common Issues

**"Unknown error" on Google Sheets:**
→ Check OAuth scope includes `spreadsheets` (not `.readonly`)

**Notion validation error:**
→ Check property values match database schema

**Webhook timeout:**
→ Send smaller batches (<20 items per category)

**CRM contact not found:**
→ Check exact spelling (case-insensitive matching)

---

## What Works

✅ CRM update existing contacts
✅ CRM create new contacts
✅ Create Notion tasks
✅ Update Notion projects
✅ Create Notion projects
✅ Create Google Calendar events
✅ Parallel processing (fast!)
✅ Error handling (continues on failure)
✅ Summary response

## Not Yet Implemented

❌ Update existing tasks
❌ Delete tasks
❌ Update calendar events
❌ Delete calendar events
❌ Task relations (project, blocked_by, blocking)
❌ Calendar attendees
❌ CRM duplicate detection
❌ Rate limiting
❌ Retry logic

See full README for planned enhancements.

---

## Next Steps

1. **Import workflow to n8n**
2. **Configure credentials**
3. **Activate workflow**
4. **Test with sample data**
5. **Integrate with my-pa-agent**
6. **Monitor execution logs**
7. **Report issues or request enhancements**

---

For complete documentation, see: `/Users/swayclarke/coding_stuff/brain-dump-workflow-README.md`
