# Document Organizer - Improvements and Missing Features

**Version:** 2.0
**Date:** January 12, 2026
**Status:** V8 Planning Document

---

## Overview

This document tracks features identified during V4-V8 development but deferred to post-production to maintain MVP focus. It also documents error scenarios that may need handling in future iterations.

**Version History:**
- **v1.0 (Dec 22, 2025):** V4 Phase 1 planning - deferred features and error scenarios
- **v2.0 (Jan 12, 2026):** V8 post-production features added - 2-tier classification enhancements

---

## Part 1: V8 Post-Production Features (January 2026)

These features were identified during V8 development but are **deferred to future versions** after Eugene uses V8 in production for 1-2 months.

### V8 Future Features Matrix

| Feature | Description | Estimated Effort | When to Build | Priority |
|---------|-------------|------------------|---------------|----------|
| Version Detection & Archiving | Detect document versions (v1, v2, v3) and archive old ones | 6-8 hours | After 1-2 months usage | Medium |
| Processing Log Sheet | Dedicated Google Sheet tracking every document processed | 3-4 hours | If Eugene needs audit trail | Low |
| Confidence Score Dashboard | Aggregate confidence scores for system health monitoring | 4-5 hours | If Eugene wants analytics | Low |
| Re-classification Workflow | Allow re-submit from 38_Unknowns for re-classification | 6-8 hours | If 38_Unknowns gets >5 docs/month | Medium |
| Batch Confidence Reporting | Weekly/monthly email with classification statistics | 5-6 hours | After 20+ documents processed | Low |
| Multi-language Support | Support English documents in addition to German | 8-10 hours | If English documents appear | Low |

---

### V8 Feature Details

#### 1. Version Detection & Archiving (Effort: 6-8 hours)

**Problem:** Clients may submit updated versions of the same document (e.g., "Exposé_v1.pdf", "Exposé_v2.pdf", "Exposé_final.pdf"). Currently, all versions are stored without archiving old ones.

**Solution:**
- Add version detection logic in Chunk 2.5
- Compare filename patterns and content similarity
- Move old versions to `_Archive_Old_Versions` folder
- Keep only latest version in main folders
- Log version history in tracker

**Why Deferred:** Adds complexity; not critical for initial V8 launch. Better to validate core classification first.

**When to Build:** After Eugene has used V8 for 1-2 months and requests version management.

**Implementation Notes:**
```javascript
// Pseudo-code for version detection
const detectVersion = (filename) => {
  const versionPatterns = [/v\d+/, /final/, /revised/, /updated/];
  // Compare with existing files in folder
  // Calculate similarity score
  // Archive older version if similarity > 85%
};
```

---

#### 2. Processing Log Sheet (Effort: 3-4 hours)

**Problem:** Client_Tracker shows current state, but no historical log of every document processed. Hard to audit or troubleshoot past classifications.

**Solution:**
- Create new Google Sheet: "Processing_Log"
- Columns: Date, ClientName, FileName, Tier1Category, Tier2Type, Tier1Confidence, Tier2Confidence, CombinedConfidence, ActionType (CORE/SECONDARY/LOW_CONFIDENCE), DestinationFolder, TrackerUpdated (Y/N)
- Append one row per document processed
- Use for analytics and troubleshooting

**Why Deferred:** Client_Tracker already provides core tracking. Log is nice-to-have for compliance/reporting.

**When to Build:** If Eugene needs detailed audit trail for compliance or wants to analyze classification trends.

**Implementation Notes:**
- Add Google Sheets append operation after successful processing
- ~200 tokens per execution, negligible cost impact
- Can query log for confidence trends over time

---

#### 3. Confidence Score Tracking Dashboard (Effort: 4-5 hours)

**Problem:** Confidence scores are in filenames and Processing Log, but no aggregated view of system health.

**Solution:**
- Create new Google Sheet: "Confidence_Dashboard"
- Auto-populate summary statistics:
  - Average Tier 1 confidence (last 30 days)
  - Average Tier 2 confidence (last 30 days)
  - Distribution by actionType (CORE/SECONDARY/LOW_CONFIDENCE)
  - Trend line chart
  - Alert if confidence drops below 80%

**Why Deferred:** Confidence in filename provides sufficient visibility for now. Need baseline data before analytics are useful.

**When to Build:** After 20+ documents processed and Eugene wants to monitor system accuracy.

