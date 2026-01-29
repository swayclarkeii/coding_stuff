# Chunk 2.5 System Architecture - Classification to Folder Mapping

**Document:** System constraints for prompt improvements
**Date:** 2026-01-28
**Workflow:** Chunk 2.5 (`okg8wTqLtPUwjQ18`)

---

## Current System Overview

### 1. Folder Structure (FIXED - Cannot Change)

**Total Folders:** 5 folders

**CORE 4 Folders (Specific document types):**
1. `FOLDER_01_PROJEKTBESCHREIBUNG` - Project descriptions/exposés
2. `FOLDER_03_GRUNDBUCHAUSZUG` - Land register extracts
3. `FOLDER_10_BAUTRAEGERKALKULATION` - Developer calculations (DIN276)
4. `FOLDER_36_EXIT_STRATEGIE` - Exit strategies

**Catch-All Folder:**
5. `FOLDER_37_OTHERS` - All other documents

### 2. Folder Routing Logic

**From Node:** "Get Destination Folder ID" (code-4)

```javascript
const CORE_4_TYPES = [
  '01_Projektbeschreibung',
  '03_Grundbuchauszug',
  '10_Bautraegerkalkulation_DIN276',
  '36_Exit_Strategie'
];

if (CORE_4_TYPES.includes(documentType)) {
  // Route to specific folder
} else {
  // Route to FOLDER_37_OTHERS
}
```

**Key Rule:** Only documents with codes in `CORE_4_TYPES` get specific folders. Everything else → 37_Others.

### 3. Tracker Column Mapping

**From Node:** "Build Google Sheets API Update Request" (code-build-sheets-api-update)

**AI Classification Codes → Tracker Columns:**

| AI Code | Tracker Column | Column Letter |
|---------|---------------|---------------|
| 01_Projektbeschreibung | 01_Exposé | C |
| 02_Kaufvertrag | 02_Grundbuchauszug | D |
| 03_Grundbuchauszug | 02_Grundbuchauszug | D |
| 10_Bautraegerkalkulation_DIN276 | 03_Bautraegerkalkulation_DIN276 | E |
| 36_Exit_Strategie | 04_Exit_Strategie | F |
| 07_Altlastenkataster | 05_Altlastenkataster | G |
| 08_Baugrundgutachten | 06_Baugrundgutachten | H |
| 09_Lageplan | 07_Lageplan | I |
| 15_Flaechenberechnung_DIN277 | 08_Flaechenberechnung | J |
| 16_GU_Werkvertraege | 09_GU_Werkvertraege | K |
| 17_Bauzeichnungen | 10_Bauzeichnungen | L |
| 18_Baugenehmigung | 11_Baugenehmigung | M |
| 22_Gutachterauftrag | 12_Gutachterauftrag | N |
| 11_Verkaufspreise | 13_Verkaufspreise | O |
| 12_Bauzeitenplan_Liquiditaet | 14_Bauzeitenplan | P |
| 13_Vertriebsweg | 15_Vertriebsweg | Q |
| 14_Bau_Ausstattungsbeschreibung | 16_Ausstattungsbeschreibung | R |
| 19_Teilungserklaerung | 17_Teilungserklaerung | S |
| 20_Versicherungen | 18_Versicherungen | T |
| 21_Muster_Verkaufsvertrag | 19_Muster_Verkaufsvertrag | U |
| 23_Umsatzsteuervoranmeldung | 20_Umsatzsteuervoranmeldung | V |
| 24_BWA | 21_BWA | W |
| 25_Jahresabschluss | 22_Jahresabschluss | X |
| 26_Finanzierungsbestaetigung | 23_Finanzierungsbestaetigung | Y |
| 27_Darlehensvertrag | 24_Darlehensvertrag | Z |
| 28_Gesellschaftsvertrag | 25_Gesellschaftsvertrag | AA |
| 29_Handelsregisterauszug | 26_Handelsregisterauszug | AB |
| 30_Gewerbeanmeldung | 27_Gewerbeanmeldung | AC |
| 31_Steuer_ID | 28_Steuer_ID | AD |
| 32_Freistellungsbescheinigung | 29_Freistellungsbescheinigung | AE |
| 33_Vollmachten | 30_Vollmachten | AF |
| 34_Korrespondenz | 31_Korrespondenz | AG |
| 35_Sonstiges_Allgemein | 32_Sonstiges | AH |
| 37_Others | 32_Sonstiges | AH |
| 38_Unknowns | 33_Unbekannt | AI |

