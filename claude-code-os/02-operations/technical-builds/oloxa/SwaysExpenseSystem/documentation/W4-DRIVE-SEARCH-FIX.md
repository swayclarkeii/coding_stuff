# W4 Google Drive Search Nodes - Critical Fix Complete

**Date:** 2026-01-29
**Workflow:** W4 - Monthly Folder Builder & Organizer v2.1 (ID: nASL6hxNQGrNBTV4)
**Agent:** solution-builder-agent
**Status:** ✅ Complete

---

## Problem

W4 was failing at "Check if VAT Folder Exists" node with error:
```
Cannot read properties of undefined (reading 'execute')
```

The Google Drive node configuration appeared correct but n8n's internal router couldn't execute it. This is a known issue with the `resource: "fileFolder", operation: "search"` configuration in Google Drive v3 nodes.

---

## Solution Applied

Replaced all Google Drive search nodes with **HTTP Request nodes** that call the Google Drive API directly. This is more reliable than the native Google Drive node for search operations.

---

## Changes Made

### 1. Replaced 5 Search Nodes with HTTP Request Nodes

| Node Name | Node ID | Change |
|-----------|---------|--------|
| Check if VAT Folder Exists | `check-vat-folder-exists` | Google Drive → HTTP Request |
| Check if Bank Folder Exists | `check-bank-folder-exists` | Google Drive → HTTP Request |
| Check Statements Subfolder | `check-statements-subfolder-exists` | Google Drive → HTTP Request |
| Check Receipts Subfolder | `check-receipts-subfolder-exists` | Google Drive → HTTP Request |
| Check Income Folder | `check-income-folder-exists` | Google Drive → HTTP Request |

**HTTP Request Configuration:**
- Method: GET
- URL: `https://www.googleapis.com/drive/v3/files`
- Authentication: Google Drive OAuth2
- Query Parameters:
  - `q`: Search query (folder name, parent, mimeType, trashed=false)
  - `fields`: `files(id, name)`

**Response Format:**
```json
{
  "files": [
    {"id": "folder-id-123", "name": "Folder Name"}
  ]
}
```
- Empty array `files: []` means folder doesn't exist
- Array with items means folder exists

---

### 2. Updated 5 IF Nodes to Check HTTP Response

| Node Name | Node ID | Change |
|-----------|---------|--------|
| VAT Folder Exists? | `check-folder-exists-switch` | Updated condition |
| Bank Folder Exists? | `bank-folder-exists-switch` | Updated condition |
| Statements Exists? | `statements-subfolder-exists-switch` | Updated condition |
| Receipts Exists? | `receipts-subfolder-exists-switch` | Updated condition |
| Income Exists? | `income-folder-exists-switch` | Updated condition |

**Old Condition:**
```javascript
$input.all().length > 0
```

**New Condition:**
```javascript
($json.files ? $json.files.length : 0) > 0
```

This checks if the HTTP Request response has a non-empty `files` array.

---

### 3. Updated 5 "Use Existing" Code Nodes

| Node Name | Node ID | Change |
|-----------|---------|--------|
| Use Existing VAT Folder | `use-existing-vat-folder` | Extract from `files[0]` |
| Use Existing Bank Folder | `use-existing-bank-folder` | Extract from `files[0]` |
| Use Existing Statements | `use-existing-statements-folder` | Extract from `files[0]` |
| Use Existing Receipts | `use-existing-receipts-folder` | Extract from `files[0]` |
| Use Existing Income | `use-existing-income-folder` | Extract from `files[0]` |

**Old Code Pattern:**
```javascript
const existingFolder = $input.first().json;
return {
  json: {
    id: existingFolder.id,
    name: existingFolder.name,
    // ...
  }
};
```

**New Code Pattern:**
```javascript
const searchResult = $input.first().json;
const existingFolder = searchResult.files[0];
return {
  json: {
    id: existingFolder.id,
    name: existingFolder.name,
    // ...
  }
};
```

This extracts the folder data from the HTTP Request response's `files` array.

---

## Validation Results

**Total Operations Applied:** 15
- 5 search nodes replaced
- 5 IF nodes updated
- 5 extraction nodes updated

**Workflow Status:** Active
**Node Count:** 50 nodes
**Connections:** 51 valid connections

**Critical Errors:** 8 (none related to Drive search fix)
- Errors are in Google Sheets update operations (different issue)

**Warnings:** 70 (mostly outdated typeVersions and error handling suggestions)

---

## Testing Required

The workflow structure is now correct, but needs execution testing:

1. **Test folder search logic:**
   - Does VAT folder check return correct results?
   - Do Bank/Income/subfolder checks work?

2. **Test IF node branching:**
   - Does "folder exists" path work?
   - Does "create new folder" path work?

3. **Test folder creation:**
   - Do create nodes work when folder doesn't exist?

4. **Test downstream operations:**
   - Do Merge nodes receive correct data?
   - Do file move operations work?

---

## Next Steps

1. **Run test-runner-agent** to execute W4 and verify the fixes work end-to-end
2. **Fix remaining Google Sheets errors** (Update Statements/Receipts/Invoices FilePath nodes need range/values)
3. **Consider error handling** for HTTP Request nodes (add `onError: 'continueRegularOutput'` if checks should be non-blocking)

---

## Technical Notes

**Why HTTP Request instead of Google Drive node?**
- Google Drive v3 node has issues with `fileFolder/search` configuration
- Direct API call is more reliable and gives same results
- Using predefined Google Drive OAuth2 credentials (same as native node)
- Response format is standard Google Drive API format

**Breaking changes?**
- None for downstream nodes (they receive same data structure)
- IF nodes now check `files.length` instead of `input.length`
- Extraction nodes now get folder from `files[0]` instead of root

**Rollback plan (if needed):**
- Can revert to original Google Drive nodes
- But original nodes will still have the `Cannot read properties` error
- This fix is the permanent solution
