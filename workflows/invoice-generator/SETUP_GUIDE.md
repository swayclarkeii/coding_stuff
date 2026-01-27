# Setup Guide - Invoice Generator Workflow

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] n8n instance running (cloud or self-hosted)
- [ ] Notion workspace with two databases:
  - [ ] Invoice Database (ID: `2f41c288bb28814aa434e23b9c714d3c`)
  - [ ] Client Database (ID: `2f41c288bb28810e8fcec0c9b125b789`)
- [ ] Google Slides template (ID: `1g2P1xP7eS1qMSat1N-OBx42SdkzoZ1d45MV3Z65rCvE`)
- [ ] Google account with Drive and Slides access
- [ ] Admin access to your n8n instance

## Step-by-Step Setup

### Phase 1: Verify Notion Databases (10 minutes)

#### 1.1 Check Invoice Database Structure

Open your Notion Invoice database and verify these fields exist:

| Field Name | Type | Required | Notes |
|------------|------|----------|-------|
| Project Name | Title | Yes | Main identifier |
| Client | Relation | Yes | Links to Client database |
| Product | Select | No | Product/service category |
| Price | Number | Yes | Invoice amount (EUR) |
| P1 Description | Text | Yes | Service description |
| Due Date | Date | Yes | Payment deadline |
| MwSt Amount | Number | No | VAT percentage (for reference) |

**Action Items:**
- [ ] Verify all required fields exist
- [ ] Check that "Client" relation points to Client database
- [ ] Ensure "Price" is formatted as number (not currency text)
- [ ] Confirm "Due Date" is a date field (not text)

#### 1.2 Check Client Database Structure

Open your Notion Client database and verify these fields exist:

| Field Name | Type | Required | Notes |
|------------|------|----------|-------|
| Client Name | Title | Yes | Company/person name |
| Client Address | Text | Yes | Full billing address |
| Client Email | Email | Yes | Billing contact email |

**Action Items:**
- [ ] Verify all three fields exist
- [ ] Check "Client Email" is Email type (not Text)
- [ ] Ensure all active clients have complete data

#### 1.3 Create Test Data

Create a test invoice to verify the workflow:

```
Test Invoice:
- Project Name: "Test Invoice - Website Dev"
- Client: Link to test client
- Price: 1000
- P1 Description: "Website development services"
- Due Date: [30 days from today]

Test Client:
- Client Name: "Test Company GmbH"
- Client Address: "Teststraße 123\n10115 Berlin\nGermany"
- Client Email: "test@example.com"
```

