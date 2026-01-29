# Google Slides Proposal Generator - Configuration Guide

## Workflow ID
**FSbhLS8ByK3vlSBh**

---

## Step-by-Step Configuration

### 1. Configure Airtable Integration

**Workflow nodes to update:**
- "Get All Company Calls"
- "Get Single Call Record"

**Required changes:**

1. **Get Airtable Application ID:**
   - Open your Airtable base
   - Look at the URL: `https://airtable.com/appXXXXXXXXXXXXXX/...`
   - Copy the `appXXXXXXXXXXXXXX` part

2. **Update both nodes:**
   - Open n8n workflow: FSbhLS8ByK3vlSBh
   - Click "Get All Company Calls" node
   - Replace `appXXXXXXXXXXXXXX` with your actual base ID
   - Repeat for "Get Single Call Record" node

3. **Configure Airtable credential:**
   - In n8n, go to Credentials
   - Create new "Airtable Token API" credential
   - Add your Airtable personal access token
   - Name it: "Airtable Account" (or note the ID for updating nodes)
   - Update credential reference in both nodes

4. **Verify table name:**
   - Ensure your Airtable table is named exactly **"Calls"**
   - If different, update the table name in both nodes

---

### 2. Configure Google Drive Integration

**Workflow node to update:**
- "Duplicate Template"

**Required changes:**

1. **Verify template exists:**
   - Open Google Drive
   - Navigate to template presentation
   - Check URL: `https://docs.google.com/presentation/d/17BkLuHdj-iNlmnZ2jkP_cLLYMOzvTriCmejpDqe-UhQ/edit`
   - Confirm template ID matches: `17BkLuHdj-iNlmnZ2jkP_cLLYMOzvTriCmejpDqe-UhQ`
   - If different, update the `fileId` in "Duplicate Template" node

2. **Configure Google Drive credential:**
   - In n8n, go to Credentials
   - Create new "Google Drive OAuth2 API" credential
   - Follow OAuth2 flow to authorize
   - Required scopes:
     - `https://www.googleapis.com/auth/drive.file`
   - Name it: "Google Drive Account"
   - Update credential reference in "Duplicate Template" node

---

### 3. Configure Google Slides Integration

**Workflow node to update:**
- "Replace All Placeholders"

**Required changes:**

1. **Configure Google Slides credential:**
   - In n8n, go to Credentials
   - Create new "Google Slides OAuth2 API" credential
   - Use SAME Google account as Drive (recommended)
   - Required scopes:
     - `https://www.googleapis.com/auth/presentations`
   - Name it: "Google Slides Account"
   - Update credential reference in "Replace All Placeholders" node

2. **Verify presentation access:**
   - Ensure credential account has edit access to template
   - Test by manually opening template with that Google account

---

### 4. Configure Slack Integration

**Workflow node to update:**
- "Slack Button Click" (webhook trigger)

**Required changes:**

1. **Get n8n webhook URL:**
   - Open workflow in n8n
   - Click "Slack Button Click" node
   - Copy the webhook URL shown (e.g., `https://n8n.oloxa.ai/webhook/slack-proposal-button`)

2. **Configure Slack App:**
   - Go to Slack API: https://api.slack.com/apps
   - Select your app (or create new one)
   - Go to "Interactivity & Shortcuts"
   - Enable "Interactivity"
   - Set "Request URL" to your n8n webhook URL
   - Save changes

3. **Add interactive components:**
   - Create Slack message with buttons using Block Kit
   - Button 1: "Generate Company Proposal"
     - action_id: `proposal_company`
     - value: `{{company_name}}` (passed from your system)
   - Button 2: "Generate Individual Proposal"
     - action_id: `proposal_individual`
     - value: `{{call_id}}` (Airtable record ID)

4. **Test Slack connection:**
   - Send test message with buttons
   - Click button
   - Verify webhook receives payload in n8n execution log

---

### 5. Prepare Google Slides Template

**Template checklist:**

1. **Open template presentation:**
   - ID: `17BkLuHdj-iNlmnZ2jkP_cLLYMOzvTriCmejpDqe-UhQ`

2. **Add all 47 placeholders:**
   - Use exact format: `{{variable_name}}`
   - See full list in `google-slides-proposal-variables-reference.md`

3. **Minimum required placeholders (24 core variables):**

**Slide 1:**
```
{{company_name}}
{{date}}
```

**Slide 2:**
```
{{client_company_description}}
{{client_name}}
```

