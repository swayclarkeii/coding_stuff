# V10 Pre-Chunk 0 Implementation Plan

**Workflow ID:** YGXWjWcBIk66ArvT
**Workflow Name:** AMA Pre-Chunk 0 - REBUILT v1
**Version:** V10 Phase 1
**Date:** January 19, 2026
**Status:** Implementation Plan

---

## Implementation Strategy

**Approach:** Incremental build with validation at each phase

V9 → V10 is a **major architecture change** from individual analysis to batch voting. Rather than trying to modify all existing nodes, I'll:

1. **Keep what works:** Gmail trigger, some infrastructure nodes
2. **Replace core logic:** New batch analysis flow
3. **Validate incrementally:** Test each phase before moving to next

---

## Current V9 Structure (To Be Replaced)

**Current flow:**
1. Gmail Trigger → Filter Attachments → Upload to Temp
2. Download PDF → Convert to Base64 → Claude Vision (single doc)
3. Parse Response → Normalize → Registry Lookup
4. Decision Gate → Route to Chunk 0/2.5 or Unknowns

**Problems with V9:**
- Analyzes only first PDF (ignores multiple attachments)
- No voting/consensus mechanism
- Unreliable client identification
- No email body parsing
- No sender email tracking

---

## V10 Architecture (New)

**New flow (5 phases, 18 key nodes):**

### PHASE 1: INTAKE (4 nodes)
1. Gmail Trigger (REUSE existing)
2. Extract Email Metadata (NEW - Code node)
3. Filter PDF/ZIP Attachments (REUSE/MODIFY existing)
4. Count & Route (NEW - IF node for single vs multiple)

### PHASE 2: SEQUENTIAL ANALYSIS (7 nodes)
5. Upload All to Temp Staging (REUSE/MODIFY existing)
6. Loop: For Each PDF (NEW - splitInBatches wrapper)
   - 6a. Download PDF (NEW - inside loop)
   - 6b. Convert to Base64 (NEW - inside loop)
   - 6c. Claude Vision Extract (NEW - inside loop)
   - 6d. Store Result (NEW - accumulate array)
7. Parse Email Body (NEW - Code node)

### PHASE 3: BATCH DECISION (4 nodes)
8. Aggregate Results (NEW - Code node)
9. Find Common Denominator (NEW - Code node with voting logic)
10-11. Finalize Identification (NEW - Code node)

### PHASE 4: REGISTRY MATCHING (3 nodes)
12. Lookup by Project Name (MODIFY existing registry lookup)
13. Lookup by Sender Email (NEW - secondary lookup)
14. Decision Gate (REUSE/MODIFY existing switch)

### PHASE 5: ROUTING + FLAGGING (5 nodes)
15. Check Flag Conditions (NEW - Code node)
16. Send Review Email (NEW - Gmail conditional)
17. Route to Chunk (MODIFY existing execute workflow)
18. Mark Email as Read (REUSE existing)
19. NoOp/Complete (REUSE existing)

**Total:** 18 core nodes (not counting loop internals and utility nodes)

---

## Node-by-Node Implementation Plan

### PHASE 1: INTAKE

#### Node 1: Gmail Trigger (REUSE)
```yaml
Status: Keep existing
Node ID: gmail-trigger-001
Type: n8n-nodes-base.gmailTrigger
Action: No changes needed
```

#### Node 2: Extract Email Metadata (NEW)
```yaml
Status: Create new
Type: n8n-nodes-base.code
Purpose: Extract sender email, name, subject, body for later analysis
Position: After Gmail Trigger

Code logic:
- Extract from field: "Name <email>" format
- Normalize sender email to lowercase
- Extract plain text body
- Count attachments
- Store for later use in voting

Output:
{
  emailId: string,
  senderEmail: string (lowercase),
  senderName: string,
  subject: string,
  bodyText: string,
  receivedAt: ISO timestamp,
  attachmentCount: number,
  attachments: array
}
```

#### Node 3: Filter PDF/ZIP Attachments (MODIFY)
```yaml
Status: Modify existing node
Node ID: filter-attachments-001
Type: n8n-nodes-base.code
Action: Update to keep metadata from Node 2

Modification:
- Keep existing PDF/ZIP filtering logic
- Add email metadata passthrough
- Ensure attachments array is complete
```

#### Node 4: Count & Route (NEW)
```yaml
Status: Create new
Type: n8n-nodes-base.if
Purpose: Single vs multiple attachment routing
Position: After Filter Attachments

Condition: attachmentCount === 1
Output 0 (TRUE): Single attachment path (will be flagged later)
Output 1 (FALSE): Multiple attachments path

Note: Both paths converge at Phase 3, difference is flagging
```

