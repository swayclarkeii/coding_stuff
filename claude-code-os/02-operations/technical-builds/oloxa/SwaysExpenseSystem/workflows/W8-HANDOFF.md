# Implementation Complete – Workflow 8: G Drive Invoice Collector

## 1. Overview
- **Platform:** n8n
- **Workflow ID:** JNhSWvFLDNlzzsvm
- **Status:** Built and validated (ready for testing)
- **Files:**
  - `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/workflows/w8-gdrive-invoice-collector.json`
  - `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/workflows/W8-HANDOFF.md`

## 2. Workflow Structure

### Trigger
- **Google Drive Trigger** - Watches Sway's invoice production folder (`1_zVNS3JHS15pUjvfEJMh9nzYWn6TltbS`)
- **Event:** `fileCreated` (only new files)
- **Poll Interval:** Every 5 minutes

### Main Steps
1. **Filter Valid Files** (IF node)
   - Extension must be `.pdf`
   - Filename must start with `"SC - "` (Sway's invoice prefix)
   - Size must be < 10MB

2. **List Invoice Pool Files** (Google Drive Search)
   - Searches Invoice Pool folder for existing files
   - Used for duplicate detection

3. **Check for Duplicates** (Code node)
   - Compares new invoice filename against existing pool files
   - Returns empty array (stops workflow) if duplicate found
   - Continues if no duplicate

4. **Download Invoice** (Google Drive Download)
   - Downloads PDF binary data from production folder
   - Preserves binary for Anthropic API

5. **Build Anthropic Request** (Code node)
   - Converts PDF to base64
   - Builds API request with extraction prompt
   - Preserves binary data through chain

6. **Call Anthropic API** (HTTP Request)
   - Model: `claude-sonnet-4-5`
   - Extracts: Invoice #, Client Name, Amount, Currency, Date, Project
   - Error handling: `onError: continueRegularOutput`

7. **Parse Anthropic Response** (Code node)
   - Extracts JSON from API response
   - Strips markdown code fences if present
   - Validates required fields
   - Maps to Google Sheets column format

8. **Copy Invoice to Pool** (Google Drive Copy)
   - **COPY** not move (preserves original in production folder)
   - Destination: Invoice Pool folder (`1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l`)

9. **Log to Invoices Sheet** (Google Sheets Append)
   - Spreadsheet: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
   - Sheet: `Invoices`
   - Range: `Invoices!A:I`
   - Mode: Auto-map columns

### Key Branches / Decisions
- **Filter Valid Files:** Only `.pdf` files starting with `"SC - "` proceed
- **Check for Duplicates:** Returns 0 items (stops execution) if duplicate found
- **Error Handling:** Anthropic API continues on fail (some PDFs may not parse correctly)

## 3. Configuration Notes

### Credentials Used
- **Google Drive OAuth2:** `google-drive-oauth`
- **Google Sheets OAuth2:** `google-sheets-oauth`
- **Anthropic API:** `MRSNO4UW3OEIA3tQ` (claude-sonnet-4-5)

### Important Mappings

#### Invoice Extraction Format (from Anthropic)
```json
{
  "invoiceNumber": "539",
  "clientName": "SUPREME MUSIC GmbH",
  "amount": 416.5,
  "currency": "EUR",
  "date": "16.12.2025",
  "project": "Project #25-0120"
}
```

#### Google Sheets Output Format
```javascript
{
  InvoiceID: "539",
  ClientName: "SUPREME MUSIC GmbH",
  Amount: 416.5,
  Currency: "EUR",
  Date: "16.12.2025",
  Project: "Project #25-0120",
  FileID: "1abc...",
  FileName: "SC - SUPREME MUSIC GmbH - 122025 #540.pdf",
  ProcessedDate: "2026-01-11T00:15:00.000Z",
  Source: "G Drive Production"
}
```

### Filters / Error Handling
- **File Filter:** `.pdf` extension AND `"SC - "` prefix AND < 10MB
- **Duplicate Prevention:** Filename-based comparison against Invoice Pool
- **Anthropic API:** Continue on fail (logs error but doesn't stop workflow)
- **Binary Preservation:** Explicitly preserved through Code nodes

## 4. Testing

### Prerequisites
Before testing, ensure:
1. **Invoices Sheet exists** in spreadsheet `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
2. **Column headers match exactly:**
   - InvoiceID
   - ClientName
   - Amount
   - Currency
   - Date
   - Project
   - FileID
   - FileName
   - ProcessedDate
   - Source
3. **Anthropic API credential** is active and has credits
4. **Google OAuth credentials** are connected and valid

### Happy-Path Test

**Input:**
1. Create a test German invoice PDF with this structure:
   ```
   RECHNUNG AN: Test Client GmbH
   DATUM: 11.01.2026
   RECHNUNG #: TEST-001
   INSGESAMT: € 100.00
   Projekt: Test Project
   ```
2. Save as: `SC - Test Client GmbH - 012026 #TEST-001.pdf`
3. Upload to Sway's invoice production folder **AFTER** activating workflow

**Expected Outcome:**
1. Workflow triggers within 5 minutes
2. Invoice details extracted by Claude Vision
3. Invoice copied to Invoice Pool folder
4. New row added to Invoices sheet with extracted data
5. Source field shows: `"G Drive Production"`

**How to Run:**
1. Activate workflow in n8n
2. Wait 1 minute (for trigger to start polling)
3. Upload test invoice to production folder (`1_zVNS3JHS15pUjvfEJMh9nzYWn6TltbS`)
4. Wait up to 5 minutes for execution
5. Check:
   - Invoice Pool folder for copied file
   - Invoices sheet for new row
   - n8n execution log for details

### Edge Case Tests

**Test 2: Duplicate Invoice**
- Upload same invoice twice
- Expected: Second upload is skipped (no duplicate in pool)

**Test 3: Non-SC Invoice**
- Upload invoice without "SC - " prefix
- Expected: Filtered out, no processing

**Test 4: Large PDF**
- Upload PDF > 10MB
- Expected: Filtered out, no processing

**Test 5: Anthropic API Failure**
- Upload malformed PDF or corrupt file
- Expected: API fails gracefully, workflow continues (doesn't crash)

## 5. Handoff

### How to Modify

**Change trigger interval:**
1. Open workflow in n8n
2. Edit "Google Drive Trigger" node
3. Modify `pollTimes` parameter

**Change extraction fields:**
1. Edit "Build Anthropic Request" node
2. Update the extraction prompt text
3. Edit "Parse Anthropic Response" node to map new fields
4. Update Google Sheets column headers

**Change invoice folder:**
1. Edit "Google Drive Trigger" node
2. Update `folderToWatch.value` parameter
3. Update "Copy Invoice to Pool" node `folderId` if needed

### Known Limitations

1. **German invoices only:** Extraction prompt is tailored for German format
2. **Filename pattern:** Must start with "SC - " to be processed
3. **PDF size limit:** 10MB maximum (Anthropic API constraint)
4. **Polling delay:** Up to 5 minutes between file upload and processing
5. **No OCR:** Relies on Claude Vision to extract from PDF (scanned images may fail)
6. **No duplicate detection by content:** Only checks filename, not invoice number
7. **Copy not move:** Original invoices remain in production folder (manual cleanup required)

### Pre-Deployment Checklist

- [ ] Create "Invoices" sheet in spreadsheet with correct column headers
- [ ] Verify Anthropic API credential has sufficient credits
- [ ] Test with sample invoice to verify extraction accuracy
- [ ] Confirm Google Drive folder IDs are correct
- [ ] Set up monitoring for failed extractions (check n8n execution logs)
- [ ] Document invoice filename convention for Sway
- [ ] Plan for Invoice Pool cleanup (archived old invoices)

### Suggested Next Steps

1. **Test with real invoices:** Use actual Sway invoices to verify extraction accuracy
2. **Create W3 integration:** Match invoices against bank statement income (as planned)
3. **Add error notifications:** Send email/Slack when Anthropic extraction fails
4. **Improve duplicate detection:** Use invoice number instead of just filename
5. **Add invoice validation:** Check if amount/client matches expected patterns
6. **Set up archival:** Move old invoices from production folder to archive

### Integration with W3 (Income Matcher)

This workflow populates the Invoice Pool that W3 will search:

**W3 will:**
1. Read income transactions from bank statements
2. Extract invoice # and client name from bank description
3. Search Invoice Pool for matches using:
   - Invoice # (exact match)
   - Client Name (fuzzy match 70%+)
   - Amount (exact match)

**Data contract:**
- `InvoiceID` must be clean (no prefixes, just number)
- `ClientName` must be full company name (not abbreviated)
- `Amount` must be decimal number (not string)
- `Currency` must always be "EUR" for Sway's invoices

## 6. Files and Resources

### Workflow Files
- **n8n Workflow ID:** `JNhSWvFLDNlzzsvm`
- **JSON Export:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/workflows/w8-gdrive-invoice-collector.json`

### Google Resources
- **Invoice Production Folder:** `1_zVNS3JHS15pUjvfEJMh9nzYWn6TltbS`
- **Invoice Pool Folder:** `1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l`
- **Invoices Sheet Spreadsheet:** `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`

### API Credentials
- **Anthropic API:** Credential ID `MRSNO4UW3OEIA3tQ` (claude-sonnet-4-5)

## 7. Monitoring and Maintenance

### What to Monitor
1. **Execution frequency:** Should trigger when new invoices are added
2. **Success rate:** Track Anthropic API extraction failures
3. **Duplicate rate:** How often duplicates are prevented
4. **Processing time:** Average time from upload to logging

### Maintenance Tasks
1. **Weekly:** Review failed extractions in n8n execution log
2. **Monthly:** Archive old invoices from production folder
3. **Quarterly:** Review and clean up Invoice Pool duplicates
4. **As needed:** Update extraction prompt if invoice format changes

### Troubleshooting

**Problem: Workflow doesn't trigger**
- Check: Workflow is activated in n8n
- Check: Trigger polling is running (view last execution time)
- Check: Invoice was uploaded AFTER trigger started polling

**Problem: Invoice not extracted correctly**
- Check: PDF is readable (not scanned/image-based)
- Check: Invoice follows expected German format
- Check: Anthropic API execution log for error details

**Problem: Invoice not copied to pool**
- Check: Google Drive credential is valid
- Check: Invoice Pool folder ID is correct
- Check: Destination folder has write permissions

**Problem: Sheet not updated**
- Check: Column headers match exactly (case-sensitive)
- Check: Sheet name is "Invoices" (exact match)
- Check: Google Sheets credential is valid
- Check: Spreadsheet ID is correct

---

**Built by:** solution-builder-agent
**Date:** 2026-01-11
**Status:** Ready for testing
**Next Agent:** test-runner-agent (for automated testing)
