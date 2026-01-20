# V8 Implementation Specification
## Eugene Document Organizer - 2-Tier Classification

**Date:** 2026-01-12
**Workflow:** AMA Chunk 2.5 (ID: okg8wTqLtPUwjQ18)
**Agent:** solution-builder-agent

---

## Overview

This document contains the complete implementation specification for V8's 2-tier hierarchical classification system.

**Changes Summary:**
- Modify 4 existing nodes
- Add 5 new nodes
- Total: 18 → 23 nodes (not 24 - revised count)

**Architecture:**
1. **Tier 1**: Classify into 4 broad categories (OBJEKTUNTERLAGEN, WIRTSCHAFTLICHE, RECHTLICHE, SONSTIGES)
2. **Tier 2**: Classify into specific document type (6-14 types per category)
3. **Action Mapping**: Route to CORE/SECONDARY/LOW_CONFIDENCE based on document type
4. **File Rename**: Add confidence score to filename
5. **Folder Routing**: 4 CORE types → specific folders, 34 SECONDARY → holding folders

---

## Document Type Taxonomy

### CORE Types (4) - Specific Folder + Tracker Update

| # | German Name | English Name | Folder | Tracker Column |
|---|-------------|--------------|--------|----------------|
| 01 | Projektbeschreibung | Exposé/Project Description | 01_Expose | Status_Expose |
| 03 | Grundbuchauszug | Land Register Extract | 02_Grundbuch | Status_Grundbuch |
| 10 | Bautraegerkalkulation_DIN276 | Developer Calculation | 03_Calculation | Status_Calculation |
| 36 | Exit_Strategie | Exit Strategy | 04_Exit_Strategy | Status_Exit_Strategy |

### SECONDARY Types (34) - Holding Folders, No Tracker

**OBJEKTUNTERLAGEN (Property/Object Documents) - 11 secondary types:**
- 02_Kaufvertrag (Purchase Agreement)
- 04_Eintragungsbewilligungen (Entry Permits)
- 05_Bodenrichtwert (Land Value)
- 06_Baulastenverzeichnis (Building Encumbrance Register)
- 07_Altlastenkataster (Contaminated Sites Register)
- 08_Baugrundgutachten (Soil Survey)
- 09_Lageplan (Site Plan)
- 15_Flaechenberechnung_DIN277 (Area Calculation DIN277)
- 16_GU_Werkvertraege (General Contractor Agreements)
- 17_Bauzeichnungen (Construction Drawings)
- 18_Baugenehmigung (Building Permit)

**WIRTSCHAFTLICHE_UNTERLAGEN (Financial/Economic Documents) - 12 types:**
- 11_Verkaufspreise (Sales Prices)
- 12_Bauzeitenplan_Liquiditaet (Construction Schedule & Liquidity)
- 13_Vertriebsweg (Distribution Channel)
- 14_Bau_Ausstattungsbeschreibung (Construction & Equipment Description)
- 19_Teilungserklaerung (Declaration of Division)
- 20_Versicherungen (Insurance)
- 21_Muster_Verkaufsvertrag (Sample Sales Contract)
- 23_Umsatzsteuervoranmeldung (VAT Advance Return)
- 24_BWA (Business Evaluation)
- 25_Jahresabschluss (Annual Financial Statement)
- 26_Finanzierungsbestaetigung (Financing Confirmation)
- 27_Darlehensvertrag (Loan Agreement)

**RECHTLICHE_UNTERLAGEN (Legal/Compliance Documents) - 6 types:**
- 28_Gesellschaftsvertrag (Partnership Agreement)
- 29_Handelsregisterauszug (Commercial Register Extract)
- 30_Gewerbeanmeldung (Business Registration)
- 31_Steuer_ID (Tax ID)
- 32_Freistellungsbescheinigung (Exemption Certificate)
- 33_Vollmachten (Powers of Attorney)

**SONSTIGES (Miscellaneous) - 5 types:**
- 22_Gutachterauftrag (Expert Assignment)
- 34_Korrespondenz (Correspondence)
- 35_Sonstiges_Allgemein (General Miscellaneous)
- 37_Others (Others)
- 38_Unknowns (Unknowns)

---

## Tier 1: Category Classification Prompt

### Node: code-1 (Build AI Classification Prompt)

**PURPOSE:** Build prompt for Tier 1 classification (4 categories)

**INPUT:**
- `$json.filename` - document filename
- `$json.clientEmail` - client email

**CODE:**
```javascript
// Build Tier 1 Classification Prompt
// Classify document into 1 of 4 broad categories

const filename = $input.first().json.filename;
const clientEmail = $input.first().json.clientEmail;

// Tier 1 Prompt: Classify into 4 broad categories
const tier1Prompt = `You are a German real estate document classifier for AMA Capital.

