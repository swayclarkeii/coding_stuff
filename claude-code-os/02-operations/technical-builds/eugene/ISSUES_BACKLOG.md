# Eugene AMA System - Issues Backlog

**Created:** 2026-01-25
**Purpose:** Track known issues, bugs, and improvements to build later

---

## Critical (Fix Before Handoff)

### 1. Server Infrastructure - OOM Risk
**Status:** 🔴 CRITICAL - Needs immediate fix
**Discovered:** 2026-01-25 (Execution 5729 crash)
**Root Cause:** Server has only 1.9GB RAM, no swap, 99% disk full

**Evidence:**
```
[Sun Jan 25 20:46:45 2026] Out of memory: Killed process 2392105 (node)
```

**Impact:** Workflows can crash randomly during long executions, losing all progress

**Fix Required:**
- [ ] Add 2GB swap space (immediate - prevents OOM kills)
- [ ] Clean disk space (binaryData + unused Docker images)
- [ ] Change cleanup cron from daily → every 6 hours
- [ ] Long-term: Upgrade server to 4GB RAM

**Effort:** 15-30 minutes for immediate fixes

---

### 2. Split In Batches Connection Issue
**Status:** ✅ FIXED (2026-01-25)
**Discovered:** Execution 5727 - workflow did nothing
**Root Cause:** Loop output (Output 1) was disconnected from Download PDF node
**Fix Applied:** Connected Output 1 → Download PDF for Classification

---

## High Priority (Build This Week)

### 3. Execution Monitoring & Alerting
**Status:** ✅ BUILT (2026-01-25)
**Workflow ID:** EKAOWgdA5FMZaQdW
**Purpose:** Hourly check for failed/stuck/silent executions
**Next Step:** Activate workflow in n8n UI

---

### 4. No Error Handling on HTTP Requests
**Status:** ⏳ TODO
**Location:** Update Client_Tracker Row (API) node
**Issue:** If Google Sheets API fails, workflow crashes without retry
**Fix:** Add `retryOnFail: true`, `maxTries: 3`, error output handling

---

### 5. No Reprocessing Capability
**Status:** ⏳ TODO
**Issue:** When files fail to process, no easy way to retry them
**Fix Options:**
- Create "Reprocess Staging Files" workflow
- Add manual trigger to Chunk 2.5
- Log failed files to a sheet for retry

---

## Medium Priority (Build Before Production)

### 6. Wait Nodes Don't Block Properly
**Status:** ⚠️ Workaround in place
**Issue:** n8n Wait nodes schedule resumes, don't truly block
**Current Fix:** Added `await new Promise(setTimeout, 30000)` in Code nodes
**Proper Fix:** Refactor to use Split In Batches correctly

---

### 7. Rate Limit Protection May Be Excessive
**Status:** ⏳ Review after testing
**Issue:** 30-second waits + 120-second retries = very slow processing
**Optimization:** Test with 15-second waits, monitor for rate limits

---

### 8. 38_Unknowns Nodes Unreachable
**Status:** ⏳ Cleanup candidate
**Issue:** With new Core 4 routing, 38_Unknowns folder nodes never execute
**Fix:** Remove unused nodes to simplify workflow

---

## Low Priority (Nice to Have)

### 9. Outdated Node Versions
**Status:** ⏳ Optional
**Nodes:** Gmail (2.1→2.2), HTTP Request (4.2→4.4)
**Risk:** Low - current versions work fine

---

### 10. Long Linear Chain Warning
**Status:** ⏳ Optional
**Issue:** Workflow has 28 nodes in sequence
**Fix:** Consider breaking into sub-workflows (post-stabilization)

---

## Resolved Issues

| Date | Issue | Resolution |
|------|-------|------------|
| 2026-01-25 | Split In Batches disconnected | Connected Output 1 to Download PDF |
| 2026-01-25 | Tracker not updating | Replaced with HTTP Request to Sheets API |
| 2026-01-25 | JSON parsing error | Added robust extraction with regex fallback |
| 2026-01-25 | Rate limit errors | Added 30s blocking sleep before API calls |
| 2026-01-25 | Disk 100% full | Cleaned binaryData, set up daily cron |
| 2026-01-24 | Database not ready | Freed disk space, restarted services |

---

## Server Health Checklist (Before Each Session)

```bash
# Quick health check
ssh n8n.oloxa.ai "df -h && free -h && systemctl status n8n"
```

**Healthy thresholds:**
- Disk: < 80% used
- RAM: > 200MB free (or swap available)
- n8n: Active (running)

---

**Last Updated:** 2026-01-25 21:00 CET
