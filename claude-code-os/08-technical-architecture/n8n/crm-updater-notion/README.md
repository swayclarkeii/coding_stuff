# CRM Updater - Notion Integration

## Overview
- **Platform:** n8n
- **Workflow ID:** `d2oR8FiBQMXedJYT`
- **Status:** Built and validated (inactive, ready for testing)
- **Created:** January 3, 2026
- **Blueprint:** `crm_updater_v1.0_20260103.json`

## Workflow Structure

### Trigger
- **Webhook** - POST endpoint at `/crm-updater`
  - Receives JSON payload with `taskName` and `projectName`
  - Error handling enabled (continues on error)

### Main Steps
1. **Create Notion Task** - Creates task in Notion Tasks database
   - Database ID: `39b8b725-0dbd-4ec2-b405-b3bba0c1d97e`
   - Title: Extracted from `$json.body.taskName`
   - Credential: "Notion API 2"

2. **Create Notion Project** - Creates project in Notion Projects database
   - Database ID: `2d01c288bb2881f6a1bee57188992200`
   - Title: Extracted from `$json.body.projectName`
   - Credential: "Notion API 2"

3. **Respond to Webhook** - Returns success response
   - JSON format with task and project details

## Configuration Notes

### Credentials Used
- **Notion API 2** (ID: `Sutx4Kyf49uSMEgO`)
  - Used for both Create Notion Task and Create Notion Project nodes
  - Must be configured in n8n before activating workflow

### Important Mappings
- Webhook body → Task title: `={{ $json.body.taskName }}`
- Webhook body → Project title: `={{ $json.body.projectName }}`
- Response includes both created items

### Database IDs
- **Tasks Database:** `39b8b725-0dbd-4ec2-b405-b3bba0c1d97e` (data source ID)
- **Projects Database:** `2d01c288bb2881f6a1bee57188992200` (data source ID)

### Notion Node Configuration
- Using correct resourceLocator format: `{mode: "id", value: "database-id"}`
- TypeVersion: 2.2 (latest)
- Resource: "databasePage"
- Operation: "create"

## Testing

### Happy-Path Test
**Input:**
```json
POST http://your-n8n-instance/webhook/crm-updater
Content-Type: application/json

{
  "taskName": "Follow up with client",
  "projectName": "Eugene Proposal"
}
```

**Expected Output:**
```json
{
  "success": true,
  "message": "CRM updated successfully",
  "task": {
    "id": "notion-page-id",
    "properties": {...}
  },
  "project": {
    "id": "notion-page-id",
    "properties": {...}
  }
}
```

### How to Run Test
1. Activate workflow in n8n UI (toggle switch)
2. Get webhook URL from the Webhook node
3. Send POST request using curl, Postman, or any HTTP client:
   ```bash
   curl -X POST http://your-n8n-url/webhook/crm-updater \
     -H "Content-Type: application/json" \
     -d '{"taskName": "Test Task", "projectName": "Test Project"}'
   ```
4. Check Notion databases to verify task and project were created
5. Verify response contains both created items

## Handoff

### How to Modify
- **Change database targets:** Update `databaseId` values in Notion nodes
- **Add more properties:** Use `propertiesUi.propertyValues` array to add custom fields
- **Change webhook path:** Update `path` parameter in Webhook node

### Known Limitations
- Only creates basic pages with titles (no additional properties configured)
- No validation of input data (webhook accepts any JSON)
- No duplicate checking (creates new items every time)
- Sequential execution (task created before project, not parallel)

### Error Handling
- Webhook has `onError: continueRegularOutput` enabled
- If either Notion node fails, error will propagate to webhook response
- No retry logic configured

### Next Steps
- **Testing:** Activate workflow and test with real data
- **Enhancement:** Add property mapping for task status, dates, priorities
- **Validation:** Add data validation before creating Notion items
- **Optimization:** Consider parallel execution if tasks/projects are independent

### Activation Checklist
1. ✅ Verify "Notion API 2" credential exists in n8n
2. ✅ Confirm database IDs are correct
3. ⬜ Activate workflow (toggle switch in n8n UI)
4. ⬜ Get webhook URL from Webhook node
5. ⬜ Test with sample data
6. ⬜ Verify items appear in Notion databases

## Technical Details

### Node Versions
- Webhook: typeVersion 2.1 (latest)
- Notion: typeVersion 2.2 (latest)
- Respond to Webhook: typeVersion 1.5 (latest)

### Validation Results
- ✅ Valid workflow structure
- ✅ All connections valid
- ✅ All expressions validated
- ✅ Error handling configured
- ⚠️ No additional error nodes (consider adding Error Trigger for monitoring)

### Workflow Settings
- Execution order: v1
- Caller policy: workflowsFromSameOwner
- MCP available: false
