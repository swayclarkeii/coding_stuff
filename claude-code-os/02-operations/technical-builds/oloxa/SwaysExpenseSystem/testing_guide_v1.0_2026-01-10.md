# Expense System Testing Guide

**Version**: 1.0
**Date**: 2026-01-10
**Workflows Covered**: W1, W2, W3, W4, W6

---

## 📋 Pre-Test Checklist

Before testing any workflow, verify the following:

### Environment Setup
- [ ] n8n instance accessible at https://n8n.oloxa.ai
- [ ] All OAuth2 credentials are valid (not expired)
- [ ] Google Drive folders exist with correct IDs
- [ ] Google Sheets exist with correct sheet names
- [ ] Sufficient Google API quota available

### Credential Verification
- [ ] Gmail OAuth2: `sway@oloxa.ai` and `swayclarkeii@gmail.com`
- [ ] Google Drive OAuth2: Connected to correct Google Workspace account
- [ ] Google Sheets OAuth2: Connected to correct Google Workspace account
- [ ] Google Cloud Vision API OAuth2: Scope `https://www.googleapis.com/auth/cloud-vision`
- [ ] Claude Sonnet 4.5 API: Valid Anthropic API key

### Workflow Status
- [ ] W1: Active (trigger-based)
- [ ] W2: Active (trigger-based)
- [ ] W3: Ready (manual trigger only)
- [ ] W4: Active (trigger-based)
- [ ] W6: Active (trigger-based)

---

## 🧪 W1: Bank Statement Monitor

### Test Type: Google Drive Trigger Test

**Trigger**: Upload new bank statement PDF to Google Drive

### Test Steps

1. **Prepare Test File:**
   - Use a real bank statement PDF (e.g., Chase, BOA, etc.)
   - Ensure PDF contains transaction table with dates, descriptions, amounts
   - Recommended: Use a statement with 5-10 transactions

2. **Upload to Google Drive:**
   - Navigate to the "Bank Statements" folder in Google Drive
   - Upload the test PDF
   - File should trigger W1 automatically

3. **Monitor Execution:**
   - In n8n, go to Executions tab
   - Look for new execution of "W1: Bank Statement Monitor"
   - Expected execution time: 30-60 seconds (depends on PDF size)

### Success Criteria

**✅ Execution Status:**
- Execution completes without errors
- All nodes show green checkmarks
- No "ERROR" status in execution log

**✅ Data Validation:**
- Open Google Sheets "Statements" sheet
- New row added with:
  - `StatementID` (unique UUID)
  - `StatementDate` (extracted from PDF)
  - `FilePath` (Google Drive link)
  - `UploadDate` (current date)
- Transactions extracted and added to "Transactions" sheet with:
  - `TransactionID` (unique UUID)
  - `StatementID` (matches statement row)
  - `Date`, `Description`, `Amount`, `Type` (Income/Expense)

**✅ File Handling:**
- Original PDF remains in "Bank Statements" folder
- PDF filename preserved in Sheets

### Common Issues

**Issue**: Execution doesn't start
- **Check**: W1 is active in n8n
- **Check**: Google Drive trigger folder ID is correct
- **Solution**: Reactivate workflow or verify folder permissions

**Issue**: No transactions extracted
- **Check**: PDF contains readable table (not scanned image)
- **Check**: Claude API key is valid
- **Solution**: Test with different PDF or check API quota

**Issue**: Duplicate transactions
- **Check**: Duplicate detection logic in Code node
- **Solution**: Verify StatementID logic in workflow

---

## 📧 W2: Gmail Receipt Monitor

### Test Type: Manual Webhook Trigger OR Schedule Trigger

**Triggers**: Daily schedule (automatic) OR Webhook (for testing)

### Test Steps (Webhook Method)

1. **Send Test Receipt Email:**
   - Send email to `sway@oloxa.ai` or `swayclarkeii@gmail.com`
   - Subject: "Your receipt from [Store Name]"
   - Attach a receipt PDF OR embed in email body (for Apple emails)
   - Include total amount in email body

2. **Trigger Workflow:**
   - In n8n, open W2 workflow
   - Click "Execute Workflow" button
   - Or use webhook URL to trigger remotely

3. **Monitor Execution:**
   - Expected execution time: 60-90 seconds (includes OCR)
   - Watch for Vision API OCR step

### Test Steps (Schedule Method)

1. **Send Test Email:**
   - Send receipt email as above
   - Wait for scheduled execution (daily at configured time)

2. **Check Execution Log:**
   - Next day, check n8n executions
   - Look for W2 execution