---

### PHASE 2: SEQUENTIAL ANALYSIS

#### Node 5: Upload All to Temp Staging (MODIFY)
```yaml
Status: Modify existing
Node ID: upload-pdf-gdrive-001
Type: n8n-nodes-base.googleDrive
Action: Ensure it uploads ALL attachments, not just first

Current issue: May only upload first attachment
Fix: Ensure loop mode or splitInBatches for multiple uploads
```

#### Node 6: Loop Through PDFs (NEW - Split In Batches)
```yaml
Status: Create new
Type: n8n-nodes-base.splitInBatches
Purpose: Process each PDF sequentially
Position: After Upload to Temp

Config:
- Batch size: 1 (process one PDF at a time)
- Input: Array of uploaded file IDs
- Reset after completion: Yes

Why sequential not parallel:
- Token cost management
- Easier to debug
- Simpler state management
- Speed not critical per design doc
```

##### Node 6a: Download PDF (NEW - Inside Loop)
```yaml
Status: Create new
Type: n8n-nodes-base.googleDrive
Resource: File
Operation: Download
Position: Inside loop

Config:
- File ID: from splitInBatches current item
- Output as binary
```

##### Node 6b: Convert to Base64 (NEW - Inside Loop)
```yaml
Status: Create new
Type: n8n-nodes-base.code
Position: Inside loop, after download

Code logic:
- Access binary data from previous node
- Convert to base64 string
- Format for Claude Vision API
- Preserve filename for tracking

Output:
{
  fileName: string,
  base64Data: string,
  mimeType: "application/pdf"
}
```

##### Node 6c: Claude Vision Extract (NEW - Inside Loop)
```yaml
Status: Create new
Type: n8n-nodes-base.httpRequest
Position: Inside loop
URL: https://api.anthropic.com/v1/messages
Method: POST

Headers:
- x-api-key: {{ credential }}
- anthropic-version: 2023-06-01
- content-type: application/json

Body:
{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 300,
  "messages": [{
    "role": "user",
    "content": [
      {
        "type": "document",
        "source": {
          "type": "base64",
          "media_type": "application/pdf",
          "data": "{{ $json.base64Data }}"
        }
      },
      {
        "type": "text",
        "text": "Extract the project or client identifier from this German real estate document.\n\nLook for (in priority order):\n1. Property/Villa name (e.g., 'Villa Martens', 'Adolf-Martenstraße 15')\n2. Project name (e.g., 'Projekt Schlossbergstraße')\n3. Company name (e.g., 'PROPOS GmbH')\n4. Client/Family name (e.g., 'Familie Wagner')\n\nReturn JSON format:\n{\n  \"identifier\": \"extracted name\",\n  \"type\": \"property|project|company|client\",\n  \"confidence\": 0.0-1.0,\n  \"alternates\": [\"other possible names\"]\n}\n\nIf nothing found, return: {\"identifier\": \"UNKNOWN\", \"type\": \"unknown\", \"confidence\": 0}"
      }
    ]
  }]
}

Response parsing: Next node
```

##### Node 6d: Store Result (NEW - Inside Loop)
```yaml
Status: Create new
Type: n8n-nodes-base.code
Purpose: Append result to analysis array
Position: Inside loop, after Claude Vision

Code logic:
- Parse Claude API response
- Extract identifier, type, confidence, alternates
- Append to persistent array (workflow static data or itemlist)
- Track which PDF this came from

Output: Accumulated array for voting
```

#### Node 7: Parse Email Body (NEW)
```yaml
Status: Create new
Type: n8n-nodes-base.code
Position: After loop completes, parallel to analysis
Purpose: Extract project/client mentions from email text

Code logic:
1. Regex patterns for German real estate:
   - "Projekt [Name]"
   - "Villa [Name]"
   - "Straße/Strasse" patterns (addresses)
   - "betreff: [Name]"

2. Signature extraction:
   - Look for company names ending in GmbH, AG, etc.
   - Extract from signature block (usually after "--" or "Mit freundlichen Grüßen")

3. Registry cross-reference (optional):
   - If we have cached registry data, check if any known projects mentioned

Output:
{
  bodyMentions: ["Project A", "Villa B"],
  signatureMentions: ["Company GmbH"],
  confidence: 0.5-0.8 (lower than PDF analysis)
}
```

---

### PHASE 3: BATCH DECISION (VOTING)

