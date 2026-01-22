// Parse Tier 2 Classification Result from Claude Vision

// Get Claude Tier 2 parsed response
const tier2Result = $('Parse Claude Tier 2 Response').first().json;

if (!tier2Result || !tier2Result.documentType) {
  // Parsing failed - route to LOW_CONFIDENCE
  return [{
    json: {
      error: 'Failed to parse Tier 2 classification',
      lowConfidence: true,
      confidenceFailureStage: 'tier2_parse_error',
      ...tier2Result
    }
  }];
}

const {
  documentType,
  tier2Confidence,
  germanName,
  englishName,
  isCoreType,
  tier2Reasoning,
  fileId,
  fileName,
  fileUrl,
  clientEmail,
  tier1Category,
  tier1Confidence,
  tier1Reasoning
} = tier2Result;

// THRESHOLD CHECK: Tier 2 confidence must be >= 70%
if (tier2Confidence < 70) {
  return [{
    json: {
      documentType,
      tier2Confidence,
      lowConfidence: true,
      confidenceFailureStage: 'tier2',
      fileId,
      fileName,
      fileUrl,
      clientEmail,
      tier1Category,
      tier1Confidence,
      tier1Reasoning
    }
  }];
}

// Calculate combined confidence
const combinedConfidence = Math.round((tier1Confidence + tier2Confidence) / 2);

return [{
  json: {
    fileId,
    fileName,
    fileUrl,
    clientEmail,
    tier1Category,
    tier1Confidence,
    tier1Reasoning,
    documentType,
    tier2Confidence,
    combinedConfidence,
    germanName,
    englishName,
    isCoreType,
    tier2Reasoning
  }
}];
