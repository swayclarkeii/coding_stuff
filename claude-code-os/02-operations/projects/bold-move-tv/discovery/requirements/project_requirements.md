# Bold Move TV - Project Requirements Document

**Project Name:** Dual Automation System (Ambushed Payment + Bold Move TV Leads)
**Client:** Sindbad Iksel - Bold Move TV & Ambushed
**Contact:** sindbad@boldmove.tv
**Last Updated:** January 12, 2026
**Status:** ⚠️ Draft - Pending Follow-Up Discovery Calls

---

## Executive Summary

### Project Vision

**Ambushed:** Reduce Sindbad's weekly invoice reconciliation time from 5-6 hours to 1-2 hours (80-90% reduction) while maintaining or improving error detection rate through automated validation with human approval checkpoints.

**Bold Move TV:** Build systematic lead capture and reactivation system to replace ad-hoc email parsing, establish conversion tracking, and enable data-driven sales optimization.

### Core Problems

**Problem 1: Ambushed Payment Reconciliation**
Sindbad spends 20-24 hours/month manually validating 15-20 weekly freelancer invoices against Google Sheets dashboard, catching ~10% error rate (missing projects, rate discrepancies, excessive hours). This prevents strategic work and Bold Move TV growth.

**Problem 2: Bold Move TV Lead Generation**
No systematic lead tracking, no conversion data, no reactivation process. Sales employee achieved only 1 meeting in 3 months. Manual email parsing into Google Sheets "Request Tracker" is inefficient and provides no actionable insights.

### Proposed Solution

**Ambushed Phase 1:** Automated invoice validation system that cross-references Google Sheets dashboard, flags discrepancies, maintains human approval checkpoint before Wise batch payments.

**Bold Move TV Phase 1:** Email-to-CRM lead capture system with categorization, conversion funnel tracking, and tactical warm lead reactivation workflow.

**Strategic Priority:** Recommend Ambushed first (clear €21K-27K annual ROI) to unlock time for Bold Move TV sales focus.

### Success Metrics

**Ambushed:**
- **Time reduction:** 80-90% (5-6 hours/week → 1-2 hours/week)
- **Error detection:** ≥10% (match or exceed current manual rate)
- **Payment accuracy:** 100% (zero errors)
- **Admin team satisfaction:** ≥4/5
- **ROI timeline:** 8-14 months payback

**Bold Move TV:**
- **Lead capture:** 100% (zero missed emails)
- **Categorization accuracy:** ≥90%
- **Meeting conversion:** 2x baseline (from 1 in 3 months)
- **Partner adoption:** Daily CRM usage
- **Funnel visibility:** Complete drop-off analysis

---

## ⚠️ Requirements Disclaimer

**Status:** Draft requirements based on initial discovery call (January 8, 2026)

**Pending Validation:**
- Ambushed admin team discovery call (understand their process, error patterns, dashboard structure)
- Bold Move TV strategy call with partner (clarify sales approach, confirm CRM preferences)

**What We Know:**
- High-level workflows and pain points
- Tools in use (Google Sheets, Wise, Gmail)
- Time costs and volume metrics
- Quality control requirements

**What We Don't Know Yet:**
- Detailed admin team workflow and data entry process
- Exact dashboard structure and calculation logic
- Root causes of 10% error rate
- Wise API capabilities and batch payment workflow
- Bold Move TV sales strategy clarity
- Partner role and tool preferences
- Historical lead conversion data (if any)

**Next Steps:**
- Complete follow-up discovery calls (Week of Jan 13-17)
- Update this document with detailed functional requirements
- Validate technical feasibility for all integrations
- Finalize success criteria and acceptance tests

---

## Project 1: Ambushed Payment System

### Phase 1 Requirements (Invoice Validation)

#### 1. Data Integration

##### FR1.1: Google Sheets Dashboard Integration
**Requirement:** System must read project data from Ambushed Google Sheets dashboard

**Acceptance Criteria:**
- Connects to Google Sheets via API
- Reads monthly tabs (current month + previous months for validation)
- Extracts: Project names, freelancer names, hours worked, hourly rates, total amounts
- Handles multiple freelancers per project
- Updates in real-time or near real-time (within 5 minutes of changes)

