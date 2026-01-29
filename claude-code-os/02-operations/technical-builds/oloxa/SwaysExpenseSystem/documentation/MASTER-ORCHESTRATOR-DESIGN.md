# Master Orchestrator Design - W0: Monthly Expense Processor

**Date:** January 28, 2026, 8:30 PM CET
**Based on:** Sway's feedback from session 2026-01-28

---

## 🎯 USER REQUIREMENTS (Sway's Vision)

### The Complete Flow

1. **Automated Processing Phase**
   - Run all workflows automatically (W1, W2, W3, W6, W7, W8)
   - Process everything in the background
   - Generate missing transaction report

2. **Human Review Phase**
   - Send Slack notification with missing transactions
   - Sway adds missing items to designated folder
   - Click Slack button: "I've added everything, reprocess"

3. **Refinement Phase**
   - Re-run matching (W3)
   - Get as close to zero missing items as possible
   - May still have a few unmatched (acceptable)

4. **Finalization Phase**
   - Click Slack button: "Finalize and create folders"
   - Run W4 (Monthly Folder Builder & Organizer)
   - Creates folder structure for accountant
   - Organizes all documents properly

5. **Notification Phase**
   - Notify accountant everything is ready
   - Month is complete

### Key Requirements from Sway

- **Single trigger:** Run once at end of month (manual or scheduled)
- **Background operation:** Runs automatically, minimal interaction
- **Missing items visibility:** Clear notification of what's missing
- **Slack integration:** Buttons to move forward with process
- **Two-stage finalization:**
  - Stage 1: Reprocess after adding items
  - Stage 2: Finalize and create folders (W4)
- **~100 transactions/month** average volume

---

## 🏗️ ARCHITECTURE DESIGN

### Workflow Name: W0 - Master Monthly Processor

### Trigger Options

**Option A: Manual Webhook** (Recommended for testing)
- Webhook: `POST https://n8n.oloxa.ai/webhook/monthly-expense-process`
- Payload: `{"month": "January", "year": "2026"}`

**Option B: Scheduled** (For production)
- Run on 1st of each month at 9am
- Processes previous month automatically

**Option C: Slack Command** (For easy access)
- Slack slash command: `/process-expenses January 2026`
- Posts to webhook

### Master Orchestrator Flow

```
[Trigger: Webhook/Schedule/Slack]
    ↓
[Store Context: Month, Year, Run ID]
    ↓
┌─────────────────────────────────┐
│  PHASE 1: AUTO-PROCESSING       │
└─────────────────────────────────┘
    ↓
[Check which workflows are needed]
    ↓
[W1: Process Bank Statements] ──→ If new PDFs in folder
    ↓
[W2: Gmail Receipts] ──→ Check last 30 days (auto-runs, just verify)
    ↓
[W6: Expensify Reports] ──→ Process any Expensify PDFs
    ↓
[W7: Downloads Monitor] ──→ Check last 30 days (auto-runs, just verify)
    ↓
[W8: Invoice Collector] ──→ Collect invoices from G Drive
    ↓
[W3: Transaction Matching] ──→ Match everything
    ↓
[Generate Missing Items Report]
    ├─ Unmatched transactions count
    ├─ Unmatched receipts count
    ├─ Missing categories
    └─ Estimated completion %
    ↓
┌─────────────────────────────────┐
│  PHASE 2: HUMAN REVIEW          │
└─────────────────────────────────┘
    ↓
[Send Slack Notification]
    │
    ├─ Message: "Monthly processing complete for [Month Year]"
    ├─ Details: "[X] unmatched transactions, [Y] missing receipts"
    ├─ Instructions: "Add missing items to folder: [link]"
    ├─ Button 1: "Reprocess Now" ──→ Go to Phase 3
    └─ Button 2: "Skip to Finalize" ──→ Go to Phase 4
    ↓
[Wait for Slack Button Click]
    ↓
┌─────────────────────────────────┐
│  PHASE 3: REFINEMENT            │
└─────────────────────────────────┘
    ↓
[User clicked "Reprocess Now"]
    ↓
[Scan folder for new items]
    ↓
[W7: Process new items from folder]
    ↓
[W3: Re-run matching]
    ↓
[Generate Updated Report]
    ↓
[Send Slack Update]
    ├─ Message: "Reprocessing complete"
    ├─ Details: "[X] still unmatched (improved from [Y])"
    ├─ Button 1: "Add more & reprocess again" ──→ Back to Phase 2
    └─ Button 2: "Finalize" ──→ Go to Phase 4
    ↓
┌─────────────────────────────────┐
│  PHASE 4: FINALIZATION          │
└─────────────────────────────────┘
    ↓
[User clicked "Finalize"]
    ↓
[W4: Monthly Folder Builder]
    ├─ Create month folder structure
    ├─ Organize all receipts by category
    ├─ Organize all invoices
    ├─ Generate summary report
    └─ Move everything to final location
    ↓
[Send Accountant Notification]
    ├─ Email: "[Month Year] expenses ready for review"
    ├─ Link to folder
    ├─ Summary stats
    └─ CC: Sway
    ↓
[Mark Month as Complete]
    ↓
[Send Final Slack Notification]
    └─ Message: "✅ [Month Year] complete! Accountant notified."
```

