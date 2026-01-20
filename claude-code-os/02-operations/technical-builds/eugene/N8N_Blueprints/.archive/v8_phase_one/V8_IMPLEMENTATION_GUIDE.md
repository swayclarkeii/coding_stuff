# V8 Implementation Guide
## Eugene Document Organizer - Chunk 2.5 Workflow

**Date:** 2026-01-12
**Workflow ID:** okg8wTqLtPUwjQ18
**Workflow Name:** Chunk 2.5 - Client Document Tracking (Eugene Document Organizer)
**Implementation Type:** Manual via n8n UI or automated via n8n MCP tools

---

## Prerequisites

✅ **COMPLETED:**
- Phase 0: Project structure setup
- Phase 1: Holding folders added to Chunk 0
- V8_IMPLEMENTATION_SPEC.md created and approved
- Initial backup created: `.backups/chunk_2.5_v8.0_BEFORE_PHASE2_20260112.json`

🔜 **REQUIRED BEFORE STARTING:**
- [ ] n8n UI access or n8n MCP tools available
- [ ] Workflow Chunk 2.5 (ID: okg8wTqLtPUwjQ18) is accessible
- [ ] OpenAI API credentials configured in n8n
- [ ] Google Drive credentials configured in n8n
- [ ] Google Sheets credentials configured in n8n

---

## Implementation Overview

**Total Changes:**
- **Phase 2:** Modify 2 existing nodes (code-1, code-2)
- **Phase 3:** Add 2 new nodes (http-openai-2, code-tier2-parse)
- **Phase 4:** Add 3 new nodes + modify 3 existing nodes (code-action-mapper, drive-rename, code-4, code-8, if-1)

**Final Node Count:** 18 → 23 nodes

---

## Phase 2: Tier 1 Classification (2 Node Modifications)

### Step 1: Modify code-1 (Build AI Classification Prompt)

**Node Name:** Build AI Classification Prompt
**Node ID:** code-1
**Type:** Code node
**Action:** Replace entire code block

**BACKUP FIRST:**
```bash
# Export workflow before modification
# Save to: .backups/chunk_2.5_v8.0_BEFORE_CODE1_20260112_[TIMESTAMP].json
```

**NEW CODE:**
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

**VALIDATION:**
- [ ] Code executes without errors
- [ ] Output includes `tier1Prompt` field
- [ ] Input data is passed through correctly

**EXPORT AFTER CHANGE:**
```bash
# Export workflow after modification
# Save to: .backups/chunk_2.5_v8.0_AFTER_CODE1_20260112_[TIMESTAMP].json
```

---

### Step 2: Modify code-2 (Parse Tier 1 + Build Tier 2 Prompt)

**Node Name:** Parse Classification Result
**Node ID:** code-2
**Type:** Code node
**Action:** Replace entire code block

**BACKUP FIRST:**
```bash
# Export workflow before modification
# Save to: .backups/chunk_2.5_v8.0_BEFORE_CODE2_20260112_[TIMESTAMP].json
```

**NEW CODE:**
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

**VALIDATION:**
- [ ] Code executes without errors
- [ ] Tier 1 result is parsed correctly
- [ ] Tier 2 prompt is generated based on Tier 1 category
- [ ] Low confidence routing works (< 60% threshold)
- [ ] Input data is passed through

**EXPORT AFTER CHANGE:**
```bash
# Export workflow after modification
# Save to: .backups/chunk_2.5_v8.0_AFTER_CODE2_20260112_[TIMESTAMP].json
```

---

## Phase 2 Complete

**Checklist:**
- [ ] code-1 modified successfully
- [ ] code-2 modified successfully
- [ ] Both backups created
- [ ] Both exports created after changes
- [ ] V8_CHANGELOG.md updated with Phase 2 completion

**Next Step:** Proceed to Phase 3 (add 2 new nodes)

---

## Phase 3: Tier 2 Classification (2 New Nodes)

