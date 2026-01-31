# n8n Test Report - Fathom AI Analysis v2 - Multi-Call

## Summary
- Total tests: 1
- Passed: 0
- Failed: 1

---

## Test Details

### Test: Discovery Call - Ambush TV Admin Automation
**Status**: FAIL

**Execution ID**: 7298
**Final status**: error
**Duration**: 2,932ms
**Stopped at**: Parse Discovery node

---

## Error Analysis

### Primary Error
```
TypeError: text.replace is not a function [line 4]
```

**Failed Node**: Parse Discovery
**Node Type**: n8n-nodes-base.code

### Root Cause Analysis

**Issue 1: Output Structure Mismatch**

The OpenAI LangChain node (`@n8n/n8n-nodes-langchain.openAi`) returns data in this structure:
```json
{
  "output": [
    {
      "id": "msg_...",
      "type": "message",
      "status": "completed",
      "content": [
        {
          "type": "output_text",
          "text": "..."
        }
      ],
      "role": "assistant"
    }
  ]
}
```

The Parse nodes are attempting to access:
```javascript
const raw = $input.first().json.text || $input.first().json.output || JSON.stringify($input.first().json);
```

This tries `json.text` first (doesn't exist), then `json.output` (which is an array, not text), then stringifies the whole object.

When `text.replace()` is called on the array, it fails because arrays don't have a `.replace()` method.

**Issue 2: AI Didn't Receive Transcript**

The AI Call 1 response was:
```
"I'm sorry, I can't analyze the meeting transcript without having the transcript text itself. Can you provide the text for analysis?"
```

This indicates the expression `{{ $json.combined_transcript }}` in the AI prompt is not being properly evaluated or the data isn't being passed through correctly.

---

## Execution Path

1. **Webhook** - SUCCESS (2ms, 1 item)
2. **Extract Company** - SUCCESS (14ms, 1 item)
3. **AI Call 1 - Discovery** - SUCCESS (2,790ms, 1 item) - But AI said it didn't receive transcript
4. **Parse Discovery** - ERROR (21ms, 0 items)

---

## Required Fixes

### Fix 1: Update Parse Node Code

All 4 Parse nodes need to correctly extract text from LangChain OpenAI output:

```javascript
// Get the raw output from LangChain OpenAI node
let text = '';

// Try different possible structures
if ($input.first().json.output && Array.isArray($input.first().json.output)) {
  // LangChain structure: output[0].content[0].text
  const output = $input.first().json.output[0];
  if (output && output.content && Array.isArray(output.content)) {
    text = output.content[0].text || '';
  }
} else if ($input.first().json.text) {
  // Direct text property
  text = $input.first().json.text;
} else {
  // Fallback: stringify the whole object
  text = JSON.stringify($input.first().json);
}

// Strip markdown fences
text = text.replace(/```json\s*/gi, '').replace(/```\s*/gi, '');

// Find JSON object
const start = text.indexOf('{');
const end = text.lastIndexOf('}');
if (start === -1 || end === -1) {
  return [{ json: { error: 'No JSON found', rawPreview: text.substring(0, 200) } }];
}

text = text.substring(start, end + 1);

// Fix trailing commas
text = text.replace(/,\s*([\]}])/g, '$1');

try {
  return [{ json: JSON.parse(text) }];
} catch(e) {
  return [{ json: { error: e.message, raw: text.substring(0, 200) } }];
}
```

### Fix 2: Verify Prompt Expression Syntax

Check if the AI nodes are using the correct expression syntax. In n8n LangChain nodes, expressions might need different syntax than standard nodes.

**Current prompt format**:
```
Transcript:
{{ $json.combined_transcript }}
```

**May need to be**:
```
Transcript:
{{ $('Extract Company').item.json.combined_transcript }}
```

Or use the visual expression editor to ensure proper data reference.

### Fix 3: Add Validation Node

Consider adding a validation node after "Extract Company" to verify:
- combined_transcript field exists
- combined_transcript is not empty
- combined_transcript is a string

This would catch data issues before expensive AI calls.

---

## Next Steps

1. Update all 4 Parse nodes with the corrected code
2. Verify the AI prompt expressions are correctly referencing the input data
3. Test with the same payload again
4. Verify all 4 AI calls execute successfully
5. Verify the Merge and Combine nodes receive all 4 parsed outputs
6. Verify the final output contains all 10 expected fields + company field

---

## Test Input Used

```json
{
  "combined_transcript": "Meeting between Sway Clarke from Oloxa and Sindbad Farahmand from Ambush TV / Bold Move Media. Discussion about freelancer payment management, rate synchronization across Google Sheets, and invoice validation. Sindbad mentioned spending 5-6 hours weekly on invoice review. They have 150,000 euros outstanding from clients, with 100,000 overdue more than 30 days. Admin team member Leonor handles rate updates across 3 Google Sheets. Key pain points include manual rate syncing, delayed invoicing, and error-prone payment reconciliation. Sindbad hourly rate is 50 euros. Admin team rate is 20 euros per hour. They discussed automating the rate synchronization as a quick win, estimated at 1-2 weeks implementation. The invoice validation system would be a larger project at 6-8 weeks. Sindbad expressed interest in a phased approach starting with quick wins. Budget range discussed was 2-3K initially for quick wins, with openness to more for the full admin chain automation. Bold Move TV is a separate entity handling media production, currently at 10 percent of revenue. Ambush TV is the main production company at 90 percent of revenue.",
  "contact_email": "sindbad@boldmove.tv",
  "contact_name": "Sindbad Farahmand",
  "title": "Discovery Call - Ambush TV Admin Automation"
}
```

---

## Workflow Details

- **Workflow ID**: QTmNH1MWW5mGBTdW
- **Workflow Name**: Fathom AI Analysis v2 - Multi-Call
- **Status**: Active
- **Trigger Type**: Webhook (POST /fathom-ai-analysis-v2)
- **Total Nodes**: 13
- **Credentials**: OpenAI API configured (xmJ7t6kaKgMwA1ce)

---

## Recommendation

This workflow cannot pass testing until the Parse nodes are fixed to handle the LangChain OpenAI output structure. The solution-builder-agent should be engaged to apply the fixes, as this requires modifying 4 nodes with the corrected parsing code.
