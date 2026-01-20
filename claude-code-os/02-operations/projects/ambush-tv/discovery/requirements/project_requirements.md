# Ambush TV - Project Requirements Document

**Project Name:** Ambush TV Automation System (Payment Validation + Admin Workflows)
**Client:** Sindbad Iksel - Ambush TV (Ambushed)
**Contact:** sindbad@boldmove.tv
**Last Updated:** January 18, 2026
**Status:** Draft - Based on Discovery Calls (Jan 8 & Jan 15, 2026)

---

## Executive Summary

### Project Vision

**Phase 1 (Quick Wins):** Automate rate synchronization across 3 Google Sheets, add dashboard validation rules, implement call recording workflow, and deploy calendar-based project reminders. Eliminate 2-3 hours/month admin team time and prevent upstream errors.

**Phase 2 (Invoice Validation):** Reduce Sindbad's weekly invoice reconciliation time from 5-6 hours to 1-2 hours (80-90% reduction) while maintaining or improving 10% error detection rate through automated validation with human approval checkpoints.

### Core Problems

**Problem 1: Manual Rate Synchronization (Leonor)**
Leonor manually updates freelancer rates across 3 separate Google Sheets (Team Directory → Freelancer Cost Assumptions → Dashboard) every time someone gets a raise. With batch raises of 5-10 freelancers and 70-80 total freelancers, this creates high error risk. Spends "whole day a month" (2+ hours) just verifying rate consistency. Rate discrepancies cause downstream errors in Sindbad's invoice validation.

**Problem 2: Freelancer Invoice Reconciliation (Sindbad)**
Sindbad spends 5-6 hours every week (20+ hours/month) manually reviewing 15-20 freelancer invoices, checking hours against Google Sheets dashboard, verifying rates, and processing payments through Wise. Must be weekly for cash flow management. Currently catches errors about 10% of time: projects not entered in dashboard (unbilled work), rate discrepancies, excessive hours.

**Problem 3: Month-End Invoicing Delays (Admin Team)**
No systematic reminders based on project end dates. Hours collection and client invoicing slip 1-2 months sometimes, creating "awkward" late payment requests. Mental burden of tracking which projects need close-out.

### Proposed Solution

**Quick Wins (Phase 1):**
1. **Rate Synchronization:** Single source of truth (Team Directory) → auto-sync to FCA and Dashboard via Google Sheets API
2. **Dashboard Validation:** Real-time error checking (missing projects, rate discrepancies, hour thresholds)
3. **Call Recording:** Fathom → auto-transcription → extract rate changes → Discord/email summary
4. **Calendar Reminders:** Project end date → 4-day (hours) and 7-day (invoicing) automated reminders

**Invoice Validation (Phase 2):**
Automated invoice validation system that cross-references Google Sheets dashboard, flags discrepancies, maintains human approval checkpoint before Wise batch payments.

**Strategic Priority:** Quick wins first (4-6 weeks, €5K-10K) to build trust and reduce upstream errors, then invoice validation (8-10 weeks, €15K-20K) for largest time savings.

### Success Metrics

**Quick Wins:**
- **Time reduction:** 2-3 hours/month (admin team)
- **Error prevention:** Zero rate discrepancies, 50%+ dashboard errors caught upstream
- **Adoption:** Admin team daily usage, Leonor 80%+ Fathom usage
- **ROI timeline:** 2-4 months payback

**Invoice Validation:**
- **Time reduction:** 80-90% (5-6 hours/week → 1-2 hours/week)
- **Error detection:** ≥10% (match or exceed current manual rate)
- **Payment accuracy:** 100% (zero errors)
- **Admin team satisfaction:** ≥4/5
- **ROI timeline:** 8-12 months payback

---

## Project 1: Quick Wins (Phase 1)

### 1.1 Rate Synchronization Automation

#### FR1.1: Google Sheets Integration
**Requirement:** System must read and write across Team Directory, FCA, and Dashboard sheets

**Acceptance Criteria:**
- Connects to all 3 Google Sheets via API
- Team Directory is single source of truth for rates
- Rate change in Team Directory triggers automatic sync to FCA and Dashboard
- Updates occur in real-time or near real-time (within 5 minutes)
- Handles edge cases: currency changes (EUR → GBP), retroactive raises, new hire onboarding

