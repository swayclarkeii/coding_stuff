# Lombok Invest Capital - Technical Documentation

**Last Updated:** December 15, 2024
**Project Status:** ✅ Scraping Complete - Ready for Make.com filtering
**Client:** Benito (Lombok Invest Capital)

---

## 🎯 Current Configuration Structure

### Three-Task Apify Setup

**Why 3 Tasks:** Easier to run and test separately; each handles specific website patterns and filtering needs.

#### Task 1 - Primary Lombok Sites (4 websites) ✅ v4 COMPLETE
**File:** `Lombok Invest Capital (Task 1) 11_12_2025 - v4 - Dec-12-2024.json`
- Reef Property Lombok (reefpropertylombok.com)
- Island Properties Lombok (islandpropertylombok.com) ⚠️ **Requires login**
- Discover Lombok Property (discoverlombokproperty.com)
- Nour Estates (nourestates.com) ✅ **Verified patterns**
- **Results:** ~20 properties with construction status detection

#### Task 2 - Mixed Sites with Bali Filtering (4 websites) ✅ v4 COMPLETE
**File:** `Lombok Invest Capital (Task 2) 11_12_2025 - v4 - Dec-14-2024.json`
- Bali Exception (baliexception.com) - Lombok properties only
- Estate Lombok (estate-lombok.com)
- South Lombok Land Sales (southlomboklandsales.com)
- Maju Properties (majuproperties.com) ✅ **Verified patterns**
- **Results:** 45 properties with construction status detection

#### Task 3 - International Sites (2 websites) ✅ v4 COMPLETE
**File:** `Lombok Invest Capital (Task 3) 11_12_2025 - v4 - Dec-14-2024.json`
- Bali Home Immo (bali-home-immo.com) - Lombok filter via Make.com
- Invest Lombok (invest-lombok.com)
- **Results:** 20 properties with title-first construction status detection

---

## 🏗️ Construction Status Terminology by Website

### ⚠️ CRITICAL: Each Website Uses Different Labels!

| Website | Completed Property | Under Construction | Off-Plan | Authentication |
|---------|-------------------|-------------------|----------|----------------|
| **Nour Estates** | "**Built**" | "**Under Construction**" | "**Off-Plan**" | ✅ Public |
| **Maju Properties** | "**Completed**" | "**In progress**" | (varies) | ✅ Public |
| **Island Properties** | Unknown | Unknown | Unknown | ❌ **Requires Login** |
| **Reef Property** | Not yet verified | Not yet verified | Not yet verified | ✅ Public |
| **Discover Lombok** | Not yet verified | Not yet verified | Not yet verified | ✅ Public |
| **Estate Lombok** | Not yet verified | Not yet verified | Not yet verified | ✅ Public |
| **Bali Exception** | Not yet verified | Not yet verified | Not yet verified | ✅ Public |
| **Bali Home Immo** | Not yet verified | Not yet verified | Not yet verified | ✅ Public |
| **Invest Lombok** | Not yet verified | Not yet verified | Not yet verified | ✅ Public |

---

## 🔍 Verified Property Patterns (Playwright Investigation)

### ✅ APPROVED Properties (What Benito Wants)

#### 1. Nour Estates - Teak Wood Villa (Row 7 from feedback)
**URL:** https://www.nourestates.com/property/teak-wood-villa-for-sale-in-kuta

**How It Displays:**
```
Ownership: "Built | For Sale | Freehold/HGB"
Year Built: 2025 (completed)
Price: $140,000
```

**What to Search For:**
- Text contains: `Built` (in ownership field)
- Text contains: `Year Built 2025` (current/past year)
- Does NOT contain: "Off-Plan", "Under Construction"

---

#### 2. Maju Properties - Villa Sun Palm 3BR (Row 20 from feedback)
**URL:** https://www.majuproperties.com/property/villa-sun-palm-3br

**How It Displays:**
```
Status: "Completed"
Year of construction: 2025
Ownership: HGB
Price: USD 275,000
```

**What to Search For:**
- Text contains: `Completed` (in status field)
- Text contains: `Year of construction: 2025` (current year)
- Does NOT contain: "In progress", "Off-plan"

---

#### 3. Island Properties - Hilltop Villa (Row 11 from feedback)
**URL:** https://islandpropertylombok.com/property/hilltop-villa-kuta-lombok/

