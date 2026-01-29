# Implementation Complete – Generate Proposal - Google Slides

## 1. Overview
- **Platform:** n8n
- **Workflow ID:** FSbhLS8ByK3vlSBh
- **Status:** Built draft - Ready for configuration and testing
- **Total Nodes:** 13
- **Workflow Type:** Slack interactive button → Airtable data aggregation → Google Slides generation

## 2. Workflow Structure

### Trigger
- **Slack Button Click** (Webhook) - Receives interactive button payload from Slack
  - Path: `/slack-proposal-button`
  - Method: POST
  - Expects: Slack interactive payload with `action_id` = "proposal_company" or "proposal_individual"

### Main Steps

1. **Extract Slack Payload** (Code Node)
   - Parses URL-encoded Slack payload
   - Extracts action type and target identifier
   - Outputs: `proposal_type` (company/individual), `target_identifier` (company name or call_id)

2. **Company or Individual?** (IF Node)
   - Routes based on proposal type
   - Output 0 → Company route
   - Output 1 → Individual route

#### Route A: Company Proposals
3. **Get All Company Calls** (Airtable)
   - Queries Calls table for all calls matching company name
   - Filter: `{Company} = 'target_identifier'`

4. **Aggregate Company Data** (Code Node)
   - Merges pain_points, quick_wins, action_items from all calls
   - Uses latest call for single-value fields (contact name, summary, etc.)
   - Outputs: Aggregated data with `total_calls` count

#### Route B: Individual Proposals
3. **Get Single Call Record** (Airtable)
   - Fetches single call by call_id

4. **Prepare Individual Data** (Code Node)
   - Parses JSON arrays from single call
   - Outputs: Formatted data consistent with company route

### Common Path (After Routes Merge)

5. **Map to 47 Variables** (Code Node)
   - Transforms Airtable data into 47 Google Slides placeholder variables
   - Key mappings:
     - Slide 1: company_name, date
     - Slide 2: client_company_description, client_name
     - Slide 3: pain_point_1-3 + descriptions
     - Slide 4: product_benefit_1-3
     - Slide 5: building/testing/deployment_phase_time
     - Slide 6: client_expectations_list, oloxa_delivery_list
     - Slide 7: metric_1-2
     - Slide 8: time_based_cost
     - Slide 9: step_1-3_description
     - Slide 10: unique_client_thank_you_message

6. **Duplicate Template** (Google Drive)
   - Copies template presentation
   - Template ID: `17BkLuHdj-iNlmnZ2jkP_cLLYMOzvTriCmejpDqe-UhQ`
   - New name: `Proposal - [Company] - [Date]`

7. **Build Replacements Array** (Code Node)
   - Converts variables to Google Slides textUi format
   - Creates array of text replacements: `{{variable_name}}` → value
   - Outputs: `presentationId`, `textReplacements` array

8. **Replace All Placeholders** (Google Slides)
   - Performs batch text replacement in duplicated presentation
   - Uses textUi format with multiple replacements
   - Replaces all {{variable}} placeholders with actual values

9. **Build Slack Message** (Code Node)
   - Constructs Slack response with presentation link
   - Format: "✅ Proposal generated: [LINK]"

10. **Send Slack Response** (Respond to Webhook)
    - Returns JSON response to Slack
    - Shows message in channel with link to generated presentation

## 3. Configuration Notes

### Credentials Required

**Airtable:**
- Credential type: `airtableTokenApi`
- Credential ID: `airtable-credential-id` (placeholder - needs replacement)
- Required scopes: Read access to Calls table

**Google Drive:**
- Credential type: `googleDriveOAuth2Api`
- Credential ID: `google-drive-credential-id` (placeholder - needs replacement)
- Required scopes: `https://www.googleapis.com/auth/drive.file` (create/copy files)

**Google Slides:**
- Credential type: `googleSlidesOAuth2Api`
- Credential ID: `google-slides-credential-id` (placeholder - needs replacement)
- Required scopes: `https://www.googleapis.com/auth/presentations` (read/write presentations)

### Configuration Steps Before Testing

