# V10 Pre-Chunk 0 - Node-by-Node Design

**Version:** V10 Phase 1
**Date:** January 19, 2026
**Status:** Design Draft

---

## Design Principles (from Sway's input)

1. **Process everything, flag uncertainty** - Don't block, but notify Eugene to review
2. **Sequential analysis, batch decision** - Analyze PDFs one-by-one, THEN vote on common identifier
3. **Project name > Email match** - If project matches but email doesn't, use project name
4. **Email body = bonus validation** - Parse email text for project/client mentions
5. **Time is not critical** - Quality over speed

---

## High-Level Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 1: INTAKE                          │
├─────────────────────────────────────────────────────────────┤
│ 1. Gmail Trigger                                            │
│ 2. Extract Email Metadata (from, subject, body)             │
│ 3. Filter PDF/ZIP Attachments                               │
│ 4. Count Attachments → Single or Multiple?                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                PHASE 2: SEQUENTIAL ANALYSIS                 │
├─────────────────────────────────────────────────────────────┤
│ 5. Upload ALL to Temp Staging                               │
│ 6. Loop: For Each PDF                                       │
│    6a. Download PDF                                         │
│    6b. Convert to Base64                                    │
│    6c. Claude Vision → Extract identifier candidates        │
│    6d. Store result in array                                │
│ 7. Parse Email Body → Extract any project/client mentions   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              PHASE 3: BATCH DECISION (VOTING)               │
├─────────────────────────────────────────────────────────────┤
│ 8. Aggregate all extracted identifiers                      │
│ 9. Find common denominator (most frequent/confident)        │
│ 10. Add email body matches as validation weight             │
│ 11. Determine: project_name + sender_email                  │
│ 12. Calculate confidence score                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               PHASE 4: REGISTRY MATCHING                    │
├─────────────────────────────────────────────────────────────┤
│ 13. Lookup registry by project_name (PRIMARY)               │
│ 14. If no match → Lookup by sender_email (SECONDARY)        │
│ 15. Decision Gate:                                          │
│     - EXISTING: Project found in registry                   │
│     - NEW_FROM_KNOWN: New project from known sender         │
│     - COMPLETELY_NEW: New sender, new project               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              PHASE 5: ROUTING + FLAGGING                    │
├─────────────────────────────────────────────────────────────┤
│ 16. Check if needs review flag:                             │
│     - Single doc from new sender? → FLAG                    │
│     - Low confidence score? → FLAG                          │
│     - Project match but email mismatch? → FLAG (info only)  │
│ 17. If FLAG → Send review email to Eugene                   │
│ 18. Route to appropriate chunk (Chunk 0 or direct to 2.5)   │
│ 19. Mark email as read                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Detailed Node Design

### PHASE 1: INTAKE

#### Node 1: Gmail Trigger
```
Type: n8n-nodes-base.gmailTrigger
Purpose: Monitor for unread emails with Eugene label
Config:
  - Labels: Eugene
  - Filters: has:attachment
  - Poll interval: 1 minute
Output:
  - emailId
  - from (sender email)
  - subject
  - body (plain text)
  - attachments[]
```

#### Node 2: Extract Email Metadata
```
Type: n8n-nodes-base.code
Purpose: Extract and normalize email metadata for later use
Input: Gmail trigger output
Output:
  {
    emailId: string,
    senderEmail: string (normalized, lowercase),
    senderName: string (from "Name <email>" format),
    subject: string,
    bodyText: string (plain text, cleaned),
    receivedAt: ISO timestamp,
    attachmentCount: number
  }
```

#### Node 3: Filter PDF/ZIP Attachments
```
Type: n8n-nodes-base.code
Purpose: Keep only PDF and ZIP files
Input: Attachments array
Output: Filtered array of {filename, mimeType, attachmentId}
```

#### Node 4: Count & Route
```
Type: n8n-nodes-base.if
Purpose: Determine single vs multiple attachments
Condition: attachmentCount === 1
Output 0 (TRUE): Single attachment path
Output 1 (FALSE): Multiple attachments path

NOTE: Both paths converge at Phase 3, difference is flagging
```

---

### PHASE 2: SEQUENTIAL ANALYSIS

#### Node 5: Upload All to Temp Staging
```
Type: n8n-nodes-base.googleDrive (loop or splitInBatches)
Purpose: Upload all attachments to temp folder
Config:
  - Folder: _Temp_Staging (ID: TBD)
  - Preserve original filename
Output: Array of {fileId, fileName, driveUrl}
```

#### Node 6: Loop - Analyze Each PDF
```
Type: n8n-nodes-base.splitInBatches + loop
Purpose: Process each PDF individually

For each PDF:
```