### Step 3: Add http-openai-2 (Tier 2 GPT-4 API Call)

**Node Name:** http-openai-2
**Node Type:** HTTP Request
**Action:** Add new node after code-2

**BACKUP FIRST:**
```bash
# Export workflow before adding node
# Save to: .backups/chunk_2.5_v8.0_BEFORE_HTTP_OPENAI_2_20260112_[TIMESTAMP].json
```

**NODE CONFIGURATION:**

**Position:** Between code-2 and sheets-1 (visually)
**Connection:** Input from code-2

**HTTP Request Settings:**
- **Method:** POST
- **URL:** `https://api.openai.com/v1/chat/completions`
- **Authentication:** Predefined Credential Type
- **Credential:** `OpenAI API (Sway)` (or configured OpenAI credential)

**Body (JSON):**
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

**Options:**
- Response Format: JSON

**VALIDATION:**
- [ ] Node added successfully
- [ ] Connected to code-2 output
- [ ] OpenAI credential configured
- [ ] Request body references `$json.tier2Prompt`

**EXPORT AFTER CHANGE:**
```bash
# Export workflow after adding node
# Save to: .backups/chunk_2.5_v8.0_AFTER_HTTP_OPENAI_2_20260112_[TIMESTAMP].json
```

---

### Step 4: Add code-tier2-parse (Parse Tier 2 Result)

**Node Name:** code-tier2-parse
**Node Type:** Code
**Action:** Add new node after http-openai-2

**BACKUP FIRST:**
```bash
# Export workflow before adding node
# Save to: .backups/chunk_2.5_v8.0_BEFORE_CODE_TIER2_PARSE_20260112_[TIMESTAMP].json
```

**NODE CONFIGURATION:**

**Position:** Between http-openai-2 and sheets-1
**Connection:** Input from http-openai-2

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

**VALIDATION:**
- [ ] Node added successfully
- [ ] Connected to http-openai-2 output
- [ ] Tier 2 result parsed correctly
- [ ] Combined confidence calculated
- [ ] Low confidence routing works (< 70% threshold)

**EXPORT AFTER CHANGE:**
```bash
# Export workflow after adding node
# Save to: .backups/chunk_2.5_v8.0_AFTER_CODE_TIER2_PARSE_20260112_[TIMESTAMP].json
```

---

## Phase 3 Complete

**Checklist:**
- [ ] http-openai-2 added successfully
- [ ] code-tier2-parse added successfully
- [ ] Both backups created
- [ ] Both exports created after changes
- [ ] V8_CHANGELOG.md updated with Phase 3 completion

**Next Step:** Proceed to Phase 4 (add 3 nodes, modify 3 nodes)

---

## Phase 4: Action Mapping and Routing (6 Node Changes)

### Step 5: Add code-action-mapper (Action Determination)

**Node Name:** code-action-mapper
**Node Type:** Code
**Action:** Add new node after code-tier2-parse

**BACKUP FIRST:**
```bash
# Export workflow before adding node
# Save to: .backups/chunk_2.5_v8.0_BEFORE_ACTION_MAPPER_20260112_[TIMESTAMP].json
```

**NODE CONFIGURATION:**

**Position:** Between code-tier2-parse and sheets-1
**Connection:** Input from code-tier2-parse

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

**VALIDATION:**
- [ ] Node added successfully
- [ ] Connected to code-tier2-parse output
- [ ] Action type determined correctly (CORE/SECONDARY/LOW_CONFIDENCE)
- [ ] Tracker update flag set correctly

**EXPORT AFTER CHANGE:**
```bash
# Export workflow after adding node
# Save to: .backups/chunk_2.5_v8.0_AFTER_ACTION_MAPPER_20260112_[TIMESTAMP].json
```

---

### Step 6: Add drive-rename (Rename File with Confidence)

**Node Name:** drive-rename
**Node Type:** Google Drive
**Action:** Add new node after code-action-mapper

