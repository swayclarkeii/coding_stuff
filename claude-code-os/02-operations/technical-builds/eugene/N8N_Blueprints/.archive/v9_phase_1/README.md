# Eugene Document Organizer v9 Phase 1 - Claude Vision Upgrade

**Implementation Date:** January 17, 2026
**Status:** Planned (not yet implemented)
**Purpose:** Replace OCR + AI classification with single Claude Vision call

---

## Overview

v9 Phase 1 represents a major architectural shift from the current OCR-based approach (v8) to a Vision AI-based approach using Claude Sonnet 4.5.

### Key Changes

**v8 (Current):**
```
Download PDF → Document AI OCR → Parse Response → Evaluate Quality → OpenAI GPT-4o Classification
```

**v9 (New):**
```
Download PDF → Convert PDF to Base64 → Claude Vision Extract Identifier → Normalize Output
```

---

## Implementation Plan

### Phase 2: Claude Vision Upgrade

#### Nodes to Add

1. **Convert PDF to Base64 Images**
   - Type: Code node
   - Purpose: Convert PDF binary to base64 for Claude Vision API
   - Position: After "Download PDF from Drive"

2. **Claude Vision Extract Identifier**
   - Type: HTTP Request node
   - Purpose: Call Anthropic API with document image
   - Model: claude-sonnet-4-20250514
   - Endpoint: https://api.anthropic.com/v1/messages

3. **Parse Claude Response**
   - Type: Code node
   - Purpose: Extract identifier from Claude response
   - Output: clientNormalized field

#### Nodes to Remove/Disable

1. ❌ Prepare Document AI Request
2. ❌ Call Document AI OCR
3. ❌ Parse Document AI Response
4. ❌ Evaluate Extraction Quality
5. ❌ AI Extract Client Name (OpenAI)

#### Connections to Update

- Disconnect: "Download PDF" → "Prepare Document AI Request"
- Connect: "Download PDF" → "Convert PDF to Base64"
- Connect: "Convert PDF to Base64" → "Claude Vision Extract Identifier"
- Connect: "Claude Vision Extract Identifier" → "Parse Claude Response"
- Connect: "Parse Claude Response" → "Normalize Client Name"

---

## Claude Vision Prompt

```
Extract the PROJECT or PROPERTY IDENTIFIER from this German real estate document.

Look for (in priority order):
1. Street address (e.g., 'Schloßbergstraße 13' → 'Schlossberg 13')
2. Project code (e.g., 'BV Propos' → 'Propos')
3. Property name (e.g., 'Villa Martens')
4. Company name (e.g., 'Propos GmbH' → 'Propos')

Rules:
- Normalize German: ß→ss, ä→ae, ö→oe, ü→ue
- Remove 'straße/str.' from addresses, keep number
- Return ONLY the identifier, nothing else
- If no identifier found, return: UNKNOWN
```

---

## Expected Improvements

### Accuracy
- **Better German understanding** - Claude trained on German legal/business docs
- **Visual context awareness** - Can interpret Grundbuch diagrams, floor plans, maps
- **Instruction following** - More reliable output format (just identifier, no explanation)

### Performance
- **Fewer API calls** - 1 call instead of 3 (OCR → Evaluate → Classification)
- **Faster processing** - Single round-trip vs multiple steps
- **Simpler pipeline** - Less code, fewer failure points

### Document Types Handled
| Type | v8 (OCR) | v9 (Vision) |
|------|----------|-------------|
| Clean PDFs | ✓ Text extraction | ✓ Better context |
| Scanned docs | ✓ OCR works | ✓ Better quality |
| Maps/Grundbuch | ✗ Labels only | ✓ Visual understanding |
| Mixed docs | △ Misses context | ✓ Full context |

---

## Testing Plan

### Phase 2 Verification

1. **Test with known documents:**
   - Schlossberg 13 document (previously worked in v8)
   - Documents with maps/diagrams
   - Multi-page documents
   - Scanned documents with stamps

2. **Expected results:**
   - ≥80% correct classification (vs 7% in v8)
   - Fewer "UNKNOWN" classifications
   - Accurate German text extraction
   - Proper address normalization

3. **Rollback criteria:**
   - Accuracy <50% (worse than random)
   - Vision API errors/timeouts
   - Cost >3x current OCR approach
   - Processing time >60 seconds per doc

---

## Phase 3: Batch Grouping (Future)

**After Phase 2 is stable**, add batch grouping:

### Option A: Extra Nodes in Pre-Chunk 0

Add 3-4 nodes after Claude Vision:

```
Claude Vision → Store to Temp Collection → Check if Last Doc → Find Common ID → Apply to All Batch
```

**How it works:**
1. Store each doc's identifier to Google Sheet (keyed by email ID)
2. Check if all attachments from that email are processed
3. Find most frequent identifier across all docs
4. Update any "UNKNOWN" docs with winning identifier

**Benefits:**
- Real-time processing
- Single workflow
- No separate scheduler needed

---

## Cost Comparison

### v8 (OCR-based)
- Google Document AI: $1.50 per 1000 pages
- OpenAI GPT-4o: ~$0.01 per classification
- **Total per doc:** ~$0.012

### v9 (Vision-based)
- Claude Vision: ~$0.003 per image
- **Total per doc:** ~$0.003

**Savings:** ~75% cost reduction

---

## Credentials Required

### Anthropic API
- **Key:** Already available in `~/.claude/.env.anthropic`
- **Model:** claude-sonnet-4-20250514
- **Authentication:** Header Auth (x-api-key)

### Existing (Still Needed)
- Google Drive OAuth (file download)
- Google Sheets (tracking)
- AWS Textract (fallback OCR if needed)

---

## Migration Steps

1. **Backup v8** ✅ Complete
2. **Create v9_phase_1 folder** ✅ Complete
3. **Implement Claude Vision nodes** 🔜 Next
4. **Test with sample docs** 🔜 Pending
5. **Compare accuracy vs v8** 🔜 Pending
6. **Deploy to production** 🔜 Pending
7. **Monitor for 1 week** 🔜 Pending
8. **Add batch grouping (Phase 3)** 🔜 Future

---

## Success Criteria

### Phase 2 Success
- [ ] Claude Vision integration working
- [ ] ≥80% classification accuracy
- [ ] <5% "UNKNOWN" rate
- [ ] German addresses properly normalized
- [ ] No regressions in v8 working cases

### Phase 3 Success (Future)
- [ ] Batch grouping implemented
- [ ] Multi-doc emails properly grouped
- [ ] <2% "UNKNOWN" rate
- [ ] Common identifiers detected accurately

---

## Related Documentation

- **v8 Backup:** `../v8_phase_1/README.md`
- **Implementation Plan:** `/Users/swayclarke/.claude/plans/giggly-cuddling-hartmanis.md`
- **n8n Patterns:** `/Users/swayclarke/coding_stuff/N8N_PATTERNS.md`
- **Credentials:** `/Users/swayclarke/coding_stuff/CREDENTIALS.md`

---

**Status:** Ready to begin implementation
**Next Action:** Build Claude Vision nodes in Pre-Chunk 0 workflow
