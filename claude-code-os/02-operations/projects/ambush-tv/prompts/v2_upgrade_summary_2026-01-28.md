# BPS Prompt v2.0 Upgrade Summary

**Date:** 2026-01-28
**Purpose:** Document transformation from shallow 2-3 sentence outputs to comprehensive 200-800+ line analysis

---

## Problem Statement

**v1.0 Output (Current State):**
- Client Insights: 2-3 sentences per field
- Performance Analysis: 2-3 sentences per field
- Total output: ~500 tokens (very shallow)
- Airtable records look "not satisfactory" and "shallow"

**v2.0 Output (Target State):**
- Client Insights: 200-800+ lines per major field
- Performance Analysis: 200-600+ lines per major field
- Total output: ~10,000-15,000 tokens (consultant-grade depth)
- Airtable records match example discovery documents (key_insights.md = 856 lines)

---

## Transformation Overview

### Client Insights Analysis Prompt

**v1.0 → v2.0 Changes:**

| Field | v1.0 Output | v2.0 Output |
|-------|------------|------------|
| **summary** | 2-3 sentences | 3-5 sentences with key metrics |
| **pain_points** | 3-5 sentences | 200-400 lines with multi-level breakdowns |
| **quick_wins** | 3-5 sentences | 150-300 lines with Opportunity Matrix |
| **action_items** | Simple list | 30-60 lines with structured prioritization |
| **key_insights** | 2-3 sentences | 300-800+ lines consultant-grade document |
| **pricing_strategy** | 2-3 sentences | 300-600 lines with multiple options |
| **client_journey_map** | 2-3 sentences | 200-400 lines step-by-step workflow |
| **requirements** | 2-3 sentences | 300-600 lines with acceptance criteria |

**Total Field Count:** 8 fields (unchanged)
**Total Output Volume:** ~50 lines → ~1,500-3,000+ lines

---

### Performance Analysis Prompt

**v1.0 → v2.0 Changes:**

| Field | v1.0 Output | v2.0 Output |
|-------|------------|------------|
| **performance_score** | Integer 0-100 | Integer 0-100 (same) |
| **improvement_areas** | 2-4 sentences | 3-6 detailed coaching bullets (20-40 lines) |
| **complexity_assessment** | 2-3 sentences | 200-400 lines with component breakdowns |
| **roadmap** | Empty string or 2-3 sentences | 200-400 lines month-by-month plan |
| **call_quality_notes** | 3-5 sentences | 100-200 lines comprehensive narrative |

**Total Field Count:** 5 fields (unchanged)
**Total Output Volume:** ~20 lines → ~520-1,040+ lines

---

## Key Structural Enhancements

### Pain Points Field (v1.0 vs v2.0)

**v1.0 Example:**
```
• **Manual rate synchronization:** Updating 3 separate sheets creates error risk. 2 hours/month.
• **Invoice validation:** 20+ hours/month manually reviewing invoices.
```

**v2.0 Structure:**
```markdown
### Pain Point 1: Manual Rate Synchronization

**Current Workflow (Step-by-Step):**
1. Weekly team meeting: Core team identifies freelancers to raise
2. Leonor conducts feedback calls (5 min each)
3. **[PAIN: Updates Team Directory sheet manually]**
4. **[PAIN: Updates FCA sheet manually - risk of forgetting]**
5. **[PAIN: Verifies Dashboard auto-populated - sometimes requires manual fix]**
6. Monthly reconciliation (2 hours) to catch discrepancies

**Time Cost:**
- Per call: 5 min/call (line 251 of transcript)
- Frequency: Bi-weekly batch raises (5-10 freelancers) (line 127)
- Verification: 2+ hours/month (line 299)
- Monthly total: 2.5 hours/month
- Annual total: 30 hours/year

**Error Scenarios:**
- Rate changed in Team Directory but not FCA → Dashboard shows old rate → Invoice validation fails
- Example from transcript: > "that person's charging is 18.5, but the dashboard says 17" (line 287)

**User Quotes:**
> "I just feel like for me personally, it opens me up to a lot of error." (line 49)
> "It just creates this like whole day a month where I go and I spend like two hours making sure..." (line 299)

**Downstream Impact:**
- Affects: Sindbad's invoice validation (catches rate discrepancies)
- Causes: 10 min fire drills every 3 months (line 299)
- Results in: Error cascade from admin → invoices → validation bottleneck

**Why It Matters:**
Leonor values personalized freelancer feedback but admin burden after calls creates avoidance behavior. Rate sync errors cascade downstream to Sindbad's invoice validation, compounding his 20+ hr/month workload.

[ASCII workflow diagram]
[Upstream/downstream data flow diagram]
```

