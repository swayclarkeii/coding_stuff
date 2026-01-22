// Parse Tier 1 Classification Result + Build Dynamic Tier 2 Prompt

const response = $input.first().json;

// === PRESERVE CRITICAL FILE METADATA FROM EARLIER NODE ===
// Get ALL file metadata fields from "Build AI Classification Prompt" node (earlier in chain)
// This node already extracted these fields with proper fallback logic
const fileId = $node["Build AI Classification Prompt"].json.fileId;
const fileName = $node["Build AI Classification Prompt"].json.fileName;
const fileUrl = $node["Build AI Classification Prompt"].json.fileUrl;
const clientEmail = $node["Build AI Classification Prompt"].json.clientEmail;

// Extract Tier 1 classification from Claude Tier 1 response
const tier1Result = $('Parse Claude Tier 1 Response').first().json;

if (!tier1Result || !tier1Result.tier1Category) {
  // If parsing failed, return error for LOW_CONFIDENCE routing
  return {
    json: {
      error: 'Failed to parse Tier 1 classification',
      tier1Category: 'UNKNOWN',
      tier1Confidence: 0,
      tier2Prompt: 'ERROR: Failed to parse Tier 1 classification',
      fileId,
      fileName,
      fileUrl,
      clientEmail,
      ...($input.first().json)
    }
  };
}

const { tier1Category, tier1Confidence, tier1Reasoning } = tier1Result;
const reasoning = tier1Reasoning || '';

// Build category-specific Tier 2 prompt
let tier2Prompt = '';

