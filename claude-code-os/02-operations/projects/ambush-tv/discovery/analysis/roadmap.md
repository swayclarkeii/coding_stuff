# Ambush TV - 6-12 Month Roadmap

**Created:** 2026-01-18
**Source:** 5 Discovery Transcripts (Jan 8 & Jan 15, 2026)
**Status:** Proposal Phase

---

## Executive Summary

This roadmap outlines a phased approach to automating Ambush TV's operational workflows, starting with quick wins that deliver immediate value and building toward comprehensive invoice automation.

**Total Investment:** €20,000-30,000
**Total Time Savings:** 20-25 hours/month
**Payback Period:** 8-14 months
**5-Year Value:** €120,000-150,000

---

## Phase Overview

```
Month 1-2: Quick Wins (Foundation)
├── Rate Synchronization
├── Fathom Call Recording
├── Dashboard Validation Rules
└── Calendar Reminder System

Month 3-4: Invoice Validation (Core Automation)
├── Invoice Parsing & Intake
├── Cross-Reference Validation
├── Error Flagging Dashboard
└── Wise Payment Prep

Month 5-6: Optimization & Scaling
├── Admin Team Training
├── Edge Case Handling
├── Process Refinement
└── Bold Move TV Discovery

Month 7-12: Continuous Improvement
├── Full Payment Automation (if trust established)
├── Freelancer Self-Service Portal
├── Advanced Analytics
└── Bold Move TV Implementation
```

---

## Month 1-2: Quick Wins (Foundation)

### Week 1-2: Rate Synchronization Automation
**Investment:** €2,000-3,000
**Time Savings:** 2+ hours/month

**Deliverables:**
- Team Directory as single source of truth
- Auto-sync to FCA and Dashboard via Google Sheets API
- Real-time rate updates across all sheets
- Audit trail of all rate changes

**Success Criteria:**
- Zero manual updates required after Team Directory change
- Zero rate discrepancies between sheets
- Leonor reports workflow improved

**Dependencies:**
- Access to Team Directory, FCA, Dashboard sheets
- n8n/Make.com automation platform setup

---

### Week 2-3: Fathom Call Recording Integration
**Investment:** €1,000-2,000
**Time Savings:** 1-2 hours/month

**Deliverables:**
- Fathom account setup for Leonor
- Post-call transcript extraction via API
- Summary sent to Discord/Email automatically
- Rate change detection triggers sync automation

**Success Criteria:**
- 80%+ feedback calls recorded
- Summaries delivered within 15 minutes of call end
- Rate changes extracted and flagged for sync

**Dependencies:**
- Fathom free account
- Rate sync automation (above)

---

### Week 3-4: Dashboard Validation Rules
**Investment:** €2,000-3,000
**Time Savings:** 6-8 hours/month

**Deliverables:**
- Google Apps Script validation in Dashboard
- Rate checking against FCA master
- Missing project alerts
- Hours threshold warnings (>10hr, >12hr flags)
- Duplicate entry detection

**Success Criteria:**
- 50%+ of current admin errors caught at entry time
- Sindbad's review time reduced by 30-40%
- Admin team reports helpful real-time feedback

**Dependencies:**
- Rate sync automation (ensures consistent rates)
- Understanding of current error patterns

---

### Week 4-5: Calendar Reminder System
**Investment:** €2,000-3,000
**Time Savings:** 2-3 hours/month

**Deliverables:**
- Google Calendar API integration
- 4-day reminder: Collect freelancer hours
- 7-day reminder: Send client invoice
- Discord/Email notifications to admin team
- Dashboard integration for project dates

**Success Criteria:**
- 100% of project end dates trigger reminders
- Invoicing within 7 days of project end
- Admin team reports reduced tracking burden

**Dependencies:**
- Dashboard project date schema understood
- Discord webhook or Gmail API setup

---

### Phase 1 Checkpoint: Week 6

**Review Meeting Agenda:**
1. Quick wins ROI assessment
2. Admin team feedback collection
3. Error rate comparison (before/after)
4. Time savings validation
5. Go/No-Go for Phase 2

**Expected Outcomes:**
- 5-7 hours/month saved (quick wins combined)
- Zero rate discrepancies
- Improved admin workflow satisfaction
- Foundation for invoice automation