---

## 📊 DATA FLOW

### State Management

Store orchestrator state in Google Sheets "Orchestrator_State" tab:

| RunID | Month | Year | Phase | Status | StartedAt | CompletedAt | UnmatchedCount | Notes |
|-------|-------|------|-------|--------|-----------|-------------|----------------|-------|
| RUN-001 | Jan | 2026 | 4 | complete | 2026-02-01 | 2026-02-01 | 3 | Success |

### Missing Items Report Structure

```json
{
  "month": "January",
  "year": "2026",
  "run_id": "RUN-001",
  "summary": {
    "total_transactions": 95,
    "matched_transactions": 87,
    "unmatched_transactions": 8,
    "total_receipts": 42,
    "matched_receipts": 40,
    "unmatched_receipts": 2,
    "completion_percentage": 91.6
  },
  "unmatched_transactions": [
    {
      "date": "2026-01-15",
      "amount": "€34.50",
      "description": "Unknown Merchant XYZ",
      "bank": "Barclay"
    }
  ],
  "unmatched_receipts": [
    {
      "date": "2026-01-20",
      "vendor": "Cafe ABC",
      "amount": "€12.00"
    }
  ],
  "folder_link": "https://drive.google.com/drive/folders/MISSING_ITEMS_FOLDER_ID"
}
```

---

## 🔔 SLACK INTEGRATION

### Slack Setup

**App Name:** Expense Processor Bot

**Required Permissions:**
- `chat:write` - Send messages
- `im:write` - Send DMs
- `commands` - Slash commands
- `incoming-webhook` - Post messages

### Slack Message Templates

**Template 1: Initial Processing Complete**
```
🎯 *Monthly Expense Processing Complete*

*Month:* January 2026
*Run ID:* RUN-001

📊 *Results:*
• Total Transactions: 95
• Matched: 87 (91.6%)
• Unmatched: 8

• Total Receipts: 42
• Matched: 40
• Unmatched: 2

⚠️ *Action Required:*
Add missing items to: <https://drive.google.com/...|Missing Items Folder>

*What's Missing:*
• 8 transactions without receipts
• 2 receipts without matching transactions

[View Full Report](https://docs.google.com/spreadsheets/d/.../report)

*Next Steps:*
```
[Button: Reprocess Now] [Button: Skip to Finalize]

**Template 2: Reprocessing Complete**
```
✅ *Reprocessing Complete*

*Improvement:*
• Before: 8 unmatched → After: 3 unmatched
• 5 new matches found!

Still missing:
• 3 transactions without receipts

*Options:*
```
[Button: Add More & Reprocess] [Button: Finalize Anyway]

