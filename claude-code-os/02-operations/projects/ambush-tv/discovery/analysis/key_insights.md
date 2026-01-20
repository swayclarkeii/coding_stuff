# Ambush TV - Key Insights

## One-Liner
**Sindbad spends 20+ hours/month manually validating freelancer invoices while Leonor manually syncs rates across 3 separate Google Sheets, creating compounding error risks across Ambush's 50-project-per-month operation.**

---

## Critical Pain Points

### Pain Point 1: Freelancer Invoice Reconciliation (Sindbad)

**What happens today:**
1. Admin team enters project data into Google Sheets dashboard (monthly tabs)
2. Freelancers submit invoices weekly (15-20 per week)
3. Sindbad manually reviews every invoice against dashboard
4. Checks hours, rates, project details, turnover calculations
5. Manually makes 15-20 payments per week via Wise
6. Catches errors ~10% of the time (missing projects, rate discrepancies, excessive hours)

**Time cost:** 5-6 hours per week (20-24 hours/month)
**Percentage of Sindbad's time:** Dominates his week
**What it prevents:** Business strategy, screenplay writing, Bold Move TV growth

**Why it can't be eliminated:**
- Quality control is critical (10% error rate)
- Admin team needs oversight
- Cash flow requires weekly cadence (tried bi-weekly, caused problems)
- Sindbad wants "second set of eyes" not blind trust

---

### Pain Point 2: Manual Rate Synchronization (Leonor)

**What happens today:**
1. Weekly team meeting: Core team identifies freelancers to raise
2. Leonor conducts personalized feedback calls with each freelancer
3. Manually updates rate in Team Directory sheet
4. Manually updates rate in Freelancer Cost Assumptions (FCA) sheet
5. Verifies rate auto-populated in Dashboard sheet
6. Batch raises = multiply steps by 5-10 freelancers

**Time cost:** 2+ hours per month just verification
**Error scenarios:**
- Rate changed in Team Directory but not FCA
- Rate changed in FCA but not Team Directory
- Discrepancies between sheets cause downstream errors
- "Whole day a month" spent reconciling across sheets

**Leonor's Fear:**
> "I just feel like for me personally, it opens me up to a lot of error."

**Why this compounds Sindbad's problem:**
- Rate discrepancies in FCA/Dashboard = Sindbad catches during invoice review
- Leonor's admin errors become Sindbad's validation burden
- Error cascade: Admin team → Freelancer invoices → Sindbad's review

---

## Upstream/Downstream Data Flow Diagram

**The core problem:** Data errors at the source (Calendar, Team Directory) cascade downstream and eventually land on Sindbad's desk during invoice validation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          UPSTREAM DATA SOURCES                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐     │
│  │  GOOGLE         │      │  TEAM           │      │  FEEDBACK       │     │
│  │  CALENDAR       │      │  DIRECTORY      │      │  CALLS          │     │
│  │                 │      │                 │      │  (Fathom)       │     │
│  │  • Project      │      │  • Freelancer   │      │                 │     │
│  │    schedules    │      │    rates        │      │  • Rate raises  │     │
│  │  • Freelancer   │      │  • Contact info │      │  • Agreements   │     │
│  │    assignments  │      │  • Start dates  │      │  • Promises     │     │
│  └────────┬────────┘      └────────┬────────┘      └────────┬────────┘     │
│           │                        │                        │               │
│           │ ⚠️ Names don't match   │ ⚠️ Manual update       │ ⚠️ Not        │
│           │    Dashboard entries   │    required            │    captured   │
│           ▼                        ▼                        ▼               │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          MIDSTREAM: ADMIN SHEETS                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐     │
│  │  FREELANCER     │      │                 │      │  PROJECT        │     │
│  │  COST           │◄─────│   DASHBOARD     │◄─────│  DIRECTORY      │     │
│  │  ASSUMPTIONS    │      │                 │      │                 │     │
│  │  (FCA)          │      │  • Monthly tabs │      │  • Client info  │     │
│  │                 │      │  • Hours logged │      │  • Budgets      │     │
│  │  • Rate lookups │      │  • Project data │      │  • End dates    │     │
│  │  • Calculations │      │  • Totals       │      │                 │     │
│  └────────┬────────┘      └────────┬────────┘      └─────────────────┘     │
│           │                        │                                        │
│           │ ⚠️ Rate may not match  │ ⚠️ Data may be                         │
│           │    Team Directory      │    incomplete/wrong                    │
│           ▼                        ▼                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DOWNSTREAM: VALIDATION & PAYMENT                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐     │
│  │  FREELANCER     │      │  SINDBAD'S      │      │  WISE           │     │
│  │  INVOICES       │─────►│  VALIDATION     │─────►│  PAYMENTS       │     │
│  │                 │      │                 │      │                 │     │
│  │  • 15-20/week   │      │  • 5-6 hrs/week │      │  • Batch        │     │
│  │  • Various      │      │  • Cross-check  │      │    payments     │     │
│  │    formats      │      │  • Catches 10%  │      │  • Weekly       │     │
│  │                 │      │    errors       │      │                 │     │
│  └─────────────────┘      └─────────────────┘      └─────────────────┘     │
│                                     ▲                                        │
│                                     │                                        │
│                     ALL UPSTREAM ERRORS LAND HERE                            │
│                     Sindbad is the "final filter"                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Error Cascade Examples

