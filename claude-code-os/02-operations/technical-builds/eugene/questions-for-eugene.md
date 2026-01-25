# Questions for Eugene - Document Classification System

**Date Created:** 2026-01-24
**Context:** Finalizing the AMA document classification and routing system

---

## 1. Document Types vs Folder Structure

**Issue:** There may be a mismatch between:
- The folders in Google Drive (what folders exist)
- The columns in Client_Tracker (what documents we track)
- The document types the AI can classify

**Questions:**
- Does every folder need a corresponding document type?
- Does every document type need its own folder?
- Or should some documents go to a general "Others" folder even if classified?

**Current observation:** The Client_Tracker has columns like `09_Altlastenkataster`, `10_Baugrundgutachten`, etc. but these may not match 1:1 with folders.

---

## 2. Baubeschreibung Classification

**Issue:** "Baubeschreibung" (building description) documents are being classified as "Exposé" but they're different document types.

**Questions:**
- What IS a Baubeschreibung in the AMA context?
- Which folder should it go to?
- Is there a tracker column for it? (I don't see "Baubeschreibung" in the current columns)
- Should it be added as a new document type or mapped to an existing one?

---

## 3. Core 4 Documents vs Everything Else

**Current "Core 4" documents that get routed to specific folders:**
1. Exposé (01_Projektbeschreibung)
2. Grundbuchauszug (03_Grundbuchauszug)
3. Calculation/DIN276 (10_Bautraegerkalkulation_DIN276)
4. Exit Strategy (36_Exit_Strategie)

**Questions:**
- Is this the correct "Core 4" list?
- Should any other documents be added to priority routing?
- For everything else - confirm they should go to "Others" folder for now?

---

## 4. Document Type Naming Convention

**Issue:** There are inconsistencies in naming:
- Folder names use numbers (01_, 02_, etc.)
- Some use German names, some English
- Classification prompts use different internal names

**Questions:**
- What's the canonical list of document types?
- What's the German name, English name, and folder name for each?
- Can you provide a master mapping table?

---

## 5. Budget Document

**Specific case:** A "Budget" document came in:
- It was classified but didn't match a specific category
- The Tier 2 classifier said it contains "cost revenues and profitability analysis"
- It was sent to "Others" (correct) but with wrong filename

**Questions:**
- Where should Budget documents be classified?
- Is it under `20_Budget_Tracking` in the tracker?
- Or is "Budget" actually a type of calculation document?

---

## 6. Tracker Column Verification

**Current Status columns (for checkmarks):**
- Status_Expose (column D)
- Status_Grundbuch (column E)
- Status_Calculation (column F)
- Status_Exit_Strategy (column G)
- Last_Updated (column H)

**Questions:**
- Are these column positions correct? (D, E, F, G, H)
- Should we add more Status columns for other document types?
- Or should we use the document columns (01_Expose, 02_Grundbuch, etc.) differently?

---

## 7. Complete Document Type List Needed

**Request:** Please provide a complete list with:

| # | German Name | English Name | Folder Name | Tracker Column | Priority |
|---|-------------|--------------|-------------|----------------|----------|
| 1 | Exposé/Projektbeschreibung | Project Description | 01_Expose | Status_Expose | Core |
| 2 | Grundbuchauszug | Land Registry | 02_Grundbuch | Status_Grundbuch | Core |
| ... | ... | ... | ... | ... | ... |

This will help ensure the AI classification, tracker updates, and folder routing all align.

---

## 8. Classification Prompt Refinement

**Issue:** The current Tier 1 and Tier 2 classification prompts may be too broad or have overlapping categories.

**Questions:**
- Can you review the classification categories and provide clearer definitions?
- What distinguishes similar documents (e.g., Baubeschreibung vs Exposé)?
- Are there documents that commonly get misclassified?

---

## Summary of Decisions Needed

1. [ ] Confirm/update the Core 4 document list
2. [ ] Provide master document type mapping table
3. [ ] Clarify Baubeschreibung classification
4. [ ] Clarify Budget classification
5. [ ] Verify tracker column positions
6. [ ] Decide: Should ALL non-Core documents go to Others for now?

---

**Next Steps After Eugene Review:**
- Update classification prompts with clearer definitions
- Update folder routing logic
- Update tracker column mappings
- Test with sample documents
