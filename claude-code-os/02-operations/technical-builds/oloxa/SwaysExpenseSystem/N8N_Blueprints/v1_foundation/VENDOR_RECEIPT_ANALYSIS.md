# Vendor Receipt Analysis & Email Strategy

**Project**: Sway's Expense System
**Purpose**: Categorize vendors by receipt delivery method and email account strategy
**Last Updated**: December 30, 2025

---

## 📧 Multiple Gmail Accounts Strategy

### Current Setup
You have **3 Gmail accounts** where vendor receipts may arrive:

1. **Primary Account**: swayclarkeii@gmail.com (main)
2. **Secondary Account**: swayfromthehook@gmail.com
3. **Tertiary Account**: sway@oloxa.ai (fewer emails)

**Strategy**: Monitor primary and secondary accounts. Test to determine which has more vendor receipts.

### Recommended Approach: Multi-Account Monitoring

**Implementation:**
```
Workflow 2 (Gmail Receipt Monitor) will be configured to:
1. Connect to Gmail Account 1 (primary) - nodes 3-9
2. Connect to Gmail Account 2 (secondary) - duplicate nodes 3-9
3. Connect to Gmail Account 3 (optional) - duplicate nodes 3-9
4. Merge all results before receipt processing
```

**Configuration Steps:**
1. In n8n, create separate Gmail OAuth2 credentials for each account:
   - `Gmail - Primary (swayclarkeii@gmail.com)`
   - `Gmail - Secondary (swayfromthehook@gmail.com)`
   - `Gmail - Tertiary (sway@oloxa.ai)` (if needed - fewer emails)

2. Duplicate the Gmail search/download nodes in Workflow 2
3. Assign each set of nodes to different credentials
4. Use a "Merge" node to combine results from all accounts

**Pros:**
- ✅ No emails missed due to forwarding failures
- ✅ Each account maintains independent permissions
- ✅ Easy to add/remove accounts
- ✅ Can track which account received which receipt

**Cons:**
- ❌ Requires separate Gmail API credentials per account
- ❌ More complex initial setup
- ❌ Slightly longer execution time (sequential searches)

### Alternative: Email Forwarding (NOT Recommended)

**Setup:**
- Create forwarding rules in Accounts 2 & 3 → Account 1
- Filter: `from:(*@email.apple.com OR *billing*.com OR *invoice*.com) has:attachment`
- Monitor only Account 1 in Workflow 2

**Why Not Recommended:**
- ⚠️ Gmail forwarding can fail silently
- ⚠️ Some emails may be caught in spam filters
- ⚠️ Forwarding adds delay (receipts arrive hours later)
- ⚠️ Forwarded emails lose original metadata (affects matching)

---

## 🏢 Vendor Receipt Delivery Methods

### Category 1: Email Receipts (Gmail Monitoring ✅)

These vendors send receipts automatically via email. **Workflow 2 handles these.**

| Vendor | Email Pattern | Gmail Search | Account | Notes |
|--------|---------------|--------------|---------|-------|
| **OpenAI** | from:noreply@openai.com | ✅ Active | Primary | Monthly subscription |
| **Anthropic** | from:billing@anthropic.com | ✅ Active | Primary | Usage-based billing |
| **AWS** | from:aws-billing@amazon.com | ✅ Active | Primary | Monthly invoice |
| **Google Cloud** | from:billing-noreply@google.com | ✅ Active | Primary | Monthly invoice |
| **GitHub** | from:billing@github.com | ✅ Active | Primary | Monthly/annual subscription |
| **Oura Ring** | from:hello@ouraring.com | ✅ Active | Primary | Monthly subscription |
| **Apple** | from:do_not_reply@email.apple.com | ✅ Active | Primary | App Store, iCloud, Music |
| Apple (alt) | from:no_reply@email.apple.com | ✅ Active | Primary | Subscription renewals |
| Apple (alt) | from:appleid@id.apple.com | ✅ Active | Primary | Account notifications |

**To Add:**
| Vendor | Email Pattern | Account | Billing Frequency | Notes |
|--------|---------------|---------|-------------------|-------|
| **Namecheap** | from:*@namecheap.com | TBD | Annual | Domain registrar |
| **Soho** | from:*@soho.com | TBD | TBD | Email service |
| **Microsoft 365** | from:*@microsoft.com | TBD | Annual (January) | Office subscription |

**Not Needed:**
| Vendor | Reason |
|--------|--------|
| **Insurance companies** | Statements not required for accountant |
| **Rent** | Receipts not required for accountant |

### Category 2: Portal Downloads Only (Manual Workflow ⚠️)

These vendors **DO NOT email receipts** (or only send email notifications without actual invoices). You must log into their website to download.

