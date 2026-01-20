# W4 Invoice Organization Flow Diagram

## Complete Workflow Structure (v2.1)

```
┌─────────────────────────┐
│ Webhook Trigger (Manual)│
└───────────┬─────────────┘
            │
            v
┌─────────────────────────┐
│ Parse Month/Year Input  │
└───────────┬─────────────┘
            │
            v
┌─────────────────────────┐
│ Create Main VAT Folder  │  Creates: VAT 2025/January
└───────────┬─────────────┘
            │
            v
┌─────────────────────────┐
│  Prepare Bank Folders   │  Prepares: DKB, Sparkasse
└───────────┬─────────────┘
            │
            v
┌─────────────────────────┐
│   Create Bank Folder    │  Creates: VAT 2025/January/DKB, etc.
└─────┬─────────┬─────────┘
      │         │
      v         v
┌─────────┐  ┌─────────┐
│Statements│  │Receipts │  Creates: Statements/ and Receipts/ subfolders
│Subfolder │  │Subfolder│
└────┬────┘  └────┬────┘
     │            │
     └─────┬──────┘
           v
    ┌──────────┐
    │  Merge   │ Wait for Subfolders
    └─────┬────┘
          │
          v
┌─────────────────────────┐
│  Get Main Folder Data   │
└───────────┬─────────────┘
            │
            v
┌─────────────────────────┐
│  Create Income Folder   │  Creates: VAT 2025/January/Income
└─┬────────┬──────┬───────┬┘
  │        │      │       │
  │        │      │       │ NEW FLOW ──────────────────┐
  │        │      │       │                            │
  v        v      v       v                            │
┌───┐   ┌───┐  ┌───┐   ┌───────────────┐            │
│Stm│   │Rcp│  │Txn│   │Read Invoices  │ ← NEW      │
│Sht│   │Sht│  │Sht│   │Sheet          │            │
└┬──┘   └┬──┘  └───┘   └───────┬───────┘            │
 │       │                      │                     │
 │       │                      v                     │
 │       │              ┌───────────────┐            │
 │       │              │Process        │ ← NEW      │
 │       │              │Invoices       │            │
 │       │              └───────┬───────┘            │
 │       │                      │                     │
 v       v                      v                     │
┌─────┐ ┌─────┐         ┌─────────────┐             │
│Proc │ │Proc │         │Filter Valid │ ← NEW       │
│Stm  │ │Rcp  │         │Invoices     │             │
└──┬──┘ └──┬──┘         └──────┬──────┘             │
   │       │                   │                      │
   v       v                   v                      │
┌──────┐ ┌──────┐       ┌─────────────┐             │
│Filter│ │Filter│       │Move Invoice │ ← NEW       │
│Valid │ │Valid │       │Files        │             │
│Stm   │ │Rcp   │       └──────┬──────┘             │
└───┬──┘ └───┬──┘              │                     │
    │        │                 v                      │
    v        v          ┌──────────────┐             │
┌────────┐ ┌────────┐  │Update        │ ← NEW       │
│Move Stm│ │Move Rcp│  │Invoices      │             │
│Files   │ │Files   │  │FilePath      │             │
└───┬────┘ └───┬────┘  └──────┬───────┘             │
    │          │               │                      │
    v          v               v                      │
┌────────┐ ┌────────┐  ┌──────────────┐             │
│Update  │ │Update  │  │              │             │
│Stm Path│ │Rcp Path│  │              │             │
└───┬────┘ └───┬────┘  └──────┬───────┘             │
    │          │               │                      │
    └────┬─────┴───────────────┘                     │
         │                                             │
         v                                             │
    ┌────────┐                                        │
    │ Merge  │ Wait for Processing (3 inputs)         │
    │ (3 in) │ ← MODIFIED (added input3)              │
    └───┬────┘                                        │
        │                                              │
        v                                              │
┌───────────────────────┐                             │
│Generate Summary Report│ ← MODIFIED (invoice stats) │
└───────────────────────┘                             │
                                                       │
         INVOICE FLOW COMPLETE ───────────────────────┘
```

## Invoice Flow Details

### NEW: Invoice Processing Chain

