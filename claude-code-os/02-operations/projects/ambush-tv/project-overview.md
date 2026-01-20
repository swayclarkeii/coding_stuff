# Ambush TV - Project Overview

**Last Updated:** January 18, 2026
**Status:** Discovery Phase (Proposal Pending)
**Project Type:** Operational Automation - Payment Validation + Admin Workflows

---

## Executive Summary

### The Problem

Ambush TV operates a high-volume advertising pitch presentation business (50 projects/month, 70-80 freelancers) with manual admin processes consuming 25+ hours/month across founder and admin team:

1. **Sindbad (Founder):** Spends 5-6 hours/week (20-24 hours/month) manually validating freelancer invoices against Google Sheets dashboard, catching ~10% error rate
2. **Leonor (Rate Manager):** Manually updates rates across 3 separate Google Sheets every time a freelancer is raised, spending 2+ hours/month just verifying consistency
3. **Admin Team:** No systematic reminders for project close-outs, causing 1-2 month delays in client invoicing

### The Solution

**Phase 1 - Quick Wins (4-6 weeks, €5K-10K):**
- Rate synchronization automation (Team Directory → auto-sync to FCA & Dashboard)
- Dashboard validation rules (real-time error detection)
- Call recording integration (Fathom → auto-transcription → Discord/email summaries)
- Calendar reminder system (project end → automated hours/invoicing reminders)

**Phase 2 - Invoice Validation (8-10 weeks, €15K-20K):**
- Automated invoice parsing and validation against dashboard
- Error flagging with human-in-the-loop approval workflow
- Wise batch payment preparation
- Weekly validation reports

### Expected ROI

**Quick Wins:**
- Time savings: 2-3 hours/month (admin team)
- Error prevention: Zero rate discrepancies, 50%+ dashboard errors caught upstream
- Payback: 2-4 months
- Annual value: €2,400-3,600

**Invoice Validation:**
- Time savings: 16-20 hours/month (Sindbad)
- Error detection: Maintain 10%+ accuracy, prevent unbilled work
- Payback: 8-12 months
- Annual value: €21,600-27,600

**Combined Total:**
- Investment: €20K-30K
- Annual value: €24K-30K
- 5-year value: €120K-150K
- Time freed: 20-25 hours/month for strategic work

---

## Business Context

### Company Profile

**Name:** Ambush TV (Ambushed)
**Industry:** Advertising pitch presentations for commercial directors
**Location:** Paris, France (European business)
**Revenue:** 90% of Sindbad's income (pays his bills)

**Team Structure:**
- 9 core team members
  - Sindbad Iksel (co-founder, handles all finances)
  - Pierre (business partner, handles recruitment, diverging visions)
  - Leonor Zuzarte (rate management, freelancer raises)
  - Madalena Ribeiro da Fonseca (systems and automation)
  - Alice Carreto (admin team member)
  - 4 additional core team members
- 70-80 freelancers (international, paid weekly)

**Volume:**
- ~50 pitches per month
- 15-20 payments per week
- Weekly payment cadence (cash flow critical)

**Business Model:**
- High-volume presentation creation for advertising competitions
- Word-of-mouth driven, sometimes unable to meet demand
- Recently raised prices and reinforced core team (higher costs)

---

### Partnership Dynamics (Sensitive)

**Context from Sindbad (Jan 8 call):**
> "The sad thing about Ambush is, my business partner and I, like, really, we were very good at the beginning. And now, it's just, I don't, I don't think we have the same vision... I would almost prefer that he did like the bare minimum."

**Current Division:**
- Sindbad: Handles all finances and payments
- Pierre: Handles recruitment
- Pierre started separate AI business without full disclosure
- No budget for buyout
- Tension around business direction

**Project Implications:**
- Focus automation on Sindbad's workflow (not partner evaluation)
- Maintain political neutrality
- Sindbad wants to reduce dependency on Ambush operations (focus on Bold Move TV)

---

## Key Stakeholders

