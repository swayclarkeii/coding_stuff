# Recovery Plan: Expense System v1.3.1 → v2.0.0

**Created**: January 2, 2026
**Current Progress**: 35% complete
**Target**: 100% (Production-ready MVP)
**Owner**: Sway Clarke

---

## 🎯 Executive Summary

**Situation**: All n8n workflows erased Dec 31, 2025. Workflows rebuilt Jan 2, 2026 but discovered critical credentials crisis preventing all functionality.

**Current State**:
- ✅ Infrastructure intact (Google Drive, Database schema, Documentation)
- ⚠️ Workflows rebuilt but non-functional due to missing credentials
- ❌ Database completely empty despite 70 test runs
- 🔴 All Google Sheets, Gmail, and partial Google Drive credentials missing

**Recovery Goal**: Reach production-ready state (v2.0.0) with 7.0/10 efficiency score

**Estimated Recovery Timeline**: 65% remaining work = 5 phases

---

## 📋 Phase-by-Phase Recovery Plan

### Phase 1: Credentials Configuration (5% → 45%)
**Target Completion**: Day 1 (Today/Tomorrow)
**Priority**: CRITICAL - Nothing works without this

#### Tasks:
1. **Google Service Account Setup**
   - [ ] Verify service account exists and has proper permissions
   - [ ] Download service account JSON key file
   - [ ] Store credentials securely in n8n
   - [ ] Document credential ID for reference

2. **Configure Workflow 1 (PDF Parser)**
   - [ ] Add Google Sheets credentials to "Write Transactions to Database" node
   - [ ] Add Google Sheets credentials to "Log Statement Record" node
   - [ ] Verify Google Drive credentials still valid on existing nodes
   - [ ] Export updated workflow JSON to `N8N_Blueprints/v1_foundation/workflow1_v1.1.2_credentialed_20260102.json`

3. **Configure Workflow 2 (Gmail Monitor)**
   - [ ] Add Gmail OAuth2 credentials to "Search Gmail for Receipts" node
   - [ ] Add Gmail credentials to "Get Email Details" node
   - [ ] Add Google Drive credentials to "Download Attachment" node
   - [ ] Add Google Drive credentials to "Upload to Receipt Pool" node
   - [ ] Add Google Sheets credentials to "Log Receipt in Database" node
   - [ ] Export updated workflow JSON to `N8N_Blueprints/v1_foundation/workflow2_v1.2.2_credentialed_20260102.json`

4. **Configure Workflow 3 (Transaction Matching)**
   - [ ] **DECISION REQUIRED**: Keep mega workflow (26 nodes) or split into modular workflows?
   - [ ] If keeping mega: Add credentials to all 15 Google-related nodes
   - [ ] If splitting: Archive mega workflow, build focused 9-node matching workflow
   - [ ] Export final workflow JSON

5. **Update VERSION_LOG.md**
   - [ ] Document v1.3.2 (Credentials Restored)
   - [ ] Update component inventory with new credential IDs
   - [ ] Mark Phase 1 complete

**Success Criteria**:
- All workflows show green "credentials configured" status in n8n
- Test execution of each workflow doesn't fail on authentication
- Progress dashboard shows 45% complete

---

### Phase 2: Workflow 1 Validation (45% → 55%)
**Target Completion**: Day 2
**Priority**: HIGH - Core functionality test

#### Tasks:
1. **Prepare Test Environment**
   - [ ] Verify `_Inbox/Bank-Statements/` folder is empty
   - [ ] Prepare 5 representative test PDFs:
     - 1x ING Bank statement (simple format)
     - 1x Deutsche Bank statement (complex format)
     - 1x Barclay credit card statement
     - 1x Miles & More credit card statement
     - 1x edge case (multi-page, unusual formatting)

2. **Execute Test Runs**
   - [ ] Upload test PDF #1, wait for processing
   - [ ] Check database: Verify transactions written to Transactions sheet
   - [ ] Check database: Verify statement logged in Statements sheet
   - [ ] Verify PDF moved to `_Archive/Statements/`
   - [ ] Repeat for all 5 test PDFs
   - [ ] Document results in TESTING_PREPARATION.md

3. **Validate Data Quality**
   - [ ] Check transaction dates parsed correctly
   - [ ] Check amounts parsed accurately (verify decimals, currency)
   - [ ] Check vendor names extracted properly
   - [ ] Check German special characters handled correctly (ä, ö, ü, ß)
   - [ ] Identify any parsing errors or edge cases

