const items = $input.all();
const outputItems = [];

for (const item of items) {
  const response = item.json;

  if (!response.content || !response.content[0] || !response.content[0].text) {
    throw new Error('Invalid Claude API response structure');
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

  outputItems.push({
    json: {
      tier1Category: parsedResult.tier1Category,
      tier1Confidence: parsedResult.tier1Confidence,
      tier1Reasoning: parsedResult.reasoning || ''
    }
  });
}

return outputItems;
