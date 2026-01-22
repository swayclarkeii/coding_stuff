const items = $input.all();
const outputItems = [];

for (const item of items) {
  const tier2Prompt = item.json.tier2Prompt;
  const imageData = $('Convert PDF to Base64').first().json.imageData;

  if (!imageData || !imageData.data) {
    throw new Error('No image data found for Tier 2 classification');
  }

  const requestBody = {
    model: 'claude-sonnet-4-20250514',
    max_tokens: 300,
    messages: [
      {
        role: 'user',
        content: [
          {
            type: 'document',
            source: {
              type: 'base64',
              media_type: imageData.media_type,
              data: imageData.data
            }
          },
          {
            type: 'text',
            text: tier2Prompt
          }
        ]
      }
    ]
  };

  outputItems.push({
    json: {
      ...item.json,
      claudeTier2RequestBody: requestBody
    }
  });
}

return outputItems;