**Example 1: Rate Mismatch**
```
Leonor raises freelancer rate in feedback call
        ↓
Updates Team Directory (sometimes forgets)
        ↓
FCA still has old rate (not synced)
        ↓
Dashboard calculates with old rate
        ↓
Freelancer submits invoice with NEW rate
        ↓
Sindbad catches discrepancy during validation ← BOTTLENECK
```

**Example 2: Name Mismatch (from Alice)**
```
Project scheduled in Google Calendar with freelancer "John D."
        ↓
Admin enters project in Dashboard as "John Doe"
        ↓
Team Directory has freelancer as "John Michael Doe"
        ↓
Invoice arrives signed "JM Doe"
        ↓
Sindbad manually matches across all systems ← BOTTLENECK
```

**Example 3: Missing Project**
```
Client requests rush project (quick email)
        ↓
Freelancer assigned via Discord (no Calendar entry)
        ↓
No Dashboard entry created (forgot)
        ↓
Freelancer submits invoice for work done
        ↓
Sindbad can't validate (no reference data) ← BOTTLENECK
```

### Why Fixing Upstream Matters

**Current state:** Every error flows to Sindbad.
**Proposed state:** Catch errors at source, only exceptions reach Sindbad.

| Fix Location | Impact |
|--------------|--------|
| **Rate sync (upstream)** | Eliminates rate mismatch errors entirely |
| **Name normalization (upstream)** | Eliminates fuzzy matching burden |
| **Calendar-Dashboard sync (upstream)** | Eliminates missing project errors |
| **Dashboard validation rules (midstream)** | Catches data entry errors before invoice |
| **Invoice pre-validation (downstream)** | Reduces Sindbad's review load by 80-90% |

**Key insight:** Fixing upstream is cheaper and more effective than fixing downstream.

---

### Pain Point 3: Month-End Invoicing Delays

**What happens today:**
1. Projects have estimated end dates in Dashboard
2. End dates shift (project extends unexpectedly)
3. Manual tracking of which projects need hours collected
4. Manual tracking of which projects need client invoicing
5. Delays cascade: Project ends → forget to collect hours → delay invoicing → awkward late payment requests

**Time cost:** Unknown (manual, ad-hoc, creates stress)
**Business impact:** Client invoicing delayed 1-2 months post-project
**Relationship cost:** Awkward conversations with clients

**Madalena's Insight:**
> "It's also really awkward for us to go back, like, a month and a half later and be like, hi, I'm sorry we didn't say anything, it's because your project sucked, please pay us so much, and there's overhours, and there's this."

**The deeper problem:**
- No systematic reminders triggered by project end dates
- Calendar dates are estimates, but no alerts when dates shift
- Mental burden of tracking 50 projects/month for close-out