### Success Criteria

**✅ Email Processing:**
- Gmail node retrieves email successfully
- Email parsed for attachments
- Apple Store emails converted to PDF (if applicable)

**✅ File Upload:**
- Receipt uploaded to "Receipt Pool" folder in Google Drive
- Filename format: `[Date]_[Store]_[Amount].pdf`

**✅ OCR Processing:**
- Vision API extracts text from receipt
- Amount extracted correctly (within $0.01 accuracy)
- OCR confidence score > 0.8

**✅ Data Validation:**
- New row in "Receipts" sheet with:
  - `ReceiptID` (unique UUID)
  - `ReceiptDate` (from email or OCR)
  - `Store/Vendor` (from email subject)
  - `Amount` (from OCR)
  - `FilePath` (Google Drive link)
  - `Source` (Gmail account email)

**✅ Duplicate Prevention:**
- If same email processed twice, no duplicate rows created
- Duplicate detection based on email ID and date

### Common Issues

**Issue**: Vision API fails
- **Check**: Google OAuth2 API credential has Vision scope
- **Check**: Vision API enabled in Google Cloud Console
- **Solution**: Verify credential at https://console.cloud.google.com

**Issue**: Amount not extracted
- **Check**: Receipt image quality (blurry receipts fail OCR)
- **Check**: OCR text contains "$" or "total" keywords
- **Solution**: Use clearer receipt image

**Issue**: Apple email not converted
- **Check**: Email contains HTML body
- **Check**: "Convert to PDF" node has correct parameters
- **Solution**: Verify HTML-to-PDF conversion logic

**Issue**: No emails found
- **Check**: Gmail search query in node (label, date range)
- **Check**: Gmail OAuth2 permission for read access
- **Solution**: Adjust search query or reauthorize Gmail

---

## 🔗 W3: Transaction-Receipt-Invoice Matching

### Test Type: Manual Trigger (No Automatic Execution)

**Trigger**: Manual execution in n8n UI or via API

### Test Prerequisites

**Required Data:**
- At least 5 unmatched expense transactions in "Transactions" sheet
- At least 5 unmatched receipts in "Receipts" sheet
- At least 2 unmatched income transactions in "Transactions" sheet (for invoice matching)
- At least 2 unmatched invoices in "Receipts" sheet

### Test Steps

1. **Verify Unmatched Data:**
   - Open "Transactions" sheet
   - Filter for rows where `ReceiptID` is empty (expenses) or `InvoiceID` is empty (income)
   - Open "Receipts" sheet
   - Filter for rows where `TransactionID` is empty

2. **Execute Workflow:**
   - In n8n, open W3 workflow
   - Click "Execute Workflow" button
   - Expected execution time: 30-45 seconds

3. **Monitor Execution:**
   - Watch fuzzy matching nodes
   - Check confidence scores in execution data

### Success Criteria

**✅ Expense Matching:**
- Code node "Fuzzy Match Expenses to Receipts" returns matches
- Matches have confidence score ≥ 0.7 (default threshold)
- Google Sheets "Transactions" updated with `ReceiptID` for matched expenses
- Google Sheets "Receipts" updated with `TransactionID` for matched expenses

**✅ Income Matching (NEW in v2.1):**
- Code node "Fuzzy Match Income to Invoices" returns matches
- Matches have confidence score ≥ 0.7
- Google Sheets "Transactions" updated with `InvoiceID` for matched income
- Google Sheets "Receipts" updated with `TransactionID` for matched invoices

**✅ Fuzzy Logic Validation:**
- Transactions matched by:
  - Similar dates (within 7 days)
  - Similar amounts (within $5 or 10%)
  - Similar vendor/description (Levenshtein distance)
- High confidence matches (≥0.9) are near-exact
- Medium confidence matches (0.7-0.89) are probable
- Low confidence matches (<0.7) are ignored

**✅ Data Integrity:**
- No duplicate matches (one transaction → one receipt only)
- No overwrites of existing matches
- Original data preserved

### Common Issues

**Issue**: No matches found
- **Check**: Date ranges overlap between transactions and receipts
- **Check**: Amounts are within fuzzy match tolerance
- **Solution**: Adjust confidence threshold or date range

**Issue**: Wrong matches
- **Check**: Confidence scores (should be ≥0.7)
- **Check**: Date differences (should be <7 days)
- **Solution**: Increase confidence threshold to 0.8 or 0.9

**Issue**: Google Sheets not updated
- **Check**: Execution completed without errors
- **Check**: Update nodes have correct sheet names and ranges
- **Solution**: Verify Google Sheets OAuth2 credential

