// Action Mapper: Determine routing based on classification results

const data = $input.first().json;

// Check for low confidence flags
if (data.lowConfidence === true) {
  return {
    json: {
      actionType: 'LOW_CONFIDENCE',
      destinationFolder: '38_Unknowns',
      trackerUpdate: false,
      sendNotification: true,
      ...data
    }
  };
}

// Check if CORE type
if (data.isCoreType === true) {
  // CORE types: Specific folder + tracker update
  return {
    json: {
      actionType: 'CORE',
      trackerUpdate: true,
      sendNotification: false,
      ...data
    }
  };
}

// SECONDARY types: Holding folder + no tracker
return {
  json: {
    actionType: 'SECONDARY',
    trackerUpdate: false,
    sendNotification: false,
    ...data
  }
};
