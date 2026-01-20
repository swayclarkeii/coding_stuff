# Terminology Analysis Across All 4 Websites (Task 1)

**Date:** December 11, 2024
**Purpose:** Determine if regex failures are consistent across all websites and identify actual terminology used

---

## Executive Summary

**Question 1:** Is the regex failure consistent across all 4 websites?
**Answer:** ✅ **YES** - But for different reasons per website

**Question 2A:** Are we searching for the wrong terms for "under construction"?
**Answer:** ✅ **YES** - Websites use "**completion**" and "**near completion**" which we're not catching

**Question 2B:** Is "off-plan" the right terminology?
**Answer:** ✅ **YES, BUT** - "off-plan" IS used (found on Reef Property), but we have no test cases in v2 to validate detection

---

## 🔍 Website-by-Website Analysis

### 1. Discover Lombok Property (9 "Unknown" properties)

**Properties tested:**
1. ✅ **Commercial Shop** - "Building **completion**: December 2026"
2. ✅ **Land properties** (8 properties) - Raw land with no construction info

**Terminology found:**
- ✅ Uses "**completion**" (not "construction")
- ✅ Uses "December 2026" format (month + year)
- ❌ Does NOT use "under construction", "in construction", "in progress", "being built"

**Regex failure reason:**
- Commercial Shop: Uses "**completion**" which our regex doesn't check
- Land properties: Correctly labeled "Unknown" (raw land has no construction status)

**Expected breakdown:**
- 1 property should be "Under Construction" (Commercial Shop)
- 8 properties correctly "Unknown" (raw land)

---

### 2. Island Properties Lombok (11 "Unknown" properties)

**Properties tested:**
1. ✅ **Hilltop Villa** - Blocked by authentication (requires login)
2. ✅ **Renovated 3-Bedroom** - "freshly renovated and fully furnished" (completed villa)
3. **Other properties:** Mostly land listings

**Terminology found:**
- ✅ Uses "**renovated**" (indicates completed)
- ⚠️ Most detail pages blocked by authentication
- Properties are mix of villas and land

**Regex failure reason:**
- Authentication barrier prevents access to construction status fields
- Properties that ARE visible (like Renovated villa) don't show construction timeline

