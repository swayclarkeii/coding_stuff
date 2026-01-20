# Ambush TV - Client Journey Map

## Client Overview

**Primary Contact:** Sindbad Iksel
**Email:** sindbad@boldmove.tv
**Company:** Ambush TV (Ambushed)
**Industry:** Advertising pitch presentations for commercial directors

**Key Stakeholders:**
- **Sindbad Iksel:** Co-founder, handles all finances and payments
- **Pierre:** Business partner, handles recruitment (diverging visions)
- **Leonor Zuzarte:** Rate management and freelancer raises
- **Madalena Ribeiro da Fonseca:** Systems and automation coordinator
- **Alice Carreto:** Admin team member

**Primary Pain Points:**
1. **Sindbad:** 20+ hours/month on invoice reconciliation (prevents strategic work)
2. **Leonor:** Manual rate synchronization across 3 Google Sheets (error-prone)
3. **Admin Team:** Month-end invoicing delays, tool integration gaps

**Project Vision:** Comprehensive automation system - invoice validation + rate synchronization + calendar reminders + dashboard validation

**Current State:**
- Sindbad: 5-6 hours/week manual invoice validation, 10% error rate
- Leonor: 2+ hours/month rate verification across Team Directory, FCA, Dashboard
- Admin team: Manual tracking of project close-outs, delayed client invoicing

**Desired State:**
- Sindbad: 1-2 hours/week with automated validation + human checkpoints
- Leonor: Single rate update, auto-sync across all sheets
- Admin team: Automated reminders for hours collection and invoicing

---

## Discovery Phase Timeline

### January 8, 2026 - Initial Discovery Call with Sindbad
**Status:** ✅ Completed
**Duration:** ~50 minutes
**Outcome:** Problem identification, admin team consultation scheduled

**What Was Learned:**

**Ambush Context:**
- 9-person team + 70-80 freelancers
- ~50 pitches per month
- 15-20 weekly payments via Wise
- Google Sheets dashboard (monthly tabs)
- Cash flow requires weekly payment cadence
- 10% error rate (missing projects, rate issues, hour discrepancies)
- Sindbad catches errors before payment
- Spends 20-24 hours/month on validation

**Partnership Dynamics:**
- Sindbad + Pierre (business partner) have diverging visions
- Pierre started separate AI business without full disclosure
- Sindbad handles all finances, Pierre handles recruitment
- No budget for buyout
- Tension around business direction
- Ambush pays Sindbad's bills (90% of income)

**Cultural Insights:**
- Quality-focused (wants oversight, not blind trust)
- Budget-conscious (free tools only)
- European business context (Paris-based)
- Creative industry (advertising presentations)

**Sindbad's Emotional State:** Overwhelmed by admin burden, aware of partnership tension, frustrated with time spent on manual validation

**Key Quote:**
> "18 to 20 hours a month... If I didn't have to do these five hour, four to five hours every week, what else would you be doing? Oh, wow. You know, I don't know, like, thinking about the strategy of the business, or working on my screenplay, you know, I might be doing my personal stuff."

**Decisions Made:**
1. Schedule follow-up call with admin team (understand their process)
2. Include Leonor, Madalena, Alice in discovery (build buy-in)
3. Focus on Ambush automation first (90% revenue, clear ROI)

**Action Items for Sindbad:**
- Send calendar availability for admin team call
- Coordinate team availability
- Share access to Google Sheets (Team Directory, FCA, Dashboard)

**Action Items for Sway:**
- Send meeting calendar link
- Prepare discovery questions for admin team
- Research Wise API capabilities

---

### January 15, 2026 - Admin Team Discovery Call
**Status:** ✅ Completed
**Duration:** ~20 minutes
**Outcome:** Rate management workflow documented, tool integration gaps identified

**What Was Learned:**

**Rate Management Process:**
- Weekly team meetings review freelancer performance
- Batch raises: 5-10 freelancers at once
- Leonor conducts personalized feedback calls with each freelancer
- Manual rate updates across 3 separate sheets:
  1. Team Directory (master freelancer data)
  2. Freelancer Cost Assumptions (FCA) (rate lookup for dashboard)
  3. Dashboard (monthly project tabs, auto-populates from FCA)