4. **Fix Issues (if any)**
   - [ ] Update OpenAI Vision prompts if parsing errors found
   - [ ] Adjust regex patterns if data extraction fails
   - [ ] Re-test failed cases

5. **Update Documentation**
   - [ ] Export workflow JSON as `workflow1_v1.1.3_validated_20260102.json`
   - [ ] Update VERSION_LOG.md with v1.1.3 (Validated)
   - [ ] Document known limitations and edge cases

**Success Criteria**:
- 5/5 test PDFs successfully processed
- All transactions appear in database with accurate data
- All statements logged with correct metadata
- All PDFs archived properly
- Zero errors in n8n execution logs
- Progress dashboard shows 55% complete

---

### Phase 3: Workflow 2 Activation & Testing (55% → 70%)
**Target Completion**: Day 3-4
**Priority**: HIGH - Receipt automation critical for time savings

#### Tasks:
1. **Multi-Account Gmail Strategy** (See VENDOR_RECEIPT_ANALYSIS.md)
   - [ ] **DECISION REQUIRED**: Which Gmail accounts to monitor?
     - Primary: swayclarkeii@gmail.com
     - Additional accounts: (identify from vendor analysis)
   - [ ] Configure OAuth2 credentials for each account
   - [ ] Update workflow to handle multiple accounts (if needed)

2. **Vendor Discovery Audit** (See VENDOR_RECEIPT_ANALYSIS.md)
   - [ ] Review current VendorMappings (12 vendors: OpenAI, Anthropic, AWS, etc.)
   - [ ] Search Gmail for receipt keywords ("receipt", "invoice", "Rechnung")
   - [ ] Identify missing vendors beyond current 12
   - [ ] Create regex patterns for new vendors
   - [ ] Update VendorMappings sheet with complete vendor list

3. **Test Workflow 2**
   - [ ] Activate workflow (enable schedule trigger: daily at 6 AM)
   - [ ] Run manual test execution
   - [ ] Verify Gmail search finds receipt emails
   - [ ] Verify attachments downloaded to `_Receipt-Pool/`
   - [ ] Verify receipts logged in Receipts sheet with correct metadata
   - [ ] Check for duplicate downloads (should skip already-downloaded)

4. **Edge Case Testing**
   - [ ] Test email with multiple attachments (should download all)
   - [ ] Test email with non-PDF attachments (should handle gracefully)
   - [ ] Test vendors not in VendorMappings (should log as "Unknown Vendor")
   - [ ] Test emails without attachments (should skip)

5. **Optimize & Refine**
   - [ ] Adjust vendor regex patterns if false positives/negatives found
   - [ ] Configure error notifications (if workflow fails)
   - [ ] Set up weekly summary reports (optional)

6. **Update Documentation**
   - [ ] Export workflow JSON as `workflow2_v1.2.3_validated_20260104.json`
   - [ ] Update VERSION_LOG.md with v1.2.3 (Validated)
   - [ ] Update VendorMappings with final vendor count
   - [ ] Document multi-account setup (if implemented)

**Success Criteria**:
- Gmail search returns expected receipt emails
- All attachments downloaded to correct folder
- All receipts logged in database with accurate metadata
- No duplicate downloads
- Workflow runs successfully on schedule
- Complete vendor list documented in VendorMappings
- Progress dashboard shows 70% complete

---

### Phase 4: Workflow 3 Build & Integration (70% → 90%)
**Target Completion**: Day 5-6
**Priority**: MEDIUM - Matching logic is complex but well-documented

#### Tasks:
1. **Architecture Decision** (REQUIRED BEFORE PROCEEDING)
   - [ ] **Option A**: Keep mega workflow (26 nodes combining W1+W2+W3)
     - Pros: Single workflow, fewer moving parts
     - Cons: Hard to debug, difficult to maintain, violates modularity
   - [ ] **Option B**: Build focused matching workflow (9 nodes as designed)
     - Pros: Modular, easier to debug, follows original design
     - Cons: Requires rebuilding, coordination between 3 workflows
   - [ ] **DECISION**: ___________________
   - [ ] Document decision rationale in VERSION_LOG.md

2. **Build/Fix Workflow 3** (Based on decision above)
   - If Option A (Keep mega):
     - [ ] Add credentials to all 15 Google-related nodes
     - [ ] Verify workflow logic flows correctly
     - [ ] Test each section independently
   - If Option B (Rebuild modular):
     - [ ] Archive mega workflow to `_archive/workflow3_mega_20260102.json`
     - [ ] Build new focused matching workflow (9 nodes)
     - [ ] Configure nodes per SYSTEM_DESIGN.md specifications
     - [ ] Add all credentials