TASK: Classify this document into ONE of 4 broad categories based on the filename.

FILENAME: ${filename}
CLIENT: ${clientEmail}

CATEGORIES:

1. OBJEKTUNTERLAGEN (Property/Object Documents)
   Keywords: Projekt, Beschreibung, Expose, Grundbuch, Kaufvertrag, Bau, Lageplan, Zeichnungen, Genehmigung, DIN276, DIN277, Werkvertrag, Flaeche
   Examples: Project descriptions, land register, purchase agreements, building permits, construction drawings, calculations

2. WIRTSCHAFTLICHE_UNTERLAGEN (Financial/Economic Documents)
   Keywords: Verkauf, Preis, Bauzeitenplan, Liquiditaet, Vertrieb, Ausstattung, Teilung, Versicherung, Umsatzsteuer, BWA, Jahresabschluss, Finanzierung, Darlehen
   Examples: Sales prices, construction schedules, insurance, VAT returns, financial statements, loan agreements

3. RECHTLICHE_UNTERLAGEN (Legal/Compliance Documents)
   Keywords: Gesellschaft, Vertrag, Handelsregister, Gewerbe, Steuer, ID, Freistellung, Vollmacht
   Examples: Partnership agreements, commercial register, business registration, tax ID, powers of attorney

4. SONSTIGES (Miscellaneous)
   Keywords: Gutachter, Korrespondenz, Sonstiges, Others
   Examples: Expert assignments, correspondence, general miscellaneous

INSTRUCTIONS:
1. Analyze the filename for German keywords
2. Match to the most appropriate category
3. Provide confidence score (0-100)
4. Explain your reasoning in 1-2 sentences

RESPONSE FORMAT (JSON only, no markdown):
{
  "tier1Category": "OBJEKTUNTERLAGEN | WIRTSCHAFTLICHE_UNTERLAGEN | RECHTLICHE_UNTERLAGEN | SONSTIGES",
  "tier1Confidence": 85,
  "reasoning": "Brief explanation of why this category was chosen"
}

STRICT RULES:
- Response must be valid JSON only
- tier1Confidence must be 0-100 number
- tier1Category must be exactly one of the 4 options above
- No markdown formatting
- No code blocks
- No explanatory text outside JSON`;

return {
  json: {
    tier1Prompt,
    filename,
    clientEmail,
    // Pass through all input data
    ...($input.first().json)
  }
};
```

**OUTPUT:**
- `tier1Prompt` - Complete prompt for GPT-4 Tier 1 classification
- All input data passed through

---

## Tier 2: Dynamic Prompt Builder

### Node: code-2 (Parse Tier 1 + Build Tier 2 Prompt)

**PURPOSE:** Parse Tier 1 result and build category-specific Tier 2 prompt

**INPUT:**
- Tier 1 GPT-4 response from `http-openai-1`

**CODE:**
```javascript
// Parse Tier 1 Classification Result + Build Dynamic Tier 2 Prompt

const response = $input.first().json;

// Extract Tier 1 classification from GPT-4 response
let tier1Result;
try {
  // GPT-4 response is in response.choices[0].message.content
  const content = response.choices[0].message.content;
  tier1Result = JSON.parse(content);
} catch (error) {
  // If parsing fails, return error for LOW_CONFIDENCE routing
  return {
    json: {
      error: 'Failed to parse Tier 1 classification',
      tier1Category: 'UNKNOWN',
      tier1Confidence: 0,
      ...($input.first().json)
    }
  };
}

const { tier1Category, tier1Confidence, reasoning } = tier1Result;

// THRESHOLD CHECK: Tier 1 confidence must be >= 60%
if (tier1Confidence < 60) {
  return {
    json: {
      tier1Category,
      tier1Confidence,
      tier1Reasoning: reasoning,
      lowConfidence: true,
      confidenceFailureStage: 'tier1',
      ...($input.first().json)
    }
  };
}

// Build category-specific Tier 2 prompt
const filename = $input.first().json.filename;
const clientEmail = $input.first().json.clientEmail;

let tier2Prompt = '';

// === OBJEKTUNTERLAGEN (14 types) ===
if (tier1Category === 'OBJEKTUNTERLAGEN') {
  tier2Prompt = `You are a German real estate document classifier for AMA Capital.

TIER 1 RESULT: This document was classified as OBJEKTUNTERLAGEN (Property/Object Documents) with ${tier1Confidence}% confidence.

TASK: Now classify into the SPECIFIC document type from the list below.

FILENAME: ${filename}
CLIENT: ${clientEmail}

SPECIFIC TYPES (choose ONE):

01_Projektbeschreibung (Exposé/Project Description) ⭐ CORE
   Keywords: Projekt, Beschreibung, Expose, Overview, Proposal
   Description: Project overview, property description, investment proposal

