# Fathom AI Analysis v2 - Fix Complete

**Date**: 2026-01-30
**Workflow ID**: QTmNH1MWW5mGBTdW
**Status**: Fixed, ready for activation and testing

---

## Issues Fixed

### Issue 1: Empty Transcript in AI Calls ✅

**Problem**: The 4 LangChain OpenAI Chat Model nodes received empty transcripts because the expression `{{ $json.combined_transcript }}` wasn't resolving properly in LangChain nodes.

**Root Cause**: LangChain OpenAI nodes (`@n8n/n8n-nodes-langchain.openAi`) have different expression resolution behavior than standard n8n nodes.

**Solution**:
- **Removed** 4 LangChain OpenAI nodes
- **Added** 4 "Build Prompt" Code nodes that construct full prompts with transcript embedded in JavaScript
- **Added** 4 HTTP Request nodes calling OpenAI API directly at `https://api.openai.com/v1/chat/completions`
- **Updated** 4 Parse nodes to extract response from `choices[0].message.content` (OpenAI API format)

**New Architecture**:
```
Extract Company → Build Prompt 1 → HTTP OpenAI 1 → Parse Discovery → Merge
                → Build Prompt 2 → HTTP OpenAI 2 → Parse Opportunity → Merge
                → Build Prompt 3 → HTTP OpenAI 3 → Parse Technical → Merge
                → Build Prompt 4 → HTTP OpenAI 4 → Parse Strategic → Merge
```

### Issue 2: Company Field Lost ✅

**Problem**: The "Combine Output" Code node tried to get company from `items[0]?.json?.company` but after the Merge node, the company field wasn't in any parsed AI response.

**Root Cause**: Company field only exists in the Extract Company node output, not in the AI responses that flow through the Merge node.

**Solution**: Changed Combine Output code to reference Extract Company node directly using `$('Extract Company')`:

```javascript
// Get company fields from Extract Company node directly
const extractCompany = $('Extract Company').first().json;
combined.company = extractCompany?.company || '';
combined.contact_email = extractCompany?.contact_email || '';
combined.contact_name = extractCompany?.contact_name || '';
combined.title = extractCompany?.title || '';
```

---

## Workflow Structure (After Fix)

**Total Nodes**: 17
**Total Connections**: 16

### Flow

1. **Webhook** (trigger)
   - Path: `fathom-ai-analysis-v2`
   - Method: POST
   - Receives: `combined_transcript`, `contact_email`, `contact_name`, `title`

2. **Extract Company** (Code)
   - Extracts company name from email domain
   - Passes all fields forward

3. **4x Build Prompt Nodes** (Code) - *NEW*
   - Build Prompt 1 - Discovery
   - Build Prompt 2 - Opportunity
   - Build Prompt 3 - Technical
   - Build Prompt 4 - Strategic
   - Each constructs full prompt with transcript embedded

4. **4x HTTP OpenAI Nodes** (HTTP Request) - *NEW*
   - HTTP OpenAI 1 - Discovery
   - HTTP OpenAI 2 - Opportunity
   - HTTP OpenAI 3 - Technical
   - HTTP OpenAI 4 - Strategic
   - Model: `gpt-4o`
   - Credentials: OpenAi account (xmJ7t6kaKgMwA1ce)

5. **4x Parse Nodes** (Code) - *UPDATED*
   - Parse Discovery
   - Parse Opportunity
   - Parse Technical
   - Parse Strategic
   - Extract from `choices[0].message.content` (OpenAI API format)

6. **Merge All Results**
   - Combines 4 parse outputs (inputs 0-3)

7. **Combine Output** (Code) - *UPDATED*
   - Merges all AI analysis fields
   - References Extract Company directly for metadata

8. **Respond to Webhook**
   - Returns combined result

---

## Key Changes Summary

| Node | Change Type | Details |
|------|-------------|---------|
| AI Call 1-4 | **REMOVED** | LangChain OpenAI nodes removed |
| Build Prompt 1-4 | **ADDED** | Code nodes construct prompts with transcript |
| HTTP OpenAI 1-4 | **ADDED** | Direct OpenAI API calls via HTTP Request |
| Parse 1-4 | **UPDATED** | Extract from OpenAI API response format |
| Combine Output | **UPDATED** | Reference Extract Company node directly |

---

## Next Steps

