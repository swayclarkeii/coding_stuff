# Ambush TV - Build Complexity Assessment

**Created:** 2026-01-18
**Source:** 5 Discovery Transcripts (Jan 8 & Jan 15, 2026)
**Purpose:** Evaluate technical complexity for accurate scoping and pricing

---

## Complexity Overview

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

**Overall Project Complexity:** Medium-High

---

## Component Analysis

### 1. Rate Synchronization Automation

**Complexity: Low**

**What It Does:**
- Watch Team Directory for rate changes
- Auto-update FCA sheet when rate changes
- Auto-update Dashboard formulas/references
- Create audit trail of changes

**Technical Requirements:**
- Google Sheets API (well-documented)
- n8n/Make.com workflow
- Trigger: onEdit or scheduled polling
- Data mapping between 3 sheets

**Why It's Low Complexity:**
- Single data type (rates)
- Clear source of truth (Team Directory)
- Standard CRUD operations
- No external APIs beyond Google
- Well-defined data schema

**Known Unknowns:**
- Exact schema of Team Directory rate column
- Formula dependencies in FCA/Dashboard
- Edge cases: currency changes, retroactive rates

**Effort Estimate:** 1-2 weeks
**Confidence Level:** High

---

### 2. Fathom Call Recording Integration

**Complexity: Low**

**What It Does:**
- Post-call webhook trigger from Fathom
- Extract transcript and summary
- Parse for rate change mentions
- Send summary to Discord/Email
- Optionally trigger rate sync

**Technical Requirements:**
- Fathom API/webhooks
- n8n/Make.com workflow
- Text parsing (regex or AI)
- Discord webhook or Gmail API

**Why It's Low Complexity:**
- Fathom provides structured output
- One-way data flow (Fathom → notification)
- No state management required
- Well-documented Discord webhooks

**Known Unknowns:**
- Fathom webhook capabilities (vs polling)
- Rate mention parsing accuracy
- Leonor's adoption willingness

**Effort Estimate:** 1 week
**Confidence Level:** High

---

### 3. Dashboard Validation Rules

**Complexity: Low-Medium**

**What It Does:**
- Validate data on entry in Dashboard
- Check rates against FCA master
- Flag missing project entries
- Warn on hours thresholds (>10hr, >12hr)
- Detect duplicate entries
- Visual indicators (colors, warnings)

**Technical Requirements:**
- Google Apps Script (native)
- Conditional formatting
- onEdit triggers
- Notification system (email/Discord)

**Why It's Low-Medium Complexity:**
- Google Apps Script is straightforward
- Validation logic is rule-based
- BUT: Dashboard structure is complex
- Multiple tabs, interdependencies
- Risk of breaking existing formulas

**Known Unknowns:**
- Full Dashboard schema
- Existing formulas and dependencies
- Edge cases in rate validation
- Hours threshold business rules

**Effort Estimate:** 1-2 weeks
**Confidence Level:** Medium

---

### 4. Calendar Reminder System

**Complexity: Low**

**What It Does:**
- Read project dates from Dashboard/Calendar
- Trigger 4-day reminder (collect hours)
- Trigger 7-day reminder (send invoice)
- Send to Discord channel or email
- Handle date changes gracefully

**Technical Requirements:**
- Google Calendar API (or Sheets dates)
- n8n/Make.com scheduled workflow
- Discord webhook or Gmail API
- Date arithmetic

**Why It's Low Complexity:**
- Simple date-based logic
- One-way notification flow
- No complex state management
- Well-documented APIs

**Known Unknowns:**
- Project date source (Calendar vs Dashboard)
- Date change handling
- Reminder recipient logic
- Snooze/dismiss requirements

**Effort Estimate:** 1-2 weeks
**Confidence Level:** High

---

### 5. Invoice Parsing & Intake

**Complexity: Medium**

**What It Does:**
- Monitor Gmail for invoice emails
- Parse invoice attachments (Google Docs, PDF)
- Extract: freelancer name, project, hours, rate, total
- Handle multiple invoice formats
- Create structured data record

