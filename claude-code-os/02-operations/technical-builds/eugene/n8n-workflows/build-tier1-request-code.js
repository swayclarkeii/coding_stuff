const items = $input.all();
const outputItems = [];

for (const item of items) {
  const tier1Prompt = $('Build AI Classification Prompt').first().json.tier1Prompt;
  const imageData = item.json.imageData;

  if (!imageData || !imageData.data) {
    throw new Error('No image data found in item');
  }

  const requestBody = {
    model: 'claude-sonnet-4-20250514',
    max_tokens: 200,
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
            text: tier1Prompt
          }
        ]
      }
    ]
  };

  outputItems.push({
    json: {
      ...item.json,
      claudeRequestBody: requestBody
    },
    binary: item.binary
  });
}

return outputItems;