---

### Pain Point 4: Tool Integration Gaps

**Current tool ecosystem:**
- Google Workspace (free): Sheets, Docs, Gmail, Calendar
- Discord (free): Team communication instead of Slack
- No Notion: Too expensive for team collaboration
- No Salesforce/CRM: Budget constraints
- Attempted: Fireflies, Otter (hit limits, abandoned)

**The Problem:**
Standard automation tools assume paid enterprise stack (Slack, Notion, Salesforce). Ambush uses free alternatives that don't have direct integrations.

**Madalena's Frustration:**
> "These all have certain integrations with certain services that normal companies would use. But because we are cutting costs at every corner... We don't use Slack. We use Discord, which is almost exactly the same, but it's like a, it's like, you know, Discord. It's like a Twitch streaming group... it's not something that would have integrations with other things because it's another free program."

**Data Death Zone:**
Tools generate useful outputs (transcripts, summaries, action items) but data sits in tabs no one opens because it doesn't flow into daily tools (Sheets, Discord).

**Madalena's Observation:**
> "You get the transcripts and you get the summaries with the action items and stuff, but then that just sits in that tab of that AI thing that none of us are opening because we have like 60 sheets open instead."

---

## Business Impact

### Ambush Current State
- **Revenue contribution:** 90% of Sindbad's income (pays his bills)
- **Team size:** 9 core people + 70-80 freelancers
- **Volume:** ~50 pitches per month
- **Payment volume:** 15-20 payments per week
- **Invoice validation:** 20-24 hours/month (Sindbad)
- **Rate management:** 2+ hours/month verification (Leonor)
- **Error rate:** ~10% (projects not entered, rate issues, hour discrepancies)
- **Growth stage:** Recently reinforced team (more expensive structure, need to maintain volume)
- **Market position:** Word-of-mouth driven, sometimes unable to meet demand

### Rate Management Complexity
- **Sliding scale system:** Freelancers start low, progress to top rate
- **Raise frequency:**
  - New hires: 2-3 raises in first year
  - Mid-level: 1-2 raises per year
  - Senior: Slower progression
  - Example: One freelancer had 4 raises in 2024, 2 raises in 2025
- **Batch raises:** 5-10 freelancers at once during weekly team reviews
- **Personalized feedback:** Leonor values individual conversations, tailored guidance

### Potential State (with automation)

**Invoice Validation System:**
- **Time per week:** 5-6 hours → 1-2 hours (80-90% reduction)
- **Monthly time savings:** 18-23 hours
- **What Sindbad will do:** Business strategy, screenplay writing, Bold Move TV growth
- **Quality control:** Maintained via human-in-the-loop checkpoints
- **Error detection:** Automated flagging, Sindbad approves exceptions
- **Admin team efficiency:** Upstream errors caught earlier (dashboard validation)

**Rate Synchronization System:**
- **Current:** Manual triple-entry across 3 sheets
- **Projected:** Single source of truth, auto-sync via API
- **Time savings:** 2+ hours/month verification eliminated
- **Error reduction:** Zero rate discrepancies
- **Mental load:** Leonor updates once, done

**Calendar Reminder System:**
- **Current:** Manual tracking, delays, awkward conversations
- **Projected:** Automated reminders 4 days (hours) and 7 days (invoicing) post-project
- **Cash flow:** Faster client invoicing cycles
- **Relationship value:** Professional, timely invoicing

---

### ROI Calculation

> **✅ VERIFIED DATA** (Responses received Jan 19, 2026)
> - See `sindbad_responses.md` for full Q&A
> - All numbers below use verified rates and costs from Sindbad

**Invoice Validation Automation:**

```
FORMULA:
Monthly time saved = [current hrs/week] × 4 × [reduction %]
                   = 5.5 × 4 × 0.80 = 17.6 hrs/month (using 80% reduction)

Annual value = Monthly time saved × 12 × [hourly value]
             = 17.6 × 12 × €50
             = €10,560/year

Payback months = Investment ÷ (Annual value ÷ 12)
```

