# Eugene Document Organizer - Summary v2.0
**Date:** January 19, 2026
**Status:** V10 Design Complete, Chunk 2.5 Bugs Identified

---

## Current State

### Version History
- **V8** (Jan 3-16): Document AI OCR approach - Working, archived
- **V9** (Jan 17-18): Claude Vision integration - Working, 69% faster than V8
- **V10** (Jan 19): Batch analysis architecture - In design phase

### Active Workflows
| Workflow | ID | Status |
|----------|-----|--------|
| AMA Pre-Chunk 0 - REBUILT v1 | YGXWjWcBIk66ArvT | ACTIVE |
| AMA Chunk 0: Folder Initialization | zbxHkXOoD1qaz6OS | ACTIVE |
| Chunk 2.5: Client Document Tracking | okg8wTqLtPUwjQ18 | ACTIVE |
| AMA Chunk 2: Text Extraction | qKyqsL64ReMiKpJ4 | INACTIVE (bypassed by V9) |

---

## V10 Architecture: Batch Analysis

### Problem Solved
V9 analyzes documents individually → Unreliable client/project identification
V10 analyzes documents in batches → Find "common denominator" identifier

### Core Flow
```
EMAIL ARRIVES WITH ATTACHMENTS
         │
         ▼
┌────────────────────────────┐
│ PHASE 1: INTAKE            │
│ - Extract email metadata   │
│ - Filter PDF/ZIP files     │
│ - Count: Single vs Multiple│
└────────────────────────────┘
         │
         ▼
┌────────────────────────────┐
│ PHASE 2: SEQUENTIAL ANALYSIS│
│ FOR EACH PDF (one by one): │
│ - Download from temp       │
│ - Convert to Base64        │
│ - Claude Vision extract ID │
│ - Store result in array    │
│ ALSO: Parse email body     │
└────────────────────────────┘
         │
         ▼
┌────────────────────────────┐
│ PHASE 3: BATCH VOTING      │
│ - Aggregate all identifiers│
│ - Find common denominator  │
│ - Weight by confidence     │
│ - Bonus for email body match│
│ - Calculate final score    │
└────────────────────────────┘
         │
         ▼
┌────────────────────────────┐
│ PHASE 4: REGISTRY MATCHING │
│ PRIMARY: project_name      │
│ SECONDARY: sender_email    │
│ Routes:                    │
│ - EXISTING (found)         │
│ - NEW_FROM_KNOWN (email ok)│
│ - COMPLETELY_NEW           │
└────────────────────────────┘
         │
         ▼
┌────────────────────────────┐
│ PHASE 5: ROUTING + FLAG    │
│ Flag conditions:           │
│ - Single doc, new sender   │
│ - Confidence < 0.6         │
│ - Project/email mismatch   │
│ Send review email if FLAG  │
└────────────────────────────┘
```

### Key Design Decisions
1. **Single doc from new sender**: Process it, but FLAG and send review email to Eugene
2. **Sequential analysis**: Analyze PDFs one-by-one, then vote at the end (not all at once)
3. **Project name priority**: If project matches but email doesn't, use project name
4. **Email body parsing**: Parse email body/signature for project/client mentions as bonus validation

### Registry Schema Changes
**New column needed:** `sender_email` for matching

---

## BLOCKER: Chunk 2.5 Bugs Identified

### Bug 1: Field Name Mismatch (Confidence)
**Location:** "Find Client Row and Validate" node
**Problem:**
```javascript
const confidence = mainData.documentClassificationConfidence || 0;
if (confidence < 70) { // triggers "Low confidence" error }
```
- Classification sets: `tier2Confidence`, `combinedConfidence`
- Validation looks for: `documentClassificationConfidence`
- Field doesn't exist → defaults to 0 → always triggers error

### Bug 2: Tracker Only Updates for CORE Types
**Location:** "Determine Action Type" node
**Logic:**
- `isCoreType === true` → `trackerUpdate: true` (updates Client_Tracker)
- `isCoreType === false` → `trackerUpdate: false` (SKIPS tracker)

**CORE types (update tracker):**
- 01_Projektbeschreibung (Exposé)
- 03_Grundbuchauszug (Land Register)
- 10_Bautraegerkalkulation_DIN276 (Developer Calculation)

**SECONDARY types (skip tracker):**
- 17_Bauzeichnungen (Construction Drawings) - and all others

**Impact:** Non-CORE documents are filed but never show in Client_Tracker with check marks.

---

## Next Steps

### Immediate (Before V10 Build)
1. [ ] Fix Chunk 2.5 confidence field mismatch
2. [ ] Decide: Should ALL types update tracker, or just CORE?
3. [ ] Test Chunk 2.5 fixes

### V10 Implementation
1. [ ] Build Phase 1-2 nodes (intake + sequential analysis)
2. [ ] Build Phase 3 nodes (batch voting)
3. [ ] Build Phase 4-5 nodes (registry matching + routing)
4. [ ] Add sender_email column to registry
5. [ ] Test with Gmail +alias approach

---

## File Locations

| Item | Path |
|------|------|
| V10 Node Design | `N8N_Blueprints/v10_phase_1/docs/V10_PRECHUNK0_DESIGN.md` |
| Session Notes | `N8N_Blueprints/v10_phase_1/docs/SESSION_SUMMARY_2026-01-19.md` |
| V9 Backups | `N8N_Blueprints/.archive/v9_phase_1/backups/` |
| This Summary | `compacting-summaries/summary_v2.0_2026-01-19.md` |

---

**Version:** 2.0
**Previous:** v1.0 (Jan 14) - archived to `.archive/`
