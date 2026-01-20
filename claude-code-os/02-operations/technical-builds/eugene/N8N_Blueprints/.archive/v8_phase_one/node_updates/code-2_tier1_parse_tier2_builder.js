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
