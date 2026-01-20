# Testing Preparation Guide

**Project**: Sway's Expense System
**Purpose**: Pre-testing configuration checklist and validation criteria
**Last Updated**: December 30, 2025

---

## 🎯 Testing Overview

### Testing Phases
1. **Phase 1**: Individual workflow testing (Workflows 1, 2, 3 separately)
2. **Phase 2**: End-to-end integration testing (all workflows together)
3. **Phase 3**: Real data processing (actual bank statements and receipts)

### Current Status
- **Workflows Built**: 3 of 4 core workflows (Workflows 1, 2, 3)
- **Tested**: None (all workflows are untested)
- **Ready for Testing**: ⚠️ No - configuration required first

---

## ⚙️ Configuration Requirements

### 1. Environment Variables (n8n)

**Required for Workflow 1** (PDF Intake & Parsing):
```bash
BANK_STATEMENTS_FOLDER_ID="<Google Drive folder ID>"
# Location: Expenses-System/_Inbox/Bank-Statements/
# How to get: Open folder → Copy ID from URL

ARCHIVE_STATEMENTS_FOLDER_ID="<Google Drive folder ID>"
# Location: Expenses-System/_Archive/Statements/
# How to get: Open folder → Copy ID from URL
```

**Required for Workflow 2** (Gmail Receipt Monitor):
```bash
RECEIPT_POOL_FOLDER_ID="<Google Drive folder ID>"
# Location: Expenses-System/_Receipt-Pool/
# How to get: Open folder → Copy ID from URL
```

**How to Set Environment Variables in n8n**:
1. Navigate to: Settings → Environments
2. Click "Add Variable"
3. Name: `BANK_STATEMENTS_FOLDER_ID`
4. Value: Paste folder ID
5. Click "Save"
6. Repeat for each variable

**Verification**:
```javascript
// Test in n8n Code node:
return {
  json: {
    bankStatementsId: $env.BANK_STATEMENTS_FOLDER_ID,
    archiveId: $env.ARCHIVE_STATEMENTS_FOLDER_ID,
    receiptPoolId: $env.RECEIPT_POOL_FOLDER_ID
  }
};
// All three should show IDs, not undefined
```

### 2. API Credentials

**OpenAI API** (for Workflow 1):
- **Required**: Yes
- **Used for**: PDF parsing with GPT-4 Vision
- **Configuration**:
  1. Get API key from: https://platform.openai.com/api-keys
  2. In n8n: Settings → Credentials → Add Credential
  3. Select: "OpenAI API"
  4. Name: "OpenAI - Expense System"
  5. API Key: Paste key
  6. Click "Save"
- **Cost Estimate**: ~€0.50-€1.00 per bank statement (4-8 pages)
- **Test First**: Use a single-page test PDF to verify before processing full statements

**Gmail API** (for Workflow 2):
- **Required**: Yes
- **Used for**: Searching emails and downloading attachments
- **Configuration**:
  1. In n8n: Settings → Credentials → Add Credential
  2. Select: "Gmail OAuth2"
  3. Follow OAuth flow to authorize
  4. Scopes needed: `gmail.readonly`, `gmail.modify`
- **Multi-Account Note**: Need separate credentials for each Gmail account
  - Primary account: "Gmail - Primary (sway@oloxa.ai)"
  - Secondary account: "Gmail - Secondary (??@gmail.com)" [waiting for account info]

**Google Drive API** (all workflows):
- **Required**: Yes
- **Used for**: File uploads, downloads, folder creation
- **Configuration**:
  1. In n8n: Settings → Credentials → Add Credential
  2. Select: "Google Drive OAuth2"
  3. Follow OAuth flow to authorize
  4. Scopes needed: `drive.file`, `drive`
- **Already Configured**: Likely yes (used to create folder structure)

**Google Sheets API** (all workflows):
- **Required**: Yes
- **Used for**: Reading/writing transaction database
- **Configuration**:
  1. In n8n: Settings → Credentials → Add Credential
  2. Select: "Google Sheets OAuth2"
  3. Follow OAuth flow to authorize
  4. Scopes needed: `spreadsheets`