#### Node 8: Aggregate Results (NEW)
```yaml
Status: Create new
Type: n8n-nodes-base.code
Purpose: Combine all PDF results + email body results
Position: After loop + email body parsing

Input sources:
- PDF analysis array from Node 6d
- Email body results from Node 7
- Email metadata from Node 2

Code logic:
- Merge all identifier candidates
- Tag each with source (pdf1, pdf2, email_body, etc.)
- Preserve confidence scores
- Track attachment count for flagging

Output:
{
  allIdentifiers: [
    {value: "Villa Martens", source: "pdf1", type: "property", confidence: 0.9},
    {value: "Villa Martens", source: "pdf2", type: "property", confidence: 0.85},
    {value: "Martens", source: "email_body", type: "mention", confidence: 0.6},
    ...
  ],
  senderEmail: "sender@example.com",
  attachmentCount: 3
}
```

#### Node 9: Find Common Denominator (NEW)
```yaml
Status: Create new
Type: n8n-nodes-base.code
Purpose: VOTING LOGIC - Find most likely identifier
Position: After aggregate

Voting algorithm:
1. Normalize all identifiers (lowercase, remove special chars)
2. Group by normalized value
3. Score each group:
   - Base: count of occurrences × avg confidence
   - Bonus: +0.5 if appears in email body
   - Bonus: +1.0 if matches known registry project (if cached)
4. Select highest scoring identifier
5. Calculate overall confidence (avg of group confidences)

Normalization function (CRITICAL):
- lowercase
- trim whitespace
- replace umlauts: ä→ae, ö→oe, ü→ue, ß→ss
- remove GmbH, AG, & Co., KG, etc.
- replace non-alphanumeric with underscore
- collapse multiple underscores

Example:
"Villa Martens GmbH" → "villa_martens"
"PROPOS Schlossbergstraße" → "propos_schlossbergstrasse"

Output:
{
  selectedIdentifier: "Villa Martens",
  selectedIdentifierNormalized: "villa_martens",
  identifierType: "property",
  overallConfidence: 0.87,
  voteBreakdown: {
    "villa_martens": {count: 3, score: 2.95, sources: ["pdf1", "pdf2", "email"]},
    "propos_gmbh": {count: 1, score: 0.8, sources: ["pdf3"]}
  },
  emailBodyValidated: true,
  attachmentCount: 3
}
```

#### Node 10-11: Finalize Identification (NEW)
```yaml
Status: Create new
Type: n8n-nodes-base.code
Purpose: Create final identification record with flagging metadata
Position: After voting

Code logic:
- Take voting result
- Add flagging conditions
- Prepare for registry lookup

Flagging logic:
- is_single_doc_new_sender: attachmentCount === 1 AND sender not in registry
- is_low_confidence: overallConfidence < 0.6
- is_medium_confidence: overallConfidence >= 0.6 AND < 0.8
- needs_high_priority_review: is_single_doc_new_sender OR is_low_confidence

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

  // Flagging
  is_single_doc_new_sender: false,
  is_low_confidence: false,
  is_medium_confidence: false,
  needs_review: false,
  review_priority: null // or "high", "medium", "low"
}
```

---

### PHASE 4: REGISTRY MATCHING

#### Node 12: Lookup by Project Name (MODIFY)
```yaml
Status: Modify existing
Node ID: lookup-registry-001
Type: n8n-nodes-base.googleSheets
Resource: Sheet Within Document
Operation: Get Row(s)

Modifications needed:
1. Change filter to use project_name_normalized
2. Add new column: sender_email to registry
3. Add new column: project_name_normalized to registry

Filter:
- Column: project_name_normalized
- Value: {{ $json.project_name_normalized }}

Output: Matching rows or empty
```

#### Node 13: Lookup by Sender Email (NEW - SECONDARY)
```yaml
Status: Create new
Type: n8n-nodes-base.googleSheets
Resource: Sheet Within Document
Operation: Get Row(s)
Purpose: Fallback if project name not found
Position: After Node 12

Condition: Only run if Node 12 returned empty

Filter:
- Column: sender_email
- Value: {{ $json.sender_email }}

Output: Matching rows or empty
```

