# Fathom AI Analysis v2 - Prompt Enhancement Complete

**Date:** 2026-01-31
**Workflow ID:** QTmNH1MWW5mGBTdW
**Status:** ✅ Complete and validated

---

## Summary

Enhanced all 4 Build Prompt Code nodes and 4 HTTP OpenAI nodes in the Fathom AI Analysis v2 workflow to produce 2-3x more verbose, structured analysis output with direct transcript quotes, severity scores, and detailed subsections.

---

## Changes Applied

### 8 Nodes Updated

**Build Prompt Nodes (4):**
- `build-prompt-1` (Discovery Call Analysis)
- `build-prompt-2` (Opportunity Analysis)
- `build-prompt-3` (Technical Assessment)
- `build-prompt-4` (Strategic Planning)

**HTTP OpenAI Nodes (4):**
- `http-openai-1`
- `http-openai-2`
- `http-openai-3`
- `http-openai-4`

---

## Prompt Enhancements (Build Prompt 1-4)

### Before
- Generic word count requests (500-1000 words)
- No structure requirements
- No quote requirements
- No severity scoring

### After

**Call 1: Discovery Analysis** (`build-prompt-1`)
- `summary`: MINIMUM 800 words with 5 subsections (Meeting Context, Stakeholders, Key Themes, Outcomes, Business Implications)
- `key_insights`: MINIMUM 600 words with 5 subsections (Meeting Classification, Decision Maker Analysis, Budget Signals, Competitive Landscape, Strategic Opportunities)
- `pain_points`: MINIMUM 600 words with severity-based categorization (Critical 9-10, High 7-8, Medium 4-6)
  - Requires: Severity scores, confidence levels, DIRECT QUOTES, business impact, root cause analysis
- `action_items`: MINIMUM 400 words with time-based priority structure (Immediate, Short-term, Medium-term)
  - Requires: Owner, priority, deadline, description (50+ words), dependencies, success criteria, effort estimate

**Call 2: Opportunity Analysis** (`build-prompt-2`)
- `quick_wins`: MINIMUM 800 words with effort/impact matrix
  - Categories: High Impact/Low Effort, High Impact/Medium Effort, Medium Impact/Low Effort
  - Requires: Impact score, effort score, ROI calculation, implementation steps, resource requirements, risk assessment, success metrics, DIRECT QUOTES
- `pricing_strategy`: MINIMUM 800 words with comprehensive tier breakdown
  - Requires: Pricing philosophy, 3 package tiers (150+ words each), add-ons, pricing justification with DIRECT QUOTES, payment terms, upsell pathways

**Call 3: Technical Assessment** (`build-prompt-3`)
- `complexity_assessment`: MINIMUM 800 words with multi-dimensional complexity scoring
  - Requires: Overall complexity score, 4 complexity breakdowns (Architecture, Integration, Data, UX) each with 100+ word assessment, DIRECT QUOTES, mitigation strategies, risk assessment matrix, resource requirements
- `requirements`: MINIMUM 800 words with comprehensive requirements documentation
  - Requires: 8-12 functional requirements (each with priority, description 100+ words, user story, DIRECT QUOTES, acceptance criteria, dependencies, effort estimate)
  - Non-functional requirements: Performance, Security, Scalability, Compliance (each 100+ words)
  - Constraints and assumptions with DIRECT QUOTES

**Call 4: Strategic Planning** (`build-prompt-4`)
- `roadmap`: MINIMUM 800 words with phased implementation plan
  - Requires: Executive summary, 4-5 phases (150+ words each with objectives, milestones, deliverables, dependencies, resources, success criteria, risk factors, DIRECT QUOTES)
  - Dependencies map, timeline visualization
- `client_journey_map`: MINIMUM 800 words with current vs future state analysis
  - Requires: 6 journey phases (Discovery, Evaluation, Purchase, Onboarding, Usage, Support)
  - Each phase: Touchpoints, pain points/delight moments, customer emotions (scores), DIRECT QUOTES
  - Gap analysis, transformation metrics with business impact

---

## HTTP Node Enhancements

### Temperature Adjustment
- **Before:** `temperature: 0.7` (more creative, less focused)
- **After:** `temperature: 0.3` (more focused, detailed, consistent)

### Max Tokens Increase
- **Before:** Default limit (often 2048 or less)
- **After:** `max_tokens: 4096` (allows for full verbose output)

