# Diagnostic Workflow: List Bank-Statements Folder

## Workflow ID
`AnT0cLvpQZyTWid3`

## Purpose
Troubleshoot why Workflow 1 isn't detecting files in the Bank-Statements folder by listing all files from n8n's perspective using the same Google Drive credentials.

## Structure

### Node 1: Manual Trigger
- **Type:** Manual Trigger
- **Purpose:** Start the workflow on demand

### Node 2: Google Drive - List Files
- **Type:** Google Drive
- **Resource:** File/Folder
- **Operation:** Search
- **Drive:** My Drive
- **Folder ID:** `1stmB5nWmoViQKKuQqpkWICPrfPQ_GDN1` (Bank-Statements folder)
- **Credential:** `a4m50EefR3DJoU0R` (Google Drive account)

## How to Use

1. Open the workflow in n8n: `Diagnostic: List Bank-Statements Folder`
2. Click "Execute Workflow" (manual trigger)
3. Check the output from the Google Drive node to see:
   - How many files are detected
   - File names, IDs, and metadata
   - Whether the folder is accessible with the current credentials

## Expected Output

The workflow will return a list of all files/folders found in the Bank-Statements folder, including:
- File names
- File IDs
- MIME types
- Creation/modification dates
- File sizes

## Troubleshooting

If the workflow returns:
- **Empty results:** The credentials may not have access to the folder, or the folder is empty
- **Error:** Check credential permissions or folder ID validity
- **Files detected here but not in Workflow 1:** Compare the trigger conditions in Workflow 1

## Status
✅ Workflow created and validated
⚠️ Workflow is inactive (use manual execution)
