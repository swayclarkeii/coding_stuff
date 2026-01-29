# Expense System - Remaining Issues Log

**Date:** January 28, 2026
**Session:** Post-W6 Implementation

---

## 🔴 CRITICAL ISSUES

### 1. W3 Matching: Expensify Receipts Not Matching ❌
**Status:** INVESTIGATING
**Priority:** HIGH

**Problem:**
- 9 Expensify receipts added to Receipts sheet (rows 17-25)
- W3 executed successfully (349 total matches)
- BUT: 0 matches for the 9 Expensify receipts
- `transaction_id` column is empty for all Expensify entries

**Possible Causes:**
1. Expensify merchants don't exist in bank statements
2. Date format mismatch (YYYY-MM-DD vs DD.MM.YYYY)
3. Matching logic not finding similar merchant names
4. Missing November 2025 bank transactions

**Next Steps:**
- [ ] Check if November 2025 bank transactions exist
- [ ] Verify merchant names in bank statements
- [ ] Test matching logic with sample data
- [ ] Check date format handling in W3

---

### 2. Duplicate Expensify Receipts ❌
**Status:** IDENTIFIED
**Priority:** MEDIUM

**Problem:**
- Rows 17-25: First set of 9 Expensify receipts
- Rows 26-34: Duplicate set of 9 Expensify receipts
- W6 ran twice and created duplicates

**Next Steps:**
- [ ] Delete duplicate rows (26-34)
- [ ] Add duplicate prevention logic to W6

---

### 3. Google Drive OAuth Expired ❌
**Status:** KNOWN ISSUE
**Priority:** MEDIUM

**Problem:**
- W3 nodes failing: "Search Production Folder", "Search Invoice Pool"
- Credential ID: PGGNF2ZKD2XqDhe0
- Affects invoice matching functionality

**Next Steps:**
- [ ] Refresh OAuth token for Google Drive
- [ ] Use browser-ops-agent for automated refresh

---

### 4. Google Sheets Rate Limit ⚠️
**Status:** OPERATIONAL CONSTRAINT
**Priority:** LOW

**Problem:**
- W3 hits "Quota exceeded for Read requests per minute"
- "Read Invoices Database" node fails after 16.4 seconds
- Impacts: Slow execution, potential failures

**Next Steps:**
- [ ] Implement rate limiting in W3
- [ ] Add delays between Google Sheets operations
- [ ] Request higher quota from Google

---

## 🟡 ENHANCEMENT REQUESTS (From User)

### 5. Single Trigger for Full Process 🆕
**Status:** NOT STARTED
**Priority:** HIGH

**Requirement:**
- User wants to trigger entire expense processing in one action
- Instead of running W1, W3, W6, W7 separately
- Need master orchestrator workflow

**Workflows to integrate:**
- W1: PDF Intake (bank statements)
- W2: Gmail Monitor (receipts)
- W3: Transaction Matching
- W6: Expensify Processing
- W7: Downloads Monitor
- W8: G Drive Collector

**Next Steps:**
- [ ] Design orchestration architecture
- [ ] Build master workflow with conditional routing
- [ ] Create single webhook/trigger endpoint

---

### 6. Automatic Expensify Email Processing 🆕
**Status:** NOT STARTED
**Priority:** HIGH

**Requirement:**
- Expensify emails reports automatically
- System should monitor Gmail for Expensify emails
- Download PDF attachment automatically
- Process with W6 without manual download

**Implementation:**
- Extend W2 (Gmail Monitor) OR create new workflow
- Filter for Expensify sender emails
- Extract PDF attachment
- Trigger W6 with downloaded PDF

**Next Steps:**
- [ ] Check W2 configuration for email filtering
- [ ] Add Expensify email detection logic
- [ ] Connect W2 → W6 pipeline

---

### 7. Handover Analysis for Guven 🆕
**Status:** NOT STARTED
**Priority:** MEDIUM

**Requirement:**
- Review in-person transcript with Guven (G-u-v-e-n)
- Identify what he needs from the system
- Determine what already exists vs what needs to be added
- Figure out customization requirements for different users
- Design easiest handover process

**Next Steps:**
- [ ] Search in-person transcripts for Guven meeting
- [ ] Analyze requirements from transcript
- [ ] Map to existing system capabilities
- [ ] Identify gaps and additions needed
- [ ] Design customization framework
- [ ] Create handover documentation

---

## 🟢 COMPLETED FIXES (This Session)

### ✅ W6 Expensify Extraction - COMPLETE
- Fixed filesystem-v2 binary access (Extract from File node)
- Fixed HTTP Request configuration
- Fixed Claude API integration
- Fixed Google Sheets append operation
- Successfully extracts 9 transactions from Expensify PDF
- Writes to Receipts sheet with Source="Expensify"

### ✅ Old W6 Workflows Deleted - COMPLETE
- Deleted 6 broken/unused W6 workflow versions
- Cleaned up workflow list

---

## 📊 System Status Summary

| Workflow | Status | Issues |
|----------|--------|--------|
| W1 - PDF Intake | ✅ Working | None |
| W2 - Gmail Monitor | ✅ Working | None |
| W3 - Matching | ⚠️ Partial | No Expensify matches, OAuth expired, rate limits |
| W6 - Expensify Processor | ✅ Working | Creates duplicates |
| W7 - Downloads Monitor | ✅ Working | None |
| W8 - G Drive Collector | ✅ Working | None |

**Overall System Health:** 🟡 Functional with issues

---

## Agent IDs (This Session)

**For resuming work:**
- ac0aaae: solution-builder-agent (W6 fixes)
- a99e2a1: test-runner-agent (W6 verification)
- adef77e: test-runner-agent (W3 matching test)
- a90e7cf: test-runner-agent (W6 final verification)

---

**Last Updated:** January 28, 2026, 6:05 PM CET
