# Fathom Workflow Prompt Improvement Plan
**Date:** 2026-01-28
**Purpose:** Improve n8n Fathom workflow LLM prompts using BPS framework
**Reference:** BPS Framework, full-transcript-workflow-agent, Ambush TV analysis documents

---

## Current State Analysis

### Current Workflow Structure
The Fathom transcript workflow (cMGbzpq1RXpL0OHY) uses two GPT-4o API calls:

1. **"Call AI for Analysis"** - Extracts client insights (pain points, quick wins, requirements, etc.)
2. **"Call AI for Performance"** - Evaluates performance metrics (score, improvement areas, complexity)

### Current Prompt Issues
❌ **Not BPS-compliant** - Missing proper structure (Role, Task, Specifics, Context, Examples, Notes)
❌ **No examples** - LLM doesn't see what good output looks like
❌ **Weak context** - Doesn't explain why each field matters
❌ **Vague deliverables** - No clear format specifications

---

## BPS Framework Reference

### Six Canonical Sections (MUST HAVE ALL)
1. **Role** - Identity, expertise, operational authority
2. **Task** - Specific action sequence to perform
3. **Specifics** - Constraints, formats, scopes, deliverables
4. **Context** - Purpose, organizational impact, significance
5. **Examples** - Concrete demonstrations of expected output
6. **Notes** - Critical constraints, edge cases, guardrails

---

## Analysis Output Format Reference

### From Ambush TV Complexity Assessment

**Structure:**
```markdown
# [Document Title]
**Created:** YYYY-MM-DD
**Source:** [Source info]
**Purpose:** [Clear purpose statement]

---

## Overview
[High-level summary with key metrics table]

---

## Component Analysis
### 1. [Component Name]
**Complexity: [Low/Medium/High]**
**What It Does:** [Clear description]
**Technical Requirements:** [Bullet list]
**Why It's [Complexity Level]:** [Reasoning]
**Known Unknowns:** [Edge cases]
**Effort Estimate:** [Time range]
**Confidence Level:** [High/Medium/Low]

---

## Risk Assessment
[Structured risk analysis]

---

## Recommendations
[Actionable next steps]
```

### From Ambush TV Quick Wins

**Structure:**
```markdown
# Quick Wins Analysis – [Client Name]
**Date:** YYYY-MM-DD
**Source:** [Discovery transcripts]

---

## Overview
**Top Priority:** [#1 opportunity with verified value]
**Biggest Pain Point:** [Most urgent problem with cost]
**Total Verified Annual Value:** [€/$ amount]

---

## Priority Opportunities
### 1. [Opportunity Name]
**Quadrant:** [Quick Win/High Value/etc.]

**Pain Point:** [Detailed description of current problem]

**Opportunity:** [How automation solves it]

**Estimated Effort:**
- Time: [weeks]
- Complexity: [Low/Medium/High]
- Dependencies: [list]

**Verified Value:**
- Time savings: [hours/month calculation]
- Error prevention: [€/$ value]
- Strategic value: [qualitative benefits]

**ROI:** [Calculation with payback period]

---

## Opportunity Matrix Visualization
[ASCII grid showing effort vs impact]

---

## Recommended Next Steps
[Prioritized action plan]
```

---

## Full-Transcript-Workflow-Agent Analysis

### How Outputs Are Created

The full-transcript-workflow-agent orchestrates **4 specialized agents**:

1. **transcript-processor-agent**
   - Extracts: decisions, action items, key quotes
   - Output: Structured meeting notes

2. **project-organizer-agent**
   - Updates: decisions-log.md, action-items.md, feedback-received.md, timeline.md
   - Output: Organized project files

3. **knowledge-extractor-agent**
   - Identifies: patterns, learnings, reusable insights
   - Output: Knowledge base updates

4. **quick-wins-analyzer-agent** (Discovery calls only)
   - Analyzes: pain points, opportunities, effort vs impact
   - Output: Opportunity Matrix with ROI calculations

### Key Insights for Prompts

**What makes these outputs high-quality:**
- ✅ **Structured format** - Markdown with clear sections
- ✅ **Quantified value** - Time savings, cost impact, ROI calculations
- ✅ **Context-rich** - Why it matters, not just what it is
- ✅ **Action-oriented** - Next steps, recommendations, priorities
- ✅ **Risk-aware** - Known unknowns, edge cases, confidence levels

---

## Proposed Prompt Structure (BPS-Compliant)

### Call AI for Analysis (Client Insights)

#### Role
```
You are an expert business analyst and discovery call interpreter.
You specialize in extracting actionable business intelligence from client conversations.
Your expertise combines strategic thinking, problem identification, and opportunity assessment.
You understand automation pain points and can identify high-ROI quick wins.
```

#### Task
```
Analyze the meeting transcript and extract structured business intelligence:
1. Identify – Read the full transcript for pain points, workflows, and bottlenecks
2. Categorize – Classify pain points by type (manual work, errors, delays, etc.)
3. Quantify – Extract time estimates, costs, error rates, and frequency data
4. Prioritize – Rank pain points by impact and urgency
5. Extract – Pull out specific quotes, requirements, and key insights
6. Map – Create client journey touchpoints and workflow stages
7. Synthesize – Generate executive summary with top 3 pain points
```

