# Quick Wins Analysis – Ambush TV
**Date:** 2026-01-18 (Updated with verified data: Jan 19, 2026)
**Source:** Admin team discovery call (Jan 15) + Sindbad discovery call (Jan 8) + Verification Q&A (Jan 19)

---

## 🚨 Critical Finding: €150,000 Outstanding Money

**Verified data (Jan 19, 2026):**
- **Total outstanding from clients:** €150,000
- **Overdue >30 days:** €100,000
- **Recent <30 days:** €50,000

**This changes the entire value proposition.** The ROI isn't just about saving 20 hours/month of Sindbad's time. It's about collecting €150K faster through systematic tracking and automated reminders.

**Direct cost:** €5,000/year (5% cost of capital on €100K overdue)
**Indirect cost:** Strategic initiatives delayed due to cash flow constraints

---

## Overview (Updated with Verified Numbers)

**Verified hourly rates:**
- Sindbad: **€50/hour** (not €100 as initially assumed)
- Admin team: **€20/hour** (not €50 as initially assumed)

**Top Priority:** Rate synchronization automation - eliminates manual updates across 3 Google Sheets, prevents errors, saves 3.5 hours/month.
- **Verified annual value:** €10,200 (€1,200 time + €9,000 error prevention)

**Biggest Pain Point:** Freelancer payment reconciliation consuming 5.5 hours/week (22 hours/month) of Sindbad's time, with 10% error rate.
- **Verified annual value:** €10,560 (time savings only)
- **But the bigger value:** Helping collect €150K outstanding money faster

**Total Verified Annual Value:** €28,400 (time + errors + cash flow cost)

---

## Priority Opportunities

### 1. Rate Synchronization Automation (Admin Team)
**Quadrant:** Quick Win (Low Effort, High Impact)

**Pain Point:**
Leonor manually updates freelancer rates across 3 separate Google Sheets (Team Directory → Freelancer Cost Assumptions → Dashboard) every time someone gets a raise. With 2-3 raises per new hire in first year and batch raises of 5-10 freelancers, this creates high error risk. Leonor spends "whole day a month" (2+ hours) just verifying rate consistency across sheets. Rate discrepancies cause downstream errors in Sindbad's invoice validation.

**Opportunity:**
Single source of truth in Team Directory → Google Sheets API automation syncs rates to FCA and Dashboard in real-time. Eliminates manual double/triple entry, prevents rate discrepancies, creates audit trail of rate changes.

**Estimated Effort:**
- Time: 1-2 weeks
- Complexity: Low (Google Sheets API, straightforward data sync)
- Dependencies: Google Sheets API, n8n/Make.com automation platform

**Verified Value (Jan 19, 2026):**
- **Time savings:** 2.5 hours/month (Leonor) + 1 hour/month (Sindbad error correction)
  - Leonor: 2.5 hrs × €20/hr = €50/month
  - Sindbad: 1 hr × €50/hr = €50/month
  - Combined time value: **€100/month = €1,200/year**
- **Error prevention:** €9,000/year (5 errors/month × €150 avg error cost)
- **Total annual value:** **€10,200**
- Mental load: Leonor no longer worries "did I update all 3 sheets?"
- Strategic value: Foundation for all future Google Sheets automations

**ROI:** €2,000-5,000 investment ÷ €10,200 annual value = **2-6 month payback**

---

### 2. Freelancer Invoice Validation System (Sindbad)
**Quadrant:** High Value (Medium Effort, High Impact)

**Pain Point:**
Sindbad spends 5-6 hours every week (20+ hours/month) manually reviewing 15-20 freelancer invoices, checking hours against Google Sheets dashboard, verifying rates, and processing payments through Wise. Must be weekly for cash flow management. Currently catches errors about 10% of time: projects not entered in dashboard (unbilled work), rate discrepancies, excessive hours. Quality control falls entirely on founder.

**Opportunity:**
Automated invoice validation system that cross-references invoices against Google Sheets project dashboard, flags discrepancies (missing projects, wrong rates, hour thresholds), and prepares batch payments for Wise. Maintains human checkpoint before final payment while eliminating manual reconciliation work. Prevents revenue leakage from unbilled projects.

**Estimated Effort:**
- Time: 6-8 weeks
- Complexity: Medium
- Dependencies: Google Sheets API, Wise API integration, error detection logic, notification system, human approval workflow