| Vendor | Portal URL | Frequency | Notes |
|--------|-----------|-----------|-------|
| **Amazon.de** | amazon.de/your-orders | Per purchase | Shared account. Has Audible subscription (monthly). Need to download order receipts manually |
| **GEMA** | gema.de/portal | Quarterly | Sends email notification but not actual invoice. Manual portal download required |
| **Vodafone** | vodafone.de | Monthly | Sends email notification but not actual invoice. Portal login required |
| **O2** | o2online.de | Monthly | Sends email notification but not actual invoice. Portal login required |
| **Telekom** | telekom.de | Monthly | Sends email notification but not actual invoice. Portal login required |

**Recommended Actions:**
1. **Amazon.de**: Install browser extension "Amazon Order History Reporter" to auto-download receipts, or implement monthly manual download workflow
2. **GEMA**: Set up quarterly reminder workflow (already planned in edge cases)
3. **Vodafone/O2/Telekom**: Consider browser automation or monthly manual download workflow
4. **Future**: May implement automated portal download workflows using Playwright/Puppeteer

### Category 3: Physical Receipts (Expensify 📱)

These are captured via Expensify mobile app:

| Source | Method | Integration |
|--------|--------|-------------|
| **Edeka** | Photo scan | Expensify → Manual export to Google Drive |
| **DM** | Photo scan | Expensify → Manual export to Google Drive |
| **Restaurants** | Photo scan | Expensify → Manual export to Google Drive |
| **Cash expenses** | Manual entry | Expensify → Manual export to Google Drive |

**Current Process:**
1. Take photo in Expensify app
2. Expensify extracts vendor, amount, date
3. Export monthly as CSV
4. Upload to `_Inbox/Expensify-Exports/`
5. **Future Workflow 4** will process these

### Category 4: Unknown / Need Investigation

| Vendor | Type | Action Needed |
|--------|------|---------------|
| Bank fees | Auto-deducted | Check if ING/Deutsche Bank email fee notices |
| ATM withdrawals | Cash | No receipt needed (tagged automatically) |
| Currency conversion fees | Auto-deducted | Check if bank emails summaries |

---

## 🔍 Discovery Process: Finding All Your Vendors

### Step 1: Analyze Bank Statements (Past 3 Months)

**Run this query after Workflow 1 processes your statements:**

```sql
-- In Google Sheets Transactions tab, create filter:
1. Select all data
2. Filter by "Description" column
3. Look for recurring patterns
4. Group by unique vendor names
```

**Expected Output:**
```
Vendor Pattern | Frequency | Last Amount | Category Guess
PAYPAL*OPENAI  | Monthly   | €20.00      | AI Services
ANTHROPIC      | Monthly   | €45.00      | AI Services
AMAZON.DE      | Weekly    | Various     | Shopping
EDEKA SCHECK   | Weekly    | €20-50      | Groceries
...
```

### Step 2: Search Gmail for Receipt Patterns

**Run these searches in each Gmail account:**

1. **Invoices & Receipts:**
   ```
   subject:(invoice OR receipt OR payment OR subscription)
   has:attachment
   after:2024/10/01
   ```

2. **Billing Notifications:**
   ```
   from:(*billing* OR *invoice* OR *payment*)
   has:attachment
   after:2024/10/01
   ```

3. **Specific Vendors:**
   ```
   from:(*apple.com OR *github.com OR *aws.amazon.com)
   has:attachment
   after:2024/10/01
   ```

**Document Results:**
```
Email From | Subject Pattern | Attachment Type | Frequency
do_not_reply@email.apple.com | Your receipt from Apple | PDF | Monthly
billing@github.com | GitHub Payment Receipt | PDF | Monthly
...
```

### Step 3: Cross-Reference

**Create a mapping table:**

```
Bank Transaction → Email Receipt Match
PAYPAL*OPENAI €20.00 → noreply@openai.com "OpenAI Invoice" ✅
ANTHROPIC €45.00 → billing@anthropic.com "Anthropic Invoice" ✅
AMAZON.DE €34.99 → ❌ NO EMAIL (portal only)
EDEKA €22.50 → ❌ NO EMAIL (Expensify photo)
```

---

## 📋 Action Plan for You

### Immediate Actions (Before Testing)

1. **Identify Your Gmail Accounts:**
   - [ ] List all Gmail addresses where receipts arrive
   - [ ] Decide which is "primary" for monitoring
   - [ ] Note which vendors send to which account

2. **Gmail Account Audit (Per Account):**
   - [ ] Run the search queries above
   - [ ] Export results to spreadsheet
   - [ ] Count how many receipts each vendor sent in last 3 months

3. **Vendor Categorization:**
   - [ ] Mark vendors as "Email" vs "Portal" vs "Expensify"
   - [ ] Document portal URLs for manual download vendors
   - [ ] Check if phone/internet providers email invoices

4. **Update VendorMappings Sheet:**
   - [ ] Add all discovered email-based vendors
   - [ ] Include email patterns for each
   - [ ] Categorize by expense type

### Questions Answered ✅

**Email Accounts:**
1. ✅ **Gmail addresses**:
   - Primary: swayclarkeii@gmail.com (main)
   - Secondary: swayfromthehook@gmail.com
   - Tertiary: sway@oloxa.ai (fewer emails)