⚠️ **BLOCKED BY AUTHENTICATION**
- Requires sign-in to view property details
- Cannot verify construction status display pattern
- Shows "For Sale" label publicly, but details behind login

**Recommendation:** Assume "For Sale" without rejection keywords = Approved

---

### ❌ REJECTED Properties (What Benito Does NOT Want)

#### 1. Nour Estates - Sunset View Villas (Row 9 from feedback)
**URL:** https://www.nourestates.com/property/sunset-villas-for-sale-in-kuta-lombok

**How It Displays:**
```
Ownership: "For Sale | Freehold/HGB | Off-Plan>Under Construction"
Overview Badges: "Off Plan" + "Under Construction"
Year Built: 2026 (future year)
Price: $160,000
```

**What to Search For:**
- Text contains: `Off-Plan` or `Off Plan` (with/without hyphen)
- Text contains: `Under Construction`
- Text contains: `Year Built 2026` (future year)

---

#### 2. Maju Properties - Sora Resort 3BR (Rows 16-19 from feedback)
**URL:** https://www.majuproperties.com/property/sora-resort-3-bedroom-villas-for-sale-kuta-lombok

**How It Displays:**
```
Status: "In progress"
Year of construction: 2026
Ownership: Leasehold
Price: USD 195,000
```

**What to Search For:**
- Text contains: `In progress` (specific to Maju Properties)
- Text contains: `Year of construction: 2026` (future year)
- Text may contain: "Pre-construction", "Staged handover through 2026"

---

## 📊 Data Fields Currently Captured

### Task 1 Current Fields
```javascript
{
  url: string,              // Property page URL
  title: string,            // Property name
  priceRaw: string,         // Unparsed price
  ownership: string,        // HGB/Freehold/Leasehold
  status: string,           // For Sale/Sold/For Rent
  propertyType: string,     // Villa/House/Land/etc
  source: string,           // Website name
  hasKuta: boolean,         // Location flag
  hasSelong: boolean,       // Location flag
  hasFreehold: boolean,     // Ownership flag
  hasLeasehold: boolean,    // Ownership flag
  scrapedAt: string         // ISO timestamp
}
```

### ⚠️ Missing Fields (TO BE ADDED)
```javascript
constructionStatus: string,  // "Completed" | "Off-Plan" | "Under Construction" | "Unknown"
yearBuilt: string           // "2025", "2026", etc. - helps validate construction status
```

---

## 🎯 Comprehensive Regex Patterns for Detection

### Completed/Built Properties (✅ APPROVE)
```javascript
if (bodyText.match(/\bbuilt\b/i) ||
    bodyText.match(/\bcompleted\b/i) ||
    bodyText.match(/\bready to move\b/i) ||
    bodyText.match(/\bmove-in ready\b/i)) {
    constructionStatus = 'Completed';
}
```

### Off-Plan Properties (❌ REJECT)
```javascript
else if (bodyText.match(/\boff[\s-]?plan\b/i) ||
         bodyText.match(/\bpre-construction\b/i)) {
    constructionStatus = 'Off-Plan';
}
```

### Under Construction Properties (❌ REJECT)
```javascript
else if (bodyText.match(/\bunder construction\b/i) ||
         bodyText.match(/\bin construction\b/i) ||
         bodyText.match(/\bin progress\b/i) ||
         bodyText.match(/\bbeing built\b/i)) {
    constructionStatus = 'Under Construction';
}
```

### Year Built Detection (Validation Helper)
```javascript
const yearMatch = bodyText.match(/(?:year\s+built|built|construction)\s*:?\s*(20\d{2})/i);
if (yearMatch) {
    yearBuilt = yearMatch[1];
}
```

**Year Logic:**
- **2024, 2025** = Current/past = Likely completed
- **2026, 2027+** = Future = Likely off-plan or under construction

---

## 🔗 Reference URLs from Benito's Feedback

### APPROVED Examples (Test Against These)
- Row 7: https://www.nourestates.com/property/teak-wood-villa-for-sale-in-kuta
- Row 8: https://www.nourestates.com/property/lush-villa-for-sale-kuta-lombok
- Row 11: https://islandpropertylombok.com/property/hilltop-villa-kuta-lombok/
- Row 12: https://islandpropertylombok.com/property/bumbang-bay-villa/
- Row 15: https://islandpropertylombok.com/property/modern-3br-villa-duduk-robbo/
- Row 20: https://www.majuproperties.com/property/villa-sun-palm-3br