**Template 3: Finalization Complete**
```
🎉 *Month Finalized!*

*January 2026 is complete*

✅ Folders created
✅ Documents organized
✅ Summary generated
✅ Accountant notified

📁 <https://drive.google.com/...|View Final Folder>
📊 <https://docs.google.com/...|View Summary Report>

*Final Stats:*
• 95 transactions processed
• 92 matched (96.8%)
• 3 unmatched (flagged for manual review)
```

---

## 🔧 TECHNICAL IMPLEMENTATION

### Node Breakdown

**W0 Master Orchestrator Nodes (Estimated: 45-55 nodes)**

1. **Trigger & Setup (3 nodes)**
   - Webhook/Schedule trigger
   - Store run context
   - Initialize state

2. **Phase 1: Auto-Processing (15 nodes)**
   - Check W1 needed (new bank statements?)
   - Execute W1 (if needed)
   - Verify W2 ran recently
   - Check W6 needed (Expensify PDFs?)
   - Execute W6 (if needed)
   - Verify W7 ran recently
   - Execute W8 (invoice collector)
   - Execute W3 (matching)
   - Query unmatched items
   - Generate report
   - Save report to Sheets
   - Update state

3. **Phase 2: Slack Notification (5 nodes)**
   - Build Slack message
   - Send to Slack with buttons
   - Wait for button click (Webhook)
   - Log user action
   - Route to Phase 3 or 4

4. **Phase 3: Refinement (8 nodes)**
   - Scan folder for new items
   - Execute W7 on new items
   - Re-execute W3 (matching)
   - Query updated unmatched
   - Calculate improvement
   - Generate updated report
   - Send Slack update
   - Wait for next action

5. **Phase 4: Finalization (10 nodes)**
   - Execute W4 (folder builder)
   - Verify W4 completion
   - Generate final summary
   - Email accountant
   - Send Slack completion message
   - Update state to "complete"
   - Archive run data
   - Cleanup temp files

6. **Error Handling (5 nodes)**
   - Workflow failure handler
   - Send error Slack message
   - Save error state
   - Retry logic
   - Manual intervention trigger

---

## 🎮 USER EXPERIENCE

### Monthly Workflow (User Perspective)

**End of Month (e.g., February 1st for January expenses):**

1. **User triggers:** Goes to Slack, types `/process-expenses January 2026`
   - OR: Runs automatically at 9am on 1st of month

2. **Wait 2-5 minutes:** System processes everything in background

3. **Slack notification arrives:**
   ```
   🎯 January 2026 processing complete!
   95 transactions, 87 matched (91.6%)
   8 items need your attention

   Add missing items here: [Folder Link]

   [Reprocess Now] [Skip to Finalize]
   ```

4. **User reviews missing items:** Opens folder link, sees what's missing

5. **User adds files:** Drops PDFs/images into "Missing Items" folder

6. **User clicks: [Reprocess Now]**

7. **Wait 1-2 minutes:** System rescans and rematches

8. **Slack update arrives:**
   ```
   ✅ Improved! 8 → 3 unmatched

   [Add More & Reprocess] [Finalize]
   ```

9. **User decides:** Good enough, clicks [Finalize]

10. **Wait 1-2 minutes:** W4 builds folders, organizes everything

11. **Slack confirmation:**
    ```
    🎉 January 2026 complete!
    Accountant notified. All done!
    ```

12. **User notifies accountant verbally/email (optional)**

**Total time:** 5-10 minutes of user attention across whole month

---

## 📈 SCALABILITY & PERFORMANCE

### Expected Execution Times

- **Phase 1 (Auto-processing):** 2-5 minutes
  - W1: 30-60s per bank statement (if new)
  - W6: 15-20s per Expensify report
  - W3: 20-60s (depends on volume)
  - Others: <10s each

- **Phase 3 (Refinement):** 1-2 minutes
  - W7 on new items: 30-60s
  - W3 re-matching: 20-60s

- **Phase 4 (Finalization):** 1-3 minutes
  - W4 folder building: 60-120s
  - Email/notifications: <10s

