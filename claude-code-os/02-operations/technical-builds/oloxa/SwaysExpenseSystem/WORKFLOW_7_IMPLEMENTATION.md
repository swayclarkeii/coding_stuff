# Implementation Complete – Workflow 7: Downloads Folder Monitor

## 1. Overview
- **Platform:** n8n
- **Workflow ID:** 6x1sVuv4XKN0002B
- **Status:** Built and validated (19 nodes + 5 sticky notes)
- **Validation:** PASSED (0 errors, 36 non-critical warnings)
- **Files created:**
  - `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/n8n/workflows/W7-downloads-folder-monitor.json`

## 2. Workflow Structure

### Trigger
**Google Drive Trigger** - Watches Downloads folder (synced via G Drive Desktop app)
- Poll interval: Every minute
- Event: File created
- **CONFIGURATION REQUIRED:** User must set the Downloads folder ID after syncing with G Drive Desktop

### Main Processing Steps

1. **Filter Valid Files** (Code node)
   - Extensions: .pdf, .jpg, .jpeg, .png only
   - Max size: 25MB
   - Modified within last 30 days
   - Skips: .csv, .xlsx, .exe, .zip, .dmg, .pkg

2. **Categorize by Filename** (Code node)
   - **sway_invoice**: Filename starts with "SC - " (e.g., "SC - SUPREME MUSIC GmbH - 122025 #540.pdf")
   - **client_invoice**: Contains SUPREME MUSIC, Massive Voices, or BOXHOUSE
   - **invoice**: Contains 'invoice' or 'rechnung'
   - **receipt**: Contains 'receipt', 'beleg', or 'quittung'
   - **unknown**: Skip processing

3. **Skip Unknown Files** (IF node)
   - Only processes files with recognized categories

4. **Download File** (Google Drive node)
   - Downloads file for Claude Vision processing
   - Error handling: Continue on fail

5. **Build Anthropic Request** (Code node)
   - Converts file to base64
   - Detects MIME type (application/pdf, image/jpeg, image/png)
   - Builds category-specific extraction prompts:
     - **Invoices**: Extract invoiceNumber, clientName, amount, currency, date
     - **Receipts**: Extract vendor, amount, currency, date

6. **Call Anthropic API** (HTTP Request node)
   - Model: claude-sonnet-4-5
   - Credential: MRSNO4UW3OEIA3tQ
   - Timeout: 60 seconds
   - Error handling: Continue on fail

7. **Parse Extraction Results** (Code node)
   - Parses JSON response from Claude
   - Error handling for parsing failures

8. **Route by Category** (IF node)
   - Output 0: Invoices (sway_invoice, invoice, client_invoice)
   - Output 1: Receipts (receipt)

### Invoice Path (Output 0)

9. **Check Invoice Pool Duplicates** (Google Drive search)
   - Searches Invoice Pool folder (1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l) for existing file

10. **Skip if Exists** (IF node)
    - Only proceeds if file doesn't already exist

11. **Upload to Invoice Pool** (Google Drive upload)
    - Uploads to folder: 1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l
    - Error handling: Continue on fail

12. **Prepare Invoice Sheet Data** (Code node)
    - Formats: InvoiceID, ClientName, Amount, Currency, Date, FileID, FilePath, ProcessedDate, Source

13. **Log to Invoices Sheet** (Google Sheets append)
    - Spreadsheet: 1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM
    - Sheet: "Invoices"
    - Range: A:I
    - Mode: Auto-map columns

### Receipt Path (Output 1)

14. **Check Receipt Pool Duplicates** (Google Drive search)
    - Searches Receipt Pool folder (1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4) for existing file

15. **Skip if Exists Receipt** (IF node)
    - Only proceeds if file doesn't already exist

16. **Upload to Receipt Pool** (Google Drive upload)
    - Uploads to folder: 1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4
    - Error handling: Continue on fail

17. **Prepare Receipt Sheet Data** (Code node)
    - Formats: Vendor, Amount, Currency, Date, FileID, FilePath, ProcessedDate, Source