**Priority:** ⭐⭐⭐⭐⭐ Critical

**Technical Notes:**
- Google Sheets API v4
- OAuth 2.0 authentication
- Read/write permissions required
- n8n or Make.com automation platform

---

#### FR1.2: Single Source of Truth Logic
**Requirement:** Team Directory rate field is authoritative, all other sheets sync from it

**Acceptance Criteria:**
- Rate changes only made in Team Directory (enforced via sheet protection)
- FCA and Dashboard are read-only for rate column (manual edits blocked)
- Sync logic detects Team Directory changes via webhook or polling
- Validation check before sync (prevent bad data propagation)
- Rollback capability if sync fails

**Priority:** ⭐⭐⭐⭐⭐ Critical

**Technical Notes:**
- Google Sheets triggers (onChange event)
- Data validation rules in FCA and Dashboard
- Audit trail of all rate changes (timestamp, user, old value, new value)

---

#### FR1.3: Rate Sync Audit Trail
**Requirement:** System must log all rate changes for compliance and debugging

**Acceptance Criteria:**
- Audit log captures: Timestamp, freelancer name, old rate, new rate, user who made change
- Log stored in separate "Audit Trail" sheet tab or external database
- Searchable by freelancer name, date range, user
- Accessible to Sindbad and admin team
- Retained for at least 2 years

**Priority:** ⭐⭐⭐⭐ High

**Technical Notes:**
- Append-only log (no deletions)
- CSV export capability for external audits
- Integration with existing Team Directory "Raise History" if it exists

---

### 1.2 Dashboard Validation Rules

#### FR2.1: Real-Time Error Detection
**Requirement:** System must validate data entry in Dashboard and flag errors immediately

**Acceptance Criteria:**
- **Missing projects:** Project entered in Dashboard but not in master project list → FLAG
- **Rate discrepancies:** Dashboard rate ≠ FCA rate for same freelancer → FLAG
- **Hour thresholds:** Hours exceed expected range for project type → WARNING
- **Duplicate entries:** Same freelancer + project + month entered twice → FLAG
- **Missing required fields:** Project name, freelancer name, hours, or rate blank → FLAG

**Priority:** ⭐⭐⭐⭐ High

**Technical Notes:**
- Google Apps Script (Sheets scripting)
- Conditional formatting for visual error highlighting
- Data validation rules (dropdowns for project names, freelancer names)
- Real-time validation on cell edit (onEdit trigger)

---

#### FR2.2: Notification System
**Requirement:** System must notify admin team of validation errors

**Acceptance Criteria:**
- Pop-up alert in Google Sheets when error detected
- Optional Discord webhook notification for high-priority errors (missing projects)
- Email summary of errors at end of day (if any errors detected)
- Error list visible in dedicated "Errors" tab or sidebar

**Priority:** ⭐⭐⭐ Medium

**Technical Notes:**
- Google Apps Script UI alerts
- Discord webhook integration
- Gmail API for email summaries
- Error categorization: High (blocks workflow), Medium (review recommended), Low (informational)

---

### 1.3 Call Recording & Transcription

#### FR3.1: Fathom Integration
**Requirement:** System must automatically process call transcripts and extract rate changes

**Acceptance Criteria:**
- Leonor uses Fathom to record feedback calls with freelancers
- Post-call automation triggers via Fathom webhook or API
- Transcript extracted and parsed for rate change keywords ("raised to €X/hour", "new rate", etc.)
- Rate change data sent to Leonor via email or Discord
- Optional: Automatically trigger rate sync in Team Directory (with approval)

**Priority:** ⭐⭐⭐ Medium

**Technical Notes:**
- Fathom API or webhook
- n8n/Make.com for post-call automation
- AI-powered transcript parsing (ChatGPT or regex)
- Email template for rate change summary

---

#### FR3.2: Call Summary Delivery
**Requirement:** System must deliver call summaries to admin team's daily tools

**Acceptance Criteria:**
- Summary includes: Freelancer name, rate change (if any), feedback highlights, action items
- Delivered via email (Gmail) or Discord (admin team preference)
- Delivered within 5 minutes of call ending
- Archive of all call summaries searchable by freelancer name or date