**BACKUP FIRST:**
```bash
# Export workflow before adding node
# Save to: .backups/chunk_2.5_v8.0_BEFORE_DRIVE_RENAME_20260112_[TIMESTAMP].json
```

**NODE CONFIGURATION:**

**Position:** Between code-action-mapper and sheets-1
**Connection:** Input from code-action-mapper

**Google Drive Settings:**
- **Resource:** File
- **Operation:** Update
- **File ID:** `={{ $json.fileId }}`

**Update Fields:**
- **Name:** Use expression below

**Name Expression:**
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

**VALIDATION:**
- [ ] Node added successfully
- [ ] Connected to code-action-mapper output
- [ ] File renamed with confidence score
- [ ] Filename format: `typeCode_clientName_XXpct.ext`

**EXPORT AFTER CHANGE:**
```bash
# Export workflow after adding node
# Save to: .backups/chunk_2.5_v8.0_AFTER_DRIVE_RENAME_20260112_[TIMESTAMP].json
```

---

### Step 7: Modify code-4 (Extended Folder Mapping)

**Node Name:** Get Destination Folder ID
**Node ID:** code-4
**Type:** Code node
**Action:** Replace entire code block

**BACKUP FIRST:**
```bash
# Export workflow before modification
# Save to: .backups/chunk_2.5_v8.0_BEFORE_CODE4_20260112_[TIMESTAMP].json
```

**NEW CODE:**
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

**VALIDATION:**
- [ ] Code executes without errors
- [ ] CORE types map to specific folders (4 types)
- [ ] SECONDARY types map to holding folders (4 folders)
- [ ] LOW_CONFIDENCE maps to 38_Unknowns
- [ ] Folder IDs retrieved from AMA_Folder_IDs sheet

**EXPORT AFTER CHANGE:**
```bash
# Export workflow after modification
# Save to: .backups/chunk_2.5_v8.0_AFTER_CODE4_20260112_[TIMESTAMP].json
```

---

### Step 8: Modify code-8 (Conditional Tracker Update)

**Node Name:** Prepare Tracker Update Data
**Node ID:** code-8
**Type:** Code node
**Action:** Replace entire code block

**BACKUP FIRST:**
```bash
# Export workflow before modification
# Save to: .backups/chunk_2.5_v8.0_BEFORE_CODE8_20260112_[TIMESTAMP].json
```

**NEW CODE:**
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

**VALIDATION:**
- [ ] Code executes without errors
- [ ] CORE types prepare tracker update data
- [ ] SECONDARY/LOW_CONFIDENCE skip tracker (skipTrackerUpdate: true)
- [ ] Tracker column mapping correct for 4 CORE types

**EXPORT AFTER CHANGE:**
```bash
# Export workflow after modification
# Save to: .backups/chunk_2.5_v8.0_AFTER_CODE8_20260112_[TIMESTAMP].json
```

---

### Step 9: Modify if-1 (Add skipTrackerUpdate Routing)

**Node Name:** Check Status
**Node ID:** if-1
**Type:** IF node
**Action:** Add new condition for skipTrackerUpdate routing

**BACKUP FIRST:**
```bash
# Export workflow before modification
# Save to: .backups/chunk_2.5_v8.0_BEFORE_IF1_20260112_[TIMESTAMP].json
```

**NEW CONFIGURATION:**

**Condition 1: Update Tracker (CORE types)**
- **Expression:** `{{ $json.skipTrackerUpdate === false }}`
- **Output:** Connect to `sheets-2` (Update Client_Tracker Row)
- **Label:** "CORE - Update Tracker"

**Condition 2: Skip Tracker (SECONDARY + LOW_CONFIDENCE)**
- **Expression:** `{{ $json.skipTrackerUpdate === true }}`
- **Output:** Connect to `sheets-3` (Lookup Client in AMA_Folder_IDs)
- **Label:** "SECONDARY/LOW - Skip Tracker"
- **NOTE:** This path skips `sheets-2` entirely