**Slide 3:**
```
{{pain_point_1}}
{{pain_point_1_description}}
{{pain_point_2}}
{{pain_point_2_description}}
{{pain_point_3}}
{{pain_point_3_description}}
```

**Slide 4:**
```
{{product_benefit_1}}
{{product_benefit_2}}
{{product_benefit_3}}
```

**Slide 5:**
```
{{building_phase_time}}
{{testing_phase_time}}
{{deployment_phase_time}}
```

**Slide 6:**
```
{{client_expectations_list}}
{{oloxa_delivery_list}}
```

**Slide 7:**
```
{{metric_1}}
{{metric_2}}
```

**Slide 8:**
```
{{time_based_cost}}
```

**Slide 9:**
```
{{step_1_description}}
{{step_2_description}}
{{step_3_description}}
```

**Slide 10:**
```
{{unique_client_thank_you_message}}
```

4. **Test placeholder format:**
   - No spaces: `{{pain_point_1}}` ✓ not `{{ pain_point_1 }}` ✗
   - Lowercase: `{{pain_point_1}}` ✓ not `{{Pain_Point_1}}` ✗
   - Underscores: `{{pain_point_1}}` ✓ not `{{painPoint1}}` ✗

---

### 6. Configure Airtable Data Structure

**Calls table required fields:**

| Field Name | Type | Format | Example |
|------------|------|--------|---------|
| Company | Single line text | Text | "Villa Martens" |
| Contact_Name | Single line text | Text | "Maria Zuzarte" |
| Summary | Long text | Text | "Villa Martens is a boutique hotel..." |
| pain_points | Long text | JSON array | `[{"title":"Manual work","description":"Slow"}]` |
| quick_wins | Long text | JSON array | `[{"title":"Automation"}]` |
| action_items | Long text | JSON array | `[{"title":"Build API","description":"Create booking API"}]` |
| requirements | Multiple select or Long text | Array or text | "Integration, Mobile app" |
| estimated_timeline | Long text | JSON object | `{"building":"4 weeks","testing":"2 weeks"}` |
| perf_numbers_captured | Long text or Multiple select | Array | "Reduce time by 70%" |
| estimated_cost | Currency or Single line text | Text with currency | "€12,500" |
| created_time | Created time | Auto | 2026-01-15T10:30:00.000Z |

**JSON format examples:**

**pain_points field:**
```json
[
  {
    "title": "Manual booking entry",
    "description": "Staff spends 3h/day entering bookings"
  },
  {
    "title": "Double bookings",
    "description": "No real-time availability"
  }
]
```

**quick_wins field:**
```json
[
  {"title": "Automated booking sync"},
  {"title": "Real-time calendar"}
]
```

**action_items field:**
```json
[
  {
    "title": "Phase 1: Discovery",
    "description": "Requirements gathering"
  },
  {
    "title": "Phase 2: Build",
    "description": "Develop workflows"
  }
]
```

**estimated_timeline field:**
```json
{
  "building": "4 weeks",
  "testing": "2 weeks",
  "deployment": "1 week"
}
```

---

### 7. Activate Workflow

1. **Open workflow in n8n:**
   - Navigate to workflow ID: FSbhLS8ByK3vlSBh

2. **Test execution first:**
   - Click "Test workflow" button
   - Use "Execute workflow" with manual trigger
   - Check execution log for errors

3. **Activate workflow:**
   - Toggle "Active" switch to ON
   - Webhook is now listening for Slack events

4. **Monitor initial executions:**
   - Watch execution log for first few runs
   - Check for errors in any node
   - Verify Google Slides presentations are created correctly

---

## Quick Configuration Checklist

Use this checklist to ensure everything is configured:

### Airtable
- [ ] Application ID updated in both nodes
- [ ] Credential created and connected
- [ ] Table name verified as "Calls"
- [ ] All required fields exist in Airtable
- [ ] JSON fields formatted correctly

### Google Drive
- [ ] Template ID verified and accessible
- [ ] OAuth2 credential created
- [ ] Credential has edit access to template
- [ ] Test: Can manually open template with credential account

### Google Slides
- [ ] OAuth2 credential created
- [ ] Same account as Drive (recommended)
- [ ] Credential connected to "Replace All Placeholders" node
- [ ] Template has all 47 placeholders (or minimum 24)

### Slack
- [ ] Webhook URL copied from n8n
- [ ] Slack app configured with webhook URL
- [ ] Interactive components enabled
- [ ] Button action_ids match: "proposal_company" and "proposal_individual"
- [ ] Test button click sends payload to n8n