**Priority:** ⭐⭐⭐ Medium

**Technical Notes:**
- Gmail API or Discord webhook
- Summary template (Markdown or plain text)
- Google Drive folder for transcript archives

---

### 1.4 Calendar Reminder System

#### FR4.1: Project End Date Triggers
**Requirement:** System must trigger reminders based on project end dates from Dashboard

**Acceptance Criteria:**
- Dashboard project end date is authoritative
- 4 days post-project end: Reminder to collect all freelancer hours
- 7 days post-project end: Reminder to send client invoice with recap
- Reminders sent to admin team via Discord or email
- Snooze/dismiss functionality (if project extended, reschedule reminder)

**Priority:** ⭐⭐⭐⭐ High

**Technical Notes:**
- Google Calendar integration with Dashboard
- Daily cron job checks for projects ending 4 or 7 days ago
- Discord webhook or Gmail API for notifications
- State tracking (which projects already reminded)

---

#### FR4.2: Project Close-Out Report
**Requirement:** System must generate weekly report of projects awaiting close-out

**Acceptance Criteria:**
- Lists all projects past end date without hours collected
- Lists all projects with hours collected but invoice not sent
- Report sent every Monday morning to admin team
- Includes project name, end date, status (awaiting hours / awaiting invoice)

**Priority:** ⭐⭐ Low (Nice-to-have)

**Technical Notes:**
- Weekly cron job (Monday 9am)
- Dashboard query for project status
- Email or Discord summary

---

## Project 2: Invoice Validation System (Phase 2)

### 2.1 Data Integration

#### FR5.1: Google Sheets Dashboard Integration
**Requirement:** System must read project data from Ambush Google Sheets dashboard

**Acceptance Criteria:**
- Connects to Google Sheets via API
- Reads monthly tabs (current month + previous months for validation)
- Extracts: Project names, freelancer names, hours worked, hourly rates, total amounts
- Handles multiple freelancers per project
- Updates in real-time or near real-time (within 5 minutes of changes)

**Priority:** ⭐⭐⭐⭐⭐ Critical

**Status:** Pending - Dashboard structure needs review

**Technical Notes:**
- Google Sheets API v4
- OAuth 2.0 authentication
- Read-only access (minimize security risk)
- Dashboard has monthly tab structure (format to be confirmed)

---

#### FR5.2: Invoice Intake & Parsing
**Requirement:** System must automatically process freelancer invoices submitted via email

**Acceptance Criteria:**
- Accepts invoices via email forwarding (freelancers email invoices)
- Supports formats: PDF (Google Docs templates), DOC, DOCX, images
- Extracts: Freelancer name, project name, hours, rate, total amount, invoice date
- Handles 15-20 invoices per batch (weekly volume)
- Preserves original invoice files for audit trail

**Priority:** ⭐⭐⭐⭐⭐ Critical

**Status:** Pending - Invoice format needs confirmation

**Technical Notes:**
- Gmail API for email-based intake
- OCR for image-based invoices (if needed)
- Document AI or ChatGPT for structured data extraction
- Freelancers use Google Docs templates (format to be confirmed)

---

### 2.2 Validation Logic

#### FR6.1: Cross-Reference Validation
**Requirement:** System must validate invoice data against dashboard data

**Acceptance Criteria:**
- **Project validation:** Confirm project exists in dashboard
- **Freelancer validation:** Confirm freelancer worked on this project
- **Hours validation:** Confirm hours match dashboard entry (within tolerance)
- **Rate validation:** Confirm rate matches FCA rate for freelancer
- **Total calculation:** Confirm math is correct (hours × rate)
- **Date validation:** Confirm work falls within project timeline

**Priority:** ⭐⭐⭐⭐⭐ Critical

**Status:** Pending - Validation rules need confirmation

**Technical Notes:**
- Fuzzy matching for project/freelancer names (typo tolerance)
- Threshold for "close enough" vs "discrepancy" (e.g., ±1 hour acceptable)
- Historical data available for ML training (optional)

---

#### FR6.2: Error Detection & Flagging
**Requirement:** System must detect and flag discrepancies for manual review

