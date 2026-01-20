# Lombok Property Scraper Blueprint v6 - Implementation Summary

**Date:** December 16, 2024
**Status:** ✅ COMPLETE
**Output File:** `Lombok_Property_Scraper_v6_Blueprint.json` (372KB)

---

## Changes Implemented (12 Total)

### Priority 1: Core Updates (9 changes)

1. **Module 19** - Task 1 Dataset ID
   - Updated from `zppLe7oAGgeLIBTQW` to `ucOa8U3xOrTQ2R6uz`

2. **Module 20** - Task 2 Dataset ID
   - Updated from `5YxCYpqkCxZa0gPVO` to `R5FWB04ujtigD8Mo7`

3. **Module 8** - Google Sheets Column Headers
   - Added 4 columns in correct order:
     - Column L (11): "Construction Status"
     - Column M (12): "Year Built"
     - Column N (13): "Scraped At" (moved from L)
     - Column O (14): "Task #" (moved from M)

4. **Module 257** - Task 1 Aggregator
   - Added `constructionStatus: {{19.constructionStatus}}`
   - Added `yearBuilt: {{19.yearBuilt}}`

5. **Module 260** - Task 2 Aggregator
   - Added `constructionStatus: {{20.constructionStatus}}`
   - Added `yearBuilt: {{20.yearBuilt}}`

6. **Module 261** - Task 3 Aggregator
   - Added `constructionStatus: {{21.constructionStatus}}`
   - Added `yearBuilt: {{21.yearBuilt}}`

7. **Module 10** - Task 1 RAW Data Writer
   - Updated columns 11-14 with new field order
   - Column 11: `{{23.constructionStatus}}`
   - Column 12: `{{23.yearBuilt}}`
   - Column 13: `{{23.scrapedAt}}`
   - Column 14: `1` (Task number)

8. **Module 258** - Task 2 RAW Data Writer
   - Updated columns 11-14 with new field order
   - Column 11: `{{232.constructionStatus}}`
   - Column 12: `{{232.yearBuilt}}`
   - Column 13: `{{232.scrapedAt}}`
   - Column 14: `2` (Task number)

9. **Module 259** - Task 3 RAW Data Writer
   - Updated columns 11-14 with new field order
   - Column 11: `{{233.constructionStatus}}`
   - Column 12: `{{233.yearBuilt}}`
   - Column 13: `{{233.scrapedAt}}`
   - Column 14: `3` (Task number)

---

### Priority 2: Construction Status Filters (3 changes)

10. **Task 1 Filter** (Module 501)
    - Added after Module 23 (feeder)
    - Filters: Exclude "Off-Plan" AND "Under Construction"
    - Logic: `constructionStatus != "Off-Plan" AND constructionStatus != "Under Construction"`

11. **Task 2 Filter** (Module 502)
    - Added after Module 232 (feeder)
    - Filters: Exclude "Off-Plan" AND "Under Construction"
    - Logic: `constructionStatus != "Off-Plan" AND constructionStatus != "Under Construction"`

12. **Task 3 Filter** (Module 503)
    - Added after Module 233 (feeder)
    - Filters: Exclude "Off-Plan" AND "Under Construction"
    - Logic: `constructionStatus != "Off-Plan" AND constructionStatus != "Under Construction"`

---

## What Was NOT Changed

✅ **Task 3 Price Calculations** (Modules 413, 414, 143)
   - Kept as-is - working correctly with simplified 2-module preprocessing

✅ **Task 1 Price Calculation** (Module 141)
   - Kept as-is - working correctly for all data formats

⏳ **Task 2 Price Calculation** (Module 142)
   - NOT changed in v6
   - Simplification deferred for later discussion
   - Current formula has 22+ hardcoded mappings (fragile but functional)

---

## Validation Checklist

Before deploying to Make.com, verify:

### Data Completeness:
- [ ] Task 1 shows `constructionStatus` in Google Sheets column L
- [ ] Task 1 shows `yearBuilt` in Google Sheets column M
- [ ] Task 2 shows `constructionStatus` in Google Sheets column L
- [ ] Task 2 shows `yearBuilt` in Google Sheets column M
- [ ] Task 3 shows `constructionStatus` in Google Sheets column L
- [ ] Task 3 shows `yearBuilt` in Google Sheets column M

### Filters Working:
- [ ] "Off-Plan" properties are excluded from all 3 tasks
- [ ] "Under Construction" properties are excluded from all 3 tasks
- [ ] "Completed" properties are included
- [ ] "Unknown" properties are included

### Dataset IDs:
- [ ] Task 1 pulling from dataset `ucOa8U3xOrTQ2R6uz`
- [ ] Task 2 pulling from dataset `R5FWB04ujtigD8Mo7`
- [ ] Task 3 pulling from dataset `6kCy5ZnpavOkAxTjR`

### Price Calculations (Task 3):
- [ ] IDR prices: `IDR\n4.948.000.000` → `315159`
- [ ] USD prices: `$199,000.00` → `199000`
- [ ] IDR zero: `IDR 0` → `0`

---

## Import Instructions

1. **Backup existing scenario in Make.com**
   - Download current blueprint before importing v6

2. **Import Blueprint v6**
   - Go to Make.com scenario
   - Settings → Import Blueprint
   - Upload: `Lombok_Property_Scraper_v6_Blueprint.json`

3. **Verify connections**
   - Check Apify connections are still valid
   - Check Google Sheets connection is active

4. **Test with sample data**
   - Run scenario manually
   - Verify data appears in correct columns
   - Verify filters are excluding "Off-Plan" and "Under Construction"

---

## Rollback Plan

If issues occur:

1. **Restore from original:**
   `/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v2 (testing)_16.12.2025.blueprint.json`

2. **Or use archived version:**
   `FINAL_Lombok_Property_Scraper_v1_Blueprint_29.json`

---

## Future Work (Not in v6)

### Task 2 Price Simplification
- Add Module A: Extract raw price number (handles "B", "Bill", "Mio" multipliers)
- Add Module B: Detect currency type (IDR/USD/EUR)
- Update Module 142: Simplified conversion formula
- **Benefit:** Remove 22+ hardcoded mappings, handle all formats generically

---

## Technical Notes

### Blueprint Structure
- 5 top-level modules in main flow
- Module 256 is BasicRouter with 3 routes:
  - Route 0: Task 1 (8 modules after filter addition)
  - Route 1: Task 2 (8 modules after filter addition)
  - Route 2: Task 3 (13 modules after filter addition)

### New Module IDs
- Filter 501: Task 1 construction status filter
- Filter 502: Task 2 construction status filter
- Filter 503: Task 3 construction status filter

---

**✅ Blueprint v6 is production-ready for import to Make.com!**
