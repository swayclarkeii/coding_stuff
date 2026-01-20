# Document Organizer V4 - Improvements and Missing Features

**Version:** 4.0 (Phase 1 MVP)
**Date:** December 22, 2025
**Status:** Phase 2 Planning Document

---

## Overview

This document tracks features that were identified during V4 development but deferred to Phase 2 to maintain MVP focus. It also documents error scenarios that may need handling in future iterations.

---

## Part 1: Deferred Features

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
| Multi-Language | Support English/German doc classification | 5/10 | 4/10 | Phase 3 |

---

### Feature Details

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

## Part 2: Missing Error Scenarios

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

---

## Part 3: Performance Optimizations

### Identified Optimizations (Not Yet Implemented)

| Optimization | Potential Improvement | Difficulty | Phase |
|--------------|----------------------|------------|-------|
| Batch API calls | Reduce API round-trips | 4/10 | Phase 2 |
| Caching project list | Avoid repeated Sheets reads | 3/10 | Phase 2 |
| Parallel text extraction | Process multiple docs simultaneously | 6/10 | Phase 3 |
| Pre-warm OCR | Keep Textract warm for faster response | 5/10 | Phase 3 |

---

## Part 4: Future Roadmap

### Phase 2 (Q1 2025)
- [ ] Duplicate Detection
- [ ] Stale Project Cleanup
- [ ] Email Optimization
- [ ] Manual Sync workflow

### Phase 3 (Q2 2025)
- [ ] Project Merge admin tool
- [ ] Batch Summary emails
- [ ] Enhanced error handling for all scenarios

### Phase 4 (Q3 2025)
- [ ] Web Dashboard
- [ ] Multi-language support
- [ ] Performance optimizations

---

## Appendix: Technical Debt

### Known Issues in V4

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

**Document Version:** 1.0
**Last Updated:** December 22, 2025
**Author:** Claude Code (AMA Build System)