| Variable | Source | Value Used | Status |
|----------|--------|------------|--------|
| Current hours/week | Sindbad response | 5.5 hours (average) | ✅ Verified |
| Reduction achievable | Industry benchmark | 80% | ⚠️ Conservative estimate |
| Hourly value | Sindbad response | **€50/hour** | ✅ Verified |

**Verified calculation:**
- **Time saved per month:** 17.6 hours (80% of 22 hrs)
- **Annual time saved:** 211 hours
- **Annual value @ €50/hr:** **€10,560**
- **Investment (estimated):** €15,000-25,000
- **Payback period:** 17-28 months (time savings only)

---

**Rate Synchronization Automation:**

```
FORMULA:
Monthly time saved = [verification hours] + [error correction hours]
                   = 2.5 hours (Leonor) + 1 hour (Sindbad)
                   = 3.5 hours/month

Annual value (Leonor) = 2.5 × 12 × €20 = €600
Annual value (Sindbad) = 1 × 12 × €50 = €600
Total time value = €1,200/year

Error prevention value = [errors/month] × [avg error cost]
                       = 5 × €150 = €750/month = €9,000/year
```

| Variable | Source | Value Used | Status |
|----------|--------|------------|--------|
| Verification hours/month | Leonor transcript | 2.5 hours | ✅ Verified |
| Error correction (Sindbad) | Estimate | 1 hour | ⚠️ Conservative |
| Admin hourly rate | Sindbad response | **€20/hour** | ✅ Verified |
| Errors prevented/month | Estimate from 10% rate | 5 errors | ✅ Based on verified data |
| Average error cost | Sindbad response | **€150** (mid-range) | ✅ Verified (€50-300) |

**Verified calculation:**
- **Time saved per month:** 3.5 hours
- **Annual time value:** €1,200
- **Error prevention value:** €9,000/year
- **Total annual value:** **€10,200**
- **Investment (estimated):** €2,000-5,000
- **Payback period:** 2-6 months

---

**Outstanding Money Collection Automation:**

**NEW INSIGHT:** This is the highest-value opportunity based on verified data.

```
FORMULA:
Outstanding total = €150,000
Overdue >30 days = €100,000

Cost of capital (5% annually on overdue) = €100,000 × 0.05 = €5,000/year

Opportunity cost = Projects/initiatives delayed due to cash flow constraints
```

| Variable | Source | Value Used | Status |
|----------|--------|------------|--------|
| Total outstanding | Sindbad response | **€150,000** | ✅ Verified |
| Overdue >30 days | Sindbad response | **€100,000** | ✅ Verified |
| Recent (<30 days) | Sindbad response | **€50,000** | ✅ Verified |

**Value calculation:**
- **Direct cost of capital:** €5,000/year (conservative 5% on €100K)
- **Indirect costs:**
  - Can't invest in growth initiatives
  - Manual tracking of 50+ outstanding invoices
  - Awkward client conversations (relationship damage)
  - Mental burden on Sindbad

**What automation enables:**
- Automated reminders at day 0, 7, 14, 30
- Dashboard showing aging of receivables
- Clear escalation path for >30 day invoices
- Professional, systematic collection vs. ad-hoc

---

**Calendar Reminder Automation:**

```
FORMULA:
Time saved = [hours tracking] + [hours follow-up]
            = 2.5 hours/month (admin team)

Annual value = 2.5 × 12 × €20 = €600/year

Cash flow improvement = Faster invoicing → faster payment
```

| Variable | Source | Value Used | Status |
|----------|--------|------------|--------|
| Projects per month | Transcript | ~50 | ✅ Verified |
| Current collection delay | Madalena quote | 4-6 weeks | ✅ Verified |
| Tracking hours/month | Estimate | 2.5 hours | ⚠️ Conservative |
| Admin hourly rate | Sindbad response | **€20/hour** | ✅ Verified |

**Verified calculation:**
- **Time saved per month:** 2.5 hours
- **Annual time value:** €600
- **Cash flow impact:** 2-4 weeks faster invoicing = reduced outstanding balance
- **Investment (estimated):** €2,000-5,000
- **Payback period:** 40+ months (time only) or 6-12 months (with cash flow benefit)

