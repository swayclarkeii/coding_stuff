  # File Flow Architecture Decision
**Date:** 2026-01-08
**Context:** Chunk 2 download failure due to Pre-Chunk 0 moving files
**Decision needed:** File location strategy for multi-chunk processing

---

## Current Problem

**Execution #592 Error:**
- Pre-Chunk 0 downloads PDF and extracts text
- Pre-Chunk 0 moves file to staging folder
- Chunk 2 tries to download same file ID → 404 (file moved, ID invalid)

---

## Three Architecture Options

### Option A: Pass Data Through Workflow Chain (RECOMMENDED)

**Design:**
```
Pre-Chunk 0:
1. Download PDF from Gmail
2. Extract text → `extractedText` field
3. Move file to staging
4. Pass extractedText + metadata to Chunk 2

Chunk 2:
1. Receive extractedText from Pre-Chunk 0
2. Skip download (already have text)
3. Process text (classify, analyze)
4. Pass results to Chunk 2.5
```

**Pros:**
✅ **No redundant downloads** - Extract once, pass data forward
✅ **No file location tracking** - Data flows through workflows, not file references
✅ **Efficient** - Each chunk processes data, doesn't re-fetch
✅ **Scalable** - Works for 5+ chunks without complexity
✅ **Already implemented** - Pre-Chunk 0 already extracts `extractedText`

**Cons:**
❌ Large files increase workflow memory (mitigated: text is small, not binary)

**Downstream Impact (Chunks 2.5, 3, 4, 5):**
- ✅ Each chunk receives data from previous chunk
- ✅ No "where is the file?" issues
- ✅ Clear data contracts between chunks
- ❌ Must maintain field names across all chunks

**Implementation:**
- ✅ Already 90% done - Pre-Chunk 0 creates `extractedText`
- ✅ Chunk 2 just needs to use `extractedText` instead of re-downloading
- ✅ Remove "Download PDF" node from Chunk 2

---

### Option B: Keep File in Original Location Until All Processing Done

**Design:**
```
Pre-Chunk 0:
1. Download PDF from Gmail → Store in TEMP folder
2. Extract text
3. DO NOT move file yet
4. Pass file_id + extractedText to Chunk 2

Chunk 2:
1. Download from TEMP folder using file_id
2. Process text
3. Pass to Chunk 2.5

Chunk 5 (Final):
1. Move file from TEMP to final location
```

**Pros:**
✅ Single source of truth for file location
✅ Any chunk can access original file if needed

**Cons:**
❌ Files sit in TEMP longer (inbox clutter)
❌ Each chunk needs file_id tracking
❌ Risk of TEMP folder growing indefinitely
❌ Multiple chunks downloading same file (redundant API calls)
❌ Complexity increases with each new chunk

**Downstream Impact:**
- ⚠️ Chunk 2.5 needs to know file is still in TEMP
- ⚠️ Chunk 3 needs to know file is still in TEMP
- ⚠️ Chunk 4 needs to know file is still in TEMP
- ❌ Every new chunk adds "where is the file?" logic
- ❌ Single point of failure - if TEMP is cleared, all chunks break

---

### Option C: Progressive File Movement Through Stages

**Design:**
```
Pre-Chunk 0: Gmail → /TEMP/
Chunk 1: /TEMP/ → /STAGING/
Chunk 2: /STAGING/ → /PROCESSING/
Chunk 2.5: /PROCESSING/ → /PROCESSING/ (in place)
Chunk 3: /PROCESSING/ → /READY_FOR_ANALYSIS/
Chunk 4: /READY_FOR_ANALYSIS/ → /ANALYZED/
Chunk 5: /ANALYZED/ → /FINAL/
```

**Pros:**
✅ Clear progression (file location = workflow stage)
✅ Can visually track where in process each file is

**Cons:**
❌ Each chunk must know previous chunk's output location
❌ Tight coupling between chunks (change one, update all downstream)
❌ File location becomes workflow state (fragile)
❌ Each move operation is API call (slower, costs operations)
❌ If chunk fails mid-way, file is "lost" in interim location

**Downstream Impact:**
- ❌ Chunk 2.5 depends on Chunk 2's output location
- ❌ Chunk 3 depends on Chunk 2.5's output location
- ❌ Change location in one chunk → update all downstream chunks
- ❌ Debugging: "Where did the file end up?" becomes common question

---

## Recommendation: Option A (Pass Data Through Chain)

### Why This is Best for Your System

**1. Aligns with Current Architecture**
- Pre-Chunk 0 already extracts `extractedText` (you did this in Phase 1)
- Chunk 2 integration already passes 7 fields including `extractedText`
- You're 90% there - just need Chunk 2 to use existing data

**2. Scales to 5+ Chunks**
Each chunk becomes a pure function:
```javascript
Chunk 2: (extractedText, metadata) → (classification, confidence)
Chunk 2.5: (classification, confidence) → (validation_result)
Chunk 3: (validation_result) → (analysis_report)
Chunk 4: (analysis_report) → (deal_score)
Chunk 5: (deal_score) → (final_recommendation)
```

**3. No Location Tracking Issues**
- File moves to final location early (Pre-Chunk 0)
- All subsequent chunks process data, not files
- Clear separation: Physical storage vs. Data processing

**4. Efficient and Fast**
- No redundant downloads (1 download vs. 5+ downloads)
- No API calls for file movement between chunks
- Faster execution (no I/O bottlenecks)

**5. Testable**
- Each chunk can be tested with mock data
- No dependency on file system state
- Easy to create test harness (see Part 2)

