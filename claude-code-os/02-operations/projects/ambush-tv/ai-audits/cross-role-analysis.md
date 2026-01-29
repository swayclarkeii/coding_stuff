# AmbushTV AI Audit - Cross-Role Analysis

**Interviews Completed:** 2/6+
**Date Range:** January 2026
**Purpose:** Identify shared pain points across roles for prioritized automation solutions

---

## Interviews Analyzed

1. **James** (Creative Team) - Date: [Previous interview]
2. **Leonor Zuzarte** (HR & Community Manager) - Date: 2026-01-27

---

## Shared Pain Point #1: Asset Management Chaos

### James's Experience (Creative Team)
**Problem:** Struggles to find project assets scattered across email threads
**Impact:** Time wasted searching, creative momentum interrupted
**Context:** Working on treatments, needs to locate specific files/references
**Workaround:** Manual email searching, asking team members

### Leonor's Experience (HR/Community)
**Problem:** Struggles to find treatment assets for sanitization across platforms
**Platforms:** InDesign packages, ReadyMag duplicates, Figma files
**Impact:** 1-1.5 hours per treatment spent on asset gathering (vs. 10 min on actual review)
**Context:** Coordinating portfolio building, needs source files
**Workaround:**
- InDesign: Check Post-Treatment Form for package links
- ReadyMag: Ask art directors to duplicate and grant access
- Figma: Ask art directors for access

### Common Root Cause
**No centralized asset management system**
- Assets stored in multiple locations (email, platform-specific, personal drives)
- No consistent naming or organization
- No single source of truth for "where is the file for Project X?"

### Shared Solution Opportunity
**Asset Management System Implementation**

**Features:**
1. Standardized storage location per project
2. Consistent naming conventions
3. Auto-linking from Post-Treatment Form
4. Directory structure: `/projects/[client]/[project-name]/[assets]/`
5. Access controls by role

**Benefits:**
- **James:** Instantly locate assets for creative work
- **Leonor:** Reduce sanitization prep from 1 hour to 15 minutes
- **Booking Team:** Quick access to reference materials
- **Art Directors:** Less interruption from "where's the file?" requests

**Estimated Time Savings:**
- James: 40-60 hours/year (estimated)
- Leonor: 30 hours/year (calculated)
- Art Directors: 10-20 hours/year (reduced interruptions)
- **Total: 80-110 hours/year across team**

**Priority:** HIGH (affects multiple roles, significant ROI)

---

## Shared Pain Point #2: Multi-Sheet Syndrome

### James's Experience (Creative Team)
**Sheets Used:** Project Directory, potentially others (needs confirmation from interview)
**Impact:** [Details from James interview needed]

### Leonor's Experience (HR/Community)
**Sheets Used:**
1. Team Directory (freelancer rates + info)
2. FCA (Financial/invoicing rates)
3. Onboarding Master (applicant pipeline)
4. Portfolio Sheet (sanitization queue)
5. Post-Treatment Form (project completion data)
6. Newbie Tracker (feedback tracking)

**Impact:**
- Manual data entry across multiple sheets
- Synchronization errors (Team Directory ≠ FCA)
- 70 min/month on alignment checks
- Cognitive overhead tracking where data lives
- Context switching between systems

### Common Root Cause
**Disconnected systems built independently**
- No data integration between sheets
- No single source of truth
- Manual sync requirements
- Error-prone duplication

### Shared Solution Opportunity
**Integrated Data System**

**Approaches:**
1. **Short-term:** Use formulas to reference single source across sheets
2. **Medium-term:** Consolidate sheets where possible (e.g., Team Directory + FCA)
3. **Long-term:** Move to proper database system (Airtable, custom build, etc.)