### Sindbad Iksel
**Role:** Co-founder, handles all finances and payments
**Email:** sindbad@boldmove.tv
**Pain Points:**
- 5-6 hours/week manual invoice validation
- 10% error rate requires quality control
- Prevents strategic work (Bold Move TV, screenplay writing)

**Needs:**
- 80-90% time reduction in invoice validation
- Maintain quality control (human-in-the-loop)
- Weekly payment cadence preserved (cash flow critical)

**Work Style:**
- Quality-focused (wants oversight, not blind trust)
- Budget-conscious (free tools preferred)
- Limited training time (prefers set-and-forget automation)

**Quote:**
> "I wouldn't want to do a batch payment before I've checked everything. But if AI could check things and, you know, tell me if there was a discrepancy..."

---

### Leonor Zuzarte
**Role:** Rate management and freelancer raises
**Pain Points:**
- Manual rate updates across 3 separate Google Sheets
- "Whole day a month" (2+ hours) verifying consistency
- Error-prone process during batch raises

**Needs:**
- Single rate update → auto-sync across all sheets
- Zero rate discrepancies
- More time for personalized feedback conversations

**Work Style:**
- Values freelancer relationships and personalized feedback
- Conducts weekly team performance reviews
- Batch raises 5-10 freelancers at once

**Quote:**
> "I just feel like for me personally, it opens me up to a lot of error."

---

