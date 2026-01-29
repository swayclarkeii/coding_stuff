# W0 Master Orchestrator Rebuild - Interactive Slack Buttons

**Date:** 2026-01-29
**Workflow ID:** ewZOYMYOqSfgtjFm
**Status:** ✅ Complete - Ready for Testing

---

## Overview

W0 Master Orchestrator has been successfully rebuilt with interactive Slack buttons and webhook callback handlers. The workflow now provides a rich interactive experience where users can trigger actions (re-matching, filing, accountant handoff) directly from Slack notifications.

---

## What Was Built

### 1. Main Orchestration Flow (UNCHANGED)

The core orchestration logic remains intact:
- **Trigger:** Webhook at `w0-expense-orchestrator-start`
- **Input:** Month or quarter parameter
- **Process:**
  1. Read Transactions from Google Sheets
  2. Filter for missing receipts/unmatched transactions
  3. Calculate summary statistics
  4. Send Slack notification

### 2. NEW: Interactive Slack Notification

**Replaced:** Simple text-based Slack messages
**With:** Interactive Block Kit message with 3 action buttons

**Node:** "Format Slack Interactive Message" → "Send Slack Interactive Message"

**Message Format:**
```
⚠️ Expense System Status - [Period]

Missing Documents Detected

Missing Receipts: X transactions (€Y)
Missing Invoices: Z transactions (€W)
Total: N documents needed (€Total)

[Re-match Now] [Execute Filing] [Send to Accountant]
```

**Implementation:**
- Format Slack Interactive Message (Code node) - Builds Block Kit JSON structure
- Send Slack Interactive Message (HTTP Request) - Posts to Slack API with blocks

### 3. NEW: Webhook Callback System

**Master Webhook:** `https://n8n.oloxa.ai/webhook/slack-expense-buttons`

**Flow:**
```
Slack Button Click
  ↓
Webhook: Slack Buttons (receives POST)
  ↓
Parse Slack Payload (extracts action_id)
  ↓
Route by Action (Switch node)
  ├─ rematch → Execute W3 → Re-read sheets → Respond
  ├─ filing → Execute W4 → Respond
  └─ accountant → Prepare email → Send Gmail → Respond
  ↓
Acknowledge Slack Button (immediate ephemeral response)
```

---

## Interactive Button Handlers

### Button 1: Re-match Now
**Action ID:** `expense_rematch`
**Behavior:**
1. Calls W3 (Matching workflow) via Execute Workflow node
2. Re-reads Transactions sheet to get updated status
3. Responds to Slack: "✅ Re-match completed! Updated status will be posted shortly."

**Nodes:**
- Execute W3 (Re-match)
- Read Transactions After Re-match
- Respond: Re-match Complete

### Button 2: Execute Filing
**Action ID:** `expense_filing`
**Behavior:**
1. Calls W4 (Filing workflow) via Execute Workflow node
2. Responds to Slack: "📁 Filing workflow started! Documents are being organized..."

**Nodes:**
- Execute W4 (Filing)
- Respond: Filing Started

### Button 3: Send to Accountant
**Action ID:** `expense_accountant`
**Behavior:**
1. Prepares email with subject: "VAT [Month] [Year] — Ready for Review"
2. Sends email via Gmail with Drive folder link
3. Responds to Slack: "✉️ Email sent to accountant with folder link!"

**Nodes:**
- Prepare Accountant Email
- Send Accountant Email (Gmail node)
- Respond: Accountant Emailed

**Drive Folder:** `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15`

---

## Removed Components

### Disabled Nodes (Kept for Reference)
- Execute W1 (Bank Statements) - disabled
- Execute W2 (Gmail Receipts) - disabled
- Execute W6 (Expensify) - disabled
- Execute W3 (Matching) - disabled

These were part of the original sequential execution design and are now disabled. W0 no longer triggers intake workflows automatically.

### Old Slack Notification Nodes (Still Present, Can Be Removed)
- Format Slack Message (Missing) - still connected, can be removed
- Send Slack Notification (Missing) - still connected, can be removed
- Format Slack Message (Success) - still connected, can be removed
- Send Slack Notification (Success) - still connected, can be removed
- Log Missing Receipts - still connected
- Log Success - still connected

**Note:** These nodes are still present in the workflow but are redundant now that we have the interactive message. They can be safely removed in a cleanup pass.

---

## Configuration Details

### Credentials Used
- **Slack API:** `iN2b9bGFpoyptSPr` (slack-workflow-notifications)
- **Google Sheets:** `H7ewI1sOrDYabelt` (Google Sheets account)
- **Gmail:** `PLACEHOLDER` (needs to be configured with actual Gmail OAuth2 credential)

### Key IDs Referenced
- **W3 (Matching):** `CJtdqMreZ17esJAW`
- **W4 (Filing):** `nASL6hxNQGrNBTV4`
- **Google Sheets:** `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
- **Drive Folder:** `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15`

### Slack Configuration
- **Channel:** `expense-reports` (existing channel from W0)
- **Webhook Path:** `slack-expense-buttons`

---

## Testing Plan

### 1. Happy Path Test
**Trigger W0:**
```bash
curl -X POST https://n8n.oloxa.ai/webhook/w0-expense-orchestrator-start \
  -H "Content-Type: application/json" \
  -d '{"month": "January 2026"}'