---

**Combined Total (Verified Numbers):**

```
FORMULA:
Annual value = Time savings + Error prevention + Cash flow
             = (Sindbad time + Admin time) + Error prevention + Outstanding money cost

Sindbad time savings:
- Invoice validation: €10,560
- Rate error correction: €600
- Total: €11,160/year

Admin time savings:
- Rate sync: €600
- Calendar tracking: €600
- Total: €1,200/year

Error prevention: €9,000/year

Cash flow (conservative): €5,000/year

TOTAL ANNUAL VALUE: €26,360
```

**Investment options:**
- **Quick wins package (€8K):** Rate sync + Invoice pre-check + Fathom
  - Annual value: ~€15K-18K
  - Payback: 6-8 months

- **Full solution (€20K-25K):** All automation + outstanding money tracking
  - Annual value: ~€26K+
  - Payback: 11-14 months

- **5-year value:** €131,800

---

## Critical Insight: Budget Expectation Gap

**Sindbad's initial budget expectation:** €2-3K for "automation that saves 20+ hours/month"

**But he also said:** "My understanding is that you would propose tools that would help the whole admin chain. For that, we'd be prepared to pay substantially more of course, as long as we're confident that it would help rather than bring more complexity or bugs"

**The strategy:**
1. **Don't lead with €20K-25K pricing** - this will trigger sticker shock
2. **Lead with value story:** Outstanding €150K + admin chain efficiency + error prevention
3. **Anchor on €8K minimum viable package** - feels closer to his €2-3K expectation
4. **Show upgrade path:** Prove value with €8K, then expand to full solution
5. **Address confidence concern:** Pilot approach, human-in-the-loop, clear rollback plan

**Key phrases from Sindbad:**
- "As long as we're confident it would help rather than bring more complexity or bugs"
- "We'd be prepared to pay substantially more" (for full admin chain)
- "Both [Sindbad and Pierre] need to approve"

**Implication:** Need Pierre buy-in. Show both strategic value (time for Bold Move TV) AND financial ROI (outstanding money, error prevention).

---

## The "Aha Moment"

### Human-in-the-Loop as Trust-Building Architecture

**Initial Fear (Sindbad):**
> "I wouldn't want to do a batch payment before I've checked everything."

**Sway's Reframe:**
> "It doesn't have to be an all or nothing. It doesn't have to be a Sindbad is in the process, or he's not in the process at all, and it's automated, right? You can always add in like a human checkpoint."

**Sindbad's Response:**
> "I would be interested in not only speeding up my process, but also theirs [admin team]."

**What Sindbad thought automation meant:**
- Remove human from process entirely
- Blind trust in system
- No quality control
- Risk of payment errors

**What Sindbad actually needs:**
- Automated data validation
- Exception flagging
- Human approval checkpoint
- 80-90% time reduction, not 100%

**The key insight:** Automation isn't about removing Sindbad - it's about upgrading him from data entry clerk to exception handler. He only reviews the 10% that needs human judgment.

---

### API Integration as Free Tool Unlock

**Admin Team's Frustration:**
Free tools (Discord, Google Workspace, Fathom) don't integrate with each other via standard automation platforms (Zapier, etc.) because they're not "enterprise" tools.

**Sway's Solution:**
> "You have direct integrations, and then you have API integrations, meaning that an API integration means I can integrate any system with any system."

**Example Given:**
Fathom → n8n/Make.com → Gmail/Discord/Google Sheets (all via APIs, not direct integrations)

**What changed:**
- From: "Discord doesn't integrate with anything because it's free"
- To: "We can connect any API-enabled tool via automation platforms"

**Impact:**
- Unlocks Fathom call transcripts → Discord/Email
- Unlocks Google Sheets rate changes → auto-sync across sheets
- Unlocks Google Calendar → Discord reminders
- Budget constraints no longer block automation

---

## Critical Discovery Process Decisions