##### Node 6a: Download PDF
```
Type: n8n-nodes-base.googleDrive
Operation: download
Input: fileId
Output: Binary PDF data
```

##### Node 6b: Convert to Base64
```
Type: n8n-nodes-base.code
Purpose: Convert binary to base64 for Claude Vision
Output: {
  imageData: {
    type: "base64",
    media_type: "application/pdf",
    data: "base64string..."
  }
}
```

##### Node 6c: Claude Vision - Extract Identifier
```
Type: n8n-nodes-base.httpRequest
URL: https://api.anthropic.com/v1/messages
Method: POST
Headers:
  - x-api-key: {{ Anthropic credential }}
  - anthropic-version: 2023-06-01

Body:
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 300,  // FIXED from v9's 100
  "messages": [{
    "role": "user",
    "content": [
      {
        "type": "document",
        "source": {
          "type": "base64",
          "media_type": "application/pdf",
          "data": "{{ base64 data }}"
        }
      },
      {
        "type": "text",
        "text": "Extract the project or client identifier from this German real estate document.\n\nLook for (in priority order):\n1. Property/Villa name (e.g., 'Villa Martens', 'Adolf-Martenstraße 15')\n2. Project name (e.g., 'Projekt Schlossbergstraße')\n3. Company name (e.g., 'PROPOS GmbH')\n4. Client/Family name (e.g., 'Familie Wagner')\n\nReturn JSON format:\n{\n  \"identifier\": \"extracted name\",\n  \"type\": \"property|project|company|client\",\n  \"confidence\": 0.0-1.0,\n  \"alternates\": [\"other possible names\"]\n}\n\nIf nothing found, return: {\"identifier\": \"UNKNOWN\", \"type\": \"unknown\", \"confidence\": 0}"
      }
    ]
  }]
}

Output: Parsed JSON with identifier, type, confidence, alternates
```

##### Node 6d: Store Result
```
Type: n8n-nodes-base.code
Purpose: Append result to analysis array
Output: Array of all PDF analysis results
```

#### Node 7: Parse Email Body
```
Type: n8n-nodes-base.code
Purpose: Extract potential project/client mentions from email body

Logic:
1. Look for patterns:
   - "Projekt [Name]"
   - "Villa [Name]"
   - "betreff: [Name]"
   - Known project names from registry
   - Street addresses (Straße/Strasse patterns)

2. Check signature block for company names

3. Return:
{
  bodyMentions: ["Project A", "Villa B"],
  signatureMentions: ["Company GmbH"],
  matchesFromRegistry: ["Known Project"] // if any
}
```

---

### PHASE 3: BATCH DECISION (VOTING)

#### Node 8: Aggregate Results
```
Type: n8n-nodes-base.code
Purpose: Combine all PDF analysis results + email body mentions

Input:
  - pdfResults: [{identifier, type, confidence, alternates}, ...]
  - emailBodyResults: {bodyMentions, signatureMentions, matchesFromRegistry}
  - metadata: {senderEmail, attachmentCount}

Output:
{
  allIdentifiers: [
    {value: "Villa Martens", source: "pdf1", type: "property", confidence: 0.9},
    {value: "Villa Martens", source: "pdf2", type: "property", confidence: 0.85},
    {value: "Villa Martens", source: "email_body", type: "mention", confidence: 0.7},
    ...
  ],
  senderEmail: "sender@example.com",
  attachmentCount: 3
}
```

#### Node 9: Find Common Denominator
```
Type: n8n-nodes-base.code
Purpose: Vote on most likely identifier

Logic:
1. Group identifiers by normalized value
2. Score each group:
   - Base score: count of occurrences
   - Weighted by confidence
   - Bonus if appears in email body (+0.5)
   - Bonus if matches registry (+1.0)
3. Select highest scoring identifier
4. Calculate overall confidence

Output:
{
  selectedIdentifier: "Villa Martens",
  identifierType: "property",
  overallConfidence: 0.87,
  voteBreakdown: {
    "Villa Martens": {count: 3, score: 2.95},
    "PROPOS GmbH": {count: 1, score: 0.8}
  },
  emailBodyValidated: true
}
```

#### Node 10-11: Finalize Identification
```
Type: n8n-nodes-base.code
Purpose: Create final identification record

Output:
{
  project_name: "Villa Martens",
  project_name_normalized: "villa_martens",
  identifier_type: "property",
  sender_email: "sender@example.com",
  confidence: 0.87,
  attachment_count: 3,
  email_body_validated: true,
  analysis_method: "batch_voting",

  // Flagging conditions
  is_single_doc_new_sender: false,
  is_low_confidence: false,
  needs_review: false
}
```

---

### PHASE 4: REGISTRY MATCHING

