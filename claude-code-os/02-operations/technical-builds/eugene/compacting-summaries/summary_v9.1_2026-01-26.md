# Eugene AMA Document Organizer - Summary

**Version:** v9.1
**Last Updated:** January 26, 2026
**Status:** Production Ready - Infrastructure Stabilized, Tracker Mapping Pending

---

## Agent IDs (Resume Work)

**CRITICAL:** Use these agent IDs to resume work in new conversations.

### Recent Session (2026-01-25/26)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| a06ac33 | solution-builder-agent | Built Eugene Workflow Monitor (hourly checks) | ✅ Complete |
| a0340d3 | server-ops-agent | Server crash investigation (execution 5729) | ✅ Complete |
| ad50cf8 | server-ops-agent | Cleanup/swap fix attempt (SSH unresponsive) | ✅ Complete |

### Previous Sessions (v9.0 - Still Relevant)

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

**Usage:** In new conversation: "Resume agent a06ac33" or reference this summary

---

## Current To-Do List

### ✅ Completed (v9.1 Session - 2026-01-25/26)

- [x] Investigated execution 5727 silent failure (0 files processed)
- [x] Fixed Split In Batches disconnection (Output 1 → Download PDF)
- [x] Investigated execution 5729 crash (OOM kill)
- [x] Fixed server 100% disk full crisis (8.2GB freed → 65%)
- [x] Added 2GB swap space (prevents OOM kills)
- [x] Fixed cleanup cron (daily/7-day → every-4-hours/12-hour retention)
- [x] Fixed JSON parse error in skipTrackerUpdate scenario (execution 5738)
- [x] Added IF node "Should Update Tracker?" before HTTP Request
- [x] Created Eugene Workflow Monitor (ID: EKAOWgdA5FMZaQdW)
- [x] Documented tracker column structure confusion for Eugene meeting

### ✅ Completed (v9.0 Session - 2026-01-25)

- [x] Fixed n8n server disk full issue (100% → 62%)
- [x] Set up automated binaryData cleanup cron job (daily 2 AM)
- [x] Fixed JSON parsing error in "Parse Claude Tier 2 Response" (robust extraction)
- [x] Added Claude API rate limit protection (30s blocking sleep + 120s retry)
- [x] Fixed tracker update (was empty, now uses Google Sheets API)
- [x] Simplified routing logic (Core 4 → folders, everything else → Others)
- [x] Created test workflow "Chunk 2.5 - TEST MODE" for rapid iteration
- [x] Created questions list for Eugene meeting

### ⏳ Pending

- [ ] **CRITICAL:** Get Eugene to clarify tracker column structure (doubled columns)
- [ ] Rebuild complete column mapping after Eugene clarifies
- [ ] Fix wrong column positions (Last_Updated should be AQ, not H)
- [ ] Activate Eugene Workflow Monitor (ID: EKAOWgdA5FMZaQdW)
- [ ] Reprocess 8 files from Wilhelmsmuehlenweg 3 staging folder
- [ ] Monitor 10-20 production executions
- [ ] Build automated V8 test runner workflow
- [ ] Add file existence validation before rename operations

### 🔴 Blockers

- **Tracker Column Structure Unknown:** Tracker has TWO sets of numbered columns (B-AL and AR-BT) with unclear purpose. Cannot properly update tracker until Eugene clarifies which columns to use.

### ⚠️ Known Issues

- Classification prompts may confuse similar document types (Baubeschreibung vs Exposé)
- Document types in tracker may not match 1:1 with folder structure
- Budget document classification unclear
- 38_Unknowns folder nodes are now unreachable (cleanup candidate)
- Timestamps appearing in column H (wrong - should be AQ)

---

## Key Decisions Made

### 1. Server Infrastructure Crisis Resolution (v9.1)
**Decision:** Add 2GB swap + aggressive cleanup every 4 hours with 12-hour retention
**Rationale:** Server was crashing from OOM kills; 7-day cleanup couldn't keep up with 8GB/day binaryData
**Impact:** Prevents OOM crashes, maintains disk at ~70% used