02_Kaufvertrag (Purchase Agreement)
   Keywords: Kauf, Vertrag, Purchase, Agreement
   Description: Property purchase contract

03_Grundbuchauszug (Land Register Extract) ⭐ CORE
   Keywords: Grundbuch, Land, Register, Auszug
   Description: Official land registry extract

04_Eintragungsbewilligungen (Entry Permits)
   Keywords: Eintragung, Bewilligung, Entry, Permit
   Description: Permits for land register entries

05_Bodenrichtwert (Land Value)
   Keywords: Boden, Richtwert, Land, Value
   Description: Official land value assessment

06_Baulastenverzeichnis (Building Encumbrance Register)
   Keywords: Baulast, Verzeichnis, Encumbrance
   Description: Register of building encumbrances

07_Altlastenkataster (Contaminated Sites Register)
   Keywords: Altlast, Kataster, Contaminated
   Description: Register of contaminated sites

08_Baugrundgutachten (Soil Survey)
   Keywords: Baugrund, Gutachten, Soil, Survey
   Description: Soil conditions assessment

09_Lageplan (Site Plan)
   Keywords: Lage, Plan, Site
   Description: Site location plan

10_Bautraegerkalkulation_DIN276 (Developer Calculation) ⭐ CORE
   Keywords: Bautraeger, Kalkulation, DIN276, Calculation
   Description: Developer cost calculation per DIN276 standard

15_Flaechenberechnung_DIN277 (Area Calculation DIN277)
   Keywords: Flaeche, Berechnung, DIN277, Area
   Description: Area calculation per DIN277 standard

16_GU_Werkvertraege (General Contractor Agreements)
   Keywords: GU, Werkvertrag, Contractor, Agreement
   Description: General contractor work agreements

17_Bauzeichnungen (Construction Drawings)
   Keywords: Bau, Zeichnung, Construction, Drawing
   Description: Construction and architectural drawings

18_Baugenehmigung (Building Permit)
   Keywords: Bau, Genehmigung, Building, Permit
   Description: Official building permit

INSTRUCTIONS:
1. Analyze filename for specific German keywords
2. Choose the MOST SPECIFIC type that matches
3. Provide confidence score (0-100)
4. Explain your reasoning

RESPONSE FORMAT (JSON only):
{
  "documentType": "01_Projektbeschreibung",
  "tier2Confidence": 88,
  "germanName": "Projektbeschreibung",
  "englishName": "Exposé/Project Description",
  "isCoreType": true,
  "reasoning": "Brief explanation"
}

STRICT RULES:
- documentType must EXACTLY match one of the codes above (e.g., "01_Projektbeschreibung")
- isCoreType: true for ⭐ CORE types, false for others
- Valid JSON only, no markdown`;
}

// === WIRTSCHAFTLICHE_UNTERLAGEN (12 types) ===
else if (tier1Category === 'WIRTSCHAFTLICHE_UNTERLAGEN') {
  tier2Prompt = `You are a German real estate document classifier for AMA Capital.

TIER 1 RESULT: This document was classified as WIRTSCHAFTLICHE_UNTERLAGEN (Financial/Economic Documents) with ${tier1Confidence}% confidence.

TASK: Now classify into the SPECIFIC document type from the list below.

FILENAME: ${filename}
CLIENT: ${clientEmail}

SPECIFIC TYPES (choose ONE):

11_Verkaufspreise (Sales Prices)
   Keywords: Verkauf, Preis, Sales, Price
   Description: Sales price lists and calculations

12_Bauzeitenplan_Liquiditaet (Construction Schedule & Liquidity)
   Keywords: Bauzeit, Plan, Liquiditaet, Schedule
   Description: Construction timeline and liquidity planning

13_Vertriebsweg (Distribution Channel)
   Keywords: Vertrieb, Weg, Distribution, Channel
   Description: Sales and distribution strategy

14_Bau_Ausstattungsbeschreibung (Construction & Equipment Description)
   Keywords: Bau, Ausstattung, Beschreibung, Equipment
   Description: Construction specifications and equipment details

19_Teilungserklaerung (Declaration of Division)
   Keywords: Teilung, Erklaerung, Division, Declaration
   Description: Property division declaration

20_Versicherungen (Insurance)
   Keywords: Versicherung, Insurance
   Description: Insurance policies and documentation

21_Muster_Verkaufsvertrag (Sample Sales Contract)
   Keywords: Muster, Verkauf, Vertrag, Sample, Sales
   Description: Template sales contract

23_Umsatzsteuervoranmeldung (VAT Advance Return)
   Keywords: Umsatz, Steuer, Voranmeldung, VAT
   Description: VAT advance return filings

