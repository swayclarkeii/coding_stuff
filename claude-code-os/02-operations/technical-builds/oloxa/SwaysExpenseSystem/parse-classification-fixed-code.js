// Parse Anthropic response with robust JSON extraction
// Node: Parse Classification (id: parse-classification)
// Workflow: Expense System - W7v2 (id: qSuG0gwuJByd2hGJ)
// Updated: 2026-01-31 08:19 UTC

const response = $input.first().json;
const textContent = response.content[0].text;

let classification;

// Step 1: Try direct JSON.parse first (in case response is pure JSON)
try {
  classification = JSON.parse(textContent);
} catch (e1) {
  // Step 2: Try removing markdown code fences
  try {
    const jsonText2 = textContent.replace(/^```json\n?/, '').replace(/\n?```$/, '').trim();
    classification = JSON.parse(jsonText2);
  } catch (e2) {
    // Step 3: Extract JSON between code fences if present
    try {
      const codeBlockMatch = textContent.match(/```(?:json)?\n?([\s\S]*?)```/);
      if (codeBlockMatch && codeBlockMatch[1]) {
        const jsonText3 = codeBlockMatch[1].trim();
        classification = JSON.parse(jsonText3);
      } else {
        throw new Error('No code block found');
      }
    } catch (e3) {
      // Step 4: Extract JSON by finding first { and last }
      const jsonStart = textContent.indexOf('{');
      const jsonEnd = textContent.lastIndexOf('}');
      if (jsonStart >= 0 && jsonEnd > jsonStart) {
        const jsonText4 = textContent.substring(jsonStart, jsonEnd + 1);
        classification = JSON.parse(jsonText4);
      } else {
        throw new Error('Failed to extract JSON: could not find opening brace');
      }
    }
  }
}

if (!classification.fileType) {
  throw new Error('Missing fileType in classification result');
}

const metadata = $('Build Classification Request').first().json;
const binaryData = $('Build Classification Request').first().binary;

return {
  json: {
    fileType: classification.fileType || 'unknown',
    vendor: classification.vendor || 'Unknown',
    date: classification.date || '',
    amount: classification.amount || '0',
    currency: classification.currency || 'USD',
    description: classification.description || '',
    confidence: classification.confidence || 0,
    fileName: metadata.fileName,
    fileId: metadata.fileId,
    processedDate: metadata.processedDate
  },
  binary: binaryData
};
