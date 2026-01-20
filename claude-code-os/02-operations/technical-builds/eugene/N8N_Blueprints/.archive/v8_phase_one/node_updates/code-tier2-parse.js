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
