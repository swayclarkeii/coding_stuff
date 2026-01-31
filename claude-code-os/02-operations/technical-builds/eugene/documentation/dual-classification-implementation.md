# Dual Classification Implementation for Chunk 2.5

## Overview
Add support for documents with BOTH primary and secondary classifications (e.g., Excel files with both DIN276 calculations AND sales price lists).

## Changes Required

### 1. Parse Classification Result (code-2)
**Location:** Tier 2 prompt generation
**Change:** Add dual classification instructions to tier2Prompt for WIRTSCHAFTLICHE_UNTERLAGEN category

**Addition to prompt (after "INSTRUCTIONS:"):**
```
DUAL CLASSIFICATION (For Excel files with multiple distinct document types):

If the document contains MULTIPLE distinct document types (common in Excel files with multiple tabs):
- Identify BOTH primary and secondary classifications
- Primary = most dominant/visible content
- Secondary = additional significant content type

Include in response (optional fields):
{
  "documentType": "11_Verkaufspreise",
  "tier2Confidence": 92,
  "germanName": "Verkaufspreise",
  "englishName": "Sales Prices",
  "isCoreType": false,
  "reasoning": "Brief explanation",
  "hasSecondaryClassification": true,
  "secondaryDocumentType": "10_Bautraegerkalkulation_DIN276",
  "secondaryGermanName": "Bauträgerkalkulation DIN276",
  "secondaryEnglishName": "Developer Calculation DIN276",
  "secondaryReasoning": "Brief explanation of secondary content"
}

If document has only ONE document type, omit hasSecondaryClassification or set to false.
```

### 2. Parse Claude Tier 2 Response (code-parse-claude-tier2)
**Change:** Add secondary classification field parsing

**After existing field extraction (around line 70):**
```javascript
  outputItems.push({
    json: {
      ...previousData,
      documentType: parsedResult.documentType,
      tier2Confidence: parsedResult.tier2Confidence,
      germanName: parsedResult.germanName,
      englishName: parsedResult.englishName,
      isCoreType: parsedResult.isCoreType,
      tier2Reasoning: parsedResult.reasoning || '',
      // NEW: Dual classification support
      hasSecondaryClassification: parsedResult.hasSecondaryClassification || false,
      secondaryDocumentType: parsedResult.secondaryDocumentType || null,
      secondaryGermanName: parsedResult.secondaryGermanName || null,
      secondaryEnglishName: parsedResult.secondaryEnglishName || null,
      secondaryReasoning: parsedResult.secondaryReasoning || null
    }
  });
```

### 3. Prepare Tracker Update Data (code-8)
**Change:** Add secondary classification to tracker data

**After trackerColumn assignment (around line 120):**
```javascript
  // NEW: Handle secondary classification
  let secondaryTrackerColumn = null;
  if (data.hasSecondaryClassification && data.secondaryDocumentType) {
    const normalizedSecondaryDocType = oldToNewTypeMap[data.secondaryDocumentType] || data.secondaryDocumentType;
    secondaryTrackerColumn = trackerColumnMapping[normalizedSecondaryDocType] || null;
  }

  // Prepare update data for Dokumenten_Tracker
  outputItems.push({
    json: {
      trackerColumn,
      trackerValue: '✓',
      skipTrackerUpdate: false,
      // NEW: Secondary classification
      hasSecondaryClassification: data.hasSecondaryClassification || false,
      secondaryTrackerColumn: secondaryTrackerColumn,
      secondaryTrackerValue: secondaryTrackerColumn ? '✓ (secondary)' : null,
      secondaryDocumentType: data.secondaryDocumentType || null,
      secondaryReasoning: data.secondaryReasoning || null,
      ...data
    }
  });
```

### 4. Build Google Sheets API Update Request (code-build-sheets-api-update)
**Change:** Add secondary column update

**After primary column update (around line 150):**
```javascript
  // NEW: Handle secondary classification if present
  if (data.hasSecondaryClassification && data.secondaryTrackerColumn) {
    const secondarySheetColumn = aiToSheetMapping[data.secondaryDocumentType] || data.secondaryTrackerColumn;
    const secondaryColumnLetter = columnLetterMapping[secondarySheetColumn];

    if (secondaryColumnLetter && rowNumber) {
      const secondaryRange = `${secondaryColumnLetter}${rowNumber}`;
      values.push({
        range: `'Dokumenten_Tracker'!${secondaryRange}`,
        values: [[data.secondaryTrackerValue || '✓ (sec)']]
      });
    }
  }
```

### 5. Add Notification Node
**New Node:** "Send Dual Classification Email"
**Type:** Gmail
**Position:** After "Parse Claude Tier 2 Response", conditional

**Connection:** Add IF node "Check Dual Classification" after "Parse Claude Tier 2 Response"
- Output 0 (yes): → Send Dual Classification Email → Parse Tier 2 Result
- Output 1 (no): → Parse Tier 2 Result

**IF Condition:**
- Field: `{{ $json.hasSecondaryClassification }}`
- Operation: equals
- Value: `true`

**Email Template:**
```
Subject: Document with Multiple Classifications

File: {{ $json.fileName }}

Primary Classification:
- Tier 1: {{ $json.tier1Category }}
- Tier 2: {{ $json.documentType }} ({{ $json.germanName }})
- Reasoning: {{ $json.tier2Reasoning }}

Secondary Classification:
- Tier 2: {{ $json.secondaryDocumentType }} ({{ $json.secondaryGermanName }})
- Reasoning: {{ $json.secondaryReasoning }}

Action: Review manually if categorization seems incorrect

Client: {{ $json.clientEmail }}
Tracker Link: [Dokumenten_Tracker Sheet Link]
```

## Test Case
**File:** 251103_Kalkulation Schlossberg.pdf
**Expected Output:**
- Primary: WIRTSCHAFTLICHE_UNTERLAGEN / 11_Verkaufspreise
- Secondary: WIRTSCHAFTLICHE_UNTERLAGEN / 10_Bautraegerkalkulation_DIN276

## Backward Compatibility
- Documents without secondary classification continue to work as before
- `hasSecondaryClassification` defaults to `false`
- Secondary fields are `null` when not present
- Google Sheets only updates secondary column if present

## Implementation Notes
- Focus on Excel files (.xlsx, .xls) initially
- Only apply dual classification for WIRTSCHAFTLICHE_UNTERLAGEN tier 1 (financial docs)
- Keep prompt additions <1000 chars
- JSON output must remain parseable
- Email notification goes to Eugene's email (from PROJECT_REFERENCE.md)