### 1. Activate Workflow ⚠️

**CRITICAL**: The workflow is currently **inactive** and needs to be activated in the n8n UI.

**To activate**:
1. Go to https://n8n.oloxa.ai/workflow/QTmNH1MWW5mGBTdW
2. Click the "Active" toggle in the top right
3. Wait for confirmation

### 2. Test Workflow

**Test Command**:
```bash
curl -X POST "https://n8n.oloxa.ai/webhook/fathom-ai-analysis-v2" \
  -H "Content-Type: application/json" \
  -d '{
    "combined_transcript": "Meeting between Sway and Marcus from Boldmove. Discussion about automation needs. Marcus mentioned they spend 20 hours per week on manual data entry. They need a CRM integration with their existing tools. Budget is around 5000 euros per month. Timeline is Q2 2026. Key pain point is duplicate data across 3 systems.",
    "contact_email": "marcus@boldmove.tv",
    "contact_name": "Marcus Schmidt",
    "title": "Discovery Call - Boldmove"
  }'
```

**Expected Response**: JSON object with all 10 analysis fields + company metadata:
- `summary`
- `key_insights`
- `pain_points`
- `action_items`
- `quick_wins`
- `pricing_strategy`
- `complexity_assessment`
- `requirements`
- `roadmap`
- `client_journey_map`
- `company` (= "Boldmove")
- `contact_email`
- `contact_name`
- `title`

### 3. Iterate if Needed

If test fails:
- Check execution logs in n8n UI
- Verify which node failed
- Check if transcript is reaching AI calls
- Verify OpenAI credentials are valid
- Document error and implement fix

---

## Technical Details

### Build Prompt Code Structure

Each Build Prompt node uses this pattern:

```javascript
const transcript = $input.first().json.combined_transcript || '';
const prompt = `[FULL PROMPT TEXT]

Transcript:
${transcript}`;

return [{ json: { prompt, combined_transcript: transcript } }];
```

This ensures the transcript is embedded directly in the string, avoiding expression resolution issues.

### HTTP Request Configuration

Each HTTP OpenAI node is configured:

```javascript
{
  method: "POST",
  url: "https://api.openai.com/v1/chat/completions",
  authentication: "predefinedCredentialType",
  nodeCredentialType: "openAiApi",
  jsonBody: "={{ JSON.stringify({
    model: 'gpt-4o',
    messages: [
      { role: 'user', content: $json.prompt }
    ],
    temperature: 0.7
  }) }}"
}
```

### Parse Response Code Structure

Each Parse node extracts the response:

```javascript
const item = $input.first().json;
let raw = '';

// OpenAI API format
if (item.choices && item.choices[0] && item.choices[0].message && item.choices[0].message.content) {
  raw = item.choices[0].message.content;
} else if (typeof item.text === 'string') {
  raw = item.text;
} else {
  raw = JSON.stringify(item);
}

// Clean and parse JSON
let text = raw;
text = text.replace(/```json\s*/gi, '').replace(/```\s*/gi, '');
const start = text.indexOf('{');
const end = text.lastIndexOf('}');
if (start === -1 || end === -1) {
  return [{ json: { error: 'No JSON found', raw: text.substring(0, 200) } }];
}
text = text.substring(start, end + 1);
text = text.replace(/,\s*([\]}])/g, '$1');

try {
  return [{ json: JSON.parse(text) }];
} catch(e) {
  return [{ json: { error: e.message, raw: text.substring(0, 200) } }];
}
```

---

## Validation

Workflow validated successfully:
- ✅ Total nodes: 17
- ✅ Enabled nodes: 17
- ✅ Valid connections: 16
- ✅ Invalid connections: 0
- ✅ Error count: 0

**Warnings** (non-critical):
- Outdated typeVersion on HTTP Request nodes (4.2 vs 4.4) - does not affect functionality
- Missing error handling - can be added later if needed

---

## Credentials Used

- **OpenAI API**
  - Credential ID: `xmJ7t6kaKgMwA1ce`
  - Name: "OpenAi account"
  - Type: `openAiApi`

---

## Files Modified

- Workflow: `Fathom AI Analysis v2 - Multi-Call` (QTmNH1MWW5mGBTdW)
- Documentation: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/oloxa/fathom-workflow/FATHOM_AI_V2_FIX_COMPLETE.md`
