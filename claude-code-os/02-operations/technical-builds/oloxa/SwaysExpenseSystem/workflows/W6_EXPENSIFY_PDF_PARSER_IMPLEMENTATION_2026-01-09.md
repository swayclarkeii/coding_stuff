# Implementation Complete – W6: Expensify PDF Parser

## 1. Overview
- **Platform:** n8n
- **Workflow ID:** `l5fcp4Qnjn4Hzc8w`
- **Status:** Built (Ready for Configuration & Testing)
- **Files touched:**
  - `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v2_foundations/workflow6_expensify_pdf_parser_v1.0_2026-01-09.json`
  - `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/workflows/W6_EXPENSIFY_PDF_PARSER_IMPLEMENTATION_2026-01-09.md`

---

## 2. Workflow Structure

### Trigger
**Watch Expensify PDFs Folder** (Google Drive Trigger)
- Monitors designated "Expensify PDFs" folder for new uploads
- Event: `fileUpdated` (detects moved/uploaded files)
- Polling: Every minute

### Main Processing Steps

**Phase 1: Transaction Table Extraction**
1. **Download Expensify PDF** – Downloads PDF from Google Drive
2. **Extract Report Metadata** – Parses filename to get report month/date
3. **Build Anthropic Table Request** – Prepares Vision API call with PDF binary
4. **Call Anthropic Table Extraction** – Extracts transaction table from pages 1-2
5. **Parse Transactions to Records** – Converts JSON to individual transaction records
6. **Write Transactions to Sheet** – Saves to Transactions sheet with unique TransactionIDs

**Phase 2: Receipt Metadata Extraction**
7. **Build Receipt Extraction Request** – Prepares second Vision API call
8. **Call Receipt Extraction** – Extracts receipt metadata from pages 3+
9. **Parse Receipt Metadata** – Converts JSON to receipt records
10. **Write Receipts to Sheet** – Saves to Receipts sheet

**Phase 3: Transaction-Receipt Linking**
11. **Match Receipts to Transactions** – Uses Expensify numbering (1, 2, 3...) to link
12. **Update Transactions with ReceiptIDs** – Updates Transactions sheet with ReceiptID and MatchStatus

### Key Data Flow
```
Expensify PDF Upload
  ↓
Transaction Table (pages 1-2) → Anthropic Vision API → Transactions Sheet
  ↓
Receipt Images (pages 3+) → Anthropic Vision API → Receipts Sheet
  ↓
Expensify Numbering → Match Logic → Update Transactions with ReceiptIDs
```

---

## 3. Configuration Notes

### Credentials Required
- **Google Drive OAuth2**: Already configured (`a4m50EefR3DJoU0R`)
- **Google Sheets OAuth2**: Already configured (`a4m50EefR3DJoU0R`)
- **Anthropic API**: `PLACEHOLDER_ANTHROPIC_CREDENTIAL_ID` ← **MUST BE CONFIGURED**

### Folder IDs to Configure
1. **Expensify PDFs Folder**: Create new folder in Google Drive
   - Current value: `PLACEHOLDER_EXPENSIFY_FOLDER_ID`
   - Update in node: "Watch Expensify PDFs Folder"
   - Location: `Expenses-System/_Inbox/Expensify-PDFs/` (recommended)