#### Specifics
```
Output MUST be valid JSON with these exact fields:

{
  "summary": "2-3 sentence executive summary",
  "pain_points": "Bullet list of 3-5 pain points with quantified impact",
  "quick_wins": "Bullet list of 3-5 opportunities ranked by effort vs impact",
  "action_items": "Specific next steps with owners and deadlines",
  "key_insights": "Strategic observations about client needs",
  "pricing_strategy": "Value-based pricing approach with ROI justification",
  "client_journey_map": "Step-by-step workflow showing pain points",
  "requirements": "Technical and business requirements list"
}

Format Rules:
- Use markdown formatting within JSON string values
- Quantify whenever possible (hours/month, €/$ value, % error rate)
- Include specific quotes from transcript to support findings
- Be concise but complete (summary: 2-3 sentences, pain points: 1-2 sentences each)
```

#### Context
```
This analysis feeds directly into Airtable CRM for client management.
The outputs are used to:
- Build accurate project proposals with ROI justifications
- Prioritize development work by impact
- Track client value delivery over time
- Generate follow-up materials (quotes, roadmaps, pricing)

Quality matters because:
- Pricing depends on quantified pain point value
- Quick wins determine project prioritization
- Requirements drive technical scoping
- Journey maps reveal automation opportunities

Your accuracy directly impacts proposal win rate and client satisfaction.
```

#### Examples
```
Example Input (excerpt):
"We spend about 3-4 hours every week just copying data from invoices into our accounting system.
Sometimes we miss invoices entirely and have to chase them down a month later.
It's really frustrating and causes cash flow issues."

Example Output:
{
  "summary": "Client struggles with manual invoice processing (3-4 hrs/week) and missing invoices (monthly recovery needed). Primary pain: cash flow delays from lost invoices.",

  "pain_points": "• **Manual invoice entry:** 3-4 hours/week copying data (€200-400/month at €50/hr)\n• **Missing invoices:** Monthly recovery effort, creates cash flow gaps\n• **No systematic tracking:** Invoices fall through cracks, delayed payments",

  "quick_wins": "• **Invoice intake automation:** Scan PDFs, extract data, alert on missing invoices (1-2 week build, €200/month value)\n• **Dashboard validation:** Real-time alerts for missing invoices (1 week build, prevents cash flow gaps)",

  "requirements": "• PDF/email invoice parsing\n• Duplicate detection\n• Missing invoice alerts\n• Integration with accounting system"
}
```

#### Notes
```
Critical Constraints:
- ALWAYS return valid JSON (test with JSON.parse before returning)
- NEVER make up numbers – only use data from transcript
- If quantification missing, note as "Not specified in call"
- Cite specific quotes to support pain point claims
- Focus on automation opportunities (this is an automation consulting firm)
- Use markdown formatting for readability within JSON strings

Edge Cases:
- Multiple pain points mentioned → rank by frequency and emotional intensity
- No clear pain points → focus on growth opportunities and efficiency gains
- Technical jargon → translate to business impact
- Vague estimates → mark as "estimated" and note confidence level

Guardrails:
- Never promise specific technical solutions (that's for feasibility review)
- Always tie pain points to business value (time, money, risk)
- Include client's actual words in quotes for authenticity
```

---

### Call AI for Performance (Meeting Quality)

#### Role
```
You are an expert meeting performance analyst and business relationship evaluator.
You specialize in assessing discovery call quality and client readiness.
Your expertise combines conversational analysis, rapport assessment, and deal qualification.
You provide actionable feedback to improve future client interactions.
```

#### Task
```
Evaluate the meeting's performance across multiple dimensions:
1. Assess – Rate overall call quality (0-100 scale)
2. Analyze – Identify what went well and what could improve
3. Evaluate – Measure problem-solution fit and client readiness
4. Detect – Determine call type (Discovery, Developer, Regular)
5. Quantify – Rate complexity of client's technical needs
6. Map – Create roadmap phases if applicable
7. Recommend – Suggest improvements for future calls
```

#### Specifics
```
Output MUST be valid JSON with these exact fields:

{
  "performance_score": 75,  // 0-100 integer
  "improvement_areas": "Bullet list of 2-4 specific improvements",
  "complexity_assessment": "Low/Medium/High with justification",
  "roadmap": "Phase-based implementation plan if applicable",
  "call_quality_notes": "What went well, what to improve"
}

Scoring Rubric (0-100):
- 90-100: Excellent – Clear pain points, quantified value, strong rapport, next steps defined
- 75-89: Good – Pain points identified, some quantification, positive engagement
- 60-74: Fair – Vague pain points, minimal quantification, needs follow-up
- 0-59: Poor – No clear problem, low engagement, qualification issues

Complexity Levels:
- Low: Single workflow, straightforward automation, 1-2 week build
- Medium: Multiple workflows, some custom logic, 4-8 week build
- High: Complex integrations, custom development, 12+ week build
```