---

## Constraints for Prompt Improvements

### What CAN Be Changed ✅
1. **Prompt text** - Improve wording, add examples, clarify boundaries
2. **AI classification logic** - Help AI choose better between existing codes
3. **Reasoning** - Enhance explanation quality
4. **Add new AI codes** - AS LONG AS they map to existing infrastructure

### What CANNOT Be Changed ❌
1. **Folder count** - Must stay at 5 folders
2. **Core 4 folder purposes** - Projektbeschreibung, Grundbuchauszug, Bauträgerkalkulation, Exit Strategie
3. **Folder IDs** - Variable names like FOLDER_01_PROJEKTBESCHREIBUNG are fixed

### Adding New Classification Codes - Requirements

If we want to add new codes like `01b_Technische_Spezifikationen` or `11b_Baukosten_GU_Angebote`:

**Step 1: Decide Folder Destination**
- Should 01b go to FOLDER_01_PROJEKTBESCHREIBUNG (same as 01)? → Add to CORE_4_TYPES
- Should 01b go to FOLDER_37_OTHERS? → Don't add to CORE_4_TYPES

**Step 2: Add to Folder Routing**
Update `CORE_4_TYPES` array in "Get Destination Folder ID" node:
```javascript
const CORE_4_TYPES = [
  '01_Projektbeschreibung',
  '01b_Technische_Spezifikationen', // NEW - routes to same folder as 01
  '03_Grundbuchauszug',
  '10_Bautraegerkalkulation_DIN276',
  '36_Exit_Strategie'
];
```

AND update `coreMapping` object:
```javascript
const coreMapping = {
  '01_Projektbeschreibung': { varName: 'FOLDER_01_PROJEKTBESCHREIBUNG', displayName: '01_Projektbeschreibung' },
  '01b_Technische_Spezifikationen': { varName: 'FOLDER_01_PROJEKTBESCHREIBUNG', displayName: '01b_Technische_Spezifikationen' }, // NEW
  // ...
};
```

**Step 3: Add to Tracker Column Mapping**
Update `aiToSheetMapping` in "Build Google Sheets API Update Request" node:
```javascript
const aiToSheetMapping = {
  '01_Projektbeschreibung': '01_Exposé',
  '01b_Technische_Spezifikationen': '01_Exposé', // Maps to same column OR new column
  // ...
};
```

**Decision:** Should 01b map to same tracker column as 01 OR a new column?
- Same column (01_Exposé) → All go to column C, lose granularity
- New column (01b_TechSpecs) → Need to add new column to `columnLetterMapping`

**Step 4: Add to Tier 2 Prompt**
Add the new code to the appropriate tier 2 prompt with keywords and description.

---

## Recommended Approach for Iteration 2

### Option A: PROMPT IMPROVEMENTS ONLY (Safest, No Architecture Changes)

**What:** Improve prompts without adding new codes
**How:**
- Add clearer boundary rules to existing categories
- Add "DO NOT CONFUSE WITH" sections
- Add consistency rules
- Improve keyword lists

**Pros:**
- No architecture changes needed
- No risk of breaking existing mappings
- Faster to implement

**Cons:**
- May not fully address technical vs marketing distinction
- Limited by existing category structure

### Option B: ADD NEW CODES WITH MAPPINGS (More granular, requires changes)

**What:** Add new classification codes like 01b, 01c, 11b, 09b
**How:**
- Create new codes in tier 2 prompts
- Map to appropriate folders (core or others)
- Map to tracker columns (new or existing)
- Update both routing nodes

**Pros:**
- More precise classification
- Better captures document nuances

**Cons:**
- Requires 3 node updates (prompts + folder routing + tracker mapping)
- More complexity
- Could break if not done carefully

