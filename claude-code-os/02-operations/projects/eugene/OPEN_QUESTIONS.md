# Eugene - Open Questions for Phase 1 Implementation

**Date:** December 20, 2024
**Purpose:** Clarify requirements before starting N8N workflow build
**Status:** Awaiting Eugene's responses

---

## Executive Summary

We've analyzed your Draft_Dataroom structure and sample documents. We successfully mapped **3 out of 4 critical documents** to existing folders in your ideal structure:

✅ **Teaser/Exposé** → `Objektunterlagen/Projektbeschreibung_Exposé/`
✅ **Kalkulation** → `Objektunterlagen/Bauträgerkalkulation_DIN276/`
✅ **Grundbuch** → `Objektunterlagen/Grundbuchauszug/`
❌ **Exit Strategy** → NO FOLDER EXISTS (see Critical Questions below)

**We have 20 questions organized by priority.** The first 4 questions are blockers that must be answered before we start building.

---

## CRITICAL QUESTIONS (Must Answer Before Starting Build)

### Exit Strategy - The Missing Document

**Finding:** Exit Strategy is listed as a "critical document" in your requirements, BUT:
- ❌ No "Exit Strategy" folder exists in your Draft_Dataroom structure
- ❌ We found ZERO Exit Strategy sample documents in any of your 10+ project folders
- ✅ Your requirements doc confirms it should exist: "Exit Strategy - Lender repayment plan"

**Questions:**

### 1. Do you actually receive standalone "Exit Strategy" documents from clients?

- **If YES:** Can you provide 1-2 sample documents for AI training?
- **If NO:** Is exit strategy information embedded in Teaser or Kalkulation documents instead?

---

### 2. Draft_Dataroom folder structure for Exit Strategy

Which approach should we take?

**Option A:** CREATE a new folder in Draft_Dataroom
Example: `Wirtschaftliche_Unterlagen/Exit_Strategie/`

**Option B:** Use temporary folder for Phase 1
Place in `0_Critical_Other/` until we build out Phase 2

