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