**Total system time:** 4-10 minutes
**User interaction time:** <2 minutes (clicking buttons, reviewing)

### Volume Handling

**Current (~100 transactions/month):**
- Well within capacity
- No optimization needed

**If scales to 500 transactions/month:**
- W3 matching may take 2-3 minutes
- Consider batch processing
- May need rate limit optimization

---

## 🔐 SECURITY & PERMISSIONS

### Slack Button Security

**Problem:** Anyone with Slack access could click buttons

**Solution:** Verify user ID matches authorized list
```javascript
const authorizedUsers = ['U01234567']; // Sway's Slack user ID
if (!authorizedUsers.includes(buttonClick.user.id)) {
  return { error: "Unauthorized" };
}
```

### Folder Permissions

**Missing Items Folder:**
- Only Sway has write access
- Bot has read access

**Final Folders (for accountant):**
- Sway + Accountant have read access
- Bot has write access

---

## 🧪 TESTING STRATEGY

### Phase 1: Unit Testing (Each workflow individually)
- ✅ W1 processes bank statements
- ✅ W2 monitors Gmail
- ✅ W3 matches transactions
- ✅ W6 processes Expensify
- ✅ W7 monitors Downloads
- ✅ W8 collects invoices
- ⏳ W4 builds folders (needs testing)

### Phase 2: Integration Testing (Orchestrator flow)
- Test Phase 1 → Phase 2 transition
- Test Slack button interactions
- Test Phase 3 refinement
- Test Phase 4 finalization

### Phase 3: End-to-End Testing (Full 2025 data)
- Wipe clean
- Process all Q1 2025
- Verify accuracy
- Process all Q2 2025
- Process all Q3 2025
- Process all Q4 2025
- Measure match rate %

---

## 🚀 DEPLOYMENT PLAN

### Stage 1: Build Core Orchestrator (Week 1)
- Create W0 workflow shell
- Build Phase 1 (auto-processing)
- Build Phase 2 (Slack notifications)
- Test basic flow

### Stage 2: Add Refinement (Week 1-2)
- Build Phase 3 (reprocessing)
- Test iterative refinement
- Optimize matching

### Stage 3: Add Finalization (Week 2)
- Build Phase 4 (W4 integration)
- Test folder creation
- Test accountant notification

### Stage 4: Polish & Test (Week 2-3)
- Add error handling
- Test with real data
- Optimize performance
- Document user guide

### Stage 5: Production Rollout (Week 3)
- Deploy to production
- Run first real month
- Monitor and adjust
- Collect feedback

---

## 📝 OPEN QUESTIONS FOR SWAY

1. **Accountant notification:**
   - Email address?
   - Preferred notification format?
   - Include summary stats?

2. **Missing items folder:**
   - Create new folder each month?
   - Or one permanent "Add Items Here" folder?

3. **Slack channel:**
   - DM to you?
   - Or specific channel like #expense-processing?

4. **Trigger preference:**
   - Manual (you run it when ready)?
   - Scheduled (auto-runs 1st of month)?
   - Slack command (most convenient)?

5. **W4 behavior:**
   - What folder structure does it create?
   - Where does it move final files?
   - Need to verify this works as expected

---

## 🎯 SUCCESS CRITERIA

### Definition of Done

**W0 Master Orchestrator is complete when:**
1. ✅ Single trigger runs all workflows
2. ✅ Slack notifications work with buttons
3. ✅ Missing items clearly reported
4. ✅ Refinement loop works (add items → reprocess)
5. ✅ W4 finalization creates folders correctly
6. ✅ Accountant notification sent
7. ✅ Full month can be processed in <10 min user time
8. ✅ Match rate consistently >95%
9. ✅ Error handling works gracefully
10. ✅ Tested end-to-end with real 2025 data

---

**Design Complete:** January 28, 2026, 8:45 PM CET
**Next Step:** Address root matching issue (W1 bank identification), then build W0
