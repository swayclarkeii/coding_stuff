# Prompt Improvements - Iteration 3 (Phase 2)

**Date:** 2026-01-28
**Based On:** Iteration 1 vs 2 comparative analysis
**Target:** Address 2 regressions identified in Iteration 2

---

## Changes Summary

### 1. Strengthen DIN276 Recognition
**Problem:** 251103_Kalkulation Schlossberg.pdf regressed from correct 10_Bautraegerkalkulation_DIN276 to incorrect 11_Verkaufspreise

**Root Cause:** Document contains both "Kalkulation" (calculation) and "Kaufpreisliste" (purchase price list), confusing the model

**Solution:** Add explicit boundary rules to Tier 2 prompt for 10_Bautraegerkalkulation_DIN276

### 2. Clarify Financing Memo Classification
**Problem:** OCP_Memo_New-KaulsCity.pdf showed inconsistency - one duplicate correct (26_Finanzierungsbestaetigung), other incorrect (35_Sonstiges_Allgemein)

**Root Cause:** "Memo" keyword triggering miscellaneous classification in some reasoning paths

**Solution:** Add explicit guidance in Tier 1 WIRTSCHAFTLICHE_UNTERLAGEN keywords and Tier 2 prompt for 26_Finanzierungsbestaetigung

### 3. Strengthen Contractor Quote Consistency
**Problem:** AN25700_GU_483564_Richtpreisangebot duplicates differed (37_Others vs 16_GU_Werkvertraege)

**Root Cause:** Inconsistent handling of "Richtpreisangebot" + "GU" keyword combination

**Solution:** Add consistency rule to Tier 2 prompt for 16_GU_Werkvertraege

---

## Detailed Prompt Changes

### Change 1: Tier 2 - 10_Bautraegerkalkulation_DIN276

**Add to existing prompt after keyword list:**

```
DO NOT CONFUSE WITH 11_Verkaufspreise (Sales Prices):

KEY DIFFERENCES to distinguish DIN276 calculations from sales price lists:

DIN276 Bauträgerkalkulation contains:
- DIN276 cost groups (100-800): Grundstück, Herrichten, Gebäude, etc.
- HK (Herstellkosten) = construction/manufacturing costs
- Developer profit margins, financing costs, sales costs
- Terms: Baukosten, Baunebenkosten, Projektentwicklung, Gewinn

Verkaufspreise (Sales Prices) contains:
- Customer-facing unit prices: "Kaufpreis WE" (purchase price per unit)
- Individual apartment/unit listings with end-buyer prices
- Terms: Verkaufspreis, Kaufpreis, Endpreis, Kundenpreis

FILENAME PRIORITY (Iteration 2 consistency rule):
- If filename contains "Kalkulation" → Check content structure FIRST
- If content shows DIN276 cost groups (100-800) OR "HK" (Herstellkosten) → 10_Bautraegerkalkulation_DIN276
- If content shows "Kaufpreis WE" or individual unit customer prices → 11_Verkaufspreise
- "Kaufpreisliste" in DIN276 context = internal pricing calculation, NOT customer sales prices

CRITICAL: A document can contain BOTH cost calculations AND sales prices in different sections. Prioritize the DOMINANT content type:
- If majority is DIN276 cost breakdown with developer calculations → 10_Bautraegerkalkulation_DIN276
- If majority is customer unit price list → 11_Verkaufspreise
```

### Change 2: Tier 1 - WIRTSCHAFTLICHE_UNTERLAGEN Keywords

**Update existing keywords section:**

```
WIRTSCHAFTLICHE_UNTERLAGEN (Financial/Economic Documents):

Keywords to identify:
- Finanzierung, Finanzierungsbestätigung, Darlehen, Kredit, Zinssatz
- Kalkulation, DIN276, Baukosten, Herstellkosten
- Verkaufspreise, Kaufpreise, Preisliste
- Angebot (if from bank/financial institution OR contains pricing)
- Werkvertrag, GU-Vertrag, Bauvertrag
- **Memo/Memorandum (if contains financial data: amounts, financing terms, capital requirements, loan conditions)**

DO NOT CONFUSE WITH SONSTIGES (Miscellaneous):
- "Memo" or "Memorandum" alone does NOT automatically mean SONSTIGES
- Check content: if memo contains financing key data → WIRTSCHAFTLICHE_UNTERLAGEN
  - Financing key data includes: project volume, capital requirement, loan amounts, interest rates, financing terms, collateral details
- If memo contains financial investment proposals or financing requests → WIRTSCHAFTLICHE_UNTERLAGEN
- Only classify as SONSTIGES if memo is general correspondence without financial specifics
```