**Acceptance Criteria:**
- **Missing projects:** Invoice for project not in dashboard → FLAG (High priority)
- **Rate discrepancies:** Invoice rate ≠ FCA rate → FLAG (Medium priority)
- **Hour discrepancies:** Invoice hours ≠ dashboard hours → FLAG (Medium priority)
- **Excessive hours:** Hours seem unreasonable for project scope → FLAG (Low priority)
- **Missing information:** Required fields blank → FLAG (High priority)
- **Duplicate invoices:** Same freelancer + project + period → FLAG (High priority)

**Priority:** ⭐⭐⭐⭐⭐ Critical (This is the 10% error rate Sindbad currently catches)

**Status:** Pending - Error patterns need documentation

**Technical Notes:**
- Error severity levels: High (blocks payment), Medium (review recommended), Low (informational)
- AI-powered anomaly detection (optional enhancement)
- Historical error data for training (if available)

---

#### FR6.3: Quality Control Dashboard
**Requirement:** System must provide Sindbad with review queue for flagged items

**Acceptance Criteria:**
- Dashboard shows all invoices with validation status (✅ Pass, ⚠️ Warning, ❌ Fail)
- Flagged items shown first (prioritized by severity)
- Sindbad can approve, reject, or edit flagged invoices
- Approved invoices move to payment preparation queue
- Rejected invoices notify freelancer with reason
- Edit capability to correct minor errors without rejecting

**Priority:** ⭐⭐⭐⭐⭐ Critical (Human-in-the-loop requirement)

**Status:** Draft - UI/UX to be designed after workflow validation

**Technical Notes:**
- Web dashboard (responsive design for mobile review)
- Email notification when flagged items require review
- Approval workflow: Single-click approve for batch, individual review for flags
- Audit trail of all approvals/edits/rejections

---

### 2.3 Payment Integration

#### FR7.1: Wise Batch Payment Preparation
**Requirement:** System must prepare batch payment file for Wise integration

**Acceptance Criteria:**
- Generates Wise-compatible batch payment file (CSV or API format)
- Includes: Freelancer name, payment amount, currency, bank details, reference
- Only includes approved invoices (passed validation + Sindbad approval)
- Handles international payments (70-80 freelancers globally)
- Maintains 3-4 week payment window promise to freelancers

**Priority:** ⭐⭐⭐⭐ High

**Status:** Pending - Wise API capabilities need validation

**Technical Notes:**
- Wise API or batch CSV upload (to be confirmed)
- Freelancer bank details stored securely (encryption required)
- Payment reference format (to be confirmed with Sindbad)
- Weekly cadence requirement (cash flow critical)

---

#### FR7.2: Payment Execution
**Requirement:** System must execute batch payments via Wise

**Acceptance Criteria:**
- **Option A:** Sindbad manually uploads batch file to Wise (lowest risk)
- **Option B:** System auto-uploads to Wise, Sindbad approves in Wise (medium risk)
- **Option C:** Full automation with Sindbad audit trail (highest automation, build trust first)
- Payment confirmation captured and logged
- Failed payments flagged for manual intervention

**Priority:** ⭐⭐⭐ Medium (Start with Option A, scale to B/C over time)

**Status:** TBD - Depends on Sindbad's comfort level and Wise API capabilities

**Technical Notes:**
- Security critical: Payment execution requires high trust
- Recommend phased approach: Start manual, automate incrementally
- MFA/2FA considerations for API access
- Wise API documentation review required

---

### 2.4 Reporting & Analytics

#### FR8.1: Weekly Validation Report
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

#### FR8.2: Admin Team Performance Insights (Optional)
**Requirement:** System may identify upstream inefficiencies in admin team workflow

**Acceptance Criteria:**
- Track error sources: Admin entry errors vs freelancer invoice errors
- Identify patterns: Which admin team members have higher error rates
- Suggest process improvements: "Projects frequently missing from dashboard"
- Sensitivity: Present insights tactfully (coaching, not punishment)

**Priority:** ⭐ Low (Nice-to-have, politically sensitive)

**Status:** TBD - Depends on admin team buy-in and Sindbad's interest

**Technical Notes:**
- Only implement if admin team feels supported, not surveilled
- Frame as "process improvement" not "performance monitoring"
- Optional feature, not core requirement

---

## Cross-Project Requirements

