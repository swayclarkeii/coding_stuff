# BPS Prompt Test Report - Leonor Transcript

**Date:** 2026-01-28
**Workflow ID:** cMGbzpq1RXpL0OHY
**Execution ID:** 6480
**Test Type:** Data Extraction Accuracy (Quantified Values vs Invention)
**Status:** ❌ **TEST FAILED - Workflow Configuration Error**

---

## Summary

- **Total tests:** 1 (Leonor transcript)
- **❌ Failed:** 1
- **Test outcome:** Cannot validate - workflow did not process the submitted transcript

---

## Test Execution Details

### Test: Leonor @ Ambushed.tv Transcript Analysis

**Status:** ❌ FAIL
**Execution ID:** 6480
**Final status:** error
**Failed at node:** Parse AI Response
**Duration:** 55.5 seconds

---

## Root Cause Analysis

### Issue 1: Workflow Not Using Webhook Input ⚠️ CRITICAL

**Finding:** The workflow processed hardcoded test data instead of the Leonor transcript submitted via webhook.

**Evidence:**
- Submitted transcript: Leonor @ Ambushed.tv (738 lines, HR coordinator interview)
- AI analyzed instead:
  1. Fathom demo call transcript
  2. Eugene's document handling transcript
  3. Benito's property search transcript

**Impact:** Cannot validate BPS prompts against test expectations because wrong data was processed.

**Recommendation:** Fix workflow to accept and use webhook `data.transcript` parameter.

---

### Issue 2: JSON Parsing Error (Secondary)

**Error:** `Unexpected token '`', "```json [line 18]"`

**Cause:** OpenAI returned JSON wrapped in markdown code fences:
```
```json
{
  "summary": "...",
  ...
}
```
```

But the "Parse AI Response" node expected pure JSON without backticks.

**Impact:** Even if correct data had been processed, the workflow would have failed at parsing.

**Recommendation:** Update parsing logic to strip markdown code fences before JSON.parse().

---

## AI Output Analysis (Wrong Transcripts)

Despite processing wrong data, I can assess the AI's behavior on the test transcripts it DID analyze:

### Transcript 1: Fathom Demo Call

**Quantified data mentioned:**
- ❌ **INVENTED:** "5-30 minutes to provide recordings" - NOT in test expectations
- ❌ **INVENTED:** "within 5 seconds" for instant recordings - NOT in test expectations

**Assessment:** AI appears to be inventing specific numbers. This is exactly what the test was designed to catch.

### Transcript 2: Eugene Document Handling

**Quantified data handling:**
- ✅ **CORRECT:** "[Not quantified in call]" appears 3 times
- ✅ **CORRECT:** AI correctly acknowledged missing data for:
  - Manual document handling time
  - Data verification delay time
  - 6 clients per year goal (mentioned but no time quantification)

**Assessment:** Good - AI is marking unquantified data appropriately when numbers aren't provided.

### Transcript 3: Benito Property Search

**Quantified data handling:**
- ✅ **CORRECT:** "[Not quantified in call]" appears 2 times
- ✅ **CORRECT:** AI acknowledged missing quantification for manual search time

**Assessment:** Consistent behavior - marking missing data appropriately.

---

## Validation Against Test Expectations

### ❌ Cannot Validate - Wrong Transcript Processed

**Expected to extract from Leonor transcript:**
- Line 251: "5 minutes" per rate raise call
- Line 268: "€20/hour" rate
- Line 284: "€17/hour" current rate
- Line 299: "once every three months" discrepancy frequency
- Line 413: "up to three hours" per sanitization
- Line 460: "6 projects per freelancer"
- Line 633: "half an hour" monthly alignment

**Actual:** None of these values were tested because Leonor transcript was never analyzed.

---

## Workflow Errors

### Error 1: Input Data Routing

**Node:** Route: Webhook or API
**Issue:** Webhook trigger received data but workflow branch processed hardcoded test data
**Fix Required:** Update conditional logic to route webhook data to AI analysis nodes

### Error 2: JSON Parsing

**Node:** Parse AI Response
**Error Message:** `Unexpected token '`', "```json [line 18]"`
**Fix Required:** Add markdown code fence stripping before JSON.parse():

```javascript
// Before
const parsed = JSON.parse($input.item.json.message.content);

// After
const content = $input.item.json.message.content;
const cleaned = content.replace(/```json\n?/g, '').replace(/```\n?/g, '');
const parsed = JSON.parse(cleaned);
```

---

## Mixed Signal Analysis (From Wrong Data)

While the wrong transcripts were processed, the AI's behavior on those transcripts shows:

**✅ Positive Signals:**
1. AI correctly used "[Not quantified in call]" when data was missing (Eugene and Benito transcripts)
2. AI acknowledged missing labor rates for ROI calculations
3. AI did not fabricate quotes from speakers

**❌ Negative Signals:**
1. AI invented specific numbers in Fathom transcript ("5-30 minutes", "5 seconds") without source citations
2. No line number citations to verify where data came from
3. Cannot confirm if AI extracts vs invents when quantified data IS present (Leonor case)

---

## Test Outcome

### Primary Test: ❌ FAILED (Cannot Validate)

**Reason:** Workflow processed wrong input data. The Leonor transcript with rich quantified data (5 min, €20/hr, 3 hours, etc.) was never analyzed.

### Secondary Observation: ⚠️ WARNING

**Finding:** AI shows inconsistent behavior:
- Good: Marks missing data as "[Not quantified in call]"
- Bad: Invents specific numbers in some cases (Fathom example)

**Cannot conclude** if BPS prompts extract vs invent quantified data because the designed test case (Leonor transcript with known numbers) was never executed.

---

## Next Steps

### Immediate (Before Re-Test)

1. **Fix webhook input routing** - Ensure workflow uses `data.transcript` from webhook
2. **Fix JSON parsing** - Strip markdown code fences before JSON.parse()
3. **Add input validation** - Confirm webhook data is received before AI analysis
4. **Add execution logging** - Log which transcript is being processed

### After Fixes (Re-Test Required)

1. **Re-run test with Leonor transcript** - Verify workflow processes correct data
2. **Validate extraction accuracy:**
   - Does AI extract "5 minutes" from line 251?
   - Does AI extract "€20/hour" from line 268?
   - Does AI extract "3 hours" from line 413?
   - Does AI extract "half an hour" from line 633?
3. **Check for invention:**
   - Does AI cite line numbers for quantified data?
   - Does AI invent numbers NOT in transcript?
   - Does AI invent quotes NOT spoken?

---

## Files

**Test Input:** `/Users/computer/coding_stuff/claude-code-os/Fathom Transcripts/January 27th, 2026/leonor@ambushed.tv - January 27th, 2026 - Transcript.txt`
**Test Expectations:** `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/leonor_transcript_test_expectations_v1.0_2026-01-28.md`
**This Report:** `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/ai-audits/leonor_bps_test_report_v1.0_2026-01-28.md`

---

## Conclusion

**Test Result:** ❌ Cannot validate BPS prompt accuracy
**Blocker:** Workflow configuration error - processed wrong input data
**Action Required:** Fix workflow webhook handling before re-testing
**Timeline:** Re-test after workflow fixes (estimate: 1-2 hours to fix + 5 minutes to re-test)

---

*Report generated by test-runner-agent on 2026-01-28*
