# Eugene V8 Document Test Runner - Phase 0

## Workflow ID
`0nIrDvXnX58VPxWW`

## Status
**Built - Needs Manual Configuration**

The workflow has been created with 21 nodes and the core structure is in place. However, there are a few configuration items that need to be completed in the n8n UI:

### Required Manual Configuration

1. **Google Sheet ID**
   - The workflow creates a sheet named "Eugene V8 Test Results"
   - After first run, you'll need to copy the Sheet ID from the URL
   - Update these nodes with the Sheet ID:
     - "Get Next Pending Document"
     - "Update Status to Testing"
     - "Mark Passed"
     - "Mark Failed"
     - "Final Summary" (in code)

2. **IF Node Connection Fix**
   - The "Check All Passed" IF node has two outputs:
     - Output 0 (True): Should connect to "Prepare Passed Status Update"
     - Output 1 (False): Should connect to "Prepare Failed Status Update"
   - This may need manual verification in the UI

3. **Google Sheets Range Configuration**
   - "Get Next Pending Document" node needs range set to "A:G"

### Known Issues

1. **Infinite Loop Warning** - This is INTENTIONAL
   - The workflow loops back from "Mark Passed" and "Mark Failed" to "Get Next Pending Document"
   - This continues until all documents are tested
   - The loop exits via "Check If Complete" when no pending documents remain

2. **Google Sheets Read Operation**
   - May need to configure filters in the UI for the "Get Next Pending Document" node
   - Should filter by Status = "pending"

### Workflow Structure

**Initialization Phase:**
1. Manual Trigger
2. Create/Get Google Sheet ("Eugene V8 Test Results")
3. List all PDFs from Drive (folder: 1-jO4unjKgedFqVqtofR4QEM18xC09Fsk)
4. Filter to .pdf files only
5. Prepare initial row data
6. Initialize sheet with all documents (Status = "pending")

**Document Processing Loop:**
7. Get Next Pending Document (query sheet for Status = "pending")
8. Check If Complete (if no pending → go to Final Summary)
9. Download PDF from Drive
10. Prepare Testing Status Update
11. Update Status to "testing" in sheet
12. Send Test Email (from swayfromthehook@gmail.com to swayclarkeii@gmail.com)
13. Wait 120 seconds
14. Query n8n Executions API (check Pre-Chunk 0, Chunk 2, Chunk 2.5)
15. Check All Passed (IF node)
    - TRUE → Prepare Passed Status Update → Mark Passed → Loop back to #7
    - FALSE → Prepare Failed Status Update → Mark Failed → Loop back to #7

**Completion Phase:**
16. Final Summary (count passed/failed/pending)
17. Send Summary Email

### Testing Plan

**Before first run:**
1. Ensure Combined Google Auth credential (a4m50EefR3DJoU0R) has permissions for:
   - Google Drive (read files)
   - Google Sheets (create, read, write)
   - Gmail (send emails)

2. Verify test folder contains PDFs:
   - Folder ID: 1-jO4unjKgedFqVqtofR4QEM18xC09Fsk
   - Should contain 50-100 German real estate PDFs

**First test run:**
1. Activate workflow in n8n
2. Click "Test workflow" button
3. Monitor execution to see if sheet is created
4. Copy Sheet ID from created Google Sheet
5. Paste Sheet ID into the nodes listed above
6. Run second test to verify full loop

**Expected behavior:**
- Sheet created with columns: Document Name, File ID, Status, Test Start, Test End, Error Details, Execution IDs
- All PDFs listed with Status = "pending"
- First PDF downloaded and emailed
- After 120s, execution status checked
- Sheet updated with "passed" or "failed"
- Next pending document processed
- Loop continues until all documents tested
- Final summary email sent

### Limitations (Phase 0)

**What's NOT included (vs full solution brief):**
- ❌ No retry logic (documents only tested once)
- ❌ No solution-builder-agent integration (no automatic fixes)
- ❌ No batch processing (one document at a time)
- ❌ No automatic re-queuing of failed documents

**What to do when documents fail:**
1. Check "Error Details" column in Google Sheet
2. Manually review the execution IDs listed
3. Fix the underlying issue manually
4. Change Status back to "pending" in sheet to re-test
5. Run workflow again to process pending documents

### Next Steps

**To enable Phase 1 features:**
1. Add retry counter column to sheet
2. Add batch processing (2-3 documents at once)
3. Design HTTP interface for solution-builder-agent calls
4. Add retry logic (max 3 attempts per document)
5. Add fix logging when agent makes changes

### Files Modified

- Workflow created: ID `0nIrDvXnX58VPxWW` in n8n

### Credentials Used

- **Combined Google Auth** (ID: a4m50EefR3DJoU0R)
  - Used for: Google Drive, Google Sheets, Gmail
  - Must have scopes: Drive, Sheets, Gmail

- **n8n API Key** (embedded in "Query n8n Executions" node)
  - Hard-coded in Code node (not ideal for production)
  - Used to query execution status via n8n API

### Code Nodes

**Filter to PDFs Only:**
```javascript
const items = $input.all();

const pdfs = items.filter(item => {
  const name = item.json.name || '';
  return name.toLowerCase().endsWith('.pdf');
});

return pdfs;
```

**Prepare Initial Row Data:**
```javascript
const items = $input.all();

const rows = items.map(item => {
  return {
    json: {
      'Document Name': item.json.name,
      'File ID': item.json.id,
      'Status': 'pending',
      'Test Start': '',
      'Test End': '',
      'Error Details': '',
      'Execution IDs (Pre/C2/C2.5)': ''
    }
  };
});

return rows;
```

**Query n8n Executions:**
```javascript
const testStartTime = $json['Test Start'];
const workflows = [
  { id: 'YGXWjWcBIk66ArvT', name: 'Pre-Chunk 0' },
  { id: 'qKyqsL64ReMiKpJ4', name: 'Chunk 2' },
  { id: 'okg8wTqLtPUwjQ18', name: 'Chunk 2.5' }
];

const results = [];

for (const wf of workflows) {
  const response = await $http.request({
    method: 'GET',
    url: `https://n8n.oloxa.ai/api/v1/executions?workflowId=${wf.id}&status=success&limit=1`,
    headers: {
      'X-N8N-API-KEY': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlOWJkOTExMi1jMmUzLTRmNjctODczYS1lMTAwMWJhZWFmZDgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY3MzgzODM0fQ.EDsEy9tZ-kHtpzir8jD_I-I3YbKgtOJcx_ZmH5SZLT4'
    }
  });

  const executions = response.data || [];
  const recent = executions.find(exec => new Date(exec.startedAt) > new Date(testStartTime));

  results.push({
    workflow: wf.name,
    workflowId: wf.id,
    executionId: recent?.id || null,
    status: recent?.status || 'not_found',
    startedAt: recent?.startedAt || null
  });
}

const allPassed = results.every(r => r.status === 'success');

return {
  json: {
    ...($input.first().json),
    executionResults: results,
    allPassed: allPassed,
    executionIds: results.map(r => r.executionId).join(', ')
  }
};
```

---

**Created:** 2026-01-16
**Status:** Ready for manual configuration and testing
**Agent:** solution-builder-agent
