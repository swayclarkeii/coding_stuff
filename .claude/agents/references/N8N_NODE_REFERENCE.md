---
name: n8n Node Reference
description: Comprehensive reference for n8n node types, parameters, and configurations
---

# n8n Node Reference - Common Services

**Purpose:** This reference provides the EXACT available operations for commonly used n8n nodes. Use this to validate that suggested operations actually exist before including them in workflows or designs.

**CRITICAL RULE:** If an operation is not listed here, it does NOT exist. Do NOT suggest operations that are not explicitly listed.

---

## Google Drive (n8n-nodes-base.googleDrive)

### Resource: File
- **Copy** - Copy a file
- **Create from text** - Create a file from text
- **Delete** - Delete a file
- **Download** - Download a file
- **Move** - Move a file (NOT "list" - use Search instead)
- **Share** - Share a file
- **Update** - Update a file
- **Upload** - Upload a file

### Resource: File/Folder
- **Search** - Search for files and folders (use this to "list" files)

### Resource: Folder
- **Create** - Create a folder
- **Delete** - Delete a folder
- **Share** - Share a folder

### Resource: Shared Drive
- **Create** - Create a shared drive
- **Delete** - Delete a shared drive
- **Get** - Get a shared drive
- **Get Many** - Get many shared drives
- **Update** - Update a shared drive

**Common Mistakes:**
- ❌ "List files" - Does NOT exist. Use **Search** in File/Folder resource instead
- ❌ "Read file" - Does NOT exist. Use **Download** instead
- ✅ To list files in a folder, use **Search** with folder ID as filter

---

## Google Sheets (n8n-nodes-base.googleSheets)

### Resource: Document (Spreadsheet)
- **Create** - Create a spreadsheet
- **Delete** - Delete a spreadsheet

### Resource: Sheet Within Document
- **Append Row** - Create a new row in a sheet
- **Append or Update Row** - Append a new row or update an existing one (upsert)
- **Clear** - Delete all the contents or a part of a sheet
- **Create** - Create a new sheet
- **Delete** - Permanently delete a sheet
- **Delete Rows or Columns** - Delete columns or rows from a sheet
- **Get Row(s)** - Retrieve one or more rows from a sheet
- **Update Row** - Update an existing row in a sheet

**Common Mistakes:**
- ❌ "Read sheet" - Use **Get Row(s)** instead
- ❌ "Insert row" - Use **Append Row** instead
- ✅ Use **Append or Update Row** for upsert operations (create if not exists, update if exists)

---

## Google Calendar (n8n-nodes-base.googleCalendar)

### Resource: Calendar
- **Availability** - Check if a time-slot is available in a calendar

### Resource: Event
- **Create** - Add an event to calendar
- **Delete** - Delete an event
- **Get** - Retrieve an event
- **Get Many** - Retrieve many events from a calendar
- **Update** - Update an event

**Common Mistakes:**
- ❌ "List events" - Use **Get Many** instead
- ✅ Use filters with **Get Many** to search for specific events

---

## Gmail (n8n-nodes-base.gmail)

### Resource: Draft
- **Create** - Create a draft
- **Delete** - Delete a draft
- **Get** - Get a draft
- **Get Many** - Get many drafts

### Resource: Label
- **Create** - Create a label
- **Delete** - Delete a label
- **Get** - Get a label info
- **Get Many** - Get many labels

### Resource: Message
- **Add Label** - Add label to message
- **Delete** - Delete a message
- **Get** - Get a message
- **Get Many** - Get many messages
- **Mark as Read** - Mark a message as read
- **Mark as Unread** - Mark a message as unread
- **Remove Label** - Remove label from message
- **Reply** - Reply to a message
- **Send** - Send a message
- **Send and Wait for Response** - Send message and wait for response

### Resource: Thread
- **Add Label** - Add label to thread
- **Delete** - Delete a thread
- **Get** - Get a thread
- **Get Many** - Get many threads
- **Remove Label** - Remove label from thread
- **Reply** - Reply to a message
- **Trash** - Trash a thread
- **Untrash** - Untrash a thread

**Common Mistakes:**
- ❌ "List messages" - Use **Get Many** instead
- ❌ "Read message" - Use **Get** instead
- ✅ Use filters with **Get Many** to search for specific messages

---

## Notion (n8n-nodes-base.notion)

### Resource: Block
- **Append After** - Append a block
- **Get Child Blocks** - Get many child blocks

### Resource: Database
- **Get** - Get a database

### Resource: Database Page
- **Create** - Create a database page
- **Get** - Get a database page
- **Get Many** - Get many database pages
- **Update** - Update a database page

### Resource: Page
- **Archive** - Archive a page
- **Create** - Create a page
- **Get** - Get a page
- **Search** - Search pages

### Resource: User
- **Get** - Get a user
- **Get Many** - Get many users

