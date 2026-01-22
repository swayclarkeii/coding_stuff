// Action Mapper: Determine routing based on classification results

const data = $input.first().json;

// Check for low confidence flags
if (data.lowConfidence === true) {
  return [{
    json: {
      ...data,  // ← CRITICAL: Preserve ALL incoming fields (fileId, fileName, etc.)
      actionType: 'LOW_CONFIDENCE',
      destinationFolder: '38_Unknowns',
      trackerUpdate: false,
      sendNotification: true
    }
  }];
}

// Check if CORE type
if (data.isCoreType === true) {
  // CORE types: Specific folder + tracker update
  return [{
    json: {
      ...data,  // ← CRITICAL: Preserve ALL incoming fields (fileId, fileName, etc.)
      actionType: 'CORE',
      trackerUpdate: true,
      sendNotification: false
    }
  }];
}

// SECONDARY types: 37_Other folder + tracker update (so Eugene can see what they are)
return [{
  json: {
    ...data,  // ← CRITICAL: Preserve ALL incoming fields (fileId, fileName, etc.)
    actionType: 'SECONDARY',
    destinationFolder: '37_Other',
    trackerUpdate: true,
    sendNotification: false
  }
}];
