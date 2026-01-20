# Chunk 2.5 GPT-4 Classification Fix

## Issue Identified

The "Classify Document with GPT-4" node was returning `"Hello! How can I assist you today?"` instead of classification results.

### Root Cause

The node was configured as a **LangChain Chat Model** (`@n8n/n8n-nodes-langchain.openAi`) instead of a direct OpenAI API caller.

**Problem with LangChain Chat Model node:**
- Designed to be used as a sub-node within AI Chains or AI Agents
- Does NOT accept direct prompt input from previous nodes
- Had NO prompt configured in parameters
- Returns default OpenAI greeting when called without proper LangChain context
- The `classificationPrompt` from "Build AI Classification Prompt" node was never received

## Solution Applied

**Replaced the LangChain node with HTTP Request node** that calls OpenAI API directly.

### Changes Made

1. **Removed:** `@n8n/n8n-nodes-langchain.openAi` (LangChain Chat Model)
2. **Added:** `n8n-nodes-base.httpRequest` (HTTP Request node)

### New Node Configuration

**Node:** "Classify Document with GPT-4" (HTTP Request)
- **Method:** POST
- **URL:** `https://api.openai.com/v1/chat/completions`
- **Authentication:** OpenAI API credentials (existing)
- **Body (JSON):**
```json
{
  "model": "gpt-4",
  "messages": [
    {
      "role": "system",
      "content": "You are a document classifier. Respond ONLY with valid JSON."
    },
    {
      "role": "user",
      "content": "={{ $json.classificationPrompt }}"
    }
  ],
  "temperature": 0.3,
  "response_format": { "type": "json_object" }
}
```

**Key improvements:**
- ✅ Now receives `classificationPrompt` from previous node via `$json.classificationPrompt`
- ✅ Uses GPT-4 model with JSON response format for structured output
- ✅ Lower temperature (0.3) for more deterministic classification
- ✅ System message ensures JSON-only responses

3. **Updated:** "Parse Classification Result" node to handle OpenAI API response format

The parser already had the correct code to extract from `aiResponse.choices[0].message.content`, so no changes were needed there.

## Expected Behavior Now

1. **Build AI Classification Prompt** → Creates prompt with document content
2. **Classify Document with GPT-4** → Receives prompt and sends to OpenAI API
3. **Parse Classification Result** → Extracts JSON classification from API response
4. **Result:** Proper document type classification (Exposé, Grundbuch, Calculation, Exit_Strategy, Other)

## Testing Status

**Ready for testing.** The workflow should now:
- Send the full classification prompt to GPT-4
- Receive structured JSON response with `documentType`, `confidence`, and `reasoning`
- Parse the response correctly
- Continue with document routing based on classification

## Validation Results

- ✅ Node connections: Valid
- ✅ HTTP Request configured correctly
- ✅ Parser handles OpenAI API response format
- ⚠️ Minor warnings about error handling (non-critical)

---

**Workflow ID:** `okg8wTqLtPUwjQ18`
**Fixed:** 2026-01-11
**Agent:** solution-builder-agent