**Verified Value (Jan 19, 2026):**
- **Time savings:** 17.6 hours/month (80% reduction from 22 hrs/month)
  - Value: 17.6 hrs × €50/hr = **€880/month = €10,560/year**
- **Error prevention:** Catches the same 10% error rate but faster
- **Strategic value:** Frees Sindbad for business strategy, screenplay writing, Bold Move TV growth

**Critical context:** This ROI is for time savings only. The bigger opportunity is the **€150K outstanding money** (€100K overdue >30 days). Automation that helps collect this faster has much higher ROI than time savings alone.

**ROI:** €15,000-25,000 investment ÷ €10,560 annual value = **17-28 month payback (time only)**
- But with outstanding money tracking included: much faster payback

---

### 3. Call Recording & Transcription System
**Quadrant:** Quick Win (Low Effort, Medium Impact)

**Pain Point:**
Leonor conducts personalized feedback calls with freelancers during raises but doesn't record them. Must manually remember to update admin (rates, feedback notes) after calls. Often delays updates because "something comes up later." No audit trail of feedback conversations. Mental burden of remembering what was discussed.

**Opportunity:**
Fathom (free) call recording → auto-transcription → extract rate changes and action items → send summary to Leonor via email/Discord post-call. Eliminates "remember to update later" burden, creates feedback audit trail, can trigger rate sync automation automatically.

**Estimated Effort:**
- Time: 1 week
- Complexity: Low
- Dependencies: Fathom account, n8n/Make.com for post-call automation, Gmail/Discord API

**Estimated Value:**
- Time savings: 1-2 hours/month (eliminate manual note-taking and post-call admin)
- Mental load: No more "did I update rates after that call?"
- Audit trail: Record of all feedback conversations for HR purposes
- Strategic value: Integrates with rate sync automation (call transcript → auto-update rates)

**ROI:** 1-2 week payback, improves admin accuracy, creates feedback documentation

---

### 4. Project Calendar Reminders (Month-End Invoicing)
**Quadrant:** Easy Win (Low Effort, Medium Impact)

**Pain Point:**
Projects end but hours collection and client invoicing get delayed because manual tracking. Sometimes invoicing slips 1-2 months later, making it "awkward" to request payment for old projects. No systematic reminders based on project end dates. Mental burden of tracking which projects need hours collected and which need invoicing.