- Verification day: "Whole day a month" (2+ hours) ensuring consistency

**Raise Frequency:**
- New hires: 2-3 raises in first year
- Mid-level: 1-2 raises per year
- Senior: Slower progression
- Example: One freelancer had 4 raises in 2024, 2 raises in 2025

**Tool Integration Gaps:**
- Google Workspace (free), Discord (free), no Notion, no Slack
- Standard automation tools assume paid enterprise stack
- Attempted Fireflies, Otter (hit limits, abandoned)
- Outputs don't flow into daily tools (Sheets, Discord)

**Calendar Reminder Pain Point:**
- Projects have estimated end dates (sometimes shift)
- No systematic reminders for hours collection or invoicing
- Delays cascade: Project ends → forget hours → delay invoicing → awkward client conversations
- Example: "Unibet of January gets left to bottom of February"

**Leonor's Emotional State:** Aware of error potential, wants automation to reduce admin burden, values personalized feedback time

**Madalena's Emotional State:** Frustrated by tool limitations, attempted ChatGPT automation (partial success), interested in API-based integration approach

**Key Quote:**
> "I just feel like for me personally, it opens me up to a lot of error." - Leonor

**Decisions Made:**
1. Use Fathom (free) for call recording and transcription
2. API-based integration approach (n8n/Make.com) for free tools
3. Schedule follow-up call for proposal review (Jan 22, 26, Feb 2, or post-Feb 9)

**Action Items for Admin Team:**
- Leonor: Test Fathom for recording feedback calls
- Madalena: Share sheet structures (Team Directory, FCA, Dashboard)
- Madalena: Document current rate change workflow step-by-step
- Alice: Review pain points, contribute additional insights

**Action Items for Sway:**
- Send calendar link with Madalena's availability constraints
- Design API-based automation architecture for rate sync
- Create Fathom → Gmail/Discord automation example

---

## Project Phases

### Phase 0: Discovery & Planning
**Timeline:** January 8-24, 2026
**Status:** 🔄 In Progress

**Milestones:**
- [x] Initial discovery call with Sindbad (Jan 8)
- [x] Admin team discovery call (Jan 15)
- [x] Meeting notes processed and organized
- [x] Quick wins analysis completed
- [x] Key insights documented
- [x] Client journey map created (this document)
- [ ] Sheet structures analyzed (Team Directory, FCA, Dashboard)
- [ ] Wise API capabilities validated
- [ ] Project requirements finalized
- [ ] Proposal created and presented

**Deliverables:**
- [x] Complete transcript analysis (Jan 8 + Jan 15 calls)
- [x] Client journey map (this document)
- [x] Quick wins analysis (discovery/analysis/)
- [x] Key insights document (discovery/analysis/)
- [ ] Project requirements document (pending sheet analysis)
- [ ] API integration architecture design
- [ ] Proposal with pricing and timeline

**Success Criteria:**
- Admin team feels heard and engaged
- Clear understanding of all workflows
- Technical integration points validated
- ROI calculations based on real data
- Prioritization aligned with team needs

---

### Phase 1: Quick Wins (Weeks 1-4)
**Timeline:** Late January - Early February 2026
**Status:** ⏳ Pending (proposal approval)

**Recommended Priority:**
1. **Rate Synchronization Automation:** Team Directory → auto-sync to FCA & Dashboard
2. **Dashboard Validation Rules:** Real-time error checking at data entry
3. **Fathom Call Recording Setup:** Transcripts → email/Discord summaries
4. **Calendar Reminder System:** Project end → 4-day (hours) and 7-day (invoicing) reminders

**Milestones:**
- [ ] Google Sheets API integration (read/write Team Directory, FCA, Dashboard)
- [ ] Rate sync automation workflow (n8n/Make.com)
- [ ] Dashboard validation rules (Google Apps Script)
- [ ] Fathom account setup and automation
- [ ] Google Calendar integration with Dashboard
- [ ] Discord webhook for reminders
- [ ] Testing with 2-3 weeks historical data
- [ ] Admin team training and handoff

