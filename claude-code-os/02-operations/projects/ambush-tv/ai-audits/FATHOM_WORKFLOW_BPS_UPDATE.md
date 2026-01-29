# Fathom Workflow BPS Prompt Update

**Date:** 2026-01-28
**Workflow ID:** cMGbzpq1RXpL0OHY
**Workflow Name:** Fathom Transcript Workflow Final_22.01.26

## Overview

Updated the AI prompt nodes in the Fathom transcript processing workflow with new BPS-compliant (Best Prompt Structure) prompts. This improves the quality and consistency of AI analysis for discovery call transcripts.

## Changes Made

### 1. Enhanced AI Analysis Node (Client Insights)

**Node Name:** Enhanced AI Analysis
**Node ID:** enhanced-ai-analysis
**Node Type:** n8n-nodes-base.set

**Updated:** The `aiPrompt` parameter with BPS-structured prompt including:
- Clear Role definition (Client Insights Analysis System)
- Step-by-step Task breakdown (Identify → Categorize → Quantify → Prioritize → Extract → Map → Synthesize)
- Specific output format requirements (JSON with 8 required fields)
- Quantification rules with examples
- Context explaining system importance
- Real-world examples (strong vs weak discovery calls)
- Guardrails and edge cases

**Key Improvements:**
- More systematic extraction of pain points
- Better quantification guidance (numbers, estimates, annual values)
- Clearer JSON output structure
- Professional tone with markdown formatting
- Explicit instructions for citing quotes

### 2. Build Performance Prompt Node (Call Quality)

**Node Name:** Build Performance Prompt
**Node ID:** build-performance-prompt
**Node Type:** n8n-nodes-base.set

**Updated:** The `performancePrompt` parameter with BPS-structured prompt including:
- Clear Role definition (Meeting Performance Analysis System)
- 8-step evaluation process (Assess → Analyze → Identify → Evaluate → Detect → Quantify → Map → Recommend)
- Scoring rubric (0-100 scale with specific adjustment rules)
- Complexity assessment criteria (Low/Medium/High)
- Context explaining coaching/qualification importance
- Real-world examples (excellent 92-score call vs fair 68-score call)
- Objectivity principles and calibration guidance

**Key Improvements:**
- Data-driven scoring (not enthusiasm-based)
- Clear complexity definitions with thresholds
- Phase-based roadmap generation
- Specific improvement recommendations
- JSON validation requirements

## Validation Results

**Workflow Status:** Valid ✅
- Total Nodes: 39
- Enabled Nodes: 33
- Valid Connections: 35
- Errors: 0
- Warnings: 56 (pre-existing, unrelated to prompt changes)

## Testing Recommendations

1. **Test with sample transcript** - Run a known discovery call through the workflow
2. **Verify JSON output** - Ensure both AI nodes return valid JSON with all required fields
3. **Check quantification** - Confirm pain points include numbers/estimates
4. **Review scoring** - Validate performance scores align with data quality (not enthusiasm)
5. **Compare before/after** - Run same transcript with old vs new prompts to see improvements

## Next Steps

1. Monitor first 5-10 executions for JSON parsing errors
2. Review AI outputs for quality improvements
3. Adjust temperature or model if needed (currently gpt-4o at 0.3 temp)
4. Consider adding error handling for JSON parse failures

## Implementation Notes

- Both prompts now follow BPS (Best Prompt Structure) framework
- Role → Task → Specifics → Context → Examples → Notes
- Prompts are stored in Set nodes, then referenced by OpenAI nodes
- No changes to workflow structure or connections
- Updates applied successfully via `n8n_update_partial_workflow`

## Files Modified

- Workflow: `cMGbzpq1RXpL0OHY` (Fathom Transcript Workflow Final_22.01.26)
  - Node: Enhanced AI Analysis (aiPrompt parameter)
  - Node: Build Performance Prompt (performancePrompt parameter)