- **Already Configured**: Yes (used to populate VendorMappings)

---

## 📋 Test Data Preparation

### Workflow 1: PDF Statement Parser

**What You Need**:
1. **1 Sample Bank Statement PDF**
   - **Preferred**: Recent ING or Deutsche Bank statement (German format)
   - **Requirements**:
     - PDF format (not scanned image)
     - Contains transactions in table format
     - Shows: Date, Description, Amount, Balance
     - German date format (DD.MM.YYYY)
   - **Size**: Ideally 1-2 pages for initial test
   - **Location**: Upload to `Expenses-System/_Inbox/Bank-Statements/`

2. **Expected Validation**:
   - After upload, workflow should trigger automatically
   - OpenAI should extract all transactions
   - Transactions should appear in Expense-Database → Transactions sheet
   - PDF should move to `_Archive/Statements/`

**Test Checklist**:
- [ ] Sample PDF uploaded to correct folder
- [ ] OpenAI API key configured and working
- [ ] Workflow triggered (check n8n execution history)
- [ ] Transactions extracted with correct data:
  - [ ] TransactionID format: `STMT-{bank}-{yearmonth}-{timestamp}-001`
  - [ ] Date in DD.MM.YYYY format
  - [ ] Amount as negative for expenses, positive for income
  - [ ] Vendor parsed correctly
  - [ ] Bank name extracted from filename
- [ ] PDF moved to Archive folder
- [ ] Statement logged in Statements sheet

**Known Risks**:
- German PDF parsing may require prompt tuning
- Some banks use different table formats
- Scanned PDFs may not work (need OCR first)

### Workflow 2: Gmail Receipt Monitor

**What You Need**:
1. **Gmail Account Access**
   - Primary account email address
   - OAuth authorization completed
   - At least 1 receipt email from monitored vendors in last 7 days

2. **Vendor Receipt Verification**:
   - **OpenAI**: Receipt from noreply@openai.com with PDF attachment
   - **Anthropic**: Receipt from billing@anthropic.com with PDF attachment
   - **AWS**: Receipt from aws-billing@amazon.com with PDF attachment
   - **Google Cloud**: Receipt from billing-noreply@google.com with PDF attachment
   - **GitHub**: Receipt from billing@github.com with PDF attachment
   - **Oura Ring**: Receipt from hello@ouraring.com with PDF attachment
   - **Apple**: Receipt from any of 3 Apple email addresses with PDF attachment

3. **Manual Search Test First**:
   ```
   In Gmail, search:
   from:noreply@openai.com has:attachment after:2024/12/23

   Expected: Should find recent receipt emails
   If not: Vendor may not be sending receipts, or email pattern is wrong
   ```

**Test Checklist**:
- [ ] Gmail API credentials configured
- [ ] Manual Gmail search confirms receipts exist
- [ ] Workflow execution triggered (or run manually first time)
- [ ] Gmail search finds receipt emails (check n8n logs)
- [ ] Attachments downloaded successfully
- [ ] Files uploaded to `_Receipt-Pool/` folder
- [ ] Receipt records logged in Receipts sheet with:
  - [ ] ReceiptID format: `RCPT-{VENDOR}-{timestamp}`
  - [ ] Vendor name matches
  - [ ] Date extracted from email
  - [ ] FileID stored correctly
  - [ ] Matched status = "unmatched"

**Known Limitations**:
- Only searches last 7 days (prevent duplicates)
- Max 10 emails per vendor per run
- Amount field left empty (requires receipt parsing)
- Single Gmail account only (multi-account not implemented yet)

### Workflow 3: Transaction-Receipt Matching

**What You Need**:
1. **Prerequisites**:
   - At least 1 transaction in Transactions sheet (from Workflow 1)
   - At least 1 receipt in Receipts sheet (from Workflow 2)
   - Both with status "unmatched"

2. **Ideal Test Scenario**:
   - Transaction: €19.99 on 2024-12-15 from "PAYPAL*OPENAI"
   - Receipt: OpenAI invoice dated 2024-12-15 for €19.99
   - **Expected**: Perfect match (confidence 1.0)