**Action Items:**
- [ ] Create test client record
- [ ] Create test invoice record
- [ ] Link invoice to client
- [ ] Copy invoice page ID (you'll need this for testing)

### Phase 2: Verify Google Slides Template (5 minutes)

#### 2.1 Check Template Access

1. Open template URL: https://docs.google.com/presentation/d/1g2P1xP7eS1qMSat1N-OBx42SdkzoZ1d45MV3Z65rCvE/edit
2. Verify you can view/edit the template
3. If you can't access it, create your own template or request access

**Action Items:**
- [ ] Confirm template opens
- [ ] Verify you have edit access
- [ ] Note the template ID from the URL

#### 2.2 Verify Template Placeholders

Your template must contain these exact text strings (case-sensitive):

```
{{invoice_number}}
{{date}}
{{due_date}}
{{client_name}}
{{client_address}}
{{client_email}}
{{project_description}}
{{price}}
{{quantity}}
{{total}}
{{subtotal}}
{{vat}}
{{final_amount}}
```

**How to Check:**
1. Open template in Google Slides
2. Use Ctrl+F (or Cmd+F) to search for "{{invoice_number}}"
3. Verify it appears somewhere in the slides
4. Repeat for all 13 variables

**Action Items:**
- [ ] Search for each variable in template
- [ ] Make note of any missing variables
- [ ] Add missing variables to template if needed

**Template Design Tips:**
- Use `{{variable}}` in text boxes, not in table cells (for easier replacement)
- Place financial values in tables for better formatting
- Include currency symbols (€) next to amount placeholders
- Format placeholder text clearly (e.g., bold or colored)

### Phase 3: Configure n8n Credentials (15 minutes)

#### 3.1 Add Notion OAuth Credential

1. In n8n, go to **Settings** → **Credentials**
2. Click **Add Credential**
3. Search for "Notion" and select **Notion OAuth2 API**
4. Click **Connect my account**
5. Follow OAuth flow to authorize n8n
6. Select which Notion pages/databases n8n can access
7. Grant access to both Invoice and Client databases
8. Save credential with name: "Notion - Invoice System"

**Troubleshooting:**
- If OAuth fails, check your Notion integration permissions
- Ensure you're logged into the correct Notion workspace
- Verify the integration has access to both databases

**Action Items:**
- [ ] Create Notion OAuth credential
- [ ] Test connection
- [ ] Verify access to both databases

#### 3.2 Add Google Drive OAuth Credential

1. In n8n, go to **Settings** → **Credentials**
2. Click **Add Credential**
3. Search for "Google Drive" and select **Google Drive OAuth2 API**
4. Click **Connect my account**
5. Authorize n8n to access your Google Drive
6. Grant permissions:
   - ✅ View files in Google Drive
   - ✅ Create and edit files
7. Save credential with name: "Google Drive - Main Account"

**Required Scopes:**
```
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/drive.file
```

**Action Items:**
- [ ] Create Google Drive OAuth credential
- [ ] Grant full Drive access
- [ ] Test connection

#### 3.3 Add Google Slides OAuth Credential

1. In n8n, go to **Settings** → **Credentials**
2. Click **Add Credential**
3. Search for "Google Slides" and select **Google Slides OAuth2 API**
4. Click **Connect my account**
5. Authorize n8n to access your Google Slides
6. Grant permissions:
   - ✅ View presentations
   - ✅ Edit presentations
7. Save credential with name: "Google Slides - Main Account"

**Required Scopes:**
```
https://www.googleapis.com/auth/presentations
https://www.googleapis.com/auth/drive.readonly
```

**Action Items:**
- [ ] Create Google Slides OAuth credential
- [ ] Grant presentations access
- [ ] Test connection

### Phase 4: Configure Workflow in n8n (20 minutes)

#### 4.1 Open Workflow

1. Go to n8n workflows: `https://[your-n8n-url]/workflows`
2. Find workflow: "Invoice Generator - Notion to Google Slides"
3. Workflow ID: `LY9HfV4xNZoQhA80`
4. Click to open

**If workflow isn't visible:**
- Check workflow isn't archived
- Verify you're logged into correct n8n instance
- Confirm workflow was successfully created (check workflow list)

**Action Items:**
- [ ] Open workflow in n8n editor
- [ ] Verify all 7 nodes are visible
- [ ] Check connections between nodes are intact

#### 4.2 Configure Node Credentials

Go through each node and assign the appropriate credential:

**Node 1: Manual Trigger**
- No credentials needed
- [ ] Verify node is active

**Node 2: Get Invoice from Notion**
1. Click the node
2. In "Credentials" dropdown, select: "Notion - Invoice System"
3. Verify "Resource" = "Database Page"
4. Verify "Operation" = "Get"
5. In "Page ID" field, you'll enter the invoice ID when running
   - For now, leave it as expression: `={{ $json.invoice_page_id }}`

**Action Items:**
- [ ] Assign Notion credential
- [ ] Verify operation is "Get"
- [ ] Leave Page ID as expression

**Node 3: Get Client Details**
1. Click the node
2. In "Credentials" dropdown, select: "Notion - Invoice System" (same as Node 2)
3. Verify "Resource" = "Database Page"
4. Verify "Operation" = "Get"
5. Check "Page ID" expression: `={{ $json.properties.Client.relation[0].id }}`
   - This pulls the Client ID from the previous node
   - Don't modify this expression

**Action Items:**
- [ ] Assign Notion credential
- [ ] Verify Page ID expression is correct
- [ ] Don't change the expression

**Node 4: Generate Invoice Number**
- No credentials needed
- This is a Code node with JavaScript
- [ ] Click node to verify code is present
- [ ] Don't modify code unless changing invoice number format

**Node 5: Calculate Totals**
- No credentials needed
- This is a Code node with JavaScript
- [ ] Click node to verify code is present
- [ ] Verify VAT calculation is 0.19 (19%)
- [ ] Verify date format function exists

**Node 6: Copy Google Slides Template**
1. Click the node
2. In "Credentials" dropdown, select: "Google Drive - Main Account"
3. Verify "Resource" = "File"
4. Verify "Operation" = "Copy"
5. Check "File ID" = `1g2P1xP7eS1qMSat1N-OBx42SdkzoZ1d45MV3Z65rCvE`
   - This is your template ID
   - Change if you're using a different template
6. Check "Drive" = "My Drive"
7. Check "Folder" = "root" (or change to organize invoices)
8. Check "Name" = `Invoice {{ $json.invoice_number }}`

**Action Items:**
- [ ] Assign Google Drive credential
- [ ] Verify template ID is correct
- [ ] Adjust folder if needed
- [ ] Keep name expression as-is

**Node 7: Replace Variables in Slides**
1. Click the node
2. In "Credentials" dropdown, select: "Google Slides - Main Account"
3. Verify "Resource" = "Presentation"
4. Verify "Operation" = "Replace Text"
5. Check "Presentation ID" = `={{ $json.id }}`
   - This gets the new presentation ID from previous node
   - Don't change this
6. Verify all 13 text replacements are configured
   - Each should have "Search For" and "Replace With" values
   - "Search For" should be literal text (e.g., "{{invoice_number}}")
   - "Replace With" should be expressions (e.g., `={{ $('Calculate Totals').first().json.invoice_number }}`)

**Action Items:**
- [ ] Assign Google Slides credential
- [ ] Verify Presentation ID expression
- [ ] Count 13 replacement rules
- [ ] Don't modify replacement logic

#### 4.3 Add Workflow Input Parameter

The workflow needs an input parameter for the invoice page ID:

1. Click the **Manual Trigger** node
2. In the node settings, look for "Form Fields" or "Parameters"
3. Add a new parameter:
   - **Name:** `invoice_page_id`
   - **Type:** String
   - **Required:** Yes
   - **Description:** "Notion invoice page ID to process"

**Action Items:**
- [ ] Add `invoice_page_id` parameter to trigger
- [ ] Set as required
- [ ] Set type to String

### Phase 5: Test the Workflow (15 minutes)

#### 5.1 Prepare Test Data

1. Copy your test invoice page ID from Notion:
   - Open the test invoice in Notion
   - Copy URL: `https://notion.so/workspace/PAGE_ID?v=...`
   - Extract the 32-character page ID
   - Example: `2f41c288bb28814aa434e23b9c714d3c`

**Action Items:**
- [ ] Copy test invoice page ID
- [ ] Verify it's 32 characters
- [ ] Have it ready to paste

#### 5.2 Run Test Execution

1. In n8n workflow editor, click **"Execute Workflow"** button (top right)
2. A popup will appear asking for `invoice_page_id`
3. Paste your test invoice page ID
4. Click **"Execute"**
5. Watch the workflow run:
   - Each node will light up as it executes
   - Green = success
   - Red = error
6. Check the output of each node:
   - Click node to see input/output data
   - Verify data is flowing correctly

**What to Watch For:**
- **Node 2 (Get Invoice):** Should output invoice properties
- **Node 3 (Get Client):** Should output client properties
- **Node 4 (Generate Number):** Should show "INV-2026-XXX"
- **Node 5 (Calculate Totals):** Should show all 13 fields
- **Node 6 (Copy Template):** Should return new presentation ID
- **Node 7 (Replace Text):** Should show 13 replacements made

**Action Items:**
- [ ] Execute workflow with test data
- [ ] Verify all nodes turn green
- [ ] Check output data at each step
- [ ] Note the new presentation ID

#### 5.3 Verify Output

1. Go to Google Drive: https://drive.google.com
2. Look for new presentation: "Invoice INV-2026-XXX"
3. Open the presentation
4. Check all variables were replaced:
   - No `{{variable}}` placeholders should remain
   - All values should be actual data from Notion
   - Dates should be DD.MM.YYYY format
   - Currency values should have 2 decimals

**Quality Checks:**
- [ ] Invoice number is formatted correctly (INV-YYYY-NNN)
- [ ] Current date is today's date in DD.MM.YYYY format
- [ ] Due date matches Notion due date
- [ ] Client name is correct
- [ ] Client address is complete
- [ ] Client email is correct
- [ ] Project description is present
- [ ] Price is formatted with 2 decimals
- [ ] Quantity is 1
- [ ] Total = price × 1
- [ ] Subtotal = total
- [ ] VAT = subtotal × 0.19 (19%)
- [ ] Final amount = subtotal + VAT

#### 5.4 Test Edge Cases

Run additional tests with different scenarios:

**Test 2: Different Client**
- Create invoice for different client
- Verify client data updates correctly

**Test 3: Different Price**
- Create invoice with different price (e.g., €5,000)
- Verify VAT calculation: €5,000 × 0.19 = €950
- Verify final amount: €5,000 + €950 = €5,950

**Test 4: Future Due Date**
- Create invoice with due date 30 days in future
- Verify due date formats correctly

**Action Items:**
- [ ] Run 3+ test executions
- [ ] Test with different clients
- [ ] Test with different prices
- [ ] Test with different due dates
- [ ] Verify calculations are always correct

### Phase 6: Activate for Production (5 minutes)

#### 6.1 Final Pre-Production Checks

Before using with real invoices:

- [ ] All test invoices generated successfully
- [ ] All 13 variables replace correctly every time
- [ ] VAT calculations are accurate
- [ ] Date formats are correct (DD.MM.YYYY)
- [ ] Currency formats have 2 decimals
- [ ] Invoice numbers are unique
- [ ] Generated invoices look professional
- [ ] No template placeholders remain

#### 6.2 Activate Workflow

1. In n8n workflow editor, look for "Active" toggle (top right)
2. Switch from "Inactive" to **"Active"**
3. Workflow is now ready for production use

**Action Items:**
- [ ] Toggle workflow to Active
- [ ] Verify it shows as active in workflow list

#### 6.3 Document Your Process

Create a quick reference guide for your team:

```markdown
# How to Generate Invoice

1. Create invoice in Notion
2. Link to client in Client field
3. Fill in: Price, Description, Due Date
4. Copy invoice page ID from URL
5. Go to n8n workflow
6. Click "Execute Workflow"
7. Paste invoice page ID
8. Click Execute
9. Find invoice in Google Drive
10. Review and send to client
```

**Action Items:**
- [ ] Create internal documentation
- [ ] Share with team members who will use this
- [ ] Include workflow ID: `LY9HfV4xNZoQhA80`

## Troubleshooting Guide

### Problem: "Notion database not found"

**Cause:** Credential doesn't have access to database

**Solution:**
1. Go to Notion integration settings
2. Add Invoice and Client databases to integration
3. Reconnect credential in n8n
4. Test again

### Problem: "Client relation is empty"

**Cause:** Invoice doesn't have Client linked

**Solution:**
1. Open invoice in Notion
2. Click Client field
3. Select a client from dropdown
4. Save and try again

### Problem: "Template ID not found"

**Cause:** Wrong template ID or no access

**Solution:**
1. Open template in Google Slides
2. Copy correct ID from URL
3. Update "Copy Google Slides Template" node
4. Ensure Google account has view access to template

### Problem: "Variables not replaced"

**Cause:** Template doesn't have placeholders

**Solution:**
1. Open Google Slides template
2. Add missing `{{variable}}` placeholders
3. Ensure exact spelling (case-sensitive)
4. Include double curly braces
5. Run workflow again

### Problem: "Invoice number not sequential"

**Cause:** Timestamp-based generation

**Solution:**
- This is by design (simple implementation)
- For true sequential numbers:
  1. Create Google Sheet "Invoice Registry"
  2. Add column "Last Invoice Number"
  3. Modify "Generate Invoice Number" code node to:
     - Read from sheet
     - Increment number
     - Write back to sheet

### Problem: "VAT calculation wrong"

**Cause:** Code error or wrong VAT rate

**Solution:**
1. Open "Calculate Totals" Code node
2. Check line: `const vat = subtotal * 0.19;`
3. Verify 0.19 is correct for your country
4. Adjust if needed (e.g., 0.20 for 20% VAT)

### Problem: "Date format incorrect"

**Cause:** Wrong date formatting in code

**Solution:**
1. Open "Calculate Totals" Code node
2. Find `formatDate` function
3. Check format string: `${day}.${month}.${year}`
4. Adjust for your preferred format
5. Examples:
   - US: `${month}/${day}/${year}`
   - ISO: `${year}-${month}-${day}`

### Problem: "Workflow doesn't run"

**Cause:** Workflow not active or credentials invalid

**Solution:**
1. Check workflow is "Active" (toggle in top right)
2. Verify all credentials are connected and valid
3. Check n8n console for error messages
4. Try re-authenticating credentials

## Next Steps

Now that setup is complete:

1. **Generate Your First Real Invoice**
   - Use actual client and invoice data
   - Verify output quality
   - Send to client or export as PDF

2. **Consider Enhancements**
   - Add email sending step
   - Implement sequential invoice numbering
   - Add folder organization by client/month
   - Create automated trigger

3. **Monitor Usage**
   - Track successful executions
   - Note any recurring issues
   - Collect feedback from users

4. **Maintain System**
   - Update VAT rates if they change
   - Refresh OAuth tokens as needed
   - Keep template design updated

## Support Resources

- **n8n Documentation:** https://docs.n8n.io
- **Notion API Docs:** https://developers.notion.com
- **Google Slides API:** https://developers.google.com/slides
- **Workflow ID:** `LY9HfV4xNZoQhA80`

---

**Setup guide created:** 2026-01-26
**Estimated setup time:** 70 minutes
**Difficulty level:** Intermediate