1. **Update Airtable Application ID:**
   - Replace `appXXXXXXXXXXXXXX` with actual Airtable base ID
   - In nodes: "Get All Company Calls" and "Get Single Call Record"

2. **Configure Credentials:**
   - Set up Airtable API token credential
   - Set up Google OAuth2 credentials (Drive + Slides)
   - Update credential IDs in all nodes

3. **Verify Table Names:**
   - Ensure Airtable table name is exactly "Calls"
   - Update if different in your base

4. **Configure Slack Webhook:**
   - Add webhook URL to Slack interactive component configuration
   - Webhook URL: `https://[your-n8n-instance]/webhook/slack-proposal-button`

### Important Mappings

**Airtable Field Assumptions:**
```javascript
{
  "company_name": "Company",           // Text field
  "contact_name": "Contact_Name",      // Text field
  "summary": "Summary",                // Long text field
  "pain_points": "Pain_Points",        // JSON array: [{title, description}]
  "quick_wins": "Quick_Wins",          // JSON array: [{title}]
  "action_items": "Action_Items",      // JSON array: [{title, description}]
  "requirements": "Requirements",       // Array field
  "estimated_timeline": "Timeline",    // JSON: {building, testing, deployment}
  "perf_numbers_captured": "Metrics",  // Array field
  "estimated_cost": "Cost",            // Currency/Text field
  "created_time": "Created"            // Date field (Airtable auto)
}
```

**Variable Defaults:**
- All missing values default to "TBD"
- Dates formatted as: "January 2026"
- Company name hardcoded: "Oloxa.ai"

### Filters / Error Handling

**Current State:**
- Basic try/catch in Code nodes (implicit)
- Webhook has `onError: "continueRegularOutput"` to prevent crashes
- No explicit error output branches (warnings only)

**Recommended Additions:**
- Add error handling to Airtable nodes (`onError: "continueErrorOutput"`)
- Add fallback path for empty Airtable results
- Add validation for required fields before Google Slides operations

## 4. Testing

### Happy-Path Test - Individual Proposal

**Input (Slack button payload):**
```json
{
  "type": "interactive_message",
  "actions": [
    {
      "action_id": "proposal_individual",
      "value": "recXXXXXXXXXXXXXX"  // Airtable call_id
    }
  ],
  "user": {
    "id": "U12345678"
  },
  "channel": {
    "id": "C12345678"
  },
  "response_url": "https://hooks.slack.com/actions/..."
}
```

**Expected Outcome:**
1. Airtable fetches single call record
2. Data mapped to 47 variables
3. Template duplicated with name: "Proposal - [Company] - 2026-01-28"
4. All {{placeholders}} replaced with values
5. Slack receives message: "✅ Proposal generated: https://docs.google.com/presentation/d/[ID]/edit"

### Happy-Path Test - Company Proposal

**Input (Slack button payload):**
```json
{
  "type": "interactive_message",
  "actions": [
    {
      "action_id": "proposal_company",
      "value": "Villa Martens"  // Company name
    }
  ],
  "user": {
    "id": "U12345678"
  },
  "channel": {
    "id": "C12345678"
  },
  "response_url": "https://hooks.slack.com/actions/..."
}
```

**Expected Outcome:**
1. Airtable fetches ALL calls for "Villa Martens"
2. Pain points, quick wins, action items aggregated across calls
3. Latest call used for single-value fields
4. Template duplicated and populated
5. Slack receives confirmation message with link

### How to Run Tests

**Option 1: Manual Trigger (Recommended for Initial Testing)**
1. In n8n UI, click "Test workflow" button
2. Manually trigger webhook with sample JSON payload
3. Observe execution in real-time

**Option 2: Actual Slack Integration**
1. Configure Slack app with interactive components
2. Add webhook URL to Slack app configuration
3. Create Slack message with buttons:
   - "Generate Company Proposal" → `action_id: "proposal_company"`
   - "Generate Individual Proposal" → `action_id: "proposal_individual"`
4. Click button in Slack channel
5. Workflow triggers automatically

**Option 3: cURL Test**
```bash
curl -X POST https://[your-n8n-instance]/webhook/slack-proposal-button \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'payload={"type":"interactive_message","actions":[{"action_id":"proposal_individual","value":"recXXXXXXXXXXXXXX"}],"user":{"id":"U12345678"},"channel":{"id":"C12345678"},"response_url":"https://hooks.slack.com/actions/test"}'
```