---

## 📁 W4: Monthly Folder Builder & Organizer

### Test Type: Webhook Trigger

**Trigger**: Webhook (manual or automated)

### Test Prerequisites

**Required Data:**
- At least 3 files in "Receipt Pool" folder with `FilePath` populated in Sheets
- At least 2 statements with `FilePath` populated in Sheets
- Files dated within current or previous month

### Test Steps

1. **Trigger Workflow:**
   - In n8n, open W4 workflow
   - Click "Test Workflow" or use webhook URL
   - Expected execution time: 45-60 seconds

2. **Specify Month (Optional):**
   - Default: Current month
   - Override: Pass `month` parameter in webhook JSON (e.g., `{"month": "2026-01"}`)

3. **Monitor Execution:**
   - Watch folder creation nodes
   - Check file move operations
   - Verify no 404 errors on empty FilePath (filter fix in v2.1)

### Success Criteria

**✅ Folder Structure Created:**
- New folder in Google Drive: `[YYYY-MM] VAT Folder/`
- Subfolders:
  - `Receipts/`
  - `Statements/`
  - `Invoices/`

**✅ File Organization:**
- Files moved from "Receipt Pool" to appropriate monthly subfolder
- Statements moved to `Statements/` subfolder
- Receipts moved to `Receipts/` subfolder
- Invoices moved to `Invoices/` subfolder

**✅ Google Sheets Updates:**
- "Receipts" sheet: `FilePath` updated with new folder location
- "Statements" sheet: `FilePath` updated with new folder location
- Old file paths replaced with new monthly folder paths

**✅ Filter Logic (v2.1 Fix):**
- Empty `FilePath` values do NOT cause 404 errors
- Filter nodes skip empty paths correctly
- Only valid file paths processed

**✅ Data Integrity:**
- No files lost during move
- No duplicate files created
- Original file metadata preserved

### Common Issues

**Issue**: Folder already exists error
- **Check**: Monthly folder created in previous run
- **Solution**: This is expected behavior; workflow should skip folder creation if exists

**Issue**: Files not moved
- **Check**: `FilePath` column populated in Sheets
- **Check**: Google Drive permission to move files
- **Solution**: Verify OAuth2 credential has Drive write access

**Issue**: 404 errors on empty FilePath
- **Check**: W4 is v2.1 (filter fix applied)
- **Solution**: If still occurring, verify filter nodes use correct string operators (not `isEmpty`)

**Issue**: Sheets not updated
- **Check**: "Map Automatically" mode is enabled in Update nodes
- **Check**: Column names match ("ReceiptID", "StatementID")
- **Solution**: Verify screenshots from v2.1 validation

---

## 📄 W6: Expensify PDF Parser

### Test Type: Google Drive Trigger Test

**Trigger**: Upload new Expensify PDF to Google Drive

### Test Prerequisites

**Required Data:**
- Expensify expense report PDF with transaction table
- PDF should contain:
  - Header with date range
  - Table with columns: Date, Merchant, Amount, Category
  - At least 5 transactions

### Test Steps

1. **Prepare Test File:**
   - Export expense report from Expensify as PDF
   - Ensure PDF has readable table (not scanned image)

2. **Upload to Google Drive:**
   - Navigate to "Expensify PDFs" folder in Google Drive
   - Upload the PDF
   - File should trigger W6 automatically

3. **Monitor Execution:**
   - Expected execution time: 45-60 seconds (depends on PDF size)
   - Watch Claude Sonnet 4.5 API call
   - Check Merge node (race condition fix in v1.1)

### Success Criteria

**✅ PDF Parsing:**
- Claude Sonnet 4.5 extracts table data
- JSON response contains transactions array
- Each transaction has: date, merchant, amount, category

**✅ Race Condition Prevention (v1.1 Fix):**
- Merge node uses `mode: "append"` (not `mergeByPosition`)
- Parallel branches merge correctly
- No data loss or corruption

**✅ Transaction Creation:**
- New rows in "Transactions" sheet with:
  - `TransactionID` (unique UUID)
  - `Date`, `Description` (merchant), `Amount`, `Type`
  - `Source` (Expensify)

**✅ Receipt Creation:**
- New rows in "Receipts" sheet with:
  - `ReceiptID` (unique UUID)
  - `Store/Vendor` (merchant)
  - `Amount`
  - `FilePath` (Google Drive link to Expensify PDF)