#### Node 14: Decision Gate (MODIFY)
```yaml
Status: Modify existing
Node ID: decision-gate-001
Type: n8n-nodes-base.switch
Purpose: Route based on registry match results

Current routes: UNKNOWN, NEW, EXISTING
New routes needed: 4 routes

Route 0: PROJECT_FOUND (EXISTING)
- Condition: Node 12 returned rows
- Meaning: Project name matched in registry
- Action: Use existing folder structure
- Next: Move to _Staging → Chunk 2.5

Route 1: EMAIL_FOUND_DIFF_PROJECT (NEW_FROM_KNOWN)
- Condition: Node 12 empty BUT Node 13 returned rows
- Meaning: Same sender, different project
- Action: Create new folders under same registry entry OR new entry with same email
- Next: Chunk 0 → Create folders

Route 2: NO_MATCH_HIGH_CONFIDENCE (COMPLETELY_NEW - Auto)
- Condition: Both empty AND confidence >= 0.8
- Meaning: New sender, new project, but confident
- Action: Create new registry entry + folders, minimal flagging
- Next: Chunk 0 → Create folders

Route 3: NO_MATCH_LOW_CONFIDENCE (COMPLETELY_NEW - Flag)
- Condition: Both empty AND confidence < 0.8
- Meaning: New sender, new project, uncertain
- Action: Create new entry + folders BUT flag for review
- Next: Chunk 0 → Create folders + send review email

Fallback: UNKNOWN (existing behavior)
- Condition: Catch-all
- Next: Unknowns folder
```

---

### PHASE 5: ROUTING + FLAGGING

#### Node 15: Check Flag Conditions (NEW)
```yaml
Status: Create new
Type: n8n-nodes-base.code
Purpose: Final flagging decision
Position: Before routing to chunks

Input: Identification record + registry match result

Flagging matrix:
1. Single doc + new sender → FLAG HIGH, send email
2. Confidence < 0.6 → FLAG HIGH, send email
3. Confidence 0.6-0.8 → FLAG MEDIUM, log only
4. Project match but email mismatch → FLAG LOW, log only
5. Multiple docs + high confidence → NO FLAG

Output:
{
  needs_review: true/false,
  flag_reasons: ["single_doc_new_sender", "low_confidence"],
  review_priority: "high" | "medium" | "low",
  send_email: true/false,

  // Pass through all previous data
  ...identificationRecord,
  ...registryMatchResult
}
```

#### Node 16: Send Review Email (NEW - Conditional)
```yaml
Status: Create new
Type: n8n-nodes-base.gmail
Resource: Message
Operation: Send
Purpose: Notify Eugene of flagged documents
Position: After flag check

Condition: Run only if send_email === true

To: eugene@ama-capital.de
Subject: [Review Needed - {{ $json.review_priority | upper }}] {{ $json.project_name }}

Body (HTML):
<h2>Document Review Required</h2>

<p>A new document has been processed that needs your attention.</p>

<h3>Details:</h3>
<ul>
  <li><strong>Project:</strong> {{ $json.project_name }}</li>
  <li><strong>Confidence:</strong> {{ $json.confidence * 100 }}%</li>
  <li><strong>Sender:</strong> {{ $json.sender_email }}</li>
  <li><strong>Number of Documents:</strong> {{ $json.attachment_count }}</li>
  <li><strong>Priority:</strong> {{ $json.review_priority | upper }}</li>
</ul>

<h3>Reason for Review:</h3>
<ul>
  {{ for reason in $json.flag_reasons }}
    <li>{{ reason | replace("_", " ") | title }}</li>
  {{ endfor }}
</ul>

<p>Please verify the classification in the <a href="REGISTRY_SHEET_URL">Client Tracker</a>.</p>

<p><em>Automated by Eugene Doc Organizer V10</em></p>
```

#### Node 17: Route to Chunk (MODIFY)
```yaml
Status: Modify existing
Type: n8n-nodes-base.switch or IF
Purpose: Route to appropriate chunk workflow
Position: After email (if sent)

Routes:
- EXISTING → Execute Chunk 2.5 (folders exist, skip Chunk 0)
- NEW/UNKNOWN → Execute Chunk 0 (create folders first)

Pass through:
- All identification data
- Registry match result
- Flagging metadata for logging
```

#### Node 18: Mark Email as Read (REUSE)
```yaml
Status: Keep existing
Node ID: mark-read-*-001 (multiple versions)
Type: n8n-nodes-base.gmail
Resource: Message
Operation: Mark as Read

Action: Ensure all paths mark email as read
```

#### Node 19: NoOp / Complete (REUSE)
```yaml
Status: Keep existing
Node ID: noop-*-complete-001
Type: n8n-nodes-base.noOp

Action: Terminal nodes for each path
```

---

## Registry Schema Updates

**Current columns** (to verify):
- client_name
- folder_id
- (others TBD - need to check actual sheet)

