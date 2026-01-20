# Environment Setup Guide

**Project**: Sway's Expense System
**Purpose**: API credential setup for n8n workflows
**Last Updated**: December 30, 2025

---

## ⚠️ IMPORTANT NOTE: Free n8n Version

**Environment variables are NOT available in the free self-hosted n8n version.**

✅ **Folder IDs are already hardcoded in your workflows:**
- Workflow 1 monitors: `_Inbox/Bank-Statements/` (ID: `1stmB5nWmoViQKKuQqpkWICPrfPQ_GDN1`)
- Workflow 1 archives to: `_Archive/Statements/` (ID: `1uohhbtaE6qvS08awMEYdVP6BqgRLxgjH`)
- Workflow 2 stores to: `_Receipt-Pool/` (ID: `12SVQzuWtKva48LvdGbszg3UcKl7iy-1x`)

**This guide now focuses on API credential setup only.**

---

## 🎯 ~~Required Environment Variables~~ (Not Applicable for Free Version)

### Summary Table

| Variable Name | Used By | Purpose | Status |
|--------------|---------|---------|--------|
| `BANK_STATEMENTS_FOLDER_ID` | Workflow 1 | Monitor inbox for PDF uploads | ⏳ Not set |
| `ARCHIVE_STATEMENTS_FOLDER_ID` | Workflow 1 | Move processed PDFs to archive | ⏳ Not set |
| `RECEIPT_POOL_FOLDER_ID` | Workflow 2 | Store downloaded receipts | ⏳ Not set |

---

## 📋 Step-by-Step Setup

### Step 1: Get Google Drive Folder IDs

**How to find a folder ID**:
1. Open Google Drive: https://drive.google.com
2. Navigate to the folder you need
3. Look at the URL in your browser
4. Copy the ID from the URL

**URL Format**:
```
https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15
                                         ↑
                                    This is the folder ID
```

### Step 2: Locate Your Expense System Folders

**Root Folder** (for reference):
- **URL**: https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15
- **ID**: `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15`
- **Name**: Expenses-System

**Navigate to each subfolder and copy its ID**:

1. **Bank Statements Inbox**:
   - Path: `Expenses-System/_Inbox/Bank-Statements/`
   - URL: [Click into folder and copy URL]
   - Variable: `BANK_STATEMENTS_FOLDER_ID`

2. **Archive Statements**:
   - Path: `Expenses-System/_Archive/Statements/`
   - URL: [Click into folder and copy URL]
   - Variable: `ARCHIVE_STATEMENTS_FOLDER_ID`

3. **Receipt Pool**:
   - Path: `Expenses-System/_Receipt-Pool/`
   - URL: [Click into folder and copy URL]
   - Variable: `RECEIPT_POOL_FOLDER_ID`

### Step 3: Set Variables in n8n

**Access n8n Instance**:
- URL: https://n8n.oloxa.ai
- Login with your credentials

**Set Each Variable**:
1. Click on your profile icon (bottom left)
2. Select **"Settings"**
3. Navigate to **"Environments"** tab
4. Click **"Add Variable"** button

**For each variable, enter**:

**Variable 1: Bank Statements Folder**
```
Name: BANK_STATEMENTS_FOLDER_ID
Value: [Paste folder ID from Step 2.1]
Description: Google Drive folder ID for bank statement uploads (optional)
```
Click **"Save"**

**Variable 2: Archive Statements Folder**
```
Name: ARCHIVE_STATEMENTS_FOLDER_ID
Value: [Paste folder ID from Step 2.2]
Description: Google Drive folder ID for processed statement archives (optional)
```
Click **"Save"**

**Variable 3: Receipt Pool Folder**
```
Name: RECEIPT_POOL_FOLDER_ID
Value: [Paste folder ID from Step 2.3]
Description: Google Drive folder ID for downloaded receipts (optional)
```
Click **"Save"**

### Step 4: Verify Configuration