**Volume:** 2 sentences → 40-100 lines per pain point

---

### Quick Wins Field (v1.0 vs v2.0)

**v1.0 Example:**
```
• **Rate synchronization automation:** Single source of truth, auto-sync via API (1-2 week build, saves 2 hrs/month)
```

**v2.0 Structure:**
```markdown
## Overview
**Top Priority:** Rate synchronization (Quick Win)
**Biggest Pain Point:** Manual updates across 3 sheets
**Estimated Total Value:** €10,200/year

---

## Priority Opportunities

### Priority 1: Rate Synchronization Automation 🎯
**Quadrant:** Quick Win (Low Effort, High Impact)

**Pain Point:**
Leonor manually updates freelancer rates across 3 separate Google Sheets (Team Directory → Freelancer Cost Assumptions → Dashboard) every time someone gets a raise. With 2-3 raises per new hire in first year and batch raises of 5-10 freelancers, this creates high error risk. Leonor spends "whole day a month" (2+ hours) just verifying rate consistency across sheets. Rate discrepancies cause downstream errors in Sindbad's invoice validation.

**Opportunity:**
Single source of truth in Team Directory → Google Sheets API automation syncs rates to FCA and Dashboard in real-time. Eliminates manual double/triple entry, prevents rate discrepancies, creates audit trail of rate changes.

**Estimated Effort:**
- Time: 1-2 weeks
- Complexity: Low (because: Google Sheets API well-documented, straightforward data sync, no complex logic)
- Dependencies: Google Sheets API access, n8n/Make.com automation platform
- Technical requirements: OAuth2 permissions, API rate limit handling, change detection webhook

**Verified Value:**

TIME SAVINGS:
```
FORMULA:
Current time = 2.5 hours/month (Leonor verification) + 1 hour/month (Sindbad error correction)
             = 3.5 hours/month

Annual time saved = 3.5 × 12 = 42 hours/year

Value (Leonor) = 30 hrs × €20/hr = €600/year
Value (Sindbad) = 12 hrs × €50/hr = €600/year
Total time value = €1,200/year
```

ERROR PREVENTION:
```
FORMULA:
Current error rate = Rate discrepancies once per 3 months = 4/year
Error rate after rate sync = ~5 errors/month prevented (10% of 50 projects)
Avg error cost = €150 (verified, line 287)

Annual error prevention = 5 errors/month × €150 × 12 months
                        = €9,000/year
```

TOTAL ANNUAL VALUE = €1,200 (time) + €9,000 (errors) = €10,200/year

**ROI Calculation:**
```
Investment estimate = €2,000-5,000 (1-2 weeks × €100/hr dev rate)
Annual value = €10,200
Payback period = €3,500 (avg) ÷ (€10,200 ÷ 12) = 4.1 months
```

[Opportunity Matrix visualization]
[Recommended sequencing]
[Success metrics]
[Deprioritized items]
```

**Volume:** 1 sentence → 30-60 lines per opportunity, plus 50-100 lines of framework structure

---

### Key Insights Field (v1.0 vs v2.0)

**v1.0 Example:**
```
• Admin team is technically capable but lacks API/automation expertise
• Rate sync is foundation for other automations
• Batch raise process amplifies error risk vs individual raises
```