**New columns to ADD:**
| Column Name | Type | Purpose | Example |
|-------------|------|---------|---------|
| sender_email | string | Email address of document sender | "sender@example.com" |
| project_name_normalized | string | Normalized project name for matching | "villa_martens" |
| last_document_date | date | When last document was added | "2026-01-19" |
| document_count | number | Total documents for this project | 15 |
| needs_review | boolean | Flagged for Eugene review | TRUE/FALSE |
| confidence_avg | number | Average confidence of identifications | 0.87 |

**Migration plan:**
1. Add new columns to registry sheet
2. Backfill project_name_normalized from client_name
3. Add sender_email manually or from first document of each project
4. Set defaults for new fields

---

## Implementation Order

**Phase-by-phase approach:**

### Sprint 1: Intake + Email Parsing (Nodes 1-4, 7)
- Create Extract Email Metadata node
- Modify Filter Attachments to preserve metadata
- Create Count & Route IF node
- Create Parse Email Body node
- Test: Verify email data extraction works

### Sprint 2: Sequential Analysis (Nodes 5-6d)
- Modify Upload to Temp to handle multiple files
- Create splitInBatches loop
- Create Download PDF (inside loop)
- Create Convert to Base64 (inside loop)
- Create Claude Vision Extract (inside loop)
- Create Store Result (inside loop)
- Test: Verify loop processes all PDFs and accumulates results

### Sprint 3: Batch Voting (Nodes 8-11)
- Create Aggregate Results node
- Create Find Common Denominator (voting logic)
- Create Finalize Identification node
- Test: Verify voting produces correct winner

### Sprint 4: Registry Matching (Nodes 12-14)
- Update registry sheet with new columns
- Modify Lookup by Project Name
- Create Lookup by Sender Email (secondary)
- Modify Decision Gate with 4 routes
- Test: Verify correct routing for all scenarios

### Sprint 5: Flagging + Routing (Nodes 15-19)
- Create Check Flag Conditions node
- Create Send Review Email (conditional)
- Modify Route to Chunk nodes
- Ensure Mark as Read on all paths
- Test: End-to-end with flagging scenarios

---

## Testing Scenarios

### Scenario 1: Multiple docs, high confidence, existing project
- Input: 3 PDFs all say "Villa Martens", sender known, project in registry
- Expected: No flag, route to Chunk 2.5, no review email

### Scenario 2: Single doc, new sender, low confidence
- Input: 1 PDF unclear identifier, sender not in registry
- Expected: FLAG HIGH, send review email, route to Chunk 0 (Unknowns)

### Scenario 3: Multiple docs, mixed identifiers
- Input: 2 PDFs say "Villa Martens", 1 says "PROPOS GmbH"
- Expected: Vote picks "Villa Martens", medium confidence, possible flag

### Scenario 4: Email body validation
- Input: PDF says "Project X", email body says "Regarding Project X"
- Expected: Higher confidence due to email match, no flag

### Scenario 5: Known sender, new project
- Input: Sender in registry with Project A, sends docs for Project B
- Expected: Route NEW_FROM_KNOWN, create new folders, link to sender

---

## Open Questions

**Before implementation:**
1. ✅ Confirm exact registry sheet ID and current columns
2. ✅ Confirm temp staging folder ID (_Temp_Staging)
3. ✅ Confirm 38_Unknowns folder ID
4. ✅ Confirm Eugene's review email: eugene@ama-capital.de
5. ❓ Should NEW_FROM_KNOWN create separate registry row or nested folder?
6. ❓ What is the Chunk 0 workflow ID?
7. ❓ What is the Chunk 2.5 workflow ID?

**Registry column decision:**
- Option 1: One row per project (same sender appears multiple times)
- Option 2: One row per sender with array/nested projects

**Recommendation:** Option 1 (one row per project) is simpler for Google Sheets filtering.

---

## Success Criteria

**V10 is complete when:**
- ✅ Processes ALL attachments, not just first
- ✅ Voting mechanism selects most likely identifier
- ✅ Email body parsing adds validation
- ✅ Registry tracks sender_email and project_name_normalized
- ✅ Flagging works for all scenarios in matrix
- ✅ Review emails sent for HIGH priority flags
- ✅ Correct routing to Chunk 0 or Chunk 2.5
- ✅ All paths mark email as read
- ✅ Workflow validated and tests pass

---

## Next Steps

1. Review this plan with Sway
2. Get answers to open questions (registry structure, workflow IDs)
3. Begin Sprint 1: Intake + Email Parsing
4. Validate each sprint before moving to next
5. Full end-to-end test before marking complete

---

**Document Version:** 1.0
**Created:** 2026-01-19
**Status:** Ready for implementation (pending answers to open questions)
