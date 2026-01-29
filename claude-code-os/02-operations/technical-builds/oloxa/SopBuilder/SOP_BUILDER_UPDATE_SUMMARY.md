# SOP Builder - Email Templates & Resubmission Flow Update

**Date:** 2026-01-29
**Workflow ID:** ikVyMpDI0az6Zk4t
**Status:** ✅ Complete

---

## Changes Made

### 1. Email Template Updates (n8n Workflow)

#### Success Email (node: `generate-success-email`)
**Changes:**
- ✅ Replaced text logo with image: `<img src="https://sopbuilder.oloxa.ai/logo.png" alt="OLOXA" style="height:40px;">`
- ✅ Added new section "Here's Your Improved SOP" BEFORE the CTA
  - Shows the `improved_sop` content in a readable format with pre tag
  - Includes note: "This is a guide to help you restructure your SOP. Fill in details from your own business."
- ✅ Updated CTA copy:
  - Above button: "You've built a solid SOP. If you're interested in what automation could look like for this process, let's talk."
  - Button text: "Book Your Free Discovery Call" (unchanged)

#### Improvement Email (node: `generate-improvement-email`)
**Changes:**
- ✅ Replaced text logo with image: `<img src="https://sopbuilder.oloxa.ai/logo.png" alt="OLOXA" style="height:40px;">`
- ✅ Updated resubmit URL to include score and quick wins:
  - Old: `https://sopbuilder.oloxa.ai?lead=xxx&email=xxx&name=xxx`
  - New: `https://sopbuilder.oloxa.ai?lead=xxx&email=xxx&name=xxx&score=60&wins=` + encoded JSON

---

### 2. Frontend Resubmission Flow (app.js)

#### Updated `handleResubmitParams()` Function
**Changes:**
- ✅ Parse new URL params: `score` and `wins` (JSON-encoded quick wins)
- ✅ When resubmit mode detected (`?lead=xxx`):
  - Replace Step 0 content with "Welcome back" summary
  - Show previous score in large text (64px)
  - Display 3 quick wins in styled cards
  - Show "Update My SOP" button that jumps directly to Step 3 (process steps)
- ✅ Pre-fill and lock email/name fields on Step 4 (existing behavior preserved)

**New Step 0 for Returning Users:**
```html
- "Welcome back, {name}! Here's where you're at:"
- Big score display (64px, centered)
- 3 Quick Wins section (styled cards with numbers)
- "Update My SOP" button → jumps to Step 3
```

---

## Files Modified

### n8n Workflow
- **Workflow:** SOP Builder Lead Magnet (ikVyMpDI0az6Zk4t)
- **Nodes Updated:** 2
  - `generate-success-email` (id: generate-success-email)
  - `generate-improvement-email` (id: generate-improvement-email)

### Frontend Files
- **Location:** `/var/www/sopbuilder/` on server (157.230.21.230)
- **Files Updated:**
  - ✅ `app.js` - Updated resubmission flow

### Local Development Files
- **Location:** `/Users/computer/coding_stuff/claude-code-os/02-operations/technical-builds/oloxa/SopBuilder/`
- **Files Created:**
  - `email-success-updated.js` - New success email template
  - `email-improvement-updated.js` - New improvement email template
  - `SOP_BUILDER_UPDATE_SUMMARY.md` - This file

---

## Testing Checklist

### Email Templates
- [ ] Test success email (≥75% score)
  - [ ] Logo displays correctly
  - [ ] "Here's Your Improved SOP" section shows before CTA
  - [ ] Updated CTA copy displays
  - [ ] improved_sop content renders in pre tag
- [ ] Test improvement email (<75% score)
  - [ ] Logo displays correctly
  - [ ] Resubmit URL includes score and wins params
  - [ ] URL decodes correctly when clicked

### Frontend Resubmission Flow
- [ ] Test with resubmit URL: `https://sopbuilder.oloxa.ai?lead=test123&email=test@example.com&name=John&score=60&wins=%5B%7B%22title%22%3A%22Test%22%2C%22action%22%3A%22Test%20action%22%7D%5D`
  - [ ] Step 0 shows "Welcome back, John!"
  - [ ] Score displays as 60%
  - [ ] Quick wins decode and display
  - [ ] "Update My SOP" button jumps to Step 3
  - [ ] Email and name are pre-filled and locked on Step 4

### Full E2E Test
- [ ] Submit new SOP → receive improvement email
- [ ] Click resubmit link → land on welcome back screen
- [ ] Update SOP → submit → verify new score email

---

## Deployment Notes

### n8n Workflow
- Changes applied via MCP `n8n_update_partial_workflow`
- No workflow restart required (changes live immediately)

### Frontend
- Deployed via SSH: `scp -i ~/.ssh/digitalocean_n8n app.js root@157.230.21.230:/var/www/sopbuilder/`
- No server restart required (static files served directly)

---

## Rollback Plan

### If Issues Detected:

**n8n Workflow:**
```javascript
// Use n8n UI to revert node changes or restore from workflow export
// Previous jsCode is preserved in git history
```

**Frontend:**
```bash
# Restore previous app.js from git
git checkout HEAD~1 -- claude-code-os/02-operations/technical-builds/oloxa/SopBuilder/app.js

# Deploy to server
scp -i ~/.ssh/digitalocean_n8n app.js root@157.230.21.230:/var/www/sopbuilder/
```

---

## Next Steps

1. Test workflow with real submission
2. Verify email templates render correctly in Gmail/Outlook
3. Test resubmission flow end-to-end
4. Monitor Airtable for any issues with URL encoding

---

## Technical Notes

### URL Parameter Encoding
- `score` = plain integer (e.g., `60`)
- `wins` = JSON array encoded with `encodeURIComponent(JSON.stringify(quickWins))`
- Frontend decodes with: `JSON.parse(decodeURIComponent(winsEncoded))`

### Logo Requirements
- Logo must be accessible at: `https://sopbuilder.oloxa.ai/logo.png`
- Height set to 40px (maintains aspect ratio)
- Alt text: "OLOXA"

### Quick Wins Format
Expected JSON structure:
```json
[
  {
    "title": "Purpose Statement",
    "action": "Add a Purpose section explaining why this process matters."
  },
  {
    "title": "Process Flow",
    "action": "Break down into numbered steps using action verbs."
  },
  {
    "title": "Checklist",
    "action": "Add a checklist with key verification points."
  }
]
```

---

## Questions for Sway

1. Should we archive previous email template versions in git?
2. Do you want to test this with a real submission now, or should I trigger the webhook programmatically?
3. Should we add analytics tracking to the resubmission flow?

---

**Implementation Complete.**
