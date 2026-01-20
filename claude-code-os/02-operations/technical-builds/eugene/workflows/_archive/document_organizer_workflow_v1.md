# Document Organizer Workflow - Version 1

**Client:** Eugene (Real Estate Debt Advisory)
**Purpose:** Automatically classify, rename, and organize uploaded documents into standardized folder structure
**Created:** 2024-12-20
**Version:** 1.0

---

## Overview

This workflow automates the organization of real estate documents by:
1. Monitoring Gmail inbox for email attachments
2. Downloading and uploading attachments to Google Drive
3. Extracting text content from documents
4. Classifying document type using AI
5. Renaming files with standardized naming convention
6. Moving files to appropriate client folders
7. Logging all actions for audit trail

---

## Workflow Diagram

```
┌─────────────────────────────┐
│  Gmail Trigger              │
│  (Watch for attachments)    │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Download Email Attachments │
│  (Extract files from email) │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Upload to Google Drive     │
│  (Client upload folder)     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Extract Text from PDF      │
│  (n8n PDF parser node)      │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  OpenAI - Classify Document │
│  (AI Agent node)            │
│                             │
│  Types:                     │
│  - gundh_book               │
│  - exit_strategy            │
│  - financial_projections    │
│  - property_deed            │
│  - loan_documents           │
│  - appraisal                │
│  - unknown                  │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Switch Node                │
│  (Route based on type)      │
└─┬───┬───┬───┬───┬───┬───┬──┘
  │   │   │   │   │   │   │
  ▼   ▼   ▼   ▼   ▼   ▼   ▼
┌───┐┌──┐┌───┐┌────┐┌────┐┌────┐┌────┐
│GB ││ES││FP ││PD  ││LD  ││APR ││UNK │
└─┬─┘└┬─┘└─┬─┘└──┬─┘└──┬─┘└──┬─┘└──┬─┘
  │   │   │     │     │     │     │
  ▼   ▼   ▼     ▼     ▼     ▼     ▼
┌────────────────────────────────────┐
│  Rename File Node                  │
│  (Set standardized filename)       │
│                                    │
│  Format:                           │
│  GUNDH_{client}_{date}.pdf         │
│  EXIT_{client}_{date}.pdf          │
│  FIN_{client}_{date}.pdf           │
│  etc.                              │
└──────────┬─────────────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Move to Folder Node        │
│  (Google Drive/Dropbox)     │
│                             │
│  Folders:                   │
│  01_Gundh_Books            │
│  02_Exit_Strategies        │
│  03_Financial_Projections  │
│  04_Property_Deeds         │
│  05_Loan_Documents         │
│  06_Appraisals             │
│  07_Miscellaneous          │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Log to Google Sheets       │
│  (Audit trail)              │
│                             │
│  Columns:                   │
│  - Timestamp                │
│  - Original Filename        │
│  - Document Type            │
│  - New Filename             │
│  - Destination Folder       │
│  - Client Name              │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Response Node              │
│  (Confirm completion)       │
└─────────────────────────────┘
```

---

## Node Details

### 1. Gmail Trigger
- **Type:** `n8n-nodes-base.gmailTrigger`
- **Mode:** Watch for new emails
- **Filter:** Emails with attachments (PDF, DOCX)
- **Label Filter:** Optional (e.g., "ClientDocuments" label)
- **Polling Interval:** Every 1 minute

### 2. Download Email Attachments
- **Type:** `n8n-nodes-base.gmail`
- **Operation:** Download attachments
- **Input:** Email ID from trigger
- **Output:** Binary file data (PDF, DOCX, etc.)

### 3. Upload to Google Drive
- **Type:** `n8n-nodes-base.googleDrive`
- **Operation:** Upload file
- **Destination:** Client upload folder
- **Filename:** Original attachment filename
- **Output:** File ID and metadata

### 4. Extract PDF Text
- **Type:** `n8n-nodes-base.extractFromFile`
- **Operation:** Extract text
- **Input:** Binary file data from Google Drive
- **Options:**
  - Max pages: 10 (first 10 pages for classification)
  - OCR: Disabled (assumes digital PDFs)
- **Output:** Plain text string

### 5. AI Classifier
- **Type:** `@n8n/n8n-nodes-langchain.agent`
- **Model:** GPT-4
- **Prompt:** Classification system prompt (see below)
- **Input:** First 3000 characters of document text
- **Output:** Document type classification

### 6. Switch Node
- **Type:** `n8n-nodes-base.switch`
- **Rules:** 7 branches based on document type
- **Default:** Route to "unknown" branch

### 7. Rename Nodes (7 branches)
- **Type:** `n8n-nodes-base.set`
- **Function:** Set new filename and destination folder
- **Naming Pattern:** `{TYPE}_{CLIENT}_{YYYYMMDD}.{ext}`

### 8. Move File Node
- **Type:** `n8n-nodes-base.googleDrive`
- **Operation:** Move and rename file
- **Destination:** Client folder structure

### 9. Log Node
- **Type:** `n8n-nodes-base.googleSheets`
- **Operation:** Append row
- **Sheet:** Document Processing Log

### 10. Email Confirmation (Optional)
- **Type:** `n8n-nodes-base.gmail`
- **Operation:** Send email
- **Recipient:** Original sender
- **Subject:** "Document Processed: {filename}"
- **Body:** Processing details and file location

---

## AI Classification Prompt

