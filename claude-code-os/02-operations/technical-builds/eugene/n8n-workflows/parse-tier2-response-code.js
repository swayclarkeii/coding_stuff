const items = $input.all();
const outputItems = [];

for (const item of items) {
  const response = item.json;

  if (!response.content || !response.content[0] || !response.content[0].text) {
    throw new Error('Invalid Claude API Tier 2 response structure');
  }

  let textContent = response.content[0].text.trim();

  // Strip markdown code fences if present
  if (textContent.startsWith('```json')) {
    textContent = textContent
      .replace(/^```json\s*\n/, '')
      .replace(/\n```\s*$/, '');
  } else if (textContent.startsWith('```')) {
    textContent = textContent
      .replace(/^```\s*\n/, '')
      .replace(/\n```\s*$/, '');
  }

  const parsedResult = JSON.parse(textContent);

  // Get metadata from previous node
  const previousData = $('Parse Classification Result').first().json;

  outputItems.push({
    json: {
      ...previousData,
      documentType: parsedResult.documentType,
      tier2Confidence: parsedResult.tier2Confidence,
      germanName: parsedResult.germanName,
      englishName: parsedResult.englishName,
      isCoreType: parsedResult.isCoreType,
      tier2Reasoning: parsedResult.reasoning || ''
    }
  });
}

return outputItems;
