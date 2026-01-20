# Workflow 2 v2.1 - Test Plan

## Quick Test Checklist

### Test 1: Apple Email WITHOUT Attachment ✅

**Setup:**
- Forward a real Apple Store receipt email to monitored Gmail
- Ensure email has NO PDF attachment
- Email should have HTML body with receipt details

**Expected Results:**
- [ ] Email detected as Apple email (check n8n logs)
- [ ] HTML extracted successfully
- [ ] PDF generated with filename: `Apple_Receipt_[DATE]_$[AMOUNT].pdf`
- [ ] PDF uploaded to Google Drive folder `1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4`
- [ ] OCR runs on generated PDF
- [ ] Amount extracted (check Google Sheets)
- [ ] Google Sheets entry created with:
  - Vendor: "Apple"
  - Notes: contains "Converted from Apple email HTML"

**Where to Check:**
- n8n execution log: Workflow 2 (ID: `dHbwemg7hEB4vDmC`)
- Google Drive: Check Receipts folder for new PDF
- Google Sheets: Check "Receipts" sheet for new row

---

### Test 2: Regular Vendor WITH Attachment ✅

**Setup:**
- Use existing workflow (should already work from v2.0)
- Email from vendor like Anthropic, OpenAI, AWS

**Expected Results:**
- [ ] Email NOT detected as Apple (goes to regular path)
- [ ] PDF attachment extracted
- [ ] Uploaded to Drive
- [ ] OCR runs
- [ ] Amount extracted
- [ ] Google Sheets entry created

**Validation:** This should work exactly as v2.0 (no changes to this path)

---

### Test 3: Apple Email WITH Attachment (Edge Case) ⚠️

**Setup:**
- Apple email that DOES have PDF attachment

**Expected Results:**
- [ ] Email detected as "Apple but has attachment"
- [ ] Goes to regular attachment path (Output 1 of IF node)
- [ ] **Skipped** by Extract Attachment Info (due to Apple filter)
- [ ] **No processing occurs**

**Note:** This is expected behavior. Apple rarely sends both HTML and PDF. Current implementation prioritizes PDF attachments over HTML conversion.

---

## Detailed Test Scenarios

### Scenario A: First-Time Apple Email

**Goal:** Verify complete Apple email flow from start to finish

**Steps:**
1. Activate Workflow 2 in n8n
2. Forward Apple receipt email to monitored Gmail account
3. Wait for next schedule run (or trigger manually)
4. Monitor execution:
   - Check "Detect Apple Emails (IF)" node output
   - Verify "Extract Apple Email HTML" receives email
   - Check "Prepare PDF Conversion Request" creates binary
   - Verify "Upload Apple Receipt PDF" completes
   - Confirm "Add PDF Metadata" passes data
   - Check "Merge Apple & Regular Receipts" combines
5. Verify outputs:
   - Google Drive: New PDF file exists
   - PDF quality: Open and read receipt
   - Google Sheets: New row with Apple vendor

**Success Criteria:**
- ✅ Execution completes without errors
- ✅ PDF readable and properly formatted
- ✅ Amount extracted correctly (within $0.10)
- ✅ All metadata fields populated

---

### Scenario B: Duplicate Apple Email

**Goal:** Test duplicate prevention (or lack thereof - known limitation)

**Steps:**
1. Run Scenario A first (create initial entry)
2. Run workflow again with SAME Apple email
3. Check results

**Expected Behavior:**
- ⚠️ **DUPLICATE ENTRY CREATED** (known limitation)
- Google Drive: New PDF file with same filename
- Google Sheets: Duplicate row

**Why:** Apple emails don't have attachments to deduplicate by filename. Email body generates new PDF each time.

**Mitigation:** Manual deletion or future enhancement (check messageId)

---

### Scenario C: Amount Extraction Accuracy

**Goal:** Verify amount parsing from Apple email HTML

**Test Cases:**
| Email HTML Contains | Expected Amount |
|---------------------|-----------------|
| `Total: $25.99` | 25.99 |
| `Amount $100.00` | 100.00 |
| `Sum: 9,99 EUR` | 9.99 |
| `You paid $15.49` | 15.49 |
| No clear amount | (empty - relies on OCR) |

**Steps:**
1. For each test case, create sample Apple email
2. Run workflow
3. Check Google Sheets "Amount" column

**Success Criteria:**
- ✅ Standard formats extracted correctly
- ✅ Empty amounts don't cause errors
- ✅ OCR fallback works when HTML parsing fails

---

### Scenario D: HTML-to-PDF Conversion Quality

**Goal:** Assess Google Drive's HTML conversion output

**Test Elements:**
- [ ] Text readability (font size, formatting)
- [ ] Images display (if present in email)
- [ ] Tables render correctly (product lists)
- [ ] Colors preserved (Apple branding)
- [ ] Links removed/converted to text
- [ ] Page breaks appropriate

**Steps:**
1. Send test Apple email with various HTML elements
2. Download generated PDF from Drive
3. Visual inspection