**Implementation Notes:**
- Requires Processing Log sheet (feature #2) as data source
- Use Google Sheets formulas for aggregation
- Optional: n8n scheduled workflow for weekly summary email

---

#### 4. Re-classification Workflow (Effort: 6-8 hours)

**Problem:** Documents in `38_Unknowns` folder (low confidence) can't be easily re-submitted for classification without emailing again.

**Solution:**
- New n8n workflow triggered from 38_Unknowns folder
- Detects new files added to 38_Unknowns
- Re-runs classification with updated prompts or manual hints
- Allows Eugene to add metadata file with classification hints
- Moves to correct folder if re-classification succeeds

**Why Deferred:** Edge case - can be handled manually by re-emailing initially. Need to see how often 38_Unknowns gets populated.

**When to Build:** If 38_Unknowns folder gets >5 documents per month consistently.

**Implementation Notes:**
- Google Drive Trigger on 38_Unknowns folder
- Check for optional metadata file (JSON with hints)
- Re-run Tier 1 + Tier 2 classification
- If confidence improves, move to correct folder

---

#### 5. Batch Confidence Reporting (Effort: 5-6 hours)

**Problem:** No proactive reporting on system health. Eugene must manually check filenames to see if classification is working well.

**Solution:**
- Scheduled n8n workflow (weekly/monthly)
- Aggregates last 30 days of classifications
- Generates report email:
  - Total documents processed
  - Average confidence scores
  - Breakdown by actionType
  - Alerts for any low-confidence trends
  - List of documents in 38_Unknowns needing review

**Why Deferred:** System needs baseline usage data first. Need 20+ documents before statistics are meaningful.

**When to Build:** After 20+ documents processed and Eugene wants regular status updates.

**Implementation Notes:**
- Requires Processing Log sheet (feature #2)
- Use Schedule Trigger (weekly on Mondays)
- Query Processing Log for last 30 days
- Generate HTML email with charts/tables

---

#### 6. Multi-language Support (Effort: 8-10 hours)

**Problem:** All prompts and document types are German. If Eugene receives English documents, classification will fail or be very low confidence.

**Solution:**
- Duplicate Tier 1 + Tier 2 prompts in English
- Add language detection step before classification
- Route to German or English prompt based on detected language
- Maintain same 38 document type taxonomy with English names
- Update filename format to include language code

**Why Deferred:** All Eugene's documents are currently German. No immediate need.

**When to Build:** If Eugene starts receiving English documents regularly (>10% of volume).

**Implementation Notes:**
```javascript
// Language detection
const detectLanguage = (text) => {
  const germanKeywords = ['Projektbeschreibung', 'Grundbuch', 'Kalkulation'];
  const englishKeywords = ['project description', 'land register', 'calculation'];
  // Return 'de' or 'en'
};
```

---

## Part 2: V4 Deferred Features (December 2025)

**Status:** Still pending - V8 implementation prioritized over V4 Phase 2 features.

### Priority Matrix

| Feature | Description | Difficulty (1-10) | Value (1-10) | Phase |
|---------|-------------|-------------------|--------------|-------|
| Duplicate Detection | MD5 hash comparison to prevent re-processing | 6/10 | 7/10 | Phase 2 |
| Project Merge | Admin workflow to merge duplicate projects | 7/10 | 6/10 | Phase 2 |
| Stale Cleanup | Auto-archive projects >90 days inactive | 4/10 | 5/10 | Phase 2 |
| Manual Sync | Button to scan folders and update tracker | 5/10 | 6/10 | Phase 2 |
| Email Optimization | Reduce Build Email from ~150 to ~50 lines | 3/10 | 4/10 | Phase 2 |
| Batch Summary | Daily digest instead of per-batch emails | 4/10 | 5/10 | Phase 3 |
| Web Dashboard | Visual status board for project tracking | 8/10 | 7/10 | Phase 3 |

---

### V4 Feature Details

#### 1. Duplicate Detection (Difficulty: 6/10)

**Problem:** If the same document is forwarded multiple times, it gets processed and filed each time.

**Solution:**
- Calculate MD5 hash of file content
- Store hash in processing log
- Before processing, check if hash exists
- If duplicate found: log but don't re-process, notify user

**Implementation Notes:**
```javascript
// Code node to calculate MD5
const crypto = require('crypto');
const hash = crypto.createHash('md5')
  .update($binary.data)
  .digest('hex');
```

**Dependencies:** None - can be added as standalone enhancement

---

#### 2. Project Merge (Difficulty: 7/10)

**Problem:** Fuzzy matching may occasionally create duplicate project entries (e.g., "Müller Building" and "Mueller Building" treated as different).

**Solution:**
- Admin workflow with manual trigger
- UI to select two project rows
- Merge all document tracking into primary project
- Update all file references
- Archive duplicate project row

**Implementation Notes:**
- Requires manual Google Sheets manipulation
- Need to handle file moves in Google Drive
- Should log all merge actions

**Dependencies:** Project Tracker must be stable first

---

#### 3. Stale Project Cleanup (Difficulty: 4/10)

**Problem:** Projects with no activity for 90+ days clutter the tracker.

**Solution:**
- Scheduled workflow (weekly)
- Query projects with Last Updated > 90 days
- Move to "Archived Projects" sheet/tab
- Option to restore archived projects

**Implementation Notes:**
```javascript
// Date comparison
const lastUpdated = new Date($json.lastUpdated);
const daysAgo = (Date.now() - lastUpdated) / (1000 * 60 * 60 * 24);
const isStale = daysAgo > 90;
```

**Dependencies:** None

---

#### 4. Manual Sync (Difficulty: 5/10)

**Problem:** If files are manually added to Google Drive folders, the Project Tracker won't know about them.

**Solution:**
- Manual trigger workflow
- Scan all document folders
- Parse filenames to extract project name and doc type
- Update Project Tracker to reflect actual folder contents

**Implementation Notes:**
- Need to handle filename parsing edge cases
- Should not overwrite existing tracker data
- Create reconciliation report

**Dependencies:** Consistent filename format (V4 provides this)

---

#### 5. Email Optimization (Difficulty: 3/10)

**Problem:** The "Build Email Summary" node has ~150 lines of code, making it hard to maintain.

**Solution:**
- Extract email template to separate Code node
- Use template literals more efficiently
- Add reusable formatting functions

**Implementation Notes:**
```javascript
// Refactored structure
const formatSection = (title, items) => { /* ... */ };
const formatDocList = (docs) => { /* ... */ };
const buildEmail = (project, docs, errors) => { /* ... */ };
```

**Dependencies:** None - purely code cleanup

---

## Part 3: Missing Error Scenarios

### Error Scenario Matrix

| Error Scenario | Description | Difficulty (1-10) | Probability | Impact | Current Handling |
|----------------|-------------|-------------------|-------------|--------|------------------|
| Gmail quota exceeded | 500 emails/day limit | 3/10 | Very Low | Medium | None (will fail) |
| Google Drive quota | 15GB free tier exceeded | 4/10 | Low | High | None |
| OpenAI rate limit | API throttling | 5/10 | Low | Medium | Basic retry |
| AWS Textract outage | Regional unavailability | 6/10 | Very Low | Medium | None |
| Sheets row limit | 10M rows per sheet | 2/10 | Very Low | Low | None |
| Concurrent emails | Two emails arrive simultaneously | 7/10 | Medium | High | **Resolved (V4 sequential)** |
| Corrupted ZIP | Extraction fails | 4/10 | Low | Low | Goes to Unknown |
| Password PDF | Can't extract text | 3/10 | Low | Low | Goes to Unknown |
| Non-German OCR | Wrong language in document | 5/10 | Medium | Medium | May misclassify |
| Empty email | No attachments | 3/10 | Low | None | Logs, no action |
| Oversized attachment | File > 25MB | 4/10 | Low | Low | Gmail rejects |
| Network timeout | API call hangs | 4/10 | Low | Medium | Basic retry |
| Invalid file type | .exe, .doc (non-PDF) | 2/10 | Low | None | Filtered out |

---

### Error Handling Details

#### Gmail Quota Exceeded (Difficulty: 3/10)

**Current Behavior:** Workflow fails with 429 error

**Recommended Fix:**
- Add exponential backoff for email sends
- Queue emails if quota hit, retry next hour
- Alert user via Slack/other channel if email fails

**Priority:** Low (unlikely for this volume)

---

#### Google Drive Quota (Difficulty: 4/10)

**Current Behavior:** Upload fails silently or with error

**Recommended Fix:**
- Pre-check available space before upload
- Alert user at 80% capacity
- Archive old files to compressed storage

**Priority:** Medium (depends on usage patterns)

---

#### OpenAI Rate Limit (Difficulty: 5/10)

**Current Behavior:** V4 has basic retry with backoff

**Recommended Fix:**
- Add request queuing
- Implement rate limit tracking
- Fall back to GPT-3.5 if GPT-4o-mini rate limited

**Priority:** Low (current volume unlikely to trigger)

---

#### Corrupted ZIP / Password PDF (Difficulty: 3-4/10)

**Current Behavior:** Goes to Unknown folder (V4)

**Recommended Fix:**
- Specific error message in email: "Password-protected PDF detected"
- Attempt password with common defaults (blank, "password")
- For corrupted: log specific extraction error

**Priority:** Low (current handling is acceptable)

---

#### Non-German OCR (Difficulty: 5/10)

**Current Behavior:** AWS Textract attempts German, may produce garbage

**Recommended Fix:**
- Language detection step before OCR
- Route English documents differently
- Alert user if unexpected language detected

**Priority:** Medium (could cause misclassification)

**Note:** V8 Multi-language Support (Feature #6 above) addresses this comprehensively.

---

## Part 4: Performance Optimizations

### Identified Optimizations (Not Yet Implemented)

| Optimization | Potential Improvement | Difficulty | Phase |
|--------------|----------------------|------------|-------|
| Batch API calls | Reduce API round-trips | 4/10 | Phase 2 |
| Caching project list | Avoid repeated Sheets reads | 3/10 | Phase 2 |
| Parallel text extraction | Process multiple docs simultaneously | 6/10 | Phase 3 |
| Pre-warm OCR | Keep Textract warm for faster response | 5/10 | Phase 3 |

---

## Part 5: Future Roadmap

### V8 Post-Production (Q1-Q2 2026)
**After V8 is in production and Eugene has used it for 1-2 months:**
- [ ] Version Detection & Archiving (if requested)
- [ ] Processing Log Sheet (if compliance/audit needed)
- [ ] Confidence Score Dashboard (after 20+ docs processed)
- [ ] Re-classification Workflow (if 38_Unknowns gets >5 docs/month)
- [ ] Batch Confidence Reporting (after 20+ docs processed)
- [ ] Multi-language Support (if English documents appear)

### V4 Phase 2 (Q2 2026 - If prioritized)
- [ ] Duplicate Detection
- [ ] Stale Project Cleanup
- [ ] Email Optimization
- [ ] Manual Sync workflow

### V4 Phase 3 (Q3 2026 - If prioritized)
- [ ] Project Merge admin tool
- [ ] Batch Summary emails
- [ ] Enhanced error handling for all scenarios

### V4 Phase 4 (Q4 2026 - If prioritized)
- [ ] Web Dashboard
- [ ] Performance optimizations

---

## Part 6: Technical Debt

### Known Issues in V7-V8

1. **Email template in single node** - Should be extracted to template file
2. **No rate limiting on n8n API calls** - Could fail if creating many variables quickly
3. **Fuzzy match threshold hardcoded** - Should be configurable variable
4. **No health check** - No way to verify all integrations are working

### Recommended Refactoring (Future)

1. Extract all hardcoded values to n8n variables
2. Add "health check" workflow that tests all API connections
3. Implement workflow versioning with automatic backup
4. Add unit tests for code nodes (export to external JS files)

---

## Appendix: Version Comparison

| Feature Area | V4 (Dec 2025) | V7 (Jan 2026) | V8 (Jan 2026) |
|--------------|---------------|---------------|---------------|
| **Document Types** | 5 types | 5 types | 38 types |
| **Classification** | Single-pass | Single-pass | 2-tier hierarchical |
| **Accuracy (CORE)** | 85-95% | 85-95% | 90-98% (projected) |
| **Accuracy (SECONDARY)** | 0% (all→Other) | 0% (all→Other) | 80-90% (projected) |
| **Filename Format** | Original name | Original name | {typeCode}_{client}_{confidence}pct.pdf |
| **Holding Folders** | No | No | Yes (4 folders) |
| **Confidence Visibility** | No | No | Yes (in filename) |

---

**Document Version:** 2.0
**Last Updated:** January 12, 2026 19:41 CET
**Author:** Claude Code (Sway's automation assistant)