// [Rest of the tier2Prompt building logic - same as before]
if (tier1Category === 'OBJEKTUNTERLAGEN') {
  tier2Prompt = `You are a German real estate document classifier for AMA Capital.\n\nTIER 1 RESULT: This document was classified as OBJEKTUNTERLAGEN (Property/Object Documents) with ${tier1Confidence}% confidence.\n\nTASK: Now classify into the SPECIFIC document type from the list below.\n\nFILENAME: ${fileName}\nCLIENT: ${clientEmail}\n\nSPECIFIC TYPES (choose ONE):\n\n01_Projektbeschreibung (Exposé/Project Description) ⭐ CORE\n   Keywords: Projekt, Beschreibung, Expose, Overview, Proposal\n   Description: Project overview, property description, investment proposal\n\n02_Kaufvertrag (Purchase Agreement)\n   Keywords: Kauf, Vertrag, Purchase, Agreement\n   Description: Property purchase contract\n\n03_Grundbuchauszug (Land Register Extract) ⭐ CORE\n   Keywords: Grundbuch, Land, Register, Auszug\n   Description: Official land registry extract\n\n04_Eintragungsbewilligungen (Entry Permits)\n   Keywords: Eintragung, Bewilligung, Entry, Permit\n   Description: Permits for land register entries\n\n05_Bodenrichtwert (Land Value)\n   Keywords: Boden, Richtwert, Land, Value\n   Description: Official land value assessment\n\n06_Baulastenverzeichnis (Building Encumbrance Register)\n   Keywords: Baulast, Verzeichnis, Encumbrance\n   Description: Register of building encumbrances\n\n07_Altlastenkataster (Contaminated Sites Register)\n   Keywords: Altlast, Kataster, Contaminated\n   Description: Register of contaminated sites\n\n08_Baugrundgutachten (Soil Survey)\n   Keywords: Baugrund, Gutachten, Soil, Survey\n   Description: Soil conditions assessment\n\n09_Lageplan (Site Plan)\n   Keywords: Lage, Plan, Site\n   Description: Site location plan\n\n10_Bautraegerkalkulation_DIN276 (Developer Calculation) ⭐ CORE\n   Keywords: Bautraeger, Kalkulation, DIN276, Calculation\n   Description: Developer cost calculation per DIN276 standard\n\n15_Flaechenberechnung_DIN277 (Area Calculation DIN277)\n   Keywords: Flaeche, Berechnung, DIN277, Area\n   Description: Area calculation per DIN277 standard\n\n16_GU_Werkvertraege (General Contractor Agreements)\n   Keywords: GU, Werkvertrag, Contractor, Agreement\n   Description: General contractor work agreements\n\n17_Bauzeichnungen (Construction Drawings)\n   Keywords: Bau, Zeichnung, Construction, Drawing\n   Description: Construction and architectural drawings\n\n18_Baugenehmigung (Building Permit)\n   Keywords: Bau, Genehmigung, Building, Permit\n   Description: Official building permit\n\nINSTRUCTIONS:\n1. Analyze filename for specific German keywords\n2. Choose the MOST SPECIFIC type that matches\n3. Provide confidence score (0-100)\n4. Explain your reasoning\n\nRESPONSE FORMAT (JSON only):\n{\n  \"documentType\": \"01_Projektbeschreibung\",\n  \"tier2Confidence\": 88,\n  \"germanName\": \"Projektbeschreibung\",\n  \"englishName\": \"Exposé/Project Description\",\n  \"isCoreType\": true,\n  \"reasoning\": \"Brief explanation\"\n}\n\nSTRICT RULES:\n- documentType must EXACTLY match one of the codes above (e.g., \"01_Projektbeschreibung\")\n- isCoreType: true for ⭐ CORE types, false for others\n- Valid JSON only, no markdown`;
} else if (tier1Category === 'WIRTSCHAFTLICHE_UNTERLAGEN') {
  tier2Prompt = `You are a German real estate document classifier for AMA Capital.\n\nTIER 1 RESULT: This document was classified as WIRTSCHAFTLICHE_UNTERLAGEN (Financial/Economic Documents) with ${tier1Confidence}% confidence.\n\nTASK: Now classify into the SPECIFIC document type from the list below.\n\nFILENAME: ${fileName}\nCLIENT: ${clientEmail}\n\nSPECIFIC TYPES (choose ONE):\n\n11_Verkaufspreise (Sales Prices)\n   Keywords: Verkauf, Preis, Sales, Price\n   Description: Sales price lists and calculations\n\n12_Bauzeitenplan_Liquiditaet (Construction Schedule & Liquidity)\n   Keywords: Bauzeit, Plan, Liquiditaet, Schedule\n   Description: Construction timeline and liquidity planning\n\n13_Vertriebsweg (Distribution Channel)\n   Keywords: Vertrieb, Weg, Distribution, Channel\n   Description: Sales and distribution strategy\n\n14_Bau_Ausstattungsbeschreibung (Construction & Equipment Description)\n   Keywords: Bau, Ausstattung, Beschreibung, Equipment\n   Description: Construction specifications and equipment details\n\n19_Teilungserklaerung (Declaration of Division)\n   Keywords: Teilung, Erklaerung, Division, Declaration\n   Description: Property division declaration\n\n20_Versicherungen (Insurance)\n   Keywords: Versicherung, Insurance\n   Description: Insurance policies and documentation\n\n21_Muster_Verkaufsvertrag (Sample Sales Contract)\n   Keywords: Muster, Verkauf, Vertrag, Sample, Sales\n   Description: Template sales contract\n\n23_Umsatzsteuervoranmeldung (VAT Advance Return)\n   Keywords: Umsatz, Steuer, Voranmeldung, VAT\n   Description: VAT advance return filings\n\n24_BWA (Business Evaluation)\n   Keywords: BWA, Business, Evaluation\n   Description: Business evaluation report\n\n25_Jahresabschluss (Annual Financial Statement)\n   Keywords: Jahres, Abschluss, Annual, Financial\n   Description: Annual financial statement\n\n26_Finanzierungsbestaetigung (Financing Confirmation)\n   Keywords: Finanzierung, Bestaetigung, Financing, Confirmation\n   Description: Financing approval or confirmation\n\n27_Darlehensvertrag (Loan Agreement)\n   Keywords: Darlehen, Vertrag, Loan, Agreement\n   Description: Loan contract\n\nINSTRUCTIONS:\n1. Analyze filename for specific German keywords\n2. Choose the MOST SPECIFIC type that matches\n3. Provide confidence score (0-100)\n4. Explain your reasoning\n\nRESPONSE FORMAT (JSON only):\n{\n  \"documentType\": \"11_Verkaufspreise\",\n  \"tier2Confidence\": 92,\n  \"germanName\": \"Verkaufspreise\",\n  \"englishName\": \"Sales Prices\",\n  \"isCoreType\": false,\n  \"reasoning\": \"Brief explanation\"\n}\n\nSTRICT RULES:\n- documentType must EXACTLY match one of the codes above\n- isCoreType: false for all WIRTSCHAFTLICHE types (none are CORE)\n- Valid JSON only, no markdown`;
} else if (tier1Category === 'RECHTLICHE_UNTERLAGEN') {
  tier2Prompt = `You are a German real estate document classifier for AMA Capital.\n\nTIER 1 RESULT: This document was classified as RECHTLICHE_UNTERLAGEN (Legal/Compliance Documents) with ${tier1Confidence}% confidence.\n\nTASK: Now classify into the SPECIFIC document type from the list below.\n\nFILENAME: ${fileName}\nCLIENT: ${clientEmail}\n\nSPECIFIC TYPES (choose ONE):\n\n28_Gesellschaftsvertrag (Partnership Agreement)\n   Keywords: Gesellschaft, Vertrag, Partnership, Agreement\n   Description: Company partnership or shareholder agreement\n\n29_Handelsregisterauszug (Commercial Register Extract)\n   Keywords: Handelsregister, Auszug, Commercial, Register\n   Description: Commercial register extract\n\n30_Gewerbeanmeldung (Business Registration)\n   Keywords: Gewerbe, Anmeldung, Business, Registration\n   Description: Business registration documentation\n\n31_Steuer_ID (Tax ID)\n   Keywords: Steuer, ID, Tax\n   Description: Tax identification number\n\n32_Freistellungsbescheinigung (Exemption Certificate)\n   Keywords: Freistellung, Bescheinigung, Exemption, Certificate\n   Description: Tax exemption certificate\n\n33_Vollmachten (Powers of Attorney)\n   Keywords: Vollmacht, Power, Attorney\n   Description: Power of attorney documents\n\nINSTRUCTIONS:\n1. Analyze filename for specific German keywords\n2. Choose the MOST SPECIFIC type that matches\n3. Provide confidence score (0-100)\n4. Explain your reasoning\n\nRESPONSE FORMAT (JSON only):\n{\n  \"documentType\": \"28_Gesellschaftsvertrag\",\n  \"tier2Confidence\": 85,\n  \"germanName\": \"Gesellschaftsvertrag\",\n  \"englishName\": \"Partnership Agreement\",\n  \"isCoreType\": false,\n  \"reasoning\": \"Brief explanation\"\n}\n\nSTRICT RULES:\n- documentType must EXACTLY match one of the codes above\n- isCoreType: false for all RECHTLICHE types (none are CORE)\n- Valid JSON only, no markdown`;
} else if (tier1Category === 'SONSTIGES') {
  tier2Prompt = `You are a German real estate document classifier for AMA Capital.\n\nTIER 1 RESULT: This document was classified as SONSTIGES (Miscellaneous) with ${tier1Confidence}% confidence.\n\nTASK: Now classify into the SPECIFIC document type from the list below.\n\nFILENAME: ${fileName}\nCLIENT: ${clientEmail}\n\nSPECIFIC TYPES (choose ONE):\n\n22_Gutachterauftrag (Expert Assignment)\n   Keywords: Gutachter, Auftrag, Expert, Assignment\n   Description: Expert assessment assignment\n\n34_Korrespondenz (Correspondence)\n   Keywords: Korrespondenz, Email, Brief, Letter, Correspondence\n   Description: Email correspondence and letters\n\n35_Sonstiges_Allgemein (General Miscellaneous)\n   Keywords: Sonstiges, Misc, General\n   Description: General miscellaneous documents\n\n36_Exit_Strategie (Exit Strategy) ⭐ CORE\n   Keywords: Exit, Strategie, Strategy\n   Description: Investment exit strategy\n\n37_Others (Others)\n   Keywords: Other, Andere\n   Description: Other unclassified documents\n\n38_Unknowns (Unknowns)\n   Keywords: Unknown, Unbekannt\n   Description: Unknown document type\n\nINSTRUCTIONS:\n1. Analyze filename for specific German keywords\n2. Choose the MOST SPECIFIC type that matches\n3. Provide confidence score (0-100)\n4. Explain your reasoning\n5. Use 38_Unknowns ONLY if truly unclear\n\nRESPONSE FORMAT (JSON only):\n{\n  \"documentType\": \"36_Exit_Strategie\",\n  \"tier2Confidence\": 95,\n  \"germanName\": \"Exit Strategie\",\n  \"englishName\": \"Exit Strategy\",\n  \"isCoreType\": true,\n  \"reasoning\": \"Brief explanation\"\n}\n\nSTRICT RULES:\n- documentType must EXACTLY match one of the codes above\n- isCoreType: true ONLY for 36_Exit_Strategie\n- Valid JSON only, no markdown`;
} else {
  tier2Prompt = `You are a German real estate document classifier for AMA Capital.\n\nERROR: Unknown category \"${tier1Category}\". Please classify as SONSTIGES > 38_Unknowns.\n\nFILENAME: ${fileName}\nCLIENT: ${clientEmail}\n\nRESPONSE FORMAT (JSON only):\n{\n  \"documentType\": \"38_Unknowns\",\n  \"tier2Confidence\": 0,\n  \"germanName\": \"Unknowns\",\n  \"englishName\": \"Unknown\",\n  \"isCoreType\": false,\n  \"reasoning\": \"Unknown Tier 1 category: ${tier1Category}\"\n}`;
}

if (tier1Confidence < 60) {
  return {
    json: {
      tier1Category,
      tier1Confidence,
      tier1Reasoning: reasoning,
      tier2Prompt,
      fileId,
      fileName,
      fileUrl,
      clientEmail,
      lowConfidence: true,
      confidenceFailureStage: 'tier1',
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
    fileId,
    fileName,
    fileUrl,
    clientEmail,
    ...($input.first().json)
  }
};
