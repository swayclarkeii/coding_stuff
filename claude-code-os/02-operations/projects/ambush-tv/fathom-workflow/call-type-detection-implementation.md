# Call Type Detection Implementation

## Workflow: Fathom Transcript Workflow Final_22.01.26
**Workflow ID**: cMGbzpq1RXpL0OHY

## Changes Made

### 1. Updated "Prepare Airtable Data" Node

**Added call type detection function:**

```javascript
function detectCallType(meetingTitle, participants) {
  const title = (meetingTitle || '').toLowerCase();
  const participantList = (participants || '').toLowerCase();

  // Rule 1: Discovery calls
  if (title.includes('discovery') ||
      title.includes('audit') ||
      title.includes('intake') ||
      title.includes('initial')) {
    return 'Discovery';
  }

  // Rule 2: Developer/Coaching calls
  if (title.includes('developer') ||
      title.includes('coaching') ||
      title.includes('tech') ||
      title.includes('feasibility') ||
      title.includes('declan') ||  // Sway's coach
      participantList.includes('declan') ||
      title.includes('build review')) {
    return 'Developer/Coaching';
  }

  // Rule 3: Default
  return 'Regular';
}
```

**Updated return statement to include call_type:**

```javascript
return {
  json: {
    ...originalData,
    matched_contact_id: matchedContactId,
    matched_client_id: matchedClientId,
    call_type: callType  // ← NEW
  }
};
```

### 2. Updated "Save to Airtable" Node

**Added Call Type field mapping:**

```javascript
"Call Type": "={{ $json.call_type }}"
```

## Detection Rules

| Call Type | Triggers |
|-----------|----------|
| **Discovery** | Meeting title contains: "discovery", "audit", "intake", or "initial" |
| **Developer/Coaching** | Meeting title or participants contain: "developer", "coaching", "tech", "feasibility", "declan", or "build review" |
| **Regular** | Default for all other meetings |

## Test Examples

| Meeting Title | Expected Result |
|---------------|-----------------|
| "Sindbad Discovery Call" | Discovery |
| "Declan Coaching Session" | Developer/Coaching |
| "Meeting with Declan" | Developer/Coaching |
| "Ambush TV Follow-up" | Regular |
| "Initial Consultation with Client" | Discovery |
| "Tech Feasibility Review" | Developer/Coaching |

## Field Configuration

- **Airtable Field**: `call_type`
- **Field ID**: `fldzE9WI9WI6nLllC`
- **Type**: singleSelect
- **Options**: "Discovery", "Developer/Coaching", "Regular"

## Status

✅ **Implementation Complete**

- Call type detection logic added
- Function checks both meeting title and participants
- Field properly mapped to Airtable
- Workflow validated (pre-existing warnings unrelated to this change)

## Next Steps

1. Test with real Fathom webhook to verify detection works
2. Monitor Airtable Calls table to ensure `call_type` is being saved correctly
3. Adjust detection keywords if needed based on actual usage patterns

## Notes

- Detection is case-insensitive for better matching
- Checks both `meeting_title` and `participants` fields
- Default fallback is "Regular" for unmatched calls
- Can easily extend detection rules by adding more keywords to the function
