# Eugene AMA Document Organizer - Summary

**Version:** v9.0
**Last Updated:** January 25, 2026
**Status:** Production Ready - Major Updates (Claude Vision, Routing Fix, Test Mode)

---

## Agent IDs (Resume Work)

**CRITICAL:** Use these agent IDs to resume work in new conversations.

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| aaeb712 | server-ops-agent | Database fix + disk cleanup (100% disk full) | ✅ Complete |
| af2478a | server-ops-agent | Automated binaryData cleanup cron job setup | ✅ Complete |
| a469a55 | solution-builder-agent | Tracker update fix (Google Sheets API) | ✅ Complete |
| aca266b | solution-builder-agent | Routing logic fix (Core 4 vs Others) | ✅ Complete |
| a9087b3 | solution-builder-agent | Test workflow creation (Chunk 2.5 TEST MODE) | ✅ Complete |
| a1da42a | solution-builder-agent | Wait node + alwaysOutputData fixes (v8.1) | ✅ Complete |
| a6af989 | solution-builder-agent | Parse Tier 2 Result fileId fetching fix (v8.1) | ✅ Complete |
| a893b5b | solution-builder-agent | TypeVersion syntax mismatch fix (v8.0) | ✅ Complete |
| aebcfd0 | solution-builder-agent | File metadata preservation fix (v8.0) | ✅ Complete |

**Usage:** In new conversation: "Resume agent a469a55" or reference this summary

---

## Current To-Do List

### ✅ Completed (v9.0 Session - 2026-01-25)
- [x] Fixed n8n server disk full issue (100% → 62%)
- [x] Set up automated binaryData cleanup cron job (daily 2 AM)
- [x] Fixed JSON parsing error in "Parse Claude Tier 2 Response" (robust extraction)
- [x] Added Claude API rate limit protection (30s blocking sleep + 120s retry)
- [x] Fixed tracker update (was empty, now uses Google Sheets API)
- [x] Simplified routing logic (Core 4 → folders, everything else → Others)
- [x] Created test workflow "Chunk 2.5 - TEST MODE" for rapid iteration
- [x] Created questions list for Eugene meeting

### ✅ Completed (v8.1 - 2026-01-14)
- [x] Fixed Google Drive 404 error (metadata preservation)
- [x] Added Wait node after staging
- [x] Fixed Parse Tier 2 Result fileId fetching

### ⏳ Pending
- [ ] Review document type classification with Eugene
- [ ] Finalize document type → folder mapping
- [ ] Clarify Baubeschreibung vs Exposé classification
- [ ] Verify tracker column positions (D, E, F, G, H)
- [ ] Monitor 10-20 production executions
- [ ] Build automated V8 test runner workflow
- [ ] Add file existence validation before rename operations

### ⚠️ Known Issues
- Classification prompts may confuse similar document types (Baubeschreibung vs Exposé)
- Document types in tracker may not match 1:1 with folder structure
- Budget document classification unclear
- 38_Unknowns folder nodes are now unreachable (cleanup candidate)

---

## Key Decisions Made

### 1. Claude Vision Instead of GPT-4 (v9.0)
**Decision:** Use Claude claude-sonnet-4-20250514 for document classification instead of GPT-4
**Rationale:** Already integrated, consistent with other Sway workflows
**Impact:** Rate limit of 30,000 tokens/minute requires spacing between API calls

### 2. Core 4 Routing Simplification (v9.0)
**Decision:** Only Core 4 documents go to specific folders, ALL others go to 37_Others
**Rationale:** Simplify routing until document type mapping is finalized with Eugene
**Impact:** Reduces routing complexity, easier to modify Core 4 list

### 3. Google Sheets API for Tracker Updates (v9.0)
**Decision:** Use HTTP Request to Google Sheets API instead of n8n Google Sheets node
**Rationale:** Dynamic column updates not supported well by native node
**Impact:** More flexible, can update any column dynamically

### 4. Test Workflow for Rapid Iteration (v9.0)
**Decision:** Create separate "Chunk 2.5 - TEST MODE" workflow
**Rationale:** Full workflow takes 26 minutes, test mode runs in ~5 seconds
**Impact:** 312x faster testing iteration

### 5. 2-Tier Classification Architecture (v8.0)
**Decision:** Tier 1 (category) → Tier 2 (specific type) classification
**Rationale:** Better accuracy for document identification
**Impact:** ~5.7 seconds classification time per document

---

## Important IDs / Paths / Workflow Names

### n8n Workflows
| Workflow Name | ID | Purpose | Status |
|--------------|-----|---------|--------|
| Pre-Chunk 0 - REBUILT v1 | p0X9PrpCShIgxxMP | Email intake, PDF conversion, staging | ✅ Active |
| Chunk 2.5 - Client Document Tracking | okg8wTqLtPUwjQ18 | Claude Vision classification, routing | ✅ Active |
| Chunk 2.5 - TEST MODE | FL8cPoYixTTKXY8Z | Rapid testing without classification | ✅ Active |
| Test Email Sender | RZyOIeBy7o3Agffa | Send test PDFs via email | ✅ Active |
| Pre-Chunk 0 (Legacy) | YGXWjWcBIk66ArvT | Original email intake | ⚠️ Legacy |
| Chunk 2 | qKyqsL64ReMiKpJ4 | Text extraction, processing | ✅ Active |

### Google Sheets
| Spreadsheet Name | ID | Purpose |
|-----------------|-----|---------|
| AMA Client Document Tracker | 12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I | Track document receipt status |
| AMA_Folder_IDs | 1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm | Client folder ID mappings |

