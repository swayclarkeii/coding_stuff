# Chunk 2.5 - Dokumenten_Tracker Update

**Date:** 2026-01-26
**Workflow ID:** okg8wTqLtPUwjQ18
**Workflow Name:** Chunk 2.5 - Client Document Tracking (Eugene Document Organizer)

## Overview

Updated Chunk 2.5 workflow to use the new streamlined **Dokumenten_Tracker** Google Sheet with German document names instead of the old Client_Tracker with 70+ columns.

## New Sheet Details

**Spreadsheet ID:** `12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I`
**Sheet Name:** `Dokumenten_Tracker`

**Key Changes:**
- 34 columns total (vs 70+ in old tracker)
- German document names (01_Projektbeschreibung, 02_Grundbuchauszug, etc.)
- Column A = **Mandant** (client name)
- Column B = **Letzte_Aktualisierung** (last updated timestamp)
- Columns C-AI = Document types

## Nodes Updated

### 1. **Lookup Client in Client_Tracker** (sheets-1)

**Change:** Updated sheet name to use Dokumenten_Tracker

**Before:**
```json
{
  "sheetName": {
    "mode": "name",
    "value": "Client_Tracker"
  }
}
```

**After:**
```json
{
  "sheetName": {
    "mode": "name",
    "value": "Dokumenten_Tracker"
  }
}
```

---

### 2. **Find Client Row and Validate** (code-3)

**Change:** Updated to look for **Mandant** field instead of Client_Name

**Key code changes:**
```javascript
// OLD: const sheetClientName = row.json.Client_Name || '';
// NEW:
const sheetClientName = row.json.Mandant || '';

// OLD: if (!clientRow || !clientRow.json.Client_Name)
// NEW:
if (!clientRow || !clientRow.json.Mandant)

// OLD: trackerClientName: clientRow.json.Client_Name
// NEW:
trackerClientName: clientRow.json.Mandant
```

**Error messages updated:**
- "No data returned from **Dokumenten_Tracker** lookup" (was Client_Tracker)

---

### 3. **Prepare Tracker Update Data** (code-8)

**Change:** Updated to map ALL document types (not just Core 4) to German column names

**Key improvements:**
1. **Backwards compatibility mapping** - Maps old type numbers to new numbers:
   ```javascript
   const oldToNewTypeMap = {
     '01_Projektbeschreibung': '01_Projektbeschreibung',
     '03_Grundbuchauszug': '02_Grundbuchauszug',  // Was 03, now 02
     '10_Bautraegerkalkulation_DIN276': '03_Bautraegerkalkulation_DIN276',  // Was 10, now 03
     '36_Exit_Strategie': '04_Exit_Strategie',  // Was 36, now 04
     // etc.
   };
   ```

2. **Complete German column mapping** - All 33 document types mapped:
   ```javascript
   const trackerColumnMapping = {
     '01_Projektbeschreibung': '01_Projektbeschreibung',
     '02_Grundbuchauszug': '02_Grundbuchauszug',
     '03_Bautraegerkalkulation_DIN276': '03_Bautraegerkalkulation_DIN276',
     '04_Exit_Strategie': '04_Exit_Strategie',
     // ... all 33 types
     '33_Unbekannt': '33_Unbekannt'
   };
   ```

3. **Unknown type fallback** - Documents not matching any type go to `33_Unbekannt`

---

### 4. **Build Google Sheets API Update Request** (code-build-sheets-api-update)

**Change:** Updated column mapping and sheet name for German tracker

**Key changes:**

1. **New column mapping** to German names and correct letters:
   ```javascript
   const columnMapping = {
     '01_Projektbeschreibung': 'C',
     '02_Grundbuchauszug': 'D',
     '03_Bautraegerkalkulation_DIN276': 'E',
     '04_Exit_Strategie': 'F',
     // ... all document types C-AI
     'Letzte_Aktualisierung': 'B'
   };
   ```

2. **Sheet reference updated** in ranges:
   ```javascript
   // OLD: const statusRange = `Client_Tracker!${columnLetter}${trackerRowIndex}`;
   // NEW:
   const statusRange = `Dokumenten_Tracker!${columnLetter}${trackerRowIndex}`;
   const timestampRange = `Dokumenten_Tracker!${timestampColumn}${trackerRowIndex}`;
   ```

3. **Timestamp column** changed to `Letzte_Aktualisierung` (column B)

---

## Behavior Changes

### ✅ What Now Works

1. **ALL document types update tracker** (not just Core 4)
   - Previously only 01, 03, 10, 36 updated tracker
   - Now all 33 document types (01-33) update tracker

