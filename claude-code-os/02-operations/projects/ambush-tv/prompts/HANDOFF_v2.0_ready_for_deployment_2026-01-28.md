# 🎯 BPS v2.0 Prompts - Ready for Deployment

**Date:** 2026-01-28
**Status:** ✅ All prep work complete - ready for your action
**Your time required:** 30-45 minutes for complete test and deployment

---

## What's Been Completed

### ✅ Core Deliverables

**1. BPS v2.0 Client Insights Prompt**
- **Location:** `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/fathom_client_insights_prompt_bps_v2.0_2026-01-28.md`
- **Output depth:** 200-800+ lines per major field (vs 2-3 sentences in v1.0)
- **Structure:** Full BPS compliance (Role, Task, Specifics, Context, Examples, Notes)
- **Features:**
  - Multi-level pain point breakdowns (40-100 lines each)
  - ASCII workflow diagrams
  - Step-by-step ROI formulas with calculations
  - Transcript line number citations
  - Opportunity Matrix prioritization
  - Consultant-grade strategic analysis

**2. BPS v2.0 Performance Analysis Prompt**
- **Location:** `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/fathom_performance_analysis_prompt_bps_v2.0_2026-01-28.md`
- **Output depth:** 200-600+ lines (vs ~20 lines in v1.0)
- **Features:**
  - Component-by-component complexity analysis (8-12 components)
  - Best/expected/worst case effort estimates
  - Week-by-week roadmap granularity
  - Risk assessment with mitigations
  - Checkpoint meeting structures

**3. Minimal Test Transcript**
- **Location:** `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/minimal_test_transcript_2026-01-28.txt`
- **Purpose:** Low-cost validation ($0.40) before processing Leonor's full transcript
- **Contains:** Clear pain points, quantified metrics, buying signals, decision-maker clarity
- **Expected output:** ~1,500-2,000 lines across all fields

**4. Deployment Checklist**
- **Location:** `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/deployment_checklist_v2.0_2026-01-28.md`
- **Contains:** Step-by-step instructions for testing and deployment
- **Includes:** Success criteria, rollback plan, validation checklist

**5. Upgrade Summary**
- **Location:** `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/v2_upgrade_summary_2026-01-28.md`
- **Shows:** Before/after comparison with examples from your discovery documents
- **Details:** Field-by-field transformation (2 sentences → 200-800+ lines)

**6. Leonor Test Expectations**
- **Location:** `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/leonor_transcript_test_expectations_v1.0_2026-01-28.md`
- **Purpose:** Validation criteria for Leonor transcript test
- **Contains:** Expected quantified data extraction (5 min/call, 3 hrs sanitization, etc.)

---

## Key Findings from Prep Work

### ✅ Airtable Integration Verified

**Tested by checking execution 6527:**
- All 8 Client Insights fields populate correctly
- All 5 Performance fields populate correctly
- Field mapping works (rec4YXRsKWLQsyBDR has all fields)
- **Issue:** Content is shallow (v1.0 prompts generate 2-3 sentences)
- **Solution:** Deploy v2.0 prompts for depth

**No integration fixes needed** - just prompt replacement.

---

### 🎯 Recommendation: Switch to Claude API

**Current:** Using GPT-4o (OpenAI) in n8n

**Recommended:** Switch to Claude Sonnet 4 (Anthropic)

**Why:**
1. **Consistency** - You use full-transcript-workflow-agent (Claude), so keep analysis on Claude too
2. **Better instruction following** - Claude excels at structured output (200+ line requirements)
3. **Larger context** - Claude: 200K tokens vs GPT-4o: 128K (matters for long transcripts)
4. **Cost comparable** - Similar pricing for our use case (~$0.40-1.50 per analysis)
5. **Quality** - Both excellent, but Claude may produce better markdown formatting

**How:** Change n8n node credentials from OpenAI → Anthropic, set model to `claude-sonnet-4-20250514`

---

## What You Need to Do Next

### Step 1: Update n8n Workflow (5 mins)

**Workflow:** cMGbzpq1RXpL0OHY