### Database Configuration
- **Spreadsheet ID**: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` (already configured)
- **Transactions Sheet**: Auto-maps fields, uses `TransactionID` as unique key
- **Receipts Sheet**: Auto-maps fields, uses `ReceiptID` as unique key

### Important Mappings

**Transaction Fields Generated:**
- `TransactionID` → `EXPENSIFY-{reportDate}-TXN-{number}`
- `Date` → Parsed from table (YYYY-MM-DD)
- `Vendor` → Merchant name from table
- `Amount` → Normalized to USD
- `Currency` → Always "USD" (converted if needed)
- `OriginalAmount` → Original amount from Expensify
- `OriginalCurrency` → Original currency (USD or EUR)
- `Category` → Category from Expensify table
- `Type` → Always "expense"
- `Source` → Always "Expensify"
- `ReportID` → Unique report identifier
- `ReceiptID` → Filled after matching (empty initially)
- `ExpensifyNumber` → 1, 2, 3... (for receipt matching)

**Receipt Fields Generated:**
- `ReceiptID` → `EXPENSIFY-{reportDate}-RCP-{number}`
- `Date` → Extracted from receipt image metadata
- `Vendor` → Merchant from receipt
- `Amount` → Total from receipt
- `ExpensifyNumber` → 1, 2, 3... (matches transaction)
- `Source` → Always "Expensify"
- `ReportID` → Same as transaction report ID
- `FilePath` → Empty (placeholder for future image extraction)

---

## 4. Testing

### Pre-Testing Checklist
- [ ] Create "Expensify PDFs" folder in Google Drive
- [ ] Get folder ID and update workflow trigger node
- [ ] Configure Anthropic API credentials in n8n
- [ ] Verify Anthropic API key has Vision API access (Claude Sonnet 4.5)
- [ ] Ensure sample Expensify PDF available (e.g., `SwayClarkeAugExpenseReport20240801[55877].pdf`)
- [ ] Verify Transactions and Receipts sheets have correct column headers

### Happy Path Test

**Input:**
- Upload sample Expensify PDF to "Expensify PDFs" folder
- Example: `SwayClarkeAugExpenseReport20240801[55877].pdf`

**Expected Outcome:**
1. Workflow detects new file within 1 minute
2. Extracts transaction table from pages 1-2:
   - 22 transactions created with unique TransactionIDs
   - All fields populated (Date, Vendor, Amount, Category)
   - Currency normalized to USD (with original preserved)
3. Extracts receipt metadata from pages 3+:
   - 22 receipt records created with unique ReceiptIDs
   - Metadata extracted (date, merchant, amount)
4. Matches receipts to transactions:
   - All 22 transactions updated with ReceiptID
   - MatchStatus set to "MATCHED"
5. Data appears in Google Sheets:
   - Transactions sheet has 22 new rows
   - Receipts sheet has 22 new rows
   - TransactionIDs and ReceiptIDs are linked

**How to Verify:**
1. Check workflow execution log in n8n (should show 13 nodes executed)
2. Open Transactions sheet → verify new entries with Source="Expensify"
3. Open Receipts sheet → verify new entries with Source="Expensify"
4. Verify ReceiptID field is populated in Transactions (not empty)

---

## 5. Edge Cases Handled

### Currency Conversion
- **Scenario**: Expensify report contains EUR transactions
- **Handling**:
  - Converts EUR to USD using placeholder rate (1.1x)
  - Stores original amount and currency in separate fields
  - **User Action Required**: Update conversion rate in "Parse Transactions to Records" node

### Missing Receipts
- **Scenario**: Transaction listed but no receipt image on pages 3+
- **Handling**:
  - Transaction created with empty ReceiptID
  - MatchStatus set to "NO_RECEIPT"
  - Transaction still saved to sheet for manual review

### Duplicate Uploads
- **Risk**: User uploads same Expensify PDF twice
- **Current Behavior**: Creates duplicate transactions
- **Mitigation**: Transactions sheet uses `TransactionID` as unique key
  - Second upload will update existing transactions (not create duplicates)
- **Recommended**: Add duplicate detection logic checking ReportID

### Multi-Page Transaction Tables
- **Scenario**: Transaction table spans more than 2 pages
- **Current Limitation**: Only pages 1-2 processed
- **User Action Required**: Manually extract remaining transactions or update prompt to process all table pages

### Receipt Image Extraction
- **Current Limitation**: Workflow extracts receipt METADATA only (not images)
- **Why**: n8n doesn't have built-in PDF image extraction
- **Future Enhancement**: Add PDF processing library or external service to extract individual receipt images as separate files

---

## 6. Known Limitations

### 1. Receipt Image Files Not Extracted
**What's Missing:**
- Workflow extracts metadata from receipt thumbnails (pages 3+)
- Does NOT extract actual image files
- `FilePath` field in Receipts sheet remains empty

**Why:**
- n8n core doesn't include PDF image extraction library
- Requires external tool (e.g., Python script with PyPDF2/pdf2image)

**Workaround:**
- Keep original Expensify PDF in Google Drive
- Reference by ReportID when receipt image needed

**Future Implementation:**
- Add HTTP Request node calling external PDF processing API
- Or: Use n8n Execute Command node with local PDF tools (if server has ImageMagick/Poppler)

### 2. Currency Conversion Hardcoded
**Current Behavior:**
- EUR to USD conversion uses fixed 1.1x multiplier
- Located in "Parse Transactions to Records" node

**User Action Required:**
- Update conversion rate manually or
- Integrate with live exchange rate API (e.g., Open Exchange Rates)

### 3. No Duplicate Detection
**Risk:**
- Re-uploading same Expensify PDF creates duplicate processing
- Anthropic API charged for duplicate Vision calls

**Mitigation:**
- `appendOrUpdate` mode on Google Sheets prevents duplicate rows
- But still processes twice (wasted API calls)

**Future Enhancement:**
- Add duplicate check node comparing ReportID in sheet before processing

### 4. Validation Warnings
**From n8n validation:**
- 27 warnings (mostly error handling recommendations)
- Nodes lack `onError` properties
- Code nodes can throw unhandled exceptions
- HTTP Request nodes lack retry logic

**Impact:**
- Workflow stops on first error (no graceful handling)
- No automatic retries for transient API failures

**Recommended Next Step:**
- Add error handling after initial testing confirms workflow works

---

## 7. Integration with Existing System

### How W6 Fits with Other Workflows

**Compared to W1 (Bank Statement Parser):**
- W1: Extracts transactions from bank PDFs → Type="income" or "expense"
- W6: Extracts transactions from Expensify → Type="expense" only
- Both: Write to same Transactions sheet
- Both: Use same schema (Date, Vendor, Amount, ReceiptID)

**Compared to W2 (Gmail Receipt Monitor):**
- W2: Monitors Gmail for receipt emails → Stores in `_Receipt-Pool/`
- W6: Extracts receipt metadata from Expensify PDF → Writes to Receipts sheet
- Both: Create entries in Receipts sheet
- Difference: W6 receipts already linked to transactions (via Expensify numbering)

**Compared to W3 (Transaction-Receipt Matching):**
- W3: Matches unmatched transactions to receipts (date ±3 days, amount exact/±€0.50)
- W6: Receipts already matched to transactions (Expensify provides numbering)
- Integration: W3 can skip W6 transactions (already have ReceiptID)
- Enhancement: W3 could verify W6 matches and flag discrepancies

**Data Flow:**
```
W1: Bank PDF → Transactions (ReceiptID=empty, Type=expense/income)
W2: Gmail → Receipts (_Receipt-Pool/)
W3: Match W1 transactions to W2 receipts → Update ReceiptID

