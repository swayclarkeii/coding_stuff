# Test Report: Workflow W6 v2 - Move Binary Data Node Test

**Date:** 2026-01-28
**Workflow ID:** zFdAi3H5LFFbqusX
**Workflow Name:** Expense System - W6 v2: Expensify Table Extractor (SIMPLE)
**Test Agent ID:** ac0aaae (solution-builder-agent)
**Execution ID:** 6406

---

## Summary

- **Total tests:** 1
- **Passed:** 0
- **Failed:** 1
- **Status:** ❌ **FAILED**

---

## Test: Extract expense table with Move Binary Data node

**Input:**
```json
{
  "drive_file_id": "1VLswjWt7hvd3kLVJ7CDm6o-FGYpwB9PX",
  "report_month": "November 2025"
}
```

**Expected:** Move Binary Data node converts filesystem-v2 binary to base64, allowing HTTP Request node to send PDF to Anthropic API.

**Result:** ❌ **FAIL**

**Execution status:** ERROR

**Failed at node:** Extract Table with Claude API

**Error message:**
```
messages.0.content.1.document.source.base64.data: Field required
```

**Anthropic API error:**
```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "messages.0.content.1.document.source.base64.data: Field required"
  },
  "request_id": "req_011CXZt9pqEZAi7yDzeVqtFd"
}
```

---

## Detailed Analysis

### Node Execution Flow

| Node | Status | Execution Time | Notes |
|------|--------|----------------|-------|
| Webhook Trigger | ✅ Success | 0ms | Received test payload |
| Download PDF from Drive | ✅ Success | 1,566ms | Retrieved PDF as filesystem-v2 binary |
| Convert Binary to Base64 | ⚠️ Executed | 1ms | **Did NOT convert binary - no output** |
| Extract Table with Claude API | ❌ Failed | 242ms | Missing base64 data field |

### Critical Finding: Move Binary Data Node Failed Silently

The "Convert Binary to Base64" node (type: `moveBinaryData`, mode: `binaryToJson`) executed but **did not convert the filesystem-v2 binary data**.

**Configuration:**
```json
{
  "mode": "binaryToJson",
  "sourceKey": "data",
  "destinationKey": "pdfBase64"
}
```

**Expected behavior:** Should extract base64 string from `binary.data` and place it in `$json.pdfBase64`

**Actual behavior:** Node executed but produced no output. The `$json.pdfBase64` field was never created.

### Evidence from Execution Data

**After Download PDF from Drive:**
```json
{
  "binary": {
    "data": {
      "mimeType": "application/pdf",
      "fileType": "pdf",
      "fileExtension": "pdf",
      "data": "filesystem-v2",
      "fileName": "SwayClarkeNOV2025ExpenseReport[37638].pdf",
      "id": "filesystem-v2:workflows/zFdAi3H5LFFbqusX/executions/6406/binary_data/63803381-ddb9-472d-9bca-4caaa1f3f08d",
      "fileSize": "1.03 MB"
    }
  }
}
```

**After Convert Binary to Base64:**
```json
{
  "json": {
    "headers": {...},
    "body": {...}
    // No pdfBase64 field!
  },
  "binary": {
    "data": {
      "data": "filesystem-v2",  // Still filesystem-v2
      "id": "filesystem-v2:workflows/zFdAi3H5LFFbqusX/executions/6406/binary_data/63803381-ddb9-472d-9bca-4caaa1f3f08d"
    }
  }
}
```

**The `$json.pdfBase64` field does not exist.**

### What the HTTP Request Node Sent

The HTTP Request node's JSON body expression:
```javascript
{{ JSON.stringify({
  model: 'claude-sonnet-4-5',
  max_tokens: 16000,
  messages: [{
    role: 'user',
    content: [
      {
        type: 'text',
        text: '...'
      },
      {
        type: 'document',
        source: {
          type: 'base64',
          media_type: 'application/pdf',
          data: $json.pdfBase64  // Evaluates to undefined
        }
      }
    ]
  }]
}) }}
```

**Actual request sent to Anthropic:**
```json
{
  "type": "document",
  "source": {
    "type": "base64",
    "media_type": "application/pdf"
    // data field is missing (undefined)
  }
}
```

Anthropic API correctly rejected this request: `"messages.0.content.1.document.source.base64.data: Field required"`

---

## Root Cause

**The `moveBinaryData` node cannot access filesystem-v2 binary data.**

When binary data uses the `filesystem-v2` storage format:
- The actual binary content is stored in the filesystem
- The binary object only contains a reference: `"data": "filesystem-v2"`
- The `moveBinaryData` node cannot dereference this and extract the actual base64 content

**This is the same fundamental limitation that affects Code nodes.** The `moveBinaryData` node cannot call `.toBase64()` on filesystem-v2 binary objects because it doesn't have access to internal n8n methods.

---

## Attempts Made (Complete History)

1. ❌ **Code node with `$binary.data.data`** - Returns string "filesystem-v2", not base64
2. ❌ **Code node with `item.binary.data.data`** - Returns string "filesystem-v2"
3. ❌ **HTTP Request node with `$binary.data.data`** - Sends string "filesystem-v2" to API
4. ❌ **Move Binary Data node** - Cannot convert filesystem-v2 reference (this test)

---

## Only Working Solutions

### Option 1: Use AI Agent Node (Recommended)

The AI Agent node has internal access to filesystem-v2 binary data:

```
Download PDF → AI Agent (vision model) → Parse Response → Google Sheets
```

**Pros:**
- Works with filesystem-v2 (internal n8n implementation handles it)
- Native support for PDF vision
- No workarounds needed

**Cons:**
- Less control over API parameters
- Limited to Claude 3.5 Sonnet (not Sonnet 4.5)
- Different response format to parse

### Option 2: Export Binary to External Storage

Write the binary to a temporary location that can generate a URL:

```
Download PDF → Write to Temp File → Upload to Cloud → Get Public URL → HTTP Request with URL
```

**Options:**
- Write to temp file, get local path
- Upload to cloud storage (S3, Google Cloud Storage)
- Use a temporary file service

**Pros:**
- Full control over API calls
- Can use any Claude model (including Sonnet 4.5)

**Cons:**
- More complex workflow
- Additional storage/services needed
- Slower execution

### Option 3: Request n8n Feature

File a feature request for n8n to expose `.toBase64()` method in expressions:

**Current limitation:**
```javascript
// Doesn't work in Code node
const base64 = item.binary.data.toBase64();
```

**Requested feature:**
```javascript
// Should work
const base64 = $binary.data.toBase64();
// or
const base64 = $('Download PDF').item.binary.data.toBase64();
```

---

## Recommendation for Sway

**Use Option 1 (AI Agent node) for now.**

The workflow can be simplified to:

```
Webhook → Download PDF → AI Agent → Parse → Google Sheets → Response
```

This will work immediately without any workarounds. The token cost difference between Sonnet 3.5 and 4.5 is minimal for this use case (expense table extraction).

**If Sonnet 4.5 is required**, implement Option 2 (export to temp storage) or file a feature request with n8n.

---

## Conclusion

**The "Move Binary Data" approach DOES NOT work with filesystem-v2.**

The `moveBinaryData` node cannot convert filesystem-v2 binary references to base64 strings. It executes without error but produces no output, leaving the target field (`$json.pdfBase64`) undefined.

This confirms the fundamental limitation: **filesystem-v2 binary data is not accessible to n8n expressions or downstream nodes that need actual base64 content.**

Only nodes with internal n8n implementation (like AI Agent) or external storage solutions can handle this binary format.
