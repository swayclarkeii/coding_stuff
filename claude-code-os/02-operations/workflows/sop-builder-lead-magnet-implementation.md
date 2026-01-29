# Implementation Complete – SOP Builder Lead Magnet

## 1. Overview
- **Platform:** n8n
- **Workflow ID:** ikVyMpDI0az6Zk4t
- **Workflow Name:** SOP Builder Lead Magnet
- **Status:** Built and ready for credential configuration
- **Files touched:**
  - n8n workflow created (ID: ikVyMpDI0az6Zk4t)
  - `/Users/computer/coding_stuff/.claude/agents/tasks/sop-builder-workflow.md` (tracker)

## 2. Workflow Structure

### Trigger
- **Node:** Webhook Trigger
- **Method:** POST
- **Path:** `/sop-builder`
- **Response Mode:** Using Respond to Webhook node
- **Error Handling:** Continue on error (sends error response)

### Main Steps

**1. Parse Form Data (Code)**
- Extracts: email, name, goal, improvement_type, department, process_steps, audio_file
- Determines if audio file is present

**2. Check Audio File (IF)**
- Branches based on presence of audio file
  - **TRUE (audio present):** → Upload to Drive → Transcribe → Set as process_steps
  - **FALSE (text only):** → Use text input directly

**Audio Processing Branch (TRUE):**
- **Upload Audio to Drive (Google Drive)**
  - Resource: File
  - Operation: Upload
  - Destination: My Drive / root
  - Filename: `{email}_sop_audio_{timestamp}.m4a`

- **Transcribe with Whisper (HTTP Request)**
  - API: OpenAI Whisper API
  - Endpoint: https://api.openai.com/v1/audio/transcriptions
  - Model: whisper-1

- **Set Transcription as Steps (Code)**
  - Replaces process_steps with transcription text

**Text Branch (FALSE):**
- **Use Text Input (Code)**
  - Passes through original text input

**3. Merge Audio and Text Paths (Merge)**
- Combines both branches into single flow

**4. LLM: Validate Completeness (HTTP Request)**
- **API:** Anthropic Claude
- **Endpoint:** https://api.anthropic.com/v1/messages
- **Model:** claude-3-5-haiku-20241022
- **Prompt:** "You are an SOP expert. Review this SOP draft and identify: 1) Missing steps 2) Unclear instructions 3) Safety gaps 4) Quality checkpoints needed. Be specific and actionable."

**5. Extract Validation Response (Code)**
- Extracts Claude's response and adds to data flow

**6. LLM: Automation Recommendations (HTTP Request)**
- **API:** Anthropic Claude
- **Endpoint:** https://api.anthropic.com/v1/messages
- **Model:** claude-3-5-haiku-20241022
- **Prompt:** "Based on this SOP, identify which steps could be automated using AI or software. For each suggestion, explain the potential time/cost savings. Be practical - focus on high-impact, easy-to-implement automations."

**7. Extract Automation Response (Code)**
- Extracts Claude's automation recommendations

**8. Generate HTML Report (Code)**
- Creates formatted HTML document with:
  - User's SOP details
  - Original process steps
  - Completeness review
  - Automation opportunities
  - CTA button to Calendly

**9. Convert HTML to PDF (HTTP Request)**
- **Service:** HTML2PDF API
- **Endpoint:** https://api.html2pdf.app/v1/generate
- **Output:** Binary PDF file

**10. Send Email with PDF (Gmail)**
- **Resource:** Message
- **Operation:** Send
- **To:** User's email
- **Subject:** "Your SOP Analysis is Ready"
- **Body:** HTML email with summary and CTA
- **Attachment:** Generated PDF

**11. Log Lead in CRM (Google Sheets)**
- **Document ID:** 1PwIqO1nfEeABoRRvTml3dN9q1rUjHIMVXsqOLtouemk
- **Operation:** Append
- **Columns:** timestamp, email, name, goal, department, improvement_type, source
- **Source value:** "sop-builder"

**12. Respond to Webhook**
- **Format:** JSON
- **Response:** `{ "success": true, "message": "Your SOP analysis has been sent to your email!" }`
- **Status Code:** 200

### Error Handling Branch
- **Error Handler (Code)** - Captures error details
- **Notify Sway of Error (Gmail)** - Sends error notification to sway@oloxa.ai
- **Error Response to User (Respond to Webhook)** - Returns error message to user

### Key Branches / Decisions
- **Audio vs Text:** IF node checks for audio file presence
  - Audio present: Upload → Transcribe → Use transcription
  - No audio: Use text input directly
- **Error handling:** Global error flow sends notification and user-friendly response

## 3. Configuration Notes

### Credentials Required
**To activate this workflow, configure these credentials in n8n:**