**Option A - Quick (Keep GPT-4o):**
1. Open "Call AI for Analysis" node
2. Copy/paste v2.0 Client Insights prompt
3. Open "Call AI for Performance" node
4. Copy/paste v2.0 Performance prompt
5. Save workflow

**Option B - Recommended (Switch to Claude):**
1. Open "Call AI for Analysis" node
2. Change credential to Anthropic API
3. Set model: `claude-sonnet-4-20250514`
4. Set max tokens: 16000
5. Copy/paste v2.0 Client Insights prompt
6. Repeat for "Call AI for Performance" node
7. Save workflow

---

### Step 2: Run Minimal Test (15-20 mins)

**Purpose:** Validate v2.0 depth + Airtable capacity before burning tokens on Leonor

**Execute:**
1. Trigger workflow manually with minimal test transcript
2. Monitor execution (~2-5 minutes)
3. Check Airtable for new "Test Discovery Call" record

**Validate:**
- ✓ pain_points field: 180-240 lines (not 3 sentences)
- ✓ key_insights field: 400-600 lines
- ✓ pricing_strategy field: 300-500 lines
- ✓ ASCII diagrams render properly
- ✓ Formulas show step-by-step calculations
- ✓ No truncation

**Cost:** ~$0.40 (Claude) or ~$0.30 (GPT-4o)

**Decision:**
- ✅ **Pass:** Proceed to Step 3 (Leonor test)
- ❌ **Fail:** Debug, iterate to v2.1, re-test

---

### Step 3: Test with Leonor Transcript (20-30 mins)

**If minimal test passes:**

**Execute:**
1. Trigger workflow with Leonor transcript: `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/ai-audits/interview-transcripts/Leonor Zuzarte - 2026-01-27 - HR & Community.txt`
2. Wait for completion (~3-8 minutes)
3. Check Airtable record

**Validate against expectations doc:**
- ✓ Extracts exact numbers (5 min, 10 min, 3 hrs, €20/hour)
- ✓ Marks estimates as "[estimated]" when extrapolating
- ✓ Doesn't invent numbers not in transcript
- ✓ Cites line numbers for all claims
- ✓ Generates 700-850 lines for key_insights (matching your example)

**Cost:** ~$1.50 (Claude) or ~$1.00 (GPT-4o)

**Decision:**
- ✅ **Pass:** Deploy to production, monitor first 3-5 runs
- ❌ **Fail:** Review output, refine prompt, re-test

---

### Step 4: Production Deployment (5 mins)

**If Leonor test passes:**

1. Mark workflow as production-ready
2. Document in version log: "BPS v2.0 deployed (2026-01-28)"
3. Process next 3-5 transcripts normally
4. Monitor quality and token usage
5. Gather your feedback on output usefulness

---

## Expected Transformation

### Before (v1.0):

**pain_points field:**
```
• Manual rate synchronization: Updating 3 sheets creates error risk. 2 hrs/month.
• Invoice validation: 20+ hours/month reviewing invoices.
• Onboarding sheet: Avoided due to frustration, causes delays.
```
*(Total: 3 sentences, ~150 tokens)*

---

### After (v2.0):

**pain_points field:**
```markdown
### Pain Point 1: Manual Rate Synchronization

**Current Workflow (Step-by-Step):**
1. Weekly team meeting: Core team identifies freelancers to raise
2. Leonor conducts feedback calls (5 min each) (line 251)
3. Updates Team Directory sheet manually
4. **[PAIN: Updates FCA sheet manually - risk of forgetting]**
5. **[PAIN: Verifies Dashboard auto-populated - sometimes manual fix needed]**
6. Monthly reconciliation (2 hours) to catch discrepancies (line 299)

**Time Cost:**
- Per call: 5 min (line 251)
- Frequency: Bi-weekly batch (5-10 freelancers) (line 127)
- Verification: 2+ hours/month (line 299)
- Monthly total: 2.5 hours/month
- Annual total: 30 hours/year

**Error Scenarios:**
- Rate changed in Team Directory but not FCA → Dashboard old rate → Invoice validation fails
- Example: > "that person's charging is 18.5, but the dashboard says 17" (line 287)

**User Quotes:**
> "I just feel like for me personally, it opens me up to a lot of error." (line 49)
> "whole day a month where I go and I spend like two hours making sure..." (line 299)

**Downstream Impact:**
- Affects: Sindbad's invoice validation (catches rate discrepancies)
- Causes: 10 min fire drills every 3 months (line 299)
- Results in: Error cascade from admin → invoices → validation bottleneck

**Why It Matters:**
Leonor values personalized freelancer feedback but admin burden after calls creates avoidance. Rate errors cascade to Sindbad's 20+ hr/month workload.

[ASCII workflow diagram - 15 lines]
```

