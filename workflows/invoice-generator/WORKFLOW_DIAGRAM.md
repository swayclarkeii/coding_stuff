# Invoice Generator Workflow - Visual Diagram

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         INVOICE GENERATOR WORKFLOW                       │
└─────────────────────────────────────────────────────────────────────────┘

[Manual Trigger]
     ↓
     │ Input: invoice_page_id (Notion page ID)
     ↓
┌──────────────────────────────┐
│  Get Invoice from Notion     │
│  Database: 2f41c288...714d3c │
│  ─────────────────────────── │
│  Retrieves:                  │
│  • Client (relation)         │
│  • Price (number)            │
│  • P1 Description (text)     │
│  • Due Date (date)           │
└──────────────────────────────┘
     ↓
     │ Passes: invoice data + Client relation ID
     ↓
┌──────────────────────────────┐
│  Get Client Details          │
│  Database: 2f41c288...b125b789│
│  ─────────────────────────── │
│  Retrieves:                  │
│  • Client Name (title)       │
│  • Client Address (text)     │
│  • Client Email (email)      │
└──────────────────────────────┘
     ↓
     │ Passes: invoice + client data
     ↓
┌──────────────────────────────┐
│  Generate Invoice Number     │
│  (Code Node)                 │
│  ─────────────────────────── │
│  Logic:                      │
│  • Get current year          │
│  • Generate 3-digit sequence │
│  • Format: INV-YYYY-NNN      │
│                              │
│  Output: INV-2026-045        │
└──────────────────────────────┘
     ↓
     │ Passes: all data + invoice_number
     ↓
┌──────────────────────────────┐
│  Calculate Totals            │
│  (Code Node)                 │
│  ─────────────────────────── │
│  Calculations:               │
│  • quantity = 1 (hardcoded)  │
│  • total = price × quantity  │
│  • subtotal = total          │
│  • vat = subtotal × 0.19     │
│  • final = subtotal + vat    │
│                              │
│  Formatting:                 │
│  • Dates → DD.MM.YYYY        │
│  • Currency → 2 decimals     │
│                              │
│  Output: Complete invoice    │
│          data object         │
└──────────────────────────────┘
     ↓
     │ Data ready for slides
     ↓
┌──────────────────────────────┐
│  Copy Google Slides Template │
│  (Google Drive)              │
│  ─────────────────────────── │
│  Template: 1g2P1xP7e...CvE   │
│  Target: My Drive / root     │
│  Name: Invoice INV-2026-045  │
│                              │
│  Output: New presentation ID │
└──────────────────────────────┘
     ↓
     │ Passes: presentation_id + invoice data
     ↓
┌──────────────────────────────┐
│  Replace Variables in Slides │
│  (Google Slides)             │
│  ─────────────────────────── │
│  Replaces 13 placeholders:   │
│  {{invoice_number}} → actual │
│  {{date}} → DD.MM.YYYY       │
│  {{due_date}} → DD.MM.YYYY   │
│  {{client_name}} → actual    │
│  ... (10 more variables)     │
│                              │
│  Output: Completed invoice!  │
└──────────────────────────────┘
     ↓
  ✅ DONE

  Result: Populated Google Slides invoice
  Location: My Drive
  Ready to send or export as PDF
```

## Node-by-Node Details

### 1. Manual Trigger
```yaml
Type: Manual workflow start
Required Input: Notion invoice page ID
Example: "2f41c288bb28814aa434e23b9c714d3c"
```

### 2. Get Invoice from Notion
```yaml
Type: Notion Database Page > Get
Configuration:
  - Database: Invoice database
  - Operation: Get single page by ID
  - Returns: All invoice properties
Data Flow Out:
  properties:
    Client: { relation: [{ id: "client-page-id" }] }
    Price: { number: 1500 }
    P1 Description: { rich_text: [{ plain_text: "Web Dev" }] }
    Due Date: { date: { start: "2026-02-15" } }
```

### 3. Get Client Details
```yaml
Type: Notion Database Page > Get
Configuration:
  - Database: Client database
  - Page ID: From previous node's Client relation
  - Operation: Get single page by ID