**✅ Data Integrity:**
- Number of transactions matches PDF table row count
- All amounts match PDF (within $0.01)
- No duplicate transactions

### Common Issues

**Issue**: Table not extracted
- **Check**: PDF has readable table (not scanned image)
- **Check**: Claude API key valid and has quota
- **Solution**: Use higher quality PDF export from Expensify

**Issue**: Race condition errors
- **Check**: W6 is v1.1 (Merge node fix applied)
- **Check**: Merge node has `mode: "append"`
- **Solution**: Verify Merge node configuration

**Issue**: Missing transactions
- **Check**: Claude API response contains all rows
- **Check**: Merge node successfully combines branches
- **Solution**: Check execution data for each branch

**Issue**: Duplicate receipts
- **Check**: Duplicate detection logic in Code node
- **Solution**: Verify ReceiptID generation uses unique PDF identifier

---

## 🔍 End-to-End Integration Test

### Test Full System Flow

This test validates the complete expense system from bank statement to organized folder.

### Test Steps

1. **Day 1: Upload Bank Statement (W1)**
   - Upload bank statement PDF to Google Drive
   - Verify transactions extracted to Sheets

2. **Day 2: Send Receipt Emails (W2)**
   - Send 3-5 receipt emails to Gmail accounts
   - Wait for W2 scheduled execution
   - Verify receipts uploaded to Receipt Pool and logged in Sheets

3. **Day 3: Upload Expensify Report (W6)**
   - Upload Expensify PDF to Google Drive
   - Verify transactions and receipts created in Sheets

4. **Day 4: Match Transactions (W3)**
   - Manually execute W3
   - Verify receipts matched to transactions
   - Check confidence scores

5. **Day 5: Organize Files (W4)**
   - Trigger W4 via webhook
   - Verify monthly folder created
   - Verify files moved from Receipt Pool to organized folders
   - Verify Sheets updated with new file paths

### Success Criteria

**✅ Data Completeness:**
- All bank transactions logged
- All receipts uploaded and logged
- All Expensify transactions and receipts created

**✅ Matching Success:**
- At least 70% of transactions matched to receipts
- No duplicate matches
- High confidence scores (≥0.8 average)

**✅ Organization:**
- All files in monthly VAT folders
- No files left in Receipt Pool
- All file paths updated in Sheets

**✅ Data Integrity:**
- No data loss across workflows
- All IDs unique
- All relationships valid (TransactionID → ReceiptID)

---

## 📊 Performance Benchmarks

### Expected Execution Times

| Workflow | Avg Time | Max Time | Factors |
|----------|----------|----------|---------|
| W1 | 45s | 90s | PDF size, transaction count |
| W2 | 60s | 120s | OCR processing, attachment size |
| W3 | 30s | 60s | Number of unmatched transactions |
| W4 | 45s | 90s | Number of files to move |
| W6 | 50s | 90s | PDF size, table complexity |

### API Quota Usage

**Google APIs (per execution):**
- Gmail API: 1-5 read requests (W2)
- Drive API: 2-10 write requests (W1, W2, W4, W6)
- Sheets API: 5-20 write requests (all workflows)
- Vision API: 1-3 OCR requests (W2)

**Daily Limits (default):**
- Gmail: 1 billion requests/day (no concern)
- Drive: 1 billion requests/day (no concern)
- Sheets: 500 requests/100 seconds/user (monitor if high volume)
- Vision: 1800 requests/minute (monitor if high volume)

**Anthropic Claude API:**
- W1: ~2,000 tokens/execution (PDF parsing)
- W6: ~3,000 tokens/execution (table extraction)

---

## 🐛 Troubleshooting Guide

### General Issues

**Workflow Won't Execute:**
1. Check workflow is active (if trigger-based)
2. Verify trigger configuration (folder ID, webhook URL, schedule)
3. Check OAuth2 credentials not expired
4. Review n8n logs for errors

**Execution Fails Mid-Workflow:**
1. Check which node failed (red X in execution view)
2. Read error message in node output
3. Verify node parameters (folder ID, sheet name, etc.)
4. Check API quota not exceeded

**Data Not Appearing in Sheets:**
1. Verify Google Sheets OAuth2 credential
2. Check sheet names match exactly (case-sensitive)
3. Confirm sheet has correct column headers
4. Verify Update nodes use "Map Automatically" mode

**Files Not Moving/Uploading:**
1. Check Google Drive OAuth2 credential
2. Verify folder IDs are correct
3. Confirm file permissions allow move/write
4. Check Drive storage quota not exceeded

### OAuth2 Token Expired