**Common Mistakes:**
- ❌ "List pages" - Use **Get Many** for database pages or **Search** for general pages
- ❌ "Delete page" - Use **Archive** instead (Notion doesn't have direct delete)
- ✅ Use **Database Page > Get Many** to query databases with filters

---

## Fathom

**Status:** No official n8n node available for Fathom.

**Alternatives:**
- Use **HTTP Request** node to call Fathom API directly
- Check n8n community nodes for unofficial Fathom integrations
- Use **Webhook** node if Fathom supports webhooks for your use case

---

## Validation Checklist for Agents

Before suggesting ANY operation in a workflow design:

1. ✅ Check this reference document
2. ✅ Verify the EXACT resource name
3. ✅ Verify the EXACT operation name
4. ✅ If operation isn't listed → Use `mcp__n8n-mcp__get_node` to verify
5. ❌ NEVER guess or assume an operation exists
6. ❌ NEVER use generic terms like "list", "read" - check exact names

**Example Good Workflow Step:**
```
Resource: Google Drive > File/Folder
Operation: Search
Parameters:
  - Query: name contains 'report'
  - Folder ID: {{parent_folder_id}}
```

**Example Bad Workflow Step:**
```
❌ Resource: Google Drive > File
❌ Operation: List Files  (DOES NOT EXIST)
```

---

## When to Call MCP for More Info

**Call `mcp__n8n-mcp__get_node` when:**
- Operation not listed in this reference
- Need to know required/optional parameters for an operation
- Need to see parameter validation rules or formats
- Need version-specific information

**Example:**
```javascript
mcp__n8n-mcp__get_node({
  nodeType: "n8n-nodes-base.googleDrive",
  mode: "info",
  detail: "standard"
})
```

This returns the full schema including all parameters, validations, and requirements.

---

## Quick Reference Table

| Service | Node Type | Key Resources | Notes |
|---------|-----------|---------------|-------|
| Google Drive | nodes-base.googleDrive | File, Folder, Shared Drive | Use Search, not "List" |
| Google Sheets | nodes-base.googleSheets | Document, Sheet | Always specify sheet name |
| Google Calendar | nodes-base.googleCalendar | Calendar, Event | Use Get Many, not "List" |
| Gmail | nodes-base.gmail | Draft, Label, Message, Thread | Supports complex queries |
| Notion | nodes-base.notion | Block, Database, Database Page, Page | Use Archive, not Delete |
| Fathom | - | N/A | Use HTTP Request node |

---

## JavaScript Code Patterns in n8n

### Binary Data Access

**✅ CORRECT - Access via item.binary:**
```javascript
const attachment = item.binary.attachment_0;
const filename = attachment.fileName;
```

**❌ INCORRECT - Other methods don't work:**
```javascript
// These patterns will fail:
const attachment = item.attachments[0];
const attachment = item.binary['data'];
```

**Key Learning:** Gmail trigger stores attachments with keys like `attachment_0`, `attachment_1`, etc. Always iterate `Object.entries(item.binary)`.

### Binary Data Preservation Through Workflow Chains

**CRITICAL ISSUE:** Binary data does NOT automatically propagate through Code nodes and transformations.

**❌ Problem Pattern:**
```
Gmail Trigger (binary created) → Extract Text from PDF → Code node → Decision Gate → Merge node
Result: Binary data is LOST by the time execution reaches Merge node
```

**Why it happens:**
- Code nodes do NOT preserve binary data unless explicitly returned
- Data transformations create new items without binary
- Long execution chains cause binary data to disappear

**✅ CORRECT - Explicitly preserve binary in Code nodes:**
```javascript
// In ANY Code node that processes items with binary data
const item = $input.first();

return {
  json: {
    // Your transformed JSON data
    client_name: extractedName,
    status: 'processed'
  },
  binary: item.binary  // ✅ CRITICAL: Preserve binary data
};
```

**❌ WRONG - Binary not preserved:**
```javascript
return {
  json: {
    client_name: extractedName,
    status: 'processed'
  }
  // ❌ Binary data is lost!
};
```

**Alternative Solutions:**

**Option 1: Upload binary to storage early**
```
Gmail Trigger → Upload PDF to Drive → Continue with file_id
(Binary stored in Drive, pass file_id through workflow)
```

**Option 2: Parallel binary path**
```
Gmail Trigger → Split
├─ Path A: Text extraction + logic (no binary)
└─ Path B: Binary preserved → Merge at end
```

**Key Learning:** When workflow needs binary data later, EVERY Code node in the chain must explicitly return `binary: item.binary` or `binary: $input.first().binary`. Missing this in even ONE node loses binary data forever.

### Node Reference Methods

**Two ways to reference node data:**

1. **$input.all()** - Items flowing through ACTUAL connection
```javascript
const items = $input.all();  // Use when node is directly connected
```

2. **$('NodeName').first().json** - Expression-based retrieval
```javascript
const data = $('Normalize Client Name').first().json;  // Use to grab data from any previous node
```

**Critical:** Use `$input.all()` for items passing through the node's input connection. Use `$('NodeName')` to reference data from nodes NOT directly connected.

### String Normalization for Matching

**❌ WRONG - Normalize only one side:**
```javascript
const clientRow = rows.find(row => {
  const clientName = row.json.Client_Name || '';
  return clientName.toLowerCase().includes(clientNormalized.toLowerCase());
  // Fails: "villa martens" doesn't include "villa_martens"
});
```

**✅ CORRECT - Normalize BOTH sides:**
```javascript
const clientRow = rows.find(row => {
  const clientName = row.json.Client_Name || '';

  // Normalize the sheet name the SAME way as the incoming normalized name
  const normalizedName = clientName
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

  return normalizedName === clientNormalized;  // Exact match after normalization
});
```

**Key Learning:** When comparing user input against database values, apply the EXACT SAME normalization logic to both sides.

### Regex Escaping in JavaScript

**❌ WRONG - Over-escaped:**
```javascript
const cleaned = text.replace(/\\\\s*(gmbh)/gi, '');  // Too many backslashes
```

**✅ CORRECT - Single backslash:**
```javascript
const cleaned = text.replace(/\s*(gmbh|ag|kg)/gi, '');
```

**Key Learning:** In JavaScript string literals used in n8n Code nodes, regex patterns need single backslash (`\s`, `\d`, `\w`), not double backslash.

### Field Name Exact Matching

**Google Sheets requires EXACT field name matches:**

```javascript
// ❌ WRONG - Field names don't match sheet headers
return [{
  json: {
    Intake_Folder_ID: stagingFolderId,  // Sheet expects "Staging_Folder_ID"
  }
}];
```

```javascript
// ✅ CORRECT - Field names match sheet headers exactly
return [{
  json: {
    Client_Name: clientNameRaw,          // Matches header
    Client_Normalized: clientNormalized, // Matches header
    Staging_Folder_ID: stagingFolderId, // Matches header exactly
    Date_Created: new Date().toISOString(),
    status: 'ACTIVE'
  }
}];
```

**Key Learning:** When using Google Sheets "Auto-Map Columns" mode, output field names must match sheet column headers EXACTLY (case-sensitive, underscore placement, etc.).

---

## Google Drive Node - Critical Details

### Move vs Update Operations

**✅ CORRECT - Move operation (simple):**
```javascript
{
  "operation": "move",
  "fileId": "={{ $json.file_id }}",
  "folderId": "={{ $json.staging_folder_id }}"  // Target folder ID
}
```

**❌ WRONG - Update operation (complex, requires parentId in updateFields):**
```javascript
{
  "operation": "update",
  "fileId": "={{ $json.file_id }}",
  "updateFields": {
    "parentId": "={{ $json.staging_folder_id }}"  // More complex
  }
}
```

**Key Learning:** Use **Move** operation with `folderId` parameter to move files between folders. The **Update** operation can also move files but requires nested `updateFields.parentId` configuration.

### Upload File Location Validation

**CRITICAL:** If folder ID parameter is missing or wrong, files upload to unknown default location.

**❌ Problem:**
```javascript
{
  "operation": "upload",
  "folderId": ""  // Empty or undefined
}
// Result: File uploads to "0ADu2vODw7d18Uk9PVA" or user's root drive
```

**Evidence from testing:**
- Expected folder: `1ahpPa6pOLR1xK3tU4q0YOTQJOczr7ZsS`
- Actual upload: `0ADu2vODw7d18Uk9PVA` (wrong location)
- Root cause: Missing/undefined folder ID parameter

**✅ CORRECT - Validate folder ID before upload:**
```javascript
// In Code node before Google Drive Upload
const folderId = $json.staging_folder_id;

if (!folderId || folderId === '') {
  throw new Error('Missing folder ID - cannot upload file');
}

return {
  json: {
    ...item.json,
    folderId: folderId  // Pass validated folder ID
  },
  binary: item.binary
};
```

**Prevention checklist:**
- [ ] Verify folder ID exists and is not empty
- [ ] Validate folder ID format (should be alphanumeric string)
- [ ] Add error handling before upload operations
- [ ] Test upload location after workflow changes

**Key Learning:** Always validate Google Drive folder IDs before upload operations. Missing folder IDs result in files uploading to unexpected locations that are hard to locate.

---

## Google Sheets Node - Data Modes

### Two Append Modes with Different Behaviors

**Mode 1: "Map Each Column Below" (manual mapping)**
- Requires explicit field mappings in "Fields to Send" section
- If mappings are missing, node reports SUCCESS but writes NO data
- Use when you need precise control over which fields map to which columns

**Mode 2: "Auto-Map Columns" (automatic)**
- Automatically matches JSON field names to sheet column headers
- Requires EXACT field name match (case-sensitive)
- Use when your JSON output fields already match sheet headers

**Critical Bug Pattern:**
```javascript
// Node configuration:
{
  "dataMode": "defineBelow",  // "Map Each Column Below"
  "columnsUi": {
    "values": []  // ❌ EMPTY - No mappings defined!
  }
}
// Result: Node shows SUCCESS but writes nothing to sheet
```

**Fix:**
```javascript
{
  "dataMode": "autoMapInputData"  // ✅ "Auto-Map Columns" mode
}
```

### Google Sheets Header Exclusion and .slice(1) Anti-Pattern

**CRITICAL BUG PATTERN:** Using `.slice(1)` to skip headers when reading Google Sheets data.

**How Google Sheets Node Handles Headers:**

When the Google Sheets node is configured with "Include Header Row" = `true` (default):
- The node **automatically excludes the header row** from the returned data
- You receive ONLY data rows, never the header row
- First item in the array is the FIRST DATA ROW, not the header

**The .slice(1) Anti-Pattern:**

```javascript
// ❌ WRONG - Skips first data row
const registryData = $('Read Client Registry').all();
const dataRows = registryData.slice(1);  // Thinking this skips header

// When sheet has: [Header, Data Row 1]
// Google Sheets returns: [Data Row 1]  (header already excluded)
// After .slice(1): []  (empty array - first data row was skipped!)
```

**Why This Fails Silently:**

When checking `registryRows.length === 1`:
```javascript
// ❌ WRONG - Misinterprets single data row as "only header"
if (registryRows.length === 0 || registryRows.length === 1) {
  // Wrongly assumes: "no data" or "only header row"
  return 'NEW';  // Creates duplicate entry!
}
const clientRow = registryRows.slice(1).find(row => {
  // This never executes when there's only 1 data row
});
```

**Real-World Bug Example:**

From "Check Client Exists" node (Eugene's Document Organizer):
```javascript
// BEFORE (BUGGY):
if (registryRows.length === 0 || registryRows.length === 1) {
  return [{ json: { ...normalizeData, client_status: 'NEW' } }];
}
const clientRow = registryRows.slice(1).find(row => {
  const clientName = row.json.Client_Name || '';
  const normalizedName = clientName
    .toLowerCase().trim()
    .replace(/[^a-z0-9]/g, '_');
  return normalizedName === clientNormalized;
});

// AFTER (FIXED):
if (registryRows.length === 0) {
  // Only return NEW if truly no data
  return [{ json: { ...normalizeData, client_status: 'NEW' } }];
}
// No .slice(1) needed - Google Sheets node already excluded headers
const clientRow = registryRows.find(row => {
  const clientName = row.json.Client_Name || '';
  const normalizedName = clientName
    .toLowerCase().trim()
    .replace(/[^a-z0-9]/g, '_');
  return normalizedName === clientNormalized;
});
```

**Impact of This Bug:**
- ✅ Sheet with 2+ data rows: Works (luck - enough rows to survive the skip)
- ❌ Sheet with 1 data row: FAILS SILENTLY (skips only data row, returns empty)
- Result: Duplicate client entries, duplicate folder creation, data corruption

**How to Identify This Pattern:**
1. Search for `.slice(1)` in Code nodes
2. Look for `registryRows.length === 1` or similar checks
3. Check if node is reading from Google Sheets with headers enabled

**Fix Checklist:**
- [ ] Remove all `.slice(1)` calls after Google Sheets reads
- [ ] Change `length === 1` checks to `length === 0`
- [ ] Add comment: "Note: Google Sheets node already excludes headers"
- [ ] Test with single-row sheet to verify fix

**Key Learning:** Google Sheets node with "Include Header Row" enabled automatically excludes headers from returned data. Using `.slice(1)` causes the first data row to be skipped, resulting in silent failures when only one data row exists.

---

## OAuth & Credentials

### Google Sheets OAuth Scopes

**❌ Insufficient scope (read-only):**
```
https://www.googleapis.com/auth/spreadsheets.readonly
```

**✅ Required scope for write operations:**
```
https://www.googleapis.com/auth/spreadsheets
```

**Key Learning:** Append Row, Update Row, and other write operations require full spreadsheets scope. Read-only scope causes "Unknown error" failures.

**After changing scopes:**
1. Update scope in Google Cloud Console
2. Reconnect credential in n8n (don't create new one)
3. Re-authenticate to get new token with updated scopes

---

## Execute Workflow Node

### Passing Parameters Between Workflows

**✅ CORRECT - Use workflowInputs:**
```javascript
{
  "workflowId": "zbxHkXOoD1qaz6OS",
  "workflowInputs": {
    "mappingMode": "defineBelow",
    "value": {
      "client_name": "={{ $json.client_name_raw }}",
      "client_normalized": "={{ $json.client_normalized }}",
      "parent_folder_id": "={{ $json.parent_folder_id }}"
    }
  }
}
```

**In called workflow - Access via Execute Workflow Trigger:**
```javascript
const inputData = $('Execute Workflow Trigger').first().json;
const clientName = inputData.client_name;
```

**Key Learning:** Execute Workflow node passes data via `workflowInputs.value` object, which becomes available in the called workflow's "Execute Workflow Trigger" node.

### Binary Data Passthrough Limitation

**CRITICAL LIMITATION:** Execute Workflow node may NOT reliably pass binary data to sub-workflows.

**❌ Problem Pattern:**
```
Parent Workflow:
  Gmail Trigger (binary data) → Execute Workflow node (passes binary + JSON)

Child Workflow:
  Execute Workflow Trigger receives: JSON ✓, Binary ✗ (MISSING)
```

**Evidence from testing:**
- Parent execution #244 had binary data in "Merge Binary + Metadata" node
- Child execution #248 received ONLY JSON metadata
- Binary data was completely missing: `binary: {}`

**✅ WORKAROUND - Upload binary first, pass file ID:**

**Parent Workflow:**
```javascript
// Step 1: Upload PDF to Drive
Gmail Trigger → Upload to Drive → Get file ID

// Step 2: Pass file ID to child workflow
{
  "workflowInputs": {
    "value": {
      "file_id": "={{ $json.file_id }}",
      "client_name": "={{ $json.client_name }}"
    }
  }
}
```

**Child Workflow:**
```javascript
// Step 1: Get parameters from parent
const fileId = $('Execute Workflow Trigger').first().json.file_id;

// Step 2: Download file from Drive using file ID
// Now child has binary data
```

**Key Learning:** Do NOT rely on Execute Workflow node to pass binary data. Upload binary to storage (Drive, S3, etc.) first, then pass storage file ID to sub-workflow for retrieval.

### Verifying Parent/Child Workflow Integration

**How to verify sub-workflow was actually called by parent (not triggered independently):**

**Check execution `mode` field:**
```javascript
// Parent-called execution:
{
  "mode": "workflow"  // ✓ Called by Execute Workflow node
}

// Independent execution:
{
  "mode": "trigger"   // ✗ Triggered by Gmail/Webhook (NOT parent)
}
```

**Evidence of broken integration:**
- Parent execution #180: Started at `2026-01-04T00:26:49.989Z`
- Child execution #182: Started at `2026-01-04T00:26:59.166Z` (9 seconds later)
- Child `mode`: **"trigger"** ← Child ran from Gmail, NOT from parent!

**Debugging checklist:**
1. Check child execution `mode` field (should be "workflow", not "trigger")
2. Verify child execution timestamp is DURING parent execution timeframe
3. Check if child has reference to parent workflow ID
4. Confirm parent's "Execute Workflow" node actually executed

**Key Learning:** When child workflow has BOTH Gmail Trigger AND Execute Workflow Trigger, Gmail can fire independently. This causes parallel execution with wrong parameters. DISABLE or DELETE Gmail Trigger in sub-workflows.

---

## Merge Node

### Binary Data Handling in Merge Operations

**CRITICAL ISSUE:** Merge node's `combineByPosition` mode may NOT preserve binary data from inputs.

**❌ Problem:**
```
Input 1: Filter PDF/ZIP Attachments (has binary data)
Input 2: Filter Staging Folder ID (has JSON metadata)
Merge node (combineByPosition): Result has JSON but NO binary
```

**Evidence from testing:**
- "Filter PDF/ZIP Attachments" output had binary: `binary.data.fileName: "OCP-Anfrage-AM10.pdf"`
- "Filter Staging Folder ID" output had metadata: `client_normalized: "villa_martens"`
- "Merge Binary + Metadata" showed 0 items executed

**Why it happens:**
- Merge node may prioritize JSON merging over binary preservation
- `combineByPosition` behavior with binary data is unpredictable
- Timing issues can cause merge to miss binary input

**✅ WORKAROUND - Use Code node instead of Merge:**
```javascript
// Get both inputs explicitly
const binaryItem = $('Filter PDF/ZIP Attachments').first();
const metadataItem = $('Filter Staging Folder ID').first();

return {
  json: {
    // Merge JSON metadata
    ...metadataItem.json,
    // Add any needed binary metadata
    hasAttachments: true,
    fileName: binaryItem.binary.data.fileName
  },
  binary: binaryItem.binary  // ✅ Explicitly preserve binary
};
```

**Testing checklist for Merge nodes:**
- [ ] Test with real binary data (not just JSON)
- [ ] Verify binary exists in merge output: `$json.binary`
- [ ] Check downstream nodes receive binary
- [ ] Consider using Code node for critical binary merges

**Key Learning:** Do NOT rely on Merge node to preserve binary data. Use Code node with explicit binary preservation for workflows that need binary + JSON merging.

---

## Common Debugging Patterns

### Gmail Trigger Binary Data

```javascript
// Gmail trigger stores attachments in item.binary
if (!item.binary) continue;

// Iterate over binary keys (attachment_0, attachment_1, etc.)
for (const [key, attachment] of Object.entries(item.binary)) {
  const filename = attachment.fileName;
  const mimeType = attachment.mimeType;
  const size = attachment.fileSize;
}
```

### Checking for Empty Data

```javascript
// ❌ WRONG - Doesn't handle empty sheets
const clientRow = registryRows.find(row => ...);

// ✅ CORRECT - Handle empty registry
if (registryRows.length === 0 || registryRows.length === 1) {
  // Empty (0 items) or only header row (1 item)
  return [{ json: { client_status: 'NEW' } }];
}

// Skip header row
const clientRow = registryRows.slice(1).find(row => ...);
```

### Debugging Workflow Execution Chains

**How to debug multi-workflow chains (parent → child relationships):**

**Step 1: Find parent execution**
```javascript
// Note parent execution ID and timestamps
Parent execution #180:
  Started: 2026-01-04T00:26:49.989Z
  Stopped: 2026-01-04T00:30:00.000Z
```

**Step 2: Search for child executions in same timeframe**
```javascript
// Child should start DURING parent execution window
Child execution #182:
  Started: 2026-01-04T00:26:59.166Z  // Within parent timeframe ✓
```

**Step 3: Verify execution mode**
```javascript
// Check if child was called by parent
{
  "mode": "workflow"  // ✓ Called by Execute Workflow node
}

// OR triggered independently (PROBLEM):
{
  "mode": "trigger"   // ✗ Triggered by Gmail/Webhook
}
```

**Step 4: Check for parent reference**
```javascript
// Child execution should reference parent workflow ID
// Look for parent workflow ID in execution metadata
```

**Common integration failures:**

**Failure Pattern 1: Child runs independently**
- Symptom: Child `mode: "trigger"`, not `"workflow"`
- Cause: Child has Gmail/Webhook Trigger still enabled
- Fix: DISABLE or DELETE trigger in child workflow

**Failure Pattern 2: Wrong parameters received**
- Symptom: Child receives empty/default values
- Cause: Parent's Execute Workflow node didn't run
- Fix: Verify parent execution path reaches Execute Workflow node

**Failure Pattern 3: Timing mismatch**
- Symptom: Child starts AFTER parent completes
- Cause: Delayed trigger firing, not workflow call
- Fix: Check child trigger configuration

**Key Learning:** When debugging workflow chains, ALWAYS verify child execution `mode` field first. If it says "trigger", the integration is broken and child is running independently.

---

## Testing Patterns

### Test Independence Design

**CRITICAL PRINCIPLE:** Tests should be self-contained, not depend on other tests.

**❌ Anti-pattern - Test dependencies:**
```
Test HP-01: Create client "Eugene Wei"
Test HP-02: Find existing client "Eugene Wei"  // Depends on HP-01 running first!

Problem: If HP-01 fails, HP-02 fails too
Problem: Can't run HP-02 in isolation
Problem: Test cleanup breaks subsequent tests
```

**✅ Best practice - Self-contained tests:**
```javascript
// Test scenario with setup/execute/cleanup phases
{
  "scenarioId": "HP-02",
  "name": "Find Existing Client - Idempotency Test",

  "setup": {
    // Create test data if it doesn't exist
    "createClient": {
      "name": "Eugene Wei",
      "email": "eugene@test.com"
    }
  },

  "execute": {
    // Run the actual test
    "operation": "findClient",
    "searchFor": "Eugene Wei"
  },

  "expected": {
    "clientFound": true,
    "folderCreated": false  // Already exists from setup
  },

  "cleanup": {
    // Remove test data after test
    "deleteClient": "Eugene Wei"
  }
}
```

**Test design checklist:**
- [ ] Test can run independently (doesn't require other tests)
- [ ] Test creates its own test data in setup phase
- [ ] Test cleans up its own data in cleanup phase
- [ ] Test has clear expected outcomes
- [ ] Test documents any dependencies explicitly

**When dependencies are unavoidable:**
```javascript
{
  "scenarioId": "HP-02",
  "dependsOn": ["HP-01"],  // Explicit dependency
  "failIfDependencyFailed": true,
  "skipIfDependencySkipped": true
}
```

**Key Learning:** Make tests independent with setup/execute/cleanup phases. Test dependencies cause cascading failures and make debugging difficult. If dependencies are necessary, document them explicitly and check prerequisite test status before running.

### Test Data Lifecycle Management

**Pattern 1: Isolated test data**
```javascript
// Each test creates unique identifiers
const testClientName = `Test_Client_${Date.now()}`;
const testEmail = `test_${Date.now()}@example.com`;

// Prevents test data collisions
```

**Pattern 2: Cleanup on failure**
```javascript
try {
  // Run test
  await executeTest();
} catch (error) {
  // Clean up even if test fails
  await cleanupTestData();
  throw error;
}
```

**Pattern 3: Shared fixtures (use sparingly)**
```javascript
// Only for read-only data that never changes
const SHARED_FIXTURES = {
  testCountry: "Germany",
  testCurrency: "EUR"
};
// NEVER modify shared fixtures during tests
```

**Key Learning:** Each test should manage its own data lifecycle. Use unique identifiers to prevent test collisions. Clean up even when tests fail.

---

## Advanced Patterns and Common Pitfalls

### Zero-Item Execution Blocking (CRITICAL)

**CRITICAL n8n BEHAVIOR:** When a node returns 0 items, ALL downstream nodes are automatically skipped.

**❌ Problem Pattern:**
```
Google Sheets lookup → 0 rows returned
↓
Code node with empty-handling logic → NEVER EXECUTES
↓
Decision Gate → NEVER EXECUTES
↓
All downstream workflows → NEVER EXECUTE
```

**Why this is critical:**
- Even if Code node has logic to handle `registryRows.length === 0`
- Even if Code node would return default values
- **The Code node NEVER RUNS because it received 0 inputs**

**Real-world example:**
```javascript
// This code exists in "Check Client Exists" node:
if (registryRows.length === 0) {
  return [{ json: { client_status: 'NEW' } }];
}

// But if "Lookup Client Registry" returns 0 items, this code NEVER EXECUTES
// Result: Entire workflow stops silently
```

**Evidence from testing:**
- Execution #262: "Lookup Client Registry" returned 0 items
- "Check Client Exists" node: NOT EXECUTED (0 items in execution log)
- All downstream nodes: NOT EXECUTED
- Workflow status: "success" (no errors, just stopped)

**✅ SOLUTION 1 - Always return at least 1 item (Recommended):**

**Modify upstream node to guarantee 1+ items:**
```javascript
// In Code node AFTER Google Sheets lookup
const registryRows = $input.all();

if (registryRows.length === 0) {
  // Return dummy header row to ensure downstream execution
  return [{
    json: {
      Client_Name: 'HEADER',
      Root_Folder_ID: '',
      Intake_Folder_ID: '',
      _isEmpty: true  // Flag to identify dummy row
    }
  }];
}

return registryRows;
```

**✅ SOLUTION 2 - Use IF node with "Continue On Fail":**
```
Google Sheets lookup → IF node (check length) → Code node
  ├─ If items > 0 → Process normally
  └─ If items = 0 → Generate default item
```

**✅ SOLUTION 3 - Change data flow:**
```
Instead of: Sheets lookup → Code node (gets 0 items)
Use:        Code node → Sheets lookup (code always runs)
            Code node manually calls $('Sheets Lookup').all()
```

**Prevention checklist:**
- [ ] Identify nodes that can return 0 items (Sheets lookups, filters, etc.)
- [ ] Add Code node AFTER to ensure at least 1 item passes through
- [ ] Test workflows with empty data sources
- [ ] Don't rely on downstream Code nodes to handle empty cases

**Key Learning:** In n8n, handling empty data means ensuring 0 items NEVER propagate. Add Code nodes to convert "0 items" to "1 item with empty flag" immediately after operations that can return 0 items.

---

### n8n Expression Syntax in JSON Parameters

**CRITICAL RULE:** n8n validates JSON syntax BEFORE evaluating expressions.

**Problem:** Embedding expressions directly in JSON parameters fails validation because expressions use syntax that isn't valid JSON.

**❌ WRONG - Embedding expressions in HTTP Request jsonBody:**
```javascript
// This configuration will FAIL with "JSON parameter needs to be valid JSON"
{
  "parameters": {
    "jsonBody": {
      "model": "claude-3-5-sonnet-20241022",
      "messages": [{
        "role": "user",
        "content": [{
          "type": "image",
          "source": {
            "type": "base64",
            "media_type": "application/pdf",
            "data": $binary.data.toBase64()  // ❌ Unquoted identifier = invalid JSON
          }
        }]
      }]
    }
  }
}
```

**Error Message:** "JSON parameter needs to be valid JSON"

**Why it fails:** `$binary` is an unquoted identifier, which is invalid JSON syntax. n8n validates the JSON structure before it evaluates the expression.

**✅ CORRECT - Build in Code node, reference from HTTP Request:**

**Step 1: Code Node "Build API Request"**
```javascript
const binaryData = $input.first().binary.data;
const base64Data = binaryData.toBase64();

const requestBody = {
  model: "claude-3-5-sonnet-20241022",
  max_tokens: 4096,
  messages: [{
    role: "user",
    content: [
      {
        type: "text",
        text: "Your parsing instructions here..."
      },
      {
        type: "image",
        source: {
          type: "base64",
          media_type: "application/pdf",
          data: base64Data  // ✅ Valid JavaScript variable
        }
      }
    ]
  }]
};

return {
  json: {
    requestBody: requestBody,
    // Pass through other data
    ...($input.first().json)
  },
  binary: $input.first().binary
};
```

**Step 2: HTTP Request Node**
```javascript
{
  "jsonBody": "={{ $json.requestBody }}"  // ✅ References pre-built object
}
```

**Key Learning:** When your JSON body needs expressions or complex logic, build the entire structure in a Code node first, then reference it as `={{ $json.fieldName }}` in the HTTP Request node. Do NOT embed expressions directly in static JSON parameters.

**When to use this pattern:**
- Complex nested JSON structures with dynamic values
- Binary data conversion (toBase64, etc.)
- Conditional logic in request body
- Combining data from multiple sources

---

### Binary Data toBase64() Method

**Binary data in n8n is stored as "filesystem-v2" references internally. To convert to base64:**

**✅ CORRECT - Call toBase64() method:**
```javascript
const binaryData = $input.first().binary.data;
const base64String = binaryData.toBase64();

// Use in request body
const requestBody = {
  file_content: base64String
};
```

**❌ WRONG - Property doesn't exist:**
```javascript
const base64String = $binary.data.data;  // ❌ Property 'data' doesn't exist
const base64String = $binary.data;       // ❌ Returns object reference, not string
```

**Key Learning:** Binary data objects have a `.toBase64()` method that returns the base64-encoded string. Do not try to access `.data.data` or assume the binary object itself is a string.

**Common use cases:**
- API requests requiring base64-encoded files (Anthropic, OpenAI, etc.)
- Embedding images in JSON
- File content manipulation

---

### HTTP Request Node - Anthropic API Integration

**Complete working pattern for Anthropic Claude API with PDF vision parsing:**

**Authentication Setup:**
- Node Credential Type: `anthropicApi` (predefined in n8n)
- API key stored in credential manager

**Required Configuration:**

**Headers:**
```javascript
{
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [{
      "name": "anthropic-version",
      "value": "2023-06-01"
    }]
  }
}
```

**Request Body (built in preceding Code node):**
```javascript
// Code node: "Build Anthropic API Request"
const binaryData = $input.first().binary.data;
const base64Data = binaryData.toBase64();

const requestBody = {
  model: "claude-3-5-sonnet-20241022",
  max_tokens: 4096,
  messages: [
    {
      role: "user",
      content: [
        {
          type: "text",
          text: "Extract all transactions from this bank statement..."
        },
        {
          type: "image",
          source: {
            type: "base64",
            media_type: "application/pdf",  // or "image/png", "image/jpeg"
            data: base64Data
          }
        }
      ]
    }
  ]
};

return {
  json: { requestBody: requestBody }
};
```

**HTTP Request Node Configuration:**
```javascript
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "anthropicApi",
  "sendHeaders": true,
  "sendBody": true,
  "specifyBody": "json",
  "jsonBody": "={{ $json.requestBody }}"
}
```

**Response Format:**
```javascript
// Parse Anthropic response in Code node
const response = $input.first().json;
const textContent = response.content[0].text;  // Anthropic format

// Parse JSON from text if needed
const parsedData = JSON.parse(textContent);
```

**Key Learning:**
- Anthropic API requires `anthropic-version` header (currently "2023-06-01")
- Response is in `response.content[0].text` (different from OpenAI's `response.choices[0].message.content`)
- Always build complex request bodies in Code nodes for Anthropic's nested structure

---

### Google Drive Trigger - Event Types and Polling Behavior

**Understanding Trigger Event Types:**

**1. `fileCreated` Event:**
- Only fires when NEW files are created directly in the folder
- Will NOT fire for files moved into folder from another location
- Will NOT fire for files copied into folder
- Will NOT fire for existing files

**2. `fileUpdated` Event:**
- Fires when files are modified
- Fires when files are moved into folder (recommended for intake workflows)
- Fires when files are copied if copy operation updates modification timestamp
- More flexible for detecting "new" files regardless of how they arrived

**Polling Behavior:**

**Critical Understanding:**
- Trigger uses `lastTimeChecked` timestamp to track when it last polled
- Polls at configured interval (e.g., "everyMinute")
- **Only detects changes AFTER trigger activation**
- Files already present in folder BEFORE trigger starts watching won't fire executions

**❌ Common Mistake:**
```
Timeline:
1. 11:00 PM - Upload test PDFs to Bank-Statements folder
2. 11:30 PM - Activate workflow with fileUpdated trigger
3. Wait for execution...
4. ❌ No execution fires - files were there BEFORE trigger started
```

**✅ Correct Approach:**
```
Timeline:
1. 11:00 PM - Activate workflow with fileUpdated trigger
2. 11:01 PM - Trigger starts polling (lastTimeChecked set)
3. 11:02 PM - Upload/move test PDF into folder
4. 11:03 PM - ✅ Execution fires - file change detected after activation
```

**Workarounds for Testing:**

**Option A: Move file to trigger update event**
1. Move file OUT of watched folder
2. Wait 5 seconds
3. Move file BACK into watched folder
4. Creates "fileUpdated" event that trigger will detect

**Option B: Manual execution**
1. Use "Test workflow" button in n8n UI
2. Manually trigger with existing files
3. Tests workflow logic without relying on trigger

**Recommendation:**
- Use `fileUpdated` for intake workflows (detects moved/copied files)
- Use `fileCreated` only when you need strict "newly created only" behavior
- Always upload test files AFTER activating trigger

**Key Learning:** Google Drive polling triggers only detect changes that occur AFTER `lastTimeChecked` timestamp. Pre-existing files won't trigger executions. For testing, either use manual execution or ensure files are added AFTER trigger activation.

---

### Code Node Best Practices for Complex JSON

**When to use Code nodes instead of direct JSON parameters:**

**Use Code nodes when:**
1. Building JSON with expressions that would fail validation
2. Constructing complex nested objects
3. Need to call methods on objects (`.toBase64()`, `.toLowerCase()`, etc.)
4. Combining data from multiple sources into one request body
5. Conditional logic in request structure
6. Transforming binary data

**Recommended Pattern:**
```
Data Source → Code Node (build complex JSON) → HTTP Request/Target Node (reference JSON)
```

**Example: Complex API Request**

**Code Node: "Build API Request"**
```javascript
const fileData = $input.first();
const base64 = fileData.binary.data.toBase64();
const metadata = fileData.json;

// Build complex request body with conditional logic
const requestBody = {
  model: metadata.useGPT4 ? "gpt-4" : "gpt-3.5-turbo",
  messages: [
    {
      role: "system",
      content: "You are a helpful assistant."
    },
    {
      role: "user",
      content: [
        { type: "text", text: metadata.instructions },
        {
          type: "image_url",
          image_url: {
            url: `data:${metadata.mimeType};base64,${base64}`
          }
        }
      ]
    }
  ],
  max_tokens: metadata.maxTokens || 1000
};

return {
  json: {
    requestBody: requestBody,
    // Pass through tracking fields
    fileName: metadata.name,
    fileId: metadata.id,
    timestamp: new Date().toISOString()
  },
  binary: fileData.binary
};
```

**HTTP Request Node:**
```javascript
{
  "jsonBody": "={{ $json.requestBody }}"
}
```

**Benefits:**
- ✅ JavaScript validation (not JSON validation)
- ✅ Can call methods and use variables
- ✅ Easy to debug with console.log
- ✅ Can handle complex conditional logic
- ✅ Clear separation: logic in Code, execution in HTTP Request

**Key Learning:** Don't fight n8n's JSON validation. Build complex structures in Code nodes where JavaScript rules apply, then reference them in nodes where JSON validation happens. This makes workflows more maintainable and avoids cryptic validation errors.

---

### HTTP Request Node - Expression Wrapping in jsonBody

**Understanding jsonBody parameter behavior:**

**✅ CORRECT - Two valid approaches:**

**Approach 1: Completely static JSON (no expressions)**
```javascript
{
  "jsonBody": {
    "model": "gpt-4",
    "temperature": 0.7,
    "messages": [{"role": "user", "content": "Hello"}]
  }
}
```

**Approach 2: Single expression wrapped in quotes**
```javascript
{
  "jsonBody": "={{ $json.requestBody }}"  // Entire body is one expression
}
```

**❌ WRONG - Cannot mix static JSON with embedded expressions:**

```javascript
{
  "jsonBody": {
    "model": "gpt-4",
    "messages": $json.messages,  // ❌ Can't embed expression in static JSON
    "temperature": 0.7
  }
}
```

```javascript
{
  "jsonBody": {
    "model": "={{ $json.model }}",  // ❌ Invalid - expression inside static JSON
    "messages": [{"role": "user", "content": "={{ $json.prompt }}"}]
  }
}
```

**Why it fails:**
- n8n validates the parameter as JSON first
- Embedded expressions break JSON syntax
- Parser sees `$json.messages` as invalid JSON (not a string, number, object, or array)

**Solution:**
If you need ANY dynamic values, build the ENTIRE body in a Code node:

```javascript
// Code node
return {
  json: {
    requestBody: {
      model: "gpt-4",
      messages: $json.messages,  // ✅ Valid in JavaScript
      temperature: 0.7
    }
  }
};
```

Then reference it:
```javascript
// HTTP Request node
{
  "jsonBody": "={{ $json.requestBody }}"
}
```

**Key Learning:** The `jsonBody` parameter is all-or-nothing:
- Either completely static JSON (no expressions)
- OR a single expression: `"={{ expression }}"` that returns the entire body
- You CANNOT partially embed expressions in static JSON structure

This applies to all n8n nodes with JSON parameters (HTTP Request, Webhook, etc.).

---

## Client Registry Data Hygiene Patterns

### Test Data Cleanup is Critical

**Context:** Eugene AMA Document Organizer - UNKNOWN client handling (Jan 5, 2026)

**Problem:** Test executions left 14 corrupted entries in Client_Registry with "n_a" values from timestamp parsing failures. These entries caused routing logic to incorrectly match UNKNOWN clients to EXISTING path.

**Root Cause:** Complex timestamp-based naming ("UNKNOWN_2026-01-05_1141") created parsing opportunities for errors during test iterations.

**Solution Patterns:**

#### 1. Simple Static Naming for UNKNOWN Clients

❌ **Complex (caused issues):**
```javascript
const timestamp = now.toISOString().replace(/:/g, '').replace(/\..+/, '').replace('T', '_').substring(0, 15);
const clientName = `UNKNOWN_${timestamp}`;  // Results: "UNKNOWN_2026-01-05_1141"
```

✅ **Simple (works reliably):**
```javascript
const clientName = "UNKNOWN_CLIENT";  // Static, no parsing needed
```

**Why:** User will rename the folder after identifying the client anyway. Uniqueness is not required. Simplicity prevents parsing errors.

#### 2. Status Field for Client Type Distinction

Instead of text pattern matching, use dedicated status field:

```javascript
// In "Prepare Registry Entry" node
const isUnknownClient = clientNameRaw.startsWith('UNKNOWN_');
const clientStatus = isUnknownClient ? 'PENDING_IDENTIFICATION' : 'ACTIVE';

return {
  json: {
    Client_Name: clientNameRaw,
    Root_Folder_ID: rootFolderId,
    Staging_Folder_ID: stagingFolderId,
    Date_Created: new Date().toISOString(),
    status: clientStatus  // ✅ Makes cleanup queries easy
  }
};
```

**Benefits:**
- Future cleanup: `WHERE status = 'PENDING_IDENTIFICATION'`
- No regex needed: `WHERE status != 'ACTIVE'`
- Clear visual distinction in spreadsheet
- Extensible: Can add other statuses like 'ARCHIVED', 'INACTIVE'

#### 3. Test Data Cleanup Pattern

When cleaning test entries from Google Sheets registry:

```javascript
// Use mcp__google-sheets__edit_row to clear specific rows
// Clear rows 2-15 (14 corrupted test entries)
for (let rowIndex = 2; rowIndex <= 15; rowIndex++) {
  mcp__google-sheets__edit_row({
    spreadsheetId: "1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI",
    rowIndex: rowIndex,
    values: ["", "", "", "", "", ""]  // Empty strings for all columns
  });
}
```

**Pro Tip:** Before bulk cleanup, export sheet as CSV backup:
```bash
# Via Google Sheets UI: File > Download > CSV
# Or via MCP: read entire sheet and save locally
```

#### 4. Three-Path Decision Routing

Eugene workflow uses three output paths from Decision Gate:

**Decision Logic:**
```javascript
// IF node or Decision Gate
Output 0: client_normalized is empty → UNKNOWN path
Output 1: client is NEW (not in registry) → NEW path
Output 2: client EXISTING (in registry) → EXISTING path
```

**Implementation in IF node:**
```javascript
{
  "conditions": {
    "options": {
      "routing": {
        "mode": "rules",
        "rules": [
          {
            // Rule 1: UNKNOWN (client_normalized is empty)
            "conditions": {
              "all": [{
                "leftValue": "={{ $json.client_normalized }}",
                "operator": "isEmpty"
              }]
            },
            "outputIndex": 0  // → UNKNOWN path
          },
          {
            // Rule 2: NEW (client not in registry)
            "conditions": {
              "all": [{
                "leftValue": "={{ $json.isNewClient }}",
                "operator": "equal",
                "rightValue": true
              }]
            },
            "outputIndex": 1  // → NEW path
          }
        ]
      },
      "defaultOutput": 2  // → EXISTING path (fallback)
    }
  }
}
```

**Benefits:**
- No orphaned documents (every path handled)
- Email notifications for manual review on UNKNOWN path
- Clear separation of NEW vs EXISTING client logic
- Fallback default prevents execution failures

**Key Learning:** Clean test data before production testing. Corrupted entries from development iterations will cause false failures in routing logic even when core system works perfectly.

---

**Last Updated:** 2026-01-05
**Version:** 1.3 - Added Client Registry Data Hygiene Patterns section: test data cleanup, static naming for UNKNOWN clients, status field patterns, three-path decision routing
