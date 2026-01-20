# Fathom CRM Auto-Populate - Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    FATHOM WEBHOOK TRIGGER                       │
│  Receives: { meeting_id, event: "content_ready" }              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              GET FATHOM TRANSCRIPT (HTTP Request)               │
│  API: https://api.fathom.video/v1/meetings/{id}/transcript     │
│  Auth: Bearer Token                                             │
│  Retry: 3x with 5s delay                                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BUILD AI PROMPT (Code)                       │
│  • Embeds transcript into extraction prompt                    │
│  • Defines scoring guidelines                                   │
│  • Specifies JSON output structure                             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              EXTRACT CONTACT DATA (AI Agent)                    │
│  Model: Claude 3.5 Sonnet                                       │
│  Extracts: name, email, company, role, scores                  │
│  Output: Structured JSON with 14 fields                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 PARSE AI RESPONSE (Code)                        │
│  • Validates required fields (full_name, contact_details)      │
│  • Extracts email via regex                                     │
│  • Normalizes email (lowercase, trim)                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              GET CRM DATA (Google Sheets Read)                  │
│  Spreadsheet: Prospects                                         │
│  Range: A:P (all 16 columns)                                    │
│  Returns: All existing contacts                                │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              CHECK FOR DUPLICATE (Code)                         │
│  • Searches all rows for exact email match                     │
│  • Returns: isDuplicate flag + matched row index               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DUPLICATE OR NEW? (IF Node)                   │
│  Condition: isDuplicate === true                                │
└─────────────┬───────────────────────────────────┬───────────────┘
              │ TRUE                                │ FALSE
              │ (Email exists in CRM)              │ (New contact)
              ▼                                     ▼
┌──────────────────────────────┐   ┌──────────────────────────────┐
│   PREPARE UPDATE DATA (Code) │   │ PREPARE NEW CONTACT (Code)   │
│                              │   │                              │
│  Smart Merge Logic:          │   │  Format Fields:              │
│  • Keep: name, company, etc  │   │  • All 16 CRM columns        │
│  • Priority: keep HIGHER     │   │  • Set "Added to CRM" = TRUE │
│  • Notes: APPEND with date   │   │  • Platform = "Unknown"      │
│  • Scores: update if HIGHER  │   │                              │
└──────────────┬───────────────┘   └──────────────┬───────────────┘
               │                                   │
               ▼                                   ▼
┌──────────────────────────────┐   ┌──────────────────────────────┐
│ UPDATE EXISTING CONTACT      │   │   ADD NEW CONTACT            │
│ (Google Sheets Update)       │   │   (Google Sheets Append)     │
│                              │   │                              │
│  • Matches by row index      │   │  • Appends to last row       │
│  • Auto-maps all fields      │   │  • Auto-maps all fields      │
└──────────────┬───────────────┘   └──────────────┬───────────────┘
               │                                   │
               └──────────────┬────────────────────┘
                              │
                              ▼
                ┌──────────────────────────────┐
                │      MERGE PATHS (Merge)     │
                │  Combines both branches      │
                └──────────────┬───────────────┘
                               │
                               ▼
                ┌──────────────────────────────┐
                │  SUCCESS NOTIFICATION (Set)  │
                │  Returns: status, message,   │
                │  action (updated/added)      │
                └──────────────────────────────┘
```

## Data Flow Example

### Example Input (Fathom Webhook)
```json
{
  "meeting_id": "abc123",
  "event": "content_ready",
  "timestamp": "2026-01-08T22:00:00Z"
}
```

### Example AI Extraction Output
```json
{
  "full_name": "John Smith",
  "company": "Acme Corp",
  "role": "VP of Marketing",
  "business_type": "SaaS",
  "contact_details": "john.smith@acmecorp.com",
  "priority_level": 8,
  "stage": "In Progress",
  "reply_sentiment": "Positive Reply",
  "notes": "Discussed automation needs for marketing team. Budget approved for Q1.",
  "objective": "Implement n8n workflows for marketing automation",
  "niche_alignment": 3,
  "connection_strength": 2,
  "decision_making_power": 3,
  "network_access": 2
}
```

### Example Google Sheets Row (New Contact)
| A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | P |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| John Smith | 8 | Acme Corp | Unknown | VP of Marketing | SaaS | john.smith@acmecorp.com | In Progress | Positive Reply | [2026-01-08]: Discussed automation needs... | TRUE | Implement n8n workflows | 3 | 2 | 3 | 2 |

### Example Update (Existing Contact)
**Before:**
- Priority Level: 6
- Notes: "[2026-01-05]: Initial call, exploring options"
- Connection Strength: 1

**After Merge:**
- Priority Level: 8 (kept HIGHER)
- Notes: "[2026-01-05]: Initial call, exploring options\n\n[2026-01-08]: Discussed automation needs..." (APPENDED)
- Connection Strength: 2 (updated because NEW is HIGHER)

## Key Decision Points

1. **Email Match** → Determines update vs append
2. **Priority Comparison** → Keeps higher score (existing vs new)
3. **Score Updates** → Only updates if new score exceeds existing
4. **Notes Handling** → Always appends, never overwrites

## Error Scenarios

1. **Missing Email** → Workflow fails at "Parse AI Response" with validation error
2. **Fathom API Down** → HTTP Request retries 3x before failing
3. **Invalid Meeting ID** → HTTP Request returns 404, workflow stops
4. **AI Extraction Fails** → Agent returns error, workflow stops
5. **Google Sheets Permission** → Sheets operations fail if credential missing/invalid