#### Node 13: Lookup by Project Name (PRIMARY)
```
Type: n8n-nodes-base.googleSheets
Operation: Read with filter
Sheet: Client Registry
Filter: project_name_normalized = {{ normalized name }}

Output: Matching rows or empty
```

#### Node 14: Lookup by Sender Email (SECONDARY)
```
Type: n8n-nodes-base.googleSheets
Operation: Read with filter
Sheet: Client Registry
Filter: sender_email = {{ sender email }}
Condition: Only run if Node 13 returned empty

Output: Matching rows or empty
```

#### Node 15: Decision Gate
```
Type: n8n-nodes-base.switch
Purpose: Route based on match results

Cases:
1. PROJECT_FOUND:
   - Project name matched in registry
   - Use existing folder structure
   - Route: EXISTING path

2. EMAIL_FOUND_DIFF_PROJECT:
   - Sender email matched but project name different
   - Create new folder structure under same registry entry?
   - OR create new registry entry with same email?
   - Route: NEW_FROM_KNOWN path

3. NO_MATCH:
   - Neither project nor email found
   - Create new registry entry + folders
   - Route: COMPLETELY_NEW path
```

---

### PHASE 5: ROUTING + FLAGGING

#### Node 16: Check Flag Conditions
```
Type: n8n-nodes-base.code
Purpose: Determine if needs_review flag should be set

Conditions that trigger flag:
1. Single document AND new sender (not in registry)
2. Confidence score < 0.6
3. Project matched but email didn't (informational flag)

Output:
{
  needs_review: true/false,
  flag_reasons: ["single_doc_new_sender", "low_confidence"],
  review_priority: "high" | "medium" | "low"
}
```

#### Node 17: Send Review Email (Conditional)
```
Type: n8n-nodes-base.gmail
Condition: Only if needs_review === true
To: eugene@ama-capital.de (or configured review email)
Subject: "[Review Needed] New document: {{ project_name }}"
Body:
  "A new document has been processed that may need your review.

  Project: {{ project_name }}
  Confidence: {{ confidence }}%
  Sender: {{ sender_email }}
  Documents: {{ attachment_count }}

  Reason for review:
  {{ flag_reasons joined }}

  Please verify the classification is correct in the Client Tracker."
```

#### Node 18: Route to Chunk
```
Type: n8n-nodes-base.switch
Purpose: Send to appropriate workflow

Routes:
- EXISTING → Execute Chunk 2.5 (skip Chunk 0, folders exist)
- NEW_FROM_KNOWN → Execute Chunk 0 (create new subfolder)
- COMPLETELY_NEW → Execute Chunk 0 (create full folder structure)
```

#### Node 19: Mark Email as Read
```
Type: n8n-nodes-base.gmail
Operation: Mark as read
Input: emailId
```

---

## Registry Schema Update

**Current columns:**
- client_name
- folder_id
- (others TBD)

**New columns needed:**
| Column | Type | Purpose |
|--------|------|---------|
| sender_email | string | Email address of sender |
| project_name_normalized | string | Lowercase, no special chars |
| last_updated | datetime | When last document added |
| document_count | number | Total docs for this project |
| needs_review | boolean | Flagged for Eugene's review |

---

## Flagging Matrix

| Situation | Flag? | Priority | Review Email? |
|-----------|-------|----------|---------------|
| Single doc, new sender | YES | HIGH | YES |
| Confidence < 0.6 | YES | HIGH | YES |
| Confidence 0.6-0.8 | YES | MEDIUM | NO (just log) |
| Project match, email mismatch | YES | LOW | NO (just log) |
| Multiple docs, high confidence | NO | - | NO |

---

## Open Questions for Implementation

1. **Chunk 0 or Chunk 2.5 for NEW_FROM_KNOWN?**
   - Same sender but different project - do we create nested folders or separate?

2. **Registry structure for multi-project senders**
   - One row per sender with array of projects?
   - Or one row per project (same sender appears multiple times)?

3. **What is the review email address?**
   - Eugene's direct email?
   - A shared inbox?

4. **Confidence threshold tuning**
   - Start with 0.6, adjust based on real-world results?

---

## Next Steps

1. [ ] Confirm registry schema changes with Sway
2. [ ] Investigate Chunk 2.5 filing + tracker issues (BLOCKER)
3. [ ] Build Phase 1-2 nodes (intake + sequential analysis)
4. [ ] Build Phase 3 nodes (batch decision)
5. [ ] Build Phase 4-5 nodes (matching + routing)
6. [ ] Test with Gmail + alias approach
7. [ ] Tune confidence thresholds based on results

---

**Document Version:** 1.0
**Created:** 2026-01-19
