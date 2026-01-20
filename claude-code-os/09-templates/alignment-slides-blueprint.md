# Alignment Presentation Template Blueprint

## Overview

This blueprint defines the structure and variables for **alignment presentations** - designed for stakeholder invitation and discovery sharing, NOT sales pitching.

**Key Differences from Proposal:**
| Alignment | Proposal |
|-----------|----------|
| "Here's what we discovered" | "Here's what I'll do for you" |
| Pricing deferred/hidden | Pricing front and center |
| "Potential directions" to explore | "Solutions" as deliverables |
| "Questions for you" to invite input | "Next Steps" to close |
| Explains how we got here | Assumes context known |

**Use When:**
- Stakeholder hasn't been in prior conversations
- Need buy-in before presenting solutions
- Partnership dynamics require care
- Want to invite input, not present decisions

---

## Template Structure (8 Slides)

### Slide 1: Title
**Purpose:** Set the tone - discovery summary, not proposal

**Variables:**
```yaml
presentation_title: "Discovery Summary & Discussion"  # NOT "Automation Proposal"
client_company: "{{client_company}}"
presenter_name: "{{presenter_name}}"
presentation_date: "{{presentation_date}}"
```

**Framing:** "Discovery Summary & Discussion" signals collaboration, not sales pitch.

---

### Slide 2: How We Got Here (NEW - Alignment Only)
**Purpose:** Provide context for stakeholders who missed prior conversations

**Variables:**
```yaml
context_timeline: "{{context_timeline}}"
# Example: "Over the past two weeks (January 8-15)"

context_stakeholders: "{{context_stakeholders}}"
# Example: "Sindbad, Leonor, Madalena, and Alice"

context_summary: "{{context_summary}}"
# Example: "We explored operational challenges around invoice validation,
# data synchronization across sheets, and project tracking across Ambush's
# 50-project-per-month operation."

context_approach: "{{context_approach}}"
# Example: "Today I want to share what we discovered and get your perspective."
```

**Extraction Rules:**
- Pull from discovery call dates and attendees
- Keep summary to 25-40 words
- End with invitation for their input

---

### Slide 3: Executive Summary / Client Context
**Purpose:** Brief overview of the company and situation

**Variables:**
```yaml
client_company_description: "{{client_company_description}}"
# Example: "Ambush TV creates advertising pitch presentations for commercial directors,
# managing 50+ projects monthly with a team of 9 core people and 70-80 freelancers."

client_context_statement: "{{client_context_statement}}"
# Example: "The admin team handles bookings, project tracking, invoicing, and freelancer
# payments across multiple interconnected Google Sheets."
```

---

### Slide 4: What We Discovered
**Purpose:** Share pain points as findings, not problems to fix

**Framing Difference:**
- Proposal: "Opportunities" / "Problems We'll Solve"
- Alignment: "What We Discovered" / "Key Findings"

**Variables (3-4 discoveries):**
```yaml
discovery_1: "{{discovery_1}}"
discovery_1_description: "{{discovery_1_description}}"
discovery_1_impact: "{{discovery_1_impact}}"  # Optional - quantified impact

discovery_2: "{{discovery_2}}"
discovery_2_description: "{{discovery_2_description}}"
discovery_2_impact: "{{discovery_2_impact}}"

discovery_3: "{{discovery_3}}"
discovery_3_description: "{{discovery_3_description}}"
discovery_3_impact: "{{discovery_3_impact}}"

discovery_4: "{{discovery_4}}"  # Optional
discovery_4_description: "{{discovery_4_description}}"
discovery_4_impact: "{{discovery_4_impact}}"
```

**Extraction Rules:**
- Frame as observations/findings, not problems
- Include quantified impact where verified
- Lead with highest-value discovery (often financial)

---

### Slide 5: Potential Directions
**Purpose:** Show possible approaches without committing to solutions

**Framing Difference:**
- Proposal: "Solutions" / "What We'll Build"
- Alignment: "Potential Directions" / "Areas to Explore"

**Variables (3-4 directions):**
```yaml
direction_1: "{{direction_1}}"
direction_1_description: "{{direction_1_description}}"

direction_2: "{{direction_2}}"
direction_2_description: "{{direction_2_description}}"

direction_3: "{{direction_3}}"
direction_3_description: "{{direction_3_description}}"

direction_4: "{{direction_4}}"  # Optional
direction_4_description: "{{direction_4_description}}"
```

**Extraction Rules:**
- Use exploratory language: "could," "might," "potential"
- Don't commit to specific technical approach
- Connect each direction to a discovery

---

### Slide 6: What This Could Look Like
**Purpose:** Give sense of timeline/phases without committing

**Framing Difference:**
- Proposal: "Timeline" / "Implementation Plan"
- Alignment: "What This Could Look Like" / "If We Proceed"