### Change 3: Tier 2 - 16_GU_Werkvertraege (General Contractor Contracts)

**Add to existing prompt after keyword list:**

```
CONSISTENCY RULE for Contractor Quotes (Richtpreisangebot):

If filename contains:
- "GU" (Generalunternehmer/General Contractor) + "Angebot" OR "Richtpreisangebot" → ALWAYS 16_GU_Werkvertraege
- "Richtpreisangebot" + construction/building scope → Check for contractor identity (GU, Bauunternehmen)

DO NOT CONFUSE WITH 11_Verkaufspreise:
- Richtpreisangebot = contractor's bid/quote TO the developer (construction cost estimate)
- Verkaufspreise = sales prices FROM developer TO end customers
- Key distinction: contractor quotes describe construction work scope, customer prices describe unit features

FILENAME PRIORITY RULE:
- "GU" + any pricing document (Angebot, Richtpreisangebot, Quote) → 16_GU_Werkvertraege
- Ignore other filename elements if "GU" is present with pricing terms
```

### Change 4: Tier 2 - 26_Finanzierungsbestaetigung (Financing Confirmation)

**Add to existing prompt after keyword list:**

```
INCLUDES Financing Memos/Memorandums:

- Investment memos, financing proposals, capital requirement memos
- "Memo" or "Memorandum" that contains:
  - Project financing details (volume, capital needs, loan amounts)
  - Financing terms (interest rates, loan duration, security/collateral)
  - Bank financing offers or confirmations
  - Investment financing structures

Examples:
- "OCP_Memo_New-KaulsCity.pdf" with 60 Mio EUR financing request → 26_Finanzierungsbestaetigung
- "Finanzierungs-Memo Projekt X" with loan terms → 26_Finanzierungsbestaetigung
- "Investment Memorandum" with financing structure → 26_Finanzierungsbestaetigung

DO NOT CONFUSE WITH 35_Sonstiges_Allgemein:
- If document title contains "Memo" BUT content is financing-focused → 26_Finanzierungsbestaetigung
- Only classify as SONSTIGES if memo lacks financial specifics
```

---

## Expected Impact

### Regression Fixes

1. **DIN276 Classification**
   - Target: 251103_Kalkulation Schlossberg.pdf correctly identified as 10_Bautraegerkalkulation_DIN276
   - Expected: 100% accuracy for DIN276 vs Verkaufspreise distinction

2. **Financing Memo Consistency**
   - Target: OCP_Memo_New-KaulsCity.pdf duplicates both classified as 26_Finanzierungsbestaetigung
   - Expected: 100% duplicate consistency for financing memos

3. **Contractor Quote Consistency**
   - Target: AN25700_GU_483564_Richtpreisangebot duplicates both classified as 16_GU_Werkvertraege
   - Expected: 100% duplicate consistency for contractor quotes

### Overall Targets

- **Accuracy:** 88% → 92%+ (gain 4%+)
- **Duplicate Consistency:** 94% → 98%+ (gain 4%+)
- **No new regressions** in categories that improved in Iteration 2

---

## Implementation Notes

1. **Prompt-Only Changes:** No architecture modifications, no new classification codes
2. **Backward Compatible:** All variable contracts, folder routing, tracker mappings unchanged
3. **Integration Safe:** No impact on Chunk 0 or Pre-Chunk 0 workflows
4. **Easy Rollback:** Can revert to Iteration 2 prompts if needed

---

**Status:** Ready for implementation
**Next Step:** Apply changes to Chunk 2.5 workflow nodes
**Testing:** Run Iteration 3 on same 50 documents, compare to Iterations 1 & 2