```
You are a document classifier for real estate files.

Classify documents into these types:
- "gundh_book": Land measurement records, plot dimensions, surveys, boundary descriptions
- "exit_strategy": Exit plans, liquidation strategies, timeline documents, ROI projections
- "financial_projections": IRR calculations, cash flow analysis, cap rate, NPV, financial models
- "property_deed": Legal property ownership documents, title documents
- "loan_documents": Mortgage agreements, loan terms, financing documents
- "appraisal": Property valuation reports, appraisal documents
- "unknown": Cannot determine type

Analyze the document content and respond with ONLY the document type.
Examples:
- If you see plot dimensions, boundaries, area → "gundh_book"
- If you see exit timeline, ROI, liquidation → "exit_strategy"
- If you see IRR, NPV, cash flows → "financial_projections"

Return ONLY the type name, nothing else.
```

---

## File Naming Convention

| Document Type | Prefix | Example |
|---------------|--------|---------|
| Gundh Book | GUNDH | `GUNDH_Eugene_Client_20241220.pdf` |
| Exit Strategy | EXIT | `EXIT_Eugene_Client_20241220.pdf` |
| Financial Projections | FIN | `FIN_Eugene_Client_20241220.pdf` |
| Property Deed | DEED | `DEED_Eugene_Client_20241220.pdf` |
| Loan Documents | LOAN | `LOAN_Eugene_Client_20241220.pdf` |
| Appraisal | APPR | `APPR_Eugene_Client_20241220.pdf` |
| Unknown | MISC | `MISC_Eugene_Client_20241220.pdf` |

---

## Folder Structure

```
clients/
└── {Client_Name}/
    ├── 01_Gundh_Books/
    ├── 02_Exit_Strategies/
    ├── 03_Financial_Projections/
    ├── 04_Property_Deeds/
    ├── 05_Loan_Documents/
    ├── 06_Appraisals/
    ├── 07_Miscellaneous/
    └── 08_Analysis_Reports/
```

---

## Variables Required

| Variable | Description | Example |
|----------|-------------|---------|
| `gmailCredentials` | Gmail OAuth2 credentials | OAuth setup in n8n |
| `clientName` | Client identifier | "Eugene_Client" |
| `openaiApiKey` | OpenAI API key | "sk-..." |
| `googleDriveFolderId` | Base client folder ID | "1a2b3c..." |
| `uploadFolderId` | Upload staging folder ID | "4d5e6f..." |
| `logSheetId` | Google Sheets log ID | "spreadsheet-id" |
| `gmailLabel` | Optional filter label | "ClientDocuments" |

---

## Error Handling

### Gmail Connection Issues
- Retry mechanism: 3 attempts with exponential backoff
- Log authentication failures
- Alert admin if Gmail quota exceeded

### No Attachments Found
- Skip email and continue monitoring
- Log emails without attachments (optional)

### Unsupported File Types
- Filter for PDF, DOCX, DOC only
- Skip other file types (images, zip, etc.)
- Log unsupported file types

### Low Confidence Classification
- If AI confidence < 70%, route to "unknown" folder
- Log warning in Google Sheets
- Flag for manual review

### File Already Exists
- Append version number: `_v2`, `_v3`, etc.
- Log duplicate in Google Sheets

### Upload Failure
- Retry upload to Google Drive (3 attempts)
- Log error details
- Send error notification to admin

---

## Performance Metrics

- **Email Detection Latency:** ~1 minute (polling interval)
- **Processing Time:** ~8-12 seconds per document
  - Gmail download: ~1-2 seconds
  - Google Drive upload: ~2-3 seconds
  - Text extraction: ~1-2 seconds
  - AI classification: ~2-3 seconds
  - File operations: ~2 seconds
- **Classification Accuracy:** ~95%
- **API Cost:** ~$0.007 per document (text extraction method)
- **Throughput:** ~300 documents/hour
- **Gmail API Quota:** 1 billion quota units/day (essentially unlimited for this use case)

---

## Future Enhancements (v2+)

1. **Multi-language Support:** Detect document language
2. **OCR Integration:** Handle scanned documents
3. **Duplicate Detection:** Check for existing similar files
4. **Auto-Analysis:** Trigger specialist agents for deep analysis
5. **Email Notifications:** Alert client when processing complete
6. **Batch Processing:** Handle multiple file uploads

---

## Testing Checklist

- [ ] Send email with PDF attachment → Gmail detects within 1 minute
- [ ] Attachment downloaded successfully from Gmail
- [ ] File uploaded to Google Drive staging folder
- [ ] Text extracted from PDF correctly
- [ ] Gundh Book → Classified correctly → Renamed → Moved to 01_Gundh_Books
- [ ] Exit Strategy → Classified correctly → Renamed → Moved to 02_Exit_Strategies
- [ ] Financial Doc → Classified correctly → Renamed → Moved to 03_Financial_Projections
- [ ] Unknown Doc → Routes to 07_Miscellaneous
- [ ] Duplicate filename → Appends version number
- [ ] Log entry created in Google Sheets with original sender email
- [ ] Error handling works for invalid file types
- [ ] Email without attachments → Skipped gracefully
- [ ] Multiple attachments in one email → All processed separately
- [ ] Optional: Confirmation email sent to original sender

---

## Maintenance Notes

**Last Updated:** 2024-12-20
**Maintained By:** Sway Clarke
**Review Frequency:** Monthly
**Next Review:** 2025-01-20

**Known Issues:**
- None (v1.0)

**Dependencies:**
- n8n (self-hosted or cloud)
- Gmail API access (OAuth2 authentication)
- OpenAI API access (GPT-4 or GPT-4o-mini)
- Google Drive API access
- Google Sheets API access

**Gmail Setup Requirements:**
1. Enable Gmail API in Google Cloud Console
2. Create OAuth2 credentials
3. Configure authorized redirect URIs for n8n
4. Grant permissions: `gmail.readonly`, `gmail.modify`