1. **Google Drive OAuth2**
   - Credential name: `google-oauth-sway` (or update in node)
   - Permissions: Drive file upload

2. **OpenAI API**
   - Credential name: `openai-sway` (or update in node)
   - Used for: Whisper transcription

3. **Anthropic API**
   - Credential name: `anthropicApi` (predefined type)
   - Used for: Claude Haiku LLM calls (2 nodes)

4. **Gmail OAuth2**
   - Credential name: Existing Gmail credentials
   - Used for: Email sending (2 nodes)

5. **Google Sheets OAuth2**
   - Credential name: Existing Google Sheets credentials
   - Sheet ID: 1PwIqO1nfEeABoRRvTml3dN9q1rUjHIMVXsqOLtouemk

### Important Mappings
- **Audio upload filename:** `{email}_sop_audio_{timestamp}.m4a`
- **PDF filename:** `{name}_SOP_Analysis.pdf`
- **Webhook path:** `/sop-builder`
- **CRM source tag:** "sop-builder"

### Filters / Error Handling
- **Webhook:** Continues on error, always sends response
- **Error notifications:** Sent to sway@oloxa.ai
- **User error message:** Generic message + contact promise
- **Error response code:** 500

## 4. Testing

### Happy-Path Test

**Input (POST to webhook):**
```json
{
  "email": "test@example.com",
  "name": "Test User",
  "goal": "Improve onboarding process",
  "improvement_type": "quality",
  "department": "HR",
  "process_steps": "1. Send welcome email\n2. Schedule orientation\n3. Set up accounts"
}
```

**Expected Outcome:**
1. Form data parsed successfully
2. Text path selected (no audio)
3. Two LLM analyses completed
4. HTML report generated
5. PDF created and attached
6. Email sent to test@example.com
7. Lead logged in Google Sheets with source="sop-builder"
8. Webhook returns: `{ "success": true, "message": "Your SOP analysis has been sent to your email!" }`

### How to Run
1. **Activate the workflow** in n8n UI
2. **Get webhook URL** from Webhook Trigger node
3. **Send POST request** with form data (JSON body or multipart form-data)
4. **Check email** for PDF delivery
5. **Verify CRM** entry in Google Sheets

### Audio Path Test

**Input (POST with audio file):**
```
Content-Type: multipart/form-data

email: test@example.com
name: Test User
goal: Improve safety protocol
improvement_type: safety
department: Operations
audio_file: [binary m4a/mp3 file]
```

**Expected Outcome:**
1. Audio uploaded to Google Drive
2. Transcribed via Whisper API
3. Transcription used as process_steps
4. Rest of flow identical to text path

## 5. Handoff

### How to Modify
- **Change LLM prompts:** Edit "LLM: Validate Completeness" and "LLM: Automation Recommendations" nodes
- **Update email template:** Edit "Send Email with PDF" node
- **Change PDF styling:** Edit HTML template in "Generate HTML Report" node
- **Modify CRM columns:** Update "Log Lead in CRM" columns mapping

### Known Limitations
1. **PDF generation** requires external API (html2pdf.app) - may need API key or fallback service
2. **Audio transcription** costs money per request (OpenAI Whisper pricing)
3. **LLM calls** incur cost per analysis (Claude Haiku pricing)
4. **Google Sheets** must have matching column headers (timestamp, email, name, goal, department, improvement_type, source)
5. **No retry logic** on API failures (errors go to error handler)

### Credentials Setup Checklist
Before activating:
- [ ] Configure Google Drive OAuth2 credentials
- [ ] Configure OpenAI API credentials
- [ ] Configure Anthropic API credentials (Claude)
- [ ] Configure Gmail OAuth2 credentials
- [ ] Configure Google Sheets OAuth2 credentials
- [ ] Verify CRM spreadsheet ID and column headers
- [ ] Test webhook endpoint with sample data
- [ ] Verify html2pdf.app service is accessible (or configure alternative)

### Suggested Next Step
- **Option 1:** Use test-runner-agent to create and run automated tests
- **Option 2:** Manually test with sample data in n8n UI
- **Option 3:** If LLM costs become an issue, use workflow-optimizer-agent to optimize prompts

### Webhook URL
After activation, webhook will be available at:
`https://n8n.oloxa.ai/webhook/sop-builder`

## 6. Cost Considerations

**Per Lead Processed:**
- OpenAI Whisper (if audio): ~$0.006 per minute of audio
- Claude Haiku (2 calls): ~$0.001 per call (varies by length)
- HTML2PDF: Check service pricing
- Gmail/Google Drive/Sheets: Free with existing workspace

**Estimated cost per lead:** $0.01 - $0.05 depending on audio length and SOP complexity

---

**Workflow Status:** ✅ Ready for credential configuration and testing
**Build Date:** 2026-01-28
**Build Agent:** solution-builder-agent