### 2. Tracker Should Log ALL Documents (v9.1 - User Clarification)
**Decision:** ALL documents should be logged in tracker, only Core 4 go to specific folders
**Rationale:** User clarified: "it's supposed to put every document into the tracker it's just only supposed to put the core 4 in their respective folders"
**Impact:** Need to rebuild tracker update logic after column structure clarified

### 3. Claude Vision Instead of GPT-4 (v9.0)
**Decision:** Use Claude claude-sonnet-4-20250514 for document classification instead of GPT-4
**Rationale:** Already integrated, consistent with other Sway workflows
**Impact:** Rate limit of 30,000 tokens/minute requires spacing between API calls

### 4. Core 4 Routing Simplification (v9.0)
**Decision:** Only Core 4 documents go to specific folders, ALL others go to 37_Others
**Rationale:** Simplify routing until document type mapping is finalized with Eugene
**Impact:** Reduces routing complexity, easier to modify Core 4 list

### 5. Google Sheets API for Tracker Updates (v9.0)
**Decision:** Use HTTP Request to Google Sheets API instead of n8n Google Sheets node
**Rationale:** Dynamic column updates not supported well by native node
**Impact:** More flexible, can update any column dynamically

### 6. Test Workflow for Rapid Iteration (v9.0)
**Decision:** Create separate "Chunk 2.5 - TEST MODE" workflow
**Rationale:** Full workflow takes 26 minutes, test mode runs in ~5 seconds
**Impact:** 312x faster testing iteration

---

## Important IDs / Paths / Workflow Names

### n8n Workflows

| Workflow Name | ID | Purpose | Status |
|--------------|-----|---------|--------|
| Pre-Chunk 0 - REBUILT v1 | p0X9PrpCShIgxxMP | Email intake, PDF conversion, staging | ✅ Active |
| Chunk 2.5 - Client Document Tracking | okg8wTqLtPUwjQ18 | Claude Vision classification, routing | ✅ Active |
| Chunk 2.5 - TEST MODE | FL8cPoYixTTKXY8Z | Rapid testing without classification | ✅ Active |
| Eugene Workflow Monitor | EKAOWgdA5FMZaQdW | Hourly execution health checks | ⏳ Needs Activation |
| Test Email Sender | RZyOIeBy7o3Agffa | Send test PDFs via email | ✅ Active |
| Pre-Chunk 0 (Legacy) | YGXWjWcBIk66ArvT | Original email intake | ⚠️ Legacy |
| Chunk 2 | qKyqsL64ReMiKpJ4 | Text extraction, processing | ✅ Active |

### Google Sheets

| Spreadsheet Name | ID | Purpose |
|-----------------|-----|---------|
| AMA Client Document Tracker | 12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I | Track document receipt status |
| AMA_Folder_IDs | 1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm | Client folder ID mappings |

### Tracker Column Mapping (NEEDS CLARIFICATION)

**Current Code Mapping (May Be Wrong):**
| Document Type | Tracker Column | Column Letter |
|---------------|----------------|---------------|
| 01_Projektbeschreibung | Status_Expose | D (or AM?) |
| 03_Grundbuchauszug | Status_Grundbuch | E (or AN?) |
| 10_Bautraegerkalkulation_DIN276 | Status_Calculation | F (or AO?) |
| 36_Exit_Strategie | Status_Exit_Strategy | G (or AP?) |
| (Always updated) | Last_Updated | H (WRONG - should be AQ) |

**Tracker Has Two Column Sets:**
- **First Set (B-AL):** 01_Expose → 37_Others (English/Project Phases)
- **Status Columns (AM-AQ):** Status_Expose, Status_Grundbuch, Status_Calculation, Status_Exit_Strategy, Last_Updated
- **Second Set (AR-BT):** 09_Altlastenkataster → 38_Unknowns (German Document Types)

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
| Issues Backlog | /eugene/ISSUES_BACKLOG.md | Known issues and future improvements |
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
    ├── Split In Batches (Output 1 → Loop)
    ├── Download PDF from staging
    ├── Convert to Base64
    ├── Build Claude Tier 1 prompt
    ├── [30s wait] → Claude Vision Tier 1 Classification
    ├── Parse Tier 1 → Build Tier 2 prompt
    ├── [30s wait] → Claude Vision Tier 2 Classification
    ├── Parse Tier 2 → Route based on document type
    ├── Check "Should Update Tracker?" (IF node)
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