**Priority:** ⭐⭐⭐⭐⭐ Critical

**Status:** ⚠️ Pending - Dashboard structure needs review in admin team call

**Technical Notes:**
- Google Sheets API v4
- OAuth 2.0 authentication
- Need read-only access (minimize security risk)
- Dashboard has monthly tab structure (format to be confirmed)

---

##### FR1.2: Invoice Intake & Parsing
**Requirement:** System must automatically process freelancer invoices submitted via email or upload

**Acceptance Criteria:**
- Accepts invoices via email forwarding or file upload
- Supports formats: PDF (Google Docs templates), DOC, DOCX, images
- Extracts: Freelancer name, project name, hours, rate, total amount, invoice date
- Handles 15-20 invoices per batch (weekly volume)
- Preserves original invoice files for audit trail

**Priority:** ⭐⭐⭐⭐⭐ Critical

**Status:** ⚠️ Pending - Invoice format needs confirmation in admin team call

**Technical Notes:**
- Gmail API for email-based intake
- OCR for image-based invoices (if needed)
- Document AI or ChatGPT for structured data extraction
- Freelancers use Google Docs templates (format to be confirmed)

---

#### 2. Validation Logic

##### FR2.1: Cross-Reference Validation
**Requirement:** System must validate invoice data against dashboard data

**Acceptance Criteria:**
- **Project validation:** Confirm project exists in dashboard
- **Freelancer validation:** Confirm freelancer worked on this project
- **Hours validation:** Confirm hours match dashboard entry
- **Rate validation:** Confirm rate matches dashboard entry
- **Total calculation:** Confirm math is correct (hours × rate)
- **Date validation:** Confirm work falls within project timeline

**Priority:** ⭐⭐⭐⭐⭐ Critical

**Status:** ⚠️ Pending - Validation rules need confirmation in admin team call

**Technical Notes:**
- Fuzzy matching for project/freelancer names (typo tolerance)
- Threshold for "close enough" vs "discrepancy" (TBD with Sindbad)
- Historical data available for ML training (optional)

---

##### FR2.2: Error Detection & Flagging
**Requirement:** System must detect and flag discrepancies for manual review

**Acceptance Criteria:**
- **Missing projects:** Invoice for project not in dashboard → FLAG (High priority)
- **Rate discrepancies:** Invoice rate ≠ dashboard rate → FLAG (Medium priority)
- **Hour discrepancies:** Invoice hours ≠ dashboard hours → FLAG (Medium priority)
- **Excessive hours:** Hours seem unreasonable for project scope → FLAG (Low priority)
- **Missing information:** Required fields blank → FLAG (High priority)
- **Duplicate invoices:** Same freelancer + project + period → FLAG (High priority)

**Priority:** ⭐⭐⭐⭐⭐ Critical (This is the 10% error rate Sindbad currently catches)

**Status:** ⚠️ Pending - Error patterns need documentation in admin team call

**Technical Notes:**
- Error severity levels: High (blocks payment), Medium (review recommended), Low (informational)
- AI-powered anomaly detection (optional enhancement)
- Historical error data for training (if available)

---

##### FR2.3: Quality Control Dashboard
**Requirement:** System must provide Sindbad with review queue for flagged items

**Acceptance Criteria:**
- Dashboard shows all invoices with validation status (✅ Pass, ⚠️ Warning, ❌ Fail)
- Flagged items shown first (prioritized by severity)
- Sindbad can approve, reject, or edit flagged invoices
- Approved invoices move to payment preparation queue
- Rejected invoices notify freelancer with reason
- Edit capability to correct minor errors without rejecting

**Priority:** ⭐⭐⭐⭐⭐ Critical (Human-in-the-loop requirement)

**Status:** ⚠️ Draft - UI/UX to be designed after workflow validation

**Technical Notes:**
- Web dashboard (responsive design for mobile review)
- Email notification when flagged items require review
- Approval workflow: Single-click approve for batch, individual review for flags
- Audit trail of all approvals/edits/rejections

---

#### 3. Payment Integration

##### FR3.1: Wise Batch Payment Preparation
**Requirement:** System must prepare batch payment file for Wise integration

