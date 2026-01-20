# Eugene - Proposal Presentation
## Project Kickoff & Agreement

**Date:** December 15, 2024
**Time:** 10:00 AM - 11:05 AM (61 minutes)
**Attendees:** Sway Clarke (Consultant), Eugene (Client)
**Meeting Type:** Proposal Presentation / Project Kickoff
**Recording:** https://fathom.video/share/pYTDPSeTCJfrWLad1u9AN4zQvBSA9sN2

---

## Executive Summary

**Meeting Purpose:** Present formal proposal for automating Eugene's debt advisory document processing.

**Outcome:** ✅ **DEAL CLOSED** - Eugene accepted the phased approach, starting with free Phase 1 trial.

**Start Date:** January 5, 2025 (intensive development and testing)

**Key Win:** Positioned as premium value exchange (free trial for testimonial, not "working for free")

---

## The Proposal Structure

### Business Goal

**Current State:**
- Processing ~6 deals/year
- 5-10 hours per client on manual document handling
- 40-50% of Eugene's time consumed by admin work

**Target State:**
- Scale to 50 deals/year
- Reduce qualification time by 80% (from 5-10 hrs to 1-2 hrs per deal)
- Free up capacity for higher-value advisory work

**Time Value:**
- Eugene's rate: €200/hr
- Sway's rate: €250/day

---

## 3-Phase Approach

### Phase 1: Document Detection & Sorting (FREE TRIAL)

**What It Does:**
- Automatically detect, identify, and sort 4 core documents required for qualification
- Create organized Google Drive folder structure
- Update Google Sheet with document checklist and status

**Technical Flow:**
1. Email hook downloads attachments when new client inquiry arrives
2. LLM (GPT-3.5 API) identifies documents with confidence score (e.g., "Grundbuch, 97%")
3. Files sorted into Google Drive folders
4. Google Sheet updates with checklist ("4/4 complete", "3/4 missing Teaser", etc.)

**Why GPT-3.5 (not GPT-4):**
- API pricing = pay per token (more cost-effective for this task)
- Well-prompted GPT-3.5 sufficient for document identification
- ChatGPT Plus subscription = flat monthly fee (unnecessary)

**Cost to Eugene:** Free
**Eugene's Investment:** Time for feedback and testing
**Sway's Request:** Video or written testimonial upon satisfaction

### Phase 1.5: Expand Document Recognition (OPTIONAL)

**What It Does:**
- Train system to recognize remaining 14 documents (total 18)
- Can be completed before OR after Phase 2 (Eugene's choice)

**Value:** More complete automation, less manual sorting

### Phase 2: Automated Client Replies (~€2,500 value)

**What It Does:**
- Automate email replies to clients for missing documents
- Trigger: Google Sheet status (e.g., "3/4 documents received")
- Action: Send personalized email requesting missing items

**Why This Matters:**
- Eliminates back-and-forth email admin
- Speeds up deal qualification
- Maintains professional client communication

**Pricing:**
- Time-based: ~10 days @ €250/day = €2,500
- Value-based: 80% time reduction = €2,400/year savings (6 deals × 8 hrs saved × €200/hr)

### Phase 3: LLM Data Analysis (~€2,500 value)

**What It Does:**
- Automatically extract and analyze data from documents
- Feed sorted documents into LLM to answer specific questions
- Deliver pre-analyzed summary to Eugene

**Why This Matters:**
- Eliminates manual document review
- Provides structured insights immediately
- Eugene reviews analysis, not raw documents

**Pricing:** Similar to Phase 2 (~€2,500)

---

## Project Logistics

### Timeline

**Pre-Jan 5:**
- Sway: Initial research and planning
- Eugene: Provide 5-20 historical client files for training/testing

**Jan 5, 2025:**
- Full development begins
- Eugene back in office and available for intensive testing

**Mid-February Target:**
- Significant progress before busy season starts
- System validated and running in production

### Roles & Responsibilities

**Eugene:**
- Provide historical client files (5-20 files, each with 4 core documents)
- Provide timely feedback during testing phase
- Test system with real incoming leads

**Sway:**
- Build automation system using N8N or Make.com
- Deliver weekly progress updates
- Create user guide and walkthrough
- Train Eugene on system usage

### Ownership Model

**System Built in Eugene's Accounts:**
- N8N/Make.com account = Eugene's
- Google Drive = Eugene's
- Google Sheets = Eugene's
- Result: Full ownership, no ongoing dependency

**Optional Management Fee:**
- Separate monthly fee for ongoing maintenance/updates
- Not required, but available if Eugene wants support

---

## Investment Summary

| Phase | What You Get | Cost | ROI |
|-------|--------------|------|-----|
| **P1** | Document detection + sorting (4 docs) | FREE (for testimonial) | Immediate time savings |
| **P1.5** | Expand to all 18 documents | TBD | More complete automation |
| **P2** | Automated client replies | ~€2,500 | €2,400/year time savings |
| **P3** | LLM data analysis | ~€2,500 | 80% reduction in qualification time |

**Long-term Opportunity:**
- If successful, package and sell system to other debt advisors
- Create new revenue stream from productization

---

## Why Eugene Said Yes

### Key Selling Points from Presentation

1. **Phased Approach = Low Risk**
   - Start with free Phase 1
   - See value before committing to Phase 2/3
   - Each phase delivers standalone value

2. **Aligned Incentives**
   - Free trial shows Sway's confidence in value
   - Testimonial exchange = mutual benefit
   - Time-based AND value-based pricing justification

3. **Full Ownership**
   - Built in Eugene's accounts
   - No ongoing dependency on consultant
   - Can maintain/modify independently

4. **Perfect Timing**
   - Jan 5 start = Eugene available for testing
   - Mid-Feb target = before busy season
   - Quiet period allows intensive collaboration

5. **Clear ROI**
   - 80% time reduction = quantifiable
   - €200/hr time savings = concrete value
   - Path to 8x business growth (6 → 50 deals/year)

---

## Technical Decisions Made

### Platform: N8N or Make.com
- Both evaluated as options
- Final choice: Eugene's preference
- Rationale: Familiarity and comfort

### LLM Strategy: Sequential Processing
- Process documents one at a time
- Avoid parallel processing complexity
- Lower cost, easier debugging

### Confidence Score Approach
- LLM returns document type + confidence percentage
- Example: "Grundbuch, 97%" or "Unknown, 45%"
- Allows Eugene to review low-confidence matches

---

## Next Steps (From Meeting)

**Sway:**
- ✅ Draft simple agreement for Phase 1
- ⏳ Begin initial research and planning

**Eugene:**
- ✅ Provide historical client files (5-20 with 4 core documents) before holidays
- ⏳ Review and sign Phase 1 agreement

**Both:**
- ⏳ Begin intensive development and testing on **January 5, 2025**

---

## Post-Meeting Reflections (Added Dec 17, 2024)

**What Worked:**
- Phased approach removed risk objection
- Free Phase 1 demonstrated confidence without appearing desperate
- Dual pricing (time + value) anchored perceived worth
- Strategic exclusions (Phase 2/3) created clear upsell path
- Perfect timing alignment (Jan 5 start, mid-Feb target)

**The Close:**
- No pressure, no hard sell
- Eugene saw value immediately
- Asked clarifying questions (good sign of engagement)
- Accepted on the call (no "let me think about it")

**Key Lesson:**
- Richard's coaching on "strategic exclusions" was exactly right
- Leaving automated follow-ups for Phase 2 = perfect upsell opportunity
- Eugene will SEE the value in Phase 1, WANT Phase 2 naturally
