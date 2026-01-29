# BPS v2.0 Deployment Checklist

**Date:** 2026-01-28
**Status:** Ready for deployment testing
**Estimated Time:** 30-45 minutes for full test

---

## Pre-Deployment Test (Minimal Transcript Validation)

### Step 1: Update n8n Workflow Nodes (5 mins)

**Workflow:** cMGbzpq1RXpL0OHY (Fathom transcript processing)

**Node 1: "Call AI for Analysis" (Client Insights)**
1. Open n8n workflow editor
2. Locate "Call AI for Analysis" node
3. **OPTION A - Keep GPT-4o:**
   - Replace prompt content with v2.0 from: `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/fathom_client_insights_prompt_bps_v2.0_2026-01-28.md`
   - Keep existing OpenAI credentials

**OPTION B - Switch to Claude (Recommended):**
   - Change credential to Anthropic API
   - Model: claude-sonnet-4-20250514
   - Replace prompt content with v2.0
   - Max tokens: 16000 (increase from default to handle large outputs)

**Node 2: "Call AI for Performance"**
1. Locate "Call AI for Performance" node
2. Same options as above:
   - **Option A:** Keep GPT-4o, replace prompt with v2.0 from: `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/fathom_performance_analysis_prompt_bps_v2.0_2026-01-28.md`
   - **Option B:** Switch to Claude + v2.0 prompt

---

### Step 2: Test with Minimal Transcript (15-20 mins)

**Transcript:** `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/minimal_test_transcript_2026-01-28.txt`

**Execute test:**
1. Trigger n8n workflow manually OR via webhook
2. Provide minimal test transcript as input
3. Monitor execution logs for errors
4. Wait for completion (~2-5 minutes depending on API speed)

**Expected token usage:**
- Client Insights: ~12,000-15,000 output tokens
- Performance: ~8,000-10,000 output tokens
- **Total cost estimate:** $0.30-0.50 (Claude) or $0.25-0.40 (GPT-4o)

---

### Step 3: Validate Airtable Output (10 mins)

**Check these in Airtable "Calls" table:**

✓ **Record created** (should have new record with Title "Test Discovery Call")

✓ **Field depth validation:**
- [ ] **pain_points:** 180-240 lines expected (not 3 sentences)
- [ ] **quick_wins:** 100-150 lines expected
- [ ] **key_insights:** 400-600 lines expected
- [ ] **pricing_strategy:** 300-500 lines expected
- [ ] **complexity_assessment:** 250-350 lines expected
- [ ] **roadmap:** 200-300 lines expected

✓ **Content quality validation:**
- [ ] ASCII diagrams render properly (box-drawing characters intact)
- [ ] Markdown formatting preserved (bold, bullets, tables)
- [ ] Transcript line number citations present (e.g., "line 2", "line 14")
- [ ] Step-by-step formulas visible with calculations
- [ ] No truncation occurred (no "..." at end of fields)

✓ **JSON parsing:**
- [ ] All 8 Client Insights fields populated
- [ ] All 5 Performance fields populated
- [ ] No parsing errors in execution log

---

### Step 4: Review Test Output Quality (5-10 mins)

**Open the test record in Airtable and verify:**

**pain_points field should contain:**
```
### Pain Point 1: Manual Invoice Processing

**Current Workflow (Step-by-Step):**
1. Receive invoice PDFs via email
2. Download PDFs to local machine
3. Open QuickBooks
4. **[PAIN: Manually type invoice data - 10-15 min per invoice]**
5. Verify amounts and vendor details
...

**Time Cost:**
- Per invoice: 10-15 min (line 4)
- Volume: 30-40 invoices/week (line 4)
- Weekly time: 8 hours (line 2)
...

[Continue for 80-100 lines]

### Pain Point 2: Data Sync Between Systems
[60-80 lines]

### Pain Point 3: Vendor Pricing Changes
[40-60 lines]
```

**key_insights field should contain:**
```
## One-Liner
**Sarah spends 8 hours/week manually processing 30-40 invoices with 10% error rate, causing $5K mistake (line 7) and preventing focus on growth initiatives.**

## Critical Pain Points
[Detailed breakdowns]

## ROI Calculation

**Invoice Automation:**

```
FORMULA:
Weekly time = 8 hours (line 2)
Hourly rate = $50 (line 9)
Weekly value = 8 × $50 = $400

Monthly value = $400 × 4 = $1,600
Annual value = $1,600 × 12 = $19,200
...
```

[Continue for 400-600 lines]
```

---

### Success Criteria

**Test PASSES if:**
✅ All Airtable fields populate without errors
✅ Field lengths match expectations (200-600+ lines per major field)
✅ Markdown formatting preserved (no garbled ASCII diagrams)
✅ Transcript line citations present throughout
✅ Formulas show step-by-step calculations
✅ No JSON parsing errors in logs
✅ Total execution time <5 minutes