18. **Log to Receipts Sheet** (Google Sheets append)
    - Spreadsheet: 1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM
    - Sheet: "Receipts"
    - Range: A:H
    - Mode: Auto-map columns

## 3. Configuration Notes

### Google Drive Folders
- **Invoice Pool:** 1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l
- **Receipt Pool:** 1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4
- **Downloads Folder:** USER_WILL_CONFIGURE_DOWNLOADS_FOLDER_ID (must be set after G Drive Desktop sync)

### Google Sheets
- **Spreadsheet ID:** 1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM
- **Invoices Sheet:** Needs to be created with columns:
  - InvoiceID, ClientName, Amount, Currency, Date, FileID, FilePath, ProcessedDate, Source
- **Receipts Sheet:** Already exists (confirmed in requirements)

### Anthropic API
- **Credential ID:** MRSNO4UW3OEIA3tQ
- **Model:** claude-sonnet-4-5
- **API Version:** 2023-06-01

### File Filtering Rules
- **Valid extensions:** .pdf, .jpg, .jpeg, .png
- **Skip extensions:** .csv, .xlsx, .exe, .zip, .dmg, .pkg
- **Max file size:** 25MB
- **Max file age:** 30 days

### Categorization Patterns
- **Sway's invoices:** Filename starts with "SC - "
- **Client invoices:** Contains "SUPREME MUSIC", "Massive Voices", or "BOXHOUSE"
- **Generic invoices:** Contains "invoice" or "rechnung"
- **Receipts:** Contains "receipt", "beleg", or "quittung"

## 4. Testing

### Prerequisites for Testing
1. **Install Google Drive Desktop app**
2. **Sync Downloads folder** with Google Drive
3. **Note the synced folder ID** from Google Drive web interface
4. **Update workflow:** Set Downloads folder ID in Google Drive Trigger node
5. **Create Invoices sheet** in spreadsheet with required columns
6. **Verify credentials:** Anthropic API, Google Drive OAuth, Google Sheets OAuth

### Happy-Path Test 1: Sway's Invoice
**Input:**
- Filename: `SC - SUPREME MUSIC GmbH - 122025 #540.pdf`
- Place in Downloads folder (after workflow is active)

**Expected Outcome:**
- File categorized as "sway_invoice"
- Invoice number extracted: "540"
- Claude extracts: invoiceNumber, clientName, amount, currency, date
- File uploaded to Invoice Pool (1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l)
- Record logged to Invoices sheet with Source="Downloads"

### Happy-Path Test 2: Client Invoice
**Input:**
- Filename: `Massive Voices - Invoice Dec 2025.pdf`
- Place in Downloads folder (after workflow is active)

**Expected Outcome:**
- File categorized as "client_invoice"
- Claude extracts invoice details
- File uploaded to Invoice Pool
- Record logged to Invoices sheet

### Happy-Path Test 3: Receipt
**Input:**
- Filename: `grocery_receipt_2025-01-10.jpg`
- Place in Downloads folder (after workflow is active)

**Expected Outcome:**
- File categorized as "receipt"
- Claude extracts: vendor, amount, currency, date
- File uploaded to Receipt Pool (1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4)
- Record logged to Receipts sheet with Source="Downloads"

### Edge Case Test 1: Duplicate Prevention
**Input:**
- Upload same invoice twice

**Expected Outcome:**
- First upload: Processes normally
- Second upload: Skips upload (file already exists in pool)
- No duplicate Google Sheets entry

### Edge Case Test 2: Unknown File
**Input:**
- Filename: `random_document.pdf`

**Expected Outcome:**
- File categorized as "unknown"
- Skipped by "Skip Unknown Files" node
- No processing, no upload, no logging

### Edge Case Test 3: Invalid File Type
**Input:**
- Filename: `invoice.xlsx`

**Expected Outcome:**
- Filtered out by "Filter Valid Files" node
- No processing

### Edge Case Test 4: Large File
**Input:**
- Invoice PDF > 25MB

**Expected Outcome:**
- Filtered out by "Filter Valid Files" node
- No processing