### Madalena Ribeiro da Fonseca
**Role:** Systems and automation coordinator
**Pain Points:**
- Tool integration gaps (Discord, free Google Workspace don't integrate with enterprise tools)
- Failed automation attempts (Fireflies, Otter, ChatGPT partial success)
- Data outputs don't flow into daily tools

**Needs:**
- API-based integrations for free tools
- Systematic project close-out reminders
- Automation that actually works

**Work Style:**
- Technical, self-taught (ChatGPT-assisted Google Sheets formulas)
- Frustrated by tool limitations
- Interested in API-based integration approach

**Quote:**
> "You get the transcripts and you get the summaries with the action items and stuff, but then that just sits in that tab of that AI thing that none of us are opening because we have like 60 sheets open instead."

**Availability:** On holiday Jan 22 - Feb 9 (available Mondays Jan 26 & Feb 2)

---

### Alice Carreto
**Role:** Admin team member
**Pain Points:** Not detailed in discovery calls (minimal speaking)
**Needs:** TBD (follow-up with Alice for input)

---

## Discovery Timeline

### January 8, 2026 - Initial Discovery with Sindbad
**Duration:** ~50 minutes
**Key Outcomes:**
- Invoice validation pain point identified (5-6 hours/week)
- 10% error rate documented
- Admin team consultation scheduled
- Human-in-the-loop architecture agreed

**Decisions:**
- Include admin team in discovery (build buy-in)
- Focus Ambush automation first (90% revenue, clear ROI)
- Bold Move TV as separate project (10% revenue, needs sales strategy clarity)

---

### January 15, 2026 - Admin Team Discovery
**Duration:** ~20 minutes
**Key Outcomes:**
- Rate sync pain point identified (manual triple-entry across sheets)
- Tool integration gaps documented (Discord, free tools don't integrate)
- Calendar reminder opportunity identified (month-end invoicing delays)
- API-based integration approach agreed

**Decisions:**
- Use Fathom (free) for call recording
- API automation via n8n/Make.com (connect free tools)
- Follow-up call scheduled for proposal review

---

## Current Workflow (Pain Points)

### Rate Management (Leonor)

**Current Process:**
1. Weekly team meeting → identify freelancers to raise
2. Leonor conducts personalized feedback calls
3. Manually updates Team Directory sheet (rate column)
4. Manually updates Freelancer Cost Assumptions (FCA) sheet
5. Manually verifies Dashboard auto-populated correctly
6. Repeat for batch of 5-10 freelancers

**Problems:**
- Triple-entry creates error risk (rate changed in one sheet, not others)
- "Whole day a month" spent verifying consistency
- Discrepancies cause downstream errors in Sindbad's validation

**Frequency:**
- New hires: 2-3 raises in first year
- Mid-level: 1-2 raises per year
- Example: One freelancer had 4 raises in 2024, 2 raises in 2025

---

### Invoice Validation (Sindbad)

**Current Process:**
1. Freelancers submit invoices weekly (15-20 per week)
2. Sindbad manually reviews every invoice
3. Checks hours against Google Sheets dashboard
4. Verifies rates against FCA
5. Confirms project details and math
6. Makes 15-20 payments via Wise
7. Repeats weekly (cash flow requires weekly cadence)

**Problems:**
- 5-6 hours per week (20-24 hours/month)
- 10% error rate (missing projects, rate issues, excessive hours)
- Prevents strategic work (Bold Move TV, screenplay)
- Quality control falls entirely on founder

**Errors Caught:**
- Projects not entered in dashboard (unbilled work)
- Rate discrepancies (wrong rate on invoice)
- Excessive hours (doesn't match project scope)
- Missing information (incomplete invoices)

---

### Project Close-Out (Admin Team)

**Current Process:**
1. Projects have estimated end dates in Dashboard
2. Manual tracking of which projects need hours collected
3. Manual tracking of which projects need client invoicing
4. Follow-up when remembered or prompted by client

**Problems:**
- No systematic reminders based on end dates
- Hours collection delayed 1-2 weeks
- Client invoicing delayed 1-2 months sometimes
- Awkward late payment requests
- Mental burden of tracking 50 projects/month

**Quote (Madalena):**
> "It's also really awkward for us to go back, like, a month and a half later and be like, hi, I'm sorry we didn't say anything, it's because your project sucked, please pay us so much, and there's overhours, and there's this."

---

## Proposed Solution

### Phase 1: Quick Wins (4-6 weeks)

**1. Rate Synchronization Automation**
- **Problem:** Manual triple-entry across Team Directory, FCA, Dashboard
- **Solution:** Team Directory as single source of truth → Google Sheets API auto-syncs to FCA & Dashboard
- **Technology:** Google Sheets API + n8n/Make.com
- **Time Savings:** 2+ hours/month (Leonor verification eliminated)
- **Impact:** Zero rate discrepancies, prevents downstream errors

**2. Dashboard Validation Rules**
- **Problem:** Errors only caught during Sindbad's manual review (too late)
- **Solution:** Real-time validation in Google Sheets (missing projects, rate discrepancies, hour thresholds)
- **Technology:** Google Apps Script (Sheets scripting)
- **Time Savings:** 6-8 hours/month (reduces Sindbad's review by 30-40%)
- **Impact:** Catches errors at data entry time, not invoice time

**3. Call Recording & Transcription**
- **Problem:** No record of feedback calls, must remember admin changes
- **Solution:** Fathom recording → auto-transcription → extract rate changes → Discord/email summary
- **Technology:** Fathom + n8n/Make.com + Discord/Gmail API
- **Time Savings:** 1-2 hours/month (eliminate manual note-taking)
- **Impact:** Audit trail, triggers rate sync automation

**4. Calendar Reminder System**
- **Problem:** Month-end delays because manual tracking
- **Solution:** Project end date → 4-day (hours) and 7-day (invoicing) automated reminders
- **Technology:** Google Calendar API + n8n/Make.com + Discord/Gmail
- **Time Savings:** 2-3 hours/month (eliminate manual tracking)
- **Impact:** Faster client invoicing, better cash flow

**Investment:** €5K-10K
**Timeline:** 4-6 weeks
**ROI:** 2-4 months payback

---

### Phase 2: Invoice Validation (8-10 weeks)

**1. Invoice Parsing & Intake**
- Automated email parsing (Gmail API)
- Extract data from Google Docs templates (OCR if needed)
- Structured data: Freelancer, project, hours, rate, total

**2. Cross-Reference Validation**
- Invoice data vs Dashboard data
- Flag discrepancies (missing projects, rate issues, hour thresholds)
- 10%+ error detection accuracy (match Sindbad's manual rate)

**3. Error Flagging Dashboard**
- Sindbad reviews only flagged items (exceptions)
- Approve, reject, or edit invoices
- Human-in-the-loop approval before payment

**4. Wise Batch Payment Preparation**
- Generate Wise-compatible payment file
- Start manual upload (Option A), scale to API upload (Option B/C)
- Weekly payment cadence maintained

**Investment:** €15K-20K
**Timeline:** 8-10 weeks
**ROI:** 8-12 months payback

---

## Technical Architecture

### Current Tool Stack

**Communication:**
- Discord (free, team chat)
- Gmail (email)

**Project Management:**
- Google Sheets (Dashboard, FCA, Team Directory)
- Google Calendar (project timelines)
- Google Docs (invoice templates)

**Payments:**
- Wise (international payment platform, batch capable)

**Attempted:**
- Notion (too expensive, rejected)
- Fireflies, Otter (hit limits, abandoned)
- ChatGPT (formula building, partial success)

---

### Proposed Additions

**Call Recording:**
- Fathom (free)

**API Automation:**
- n8n cloud (€20/month) or Make.com (€9/month)

**Integrations:**
- Google Sheets API (rate sync, dashboard access)
- Gmail API (invoice parsing, email summaries)
- Google Calendar API (project reminders)
- Discord API (webhooks for notifications)
- Wise API (batch payment preparation, TBD)
- Fathom API (transcript extraction)

---

### API Integration Strategy

**Why API-Based:**
Standard automation tools (Zapier, etc.) assume paid enterprise stack (Slack, Notion, Salesforce). Ambush uses free alternatives (Discord, Google Workspace Free) that lack direct integrations. API-level integrations via n8n/Make.com unlock automation without enterprise tool budget.

**Example Workflows:**
1. **Rate Sync:** Team Directory onChange → n8n → update FCA & Dashboard via Sheets API
2. **Fathom Summary:** Call ends → Fathom webhook → n8n → extract rate → Discord/Gmail
3. **Calendar Reminder:** Project end date → n8n cron → check Dashboard → Discord/Gmail notification
4. **Invoice Validation:** Gmail new email → n8n → parse invoice → validate → flag → notify Sindbad

---

## Success Metrics

### Quick Wins (Phase 1)

**Time Metrics:**
- Admin team: 2-3 hours/month saved
- ROI: 2-4 months payback
- Annual value: €2,400-3,600

**Quality Metrics:**
- Rate discrepancies: 0% (currently causes downstream errors)
- Dashboard errors caught: 50%+ before Sindbad review
- Calendar reminders: 100% delivery within 24 hours

**Adoption Metrics:**
- Leonor rate sync usage: 100% (no manual triple-entry)
- Fathom call recording: 80%+ of feedback calls
- Admin team satisfaction: ≥4/5

---

### Invoice Validation (Phase 2)

**Time Metrics:**
- Sindbad: 5-6 hours/week → 1-2 hours/week (80-90% reduction)
- Monthly savings: 16-20 hours
- Annual savings: 192-240 hours
- ROI: 8-12 months payback
- Annual value: €21,600-27,600

**Quality Metrics:**
- Error detection: ≥10% (match Sindbad's manual rate)
- Payment accuracy: 100% (zero errors)
- Cash flow timing: Weekly cadence maintained

**Adoption Metrics:**
- Sindbad trust: ≥4/5 (approves exceptions only)
- Admin team satisfaction: ≥4/5 (upstream validation helps)
- Weeks to autonomous: ≤8 weeks

---

## Risk Factors

### High Priority Risks

**R1: Admin team fears job loss → resistance**
- **Mitigation:** Frame as "upgrade admin role" not replacement; involve team in design; show efficiency gains benefit them

**R2: Rate sync errors → downstream chaos**
- **Mitigation:** Parallel manual process for 4 weeks; extensive testing; rollback plan

**R3: Partnership tension → political complications**
- **Mitigation:** Focus automation on Sindbad/admin workflows, not partner evaluation

---

### Medium Priority Risks

**R4: Google Sheets structure changes → integration breaks**
- **Mitigation:** Version control on schema; alert system; documentation

**R5: Wise API limitations → payment automation blocked**
- **Mitigation:** Validate during proposal phase; fallback to payment prep only

---

### Low Priority Risks

**R6: Budget constraints → scope reduction**
- **Mitigation:** Phase implementation (quick wins first); demonstrate ROI before invoice validation

---

## Budget & Timeline

### Phase 1: Quick Wins
**Investment:** €5,000-10,000
**Timeline:** 4-6 weeks
**Payback:** 2-4 months
**Scope:**
- Rate synchronization automation
- Dashboard validation rules
- Fathom call recording integration
- Calendar reminder system

---

### Phase 2: Invoice Validation
**Investment:** €15,000-20,000
**Timeline:** 8-10 weeks (after Phase 1)
**Payback:** 8-12 months
**Scope:**
- Invoice parsing and validation
- Error flagging dashboard
- Wise batch payment preparation
- Weekly validation reports

---

### Total Project
**Investment:** €20,000-30,000
**Timeline:** 12-16 weeks (both phases)
**Payback:** 8-14 months
**5-Year Value:** €120,000-150,000

---

## Next Steps

### Immediate (This Week - Jan 18-24)
1. ✅ Complete discovery documentation
2. ⏳ Analyze Team Directory, FCA, Dashboard sheet structures
3. ⏳ Validate Wise API capabilities
4. ⏳ Create proposal with pricing and timeline
5. ⏳ Send calendar link for proposal review call

### Short-Term (Jan 25-31)
1. ⏳ Present proposal to Sindbad and admin team
2. ⏳ Negotiate contract and timeline
3. ⏳ Finalize success metrics and acceptance criteria
4. ⏳ Plan development kickoff

### Month 1 (February)
1. ⏳ Begin quick wins development
2. ⏳ Weekly progress check-ins with admin team
3. ⏳ Iterative testing and feedback
4. ⏳ Admin team training sessions

### Month 2-3 (March-April)
1. ⏳ Deploy quick wins to production
2. ⏳ Begin invoice validation development
3. ⏳ Parallel manual/automated process testing
4. ⏳ Gradual automation increase

---

## Key Quotes

### On Time Value (Sindbad)
> "18 to 20 hours a month... If I didn't have to do these five hour, four to five hours every week, what else would you be doing? Oh, wow. You know, I don't know, like, thinking about the strategy of the business, or working on my screenplay, you know, I might be doing my personal stuff."

### On Quality Control (Sindbad)
> "I wouldn't want to do a batch payment before I've checked everything. But if AI could check things and, you know, tell me if there was a discrepancy..."

### On Rate Management Pain (Leonor)
> "I just feel like for me personally, it opens me up to a lot of error."

### On Tool Integration Frustration (Madalena)
> "You get the transcripts and you get the summaries with the action items and stuff, but then that just sits in that tab of that AI thing that none of us are opening because we have like 60 sheets open instead."

### On Human-in-the-Loop (Sway)
> "It doesn't have to be an all or nothing. It doesn't have to be a Sindbad is in the process, or he's not in the process at all, and it's automated, right? You can always add in like a human checkpoint."

---

## Related Projects

### Bold Move TV (Separate Project)
- **Revenue:** 10% of Sindbad's income
- **Status:** Not yet profitable
- **Pain Point:** Lead generation (1 meeting in 3 months)
- **Recommendation:** Separate project after Ambush automation proven
- **Rationale:** Ambush time savings unlock Bold Move TV sales focus

**Cross-Project Value:**
Ambush automation → Sindbad has 20 hours/month for Bold Move TV growth → increase revenue diversification

---

## Documentation

### Discovery Files
- `/discovery/transcripts/2026-01-08-sindbad-discovery-call.md` (from Bold Move TV folder, Ambush content)
- `/discovery/transcripts/2026-01-15-admin-team-discovery-call.md`
- `/discovery/analysis/quick_wins.md`
- `/discovery/analysis/key_insights.md`
- `/discovery/journey/client_journey_map.md`
- `/discovery/requirements/project_requirements.md`
- `/project-overview.md` (this document)

### External References
- Bold Move TV documentation (cross-reference for Ambush/Bold Move relationship)

---

*Last updated: January 18, 2026*
*Next review: After proposal presentation*
