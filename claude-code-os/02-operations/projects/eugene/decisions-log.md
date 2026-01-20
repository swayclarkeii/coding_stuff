# Decisions Log - Eugene (AMA Capital)

Track all key decisions made during the project lifecycle.

---

## Discovery Phase Decisions

### December 1, 2025

**Decision 1: Pursue Automated Document Processing Solution**
- **Context:** Eugene spending 5-10 hours per deal on document management
- **Options Considered:** Continue manual process vs. build automation
- **Decision:** Pursue automation solution
- **Rationale:** 5-10 hours per deal is unsustainable for growth; prevents scaling beyond 6 deals/year
- **Impact:** Initiated discovery and solution design process
- **Decision Maker:** Eugene + Sway
- **Status:** ✅ Confirmed

---

### December 9, 2025

**Decision 2: Email Forwarding vs. Client Portal for Phase 1**
- **Context:** Need to determine how documents enter the system
- **Options Considered:**
  - Option A: Client portal with direct uploads
  - Option B: Email forwarding automation (Eugene forwards client emails)
  - Option C: Both simultaneously
- **Decision:** Email forwarding for Phase 1, client portal deferred to Phase 2
- **Rationale:**
  - Simpler and faster to build
  - No change to Eugene's current workflow
  - No client training required
  - Faster time to value (ROI in 3-6 months vs. 6-12 months)
  - Validates AI accuracy before building client-facing features
- **Impact:**
  - Phase 1 focused on backend automation only
  - Phase 2 will include client-facing portal
  - Reduced development time from 16-20 weeks to 8-12 weeks
- **Decision Maker:** Eugene + Sway
- **Status:** ✅ Confirmed

---

**Decision 3: PipeDrive Integration Critical, Motion Nice-to-Have**
- **Context:** Eugene uses multiple tools (PipeDrive, Motion, Email)
- **Options Considered:**
  - Option A: Integrate with all tools in Phase 1
  - Option B: PipeDrive only in Phase 1
  - Option C: No integrations, manual updates
- **Decision:** PipeDrive integration in Phase 1, Motion deferred to Phase 2
- **Rationale:**
  - Eugene manually updates PipeDrive for every deal
  - PipeDrive is source of truth for deals
  - Highest ROI integration (saves most manual work)
  - Motion is nice-to-have but not critical
- **Impact:**
  - PipeDrive API integration included in core Phase 1 scope
  - Motion integration moved to Phase 2 enhancement list
- **Decision Maker:** Eugene + Sway
- **Status:** ✅ Confirmed

---