**Acceptance:**
- ✅ Text is readable (minimum 10pt font)
- ✅ No major layout issues
- ⚠️ Minor formatting differences acceptable (Google Drive conversion is basic)

---

## Rollback Plan

**If v2.1 causes issues:**

1. **Deactivate Workflow:**
   - Open n8n
   - Toggle workflow to "Inactive"

2. **Identify Rollback Point:**
   - Check execution logs for last successful v2.0 run
   - Note execution ID

3. **Restore Previous Version:**
   - Option A: Delete new nodes manually in n8n UI
   - Option B: Re-import v2.0 workflow JSON (if archived)
   - Option C: Use n8n version history (if enabled)

4. **Verify Rollback:**
   - Run test with regular vendor attachment
   - Confirm v2.0 functionality works
   - Document issue for future fix

---

## Monitoring After Deployment

### First Week

**Check daily:**
- Google Sheets for new entries
- Look for Apple vendor entries
- Verify "Converted from Apple email HTML" note
- Check PDF quality in Drive

**Watch for:**
- Duplicate entries from same Apple email
- Missing amounts (OCR failures)
- Broken PDFs (conversion issues)
- Execution errors in n8n

### Ongoing

**Check weekly:**
- Execution count (should match expected email volume)
- Error rate (should be <5%)
- Apple email success rate

**Monthly review:**
- Total Apple emails processed
- Amount extraction accuracy
- Any manual corrections needed

---

## Troubleshooting Guide

### Issue: Apple email not detected

**Symptoms:**
- Apple email goes to regular attachment path
- No PDF generated from email body

**Checks:**
1. Verify email is from `@apple.com` domain
2. Check if email has attachments (binary count > 0)
3. Review "Detect Apple Emails (IF)" node execution output

**Fix:**
- If sender domain different, update IF node condition
- If email has attachment, expected behavior (regular path handles it)

---

### Issue: HTML extraction fails

**Symptoms:**
- "Extract Apple Email HTML" node shows 0 items
- No HTML body found

**Checks:**
1. Inspect email structure in "Combine Both Gmail Accounts" output
2. Check `email.payload.parts` structure
3. Verify `mimeType: "text/html"` part exists

**Fix:**
- Update HTML extraction logic to handle email format
- Add error logging to identify structure

---

### Issue: PDF conversion produces unreadable file

**Symptoms:**
- PDF generated but text garbled
- Images missing or broken
- Layout completely wrong

**Checks:**
1. Download generated PDF from Drive
2. Check original email HTML in n8n execution
3. Verify "Prepare PDF Conversion Request" wrapped HTML correctly

**Fixes:**
- Adjust CSS in HTML wrapper
- Remove problematic HTML elements
- Consider external PDF conversion service

---

### Issue: Amount not extracted

**Symptoms:**
- Google Sheets entry has empty "Amount" field
- Both HTML parsing and OCR failed

**Checks:**
1. Check "Extract Apple Email HTML" output for extractedAmount
2. Check "Parse Amount from OCR Text" output
3. Review original email HTML for amount format

**Fixes:**
- Update amount regex pattern
- Add additional amount formats
- Manual entry acceptable for edge cases

---

## Success Metrics

**After 1 Week:**
- [ ] 100% of Apple emails detected and processed
- [ ] <10% amount extraction failures
- [ ] 0 workflow execution errors
- [ ] <5 minutes average processing time per email

**After 1 Month:**
- [ ] Zero duplicate cleanup needed (or automated)
- [ ] Amount extraction accuracy >90%
- [ ] No manual PDF conversions needed

---

## Quick Command Reference

**View workflow:**
```bash
# n8n UI: https://n8n.oloxa.ai/workflow/dHbwemg7hEB4vDmC
```

**Check Google Sheets:**
```bash
# Spreadsheet ID: 1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM
# Sheet name: Receipts
```

**Check Google Drive folder:**
```bash
# Folder ID: 1NP5y-HvPfAv28wz2It6BtNZXD7Xfe5D4
# Name: Receipts (Gmail attachments)
```

**Manual workflow trigger:**
```bash
# Use webhook: POST to https://n8n.oloxa.ai/webhook/test-expense-w2
```

---

## Test Data Recommendations

**Good test Apple email should have:**
- Clear receipt subject line
- HTML body with product details
- Total amount clearly marked
- Date of purchase
- Order number or transaction ID

**Where to get test data:**
- Forward real Apple Store receipt
- iTunes/App Store purchase receipt
- Apple Support invoice
- Apple Music/iCloud subscription receipt

---

## Completion Checklist

Before marking v2.1 as "Production Ready":

- [ ] Scenario A tested successfully
- [ ] Scenario C tested (amount extraction) with 3+ formats
- [ ] Scenario D assessed (PDF quality acceptable)
- [ ] Duplicate behavior documented and accepted
- [ ] Rollback plan tested
- [ ] Monitoring schedule established
- [ ] Team trained on new functionality
- [ ] Documentation updated in project wiki