Data Flow Out:
  properties:
    Client Name: { title: [{ plain_text: "Acme Corp" }] }
    Client Address: { rich_text: [{ plain_text: "123 Main St" }] }
    Client Email: { email: "billing@acme.com" }
```

### 4. Generate Invoice Number
```yaml
Type: Code Node (JavaScript)
Input: All previous data
Logic:
  const year = new Date().getFullYear()  // 2026
  const sequence = String(Date.now()).slice(-3)  // 045
  const invoiceNumber = `INV-${year}-${sequence}`  // INV-2026-045
Output:
  invoice_number: "INV-2026-045"
  + all previous data
```

### 5. Calculate Totals
```yaml
Type: Code Node (JavaScript)
Input: Invoice + Client + Invoice Number
Logic:
  # Extract from Notion
  price = invoice.Price.number  # 1500
  description = invoice.P1_Description.rich_text[0].plain_text
  dueDate = invoice.Due_Date.date.start
  clientName = client.Client_Name.title[0].plain_text
  clientAddress = client.Client_Address.rich_text[0].plain_text
  clientEmail = client.Client_Email.email

  # Calculate
  quantity = 1  # Hardcoded
  total = price × quantity  # 1500.00
  subtotal = total  # 1500.00
  vat = subtotal × 0.19  # 285.00
  final_amount = subtotal + vat  # 1785.00

  # Format dates
  date = formatToEuropean(new Date())  # 26.01.2026
  due_date = formatToEuropean(dueDate)  # 15.02.2026

Output:
  invoice_number: "INV-2026-045"
  date: "26.01.2026"
  due_date: "15.02.2026"
  client_name: "Acme Corp"
  client_address: "123 Main St"
  client_email: "billing@acme.com"
  project_description: "Web Development Services"
  price: "1500.00"
  quantity: 1
  total: "1500.00"
  subtotal: "1500.00"
  vat: "285.00"
  final_amount: "1785.00"
```

### 6. Copy Google Slides Template
```yaml
Type: Google Drive > File > Copy
Configuration:
  - Source File ID: 1g2P1xP7eS1qMSat1N-OBx42SdkzoZ1d45MV3Z65rCvE
  - Target Drive: My Drive
  - Target Folder: root
  - New Name: "Invoice {{ invoice_number }}"  # Invoice INV-2026-045
Output:
  id: "new-presentation-id-12345"
  name: "Invoice INV-2026-045"
  mimeType: "application/vnd.google-apps.presentation"
```

### 7. Replace Variables in Slides
```yaml
Type: Google Slides > Presentation > Replace Text
Configuration:
  - Presentation ID: From previous node
  - Replace these 13 text patterns:

    Search: "{{invoice_number}}" → Replace: "INV-2026-045"
    Search: "{{date}}" → Replace: "26.01.2026"
    Search: "{{due_date}}" → Replace: "15.02.2026"
    Search: "{{client_name}}" → Replace: "Acme Corp"
    Search: "{{client_address}}" → Replace: "123 Main St"
    Search: "{{client_email}}" → Replace: "billing@acme.com"
    Search: "{{project_description}}" → Replace: "Web Development Services"
    Search: "{{price}}" → Replace: "1500.00"
    Search: "{{quantity}}" → Replace: "1"
    Search: "{{total}}" → Replace: "1500.00"
    Search: "{{subtotal}}" → Replace: "1500.00"
    Search: "{{vat}}" → Replace: "285.00"
    Search: "{{final_amount}}" → Replace: "1785.00"

Output:
  replies: [13 successful replacements]
  presentationId: "new-presentation-id-12345"
