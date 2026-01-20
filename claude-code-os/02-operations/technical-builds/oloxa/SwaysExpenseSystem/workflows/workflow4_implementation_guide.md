# Workflow 4: File Organization & Sorting - Implementation Guide

**Version**: v1.2.4
**Date**: January 4, 2026
**Status**: Blueprint Ready for Import
**Workflow Type**: Manual Trigger

---

## Overview

**Purpose**: Organize receipts from the Receipt Pool into monthly vendor folders based on metadata in the Receipts sheet.

**Trigger**: Manual execution (no scheduling) - run when Sway wants to organize accumulated receipts.

**Processing Model**:
- Loads all files from Receipt Pool
- Matches files with database records
- Determines target folder structure
- Generates organization report (v1.2.4 does NOT move files yet)

---

## Workflow Architecture

### Node Flow

```
Manual Trigger
    ↓
    ├─→ Load Receipt Files (Google Drive: List files in Receipt Pool)
    │
    └─→ Read Receipt Metadata (Google Sheets: Load Receipts sheet)
         ↓
    Merge Data Streams (Combine both inputs)
         ↓
    Match Files to Metadata (Code: Join by FileID)
         ↓
    Determine Target Folder (Code: Calculate destination path)
         ↓
    Generate Summary Report (Code: Output organization plan)
```

### Design Decisions

**Why no actual file moves in v1.2.4?**
- Folder ID lookup requires dynamic Google Drive search or hardcoded mapping
- Hardcoding 144+ folder IDs (6 vendors × 12 months × 2 years) is error-prone
- v1.2.4 focuses on validation: "Can we match files to folders correctly?"
- v1.2.5 will implement actual moves after validating the logic

**Why not use splitInBatches?**
- Initial design had splitInBatches for sequential processing
- Not needed for v1.2.4 since we're not moving files yet
- Code nodes process all items efficiently without looping

---

## Node Details

### 1. Manual Trigger
- **Type**: Manual Trigger
- **Purpose**: User-initiated execution
- **Configuration**: None required

### 2. Load Receipt Files
- **Type**: Google Drive (v3)
- **Operation**: List Files
- **Folder ID**: `12SVQzuWtKva48LvdGbszg3UcKl7iy-1x` (_Receipt-Pool/)
- **Credentials**: Google OAuth2 API (ID: a4m50EefR3DJoU0R)
- **Output**: Array of file objects with `id`, `name`, `mimeType`

