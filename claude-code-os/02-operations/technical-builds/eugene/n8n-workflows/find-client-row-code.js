const trackerData = $('Lookup Client in Client_Tracker').all();
const mainData = $('Parse Classification Result').first().json;

const clientNormalized = mainData.clientNormalized || '';
const documentType = mainData.documentType || '';
const confidence = mainData.combinedConfidence || mainData.tier2Confidence || 0;

// Check if confidence is too low
if (confidence < 70) {
  return {
    json: {
      ...mainData,
      chunk2_5_status: 'error_unclear_type',
      errorMessage: `Low confidence (${confidence}%) - document type unclear`
    }
  };
}

// Check if any data was returned
if (!trackerData || trackerData.length === 0) {
  return {
    json: {
      ...mainData,
      chunk2_5_status: 'error_client_not_found',
      errorMessage: 'No data returned from Client_Tracker lookup'
    }
  };
}

// Google Sheets lookup returns matching rows (no header in result)
// If we got results, the first row is the client data
const clientRow = trackerData[0];

// Validate that we have a Client_Name field
if (!clientRow.json.Client_Name) {
  return {
    json: {
      ...mainData,
      chunk2_5_status: 'error_client_not_found',
      errorMessage: 'Client_Tracker returned invalid data (no Client_Name field)'
    }
  };
}

// Verify this is the correct client by comparing normalized names
const sheetClientName = clientRow.json.Client_Name || '';
const normalizedSheetName = sheetClientName
  .toLowerCase()
  .trim()
  .replace(/ä/g, 'ae')
  .replace(/ö/g, 'oe')
  .replace(/ü/g, 'ue')
  .replace(/ß/g, 'ss')
  .replace(/\s*(gmbh|ag|kg|e\.v\.|mbh|co\.|&\s*co\.?)\s*/gi, '')
  .replace(/[^a-z0-9]/g, '_')
  .replace(/_+/g, '_')
  .replace(/^_|_$/g, '');

if (normalizedSheetName !== clientNormalized) {
  return {
    json: {
      ...mainData,
      chunk2_5_status: 'error_client_not_found',
      errorMessage: `Client name mismatch: expected "${clientNormalized}", got "${normalizedSheetName}"`
    }
  };
}

// Client found and validated - prepare for update
return {
  json: {
    ...mainData,
    trackerRowIndex: 0, // First row in lookup result
    trackerClientName: clientRow.json.Client_Name,
    chunk2_5_status: 'success'
  }
};