**Variables:**
```yaml
phase_1_name: "{{phase_1_name}}"
phase_1_description: "{{phase_1_description}}"
phase_1_duration: "{{phase_1_duration}}"  # "4-6 weeks" not "4 weeks"

phase_2_name: "{{phase_2_name}}"
phase_2_description: "{{phase_2_description}}"
phase_2_duration: "{{phase_2_duration}}"

timeline_caveat: "{{timeline_caveat}}"
# Example: "This is a rough outline - actual approach depends on priorities we align on today."
```

**Extraction Rules:**
- Use ranges, not specific dates
- Include caveat that this depends on alignment
- Keep high-level, not detailed milestones

---

### Slide 7: Questions for You (NEW - Alignment Only)
**Purpose:** Invite stakeholder input and perspective

**Variables:**
```yaml
input_question_1: "{{input_question_1}}"
# Example: "What's your perspective on these operational challenges?"

input_question_2: "{{input_question_2}}"
# Example: "Are there other pain points I should understand?"

input_question_3: "{{input_question_3}}"
# Example: "How do you see AI/automation fitting into Ambush's direction?"

input_question_4: "{{input_question_4}}"  # Optional
# Example: "What would success look like from your view?"
```

**Extraction Rules:**
- Genuinely open-ended (not leading questions)
- At least one question about their unique perspective
- At least one question inviting additional input
- Consider their role/interests (e.g., Pierre is into AI)

---

### Slide 8: Discussion Points
**Purpose:** Frame next steps as conversation, not action items

**Framing Difference:**
- Proposal: "Next Steps" / "To Proceed"
- Alignment: "Discussion Points" / "Things to Align On"

**Variables:**
```yaml
discussion_point_1: "{{discussion_point_1}}"
# Example: "What we should prioritize first"

discussion_point_2: "{{discussion_point_2}}"
# Example: "Who else should be involved in decisions"

discussion_point_3: "{{discussion_point_3}}"
# Example: "Timeline for making decisions"

discussion_point_4: "{{discussion_point_4}}"  # Optional
# Example: "Questions or concerns to address"
```

**Extraction Rules:**
- Frame as topics for discussion, not tasks
- Include "who else should be involved" for multi-stakeholder situations
- Don't push for immediate decision

---

### Slide 9: Thank You
**Purpose:** Close warmly with appreciation

**Variables:**
```yaml
unique_client_thank_you_message: "{{unique_client_thank_you_message}}"
# Example: "Thank you for taking the time to share your perspective.
# Looking forward to continuing this conversation."

presenter_contact: "{{presenter_contact}}"
```

---

## Variable Extraction Guidelines

### For "What We Discovered" (Pain Points)

**Priority Order for Discoveries:**
1. **Financial impact** (outstanding money, error costs, revenue at risk)
2. **Time burden** (hours spent, capacity lost)
3. **Error/quality risk** (mistakes, rework, reputation)
4. **Operational friction** (delays, bottlenecks, manual work)

**Framing Rules:**
- Use observation language: "We found...", "The team described...", "Data shows..."
- Include verified numbers with source
- Don't exaggerate or dramatize

### For "Potential Directions" (Solutions)

**Mapping Discoveries to Directions:**
| Discovery Type | Direction Framing |
|---------------|-------------------|
| Financial loss/outstanding | "Collection visibility and systematic follow-up" |
| Time burden on person | "Automation to free capacity for higher-value work" |
| Manual data entry | "Single source of truth architecture" |
| Delayed invoicing | "Calendar-driven reminders and tracking" |
| Error-prone sync | "Upstream automation with validation" |

**Language to Use:**
- "Could explore..."
- "Potential approach..."
- "One direction might be..."
- "Area worth investigating..."

**Language to Avoid:**
- "We will build..."
- "The solution is..."
- "Here's what we'll deliver..."

### For "Questions for You"

**Tailor to Stakeholder:**
- **Decision-maker who missed meetings:** "What's your perspective on these challenges?"
- **Technical person:** "Are there constraints I should know about?"
- **Budget holder:** "What would make this investment worthwhile?"
- **AI enthusiast:** "How do you see AI fitting into your direction?"

---

## Ambush TV - Pierre Alignment Variables

Based on discovery materials (Jan 8-15, 2026):

### Context Variables
```yaml
context_timeline: "Over the past two weeks (January 8-15, 2026)"
context_stakeholders: "Sindbad, Leonor, Madalena, and Alice"
context_summary: "We explored operational challenges around invoice validation, data synchronization across multiple sheets, and project tracking across Ambush's 50-project-per-month operation."
context_approach: "Today I want to share what we discovered and get your perspective on these challenges and potential directions."
```