**v2.0 Structure:**
```markdown
## One-Liner
**Sindbad spends 20+ hours/month manually validating freelancer invoices while Leonor manually syncs rates across 3 separate Google Sheets, creating compounding error risks across Ambush's 50-project-per-month operation.**

---

## Critical Pain Points

### Pain Point 1: Freelancer Invoice Reconciliation (Sindbad)

**What happens today:**
[8-10 step detailed current workflow]

**Time cost:** 5-6 hours per week (20-24 hours/month)
**Percentage of Sindbad's time:** Dominates his week
**What it prevents:** Business strategy, screenplay writing, Bold Move TV growth

**Why it can't be eliminated:**
- Quality control is critical (10% error rate)
- Admin team needs oversight
- Cash flow requires weekly cadence
- Sindbad wants "second set of eyes" not blind trust

---

## Upstream/Downstream Data Flow Diagram

[Comprehensive ASCII diagram showing:]
```
┌─────────────────────────────────────────────────────┐
│                UPSTREAM DATA SOURCES                 │
├─────────────────────────────────────────────────────┤
│  Google Calendar    Team Directory    Feedback Calls │
│      ↓                  ↓                  ↓          │
│  ⚠️ Names don't    ⚠️ Manual       ⚠️ Not captured  │
└──────────────────────┬──────────────────────────────┘
                       ↓
[Midstream systems with error points]
                       ↓
[Downstream validation with bottleneck]
```

### Error Cascade Examples
[3-4 detailed error cascade flow diagrams]

### Why Fixing Upstream Matters
[Comparison table showing fix location impact]

---

## Business Impact

### Ambush Current State
[15-20 metrics and context points with line citations]

### Rate Management Complexity
[Detailed breakdown of sliding scale system, frequencies, volumes]

### Potential State (with automation)
[Detailed projections per system with metrics]

---

## ROI Calculation

> **✅ VERIFIED DATA** (Responses received Jan 19, 2026)
> [Reference and validation notes]

**Invoice Validation Automation:**
[Step-by-step formula with intermediate calculations]
[Variable table with sources and verification status]
[Best/expected/worst case scenarios]

**Rate Synchronization Automation:**
[Same detailed formula structure]

**Combined Total:**
[Grand total formula with 5-year value calculation]

---

[Continue for 300-800+ lines total covering:]
- Critical insights
- Technical feasibility
- Business context
- Cultural factors
- Next steps requirements
- Risk factors
- Strategic recommendations
- Key quotes archive
```

**Volume:** 3-5 sentences → 300-800+ lines (full consultant-grade document)

---

### Complexity Assessment Field (v1.0 vs v2.0)

**v1.0 Example:**
```
Low — Single workflow automation (Google Sheets API sync across 3 sheets), well-documented API, straightforward data mapping. Estimated 1-2 week build.
```

