# Fathom Workflow Call Type Field Fix

## Date: 2026-01-28

## Workflow
- **ID**: cMGbzpq1RXpL0OHY
- **Name**: Fathom Transcript Workflow Final_22.01.26

## Problem
The "Save to Airtable" node was mapping the call_type value to the wrong Airtable field.

### Two "Call Type" Fields in Airtable
1. **"Call Type"** (id: fldUcj9I0kkuKX2fm)
   - Original field
   - 8 options
   - Being mapped incorrectly

2. **"call_type"** (id: fldzE9WI9WI6nLllC)
   - New field
   - 3 options: Discovery, Developer/Coaching, Regular
   - Target field (correct)

## Root Cause
Field name mismatch in the Airtable node's column mapping:
- **Before**: `"Call Type": "={{ $json.call_type }}"`
- **After**: `"call_type": "={{ $json.call_type }}"`

The capital letters "Call Type" mapped to the old field (fldUcj9I0kkuKX2fm), while lowercase "call_type" maps to the new field (fldzE9WI9WI6nLllC).

## Fix Applied
Updated the "Save to Airtable" node field mapping:

```json
{
  "Summary": "={{ $json.summary }}",
  "Pain Points": "={{ $json.pain_points }}",
  "Quick Wins": "={{ $json.quick_wins }}",
  "Action Items": "={{ $json.action_items }}",
  "Performance Score": "={{ $json.performance_score }}",
  "Improvement Areas": "={{ $json.improvement_areas }}",
  "Complexity Assessment": "={{ $json.complexity_assessment }}",
  "Roadmap": "={{ $json.roadmap }}",
  "Key Insights": "={{ $json.key_insights }}",
  "Pricing Strategy": "={{ $json.pricing_strategy }}",
  "Client Journey Map": "={{ $json.client_journey_map }}",
  "Requirements": "={{ $json.requirements }}",
  "Contact": "={{ $json.matched_contact_id || '' }}",
  "Company": "={{ $json.matched_client_id ? [$json.matched_client_id] : [] }}",
  "call_type": "={{ $json.call_type }}"  // CHANGED: lowercase to map to new field
}
```

## Operation Used
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow({
  id: "cMGbzpq1RXpL0OHY",
  operations: [{
    type: "updateNode",
    nodeName: "Save to Airtable",
    updates: {
      parameters: {
        columns: {
          value: { /* updated field mapping */ }
        }
      }
    }
  }]
})
```

## Testing
After fix is applied, test the workflow by:
1. Executing the workflow with a test meeting
2. Verifying the call_type value is saved to the correct field (lowercase "call_type")
3. Confirming the value matches one of: Discovery, Developer/Coaching, Regular

## Pattern for Future
**Airtable Field Name Sensitivity**
- Field names in Airtable are case-sensitive
- Always verify the EXACT field name in Airtable before mapping
- Use the Airtable UI or API to confirm field IDs if ambiguous
- When duplicate field names exist (different cases), be very careful with mapping

## Alternative Solution (Not Implemented)
Could consolidate the two "Call Type" fields in Airtable:
1. Migrate data from old "Call Type" to new "call_type"
2. Delete old "Call Type" field
3. Prevents future confusion

This would require:
- Reviewing all workflows using either field
- Data migration script
- Coordination with team using Airtable
