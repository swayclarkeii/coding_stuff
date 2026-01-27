# Implementation Complete – Invoice Generator from Notion to Google Slides

## 1. Overview
- **Platform:** n8n
- **Workflow ID:** `LY9HfV4xNZoQhA80`
- **Status:** Built and ready for configuration
- **Files touched:**
  - `/Users/swayclarke/coding_stuff/workflows/invoice-generator/IMPLEMENTATION_SUMMARY.md` (this file)

## 2. Workflow Structure

### Trigger
- **Manual Trigger** - Requires Notion invoice page ID as input

### Main Steps
1. **Get Invoice from Notion** – Fetches invoice record from Notion database
   - Database ID: `2f41c288bb28814aa434e23b9c714d3c`
   - Retrieves: Project Name, Client (relation), Product, Price, P1 Description, Due Date, MwSt Amount

2. **Get Client Details** – Follows the Client relation to get client information
   - Database ID: `2f41c288bb28810e8fcec0c9b125b789`
   - Retrieves: Client Name, Client Address, Client Email

3. **Generate Invoice Number** – Creates unique invoice ID
   - Format: `INV-YYYY-NNN` (e.g., `INV-2026-001`)
   - Uses timestamp-based sequence (last 3 digits of timestamp)
   - **Note:** For production, consider storing sequence number in Notion or Google Sheets

4. **Calculate Totals** – Computes all financial values
   - Extracts price and description from invoice
   - Hardcodes quantity = 1 (as requested)
   - Calculates: subtotal, VAT (19%), final amount
   - Formats dates to DD.MM.YYYY (European format)
   - Formats currency values to 2 decimal places

5. **Copy Google Slides Template** – Duplicates the template
   - Template ID: `1g2P1xP7eS1qMSat1N-OBx42SdkzoZ1d45MV3Z65rCvE`
   - Creates new presentation named: `Invoice INV-YYYY-NNN`
   - Saves to: My Drive / root folder (can be customized)

6. **Replace Variables in Slides** – Populates the invoice
   - Searches for `{{variable}}` placeholders in the slides
   - Replaces with calculated values from step 4

### Variables Replaced
All 13 variables are replaced in the Google Slides template:

| Variable | Source |
|----------|--------|
| `{{invoice_number}}` | Generated (INV-YYYY-NNN) |
| `{{date}}` | Current date (DD.MM.YYYY) |
| `{{due_date}}` | Notion Due Date field (DD.MM.YYYY) |
| `{{client_name}}` | Client database → Client Name |
| `{{client_address}}` | Client database → Client Address |
| `{{client_email}}` | Client database → Client Email |
| `{{project_description}}` | Notion P1 Description field |
| `{{price}}` | Notion Price field |
| `{{quantity}}` | Hardcoded as 1 |
| `{{total}}` | price × quantity |
| `{{subtotal}}` | Same as total (single product) |
| `{{vat}}` | subtotal × 0.19 (19% MwSt) |
| `{{final_amount}}` | subtotal + vat |

## 3. Configuration Notes

### Credentials Required
You'll need to set up these credentials in n8n:

1. **Notion OAuth** (2 instances needed)
   - For "Get Invoice from Notion" node
   - For "Get Client Details" node
   - Ensure integration has access to both databases

2. **Google Drive OAuth**
   - For "Copy Google Slides Template" node
   - Needs permission to copy files

3. **Google Slides OAuth**
   - For "Replace Variables in Slides" node
   - Needs permission to edit presentations

### Important Mappings

#### Notion Field Mapping
The workflow expects these exact Notion field names:
- **Invoice Database:**
  - `Client` (relation to Client database)
  - `Price` (number field)
  - `P1 Description` (text field)
  - `Due Date` (date field)

- **Client Database:**
  - `Client Name` (title field)
  - `Client Address` (text field)
  - `Client Email` (email field)

#### Google Slides Template Requirements
Your template must contain these exact placeholder strings (including double curly braces):
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

**Important:** The placeholders are case-sensitive and must include the double curly braces `{{` and `}}`.

### Filters / Error Handling
**Current State:** Basic implementation without error handling

**Recommended Additions:**
1. Add error handling to Code nodes (try-catch blocks)
2. Add IF node to check if Client relation exists before fetching
3. Add validation for required Notion fields
4. Consider adding notification step (email/Slack) on completion or error

## 4. Testing

### Setup Steps (One-time)

1. **Configure n8n Credentials**
   ```
   Go to n8n UI → Credentials
   - Add Notion OAuth credential
   - Add Google Drive OAuth credential
   - Add Google Slides OAuth credential
   ```

2. **Assign Credentials to Nodes**
   - Open workflow in n8n UI
   - Click each node and select the appropriate credential from dropdown
   - "Get Invoice from Notion" → Notion OAuth
   - "Get Client Details" → Notion OAuth
   - "Copy Google Slides Template" → Google Drive OAuth
   - "Replace Variables in Slides" → Google Slides OAuth

3. **Configure Input Parameter**
   - Click "Manual Trigger" node
   - Add workflow input parameter: `invoice_page_id` (string)
   - This will be the Notion page ID to process

### Happy-Path Test

**Test Data Requirements:**
- A valid invoice record in Notion database `2f41c288bb28814aa434e23b9c714d3c`
- Invoice must have:
  - Client relation pointing to valid client record
  - Price (number)
  - P1 Description (text)
  - Due Date (date)
- Client record must have:
  - Client Name (title)
  - Client Address (text)
  - Client Email (email)