**Option C:** Reclassify the document
Remove from "critical" category and move to "important" (if it's rare/optional)

---

### 3. What makes an Exit Strategy document identifiable?

To train the AI, we need to know:

- **German terms:** What words appear in the document?
  (Exit-Strategie? Ausstiegsstrategie? Verkaufsstrategie? Tilgungsplan?)

- **Content indicators:** What should ChatGPT look for?
  (Timeline? Target buyers? Sale price projections? Lender repayment schedule?)

---

### 4. Email forwarding workflow - confirm the flow

Which workflow matches how you'll actually use this?

**Option A:**
Client sends email → You receive it → Forward to your own email → Forward to automation email

**Option B:**
Client sends email → You receive it → Forward DIRECTLY to automation email

**Also:**
- Should we preserve the original sender's email address in the folder name?
  Example: `[ClientEmail]_[PropertyName]_[Date]/`

---

### 5. Phase 1 scope - which documents to automate?

**Option A: Start small (faster to build, less to test)**
Automate ONLY the 4 critical documents

**Option B: Start comprehensive (longer build time)**
Include all 18 document types from the start

**Option C: Balanced approach (RECOMMENDED)**
Start with 4 critical + 4-5 "important" documents, expand in Phase 2

Your preference?

---

## HIGH PRIORITY QUESTIONS (Should Answer Before Testing)

### Document Samples & AI Training

### 6. Can you provide 2-3 sample documents for each critical type?

Current status:
- Teaser/Exposé: ✅ Have 3+ samples
- Kalkulation: ✅ Have 3+ samples (PDF + Excel)
- Grundbuch: ✅ Have 6+ samples
- Exit Strategy: ❌ **NEED SAMPLES**

---

### 7. What accuracy threshold is acceptable for Phase 1?

- Your requirements say **95%+ target** - is that firm?
- Or can we start with **85-90%** and iterate based on real-world performance?
- How should we handle edge cases? (e.g., handwritten notes on documents, multi-page combinations)

---

### 8. Document variations to test

- Do you receive **Kalkulation in Excel format**, or only PDF? (We found both in your samples)
- Do **Teasers vary significantly** in format between different clients/brokers?
- Are there **common "false positives"** we should watch for? (e.g., documents that look like Grundbuch but aren't)

---

### Google Sheets Dashboard Structure

### 9. What information should the Google Sheets dashboard show?

**Option A: Deal summary**
One row per deal, showing 4 critical docs status (✅ received / ❌ missing)

**Option B: Document details**
One row per document, showing all details (doc type, confidence %, date received)

**Option C: Both (RECOMMENDED)**
Two sheets: "Deal Summary" + "Document Details"

---

### 10. Dashboard updates - how should we handle duplicates?

If we receive a Grundbuch for "Malzfabrik" on Day 1, then another Grundbuch for "Malzfabrik" on Day 5:

**Option A:** UPDATE the existing row with newest version
**Option B:** CREATE new row every time (track historical versions)
**Option C:** Create new row but mark old one as "superseded"

Also:
- Should low-confidence documents (<70%) appear in a separate "Review Needed" tab?

---

### 11. What actions should you take from the dashboard?

**Option A: Just monitoring**
View status only, no interaction needed

**Option B: Clickable links**
Click to open documents/folders directly from dashboard

**Option C: Manual override (RECOMMENDED)**
Include column where you can mark documents as correct/incorrect to improve AI over time

---

### Folder Organization

### 12. Folder naming convention - which format do you prefer?

**Option A:** `[ClientEmail]_[PropertyName]_[Date]/`
Example: `broker@immobilien.de_Malzfabrik_20241220/`

**Option B:** `[Date]_[PropertyName]_[ClientCompany]/`
Example: `20241220_Malzfabrik_Immobilien_GmbH/`

**Option C:** `[PropertyName]_[Date]/` (simpler)
Example: `Malzfabrik_20241220/`

---

### 13. ZIP file handling

- How often do clients send **ZIP files** vs individual attachments?
- Should we extract **ALL files** from ZIPs, or only certain file types (PDFs, Excel, images)?
- Should we **keep the original ZIP file**, or delete it after extraction?

---

### Notifications

### 14. Eugene notification preferences

**Frequency:**
- Email notification for **EVERY processed email**? OR
- **Daily summary** (e.g., "Processed 3 deals today, 2 complete, 1 missing docs")

**Content:**
- What info should notification include?
  - Deal/property name
  - Documents found vs missing
  - Link to Google Drive folder
  - Low-confidence items needing review

**Urgency:**
- Should low-confidence docs trigger **immediate notification**?
- Or just flag in dashboard for you to review when convenient?

---

### 15. Client notifications (German language)

Should the system send **automatic confirmation emails** to clients in German?

**Option A: Fully automatic**
System sends: "Vielen Dank, wir haben X Dokumente erhalten. Wir prüfen noch Y Dokumente..."

**Option B: Eugene reviews first (RECOMMENDED)**
System processes silently, you manually send confirmations after reviewing

**Option C: Hybrid**
Auto-confirm receipt, but you manually request missing documents

If automatic, what should the message say?

---

## MEDIUM PRIORITY QUESTIONS (Can Answer During Testing)

### Error Handling

### 16. Edge cases - how should the system respond?

**Scenario A: Email with NO attachments**
- Ignore silently?
- Notify you? ("Email received with no attachments from [sender]")

**Scenario B: ChatGPT can't identify ANY documents**
- All documents score <70% confidence
- Create "Needs Review" notification?
- Still create folders and let you manually organize?

**Scenario C: Duplicate property name detected**
- Receive "Malzfabrik" documents twice
- Create new folder (Malzfabrik_20241220, Malzfabrik_20241227)?
- Or merge into existing folder?

---

### 17. Email labeling preferences

- Label format: **"Processed - [PropertyName]"** or just **"Processed"**?
- Label where: Your inbox? Or only the automation inbox?
- Should low-confidence results get different label? (**"Needs Review"** instead of "Processed")

---

## LOW PRIORITY QUESTIONS (Validate During Testing)

### Success Criteria

### 18. What does "success" look like for Phase 1 launch?

**Option A:** Process 1 test deal perfectly (100% accuracy)
**Option B:** Process 3-5 real deals with <5% errors
**Option C:** Save you 4+ hours on the very first real deal

What's your success threshold?

---

### 19. Timeline expectations

- **When would you ideally start testing Phase 1?**
  (Week of X, or "as soon as ready")

- **How many weeks of testing before "production" use?**
  (1 week? 2-4 weeks? Until perfect?)

- **What's your tolerance for bugs during initial testing?**
  (None? Minor issues OK? Expect some iteration?)

---

### 20. Handoff & maintenance

- Do you want to **learn how to modify the N8N workflow** yourself?
- Or should **all changes go through us** during Phase 1?
- At what point do you want to **take over workflow maintenance**?

---

## PRIORITY SUMMARY

### 🔴 Must Answer Before Starting Build (Blockers):
1. Exit Strategy status - standalone doc or embedded? (Questions 1-3)
2. Exit Strategy sample documents (Question 1)
3. Email workflow confirmation (Question 4)
4. Phase 1 scope - which documents to include (Question 5)

### 🟡 Should Answer Before Testing (High Priority):
- Document samples for AI training (Questions 6-8)
- Google Sheets dashboard structure (Questions 9-11)
- Folder naming convention (Question 12)
- ZIP file handling (Question 13)
- Notification preferences (Questions 14-15)

### 🟢 Can Answer During Testing (Medium Priority):
- Edge case handling (Questions 16-17)
- Success criteria and timeline (Questions 18-19)
- Handoff and maintenance (Question 20)

---

## What Happens Next

**Step 1:** You answer the 🔴 Critical Questions (1-5)
**Step 2:** We finalize the folder structure and document mapping
**Step 3:** You answer 🟡 High Priority Questions (6-15)
**Step 4:** We build and test the N8N workflow
**Step 5:** You answer 🟢 Medium Priority Questions (16-20) based on real testing
**Step 6:** We refine and launch Phase 1

---

## How to Respond

**Option 1: Direct answers**
Reply with numbered responses (e.g., "Q1: Yes, we receive Exit Strategy docs, sending samples...")

**Option 2: Schedule call**
Let's discuss the critical questions together (30-45 min call)

**Option 3: Hybrid**
Answer critical questions now, schedule call for detailed questions

---

**Questions compiled by:** Sway
**Next review:** After Eugene's responses received
**Related documents:**
- [project_requirements.md](requirements/project_requirements.md) - Full technical requirements
- [README.md](README.md) - Project overview and business case
- Draft_Dataroom folder structure - Your ideal target structure