**Decision 4: 95% Accuracy Threshold for AI Document Identification**
- **Context:** Need to define acceptable accuracy for AI
- **Options Considered:**
  - Option A: 100% accuracy (impossible, would require too much manual work)
  - Option B: 95%+ accuracy with confidence scoring
  - Option C: 85-90% accuracy (too low, Eugene wouldn't trust it)
- **Decision:** Target 95%+ accuracy with confidence scoring and manual review for low-confidence items
- **Rationale:**
  - Eugene needs to trust the system
  - Some manual review is acceptable (still saves 80% of time)
  - Confidence scoring allows Eugene to prioritize manual review
  - Achievable with proper training data and prompt engineering
- **Impact:**
  - Extensive sample documents required (3-5 per type)
  - Confidence scoring feature added to requirements
  - Low-confidence alerts implemented
- **Decision Maker:** Eugene + Sway
- **Status:** ✅ Confirmed

---

**Decision 5: German Language Primary, English Secondary**
- **Context:** Eugene's documents are mostly German, some English
- **Options Considered:**
  - Option A: German only
  - Option B: Both German and English equally
  - Option C: Multi-language support (German, English, French, etc.)
- **Decision:** Optimize for German, support English, defer other languages
- **Rationale:**
  - 95% of documents are German official documents
  - ChatGPT API handles German well
  - German bureaucratic documents have standardized formats
  - English support needed for international clients (5% of deals)
- **Impact:**
  - ChatGPT prompts optimized for German language
  - Training data focused on German document structures
  - English support included but not primary focus
- **Decision Maker:** Eugene + Sway
- **Status:** ✅ Confirmed

---

**Decision 6: Phase 1 Budget and Timeline**
- **Context:** Need to scope Phase 1 investment and duration
- **Options Considered:**
  - Option A: €10-15K, 6-8 weeks (too rushed, high risk)
  - Option B: €15-25K, 8-12 weeks (balanced)
  - Option C: €25-35K, 12-16 weeks (too long, delayed ROI)
- **Decision:** €15,000-25,000 budget, 8-12 week timeline
- **Rationale:**
  - Balanced approach for quality and speed
  - Allows proper testing and refinement
  - ROI positive in 3-6 months
  - Scope matches budget and timeline
- **Impact:**
  - Phase 1 scope defined around budget constraints
  - Phase 2 features clearly separated
- **Decision Maker:** Eugene + Sway (pending final approval)
- **Status:** ⏳ Proposal phase

---

## Technical Decisions

### December 9, 2025

**Decision 7: ChatGPT API (GPT-4) for Document Identification**
- **Context:** Need to select AI technology for document identification
- **Options Considered:**
  - Option A: ChatGPT API (OpenAI)
  - Option B: Custom ML model trained from scratch
  - Option C: Other AI services (Google, AWS, etc.)
- **Decision:** Use ChatGPT API (GPT-4 or GPT-4 Turbo)
- **Rationale:**
  - Eugene already uses ChatGPT successfully (proof of concept)
  - No training required (prompt engineering only)
  - Excellent German language support
  - Fast to implement vs. custom ML model
  - Mature API with good documentation
- **Impact:**
  - Development faster than custom ML approach
  - Sample documents used for prompt engineering, not model training
  - API costs included in operational budget
- **Decision Maker:** Sway + Development Team
- **Status:** ✅ Confirmed

---

**Decision 8: 18 Document Types (Standardized)**
- **Context:** Need to define which documents the system will identify
- **Options Considered:**
  - Option A: Start with 4 critical documents, expand later
  - Option B: All 18 documents from Day 1
  - Option C: Custom document list per deal type
- **Decision:** System checks all 18 documents by default
- **Rationale:**
  - Covers all deal types (Acquisition, Development, Refinance)
  - Eugene manually ignores irrelevant ones for now
  - Future enhancement: Auto-filter by deal type
  - Complete from Day 1 better than iterative additions
- **Impact:**
  - 18 document types in training/prompt data
  - Checklist shows all 18 (Eugene ignores irrelevant)
- **Decision Maker:** Eugene + Sway
- **Status:** ✅ Confirmed

**18 Document Types:**
1. Teaser/Exposé (Critical)
2. Calculation (Critical)
3. Grundbuch (Critical)
4. Exit Strategy (Critical)
5. Bauplan (Important)
6. Baugenehmigung (Important)
7. Wirtschaftsplan (Important)
8. Energy Certificate (Important)
9. Property Photos (Important)
10. Architect Statements (Important)
11. Site Survey (Important)
12. Rental Agreement (Important)
13. Insurance Documentation (Important)
14. Title Deed (Important)
15. Tax Assessment (Important)
16. Previous Loan Documentation (Optional)
17. Market Analysis (Optional)
18. Environmental Reports (Optional)

---

## Scope Decisions

### December 9, 2025

**Decision 9: Phase 1 vs. Phase 2 Feature Boundaries**
- **Context:** Need to prevent scope creep and deliver value quickly
- **Decision:** Strict boundary between Phase 1 (backend automation) and Phase 2 (client-facing features)

**Phase 1 Scope (IN):**
✅ Email forwarding automation
✅ AI document identification
✅ File labeling and organization
✅ Checklist generation
✅ PipeDrive CRM integration
✅ Email notifications to Eugene
✅ Error handling and logging

**Phase 2 Scope (OUT of Phase 1):**
❌ Client-facing data room portal
❌ Direct client document uploads
❌ Real-time checklist for clients
❌ Automated client communication (draft emails)
❌ Motion integration
❌ Advanced document verification (quality checks)
❌ Data extraction from documents

- **Rationale:**
  - Phase 1 delivers 80% of value in 1/3 of the time
  - Client portal requires client training and adoption
  - Validate AI accuracy before building client-facing features
  - Faster ROI with focused scope
- **Impact:**
  - 8-12 week timeline vs. 16-20 weeks if bundled
  - Clear change request process for additions
  - Phase 2 starts after Phase 1 is stable
- **Decision Maker:** Eugene + Sway
- **Status:** ✅ Confirmed

---

## Pending Decisions

### To Be Decided Before Development

**Decision TBD-1: Email Forwarding Address**
- **Options:** automation@[domain], docs@[domain], process@[domain], or custom
- **Deadline:** Before development starts
- **Decision Maker:** Eugene
- **Status:** ⏳ Pending

**Decision TBD-2: PipeDrive Stage Mapping**
- **Context:** Which deal stages to use for different document statuses
- **Options:** Define "Pending Documents", "Qualified", "Needs Review" stages
- **Deadline:** Before PipeDrive integration sprint
- **Decision Maker:** Eugene
- **Status:** ⏳ Pending

**Decision TBD-3: Checklist Format Preference**
- **Options:** PDF attachment, plain text in email, Excel/CSV, or all three
- **Deadline:** Before checklist generation sprint
- **Decision Maker:** Eugene
- **Status:** ⏳ Pending

**Decision TBD-4: Document Retention Policy**
- **Context:** How long should system store documents?
- **Options:** Delete after X days, keep indefinitely, or delete after confirmation
- **Considerations:** GDPR compliance, data privacy, backup strategy
- **Deadline:** Before architecture finalized
- **Decision Maker:** Eugene + Sway (Legal/Compliance)
- **Status:** ⏳ Pending

---

## Decision-Making Process

### Levels of Authority
- **Eugene:** Final approval on scope, budget, timeline, feature priorities
- **Sway:** Technical approach, vendor selection, architecture decisions
- **Development Team:** Implementation details, technology stack, coding standards

### Escalation Path
1. Developer → Development Lead → Sway → Eugene
2. Response times: <24 hours non-urgent, <4 hours urgent

### Change Request Process
1. Identify proposed change
2. Assess impact on scope, timeline, budget
3. Document options and recommendation
4. Obtain Eugene's approval before proceeding
5. Update project plan and communicate to team

---

*This log will be updated after each major decision. All decisions are documented for transparency and future reference.*