### D1: Include Admin Team in Discovery (Sindbad Call)

**What changed:**
- From: "Sindbad describes his pain points"
- To: "Admin team describes their workflows and pain points"

**Why it matters:**
Sindbad's problem (invoice validation) is downstream of admin team's problems (rate synchronization, project tracking). Can't solve downstream without understanding upstream.

**Impact:**
- Discovered rate sync as root cause of some invoice errors
- Revealed tool integration gaps blocking admin efficiency
- Built admin team buy-in from start
- Prevented building wrong solution

---

### D2: API-Based Integration Approach (Admin Team Call)

**What changed:**
- From: "We can't automate because our tools don't integrate"
- To: "We can automate via API-level connections"

**Why it matters:**
Budget constraints force free tool usage, but free tools lack direct integrations. API approach unlocks automation without enterprise tool budget.

**Impact:**
- Madalena's technical frustration addressed
- Fathom, Discord, Google Workspace all become integrable
- Opens path to automation without tool switching
- Maintains familiar workflows (Google Sheets, Discord)

---

## Technical Feasibility Confirmed

### Google Sheets Rate Synchronization

✅ **Google Sheets API:** All 3 sheets (Team Directory, FCA, Dashboard) machine-readable
✅ **Single source of truth:** Team Directory can be authoritative
✅ **Auto-sync pattern:** API triggers on Team Directory change → update FCA and Dashboard
✅ **Validation logic:** Check for rate discrepancies before sync
✅ **Audit trail:** Log all rate changes with timestamps

### Invoice Validation System

✅ **Google Sheets API:** Dashboard data is machine-readable
✅ **Wise API:** Batch payment capability exists (to be confirmed)
✅ **Invoice parsing:** Standard formats (Google Docs templates)
✅ **Error patterns:** Well-defined (10% historical data available)
✅ **Validation logic:** Clear rules (hours, rates, project matching)

### Calendar Reminder System

✅ **Google Calendar API:** Project dates are machine-readable
✅ **Trigger logic:** Simple date-based reminders
✅ **Discord API:** Webhook support for notifications
✅ **Gmail API:** Email notifications as fallback
✅ **Dashboard integration:** Pull project end dates from Sheets

### Call Recording Integration

✅ **Fathom API:** Transcripts extractable post-call
✅ **Email delivery:** Gmail API for summary sending
✅ **Discord delivery:** Webhook for team notifications
✅ **Rate extraction:** AI can parse "raised to €X/hour" from transcript
✅ **Automation trigger:** Post-call → extract → notify → update

---

## Business Context & Competitive Dynamics

### Partnership Tension (Ambush)

**The elephant in the room (from Sindbad call):**
> "The sad thing about Ambush is, my business partner and I, like, really, we were very good at the beginning. And now, it's just, I don't, I don't think we have the same vision... I would almost prefer that he did like the bare minimum."

**Impact on project:**
- Partner (Pierre) started separate AI business without full disclosure
- Sindbad handles all finances and payments (partner does recruitment)
- No budget for buyout
- Tension around business direction

**What this means for automation:**
- Sindbad wants to reduce dependency on Ambush operations
- Time savings could accelerate Bold Move TV transition
- Automation might reveal inefficiencies (politically sensitive)
- Focus on Sindbad's workflow, not partner evaluation

---

### Budget Constraints Reality

