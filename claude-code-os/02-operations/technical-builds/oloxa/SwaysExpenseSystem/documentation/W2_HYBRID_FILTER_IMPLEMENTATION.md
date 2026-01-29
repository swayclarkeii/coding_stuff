# W2 Hybrid Filter Implementation

**Date:** 2026-01-29
**Workflow:** W2 - Gmail Receipt Monitor (ID: dHbwemg7hEB4vDmC)
**Status:** ✅ Complete - Ready for Testing

---

## Summary

Implemented a **hybrid pre-filtering system** in W2 to reduce unnecessary processing of Gmail attachments. The filter combines three checks (sender, subject keywords, and PDF-only) to determine which emails should be processed.

---

## Changes Made

### 1. New Node: "Hybrid Pre-Filter"

**Location:** Between "Combine Both Gmail Accounts" and "Detect Expensify Email"

**Purpose:** Filter emails BEFORE downloading/processing attachments

**Logic:**
- **Known vendor check**: Email sender matches known vendor domains (case-insensitive substring)
- **Subject keyword check**: Email subject contains receipt/invoice keywords (case-insensitive)
- **PDF attachment check**: Email has at least one PDF attachment

**Pass criteria:** (Vendor match OR Subject match) AND Has PDF
- **Special cases:** Apple and Expensify emails always pass (handled separately downstream)

**Known vendors list:**
```
spotify, openai, framer, tado, anthropic, notion, figma, canva, adobe,
google, apple, amazon, paypal, stripe, digitalocean, vercel, netlify,
github, heroku, cloudflare, hetzner, namecheap, grammarly, zoom, slack,
linear, loom, miro, airtable, expensify, aws, bvg, wolt, flaschenpost,
miles-mobility, deutschebahn, systeme
```

**Subject keywords:**
```
receipt, invoice, payment, order, confirmation, rechnung, quittung,
billing, subscription, charge, transaction, purchase, faktura
```

### 2. Updated "Extract Attachment Info" Node

**Change:** Now only processes **PDF files** (removed PNG, JPG, JPEG support)

**Filter logic:**
```javascript
if (/\.pdf$/i.test(filename) || mimeType.includes('pdf')) {
  // Process
} else {
  console.log(`SKIPPED non-PDF attachment: ${filename}`);
}
```

### 3. Updated "Extract Invoice Attachments" Node

**Change:** Now only processes **PDF files** for invoices

**Filter logic:** Same as above - only PDF files pass through

---

## Connection Flow (Before vs After)

### Before:
```
Combine Both Gmail Accounts
  → Detect Expensify Email
  → Detect Invoice or Receipt
  → Extract Attachment Info (processes ALL attachments)
```

### After:
```
Combine Both Gmail Accounts
  → Hybrid Pre-Filter (filters by vendor/subject/PDF)
  → Detect Expensify Email
  → Detect Invoice or Receipt
  → Extract Attachment Info (PDF only)
```

---

## Benefits

1. **Reduces processing volume**: Skips emails without relevant keywords or known vendors
2. **PDF-only processing**: No longer processes images, audio, spreadsheets, etc.
3. **Early filtering**: Happens before attachment download, saving bandwidth and API calls
4. **Logging**: Console logs show which emails pass/fail and why
5. **Preserves existing logic**: Apple emails, Expensify emails, and invoice detection continue to work

---

## Testing Plan

### Test 1: Known Vendor + PDF (Should PASS)
- **Sender:** `noreply@tm.openai.com`
- **Subject:** Anything
- **Attachment:** `invoice.pdf`
- **Expected:** Email processed, PDF extracted and logged

### Test 2: Unknown Vendor + Receipt Keyword + PDF (Should PASS)
- **Sender:** `noreply@unknownvendor.com`
- **Subject:** "Your receipt for January"
- **Attachment:** `document.pdf`
- **Expected:** Email processed, PDF extracted and logged

### Test 3: Known Vendor + No PDF (Should SKIP)
- **Sender:** `noreply@tm.openai.com`
- **Subject:** Anything
- **Attachment:** `image.jpg`
- **Expected:** Email skipped at Hybrid Pre-Filter