### How to Run Tests
1. **Activate workflow** in n8n
2. **Wait 1 minute** for trigger to initialize (sets lastTimeChecked timestamp)
3. **Add test file** to Downloads folder
4. **Wait up to 1 minute** for trigger to poll
5. **Check execution log** in n8n for results
6. **Verify:**
   - File uploaded to correct pool folder
   - Record added to correct Google Sheet
   - Extracted data is accurate

## 5. Handoff

### How to Activate
1. Open workflow in n8n (ID: 6x1sVuv4XKN0002B)
2. Configure Downloads folder ID in Google Drive Trigger node
3. Create Invoices sheet with columns: InvoiceID, ClientName, Amount, Currency, Date, FileID, FilePath, ProcessedDate, Source
4. Verify all credentials are connected (Google Drive, Google Sheets, Anthropic)
5. Click "Active" toggle in workflow header
6. Test with sample files

### How to Modify
- **Change poll interval:** Edit Google Drive Trigger > pollTimes
- **Adjust file filters:** Edit "Filter Valid Files" node code
- **Add categorization rules:** Edit "Categorize by Filename" node code
- **Change extraction prompts:** Edit "Build Anthropic Request" node code
- **Adjust Claude model:** Edit "Call Anthropic API" node parameters

### Where to Look When Something Fails

**No executions firing:**
- Check workflow is Active
- Verify Downloads folder ID is correct
- Ensure G Drive Desktop is syncing
- Check that files were added AFTER workflow activation (trigger only detects changes after lastTimeChecked)

**Files not categorized correctly:**
- Check "Categorize by Filename" node execution
- Verify filename patterns match expectations

**Claude extraction failing:**
- Check "Call Anthropic API" node execution
- Verify Anthropic credential is valid
- Check file is < 25MB and valid format
- Review "Parse Extraction Results" for JSON parsing errors

**Duplicate files appearing:**
- Check "Check Invoice/Receipt Pool Duplicates" node execution
- Verify folder IDs are correct
- Ensure duplicate check query is working

**Files not uploading:**
- Check "Upload to Invoice/Receipt Pool" node execution
- Verify folder IDs: 1V7UmNvDP3a2t6IIbJJI7y8YXz6_X7F6l (invoices), 1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4 (receipts)
- Check Google Drive OAuth credential

**Google Sheets logging failing:**
- Verify Invoices sheet exists and has correct columns
- Check Google Sheets OAuth credential
- Review "Prepare Invoice/Receipt Sheet Data" node for data formatting issues

### Known Limitations

1. **Polling-based trigger** - Only checks every minute (not instant)
2. **Files added before activation** - Won't trigger executions (polling only detects changes after lastTimeChecked)
3. **Filename-based categorization** - Relies on consistent naming patterns
4. **Claude extraction quality** - Depends on invoice/receipt image quality and format
5. **No fuzzy matching** - W7 doesn't do client matching (simple extraction and routing only)
6. **Error handling** - Continue on fail for some nodes (errors won't stop workflow but may result in incomplete processing)

### Suggested Next Steps
- **Test with real files** - Run through all test scenarios above
- **Monitor executions** - Watch first few days of operation for issues
- **Adjust categorization** - Update filename patterns based on actual invoice naming
- **Consider adding notifications** - Add email/Slack node for errors or successful processing
- **Evaluate Claude accuracy** - Review extraction quality, adjust prompts if needed
- **Create Invoices sheet** - Set up with required columns before activating
- **Optimize poll interval** - Adjust based on volume (every minute may be too frequent)

### Related Workflows
- **W7 feeds data to future workflows** - Extracted invoice/receipt data will be used by accounting automation
- **Not integrated with client registry** - W7 is standalone (no client folder routing like other workflows)

## 6. Blueprint Export
**Location:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/n8n/workflows/W7-downloads-folder-monitor.json`

**Import Instructions:**
1. Copy W7-downloads-folder-monitor.json content
2. In n8n, click "Add workflow" → "Import from File"
3. Paste JSON content
4. Configure Downloads folder ID
5. Create Invoices sheet
6. Verify credentials
7. Activate

---

**Built:** 2026-01-11
**Agent:** solution-builder-agent
**Workflow ID:** 6x1sVuv4XKN0002B
**Status:** Ready for testing
