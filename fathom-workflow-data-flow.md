# Fathom Workflow - Data Flow Visualization

## Complete Data Flow (After Fix)

```
┌──────────────────────┐
│  Manual Trigger /    │
│  Webhook Trigger     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Route: Webhook or    │
│     API              │
└──────────┬───────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌────────────┐
│Webhook  │  │ API Path   │
│  Path   │  │(Fathom API)│
└────┬────┘  └─────┬──────┘
     │             │
     ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│         Enhanced AI Analysis (Set Node)                      │
│  Creates prompt with meeting metadata:                       │
│  - meeting_title: ${ $json.meeting_title }                   │
│  - meeting_date: ${ $json.meeting_date }                     │
│  - contact_name: ${ $json.contact_name }                     │
│  - contact_email: ${ $json.contact_email }                   │
│  - combined_transcript: ${ $json.combined_transcript }       │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│           Call AI for Analysis (OpenAI Node)                 │
│  GPT-4o analyzes transcript + returns JSON with:            │
│  - Analysis fields (summary, pain_points, etc.)              │
│  - Meeting metadata (meeting_title, meeting_date, etc.)      │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│           Parse AI Response (Code Node)                      │
│  Extracts JSON from GPT response:                            │
│  OUTPUT: {                                                   │
│    meeting_title: "John Doe",                                │
│    meeting_date: "2026-01-25",                               │
│    contact_name: "John Doe",                                 │
│    contact_email: "john@example.com",                        │
│    summary: "...",                                           │
│    pain_points: "...",                                       │
│    quick_wins: "...",                                        │
│    action_items: "...",                                      │
│    key_insights: "...",                                      │
│    pricing_strategy: "...",                                  │
│    client_journey_map: "...",                                │
│    requirements: "..."                                       │
│  }                                                           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│       Build Performance Prompt (Set Node)                    │
│  Creates performance prompt with metadata again              │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│       Call AI for Performance (OpenAI Node)                  │
│  GPT-4o analyzes performance + returns JSON                  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│       Parse Performance Response (Code Node)                 │
│  OUTPUT: {                                                   │
│    meeting_title: "John Doe",                                │
│    meeting_date: "2026-01-25",                               │
│    contact_name: "John Doe",                                 │
│    contact_email: "john@example.com",                        │
│    summary: "..." (from upstream),                           │
│    pain_points: "..." (from upstream),                       │
│    ... (all analysis fields from upstream),                  │
│    performance_summary: "...",                               │
│    performance_metrics: "...",                               │
│    performance_trends: "..."                                 │
│  }                                                           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                       ┌───────┴────────┐
                       │                │
                       ▼                ▼
┌────────────────────────────┐  ┌──────────────────────┐
│Extract Participant Names   │  │ Merge Performance    │
│(Code Node)                 │  │ Data (Merge Node)    │
│OUTPUT: {                   │  │ (Input 1)            │
│  ...all fields above,      │  │ Waits for Save to    │
│  participant_names: [..],  │  │ Airtable to complete │
│  primary_participant: ".." │  │                      │
│}                           │  └──────────────────────┘
└──────────┬─────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│           Search Contacts (Airtable Node)                     │
│  Searches Contacts table for participant                      │
│  ❌ REPLACES INPUT DATA with Airtable contact records         │
│  OUTPUT: { Name: "John Doe", Email: "john@example.com", ...} │
│  ⚠️  ALL UPSTREAM DATA LOST (meeting_title, summary, etc.)    │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│           Search Clients (Airtable Node)                      │
│  Searches Clients table                                       │
│  ❌ REPLACES INPUT DATA AGAIN with Airtable client records    │
│  OUTPUT: { Company Name: "Acme Inc", ...}                     │
│  ⚠️  ALL UPSTREAM DATA STILL LOST                             │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│           ✨ Merge Search Data (NEW CODE NODE) ✨             │
│  ✅ RESTORES UPSTREAM DATA from Parse Performance Response    │
│                                                               │
│  const upstreamData = $('Parse Performance Response').item.j  │
│  const contactData = $('Search Contacts').item.json;          │
│  const clientData = $('Search Clients').item.json;            │
│                                                               │
│  return {                                                     │
│    json: {                                                    │
│      ...upstreamData, // ✅ ALL meeting/analysis/perf data    │
│      matched_contact: contactData,                            │
│      matched_client: clientData,                              │
│      matched_contact_name: contactData?.Name || "Unknown",    │
│      matched_client_name: clientData?.["Company Name"] || ".."│
│    }                                                          │
│  };                                                           │
│                                                               │
│  OUTPUT: {                                                    │
│    meeting_title: "John Doe", ✅                              │
│    meeting_date: "2026-01-25", ✅                             │
│    contact_name: "John Doe", ✅                               │
│    contact_email: "john@example.com", ✅                      │
│    summary: "...", ✅                                         │
│    pain_points: "...", ✅                                     │
│    performance_summary: "...", ✅                             │
│    matched_contact: { Name: "John", ... }, ✅                 │
│    matched_client: { Company Name: "Acme", ... } ✅           │
│  }                                                            │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│           Prepare Airtable Data (Code Node)                   │
│  Maps all fields to Airtable format:                          │
│  - Title: contact_name (✅ "John Doe")                        │
│  - Date: meeting_date (✅ "2026-01-25")                       │
│  - Contact: contact_email (✅ "john@example.com")             │
│  - Summary: summary (✅ populated)                            │
│  - Pain Points: pain_points (✅ populated)                    │
│  - Performance Score: performance_score (✅ populated)         │
│  - ... all other fields                                       │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│           Limit to 1 Record (Limit Node)                      │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│           Save to Airtable (Airtable Node)                    │
│  Saves to Calls table (tblkcbS4DIqvIzJW2)                     │
│  OUTPUT: { id: "recXXX", fields: {...} }                      │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│           Merge Performance Data (Merge Node)                 │
│  INPUT 0: Save to Airtable output (Airtable record ID)        │
│  INPUT 1: Parse Performance Response (performance data)       │
│  Combines by position → single merged item                    │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│           Prepare Performance Data (Code Node)                │
│  Extracts data from merged inputs:                            │
│  - Airtable record ID (from input 0)                          │
│  - Performance fields (from input 1)                          │
│  Maps to Call Performance table format                        │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────┐
│       Save Performance to Airtable (Airtable Node)            │
│  Saves to Call Performance table (tblRX43do0HJVOPgC)          │
│  Links to Calls record via record ID                          │
└──────────────────────────────┬───────────────────────────────┘
                               │
                       ┌───────┴────────┐
                       │                │
                       ▼                ▼
┌────────────────────────────┐  ┌──────────────────────┐
│Prepare Date Folder Name    │  │Build Slack Blocks    │
│(Save transcripts to Drive) │  │(Notification)        │
└────────────────────────────┘  └──────────────────────┘
```

