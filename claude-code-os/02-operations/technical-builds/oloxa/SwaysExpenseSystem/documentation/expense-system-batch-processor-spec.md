# Expense System - Batch Processor Specification

## Purpose
One-time workflow to process 16 existing bank statement PDFs that were uploaded before W1's Google Drive trigger was activated.

## Status
- **Workflow ID:** `y3A3JHocwVaOuMHT`
- **Name:** "Expense System - W1 Batch Processor (One-Time Use)"
- **Current State:** Partial (Manual Trigger + List Files nodes created)
- **Next Step:** Add processing nodes manually in n8n UI

## Why Manual Build Required
n8n's API diff engine has errors when adding multiple connected nodes. Building via UI is more reliable.

## Complete Workflow Structure

### Node 1: Manual Trigger
- **Type:** Manual Trigger (n8n-nodes-base.manualTrigger)
- **Position:** (240, 400)
- **Purpose:** Click to start batch processing
- **Config:** Default settings

### Node 2: List Files in Bank Statements Folder  ✅ CREATED
- **Type:** Google Drive (n8n-nodes-base.googleDrive)
- **Position:** (460, 400)
- **Resource:** File/Folder
- **Operation:** Search
- **Config:**
  - Query: `'1UYhIP6Nontc2vuE2G1aMvkggaEk6szv8' in parents`
  - Credentials: Google Drive account
- **Purpose:** Find all files in Bank & CC Statements folder

### Node 3: Download PDF
- **Type:** Google Drive (n8n-nodes-base.googleDrive)
- **Position:** (680, 400)
- **Resource:** File
- **Operation:** Download
- **Config:**
  - File ID: `={{$json.id}}` (from List Files)
  - Credentials: Google Drive account
- **Purpose:** Download each PDF file