### 3.1 Security & Privacy

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

### 3.2 Integration Architecture

#### IA1.1: Google Workspace Integration
**Requirement:** Seamless integration with Google ecosystem

**Acceptance Criteria:**
- **Gmail API:** Email parsing and sending
- **Google Sheets API:** Dashboard read/write (Team Directory, FCA, Dashboard)
- **Google Calendar API:** Project date tracking and reminders
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
- **Fathom API:** Call transcript extraction
- **Discord API:** Webhook for team notifications
- **n8n/Make.com:** Workflow orchestration platform
- **AI API:** ChatGPT or equivalent for document/email analysis
- **Version control:** API version pinning (avoid breaking changes)

**Priority:** ⭐⭐⭐⭐ High

---

### 3.3 User Experience

#### UX1.1: Simplicity First
**Requirement:** System must be simple to use, minimal training required

**Acceptance Criteria:**
- **Rate sync:** Leonor updates Team Directory once, done (0 extra steps)
- **Dashboard validation:** Real-time alerts in Google Sheets (familiar interface)
- **Call recording:** Fathom auto-triggers, summaries delivered to email/Discord
- **Invoice validation:** Email forwarding + dashboard review (2 steps max)
- **Onboarding:** <30 minutes training per user
- **Documentation:** Clear, concise, with screenshots

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

### 3.4 Performance & Reliability

#### PR1.1: Processing Speed
**Requirement:** System must process data quickly

**Acceptance Criteria:**
- **Rate sync:** <30 seconds from Team Directory update to FCA/Dashboard sync
- **Dashboard validation:** <1 second error detection on cell edit
- **Invoice batch:** <5 minutes processing for 20 invoices
- **Calendar reminders:** Delivered within 1 hour of trigger time

**Priority:** ⭐⭐⭐⭐ High

---

#### PR1.2: Uptime & Reliability
**Requirement:** System must be available when needed

**Acceptance Criteria:**
- **Uptime:** 99.5% (approximately 3.5 hours downtime per month acceptable)
- **Graceful degradation:** Manual fallback if automation fails
- **Error notifications:** Alert admin team and Sway if system errors
- **Monitoring:** Real-time health checks and alerts

**Priority:** ⭐⭐⭐⭐ High

---

## Success Criteria Summary

### Quick Wins (Phase 1)

**Quantitative Metrics:**
- ✅ Time reduction: 2-3 hours/month (admin team verification eliminated)
- ✅ Error prevention: Zero rate discrepancies across sheets
- ✅ Dashboard validation: 50%+ errors caught before Sindbad review
- ✅ Fathom adoption: 80%+ of feedback calls recorded
- ✅ Calendar reminders: 100% delivery within 24 hours
- ✅ ROI: <4 months payback period

**Qualitative Metrics:**
- ✅ Admin team reports "single update" workflow (Leonor)
- ✅ Madalena reports tool integration success
- ✅ Fathom summaries useful in Discord/email
- ✅ No missed project close-outs due to reminders
- ✅ Team reports reduced stress and mental load

---

### Invoice Validation (Phase 2)

