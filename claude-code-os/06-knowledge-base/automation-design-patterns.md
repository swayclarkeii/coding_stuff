# Automation Design Patterns

Reusable technical patterns for automation solutions.

---

## Pattern: Payment Reconciliation Automation

**Use Case:** Bold Move TV / Ambushed - Jan 8, 2026

### Business Problem
- Manual review of 15-20 invoices per week
- 5-6 hours/week spent on reconciliation
- 10% error rate (wrong rates, missing projects, excessive hours)
- Weekly processing required for cash flow
- Quality control needed (second set of eyes)

### Current Workflow
```
1. Admin team enters data → Google Sheets dashboard
   - Project name, client, freelancer, hours, rates
   - Monthly tabs with all projects

2. Weekly: Sindbad reviews dashboard
   - Checks hours against projects
   - Verifies rates match agreements
   - Confirms project codes correct
   - Calculates payment window (3-4 weeks from invoice)

3. Manual payment via Wise
   - 15-20 individual payments per week
   - Cross-reference invoice with dashboard
   - Enter payment details manually
```

**Total time:** 5-6 hours/week = 20-24 hours/month

### Automation Architecture

#### Phase 1: Automated Quality Control
```javascript
Google Sheets → AI Validation Engine → Exception Report

Components:
1. Google Sheets API integration
2. Business rules engine:
   - Rate validation (check against freelancer contracts)
   - Hours validation (flag if >X hours for project type)
   - Project code validation (ensure project exists in invoice system)
   - Duplicate detection (same person/project multiple entries)

3. Exception flagging system:
   - Green: All validations passed
   - Yellow: Minor discrepancy (review suggested)
   - Red: Major error (must fix before payment)

4. Weekly email digest:
   - Summary of all invoices ready for payment
   - List of exceptions requiring attention
   - Total payment amount for week
```

**Time saved:** 4-5 hours/week (checking), leaves 1 hour for exception review and payment execution

#### Phase 2: Human-in-the-Loop Payment
```javascript
Exception Review → Sindbad Approval → Batch Payment API

Components:
1. Approval dashboard:
   - Shows all validated invoices (green)
   - Shows flagged exceptions (yellow/red)
   - One-click approval for clean batch
   - Quick fix interface for exceptions

2. Wise API integration:
   - Bulk payment CSV upload
   - Auto-populate from approved invoices
   - Execution on Sindbad's approval

3. Audit trail:
   - Every approval logged
   - Every exception resolution documented
   - Payment confirmation stored
```

**Time saved:** Additional 30-45 minutes/week (payment execution)

**Total time after automation:** 15-30 minutes/week = 1-2 hours/month
**Time savings:** 18-23 hours/month (90%+ reduction)

### Technical Stack
- **Data source:** Google Sheets API
- **Backend:** n8n workflows or custom Python
- **Validation:** Rule engine with freelancer contract database
- **Payments:** Wise API (batch payment capability)
- **UI:** Simple approval dashboard (web-based)
- **Notifications:** Email digest + exception alerts

### Implementation Considerations

**Must have:**
- Human approval checkpoint (Sindbad requirement)
- Error flagging before payment (quality control)
- Cash flow timing preserved (weekly processing)
- Audit trail for all payments

**Nice to have:**
- Mobile approval capability
- SMS alerts for high-value exceptions
- Trend analysis (frequent errors by project/freelancer)
- Admin team feedback on data quality

**Risk mitigation:**
- Pilot with 1-2 weeks of data before full deployment
- Parallel run (manual + automated) for first month
- Easy rollback to manual process
- Admin team training on exception handling

---

## Pattern: Lead Tracking and Reactivation System

**Use Case:** Bold Move TV - Jan 8, 2026

### Business Problem
- No systematic lead tracking
- Warm leads going cold (people who showed interest then ghosted)
- Manual email review to find opportunities
- Unknown drop-off points in sales conversations
- Limited sales capacity (1 meeting in 3 months from employee)
- Concerned about being "annoying" with automated outreach

### Current State
- Manual Google Sheets "Request Tracker"
- Categories: waiting on client, ghosted, canceled
- No automated email parsing
- No reactivation workflow

### Automation Architecture

#### Phase 1: Automated Lead Capture
```javascript
Gmail API → Lead Parser → CRM Database

Components:
1. Gmail integration:
   - Monitor sindbad@boldmove.tv inbox
   - Identify inbound inquiries (subject lines, keywords)
   - Extract contact info, project details, budget signals

2. Lead categorization AI:
   - New inquiry vs. existing conversation
   - Project type (film, TV, documentary)
   - Budget indicator (explicit mention or inferred)
   - Urgency level (timeline mentions)

3. Auto-populate CRM:
   - Contact record creation
   - Conversation thread linking
   - Timeline of all touchpoints
   - Current status classification
```