### Discovery Variables (Prioritized by Value)
```yaml
# Discovery 1: Lead with €150K (highest value)
discovery_1: "Outstanding Client Payments"
discovery_1_description: "€150,000 in outstanding client payments, with €100,000 overdue by more than 30 days. Late invoicing (often 1-2 months after project end) and no systematic follow-up contributes to slow collection."
discovery_1_impact: "Cash flow impact + awkward client conversations"

# Discovery 2: Data Interoperability (root cause of many issues)
discovery_2: "Data Doesn't Flow Between Systems"
discovery_2_description: "Information exists in 12+ sheets that don't talk to each other. Names don't match ('Dan Thomas French' vs 'Dan French'), team changes don't sync from Calendar to Dashboard, rates require triple-entry. The team described spending significant time manually transferring and verifying data."
discovery_2_impact: "5+ hours/week on manual sync and verification across admin team"

# Discovery 3: Invoice Validation Burden
discovery_3: "Invoice Validation Takes 5+ Hours Weekly"
discovery_3_description: "Sindbad manually validates 15-25 freelancer invoices each week against project hours, catching approximately 10% with errors. Each error averaging €150 requires investigation and correction."
discovery_3_impact: "22 hours/month of Sindbad's time + €150/error cost"

# Discovery 4: Month-End Pile-Up
discovery_4: "Month-End Invoicing Delays"
discovery_4_description: "No systematic reminders for project close-out. Projects end, then 1-2 months pass before hours are collected and clients are invoiced. December projects weren't fully closed until January 12th."
discovery_4_impact: "Delayed cash flow + awkward late invoice conversations"
```

### Direction Variables
```yaml
# Direction 1: Addresses Discovery 2 (Data Flow)
direction_1: "Single Source of Truth Architecture"
direction_1_description: "Data entered once, flows everywhere. Calendar → Dashboard → Project Directory → Invoicing. Names normalized. Team changes reflect automatically. Edits anywhere update everywhere."

# Direction 2: Addresses Discovery 1 + 4 (Outstanding + Delays)
direction_2: "Systematic Collection & Visibility"
direction_2_description: "Calendar-driven reminders (Day 4: collect hours, Day 7: invoice client). Aging dashboard showing who owes what, how long. Freed admin capacity to actually chase overdue payments."

# Direction 3: Addresses Discovery 3 (Invoice Validation)
direction_3: "Invoice Pre-Validation with Human Checkpoints"
direction_3_description: "Automated checks flag potential issues before Sindbad reviews. Dashboard validates hours against timesheets. Exceptions surfaced for human decision. Reduces validation time while keeping human judgment."
```

### Question Variables (Tailored to Pierre)
```yaml
input_question_1: "What's your perspective on these operational challenges?"
input_question_2: "Are there pain points from the recruitment side I should understand?"
input_question_3: "How do you see AI and automation fitting into Ambush's future direction?"
input_question_4: "What would success look like from your view?"
```

### Discussion Variables
```yaml
discussion_point_1: "Which of these challenges feels most urgent to address"
discussion_point_2: "Who else should be involved in decisions about next steps"
discussion_point_3: "Timeline for deciding how to proceed"
discussion_point_4: "Questions or concerns I can address"
```

### Thank You Variable
```yaml
unique_client_thank_you_message: "Thank you for taking the time to share your perspective. Ambush has built something impressive - looking forward to exploring how we can help it run even smoother."
```

---

## Template Configuration

**Google Slides Template ID:** `[To be created - duplicate from proposal template]`

**Slide Order:**
1. Title
2. How We Got Here (NEW)
3. Executive Summary
4. What We Discovered
5. Potential Directions
6. What This Could Look Like
7. Questions for You (NEW)
8. Discussion Points
9. Thank You

**Slides NOT Included (vs Proposal):**
- What to Expect (deliverables/responsibilities)
- Investment (pricing)
- Metrics/ROI slide

---

## Agent Instructions

### alignment-architect-agent

When generating alignment presentations:

1. **Check context:** Has stakeholder been in prior meetings? If yes, "How We Got Here" can be brief.

2. **Lead with value:** Put highest-value discovery first (usually financial).

3. **Frame as exploration:** Use "potential," "could," "might" language.

4. **Tailor questions:** Consider stakeholder's role and interests.

5. **Don't oversell:** This is invitation, not pitch.

6. **Have proposal ready:** Generate companion proposal for "back pocket" in case they ask about pricing.

### proposal-variable-extractor-agent

When extracting for alignment mode:

1. **Same sources:** Use discovery materials, transcripts, key_insights.md

2. **Different framing:** Apply alignment language rules (observation not solution)

3. **Verified numbers only:** Don't inflate or estimate

4. **Include stakeholder context:** Note who's been involved vs who hasn't