**v2.0 Structure:**
```markdown
## Complexity Overview

**Overall Project Complexity:** Medium-High (6.5/10)

| Component | Complexity | Effort | Risk | Priority |
|-----------|------------|--------|------|----------|
| Rate Synchronization | Low | 1-2 weeks | Low | 1 |
| Fathom Integration | Low | 1 week | Low | 2 |
| Dashboard Validation | Low-Medium | 1-2 weeks | Low | 3 |
| Calendar Reminders | Low | 1-2 weeks | Low | 4 |
| Invoice Parsing | Medium | 3-4 weeks | Medium | 5 |
| Invoice Validation | Medium-High | 2-3 weeks | Medium | 6 |
| Error Flagging UI | Medium | 2-3 weeks | Low | 7 |
| Wise Integration | Medium-High | 2-3 weeks | High | 8 |

**Summary:**
8 components ranging from Low to Medium-High complexity. Foundation components (1-4) are low-risk quick wins with well-documented APIs. Core automation components (5-8) have moderate complexity due to multiple validation rules and payment integration risks. Overall confidence: Medium (needs Wise API validation).

---

## Component Analysis

### 1. Rate Synchronization Automation

**Complexity: Low**

**What It Does:**
Watch Team Directory for rate changes, auto-update FCA sheet when rate changes, auto-update Dashboard formulas/references, create audit trail of changes.

**Technical Requirements:**
- Google Sheets API (well-documented, stable v4 API)
- n8n/Make.com workflow engine
- Trigger: onEdit webhook or scheduled polling (5-min intervals)
- Data mapping: Team Directory rate column → FCA rate lookup → Dashboard formula references
- Audit logging: Append-only change log with timestamps

**Why It's Low Complexity:**
Single data type (rates), clear source of truth (Team Directory), standard CRUD operations, no external APIs beyond Google, well-defined data schema, extensive Google Sheets API documentation available.

**Factors that make it Simple:**
- Google Sheets API is mature and stable (v4, released 2016)
- Rate data is scalar value (no complex transformations)
- Sync is one-directional (Team Directory → others)
- Error handling is straightforward (retry on failure, alert on persistent errors)

**Known Unknowns:**
- Exact schema of Team Directory rate column (need to validate format: €20 vs 20 vs "20 EUR")
- Formula dependencies in FCA/Dashboard (need to map cell references to ensure sync doesn't break formulas)
- Edge cases: currency changes (€ to $ conversions?), retroactive rate adjustments (backfill needed?), new hire onboarding flow integration

**Effort Estimate:**
- **Best case:** 5 days (if schema is simple, no formula dependencies, straightforward webhook setup)
- **Expected case:** 1-2 weeks (realistic with normal schema complexity and formula mapping required)
- **Worst case:** 3 weeks (if extensive formula dependencies require refactoring or edge cases multiply)

**Confidence Level:** High
**Reasoning:** Google Sheets API is well-documented, rate sync is common automation pattern, minimal unknowns compared to other components.

**Dependencies:**
- Requires: Google Sheets API OAuth2 setup, n8n/Make.com platform access
- Enables: Fathom integration (rate change extraction triggers), Dashboard validation (relies on accurate FCA rates)
- External: Admin team to provide read-only access to sheets for schema analysis

[Continue for 7 more components with same 40-60 line detailed structure]

---

## Risk Assessment

### High Risk Components

**1. Wise Payment Integration**
- **Risk:** Wise API may not support batch payment automation or may have undocumented rate limits
- **Likelihood:** Medium (Wise API exists but capabilities unclear until validation)
- **Impact:** If API doesn't support required operations, must fall back to manual CSV upload (eliminates 30% of Phase 2 value)
- **Mitigation Strategy:** Schedule Wise API validation call within first week of project, test batch payment capabilities in sandbox before Phase 2 commitment
- **Fallback Plan:** Generate CSV export for manual Wise upload (user still saves time via validation, loses batch automation benefit)
- **Owner:** Tech lead to validate API within Week 1

[Continue for 2-3 high risks]

---

### Medium Risk Components

[3-4 medium risks with same detailed structure]

---

### Low Risk Components

[Brief list of 3-5 low risks]

---

## Technical Dependencies

[Infrastructure table with costs]

### API Access Requirements

**Google Sheets API:**
- Authentication: OAuth2 with service account (recommended) or user OAuth
- Permissions needed: https://www.googleapis.com/auth/spreadsheets scope (read/write)
- Rate limits: 300 requests/minute per project, 100 requests/100 seconds per user
- Documentation: Excellent (Google developer docs are comprehensive)
- Known limitations: onEdit triggers only work via Apps Script (not external webhook), must poll for changes or use Apps Script intermediary

[Continue for 3-5 more APIs with detailed breakdown]

---

## Effort Summary

### Phase 1: Quick Wins (Weeks 1-6)

| Component | Effort | Complexity | Dependencies |
|-----------|--------|------------|--------------|
| Rate Synchronization | 1-2 weeks | Low | None |
| Fathom Integration | 1 week | Low | Rate Sync |
| Dashboard Validation | 1-2 weeks | Low-Medium | Rate Sync |
| Calendar Reminders | 1-2 weeks | Low | Dashboard dates |
| **Total** | **4-7 weeks** | **Low-Medium** | **Sequential** |

[Continue for Phase 2 and Combined Timeline]

---

## Recommendations

[Strategic prioritization logic]

---

## Complexity Scoring Detail

**Overall Project Complexity:** 6.5/10

| Category | Score | Notes |
|----------|-------|-------|
| API Integrations | 4/10 | Google APIs well-documented, Wise unknown |
| Data Complexity | 6/10 | Multiple formats (invoices), rate edge cases |
| Business Logic | 7/10 | Many validation rules, 10% error detection target |
| UI/UX Requirements | 5/10 | Simple dashboard, approval workflow |
| Security Requirements | 6/10 | Financial data, payment triggers (no PII storage) |
| Integration Points | 7/10 | 5+ systems (Google Sheets ×3, Wise, Fathom, Discord) |
| Edge Case Handling | 8/10 | Invoice variability, rate complexities (overtime, holiday) |

**Confidence Level:** Medium
**Reasoning:** Core components (rate sync, Fathom) have high confidence. Invoice validation and Wise integration have moderate unknowns requiring validation. Overall 70% confidence until Week 1 discovery validates unknowns.

---

*Assessment created: 2026-01-28*
*Confidence level: Medium (needs Wise API validation and invoice format inventory)*
```