### Tracker Column Mapping
| Document Type | Tracker Column | Column Letter |
|---------------|----------------|---------------|
| 01_Projektbeschreibung | Status_Expose | D |
| 03_Grundbuchauszug | Status_Grundbuch | E |
| 10_Bautraegerkalkulation_DIN276 | Status_Calculation | F |
| 36_Exit_Strategie | Status_Exit_Strategy | G |
| (Always updated) | Last_Updated | H |

### Google Drive
| Folder Name | Purpose |
|-------------|---------|
| clients/[client_name]/_Staging | Files land here after Pre-Chunk 0 |
| clients/[client_name]/_Temp | Upload location |
| clients/[client_name]/01_Projektbeschreibung | Exposé documents |
| clients/[client_name]/37_Others | Non-Core-4 documents |

### Credentials
| Name | ID | Type |
|------|-----|------|
| Google Drive account | a4m50EefR3DJoU0R | googleDriveOAuth2Api |
| Google Sheets account | H7ewI1sOrDYabelt | googleSheetsOAuth2Api |
| Anthropic API key | (in HTTP Request) | Header Auth |

### File Paths
| File | Location | Purpose |
|------|----------|---------|
| VERSION_LOG.md | /eugene/VERSION_LOG.md | Version history and changelog |
| Questions for Eugene | /eugene/questions-for-eugene.md | Discussion items for client meeting |
| Routing Fix Summary | /eugene/IMPLEMENTATION_SUMMARY_Chunk2.5_Routing_Fix.md | Technical documentation |
| Test Mode Implementation | /oloxa/SwaysExpenseSystem/N8N_Blueprints/CHUNK_2.5_TEST_MODE_IMPLEMENTATION.md | Test workflow docs |

---

## Technical Architecture

### Document Processing Flow
```
Email Received (Gmail)
    ↓
Pre-Chunk 0 (p0X9PrpCShIgxxMP)
    ├── Extract attachments
    ├── Convert non-PDF to PDF (Gotenberg)
    ├── Move to _Staging folder
    └── Trigger Chunk 2.5
    ↓
Chunk 2.5 (okg8wTqLtPUwjQ18)
    ├── Download PDF from staging
    ├── Convert to Base64
    ├── Build Claude Tier 1 prompt
    ├── [30s wait] → Claude Vision Tier 1 Classification
    ├── Parse Tier 1 → Build Tier 2 prompt
    ├── [30s wait] → Claude Vision Tier 2 Classification
    ├── Parse Tier 2 → Route based on document type
    ├── Update Client_Tracker (Google Sheets API)
    └── Move file to destination folder
```

### Rate Limit Protection
- 30-second blocking sleep before each Claude API call
- 120-second retry wait if rate limit hit
- HTTP Request retry: 5 max attempts

### Core 4 Document Types
```javascript
const CORE_4_TYPES = [
  '01_Projektbeschreibung',      // Exposé
  '03_Grundbuchauszug',          // Grundbuch
  '10_Bautraegerkalkulation_DIN276',  // Calculation
  '36_Exit_Strategie'            // Exit Strategy
];
```

---

## Current State Summary

**Version:** v9.0 (v8.1 base + Claude Vision + Routing Fix + Test Mode)
**Phase:** Production Ready with pending refinements
**Classification:** Claude Vision (claude-sonnet-4-20250514)
**Processing Time:** ~60+ seconds per file (due to rate limit protection)

### Success Metrics (v8.1 baseline)
- Classification accuracy: 95%
- File rename success: 100%
- Metadata preservation: 100%
- Overall workflow: 100%

### Performance (v9.0)
- Wait time per file: ~60 seconds (rate limit protection)
- Total execution (4 files): ~26 minutes
- Test mode execution: ~5 seconds

---

## Next Steps

### Immediate (Before Next Eugene Meeting)
1. Review `/eugene/questions-for-eugene.md` with Eugene
2. Get master document type mapping table
3. Clarify Baubeschreibung, Budget classification
4. Confirm Core 4 list is correct

### Short-Term (This Week)
1. Update classification prompts based on Eugene feedback
2. Test with Chunk 2.5 TEST MODE workflow
3. Monitor 10-20 production executions
4. Optimize rate limit timing if possible

### Medium-Term
1. Add more document types to specific folder routing
2. Build automated test runner workflow
3. Add file existence validation before operations
4. Create monitoring alerts for systematic failures
5. Clean up unused 38_Unknowns nodes

---

## Server Status

### n8n Server (n8n.oloxa.ai)
- **Status:** Healthy
- **Disk:** 62% used (was 100%)
- **Automated Cleanup:** Daily 2 AM (files >7 days)
- **Disk Monitoring:** Daily 2:15 AM (warns at 80%)

---

## References

- VERSION_LOG: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/VERSION_LOG.md`
- Questions for Eugene: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/questions-for-eugene.md`
- Test Mode Docs: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/oloxa/SwaysExpenseSystem/N8N_Blueprints/CHUNK_2.5_TEST_MODE_IMPLEMENTATION.md`
- Server Diagnostics: `/Users/swayclarke/coding_stuff/server-diagnostics/2026-01-24-database-not-ready-disk-full-fix.md`

---

**Document Version:** summary_v9.0_2026-01-25.md
**Generated:** 2026-01-25 01:25 CET
**Author:** Claude Code (Sway's automation assistant)
