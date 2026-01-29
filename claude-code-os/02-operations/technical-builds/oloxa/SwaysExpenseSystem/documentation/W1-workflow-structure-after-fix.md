# W1 Workflow Structure - After Bank Identification Fix

## Visual Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     TRIGGER OPTIONS                          │
├─────────────────────────────────────────────────────────────┤
│ Option A: Watch Bank Statements Folder (Production)         │
│           - Polls every minute for new/updated PDFs          │
│           - Folder: 1UYhIP6Nontc2vuE2G1aMvkggaEk6szv8        │
│                                                              │
│ Option B: Webhook Trigger (Testing)                          │
│           - POST /process-bank-statement                     │
│           - For manual testing with test PDFs                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 1. Download PDF                                             │
│    - Input: File ID from trigger                            │
│    - Output: Binary PDF data                                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Extract File Metadata (Code Node)                       │
│    - Parse filename for bank/date (backup only)             │
│    - Generate initial StatementID                           │
│    - Preserve binary data for next step                     │
│                                                              │
│    Output:                                                   │
│    {                                                         │
│      fileName: "Barclay_2025-11_Statement.pdf",            │
│      fileId: "abc123...",                                   │
│      bank: "Barclay" (from filename, may be "Unknown"),    │
│      year: "2025",                                          │
│      month: "11",                                           │
│      statementId: "STMT-Unknown-202511-..."                │
│    }                                                         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Build Anthropic API Request (Code Node) ✨ UPDATED       │
│    - Convert binary PDF to base64                           │
│    - Build Vision API request body                          │
│                                                              │
│    ✨ NEW PROMPT:                                            │
│    "Extract the bank name AND transactions from this PDF"   │
│                                                              │
│    Expected Response Format:                                 │
│    {                                                         │
│      "bank": "Barclay",                                     │
│      "transactions": [                                       │
│        {                                                     │
│          "date": "15.11.2025",                              │
│          "description": "REWE Supermarket",                 │
│          "amount": -42.50,                                  │
│          "currency": "EUR"                                  │
│        }                                                     │
│      ]                                                       │
│    }                                                         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Parse PDF with Anthropic Vision (HTTP Request)          │
│    - POST to https://api.anthropic.com/v1/messages         │
│    - Model: claude-sonnet-4-5                               │
│    - Analyzes PDF visual content                            │
│    - Returns JSON with bank + transactions                  │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Parse Anthropic Response (Code Node) ✨ UPDATED          │
│    - Strip markdown code fences (```json...```)             │
│    - Parse JSON response                                    │
│                                                              │
│    ✨ NEW LOGIC:                                             │
│    const bankFromVision = parsedData.bank || 'Unknown';    │
│    const statementId = `STMT-${bankFromVision}-...`;       │
│                                                              │
│    - Creates transaction objects with correct bank          │
│    - Each transaction gets:                                 │
│      - TransactionID                                        │
│      - Bank (from Vision AI, not filename!)                │
│      - StatementID (with correct bank)                      │
│      - Date, Amount, Description, Currency                  │
│      - Empty fields for matching: Vendor, Category, etc.    │
└─────────────────────────────────────────────────────────────┘
                          ↓
                    ┌─────┴─────┐
                    │             │
                    ↓             ↓
┌──────────────────────────┐  ┌──────────────────────────┐
│ 6A. Write Transactions   │  │ 6B. Log Statement Record │
│     to Database          │  │     ✨ UPDATED            │
│                          │  │                          │
│ Sheet: Transactions      │  │ Sheet: Statements        │
│                          │  │                          │
│ Writes ALL transactions  │  │ Writes ONE row:          │
│ with Bank field from     │  │ - StatementID (correct)  │
│ Vision AI extraction     │  │ - Bank (from Vision AI)  │
│                          │  │ - Month, Year            │
│ Example:                 │  │ - FileID, FilePath       │
│ Bank: "Barclay"          │  │ - ProcessedDate          │
│ (not "Unknown"!)         │  │ - TransactionCount       │
└──────────────────────────┘  └──────────────────────────┘
                    │             │
                    └─────┬─────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Move PDF to Archive                                      │
