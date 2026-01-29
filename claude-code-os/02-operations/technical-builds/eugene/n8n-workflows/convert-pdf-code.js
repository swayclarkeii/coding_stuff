const item = $input.first();
const binaryKey = Object.keys(item.binary)[0];
const buffer = await this.helpers.getBinaryDataBuffer(0, binaryKey);
const base64Content = buffer.toString('base64');
const mimeType = item.json.mimeType || 'application/pdf';

return {
  json: {
    ...item.json,
    imageData: {
      type: 'base64',
      media_type: mimeType,
      data: base64Content
    }
  },
  binary: item.binary
};