## Server Status

### n8n Server (n8n.oloxa.ai)

- **Status:** Healthy (post-crisis)
- **Disk:** ~70% used (was 100%)
- **Swap:** 2GB available (was 0)
- **RAM:** 1.9GB

### Cron Jobs

| Schedule | Command | Purpose |
|----------|---------|---------|
| Every 4 hours (*/4) | find ... -mmin +720 -delete | Clean binaryData >12 hours old |
| Every 4 hours + 30min | docker system prune -f | Clean unused Docker resources |
| Hourly | df -h / >> disk-monitor.log | Log disk usage |

### Health Check Command

```bash
ssh n8n.oloxa.ai "df -h && free -h && systemctl status n8n"
```

**Healthy thresholds:**
- Disk: < 80% used
- RAM: > 200MB free (or swap available)
- n8n: Active (running)

---

## Current State Summary

**Version:** v9.1 (v9.0 base + Infrastructure Crisis Fix + Tracker Structure Investigation)
**Phase:** Production Ready with pending tracker column clarification
**Classification:** Claude Vision (claude-sonnet-4-20250514)
**Processing Time:** ~60+ seconds per file (due to rate limit protection)

### Success Metrics (v8.1 baseline)

- Classification accuracy: 95%
- File rename success: 100%
- Metadata preservation: 100%
- Overall workflow: 100%

### Performance (v9.1)

- Wait time per file: ~60 seconds (rate limit protection)
- Total execution (4 files): ~26 minutes
- Test mode execution: ~5 seconds

### Recent Execution Issues Resolved

| Execution | Issue | Root Cause | Fix |
|-----------|-------|------------|-----|
| 5727 | 0 files processed | Split In Batches Output 1 disconnected | Connected Output 1 → Download PDF |
| 5729 | Crash with "Unknown error" | OOM kill (no swap, 100% disk) | Added swap, cleaned disk |
| 5738 | JSON parse error | skipTrackerUpdate=true but HTTP Request executed | Added IF node check |

---

## Next Steps

### Immediate (Before Next Eugene Meeting)

1. Review `/eugene/questions-for-eugene.md` with Eugene
2. **CRITICAL:** Get clarification on doubled tracker columns
3. Get master document type mapping table
4. Clarify Baubeschreibung, Budget classification
5. Confirm Core 4 list is correct

### Short-Term (This Week)

1. Activate Eugene Workflow Monitor (ID: EKAOWgdA5FMZaQdW)
2. Rebuild tracker column mapping based on Eugene feedback
3. Fix wrong column positions (Last_Updated = AQ)
4. Reprocess 8 files from Wilhelmsmuehlenweg 3
5. Test with Chunk 2.5 TEST MODE workflow

### Medium-Term

1. Add more document types to specific folder routing
2. Build automated test runner workflow
3. Add file existence validation before operations
4. Create monitoring alerts for systematic failures
5. Clean up unused 38_Unknowns nodes
6. Monitor server disk usage (target <80%)

---

## References

- VERSION_LOG: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/VERSION_LOG.md`
- Questions for Eugene: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/questions-for-eugene.md`
- Issues Backlog: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/ISSUES_BACKLOG.md`
- Test Mode Docs: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/oloxa/SwaysExpenseSystem/N8N_Blueprints/CHUNK_2.5_TEST_MODE_IMPLEMENTATION.md`
- Server Diagnostics: `/Users/swayclarke/coding_stuff/server-diagnostics/`

---

**Document Version:** summary_v9.1_2026-01-26.md
**Generated:** 2026-01-26 00:34 CET
**Author:** Claude Code (Sway's automation assistant)