---

## Impact Analysis for Proposed Changes

### Change 1: Municipal Certificate Distinctions
**Type:** Prompt improvement only
**Nodes affected:** Build AI Classification Prompt (tier 1)
**Architecture impact:** None
**Risk:** Low

### Change 2: Construction Costs vs Sales Prices
**Type:** Add new code `11b_Baukosten_GU_Angebote`
**Nodes affected:**
1. Parse Classification Result (tier 2 prompt)
2. Get Destination Folder ID (folder routing)
3. Build Google Sheets API Update Request (tracker mapping)

**Architecture impact:**
- New code routes to FOLDER_37_OTHERS (not core)
- New tracker column needed? Or map to existing?

**Recommendation:** Map to same tracker column as 11_Verkaufspreise for now, differentiate via reasoning

**Risk:** Medium (3 nodes to update)

### Change 3: Technical vs Marketing Split (01b, 01c)
**Type:** Add new codes `01b_Technische_Spezifikationen`, `01c_Energieausweis`
**Nodes affected:**
1. Parse Classification Result (tier 2 prompt)
2. Get Destination Folder ID (add to CORE_4, route to FOLDER_01)
3. Build Google Sheets API Update Request (map to tracker)

**Architecture impact:**
- Add to CORE_4_TYPES to route to same folder as 01
- Need to decide: same tracker column OR new columns?

**Recommendation:** For iteration 2, DON'T add these codes yet. Instead, improve prompts to better choose between 01_Projektbeschreibung vs 14_Bau_Ausstattungsbeschreibung

**Risk:** High (architecture change, multiple mappings)

### Change 4: Bebauungsplan vs Lageplan
**Type:** Add new code `09b_Bebauungsplan`
**Nodes affected:** Same 3 as above
**Architecture impact:** Routes to FOLDER_37_OTHERS
**Risk:** Medium

### Change 5: Consistency Rules
**Type:** Prompt improvement only
**Nodes affected:** Both tier 1 and tier 2 prompts
**Architecture impact:** None
**Risk:** Low

### Change 6: Fallback Rules
**Type:** Prompt improvement only
**Nodes affected:** All tier 2 prompts
**Architecture impact:** None
**Risk:** Low

---

## Recommended Implementation Plan

### Phase 1: Prompt Improvements Only (Safest)
✅ Low risk, no architecture changes

**Changes:**
1. Add municipal certificate distinctions (tier 1 keywords)
2. Add "DO NOT CONFUSE WITH" sections (tier 2 prompts)
3. Add consistency rules (both tiers)
4. Add fallback rules (tier 2)
5. Clarify Bebauungsplan vs Lageplan (tier 2 description only)

**Expected improvement:** 76% → 85-88%
**Duplicate consistency:** 80% → 95%+

### Phase 2: Add Critical New Codes (If Phase 1 < 90%)
⚠️ Medium risk, requires architecture updates

**Add:**
- `11b_Baukosten_GU_Angebote` (construction costs)
  - Routes to: FOLDER_37_OTHERS
  - Maps to: same tracker column as 11_Verkaufspreise OR new column

**Do NOT add yet:**
- 01b, 01c (technical/energy splits) - defer to Phase 3
- 09b (Bebauungsplan) - improve description first

**Expected improvement:** 85-88% → 90-93%

### Phase 3: Fine-Grained Splits (If Phase 2 < 95%)
⚠️ High risk, significant architecture changes

**Add only if needed:**
- 01b, 01c codes with proper folder + tracker mappings

---

## Summary

**Current System:**
- 5 folders (4 core + others)
- 38 AI classification codes
- 33 tracker columns
- Simple routing: core types → specific folders, all else → Others

**Constraints:**
- Cannot add folders
- Can add AI codes if properly mapped
- Must update 3 nodes for new codes: prompts, folder routing, tracker mapping

**Recommendation:**
Start with Phase 1 (prompt improvements only) for Iteration 2. This is safest and should get us to 85-88% accuracy and 95%+ duplicate consistency without architecture changes.

Only proceed to Phase 2/3 if Phase 1 results are insufficient.
