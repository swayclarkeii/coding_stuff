# W7 Direction Classification Update - Implementation Complete

**Workflow ID:** `6x1sVuv4XKN0002B`
**Workflow Name:** Expense System - Workflow 7: Downloads Folder Monitor
**Updated:** 2026-01-17
**Agent:** solution-builder-agent

---

## Summary

Updated W7 to classify invoices into two directions:
- **INCOME**: Invoices where Sway receives money
- **EXPENSE**: Invoices where Sway owes money

This enables proper financial tracking and tax categorization.

---

## Changes Made

### 1. Node 6: Build Anthropic Request

**Updated the invoice prompt** to include comprehensive direction classification logic.

**Key Features:**
- Two-step analysis: (1) Classify direction, (2) Extract details
- INCOME indicators: Document FROM Sway, contains "RECHNUNG AN:", agency billing with "Auftraggeber:", GEMA royalties
- EXPENSE indicators: Document TO Sway, standard invoices, no third-party fields
- Returns structured JSON with: `direction`, `documentType`, `invoiceNumber`, `date`, `amount`, `currency`, `vendor`, `clientName`, `directionReason`
- **Default behavior**: When uncertain, defaults to EXPENSE (conservative for tax purposes)

**Receipt handling:**
- Receipts always include `"direction": "EXPENSE"` in extraction

### 2. Node 13: Prepare Invoice Sheet Data

**Added new fields** to the sheet data output:

```javascript
{
  InvoiceID: extracted.invoiceNumber || 'N/A',
  Direction: extracted.direction || 'EXPENSE',          // NEW
  ClientName: extracted.clientName || extracted.vendor || 'Unknown',
  Amount: extracted.amount || 0,
  Currency: extracted.currency || 'EUR',
  Date: extracted.date || new Date().toLocaleDateString('de-DE'),
  DocumentType: extracted.documentType || 'invoice',    // NEW
  DirectionReason: extracted.directionReason || '',     // NEW
  FileID: fileId,
  FilePath: filePath,
  ProcessedDate: new Date().toISOString(),
  Source: 'Downloads'
}
```

**New fields:**
- `Direction`: "INCOME" or "EXPENSE" (defaults to EXPENSE)
- `DocumentType`: "invoice", "credit_note", or "statement"
- `DirectionReason`: Brief explanation of classification decision

### 3. Node 18: Prepare Receipt Sheet Data

**Added Direction field** (always EXPENSE):

```javascript
{
  Vendor: extracted.vendor || 'Unknown',
  Direction: 'EXPENSE',                                 // NEW
  Amount: extracted.amount || 0,
  Currency: extracted.currency || 'EUR',
  Date: extracted.date || new Date().toLocaleDateString('de-DE'),
  FileID: fileId,
  FilePath: filePath,
  ProcessedDate: new Date().toISOString(),
  Source: 'Downloads'
}
```

---

## Validation Results

✅ **Workflow validation completed**
- 3 operations applied successfully
- All node updates verified
- Pre-existing warnings (outdated typeVersions, error handling) remain
- No new errors introduced

---

## Next Steps

1. **Update Google Sheet columns** - Add Direction, DocumentType, DirectionReason columns to the Invoices sheet
2. **Test with real invoices** - Verify classification accuracy with:
   - Sway's invoices (SC - format)
   - Agency invoices (with Auftraggeber field)
   - GEMA royalty statements
   - Direct expense invoices to Sway
3. **Monitor extraction accuracy** - Check `DirectionReason` field to verify Claude's classification logic
4. **Adjust thresholds** - If needed, refine INCOME/EXPENSE indicators based on real-world results

---

## Sheet Column Updates Required

**Invoices Sheet needs these new columns:**
- Direction (text)
- DocumentType (text)
- DirectionReason (text)

**Receipts Sheet needs this new column:**
- Direction (text) - will always be "EXPENSE"

---

## Testing Checklist

- [ ] Add new columns to Google Sheets
- [ ] Upload Sway invoice (SC - format) → Should classify as INCOME
- [ ] Upload agency invoice with Auftraggeber → Should classify as INCOME
- [ ] Upload GEMA royalty statement → Should classify as INCOME
- [ ] Upload vendor invoice to Sway → Should classify as EXPENSE
- [ ] Upload receipt → Should classify as EXPENSE
- [ ] Verify DirectionReason provides clear explanations
- [ ] Check all extracted data flows correctly to sheet

---

## Configuration Preserved

✅ All existing node configurations preserved:
- Binary data handling (`getBinaryDataBuffer`)
- MIME type detection for images/PDFs
- `mode: "runOnceForEachItem"` on all Code nodes
- Existing error handling (`continueOnFail: true`)
- All credentials (Google Drive, Google Sheets, Anthropic API)

---

## Implementation Notes

- No workflow structure changes (no new nodes or connections)
- Only parameter updates to 3 Code nodes
- Backward compatible (defaults to EXPENSE if direction missing)
- Conservative approach (uncertain = EXPENSE) for tax safety