#### Phase 2: Drop-Off Analysis
```javascript
Conversation History → Pattern Analysis → Insight Report

Components:
1. Conversation stage detection:
   - Initial inquiry
   - Pricing shared
   - Examples/portfolio sent
   - Meeting scheduled/completed
   - Proposal sent
   - Ghosted/cold

2. Drop-off point identification:
   - Where in funnel did conversation stop?
   - What was last message sent?
   - What was their last response?
   - Time since last contact

3. Pattern insights:
   - Common drop-off points across leads
   - Messaging that correlates with ghost rate
   - Timeline factors (how long until ghost)
   - Project type or budget patterns
```

#### Phase 3: Tactical Reactivation (NOT Auto-Send)
```javascript
Warm Lead Database → Reactivation Suggestions → Manual Outreach

Components:
1. Lead scoring for reactivation:
   - Time since last contact (30-90 days = sweet spot)
   - Previous engagement level (high interest = higher priority)
   - Project alignment (do they fit Bold Move TV ideal customer?)
   - Reason for drop-off (price? timing? unclear?)

2. Message suggestions (NOT auto-send):
   - Contextual prompt: "Last spoke about [project], mentioned [concern]"
   - Suggested angle: "New case study relevant to their project"
   - CTA recommendation: Based on what worked historically

3. Manual review and send:
   - Sindbad reviews suggested leads
   - Edits/personalizes message
   - Sends manually (maintains authenticity)
   - System logs outcome for learning
```

**Key principle:** Automation provides intelligence, human maintains relationships

### Technical Stack
- **Email integration:** Gmail API
- **Lead database:** Lightweight CRM (HubSpot Free, Pipedrive, or custom Airtable)
- **AI parsing:** OpenAI API for conversation analysis
- **Workflow:** n8n for automation orchestration
- **UI:** CRM native interface or custom dashboard

### Design Constraints (Bold Move TV Specific)

**Must preserve:**
- Personal touch (no mass emails)
- Thoughtful approach (quality over quantity)
- Sindbad's control (he decides what to send)
- Relationship integrity (no risk of being "annoying")

**Must avoid:**
- Auto-sending emails
- Generic templates
- Aggressive follow-up sequences
- Anything that feels "spammy"

### Implementation Approach

**Week 1:** Gmail parsing and lead database setup
- Backfill historical leads from last 6-12 months
- Categorize by stage and status
- Build warm lead inventory

**Week 2:** Drop-off analysis and insights
- Identify patterns in successful vs. ghosted conversations
- Document messaging that works/doesn't work
- Create reactivation prioritization framework

**Week 3:** Pilot reactivation campaign
- Select 5-10 highest-priority warm leads
- Generate personalized message suggestions
- Sindbad reviews and sends manually
- Track response rates and booking conversions

**Week 4:** Refine and scale
- Adjust scoring based on pilot results
- Build sustainable weekly rhythm (5-10 reactivations/week)
- Integrate learnings into new lead handling

---

## Pattern: Quality Control as Automation Constraint

**Insight from:** Bold Move TV - Jan 8, 2026

### The Control Paradox
**Client wants:** Time savings from automation
**Client fears:** Loss of quality control and oversight

### Solution Framework: Progressive Trust Automation

#### Level 1: AI as Assistant (Low Risk)
```
Human does work → AI suggests improvements → Human approves
```
**Example:** Human writes email, AI suggests better subject line
**Trust required:** Minimal (human makes all decisions)
**Time savings:** 10-20% (efficiency gains)

#### Level 2: AI as Checker (Medium-Low Risk)
```
Human does work → AI validates → Flags exceptions → Human reviews
```
**Example:** Admin enters data, AI checks for errors, human fixes
**Trust required:** Low (AI just flags issues)
**Time savings:** 30-50% (less checking needed)