```

**Expected:**
1. W0 executes
2. Reads transactions from Google Sheets
3. Filters for missing receipts
4. Sends interactive Slack message to #expense-reports
5. Message displays with 3 buttons

### 2. Button Interaction Tests

**Test A: Re-match Button**
1. Click "Re-match Now" button in Slack
2. Verify ephemeral "Processing..." message appears
3. Verify W3 execution starts (check n8n executions)
4. Verify "Re-match completed" response in Slack

**Test B: Execute Filing Button**
1. Click "Execute Filing" button
2. Verify W4 execution starts
3. Verify "Filing started" response in Slack

**Test C: Send to Accountant Button**
1. Click "Send to Accountant" button
2. Verify email is sent via Gmail
3. Verify "Email sent" response in Slack

### 3. Error Scenarios

**Scenario 1: W3 fails during re-match**
- Expected: Error should be logged, but workflow should not crash
- Note: Need to add error handling to Execute W3 node

**Scenario 2: Gmail credential missing**
- Expected: Clear error message about missing credential
- Fix: Configure Gmail OAuth2 credential in "Send Accountant Email" node

**Scenario 3: Slack payload parsing fails**
- Expected: Workflow should handle gracefully
- Current: Parse Slack Payload node will throw error (needs error handling)

---

## Known Issues & TODO

### Critical
1. **Gmail Credential Missing:** "Send Accountant Email" node has placeholder credential
   - Action: Replace with actual Gmail OAuth2 credential
   - User: Sway's Gmail account

2. **Accountant Email Address:** Hardcoded to `accountant@example.com`
   - Action: Replace with actual accountant email in "Prepare Accountant Email" node

### Cleanup Needed
3. **Remove Old Slack Nodes:** Old notification nodes are redundant
   - Nodes to remove:
     - Format Slack Message (Missing)
     - Send Slack Notification (Missing)
     - Format Slack Message (Success)
     - Send Slack Notification (Success)
     - Log Missing Receipts
     - Log Success

4. **Remove Disabled Execute Nodes:** No longer needed
   - Execute W1 (Bank Statements)
   - Execute W2 (Gmail Receipts)
   - Execute W6 (Expensify)
   - Execute W3 (Matching)

### Error Handling
5. **Add Error Handling:**
   - Execute W3 (Re-match) - if W3 fails, respond with error message
   - Execute W4 (Filing) - if W4 fails, respond with error message
   - Send Accountant Email - if email fails, respond with error message
   - Parse Slack Payload - if parsing fails, respond with error message

### Enhancement Opportunities
6. **Dynamic Processing Period:** Currently uses current month/year in accountant email
   - Improvement: Pass processing period from original W0 execution context

7. **More Detailed Status Updates:** After re-match, could re-run the full status calculation and post updated interactive message

8. **Button Confirmation:** Add confirmation step before sending to accountant (destructive action)

---

## Slack App Configuration Required

**IMPORTANT:** For interactive buttons to work, the Slack app needs to have an "Interactivity & Shortcuts" URL configured:

**Steps:**
1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Select your app (slack-workflow-notifications)
3. Go to "Interactivity & Shortcuts"
4. Enable interactivity
5. Set Request URL to: `https://n8n.oloxa.ai/webhook/slack-expense-buttons`
6. Click "Save Changes"

**Without this configuration, buttons will appear in Slack but won't trigger the webhook when clicked.**

---

## Next Steps

### Immediate
1. ✅ Configure Gmail OAuth2 credential for "Send Accountant Email" node
2. ✅ Update accountant email address in "Prepare Accountant Email" code
3. ✅ Configure Slack app "Interactivity & Shortcuts" URL
4. ✅ Test all three buttons in Slack

### Cleanup (After Testing)
5. Remove old Slack notification nodes
6. Remove disabled Execute Workflow nodes
7. Add error handling to all callback handlers

### Optimization
8. Add retry logic for transient API failures
9. Consider adding rate limiting for button clicks
10. Add analytics/logging for button usage

---

## Handoff Notes

### How to Trigger W0
```bash
# Via webhook
curl -X POST https://n8n.oloxa.ai/webhook/w0-expense-orchestrator-start \
  -H "Content-Type: application/json" \
  -d '{"month": "January 2026"}'

# Via n8n UI
# 1. Open W0 workflow
# 2. Click "Test workflow" button
# 3. Click "Execute Workflow" on Webhook Trigger node
```

### How to View Slack Webhook URL
- Webhook path: `slack-expense-buttons`
- Full URL: `https://n8n.oloxa.ai/webhook/slack-expense-buttons`
- This URL must be configured in Slack app settings

### How to Modify Button Actions
1. Open W0 workflow in n8n
2. Find "Route by Action" Switch node
3. Each output port corresponds to a button action:
   - Port 0 (rematch) → "Re-match Now" button
   - Port 1 (filing) → "Execute Filing" button
   - Port 2 (accountant) → "Send to Accountant" button
4. Modify the nodes connected to each port to change behavior

### Debugging Button Clicks
1. Click button in Slack
2. Check n8n workflow executions for W0
3. Look for execution triggered by webhook (not manual)
4. Examine "Parse Slack Payload" node output to see action_id
5. Trace through Switch node to see which path was taken

---

## Architecture Summary

**W0 Now Has Two Modes:**

### Mode 1: Status Reporting (Original Webhook)
```
Manual Trigger → Read Sheets → Calculate Status → Send Interactive Slack Message
```

### Mode 2: Button Callbacks (New Webhook)
```
Slack Button Click → Parse Payload → Route → Execute Action → Respond
```

**Key Design Principle:** W0 no longer triggers intake workflows (W1, W2, W6) automatically. Those are handled separately. W0 focuses on:
1. Status reporting with interactive notifications
2. On-demand actions (re-match, filing, accountant handoff)

---

## Files Modified
- Workflow: W0 - Master Orchestrator (Phase 0) (ID: ewZOYMYOqSfgtjFm)

## Documentation Created
- `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/oloxa/SwaysExpenseSystem/W0-rebuild-interactive-buttons-complete.md`

---

**Agent:** solution-builder-agent
**Session:** 2026-01-29
**Status:** Implementation complete, ready for configuration and testing