3. **Edge Case Test Scenarios**:
   - **Date +1 day**: Transaction 12-15, Receipt 12-16 (should match with 0.95 confidence)
   - **Amount ±€0.50**: Transaction €20.00, Receipt €19.99 (should match with 0.9 confidence)
   - **Date +4 days**: Transaction 12-15, Receipt 12-19 (should NOT match - outside ±3 day range)

**Test Checklist**:
- [ ] At least 2 unmatched transactions exist
- [ ] At least 2 unmatched receipts exist
- [ ] Workflow executes without errors
- [ ] Matches found and logged (check n8n execution output)
- [ ] Transaction sheet updated:
  - [ ] ReceiptID field populated
  - [ ] MatchStatus changed to "matched"
  - [ ] MatchConfidence between 0.70-1.00
- [ ] Receipt sheet updated:
  - [ ] Matched field changed to "matched"
- [ ] Receipt file moved to correct folder:
  - [ ] Path: `Expenses-System/{Year}/{Month}/{Bank}/Receipts/`
  - [ ] Example: `Expenses-System/2024/12-December/ING/Receipts/`

**Known Limitations**:
- Only matches if confidence ≥ 0.7 (70%)
- One receipt can only match one transaction (no 1-to-many)
- Vendor matching is exact string match (case-insensitive)
- German date parsing required (DD.MM.YYYY)

---

## 🧪 Testing Sequence

### Pre-Testing Validation

**Before testing any workflow, verify**:
```bash
# 1. Check n8n is accessible
curl https://n8n.oloxa.ai/healthz

# 2. Verify Google Drive folders exist
# Open: https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15
# Confirm: _Inbox, _Receipt-Pool, _Archive folders exist

# 3. Verify Transaction Database accessible
# Open: https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM/edit
# Confirm: Transactions, Receipts, Statements, VendorMappings sheets exist

# 4. Check workflow exists in n8n
# Navigate to: https://n8n.oloxa.ai/workflows
# Confirm: All 3 workflows visible with correct IDs
```

### Testing Order (Recommended)

**Step 1: Test Workflow 2 First (Gmail Receipt Monitor)**
- **Why**: Least risky, no API costs, easy to verify
- **Duration**: ~5 minutes
- **Success Criteria**: At least 1 receipt downloaded to Receipt Pool

**Step 2: Test Workflow 3 (Transaction-Receipt Matching)**
- **Why**: Uses data from Workflow 2, no API costs
- **Duration**: ~5 minutes
- **Success Criteria**: At least 1 transaction matched to receipt

**Step 3: Test Workflow 1 Last (PDF Statement Parser)**
- **Why**: Uses OpenAI API (costs money), most complex
- **Duration**: ~10 minutes
- **Success Criteria**: All transactions extracted from test PDF

**Step 4: End-to-End Test**
- **Scenario**: Upload 1 bank statement PDF → Wait for processing → Verify full workflow chain
- **Expected Timeline**:
  - T+0min: Upload PDF to _Inbox
  - T+1min: Workflow 1 triggers, parses PDF, writes transactions
  - T+2min: Manual trigger Workflow 2 to download receipts (or wait 24h for daily trigger)
  - T+3min: Manual trigger Workflow 3 to match transactions
  - T+4min: Verify receipts moved to organized folders
- **Success Criteria**: 80%+ of transactions matched to receipts

---

## ✅ Success Criteria by Workflow

### Workflow 1: PDF Statement Parser
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Parsing accuracy | 95%+ | Manual count: transactions in PDF vs database |
| Transaction ID format | 100% correct | Check TransactionID column matches pattern |
| Date format | 100% DD.MM.YYYY | No ISO dates in database |
| Vendor extraction | 80%+ | Vendor column populated (not "Unknown") |
| File archiving | 100% | PDF moved from _Inbox to _Archive |
| Database logging | 100% | Statement record in Statements sheet |

