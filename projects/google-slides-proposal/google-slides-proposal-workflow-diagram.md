# Generate Proposal - Google Slides Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         SLACK BUTTON TRIGGER                            │
│  Webhook: POST /slack-proposal-button                                  │
│  Receives: action_id (proposal_company or proposal_individual)         │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      EXTRACT SLACK PAYLOAD                              │
│  Parse URL-encoded Slack payload                                       │
│  Extract: proposal_type, target_identifier, user_id, channel_id        │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   COMPANY OR INDIVIDUAL? (IF)                           │
│  Route based on proposal_type                                          │
└────────────┬────────────────────┴────────────────────┬─────────────────┘
             │                                         │
   proposal_type = "company"              proposal_type = "individual"
             │                                         │
             ▼                                         ▼
┌───────────────────────────┐             ┌──────────────────────────────┐
│ GET ALL COMPANY CALLS     │             │ GET SINGLE CALL RECORD       │
│ (Airtable)                │             │ (Airtable)                   │
│                           │             │                              │
│ Filter: {Company} =       │             │ Get by call_id               │
│   target_identifier       │             │                              │
└──────────┬────────────────┘             └──────────┬───────────────────┘
           │                                         │
           ▼                                         ▼
┌───────────────────────────┐             ┌──────────────────────────────┐
│ AGGREGATE COMPANY DATA    │             │ PREPARE INDIVIDUAL DATA      │
│ (Code)                    │             │ (Code)                       │
│                           │             │                              │
│ - Merge pain_points       │             │ - Parse pain_points JSON     │
│ - Merge quick_wins        │             │ - Parse quick_wins JSON      │
│ - Merge action_items      │             │ - Parse action_items JSON    │
│ - Use latest call for     │             │ - Format for consistency     │
│   single-value fields     │             │                              │
└──────────┬────────────────┘             └──────────┬───────────────────┘
           │                                         │
           └──────────────┬──────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      MAP TO 47 VARIABLES (Code)                         │
│                                                                         │
│  Transform Airtable data → Google Slides placeholders                  │
│                                                                         │
│  Slide 1: company_name, date                                           │
│  Slide 2: client_company_description, client_name                      │
│  Slide 3: pain_point_1-3 + descriptions (6 vars)                       │
│  Slide 4: product_benefit_1-3 (3 vars)                                 │
│  Slide 5: building/testing/deployment_phase_time (3 vars)              │
│  Slide 6: client_expectations_list, oloxa_delivery_list (2 vars)       │
│  Slide 7: metric_1-2 (2 vars)                                          │
│  Slide 8: time_based_cost (1 var)                                      │
│  Slide 9: step_1-3_description (3 vars)                                │
│  Slide 10: unique_client_thank_you_message (1 var)                     │
│                                                                         │
│  Total: 47 variables with TBD defaults                                 │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    DUPLICATE TEMPLATE (Google Drive)                    │
│                                                                         │
│  Template ID: 17BkLuHdj-iNlmnZ2jkP_cLLYMOzvTriCmejpDqe-UhQ             │
│  New name: Proposal - [Company] - [Date]                               │
│  Output: New presentation ID                                           │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               BUILD REPLACEMENTS ARRAY (Code)                           │
│                                                                         │
│  Convert variables → Google Slides textUi format                       │
│  [                                                                      │
│    { text: "{{company_name}}", replaceText: "Oloxa.ai", ... },         │
│    { text: "{{date}}", replaceText: "January 2026", ... },             │
│    ...                                                                  │
│  ]                                                                      │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│            REPLACE ALL PLACEHOLDERS (Google Slides)                     │
│                                                                         │
│  Batch replace all {{variable}} placeholders                           │
│  Uses textUi.textValues array for multiple replacements                │
│  Operation: replaceText                                                 │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                  BUILD SLACK MESSAGE (Code)                             │
│                                                                         │
│  Construct response:                                                   │
│  {                                                                      │
│    "response_type": "in_channel",                                      │
│    "text": "✅ Proposal generated: [PRESENTATION_LINK]"                │
│  }                                                                      │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│               SEND SLACK RESPONSE (Respond to Webhook)                  │
│                                                                         │
│  Returns JSON response to Slack                                        │
│  Message appears in Slack channel with clickable link                  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Summary

### Route A: Company Proposal
```
Slack Button
  → Extract payload (company_name)
  → Query Airtable for ALL company calls
  → Aggregate pain_points/quick_wins/action_items
  → Map to 47 variables
  → Duplicate template
  → Replace placeholders
  → Send Slack link
```

### Route B: Individual Proposal
```
Slack Button
  → Extract payload (call_id)
  → Get single Airtable call
  → Parse JSON arrays
  → Map to 47 variables
  → Duplicate template
  → Replace placeholders
  → Send Slack link
```

## Variable Mapping Example

```javascript
// Input (from Airtable)
{
  "company_name": "Villa Martens",
  "contact_name": "Maria Zuzarte",
  "summary": "Villa Martens needs automation for booking system...",
  "pain_points": [
    {
      "title": "Manual booking entry",
      "description": "Staff spends 3h/day entering bookings manually"
    },
    {
      "title": "Double bookings",
      "description": "Lack of real-time availability causes conflicts"
    }
  ],
  "quick_wins": [
    {
      "title": "Automated booking sync"
    },
    {
      "title": "Real-time calendar"
    }
  ]
}

// Output (to Google Slides)
{
  "company_name": "Oloxa.ai",
  "date": "January 2026",
  "client_company_description": "Villa Martens needs automation for booking system",
  "client_name": "Maria Zuzarte",
  "pain_point_1": "Manual booking entry",
  "pain_point_1_description": "Staff spends 3h/day entering bookings manually",
  "pain_point_2": "Double bookings",
  "pain_point_2_description": "Lack of real-time availability causes conflicts",
  "pain_point_3": "TBD",
  "pain_point_3_description": "TBD",
  "product_benefit_1": "Automated booking sync",
  "product_benefit_2": "Real-time calendar",
  "product_benefit_3": "TBD",
  // ... remaining 35 variables
}
```

## Node Execution Order

1. **Slack Button Click** (trigger)
2. **Extract Slack Payload** (always)
3. **Company or Individual?** (always)
4. **Route A OR Route B** (conditional)
   - 4a. Get All Company Calls → Aggregate Company Data
   - 4b. Get Single Call Record → Prepare Individual Data
5. **Map to 47 Variables** (routes merge)
6. **Duplicate Template** (always)
7. **Build Replacements Array** (always)
8. **Replace All Placeholders** (always)
9. **Build Slack Message** (always)
10. **Send Slack Response** (always)

Total execution time estimate: **5-10 seconds**
- Airtable query: 1-2s
- Google Drive copy: 2-3s
- Google Slides replace: 2-4s
- Slack response: <1s

