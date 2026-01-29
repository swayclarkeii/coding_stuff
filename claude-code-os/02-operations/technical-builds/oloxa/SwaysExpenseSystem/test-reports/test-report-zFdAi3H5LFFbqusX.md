# n8n Test Report - Expensify PDF Processor (zFdAi3H5LFFbqusX)

## Summary
- Total tests: 1
- Failed: 1
- Status: **FAILED - Configuration Error**

---

## Execution Details

### Test: Process November 2025 Expense Report
- **Status**: FAILED
- **Execution ID**: 6401
- **Started**: 2026-01-28T13:43:34.630Z
- **Stopped**: 2026-01-28T13:43:36.621Z
- **Duration**: 1.99 seconds
- **Final Status**: error

---

## Error Analysis

**Primary Error Node**: Extract Table with Claude API (call-claude-api)
**Error Type**: NodeApiError (HTTP 400)
**Error Message**: "Bad request - please check your parameters"

**Root Cause**: Claude API error - "model: Field required"

**API Response**:
```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "model: Field required"
  },
  "request_id": "req_011CXZshZjQx3TPtDqcUrTxG"
}
```

---

## Execution Path (3 nodes executed)

1. **Webhook Trigger** - SUCCESS (0ms)
   - Received test payload correctly
   - drive_file_id: 1VLswjWt7hvd3kLVJ7CDm6o-FGYpwB9PX
   - report_month: November 2025

2. **Download PDF from Drive** - SUCCESS (1,678ms)
   - Downloaded PDF successfully
   - Filename: SwayClarkeNOV2025ExpenseReport[37638].pdf
   - Size: 1.03 MB
   - Binary data stored correctly in filesystem-v2

3. **Extract Table with Claude API** - FAILED (305ms)
   - HTTP Request node to api.anthropic.com/v1/messages
   - Authentication: Using credential "Anthropic account" (ID: MRSNO4UW3OEIA3tQ)
   - Headers: anthropic-version: 2023-06-01
   - **Problem**: Body parameters are EMPTY
     - name: "" (empty string)
     - value: "" (empty string)

---

## Problem Diagnosis

**Issue**: The HTTP Request node "Extract Table with Claude API" has incorrect body parameter configuration.

**Current Configuration**:
```json
"bodyParameters": {
  "parameters": [
    {
      "name": "",
      "value": ""
    }
  ]
}
```

**Expected Configuration for Claude API**:
The body should contain:
- `model`: The Claude model to use (e.g., "claude-3-5-sonnet-20241022")
- `messages`: Array of message objects with the prompt
- `max_tokens`: Maximum tokens in response
- Additional parameters for vision/PDF processing

**Why it's failing**:
- The bodyParameters has empty name/value pairs
- Claude API requires at minimum: `model`, `messages`, `max_tokens`
- The API correctly rejects the request because required field "model" is missing

---

## Upstream Context (What worked)

The PDF download worked perfectly:
- Binary data is accessible at `$binary.data`
- File size: 1.03 MB
- File type: PDF
- Stored in n8n's filesystem-v2 storage

---

## Next Steps

**solution-builder-agent needs to fix the HTTP Request node body**:

1. Switch from `keypair` parameters to `json` body specification
2. Build proper Claude API request with:
   - Model specification (claude-3-5-sonnet-20241022 or similar)
   - Messages array with vision content for PDF
   - Max tokens setting
   - System prompt for table extraction

**Example body structure needed**:
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 4096,
  "messages": [{
    "role": "user",
    "content": [
      {
        "type": "document",
        "source": {
          "type": "base64",
          "media_type": "application/pdf",
          "data": "{{ $binary.data }}"
        }
      },
      {
        "type": "text",
        "text": "Extract expense table from this PDF..."
      }
    ]
  }]
}
```

---

## Test Payload Used
```json
{
  "drive_file_id": "1VLswjWt7hvd3kLVJ7CDm6o-FGYpwB9PX",
  "report_month": "November 2025"
}
```

---

## Verdict

**CONFIGURATION ERROR - Not a timeout issue**

The workflow is not stuck or long-running. It fails immediately (2 seconds) because the HTTP Request node has empty body parameters when it should have a complete Claude API request payload.

Previous validation passed because n8n doesn't validate HTTP Request body content - it only checks that the node configuration structure is valid. The actual API call reveals the missing parameters.