### Workflow
- [ ] All credential IDs updated
- [ ] All placeholder IDs replaced
- [ ] Test execution successful
- [ ] Workflow activated
- [ ] Monitoring enabled

---

## Testing Procedure

### Test 1: Manual Execution (Recommended First)

1. **Prepare test data in Airtable:**
   - Create test call record
   - Fill all required fields
   - Note the record ID (e.g., `recXXXXXXXXXXXXXX`)

2. **Trigger workflow manually:**
   - Open workflow in n8n
   - Click "Test workflow"
   - Use "Execute workflow" button
   - Manually input test JSON:

```json
{
  "body": {
    "type": "interactive_message",
    "actions": [
      {
        "action_id": "proposal_individual",
        "value": "recXXXXXXXXXXXXXX"
      }
    ],
    "user": {
      "id": "U12345678"
    },
    "channel": {
      "id": "C12345678"
    },
    "response_url": "https://hooks.slack.com/actions/test"
  }
}
```

3. **Verify execution:**
   - Check each node executed successfully
   - Verify Airtable data was fetched
   - Check Google Slides presentation was created
   - Open generated presentation
   - Verify all placeholders were replaced
   - Check for any "TBD" values (indicates missing data)

### Test 2: Slack Integration Test

1. **Create Slack message with test button:**
   - Use Block Kit Builder: https://app.slack.com/block-kit-builder
   - Add button with action_id and test value
   - Post to test Slack channel

2. **Click button and verify:**
   - Button click triggers n8n workflow
   - Workflow execution appears in n8n log
   - Slack receives response message
   - Link in response opens generated presentation

### Test 3: Company Aggregation Test

1. **Create multiple calls for same company:**
   - Add 2-3 test calls with same company name
   - Each with different pain points and action items

2. **Trigger company proposal:**
   - Use action_id: "proposal_company"
   - Value: company name (e.g., "Villa Martens")

3. **Verify aggregation:**
   - Check execution log shows all calls retrieved
   - Verify pain points merged from all calls
   - Check presentation has data from multiple calls

---

## Troubleshooting

### Issue: "Airtable returns no data"

**Symptoms:**
- Workflow fails at "Get All Company Calls" or "Get Single Call Record"
- Error: "Record not found" or empty result

**Solutions:**
1. Verify application ID is correct
2. Check credential has read access
3. Verify table name is exact: "Calls"
4. Check filter formula syntax
5. Ensure record ID format is correct (starts with "rec")

### Issue: "Google Slides template not found"

**Symptoms:**
- Workflow fails at "Duplicate Template"
- Error: "File not found" or permission denied

**Solutions:**
1. Verify template ID is correct
2. Check credential account has edit access
3. Ensure template is not in Trash
4. Try opening template manually with credential account
5. Check Google Drive OAuth scopes include `drive.file`

### Issue: "Placeholders not replaced"

**Symptoms:**
- Presentation created but still shows {{placeholders}}
- Some placeholders replaced, others not

**Solutions:**
1. Check placeholder format in template (exact match required)
2. Verify "Replace All Placeholders" node executed
3. Check variable mapping in "Map to 47 Variables" node
4. Ensure Google Slides credential has write access
5. Look for typos in placeholder names

### Issue: "Slack doesn't receive response"

**Symptoms:**
- Workflow executes but Slack shows no message
- Button click times out in Slack

**Solutions:**
1. Check webhook has `responseMode: "responseNode"`
2. Verify "Respond to Webhook" node executed
3. Check response_url is passed through workflow
4. Ensure Slack expects JSON format
5. Test with manual Slack webhook tester

---

## Support & Next Steps

**Workflow files:**
- Implementation summary: `/Users/computer/coding_stuff/implementation-summary-google-slides-proposal.md`
- Workflow diagram: `/Users/computer/coding_stuff/google-slides-proposal-workflow-diagram.md`
- Variable reference: `/Users/computer/coding_stuff/google-slides-proposal-variables-reference.md`
- This guide: `/Users/computer/coding_stuff/google-slides-proposal-configuration-guide.md`

**After successful testing:**
1. Add error handling to Airtable nodes
2. Implement duplicate detection
3. Add proposal versioning
4. Consider email notifications
5. Add analytics tracking

**For questions or issues:**
- Check n8n execution logs for detailed error messages
- Review validation report from `n8n_validate_workflow`
- Test each node individually in n8n UI
- Verify all credentials are properly connected