**Acceptance Criteria:**
- Generates Wise-compatible batch payment file (CSV or API format)
- Includes: Freelancer name, payment amount, currency, bank details, reference
- Only includes approved invoices (passed validation + Sindbad approval)
- Handles international payments (70-80 freelancers globally)
- Maintains 3-4 week payment window promise to freelancers

**Priority:** ⭐⭐⭐⭐ High

**Status:** ⚠️ Pending - Wise API capabilities need validation during architecture phase

**Technical Notes:**
- Wise API or batch CSV upload (to be confirmed)
- Freelancer bank details stored securely (encryption required)
- Payment reference format (to be confirmed with Sindbad)
- Weekly cadence requirement (cash flow critical)

---

##### FR3.2: Payment Execution
**Requirement:** System must execute batch payments via Wise

**Acceptance Criteria:**
- **Option A:** Sindbad manually uploads batch file to Wise (lowest risk)
- **Option B:** System auto-uploads to Wise, Sindbad approves in Wise (medium risk)
- **Option C:** Full automation with Sindbad audit trail (highest automation, build trust first)
- Payment confirmation captured and logged
- Failed payments flagged for manual intervention

**Priority:** ⭐⭐⭐ Medium (Start with Option A, scale to B/C over time)

**Status:** ⚠️ TBD - Depends on Sindbad's comfort level and Wise API capabilities

**Technical Notes:**
- Security critical: Payment execution requires high trust
- Recommend phased approach: Start manual, automate incrementally
- MFA/2FA considerations for API access
- Wise API documentation review required

---

#### 4. Reporting & Analytics

##### FR4.1: Weekly Validation Report
**Requirement:** System must generate weekly summary report for Sindbad

**Acceptance Criteria:**
- Total invoices processed: X
- Passed validation automatically: Y
- Flagged for review: Z
- Error breakdown by category (missing projects, rate issues, etc.)
- Time saved estimate (baseline 5-6 hours → actual time spent)
- Admin team performance insights (optional)

**Priority:** ⭐⭐⭐ Medium

**Status:** Draft - Report format to be confirmed with Sindbad

---

##### FR4.2: Admin Team Performance Insights (Optional)
**Requirement:** System may identify upstream inefficiencies in admin team workflow

**Acceptance Criteria:**
- Track error sources: Admin entry errors vs freelancer invoice errors
- Identify patterns: Which admin team members have higher error rates
- Suggest process improvements: "Projects frequently missing from dashboard"
- Sensitivity: Present insights tactfully (coaching, not punishment)

**Priority:** ⭐⭐ Low (Nice-to-have, politically sensitive)

**Status:** TBD - Depends on admin team buy-in and Sindbad's interest

**Technical Notes:**
- Only implement if admin team feels supported, not surveilled
- Frame as "process improvement" not "performance monitoring"
- Optional feature, not core requirement

---

### Phase 2 Requirements (Future Enhancement)

**Scope:** TBD after Phase 1 proven successful

**Potential Features:**
- Predictive cash flow modeling
- Automated project billing to clients (match freelancer payments)
- Integration with accounting software (Xero, QuickBooks)
- Mobile app for on-the-go approvals
- AI-powered fraud detection
- Freelancer self-service portal (invoice submission + tracking)

---

## Project 2: Bold Move TV Lead System

### Phase 1 Requirements (Lead Capture & Tracking)

#### 1. Email Integration

##### FR1.1: Gmail Lead Identification
**Requirement:** System must automatically identify leads from incoming email

**Acceptance Criteria:**
- Monitors Sindbad's Gmail inbox (bold move TV account or personal)
- Identifies emails containing lead indicators (pricing questions, interest in services, etc.)
- Parses lead information: Name, email, company, inquiry type, timestamp
- Handles forwarded emails (e.g., from website contact form)
- Processes historical emails to identify past warm leads

**Priority:** ⭐⭐⭐⭐⭐ Critical

**Status:** ⚠️ Pending - Email patterns need analysis in strategy call

**Technical Notes:**
- Gmail API integration
- Pattern matching or AI-based classification
- Historical email analysis (identify reactivation opportunities)
- Privacy considerations (email scanning permissions)

