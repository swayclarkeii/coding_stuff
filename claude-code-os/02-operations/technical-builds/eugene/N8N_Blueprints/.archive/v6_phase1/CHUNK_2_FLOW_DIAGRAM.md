# Chunk 2 Workflow Flow - Option A Implementation

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CHUNK 2: TEXT EXTRACTION                           │
│                         (Document Organizer V4)                            │
└─────────────────────────────────────────────────────────────────────────────┘

Input from Pre-Chunk 0 (via Chunk 1):
{
  id, name, mimeType, size,
  client_normalized, staging_folder_id,
  extractedText: "..." ← ALREADY EXTRACTED
  extractionMethod: "digital_pre_chunk"
}
                              ↓
        ╔═══════════════════════════════════════╗
        ║   Execute Workflow Trigger            ║
        ╚═══════════════════════════════════════╝
                              ↓
        ╔═══════════════════════════════════════╗
        ║   Normalize Input                     ║
        ║   • Check extractedText length        ║
        ║   • If > 100 chars: needsReExtraction = false ║
        ║   • If ≤ 100 chars: needsReExtraction = true  ║
        ╚═══════════════════════════════════════╝
                              ↓
        ╔═══════════════════════════════════════╗
        ║   IF Has Extracted Text               ║ ← NEW NODE
        ║   Condition: needsReExtraction = false║
        ╚═══════════════════════════════════════╝
                              ↓
            ┌─────────────────┴─────────────────┐
            │                                   │
         [TRUE]                              [FALSE]
    (Has extracted text)                 (Needs re-extraction)
         99% of cases                         1% edge cases
            │                                   │
            ↓                                   ↓
    ╔═══════════════════╗           ╔═══════════════════╗
    ║ Normalize Output  ║           ║  Download PDF     ║
    ║                   ║           ║  (from Google     ║
    ║ DIRECT PATH       ║           ║   Drive)          ║
    ║ • No download     ║           ╚═══════════════════╝
    ║ • No extraction   ║                     ↓
    ║ • Just pass data  ║           ╔═══════════════════╗
    ║   forward         ║           ║ Extract PDF Text  ║
    ╚═══════════════════╝           ╚═══════════════════╝
            │                                   ↓
            │                       ╔═══════════════════╗
            │                       ║ Detect Scan vs    ║
            │                       ║ Digital           ║
            │                       ║ • Check text len  ║
            │                       ║ • Set needsOcr    ║
            │                       ╚═══════════════════╝
            │                                   ↓
            │                       ╔═══════════════════╗
            │                       ║ IF Needs OCR      ║
            │                       ╚═══════════════════╝
            │                                   ↓
            │               ┌───────────────────┴────────────────┐
            │               │                                    │
            │            [TRUE]                              [FALSE]
            │        (Is scanned)                         (Is digital)
            │               │                                    │
            │               ↓                                    │
            │    ╔═══════════════════╗                          │
            │    ║ AWS Textract OCR  ║                          │
            │    ╚═══════════════════╝                          │
            │               ↓                                    │
            │    ╔═══════════════════╗                          │
            │    ║ Process OCR Result║                          │
            │    ╚═══════════════════╝                          │
            │               │                                    │
            │               └────────────────┬───────────────────┘
            │                                ↓
            └──────────────────────→ ╔═══════════════════╗
                                     ║ Normalize Output  ║
                                     ║                   ║
                                     ║ Merge all paths:  ║
                                     ║ • Direct          ║
                                     ║ • OCR             ║
                                     ║ • Digital         ║
                                     ╚═══════════════════╝
                                               ↓