### Node 4: Extract File Metadata
- **Type:** Code (n8n-nodes-base.code)
- **Position:** (900, 400)
- **Code:** (Copy from W1's "Extract File Metadata" node)
```javascript
// Extract metadata from the PDF file
const item = $input.first();
const fileName = item.json.name;
const fileId = item.json.id;

// Parse bank from filename (e.g., "ING_2025-01_Statement.pdf")
const bankMatch = fileName.match(/^([A-Za-z-]+)_/);
const bank = bankMatch ? bankMatch[1] : 'Unknown';

// Parse month/year from filename
const dateMatch = fileName.match(/_([0-9]{4})-([0-9]{2})_/);
const year = dateMatch ? dateMatch[1] : new Date().getFullYear().toString();
const month = dateMatch ? dateMatch[2] : (new Date().getMonth() + 1).toString().padStart(2, '0');

// Generate statement ID
const statementId = `STMT-${bank}-${year}${month}-${Date.now()}`;

// ✅ CORRECT: Preserve entire binary object (not nested)
return {
  json: {
    fileName,
    fileId,
    bank,
    year,
    month,
    statementId
  },
  binary: item.binary
};
```

### Node 5: Build Anthropic API Request
- **Type:** Code (n8n-nodes-base.code)
- **Position:** (1120, 400)
- **Code:** (Copy from W1's "Build Anthropic API Request" node)
```javascript
// Build the Anthropic API request with proper binary handling for filesystem mode
const inputItem = $input.first();
const metadata = inputItem.json;

// CRITICAL FIX for n8n 2.1.4 filesystem mode:
// Use this.helpers.getBinaryDataBuffer() to read actual file from disk
const binaryPropertyName = 'data';
const binaryBuffer = await this.helpers.getBinaryDataBuffer(0, binaryPropertyName);
const base64Data = binaryBuffer.toString('base64');

// Verify we got actual PDF data (should start with JVBERi... which is "%PDF-" in base64)
if (base64Data.startsWith('ZmlsZXN5c3RlbS')) {
  throw new Error('ERROR: Still encoding filesystem reference, not PDF bytes. Got: ' + base64Data.substring(0, 50));
}

// Additional validation: Check if it starts with valid PDF header
if (!base64Data.startsWith('JVBERi')) {
  throw new Error('ERROR: Base64 does not start with PDF magic bytes. Got: ' + base64Data.substring(0, 50));
}

// Build the complete Anthropic API request with DOCUMENT type
const requestBody = {
  model: "claude-sonnet-4-5",
  max_tokens: 4096,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "text",
          text: "You are a German bank statement parser. Extract all transactions from this bank statement and return them as a JSON array with fields: date (DD.MM.YYYY), description, amount (negative for expenses, positive for income), currency."
        },
        {
          type: "document",
          source: {
            type: "base64",
            media_type: "application/pdf",
            data: base64Data
          }
        }
      ]
    }
  ]
};

// Return the request body and metadata
return {
  json: {
    requestBody: requestBody,
    fileName: metadata.fileName,
    fileId: metadata.fileId,
    bank: metadata.bank,
    year: metadata.year,
    month: metadata.month,
    statementId: metadata.statementId
  }
};
```

### Node 6: Parse PDF with Anthropic Vision
- **Type:** HTTP Request (n8n-nodes-base.httpRequest)
- **Position:** (1340, 400)
- **Config:**
  - Method: POST
  - URL: `https://api.anthropic.com/v1/messages`
  - Authentication: Predefined Credential Type
  - Credential Type: Anthropic API
  - Send Headers: YES
    - Header: `anthropic-version` = `2023-06-01`
  - Send Body: YES
  - Body Content Type: JSON
  - Specify Body: JSON
  - JSON Body: `={{ $json.requestBody }}`
  - Credentials: Anthropic account

### Node 7: Parse Anthropic Response
- **Type:** Code (n8n-nodes-base.code)
- **Position:** (1560, 400)
- **Code:** (Copy from W1's "Parse Anthropic Response" node)
```javascript
// Parse Anthropic response and prepare transaction data
const response = $input.first().json;
const textContent = response.content[0].text;

// Strip markdown code fences if present (Anthropic wraps JSON in ```json...```)
const jsonText = textContent.replace(/^```json\n?/, '').replace(/\n?```$/, '').trim();

// Parse the JSON
const transactions = JSON.parse(jsonText);

const metadata = $('Extract File Metadata').first().json;

return transactions.map((txn, index) => ({
  json: {
    TransactionID: `${metadata.statementId}-${(index + 1).toString().padStart(3, '0')}`,
    Date: txn.date,
    Bank: metadata.bank,
    Amount: txn.amount.toString(),
    Currency: txn.currency || 'EUR',
    Description: txn.description,
    Vendor: '',
    Category: '',
    ReceiptID: '',
    StatementID: metadata.statementId,
    MatchStatus: 'unmatched',
    MatchConfidence: '0',
    Notes: '',
    Tags: '',
    Type: 'expense',
    AnnualInvoiceID: ''
  }
}));
```

### Node 8: Write Transactions to Database
- **Type:** Google Sheets (n8n-nodes-base.googleSheets)
- **Position:** (1780, 320)
- **Resource:** Sheet Within Document
- **Operation:** Append Row
- **Config:**
  - Document ID: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
  - Sheet: Transactions
  - Data Mode: Auto-Map Columns (or copy exact mapping from W1)
  - Credentials: Google Sheets account
- **Note:** Copy exact field mappings from W1 node

### Node 9: Log Statement Record
- **Type:** Google Sheets (n8n-nodes-base.googleSheets)
- **Position:** (1780, 480)
- **Resource:** Sheet Within Document
- **Operation:** Append Row
- **Config:**
  - Document ID: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
  - Sheet: Statements
  - Fields to map:
    - StatementID: `={{$('Extract File Metadata').first().json.statementId}}`
    - Bank: `={{$('Extract File Metadata').first().json.bank}}`
    - Month: `={{$('Extract File Metadata').first().json.month}}`
    - Year: `={{$('Extract File Metadata').first().json.year}}`
    - FileID: `={{$('Extract File Metadata').first().json.fileId}}`
    - FilePath: `={{$('Extract File Metadata').first().json.fileName}}`
    - ProcessedDate: `={{new Date().toISOString()}}`
    - TransactionCount: `={{$('Parse Anthropic Response').all().length}}`
  - Credentials: Google Sheets account

### Node 10: Move PDF to Archive
- **Type:** Google Drive (n8n-nodes-base.googleDrive)
- **Position:** (2000, 320)
- **Resource:** File
- **Operation:** Move
- **Config:**
  - File ID: `={{$('List Files in Bank Statements Folder').first().json.id}}`
  - Folder ID: `1Z5VTiBW7RBEZaLXbsCdvWZrhj9SLmp3r` (Archive folder)
  - Credentials: Google Drive account

## Connections

```
Manual Trigger
  → List Files in Bank Statements Folder
  → Download PDF
  → Extract File Metadata
  → Build Anthropic API Request
  → Parse PDF with Anthropic Vision
  → Parse Anthropic Response
  ├─→ Write Transactions to Database → Move PDF to Archive
  └─→ Log Statement Record
```

## Credentials Needed

From W1 workflow:
- **Google Drive OAuth2:** ID `a4m50EefR3DJoU0R` (name: "Google Drive account")
- **Google Sheets OAuth2:** ID `H7ewI1sOrDYabelt` (name: "Google Sheets account")
- **Anthropic API:** ID `MRSNO4UW3OEIA3tQ` (name: "Anthropic account")

## Testing Steps

### Step 1: Test with ONE file
1. Open workflow in n8n UI
2. Click "Test workflow" button
3. Verify execution completes
4. Check:
   - Transactions appear in Transactions sheet
   - Statement logged in Statements sheet
   - File moved to Archive folder
5. If errors → debug and fix

### Step 2: Process remaining files
1. Once validated, run workflow again
2. It will process ALL files in folder (15 remaining)
3. Monitor executions for errors
4. Verify final count:
   - 16 statements in Statements sheet
   - Hundreds of transactions in Transactions sheet
   - 16 files in Archive folder
   - 0 files in Bank & CC Statements folder

## Important Notes

### Why Batch Processor vs Modifying W1

**Advantages:**
- ✅ Doesn't modify production W1 workflow
- ✅ Can be deactivated after one-time use
- ✅ Clear separation of concerns
- ✅ Safer (W1 remains unchanged if something fails)

**Trade-offs:**
- Duplicates W1's logic (acceptable for one-time use)
- Need to keep in sync if W1 changes (not relevant after batch completes)

### After Batch Processing Complete

**Deactivate this workflow:**
1. Future files will be processed by W1's Google Drive Trigger
2. This batch processor is only for the 16 pre-existing files
3. Mark workflow as "archived" or delete it

**Verify Results:**
1. Check Transactions sheet has expected number of transactions
2. Check all files moved to Archive
3. Test W1 with a NEW file to ensure it still works

## Alternative: Simple Manual Approach

If building the batch processor is too complex, you can trigger W1 manually:

**For each of the 16 files:**
1. Move file OUT of Bank & CC Statements folder (to Desktop)
2. Wait 5 seconds
3. Move file BACK into Bank & CC Statements folder
4. W1's Google Drive Trigger will detect the "fileUpdated" event
5. W1 processes the file automatically

**Pros:** No new workflow needed
**Cons:** Manual, tedious (16 files × 2 moves each = 32 operations)

## Next Steps

1. ✅ Build batch processor in n8n UI (follow spec above)
2. Test with ONE file (ING Oct)
3. Process all 16 files
4. Move to W3 fixes
5. Test W3 matching

---

**Created:** 2026-01-28
**Workflow ID:** y3A3JHocwVaOuMHT
**Status:** Specification complete, ready for manual build