**Test FAILS if:**
❌ Any field is empty or shows "[Error]"
❌ Fields contain only 2-3 sentences (v1.0 depth)
❌ ASCII diagrams broken (symbols garbled)
❌ No transcript line number citations
❌ Formulas missing or incomplete
❌ JSON parsing errors in n8n logs
❌ Airtable truncates content (fields end with "...")

---

## Post-Test: Full Deployment (If Test Passes)

### Step 5: Deploy to Production (5 mins)

**If minimal test passes all criteria:**

1. **Save n8n workflow** with v2.0 prompts
2. **Document in version log:** "Upgraded to BPS v2.0 prompts (2026-01-28) - generates 200-800+ line comprehensive analysis"
3. **Set workflow to active** (if it was paused for testing)

---

### Step 6: Test with Leonor Transcript (20-30 mins)

**Transcript:** `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/ai-audits/interview-transcripts/Leonor Zuzarte - 2026-01-27 - HR & Community.txt`

**Expected output:**
- pain_points: 300-400 lines (3-5 detailed pain points)
- key_insights: 700-850 lines (matching key_insights.md example structure)
- pricing_strategy: 500-650 lines
- complexity_assessment: 350-450 lines
- roadmap: 400-500 lines

**Validation against test expectations:**
Use `/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/prompts/leonor_transcript_test_expectations_v1.0_2026-01-28.md` to verify:
- ✓ Extracts exact numbers (5 min/call, 10 min fixes, 3 hrs sanitization)
- ✓ Marks estimates as "[estimated]" or "[Not quantified in call]"
- ✓ Doesn't invent calculations not supported by transcript data
- ✓ Cites transcript line numbers for all quantified claims

**Estimated cost:** $0.80-1.50 per full Leonor transcript analysis

---

### Step 7: Production Monitoring (Ongoing)

**After 3-5 production runs:**

1. **Review output quality:**
   - Is depth consistent across different transcript types?
   - Are ASCII diagrams rendering properly?
   - Are formulas complete and correct?

2. **Token usage analysis:**
   - Average tokens per analysis?
   - Cost per analysis vs. value delivered?
   - Any prompts hitting token limits?

3. **Airtable performance:**
   - Field loading times acceptable?
   - Markdown rendering issues?
   - Need to adjust field types (long text vs. rich text)?

4. **Iterate if needed:**
   - Adjust prompt instructions if consistent issues emerge
   - Refine Examples section based on edge cases
   - Update Notes section with new learnings

---

## Rollback Plan (If Test Fails)

**If test reveals issues:**

1. **Immediate rollback:**
   - Restore v1.0 prompts in n8n
   - Document failure mode in issue log
   - Don't process production transcripts until fixed

2. **Debug approach:**
   - **JSON parsing error:** Check prompt output format, ensure valid JSON
   - **Truncated fields:** Increase max tokens in n8n node settings
   - **Garbled ASCII:** Check character encoding in Airtable fields
   - **Missing content:** Review prompt instructions for that specific field
   - **Format issues:** Test prompt directly in Claude/GPT playground first

3. **Iteration:**
   - Fix identified issues in v2.1
   - Re-test with minimal transcript
   - Only deploy to production after clean test

---

## Current Status Summary

**Completed:**
- ✅ v2.0 Client Insights prompt created (fathom_client_insights_prompt_bps_v2.0_2026-01-28.md)
- ✅ v2.0 Performance Analysis prompt created (fathom_performance_analysis_prompt_bps_v2.0_2026-01-28.md)
- ✅ Minimal test transcript created (minimal_test_transcript_2026-01-28.txt)
- ✅ Test expectations documented (leonor_transcript_test_expectations_v1.0_2026-01-28.md)
- ✅ Upgrade summary documented (v2_upgrade_summary_2026-01-28.md)
- ✅ Airtable integration verified (working, just needs v2.0 depth)

**Pending (requires Sway action):**
- ⏳ Update n8n workflow nodes with v2.0 prompts
- ⏳ Execute minimal transcript test
- ⏳ Validate Airtable output depth and quality
- ⏳ Deploy to production if test passes
- ⏳ Test with Leonor transcript
- ⏳ Monitor first 3-5 production runs

**Blockers:**
- None - all prep work complete, ready for Sway to execute n8n changes

---

## Recommendation

**Approach: Test → Validate → Deploy**

1. **Start with minimal transcript test** (30-45 mins total)
   - Low risk, low cost (~$0.40)
   - Validates all assumptions
   - Identifies issues early

2. **If test passes:** Deploy immediately and test with Leonor
   - High confidence after minimal test success
   - Real-world validation with actual discovery call

3. **If test fails:** Debug, iterate to v2.1, re-test
   - Better to find issues with $0.40 test than $1.50 production run

4. **After 3-5 successful runs:** Consider production-ready
   - Gather Sway feedback on output usefulness
   - Document any edge cases for prompt refinement
   - Update Examples section based on real outputs

---

*Checklist created: 2026-01-28*
*Status: Ready for Sway to execute Steps 1-3*
*Next action: Update n8n workflow nodes, run minimal test*