3. **Implement Matching Algorithm**
   - [ ] Configure date matching (±3 days tolerance)
   - [ ] Configure amount matching (exact or ±€0.50)
   - [ ] Implement confidence scoring (0.0-1.0)
   - [ ] Set confidence threshold (recommend: 0.7)
   - [ ] Configure fuzzy vendor name matching

4. **Test Matching Logic**
   - [ ] Create test data:
     - 3 transactions with exact receipt matches (should match high confidence)
     - 2 transactions with ±2 day receipt matches (should match medium confidence)
     - 2 transactions with ±€0.50 amount matches (should match medium confidence)
     - 1 transaction with no matching receipt (should remain unmatched)
   - [ ] Run workflow on test data
   - [ ] Verify matches recorded in database
   - [ ] Verify confidence scores calculated correctly
   - [ ] Verify receipts moved to correct monthly folders

5. **Edge Case Testing**
   - [ ] Test multiple receipts matching same transaction (should pick highest confidence)
   - [ ] Test transaction matching multiple receipts (should match best candidate)
   - [ ] Test transactions with no receipts (should flag as unmatched)
   - [ ] Test receipts with no transactions (should remain in pool)

6. **Update Documentation**
   - [ ] Export workflow JSON as `workflow3_v1.3.3_validated_20260106.json`
   - [ ] Update VERSION_LOG.md with v1.3.3 (Validated)
   - [ ] Document matching algorithm parameters
   - [ ] Document edge case handling

**Success Criteria**:
- Matching algorithm identifies correct receipt-transaction pairs
- Confidence scores calculated accurately
- Matched receipts moved to correct monthly folders
- Unmatched transactions flagged in database
- Zero false positive matches
- Progress dashboard shows 90% complete

---

### Phase 5: End-to-End Integration & Production Readiness (90% → 100%)
**Target Completion**: Day 7-8
**Priority**: MEDIUM - Final validation before production

#### Tasks:
1. **Full System Integration Test**
   - [ ] Upload 2 real bank statements to `_Inbox/Bank-Statements/`
   - [ ] Wait for Workflow 1 to process (should extract transactions)
   - [ ] Wait for Workflow 2 daily run (should download matching receipts)
   - [ ] Manually trigger Workflow 3 (should match transactions to receipts)
   - [ ] Verify complete flow from PDF → Database → Matching → Organization

2. **Data Quality Audit**
   - [ ] Review all database entries for accuracy
   - [ ] Check for duplicate transactions
   - [ ] Verify all receipts logged properly
   - [ ] Confirm all matches have reasonable confidence scores
   - [ ] Identify any data quality issues

3. **File Organization Validation**
   - [ ] Verify statements archived to `_Archive/Statements/`
   - [ ] Verify receipts organized into monthly folders
   - [ ] Check folder structure matches expected pattern:
     - `2025/01-January/ING/Receipts/`
     - `2025/01-January/Deutsche-Bank/Receipts/`
     - etc.
   - [ ] Verify unmatched transactions logged to `_Unmatched/`

4. **Error Handling & Recovery**
   - [ ] Test workflow behavior with corrupted PDF (should log error, continue)
   - [ ] Test workflow behavior with invalid Gmail credentials (should notify, retry)
   - [ ] Test workflow behavior with Google API rate limits (should queue, retry)
   - [ ] Verify error notifications configured (email/Slack/etc.)

5. **Performance Optimization**
   - [ ] Measure workflow execution times
   - [ ] Identify bottlenecks (likely: OpenAI Vision API calls)
   - [ ] Optimize slow nodes (batch processing, parallel execution)
   - [ ] Set up monitoring/alerting for failures

6. **Production Deployment**
   - [ ] Enable all workflow schedules:
     - Workflow 1: Google Drive trigger (real-time)
     - Workflow 2: Daily 6 AM CET
     - Workflow 3: Daily 7 AM CET (after Workflow 2)
   - [ ] Configure backup/export routine (weekly workflow JSON exports)
   - [ ] Set up monthly summary generation (optional for v2.0)
   - [ ] Document production operating procedures

7. **Final Documentation**
   - [ ] Export all 3 workflows as v2.0.0 JSONs
   - [ ] Update VERSION_LOG.md with v2.0.0 (Production MVP)
   - [ ] Update README.md with production status
   - [ ] Create user guide for Sway (how to use system)
   - [ ] Update efficiency score (target: 7.0/10)