---

## Key Insight: The Fix Point

**The critical fix is the "Merge Search Data" node.**

Without it:
- Search Contacts/Clients **wipe out** all upstream data
- Prepare Airtable Data receives empty Airtable records
- Result: Title="Unknown", Date=today, missing all fields

With it:
- Merge Search Data **fetches upstream data** from Parse Performance Response
- Prepare Airtable Data receives **complete data** (meeting metadata + analysis + performance + search results)
- Result: ✅ All fields populated correctly

---

## Why $('Parse Performance Response') Works

The Merge Search Data node uses:
```javascript
const upstreamData = $('Parse Performance Response').item.json;
```

This works because:
1. n8n Code nodes support referencing other nodes via `$('NodeName')`
2. Parse Performance Response executed **before** Search Clients (it's upstream)
3. n8n keeps all node outputs in memory until workflow completes
4. This bypasses the Search nodes that wiped out the data

---

## Data Structure at Each Stage

### Parse Performance Response Output
```json
{
  "meeting_title": "John Doe",
  "meeting_date": "2026-01-25",
  "contact_name": "John Doe",
  "contact_email": "john@example.com",
  "meeting_url": "https://app.fathom.video/calls/...",
  "recording_id": "...",
  "summary": "Discussion about automation...",
  "pain_points": "Manual data entry taking 5 hours/week...",
  "quick_wins": "Automate report generation...",
  "action_items": "1. Schedule discovery call...",
  "key_insights": "Client needs end-to-end automation...",
  "pricing_strategy": "Value-based: $3K-5K/month...",
  "client_journey_map": "Awareness → Discovery → Proposal...",
  "requirements": "Must integrate with Salesforce...",
  "performance_summary": "Strong discovery, good quantification...",
  "performance_metrics": "Talk ratio: 30/70...",
  "performance_trends": "Improving over time..."
}
```

### After Search Clients (BEFORE FIX - DATA LOST)
```json
{
  "Company Name": "Acme Inc",
  "Industry": "SaaS",
  "Status": "Active"
  // ❌ ALL MEETING DATA LOST
}
```

### After Merge Search Data (AFTER FIX - DATA RESTORED)
```json
{
  "meeting_title": "John Doe", // ✅ RESTORED
  "meeting_date": "2026-01-25", // ✅ RESTORED
  "contact_name": "John Doe", // ✅ RESTORED
  "contact_email": "john@example.com", // ✅ RESTORED
  "summary": "Discussion about automation...", // ✅ RESTORED
  "pain_points": "Manual data entry...", // ✅ RESTORED
  "performance_summary": "Strong discovery...", // ✅ RESTORED
  "matched_contact": {
    "Name": "John Doe",
    "Email": "john@example.com"
  }, // ✅ ADDED
  "matched_client": {
    "Company Name": "Acme Inc",
    "Industry": "SaaS"
  }, // ✅ ADDED
  "matched_contact_name": "John Doe", // ✅ ADDED
  "matched_client_name": "Acme Inc" // ✅ ADDED
}
```

---

## Testing Checkpoint

When testing, verify these nodes output the expected data:

1. ✅ **Parse Performance Response:** Has meeting_title, summary, performance_summary
2. ❌ **Search Clients:** Does NOT have meeting_title, summary (expected — it's replaced)
3. ✅ **Merge Search Data:** Has meeting_title, summary, performance_summary, matched_contact, matched_client
4. ✅ **Prepare Airtable Data:** Has Title (NOT "Unknown"), Date (NOT today), all fields
5. ✅ **Airtable Calls Table:** Record with correct Title, Date, Contact, all analysis fields
6. ✅ **Airtable Call Performance Table:** Record linked to Calls, with performance fields

If ANY of these fail, the data flow is broken.