2. **German column names** match new sheet structure
   - Uses proper German naming: Mandant, Letzte_Aktualisierung

3. **Unknown documents handled gracefully**
   - Documents with unrecognized types go to `33_Unbekannt` column
   - Still get checkmark (✓) and timestamp

4. **Backwards compatibility**
   - Old document type numbers automatically map to new numbers
   - Example: `03_Grundbuchauszug` (old) → `02_Grundbuchauszug` (new)

### 📝 What Stays the Same

1. **Routing logic unchanged**
   - Routes based on `chunk2_5_status` (success/error)
   - No changes to `Route Based on Document Type1` node

2. **Checkmark system unchanged**
   - Still puts `✓` in document column when received
   - Still updates timestamp in Letzte_Aktualisierung column

3. **Conditional tracker updates unchanged**
   - Still only updates tracker if `trackerUpdate === true`
   - SECONDARY and LOW_CONFIDENCE documents skip tracker

---

## Testing Checklist

- [ ] Upload a Core 4 document (01, 02, 03, or 04)
  - [ ] Checkmark (✓) appears in correct German column
  - [ ] Timestamp updates in column B (Letzte_Aktualisierung)

- [ ] Upload a non-Core document (e.g., 05-32)
  - [ ] Checkmark (✓) appears in correct column
  - [ ] Timestamp updates correctly

- [ ] Upload a document with unrecognized type
  - [ ] Checkmark (✓) goes to column AI (33_Unbekannt)
  - [ ] Timestamp updates

- [ ] Check client lookup
  - [ ] Client found by Mandant name in column A
  - [ ] Error handling works for missing clients

---

## Validation Results

Workflow validated successfully with **43 warnings** but **no critical errors**.

**Key warnings** (informational only):
- Code nodes lack error handling (expected)
- Some typeVersions outdated (not critical)
- Long linear chain (design choice)

**Status:** ✅ Ready for testing

---

## Files Modified

- Workflow: `okg8wTqLtPUwjQ18` (Chunk 2.5 - Client Document Tracking)
- 4 nodes updated:
  1. `sheets-1` - Lookup Client in Client_Tracker
  2. `code-3` - Find Client Row and Validate
  3. `code-8` - Prepare Tracker Update Data
  4. `code-build-sheets-api-update` - Build Google Sheets API Update Request

---

## Next Steps

1. **Test with real documents** - Upload test PDFs for each document type category
2. **Verify Google Sheet updates** - Check that checkmarks and timestamps appear correctly
3. **Monitor for errors** - Watch for client lookup failures or unknown document types
4. **Document any edge cases** - Note any issues with specific document types

---

## Reference: Complete Column Mapping

| Column Letter | Index | Document Type |
|---------------|-------|---------------|
| A | 0 | Mandant |
| B | 1 | Letzte_Aktualisierung |
| C | 2 | 01_Projektbeschreibung |
| D | 3 | 02_Grundbuchauszug |
| E | 4 | 03_Bautraegerkalkulation_DIN276 |
| F | 5 | 04_Exit_Strategie |
| G | 6 | 05_Altlastenkataster |
| H | 7 | 06_Baugrundgutachten |
| I | 8 | 07_Lageplan |
| J | 9 | 08_Flaechenberechnung |
| K | 10 | 09_GU_Werkvertraege |
| L | 11 | 10_Bauzeichnungen |
| M | 12 | 11_Baugenehmigung |
| N | 13 | 12_Gutachterauftrag |
| O | 14 | 13_Verkaufspreise |
| P | 15 | 14_Bauzeitenplan |
| Q | 16 | 15_Vertriebsweg |
| R | 17 | 16_Ausstattungsbeschreibung |
| S | 18 | 17_Teilungserklaerung |
| T | 19 | 18_Versicherungen |
| U | 20 | 19_Muster_Verkaufsvertrag |
| V | 21 | 20_Umsatzsteuervoranmeldung |
| W | 22 | 21_BWA |
| X | 23 | 22_Jahresabschluss |
| Y | 24 | 23_Finanzierungsbestaetigung |
| Z | 25 | 24_Darlehensvertrag |
| AA | 26 | 25_Gesellschaftsvertrag |
| AB | 27 | 26_Handelsregisterauszug |
| AC | 28 | 27_Gewerbeanmeldung |
| AD | 29 | 28_Steuer_ID |
| AE | 30 | 29_Freistellungsbescheinigung |
| AF | 31 | 30_Vollmachten |
| AG | 32 | 31_Korrespondenz |
| AH | 33 | 32_Sonstiges |
| AI | 34 | 33_Unbekannt |