24_BWA (Business Evaluation)
   Keywords: BWA, Business, Evaluation
   Description: Business evaluation report

25_Jahresabschluss (Annual Financial Statement)
   Keywords: Jahres, Abschluss, Annual, Financial
   Description: Annual financial statement

26_Finanzierungsbestaetigung (Financing Confirmation)
   Keywords: Finanzierung, Bestaetigung, Financing, Confirmation
   Description: Financing approval or confirmation

27_Darlehensvertrag (Loan Agreement)
   Keywords: Darlehen, Vertrag, Loan, Agreement
   Description: Loan contract

INSTRUCTIONS:
1. Analyze filename for specific German keywords
2. Choose the MOST SPECIFIC type that matches
3. Provide confidence score (0-100)
4. Explain your reasoning

RESPONSE FORMAT (JSON only):
{
  "documentType": "11_Verkaufspreise",
  "tier2Confidence": 92,
  "germanName": "Verkaufspreise",
  "englishName": "Sales Prices",
  "isCoreType": false,
  "reasoning": "Brief explanation"
}

STRICT RULES:
- documentType must EXACTLY match one of the codes above
- isCoreType: false for all WIRTSCHAFTLICHE types (none are CORE)
- Valid JSON only, no markdown`;
}

// === RECHTLICHE_UNTERLAGEN (6 types) ===
else if (tier1Category === 'RECHTLICHE_UNTERLAGEN') {
  tier2Prompt = `You are a German real estate document classifier for AMA Capital.

TIER 1 RESULT: This document was classified as RECHTLICHE_UNTERLAGEN (Legal/Compliance Documents) with ${tier1Confidence}% confidence.

TASK: Now classify into the SPECIFIC document type from the list below.

FILENAME: ${filename}
CLIENT: ${clientEmail}

SPECIFIC TYPES (choose ONE):

28_Gesellschaftsvertrag (Partnership Agreement)
   Keywords: Gesellschaft, Vertrag, Partnership, Agreement
   Description: Company partnership or shareholder agreement

29_Handelsregisterauszug (Commercial Register Extract)
   Keywords: Handelsregister, Auszug, Commercial, Register
   Description: Commercial register extract

30_Gewerbeanmeldung (Business Registration)
   Keywords: Gewerbe, Anmeldung, Business, Registration
   Description: Business registration documentation

31_Steuer_ID (Tax ID)
   Keywords: Steuer, ID, Tax
   Description: Tax identification number

32_Freistellungsbescheinigung (Exemption Certificate)
   Keywords: Freistellung, Bescheinigung, Exemption, Certificate
   Description: Tax exemption certificate

33_Vollmachten (Powers of Attorney)
   Keywords: Vollmacht, Power, Attorney
   Description: Power of attorney documents

INSTRUCTIONS:
1. Analyze filename for specific German keywords
2. Choose the MOST SPECIFIC type that matches
3. Provide confidence score (0-100)
4. Explain your reasoning

RESPONSE FORMAT (JSON only):
{
  "documentType": "28_Gesellschaftsvertrag",
  "tier2Confidence": 85,
  "germanName": "Gesellschaftsvertrag",
  "englishName": "Partnership Agreement",
  "isCoreType": false,
  "reasoning": "Brief explanation"
}

STRICT RULES:
- documentType must EXACTLY match one of the codes above
- isCoreType: false for all RECHTLICHE types (none are CORE)
- Valid JSON only, no markdown`;
}

// === SONSTIGES (6 types) ===
else if (tier1Category === 'SONSTIGES') {
  tier2Prompt = `You are a German real estate document classifier for AMA Capital.

TIER 1 RESULT: This document was classified as SONSTIGES (Miscellaneous) with ${tier1Confidence}% confidence.

TASK: Now classify into the SPECIFIC document type from the list below.

FILENAME: ${filename}
CLIENT: ${clientEmail}

SPECIFIC TYPES (choose ONE):

22_Gutachterauftrag (Expert Assignment)
   Keywords: Gutachter, Auftrag, Expert, Assignment
   Description: Expert assessment assignment

34_Korrespondenz (Correspondence)
   Keywords: Korrespondenz, Email, Brief, Letter, Correspondence
   Description: Email correspondence and letters

35_Sonstiges_Allgemein (General Miscellaneous)
   Keywords: Sonstiges, Misc, General
   Description: General miscellaneous documents

36_Exit_Strategie (Exit Strategy) ⭐ CORE
   Keywords: Exit, Strategie, Strategy
   Description: Investment exit strategy

37_Others (Others)
   Keywords: Other, Andere
   Description: Other unclassified documents

38_Unknowns (Unknowns)
   Keywords: Unknown, Unbekannt
   Description: Unknown document type