**Steps to Run:**
1. Open workflow in n8n UI
2. Click "Execute Workflow" button
3. When prompted, enter the Notion invoice page ID
   - Example: `2f41c288bb28814aa434e23b9c714d3c` (this is your database ID, you'll need a page ID)
4. Watch execution progress through each node
5. Verify output:
   - New Google Slides created in My Drive
   - Title: "Invoice INV-YYYY-NNN"
   - All 13 variables replaced with actual values

**Expected Outcome:**
- ✅ New Google Slides presentation created
- ✅ Named "Invoice INV-2026-XXX" (with unique number)
- ✅ All placeholders replaced with invoice data
- ✅ Dates formatted as DD.MM.YYYY
- ✅ Currency values formatted with 2 decimals
- ✅ VAT calculated at 19%

**How to Find Notion Page ID:**
- Option 1: Open invoice in Notion, copy URL
  - URL format: `https://notion.so/workspace-name/PAGE_ID?v=...`
  - Extract the 32-character ID from URL
- Option 2: Use Notion API to query database
- Option 3: Create a Notion database view with page ID column

## 5. Handoff

### How to Modify

**To Change Invoice Number Format:**
- Edit "Generate Invoice Number" Code node
- Modify line: `const invoiceNumber = \`INV-${year}-${sequence}\`;`
- Example: Change to `INV-${year}-${month}-${sequence}` for monthly sequences

**To Change VAT Rate:**
- Edit "Calculate Totals" Code node
- Modify line: `const vat = subtotal * 0.19;`
- Example: Change to `0.20` for 20% VAT

**To Add More Variables:**
1. Add new variable to "Calculate Totals" Code node return object
2. Add placeholder `{{new_variable}}` to Google Slides template
3. Add new text replacement in "Replace Variables in Slides" node:
   ```json
   {
     "text": "{{new_variable}}",
     "replaceText": "={{ $('Calculate Totals').first().json.new_variable }}",
     "matchCase": false
   }
   ```

**To Save to Different Folder:**
- Edit "Copy Google Slides Template" node
- Change `folderId` from "root" to your target folder ID
- Get folder ID from folder URL in Google Drive

**To Change Date Format:**
- Edit "Calculate Totals" Code node
- Modify `formatDate` function
- Example: Change `${day}.${month}.${year}` to `${month}/${day}/${year}` for US format

### Known Limitations

1. **Invoice Number Sequence**
   - Current implementation uses timestamp-based sequence
   - **Not** truly incremental (INV-2026-001, INV-2026-002, etc.)
   - For production: Store last sequence number in Notion database or Google Sheets
   - Risk: Multiple invoices created in same millisecond could have same number

2. **Single Product Only**
   - Workflow handles only one line item (P1 Description, Price)
   - No support for P2, P3, or multiple products
   - To add multiple products, would need to:
     - Modify "Calculate Totals" to loop through product fields
     - Update Google Slides template with multiple product rows
     - Add dynamic text replacement for each product

3. **Manual Trigger Only**
   - Workflow must be triggered manually with page ID
   - No automatic trigger when new invoice is created
   - To add automation:
     - Option A: Add Schedule Trigger to check for new invoices
     - Option B: Add Webhook Trigger for Notion database changes
     - Option C: Use n8n Notion Trigger (if available in your version)

4. **No Duplicate Detection**
   - Workflow doesn't check if invoice already generated
   - Running twice creates duplicate Google Slides
   - To add: Query Google Drive for existing invoice file before creating

5. **Fixed Destination Folder**
   - All invoices saved to My Drive root
   - Might want to organize by:
     - Client name
     - Month/Year
     - Invoice status
   - Would require additional Google Drive folder management nodes

6. **Currency Hardcoded**
   - Assumes EUR currency (19% MwSt is German VAT rate)
   - No currency symbol or multi-currency support
   - To add: Include currency field in Notion and adjust formatting

### Suggested Next Steps

**Immediate (Before First Use):**
1. ✅ Set up all three OAuth credentials in n8n
2. ✅ Test with sample invoice to verify all fields map correctly
3. ✅ Check Google Slides template has all 13 placeholders
4. ✅ Verify date formats match your requirements (DD.MM.YYYY)

**Short-term Improvements:**
1. 🔧 Implement proper invoice number sequencing
   - Create Google Sheets "Invoice Registry" with last sequence number
   - Read sequence → increment → save back to sheet
2. 🔧 Add error handling with try-catch blocks
3. 🔧 Add email notification on completion
4. 🔧 Create organized folder structure (by year/month)

**Long-term Enhancements:**
1. 🚀 Add automated trigger (schedule or webhook)
2. 🚀 Support multiple products (P2, P3, etc.)
3. 🚀 Add PDF export option
4. 🚀 Integrate with accounting system
5. 🚀 Add invoice status tracking back to Notion

**Alternative Approach for Invoice Numbers:**
Instead of generating unique numbers, consider:
- Store last invoice number in a dedicated Notion page
- Use "Get" to fetch current number
- Increment in Code node
- Use "Update" to save new number back
- This ensures true sequential numbering

## 6. Quick Reference

### Workflow ID
```
LY9HfV4xNZoQhA80
```

### Database IDs
```
Invoice Database: 2f41c288bb28814aa434e23b9c714d3c
Client Database:  2f41c288bb28810e8fcec0c9b125b789
```

### Template ID
```
Google Slides: 1g2P1xP7eS1qMSat1N-OBx42SdkzoZ1d45MV3Z65rCvE
```

### Direct Link to Workflow
```
https://n8n.swayclarke.com/workflow/LY9HfV4xNZoQhA80
(Replace with your actual n8n URL)
```

### Support
For questions or modifications, refer to:
- n8n documentation: https://docs.n8n.io
- Notion API docs: https://developers.notion.com
- Google Slides API: https://developers.google.com/slides

---

**Implementation completed:** 2026-01-26
**Agent:** solution-builder-agent
**Status:** ✅ Ready for credential configuration and testing
