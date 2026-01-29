# Test Report - Expense System W6: Extract from File Node Test

**Date:** 2026-01-28
**Workflow:** zFdAi3H5LFFbqusX (Expense System - W6 v2: Expensify Table Extractor SIMPLE)
**Execution ID:** 6437
**Status:** ❌ FAILED

---

## Test Summary

**Test Input:**
```json
{
  "drive_file_id": "1VLswjWt7hvd3kLVJ7CDm6o-FGYpwB9PX",
  "report_month": "November 2025"
}
```

**Expected:** Extract from File node converts filesystem-v2 binary to base64 in `$json.pdfBase64`

**Actual:** Extract from File node was **NEVER EXECUTED**

---

## Critical Finding: Connection Bug

### What Actually Happened

1. ✅ **Webhook Trigger** → Success
2. ✅ **Download PDF from Drive** → Success (binary data with `"data": "filesystem-v2"`)
3. ❌ **Convert PDF to Base64 (Extract from File)** → **NOT EXECUTED**
4. ✅ **Build Claude Request** → Success (disabled but still in execution path)
5. ❌ **Extract Table with Claude API** → FAILED - `$json.pdfBase64` does not exist

### The Connection Problem

The workflow has TWO parallel branches from "Download PDF from Drive":
- Branch 1: → Build Claude Request → Extract Table with Claude API
- Branch 2: → Convert PDF to Base64 → Extract Table with Claude API

**However, the execution shows only Branch 1 executed.** The HTTP Request node is trying to reference `$json.pdfBase64` from the "Convert PDF to Base64" node, but that node never ran.

### Execution Flow

```
Webhook Trigger
     ↓
Download PDF from Drive (binary: filesystem-v2)
     ↓
     ├──→ Build Claude Request ──→ Extract Table with Claude API ← RUNS (gets undefined $json.pdfBase64)
     │
     └──→ Convert PDF to Base64 ← NEVER EXECUTED
```

---

## Error Details

**Failed Node:** Extract Table with Claude API (HTTP Request)
**Error Message:**
```
400 - Bad request - please check your parameters
messages.0.content.1.document.source.base64.data: Field required
```

**Request Body Sent:**
```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 16000,
  "messages": [{
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "Extract the expense table from page 1..."
      },
      {
        "type": "document",
        "source": {
          "type": "base64",
          "media_type": "application/pdf"
          // data field is MISSING - because $json.pdfBase64 is undefined
        }
      }
    ]
  }]
}
```

---

## Root Cause

**The "Extract from File" node was added to the workflow but NOT connected in the execution path.**

Looking at the workflow's `nodeExecutionStack`, the HTTP Request node has this in its source:
```json
"source": {
  "main": [
    {
      "previousNode": "Build Claude Request"
    }
  ]
}
```

It should be:
```json
"source": {
  "main": [
    {
      "previousNode": "Convert PDF to Base64"
    }
  ]
}
```

---

## Conclusion

**Extract from File was never tested** because it was never executed. The workflow connections are incorrect.

### What We Know:
- ✅ Extract from File node EXISTS in the workflow
- ❌ Extract from File node is NOT connected in the execution path
- ❌ HTTP Request is reading from the wrong source node

### What We DON'T Know:
- Can "Extract from File" actually read filesystem-v2 binary data?
- This test did not answer the original question

---

## Next Steps

**Fix Required:** solution-builder-agent needs to correct the workflow connections:

1. **Remove connection:** Download PDF from Drive → Build Claude Request
2. **Keep connection:** Download PDF from Drive → Convert PDF to Base64
3. **Fix connection:** Convert PDF to Base64 → Extract Table with Claude API (NOT Build Claude Request → Extract Table with Claude API)

OR: If "Build Claude Request" is meant to stay in the flow, the connections should be:
```
Download PDF → Convert PDF to Base64 → Build Claude Request → HTTP Request
```

Once connections are fixed, re-run this test to see if Extract from File can actually handle filesystem-v2.

---

## Execution Timeline

- **Started:** 2026-01-28T14:38:18.288Z
- **Stopped:** 2026-01-28T14:38:20.988Z
- **Duration:** 2.7 seconds
- **Last Node Executed:** Extract Table with Claude API

### Node Execution Times:
- Webhook Trigger: 0ms
- Download PDF from Drive: 2,417ms (binary download successful)
- Build Claude Request: 0ms
- Extract Table with Claude API: 277ms (failed with 400 error)
- **Convert PDF to Base64: NOT EXECUTED**
