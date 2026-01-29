# n8n Test Report - SOP Builder Lead Magnet

**Workflow ID:** ikVyMpDI0az6Zk4t
**Test Date:** 2026-01-28
**Execution ID:** 6501 (primary), 6502 (error trigger)

## Summary
- Total tests: 1
- ✅ Passed: 0
- ❌ Failed: 1

---

## Test 1: Detailed SOP (≥75% score expected)

### Status: ❌ FAIL

**Execution Details:**
- **Execution ID:** 6501
- **Final Status:** error
- **Duration:** 548ms
- **Last Node Executed:** LLM: Validate Completeness
- **Failed at Node:** LLM: Validate Completeness

### Error Information

**Error Type:** NodeApiError
**HTTP Status:** 400
**Error Message:** `you must provide a model parameter`

**OpenAI Response:**
```json
{
  "error": {
    "message": "you must provide a model parameter",
    "type": "invalid_request_error",
    "param": null,
    "code": null
  }
}
```

### Root Cause

The HTTP Request node "LLM: Validate Completeness" is configured with **empty body parameters**:

```json
{
  "bodyParameters": {
    "parameters": [
      {
        "name": "",
        "value": ""
      }
    ]
  }
}
```

The node is making a POST request to `https://api.openai.com/v1/chat/completions` but sending no request body. OpenAI requires at minimum:
- `model` (e.g., "gpt-4", "gpt-3.5-turbo")
- `messages` (array of conversation messages)

### Execution Path

The workflow executed these nodes before failing:

1. ✅ **Webhook Trigger** (0ms) - Successfully received test data
2. ✅ **Parse Form Data** (27ms) - Parsed input fields correctly
3. ✅ **Check Audio File** (2ms) - No audio file provided (expected)
4. ⏭️ **Upload Audio to Drive** - Skipped (no audio)
5. ⏭️ **Transcribe with Whisper** - Skipped (no audio)
6. ⏭️ **Set Transcription as Steps** - Skipped (no audio)
7. ✅ **Merge Audio and Text Paths** (3ms) - Successfully merged data
8. ❌ **LLM: Validate Completeness** (484ms) - **FAILED HERE**

### Upstream Data

The node received the following data from "Merge Audio and Text Paths":

```json
{
  "email": "sway@oloxa.ai",
  "name": "Sway Clarke",
  "goal": "Customer Order Fulfillment",
  "improvement_type": "process_improvement",
  "department": "general",
  "process_steps": "[detailed SOP text]",
  "has_audio": false,
  "audio_data": null
}
```

This data is correct and ready to be sent to the LLM.

### What Needs to Be Fixed

The "LLM: Validate Completeness" HTTP Request node needs to have its body configured with:

1. **Model parameter** - e.g., `gpt-4` or `gpt-3.5-turbo`
2. **Messages array** - containing the system prompt and user content
3. **Proper JSON structure** - following OpenAI's chat completions API format

Expected body structure:
```json
{
  "model": "gpt-4",
  "messages": [
    {
      "role": "system",
      "content": "[system prompt for validation]"
    },
    {
      "role": "user",
      "content": "{{ $json.process_steps }}"
    }
  ],
  "temperature": 0.7
}
```

### Verification Checklist

None of the verification steps could be completed due to the LLM node failure:

- ❌ Workflow executes without errors
- ❌ OpenAI responds (LLM nodes work)
- ❌ Score is calculated
- ❌ Email is sent to sway@oloxa.ai
- ❌ Lead logged in Airtable
- ❌ Email uses oloxa.ai branding

### Notes

- This is the same node type error that was previously reported as "fixed"
- The HTTP Request node configuration shows it was likely not saved properly or was overwritten
- This is a critical blocker - the workflow cannot proceed past this point
- The Error Trigger node (execution 6502) successfully caught the error and would trigger error handling logic

### Recommended Next Steps

1. Fix the "LLM: Validate Completeness" node body parameters
2. Apply the same fix to all other LLM HTTP Request nodes in the workflow
3. Re-test with the same input data
4. Verify all downstream nodes (scoring, email, Airtable) work correctly