**Test in n8n**:
1. Create a new workflow (temporary test)
2. Add a "Code" node
3. Paste this code:
```javascript
return {
  json: {
    test: "Environment Variables Check",
    bankStatementsId: $env.BANK_STATEMENTS_FOLDER_ID || "NOT SET",
    archiveId: $env.ARCHIVE_STATEMENTS_FOLDER_ID || "NOT SET",
    receiptPoolId: $env.RECEIPT_POOL_FOLDER_ID || "NOT SET",
    allConfigured: (
      $env.BANK_STATEMENTS_FOLDER_ID &&
      $env.ARCHIVE_STATEMENTS_FOLDER_ID &&
      $env.RECEIPT_POOL_FOLDER_ID
    ) ? "YES - Ready to test!" : "NO - Missing variables"
  }
};
```
4. Click **"Test step"**
5. Check output - all three should show folder IDs, not "NOT SET"
6. Delete temporary workflow when done

**Expected Output**:
```json
{
  "test": "Environment Variables Check",
  "bankStatementsId": "1abc...xyz",
  "archiveId": "1def...uvw",
  "receiptPoolId": "1ghi...rst",
  "allConfigured": "YES - Ready to test!"
}
```

---

## 🔐 API Credentials Setup

### OpenAI API (Workflow 1)

**Required for**: PDF statement parsing

**Setup Steps**:
1. Get API key:
   - Visit: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Name: "Expense System - n8n"
   - Copy the key (shown once!)

2. Add to n8n:
   - In n8n: Settings → Credentials
   - Click "Add Credential"
   - Search for: "OpenAI API"
   - Enter:
     - Name: `OpenAI - Expense System`
     - API Key: [Paste key from step 1]
   - Click "Save"

3. Verify:
   - In Workflow 1, check node "Parse PDF with OpenAI Vision"
   - Credential dropdown should show: "OpenAI - Expense System"

**Cost Estimate**: €0.50-€1.00 per bank statement (4-8 pages)

### Gmail OAuth2 (Workflow 2)

**Required for**: Searching emails and downloading attachments

**Setup Steps**:
1. In n8n: Settings → Credentials
2. Click "Add Credential"
3. Search for: "Gmail OAuth2"
4. Enter:
   - Name: `Gmail - Primary (sway@oloxa.ai)`
   - Click "Connect my account"
5. Follow Google OAuth flow:
   - Select Google account
   - Grant permissions:
     - ✅ Read, compose, and send emails
     - ✅ Manage drafts and send emails
   - Click "Allow"
6. Return to n8n, click "Save"

**Multi-Account Setup** (if needed):
- Repeat steps above for each Gmail account
- Use descriptive names:
  - `Gmail - Primary (sway@oloxa.ai)`
  - `Gmail - Secondary (personal@gmail.com)`
  - `Gmail - Tertiary (other@gmail.com)`

### Google Drive OAuth2 (All Workflows)

**Required for**: File uploads, downloads, folder operations

**Likely Already Configured** (used to create folder structure)

**Verify**:
1. In n8n: Settings → Credentials
2. Search for existing: "Google Drive"
3. Should see credential like: "Google Drive - Expense System"

**If Not Configured**:
1. Settings → Credentials → Add Credential
2. Search for: "Google Drive OAuth2"
3. Follow OAuth flow similar to Gmail above

### Google Sheets OAuth2 (All Workflows)

**Required for**: Reading/writing transaction database

**Likely Already Configured** (used to populate VendorMappings)

**Verify**:
1. In n8n: Settings → Credentials
2. Search for existing: "Google Sheets"
3. Should see credential like: "Google Sheets - Expense System"

**If Not Configured**:
1. Settings → Credentials → Add Credential
2. Search for: "Google Sheets OAuth2"
3. Follow OAuth flow

---

## 🧪 Testing Configuration

**Quick Test Checklist**:

**Environment Variables**:
- [ ] All 3 variables set in n8n
- [ ] Code node test shows all IDs (not "NOT SET")
- [ ] No typos in variable names (exact match required)