### REJECTED Examples (Must Filter Out)
- Row 9: https://www.nourestates.com/property/sunset-villas-for-sale-in-kuta-lombok
- Row 10: https://www.nourestates.com/property/boutique-villas-for-sale-kuta-lombok
- Row 13-14: https://www.nourestates.com/property/seaview-villas-for-sale-in-selong
- Row 16-19: https://www.majuproperties.com/property/sora-resort-* (multiple variants)
- Row 26: https://www.invest-lombok.com/property/villa-off-plan-for-lease-in-are-guling-lombok/

---

## 📁 File Locations

### Apify Configurations
```
/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/lombok-invest-capital/apify-configs/json/
├── Lombok Invest Capital (Task 1) 11_12_2025 - v4 - Dec-12-2024.json  ← TASK 1 FINAL
├── Lombok Invest Capital (Task 2) 11_12_2025 - v4 - Dec-14-2024.json  ← TASK 2 FINAL
├── Lombok Invest Capital (Task 3) 11_12_2025 - v4 - Dec-14-2024.json  ← TASK 3 FINAL
└── .archive/
    └── [All previous versions v1-v3 archived]
```

**Note:** This project follows the **File Versioning Protocol** defined in `/02-operations/technical-builds/CLAUDE.md`. All configuration file modifications must be versioned and archived.

### Make.com Blueprints
```
/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/lombok-invest-capital/make-blueprints/
├── FINAL_Lombok_Property_Scraper_v1_Blueprint_29.json  ← Current production
├── TASK2-FORMULA-FINAL-100PERCENT.txt  ← Price normalization logic
└── [other formula variants]
```

### Project Management
```
/Users/swayclarke/coding_stuff/claude-code-os/02-operations/projects/lombok-invest-capital/
├── project-brief.md         ← Overview and scope
├── action-items.md          ← Current tasks (Dec 8-12, 2024)
├── feedback-received.md     ← Benito's feedback log
├── decisions-log.md         ← Technical decisions
└── timeline.md              ← Project milestones
```

---

## ⚠️ Known Issues & Special Cases

### Issue 1: Island Properties Authentication
**Problem:** Website requires login to view full property details
**Impact:** Cannot verify construction status display patterns
**Workaround:** Use comprehensive regex that catches common patterns; assume "For Sale" without rejection keywords = approved
**Status:** Unresolved - needs client credentials or accept risk

### Issue 2: Location False Positives (Senggigi/Kuta)
**Problem:** Properties in Senggigi flagged as `hasKuta: true` because "Kuta" appears in footer links, galleries, related listings
**Current Detection:** `bodyText.toLowerCase().includes('kuta')` - too broad
**Solution:** Extract location from title + specific selectors only (`.property-location`, `address`, etc.)
**Status:** Documented, needs implementation

### Issue 3: Inconsistent Terminology
**Problem:** Different websites use different labels for same construction status
**Examples:**
- "Built" (Nour Estates) vs "Completed" (Maju Properties)
- "Off-Plan" vs "Pre-construction"
- "Under Construction" vs "In progress" vs "Being built"
**Solution:** Comprehensive regex patterns covering all variations
**Status:** Documented in this file

---

## 🧪 Testing Strategy

### Phase A: Task 1 Testing (Dec 11)
1. Modify Task 1 JSON only
2. Run scraper on 4 websites
3. Validate against known URLs:
   - Row 7 (approved) → Should capture "Completed" + year "2025"
   - Row 9 (rejected) → Should capture "Off-Plan" or "Under Construction" + year "2026"
4. If successful → Proceed to Phase B

### Phase B: Tasks 2 & 3 (Dec 12)
5. Apply same logic to Task 2 (includes Maju Properties - verified patterns)
6. Apply same logic to Task 3
7. Test all three tasks together

### Phase C: Make.com Integration (Dec 12)
8. Add filtering module (exclude "Off-Plan" and "Under Construction")
9. Add "not yet seen" tracking with Data Store
10. Deploy and get Benito's approval

---

## 📝 Quick Reference Commands