W6: Expensify PDF → Transactions (ReceiptID=auto-linked, Type=expense)
                   → Receipts (already linked via ExpensifyNumber)
                   → Skip W3 matching (already complete)
```

### Source Field Usage
- All W6 transactions: `Source="Expensify"`
- All W6 receipts: `Source="Expensify"`
- Use Source field to filter/group by data source in reports

---

## 8. Testing Recommendations

### Phase 1: Basic Functionality
1. **Test with sample PDF** (provided: `SwayClarkeAugExpenseReport20240801[55877].pdf`)
   - Verify 22 transactions extracted
   - Verify 22 receipts extracted
   - Verify all transactions matched (ReceiptID populated)

2. **Validate data quality**
   - Check date formats (YYYY-MM-DD)
   - Check amount parsing (no currency symbols)
   - Check vendor names (no truncation)

### Phase 2: Edge Cases
1. **Test currency conversion**
   - Find Expensify report with EUR transactions
   - Verify conversion applied
   - Verify original currency preserved

2. **Test missing receipts**
   - Find report with fewer receipts than transactions
   - Verify unmatched transactions have empty ReceiptID
   - Verify MatchStatus="NO_RECEIPT"

3. **Test duplicate upload**
   - Upload same PDF twice
   - Verify no duplicate rows in sheet
   - Check Anthropic API costs (should be 2x)

### Phase 3: Error Handling
1. **Test malformed PDF**
   - Upload non-Expensify PDF
   - Verify workflow handles gracefully (doesn't crash)

2. **Test API failure**
   - Disable Anthropic credentials
   - Verify error logged (doesn't halt entire workflow)

---

## 9. Handoff

### What Was Built
- Complete 13-node n8n workflow
- Processes Expensify PDFs from upload to database
- Extracts transactions and receipt metadata
- Auto-links receipts to transactions
- Writes to existing Expense-Database sheets

### What's Configured
- ✅ Google Drive integration (existing credentials)
- ✅ Google Sheets integration (existing credentials)
- ✅ Database sheet IDs (Transactions, Receipts)
- ✅ Field mappings (auto-mapped to sheet headers)

### What Needs Configuration
- ❌ Anthropic API credentials (placeholder ID needs replacement)
- ❌ Expensify PDFs folder ID (user must create folder and update)
- ❌ Currency conversion rate (hardcoded 1.1x needs updating)

### How to Activate
1. **In n8n UI:**
   - Go to workflow ID `l5fcp4Qnjn4Hzc8w`
   - Update placeholder IDs (Anthropic credential, folder ID)
   - Click "Activate" toggle (top-right)

2. **Create trigger folder:**
   ```
   Google Drive: Expenses-System/_Inbox/Expensify-PDFs/
   ```
   - Get folder ID from URL (after `/folders/`)
   - Update "Watch Expensify PDFs Folder" node → `folderToWatch.value`

3. **Configure Anthropic:**
   - In n8n: Settings → Credentials → Add Credential
   - Type: "Anthropic API"
   - Paste API key
   - Note credential ID
   - Update all 3 Anthropic nodes with correct credential ID

### How to Monitor
- **Execution Log**: n8n UI → Executions tab → Filter by workflow
- **Success Indicator**: 13 nodes executed, green checkmarks
- **Data Verification**: Check Transactions and Receipts sheets for new entries
- **Error Indicator**: Red node in execution log, check error message

### How to Modify
**Common Modifications:**

1. **Change polling frequency:**
   - Node: "Watch Expensify PDFs Folder"
   - Parameter: `pollTimes.item[0].mode`
   - Options: `everyMinute`, `everyHour`, `everyDay`

2. **Update currency conversion rate:**
   - Node: "Parse Transactions to Records"
   - Code line: `amountUSD = txn.amount * 1.1;`
   - Change `1.1` to desired rate

3. **Add error handling:**
   - Select any node
   - Settings → "On Error" → Choose behavior
   - Options: `stopWorkflow`, `continueRegularOutput`, `continueErrorOutput`

---

## 10. Suggested Next Steps

### Immediate (Before Production)
1. **Configure Anthropic API** (see Handoff section above)
2. **Create Expensify PDFs folder** and update trigger
3. **Test with sample PDF** (validate end-to-end)
4. **Review currency conversion rate** (update if needed)

### Short-Term Enhancements
1. **Add error handling** to all nodes (use `onError` property)
2. **Add duplicate detection** (check ReportID before processing)
3. **Integrate exchange rate API** (replace hardcoded conversion)
4. **Add notification on completion** (email summary of processed transactions)

### Long-Term Enhancements
1. **Extract receipt image files** (add PDF image extraction)
2. **Upload receipt images to Drive** (populate FilePath field)
3. **Add W3 integration** (verify W6 matches against receipt images)
4. **Create monthly summary report** (Expensify totals by category)

### Optimization Opportunities
1. **Run test-runner-agent** for automated testing
2. **Run workflow-optimizer-agent** if Anthropic costs become concern
3. **Break into sub-workflows** (validation warning about long chain)

---

## 11. Cost Analysis

### Anthropic API Costs (Estimated)

**Per Expensify PDF:**
- Transaction table extraction (pages 1-2): ~2,000 tokens input, ~500 tokens output
- Receipt metadata extraction (pages 3+): ~4,000 tokens input, ~1,000 tokens output
- **Total per PDF**: ~7,500 tokens

**Pricing (Claude Sonnet 4.5):**
- Input: $3.00 per 1M tokens
- Output: $15.00 per 1M tokens
- **Cost per PDF**: ~$0.03

**Monthly Estimate (12 PDFs/year):**
- 12 PDFs × $0.03 = $0.36/year
- **Negligible cost** compared to manual processing time

### Processing Time

**Per Expensify PDF:**
1. Download: ~2 seconds
2. Anthropic Vision API calls: ~15 seconds (2 calls)
3. Data processing: ~5 seconds
4. Google Sheets writes: ~3 seconds
5. **Total**: ~25 seconds per PDF

**Manual Alternative:**
- Reading 22 transactions: 10 minutes
- Typing into spreadsheet: 15 minutes
- Matching receipts: 10 minutes
- **Total**: 35 minutes per PDF

**Time Savings:**
- 35 minutes → 25 seconds = **98.8% time reduction**
- Annual savings: 12 PDFs × 35 min = 7 hours → 5 minutes automated

---

## 12. Validation Results

**n8n Validation Profile:** runtime

**Status:** ✅ Valid (with warnings)

**Summary:**
- Total Nodes: 13
- Enabled Nodes: 13
- Trigger Nodes: 1
- Valid Connections: 13
- Invalid Connections: 0
- Expressions Validated: 3
- Error Count: 0
- Warning Count: 27

**Key Warnings:**
1. Code nodes lack error handling (consider try/catch)
2. HTTP Request nodes lack retry logic (add `retryOnFail: true`)
3. Google Sheets nodes lack `onError` property
4. Outdated typeVersions (4.2 → 4.3, 4.5 → 4.7)
5. Long linear chain (12 nodes, consider sub-workflows)

**Recommendation:**
- Workflow is functional as-is for testing
- Add error handling before production use
- Update typeVersions for latest n8n features

---

## 13. Files & Resources

### Workflow Files
- **Blueprint JSON**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v2_foundations/workflow6_expensify_pdf_parser_v1.0_2026-01-09.json`
- **Implementation Doc**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/workflows/W6_EXPENSIFY_PDF_PARSER_IMPLEMENTATION_2026-01-09.md`

### n8n Resources
- **Workflow ID**: `l5fcp4Qnjn4Hzc8w`
- **Workflow URL**: https://n8n.oloxa.ai/workflow/l5fcp4Qnjn4Hzc8w

### Google Resources
- **Expense Database**: https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM/edit
- **Transactions Sheet**: `Transactions` (spreadsheet above)
- **Receipts Sheet**: `Receipts` (spreadsheet above)
- **Drive Root**: https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15

### Sample Data
- **Test PDF**: `SwayClarkeAugExpenseReport20240801[55877].pdf`
- **Expected Transactions**: 22
- **Expected Receipts**: 22

---

**Implementation Date**: January 9, 2026
**Version**: v1.0
**Status**: Built (Awaiting Configuration & Testing)
**Next Owner**: test-runner-agent (for automated testing) OR workflow-optimizer-agent (if costs scale)

---

## Quick Reference: Configuration Checklist

- [ ] Create "Expensify PDFs" folder in Google Drive
- [ ] Get folder ID and update trigger node
- [ ] Configure Anthropic API credentials in n8n
- [ ] Update Anthropic credential ID in 3 nodes (Build Table Request, Call Table Extraction, Call Receipt Extraction)
- [ ] Review currency conversion rate in "Parse Transactions to Records"
- [ ] Test with sample Expensify PDF
- [ ] Verify data in Transactions and Receipts sheets
- [ ] Activate workflow in n8n
- [ ] Monitor first execution in n8n Executions log
- [ ] Consider adding error handling before production use