**Opportunity:**
Google Calendar automation triggers reminders based on project end dates:
- 4 days post-project: Reminder to collect all freelancer hours
- 7 days post-project: Reminder to send client invoice with recap
Send reminders to Discord or email (admin team's daily tools). Prevent cascade delays from hours → invoicing → payment.

**Estimated Effort:**
- Time: 1-2 weeks
- Complexity: Low
- Dependencies: Google Calendar API, Dashboard integration for project dates, Discord/Gmail notifications

**Estimated Value:**
- Time savings: 2-3 hours/month (eliminate manual tracking of project close-outs)
- Cash flow: Faster client invoicing = faster payment cycles
- Relationship value: Less awkward "oh sorry we forgot to invoice you 6 weeks ago" conversations
- Strategic value: Smoother month-end close process

**ROI:** 2-3 week payback, improves cash flow timing, reduces admin stress

---

### 5. Dashboard Validation Rules
**Quadrant:** Easy Win (Low Effort, Medium Impact)

**Pain Point:**
Admin team enters project hours and rates into Google Sheets dashboard, but errors slip through: projects not entered (unbilled work), rate discrepancies, excessive hours. These errors are only caught when Sindbad manually reviews invoices weekly. No upstream validation means quality control happens too late in the process.

**Opportunity:**
Add automated validation rules directly into Google Sheets dashboard: rate checking against FCA, missing project alerts, hours threshold warnings, duplicate entry detection. Catches errors at data entry time instead of invoice review time. Improves admin team efficiency and reduces Sindbad's review burden by 30-40%.

**Estimated Effort:**
- Time: 1-2 weeks
- Complexity: Low
- Dependencies: Google Sheets scripting (Apps Script), validation rule logic, notification setup

**Estimated Value:**
- Time savings: 6-8 hours per month (reduces Sindbad's manual review by 30-40%)
- Revenue impact: Prevents unbilled work by catching missing projects immediately
- Strategic value: Complements invoice validation system, identifies admin team workflow inefficiencies

**ROI:** 2-3 week payback, recurring monthly value, low-risk quick win that can be implemented independently

---

## Opportunity Matrix Visualization

```
HIGH IMPACT
    │
    │  #1 ✓         │  #2 ✓
    │  #3 ✓         │
    │  #4 ✓         │
    │  #5 ✓         │
────┼───────────────┼─────────
    │               │
    │               │
    │               │
LOW IMPACT         HIGH EFFORT
```

---

## Recommended Next Steps

1. **Immediate (Week 1):** Implement Rate Synchronization Automation (#1) - fastest ROI, prevents errors upstream, unlocks other automations. Parallel: Set up Fathom call recording (#3) for Leonor's feedback calls.

2. **This Month (Weeks 2-4):** Deploy Dashboard Validation Rules (#5) and Project Calendar Reminders (#4) - both low-hanging fruit with independent value. These can run in parallel.

3. **Next Quarter (Months 2-3):** Build Invoice Validation System (#2) after admin team workflows are optimized. This is the highest-value automation but requires the foundation pieces first.

---

## Comparative Analysis: Ambush vs Bold Move TV

### Why Prioritize Ambush First

**Ambush (Verified Data):**
- **Clear ROI:** €28,400/year (€13,200 time + €9,000 errors + €5,000 cash flow)
- **Outstanding money:** €150K needs collection (€100K overdue >30 days)
- Pays Sindbad's bills (90% revenue)
- Budget available: €2-3K initially, open to more for full admin chain
- Well-defined workflows and error patterns
- Admin team engaged and bought in

**Bold Move TV:**
- Unknown ROI: No baseline conversion data
- Not yet profitable (10% revenue)
- Sales strategy unclear (needs partner alignment)
- Lower immediate impact on time savings

**Recommendation:** Focus Ambush automation first. Time saved = Sindbad can focus on Bold Move TV sales growth. Use Ambush ROI to fund Bold Move TV automation later.

---

## Deprioritized Items

**Newsletter Automation (Bold Move TV):**
- Why deprioritized: Requires content creation capacity that doesn't exist yet. Better to solve lead capture first, then consider content marketing in Phase 2.

**Full Payment Automation (Ambush):**
- Why deprioritized: Start with validation + payment prep (human approval checkpoint). Build trust before full automation. Gradual adoption path reduces risk.

**Freelancer Self-Service Portal:**
- Why deprioritized: High build complexity, low immediate ROI. Current email/Discord workflow acceptable for now. Consider in Phase 3 after core automations proven.

---

## Success Metrics Summary

### Rate Synchronization
- **Time:** 2+ hours/month saved (verification eliminated)
- **Errors:** Zero rate discrepancies across sheets
- **Adoption:** Admin team reports "single update, done" workflow

### Invoice Validation
- **Time:** 16-20 hours/month saved (80% reduction)
- **Accuracy:** ≥10% error detection (match manual rate)
- **Revenue:** Zero unbilled projects (all work invoiced)

### Call Recording
- **Time:** 1-2 hours/month saved (note-taking eliminated)
- **Adoption:** Leonor uses Fathom for 100% of feedback calls
- **Audit:** Complete feedback history documented

### Calendar Reminders
- **Time:** 2-3 hours/month saved (tracking eliminated)
- **Cash flow:** Invoicing within 7 days of project end
- **Relationships:** Zero awkward late invoicing conversations

### Dashboard Validation
- **Time:** 6-8 hours/month saved (Sindbad review reduced)
- **Errors:** 50% reduction in admin entry errors
- **Adoption:** Admin team reports helpful real-time feedback

---

## Total Value Proposition

**Time Savings:**
- Admin team: 3-4 hours/month
- Sindbad: 16-20 hours/month
- **Total: 20-25 hours/month**

**Financial Impact:**
- Time saved: €21K-27K annually (at €100/hour conservative)
- Unbilled work prevented: €5K-10K annually (10% error rate across 50 projects/month)
- Cash flow improvement: 2-4 weeks faster client payment cycles
- **Total Annual Value: €25K-40K**

**Investment:**
- Quick wins (#1, #3, #4, #5): €5K-10K estimated
- Invoice validation (#2): €15K-20K estimated
- **Total Investment: €20K-30K**

**ROI Timeline:**
- Quick wins: 2-4 months payback
- Invoice validation: 8-12 months payback
- **Overall: <12 months payback, then €25K-40K annually**

---

*Compiled from admin team discovery call (Jan 15) and Sindbad discovery call (Jan 8, 2026)*
*File created: January 18, 2026*