**Volume:** 2-3 sentences → 200-400 lines (8-12 components with full analysis)

---

### Roadmap Field (v1.0 vs v2.0)

**v1.0 Example:**
```
Phase 1 (1-2 weeks): Rate synchronization automation
Phase 2 (1 week): Fathom call recording integration
```

**v2.0 Structure:**
```markdown
## Executive Summary

**Total Investment:** €20,000-30,000
**Total Time Savings:** 20-25 hours/month
**Payback Period:** 8-14 months
**Implementation Duration:** 12-16 weeks (3-4 months)
**5-Year Value:** €131,800 (€28,400/year × 5 years - €30K investment)

---

## Phase Overview

```
Month 1-2: Quick Wins (Foundation)
├── Week 1-2: Rate Synchronization
├── Week 2-3: Fathom Call Recording
├── Week 3-4: Dashboard Validation Rules
└── Week 4-5: Calendar Reminder System
    └── Checkpoint: Week 6 review

Month 3-4: Invoice Validation (Core Automation)
├── Week 7-10: Invoice Parsing & Intake
├── Week 10-12: Cross-Reference Validation
├── Week 12-14: Error Flagging Dashboard
└── Week 14-16: Wise Payment Prep
    └── Checkpoint: Week 16 review

Month 5-6: Optimization & Scaling
├── Week 17-18: Admin Team Training
├── Week 19-20: Edge Case Handling
├── Week 21-22: Process Refinement
└── Week 23-24: Bold Move TV Discovery
    └── Checkpoint: Final review
