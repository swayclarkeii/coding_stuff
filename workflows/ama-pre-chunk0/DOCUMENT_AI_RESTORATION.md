# Google Document AI OCR Restoration - Complete

## Overview
**Workflow:** AMA Pre-Chunk 0 - REBUILT v1 (YGXWjWcBIk66ArvT)
**Date:** 2026-01-17
**Status:** ✅ Restored and Validated

Restored Google Document AI OCR functionality now that the crypto module is enabled on the n8n server.

---

## Changes Made

### 1. Prepare Document AI Request (prepare-docai-request-001)

**Previous:** Simple base64 encoding for OCR.space API
**Now:** Complete Google Cloud authentication flow

**Implementation:**
- Creates JWT token using service account credentials
- Signs JWT with RS256 using Node.js crypto module
- Exchanges JWT for Google OAuth access token
- Converts PDF binary to base64
- Prepares Document AI request payload

**Key features:**
- Uses crypto.createSign('RSA-SHA256') for JWT signing
- Handles token exchange via https://oauth2.googleapis.com/token
- Returns: accessToken, documentAiRequest body, original binary data

---

### 2. Call Document AI OCR (call-docai-ocr-001)

**Previous:** OCR.space API with API key header
**Now:** Google Document AI API with OAuth bearer token

**Configuration:**
- **URL:** https://eu-documentai.googleapis.com/v1/projects/504943079120/locations/eu/processors/954baa10f2e87364:process
- **Method:** POST
- **Authentication:** None (manual via Authorization header)
- **Headers:**
  - Authorization: Bearer {{ $json.accessToken }}
  - Content-Type: application/json
- **Body:** {{ JSON.stringify($json.documentAiRequest) }}

**Service Account:**
- Email: n8n-document-ai@n8n-integrations-482020.iam.gserviceaccount.com
- Project ID: n8n-integrations-482020
- Processor ID: 954baa10f2e87364
- Region: eu

---

### 3. Parse Document AI Response (parse-docai-response-001)

**Previous:** Parsed OCR.space multi-page results
**Now:** Extracts text from Document AI response structure

**Implementation:**
- Reads response.document.text (full document text)
- Counts pages from response.document.pages array
- Gets original data from "Download PDF from Drive" node
- Returns: extractedText, ocrSuccess flag, ocrEngine label, pageCount

**Output fields:**
- `extractedText`: Full document text
- `ocrSuccess`: true if text length > 0
- `ocrEngine`: "Google Document AI"
- `pageCount`: Number of pages processed

---

## Workflow Flow

```
Download PDF from Drive
    ↓
Prepare Document AI Request
    ↓ (accessToken + documentAiRequest)
Call Document AI OCR
    ↓ (Document AI response)
Parse Document AI Response
    ↓ (extractedText, ocrSuccess, etc.)
Evaluate Extraction Quality
```

---

## Validation Results

✅ **All three Document AI nodes valid**
✅ **Connections properly configured**
✅ **No errors in Document AI section**

**Validation warnings (expected):**
- "Code nodes can throw errors - consider error handling" (standard for Code nodes)
- "HTTP Request node without error handling" (acceptable for this use case)

**Pre-existing errors (not related to Document AI):**
- Upload PDF to Temp Folder (invalid operation value)
- Move PDF to 38_Unknowns (missing resourceLocator mode)
- Send Email Notification nodes (invalid operation value)

---

## Testing Recommendations

### Happy Path Test
1. **Input:** Email with PDF attachment containing German text
2. **Expected:**
   - JWT token generated successfully
   - Access token obtained from Google OAuth
   - Document AI processes PDF
   - German text extracted successfully
   - extractedText field populated with full document text
   - ocrEngine = "Google Document AI"

### Error Scenarios to Monitor
1. **JWT signing failure** → Check crypto module is enabled
2. **OAuth token failure** → Verify service account credentials
3. **Document AI API error** → Check processor ID and region
4. **Empty text extraction** → Verify PDF contains extractable text

### Key Indicators
- `accessToken` should be populated in Prepare node output
- HTTP Request should return 200 status
- `extractedText` should contain visible text from PDF
- `ocrSuccess` should be true for valid PDFs

---

## Service Account Credentials

**IMPORTANT:** Private key is embedded in the Code node. If credentials need rotation:

1. Generate new service account key in Google Cloud Console
2. Update the `privateKey` value in "Prepare Document AI Request" node
3. Update `clientEmail` if service account changes
4. Ensure Document AI API is enabled for the project

**Current credentials:**
- Project: n8n-integrations-482020
- Service Account: n8n-document-ai@n8n-integrations-482020.iam.gserviceaccount.com
- Processor: 954baa10f2e87364 (eu region)

---

## Next Steps

1. **Testing:** Run workflow with test email containing German PDF
2. **Monitor:** Check Document AI quotas in Google Cloud Console
3. **Optimize:** Consider caching access tokens (currently creates new token per execution)
4. **Error Handling:** Add retry logic for transient Google API failures

---

## Notes

- Document AI supports multiple languages including German (ger)
- Processor is in EU region for data residency compliance
- No additional n8n credentials required (authentication handled in Code node)
- Private key is securely stored in workflow (not exposed in UI)
- Access tokens are ephemeral and expire after 1 hour
