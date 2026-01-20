# Task 3 IDR Price Parsing Fix - Implementation Guide

**Scenario:** Lombok Property Scraper v2 (testing)
**Date:** 2024-12-16

---

## Overview

This fix adds 2 preprocessing modules before Module 143 to handle the new IDR format:
`"IDR\n4.948.000.000"` (with newline and period thousands separators)

### Changes Required:
1. Update Module 21 datasetId
2. Add Module A: "Extract Raw Number" (after Module 259)
3. Add Module B: "Detect Currency Type" (after Module A)
4. Update Module 143 formula (simplified)

---

## Change 1: Update Module 21 DatasetId

**Module:** "Get Task 3 Results" (ID: 21)
**Location:** Task 3 flow

**Current Value:**
```
ShuCkfxdhlP39IXOr
```

**New Value:**
```
6kCy5ZnpavOkAxTjR
```

---

## Change 2: Add Module A - "Extract Raw Number"

**Add AFTER:** Module 259 "Writes RAW Apify data (Task 3)"
**Add BEFORE:** Module 143 "Normalize Price USD for Task 3"

### Module Settings:
- **Type:** Tools → Set Variable
- **Name:** `Extract Raw Number (Task 3)`
- **Variable name:** `cleanedPriceNumber`
- **Variable lifetime:** One cycle

### Formula (copy exactly):
```
{{if(contains(233.priceRaw; "IDR"); parseNumber(replace(replace(replace(replace(233.priceRaw; newline; emptystring); "IDR"; emptystring); "."; emptystring); " "; emptystring)); if(contains(233.priceRaw; "$"); floor(parseNumber(replace(replace(replace(233.priceRaw; "$"; emptystring); ","; emptystring); " "; emptystring))); 0))}}
```

### What This Does:
| Input | Processing | Output |
|-------|------------|--------|
| `IDR\n4.948.000.000` | Strip newline → "IDR" → periods → spaces | `4948000000` |
| `IDR\n22.000.000.000` | Strip newline → "IDR" → periods → spaces | `22000000000` |
| `IDR 0` | Strip "IDR" → spaces | `0` |
| `$199,000.00` | Strip "$" → commas → floor | `199000` |
| `$99,000.00` | Strip "$" → commas → floor | `99000` |

---

## Change 3: Add Module B - "Detect Currency Type"

**Add AFTER:** Module A "Extract Raw Number"
**Add BEFORE:** Module 143

### Module Settings:
- **Type:** Tools → Set Variable
- **Name:** `Detect Currency Type (Task 3)`
- **Variable name:** `currencyType`
- **Variable lifetime:** One cycle

### Formula (copy exactly):
```
{{if(contains(233.priceRaw; "IDR"); "IDR"; if(contains(233.priceRaw; "$"); "USD"; "UNKNOWN"))}}
```

### What This Does:
| Input | Output |
|-------|--------|
| `IDR\n4.948.000.000` | `IDR` |
| `$199,000.00` | `USD` |
| Anything else | `UNKNOWN` |

---

## Change 4: Update Module 143 Formula

**Module:** "Normalize Price USD for Task 3" (ID: 143)

### Current Formula (REPLACE THIS):
The current formula is complex and handles many formats but breaks on newlines.

### New Simplified Formula (copy exactly):
```
{{if(currencyType = "IDR"; round(cleanedPriceNumber / 15700); cleanedPriceNumber)}}
```

### What This Does:
| cleanedPriceNumber | currencyType | priceUSD Output |
|--------------------|--------------|-----------------|
| `4948000000` | `IDR` | `315159` |
| `22000000000` | `IDR` | `1401274` |
| `0` | `IDR` | `0` |
| `199000` | `USD` | `199000` (unchanged) |
| `99000` | `USD` | `99000` (unchanged) |

---

## Final Flow (Task 3)

```
[Module 21: Get Task 3 Results]
        ↓
[Module 261: Aggregator]
        ↓
[Module 233: Feeder]
        ↓
[Module 259: Writes RAW data]
        ↓
[NEW Module A: Extract Raw Number] ← cleanedPriceNumber
        ↓
[NEW Module B: Detect Currency]    ← currencyType
        ↓
[Module 143: Normalize Price USD]  ← Uses cleanedPriceNumber + currencyType
        ↓
[Module 153: Data Quality Check]
```

---

## Testing Checklist

After implementing, test with:

- [ ] IDR price with newline: `IDR\n4.948.000.000` → Should output `315159`
- [ ] IDR price no newline: `IDR 1.000.000.000` → Should output `63694`
- [ ] IDR zero: `IDR 0` → Should output `0`
- [ ] USD price: `$199,000.00` → Should output `199000`
- [ ] USD price: `$99,000.00` → Should output `99000`

---

## Rollback Plan

If issues occur, restore from:
```
/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/lombok-invest-capital/make-blueprints/.archive/FINAL_Lombok_Property_Scraper_v1_Blueprint_29.json
```