**Deliverables:**
- [ ] Automated rate synchronization system
- [ ] Dashboard validation rules (missing projects, rate discrepancies, hour thresholds)
- [ ] Fathom → Gmail/Discord automation
- [ ] Calendar reminder automation
- [ ] Admin team training materials
- [ ] Weekly report (errors prevented, time saved)

**Success Criteria:**
- Zero rate discrepancies across sheets
- Admin team reports "single update" workflow
- Fathom used for 100% of feedback calls
- Reminders sent within 24 hours of project end
- Dashboard validation catches 50%+ of errors before Sindbad review
- 2-3 hours/month time savings for admin team

**Risk Mitigation:**
- Parallel manual process for first 4 weeks (safety net)
- Weekly check-ins with admin team
- Rollback plan if automation fails
- Audit trail of all automated changes

---

### Phase 2: Invoice Validation System (Months 2-3)
**Timeline:** February - March 2026
**Status:** ⏳ Pending (after Quick Wins proven)

**Milestones:**
- [ ] Google Sheets API integration (dashboard data extraction)
- [ ] Invoice parsing automation (email intake + Google Docs parsing)
- [ ] Validation logic implementation (hours, rates, projects)
- [ ] Error detection AI (flag 10%+ discrepancies)
- [ ] Wise API integration (batch payment preparation)
- [ ] Human approval workflow (exceptions for Sindbad)
- [ ] Validation dashboard (review queue for Sindbad)
- [ ] Admin team notification system
- [ ] Testing with 4-6 weeks of real invoices
- [ ] Security audit and data privacy compliance

