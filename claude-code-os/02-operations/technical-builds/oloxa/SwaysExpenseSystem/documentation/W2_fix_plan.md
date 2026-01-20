# W2 v2.1 Fix Plan - Detailed Analysis

## Issues Identified from Screenshots & Workflow Data

### 1. Continue On Fail Conflicts (3 nodes)

**The Problem**: These 3 nodes have BOTH `continueOnFail: false` AND `onError: "continueRegularOutput"` properties, which n8n validation rejects as mutually exclusive.

**Affected Nodes:**

1. **"Build Vision API Request"**
   - Node ID: `build-vision-api-request`
   - Location: Position [1720, -112] (after "Merge Apple & Regular Receipts")
   - Current config: Has `continueOnFail: false` + `onError: "continueRegularOutput"`
   - Fix: Remove `continueOnFail` property entirely

2. **"Extract Text with Vision API"**
   - Node ID: `ocr-vision-api-node`
   - Location: Position [1900, -112] (after "Build Vision API Request")
   - Current config: Has `continueOnFail: false` + `onError: "continueRegularOutput"`
   - Fix: Remove `continueOnFail` property entirely

3. **"Parse Amount from OCR Text"**
   - Node ID: `parse-amount-from-ocr`
   - Location: Position [2080, -112] (after "Extract Text with Vision API")
   - Current config: Has `continueOnFail: false` + `onError: "continueRegularOutput"`
   - Fix: Remove `continueOnFail` property entirely

**Why MCP Tool Can't Fix**: The n8n MCP `n8n_update_partial_workflow` tool can UPDATE property values but cannot REMOVE properties. Setting `continueOnFail: undefined` or using `removeProperties` doesn't work.

**Manual Fix Steps** (Sway to perform in n8n UI):
```
For each of the 3 nodes above:
1. Click on the node to open its settings
2. Look for "Settings" tab or "Continue On Fail" toggle
3. If you see a "Continue On Fail" toggle, turn it OFF
4. Keep "On Error" setting as "Continue Regular Output"
5. Save the node

Alternative if toggle not visible:
1. Click "..." menu on node → "Settings"
2. Under "Error Handling", disable "Continue On Fail"
3. Keep "On Error" dropdown as "Continue Regular Output"
```

---

### 2. Google Vision API Service Account Issue (CRITICAL)

**The Problem**: The "Extract Text with Vision API" node is configured to use "Google Service Account API" credential, which you're no longer using. The screenshot shows:
- Authentication: "Predefined Credential Type"
- Credential Type: "Google Service Account API"
- Google Service Account API: "Select Credential" (red error - no credential selected)

**Current Configuration:**
```json
{
  "name": "Extract Text with Vision API",
  "type": "n8n-nodes-base.httpRequest",
  "parameters": {
    "method": "POST",
    "url": "https://vision.googleapis.com/v1/images:annotate",
    "authentication": "predefinedCredentialType",
    "nodeCredentialType": "googleApi"
  }
}
```

**What Needs to Change:**
The node needs to use OAuth2 Google API credentials instead of Service Account.

**Fix Options:**

**Option A: Use OAuth2 Google API (Recommended)**
1. Change authentication to use existing Google OAuth2 credential
2. This matches the pattern used by Gmail/Drive/Sheets nodes
3. Requires creating a "Google Cloud API" OAuth2 credential in n8n

**Option B: Use HTTP Request with Bearer Token**
1. Get OAuth2 access token from Gmail/Drive credential
2. Use that token in Authorization header
3. More complex, not recommended

**Manual Fix Steps** (Sway to perform in n8n UI):
```
1. Open "Extract Text with Vision API" node
2. Under "Authentication", keep "Predefined Credential Type"
3. Under "Credential Type", keep "Google API" (or select "Google Cloud API")
4. Under "Google API" dropdown, click "Create New Credential"
5. Follow OAuth2 flow to connect your Google account
6. Ensure the credential has "Cloud Vision API" scope enabled
7. Save the credential and select it in the node
8. Test the node to verify it works
```

**Alternative if you have existing Google Cloud API credential:**
```
1. Open "Extract Text with Vision API" node
2. Under "Google Service Account API" dropdown
3. Select your existing Google Cloud OAuth2 credential
4. Save
```

---

### 3. Service Account Audit Across All Workflows

**Workflows to Check:**
- W1: Bank Statement Monitor
- W2: Gmail Receipt Monitor (this one)
- W3: Transaction-Receipt-Invoice Matching
- W4: Monthly Folder Builder
- W6: Expensify PDF Parser

**What to Look For:**
- Any node using "Google Service Account API" credential type
- Any HTTP Request nodes calling Google APIs with service account auth
- Any credentials named "service account" or similar

**Expected Result:**
- All Google integrations should use OAuth2 credentials:
  - Gmail: `gmailOAuth2`
  - Google Drive: `googleDriveOAuth2Api`
  - Google Sheets: `googleSheetsOAuth2Api`
  - Google Cloud Vision: `googleApi` (OAuth2)

---

## W4 Validation False Positives (CONFIRMED)

Based on your screenshots, both Update nodes are correctly configured:

**"Update Statements FilePath":**
- ✅ Mapping Column Mode: "Map Automatically"
- ✅ Column to match on: "StatementID"
- ✅ Sheet: "Statements"

**"Update Receipts FilePath":**
- ✅ Mapping Column Mode: "Map Automatically"
- ✅ Column to match on: "ReceiptID"
- ✅ Sheet: "Receipts"

**Conclusion**: The 2 validation errors are false positives. The validator doesn't recognize that "Map Automatically" mode pulls values from incoming data. **No fix needed for W4.**

---

## Summary of Actions Required

### Sway's Manual Fixes:

**W2 - Continue On Fail (3 nodes):**
1. Build Vision API Request - disable "Continue On Fail"
2. Extract Text with Vision API - disable "Continue On Fail"
3. Parse Amount from OCR Text - disable "Continue On Fail"

**W2 - Vision API Authentication (1 node):**
4. Extract Text with Vision API - change from Service Account to OAuth2 Google API credential

**Service Account Audit (all workflows):**
5. Check W1, W3, W4, W6 for any Service Account usage
6. Replace with OAuth2 credentials if found

### After Manual Fixes:

**Claude Actions:**
1. Re-test W2 with test-runner-agent
2. Re-audit all workflows for service account usage
3. Generate final test report
4. Activate validated workflows

---

## Testing After Fixes

Once manual fixes are complete:

```bash
# Test W2 specifically
test-runner-agent: Test W2 v2.1 validation

# Full system test
test-runner-agent: Test all 4 expense system workflows
```

**Expected Results After Fixes:**
- W2: 0 validation errors (all 5 fixed)
- W3: 0 validation errors ✅ (already validated)
- W4: 2 false positive warnings (ignore) ✅
- W6: 0 validation errors ✅ (already validated)

---

## Node Location Reference for Sway

**W2 Workflow Canvas - Node Positions:**

The 3 nodes with Continue On Fail issues are in the **bottom-right section** of the workflow:

```
[After Apple/Regular merge] → Build Vision API Request → Extract Text with Vision API → Parse Amount from OCR Text → Prepare Receipt Record
                              ^^^^^^^^^^^^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^^^^^^^^^^^
                              FIX 1                      FIX 2 (also auth issue)         FIX 3
                              Position: [1720, -112]     Position: [1900, -112]          Position: [2080, -112]
```

All 3 nodes are in a horizontal line at Y-coordinate -112, processing OCR text extraction.
