# BPS Prompting Framework - Blank Template

**Version:** 1.0
**Date:** 2026-01-28
**Purpose:** Reusable template for creating BPS-compliant prompts for any domain

---

## How to Use This Template

1. **Copy this entire template**
2. **Replace all [PLACEHOLDER] text** with your specific content
3. **Follow the structure exactly** - do not skip or reorder sections
4. **Validate compliance** using the checklist at the end

---

## Template Structure

```markdown
# Role

You are [SYSTEM_NAME], an expert [DOMAIN] [ROLE_TYPE].
You specialize in [CORE_COMPETENCY] with [METHOD/APPROACH].

Your expertise combines [SKILL_1], [SKILL_2], and [SKILL_3] to ensure [PRIMARY_OUTCOME].

You act as [RELATIONSHIP_TO_USER] — [HOW_YOU_OPERATE_DESCRIPTION].

---

# Task

Your core task is to [MAIN_OBJECTIVE].

Follow this process:

1. [ACTION_1] — [DESCRIPTION_1]
2. [ACTION_2] — [DESCRIPTION_2]
3. [ACTION_3] — [DESCRIPTION_3]
4. [ACTION_4] — [DESCRIPTION_4]
5. [ACTION_5] — [DESCRIPTION_5]
6. [ACTION_6] — [DESCRIPTION_6]
7. [ACTION_7] — [DESCRIPTION_7]

At every stage, [KEY_OPERATING_PRINCIPLES].

---

# Specifics

**[CONSTRAINT_CATEGORY_1]:**
[DETAILS_AND_RULES]

**[CONSTRAINT_CATEGORY_2]:**
[DETAILS_AND_RULES]

**Scope:**
- [WHAT_IS_INCLUDED]
- [WHAT_IS_EXCLUDED]

**Deliverables:**
- **[OUTPUT_1]** — [DESCRIPTION_OF_OUTPUT_1]
- **[OUTPUT_2]** — [DESCRIPTION_OF_OUTPUT_2]
- **[OUTPUT_3]** — [DESCRIPTION_OF_OUTPUT_3]

**[RULES_CATEGORY]:**
- [RULE_1]
- [RULE_2]
- [RULE_3]

**Language & Tone:**
- [FORMATTING_REQUIREMENT_1]
- [FORMATTING_REQUIREMENT_2]
- [STYLE_GUIDELINE]

---

# Context

This system prompt governs [PROJECT_NAME], [PURPOSE_DESCRIPTION].

It exists to ensure [PRIMARY_GOAL] and to [SECONDARY_GOAL] through [METHOD].

The system operates in [MODE_DESCRIPTION]:
- [MODE_1]: [DESCRIPTION]
- [MODE_2]: [DESCRIPTION]

Your role is pivotal — the [QUALITY_ATTRIBUTES] of your [OUTPUTS] directly determine [ORGANIZATIONAL_IMPACT].

By [KEY_ACTION], you ensure [DESIRED_ORGANIZATIONAL_OUTCOME].

---

# Examples

### Example 1: [SCENARIO_TITLE_1]

**Input:**
```
[EXAMPLE_INPUT_1]
```

**System Response:**

[EXPECTED_OUTPUT_STRUCTURE_1]

---

### Example 2: [SCENARIO_TITLE_2]

**Input:**
```
[EXAMPLE_INPUT_2]
```

**System Response:**

[EXPECTED_OUTPUT_STRUCTURE_2]

---

### Example 3: [EDGE_CASE_SCENARIO]

**[EDGE_CASE_DESCRIPTION]**

[HOW_TO_HANDLE_EDGE_CASE]

---

# Notes

**[KEY_PRINCIPLE_1]:**
[EXPLANATION_AND_ENFORCEMENT_DETAILS]

**[KEY_PRINCIPLE_2]:**
[EXPLANATION_AND_ENFORCEMENT_DETAILS]

**[KEY_PRINCIPLE_3]:**
[EXPLANATION_AND_ENFORCEMENT_DETAILS]

**Training/Iteration Cadence:**
[HOW_SYSTEM_IMPROVES_OVER_TIME]

**Guardrails:**
- Never [CONSTRAINT_1]
- Never [CONSTRAINT_2]
- Never [CONSTRAINT_3]
- Always [REQUIREMENT_1]
- Always [REQUIREMENT_2]
- Maintain [STANDARD_TO_UPHOLD]

**Edge Case Handling:**
- [EDGE_CASE_TYPE_1]: [HOW_TO_HANDLE]
- [EDGE_CASE_TYPE_2]: [HOW_TO_HANDLE]
- [EDGE_CASE_TYPE_3]: [HOW_TO_HANDLE]
```

---

## Compliance Checklist

Before finalizing your prompt, verify:

- [ ] **Role Section**
  - [ ] Includes confidence descriptors (expert, visionary, analytical, etc.)
  - [ ] Specifies domain expertise
  - [ ] Describes operational approach
  - [ ] Establishes relationship dynamic

- [ ] **Task Section**
  - [ ] Clear action sequence (numbered steps)
  - [ ] Each step has description
  - [ ] Steps follow logical progression
  - [ ] Operating principles stated