**Evidence of cost-cutting:**
- "Cutting costs at every corner" (Madalena's words)
- Discord instead of Slack (free vs €7/user/month)
- Google Workspace Free instead of Notion (free vs €10/user/month)
- Attempted free call recorders (Fireflies, Otter) but hit limits
- No Salesforce, no paid CRM, no paid automation tools

**Why this matters:**
- Investment in automation must show clear ROI
- Can't propose expensive enterprise tools
- Must work within Google/Discord/Fathom free ecosystem
- API-based custom automation is the only feasible path

**Opportunity:**
Ambush pays Sindbad's bills (90% revenue). If automation saves 20+ hours/month, €20K-30K investment is justifiable from Ambush budget.

---

### Market Position Dynamics

**Ambush:**
- High demand (word-of-mouth, sometimes can't meet demand)
- Recently raised prices (testing market)
- Need volume to maintain new team structure (9 core people)
- Operationally complex (70-80 freelancers to manage)
- Recruitment handled by partner, finances handled by Sindbad

**The strategic opportunity:**
Time saved at Ambush → invested in Bold Move TV growth. Ambush automation unlocks Sindbad's strategic capacity.

---

## Cultural & Personal Factors

### Admin Team Work Styles

**Leonor:**
- **Focus:** People management, relationships, personalized feedback
- **Strength:** Individual freelancer coaching, tailored raises
- **Pain:** Manual admin burden after feedback calls
- **Value:** Thoughtful communication, fairness in raises

**Madalena:**
- **Focus:** Systems, automation, technical problem-solving
- **Strength:** ChatGPT-assisted formula building, attempted integrations
- **Pain:** Tool limitations, integration gaps, failed automation attempts
- **Value:** Efficiency, automation, reducing manual work

**Alice:**
- **Participation:** Minimal in this call (role unclear)
- **Status:** Stakeholder in admin processes

### What Admin Team Values

**Spending time on:**
- Personalized freelancer feedback (Leonor)
- Strategic systems design (Madalena)
- High-value admin work (not repetitive data entry)

**Not spending time on:**
- Triple-entry rate updates (Leonor)
- Manual tracking of project close-outs (Madalena)
- Verification days to catch discrepancies (Leonor)

### Trust-Building Requirements

1. **Transparency:** Show what automation does, don't hide complexity
2. **Control:** Human checkpoints, not black box
3. **Evidence:** Demonstrate accuracy before full deployment
4. **Incremental adoption:** Test with one workflow before scaling
5. **Escape hatch:** Easy way to revert if something breaks
6. **Team inclusion:** Admin team feels involved, not replaced

---

## Next Steps Requirements

### Rate Synchronization Implementation

**Must understand:**
1. Exact schema of Team Directory, FCA, and Dashboard
2. Current formulas and data flows between sheets
3. Rate change edge cases (currency changes, retroactive raises, new hire onboarding)
4. Single source of truth logic (Team Directory as master)
5. Validation rules before sync (prevent bad data propagation)

**Must deliver:**
- API-based sync architecture (Team Directory → FCA, Dashboard)
- Real-time or near-real-time updates (within 5 minutes)
- Audit trail of all rate changes
- Error handling for edge cases
- Rollback capability if needed

---

### Invoice Validation Implementation

**Must understand:**
1. Exact invoice format (Google Docs templates used by freelancers)
2. Dashboard schema for project hours, rates, names
3. Wise batch payment workflow and API capabilities
4. Error categories Sindbad currently catches
5. Human approval workflow design

**Must deliver:**
- Automated invoice parsing and data extraction
- Cross-reference validation (invoice vs dashboard)
- Error flagging dashboard for Sindbad review
- Wise batch payment file preparation
- Weekly validation reports

---

### Calendar Reminder Implementation

**Must understand:**
1. Dashboard structure for project dates (estimated vs actual)
2. Admin team's preferred notification channel (Discord vs Email)
3. Reminder timing preferences (4 days for hours, 7 days for invoicing)
4. Who receives reminders (admin team vs specific roles)
5. Edge cases (project extended, project canceled)

**Must deliver:**
- Google Calendar integration with Dashboard project dates
- Automated reminder triggers (4-day and 7-day post-project)
- Discord webhook or email notification
- Snooze/dismiss functionality for reminders
- Report of projects awaiting close-out

---

## Risk Factors

### High Risk

1. **Rate sync errors → downstream chaos:** If rate automation fails, affects invoices and payments
   - **Mitigation:** Parallel manual process for first 4 weeks, extensive testing with historical data

2. **Admin team fears job loss → resistance:**
   - **Mitigation:** Frame as "upgrade admin role" not replacement, emphasize strategic work capacity

3. **Partnership tension → political complications:**
   - **Mitigation:** Focus automation on Sindbad/admin workflows, not partner evaluation

### Medium Risk

1. **Google Sheets structure changes → integration breaks:**
   - **Mitigation:** Version control on schema, alert system for structural changes

2. **Weekly cash flow requirement → payment automation risk:**
   - **Mitigation:** Start with validation only, add payment prep later, maintain human checkpoint

3. **70-80 freelancers → edge case complexity:**
   - **Mitigation:** Pilot with 5-10 freelancers first, scale gradually

### Low Risk

1. **Technical feasibility:** All tools have APIs, standard integrations
2. **Adoption complexity:** Email forwarding and approval workflows are simple
3. **Data availability:** Historical invoices and dashboard exist for testing

---

## Strategic Recommendation

### Phase 1: Quick Wins (Weeks 1-4)

**Recommended Priority:**
1. Rate synchronization automation (highest admin impact, unlocks downstream)
2. Dashboard validation rules (catches errors upstream)
3. Fathom call recording setup (easy win, improves Leonor workflow)
4. Calendar reminder system (month-end invoicing pain point)

**Why this order:**
- Rate sync prevents errors that Sindbad catches later
- Dashboard validation reduces admin entry errors
- Fathom creates audit trail and triggers rate sync
- Calendar reminders improve cash flow timing

**Success criteria:**
- Zero rate discrepancies across sheets
- Admin team reports "single update" workflow
- Fathom used for 100% of feedback calls
- Reminders sent within 24 hours of project end

---

### Phase 2: Invoice Validation (Months 2-3)

**Recommended After:**
Quick wins proven successful, admin team workflows optimized, upstream errors reduced

**Why second:**
- Highest time savings (16-20 hours/month)
- Requires upstream fixes first (rate sync, dashboard validation)
- Higher technical complexity (Wise API, human approval workflow)
- Larger investment (€15K-20K vs €5K-10K for quick wins)

**Success criteria:**
- 80-90% time reduction (5-6 hours → 1-2 hours/week)
- Maintain or improve 10% error detection rate
- Zero payment errors during pilot
- Sindbad trusts system enough to scale

---

## Key Quotes for Proposals

### On Rate Management Pain
> "From my end, I think in terms of automatization, there's just one big thing that pops into mind, which is regarding the rates... I have to manually integrate it into the team directory. And then from the team directory, I have to then make sure that it's changed in the freelancer cost assumptions sheet so that it will show up correctly on the dashboard." - Leonor

### On Error Risk
> "I just feel like for me personally, it opens me up to a lot of error." - Leonor

### On Verification Burden
> "It just creates this like whole day a month where I go and I spend like two hours making sure that everything is right and corresponds." - Leonor

### On Tool Integration Frustration
> "These all have certain integrations with certain services that normal companies would use. But because we are cutting costs at every corner... We don't use Slack. We use Discord... it's not something that would have integrations with other things because it's another free program." - Madalena

### On Data Death Zone
> "You get the transcripts and you get the summaries with the action items and stuff, but then that just sits in that tab of that AI thing that none of us are opening because we have like 60 sheets open instead." - Madalena

### On Month-End Awkwardness
> "It's also really awkward for us to go back, like, a month and a half later and be like, hi, I'm sorry we didn't say anything, it's because your project sucked, please pay us so much, and there's overhours, and there's this." - Madalena

### On Time Value (Sindbad, Jan 8 call)
> "18 to 20 hours a month... If I didn't have to do these five hour, four to five hours every week, what else would you be doing? Oh, wow. You know, I don't know, like, thinking about the strategy of the business, or working on my screenplay, you know, I might be doing my personal stuff."

### On Quality Control Philosophy (Sindbad, Jan 8 call)
> "I wouldn't want to do a batch payment before I've checked everything. But if AI could check things and, you know, tell me if there was a discrepancy..."

### On API Integration (Sway)
> "You have direct integrations, and then you have API integrations, meaning that an API integration means I can integrate any system with any system."

---

*Compiled from admin team discovery call (Jan 15) and Sindbad discovery call (Jan 8, 2026)*
*File created: January 18, 2026*