```

---

## Month 1-2: Quick Wins (Foundation)

### Overview
**Investment:** €6,500
**Time Savings:** 5-7 hours/month (upon Phase 1 completion)
**Duration:** 4-6 weeks
**Risk Level:** Low

---

### Week 1-2: Rate Synchronization Automation

**Investment:** €2,000-3,000
**Time Savings:** 2.5 hours/month (upon completion)

**Deliverables:**
- Team Directory configured as authoritative source with validation rules
- n8n workflow: onEdit trigger → change detection → API sync to FCA and Dashboard
- Audit trail: Change log showing all rate updates with timestamps and user attribution
- Error handling: Retry logic + Discord alerts for failed syncs
- Documentation: Setup guide, troubleshooting runbook for admin team

**Success Criteria:**
- [ ] Zero manual updates required after Team Directory rate change (100% auto-sync)
- [ ] Sync completes within 5 minutes of Team Directory update
- [ ] Zero rate discrepancies between sheets (verified via weekly audit script)
- [ ] Leonor reports workflow improved ("single update, done")
- [ ] Admin team trained and comfortable with new process

**Dependencies:**
- **Requires:**
  - Access to Team Directory, FCA, Dashboard sheets (Owner: Sindbad, ETA: Week 1 Day 1)
  - Google Sheets API OAuth2 setup (Owner: Dev team, ETA: Week 1 Day 2)
  - n8n/Make.com platform provisioned (Owner: Dev team, ETA: Week 1 Day 1)
- **Provides to next step:**
  - Clean rate data in FCA (enables Dashboard validation accuracy)
  - Change detection pattern (reusable for Fathom integration)
- **External dependencies:**
  - Admin team availability for schema walkthrough (2-hour session, Week 1)

**Risks:**
- Formula dependencies in FCA/Dashboard may break if sync approach is naive → Mitigation: Schema analysis first, test in sandbox sheet
- Admin team may resist new workflow if training insufficient → Mitigation: 1-hour hands-on training, 2-week parallel manual process

**Team Involvement:**
- Leonor: 2 hours for schema walkthrough, 1 hour for training
- Madalena: 1 hour for technical validation, 1 hour for training
- Sindbad: 30 min for approval checkpoint

[Continue for Weeks 2-3, 3-4, 4-5 with same 50-80 line detailed structure]

---

### Phase 1 Checkpoint: Week 6

**Checkpoint Meeting Agenda:**
1. Rate sync adoption review - Leonor feedback on workflow satisfaction (Target: 8/10+ satisfaction)
2. Error rate measurement - Compare pre/post discrepancy frequency (Target: Zero discrepancies in 4-week period)
3. Time savings validation - Admin team logs actual time saved (Target: 5-7 hrs/month confirmed)
4. Technical stability assessment - Review error logs and uptime (Target: 99%+ uptime, <3 failed syncs)
5. Go/No-Go Decision for Phase 2 - Based on criteria below

**Expected Outcomes:**
- **Zero rate discrepancies** achieved across all 3 sheets
- **5-7 hours/month time savings** confirmed by admin team logs
- **Admin team satisfaction** at 8/10 or higher
- **System uptime** at 99%+ with no critical failures

**Decision Criteria for Phase 2:**
- ✅ Quick wins delivered value (time savings ≥5 hrs/month confirmed)
- ✅ Admin team adoption successful (Leonor actively uses new workflow)
- ✅ No major technical issues (system stable for 4 consecutive weeks)
- ✅ Budget approved for Phase 2 (Sindbad + Pierre agreement secured)

**If Not Ready for Phase 2:**
- **Remediation Option 1:** Extend Phase 1 by 2 weeks to address adoption issues or technical bugs
- **Remediation Option 2:** Pause for 1 month to secure Phase 2 budget (admin team continues using Phase 1 tools)
- **Remediation Option 3:** Pivot to alternative Phase 2 scope if invoice validation deemed too risky

[Continue for Month 3-4 and Month 5-6 with same week-by-week structure]

---

## Timeline Summary

### Best Case Scenario
| Phase | Duration | Deliverables | Value |
|-------|----------|--------------|-------|
| Phase 1 | 4 weeks | 4 Quick Wins | €12,000/year |
| Phase 2 | 9 weeks | Invoice automation | €16,000/year |
| Phase 3 | - | N/A | N/A |
| **Total** | **13 weeks** | **8 components** | **€28,000/year** |

[Continue for Expected and Worst case scenarios]

---

## Risk Mitigation Timeline

### Month 1 Risks
- **Week 1:** Schema complexity risk - Mitigation: 2-hour deep dive with admin team - Owner: Tech lead
- **Week 2:** Formula dependency risk - Mitigation: Sandbox testing before production - Owner: Dev team
[Continue for all weeks]

---

## Success Metrics by Phase

### Phase 1 Success Metrics

**Quantitative:**
- **Rate discrepancies:** Baseline 1 per 3 months → Target 0 discrepancies (100% reduction)
- **Admin verification time:** Baseline 2.5 hrs/month → Target 0 hrs/month (100% elimination)
- **Sync success rate:** Baseline N/A → Target 99%+ (automated reliability)

**Qualitative:**
- **Admin satisfaction:** Leonor reports "single update, done" workflow improvement
- **Error anxiety:** Leonor reports reduced fear of "opening me up to a lot of error"

**Leading Indicators** (Week 3 check-in):
- First 2 weeks: 100% sync success rate should be achieved
- Leonor should report using new workflow for all rate updates (no manual fallback)

[Continue for Phase 2 and Phase 3]

---

## Resource Allocation

[Development hours table]
[Client resources table]

---

## Change Management

[Training plans per phase]
[Ongoing support model]

---

*Roadmap created: 2026-01-28*
*Status: Draft*
*Next update: After discovery completion*
```

