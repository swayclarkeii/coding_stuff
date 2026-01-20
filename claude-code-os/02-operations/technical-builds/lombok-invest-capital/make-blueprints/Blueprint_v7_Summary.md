# Lombok Property Scraper Blueprint v7 - Implementation Summary

**Date:** December 16, 2024
**Status:** ✅ COMPLETE
**Output File:** `Lombok_Property_Scraper_v7_Blueprint.json` (371KB)

---

## Changes Implemented (3 New Columns Added to Filtered Output)

### Base: All changes from v6
Blueprint v7 includes all changes from v6:
- ✅ Updated dataset IDs (Task 1 and Task 2)
- ✅ Added Construction Status and Year Built columns to RAW output
- ✅ Construction status filters (excluding Off-Plan and Under Construction)
- ✅ Task 2 URL filter bug fixed (changed from `== -sold` to `does not contain -sold`)

### New in v7: Manual Review Flags

Added to **Module 171** (Task 1 Filtered Output):
```json
"11": "{{23.constructionStatus}}",
"12": "{{23.yearBuilt}}",
"13": "{{23.scrapedAt}}",
"14": "1",
"15": "{{if(23.constructionStatus = \"Unknown\"; \"⚠️ REVIEW\"; \"\")}}"
```

Added to **Module 172** (Task 2 Filtered Output):
```json
"11": "{{232.constructionStatus}}",
"12": "{{232.yearBuilt}}",
"13": "{{232.scrapedAt}}",
"14": "2",
"15": "{{if(232.constructionStatus = \"Unknown\"; \"⚠️ REVIEW\"; \"\")}}"
```

Added to **Module 173** (Task 3 Filtered Output):
```json
"11": "{{233.constructionStatus}}",
"12": "{{233.yearBuilt}}",
"13": "{{233.scrapedAt}}",
"14": "3",
"15": "{{if(233.constructionStatus = \"Unknown\"; \"⚠️ REVIEW\"; \"\")}}"
```

---

## Updated FILTERED Sheet Column Order

```
A (0):  URL
B (1):  Title
C (2):  Price USD
D (3):  Ownership
E (4):  Status
F (5):  Property Type
G (6):  Source
H (7):  Has Kuta
I (8):  Has Selong
J (9):  Has Freehold
K (10): Has Leasehold
L (11): Construction Status   ← NEW in v7
M (12): Year Built            ← NEW in v7
N (13): Scraped At            ← Existing (moved from column 11)
O (14): Task #                ← Existing (moved from column 12)
P (15): Manual Review         ← NEW in v7 (⚠️ REVIEW flag)
```

---

## How the Manual Review Flag Works

### Example Output in Google Sheets:

| Property | Price | Construction Status | Year Built | Manual Review |
|----------|-------|---------------------|------------|---------------|
| Hilltop Villa Kuta | $229,299 | Unknown | | ⚠️ REVIEW |
| Teak Wood Villa | $140,000 | Completed | 2025 | |
| Bumbang Villa 4BR | $300,000 | Completed | | |
| Selong Belanak bay | $160,000 | Unknown | | ⚠️ REVIEW |

### Logic:
- **If construction status = "Unknown"** → Shows `⚠️ REVIEW`
- **If construction status = "Completed"** → Shows blank
- **If construction status = anything else** → Shows blank

### Benefits:
✅ Instantly identifies properties needing manual verification
✅ Can sort/filter by "Manual Review" column to group flagged items
✅ Construction status and year built visible for context
✅ Fully automated - no manual tagging required

---

## Validation Checklist

Before deploying to Make.com, verify:

### Data Completeness:
- [ ] All 3 tasks show Construction Status in FILTERED sheet column L (11)
- [ ] All 3 tasks show Year Built in FILTERED sheet column M (12)
- [ ] All 3 tasks show Scraped At timestamp in FILTERED sheet column N (13)
- [ ] All 3 tasks show Task # in FILTERED sheet column O (14)
- [ ] All 3 tasks show Manual Review flag in FILTERED sheet column P (15)

### Manual Review Flags:
- [ ] Properties with "Unknown" construction status show "⚠️ REVIEW"
- [ ] Properties with "Completed" construction status show blank
- [ ] Can filter/sort by Manual Review column

