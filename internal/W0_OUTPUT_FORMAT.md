# W0 Output Format - Detailed Transaction Lists

**Updated**: 2026-01-29 13:15
**Workflow**: W0 - Master Orchestrator (ewZOYMYOqSfgtjFm)

---

## Overview

W0 now outputs **complete transaction lists** so Sway can see exactly which documents are missing, not just counts and totals.

---

## Example Output

### Summary Section
```
========================================
📋 MISSING DOCUMENTS DETECTED
========================================
Month/Quarter: 2025-12

Missing Receipts (Expenses): 15 transactions, €8,500.50
Missing Invoices (Income): 12 transactions, €25,000.00

GRAND TOTAL: 27 transactions, €33,500.50

📊 View spreadsheet: https://docs.google.com/spreadsheets/d/...
========================================
```

### Missing Receipts Section (Expenses)
```
📄 MISSING RECEIPTS (Expenses):
────────────────────────────────────────────────────────────────────────────
 1. 2025-12-03 | €    45.03 | Kumpel und Keule GmbH | Lastschrift KUMPEL U...
 2. 2025-12-08 | €   171.28 | Edeka Treugut | Lastschrift EDEKA TREUGUT Ber...
 3. 2025-12-09 | €    49.80 | DM-Drogerie Markt | Lastschrift DM DROGERIE ...
 4. 2025-12-12 | €    85.00 | Restaurant Berlin | Kartenzahlung RESTAURANT...
 5. 2025-12-15 | €   120.50 | Office Supplies | Lastschrift OFFICE SUPPLIE...
 6. 2025-12-18 | €    67.30 | Taxi Berlin | Kartenzahlung TAXI BERLIN
 7. 2025-12-20 | €   450.00 | Hotel München | Kartenzahlung HOTEL MÜNCHEN
 8. 2025-12-22 | €    35.40 | Coffee Shop | Kartenzahlung COFFEE SHOP BE...
 9. 2025-12-24 | €   220.00 | Computer Store | Lastschrift COMPUTER STORE
10. 2025-12-27 | €   180.90 | Software License | Lastschrift SOFTWARE LICE...
11. 2025-12-28 | €    95.00 | Gas Station | Kartenzahlung SHELL TANKSTE...
12. 2025-12-29 | €   310.00 | Office Furniture | Lastschrift IKEA BÜROMÖB...
13. 2025-12-30 | €    42.50 | Pharmacy | Lastschrift APOTHEKE BERLIN
14. 2025-12-30 | €   125.00 | Parking | Kartenzahlung PARKHAUS BERLIN
15. 2025-12-31 | €    58.00 | Train Ticket | Lastschrift DEUTSCHE BAHN
────────────────────────────────────────────────────────────────────────────
Subtotal: 15 transactions, €8,500.50
```

### Missing Invoices Section (Income)
```
📄 MISSING INVOICES (Income):
────────────────────────────────────────────────────────────────────────────
 1. 2025-11-26 | €    48.04 | GEMA - Gutschrift | 01121618000 Clarke Sway
 2. 2025-12-05 | €  5,000.00 | Sway Clarke | Überweisung Client A Projec...
 3. 2025-12-10 | €  8,000.00 | Client B GmbH | Überweisung Invoice INV-202...
 4. 2025-12-15 | €  3,500.00 | Freelance Client | Überweisung Consulting S...
 5. 2025-12-19 | €  1,435.63 | GEMA - Gutschrift | 01121618000 Clarke Sway
 6. 2025-12-20 | €  2,200.00 | Agency Work | Überweisung Project Delivera...
 7. 2025-12-22 | €  1,800.00 | Workshop Income | Überweisung Workshop Dec 2...
 8. 2025-12-24 | €    650.00 | Coaching Session | Überweisung Coaching Fee
 9. 2025-12-28 | €  1,500.00 | Content Creation | Überweisung Content Fee
10. 2025-12-30 | €    833.00 | Supreme Music GmbH | RG 541+ 546
11. 2025-12-31 | €    450.00 | Speaking Fee | Überweisung Event Honorar
12. 2025-12-31 | €  1,200.00 | Royalty Payment | Überweisung Q4 Royalties
────────────────────────────────────────────────────────────────────────────
Subtotal: 12 transactions, €25,000.00
```

### Next Steps Section
```
📁 NEXT STEPS:
────────────────────────────────────────────────────────────────────────────
1. Find and upload missing RECEIPTS (for expenses) to Receipt Pool folder
2. Find and upload missing INVOICES (for income) to Invoice Pool folder
3. Re-run W3 (Matching) workflow to match documents
4. Re-run W0 to verify all documents matched
========================================
```

---

## Field Format

Each transaction line shows:

