// Get Destination Folder ID - V8 Extended Mapping

const data = $input.first().json;
const actionType = data.actionType;
const documentType = data.documentType;
const tier1Category = data.tier1Category;

// Get folder IDs from AMA_Folder_IDs sheet
const folderData = data; // Folder IDs are already in the data from sheets-3

let destinationFolderId;
let destinationFolderName;

// === LOW_CONFIDENCE → 38_Unknowns ===
if (actionType === 'LOW_CONFIDENCE') {
  destinationFolderId = folderData.FOLDER_38_Unknowns;
  destinationFolderName = '38_Unknowns';
}

// === CORE TYPES → Specific Folders ===
else if (actionType === 'CORE') {
  const coreMapping = {
    '01_Projektbeschreibung': { id: 'FOLDER_01_Expose', name: '01_Expose' },
    '03_Grundbuchauszug': { id: 'FOLDER_02_Grundbuch', name: '02_Grundbuch' },
    '10_Bautraegerkalkulation_DIN276': { id: 'FOLDER_03_Calculation', name: '03_Calculation' },
    '36_Exit_Strategie': { id: 'FOLDER_04_Exit_Strategy', name: '04_Exit_Strategy' }
  };

  const mapping = coreMapping[documentType];
  if (mapping) {
    destinationFolderId = folderData[mapping.id];
    destinationFolderName = mapping.name;
  } else {
    // Fallback: should not happen if isCoreType is correct
    destinationFolderId = folderData.FOLDER_38_Unknowns;
    destinationFolderName = '38_Unknowns (CORE mapping error)';
  }
}

// === SECONDARY TYPES → Holding Folders ===
else if (actionType === 'SECONDARY') {
  // Map based on Tier 1 category to corresponding holding folder
  const holdingMapping = {
    'OBJEKTUNTERLAGEN': { id: 'FOLDER_HOLDING_PROPERTY', name: '_Holding_Property' },
    'WIRTSCHAFTLICHE_UNTERLAGEN': { id: 'FOLDER_HOLDING_FINANCIAL', name: '_Holding_Financial' },
    'RECHTLICHE_UNTERLAGEN': { id: 'FOLDER_HOLDING_LEGAL', name: '_Holding_Legal' },
    'SONSTIGES': { id: 'FOLDER_HOLDING_MISC', name: '_Holding_Misc' }
  };

  const mapping = holdingMapping[tier1Category];
  if (mapping) {
    destinationFolderId = folderData[mapping.id];
    destinationFolderName = mapping.name;
  } else {
    // Fallback
    destinationFolderId = folderData.FOLDER_38_Unknowns;
    destinationFolderName = '38_Unknowns (SECONDARY mapping error)';
  }
}

// Unknown action type fallback
else {
  destinationFolderId = folderData.FOLDER_38_Unknowns;
  destinationFolderName = '38_Unknowns (Unknown action type)';
}

return {
  json: {
    destinationFolderId,
    destinationFolderName,
    ...data
  }
};
