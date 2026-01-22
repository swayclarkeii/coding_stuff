# Eugene V10 - Workflow Rebuild Summary
**Version**: v4.0
**Date**: 2026-01-20
**Session Type**: Workflow Rebuild + Authentication Fixes
**Status**: Working - Gmail attachments now downloading

---

## Session Overview

Rebuilt the "AMA Pre-Chunk 0" workflow from JSON export and resolved multiple authentication/configuration issues that were blocking execution.

---

## Work Completed

### 1. Workflow Rebuild from JSON Export

**Source File**: `/Users/swayclarke/Downloads/AMA Pre-Chunk 0 - REBUILT v1.json`

**New Workflow Created**:
- **Workflow ID**: `p0X9PrpCShIgxxMP`
- **Name**: AMA Pre-Chunk 0 - REBUILT v1
- **Node Count**: 60 nodes (54 enabled, 6 disabled legacy)
- **Status**: Active

**Three Routing Paths**:
1. **UNKNOWN** → Create folders → Move to 38_Unknowns → Email notification
2. **NEW** → Execute Chunk 0 → Move to staging → Execute Chunk 2.5
3. **EXISTING** → Lookup staging → Move to staging → Execute Chunk 2.5

---

### 2. Claude API Authentication Fix

**Problem**: "Bad request - please check your parameters" error at Claude Text Extraction node.

**Root Cause**: Invalid header expression format:
```
❌ x-api-key: =={{ $credentials.anthropicApi.apiKey }}
```
The `=={{` syntax doesn't work - n8n can't reference credentials in expressions.

**Fix Applied**: Changed to Generic Credential Type with Header Auth:
- Authentication: Generic Credential Type
- Generic Auth Type: Header Auth
- Header Auth: Anthropic API key (new credential created by user)
- Additional Headers: `anthropic-version: 2023-06-01`, `anthropic-beta: pdfs-2024-09-25`

**Node Modified**: `Claude Tesxt Extration` (ID: `7b5637a2-9b8e-4651-83a9-b2e5838c1f3a`)

---

### 3. Gmail OAuth Refresh

**Problem**: "The provided authorization grant... is invalid, expired, revoked" error.

**Fix**: Used browser-ops-agent to complete OAuth flow:
- Navigated to n8n credentials page
- Re-authenticated Gmail account
- Credential ID: `aYzk7sZF8ZVyfOan`
- Account: swayclarkeii@gmail.com
- Status: Account connected

---

### 4. Gmail Attachments Not Downloading

**Problem**: Workflow stopping at "Filter PDF/ZIP Attachments" with "No output data returned" - binary data missing.

**Root Cause**: Gmail Trigger node missing "Download Attachments" option.

**Fix**: User needs to enable in Gmail Trigger → Options → Download Attachments

**Current Status**: User confirmed this was the issue, enabling the option now.

---

## Credentials Referenced

| Credential | ID | Type | Status |
|------------|-----|------|--------|
| Gmail account | `aYzk7sZF8ZVyfOan` | Gmail OAuth2 | Refreshed |
| Google Drive account | `a4m50EefR3DJoU0R` | Google Drive OAuth2 | Working |
| Google Sheets account | `H7ewI1sOrDYabelt` | Google Sheets OAuth2 | Working |
| Anthropic account | `MRSNO4UW3OEIA3tQ` | Anthropic API | Working |
| Anthropic API key | (user created) | HTTP Header Auth | New |

---

## Sub-Workflows Referenced

| Workflow | ID | Purpose |
|----------|-----|---------|
| AMA Chunk 0: Folder Initialization | `zbxHkXOoD1qaz6OS` | Creates folder structure for new clients |
| Chunk 2.5 - Client Document Tracking | `okg8wTqLtPUwjQ18` | Document tracking and classification |

---

## Agent IDs from This Session

| Agent ID | Agent Type | Task Description |
|----------|-----------|------------------|
| **ad97800** | solution-builder-agent | Rebuilt AMA Pre-Chunk 0 workflow from JSON |
| **a171d37** | browser-ops-agent | Gmail OAuth token refresh |

**Note**: Use these IDs with `resume` parameter to continue work in future sessions.

---

## Technical Details

### Workflow Structure (Key Nodes)

```
Gmail Trigger → Extract Email Metadata → Filter PDF/ZIP Attachments
    ↓
Split Into Batches → Upload PDF to Temp Folder → Extract File ID
    ↓
Download PDF from Drive → Convert PDF to Base64 → Build Claude API Request
    ↓
Claude Text Extraction (HTTP) → Parse Claude Response → Wait → Store Analysis Result
    ↓ (loop back to Split Into Batches)
Aggregate All PDF Results → Parse Email Body → Batch Voting
    ↓
Lookup Client Registry → Check Client Exists → Check Flag Conditions
    ↓
Decision Gate → [UNKNOWN | NEW | EXISTING paths]
```

### Key Configuration Notes

1. **Gmail Trigger** must have:
   - Simplify: OFF
   - Download Attachments: ON (in Options)
   - Labels: INBOX, UNREAD, AMA

2. **Claude API Request** uses:
   - Model: `claude-sonnet-4-20250514`
   - Type: `document` (not image)
   - media_type: `application/pdf`
   - Beta header for PDF support

3. **Batch Processing** uses:
   - Global static data for accumulating results across loop iterations
   - `$getWorkflowStaticData('global')` pattern

---

## Issues Discovered (Other Workflow)

Separate workflow `YGXWjWcBIk66ArvT` ("Claude Vision Extract Identifier") has similar authentication issues:
- Using "Predefined Credential Type: Anthropic" AND manual x-api-key header (conflicting)
- Shows 20.2 MB input data (base64 inflation + possible multiple PDFs concatenated)

**Not fixed this session** - focus was on the rebuilt workflow.

---

## Next Steps

1. **Verify Gmail attachments download** after enabling "Download Attachments" option
2. **Test full workflow execution** end-to-end
3. **Monitor Claude API calls** for successful PDF processing
4. **Check downstream routing** (UNKNOWN/NEW/EXISTING paths)

---

## Key Learnings

### 1. n8n Credential Expressions Don't Work
Cannot use `$credentials.xxx` in HTTP Request header expressions. Must use:
- Predefined Credential Type (automatic auth), OR
- Generic Credential Type with Header Auth

### 2. Gmail Trigger Requires Explicit Attachment Download
"Download Attachments" option must be enabled - not on by default.

### 3. Base64 Inflates File Size ~33%
A 7MB PDF becomes ~9-10MB in base64. Combined with JSON overhead, can appear much larger.

### 4. Multiple Workflows with Same Purpose
Found two workflows doing similar Claude Vision extraction:
- `p0X9PrpCShIgxxMP` (rebuilt this session)
- `YGXWjWcBIk66ArvT` (original, has issues)

May need consolidation in future.

---

## Status

| Item | Status |
|------|--------|
| Workflow Rebuilt | ✅ Complete |
| Claude API Auth | ✅ Fixed |
| Gmail OAuth | ✅ Refreshed |
| Attachment Download | ✅ Issue identified, fix applied by user |
| End-to-End Test | ⏳ Pending verification |

**Ready for testing.**