---

## Month 3-4: Invoice Validation (Core Automation)

### Week 7-10: Invoice Parsing & Intake
**Investment:** €5,000-7,000

**Deliverables:**
- Gmail API integration for invoice emails
- Invoice parsing from Google Docs templates
- OCR for non-standard invoices (if needed)
- Structured data extraction: freelancer, project, hours, rate, total

**Success Criteria:**
- 95%+ invoices parsed automatically
- Data extraction accuracy >98%
- Processing within 5 minutes of receipt

**Dependencies:**
- Invoice template analysis
- Freelancer email patterns identified

---

### Week 10-12: Cross-Reference Validation
**Investment:** €4,000-6,000

**Deliverables:**
- Invoice data vs Dashboard cross-reference
- Error detection logic:
  - Missing projects (not in dashboard)
  - Rate discrepancies (invoice vs FCA)
  - Hours thresholds (>12hr automatic flag)
  - Project date mismatches
- Validation accuracy ≥10% (match Sindbad's manual rate)

**Success Criteria:**
- All invoices validated before reaching Sindbad
- Error types categorized and logged
- Historical error patterns identified

**Dependencies:**
- Dashboard schema documented
- Rate sync automation operational

---

### Week 12-14: Error Flagging Dashboard
**Investment:** €3,000-4,000

**Deliverables:**
- Sindbad-facing exception dashboard
- Flagged invoices with error details
- Approve/Reject/Edit workflow
- Human-in-the-loop checkpoint before payment
- Weekly validation summary report

**Success Criteria:**
- Sindbad reviews only flagged items (exceptions)
- Decision time per invoice <2 minutes
- Audit trail of all approvals

**Dependencies:**
- Validation logic operational
- UI/UX design approved

---

### Week 14-16: Wise Batch Payment Preparation
**Investment:** €3,000-4,000

**Deliverables:**
- Wise API integration (or CSV export)
- Batch payment file generation
- Approved invoices → payment-ready format
- Manual payment trigger (Option A) or API trigger (Option B)

**Success Criteria:**
- Payment prep time reduced from hours to minutes
- Zero payment errors during pilot
- Weekly payment cadence maintained

**Dependencies:**
- Wise API capabilities confirmed
- Error flagging dashboard operational

---

### Phase 2 Checkpoint: Week 16

**Review Meeting Agenda:**
1. Invoice validation accuracy assessment
2. Time savings measurement (target: 80% reduction)
3. Sindbad trust level evaluation
4. Payment accuracy verification
5. Scale to full operation decision

**Expected Outcomes:**
- 16-20 hours/month saved (Sindbad)
- ≥10% error detection rate maintained
- Zero payment errors
- Ready for full autonomous operation

---

## Month 5-6: Optimization & Scaling

### Week 17-20: Admin Team Training & Documentation
**Investment:** €2,000-3,000

**Deliverables:**
- Video walkthroughs for all automations
- Written SOPs for edge cases
- Troubleshooting guide
- FAQ documentation
- Admin team confidence building

**Success Criteria:**
- Admin team can handle 80% of issues independently
- Sindbad not required for routine operations
- Documentation complete and accessible

---

### Week 20-24: Edge Case Handling & Process Refinement
**Investment:** €2,000-3,000

**Deliverables:**
- Edge case identification from pilot period
- Additional validation rules for unusual scenarios
- Error handling improvements
- Performance optimization
- Alert system refinement

**Success Criteria:**
- Edge cases documented and automated
- System handles 98%+ of invoices without manual intervention
- Alert fatigue eliminated

---

### Bold Move TV Discovery (Parallel Track)
**Investment:** Included in consulting time

**Deliverables:**
- Lead generation strategy session
- CRM requirements definition
- Reactivation campaign design
- ROI projection based on Ambush learnings

**Success Criteria:**
- Clear sales strategy alignment
- Technical requirements documented
- Budget approved for Phase 3

---

## Month 7-12: Continuous Improvement

### Full Payment Automation (if trust established)
**Investment:** €3,000-5,000

**Deliverables:**
- Remove manual payment trigger
- Automated Wise API payments
- Exception handling for failed payments
- Reconciliation automation

**Prerequisites:**
- 3+ months zero payment errors
- Sindbad trust level ≥4/5
- Wise API fully validated

---

### Freelancer Self-Service Portal (Optional)
**Investment:** €8,000-15,000

**Deliverables:**
- Freelancer timesheet submission portal
- Invoice upload interface
- Status tracking for payments
- Rate history visibility

**Prerequisites:**
- Core automation stable
- Freelancer interest validated
- Budget approved

---

### Advanced Analytics (Optional)
**Investment:** €3,000-5,000

**Deliverables:**
- Project profitability dashboard
- Freelancer performance metrics
- Client payment behavior analysis
- Margin trend reporting

**Prerequisites:**
- 6+ months data collection
- Analytics requirements defined

---

### Bold Move TV Implementation
**Investment:** €10,000-15,000

**Deliverables:**
- Lead capture automation
- CRM integration
- Reactivation campaign system
- Conversion tracking

**Prerequisites:**
- Ambush automation proven successful
- Sales strategy finalized
- Budget allocated

---

## Timeline Summary

| Phase | Months | Investment | Time Savings | Cumulative |
|-------|--------|------------|--------------|------------|
| Quick Wins | 1-2 | €5K-10K | 5-7 hrs/mo | 5-7 hrs/mo |
| Invoice Validation | 3-4 | €15K-20K | +16-20 hrs/mo | 21-27 hrs/mo |
| Optimization | 5-6 | €4K-6K | (stabilization) | 21-27 hrs/mo |
| Continuous Improvement | 7-12 | €5K-15K | (incremental) | 23-30 hrs/mo |

**Total Investment (Months 1-6):** €20,000-36,000
**Total Monthly Savings (Steady State):** 21-27 hours/month
**Annual Value:** €25,000-40,000

---

## Risk Mitigation Timeline

### Month 1: Parallel Manual Process
- Rate sync: Manual backup for 2 weeks
- Dashboard validation: Alerts only (no blocking)

### Month 2: Gradual Automation
- Fathom: Optional usage, encouraged
- Calendar reminders: Notification only

### Month 3-4: Trust Building
- Invoice validation: Validation only, no payment automation
- All invoices still reviewed by Sindbad

### Month 5-6: Confidence Establishment
- Exception-only review (Sindbad sees flagged items only)
- Payment preparation automated, trigger manual

### Month 7+: Full Automation (Conditional)
- Payment automation only after 3+ months zero errors
- Rollback capability maintained

---

## Dependencies & Assumptions

### Technical Dependencies
- Google Workspace API access (Sheets, Calendar, Gmail)
- n8n cloud or Make.com subscription
- Wise API access (to be validated)
- Discord webhook or Gmail API
- Fathom API access

### Business Assumptions
- Admin team available for feedback and testing
- Sindbad available for weekly check-ins (30 min)
- No major changes to Google Sheets structure
- Freelancer invoice format remains consistent
- Weekly payment cadence maintained

### External Risks
- Wise API limitations (validate before Phase 2)
- Google Sheets structural changes
- Admin team turnover
- Budget constraints mid-project

---

## Key Milestones

| Milestone | Target Date | Success Criteria |
|-----------|-------------|------------------|
| Quick Wins Deployed | End Month 2 | 5-7 hrs/mo saved, zero rate discrepancies |
| Invoice Validation Live | End Month 4 | 80% time reduction achieved |
| Full Operation | End Month 6 | Autonomous operation, minimal oversight |
| Bold Move TV Kickoff | Month 7 | Strategy aligned, budget approved |
| Payment Automation | Month 9+ | Zero errors for 3 months |

---

## Next Steps

### This Week (Jan 18-24)
1. Finalize proposal document
2. Validate Wise API capabilities
3. Analyze Google Sheets schemas
4. Schedule proposal presentation call

### Next Week (Jan 25-31)
1. Present proposal to Sindbad (and Pierre if required)
2. Negotiate scope and timeline
3. Contract and kickoff planning
4. Admin team availability confirmation

### Month 1 Kickoff (February 2026)
1. Begin rate synchronization development
2. Set up Fathom for Leonor
3. Weekly progress check-ins established
4. Iterative testing with admin team

---

*Roadmap created: 2026-01-18*
*Sources: 5 discovery transcripts (Jan 8 & Jan 15, 2026)*