**Updated Request Body:**
```javascript
JSON.stringify({
  model: 'gpt-4o',
  messages: [{ role: 'user', content: $json.prompt }],
  temperature: 0.3,
  max_tokens: 4096
})
```

---

## Expected Output Improvements

### Word Counts (Minimum)

| Field | Old Target | New Minimum | Improvement |
|-------|-----------|-------------|-------------|
| summary | 500-1000 | 800+ | +60% min |
| key_insights | 500-800 | 600+ | +20% min |
| pain_points | 500-800 | 600+ | +20% min |
| action_items | 300-600 | 400+ | +33% min |
| quick_wins | 500-800 | 800+ | +60% min |
| pricing_strategy | 500-800 | 800+ | +60% min |
| complexity_assessment | 500-800 | 800+ | +60% min |
| requirements | 500-800 | 800+ | +60% min |
| roadmap | 500-800 | 800+ | +60% min |
| client_journey_map | 500-800 | 800+ | +60% min |

### Structure Improvements

**Before:**
- 1-2 paragraph fields
- ~150-200 words per field (actual GPT-4o output)

**After:**
- Markdown-structured fields with ##/### headers
- Bullet points, numbered lists, tables
- Multiple subsections (3-5 per field)
- Direct quotes with speaker attribution
- Severity scores and confidence levels
- Detailed breakdowns with metrics
- Expected output: 600-1200+ words per field

---

## Validation Results

**Workflow Status:** ✅ Active and validated

**Node Count:** 15 (unchanged)
**Connection Count:** 14 (unchanged)
**All connections:** Valid

**Validator Warnings:**
- HTTP URL warnings are false positives (validator can't see expression-based URLs)
- Workflow is fully functional

---

## Testing Notes

**Next Steps:**
1. Test with a real transcript to verify output quality
2. Measure actual word counts per field
3. Verify GPT-4o respects the new minimum requirements
4. Adjust if output still falls short (may need to be even more explicit)

**Expected Behavior:**
- Each API call should now take longer (more tokens to generate)
- Output should be 2-3x more detailed than before
- Should see markdown structure in JSON field values
- Should see direct quotes throughout
- Should see numerical scores and ratings

---

## Files Modified

**Workflow:** `QTmNH1MWW5mGBTdW` (Fathom AI Analysis v2 - Multi-Call)

**Nodes Updated (8 total):**
1. Build Prompt 1 - jsCode parameter (3,200+ characters)
2. HTTP OpenAI 1 - jsonBody parameter (temperature 0.3, max_tokens 4096)
3. Build Prompt 2 - jsCode parameter (3,100+ characters)
4. HTTP OpenAI 2 - jsonBody parameter (temperature 0.3, max_tokens 4096)
5. Build Prompt 3 - jsCode parameter (3,900+ characters)
6. HTTP OpenAI 3 - jsonBody parameter (temperature 0.3, max_tokens 4096)
7. Build Prompt 4 - jsCode parameter (4,300+ characters)
8. HTTP OpenAI 4 - jsonBody parameter (temperature 0.3, max_tokens 4096)

**Documentation:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/fathom/FATHOM_V2_PROMPT_ENHANCEMENT_2026-01-31.md`

---

## Key Requirements Added to Prompts

1. **Explicit minimum word counts** - "You MUST write AT LEAST X words"
2. **Markdown structure** - Headers (##, ###), bullets, lists, tables
3. **Direct quotes** - "Speaker: 'exact quote'" format with speaker attribution
4. **Numerical scores** - Severity (1-10), confidence (%), impact, effort, ROI
5. **Multi-level categorization** - Critical/High/Medium severity, Immediate/Short-term/Medium-term priorities
6. **Detailed subsections** - 3-5 subsections per field with specific requirements
7. **Evidence-based** - Every claim requires DIRECT QUOTE support
8. **Structured formats** - User stories, acceptance criteria, risk matrices, timeline visualizations

---

## Handoff Notes

**Status:** Ready for testing
**Workflow Active:** Yes
**Changes Applied:** 8 node updates (4 prompts + 4 HTTP configs)
**No breaking changes:** Connections unchanged, workflow structure intact

**Suggested Next Step:**
Run test-runner-agent with a real Fathom transcript to validate output quality and measure actual word counts.