**Symptoms:**
- Error: "invalid_grant" or "Token has been expired or revoked"
- Workflows fail at Google API calls

**Solution:**
1. Go to n8n Credentials settings
2. Find expired credential
3. Click "Reconnect" or "Refresh Token"
4. Follow OAuth2 flow to reauthorize

### Vision API Errors

**Error: "Permission denied"**
- **Check**: Google OAuth2 API credential has Vision scope
- **Solution**: Add scope `https://www.googleapis.com/auth/cloud-vision`

**Error: "Quota exceeded"**
- **Check**: Vision API quota in Google Cloud Console
- **Solution**: Increase quota or wait for reset

### Claude API Errors

**Error: "API key invalid"**
- **Solution**: Update Anthropic API key in n8n credentials

**Error: "Rate limit exceeded"**
- **Solution**: Wait 60 seconds, Claude API has rate limits

---

## 📝 Test Tracking Template

Use this template to track your test runs:

```markdown
## Test Run: [Date]

**Tester**: [Your Name]
**Workflows Tested**: W1, W2, W3, W4, W6

### W1 Results
- [ ] Execution completed without errors
- [ ] Transactions extracted correctly
- [ ] Data logged in Sheets
- **Notes**: [Any observations]

### W2 Results
- [ ] Email processed successfully
- [ ] OCR extracted amount correctly
- [ ] Receipt uploaded to Drive
- [ ] Data logged in Sheets
- **Notes**: [Any observations]

### W3 Results
- [ ] Matches found with confidence ≥0.7
- [ ] Sheets updated with ReceiptID/InvoiceID
- [ ] No duplicate matches
- **Notes**: [Any observations]

### W4 Results
- [ ] Monthly folder created
- [ ] Files moved successfully
- [ ] Sheets updated with new paths
- [ ] No 404 errors on empty paths
- **Notes**: [Any observations]

### W6 Results
- [ ] PDF table extracted
- [ ] Transactions created in Sheets
- [ ] Receipts created in Sheets
- [ ] Merge node worked correctly
- **Notes**: [Any observations]

### Integration Test Results
- [ ] Complete flow tested (W1 → W2 → W6 → W3 → W4)
- [ ] Data integrity maintained
- [ ] Files organized correctly
- **Notes**: [Any observations]

### Issues Found
1. [Issue description]
   - Workflow: [W#]
   - Severity: [Critical/High/Medium/Low]
   - Resolution: [How it was fixed]

### Next Steps
- [ ] [Action item]
```

---

## 🎯 Quality Assurance Checklist

Before marking a workflow as "production ready", verify:

### Code Quality
- [ ] No console.log statements left in Code nodes
- [ ] Error handling implemented in critical nodes
- [ ] Comments added to complex logic
- [ ] No hardcoded values (use variables/env)

### Data Quality
- [ ] All required fields populated in Sheets
- [ ] UUIDs are unique (no duplicates)
- [ ] Dates in correct format (YYYY-MM-DD)
- [ ] Amounts have 2 decimal places

### Security
- [ ] No API keys in workflow JSON
- [ ] OAuth2 credentials properly scoped
- [ ] No sensitive data in logs
- [ ] File permissions correct (not public)

### Performance
- [ ] Execution time within benchmarks
- [ ] API quota usage acceptable
- [ ] No unnecessary API calls
- [ ] Efficient data processing (no loops on large datasets)

### Documentation
- [ ] Workflow description updated
- [ ] Node names descriptive
- [ ] Critical nodes have notes
- [ ] Version documented in workflow settings

---

## 📚 Additional Resources

**n8n Documentation:**
- Workflows: https://docs.n8n.io/workflows/
- Nodes: https://docs.n8n.io/integrations/builtin/
- Error handling: https://docs.n8n.io/workflows/error-handling/

**Google API Documentation:**
- Gmail: https://developers.google.com/gmail/api
- Drive: https://developers.google.com/drive/api
- Sheets: https://developers.google.com/sheets/api
- Vision: https://cloud.google.com/vision/docs

**Claude API Documentation:**
- Anthropic API: https://docs.anthropic.com/claude/reference

**Internal Documentation:**
- Build summary: `build_summary_v2.1_2026-01-10.md`
- Configuration: `configuration-summary_v1.0_2026-01-09.md`
- Deployment summary: `/Users/swayclarke/coding_stuff/EXPENSE_SYSTEM_COMPLETE.md`

---

**Version**: 1.0
**Last Updated**: 2026-01-10
**Maintained By**: Sway Clarke
**Status**: ✅ Current