### 3. Read Receipt Metadata
- **Type**: Google Sheets (v4.5)
- **Operation**: Read
- **Document ID**: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM` (Expense-Database)
- **Sheet**: Receipts
- **Credentials**: Google OAuth2 API (ID: a4m50EefR3DJoU0R)
- **Output**: Array of receipt records with all database fields

### 4. Merge Data Streams
- **Type**: Merge (v3)
- **Mode**: Combine
- **Combination**: Merge by Position
- **Purpose**: Combine Drive files and Sheet records into single data stream

### 5. Match Files to Metadata
- **Type**: Code (v2)
- **Mode**: Run Once for All Items
- **Logic**:
  1. Separate Drive files (have `mimeType`) from Sheet records (have `FileID`)
  2. Create lookup map: `FileID → metadata record`
  3. Match each file to its metadata
  4. Filter out files missing `Date` or `Vendor`
  5. Log errors to console
- **Output**: Array of matched receipt objects

**Output Schema**:
```javascript
{
  fileId: "1abc...",
  fileName: "Receipt_OpenAI_2025-01.pdf",
  vendor: "OpenAI",
  date: "2025-01-15",
  receiptId: "RCPT-OpenAI-1704672000",
  currentPath: "_Receipt-Pool"
}
```

### 6. Determine Target Folder
- **Type**: Code (v2)
- **Mode**: Run Once for Each Item
- **Logic**:
  1. Parse date: `YYYY-MM-DD` → `year`, `month`
  2. Map month number to folder name: `01` → `01-January`
  3. Normalize vendor name to folder name:
     - `OpenAI` → `OpenAI`
     - `Google Cloud` → `Google-Cloud`
     - `Oura Ring` → `Oura-Ring`
  4. Construct target path: `Receipts/{year}/{monthFolder}/{vendorFolder}`
  5. Mark items with missing/invalid data as `skip: true`

**Vendor Folder Mapping**:
| Database Value | Folder Name |
|----------------|-------------|
| OpenAI | OpenAI |
| Anthropic | Anthropic |
| AWS | AWS |
| Google Cloud | Google-Cloud |
| GitHub | GitHub |
| Oura Ring | Oura-Ring |

**Output Schema**:
```javascript
{
  fileId: "1abc...",
  fileName: "Receipt_OpenAI_2025-01.pdf",
  vendor: "OpenAI",
  date: "2025-01-15",
  receiptId: "RCPT-OpenAI-1704672000",
  currentPath: "_Receipt-Pool",
  targetYear: "2025",
  targetMonth: "01-January",
  targetVendor: "OpenAI",
  targetPath: "Receipts/2025/01-January/OpenAI",
  skip: false
}
```

### 7. Generate Summary Report
- **Type**: Code (v2)
- **Mode**: Run Once for All Items
- **Logic**:
  1. Count total files, ready to organize, skipped
  2. Group by vendor: `{OpenAI: 5, Anthropic: 3, ...}`
  3. Group by month: `{2025-01-January: 8, 2024-12-December: 2, ...}`
  4. Collect all errors (missing data, unknown vendors)
  5. Generate detailed file list with target paths
  6. Log to console for review

**Output Schema**:
```javascript
{
  timestamp: "2026-01-04T12:00:00.000Z",
  totalFiles: 15,
  readyToOrganize: 12,
  skipped: 3,
  byVendor: {
    "OpenAI": 5,
    "Anthropic": 3,
    "AWS": 2,
    "GitHub": 2
  },
  byMonth: {
    "2025-01-January": 8,
    "2024-12-December": 4
  },
  errors: [
    {
      receiptId: "RCPT-UnknownVendor-1704672000",
      fileName: "Receipt.pdf",
      error: "Unknown vendor: SomeService"
    }
  ],
  fileDetails: [
    {
      receiptId: "RCPT-OpenAI-1704672000",
      fileName: "Receipt_OpenAI.pdf",
      vendor: "OpenAI",
      date: "2025-01-15",
      currentLocation: "_Receipt-Pool",
      targetPath: "Receipts/2025/01-January/OpenAI",
      status: "ready",
      error: null
    }
  ]
}
```

---

## Database Schema (Receipts Sheet)

**Required Fields for Organization**:
- `FileID` (string) - Google Drive file ID (join key)
- `Vendor` (string) - Must match one of 6 supported vendors
- `Date` (string) - Format: YYYY-MM-DD

**Optional Fields** (not used by this workflow):
- `ReceiptID` (string) - Unique receipt identifier
- `Source` (string) - Gmail/Manual
- `Amount` (number)
- `Currency` (string)
- `FilePath` (string) - Current location (will be updated in v1.2.5)
- `ProcessedDate` (date)
- `Matched` (boolean)

---

## Error Handling

### File Matching Errors
**Scenario**: File in Receipt Pool but no metadata in database
- **Action**: Skip file, log error to console
- **Error Message**: `"No metadata found in Receipts sheet"`
- **Resolution**: Add metadata manually or re-run Workflow 2 (Gmail Receipt Monitor)

### Missing Required Fields
**Scenario**: Metadata exists but `Date` or `Vendor` is empty
- **Action**: Skip file, log error to console
- **Error Message**: `"Missing required fields - Date: undefined, Vendor: undefined"`
- **Resolution**: Update Receipts sheet with missing data

### Unknown Vendor
**Scenario**: Vendor in database doesn't match any of 6 supported vendors
- **Action**: Mark as `skip: true`, include in error report
- **Error Message**: `"Unknown vendor: SomeService. Expected: OpenAI, Anthropic, AWS, Google Cloud, GitHub, or Oura Ring"`
- **Resolution**:
  1. Check for typos in Receipts sheet
  2. If new vendor, add to VendorMappings and create folder structure
  3. Update vendor folder map in "Determine Target Folder" node

### Invalid Date Format
**Scenario**: Date field doesn't match YYYY-MM-DD format
- **Action**: Mark as `skip: true`, include in error report
- **Error Message**: `"Invalid month: XX"`
- **Resolution**: Update date format in Receipts sheet

---

## Testing Workflow

### Prerequisites
1. At least 3-5 test receipts in Receipt Pool folder
2. Corresponding records in Receipts sheet with:
   - Correct `FileID` matching Drive file IDs
   - Valid `Vendor` (one of 6 supported)
   - Valid `Date` (YYYY-MM-DD format)

### Test Execution Steps
1. Open n8n workflow: "Workflow 4: File Organization & Sorting"
2. Click "Execute Workflow" button (manual trigger)
3. Review execution results:
   - Check "Generate Summary Report" node output
   - Verify `readyToOrganize` count matches expectations
   - Check `errors` array for any issues
   - Review `fileDetails` for correct target paths
4. Inspect console logs (n8n execution panel → Console)
5. Validate folder paths match existing folder structure

### Expected Results
```json
{
  "timestamp": "2026-01-04T12:00:00.000Z",
  "totalFiles": 5,
  "readyToOrganize": 5,
  "skipped": 0,
  "byVendor": {
    "OpenAI": 2,
    "Anthropic": 2,
    "GitHub": 1
  },
  "byMonth": {
    "2025-01-January": 3,
    "2024-12-December": 2
  },
  "errors": [],
  "fileDetails": [...]
}
```

### Validation Checklist
- [ ] All files from Receipt Pool loaded (count matches)
- [ ] All receipts from database loaded (count matches)
- [ ] Files correctly matched by FileID
- [ ] Target paths follow format: `Receipts/{year}/{month}/{vendor}`
- [ ] Month folders use correct naming: `01-January` not `January`
- [ ] Vendor folders match existing structure (e.g., `Google-Cloud` not `Google Cloud`)
- [ ] Errors logged for invalid data
- [ ] No crashes or node failures

---

## Known Limitations (v1.2.4)

1. **No actual file moves** - This version only generates organization reports
2. **No folder ID lookup** - Would require 144+ hardcoded IDs or dynamic search
3. **No database updates** - FilePath field not updated (comes in v1.2.5)
4. **6 vendors only** - Only supports: OpenAI, Anthropic, AWS, Google Cloud, GitHub, Oura Ring
5. **2024-2025 only** - Folder structure only exists for these years
6. **No folder creation** - Assumes all monthly vendor folders already exist

---

## Roadmap to v1.2.5 (Actual File Organization)

### Remaining Tasks

**1. Implement Folder ID Lookup**
Two approaches:
- **Option A**: Hardcode 144 folder IDs (6 vendors × 12 months × 2 years)
- **Option B**: Dynamic lookup using Google Drive search (slower but maintainable)

**Option B Implementation (Recommended)**:
```javascript
// Add node after "Determine Target Folder"
// Use Google Drive "Search" operation
const folderQuery = `name='${targetVendor}' and '${monthFolderId}' in parents and mimeType='application/vnd.google-apps.folder'`;
// Returns folder ID for move operation
```

**2. Add Google Drive Move Node**
- **Type**: Google Drive (v3)
- **Operation**: Move File
- **File ID**: `={{ $json.fileId }}`
- **Destination Folder ID**: `={{ $json.targetFolderId }}`

**3. Add Database Update Node**
- **Type**: Google Sheets (v4.5)
- **Operation**: Update
- **Document**: Expense-Database
- **Sheet**: Receipts
- **Lookup Column**: FileID
- **Update Column**: FilePath = `{{ $json.targetPath }}`

**4. Add Error Logging Sheet** (Optional)
- Create new sheet: "OrganizationErrors"
- Log failed moves with timestamps
- Allows Sway to review and fix issues

**Estimated Effort**: 2-3 hours to implement v1.2.5 with folder lookup and moves

---

## Import Instructions

### Step 1: Delete Placeholder Workflow
The workflow created via MCP (ID: `nASL6hxNQGrNBTV4`) is just a placeholder. Either:
- Delete it in n8n UI
- Import blueprint as new workflow (don't overwrite)

### Step 2: Import Blueprint
1. Open n8n web interface
2. Navigate to Workflows
3. Click "+ Add workflow" → "Import from File"
4. Select file: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/workflow4_file_organization_v1.2.4.json`
5. Click "Import"