Output to downstream chunks:
{
  fileId, fileName, extractedText,
  isScanned, ocrUsed, extractionMethod,
  chunk2_path: "direct_from_pre_chunk" | "ocr_extraction" | "digital_extraction"
}
```

---

## Path Breakdown

### Path 1: Direct from Pre-Chunk 0 (99% of cases)
**Nodes executed:** 4
1. Execute Workflow Trigger
2. Normalize Input
3. IF Has Extracted Text (TRUE branch)
4. Normalize Output

**Time saved:** ~3-5 seconds (no download, no extraction)
**API calls saved:** 1 Google Drive download

---

### Path 2: Fallback - Digital PDF (Edge case)
**Nodes executed:** 8
1. Execute Workflow Trigger
2. Normalize Input
3. IF Has Extracted Text (FALSE branch)
4. Download PDF
5. Extract PDF Text
6. Detect Scan vs Digital
7. IF Needs OCR (FALSE branch)
8. Normalize Output

**When used:** extractedText missing or < 100 chars
**Outcome:** Extract text from digital PDF

---

### Path 3: Fallback - Scanned PDF (Edge case)
**Nodes executed:** 10 (all nodes)
1. Execute Workflow Trigger
2. Normalize Input
3. IF Has Extracted Text (FALSE branch)
4. Download PDF
5. Extract PDF Text
6. Detect Scan vs Digital
7. IF Needs OCR (TRUE branch)
8. AWS Textract OCR
9. Process OCR Result
10. Normalize Output

**When used:** extractedText missing AND PDF is scanned
**Outcome:** Use AWS Textract OCR for text extraction

---

## Key Decision Points

### Decision 1: Has Extracted Text?
**Node:** "IF Has Extracted Text"
**Condition:** `$json.needsReExtraction === false`
- **TRUE:** Text already exists, skip download → go direct to output (Path 1)
- **FALSE:** No text, need to download and extract (Path 2 or 3)

### Decision 2: Needs OCR?
**Node:** "IF Needs OCR"
**Condition:** `$json.needsOcr === true`
- **TRUE:** Scanned PDF, use AWS Textract (Path 3)
- **FALSE:** Digital PDF, use standard extraction (Path 2)

---

## Benefits of Option A

✅ **Efficiency:** 99% of executions use only 4 nodes (vs. 10 before)
✅ **No 404 errors:** File already moved to staging, we don't re-download
✅ **API call reduction:** 1 less Google Drive download per execution
✅ **Faster execution:** ~3-5 seconds saved per file
✅ **Clear debugging:** `chunk2_path` shows which path was used
✅ **Scalable:** Same pattern works for Chunks 2.5, 3, 4, 5

---

## Monitoring Tips

### Check Execution Logs For:

1. **Path distribution:**
   - Count of `chunk2_path: "direct_from_pre_chunk"` (should be ~99%)
   - Count of `chunk2_path: "digital_extraction"` (should be rare)
   - Count of `chunk2_path: "ocr_extraction"` (should be rare)

2. **Node execution counts:**
   - "Download PDF" executions (should be <1%)
   - "AWS Textract OCR" executions (should be minimal)

3. **Error patterns:**
   - No more 404 errors on "Download PDF" (was the original issue)
   - Any extraction failures in Pre-Chunk 0 (would trigger fallback)

### Success Indicators:

✅ Most executions show 4-node path (Trigger → Normalize Input → IF → Output)
✅ No 404 errors in execution logs
✅ Execution time reduced by ~3-5 seconds on average
✅ Google Drive API calls reduced by ~50% (1 download in Pre-Chunk 0 vs. 2 before)

---

## Data Contract Reminder

### Pre-Chunk 0 → Chunk 2:
```javascript
{
  // File identifiers
  id: string,
  name: string,
  mimeType: string,
  size: number,

  // Client context
  client_normalized: string,
  staging_folder_id: string,

  // Extracted text (THE KEY FIELD)
  extractedText: string,  // Already extracted in Pre-Chunk 0
  extractionMethod: "digital_pre_chunk" | "ocr_pre_chunk"
}
```

### Chunk 2 → Downstream:
```javascript
{
  // All input fields, plus:

  // Text extraction results
  extractedText: string,
  textLength: number,
  isScanned: boolean,
  ocrUsed: boolean,
  extractionMethod: string,

  // Processing metadata
  processedAt: string,
  chunk2_path: "direct_from_pre_chunk" | "digital_extraction" | "ocr_extraction",

  // Empty fields for downstream chunks
  documentType: null,
  confidence: null,
  projectName: null,
  normalizedProjectName: null
}
```

---

**Date:** 2026-01-08
**Implementation:** Option A (Pass Data Through Chain)
**Status:** ✅ Active and validated
