# Implementation Complete – Fathom to Airtable Workflow

## 1. Overview
- **Platform:** n8n
- **Workflow ID:** cMGbzpq1RXpL0OHY
- **Status:** Built and ready for testing
- **Files touched:**
  - Modified existing workflow: Fathom Transcript Workflow Final_22.01.26

## 2. Workflow Structure

### Trigger Options
1. **Manual Trigger** (enabled) - For manual testing
2. **Webhook Trigger** (enabled) - Path: `/fathom-test`, POST method
3. **Daily Schedule** (disabled) - Runs at 11:30 PM daily

### Main Flow
```
Trigger → Config (60 days back)
    ↓
List Meetings (Fathom API)
    ↓
Extract Meetings Array (pagination + date filter)
    ↓
Get Transcript (for each meeting)
    ↓
Combine Meeting + Transcript
    ↓
Process Each Meeting (format data)
    ↓
Enhanced AI Analysis (build prompt)
    ↓
Call AI for Analysis (GPT-4o)
    ↓
Parse AI Response (extract 12 fields)
    ↓
Extract Participant Names
    ↓
Search Contacts (Airtable)
    ↓
Search Clients (Airtable)
    ↓
Prepare Airtable Data (merge matches)
    ↓
Save to Airtable (PRIMARY)
    ↓
Prepare Date Folder Name
    ↓
Get Unique Dates
    ↓
Create or Get Date Folder (Google Drive)
    ↓
Match Meetings to Folders
    ↓
Convert to Binary
    ↓
Save Transcript to Drive (SECONDARY backup)
```

## 3. Enhanced AI Analysis

**AI Model:** GPT-4o (temperature: 0.3)

**12 Fields Extracted:**
1. **Summary** - Brief 2-3 sentence overview
2. **Pain Points** - Key challenges/problems mentioned
3. **Quick Wins** - Immediate opportunities
4. **Action Items** - Clear next steps
5. **Performance Score** - 0-100 numeric score
6. **Improvement Areas** - Areas needing work
7. **Complexity Assessment** - Simple/Medium/Complex
8. **Roadmap** - Strategic implementation plan
9. **Key Insights** - Important patterns/discoveries
10. **Pricing Strategy** - Budget/pricing discussion
11. **Client Journey Map** - Where client is in journey
12. **Requirements** - Technical/business requirements

## 4. Airtable Integration

### Primary Destination
- **Base ID:** appvd4nlsNhIWYdbI
- **Table:** Calls (tblkcbS4DIqvIzJW2)

### Fields Mapped
- Meeting Title
- Meeting Date
- Meeting URL
- Transcript (full raw transcript)
- All 12 AI-extracted fields (above)
- Contact (linked record) - matched from Contacts table
- Company (linked record) - matched from Clients table

### Participant Matching Logic
1. Extract participant names from meeting data or title
2. Search Contacts table (tblEB4I4qVQmkSKpw) by name
3. Search Clients table (tblbr6SBSc5K4l3uk) by name
4. Link first match for each (if found)

### Credentials
- **Authentication:** Access Token (airtableTokenApi)
- **Credential ID:** airtable-creds
- **Token Used:** claude_code_token from `/Users/computer/coding_stuff/.credentials/airtable.json`

## 5. Google Drive Backup (Secondary)

**Purpose:** Raw transcript backup (unchanged from original workflow)

**Location:**
- Parent Folder ID: 1fzJztc3nweG6mzsEJOJBeaA6tk84jys9
- Creates date-based subfolders (e.g., "January 28th, 2026")
- Saves as: `[Contact Name] - [Date] - Transcript.txt`

**Credentials:** Google Drive OAuth2 (a4m50EefR3DJoU0R)

## 6. Configuration Changes

### Fathom Date Range
- **Previous:** 1 day back
- **New:** 60 days back (December 1, 2025 onwards)
- **Parameter:** `daysBack` in Config node

### Disabled Nodes (Old Logic)
- Is Standalone Impromptu?
- Build AI Prompt
- Extract Name (OpenAI)
- Extract AI Name
- Merge

**Reason:** Replaced with enhanced AI analysis that runs for ALL meetings (not just impromptu)

## 7. Testing

### Webhook Testing
**URL:** `https://n8n.oloxa.ai/webhook/fathom-test`

**Method:** POST

**Test Payload Example:**
```json
{
  "meeting_title": "Test Meeting with John Doe",
  "meeting_url": "https://fathom.ai/meetings/test-123",
  "recording_id": "test-recording-id",
  "transcript": [
    {
      "speaker": {"display_name": "John Doe"},
      "text": "I'm looking for help with automation."
    },
    {
      "speaker": {"display_name": "Sway Clarke"},
      "text": "Tell me about your current process."
    }
  ],
  "created_at": "2026-01-28T00:00:00Z",
  "calendar_invitees": [
    {
      "name": "John Doe",
      "email": "john@example.com",
      "is_external": true
    }
  ]
}
```

### Manual Testing
1. Enable Manual Trigger
2. Click "Test Workflow" in n8n
3. Verify:
   - AI extracts all 12 fields
   - Participant matching finds contacts/clients
   - Airtable record created
   - Google Drive backup saved