INSTRUCTIONS:
1. Analyze filename for specific German keywords
2. Choose the MOST SPECIFIC type that matches
3. Provide confidence score (0-100)
4. Explain your reasoning
5. Use 38_Unknowns ONLY if truly unclear

RESPONSE FORMAT (JSON only):
{
  "documentType": "36_Exit_Strategie",
  "tier2Confidence": 95,
  "germanName": "Exit Strategie",
  "englishName": "Exit Strategy",
  "isCoreType": true,
  "reasoning": "Brief explanation"
}

STRICT RULES:
- documentType must EXACTLY match one of the codes above
- isCoreType: true ONLY for 36_Exit_Strategie
- Valid JSON only, no markdown`;
}

// Unknown category fallback
else {
  return {
    json: {
      error: 'Unknown Tier 1 category',
      tier1Category,
      tier1Confidence,
      lowConfidence: true,
      confidenceFailureStage: 'tier1_unknown_category',
      ...($input.first().json)
    }
  };
}

return {
  json: {
    tier1Category,
    tier1Confidence,
    tier1Reasoning: reasoning,
    tier2Prompt,
    ...($input.first().json)
  }
};
```

**OUTPUT:**
- `tier1Category` - Category from Tier 1
- `tier1Confidence` - Confidence score from Tier 1
- `tier1Reasoning` - Why that category was chosen
- `tier2Prompt` - Dynamic Tier 2 prompt (category-specific)
- `lowConfidence: true` if Tier 1 confidence < 60%

---

## Phase 3: Tier 2 Implementation

### Node: http-openai-2 (Tier 2 GPT-4 API Call)

**PURPOSE:** Call GPT-4 with dynamic Tier 2 prompt

**TYPE:** HTTP Request
**METHOD:** POST
**URL:** `https://api.openai.com/v1/chat/completions`

**AUTHENTICATION:**
- Type: Predefined Credential
- Credential: `OpenAI API (Sway)`

**BODY (JSON):**
```json
{
  "model": "gpt-4",
  "messages": [
    {
      "role": "user",
      "content": "={{ $json.tier2Prompt }}"
    }
  ],
  "temperature": 0.3,
  "max_tokens": 300
}
```

**OPTIONS:**
- Response Format: JSON

**CONNECTION:**
- Input: `code-2` (Parse Tier 1 + Build Tier 2 Prompt)
- Output: `code-tier2-parse` (Parse Tier 2 Result)

---

### Node: code-tier2-parse (Parse Tier 2 Result)

**PURPOSE:** Extract and validate Tier 2 classification results

**CODE:**
```javascript
// Parse Tier 2 Classification Result

const response = $input.first().json;

// Extract Tier 2 classification from GPT-4 response
let tier2Result;
try {
  const content = response.choices[0].message.content;
  tier2Result = JSON.parse(content);
} catch (error) {
  // Parsing failed - route to LOW_CONFIDENCE
  return {
    json: {
      error: 'Failed to parse Tier 2 classification',
      lowConfidence: true,
      confidenceFailureStage: 'tier2_parse_error',
      ...($input.first().json)
    }
  };
}

const {
  documentType,
  tier2Confidence,
  germanName,
  englishName,
  isCoreType,
  reasoning: tier2Reasoning
} = tier2Result;

// THRESHOLD CHECK: Tier 2 confidence must be >= 70%
if (tier2Confidence < 70) {
  return {
    json: {
      documentType,
      tier2Confidence,
      lowConfidence: true,
      confidenceFailureStage: 'tier2',
      ...($input.first().json)
    }
  };
}

// Calculate combined confidence
const tier1Confidence = $input.first().json.tier1Confidence;
const combinedConfidence = Math.round((tier1Confidence + tier2Confidence) / 2);

return {
  json: {
    // Classification results
    documentType,
    tier2Confidence,
    combinedConfidence,
    germanName,
    englishName,
    isCoreType,
    tier2Reasoning,
    // Pass through Tier 1 data
    tier1Category: $input.first().json.tier1Category,
    tier1Confidence: $input.first().json.tier1Confidence,
    tier1Reasoning: $input.first().json.tier1Reasoning,
    // Pass through original data
    ...($input.first().json)
  }
};
```

**OUTPUT:**
- `documentType` - Specific document type (e.g., "01_Projektbeschreibung")
- `tier2Confidence` - Tier 2 confidence score
- `combinedConfidence` - Average of Tier 1 + Tier 2
- `germanName` - German document name
- `englishName` - English document name
- `isCoreType` - Boolean (true for 4 CORE types)
- `lowConfidence: true` if Tier 2 confidence < 70%

---

## Phase 4: Action Mapping and Routing

### Node: code-action-mapper (Action Determination)