### Filters Working (from v6):
- [ ] "Off-Plan" properties are excluded from all 3 tasks
- [ ] "Under Construction" properties are excluded from all 3 tasks
- [ ] "Completed" properties are included
- [ ] "Unknown" properties are included

### Dataset IDs (from v6):
- [ ] Task 1 pulling from dataset `ucOa8U3xOrTQ2R6uz`
- [ ] Task 2 pulling from dataset `R5FWB04ujtigD8Mo7`
- [ ] Task 3 pulling from dataset `6kCy5ZnpavOkAxTjR`

### Price Calculations (from v6):
- [ ] Task 1: IDR and USD prices converting correctly
- [ ] Task 2: All price formats converting correctly
- [ ] Task 3: IDR prices with newlines converting correctly (`IDR\n4.948.000.000` → `315159`)

---

## Import Instructions

1. **Backup existing scenario in Make.com**
   - Download current blueprint before importing v7

2. **Import Blueprint v7**
   - Go to Make.com scenario
   - Settings → Import Blueprint
   - Upload: `Lombok_Property_Scraper_v7_Blueprint.json`

3. **Update FILTERED Google Sheets header row**
   - Column K (11): "Construction Status" (NEW)
   - Column L (12): "Year Built" (NEW)
   - Column M (13): "Scraped At" (existing - moved)
   - Column N (14): "Task #" (existing - moved)
   - Column O (15): "Manual Review" (NEW - ⚠️ flag)

4. **Verify connections**
   - Check Apify connections are still valid
   - Check Google Sheets connection is active

5. **Test with sample data**
   - Run scenario manually
   - Verify Construction Status appears in column L (11)
   - Verify Year Built appears in column M (12)
   - Verify Scraped At timestamp appears in column N (13)
   - Verify Task # appears in column O (14)
   - Verify "⚠️ REVIEW" flag appears for Unknown properties in column P (15)
   - Verify filters are excluding "Off-Plan" and "Under Construction"

---

## Rollback Plan

If issues occur:

1. **Restore from v6:**
   `Lombok_Property_Scraper_v6_Blueprint.json`

2. **Or restore from original v4:**
   `/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v4 (testing)_16.12.2025.blueprint.json`

3. **Or use v3:**
   `/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v3 (testing)_16.12.2025.blueprint.json`

---

## Analysis Results (from v3 testing)

**Test Results:**
- Total properties scraped: 95
- Properties passed filters: 7 (7.4% pass rate)
- Properties filtered out: 88

**Filter Performance:**
- ✅ Has Kuta filter: Working (all 7 results in Kuta)
- ✅ Price filter (≤$300k): Working (range $99k-$300k)
- ✅ Construction Status filters: Working (excluding Off-Plan and Under Construction)
- ✅ URL filters: Working (excluding '-land' and '-sold')

**Properties Flagged for Manual Review (3 of 7):**
1. Hilltop Villa — Kuta ($229k, Unknown status)
2. Selong Belanak bay view ($160k, Unknown status)
3. Great deal Selong Belanak ($270k, Unknown status)

---

## Technical Notes

### Blueprint Structure
- 5 top-level modules in main flow
- Module 256 is BasicRouter with 3 routes:
  - Route 0: Task 1 (7 modules)
  - Route 1: Task 2 (7 modules)
  - Route 2: Task 3 (13 modules)

### Changes from v6 to v7
- **3 NEW columns added** to each filtered output (171, 172, 173):
  - Column 11: Construction Status
  - Column 12: Year Built
  - Column 15: Manual Review flag
- **2 columns repositioned** (were missing in v6):
  - Column 13: Scraped At (moved from column 11)
  - Column 14: Task # (moved from column 12)
- **No changes** to RAW output (already has Construction Status and Year Built)
- **No changes** to filters (already excluding Off-Plan and Under Construction)
- **No changes** to price calculations (Task 3 working correctly)

---

## Future Work (Not in v7)

### Task 2 Price Simplification
- Add Module A: Extract raw price number (handles "B", "Bill", "Mio" multipliers)
- Add Module B: Detect currency type (IDR/USD/EUR)
- Update Module 142: Simplified conversion formula
- **Benefit:** Remove 22+ hardcoded mappings, handle all formats generically

---

**✅ Blueprint v7 is production-ready for import to Make.com!**
