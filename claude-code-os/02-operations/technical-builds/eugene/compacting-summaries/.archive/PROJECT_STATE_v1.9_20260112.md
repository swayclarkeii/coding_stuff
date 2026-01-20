# Eugene Document Organizer - Project State v1.9

**Version:** 1.9
**Date:** 2026-01-12
**Status:** 🎯 **PLANNING V8 - 2-Tier Classification Architecture**

---

## Executive Summary

Eugene Document Organizer has achieved V7 production readiness and is currently in planning phase for V8, which will introduce **2-tier hierarchical classification** to handle all 38 German real estate document types (vs current 5 types).

**Current Production State (V7):**
- ✅ End-to-end pipeline functional (Pre-Chunk 0 → Chunk 0 → Chunk 2 → Chunk 2.5)
- ✅ GPT-4 classification working (85% confidence on test execution #1760)
- ✅ Client_Tracker restructured (43 columns, simplified from 70+)
- ✅ Status column tracking with ✓ checkmarks
- ✅ File movement to correct Google Drive folders

**V8 Goals:**
- Classify all 38 document types (not just 5)
- 2-tier architecture: Tier 1 (4 categories) → Tier 2 (6-14 types per category)
- Only MOVE 4 CORE types, but correctly classify all 34 SECONDARY types
- Add confidence scores to filenames
- Create holding folders for SECONDARY types

---

## Current Session Context (2026-01-12)

### Active Planning Session

**Plan File:** `/Users/swayclarke/.claude/plans/polished-singing-peacock.md`

**Status:** In plan mode - V8 2-tier classification architecture designed, awaiting implementation

**Key Decisions Made:**
1. ✅ Keep 4 categories (not 6) for Tier 1 classification
2. ✅ Version V8 (not V7.1) - V7 remains untouched as rollback point
3. ✅ Incremental node changes with before/after tracking for safety
4. ✅ Automated webhook testing (not manual browser testing)
5. ✅ Future features tracked in IMPROVEMENTS_AND_MISSING_FEATURES.md v2.0

### Agent IDs from Current Session

**Critical:** These agent IDs can be resumed to continue work after session restart.

| Agent ID | Type | Purpose | Status |
|----------|------|---------|--------|
| (Explore agents used during planning) | Explore | Found 38 document type taxonomy | ✅ Complete |
| (Plan agent used with Opus) | Plan | Designed 2-tier classification architecture | ✅ Complete |

**Note:** Full plan document contains comprehensive implementation details for V8.

---

## Current To-Do List

### ✅ Completed (V7 Phase 1)
- [x] V6 production readiness achieved
- [x] Client_Tracker restructured to 43 columns
- [x] 5 critical fixes resolved (If nodes, Google Sheets, JS syntax, workflow cache, execution context)
- [x] End-to-end test successful (Execution #1760)
- [x] V7 workflows backed up to v7_phase_one folder
- [x] Archives consolidated (.archive folder structure cleaned)
- [x] PROJECT_STATE v1.8 created
- [x] MY-JOURNEY.md updated with V6→V7 transition
- [x] V8 2-tier classification architecture designed
- [x] Existing IMPROVEMENTS_AND_MISSING_FEATURES.md document located

### ⏳ Pending (V8 Implementation)

**Phase 0: Setup (30 min)**
- [ ] Create v8_phase_one folder structure
- [ ] Copy V7 workflows to V8 folder as starting point
- [ ] Create V8 changelog file
- [ ] Update IMPROVEMENTS_AND_MISSING_FEATURES document to v2.0

**Phase 1: Infrastructure (2-3 hours)**
- [ ] Create holding folders in Google Drive (_Holding_Property, _Holding_Financial, _Holding_Legal, _Holding_Misc)
- [ ] Update AMA_Folder_IDs sheet with 4 holding folder columns
- [ ] Update Chunk 0 to create holding folders for new clients

**Phase 2-4: Incremental Implementation (9-13 hours)**
- [ ] Implement Tier 1 classification (modify code-1 node)
- [ ] Implement Tier 2 classification (modify code-2, add http-openai-2, add code-tier2-parse)
- [ ] Add action mapping (add code-action-mapper node)
- [ ] Add file rename with confidence (add drive-rename node)
- [ ] Update folder mapping (modify code-4 node)
- [ ] Update tracker conditional logic (modify code-8 node)
- [ ] Update routing logic (modify if-1 node)

**Phase 5: Automated Testing (4-6 hours)**
- [ ] Setup webhook test infrastructure
- [ ] Execute 5 automated test cases via test-runner-agent
- [ ] Validate all checkpoints (Tier 1/2 accuracy >85%, tracker updates, filenames, holding folders)
- [ ] Fix any issues found

**Phase 6: Production Deployment**
- [ ] Final validation on V8
- [ ] Deactivate V7 workflows
- [ ] Activate V8 workflows
- [ ] Monitor first real execution
- [ ] Keep V7 backup ready for rollback

### 🔴 Blockers
None - V7 is production-ready, V8 is in planning phase

### ⚠️ Known Issues
None blocking V8 implementation

---

## Key Decisions Made

### 1. 2-Tier Classification Architecture (V8, 2026-01-12)
**Decision:** Implement 2-tier hierarchical classification (Tier 1: 4 categories, Tier 2: 6-14 types per category)

**Rationale:**
- Current system only classifies 5 types (Exposé, Grundbuch, Calculation, Exit_Strategy, Other)
- All 34 secondary document types lumped into "Other" with no visibility
- Edge case risk: Purchase Agreement might be misclassified as Calculation
- User experience: Eugene can't tell if system is working when files classified as "Other"

**Impact:**
- Better accuracy (80-90% for all 38 types vs 0% for 34 types)
- Diagnostic visibility (confidence scores in filenames)
- Future-proof architecture (add folder mappings without re-engineering)
- Better UX (Eugene sees "purchase_agreement_88pct.pdf" not "other_60pct.pdf")
- Performance: +20-25% latency, +60% cost ($18-36/year vs $12-24/year)

### 2. Classification ≠ Action (V8, 2026-01-12)
**Decision:** Classify all 38 types, but only MOVE 4 CORE types to specific folders

**Rationale:**
- System needs to identify all document types for resilience
- But only 4 types need immediate folder organization
- Other 34 types: classified, renamed with confidence, moved to holding folders
- Allows future expansion without re-engineering classification logic

**Impact:**
- CORE types (4): 01_Projektbeschreibung, 03_Grundbuchauszug, 10_Bautraegerkalkulation_DIN276, 36_Exit_Strategie
- SECONDARY types (34): Moved to holding folders by category, no tracker updates
- Filename format: `{typeCode}_{clientName}_{confidence}pct.{extension}`

### 3. 4 Categories vs 6 Categories (V8, 2026-01-12)
**Decision:** Keep 4 broad categories for Tier 1 (not split into 6)

**Rationale:**
- OBJEKTUNTERLAGEN (14 types), WIRTSCHAFTLICHE_UNTERLAGEN (12 types), RECHTLICHE_UNTERLAGEN (6 types), SONSTIGES (6 types)
- GPT-4 can handle 12-14 types reliably with well-structured prompts
- Splitting into 6 doesn't solve WIRTSCHAFTLICHE_UNTERLAGEN (still 12 types)
- Simpler Tier 1 (4 choices) = higher Tier 1 accuracy
- Fewer prompts to maintain and debug

**Impact:**
- Tier 1 prompt: 4 category classification with German keywords
- Tier 2 prompts: 4 category-specific prompts (one for each Tier 1 category)
- Mitigation for 14-type category: Rich German keyword lists, disambiguation examples

### 4. Version V8 (not V7.1) (V8, 2026-01-12)
**Decision:** V8 implementation (major version bump), not V7.1

**Rationale:**
- V7 Phase 1 is production-ready and should remain untouched
- V8 represents significant architecture change (2-tier classification)
- Clean rollback path: V7 → V8, not V7.0 → V7.1
- New folder structure: v8_phase_one/ (parallel to v7_phase_one/)

**Impact:**
- V7 workflows remain active during V8 development
- Only deploy V8 after full testing
- V7 backup always available for rollback

### 5. Incremental Node Changes with Safety Protocol (V8, 2026-01-12)
**Decision:** Modify one node at a time with before/after exports and validation

**Rationale:**
- Prevents breaking production workflow with multi-node changes
- Allows surgical rollback to any point
- Catches unintended changes early (n8n sometimes modifies other nodes)

**Impact:**
- Export workflow before EACH node modification
- Make ONE change, export after, validate, test
- Optional diff check for critical changes
- ~50K token budget for safety protocol (worth it)
- 9 nodes modified sequentially in V8

### 6. Automated Webhook Testing (not manual browser) (V8, 2026-01-12)
**Decision:** Use test-runner-agent with webhook triggers for V8 testing

**Rationale:**
- Faster, reproducible, token-efficient
- Manual browser testing wastes 20K-150K tokens per Playwright snapshot
- Webhook testing: ~100 tokens per test
- Systematic test coverage (5 test cases)
- CI/CD ready for future

**Impact:**
- Use existing Sway Clarke webhook infrastructure
- 5 automated test cases: CORE Exposé, CORE Calculation, SECONDARY Kaufvertrag, Low confidence, Mixed batch
- test-runner-agent handles execution and validation

---

## Important IDs / Paths / Workflow Names

### n8n Workflows (V7 Production)

| Workflow Name | ID | Nodes | Status | Backup Location |
|--------------|-----|-------|--------|-----------------|
| Pre-Chunk 0 | YGXWjWcBIk66ArvT | 42 | ✅ Active | v7_phase_one/pre_chunk_0_v7.0_20260112.json |
| Chunk 0 | zbxHkXOoD1qaz6OS | 20 | ✅ Active | v7_phase_one/chunk_0_v7.0_20260112.json |
| Chunk 2 | qKyqsL64ReMiKpJ4 | 11 | ✅ Active | v7_phase_one/chunk_2_v7.0_20260112.json |
| Chunk 2.5 | okg8wTqLtPUwjQ18 | 18 | ✅ Active | v7_phase_one/chunk_2.5_v7.0_20260112.json |

**V8 Target:** Chunk 2.5 will expand from 18 → 24 nodes (add 6 new nodes for 2-tier classification)

### Google Sheets

| Spreadsheet Name | ID | Purpose |
|-----------------|-----|---------|
| Client_Tracker | 12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I | 43-column tracker (37 folder IDs + 4 Status columns + metadata) |
| Client_Registry | 1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI | Client lookup registry with status tracking |
| AMA_Folder_IDs | 1-CPnCr3locAORVX5tUEoh6r0i-x3tQ_ROTN0VXatOAU | Folder ID mapping for each client |

**V8 Changes:** AMA_Folder_IDs will add 4 holding folder columns (_Holding_Property, _Holding_Financial, _Holding_Legal, _Holding_Misc)

### Google Drive

| Folder Name | ID | Purpose |
|------------|-----|---------|
| Client Root Parent | 1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm | Root folder for all client folders |
| dummy_files | 1GG_OCKvT1ivR0F-uIVq0b1jhHreWg1Kh | Test PDF files for development |

### File Paths

| File | Location | Purpose |
|------|----------|---------|
| VERSION_LOG.md | `/02-operations/technical-builds/eugene/compacting-summaries/VERSION_LOG.md` | Version history tracking |
| PROJECT_STATE v1.8 | `/02-operations/technical-builds/eugene/compacting-summaries/PROJECT_STATE_v1.8_20260112.md` | V7 production readiness state |
| PROJECT_STATE v1.9 | `/02-operations/technical-builds/eugene/compacting-summaries/PROJECT_STATE_v1.9_20260112.md` | Current state (this file) |
| V8 Plan | `/Users/swayclarke/.claude/plans/polished-singing-peacock.md` | Complete V8 implementation plan |
| IMPROVEMENTS_AND_MISSING_FEATURES | `/02-operations/technical-builds/eugene/N8N_Blueprints/.archive/v4_phase1/IMPROVEMENTS_AND_MISSING_FEATURES.md` | Future features list (will update to v2.0) |
| MY-JOURNEY.md | `/00-progress-advisor/MY-JOURNEY.md` | Progress log with V6→V7 transition documented |

---

## Technical Architecture

### Current V7 Pipeline Flow

```
Gmail Inbox
    ↓
Pre-Chunk 0 (Email Receiver & Client Identifier)
    ↓
Chunk 0 (Folder Initialization)
    ↓
Chunk 2 (Text Extraction)
    ↓
Chunk 2.5 (GPT-4 Classification + Tracker Update)
    ↓
Final Destination Folders
```

### V8 Enhanced Chunk 2.5 Flow (Planned)

```
Chunk 2.5 (Current: 18 nodes → V8: 24 nodes)

Trigger → Build Tier 1 Prompt → GPT-4 Tier 1 API Call → Parse Tier 1 + Build Tier 2 Prompt
    ↓
GPT-4 Tier 2 API Call → Parse Tier 2 Result → Action Mapper (CORE vs SECONDARY)
    ↓
Rename File with Confidence → Lookup Client in Tracker → Validate
    ↓
IF (CORE vs SECONDARY routing)
    ↓                           ↓
CORE Path:                 SECONDARY Path:
- Update Tracker           - Skip Tracker
- Move to specific folder  - Move to holding folder
- Send success response    - Send success response
```

### V8 Node Modifications

**6 New Nodes:**
1. `http-openai-2` - Tier 2 GPT-4 API call
2. `code-tier2-parse` - Parse Tier 2 classification result
3. `code-action-mapper` - Determine CORE vs SECONDARY action type
4. `drive-rename` - Rename file with type + confidence
5. `code-holding-folder` - Map SECONDARY types to holding folders (may merge with code-action-mapper)

**4 Modified Nodes:**
1. `code-1` - Build Tier 1 prompt (was single-pass 5-type prompt)
2. `code-2` - Parse Tier 1 + build dynamic Tier 2 prompt (was single parse)
3. `code-4` - Extended folder mapping for 38 types + holding folders
4. `code-8` - Conditional tracker update (only for CORE types)

---

## V8 Document Type Taxonomy (38 Total Types)

### CORE Types (4) - Move to Specific Folders + Update Tracker
1. **01_Projektbeschreibung** → Folder: 01_Expose, Status: Status_Expose
2. **03_Grundbuchauszug** → Folder: 02_Grundbuch, Status: Status_Grundbuch
3. **10_Bautraegerkalkulation_DIN276** → Folder: 03_Calculation, Status: Status_Calculation
4. **36_Exit_Strategie** → Folder: 04_Exit_Strategy, Status: Status_Exit_Strategy

### SECONDARY Types (34) - Move to Holding Folders, No Tracker Update

**OBJEKTUNTERLAGEN (11 secondary types):**
02_Kaufvertrag, 04_Eintragungsbewilligungen, 05_Bodenrichtwert, 06_Baulastenverzeichnis, 07_Altlastenkataster, 08_Baugrundgutachten, 09_Lageplan, 15_Flaechenberechnung_DIN277, 16_GU_Werkvertraege, 17_Bauzeichnungen, 18_Baugenehmigung
→ Holding folder: `_Holding_Property`

**WIRTSCHAFTLICHE_UNTERLAGEN (12 types):**
11_Verkaufspreise, 12_Bauzeitenplan_Liquiditaet, 13_Vertriebsweg, 14_Bau_Ausstattungsbeschreibung, 19_Teilungserklaerung, 20_Versicherungen, 21_Muster_Verkaufsvertrag, 23_Umsatzsteuervoranmeldung, 24_BWA, 25_Jahresabschluss, 26_Finanzierungsbestaetigung, 27_Darlehensvertrag
→ Holding folder: `_Holding_Financial`

**RECHTLICHE_UNTERLAGEN (6 types):**
28_Gesellschaftsvertrag, 29_Handelsregisterauszug, 30_Gewerbeanmeldung, 31_Steuer_ID, 32_Freistellungsbescheinigung, 33_Vollmachten
→ Holding folder: `_Holding_Legal`

**SONSTIGES (5 secondary types):**
22_Gutachterauftrag, 34_Korrespondenz, 35_Sonstiges_Allgemein, 37_Others, 38_Unknowns
→ Holding folder: `_Holding_Misc`

---

## V8 Filename Format

### New Format
```
{typeCode}_{clientName}_{confidence}pct.{extension}
```

**Examples:**
- `CORE_expose_villa_martens_95pct.pdf` (CORE type - visual prefix)
- `purchase_agreement_villa_martens_88pct.pdf` (SECONDARY type)
- `REVIEW_unknown_villa_martens_45pct.pdf` (LOW_CONFIDENCE)

**Confidence Calculation:**
- Combined confidence = `(tier1Confidence + tier2Confidence) / 2`
- Example: Tier 1 = 92%, Tier 2 = 88% → Combined = 90%

---

## V8 Future Features (Deferred Post-Production)

**Document Location:** `/02-operations/technical-builds/eugene/IMPROVEMENTS_AND_MISSING_FEATURES_v2.0_20260112.md` (to be created in Phase 0)

### 1. Version Detection & Archiving
- **What:** Detect if document is v1, v2, v3 of same document and archive old versions
- **Estimated Effort:** 6-8 hours
- **When:** After Eugene uses V8 for 1-2 months

### 2. Processing Log Sheet
- **What:** Dedicated Google Sheet tracking every document processed
- **Estimated Effort:** 3-4 hours
- **When:** If Eugene needs detailed audit trail

### 3. Confidence Score Tracking Dashboard
- **What:** Separate sheet aggregating confidence scores
- **Estimated Effort:** 4-5 hours
- **When:** If Eugene wants analytics on accuracy trends

### 4. Re-classification Workflow
- **What:** Allow re-submit from 38_Unknowns for re-classification
- **Estimated Effort:** 6-8 hours
- **When:** If 38_Unknowns folder gets >5 documents/month

### 5. Batch Confidence Reporting
- **What:** Weekly/monthly email with classification statistics
- **Estimated Effort:** 5-6 hours
- **When:** After 20+ documents processed

### 6. Multi-language Support
- **What:** Support for English documents
- **Estimated Effort:** 8-10 hours
- **When:** If Eugene starts receiving English documents

---

## V7 Performance Metrics (Current Production)

### Execution Times
- **Pre-Chunk 0:** ~5-8 seconds
- **Chunk 2:** ~2-3 seconds
- **Chunk 2.5:** ~5-8 seconds
- **Total End-to-End:** ~15-20 seconds

### V8 Projected Performance
- **Chunk 2.5 (V8):** ~8-12 seconds (+50% due to 2 API calls)
- **Total End-to-End:** ~18-25 seconds (+20-25%)

### Resource Usage
- **AI Model (V7):** GPT-4 Turbo (1 API call per document)
- **AI Model (V8):** GPT-4 Turbo (2 API calls per document)
- **Cost per Document (V7):** $0.03-0.05
- **Cost per Document (V8):** $0.05-0.08 (+60%)
- **Monthly Estimate (15 deals, V7):** $1-2/month
- **Monthly Estimate (15 deals, V8):** $1.50-3/month
- **Annual Estimate (V8):** $18-36/year (vs $12-24 for V7)

**Verdict:** Acceptable cost increase for resilience and accuracy improvements

---

## V7 Test Results (Production Verification)

### Execution #1760 (2026-01-12 09:53 UTC)
- **Status:** ✅ SUCCESS
- **Duration:** 16 seconds
- **Test Document:** 251103_Kaufpreise Schlossberg.pdf
- **Document Type:** Digital PDF (2,249 characters extracted)
- **Classification Result:** "Calculation" (85% confidence)
- **Reasoning:** "The document includes detailed financial analysis and calculations related to the sales prices of apartment units"
- **Client:** villa_martens
- **Tracker Update:** Status_Calculation = "✓"
- **File Movement:** Moved to 03_Calculation folder

**Pipeline Flow Verified:**
1. ✅ Gmail Trigger received test email
2. ✅ Filtered PDF attachment
3. ✅ Uploaded to temp folder
4. ✅ Downloaded and extracted text
5. ✅ AI extracted client: "Villa Martens" → "villa_martens"
6. ✅ Looked up in Client_Registry: FOUND
7. ✅ Moved to villa_martens/_Staging
8. ✅ Chunk 2: OCR detection (not needed, digital PDF)
9. ✅ Chunk 2.5: GPT-4 classification + tracker update
10. ✅ Client_Tracker updated with ✓
11. ✅ File moved to final location

---

## Current State Summary

**Version:** V7 Phase 1 (Production Ready)
**Next Version:** V8 (2-Tier Classification - In Planning)
**Phase:** Planning → Implementation
**Environment:** n8n (self-hosted), Google Cloud/Digital Ocean

**V7 Status:**
- ✅ All 4 workflows active and functional
- ✅ End-to-end test successful
- ✅ Client_Tracker restructured (43 columns)
- ✅ 5 critical fixes resolved
- ✅ Workflows backed up to v7_phase_one/

**V8 Status:**
- 🎯 Complete implementation plan written
- 🎯 Ready to begin Phase 0 (setup)
- 🎯 Estimated effort: 16-23 hours
- 🎯 Estimated calendar time: 4-6 days (4 hours/day)

---

## Next Steps (V8 Implementation)

**Immediate Next Actions:**

1. **Exit Plan Mode** - Complete V8 planning session
2. **Begin Phase 0** - Create v8_phase_one folder structure
3. **Update IMPROVEMENTS document** - Copy from archive, add V8 future features
4. **Create V8 changelog file** - Track all node modifications

**Then proceed sequentially:**
5. Phase 1: Infrastructure (holding folders, AMA_Folder_IDs updates)
6. Phase 2-4: Incremental node modifications (1 at a time with exports)
7. Phase 5: Automated testing (5 test cases via webhook)
8. Phase 6: Production deployment (deactivate V7, activate V8)

**Critical Success Criteria:**
- ✅ All 38 document types correctly classified
- ✅ CORE types maintain 100% success rate
- ✅ SECONDARY types identifiable from filenames
- ✅ Tier 1/2 accuracy >85%
- ✅ <25% latency increase (<25 seconds end-to-end)
- ✅ V7 backup ready for rollback

---

## References

**Current Session:**
- V8 Plan File: `/Users/swayclarke/.claude/plans/polished-singing-peacock.md`
- PROJECT_STATE v1.8: `PROJECT_STATE_v1.8_20260112.md`
- VERSION_LOG: `VERSION_LOG.md` (v1.5 as of 2026-01-05)

**V7 Backups:**
- Location: `/02-operations/technical-builds/eugene/N8N_Blueprints/v7_phase_one/`
- Files: pre_chunk_0, chunk_0, chunk_2, chunk_2.5 (all v7.0_20260112.json)

**Archives:**
- Location: `/02-operations/technical-builds/eugene/N8N_Blueprints/.archive/`
- Folders: v5_phase1/, v6_phase1/, v6_phase1_eugene_intermediate/

**Future Features:**
- Current location: `.archive/v4_phase1/IMPROVEMENTS_AND_MISSING_FEATURES.md` (v1.0)
- Will update to: `IMPROVEMENTS_AND_MISSING_FEATURES_v2.0_20260112.md` in Phase 0

---

**Document Version:** v1.9
**Generated:** 2026-01-12 17:58:53 CET
**Author:** Claude Code (Sway's automation assistant)
**Purpose:** Final V8 planning session backup with agent IDs and complete project state

---

## Quick Restart Guide

**To resume V8 implementation after session restart:**

1. Read this file for complete context
2. Read V8 plan: `/Users/swayclarke/.claude/plans/polished-singing-peacock.md`
3. Start with Phase 0 setup (create v8_phase_one folder)
4. Use solution-builder-agent for node modifications (≥3 nodes)
5. Use test-runner-agent for automated testing (Phase 5)
6. Keep V7 workflows active until V8 fully tested

**Agent Resume (if available):**
- Plan agent ID: (completed - see plan file)
- Explore agent IDs: (completed - taxonomy found)

**No agents need resuming - ready to begin fresh V8 implementation.**