**PURPOSE:** Determine routing action (CORE/SECONDARY/LOW_CONFIDENCE)

**CODE:**
```javascript
// Action Mapper: Determine routing based on classification results

const data = $input.first().json;

// Check for low confidence flags
if (data.lowConfidence === true) {
  return {
    json: {
      actionType: 'LOW_CONFIDENCE',
      destinationFolder: '38_Unknowns',
      trackerUpdate: false,
      sendNotification: true,
      ...data
    }
  };
}

// Check if CORE type
if (data.isCoreType === true) {
  // CORE types: Specific folder + tracker update
  return {
    json: {
      actionType: 'CORE',
      trackerUpdate: true,
      sendNotification: false,
      ...data
    }
  };
}

// SECONDARY types: Holding folder + no tracker
return {
  json: {
    actionType: 'SECONDARY',
    trackerUpdate: false,
    sendNotification: false,
    ...data
  }
};
```

**OUTPUT:**
- `actionType` - "CORE" | "SECONDARY" | "LOW_CONFIDENCE"
- `trackerUpdate` - Boolean (true only for CORE)
- `sendNotification` - Boolean (true only for LOW_CONFIDENCE)
- `destinationFolder` - "38_Unknowns" for LOW_CONFIDENCE

---

### Node: drive-rename (Rename File with Confidence)

**PURPOSE:** Rename file to include confidence score

**TYPE:** Google Drive
**OPERATION:** Update a File
**RESOURCE:** File

**CONFIGURATION:**
- **File ID:** `={{ $json.fileId }}`
- **Name:**
```javascript
={{
  const actionType = $json.actionType;
  const documentType = $json.documentType;
  const combinedConfidence = $json.combinedConfidence;
  const originalFilename = $json.filename;

  // Extract file extension
  const extension = originalFilename.split('.').pop();

  // Extract client name from email (e.g., villa_martens@ama.de → villa_martens)
  const clientEmail = $json.clientEmail;
  const clientName = clientEmail.split('@')[0];

  // Build type code (snake_case English name from documentType)
  let typeCode;

  if (actionType === 'LOW_CONFIDENCE') {
    typeCode = 'REVIEW_unknown';
  } else {
    // Map document type to English snake_case
    const typeMapping = {
      '01_Projektbeschreibung': 'CORE_expose',
      '02_Kaufvertrag': 'purchase_agreement',
      '03_Grundbuchauszug': 'CORE_grundbuch',
      '04_Eintragungsbewilligungen': 'entry_permits',
      '05_Bodenrichtwert': 'land_value',
      '06_Baulastenverzeichnis': 'building_encumbrance',
      '07_Altlastenkataster': 'contaminated_sites',
      '08_Baugrundgutachten': 'soil_survey',
      '09_Lageplan': 'site_plan',
      '10_Bautraegerkalkulation_DIN276': 'CORE_calculation',
      '11_Verkaufspreise': 'sales_prices',
      '12_Bauzeitenplan_Liquiditaet': 'construction_schedule',
      '13_Vertriebsweg': 'distribution_channel',
      '14_Bau_Ausstattungsbeschreibung': 'construction_specs',
      '15_Flaechenberechnung_DIN277': 'area_calculation',
      '16_GU_Werkvertraege': 'contractor_agreements',
      '17_Bauzeichnungen': 'construction_drawings',
      '18_Baugenehmigung': 'building_permit',
      '19_Teilungserklaerung': 'division_declaration',
      '20_Versicherungen': 'insurance',
      '21_Muster_Verkaufsvertrag': 'sample_sales_contract',
      '22_Gutachterauftrag': 'expert_assignment',
      '23_Umsatzsteuervoranmeldung': 'vat_return',
      '24_BWA': 'business_evaluation',
      '25_Jahresabschluss': 'annual_financial',
      '26_Finanzierungsbestaetigung': 'financing_confirmation',
      '27_Darlehensvertrag': 'loan_agreement',
      '28_Gesellschaftsvertrag': 'partnership_agreement',
      '29_Handelsregisterauszug': 'commercial_register',
      '30_Gewerbeanmeldung': 'business_registration',
      '31_Steuer_ID': 'tax_id',
      '32_Freistellungsbescheinigung': 'exemption_certificate',
      '33_Vollmachten': 'power_of_attorney',
      '34_Korrespondenz': 'correspondence',
      '35_Sonstiges_Allgemein': 'general_misc',
      '36_Exit_Strategie': 'CORE_exit_strategy',
      '37_Others': 'others',
      '38_Unknowns': 'unknowns'
    };

    typeCode = typeMapping[documentType] || 'unknown';
  }

  // Build filename: typeCode_clientName_confidencePct.ext
  return `${typeCode}_${clientName}_${combinedConfidence}pct.${extension}`;
}}
```