*(Total: 80-100 lines per pain point × 3-5 pain points = 240-500 lines, ~3,000-6,000 tokens)*

---

## Success Metrics

### Immediate (After minimal test):
- ✅ All fields populate without errors
- ✅ Field depth 10-100x increase (2 sentences → 200+ lines)
- ✅ Markdown formatting preserved
- ✅ No truncation in Airtable

### Post-Deployment (After 3-5 runs):
- ✅ Consistent depth across transcript types
- ✅ ASCII diagrams render correctly
- ✅ Formulas complete and accurate
- ✅ Output matches example document quality
- ✅ Sway feedback: "This is what I wanted"

---

## Risk Mitigation

**Low-risk approach:**
1. ✅ Minimal test first ($0.40) - finds issues early
2. ✅ Leonor test second ($1.50) - real-world validation
3. ✅ Rollback plan ready - can restore v1.0 if needed
4. ✅ Clear success criteria - know when to proceed/stop
5. ✅ Airtable pre-validated - integration already working

**Total investment before production:** ~$2.00 for both tests

---

## Files Summary

**All files in:** `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/`

| File | Purpose | Status |
|------|---------|--------|
| `fathom_client_insights_prompt_bps_v2.0_2026-01-28.md` | Production prompt (Client Insights) | ✅ Ready |
| `fathom_performance_analysis_prompt_bps_v2.0_2026-01-28.md` | Production prompt (Performance) | ✅ Ready |
| `minimal_test_transcript_2026-01-28.txt` | Test input | ✅ Ready |
| `leonor_transcript_test_expectations_v1.0_2026-01-28.md` | Validation criteria | ✅ Ready |
| `deployment_checklist_v2.0_2026-01-28.md` | Step-by-step guide | ✅ Ready |
| `v2_upgrade_summary_2026-01-28.md` | Before/after documentation | ✅ Ready |
| `HANDOFF_v2.0_ready_for_deployment_2026-01-28.md` | This file | ✅ Ready |

**Leonor transcript location:**
`/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/ai-audits/interview-transcripts/Leonor Zuzarte - 2026-01-27 - HR & Community.txt`

---

## Estimated Timeline

**If you start now:**

- **5 mins:** Update n8n prompts (copy/paste)
- **15 mins:** Run minimal test + validate
- **20 mins:** Run Leonor test + validate
- **5 mins:** Deploy to production

**Total: 45 minutes end-to-end**

---

## Questions Answered

### 1. Will it write to Airtable correctly?
✅ **YES** - Integration verified with execution 6527. All fields populate. Just needs v2.0 depth.

### 2. Should we use Claude Code agents or ChatGPT?
✅ **Recommendation: Switch to Claude API** for consistency with your agent usage and better instruction following.

### 3. Are we using agents with tools or basic completion nodes?
✅ **Basic completion nodes** - correct architecture for this use case. No need for agent tools.

---

## Next Action

**👉 Follow deployment_checklist_v2.0_2026-01-28.md starting at Step 1**

Or if you want the quick version:
1. Open n8n workflow cMGbzpq1RXpL0OHY
2. Update two nodes with v2.0 prompts
3. Test with minimal_test_transcript_2026-01-28.txt
4. Validate output in Airtable
5. If good → test Leonor transcript
6. If good → deploy to production

**Everything is ready. Just needs your n8n access to execute.**

---

*Handoff document created: 2026-01-28*
*All prep work complete - ready for deployment*
*Estimated value: Airtable analysis goes from "shallow" to "consultant-grade depth"*