**Existing Error Path (unchanged):**
- **Condition 3:** `{{ $json.clientFound === false }}`
- **Output:** Connect to error handling (sheets-4 → 38_Unknowns)
- **Label:** "Client Not Found"

**CRITICAL CONNECTION CHANGE:**
From code-action-mapper node, route to:
1. drive-rename (new node)
2. drive-rename → sheets-1 (unchanged)
3. sheets-1 → code-3 (unchanged)
4. code-3 → if-1 (unchanged, but if-1 now has new routing logic)

**VALIDATION:**
- [ ] New condition added successfully
- [ ] CORE path routes through sheets-2 (tracker update)
- [ ] SECONDARY path bypasses sheets-2 (skips tracker)
- [ ] Error path unchanged
- [ ] All connections updated correctly

**EXPORT AFTER CHANGE:**
```bash
# Export workflow after modification
# Save to: .backups/chunk_2.5_v8.0_AFTER_IF1_20260112_[TIMESTAMP].json
```

---

## Phase 4 Complete

**Checklist:**
- [ ] code-action-mapper added successfully
- [ ] drive-rename added successfully
- [ ] code-4 modified successfully
- [ ] code-8 modified successfully
- [ ] if-1 modified successfully
- [ ] All backups created (5 backups for Phase 4)
- [ ] All exports created after changes
- [ ] V8_CHANGELOG.md updated with Phase 4 completion

---

## Final Validation

### Workflow Structure Check

**Expected Node Count:** 23 nodes (18 original + 5 new)

**New Nodes:**
1. http-openai-2 (Tier 2 GPT-4 API call)
2. code-tier2-parse (Parse Tier 2 result)
3. code-action-mapper (Determine routing)
4. drive-rename (Rename with confidence)
5. (Note: Spec says 5 new but only 4 listed - verify with spec)

**Modified Nodes:**
1. code-1 (Tier 1 prompt)
2. code-2 (Tier 1 parse + Tier 2 prompt builder)
3. code-4 (Extended folder mapping)
4. code-8 (Conditional tracker update)
5. if-1 (Skip tracker routing)

**Unchanged Nodes:** 13 nodes remain unchanged

### Connection Validation

**Expected Flow:**
```
trigger-1 → code-1 → http-openai-1 → code-2 → http-openai-2 → code-tier2-parse → code-action-mapper → drive-rename → sheets-1 → code-3 → if-1
                                                                                                                                                        ├─ [CORE] code-8 → sheets-2 → sheets-3 → code-4 → drive-1 → code-5
                                                                                                                                                        ├─ [SECONDARY] → sheets-3 → code-4 → drive-1 → code-5
                                                                                                                                                        └─ [Error] sheets-4 → code-6 → drive-2 → code-7 → gmail-1
```

**Validation Checklist:**
- [ ] All 23 nodes present
- [ ] Tier 1 → Tier 2 → Action Mapper flow correct
- [ ] drive-rename positioned correctly
- [ ] CORE path includes tracker update
- [ ] SECONDARY path skips tracker update
- [ ] Error path unchanged
- [ ] No orphaned nodes
- [ ] No missing connections

### Functional Validation

**Test Scenarios:**

**Test 1: CORE Document (e.g., Exposé)**
- [ ] Tier 1 classifies as OBJEKTUNTERLAGEN
- [ ] Tier 2 classifies as 01_Projektbeschreibung
- [ ] isCoreType = true
- [ ] actionType = CORE
- [ ] File renamed with confidence score
- [ ] Tracker updated with ✓
- [ ] File moved to 01_Expose folder

**Test 2: SECONDARY Document (e.g., Kaufvertrag)**
- [ ] Tier 1 classifies as OBJEKTUNTERLAGEN
- [ ] Tier 2 classifies as 02_Kaufvertrag
- [ ] isCoreType = false
- [ ] actionType = SECONDARY
- [ ] File renamed with confidence score
- [ ] Tracker NOT updated (skipped)
- [ ] File moved to _Holding_Property folder