**CONNECTION:**
- Input: `code-action-mapper`
- Output: `sheets-1` (Lookup Client in Client_Tracker)

---

### Node: code-4 (MODIFIED - Get Destination Folder ID)

**PURPOSE:** Map document type to destination folder ID

**CHANGES:** Extend mapping to include 38 types + 4 holding folders

**CODE:**
```javascript
// Get Destination Folder ID - V8 Extended Mapping

const data = $input.first().json;
const actionType = data.actionType;
const documentType = data.documentType;
const tier1Category = data.tier1Category;

// Get folder IDs from AMA_Folder_IDs sheet
const folderData = data; // Folder IDs are already in the data from sheets-3

let destinationFolderId;
let destinationFolderName;

// === LOW_CONFIDENCE → 38_Unknowns ===
if (actionType === 'LOW_CONFIDENCE') {
  destinationFolderId = folderData.FOLDER_38_Unknowns;
  destinationFolderName = '38_Unknowns';
}

// === CORE TYPES → Specific Folders ===
else if (actionType === 'CORE') {
  const coreMapping = {
    '01_Projektbeschreibung': { id: 'FOLDER_01_Expose', name: '01_Expose' },
    '03_Grundbuchauszug': { id: 'FOLDER_02_Grundbuch', name: '02_Grundbuch' },
    '10_Bautraegerkalkulation_DIN276': { id: 'FOLDER_03_Calculation', name: '03_Calculation' },
    '36_Exit_Strategie': { id: 'FOLDER_04_Exit_Strategy', name: '04_Exit_Strategy' }
  };

  const mapping = coreMapping[documentType];
  if (mapping) {
    destinationFolderId = folderData[mapping.id];
    destinationFolderName = mapping.name;
  } else {
    // Fallback: should not happen if isCoreType is correct
    destinationFolderId = folderData.FOLDER_38_Unknowns;
    destinationFolderName = '38_Unknowns (CORE mapping error)';
  }
}

// === SECONDARY TYPES → Holding Folders ===
else if (actionType === 'SECONDARY') {
  // Map based on Tier 1 category to corresponding holding folder
  const holdingMapping = {
    'OBJEKTUNTERLAGEN': { id: 'FOLDER_HOLDING_PROPERTY', name: '_Holding_Property' },
    'WIRTSCHAFTLICHE_UNTERLAGEN': { id: 'FOLDER_HOLDING_FINANCIAL', name: '_Holding_Financial' },
    'RECHTLICHE_UNTERLAGEN': { id: 'FOLDER_HOLDING_LEGAL', name: '_Holding_Legal' },
    'SONSTIGES': { id: 'FOLDER_HOLDING_MISC', name: '_Holding_Misc' }
  };

  const mapping = holdingMapping[tier1Category];
  if (mapping) {
    destinationFolderId = folderData[mapping.id];
    destinationFolderName = mapping.name;
  } else {
    // Fallback
    destinationFolderId = folderData.FOLDER_38_Unknowns;
    destinationFolderName = '38_Unknowns (SECONDARY mapping error)';
  }
}

// Unknown action type fallback
else {
  destinationFolderId = folderData.FOLDER_38_Unknowns;
  destinationFolderName = '38_Unknowns (Unknown action type)';
}

return {
  json: {
    destinationFolderId,
    destinationFolderName,
    ...data
  }
};
```

**OUTPUT:**
- `destinationFolderId` - Google Drive folder ID
- `destinationFolderName` - Folder name (for logging)

---

### Node: code-8 (MODIFIED - Prepare Tracker Update Data)

**PURPOSE:** Conditionally prepare tracker data ONLY for CORE types

**CHANGES:** Add conditional check for `trackerUpdate` flag

**CODE:**
```javascript
// Prepare Tracker Update Data - V8 Conditional (CORE types only)

const data = $input.first().json;

// CONDITIONAL: Only prepare tracker data if trackerUpdate === true
if (data.trackerUpdate !== true) {
  // SECONDARY or LOW_CONFIDENCE: Skip tracker update, pass through to folder move
  return {
    json: {
      skipTrackerUpdate: true,
      ...data
    }
  };
}

// CORE types: Prepare tracker update data
const documentType = data.documentType;

// Map document type to tracker column
const trackerColumnMapping = {
  '01_Projektbeschreibung': 'Status_Expose',
  '03_Grundbuchauszug': 'Status_Grundbuch',
  '10_Bautraegerkalkulation_DIN276': 'Status_Calculation',
  '36_Exit_Strategie': 'Status_Exit_Strategy'
};

const trackerColumn = trackerColumnMapping[documentType];

if (!trackerColumn) {
  // Should not happen if CORE mapping is correct
  return {
    json: {
      error: 'Unknown CORE document type for tracker mapping',
      skipTrackerUpdate: true,
      ...data
    }
  };
}

// Prepare update data for Client_Tracker
const updateData = {
  [trackerColumn]: '✓'
};

return {
  json: {
    trackerColumn,
    trackerValue: '✓',
    updateData,
    skipTrackerUpdate: false,
    ...data
  }
};
```