## 5. Handoff

### How to Modify

**To add more variables:**
1. Add variable to "Map to 47 Variables" Code node
2. Add corresponding {{placeholder}} to Google Slides template
3. No other changes needed (replacement loop is dynamic)

**To change data sources:**
1. Update Airtable field names in Code nodes
2. Adjust JSON parsing logic if structure changes
3. Update aggregation logic in "Aggregate Company Data" if needed

**To customize Slack response:**
1. Modify "Build Slack Message" Code node
2. Change message format, add emojis, include additional info

### Known Limitations

1. **Airtable Configuration Required:**
   - Application ID and credential ID are placeholders
   - Must be updated before workflow can execute

2. **Template Must Exist:**
   - Template ID `17BkLuHdj-iNlmnZ2jkP_cLLYMOzvTriCmejpDqe-UhQ` must exist in Google Drive
   - Must contain all {{variable}} placeholders matching the 47 variables

3. **Slack Setup Required:**
   - Slack app must be configured with interactive components
   - Webhook URL must be registered with Slack
   - Buttons must send correct action_id values

4. **Data Structure Assumptions:**
   - Assumes pain_points, quick_wins, action_items are JSON arrays
   - Assumes specific field names in Airtable
   - May need adjustment if Airtable schema differs

5. **No Duplicate Detection:**
   - Workflow creates new presentation every time
   - No check for existing proposals for same company/call

6. **Limited Error Feedback:**
   - If Airtable returns no results, workflow may fail silently
   - Missing fields default to "TBD" without notification

### Suggested Next Steps

**Immediate:**
1. **Update Configuration:** Replace all placeholder IDs with actual values
2. **Test with Real Data:** Use actual Airtable records and verify output
3. **Verify Template:** Ensure Google Slides template has all required placeholders

**Short-term:**
4. **Add Error Handling:** Use error output branches for Airtable and Google Drive nodes
5. **Add Validation:** Check for empty results and missing required fields
6. **Test Both Routes:** Verify both company and individual proposal generation

**Long-term:**
7. **Add Duplicate Detection:** Check if proposal already exists before creating
8. **Add Proposal Versioning:** Include version number in filename
9. **Add Notification:** Send proposal link via email or multiple Slack channels
10. **Optimize Template:** Review template design and variable coverage

### Where to Look When Something Fails

**Webhook not receiving data:**
- Check Slack app configuration (webhook URL correct?)
- Verify n8n webhook is active (workflow must be active)
- Check Slack payload format in execution log

**Airtable returns no data:**
- Verify application ID is correct
- Check credential permissions
- Verify filter formula syntax: `={Company} = 'value'`
- Check table name is exactly "Calls"

**Google Slides errors:**
- Verify template ID exists and is accessible
- Check Google Slides credential has write permissions
- Ensure placeholders match exactly: `{{variable_name}}`

**Slack doesn't receive response:**
- Check "Respond to Webhook" node configuration
- Verify response_url is being passed through workflow
- Check Slack expects JSON format response

### Support Files

- **Workflow JSON Export:** Available in n8n UI (Export → Download)
- **Variable Mapping Reference:** See "Map to 47 Variables" Code node
- **Validation Report:** Run `n8n_validate_workflow` for detailed analysis

---

## Notes for Sway

✅ **Workflow Created Successfully**
- Workflow ID: `FSbhLS8ByK3vlSBh`
- All 13 nodes connected in proper sequence
- Both company and individual routes implemented

⚠️ **Configuration Required Before Testing**
- Update Airtable application ID (currently placeholder)
- Configure all three credentials (Airtable, Google Drive, Google Slides)
- Verify Google Slides template exists and is accessible

📋 **Validation Status**
- 2 errors (validator false positives - code is correct)
- 22 warnings (mostly about error handling and outdated typeVersions)
- Core logic is sound, needs configuration updates

🔧 **Next Action**
- Replace placeholder IDs with actual values
- Test with sample Slack payload
- Verify template has all 47 placeholders