**Quantitative Metrics:**
- ✅ Time reduction: 5-6 hours/week → 1-2 hours/week (≥80% reduction)
- ✅ Error detection: ≥10% (match or exceed Sindbad's manual rate)
- ✅ Payment accuracy: 100% (zero payment errors)
- ✅ Processing time: <5 minutes per batch
- ✅ ROI: <12 months payback period

**Qualitative Metrics:**
- ✅ Sindbad reports time savings reinvested in Bold Move TV / screenplay
- ✅ Admin team reports process improvements (not job threat)
- ✅ Sindbad trusts system enough to approve without re-checking
- ✅ Weekly payment cadence maintained (cash flow protected)
- ✅ Partner relationship neutral or improved (no blame games)

---

## Constraints & Assumptions

### Budget Constraints
- **Ambush:** Budget available (pays Sindbad's bills, €20K-30K estimated acceptable)
- **Quick wins:** €5K-10K budget
- **Invoice validation:** €15K-20K budget
- **Combined:** Prioritize quick wins first, invoice validation after ROI proven

### Technical Constraints
- **Google Workspace:** Must work within Google ecosystem (Sheets, Gmail, Calendar)
- **Free tools only:** Discord (not Slack), Google Workspace Free (not Notion)
- **Wise API:** Capabilities unknown (may require manual upload)
- **n8n/Make.com:** API automation platform (budget: €20/month max)

### Time Constraints
- **Weekly payment cadence:** Non-negotiable (cash flow critical)
- **Madalena availability:** On holiday Jan 22 - Feb 9 (available Mondays)
- **Development:** 4-6 weeks quick wins, 8-10 weeks invoice validation

### Human Constraints
- **Sindbad:** Limited time for training, prefers set-and-forget automation
- **Admin team:** Need buy-in, fear of job loss, require communication
- **Leonor:** Values personalized feedback time, wants admin burden reduced
- **Madalena:** Technical, frustrated by past failures, wants integrations to work
- **Freelancers:** 70-80 people, international, no workflow change needed

### Assumptions (TO BE VALIDATED)
- ⚠️ Admin team willing to participate in implementation and testing
- ⚠️ Google Sheets schemas are stable and documented
- ⚠️ Wise API supports required batch payment workflow
- ⚠️ Fathom can extract rate changes from call transcripts
- ⚠️ Discord webhooks sufficient for notifications (vs custom bot)
- ⚠️ Sindbad has authority to approve automation investment
- ⚠️ Error patterns are consistent and learnable (10% rate is not random)

---

## Next Steps

### Immediate (This Week)
1. ⏳ Analyze Team Directory, FCA, and Dashboard sheet structures
2. ⏳ Validate Wise API capabilities (batch payment feasibility)
3. ⏳ Create quick wins proposal with pricing and timeline
4. ⏳ Send calendar link for proposal review call

### Short-Term (Next 2 Weeks)
1. ⏳ Present proposal to Sindbad and admin team
2. ⏳ Finalize contract and development timeline
3. ⏳ Design API integration architecture (rate sync, dashboard validation)
4. ⏳ Set up development environment (n8n cloud, API keys)
5. ⏳ Begin quick wins development

### Medium-Term (Month 1)
1. ⏳ Deploy rate synchronization automation
2. ⏳ Deploy dashboard validation rules
3. ⏳ Set up Fathom integration
4. ⏳ Deploy calendar reminder system
5. ⏳ Admin team training and handoff
6. ⏳ Weekly check-ins and iterative improvements

---

## Appendices

### Appendix A: Tool Stack (Current State)

**Communication:**
- Discord (free, team chat)
- Gmail (email)

**Project Management:**
- Google Sheets (Dashboard, FCA, Team Directory)
- Google Calendar (project timelines)
- Google Docs (invoice templates)

**Payments:**
- Wise (international payment platform, batch capable)

**Call Recording:**
- None currently (will add Fathom)

**Attempted:**
- Notion (too expensive)
- Fireflies, Otter (hit limits)
- ChatGPT (formula building, partial success)

**Proposed Additions:**
- Fathom (free call recording)
- n8n cloud (€20/month API automation)

---

### Appendix B: Team Structure

**Ambush Core Team:**
- Sindbad Iksel (co-founder, handles all finances and payments)
- Pierre (business partner, handles recruitment, diverging visions)
- Leonor Zuzarte (rate management, freelancer feedback)
- Madalena Ribeiro da Fonseca (systems and automation)
- Alice Carreto (admin team member)
- 4 other core team members (roles TBD)

**Freelancer Network:**
- 70-80 freelancers (international)
- Paid weekly via Wise
- Submit invoices via email (Google Docs templates)

---

### Appendix C: Volume Metrics

**Ambush Operations:**
- ~50 pitches per month
- 15-20 payments per week
- 5-6 hours per week validation (Sindbad)
- 2+ hours per month rate verification (Leonor)
- 10% error rate (flagged before payment)
- 3-4 week payment window promise

**Rate Management:**
- New hires: 2-3 raises in first year
- Mid-level: 1-2 raises per year
- Batch raises: 5-10 freelancers at once
- Sliding scale: €X/hour start → €Y/hour maximum

---

*Document Status: Draft pending sheet structure analysis and Wise API validation*
*Last Updated: January 18, 2026*
*Next Review: After proposal presentation (Week of Jan 25-31)*