**OUTPUT:**
- `skipTrackerUpdate` - Boolean (true for SECONDARY/LOW_CONFIDENCE)
- `trackerColumn` - Column name to update (only for CORE)
- `trackerValue` - "✓" (only for CORE)
- `updateData` - Object with column: value (only for CORE)

---

### Node: if-1 (MODIFIED - Check Status)

**PURPOSE:** Route based on `skipTrackerUpdate` flag

**CHANGES:** Add condition for skipping tracker

**CONDITIONS:**

**Condition 1: Update Tracker (CORE types)**
- Expression: `{{ $json.skipTrackerUpdate === false }}`
- Output: Connect to `sheets-2` (Update Client_Tracker Row)

**Condition 2: Skip Tracker (SECONDARY + LOW_CONFIDENCE)**
- Expression: `{{ $json.skipTrackerUpdate === true }}`
- Output: Connect to `sheets-3` (Lookup Client in AMA_Folder_IDs)
  - This skips `sheets-2` entirely

**Existing Error Path (unchanged):**
- Condition 3: `{{ $json.clientFound === false }}`
- Output: Connect to error handling (sheets-4 → 38_Unknowns)

---

## Updated Workflow Topology

### Current Flow (18 nodes):
```
trigger-1 → code-1 → http-openai-1 → code-2 → sheets-1 → code-3 → if-1
                                                                      ├─ [Success] code-8 → sheets-2 → sheets-3 → code-4 → drive-1 → code-5
                                                                      └─ [Error] sheets-4 → code-6 → drive-2 → code-7 → gmail-1
```

### New Flow (23 nodes):
```
trigger-1 → code-1 → http-openai-1 → code-2 → http-openai-2 → code-tier2-parse → code-action-mapper → drive-rename → sheets-1 → code-3 → if-1
                                                                                                                                                 ├─ [CORE] code-8 → sheets-2 → sheets-3 → code-4 → drive-1 → code-5
                                                                                                                                                 ├─ [SECONDARY] → sheets-3 → code-4 → drive-1 → code-5
                                                                                                                                                 └─ [Error] sheets-4 → code-6 → drive-2 → code-7 → gmail-1
```

**Node Count:**
- Original: 18 nodes
- Added: 5 nodes (http-openai-2, code-tier2-parse, code-action-mapper, drive-rename, + routing)
- Modified: 4 nodes (code-1, code-2, code-4, code-8, if-1)
- **Total: 23 nodes**

---

## Testing Checklist

After implementation, validate:

- [ ] Tier 1 prompt generates correctly
- [ ] Tier 1 confidence threshold (60%) enforced
- [ ] Tier 2 prompt dynamically built based on category
- [ ] Tier 2 confidence threshold (70%) enforced
- [ ] Action mapper correctly identifies CORE/SECONDARY/LOW_CONFIDENCE
- [ ] File rename includes confidence score in format: `type_client_XXpct.ext`
- [ ] CORE types route to specific folders + update tracker
- [ ] SECONDARY types route to holding folders + skip tracker
- [ ] LOW_CONFIDENCE types route to 38_Unknowns + send email
- [ ] Combined confidence calculated correctly ((T1+T2)/2)
- [ ] All 38 document types have folder mappings
- [ ] Holding folder IDs exist in AMA_Folder_IDs sheet
- [ ] Error handling for parse failures

---

## Implementation Safety Protocol

**For EACH node modification:**

1. ✅ Export workflow before change
2. ✅ Make ONE change
3. ✅ Export workflow after change
4. ✅ Validate with `n8n_validate_workflow`
5. ✅ Update V8_CHANGELOG.md
6. ✅ Test execution (if possible)

**Backup locations:**
- Pre-Phase 2: `.backups/chunk_2.5_v8.0_BEFORE_PHASE2_20260112.json`
- After each major change: `.backups/chunk_2.5_v8.0_AFTER_[node-name]_20260112.json`

---

## Next Steps

1. Review this specification with Sway for approval
2. Begin Phase 2 implementation (modify code-1, code-2)
3. Proceed to Phase 3 (add http-openai-2, code-tier2-parse)
4. Complete Phase 4 (action mapping, rename, routing)
5. Export final workflow and validate
6. Hand off to test-runner-agent for automated testing

---

**Document Version:** 1.0
**Last Updated:** 2026-01-12 20:45 CET
**Author:** solution-builder-agent