```

## Error Handling Points

**Current State:** No error handling implemented

**Where Errors Could Occur:**

```
┌─────────────────────────────────────────┐
│ POTENTIAL ERROR POINTS                  │
├─────────────────────────────────────────┤
│                                         │
│ 1. Get Invoice from Notion              │
│    ❌ Page ID doesn't exist             │
│    ❌ No access to database             │
│    ❌ Missing required fields           │
│                                         │
│ 2. Get Client Details                   │
│    ❌ Client relation is empty          │
│    ❌ Client page deleted               │
│    ❌ No access to client database      │
│                                         │
│ 3. Generate Invoice Number              │
│    ⚠️  Timestamp collision (unlikely)   │
│    ⚠️  Code execution error             │
│                                         │
│ 4. Calculate Totals                     │
│    ❌ Price field is empty/null         │
│    ❌ Date field is missing             │
│    ❌ Rich text fields are empty        │
│                                         │
│ 5. Copy Google Slides Template          │
│    ❌ Template ID doesn't exist         │
│    ❌ No permission to access template  │
│    ❌ Quota exceeded                    │
│                                         │
│ 6. Replace Variables in Slides          │
│    ⚠️  Placeholders not found in template│
│    ❌ Presentation was deleted          │
│                                         │
└─────────────────────────────────────────┘
```

**Recommended Error Handling:**

```javascript
// Add to Code nodes:
try {
  // existing code
  return { json: { ... } };
} catch (error) {
  return {
    json: {
      error: true,
      message: error.message,
      node: 'Calculate Totals'
    }
  };
}

// Add IF nodes after risky operations:
IF Client relation exists → Continue
                         ↘ Send error notification
```

## Data Structure Reference

### Invoice Record (Notion)
```json
{
  "id": "page-id-12345",
  "properties": {
    "Project Name": {
      "title": [{ "plain_text": "Q1 Website Redesign" }]
    },
    "Client": {
      "relation": [{ "id": "client-page-id-67890" }]
    },
    "Product": {
      "select": { "name": "Web Development" }
    },
    "Price": {
      "number": 1500
    },
    "P1 Description": {
      "rich_text": [{ "plain_text": "Full website redesign" }]
    },
    "Due Date": {
      "date": { "start": "2026-02-15" }
    },
    "MwSt Amount": {
      "number": 19
    }
  }
}
```

### Client Record (Notion)
```json
{
  "id": "client-page-id-67890",
  "properties": {
    "Client Name": {
      "title": [{ "plain_text": "Acme Corporation" }]
    },
    "Client Address": {
      "rich_text": [{
        "plain_text": "123 Main Street\nBerlin, 10115\nGermany"
      }]
    },
    "Client Email": {
      "email": "billing@acmecorp.com"
    }
  }
}
```

### Final Invoice Data (Code Node Output)
```json
{
  "invoice_number": "INV-2026-045",
  "date": "26.01.2026",
  "due_date": "15.02.2026",
  "client_name": "Acme Corporation",
  "client_address": "123 Main Street\nBerlin, 10115\nGermany",
  "client_email": "billing@acmecorp.com",
  "project_description": "Full website redesign",
  "price": "1500.00",
  "quantity": 1,
  "total": "1500.00",
  "subtotal": "1500.00",
  "vat": "285.00",
  "final_amount": "1785.00"
}
```

## Usage Examples

### Example 1: Standard Invoice
```
Input: invoice_page_id = "2f41c288bb28814aa434e23b9c714d3c"

Process Flow:
1. Fetch invoice: "Website Development" - €2,500
2. Fetch client: "Tech Startup GmbH"
3. Generate number: INV-2026-128
4. Calculate: €2,500 + €475 VAT = €2,975
5. Create slides: "Invoice INV-2026-128"
6. Populate with all data

Result: Ready-to-send invoice in Google Slides
```

### Example 2: Consulting Invoice
```
Input: invoice_page_id = "abc123def456"

Process Flow:
1. Fetch invoice: "Q1 Consulting Services" - €5,000
2. Fetch client: "Enterprise Solutions AG"
3. Generate number: INV-2026-129
4. Calculate: €5,000 + €950 VAT = €5,950
5. Create slides: "Invoice INV-2026-129"
6. Populate with all data

Result: Professional invoice ready for client
```

---

**Diagram created:** 2026-01-26
**Workflow ID:** LY9HfV4xNZoQhA80