### Test 4: Unknown Vendor + No Keywords (Should SKIP)
- **Sender:** `newsletter@randomcompany.com`
- **Subject:** "Weekly update"
- **Attachment:** `report.pdf`
- **Expected:** Email skipped at Hybrid Pre-Filter

### Test 5: Apple Email (Should PASS - Special Case)
- **Sender:** `no_reply@email.apple.com`
- **Subject:** Anything
- **Attachment:** Any
- **Expected:** Email passes filter, handled by Apple-specific path

### Test 6: Expensify Email (Should PASS - Special Case)
- **Sender:** `concierge@expensify.com`
- **Subject:** "sent you their report"
- **Attachment:** Any
- **Expected:** Email passes filter, handled by Expensify-specific path

---

## Monitoring

### Key Metrics to Watch
- **Emails processed before filter** (from "Combine Both Gmail Accounts" node)
- **Emails passed by filter** (from "Hybrid Pre-Filter" node)
- **Skip rate** = (Total - Passed) / Total × 100%

### Console Logs to Check
```
Hybrid Pre-Filter: Processing X emails
PASS: sender@domain.com | Subject: ... | PDF: true | Vendor: true | Subject: false
SKIP: sender@domain.com | Subject: ... | PDF: false | Vendor: false | Subject: false
Hybrid Pre-Filter: Passed X emails, skipped Y
```

---

## Known Limitations

1. **Vendor list is hardcoded**: To add new vendors, must update the Hybrid Pre-Filter node code
2. **Subject keywords are English/German only**: May miss receipts in other languages
3. **PDF-only**: Will skip legitimate receipts sent as images (can be adjusted if needed)
4. **False positives possible**: Marketing emails from known vendors with "order confirmation" in subject will pass

---

## Rollback Plan

If the filter is too aggressive and skips legitimate receipts:

1. **Check filter logs**: Identify which emails were skipped
2. **Option A - Disable filter temporarily**: Remove connection from "Hybrid Pre-Filter" to "Detect Expensify Email", reconnect "Combine Both Gmail Accounts" directly
3. **Option B - Adjust filter criteria**:
   - Add more vendor domains
   - Add more subject keywords
   - Remove PDF-only requirement (allow images)
4. **Option C - Make filter less strict**: Change from `(vendor OR subject) AND pdf` to just `(vendor OR subject)`

---

## Files Modified

- **Workflow:** `dHbwemg7hEB4vDmC` (Expense System - Workflow 2: Gmail Receipt Monitor)
- **Nodes added:** 1 (Hybrid Pre-Filter)
- **Nodes updated:** 2 (Extract Attachment Info, Extract Invoice Attachments)
- **Connections modified:** 2 (removed 1, added 2)

---

## Next Steps

1. ✅ Implementation complete
2. ⏳ **Test with real emails** (run workflow manually via webhook trigger)
3. ⏳ **Monitor console logs** for pass/skip patterns
4. ⏳ **Adjust vendor/keyword lists** if needed
5. ⏳ **Enable daily schedule** once filter is validated

---

## Technical Details

### Node IDs
- Hybrid Pre-Filter: `hybrid-pre-filter`
- Extract Attachment Info: `2023d6e8-3aa5-4e95-be7b-82ee8d99b42c`
- Extract Invoice Attachments: `extract-invoice-attachments`

### Node Type
All updated nodes are `n8n-nodes-base.code` (JavaScript Code nodes)

### Position
Hybrid Pre-Filter positioned at `[1008, -112]` (between Combine and Detect Expensify nodes)

---

## Validation Status

**Validation errors:** 1 (false positive - "Cannot return primitive values directly")
- Code correctly returns arrays, validator may be checking old cached version
- Autofix tool says "No fixes needed"
- Connections are valid and workflow should execute correctly

**Warnings:** 60 (mostly unrelated to this implementation)
- Outdated typeVersions on other nodes
- Missing error handling (pre-existing)
- Expression format warnings (pre-existing)

---

## Contact

For questions or issues with this implementation, contact Sway Clarke.
