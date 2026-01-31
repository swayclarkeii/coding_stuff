# n8n Test Report - Fathom AI Analysis v2 - Multi-Call

## Summary
- Total tests: 1 (manual trigger attempted + execution analysis)
- Status: BLOCKED - Workflow cannot be triggered via API (inactive)
- Root Cause: **Data extraction bug** in Extract Company node

---

## Test Details

### Workflow Information
- **Workflow ID**: QTmNH1MWW5mGBTdW
- **Workflow Name**: Fathom AI Analysis v2 - Multi-Call
- **Active Status**: Inactive (cannot be activated due to n8n telemetry error)
- **Last Successful Execution**: Execution 7299 on 2026-01-30 at 22:37:46

### Test Attempted
- **Test Type**: Webhook trigger via n8n_test_workflow
- **Test Data**:
  ```json
  {
    "combined_transcript": "Meeting between Sway and Marcus from Boldmove...",
    "contact_email": "marcus@boldmove.tv",
    "contact_name": "Marcus Schmidt",
    "title": "Discovery Call - Boldmove"
  }
  ```
- **Result**: BLOCKED - Cannot trigger inactive workflow via API

---

## Analysis of Recent Execution (7299)

### Execution Flow
Workflow executed 13 of 17 nodes successfully:
1. Webhook (success)
2. Extract Company (success - but with bug)
3. Build Prompt 1-4 (all executed in parallel)
4. HTTP OpenAI 1-4 (all executed in parallel)
5. Parse Discovery/Opportunity/Technical/Strategic (all executed)
6. Merge All Results (success)
7. Combine Output (success)
8. Respond to Webhook (success)

**Duration**: 13.4 seconds

### Critical Bug Identified

**Location**: "Extract Company" node (id: extract-company)

**Issue**: The node is reading from the wrong data path.

**Current code** reads from:
```javascript
$input.first().json.contact_email
$input.first().json.combined_transcript
// etc.
```

**But webhook data structure is**:
```json
{
  "headers": {...},
  "params": {},
  "query": {},
  "body": {
    "combined_transcript": "...",
    "contact_email": "...",
    "contact_name": "...",
    "title": "..."
  }
}
```

**Should read from**:
```javascript
$input.first().json.body.contact_email
$input.first().json.body.combined_transcript
// etc.
```

### Impact

Because Extract Company cannot read the webhook body correctly:

1. **Extract Company output** was:
   ```json
   { "company": "" }
   ```

   Instead of:
   ```json
   {
     "combined_transcript": "Meeting text...",
     "contact_email": "sindbad@boldmove.tv",
     "contact_name": "Sindbad Farahmand",
     "title": "Discovery Call - Ambush TV Admin Automation",
     "company": "Boldmove"
   }
   ```

2. **All 4 Build Prompt nodes** received incomplete data (missing `combined_transcript`)

3. **All 4 AI API calls** failed with "I need the transcript text" errors

4. **Final output** returned error response:
   ```json
   {
     "error": "No JSON found",
     "raw": "I'm sorry, I need the actual text...",
     "company": ""
   }
   ```

### Evidence from Execution 7299

**Extract Company node output**:
```json
{
  "company": ""
}
```

**AI Call responses** (all 4 identical pattern):
- "I'm sorry, I need the actual text from the meeting transcript to generate the requested JSON object."

**Parse node outputs** (all 4):
```json
{
  "error": "No JSON found",
  "raw": "I'm sorry, I need the actual text from the meeting transcript..."
}
```

---

## Required Fix

### Extract Company Node

Replace current code:
```javascript
const personalDomains = ['gmail.com', 'yahoo.com', 'hotmail.com', ...];

const email = $input.first().json.contact_email || '';
const domain = email.split('@')[1] || '';

let company = '';
if (domain && !personalDomains.includes(domain.toLowerCase())) {
  const companyName = domain.split('.')[0];
  company = companyName.charAt(0).toUpperCase() + companyName.slice(1);
}

return [{
  json: {
    combined_transcript: $input.first().json.combined_transcript,
    contact_email: $input.first().json.contact_email,
    contact_name: $input.first().json.contact_name,
    title: $input.first().json.title,
    company: company
  }
}];
```

With fixed code:
```javascript
const personalDomains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'aol.com', 'proton.me', 'protonmail.com', 'gmx.com', 'gmx.de', 'web.de', 't-online.de', 'freenet.de', 'posteo.de', 'live.com', 'msn.com', 'me.com', 'mac.com'];

// FIX: Read from .body instead of root
const email = $input.first().json.body.contact_email || '';
const domain = email.split('@')[1] || '';

let company = '';
if (domain && !personalDomains.includes(domain.toLowerCase())) {
  const companyName = domain.split('.')[0];
  company = companyName.charAt(0).toUpperCase() + companyName.slice(1);
}

return [{
  json: {
    combined_transcript: $input.first().json.body.combined_transcript,
    contact_email: $input.first().json.body.contact_email,
    contact_name: $input.first().json.body.contact_name,
    title: $input.first().json.body.title,
    company: company
  }
}];
```

**Key change**: Add `.body` to all `$input.first().json.X` references.

---

## Secondary Issue: Workflow Activation Error

The workflow cannot be activated due to a known n8n telemetry error:
- Error: "Could not find property option"
- Location: n8n telemetry system (`getNodeParameters()` function)
- Impact: Prevents workflow activation, but workflow CAN execute when triggered manually in n8n UI
- Status: Server-wide issue documented in `/server-diagnostics/2026-01-30-workflow-activation-error.md`

This is a separate issue from the data extraction bug.

---

## Next Steps

1. **Fix Extract Company node** - Update code to read from `.body` path
2. **Test via n8n UI** - Manual test trigger (workflow doesn't need to be active for manual tests)
3. **Verify AI responses** - Check that all 10 analysis fields are populated
4. **Address activation error** (optional) - Investigate telemetry error if API triggering is required

---

## Test Status: FAIL

**Reason**: Data extraction bug prevents workflow from functioning correctly.

**Expected fields in response**:
- summary
- key_insights
- pain_points
- action_items
- quick_wins
- pricing_strategy
- complexity_assessment
- requirements
- roadmap
- client_journey_map
- company (metadata field)

**Actual fields in response** (execution 7299):
- error: "No JSON found"
- raw: "I'm sorry, I need the actual text..."
- company: ""

**Pass criteria**: All 10 AI analysis fields + company populated with valid data

**Actual result**: 0 of 10 fields populated, error responses from all AI calls

---

**Report Generated**: 2026-01-30T23:00:00Z
**Execution Analyzed**: 7299 (2026-01-30 22:37:46)
**Agent**: test-runner-agent
