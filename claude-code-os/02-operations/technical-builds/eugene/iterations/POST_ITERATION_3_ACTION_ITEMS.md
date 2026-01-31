# Post-Iteration 3 Action Items

**Created:** 2026-01-28
**Status:** Pending Iteration 3 completion

---

## Priority 1: Analyze Iteration 3 Results

**After all 50 tests complete:**

1. **Generate comparative analysis**
   - Iteration 1 vs Iteration 2 vs Iteration 3
   - Focus on: accuracy, duplicate consistency, JSON parsing errors
   - Document: what improved, what regressed, what stayed same

2. **Assess Phase 2 prompt changes**
   - Did DIN276 boundary rules fix the regression? (251103_Kalkulation)
   - Did financing memo rules fix inconsistency? (OCP_Memo duplicates)
   - Did contractor quote rules fix inconsistency? (Richtpreisangebot duplicates)
   - What was the JSON parsing error rate? (Target: <5%)

3. **Make go/no-go decision**
   - If JSON errors <5% AND Phase 2 fixes worked → Proceed to Iteration 4 (BPS pilot)
   - If JSON errors >5% → Simplify prompts before BPS pilot
   - If Phase 2 fixes didn't work → Redesign boundary rules before BPS pilot

---

## Priority 2: BPS Framework Pilot (If Iteration 3 is stable)

**Goal:** Test hybrid BPS approach on single category to validate improvement without breaking system

### Pilot Scope

**Target Category:** 10_Bautraegerkalkulation_DIN276
- **Why this category:** Persistent regression problem (Iteration 2 → Iteration 3)
- **Current accuracy:** TBD after Iteration 3
- **Target accuracy:** 100% on DIN276 vs Verkaufspreise distinction

### Pilot Changes

**Add to Tier 2 prompt for category 10:**

1. **Role section** (top):
   ```markdown
   You are analyzing construction cost calculations (Bauträgerkalkulation) using DIN276 standard.
   Your expertise: Distinguishing developer cost calculations from customer sales prices.
   ```

2. **Structured Examples** (3 examples):
   - Example 1: Clear DIN276 with cost groups 100-800
   - Example 2: Ambiguous filename with mixed content (DIN276 + prices)
   - Example 3: Sales price list misnamed as "Kalkulation"

3. **Guardrails section** (bottom):
   ```markdown
   **Always:**
   - Check for DIN276 cost groups (100-800) or "HK" (Herstellkosten)
   - Prioritize filename if it contains "Bautraegerkalkulation" or "DIN276"
   - Return JSON only

   **Never:**
   - Classify as 11_Verkaufspreise if document shows DIN276 structure
   - Ignore cost group structure when present
   - Return plain text explanations
   ```

**Keep unchanged:**
- Keyword lists
- DO NOT CONFUSE WITH section
- Technical style

### Pilot Testing

**Test dataset:** 10 documents containing "Kalkulation" in filename
- 5x should be 10_Bautraegerkalkulation_DIN276
- 5x should be 11_Verkaufspreise

**Success criteria:**
- 100% accuracy on 10 test documents
- Zero JSON parsing errors
- Duplicate consistency maintained

**Rollback plan:** Revert category 10 prompt to Iteration 3 version

### If Pilot Succeeds

**Iteration 4 expansion:** Apply hybrid BPS to problem categories:
- 16_GU_Werkvertraege
- 26_Finanzierungsbestaetigung
- 11_Verkaufspreise

**Iteration 5:** Migrate all 38 categories to hybrid BPS structure

---

## Priority 3: Fix Workflow Duplicate Write Issue

**Problem:** Eugene Quick Test Runner writes 2 rows per test instead of 1

**Impact:**
- 50 tests → 100 rows in sheet (confusing)
- Complicates analysis
- Wastes storage

**Investigation needed:**
- Check "Prepare Log Data" → "Append to Test_Results" connection
- Likely: Google Sheets node receiving data twice from upstream
- Possible: Workflow executing append operation twice

**Fix:** TBD after investigation

---

## Priority 4: Production Readiness Decision

**After Iteration 3/4 results:**

**Criteria for production:**
- ✅ 90%+ overall accuracy
- ✅ 95%+ duplicate consistency
- ✅ <5% JSON parsing errors
- ✅ No critical category regressions
- ✅ Integration compatibility verified

**Current status (after Iteration 2):**
- 88% accuracy (need +2%)
- 94% consistency (need +1%)
- 0% JSON errors (Iteration 2) / TBD% (Iteration 3)
- 1 critical regression (DIN276)
- Integration verified ✅

**If production ready:**
- Update Chunk 2.5 to Iteration N (best version)
- Document final configuration
- Close out Eugene project phase

**If not production ready:**
- Continue to Iteration 4/5 with BPS pilot
- Focus on remaining accuracy gaps

---

## Summary Checklist

- [ ] Iteration 3 completes (all 50 tests)
- [ ] Comparative analysis generated (Iter 1 vs 2 vs 3)
- [ ] JSON parsing error rate calculated
- [ ] Phase 2 fixes validated (DIN276, OCP_Memo, Richtpreisangebot)
- [ ] Go/no-go decision made for BPS pilot
- [ ] If go: BPS pilot executed on category 10
- [ ] If successful: Expand BPS to 3-4 categories
- [ ] If very successful: Plan full migration
- [ ] Production readiness assessment
- [ ] Fix duplicate write issue in test runner

---

**Next Review:** After Iteration 3 completes (~04:25 CET)
**Responsible:** Claude Code
**Priority:** High - blocks production deployment
