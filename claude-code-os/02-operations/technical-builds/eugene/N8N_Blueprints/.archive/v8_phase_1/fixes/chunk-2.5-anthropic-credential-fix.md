# Chunk 2.5 Anthropic Credential Fix

**Date:** 2026-01-18
**Agent:** solution-builder-agent
**Workflow:** Chunk 2.5 - Client Document Tracking (ID: okg8wTqLtPUwjQ18)

---

## Problem

Chunk 2.5 workflow was failing with credential error:
```
"Credential with ID 'anthropic-api-key' does not exist for type 'anthropicApi'"
```

This error occurred in both Claude Vision nodes:
- Claude Vision Tier 1 Classification (http-claude-tier1)
- Claude Vision Tier 2 Classification (http-claude-tier2)

---

## Root Cause

The Claude Vision nodes in Chunk 2.5 were configured with **incorrect credential type**:

**Broken configuration:**
```json
{
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "anthropicApi",
  "credentials": {
    "anthropicApi": {
      "id": "anthropic-api-key",  // This ID doesn't exist
      "name": "Anthropic API Key"
    }
  }
}
```

**Working configuration (from Pre-Chunk 0):**
```json
{
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "credentials": {
    "httpHeaderAuth": {
      "id": "vfoYopBRX35Znmq6",  // Actual credential ID
      "name": "Anthropic API key"
    }
  }
}
```

---

## Solution Applied

Updated both Claude Vision nodes to use the same credential configuration as Pre-Chunk 0's working "Claude Vision Extract Identifier" node.

**Changes:**
1. Changed `authentication` from `"predefinedCredentialType"` to `"genericCredentialType"`
2. Added `genericAuthType: "httpHeaderAuth"`
3. Updated `credentials` to use `httpHeaderAuth` with correct credential ID
4. Added `Content-Type: application/json` header to match Pre-Chunk 0

**MCP Operation:**
```javascript
mcp__n8n-mcp__n8n_update_partial_workflow({
  id: "okg8wTqLtPUwjQ18",
  operations: [
    {
      type: "updateNode",
      nodeId: "http-claude-tier1",
      updates: {
        parameters: {
          authentication: "genericCredentialType",
          genericAuthType: "httpHeaderAuth",
          headerParameters: {
            parameters: [
              { name: "anthropic-version", value: "2023-06-01" },
              { name: "Content-Type", value: "application/json" }
            ]
          },
          credentials: {
            httpHeaderAuth: {
              id: "vfoYopBRX35Znmq6",
              name: "Anthropic API key"
            }
          }
        }
      }
    },
    // Same for http-claude-tier2
  ]
})
```

---

## Validation Results

**Before fix:**
- ❌ Error: Credential with ID 'anthropic-api-key' does not exist
- ❌ Workflow could not execute Claude Vision classification

**After fix:**
- ✅ Both Claude Vision nodes now use correct credential (vfoYopBRX35Znmq6)
- ✅ Authentication changed to genericCredentialType + httpHeaderAuth
- ✅ Matches working Pre-Chunk 0 configuration
- ⚠️ Remaining workflow validation warnings unrelated to credentials (Gmail operation, typeVersions)

**Validation output:**
```
Workflow valid: false (due to unrelated Gmail node issue)
Error count: 1 (Gmail node only - not credential related)
Warning count: 47 (mostly best practices - code error handling, typeVersion upgrades)
```

---

## Testing Recommendations

1. **Manual test in n8n UI:**
   - Trigger Chunk 2.5 with a test PDF
   - Verify Claude Vision Tier 1 Classification executes successfully
   - Verify Claude Vision Tier 2 Classification executes successfully
   - Check that document classification results are correct

2. **End-to-end test:**
   - Run Pre-Chunk 0 → Chunk 2.5 flow with a real email
   - Confirm both workflows complete without credential errors
   - Verify PDF is classified and moved to correct folder

---

## Related Workflows

**Confirmed working with same credential:**
- Pre-Chunk 0 (YGXWjWcBIk66ArvT) - "Claude Vision Extract Identifier" node
  - Uses credential ID: vfoYopBRX35Znmq6
  - Authentication: genericCredentialType + httpHeaderAuth

**Now fixed:**
- Chunk 2.5 (okg8wTqLtPUwjQ18) - Both Claude Vision nodes
  - Updated to use credential ID: vfoYopBRX35Znmq6
  - Authentication: genericCredentialType + httpHeaderAuth

---

## Notes

- The credential name is "Anthropic API key" (lowercase 'key') not "Anthropic API Key" (uppercase)
- The credential type must be `httpHeaderAuth`, not `anthropicApi`
- Pre-Chunk 0 was used as the reference because it's confirmed working in production
- This fix only addresses the credential error - other validation warnings remain (non-critical)