**Volume:** 2 sentences → 200-400 lines (week-by-week breakdown with checkpoints and metrics)

---

## Implementation Approach

### Deployment Steps

1. **Update n8n workflow nodes** with v2.0 prompts:
   - Replace "Call AI for Analysis" node prompt with v2.0 Client Insights prompt
   - Replace "Call AI for Performance" node prompt with v2.0 Performance Analysis prompt

2. **Test with Leonor transcript** (test case from leonor_transcript_test_expectations_v1.0_2026-01-28.md):
   - Run workflow with Leonor transcript
   - Validate output depth matches expectations (200-800+ lines per field)
   - Check that transcript line number citations are included
   - Verify formulas show step-by-step calculations
   - Confirm ASCII diagrams render properly

3. **Adjust token limits** if needed:
   - v2.0 prompts will generate 10-15K tokens per analysis (vs ~500 tokens in v1.0)
   - May need to increase GPT-4o max tokens setting in n8n node
   - Monitor for completion token limits

4. **Validate Airtable population:**
   - Ensure Airtable cells can handle large markdown content (long text fields)
   - Check that formatting (markdown, tables, diagrams) displays correctly
   - Verify no truncation occurs

5. **Production rollout:**
   - Test with 1-2 additional transcripts
   - Monitor for quality consistency
   - Gather Sway feedback on output usefulness
   - Iterate on prompt refinements based on edge cases

---

## Expected Output Quality

### Client Insights Analysis (v2.0)

**pain_points field example:**
```
Total lines: 350
Structure:
- Pain Point 1: Manual Rate Synchronization (80 lines)
  - Current Workflow (12 steps with 20 lines)
  - Time Cost (15 lines with formula)
  - Error Scenarios (25 lines with 3 examples)
  - User Quotes (5 quotes with context, 15 lines)
  - Downstream Impact (10 lines)
  - ASCII workflow diagram (15 lines)
- Pain Point 2: Onboarding Sheet Avoidance (70 lines)
  [Same structure]
- Pain Point 3: Sanitization Coordination (65 lines)
  [Same structure]
- Upstream/Downstream Data Flow Diagram (70 lines)
- Error Cascade Examples (35 lines)
- Why Fixing Upstream Matters (30 lines with comparison table)
```

**key_insights field example:**
```
Total lines: 750
Structure:
- One-Liner (3 lines)
- Critical Pain Points (150 lines)
- Upstream/Downstream Data Flow Diagram (80 lines)
- Business Impact (120 lines with metrics)
- ROI Calculation (100 lines with step-by-step formulas)
- Critical Insight: Budget Gap (60 lines)
- The "Aha Moment" (50 lines)
- Critical Discovery Decisions (40 lines)
- Technical Feasibility (50 lines)
- Business Context (60 lines)
- Next Steps Requirements (40 lines)
- Key Quotes for Proposals (50 lines with 10-15 quotes)
```

**pricing_strategy field example:**
```
Total lines: 550
Structure:
- Executive Summary (10 lines)
- Pricing Insights from Discovery (40 lines)
- Budget Context (30 lines)
- Decision Makers (20 lines)
- Value Anchor Points (100 lines with formulas)
- Critical Budget Insight (50 lines)
- Pricing Options (200 lines: A/B/C with full details)
- Recommended Pricing (50 lines)
- Comparison Table (20 lines)
- Objection Handling (40 lines)
```