### Workflow 2: Gmail Receipt Monitor
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Email search success | 100% | All vendor searches return results (if emails exist) |
| Attachment download | 100% | All found emails have attachments downloaded |
| File upload | 100% | All attachments uploaded to Receipt Pool |
| Receipt ID format | 100% correct | Check ReceiptID column matches pattern |
| Database logging | 100% | All receipts logged in Receipts sheet |
| Vendor identification | 100% | Vendor column populated correctly |

### Workflow 3: Transaction-Receipt Matching
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Match accuracy | 90%+ | Manual verification of matches |
| False positives | <5% | Check MatchConfidence <0.8 for incorrectly matched |
| File organization | 100% | All matched receipts moved to correct year/month/bank folder |
| Database updates | 100% | Both Transactions and Receipts sheets updated |
| Unmatched handling | 100% | Transactions without receipts remain "unmatched" |

---

## 🚨 Troubleshooting Guide

### Common Issues

**Issue**: Workflow 1 doesn't trigger after PDF upload
- **Check**: Is workflow Active in n8n?
- **Check**: Is PDF in correct folder (`_Inbox/Bank-Statements/`)?
- **Check**: Is Google Drive Trigger configured with correct folder ID?
- **Fix**: Manually trigger workflow using "Test workflow" button in n8n

**Issue**: OpenAI API returns error "Invalid API key"
- **Check**: Is API key configured in n8n credentials?
- **Check**: Does API key have sufficient credits?
- **Fix**: Regenerate API key at https://platform.openai.com/api-keys

**Issue**: Gmail search returns 0 results
- **Check**: Are there actually receipt emails in last 7 days?
- **Check**: Is email pattern correct (test manually in Gmail)?
- **Check**: Is Gmail API authorized with correct scopes?
- **Fix**: Manually search Gmail with same query to verify emails exist

**Issue**: Transactions not matching to receipts
- **Check**: Are dates within ±3 days range?
- **Check**: Are amounts exact or within ±€0.50?
- **Check**: Do transactions have "unmatched" status?
- **Fix**: Lower confidence threshold from 0.7 to 0.6 for testing

**Issue**: Receipt file not moving to organized folder
- **Check**: Does target folder exist (e.g., `2024/12-December/ING/Receipts/`)?
- **Check**: Is Google Drive API authorized?
- **Check**: Check n8n execution logs for error messages
- **Fix**: Create missing folders manually first, or update Workflow 3 to create folders automatically

---

## 📊 Testing Results Template

Use this template to document testing outcomes:

```markdown
## Workflow 1 Testing Results
**Date**: YYYY-MM-DD
**Tester**: Sway Clarke
**Test Data**: [PDF filename]

### Results:
- [ ] Workflow triggered successfully
- [ ] Transactions extracted: X of Y (success rate: %)
- [ ] PDF archived successfully
- [ ] Database updated correctly

### Issues Found:
1. [Issue description]
2. [Issue description]

### Next Steps:
- [ ] Fix issue #1
- [ ] Re-test with different PDF
- [ ] Proceed to Workflow 2 testing
```

---

## 🎯 Next Steps After Configuration

Once all configuration is complete:

1. **Start with Workflow 2 testing** (lowest risk, fastest validation)
2. **Document any issues** in GitHub/Notion
3. **Iterate on vendor patterns** based on test results
4. **Expand to Workflow 1** once confident in system
5. **Complete end-to-end test** with real monthly data
6. **Update VERSION_LOG.md** with test results and any bug fixes

---

## 📞 Support Resources

- **System Design**: [SYSTEM_DESIGN.md](SYSTEM_DESIGN.md)
- **Version History**: [VERSION_LOG.md](VERSION_LOG.md)
- **Vendor Analysis**: [VENDOR_RECEIPT_ANALYSIS.md](VENDOR_RECEIPT_ANALYSIS.md)
- **n8n Documentation**: https://docs.n8n.io
- **OpenAI API Docs**: https://platform.openai.com/docs

---

**Last Updated**: December 30, 2025
**Status**: Configuration Required - Not Ready for Testing