│    - Move processed PDF to Archive folder                   │
│    - Folder: 1uohhbtaE6qvS08awMEYdVP6BqgRLxgjH             │
│    - Keeps Bank-Statements folder clean                     │
└─────────────────────────────────────────────────────────────┘
```

## Key Changes Summary

### Before Fix:
1. **Extract File Metadata**: Tried to parse bank from filename → Often "Unknown"
2. **Build API Request**: Only asked for transactions
3. **Parse Response**: Used filename bank (often "Unknown")
4. **Log Statement**: Referenced wrong node name, never executed

### After Fix:
1. **Extract File Metadata**: Still parses filename (backup), preserves binary
2. **Build API Request**: ✨ Asks Claude to identify bank from PDF visual content
3. **Parse Response**: ✨ Uses bank from Claude Vision AI (accurate!)
4. **Log Statement**: ✨ Fixed node reference, now works correctly

## Data Flow: Bank Identification

### Old Flow (Filename-Based):
```
PDF Filename → Parse filename → bank = "Unknown" (if no match)
                                    ↓
                              Write "Unknown" to DB
                                    ↓
                              W3 can't filter by bank ❌
```

### New Flow (Vision AI-Based):
```
PDF Binary → Claude Vision AI → Identifies bank from logo/header
                                    ↓
                              bank = "Barclay" (accurate!)
                                    ↓
                              Write "Barclay" to DB
                                    ↓
                              W3 filters by bank correctly ✅
```

## Sheets Structure

### Transactions Sheet
```
| TransactionID | Date       | Bank    | Amount  | Description      | ReceiptID | MatchStatus |
|---------------|------------|---------|---------|------------------|-----------|-------------|
| STMT-Bar...01 | 15.11.2025 | Barclay | -42.50  | REWE Supermarket |           | unmatched   |
| STMT-Bar...02 | 16.11.2025 | Barclay | -89.00  | Amazon           |           | unmatched   |
| STMT-Mil...01 | 15.11.2025 | Miles & More | -120.00 | Lufthansa   |           | unmatched   |
```

### Statements Sheet (Previously Empty!)
```
| StatementID           | Bank         | Month | Year | FileID   | ProcessedDate       | TransactionCount |
|-----------------------|--------------|-------|------|----------|---------------------|------------------|
| STMT-Barclay-202509-... | Barclay      | 09    | 2025 | abc123   | 2026-01-28T11:00... | 38               |
| STMT-Barclay-202510-... | Barclay      | 10    | 2025 | def456   | 2026-01-28T11:01... | 42               |
| STMT-MilesMore-202509-...| Miles & More | 09    | 2025 | ghi789   | 2026-01-28T11:02... | 15               |
| STMT-MilesMore-202510-...| Miles & More | 10    | 2025 | jkl012   | 2026-01-28T11:03... | 18               |
```

## Testing Checklist

### 1. Verify Bank Extraction
- [ ] Upload Barclay statement → Bank = "Barclay"
- [ ] Upload Miles & More statement → Bank = "Miles & More"
- [ ] Upload unknown bank → Bank = actual bank name (or "Unknown" if Claude can't identify)

### 2. Verify Statements Sheet
- [ ] One row per processed statement
- [ ] Bank field populated correctly
- [ ] StatementID contains correct bank name
- [ ] TransactionCount matches actual transaction count

### 3. Verify Transactions Sheet
- [ ] All transactions have correct Bank field
- [ ] Bank matches the statement that created them
- [ ] No "Unknown" banks (unless truly unidentifiable)

### 4. Verify W3 Compatibility
- [ ] W3 can filter by Bank field
- [ ] Expensify receipts match to correct bank transactions only
- [ ] No cross-bank matching errors

## Error Handling Notes

**Current state:** Minimal error handling (warnings in validation)

**Recommended additions:**
1. Add error output to Anthropic API call (handle Vision failures)
2. Add error handling to Google Sheets writes (handle quota/permission errors)
3. Add fallback logic if Claude can't identify bank (default to filename parsing)

**Not critical for initial testing** - workflow will stop on errors, which is acceptable for debugging.

---

**Last Updated:** 2026-01-28
**Workflow Version:** Updated with bank identification via Vision AI