- [ ] **Specifics Section**
  - [ ] Constraints clearly defined
  - [ ] Scope boundaries set (included/excluded)
  - [ ] Deliverables listed with descriptions
  - [ ] Rules/guidelines provided
  - [ ] Language & tone specified

- [ ] **Context Section**
  - [ ] Explains project purpose
  - [ ] Links to organizational goals
  - [ ] Describes operational modes
  - [ ] States why accuracy matters
  - [ ] Shows impact of outputs

- [ ] **Examples Section**
  - [ ] At least 2-3 concrete examples
  - [ ] Shows input → output format
  - [ ] Includes edge case handling
  - [ ] Demonstrates proper structure

- [ ] **Notes Section**
  - [ ] Key principles reinforced
  - [ ] Guardrails clearly stated
  - [ ] Edge cases addressed
  - [ ] Training/iteration described
  - [ ] Constraints repeated from top

---

## Common Placeholders Guide

### Role Section
- `[SYSTEM_NAME]`: Name of the system/agent (e.g., "Transcript Analysis System", "Invoice Validator")
- `[DOMAIN]`: Field of expertise (e.g., "business analysis", "data validation")
- `[ROLE_TYPE]`: Type of role (e.g., "analyst", "evaluator", "processor")
- `[CORE_COMPETENCY]`: Main skill (e.g., "extracting actionable insights", "detecting errors")
- `[METHOD/APPROACH]`: How it works (e.g., "systematic analysis", "pattern recognition")
- `[SKILL_1/2/3]`: Specific capabilities (e.g., "strategic thinking", "problem identification")
- `[PRIMARY_OUTCOME]`: What it achieves (e.g., "accurate business intelligence", "zero errors")
- `[RELATIONSHIP_TO_USER]`: How it interacts (e.g., "advisor", "quality checker", "assistant")
- `[HOW_YOU_OPERATE_DESCRIPTION]`: Operational style (e.g., "systematically enforcing standards while training the team")

### Task Section
- `[MAIN_OBJECTIVE]`: Overall goal (e.g., "analyze meeting transcripts and extract structured data")
- `[ACTION_X]`: Verb-based step (e.g., "Extract", "Categorize", "Validate")
- `[DESCRIPTION_X]`: What happens in that step (e.g., "Read transcript for pain points")
- `[KEY_OPERATING_PRINCIPLES]`: How to behave (e.g., "maintain accuracy, prioritize clarity")

### Specifics Section
- `[CONSTRAINT_CATEGORY_X]`: Type of rule (e.g., "Data Format", "Output Structure")
- `[OUTPUT_X]`: What gets delivered (e.g., "JSON file", "Summary report")
- `[RULES_CATEGORY]`: Type of rules (e.g., "Validation Rules", "Quality Standards")

### Context Section
- `[PROJECT_NAME]`: Name of initiative (e.g., "Fathom Transcript Analysis Pipeline")
- `[PURPOSE_DESCRIPTION]`: Why it exists (e.g., "automated client insight extraction")
- `[PRIMARY_GOAL]`: Main objective (e.g., "accurate CRM data population")
- `[ORGANIZATIONAL_IMPACT]`: Business effect (e.g., "proposal win rate", "time savings")

---

## Usage Examples

**For Transcript Analysis:**
- `[SYSTEM_NAME]`: "Transcript Analysis System"
- `[DOMAIN]`: "business analysis"
- `[ROLE_TYPE]`: "discovery call interpreter"
- `[MAIN_OBJECTIVE]`: "analyze meeting transcripts and extract structured business intelligence"

**For Invoice Validation:**
- `[SYSTEM_NAME]`: "Invoice Validation System"
- `[DOMAIN]`: "financial analysis"
- `[ROLE_TYPE]`: "error detection specialist"
- `[MAIN_OBJECTIVE]`: "validate invoices against project data and flag discrepancies"

**For Email Classification:**
- `[SYSTEM_NAME]`: "Email Classification System"
- `[DOMAIN]`: "natural language processing"
- `[ROLE_TYPE]`: "message categorizer"
- `[MAIN_OBJECTIVE]`: "classify incoming emails by intent and route to appropriate workflow"

---

## Best Practices

1. **Be Specific** - Replace ALL placeholders with concrete details
2. **Be Complete** - Don't skip sections or leave placeholders
3. **Be Consistent** - Use same terminology throughout
4. **Be Actionable** - Task steps should be verb-based actions
5. **Be Realistic** - Examples should use real/representative data
6. **Be Clear** - Avoid jargon without explanation
7. **Be Thorough** - Include edge cases and failure modes

---

## Anti-Patterns (Avoid These)

❌ Skipping sections ("I don't need Context")
❌ Vague roles ("You are helpful")
❌ Generic tasks ("Do your best")
❌ No examples ("User will figure it out")
❌ Missing guardrails ("Just be careful")
❌ Incomplete specifics ("Output should be good")

---

*Template Version: 1.0*
*Created: 2026-01-28*
*Location: `/claude-code-os/06-knowledge-base/frameworks/`*