**Test 3: LOW_CONFIDENCE Document**
- [ ] Tier 1 confidence < 60% OR Tier 2 confidence < 70%
- [ ] actionType = LOW_CONFIDENCE
- [ ] File renamed as REVIEW_unknown_client_XXpct
- [ ] Tracker NOT updated (skipped)
- [ ] File moved to 38_Unknowns folder
- [ ] Email notification sent

### n8n Workflow Validation

Use n8n built-in validation:

```bash
# If using n8n MCP tools:
mcp__n8n-mcp__n8n_validate_workflow({
  workflowId: "okg8wTqLtPUwjQ18"
})

# If using n8n UI:
# Open workflow → Click "Validate" button → Check for errors
```

**Expected Result:** No validation errors

### Autofix (if needed)

If validation errors occur:

```bash
# If using n8n MCP tools:
mcp__n8n-mcp__n8n_autofix_workflow({
  workflowId: "okg8wTqLtPUwjQ18"
})

# Review autofix changes before accepting
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] All modifications complete
- [ ] All validations passed
- [ ] All backups created and verified
- [ ] V8_CHANGELOG.md fully updated
- [ ] No errors in n8n validation

### Deployment
- [ ] Deactivate V7 workflow (if running separately)
- [ ] Activate V8 workflow
- [ ] Monitor first execution
- [ ] Verify all 3 paths work (CORE/SECONDARY/LOW_CONFIDENCE)

### Post-Deployment
- [ ] First real execution successful
- [ ] Logs reviewed for errors
- [ ] File renaming works correctly
- [ ] Folder routing works correctly
- [ ] Tracker updates work for CORE types
- [ ] Email notifications work for LOW_CONFIDENCE

### Rollback Plan
If issues occur:
1. Deactivate V8 workflow immediately
2. Restore from backup: `.backups/chunk_2.5_v8.0_BEFORE_PHASE2_20260112.json`
3. Reactivate V7 workflow (or restore from `.archive/v7_phase_1/`)
4. Document issue in V8_CHANGELOG.md
5. Debug and fix before re-deployment

---

## Testing Recommendations

After V8 deployment, use **test-runner-agent** to:
1. Test all 38 document types
2. Validate Tier 1 accuracy (target >90%)
3. Validate Tier 2 accuracy (target >85%)
4. Test confidence thresholds (60% Tier 1, 70% Tier 2)
5. Verify CORE/SECONDARY routing
6. Verify holding folder placement
7. Verify filename confidence formatting

---

## Summary

**V8 Implementation Complete**

**Total Changes:**
- 2 nodes modified in Phase 2
- 2 nodes added in Phase 3
- 3 nodes added + 3 nodes modified in Phase 4
- **Total:** 5 nodes added, 5 nodes modified

**Final State:**
- Workflow: Chunk 2.5 (ID: okg8wTqLtPUwjQ18)
- Nodes: 18 → 23 (+5 nodes)
- Classification: Single-pass → 2-tier hierarchical
- Document types: 5 → 38 (+33 types)
- Folders: 5 specific + 1 unknown → 4 CORE specific + 4 holding + 1 unknown
- Filename format: Added confidence scores

**Key Features:**
- ✅ 2-tier classification (4 categories → 38 types)
- ✅ Confidence thresholds (60% Tier 1, 70% Tier 2)
- ✅ CORE/SECONDARY/LOW_CONFIDENCE routing
- ✅ Filename confidence scores
- ✅ Conditional tracker updates (CORE only)
- ✅ Holding folders for SECONDARY types
- ✅ Email notifications for LOW_CONFIDENCE

**Ready for:** test-runner-agent automated testing

---

**Document Version:** 1.0
**Last Updated:** 2026-01-12 22:30 CET
**Created By:** solution-builder-agent (a7e6ae4)