### Step 3: Verify Credentials
After import, check all Google nodes have credentials configured:
- Load Receipt Files → Google OAuth2 API (a4m50EefR3DJoU0R)
- Read Receipt Metadata → Google OAuth2 API (a4m50EefR3DJoU0R)

If credentials are missing, re-select in each node.

### Step 4: Test Execution
1. Click "Execute Workflow" (manual trigger)
2. Review "Generate Summary Report" output
3. Check console logs for errors
4. Validate target paths match folder structure

### Step 5: Update VERSION_LOG.md
Add entry for v1.2.4 with workflow ID from n8n.

---

## Troubleshooting

### Issue: No files returned from Receipt Pool
**Check**:
- Folder ID is correct: `12SVQzuWtKva48LvdGbszg3UcKl7iy-1x`
- Folder contains files
- Google Drive credentials are valid
- Service account has access to Expenses-System folder

### Issue: No metadata returned from Receipts sheet
**Check**:
- Spreadsheet ID is correct: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
- Sheet name is exactly "Receipts" (case-sensitive)
- Sheet has header row
- Google Sheets credentials are valid

### Issue: All files marked as "skipped"
**Check**:
- FileID values in Receipts sheet match Google Drive file IDs
- Date field format is YYYY-MM-DD (not MM/DD/YYYY)
- Vendor names match exactly (check capitalization, spaces)

### Issue: "Unknown vendor" errors
**Check**:
- Vendor names in database match one of 6 supported:
  - OpenAI
  - Anthropic
  - AWS
  - Google Cloud (not "Google-Cloud" in database)
  - GitHub
  - Oura Ring (not "Oura-Ring" in database)

### Issue: Wrong month folder names
**Check**:
- Code uses format: `01-January` (not `January` or `1-January`)
- Matches existing folder structure in Google Drive

---

## Next Steps After v1.2.4

1. **Test with real data** - Run on actual receipts in Receipt Pool
2. **Validate folder paths** - Manually check if paths match Drive structure
3. **Review error report** - Fix any data quality issues in Receipts sheet
4. **Plan v1.2.5** - Decide on folder lookup approach (hardcode vs dynamic)
5. **Implement moves** - Add Google Drive move operation
6. **Update database** - Add FilePath update after successful move
7. **End-to-end test** - Verify full organization cycle works

---

## Support & Maintenance

**Workflow Location**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/`

**Documentation**: This file + VERSION_LOG.md

**Related Workflows**:
- Workflow 1: PDF Intake & Parsing (creates Statements records)
- Workflow 2: Gmail Receipt Monitor (creates Receipts records)
- Workflow 3: Transaction-Receipt Matching (links transactions to receipts)

**Questions**: Refer to main design doc at `/Users/swayclarke/.claude/plans/typed-tickling-sprout.md`