---

## Implementation Plan for Option A

### Step 1: Fix Chunk 2 "Normalize Input" Node

**Current (BROKEN):**
```javascript
// Tries to download file that was already moved
const file = await downloadFile(item.id);
```

**Fixed:**
```javascript
// Use extractedText passed from Pre-Chunk 0
const extractedText = item.extractedText || '';
const hasExtractedText = extractedText.trim().length > 100;

if (hasExtractedText) {
  // Use existing text
  return { extractedText, source: 'pre-chunk-0' };
} else {
  // Edge case: Text extraction failed in Pre-Chunk 0
  // Option 1: Try to download and re-extract
  // Option 2: Flag as error and skip
  return { error: 'No text available', needsManualReview: true };
}
```

### Step 2: Remove "Download PDF" Node from Chunk 2

Since Pre-Chunk 0 already extracted text and passed it, Chunk 2 doesn't need to download anything.

**Chunk 2 New Flow:**
```
Workflow Trigger (receives data from Pre-Chunk 0)
  ↓
Normalize Input (use extractedText from input)
  ↓
Classify Document (OpenAI call)
  ↓
Calculate Confidence
  ↓
Return classification + confidence
```

### Step 3: Establish Data Contract

**Pre-Chunk 0 → Chunk 2:**
```javascript
{
  fileId: "...",              // For reference only
  fileName: "...",            // For logging
  client_normalized: "...",   // For folder structure
  extractedText: "...",       // ✅ TEXT DATA (not file reference)
  extractionMethod: "digital_pre_chunk",
  textLength: 12543,
  stagingPath: "..."          // File is already here, don't move again
}
```

**Chunk 2 → Chunk 2.5:**
```javascript
{
  fileId: "...",
  fileName: "...",
  extractedText: "...",       // Pass forward
  documentType: "Grundbuch",  // ✅ NEW DATA from Chunk 2
  confidence: 0.95,           // ✅ NEW DATA from Chunk 2
  classification_timestamp: "..."
}
```

**Chunk 2.5 → Chunk 3:**
```javascript
{
  ...previousData,            // Pass everything forward
  validation_result: "...",   // ✅ NEW DATA from Chunk 2.5
  validation_issues: []       // ✅ NEW DATA from Chunk 2.5
}
```

---

## Comparison: Downstream Complexity

### Option A: Pass Data (RECOMMENDED)
```
Chunk 2.5 needs to know: Previous chunk's output fields
Chunk 3 needs to know: Previous chunk's output fields
Chunk 4 needs to know: Previous chunk's output fields
Chunk 5 needs to know: Previous chunk's output fields

Complexity per new chunk: LOW (just define data contract)
Breaking changes: RARE (add new fields, don't remove old ones)
```

### Option B: Keep in Original Location
```
Chunk 2.5 needs to know: File is in TEMP, file_id
Chunk 3 needs to know: File is in TEMP, file_id
Chunk 4 needs to know: File is in TEMP, file_id
Chunk 5 needs to know: File is in TEMP, file_id, MOVE FILE TO FINAL

Complexity per new chunk: MEDIUM (track file location + download logic)
Breaking changes: FREQUENT (if TEMP location changes, all chunks break)
```

### Option C: Progressive Movement
```
Chunk 2.5 needs to know: Chunk 2 output location, download, move to next location
Chunk 3 needs to know: Chunk 2.5 output location, download, move to next location
Chunk 4 needs to know: Chunk 3 output location, download, move to next location
Chunk 5 needs to know: Chunk 4 output location, download, move to FINAL

Complexity per new chunk: HIGH (download + move logic in every chunk)
Breaking changes: VERY FREQUENT (change any location, update all downstream)
```

---

## Risk Analysis

### Option A Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Large text data in workflow memory | Low | Low | Text is small (~50KB max per PDF) |
| Field name mismatch between chunks | Medium | Medium | Establish data contracts, use validation |
| Binary data loss | Low | Medium | Store file once, reference by path if needed later |

### Option B Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| TEMP folder cleanup breaks all chunks | High | Critical | Must coordinate cleanup with all chunks |
| File location tracking failure | Medium | High | Complex logic to track where file is |
| Redundant downloads slow system | High | Medium | Each chunk downloads same file (inefficient) |

### Option C Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Location change breaks downstream | High | Critical | Tight coupling, one change breaks all |
| File "lost" between stages | Medium | High | If chunk fails, file stuck in interim location |
| Complex debugging | High | Medium | "Where is the file?" becomes frequent question |

---

## Decision: Option A (Pass Data Through Chain)

**Rationale:**
1. ✅ Lowest complexity for 5+ chunks
2. ✅ Least breaking changes over time
3. ✅ Most efficient (no redundant operations)
4. ✅ Already 90% implemented
5. ✅ Easiest to test (pure functions)
6. ✅ Clear separation: storage vs. processing

**Next Steps:**
1. Update Chunk 2 "Normalize Input" to use `extractedText` from input
2. Remove "Download PDF" node from Chunk 2
3. Test Chunk 2 with existing execution data
4. Document data contract between chunks
5. Apply same pattern to Chunks 2.5, 3, 4, 5

---

## References
- Build Proposal: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/build_proposal_v1.0_2025-12-10.md`
- Workflow Audit: `/Users/swayclarke/coding_stuff/WORKFLOW_AUDIT_FIXES_2026-01-08.md`
- Chunk 2 Integration: `/Users/swayclarke/coding_stuff/chunk2-integration-summary.md`