---

##### FR1.2: Lead Categorization
**Requirement:** System must categorize leads by status and temperature

**Acceptance Criteria:**
- **Temperature:** Cold (no prior contact), Warm (engaged but didn't convert), Hot (active conversation)
- **Status:** New, Waiting on Client, Ghosted, Canceled, Converted
- **Stage:** Initial Inquiry → Proposal Sent → Meeting Scheduled → Closed Won/Lost
- Auto-categorization based on email content and conversation history
- Manual override capability (partner can reclassify)

**Priority:** ⭐⭐⭐⭐ High

**Status:** ⚠️ Pending - Categorization logic needs validation in strategy call

**Technical Notes:**
- AI-based sentiment/intent detection (ChatGPT or similar)
- Historical conversation analysis
- Integration with eventual CRM

---

#### 2. CRM Integration

##### FR2.1: CRM Setup & Data Migration
**Requirement:** System must migrate from Google Sheets "Request Tracker" to proper CRM

**Acceptance Criteria:**
- **Option A:** Enhanced Google Sheets (low friction, familiar, limited features)
- **Option B:** HubSpot Free (CRM-designed, robust, learning curve)
- **Option C:** Pipedrive (sales-focused, paid, Eugene uses it = potential synergy)
- **Option D:** Notion (flexible, visual, multi-purpose)
- Migrate existing leads from current Request Tracker
- Minimal disruption to current workflow
- Partner daily adoption (5+ days/week usage)

**Priority:** ⭐⭐⭐⭐ High

**Status:** ⚠️ TBD - Pending partner preferences in strategy call

**Technical Notes:**
- Budget constraints (Bold Move TV not yet profitable)
- Partner must use it daily (adoption critical)
- Integration complexity varies by tool
- Don't over-engineer for current scale (3-person team)

---

##### FR2.2: Automated Lead Entry
**Requirement:** System must automatically create CRM records from identified emails

**Acceptance Criteria:**
- New lead identified in Gmail → Auto-created in CRM
- Data extracted: Name, email, company, inquiry details, source
- Conversation history linked to lead record
- Duplicate detection (don't create same lead twice)
- 100% capture rate (zero missed leads)

**Priority:** ⭐⭐⭐⭐⭐ Critical

**Status:** Draft - Pending CRM selection

**Technical Notes:**
- Gmail API → CRM API integration
- Zapier/Make.com/n8n for automation workflow
- Data mapping and field validation
- Error handling for failed entries

---

#### 3. Conversion Funnel Tracking

##### FR3.1: Funnel Stage Tracking
**Requirement:** System must track leads through sales funnel stages

**Acceptance Criteria:**
- Stages: Inquiry → Qualification → Proposal → Meeting → Closed (Won/Lost)
- Auto-advancement based on email activity (e.g., proposal sent → "Proposal" stage)
- Manual stage updates by partner
- Time-in-stage metrics (how long at each stage)
- Drop-off analysis (where leads go cold)

**Priority:** ⭐⭐⭐⭐ High

**Status:** ⚠️ Pending - Sales process mapping in strategy call

**Technical Notes:**
- CRM pipeline configuration
- Triggers for stage advancement
- Email pattern matching (e.g., "proposal attached" → move to Proposal stage)

---

##### FR3.2: Conversion Metrics Dashboard
**Requirement:** System must provide visibility into conversion rates

**Acceptance Criteria:**
- Total leads by source (website, referral, cold outreach, etc.)
- Conversion rate by stage (Inquiry→Qualification: X%, Qualification→Proposal: Y%)
- Average time to convert (Inquiry→Closed Won)
- Drop-off points identified (where most leads go cold)
- Meeting booking rate (from cold lead to scheduled meeting)
- Revenue attribution (which leads closed, deal size)

**Priority:** ⭐⭐⭐⭐ High

**Status:** ⚠️ Pending - Baseline metrics unknown, need historical data analysis

**Technical Notes:**
- CRM native analytics or custom dashboard
- Historical data may not exist (establish baseline going forward)
- Partner needs weekly review habit (analytics only useful if reviewed)

---

#### 4. Lead Reactivation Workflow

##### FR4.1: Warm Lead Identification
**Requirement:** System must identify reactivation opportunities from historical leads

**Acceptance Criteria:**
- Analyzes email history to find warm leads (engaged but didn't convert)
- Categorizes by: Time since last contact, engagement level, drop-off stage
- Prioritizes: Recently ghosted (1-3 months) > older leads (3-6 months)
- Excludes: Explicit rejections, unsubscribes, closed-lost with reason
- Surfaces X warm leads per week for partner review

**Priority:** ⭐⭐⭐⭐ High (Quick win potential)

**Status:** ⚠️ Pending - Need to analyze historical email for reactivation pool size

**Technical Notes:**
- Gmail historical analysis (permission required)
- AI sentiment analysis (was it truly warm or cold rejection?)
- Exclusion rules (don't be annoying)

---

##### FR4.2: Tactical Reactivation Messaging
**Requirement:** System must support tactical (non-aggressive) reactivation outreach

**Acceptance Criteria:**
- Email template library for reactivation (4-6 templates)
- Templates: Value-add approach (not "just checking in")
- Examples: New case study, industry insight, limited offer, process improvement
- **Manual approval required** - Partner reviews and approves before sending
- Personalization fields (name, company, previous inquiry topic)
- A/B testing capability (test different messaging approaches)

**Priority:** ⭐⭐⭐ Medium

**Status:** Draft - Messaging strategy to be defined in strategy call

**Technical Notes:**
- Email sending via Gmail API or SMTP
- Template management (editable by partner)
- Approval workflow (no auto-send without human approval)
- Unsubscribe/opt-out mechanism (legal requirement)
- Cadence limits (no spam: max 1 email per lead per month)

---

##### FR4.3: Reactivation Performance Tracking
**Requirement:** System must track effectiveness of reactivation efforts

**Acceptance Criteria:**
- Reactivation emails sent: X
- Response rate: Y%
- Meeting booked: Z
- Closed won from reactivation: €€€
- Template performance comparison (which messaging works best)
- ROI calculation (time invested vs meetings/revenue generated)

**Priority:** ⭐⭐⭐ Medium

**Status:** Draft - Metrics framework to be confirmed

**Technical Notes:**
- Email tracking (open rate, reply rate)
- Attribution model (reactivation → meeting → closed won)
- Report format (weekly summary for partner)

---

### Phase 2 Requirements (Outbound Lead Generation - Future)

**Scope:** TBD after Phase 1 proven successful and sales strategy clarified

**Potential Features:**
- Automated cold outbound email sequences (if strategy shifts)
- LinkedIn integration for prospecting
- Website visitor tracking (who visited, what they viewed)
- Newsletter automation (if content creation capacity exists)
- Calendly/booking system integration (streamline meeting scheduling)
- Lead scoring model (prioritize highest-value prospects)

**Dependency:** Requires clear sales strategy from Sindbad and partner

---

## Cross-Project Requirements

### 1. Security & Privacy

#### SR1.1: Data Protection
**Requirement:** All client data must be handled securely

**Acceptance Criteria:**
- **Encryption:** Data at rest and in transit (TLS 1.2+)
- **Access control:** Role-based permissions (Sindbad admin, team member read-only)
- **Audit trail:** All data access and modifications logged
- **Backup:** Daily automated backups with 30-day retention
- **Data residency:** EU/GDPR compliant storage (Sindbad is Paris-based)

**Priority:** ⭐⭐⭐⭐⭐ Critical (Non-negotiable)

---

#### SR1.2: Payment Security
**Requirement:** Payment data must meet highest security standards

**Acceptance Criteria:**
- **PCI compliance:** If storing payment info (prefer not to store)
- **MFA:** Multi-factor authentication for payment execution
- **Approval workflow:** Human approval required before any payment
- **Fraud detection:** Anomaly detection for unusual payment patterns

**Priority:** ⭐⭐⭐⭐⭐ Critical (Non-negotiable)

---

### 2. Integration Architecture

#### IA1.1: Google Workspace Integration
**Requirement:** Seamless integration with Google ecosystem

**Acceptance Criteria:**
- **Gmail API:** Email parsing and sending
- **Google Sheets API:** Dashboard read/write
- **Google Docs API:** Invoice parsing (if needed)
- **OAuth 2.0:** Secure authentication
- **Rate limits:** Respect API quotas, implement backoff
- **Error handling:** Graceful degradation if API unavailable

**Priority:** ⭐⭐⭐⭐⭐ Critical

---

#### IA1.2: Third-Party Integrations
**Requirement:** Integrate with selected third-party tools

**Acceptance Criteria:**
- **Wise API:** Payment batch preparation and execution (pending capability validation)
- **CRM API:** Lead management (HubSpot, Pipedrive, or selected tool)
- **Automation platform:** n8n or Make.com for workflow orchestration
- **AI API:** ChatGPT or equivalent for document/email analysis
- **Version control:** API version pinning (avoid breaking changes)

**Priority:** ⭐⭐⭐⭐ High

---

### 3. User Experience

#### UX1.1: Simplicity First
**Requirement:** System must be simple to use, minimal training required

**Acceptance Criteria:**
- **Ambushed:** Email forwarding + dashboard review (2 steps max)
- **Bold Move TV:** Auto-capture + partner CRM usage (zero extra steps)
- **Onboarding:** <30 minutes training per user
- **Documentation:** Clear, concise, with screenshots
- **Support:** Email support during business hours (EU timezone)

**Priority:** ⭐⭐⭐⭐ High

---

#### UX1.2: Mobile Accessibility
**Requirement:** Sindbad must be able to approve payments from mobile

**Acceptance Criteria:**
- Dashboard responsive design (works on phone)
- One-click approval for validated invoices
- Email notifications with approval links
- No app download required (web-based)

**Priority:** ⭐⭐⭐ Medium (Nice-to-have, not critical for v1)

---

### 4. Performance & Reliability

#### PR1.1: Processing Speed
**Requirement:** System must process data quickly

**Acceptance Criteria:**
- **Ambushed:** Invoice batch processing <5 minutes for 20 invoices
- **Bold Move TV:** Email-to-CRM capture <2 minutes per email
- **Dashboard:** Load time <3 seconds
- **API calls:** <1 second response time

**Priority:** ⭐⭐⭐⭐ High

---

#### PR1.2: Uptime & Reliability
**Requirement:** System must be available when needed

**Acceptance Criteria:**
- **Uptime:** 99.5% (approximately 3.5 hours downtime per month acceptable)
- **Graceful degradation:** Manual fallback if automation fails
- **Error notifications:** Alert Sindbad and Sway if system errors
- **Monitoring:** Real-time health checks and alerts

**Priority:** ⭐⭐⭐⭐ High

---

## Success Criteria Summary

### Ambushed Payment System

**Quantitative Metrics:**
- ✅ Time reduction: 5-6 hours/week → 1-2 hours/week (≥80% reduction)
- ✅ Error detection: ≥10% (match or exceed Sindbad's manual rate)
- ✅ Payment accuracy: 100% (zero payment errors)
- ✅ Processing time: <5 minutes per batch
- ✅ ROI: <12 months payback period

**Qualitative Metrics:**
- ✅ Sindbad reports time savings reinvested in strategic work
- ✅ Admin team reports process improvements (not job threat)
- ✅ Sindbad trusts system enough to approve without re-checking
- ✅ Weekly payment cadence maintained (cash flow protected)
- ✅ Partner relationship neutral or improved (no blame games)

---

### Bold Move TV Lead System

**Quantitative Metrics:**
- ✅ Lead capture: 100% (zero missed emails)
- ✅ Categorization accuracy: ≥90%
- ✅ Partner CRM usage: ≥5 days/week
- ✅ Meeting conversion: 2x baseline (from 1 in 3 months)
- ✅ Reactivation response rate: ≥10%

**Qualitative Metrics:**
- ✅ Partner reports system saves time (not creates work)
- ✅ Conversion funnel visibility enables strategic decisions
- ✅ Warm lead reactivation feels tactical, not spammy
- ✅ Sales strategy clarity improves (automation serves strategy)
- ✅ Sindbad reports Bold Move TV sales progress

---

## Constraints & Assumptions

### Budget Constraints
- **Ambushed:** Budget available (pays Sindbad's bills, €15K-25K estimated acceptable)
- **Bold Move TV:** Limited budget (not yet profitable, prefer low-cost tools)
- **Combined:** Prioritize Ambushed first to unlock Bold Move TV investment

### Technical Constraints
- **Google Workspace:** Must work within Google ecosystem (Sheets, Gmail, Docs)
- **Wise API:** Capabilities unknown (may require manual upload)
- **CRM:** Must be partner-approved (adoption critical)
- **AI:** ChatGPT or equivalent (German language support required)

### Time Constraints
- **Ambushed:** Weekly payment cadence non-negotiable (cash flow critical)
- **Bold Move TV:** No hard deadline, but sales need improving
- **Development:** 8-12 weeks per project estimated (to be refined in architecture phase)

### Human Constraints
- **Sindbad:** Limited time for training, prefers set-and-forget automation
- **Admin team:** Need buy-in, fear of job loss, require communication
- **Partner:** Must adopt CRM daily, unclear current engagement level
- **Freelancers:** 70-80 people, international, no workflow change needed

### Assumptions (TO BE VALIDATED)
- ⚠️ Admin team willing to participate in discovery and implementation
- ⚠️ Bold Move TV partner committed to sales process improvement
- ⚠️ Google Sheets dashboard structure is stable and documented
- ⚠️ Wise API supports required batch payment workflow
- ⚠️ Historical email data available for lead reactivation analysis
- ⚠️ Sindbad has authority to approve automation investment for both companies
- ⚠️ Error patterns are consistent and learnable (10% rate is not random)

---

## Next Steps

### Immediate (This Week)
1. ✅ Send calendar link to Sindbad
2. ⏳ Conduct Ambushed admin team discovery call
3. ⏳ Conduct Bold Move TV strategy call with partner
4. ⏳ Document dashboard structure and validation rules
5. ⏳ Analyze historical email for lead reactivation pool

### Short-Term (Next 2 Weeks)
1. ⏳ Update this requirements document with detailed functional specs
2. ⏳ Create technical architecture document (API integrations, data flows)
3. ⏳ Validate Wise API capabilities (payment automation feasibility)
4. ⏳ Finalize CRM recommendation (partner buy-in critical)
5. ⏳ Calculate detailed ROI with real data (not estimates)
6. ⏳ Create formal proposal with pricing and timeline

### Medium-Term (Month 1)
1. ⏳ Contract signed and development kickoff
2. ⏳ Begin Ambushed payment system development (recommended first)
3. ⏳ Weekly check-ins with Sindbad and admin team
4. ⏳ Iterative testing and feedback loop

---

## Appendices

### Appendix A: Tool Stack (Current State)

**Ambushed:**
- Google Sheets (project dashboard, monthly tabs)
- Google Docs (invoice templates)
- Wise (international payment platform)
- Gmail (communication)

**Bold Move TV:**
- Gmail (lead inbox)
- Google Sheets ("Request Tracker" manual CRM)
- Website (boldmove.tv, recently updated)

### Appendix B: Team Structure

**Ambushed:**
- Sindbad (co-founder, handles all finances)
- Business partner (recruitment, diverging vision, separate AI business)
- 7 core team members (admin, production)
- 70-80 freelancers (international, paid weekly)

**Bold Move TV:**
- Sindbad (founder, part-time)
- 1 full-time employee (operations manager)
- 1 part-time employee (writer/admin/sales)
- Partner (needs to join strategy call)

### Appendix C: Volume Metrics

**Ambushed:**
- ~50 pitches per month
- 15-20 payments per week
- 5-6 hours per week validation (Sindbad)
- 10% error rate (flagged before payment)
- 3-4 week payment window promise

**Bold Move TV:**
- 1 meeting in 3 months (current sales performance)
- Unknown lead volume (no systematic tracking)
- Unknown conversion rate (no funnel data)
- Manual email parsing (time cost unknown)

---

*Document Status: Draft pending follow-up discovery calls*
*Last Updated: January 12, 2026*
*Next Review: After admin team and partner calls (Week of Jan 13-17)*