2. ⏳ **Which account has most receipts**: Need to test to determine
3. ⏳ **Vendor distribution**: Will be discovered during testing

**Vendors Categorized:**
1. ✅ **Phone/Internet**: Vodafone/O2/Telekom send email notifications but NOT actual invoices - portal login required
2. ✅ **Insurance**: Not needed for accountant
3. ✅ **Rent**: Not needed for accountant
4. ✅ **Domains**: Namecheap - need to add email pattern to monitoring
5. ✅ **Other subscriptions**: Soho (email), Microsoft 365 (yearly in January)

**Amazon Receipts:**
1. ✅ **Shared account** with Audible subscription (monthly)
2. ✅ **Portal download only** - receipts not sent by email
3. ⏳ **Download strategy**: Manual monthly download or browser extension TBD

---

## 🛠️ Technical Implementation

### Workflow 2 Multi-Account Update (v1.2.1)

**Current Structure:**
```
Daily Receipt Check → Load Vendor Patterns → Search Gmail (Account 1) → ...
```

**Updated Structure (Multi-Account):**
```
Daily Receipt Check → Load Vendor Patterns
  ├→ Search Gmail Account 1 → Get Details → Extract Attachments
  ├→ Search Gmail Account 2 → Get Details → Extract Attachments
  └→ Search Gmail Account 3 → Get Details → Extract Attachments
       ↓
  Merge Results → Download Attachment → Upload to Receipt Pool → ...
```

**Node Changes:**
- **Add**: "Search Gmail Account 2" node (duplicate of existing)
- **Add**: "Get Email Details Account 2" node
- **Add**: "Extract Attachment Info Account 2" node
- **Add**: "Merge" node to combine all results
- **Update**: Credentials for each account's nodes

### Environment Variables Needed

```bash
# Gmail Account Configuration
GMAIL_ACCOUNT_1_NAME="Primary (swayclarkeii@gmail.com)"
GMAIL_ACCOUNT_2_NAME="Secondary (swayfromthehook@gmail.com)"
GMAIL_ACCOUNT_3_NAME="Tertiary (sway@oloxa.ai)" # Optional - fewer emails

# Folder IDs (already defined)
RECEIPT_POOL_FOLDER_ID="..."
BANK_STATEMENTS_FOLDER_ID="..."
ARCHIVE_STATEMENTS_FOLDER_ID="..."
```

---

## 📊 Vendor Discovery Template

Use this template to document your findings:

```markdown
## My Vendor Receipt Audit

### Email Receipts (Workflow 2)
- [ ] OpenAI - noreply@openai.com - Primary Account - $20/month
- [ ] Anthropic - billing@anthropic.com - Primary Account - $45/month
- [ ] AWS - aws-billing@amazon.com - Primary Account - Variable
- [ ] Google Cloud - billing-noreply@google.com - Primary Account - Variable
- [ ] GitHub - billing@github.com - Primary Account - $4/month
- [ ] Oura Ring - hello@ouraring.com - Primary Account - $6/month
- [ ] Apple - do_not_reply@email.apple.com - Primary Account - Variable
- [ ] ??? - Add more as discovered

### Portal Downloads (Manual)
- [ ] Amazon.de - amazon.de/your-orders - Weekly - ~€100/month
- [ ] GEMA - gema.de/portal - Quarterly - Variable
- [ ] ??? - Add more as discovered

### Expensify Photos
- [ ] Edeka - N/A - Weekly - ~€50/week
- [ ] DM - N/A - Weekly - ~€20/week
- [ ] ??? - Add more as discovered

### Need to Investigate
- [ ] Vodafone/O2 - Do they email invoices?
- [ ] Insurance - Which company? Email or portal?
- [ ] Rent - Email or mail?
- [ ] ??? - Other vendors to check
```

---

## 🎯 Next Steps After Analysis

1. **Update Workflow 2** with multi-account support
2. **Add discovered vendors** to VendorMappings sheet
3. **Configure Gmail credentials** for all accounts
4. **Test searches** manually in Gmail first
5. **Run Workflow 2** and verify receipt downloads
6. **Iterate** on vendor patterns as needed

---

## 📋 Current Status

**Gmail Accounts Identified**: 3 accounts
- ✅ Primary: swayclarkeii@gmail.com
- ✅ Secondary: swayfromthehook@gmail.com
- ✅ Tertiary: sway@oloxa.ai

**Email Vendors Currently Monitored**: 7 vendors
- OpenAI, Anthropic, AWS, Google Cloud, GitHub, Oura Ring, Apple

**Email Vendors To Add**: 3 vendors
- Namecheap, Soho, Microsoft 365

**Portal-Only Vendors**: 5 vendors
- Amazon, GEMA, Vodafone, O2, Telekom

**Next Steps**:
1. Test Workflow 2 with current 7 vendors on primary account
2. Determine which Gmail account receives which vendor receipts
3. Add Namecheap, Soho, Microsoft 365 email patterns
4. Implement multi-account monitoring (primary + secondary)
5. Plan manual workflows for portal-only vendors