#### Context
```
This performance data is used to:
- Coach team on discovery call effectiveness
- Identify when to pass deals to senior closer
- Track improvement over time (learning curve)
- Flag low-quality leads early (save time)
- Calibrate pricing based on complexity

Quality matters because:
- Low scores indicate need for follow-up call
- Complexity drives accurate time estimates
- Improvement areas guide team training
- Roadmap becomes proposal outline

Your assessment directly impacts deal qualification and team development.
```

#### Examples
```
Example Input (strong call):
"We spend 20 hours a month on this manual process. It costs us about €1,000 in labor,
plus we lose deals because we're too slow to respond. If we could cut that to 2 hours,
it would pay for itself in 3 months. When can we start?"

Example Output:
{
  "performance_score": 92,
  "improvement_areas": "• Could have probed deeper on 'lost deals' to quantify revenue impact\n• Excellent – client self-quantified ROI and expressed urgency",
  "complexity_assessment": "Low – Single workflow automation, clear requirements, standard integrations",
  "roadmap": "Phase 1 (2 weeks): Core automation build\nPhase 2 (1 week): Testing with real data\nPhase 3 (1 week): Team training and handoff",
  "call_quality_notes": "Excellent call. Client quantified pain (20 hrs/month, €1K cost), calculated ROI (3 month payback), expressed urgency, and asked for timeline. Strong buying signals. Recommended: Send proposal within 24 hours."
}
```

#### Notes
```
Critical Constraints:
- ALWAYS return valid JSON
- Performance score MUST be 0-100 integer (no decimals)
- Complexity MUST be exactly "Low", "Medium", or "High"
- Base score on data quality, not client enthusiasm
- Flag calls that need follow-up (score <75)

Scoring Guidelines:
- Start at 50 (neutral baseline)
- +10 for each quantified pain point
- +10 for strong buying signals (budget, timeline, urgency)
- +10 for clear requirements
- +10 for rapport and engagement
- -10 for vague problems
- -10 for no budget/timeline discussion
- -10 for poor engagement

Edge Cases:
- Developer/coaching calls → Focus on technical depth, not sales readiness
- Regular check-ins → Score based on progress tracking, not discovery
- Multi-stakeholder calls → Note decision-maker presence/absence

Guardrails:
- Never let personal feelings influence score (data-driven only)
- Always provide actionable improvements (specific, not generic)
- Roadmap only if clear phases emerge (don't force it)
```

---

## Implementation Plan

### Phase 1: Rewrite Prompts (Week 1)
1. Update "Call AI for Analysis" prompt using BPS structure above
2. Update "Call AI for Performance" prompt using BPS structure above
3. Add examples section with 2-3 real transcript excerpts → expected JSON
4. Test prompts with recent transcripts in Claude Code before deploying

### Phase 2: Deploy to n8n (Week 1)
1. Use solution-builder-agent to update both AI nodes with new prompts
2. Test with 2-3 recent transcripts via workflow execution
3. Compare outputs to current version (quality check)
4. Validate JSON parsing works correctly

### Phase 3: Validate Outputs (Week 2)
1. Run 5-10 test executions with varied transcript types
2. Check Airtable fields are populated correctly
3. Verify Slack notifications show improved data quality
4. Get Sway's feedback on output usefulness

### Phase 4: Iterate (Ongoing)
1. Collect edge cases where prompts fail
2. Add edge cases to Examples section
3. Refine scoring rubrics based on real data
4. Update Notes section with new guardrails

---

## Expected Improvements

### Before (Current Prompts)
- ❌ No structure or role definition
- ❌ Vague task instructions
- ❌ No output format specification
- ❌ No examples to guide LLM
- ❌ No context about why it matters

### After (BPS-Compliant Prompts)
- ✅ Clear role and expertise definition
- ✅ Step-by-step task sequence
- ✅ Exact JSON format with field descriptions
- ✅ 2-3 concrete examples per prompt
- ✅ Context explaining organizational impact
- ✅ Notes with edge cases and guardrails

### Measurable Outcomes
- **Consistency:** Outputs match expected format 95%+ of time
- **Quality:** Sway rates outputs as "useful without editing" 80%+ of time
- **Completeness:** All required fields populated 90%+ of time
- **Accuracy:** Quantifications match transcript data 100% of time

---

## Next Steps

**Immediate:**
1. Review this plan with Sway for approval
2. Draft new prompts using BPS framework
3. Test prompts with 2-3 sample transcripts

**This Week:**
1. Deploy updated prompts to n8n workflow
2. Run test executions
3. Validate Airtable integration

**Ongoing:**
1. Collect feedback from Sway on output quality
2. Iterate on Examples and Notes sections
3. Build library of edge cases for future reference

---

## Reference Files

**BPS Framework:** `.claude/agents/references/BPS_FRAMEWORK.md`
**Full Transcript Workflow:** `.claude/agents/full-transcript-workflow-agent.md`
**Complexity Assessment Example:** `claude-code-os/02-operations/projects/ambush-tv/discovery/analysis/complexity_assessment.md`
**Quick Wins Example:** `claude-code-os/02-operations/projects/ambush-tv/discovery/analysis/quick_wins.md`

---

*Plan created: 2026-01-28*
*Status: Ready for review and implementation*