**Success Criteria**:
- Complete end-to-end flow works without errors
- All data quality checks pass
- All receipts organized into correct folders
- Error handling gracefully manages failures
- System runs autonomously on schedule
- User guide completed
- Efficiency score ≥ 7.0/10
- Progress dashboard shows 100% complete
- **Version v2.0.0 deployed to production**

---

## 🚨 Critical Path & Blockers

### Must-Complete Before Anything Else:
1. **Google Service Account credentials** - Without this, NOTHING works
2. **Workflow 3 architecture decision** - Blocks all Phase 4 work

### Known Blockers:
- **OpenAI API Credits**: Need $5+ for PDF parsing (hundreds of Vision API calls)
- **Gmail OAuth2**: Need to complete OAuth flow for each Gmail account
- **Test Data**: Need real German bank statement PDFs for validation

### Risk Mitigation:
- **Backup Strategy**: Export workflow JSONs after every major change
- **Rollback Plan**: Keep working v1.3.1 as fallback (see VERSION_LOG.md)
- **Testing Strategy**: Test with small batches before full production

---

## 📊 Success Metrics

### Target Efficiency Score: 7.0/10
**Current**: 4.5/10
**Required improvement**: +2.5 points

**Efficiency Breakdown**:
- **Time Savings**: 5-6 hours/month → 25-30 minutes/month ✅ (Already designed)
- **Automation Coverage**: 35% → 100% (Missing: credentials, testing, integration)
- **Reliability**: 0% → 95%+ (Need: error handling, monitoring)
- **Data Accuracy**: Unknown → 98%+ (Need: validation testing)
- **User Experience**: Manual → Autonomous (Need: production deployment)

### Phase-by-Phase Progress Checkpoints:
- Phase 1 complete: 45% (Credentials configured)
- Phase 2 complete: 55% (Workflow 1 validated)
- Phase 3 complete: 70% (Workflow 2 validated)
- Phase 4 complete: 90% (Workflow 3 validated)
- Phase 5 complete: 100% (Production MVP deployed)

---

## 🎯 Next Immediate Actions

### Today (January 2, 2026):
1. **Configure Google Service Account credentials in n8n**
   - Locate service account JSON key file
   - Add to n8n credentials store
   - Document credential ID

2. **Update Workflow 1 with Google Sheets credentials**
   - Add to "Write Transactions to Database" node
   - Add to "Log Statement Record" node
   - Test with single PDF

3. **Make Workflow 3 architecture decision**
   - Review mega workflow structure
   - Decide: Keep or rebuild modular
   - Document decision

### Tomorrow (January 3, 2026):
1. **Complete Workflow 1 validation** (Phase 2)
   - Test with 5 representative PDFs
   - Verify database writes
   - Fix any parsing issues

2. **Begin Workflow 2 configuration** (Phase 3)
   - Configure Gmail OAuth2
   - Run vendor discovery audit
   - Update VendorMappings

---

## 📁 Documentation Updates Required

### Files to Update:
1. **VERSION_LOG.md**
   - Add v1.3.2 (Credentials Restored)
   - Add v1.1.3, v1.2.3, v1.3.3 (Validated versions)
   - Add v2.0.0 (Production MVP)

2. **README.md**
   - Update workflow IDs (already done)
   - Update current status section
   - Update efficiency score

3. **Progress Dashboard**
   - Update after each phase completion
   - Track efficiency score improvements
   - Log blocker resolutions

4. **TESTING_PREPARATION.md**
   - Document test results for each phase
   - Update success criteria checklist

---

## 💰 Cost Estimate

### Required Investments:
- **OpenAI API Credits**: ~$5-10 (for initial validation + ongoing use)
- **Time Investment**:
  - Phase 1: 2-3 hours (credentials setup)
  - Phase 2: 3-4 hours (Workflow 1 validation)
  - Phase 3: 4-5 hours (Workflow 2 validation + vendor audit)
  - Phase 4: 5-6 hours (Workflow 3 build/fix + testing)
  - Phase 5: 3-4 hours (integration testing + production)
  - **Total**: ~17-22 hours

### Return on Investment:
- **Monthly time savings**: 5-6 hours → 25-30 minutes = **4.5-5.5 hours saved/month**
- **Break-even**: ~3-4 months
- **Annual savings**: ~54-66 hours (1-1.5 work weeks)

---

**Document Owner**: Sway Clarke
**Last Updated**: January 2, 2026
**Version**: 1.0
**Status**: Active Recovery Plan