### Happy Path Test
- **Input:** Real Fathom meeting from last 60 days
- **Expected:**
  - Meeting pulled from Fathom API
  - Transcript retrieved
  - AI analysis generates all 12 fields
  - Participant name extracted
  - Contact/Client matched (if exists in Airtable)
  - New record created in Calls table
  - Raw transcript saved to Google Drive

## 8. Known Limitations

1. **Participant Matching:** Uses simple name search (case-insensitive SEARCH formula)
   - May not match if name format differs significantly
   - Takes first match only (could improve with fuzzy matching)

2. **AI Parsing:** If GPT-4o returns invalid JSON, fallback values are used
   - Summary: "Failed to parse AI response"
   - All other fields: empty strings
   - Performance Score: 0

3. **Error Handling:** Most nodes use `continueOnFail: true`
   - Workflow continues even if individual steps fail
   - Check execution logs for failures

4. **Credentials:**
   - Airtable credentials need to be configured in n8n
   - Credential ID: "airtable-creds"
   - Must have token: [REDACTED - stored in .credentials/airtable.json]

## 9. Handoff

### How to Turn On/Off
- **Activate:** Toggle workflow active in n8n UI
- **Schedule:** Enable "Daily Schedule" trigger node (currently disabled)
- **Webhook:** Already enabled at `/fathom-test`

### Credentials to Configure
Before first run, ensure these credentials exist in n8n:

1. **Airtable Token** (ID: airtable-creds)
   - Type: Access Token
   - Token: [REDACTED - stored in .credentials/airtable.json]

2. **Google Drive OAuth2** (ID: a4m50EefR3DJoU0R)
   - Already configured (for backup)

3. **OpenAI API** (ID: xmJ7t6kaKgMwA1ce)
   - Already configured (for AI analysis)

4. **Fathom API Key**
   - Stored in Config node (not as credential)
   - Key: lzTrFSjfaTlbGrxW_txpEg.iKQ-dm_4tL395VFtFv04FmLuLiTweAVQXMeiUWrdB_4

### Where to Look When Something Fails
1. **n8n Executions:** Check workflow execution history
2. **AI Parsing Errors:** Check "Parse AI Response" node output
3. **Airtable Errors:** Check "Save to Airtable" node output
4. **Participant Matching:** Check "Search Contacts" and "Search Clients" outputs
5. **Google Drive:** Check "Save Transcript to Drive" node output

## 10. Suggested Next Steps

1. **Test with real data:** Run webhook test with actual Fathom meeting
2. **Verify Airtable schema:** Ensure all column names match exactly
3. **Check AI quality:** Review a few AI-extracted fields for accuracy
4. **Improve participant matching:** Consider fuzzy matching or multiple field comparison
5. **Monitor costs:** GPT-4o calls for every meeting (can be expensive at scale)
6. **Add error notifications:** Set up alerts for failed executions

## 11. Optimization Opportunities (Future)

- Use workflow-optimizer-agent if:
  - Token costs for GPT-4o become too high (consider GPT-4o-mini for some fields)
  - Participant matching accuracy is low (needs better fuzzy logic)
  - Execution time is slow (consider parallel processing)

## 12. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ TRIGGERS                                                     │
├─────────────────────────────────────────────────────────────┤
│ • Manual Trigger (enabled)                                  │
│ • Webhook Trigger (enabled) - /fathom-test                  │
│ • Daily Schedule (disabled) - 11:30 PM                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ DATA COLLECTION                                              │
├─────────────────────────────────────────────────────────────┤
│ Config (60 days) → List Meetings → Extract Meetings Array   │
│                  → Get Transcript → Combine Data            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ AI ANALYSIS (GPT-4o)                                         │
├─────────────────────────────────────────────────────────────┤
│ Process Each Meeting → Enhanced AI Analysis                 │
│                     → Call AI for Analysis                  │
│                     → Parse AI Response (12 fields)         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ PARTICIPANT MATCHING                                         │
├─────────────────────────────────────────────────────────────┤
│ Extract Participant Names → Search Contacts (Airtable)      │
│                          → Search Clients (Airtable)        │
│                          → Prepare Airtable Data            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ PRIMARY SAVE                                                 │
├─────────────────────────────────────────────────────────────┤
│ Save to Airtable (Calls table)                              │
│ • All 12 AI fields                                          │
│ • Linked Contact/Company records                            │
│ • Full transcript                                           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ SECONDARY BACKUP                                             │
├─────────────────────────────────────────────────────────────┤
│ Prepare Date Folder Name → Get Unique Dates                │
│                          → Create/Get Date Folder           │
│                          → Match Meetings to Folders        │
│                          → Convert to Binary                │
│                          → Save Transcript to Drive         │
└─────────────────────────────────────────────────────────────┘
```

---

## Summary

Enhanced Fathom workflow successfully modified to:
- Pull transcripts from December 1, 2025 onwards (60+ days)
- Extract 12 comprehensive fields using GPT-4o AI analysis
- Save primary data to Airtable (Calls table)
- Match participants to existing Contacts/Clients
- Maintain Google Drive backup as secondary storage
- Enable webhook testing at `/fathom-test`

Ready for testing and deployment.