**Expected breakdown:**
- 2-3 properties might be "Completed" (Hilltop Villa, Renovated villa, Green Valley villa - all from Benito's approved list)
- 8-9 properties correctly "Unknown" (land or auth-blocked)

**NOTE:** Hilltop Villa (Row 11) was APPROVED by Benito, suggesting it's completed, but we can't verify due to authentication

---

### 3. Reef Property Lombok (2 "Unknown" properties)

**Properties tested:**
1. ✅ **RECENTLY SOLD page** - Shows "Villa Aloha: **near completion**" + "**off-plan opportunity**"

**Terminology found:**
- ✅ Uses "**near completion**" (variation of "completion")
- ✅ Uses "**off-plan**" (CONFIRMED - this terminology IS used!)

**Regex failure reason:**
- "near completion" not matched by our regex (we check "under construction" but not "completion")
- These are "RECENTLY SOLD" pages (aggregation pages) not individual property pages

**Expected breakdown:**
- Both properties are sold property galleries (not active listings)
- May not be relevant for filtering

**CRITICAL FINDING:** ✅ **"Off-plan" terminology IS used by Reef Property!**

---

### 4. Nour Estates (5 "Completed" properties) ⭐

**Properties tested:**
1. ✅ All 5 properties correctly detected as "Completed"

**Terminology found:**
- ✅ Uses "**Built**" (matched by our regex)
- ✅ Uses "**Off-Plan**" (Row 9 - NOT in v2, completely missing)
- ✅ Uses "**Under Construction**" (Row 9 - NOT in v2)

**Regex success:**
- 100% success rate for "Completed" detection
- "Off-Plan" and "Under Construction" properties ARE being excluded (not in v2 at all)

**Expected breakdown:**
- 5 "Completed" ✅ CORRECT
- 0 "Off-Plan" or "Under Construction" in v2 (correctly excluded from scrape)

---

## 🎯 TERMINOLOGY USED BY WEBSITES

### ✅ TERMINOLOGY WE'RE CATCHING:

| Term | Regex | Found On | Detection Status |
|------|-------|----------|------------------|
| "built" | `/\bbuilt\b/i` | Nour Estates | ✅ Working |
| "completed" | `/\bcompleted\b/i` | Nour Estates | ✅ Working |
| "under construction" | `/\bunder construction\b/i` | Nour Estates (Row 9) | ✅ Working (but Row 9 not in v2) |
| "off-plan" | `/\boff[\s-]?plan\b/i` | Nour Estates (Row 9), Reef Property | ✅ Working (but Row 9 not in v2) |

---

### ❌ TERMINOLOGY WE'RE MISSING:

| Term | Found On | Example | Should Detect As |
|------|----------|---------|------------------|
| "**completion**" | Discover Lombok | "Building **completion**: December 2026" | Under Construction |
| "**near completion**" | Reef Property | "Villa Aloha **near completion**" | Under Construction |
| "**renovated**" | Island Properties | "freshly **renovated**" | Completed |
| "**ready**" | Multiple | "ready to move", "ready to occupy" | Completed |
| "**available from [future date]**" | Discover Lombok | "available from January 2026" | Under Construction |

---

## 📊 SUMMARY BY WEBSITE

### Consistent Pattern: YES (but different reasons)

| Website | Total Unknown | Likely Mislabeled | Correctly Unknown | Primary Issue |
|---------|---------------|-------------------|-------------------|---------------|
| **Discover Lombok** | 9 | 1 (Commercial Shop) | 8 (raw land) | Missing "**completion**" keyword |
| **Island Properties** | 11 | 2-3 (villas) | 8-9 (land/auth) | Authentication barrier |
| **Reef Property** | 2 | 0 (sold pages) | 2 (aggregation) | Scraping wrong page type |
| **Nour Estates** | 0 | 0 | 0 | ✅ 100% working |

**Total mislabeled:** ~3-4 properties out of 22 "Unknown"
**Correctly "Unknown":** ~18-19 properties (raw land, auth-blocked, or genuinely no info)

---

## 🔍 ANSWERING THE TWO QUESTIONS

### Question 1: Is this consistent across all websites?

**Answer:** ✅ **YES** - The regex is failing across all websites, but for different reasons:

1. **Discover Lombok:** Uses "**completion**" instead of "construction" → Our regex misses it
2. **Island Properties:** Authentication blocks access → Can't see construction status fields
3. **Reef Property:** Uses "**near completion**" → Our regex misses this variation
4. **Nour Estates:** ✅ 100% working (uses "Built" which we catch)

**Consistent problem:** We're searching for "under construction" but websites use "**completion**" variants

---

### Question 2A: Are we searching for wrong terms (under construction)?

**Answer:** ✅ **YES** - We need to ADD "**completion**" to our search terms

**Current search terms:**
```javascript
'under construction', 'in construction', 'in progress', 'being built'
```

**Terms we're MISSING:**
```javascript
'completion', 'near completion', 'building completion', 'available from', 'delivery'
```

**Why this matters:**
- Discover Lombok says "Building **completion**: December 2026"
- Reef Property says "**near completion**"
- Neither matches our current regex

---

### Question 2B: Is "off-plan" the right terminology?

**Answer:** ✅ **YES** - "Off-plan" IS the correct term and IS used by websites

**Evidence:**
1. ✅ **Nour Estates** uses "Off-Plan" (Row 9: Sunset View Villas)
2. ✅ **Reef Property** uses "off-plan opportunity" (Villa Aloha)

**BUT there's a problem:**
- We validated "off-plan" detection works (WebFetch on Row 9 showed it would match)
- BUT Row 9 is NOT in v2 at all (completely missing from scrape)
- We have ZERO "off-plan" properties in v2 to test if detection actually works

**Conclusion:**
- "Off-plan" IS the right terminology
- Our regex `/\boff[\s-]?plan\b/i` should work
- But we can't validate it because no off-plan properties made it into v2 scrape

**Possible explanations why Row 9 missing:**
1. Pagination limit (scraper stopped before reaching it)
2. Property removed from website
3. Scraper error on that specific URL

---

## 🔧 REQUIRED FIXES FOR v3

### Fix #1: Add "completion" keywords

```javascript
// CURRENT (v2)
else if (bodyText.match(/\bunder construction\b/i) ||
         bodyText.match(/\bin construction\b/i) ||
         bodyText.match(/\bin progress\b/i) ||
         bodyText.match(/\bbeing built\b/i)) {
    constructionStatus = 'Under Construction';
}

// NEW (v3) - ADD THESE LINES
else if (bodyText.match(/\bunder construction\b/i) ||
         bodyText.match(/\bin construction\b/i) ||
         bodyText.match(/\bin progress\b/i) ||
         bodyText.match(/\bbeing built\b/i) ||
         bodyText.match(/\bcompletion\b/i) ||           // NEW - catches "completion", "near completion", "building completion"
         bodyText.match(/\bavailable from\b/i) ||       // NEW - catches "available from January 2026"
         bodyText.match(/\bdelivery\b/i) ||             // NEW - catches "delivery date", "delivery 2026"
         bodyText.match(/\bhandover\b/i)) {             // NEW - catches "handover", "staged handover"
    constructionStatus = 'Under Construction';
}
```

### Fix #2: Add "renovated" to completed detection

```javascript
// CURRENT (v2)
if (bodyText.match(/\bbuilt\b/i) ||
    bodyText.match(/\bcompleted\b/i) ||
    bodyText.match(/\bready to move\b/i) ||
    bodyText.match(/\bmove-in ready\b/i)) {
    constructionStatus = 'Completed';
}

// NEW (v3) - ADD THIS LINE
if (bodyText.match(/\bbuilt\b/i) ||
    bodyText.match(/\bcompleted\b/i) ||
    bodyText.match(/\bready to move\b/i) ||
    bodyText.match(/\bmove-in ready\b/i) ||
    bodyText.match(/\brenovated\b/i)) {                // NEW - catches "renovated", "freshly renovated"
    constructionStatus = 'Completed';
}
```

### Fix #3: Keep "off-plan" detection (already correct)

```javascript
// KEEP THIS (already in v2)
else if (bodyText.match(/\boff[\s-]?plan\b/i) ||
         bodyText.match(/\bpre-construction\b/i)) {
    constructionStatus = 'Off-Plan';
}
```

### Fix #4: Enhance year detection (flexible formats)

```javascript
// CURRENT (v2) - TOO NARROW
const yearMatch = bodyText.match(/(?:year\s+built|built|construction)\s*:?\s*(20\d{2})/i);

// NEW (v3) - FLEXIBLE FORMATS
let yearBuilt = '';

// Pattern 1: Standard (year built: 2025, construction: 2026)
const yearMatch1 = bodyText.match(/(?:year\s+built|built|construction|completion)\s*:?\s*(20\d{2})/i);
if (yearMatch1) {
    yearBuilt = yearMatch1[1];
}

// Pattern 2: Month + Year (December 2026, January 2026)
if (!yearBuilt) {
    const yearMatch2 = bodyText.match(/(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+(20\d{2})/i);
    if (yearMatch2) {
        yearBuilt = yearMatch2[1];
    }
}

// Pattern 3: Context-based (any year near completion/construction/available/delivery)
if (!yearBuilt) {
    const yearMatch3 = bodyText.match(/(?:completion|construction|available|delivery|handover)[^.]*?(20\d{2})/i);
    if (yearMatch3) {
        yearBuilt = yearMatch3[1];
    }
}
```

### Fix #5: Future year validation

```javascript
// NEW (v3) - Validate future years indicate under construction
if (yearBuilt) {
    const currentYear = new Date().getFullYear();  // 2024
    const propYear = parseInt(yearBuilt, 10);

    // Future year = likely under construction
    if (propYear > currentYear && constructionStatus === 'Unknown') {
        constructionStatus = 'Under Construction';
    }
}
```

---

## 📈 EXPECTED IMPACT OF v3 FIXES

### Before v3 (current):
- 7 "Completed"
- 22 "Unknown" (includes 3-4 mislabeled properties)
- 0 "Off-Plan"
- 0 "Under Construction"

### After v3 (expected):
- 9-10 "Completed" (add Renovated villa, maybe Island Properties villas if auth allows)
- 17-18 "Unknown" (mostly raw land, auth-blocked properties)
- 0 "Off-Plan" (none in v2 to detect)
- 1-2 "Under Construction" (Commercial Shop, maybe others)

### After filtering out "Under Construction":
- **Final results:** ~26-28 properties (Completed + genuinely Unknown land)
- **Commercial Shop filtered out** ✅

---

## 🎯 KEY TAKEAWAYS

1. ✅ **"Completion" is the missing keyword** - Multiple websites use this instead of "under construction"

2. ✅ **"Off-plan" IS correct terminology** - Used by Reef Property and Nour Estates

3. ✅ **Regex failure IS consistent** - All websites affected, but for different reasons:
   - Discover Lombok: Missing "completion" keyword
   - Island Properties: Authentication barrier
   - Reef Property: Missing "near completion" variation
   - Nour Estates: ✅ Working perfectly

4. ✅ **Most "Unknown" are correctly labeled** - ~18-19 out of 22 are genuinely unknown (raw land, auth-blocked)

5. ✅ **Only 3-4 properties are mislabeled** - Commercial Shop + maybe 2-3 Island Properties villas

---

**Analysis prepared by:** Claude Code
**Date:** December 11, 2024
**Next action:** Create v3 JSON with enhanced regex patterns
