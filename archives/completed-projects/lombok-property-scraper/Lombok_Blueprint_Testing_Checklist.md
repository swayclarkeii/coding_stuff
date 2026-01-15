# Lombok Blueprint v6 - Testing Checklist

**Date:** 2026-01-08
**Updated Blueprint Location:** `/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v6.blueprint.json`

---

## ✅ Pre-Import Checklist

- [ ] Backup current working blueprint (v5) in Make.com
- [ ] Download current scenario as JSON backup
- [ ] Note down current scenario ID
- [ ] Verify v6 blueprint file exists at location above

---

## 🔧 Import & Configuration

### 1. Import Blueprint
- [ ] Go to Make.com → Scenarios
- [ ] Click "Create a new scenario"
- [ ] Click the three dots menu → "Import Blueprint"
- [ ] Select: `Lombok invest capital Property Scraper v6.blueprint.json`
- [ ] Wait for import to complete

### 2. Verify Variable Module
- [ ] First module should be: "🔧 Configuration Variables"
- [ ] Check variables are set:
  - [ ] `userEmail` = swayclarkeii@gmail.com
  - [ ] `notificationEmail` = sway@oloxa.ai
  - [ ] `spreadsheetId` = 1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54
  - [ ] `dataStoreId` = 81942
  - [ ] `workflowName` = Lombok Invest Capital Property Scraper

### 3. Reconnect Integrations
- [ ] Google Sheets - reconnect if needed
- [ ] Gmail - reconnect if needed
- [ ] Apify - reconnect if needed
- [ ] DataStore - verify ID is correct

### 4. Verify Module 515 Updates
- [ ] Open module 515 "Send New Leads (Unified)"
- [ ] Subject line shows: "🎉 You Got {{length(508.array) + length(260.array) + length(261.array)}} New Lombok Leads!"
- [ ] Email body shows formatted table with Task 1, 2, 3 counts
- [ ] "To" field shows: `{{1.notificationEmail}}`

---

## 🧪 Test Run (Small Data)

### 5. Initial Test
- [ ] Set scenario to run ONCE (not scheduled)
- [ ] Trigger with small test data if possible
- [ ] Monitor execution in real-time

### 6. Check Variable References
- [ ] Verify variable module outputs values
- [ ] Check subsequent modules can access `{{1.userEmail}}`, etc.
- [ ] No errors about undefined variables

### 7. Verify Email Output
- [ ] Check inbox for "New Leads" email
- [ ] Email subject includes property count (e.g., "You Got 5 New Lombok Leads!")
- [ ] Email body shows:
  - [ ] Task 1 count (number of properties)
  - [ ] Task 2 count
  - [ ] Task 3 count
  - [ ] Total count (sum)
  - [ ] Run timestamp
  - [ ] "View Full Report" button works
- [ ] Attachment is present (spreadsheet export)

### 8. Check Data Store Operations
- [ ] New properties are added to data store
- [ ] Duplicates are detected and skipped
- [ ] No errors about dataStoreId

### 9. Verify Google Sheets Writing
- [ ] RAW data sheet created with today's date
- [ ] Property data written correctly
- [ ] Spreadsheet ID variable worked (`{{1.spreadsheetId}}`)

---

## 🛡️ Error Handler Testing (Optional)

### 10. Test Error Scenarios (CAREFULLY)
Only test these in a non-production environment or duplicate scenario:

- [ ] **Gmail Error Test**: Temporarily disconnect Gmail connection
  - Expected: Error logged to sheet OR error email sent
  - Re-connect Gmail after test

- [ ] **DataStore Error Test**: Use invalid datastore ID temporarily
  - Expected: Error notification email received
  - Restore correct ID after test

- [ ] **Google Sheets Quota Test**: (Skip this unless needed)
  - Can't easily test without hitting quota
  - Just verify error handler is attached to Sheets modules

---

## 📊 Production Validation

### 11. Full Production Run
- [ ] Set scenario to scheduled (bi-weekly as needed)
- [ ] Run with REAL data (full Apify datasets)
- [ ] Monitor operation count (should be ~150-200)

### 12. Validate Production Results
- [ ] Email received with accurate counts
- [ ] All properties written to sheet
- [ ] Duplicates properly filtered
- [ ] No execution errors
- [ ] Check Make.com operation usage

---

## 🎯 Success Criteria

✅ **All Must Pass:**
1. Variable module loads and provides values
2. Email includes property counts from all 3 tasks
3. No hardcoded emails visible in execution logs
4. DataStore operations work with variable ID
5. Google Sheets operations work with variable ID
6. Email arrives in inbox successfully
7. Attachment is present and correct
8. Total operation count < 250 per run

---

## ⚠️ Rollback Plan (If Needed)

If v6 has issues:
1. Go to scenario settings → "Import Blueprint"
2. Import your v5 backup JSON
3. Reconnect integrations
4. Resume old schedule
5. Report issues to me with error logs

---

## 📝 Post-Test Actions

After successful testing:
- [ ] Update scenario name to "Lombok Invest Capital Property Scraper v6"
- [ ] Add tags: "production", "property-scraper", "lombok"
- [ ] Document any custom changes in scenario notes
- [ ] Archive v5 blueprint for reference
- [ ] Monitor first 3 scheduled runs for consistency

---

## 🆘 Common Issues & Fixes

### Issue: "Variable 1.notificationEmail is undefined"
**Fix:** Variable module might not be first. Move it to position 0.

### Issue: "Email shows {{length(508.array)}}" literally
**Fix:** Check that aggregators 508, 260, 261 are connected properly to the email flow.

### Issue: "DataStore operation failed"
**Fix:** Verify dataStoreId variable is set correctly and datastore exists in Make.com.

### Issue: "Email counts show 0 even with data"
**Fix:** Ensure aggregators are properly filtering (exist = false for new properties).

---

## 📞 Need Help?

If you encounter issues:
1. Take screenshot of error
2. Copy error message
3. Note which module failed (module ID)
4. Check if it's related to variables or connections
5. Ask me for help with specific error details

---

**End of Testing Checklist**
