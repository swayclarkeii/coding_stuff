# Staff Pre-Interview Questionnaire - Flow Diagram

## Visual Workflow Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TALLY FORM SUBMISSION                        │
│  (User completes pre-interview questionnaire on Tally platform)     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ POST webhook
                             │ (JSON payload)
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  NODE 1: Webhook Trigger                                            │
│  ─────────────────────────                                          │
│  • Receives POST request from Tally                                 │
│  • Path: /pre-interview-questionnaire                               │
│  • Responds immediately (200 OK)                                    │
│                                                                     │
│  Output: Raw webhook payload                                        │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ JSON payload
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  NODE 2: Parse Tally Payload (Code)                                 │
│  ────────────────────────────────────                               │
│  • Extracts fields from Tally JSON structure                        │
│  • Flexible parsing (handles multiple field name variations)        │
│  • Maps to standardized field names                                 │
│                                                                     │
│  Extracted Fields:                                                  │
│    ✓ name          (full name of respondent)                        │
│    ✓ role          (job title/role)                                 │
│    ✓ tools         (daily software/apps used)                       │
│    ✓ tasks         (3 most frequent tasks)                          │
│    ✓ frustration   (most frustrating part of job)                   │
│    ✓ quick_win     (one thing to fix)                               │
│    ✓ email         (respondent's email)                             │
│    ✓ timestamp     (submission time)                                │
│                                                                     │
│  Output: Structured JSON object with mapped fields                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ Structured data
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  NODE 3: Append to Sheet (Google Sheets)                            │
│  ──────────────────────────────────────────                         │
│  • Connects to Google Sheets via OAuth2                             │
│  • Sheet: "Pre-Interview Responses"                                 │
│  • Auto-maps JSON fields to matching column headers                 │
│  • Appends new row at bottom of sheet                               │
│                                                                     │
│  Sheet Columns:                                                     │
│  | Name | Role | Tools | Tasks | Frustration | Quick_win | Email |  │
│                                                                     │
│  Output: Confirmation of row append (passes data forward)           │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ Data + confirmation
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  NODE 4: Notify Sway (Gmail)                                        │
│  ──────────────────────────────                                     │
│  • Sends HTML-formatted email via Gmail OAuth2                      │
│  • To: sway@oloxa.ai                                                │
│  • Subject: "New Pre-Interview Submission: [Name]"                  │
│  • Body: Formatted summary of all form responses                    │
│                                                                     │
│  Email Content Includes:                                            │
│    • Timestamp                                                      │
│    • Respondent details (name, role, email)                         │
│    • Tools & software used                                          │
│    • 3 most frequent tasks                                          │
│    • Most frustrating part of job                                   │
│    • One thing to fix (quick win)                                   │
│                                                                     │
│  Output: Email sent confirmation                                    │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             │
                             ▼
                    ┌────────────────┐
                    │  WORKFLOW END  │
                    │  ✓ Complete    │
                    └────────────────┘
```

## Data Flow Example

### Input (from Tally webhook)
```json
{
  "data": {
    "fields": {
      "name": "Sarah Johnson",
      "role": "Operations Manager",
      "tools": "Monday.com, Slack, Google Workspace",
      "tasks": "Team coordination, Process documentation, Budget tracking",
      "frustration": "Too many manual status update requests",
      "quick_win": "Automate weekly status reports",
      "email": "sarah.j@company.com"
    }
  },
  "createdAt": "2026-01-24T14:30:00Z"
}
```

### After Parse Tally Payload
```json
{
  "name": "Sarah Johnson",
  "role": "Operations Manager",
  "tools": "Monday.com, Slack, Google Workspace",
  "tasks": "Team coordination, Process documentation, Budget tracking",
  "frustration": "Too many manual status update requests",
  "quick_win": "Automate weekly status reports",
  "email": "sarah.j@company.com",
  "timestamp": "2026-01-24T14:30:00Z"
}
```

### Google Sheet Row
| Name | Role | Tools | Tasks | Frustration | Quick_win | Email | Timestamp |
|------|------|-------|-------|-------------|-----------|-------|-----------|
| Sarah Johnson | Operations Manager | Monday.com, Slack, Google Workspace | Team coordination, Process documentation, Budget tracking | Too many manual status update requests | Automate weekly status reports | sarah.j@company.com | 2026-01-24T14:30:00Z |

### Email to Sway
```
Subject: New Pre-Interview Submission: Sarah Johnson

─────────────────────────────────

New Pre-Interview Questionnaire Submission

Timestamp: 2026-01-24T14:30:00Z

Respondent Details
──────────────────
Name: Sarah Johnson
Role: Operations Manager
Email: sarah.j@company.com

Tools & Software
────────────────
Monday.com, Slack, Google Workspace

3 Most Frequent Tasks
──────────────────────
Team coordination, Process documentation, Budget tracking

Most Frustrating Part of Job
─────────────────────────────
Too many manual status update requests

One Thing to Fix
────────────────
Automate weekly status reports

────────────────────────────────────────────────────────────
This submission has been automatically saved to the
Pre-Interview Responses Google Sheet.
```

## Error Handling (Recommended Future Enhancement)

```
┌─────────────────┐
│  Any Node Fails │
│                 │
└────────┬────────┘
         │
         │ On Error
         ▼
┌─────────────────────────┐
│  Error Notification     │
│  (Future Enhancement)   │
│                         │
│  • Log to error sheet   │
│  • Send error alert     │
│  • Retry logic          │
└─────────────────────────┘
```

## Webhook URL Format

Once workflow is activated, webhook URL will be:

```
https://[your-n8n-instance].app.n8n.cloud/webhook/pre-interview-questionnaire
```

Or if self-hosted:

```
https://[your-n8n-domain]/webhook/pre-interview-questionnaire
```

## Configuration Checklist

- [ ] Create Google Sheet with exact column headers
- [ ] Configure Google Sheets OAuth2 credential
- [ ] Configure Gmail OAuth2 credential
- [ ] Update Spreadsheet ID in "Append to Sheet" node
- [ ] Activate workflow in n8n
- [ ] Copy webhook URL
- [ ] Configure Tally form with webhook URL
- [ ] Test with sample submission
- [ ] Verify sheet row appears
- [ ] Verify email notification arrives

## Performance Notes

- **Average execution time:** 2-4 seconds
- **Bottlenecks:** Google Sheets API write (1-2s), Gmail send (1-2s)
- **Throughput:** Handles concurrent submissions (n8n queues them)
- **Reliability:** Webhook responds immediately; processing happens async

## Scalability Considerations

- **Current design:** Suitable for <100 submissions/day
- **For higher volume:**
  - Consider batching sheet appends
  - Add rate limiting on Tally side
  - Use Google Sheets API batch update
  - Consider database instead of sheets for >1000 submissions/day