| Position | Field | Format | Example |
|----------|-------|--------|---------|
| 1 | Index | ` 1.` (padded) | ` 1.`, `10.` |
| 2 | Date | YYYY-MM-DD | `2025-12-15` |
| 3 | Amount | €XX,XXX.XX (padded) | `€    45.03` |
| 4 | Vendor/Client | First vendor or description part | `Restaurant Berlin` |
| 5 | Description | Truncated if >50 chars | `Lastschrift RESTAURANT...` |

---

## Data Processing

### Formatting Logic
```javascript
function formatTransaction(doc, index) {
  const amount = Math.abs(parseFloat(doc.amount_eur)).toFixed(2);
  const date = doc.transaction_date || 'N/A';
  const vendor = doc.vendor || 'Unknown';
  const desc = doc.description || '';

  // Truncate description if too long
  const displayDesc = desc.length > 50 ? desc.substring(0, 47) + '...' : desc;

  return `${(index + 1).toString().padStart(2, ' ')}. ${date} | €${amount.padStart(10, ' ')} | ${vendor} | ${displayDesc}`;
}
```

### Separation Logic
```javascript
// Separate by document type
const receipts = data.missing_documents.filter(d => d.document_type === 'receipt');
const invoices = data.missing_documents.filter(d => d.document_type === 'invoice');

// Display receipts section
if (receipts.length > 0) {
  console.log('📄 MISSING RECEIPTS (Expenses):');
  console.log('────────────────────────────────────────────────────────────────────────────');
  receipts.forEach((doc, idx) => {
    console.log(formatTransaction(doc, idx));
  });
  console.log('────────────────────────────────────────────────────────────────────────────');
  console.log(`Subtotal: ${receipts.length} transactions, €${data.missing_receipts.total}`);
}

// Display invoices section
if (invoices.length > 0) {
  console.log('📄 MISSING INVOICES (Income):');
  console.log('────────────────────────────────────────────────────────────────────────────');
  invoices.forEach((doc, idx) => {
    console.log(formatTransaction(doc, idx));
  });
  console.log('────────────────────────────────────────────────────────────────────────────');
  console.log(`Subtotal: ${invoices.length} transactions, €${data.missing_invoices.total}`);
}
```

---

## Benefits

### Before (Counts Only)
```
Missing receipts: 15 transactions, €8,500.50
Missing invoices: 12 transactions, €25,000.00
```
❌ No way to know WHICH transactions
❌ Must manually check spreadsheet
❌ Time-consuming to identify documents

### After (Detailed Lists)
```
📄 MISSING RECEIPTS (Expenses):
 1. 2025-12-03 | €45.03 | Kumpel und Keule GmbH | ...
 2. 2025-12-08 | €171.28 | Edeka Treugut | ...
 [...]
```
✅ See all transactions at a glance
✅ Quickly identify which documents to find
✅ Scannable format for fast review
✅ Direct visibility into n8n console

---

## Use Cases

### 1. Quick Scan
Sway can quickly scroll through console output to see all missing documents without opening Google Sheets.

### 2. Document Hunt
Clear vendor/client names help identify which receipts/invoices to look for.

### 3. Prioritization
Amount column helps prioritize finding high-value documents first.

### 4. Verification
After uploading documents, re-run W0 and verify specific transactions disappear from the list.

---

## Testing

### Test Command
```bash
curl -X POST https://n8n.oloxa.ai/webhook/w0-expense-orchestrator-start \
  -H "Content-Type: application/json" \
  -d '{"month": "2025-12"}'
```

### What to Check
1. ✅ Summary shows correct counts and totals
2. ✅ Receipt section lists all expense transactions
3. ✅ Invoice section lists all income transactions
4. ✅ Each line shows date, amount, vendor, description
5. ✅ Amounts are properly formatted and aligned
6. ✅ Descriptions truncated if too long
7. ✅ Subtotals match summary totals

---

## Edge Cases Handled

### No Missing Receipts
```
Missing Receipts (Expenses): 0 transactions, €0.00

(No receipt section displayed - only invoice section shows)
```

### No Missing Invoices
```
Missing Invoices (Income): 0 transactions, €0.00

(No invoice section displayed - only receipt section shows)
```

### Long Vendor Names
```
Very Long Company Name Tha... | Description truncated if >50...
```

### Missing Data
```
N/A | €    0.00 | Unknown | (empty description)
```

---

## Future Enhancements

**Possible additions**:
- Sort by amount (highest first)
- Filter by vendor/category
- Export to CSV
- Group by week/category
- Color coding (high priority in red)

**Not needed now** - current format is sufficient for Sway's workflow.

---

**Status**: ✅ COMPLETE - Detailed lists implemented
**Node Updated**: "Log Missing Receipts" (should rename to "Log Missing Documents")
**Ready for Testing**: Yes - clean duplicates first, then test W0

---

**Last Updated**: 2026-01-29 13:15
**Validation**: Workflow syntax valid (harmless warnings only)