---

### Performance Analysis (v2.0)

**complexity_assessment field example:**
```
Total lines: 380
Structure:
- Complexity Overview (30 lines with table)
- Component 1: Rate Synchronization (40 lines)
- Component 2: Fathom Integration (35 lines)
- Component 3: Dashboard Validation (40 lines)
- Component 4: Calendar Reminders (35 lines)
- Component 5: Invoice Parsing (45 lines)
- Component 6: Invoice Validation (50 lines)
- Component 7: Error Flagging UI (40 lines)
- Component 8: Wise Integration (45 lines)
- Risk Assessment (50 lines: High/Medium/Low categories)
- Technical Dependencies (30 lines with tables)
- Effort Summary (40 lines with phase breakdowns)
- Recommendations (30 lines)
- Complexity Scoring Detail (20 lines with category scores)
```

**roadmap field example:**
```
Total lines: 420
Structure:
- Executive Summary (15 lines with totals)
- Phase Overview (30 lines with ASCII tree)
- Month 1-2: Quick Wins (150 lines)
  - Week 1-2: Component 1 (35 lines with deliverables, success criteria, dependencies)
  - Week 2-3: Component 2 (35 lines)
  - Week 3-4: Component 3 (35 lines)
  - Week 4-5: Component 4 (35 lines)
  - Phase 1 Checkpoint (30 lines)
- Month 3-4: Core Implementation (140 lines)
  [Same week-by-week structure]
- Month 5-6: Optimization (80 lines)
  [Same structure]
- Timeline Summary (30 lines with best/expected/worst tables)
- Risk Mitigation Timeline (30 lines)
- Success Metrics by Phase (40 lines)
- Resource Allocation (20 lines)
- Change Management (20 lines)
```

**call_quality_notes field example:**
```
Total lines: 180
Structure:
- Call Overview (15 lines)
- What Went Well (60 lines)
  - Quantification Quality (15 lines with examples)
  - Engagement Level (15 lines with indicators)
  - Requirements Clarity (15 lines with strengths)
  - Buying Signals (15 lines with quotes)
- What Needs Improvement (40 lines)
  - Missing Quantification (15 lines with coaching)
  - Budget Qualification Gap (15 lines with coaching)
  - [Other gaps] (10 lines)
- Client Readiness Assessment (30 lines)
  - Technical Maturity (10 lines)
  - Decision-Making Clarity (10 lines)
  - Urgency Level (10 lines)
- Competitive Intelligence (15 lines)
- Recommended Next Steps (20 lines)
- Proposal Strategy (20 lines)
- Overall Assessment (20 lines with score breakdown)
- Coaching Summary (10 lines)
```

---

## Validation Checklist

**Before marking as complete:**

- [x] v2.0 Client Insights prompt created at `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/fathom_client_insights_prompt_bps_v2.0_2026-01-28.md`
- [x] v2.0 Performance Analysis prompt created at `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/fathom_performance_analysis_prompt_bps_v2.0_2026-01-28.md`
- [x] Both prompts maintain BPS structure (Role, Task, Specifics, Context, Examples, Notes)
- [x] Both prompts instruct for 200-800+ line comprehensive analysis
- [x] Both prompts include ASCII diagram instructions
- [x] Both prompts include step-by-step formula calculation instructions
- [x] Both prompts include transcript line number citation requirements
- [x] Both prompts maintain JSON output format (no breaking changes to field names/structure)
- [ ] Deploy to n8n workflow (Task #11)
- [ ] Test with Leonor transcript (Task #10 continuation)
- [ ] Validate Airtable population (Task #12)

**Next steps:**
1. Update n8n workflow nodes with v2.0 prompts
2. Test with Leonor transcript
3. Validate output depth and quality
4. Adjust if needed
5. Deploy to production

---

*Summary created: 2026-01-28*
*Status: Prompts ready for deployment*
*Estimated deployment time: 30 minutes (update n8n nodes + test)*
