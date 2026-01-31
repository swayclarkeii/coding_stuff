# n8n Test Report - Fathom AI Analysis v2 (Multi-Call)

**Workflow ID**: QTmNH1MWW5mGBTdW
**Test Date**: 2026-01-30
**Execution ID**: 7299

---

## Summary

- **Total Tests**: 1
- **Passed**: 0
- **Failed**: 1

---

## Test Details

### Test: Fathom Multi-Call AI Analysis - Sindbad/Ambush TV Discovery Call

**Status**: FAIL

**Test Input**:
```json
{
  "combined_transcript": "Meeting between Sway Clarke from Oloxa and Sindbad Farahmand from Ambush TV / Bold Move Media...",
  "contact_email": "sindbad@boldmove.tv",
  "contact_name": "Sindbad Farahmand",
  "title": "Discovery Call - Ambush TV Admin Automation"
}
```

**Execution Details**:
- Execution ID: 7299
- Status: success (workflow completed)
- Duration: 13.4 seconds
- Nodes executed: 13/13

**What Happened**:

The workflow executed all 13 nodes successfully, but **all 4 AI calls failed to receive the transcript data**. Here's what each AI agent responded with:

1. **AI Call 1 - Discovery**: "I'm sorry for any inconvenience, but a specific meeting transcript is required to proceed."
2. **AI Call 2 - Opportunity**: "I'm sorry, I need the actual text from the meeting transcript to generate the requested JSON object."
3. **AI Call 3 - Technical**: "I'm sorry, I can't generate a valid result without more information from the transcript."
4. **AI Call 4 - Strategic**: "I'm sorry, I need the text of the transcript to proceed with the request."

**Root Cause Analysis**:

Looking at the execution data:

1. **Webhook node** (WORKING): Correctly received the test data in `body.combined_transcript` with the full 1,291-character transcript.

2. **Extract Company node** (WORKING): Successfully extracted company name from email domain and passed through all 4 fields:
   - `combined_transcript` (full text)
   - `contact_email`
   - `contact_name`
   - `title`
   - `company` (extracted as "Boldmove")

3. **AI Call nodes** (FAILING): All 4 OpenAI LangChain nodes are configured with prompts using the expression `{{ $json.combined_transcript }}`, which should pull the transcript from the incoming data. However, the AI agents are receiving empty/null values.

**The Problem**:

The OpenAI LangChain node (type: `@n8n/n8n-nodes-langchain.openAi`) is using the `responses.values[0].content` parameter with an expression like:

```
Analyze this meeting transcript...

Transcript:
{{ $json.combined_transcript }}
```

But the expression `{{ $json.combined_transcript }}` is **not resolving** to the actual transcript text. Instead, the AI is receiving either:
- An empty string
- The literal text "{{ $json.combined_transcript }}"
- Or nothing at all

This is why all 4 AI agents are asking for the transcript to be provided.

**Expected vs Actual**:

| Expected | Actual |
|----------|--------|
| 4 AI calls process transcript | All 4 AI calls receive empty transcript |
| 10 JSON fields populated (summary, key_insights, pain_points, action_items, quick_wins, pricing_strategy, complexity_assessment, requirements, roadmap, client_journey_map) | All fields show error: "No JSON found" |
| Detailed analysis returned | Generic error messages returned |

**Output Structure**:

The final webhook response was:
```json
{
  "error": "No JSON found",
  "raw": "I'm sorry, I need the actual text from the meeting transcript...",
  "company": ""
}
```

Note: The `company` field is also empty, even though "Extract Company" successfully extracted "Boldmove". This suggests the Merge/Combine nodes may also have issues.

---

## Diagnosis

**Confirmed Issues**:

1. **Expression Resolution Failure**: The n8n expression `{{ $json.combined_transcript }}` in the OpenAI LangChain nodes is not resolving to the actual transcript text.

2. **Data Not Flowing to AI Nodes**: Despite Extract Company having the correct data in its output, the 4 AI call nodes are not receiving it.

3. **Company Field Lost**: The company name extracted in "Extract Company" is not making it to the final output.

**Possible Causes**:

1. **OpenAI LangChain node expression syntax**: The `responses.values[0].content` parameter may require different expression syntax (e.g., `$('Extract Company').item.json.combined_transcript` instead of `{{ $json.combined_transcript }}`)

2. **Data type mismatch**: The OpenAI node may be expecting a different data structure

3. **Expression execution timing**: The expression may be evaluating before the data is available

**What's Working**:

- Webhook trigger correctly receives POST data
- Extract Company node correctly processes the input
- All parsing nodes execute (even though they get error responses)
- Merge and Combine nodes execute
- Webhook response is sent

**What's NOT Working**:

- Transcript data not reaching any of the 4 AI nodes
- All 10 expected JSON fields are empty/error
- Company field not in final output

---

## Next Steps

**To Fix**:

1. **Check OpenAI LangChain node expression syntax** - Verify the correct way to reference input data in the `content` parameter
2. **Test with simpler expression** - Try using `$json.combined_transcript` without the curly braces
3. **Check node input/output mapping** - Verify Extract Company output is properly connected to AI nodes
4. **Add debug logging** - Insert Code nodes before AI calls to log what data they're receiving
5. **Review n8n documentation** - Check if OpenAI LangChain v2.1 has specific expression requirements

**Recommended Approach**:

Use `solution-builder-agent` to:
1. Examine the OpenAI LangChain node expression syntax
2. Fix the data flow from Extract Company → AI Calls
3. Fix the Combine Output node to preserve the company field
4. Re-test with same payload

---

## Test Environment

- **n8n Instance**: n8n.oloxa.ai
- **Workflow Version**: v27
- **OpenAI Model**: gpt-4o
- **Test Method**: n8n_test_workflow via webhook trigger