**Deliverables:**
- [ ] Automated invoice validation system
- [ ] Error flagging dashboard (Sindbad's review queue)
- [ ] Wise batch payment integration
- [ ] Weekly validation reports (automated)
- [ ] Admin team performance insights (optional)
- [ ] System documentation and training materials

**Success Criteria:**
- 90%+ accuracy in error detection (match or exceed Sindbad's 10%)
- Time reduction from 5-6 hours/week to 1-2 hours/week (80-90%)
- Zero payment errors during pilot period
- Admin team reports process improvements
- Sindbad trusts the system enough to scale
- Cash flow timing maintained (weekly cadence)

**Risk Mitigation:**
- Parallel manual process for first 6-8 weeks (safety net)
- Weekly review meetings with Sindbad and admin team
- Gradual automation increase (validation → payment prep → full automation)
- Escape hatch: easy revert to manual if needed
- MFA/2FA for payment execution

---

### Phase 3: Testing & Refinement (Months 3-4)
**Timeline:** March - April 2026
**Status:** ⏳ Pending

**Milestones:**
- [ ] Test invoice validation with 8-10 weeks of real payments
- [ ] Bug fixes and edge case handling
- [ ] Accuracy improvements based on feedback
- [ ] Admin team and Sindbad training
- [ ] Process documentation and optimization
- [ ] Handoff to ongoing operations

**Deliverables:**
- [ ] Tested system with real-world data
- [ ] Bug fix log and resolution documentation
- [ ] User training sessions completed
- [ ] Process documentation (SOPs)
- [ ] Handoff documentation for future maintenance

**Success Criteria:**
- 80-90% time reduction achieved consistently
- Zero critical bugs in production
- Admin team autonomous usage
- Sindbad reports satisfaction with quality control
- Time savings reinvested in strategic work (Bold Move TV, screenplay)

---

### Phase 4: Optimization & Scaling (Months 5-6+)
**Timeline:** May 2026+
**Status:** ⏳ Pending

**Potential Enhancements:**
- Upstream admin team workflow improvements (based on performance data)
- Predictive cash flow modeling (based on project pipeline)
- Freelancer self-service portal (invoice submission and tracking)
- AI-powered recommendations (e.g., "freelancer X always accurate")
- Cross-system insights (financial health dashboard)
- Integration with accounting software (Xero, QuickBooks)

**Success Criteria:**
- Systems running autonomously
- Continuous improvement based on data
- Sindbad spending <10% time on Ambush operations
- Admin team reports sustained efficiency gains
- ROI validated and documented

---

## Emotional Journey & Trust Building

### January 8 - Initial Overwhelm to Cautious Hope
**Emotional State:** Overwhelmed by admin burden, uncertain if automation is right approach

**Concerns Expressed (Sindbad):**
- "I wouldn't want to do a batch payment before I've checked everything"
- Worried about losing quality control
- Unclear if automation will actually save time

**Breakthrough Moment:**
> Sway: "It doesn't have to be an all or nothing. It doesn't have to be a Sindbad is in the process, or he's not in the process at all, and it's automated, right? You can always add in like a human checkpoint."

**Result:** Shifted from fear of automation to excitement about human-in-the-loop design

---

### January 15 - Collaborative Problem Solving with Admin Team
**Emotional State:** Admin team engaged, collaborative, willing to share workflows

**Trust Indicators:**
- Leonor openly shared rate management pain points
- Madalena shared failed automation attempts (vulnerability)
- Team willing to test new tools (Fathom)
- Open to API-based integration approach
- Agreed to share sheet structures for analysis

**Leonor's Shift:**
- From: "This is just how we do things"
- To: "I really should be recording these calls, shouldn't I?"

**Madalena's Shift:**
- From: "Our tools don't integrate because they're free"
- To: "API integrations can connect any system - this changes everything"

**Next Trust-Building Steps:**
- Follow through on calendar link (responsiveness test)
- Deliver working API integration examples
- Show rate sync automation working in test environment
- Admin team sees efficiency gains, not job threats

---

### Future Milestones - From Pilot to Partnership

**Expected Evolution:**

**Week 1-2 (Quick Wins Launch):**
- Leonor updates rate in Team Directory once → auto-syncs to FCA & Dashboard
- "This is amazing, I don't have to triple-check anymore"
- Fathom transcripts arrive in Discord/email post-call

**Week 3-4 (Admin Team Adoption):**
- Dashboard validation catches missing project before Sindbad sees it
- Calendar reminder triggers 4 days post-project
- Admin team reports: "System is helping, not replacing"

**Month 2 (Invoice Validation Pilot):**
- Sindbad reviews 15 invoices → system flags 2 discrepancies automatically
- Approves 13 in 10 minutes (vs 5-6 hours previously)
- "I'm only looking at the exceptions now"

**Month 3 (Confidence Building):**
- Admin team autonomous on quick wins
- Sindbad reports time savings in screenplay work
- Zero payment errors during pilot
- "I trust the system, let's scale this"

**Month 6 (Full Automation):**
- Sindbad spends 1-2 hours/week vs 5-6 hours (80%+ reduction)
- Admin team spends 3-4 hours/month less on verification
- Ambush operations running smoothly
- Sindbad focuses on Bold Move TV growth

---

## Key Decision Points

### Decision 1: Quick Wins First or Full System?
**Timeline:** Late January 2026 (proposal phase)
**Options:**
1. **Quick wins first** (recommended) - rate sync, dashboard validation, calendar reminders (4-6 weeks)
2. **Full system immediately** - include invoice validation from start (8-12 weeks)
3. **Invoice validation only** - skip quick wins, go straight to biggest pain point

**Recommendation:** Quick wins first
**Rationale:**
- Builds admin team trust and adoption
- Reduces upstream errors before tackling downstream validation
- Lower investment, faster ROI (2-4 months vs 8-12 months)
- Proven success unlocks budget for invoice validation

---

### Decision 2: How Much Automation in Invoice Validation?
**Timeline:** Month 2 (before invoice validation development)
**Options:**
1. **Validation only** - AI flags errors, Sindbad reviews, manual payments
2. **Validation + payment prep** - AI prepares Wise batch, Sindbad approves and executes
3. **Full automation** - AI validates, prepares, and executes payments (Sindbad audit trail)

**Recommendation:** Start with #2, scale to #3
**Rationale:**
- Build trust incrementally
- Maintain human checkpoint during pilot
- Reduce risk of payment errors
- Gradual adoption path

---

### Decision 3: API Platform Choice?
**Timeline:** Proposal phase
**Options:**
1. **n8n (self-hosted)** - Free, full control, technical setup required
2. **n8n (cloud)** - €20/month, easier setup, less control
3. **Make.com** - €9/month starter, visual interface, limited operations
4. **Zapier** - €20/month, easiest UI, most expensive long-term

**Recommendation:** n8n cloud (€20/month)
**Rationale:**
- Budget-friendly for Ambush cost-cutting culture
- More powerful than Make.com or Zapier
- Cloud version = no DevOps burden
- Can migrate to self-hosted later if needed

---

## Success Metrics

### Quick Wins (Phase 1)

**Time Metrics:**
- Admin team: 2-3 hours/month saved (rate verification, tracking)
- Monthly time saved: 2-3 hours
- Annual time saved: 24-36 hours

**Quality Metrics:**
- Rate discrepancy errors: 100% → 0%
- Dashboard validation catches: 50%+ of errors before Sindbad
- Calendar reminders: 100% delivery within 24 hours

**Adoption Metrics:**
- Leonor Fathom usage: ≥80% of feedback calls recorded
- Admin team satisfaction: ≥4/5 (tool helps, not replaces)
- Rate sync usage: 100% of raises (no manual triple-entry)

**Business Impact:**
- ROI: 2-4 months payback period
- Error prevention: Reduces downstream errors in Sindbad's validation
- Mental load: Admin team reports less stress

---

### Invoice Validation System (Phase 2)

**Time Metrics:**
- Weekly time: 5-6 hours → 1-2 hours (80-90% reduction target)
- Monthly time saved: 18-23 hours
- Annual time saved: 216-276 hours

**Quality Metrics:**
- Error detection rate: ≥10% (match or exceed Sindbad's manual rate)
- Payment accuracy: 100% (zero errors during pilot)
- Cash flow timing: Weekly cadence maintained

**Adoption Metrics:**
- Sindbad trust score: ≥4/5 (comfortable approving exceptions only)
- Admin team satisfaction: ≥4/5 (upstream validation helps)
- Weeks to autonomous operation: ≤8 weeks

**Business Impact:**
- ROI: <12 months payback period
- Annual value: €21,600-27,600 (at €100/hour)
- Time reinvestment: ≥50% to Bold Move TV and strategy work
- Admin team efficiency: ≥20% reduction in data entry time

---

## Risk Register

### High Priority Risks

**R1: Admin team fears job loss → resistance**
- **Impact:** High (implementation failure, low adoption)
- **Probability:** Medium
- **Mitigation:** Frame as "upgrade admin role" not replacement; show efficiency gains benefit them; involve team in design decisions

**R2: Rate sync errors → downstream chaos**
- **Impact:** High (affects invoices, payments, client billing)
- **Probability:** Low (if tested properly)
- **Mitigation:** Parallel manual process for first 4 weeks; extensive testing with historical data; rollback plan

**R3: Partnership tension at Ambush → political complications**
- **Impact:** Medium (automation might expose inefficiencies)
- **Probability:** Medium (already diverging visions)
- **Mitigation:** Focus automation on Sindbad/admin workflows, not partner evaluation; maintain neutrality

---

### Medium Priority Risks

**R4: Google Sheets structure changes → integration breaks**
- **Impact:** Medium (requires updates to automation)
- **Probability:** Low (stable monthly structure)
- **Mitigation:** Version control on schema; alert system for structural changes; documentation

**R5: Wise API limitations → payment automation blocked**
- **Impact:** Medium (reduces time savings potential)
- **Probability:** Low (Wise has batch payment feature)
- **Mitigation:** Technical validation during proposal phase; fallback to payment prep only

**R6: No baseline metrics → unprovable ROI**
- **Impact:** Low (still saves time objectively)
- **Probability:** Low (Sindbad tracks hours manually)
- **Mitigation:** Document current time spent before automation; weekly time tracking during pilot

---

### Low Priority Risks

**R7: Madalena on holiday → delayed feedback**
- **Impact:** Low (can proceed with Leonor feedback)
- **Probability:** High (Jan 22 - Feb 9, available Mondays)
- **Mitigation:** Schedule calls around Madalena's availability; async communication via email

**R8: Budget constraints → scope reduction**
- **Impact:** Low (quick wins are affordable)
- **Probability:** Medium (cost-cutting culture)
- **Mitigation:** Phase implementation (quick wins first); demonstrate ROI before invoice validation investment

---

## Next Actions

### Immediate (Within 48 Hours)
1. **Analyze sheet structures:** Review Team Directory, FCA, Dashboard schemas
2. **Validate Wise API:** Confirm batch payment capabilities
3. **Create proposal:** Quick wins package with pricing and timeline

### This Week (January 18-24)
1. Send calendar link to admin team for proposal review call
2. Design rate sync automation architecture (API workflow diagram)
3. Create Fathom → Gmail/Discord automation demo
4. Draft project requirements document

### Next Week (January 25-31)
1. Present proposal to Sindbad and admin team
2. Negotiate contract and timeline
3. Finalize success metrics and acceptance criteria
4. Plan development kickoff

### Month 1 (February 2026)
1. Begin quick wins development (rate sync, dashboard validation, calendar reminders)
2. Weekly progress check-ins with admin team
3. Iterative testing and feedback
4. Admin team training sessions

---

## Key Quotes Archive

### On Rate Management Pain (Leonor)
> "From my end, I think in terms of automatization, there's just one big thing that pops into mind, which is regarding the rates... I have to manually integrate it into the team directory. And then from the team directory, I have to then make sure that it's changed in the freelancer cost assumptions sheet so that it will show up correctly on the dashboard."

### On Error Risk (Leonor)
> "I just feel like for me personally, it opens me up to a lot of error."

### On Verification Burden (Leonor)
> "It just creates this like whole day a month where I go and I spend like two hours making sure that everything is right and corresponds and like that the people's time sheets also corresponds and that they like really actually understood that they were raised."

### On Tool Integration Frustration (Madalena)
> "These all have certain integrations with certain services that normal companies would use. But because we are cutting costs at every corner... We don't use Slack. We use Discord, which is almost exactly the same, but it's like, you know, Discord. It's like a Twitch streaming group... it's not something that would have integrations with other things because it's another free program."

### On Data Death Zone (Madalena)
> "You get the transcripts and you get the summaries with the action items and stuff, but then that just sits in that tab of that AI thing that none of us are opening because we have like 60 sheets open instead."

### On Month-End Awkwardness (Madalena)
> "It's also really awkward for us to go back, like, a month and a half later and be like, hi, I'm sorry we didn't say anything, it's because your project sucked, please pay us so much, and there's overhours, and there's this."

### On Time Value (Sindbad, Jan 8)
> "18 to 20 hours a month... If I didn't have to do these five hour, four to five hours every week, what else would you be doing? Oh, wow. You know, I don't know, like, thinking about the strategy of the business, or working on my screenplay, you know, I might be doing my personal stuff."

### On Quality Control (Sindbad, Jan 8)
> "I wouldn't want to do a batch payment before I've checked everything. But if AI could check things and, you know, tell me if there was a discrepancy..."

### On Human-in-the-Loop (Sway)
> "It doesn't have to be an all or nothing. It doesn't have to be a Sindbad is in the process, or he's not in the process at all, and it's automated, right? You can always add in like a human checkpoint."

### On API Integration (Sway)
> "You have direct integrations, and then you have API integrations, meaning that an API integration means I can integrate any system with any system."

### On Team Efficiency (Sindbad, Jan 8)
> "I would be interested in not only speeding up my process, but also theirs [admin team]."

---

*Last updated: January 18, 2026*
*Next review: After proposal presentation (Week of Jan 25-31)*