### Search for Construction Status in Body Text
```javascript
// In Apify pageFunction:
const bodyText = document.body.innerText;

// Check patterns (case-insensitive)
const isCompleted = /\b(built|completed|ready to move|move-in ready)\b/i.test(bodyText);
const isOffPlan = /\b(off[\s-]?plan|pre-construction)\b/i.test(bodyText);
const isUnderConstruction = /\b(under construction|in construction|in progress|being built)\b/i.test(bodyText);
```

### Extract Year Built
```javascript
const yearMatch = bodyText.match(/(?:year\s+built|built|construction)\s*:?\s*(20\d{2})/i);
const yearBuilt = yearMatch ? yearMatch[1] : '';
```

---

## 📦 Configuration Version History

### Task 1 Apify Config

| Version | Date | Changes | Status |
|---------|------|---------|--------|
| **v4** | Dec 12, 2024 | Fixed future year validation to override ALL statuses (not just Unknown) | ✅ FINAL |
| v3 | Dec 11, 2024 | Enhanced regex; Future year validation | 🗄️ Archived |
| v2 | Dec 11, 2024 | Added constructionStatus and yearBuilt | 🗄️ Archived |
| v1 | Dec 11, 2024 | Original configuration | 🗄️ Archived |

### Task 2 Apify Config

| Version | Date | Changes | Status |
|---------|------|---------|--------|
| **v4** | Dec 14, 2024 | Fixed Estate Lombok selector; 45 properties working | ✅ FINAL |
| v3 | Dec 14, 2024 | Timeout fixes, scroll settings | 🗄️ Archived |
| v2 | Dec 12, 2024 | Added construction status detection | 🗄️ Archived |
| v1 | Dec 12, 2024 | Original configuration | 🗄️ Archived |

### Task 3 Apify Config

| Version | Date | Changes | Status |
|---------|------|---------|--------|
| **v4** | Dec 15, 2024 | Title-first detection; non-www glob fix; 20 properties | ✅ FINAL |
| v3 | Dec 14, 2024 | Reordered Off-Plan priority (partial fix) | 🗄️ Archived |
| v1 | Dec 14, 2024 | Added construction status detection | 🗄️ Archived |

### Key Technical Improvements (All Tasks)

**Task 1 v4:**
- Future year validation overrides ALL statuses (not just Unknown)
- Properties with years 2026+ always marked "Under Construction"

**Task 2 v4:**
- Fixed Estate Lombok link selector
- Increased timeouts to 90 seconds
- 45 properties across 4 websites

**Task 3 v4:**
- **Title-first detection** - Checks title for "off plan" or "brand new" BEFORE body text
- Prevents false positives from "Similar Properties" sections
- Added `bali-home-immo.com/**` glob (non-www) - fixed 0 → 13 properties
- 20 properties across 2 websites

---

## 🔄 Update History

| Date | Change | By |
|------|--------|-----|
| Dec 11, 2024 | Initial documentation created with Playwright verification findings | Claude |
| Dec 11, 2024 | Verified Nour Estates and Maju Properties patterns | Claude |
| Dec 11, 2024 | Documented Island Properties authentication requirement | Claude |
| Dec 11, 2024 | **TASK 1 v2** - Added construction status detection with comprehensive regex | Claude |
| Dec 11, 2024 | **TASK 1 v2** - Added `constructionStatus` and `yearBuilt` fields | Claude |
| Dec 11, 2024 | **TASK 1 v2** - Fixed location detection false positives (Senggigi/Kuta issue) | Claude |
| Dec 11, 2024 | **Versioning Protocol** - Implemented file versioning with `.archive/` folder | Claude |

---

## 📌 Important Notes

1. **Always test on Task 1 first** before applying changes to Tasks 2 & 3
2. **Benito's feedback spreadsheet** is the source of truth: https://docs.google.com/spreadsheets/d/1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54/edit?gid=1808301101
3. **Year Built is a validation helper** - future years (2026+) almost always indicate off-plan
4. **When in doubt, filter out** - Conservative approach preferred (only show confirmed completed properties)
5. **Island Properties** will need special handling due to authentication barrier

---

**For questions or updates to this documentation, see:**
- Action Items: `action-items.md`
- Implementation Plan: `/Users/swayclarke/.claude/plans/tidy-dazzling-duckling.md`
