# Eugene Test Results Setup Instructions

## Test_Results Sheet Creation

**Spreadsheet ID**: `12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I`

### Manual Steps (One-time setup)

1. Open the spreadsheet in Google Sheets
2. Create a new sheet called **"Test_Results"**
3. Add the following headers in row 1 (columns A-L):

| Column | Header |
|--------|--------|
| A | Test_Date |
| B | File_Name |
| C | Client |
| D | Tier1_Category |
| E | Tier2_DocumentType |
| F | Confidence |
| G | Tracker_Column |
| H | Tracker_Updated |
| I | File_Moved |
| J | Final_Location |
| K | Status |
| L | Error_Message |

### What Gets Logged

Each test run will append a new row with:

- **Test_Date**: When the test ran (DD.MM.YYYY HH:mm format)
- **File_Name**: Name of the PDF file tested
- **Client**: Client normalized name (e.g., villa_martens)
- **Tier1_Category**: AI's Tier 1 classification
- **Tier2_DocumentType**: AI's Tier 2 classification (final document type)
- **Confidence**: AI confidence score (if available)
- **Tracker_Column**: Which column was updated in Client_Tracker
- **Tracker_Updated**: "yes" or "no" - whether tracker was updated
- **File_Moved**: "yes" or "no" - whether file was moved to final location
- **Final_Location**: Google Drive folder ID where file was moved
- **Status**: "success" or "error"
- **Error_Message**: Any error message if status is "error"

### Usage

After creating the sheet, the Quick Test Runner workflow will automatically log results after each test execution.

## Updates Made

### 1. Timestamp Format (Chunk 2.5)
- **Node**: "Build Google Sheets API Update Request"
- **Change**: Timestamp now formatted as **DD.MM.YYYY HH:mm** (German format)
- **Example**: `27.01.2026 08:02` instead of `2026-01-26T22:57:23.368Z`

### 2. Test Logging (Quick Test Runner)
- **New Nodes**:
  - "Prepare Log Data" - Formats test results for logging
  - "Append to Test_Results" - Writes to Test_Results sheet
- **Flow**: Show Test Results → Prepare Log Data → Append to Test_Results

### 3. Random File Selection (Quick Test Runner)
- **Node**: "Grab First File" renamed to "Pick Random File"
- **Change**: Now selects a **random file** from test folder instead of always first
- **Logic**: `Math.floor(Math.random() * files.length)`
- **Test Folder ID**: Updated to `1-jO4unjKgedFqVqtofR4QEM18xC09Fsk`

## Testing

1. Create the Test_Results sheet (one-time)
2. Upload test PDFs to folder `1-jO4unjKgedFqVqtofR4QEM18xC09Fsk`
3. Run Quick Test Runner workflow
4. Check Test_Results sheet for logged results
5. Run again - should pick a different random file each time