**Technical Requirements:**
- Gmail API (email monitoring)
- Google Docs API (document parsing)
- OCR for PDFs (if needed)
- AI/regex for data extraction
- Error handling for malformed invoices

**Why It's Medium Complexity:**
- Multiple invoice formats (freelancer variability)
- Document parsing is imperfect
- Need high accuracy (financial data)
- Edge cases: multiple projects per invoice
- Potential OCR complexity

**Known Unknowns:**
- Number of invoice formats in use
- Freelancer compliance with templates
- PDF vs Google Docs ratio
- Email vs attachment submission

**Effort Estimate:** 3-4 weeks
**Confidence Level:** Medium

---

### 6. Invoice Validation Logic

**Complexity: Medium-High**

**What It Does:**
- Compare invoice data to Dashboard
- Validate: project exists, rate matches, hours reasonable
- Flag discrepancies with categorization
- Handle edge cases (multiple projects, split invoices)
- Maintain 10%+ error detection rate

**Technical Requirements:**
- Cross-reference logic (invoice ↔ Dashboard)
- Fuzzy matching (project names, freelancer names)
- Threshold logic (hours, rates, totals)
- Error categorization system
- Historical comparison (previous invoices)

**Why It's Medium-High Complexity:**
- Many validation rules needed
- Fuzzy matching for inconsistent naming
- Edge cases: overtime, weekend rates, holiday rates
- Need to match/exceed Sindbad's 10% error detection
- False positive management

**Known Unknowns:**
- Full list of error types Sindbad catches
- Rate edge cases (holiday, weekend, overtime)
- Project naming consistency
- Multi-project invoice handling

**Effort Estimate:** 2-3 weeks
**Confidence Level:** Medium

---

### 7. Error Flagging Dashboard

**Complexity: Medium**

**What It Does:**
- Display flagged invoices to Sindbad
- Show error details and original invoice
- Approve/Reject/Edit workflow
- Update validation status
- Generate weekly summary reports

**Technical Requirements:**
- Web interface or Google Sheets dashboard
- State management (pending, approved, rejected)
- User authentication (if web)
- Notification system
- Audit trail

**Why It's Medium Complexity:**
- UI/UX design required
- State management across sessions
- Integration with validation logic
- Needs to be intuitive for Sindbad
- Report generation

**Known Unknowns:**
- Sindbad's preferred interface (web vs Sheets)
- Mobile access requirements
- Edit workflow complexity
- Bulk approval needs

**Effort Estimate:** 2-3 weeks
**Confidence Level:** Medium

---

### 8. Wise Payment Integration

**Complexity: Medium-High**

**What It Does:**
- Generate batch payment files
- Integrate with Wise API (if available)
- Prepare payments from approved invoices
- Handle payment failures
- Reconciliation with bank statements

**Technical Requirements:**
- Wise API integration
- Payment file format (CSV or API)
- Error handling for failed payments
- Reconciliation logic
- Security considerations

**Why It's Medium-High Complexity:**
- Financial transactions (high stakes)
- API limitations unknown
- Security requirements
- Rollback complexity
- Reconciliation accuracy

**Known Unknowns:**
- Wise API capabilities and limits
- Batch payment format requirements
- Authentication and security
- Payment failure handling
- Reconciliation data availability

**Effort Estimate:** 2-3 weeks
**Confidence Level:** Low (needs API validation)

---

## Risk Assessment

### High Risk Components

**1. Wise API Integration**
- **Risk:** API may not support all required operations
- **Impact:** May need manual payment trigger instead of full automation
- **Mitigation:** Validate API capabilities before Phase 2 commitment
- **Fallback:** CSV export for manual batch upload

**2. Invoice Format Variability**
- **Risk:** Freelancers use many different formats
- **Impact:** Parsing accuracy may be <95%
- **Mitigation:** Start with template standardization push
- **Fallback:** Manual review for non-standard formats