**API Credentials**:
- [ ] OpenAI API credential created
- [ ] OpenAI account has sufficient credits ($5+ recommended)
- [ ] Gmail OAuth2 authorized for primary account
- [ ] Google Drive OAuth2 credential exists
- [ ] Google Sheets OAuth2 credential exists

**Workflow Configuration**:
- [ ] Workflow 1: OpenAI credential selected in "Parse PDF" node
- [ ] Workflow 1: Environment variables referenced in trigger node
- [ ] Workflow 2: Gmail credential selected in all Gmail nodes
- [ ] Workflow 2: Environment variable referenced in "Upload to Receipt Pool" node
- [ ] All workflows: Spreadsheet ID matches Transaction Database

---

## 🚨 Troubleshooting

### "Environment variable is undefined"

**Symptom**: Workflow error: `Cannot read property 'BANK_STATEMENTS_FOLDER_ID' of undefined`

**Causes**:
1. Variable not set in n8n
2. Typo in variable name
3. n8n needs restart after adding variables

**Fix**:
1. Double-check variable name spelling (case-sensitive!)
2. In n8n workflow, use: `$env.BANK_STATEMENTS_FOLDER_ID` (not `$BANK_STATEMENTS_FOLDER_ID`)
3. Try: Settings → Restart n8n (if self-hosted)
4. Try: Re-save the variable in Settings → Environments

### "Invalid API key" (OpenAI)

**Symptom**: OpenAI node returns 401 Unauthorized

**Causes**:
1. API key expired or deleted
2. API key not saved in n8n credentials
3. Insufficient credits in OpenAI account

**Fix**:
1. Visit https://platform.openai.com/api-keys
2. Verify key exists and is active
3. Check account balance: https://platform.openai.com/account/billing/overview
4. Regenerate key if needed, update in n8n

### "Insufficient permissions" (Gmail)

**Symptom**: Gmail node returns 403 Forbidden

**Causes**:
1. OAuth scopes not granted correctly
2. Account not authorized
3. Gmail API not enabled in Google Cloud Console

**Fix**:
1. Delete existing Gmail credential in n8n
2. Re-add credential and carefully grant all permissions during OAuth flow
3. If still fails: Check Google Cloud Console for API enablement

### "Folder not found" (Google Drive)

**Symptom**: Google Drive node returns 404 Not Found

**Causes**:
1. Incorrect folder ID
2. Folder was deleted or moved
3. Google Drive credential doesn't have access to folder

**Fix**:
1. Verify folder exists in Google Drive
2. Re-copy folder ID from URL (must be exact)
3. Check that Google account used for OAuth has access to folder
4. If using shared Drive: Ensure credential account has permissions

---

## 📊 Configuration Status

**Current Status**: ⏳ Not Configured

**Checklist**:
```
Environment Variables:
[ ] BANK_STATEMENTS_FOLDER_ID - Not set
[ ] ARCHIVE_STATEMENTS_FOLDER_ID - Not set
[ ] RECEIPT_POOL_FOLDER_ID - Not set

API Credentials:
[ ] OpenAI API - Not configured
[ ] Gmail OAuth2 (Primary) - Not configured
[ ] Gmail OAuth2 (Secondary) - Not needed yet
[ ] Google Drive OAuth2 - Already configured (verify)
[ ] Google Sheets OAuth2 - Already configured (verify)

Ready for Testing:
[ ] All environment variables set
[ ] All API credentials configured
[ ] Test executions successful
[ ] Proceed to TESTING_PREPARATION.md
```

**Once complete, mark**: ✅ Configured - Ready for Testing

---

## 📞 Support Resources

- **Testing Guide**: [TESTING_PREPARATION.md](TESTING_PREPARATION.md)
- **System Design**: [SYSTEM_DESIGN.md](SYSTEM_DESIGN.md)
- **Version History**: [VERSION_LOG.md](VERSION_LOG.md)
- **n8n Environment Docs**: https://docs.n8n.io/environments/
- **n8n Credentials Docs**: https://docs.n8n.io/credentials/

---

**Last Updated**: December 30, 2025
**Status**: Configuration Required
