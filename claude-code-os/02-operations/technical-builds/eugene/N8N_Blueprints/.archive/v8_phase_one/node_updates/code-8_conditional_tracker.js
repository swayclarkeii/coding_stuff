// Prepare Tracker Update Data - V8 Conditional (CORE types only)

const data = $input.first().json;

// CONDITIONAL: Only prepare tracker data if trackerUpdate === true
if (data.trackerUpdate !== true) {
  // SECONDARY or LOW_CONFIDENCE: Skip tracker update, pass through to folder move
  return {
    json: {
      skipTrackerUpdate: true,
      ...data
    }
  };
}

// CORE types: Prepare tracker update data
const documentType = data.documentType;

// Map document type to tracker column
const trackerColumnMapping = {
  '01_Projektbeschreibung': 'Status_Expose',
  '03_Grundbuchauszug': 'Status_Grundbuch',
  '10_Bautraegerkalkulation_DIN276': 'Status_Calculation',
  '36_Exit_Strategie': 'Status_Exit_Strategy'
};

const trackerColumn = trackerColumnMapping[documentType];

if (!trackerColumn) {
  // Should not happen if CORE mapping is correct
  return {
    json: {
      error: 'Unknown CORE document type for tracker mapping',
      skipTrackerUpdate: true,
      ...data
    }
  };
}

// Prepare update data for Client_Tracker
const updateData = {
  [trackerColumn]: '✓'
};

return {
  json: {
    trackerColumn,
    trackerValue: '✓',
    updateData,
    skipTrackerUpdate: false,
    ...data
  }
};