```
Read Invoices Sheet
         │
         │ (All columns A:Z from "Invoices" sheet)
         │
         v
Process Invoices
         │
         │ Filters:
         │ - Month matches input
         │ - Year matches input
         │ - InvoiceFileID exists
         │ - InvoiceFileID not blank
         │
         v
Filter Valid Invoices
         │
         │ (Double-check InvoiceFileID not empty)
         │
         v
Move Invoice Files
         │
         │ Operation: Move file to Income folder
         │ Source: InvoiceFileID
         │ Destination: VAT YYYY/Month/Income/
         │
         v
Update Invoices FilePath
         │
         │ Updates:
         │ - FilePath: "VAT 2025/January/Income/[filename]"
         │ - FileID: (new file ID after move)
         │ - OrganizedDate: (current timestamp)
         │
         v
Wait for Processing (input3)
```

## File Destinations

### Bank Statements
```
VAT 2025/January/
  └── DKB/
      └── Statements/ ← DKB bank statements
  └── Sparkasse/
      └── Statements/ ← Sparkasse bank statements
```

### Expense Receipts
```
VAT 2025/January/
  └── DKB/
      └── Receipts/ ← DKB expense receipts
  └── Sparkasse/
      └── Receipts/ ← Sparkasse expense receipts
```

### Invoices (NEW)
```
VAT 2025/January/
  └── Income/ ← ALL invoices (not bank-specific)
      ├── Invoice_001.pdf
      ├── Invoice_002.pdf
      └── Invoice_003.pdf
```

## Data Flow

### Input Data
```javascript
// Webhook input
{
  "month": "January",
  "year": "2025"
}

// Invoices sheet columns (example)
InvoiceID | Date       | Amount | Client    | InvoiceFileID | FilePath | ...
INV001    | 2025-01-15 | 1500   | ClientA   | abc123xyz     | (empty)  | ...
INV002    | 2025-01-20 | 2000   | ClientB   | def456uvw     | (empty)  | ...
```

### Processing Logic
```javascript
// Process Invoices node
1. Read all invoices from sheet
2. Filter by month/year matching input
3. Filter by InvoiceFileID exists
4. Add destinationFolder (Income folder ID)
5. Pass to next node

// Move Invoice Files node
1. Get file from InvoiceFileID
2. Move to destinationFolder (Income)
3. Return new file metadata

// Update Invoices FilePath node
1. Update FilePath column: "VAT 2025/January/Income/[filename]"
2. Update FileID column: (new file ID)
3. Update OrganizedDate: (current timestamp)
```

### Output Data
```javascript
// Invoices sheet after processing
InvoiceID | Date       | InvoiceFileID | FilePath                              | OrganizedDate
INV001    | 2025-01-15 | newID123      | VAT 2025/January/Income/Invoice_001   | 2025-01-11T10:30:00Z
INV002    | 2025-01-20 | newID456      | VAT 2025/January/Income/Invoice_002   | 2025-01-11T10:30:05Z

// Summary report
{
  "success": true,
  "month": "January",
  "year": "2025",
  "statistics": {
    "statementsProcessed": 2,
    "receiptsProcessed": 15,
    "invoicesProcessed": 8,  ← NEW
    "totalFilesOrganized": 25
  },
  "message": "Successfully organized January 2025:\n- 2 bank statements\n- 15 expense receipts\n- 8 invoices\nTotal: 25 files organized"
}
```

## Node Count Summary

### Before Invoice Flow
- Total Nodes: 23
- Total Connections: 20

### After Invoice Flow
- Total Nodes: 28 (+5)
- Total Connections: 26 (+6)

### New Nodes (5)
1. Read Invoices Sheet (Google Sheets)
2. Process Invoices (Code)
3. Filter Valid Invoices (Filter)
4. Move Invoice Files (Google Drive)
5. Update Invoices FilePath (Google Sheets)

### Modified Nodes (2)
1. Create Income Folder (added 4th output connection)
2. Generate Summary Report (added invoice statistics)

## Parallel Processing

The workflow now processes THREE parallel streams:

```
Create Income Folder
         │
         ├───────────┬───────────┬───────────┐
         │           │           │           │
         v           v           v           v
    Statements   Receipts   Transactions  Invoices
      Flow         Flow        Flow        Flow
         │           │           │           │
         └───────────┴───────────┴───────────┘
                     │
                     v
            Wait for Processing
                  (Merge)
```

**Key Point:** All three flows run in parallel for maximum efficiency.