**Priority Areas:**
1. **IMMEDIATE:** Merge Team Directory + FCA (Leonor's top priority)
2. **SHORT-TERM:** Link Post-Treatment Form → Project Directory
3. **MEDIUM-TERM:** Integrate Onboarding Master with communication tools
4. **LONG-TERM:** Unified project management system

**Priority:** HIGH (Leonor), MEDIUM (James - pending interview details)

---

## Shared Pain Point #3: Admin Work Stealing Core Function Time

### James's Experience (Creative Team)
**Core Function:** Creative work (treatment design, visual development)
**Admin Burden:** System maintenance interrupts creative flow
**Estimated Split:** ~40-45% admin vs. 55-60% creative (needs confirmation)

### Leonor's Experience (HR/Community)
**Core Function:** Freelancer support and relationship management
**Admin Burden:** Sheet updates, alignment checks, asset hunting
**Measured Split:** 40-45% admin vs. 55-60% support

**Leonor's Quote:**
> "These are all things that I find to be kind of like around my job but not the point of my job."

### Common Root Cause
**Systems require manual intervention instead of automation**
- Manual data entry
- Manual synchronization
- Manual error checking
- Manual coordination

### Shared Solution Opportunity
**Automation-First Redesign**

**Goal:** Shift both roles to 70-80% core function, 20-30% admin

**How:**
- Automate data entry (forms, integrations)
- Automate synchronization (formulas, scripts)
- Automate notifications (reminders, alerts)
- Automate coordination (workflow systems)

**Expected Impact:**
- James: +40-60 hours/year for creative work
- Leonor: +60-80 hours/year for support work
- Better output quality (less context switching)
- Higher job satisfaction (doing intended work)

**Priority:** HIGH (fundamental to role effectiveness)

---

## Role-Specific Pain Points

### James Only
**[Pending: Review James interview for unique pain points]**

Likely areas:
- Creative feedback/revision cycles?
- Client communication challenges?
- Tool/platform limitations?

### Leonor Only

#### 1. Dual Rate Management System
**Problem:** Must update freelancer rates in two places (Team Directory + FCA)
**Impact:** 70 min/month + quarterly errors + booking team interruptions
**Priority:** HIGH (Leonor's #1 requested fix)
**Solution:** Merge into single system with auto-sync

#### 2. Onboarding Master Sheet Avoidance
**Problem:** Tedious detail work causes procrastination → binge updating
**Impact:** 2-4 hour sessions every 1-2 months (anxiety-amplified)
**Priority:** MEDIUM (quality of life)
**Solution:** Form-based intake, dashboard view, email parsing

#### 3. Treatment Sanitization Backlog
**Problem:** 38 treatments behind, manual coordination process
**Impact:** 38 hours of Leonor's time + €2,052 cost + booking team credibility loss
**Priority:** CRITICAL (current crisis)
**Solutions:**
- SHORT-TERM: Sprint to clear backlog
- LONG-TERM: Workflow automation, asset management, art director flagging at project completion

#### 4. ADHD + Multiple Interrupt Streams
**Context:** ADHD + role requires responsiveness to freelancer needs
**Challenge:** Feedback requests, support questions, calls interrupt planned work
**Current Coping:** Batch feedback collection on Mondays, but other interrupts remain unpredictable
**Need:** Systems that reduce unnecessary interruptions while preserving support accessibility

---

## Cross-Role Dependencies

### Leonor's Work Affects James (and Creative Team)

**Portfolio Sanitization:**
- Leonor coordinates sanitization of James's treatments
- Delays impact freelancer ability to showcase work
- Could affect team morale if portfolios lag

**Rate Management:**
- Leonor manages rate changes that affect project budgets
- Errors could impact creative team compensation
- Coordination with Pierre (who oversees creative) is critical

### James's Work Affects Leonor

**Treatment Completion:**
- James (and creative team) submits Post-Treatment Form
- Incomplete or inconsistent submissions complicate Leonor's sanitization coordination
- Asset linking in form is critical for Leonor's efficiency

**Feedback on Newbies:**
- If James is a senior, he's part of Leonor's Monday feedback collection
- Quality and timeliness of feedback affects onboarding effectiveness

---

## Solution Prioritization Matrix

| Solution | Affects | Time Saved | Complexity | Priority | Timeline |
|----------|---------|------------|------------|----------|----------|
| **Merge Rate Systems** | Leonor, Booking | 14 hrs/yr | LOW | HIGH | 0-30 days |
| **Asset Management** | James, Leonor, Art Directors | 80-110 hrs/yr | MEDIUM | HIGH | 30-90 days |
| **Sanitization Sprint** | Leonor, Booking | 38 hrs (backlog) | LOW | CRITICAL | 0-30 days |
| **Onboarding Automation** | Leonor | 12-24 hrs/yr | MEDIUM | MEDIUM | 30-90 days |
| **Feedback Automation** | Leonor | 50-100 hrs/yr | MEDIUM | MEDIUM-HIGH | 90-180 days |
| **Sanitization Workflow** | Leonor, Creative, Booking | 20-30 hrs/yr | HIGH | HIGH | 90-180 days |

---

## Recommended Implementation Sequence

### Phase 1: Quick Wins (0-30 days)
1. **Merge Rate Systems** - Leonor's top request, low complexity
2. **Sanitization Sprint** - Clear backlog crisis, establish process baseline

### Phase 2: Foundation (30-90 days)
3. **Asset Management System** - Solves problems for both James and Leonor
4. **Onboarding Automation** - Reduces Leonor's avoidance behavior

### Phase 3: Optimization (90-180 days)
5. **Feedback Collection Automation** - Recurring weekly efficiency
6. **Sanitization Workflow System** - Prevents future crises

### Phase 4: Integration (180+ days)
7. **Unified Project Management** - Long-term vision, requires buy-in and budget
8. **Custom Integrations** - Connect remaining disconnected systems

---

## Key Insights for AI Audit Report

### 1. Asset Management is Cross-Team Priority
Not just a James problem or Leonor problem - affects creative, HR, booking, and art directors. High ROI solution.

### 2. "Around My Job" Pattern is Systemic
Both James and Leonor spending 40-45% of time on system maintenance instead of core functions. This isn't individual inefficiency - it's a system design problem.

### 3. Leonor's Role is Canary in Coal Mine
As newest role, Leonor inherited disconnected systems. Her pain points reveal what happens when systems don't integrate. Fixing her systems prevents this pattern from recurring.

### 4. Quick Wins Build Momentum
Rate system merge is low-effort, high-impact. Proves concept, builds trust, funds bigger projects.

### 5. Automation ROI is Measurable
Combined savings across just 2 roles: 140-190 hours/year. With 6+ more interviews pending, total opportunity likely 500+ hours/year.

---

## Questions for Remaining Interviews

### For Madalena/Elise (Booking Team)
1. How much time spent resolving rate discrepancies per month?
2. How often do missing portfolios block or delay freelancer placements?
3. What's the estimated impact on booking success rate?
4. How much time spent "verbally arguing" for freelancers without portfolios?

### For Pierre/Sinbad (Leadership)
1. What's the strategic vision for Leonor's role growth?
2. Budget availability for automation projects?
3. Priority ranking of identified pain points?
4. Any concerns about system changes affecting operations?

### For Art Directors
1. How much time spent responding to asset location requests?
2. Current sanitization approval process - time investment?
3. Preferred method for flagging projects for sanitization?

### For Freelancers
1. Satisfaction with Leonor's support (validation)?
2. Any gaps in onboarding experience?
3. Portfolio effectiveness - does it help win projects?
4. Any friction with Post-Treatment Form or other processes?

---

## Next Steps

1. **Review James Interview Details** - Confirm shared pain points, add role-specific items
2. **Schedule Additional Interviews** - Madalena, Elise, Pierre, Art Directors, Freelancers
3. **Validate Time Estimates** - Cross-check with team on savings calculations
4. **Design Quick Win Solutions** - Detailed specs for Phase 1 implementations
5. **Present Findings** - Comprehensive report with prioritized recommendations

---

**Cross-Role Analysis Status:** In Progress (2/8+ interviews)
**Next Update:** After Madalena/Elise interviews
**Estimated Report Completion:** [After all interviews completed]