---

### Medium Risk Components

**3. Google Sheets Structural Changes**
- **Risk:** Admin team modifies sheet structure
- **Impact:** Automations break
- **Mitigation:** Version control, schema documentation, alerts
- **Fallback:** Quick fix deployments, manual backup

**4. Rate Complexity**
- **Risk:** Weekend, overtime, holiday rates create edge cases
- **Impact:** Validation accuracy drops
- **Mitigation:** Thorough edge case documentation
- **Fallback:** Human review for complex rate scenarios

---

### Low Risk Components

**5. API Availability**
- All core tools (Google, Discord, Fathom) have documented APIs
- n8n/Make.com has existing integrations
- Low risk of API changes breaking integrations

**6. Team Adoption**
- Admin team actively requested these improvements
- Sindbad bought into human-in-the-loop approach
- Low risk of resistance

---

## Technical Dependencies

### Required Infrastructure
| Component | Cost | Setup Time |
|-----------|------|------------|
| n8n Cloud | €20/month | 1 day |
| OR Make.com | €9/month | 1 day |
| Google Workspace API | Free (existing) | 1 day |
| Fathom | Free tier | 1 hour |
| Discord Webhook | Free | 1 hour |

### API Access Requirements
- **Google Sheets API:** OAuth2, read/write access to specific sheets
- **Google Calendar API:** OAuth2, read access to calendars
- **Gmail API:** OAuth2, read access to specific labels
- **Discord API:** Webhook (no OAuth needed)
- **Fathom API:** API key (to be validated)
- **Wise API:** API key + OAuth2 (to be validated)

---

## Effort Summary

### Phase 1: Quick Wins (Weeks 1-6)
| Component | Effort | Complexity |
|-----------|--------|------------|
| Rate Sync | 1-2 weeks | Low |
| Fathom | 1 week | Low |
| Dashboard Validation | 1-2 weeks | Low-Medium |
| Calendar Reminders | 1-2 weeks | Low |
| **Total** | **4-7 weeks** | **Low** |

### Phase 2: Invoice Validation (Weeks 7-16)
| Component | Effort | Complexity |
|-----------|--------|------------|
| Invoice Parsing | 3-4 weeks | Medium |
| Validation Logic | 2-3 weeks | Medium-High |
| Error Flagging UI | 2-3 weeks | Medium |
| Wise Integration | 2-3 weeks | Medium-High |
| **Total** | **9-13 weeks** | **Medium-High** |

### Combined Timeline
- **Best Case:** 13 weeks (3.25 months)
- **Expected Case:** 16-18 weeks (4-4.5 months)
- **Worst Case:** 20+ weeks (5+ months)

---

## Recommendations

### Start With Lowest Complexity
1. Rate Synchronization (1-2 weeks, low risk)
2. Fathom Integration (1 week, low risk)
3. Calendar Reminders (1-2 weeks, low risk)

### Validate Before Committing
1. Wise API capabilities (critical for Phase 2)
2. Invoice format inventory (impacts parsing complexity)
3. Dashboard schema documentation

### De-Risk High Complexity
1. Build validation logic incrementally (start simple)
2. Pilot with 5-10 freelancers before full rollout
3. Maintain manual fallback during transition

---

## Complexity Scoring Summary

**Overall Project Complexity:** 6.5/10

| Category | Score | Notes |
|----------|-------|-------|
| API Integrations | 4/10 | Well-documented APIs, standard patterns |
| Data Complexity | 6/10 | Multiple formats, rate edge cases |
| Business Logic | 7/10 | Many validation rules, edge cases |
| UI/UX Requirements | 5/10 | Simple dashboard, approval workflow |
| Security Requirements | 6/10 | Financial data, payment triggers |
| Integration Points | 7/10 | 5+ systems to connect |
| Edge Case Handling | 8/10 | Many unknowns until implementation |

---

*Assessment created: 2026-01-18*
*Confidence level: Medium (needs API validation for Wise)*