#### Level 3: AI as Executor with Approval (Medium Risk)
```
AI does work → Human reviews → Human approves → AI executes
```
**Example:** AI prepares payments, Sindbad approves, AI sends
**Trust required:** Medium (AI does work, human has veto)
**Time savings:** 70-90% (human only reviews, doesn't execute)
**This is where Bold Move TV payment system should start**

#### Level 4: AI as Executor with Exception-Only Review (Medium-High Risk)
```
AI does work → Auto-execute if clean → Flag exceptions → Human reviews exceptions only
```
**Example:** AI pays invoices automatically if all validations pass, flags outliers
**Trust required:** High (AI handles routine, human only sees problems)
**Time savings:** 90-95% (human touches very little)

#### Level 5: AI Fully Autonomous (High Risk)
```
AI does work → Auto-execute → Periodic audit by human
```
**Example:** AI handles all payments, Sindbad reviews monthly report
**Trust required:** Very high (AI operates independently)
**Time savings:** 95-99% (human rarely involved)
**Not recommended for high-stakes processes**

### Design Decision Tree

**Q1: What's the cost of an error?**
- High (money, reputation, legal) → Start Level 2-3, maybe progress to 4
- Medium → Start Level 3, can progress to 4-5
- Low → Can start Level 4-5

**Q2: How often do errors occur currently?**
- >10% → Start Level 2 (AI checker)
- 5-10% → Start Level 3 (AI executor with approval)
- <5% → Can start Level 4 (exception-only review)

**Q3: Client comfort with automation?**
- Skeptical → Start Level 1-2, build trust gradually
- Cautious → Start Level 3, pilot before expanding
- Enthusiastic → Can start Level 4

**For Bold Move TV payment system:**
- Error cost: **HIGH** (wrong payments damage freelancer relationships)
- Current error rate: **10%** (relatively high)
- Client comfort: **CAUTIOUS** (wants control)
- **Recommendation: Start Level 3, progress to Level 4 after 3-6 months of trust-building**

---

## Pattern: API Integration Assessment

**Tools observed in:** Bold Move TV - Jan 8, 2026

### Integration Checklist

#### Google Sheets
- **API:** ✅ Google Sheets API v4
- **Auth:** OAuth 2.0 or Service Account
- **Read:** Real-time access to all data
- **Write:** Programmatic updates to cells
- **Use case:** Payment dashboard data source
- **Complexity:** Low (well-documented, reliable)

#### Wise (Payment Platform)
- **API:** ✅ Wise API (formerly TransferWise)
- **Capability:** Batch payments, recipient management
- **Auth:** API key authentication
- **Use case:** Automated payment execution
- **Complexity:** Medium (financial API, security important)
- **Note:** Check if client has business account (required for API)

#### Gmail
- **API:** ✅ Gmail API
- **Read:** Email parsing, thread tracking
- **Send:** Programmatic email sending (use carefully)
- **Search:** Advanced queries for lead identification
- **Use case:** Lead capture and conversation analysis
- **Complexity:** Medium (OAuth, scope management)

### Integration Risk Assessment

**Before proposing API-based solution:**

1. **Does API exist?**
   - ✅ Yes → Continue assessment
   - ❌ No → Look for webhooks, CSV export, or alternative tools

2. **Is it publicly documented?**
   - ✅ Yes → Good
   - ⚠️ Limited → Request access from vendor
   - ❌ No → High risk, avoid if possible

3. **What's the authentication complexity?**
   - ✅ API key → Easy
   - ⚠️ OAuth 2.0 → Medium (manageable)
   - ❌ Complex enterprise auth → Difficult, may need IT involvement

4. **Are there rate limits?**
   - Check limits (requests per minute/hour/day)
   - Ensure client's volume fits within limits
   - Plan for rate limit handling in code

5. **Is there a cost?**
   - Free tier available? (e.g., Google APIs)
   - Pay-per-call? (budget implications)
   - Enterprise only? (may need account upgrade)

6. **What's the reliability?**
   - SLA available?
   - Uptime history?
   - What happens if API is down? (fallback plan)

---

## Pattern: Workflow Tools vs. Custom Code

**Decision framework from:** Bold Move TV - Jan 8, 2026

### When to Use n8n (or Similar No-Code/Low-Code Tools)

**Use n8n when:**
- ✅ Standard API integrations (Google, Wise, Gmail)
- ✅ Simple logic (if/then, filtering, routing)
- ✅ Client may want to modify later (visual editing)
- ✅ Fast prototyping needed (build in hours, not days)
- ✅ Budget constrained (faster = cheaper)

**Examples from Bold Move TV:**
- Gmail monitoring for new leads
- Google Sheets data validation rules
- Wise payment batch preparation
- Weekly summary email generation

### When to Use Custom Code (Python, Node.js, etc.)

**Use custom code when:**
- ✅ Complex business logic (error detection algorithms)
- ✅ Machine learning / AI analysis (conversation pattern detection)
- ✅ Performance critical (processing large datasets)
- ✅ Custom UI needed (approval dashboard)
- ✅ Advanced data transformations

**Examples from Bold Move TV:**
- Rate validation against historical freelancer contracts
- Lead scoring algorithm (ML-based prioritization)
- Conversation stage detection (NLP analysis)
- Custom approval dashboard for payment review

### Hybrid Approach (Best of Both)

**Pattern:**
```
n8n for orchestration + Custom code for complex logic

Example: Bold Move TV Payment System
- n8n: Monitors Google Sheets for new entries
- Custom Python: Validates rates against contract database
- n8n: Sends validation results to approval UI
- Custom dashboard: Sindbad reviews and approves
- n8n: Triggers Wise API batch payment
```

**Benefits:**
- Speed of n8n for standard integrations
- Power of custom code for complex logic
- Visual workflow for maintenance
- Scalable and flexible

---

**Knowledge Base Entry Created:** 2026-01-12
**Source:** Bold Move TV Discovery Call (Jan 8, 2026)
**Patterns Documented:** 6
**Next Review:** After implementation phase to validate patterns

---

*Technical patterns extracted for reusable application across automation projects*
