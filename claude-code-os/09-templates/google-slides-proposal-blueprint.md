# Google Slides Proposal Blueprint

**Version:** 1.0
**Template ID:** `17BkLuHdj-iNlmnZ2jkP_cLLYMOzvTriCmejpDqe-UhQ`
**Last Updated:** 2025-12-14
**Reference Implementation:** Eugene (AMA Capital)

---

## Overview

This blueprint provides a comprehensive mapping between discovery data and Google Slides proposal template variables. It enables automatic proposal generation by extracting client discovery information and populating template variables with standardized formatting and word counts.

### Purpose
- **Input:** Client discovery documents (key_insights.md, project_requirements.md, transcripts, etc.)
- **Process:** Extract variables using defined rules
- **Output:** Complete variable map for Google Slides template population

### How to Use This Blueprint
1. Gather all discovery documents for a client project
2. Use the Variable Reference section to identify required data
3. Extract values following the extraction rules
4. Validate against word count and format requirements
5. Generate variable map (YAML/JSON)
6. Present to user for approval
7. Populate Google Slides template

---

## Template Variable Reference

### Slide 1: Title Slide

#### `{{company_name}}`
- **Data Source:** Company branding/config
- **Format:** Text, proper case
- **Word Count:** 1-3 words
- **Example (Eugene):** "Oloxa.ai"
- **Extraction Rule:** Use your company name (constant value)
- **Required:** Yes

#### `{{date}}`
- **Data Source:** Current date at proposal generation
- **Format:** "Month YYYY" (e.g., "December 2025")
- **Word Count:** 2 words
- **Example (Eugene):** "December 2025"
- **Extraction Rule:** Format current date as full month name + year
- **Required:** Yes

---

### Slide 2: Executive Summary

#### `{{client_company_description}}`
- **Data Source:** `/discovery/analysis/key_insights.md` → "One-Liner" section
- **Format:** 1-2 sentence description combining client business + goal
- **Word Count:** 25-40 words
- **Example (Eugene):** "A real estate debt advisor processing 6 deals/year aiming to scale to 15 deals by reducing 80% time on manual document processing"
- **Extraction Rule:** Extract or synthesize from "One-Liner" section - should capture:
  - What the client does (business description)
  - Current state metric
  - Desired state goal
  - Primary pain point or constraint
- **Required:** Yes

#### `{{client_name}}`
- **Data Source:** Project folder name or client name field
- **Format:** "FirstName (CompanyName)" or "CompanyName"
- **Word Count:** 2-4 words
- **Example (Eugene):** "Eugene (AMA Capital)"
- **Extraction Rule:**
  - If first name known: "FirstName (CompanyName)"
  - If only company: "CompanyName"
  - Extract from project folder structure or discovery metadata
- **Required:** Yes

---

### Slide 3: Opportunities (Pain Points)

#### `{{pain_point_1}}`
- **Data Source:** `/discovery/analysis/key_insights.md` → "Confirmed Pain Points" or "Critical Pain Point" section
- **Format:** Short heading
- **Word Count:** 2-5 words
- **Example (Eugene):** "Document Labeling Bottleneck"
- **Extraction Rule:** Extract first 2-5 words from primary pain point heading
- **Required:** Yes

#### `{{pain_point_1_description}}`
- **Data Source:** `/discovery/analysis/key_insights.md` → Pain point detail
- **Format:** Detailed description sentence
- **Word Count:** 15-25 words
- **Example (Eugene):** "Eugene spends 5-10 hours per deal manually opening, identifying, and labeling unlabeled German real estate documents"
- **Extraction Rule:** Synthesize from pain point details - must include:
  - Quantified time/cost
  - Specific action being performed
  - Impact or constraint
- **Required:** Yes

#### `{{pain_point_2}}`
- **Data Source:** `/discovery/analysis/key_insights.md` → Second pain point
- **Format:** Short heading
- **Word Count:** 2-5 words
- **Example (Eugene):** "Capacity Limitation"
- **Extraction Rule:** Extract heading from second major pain point
- **Required:** Yes

#### `{{pain_point_2_description}}`
- **Data Source:** `/discovery/analysis/key_insights.md` → Pain point detail
- **Format:** Detailed description sentence
- **Word Count:** 15-25 words
- **Example (Eugene):** "Current bottleneck prevents scaling from 6 deals per year to potential 15-20 deals annually"
- **Extraction Rule:** Synthesize from business impact section
- **Required:** Yes

#### `{{pain_point_3}}`
- **Data Source:** `/discovery/analysis/key_insights.md` → Third pain point
- **Format:** Short heading
- **Word Count:** 2-5 words
- **Example (Eugene):** "Revenue Loss"
- **Extraction Rule:** Extract heading from third pain point or business impact
- **Required:** Yes

#### `{{pain_point_3_description}}`
- **Data Source:** `/discovery/analysis/key_insights.md` → Business metrics
- **Format:** Detailed description sentence
- **Word Count:** 15-25 words
- **Example (Eugene):** "Lost opportunity of €27,000-42,000 annually due to inability to handle increased deal volume"
- **Extraction Rule:** Extract from "Business Impact" or ROI sections with specific revenue numbers
- **Required:** Yes

---

### Slide 4: Solutions

#### `{{product_benefit_1}}`
- **Data Source:** `/discovery/analysis/key_insights.md` → "Phasing Strategy" Phase 1 or `/discovery/requirements/project_requirements.md` → Phase 1 deliverables
- **Format:** Phase title or benefit heading
- **Word Count:** 3-6 words
- **Example (Eugene):** "Email Forwarding Automation"
- **Extraction Rule:** Extract Phase 1 heading or main deliverable name
- **Required:** Yes

#### `{{product_benefit_1_description}}`
- **Data Source:** Phase 1 description
- **Format:** Concise benefit description
- **Word Count:** 12-20 words
- **Example (Eugene):** "AI automatically identifies, labels, and organizes documents from forwarded emails within 5 minutes"
- **Extraction Rule:** Synthesize from Phase 1 "What" section - focus on outcome, not process
- **Required:** Yes

#### `{{product_benefit_2}}`
- **Data Source:** Phase 2 or secondary benefit
- **Format:** Phase title or benefit heading
- **Word Count:** 3-6 words
- **Example (Eugene):** "CRM Integration"
- **Extraction Rule:** Extract Phase 2 heading or second major deliverable
- **Required:** Yes

#### `{{product_benefit_2_description}}`
- **Data Source:** Phase 2 description
- **Format:** Concise benefit description
- **Word Count:** 12-20 words
- **Example (Eugene):** "Automatic PipeDrive updates with document checklists and deal status synchronization"
- **Extraction Rule:** Synthesize from Phase 2 "What" section
- **Required:** Yes

#### `{{product_benefit_3}}`
- **Data Source:** Phase 3 or tertiary benefit
- **Format:** Phase title or benefit heading
- **Word Count:** 3-6 words
- **Example (Eugene):** "Time Savings Delivery"
- **Extraction Rule:** Extract Phase 3 or summary benefit
- **Required:** Yes

#### `{{product_benefit_3_description}}`
- **Data Source:** ROI or outcome metrics
- **Format:** Concise benefit description
- **Word Count:** 12-20 words
- **Example (Eugene):** "Reduce document processing time by 80%, from 5-10 hours to 1-2 hours per deal"
- **Extraction Rule:** Extract from "Business Impact" or success metrics - must quantify outcome
- **Required:** Yes

---

### Slide 5: Timeline

#### `{{building_phase_time}}`
- **Data Source:** `/discovery/requirements/project_requirements.md` → Timeline or `/discovery/analysis/key_insights.md` → "Phasing Strategy"
- **Format:** Duration (e.g., "3 weeks", "8-12 weeks")
- **Word Count:** 2-3 words
- **Example (Eugene):** "8-12 weeks"
- **Extraction Rule:** Extract development timeline from phasing strategy
- **Required:** Yes

#### `{{building_phase_description}}`
- **Data Source:** Phase 1 timeline description
- **Format:** Short action description
- **Word Count:** 2-4 words
- **Example (Eugene):** "Core System Development"
- **Extraction Rule:** Summarize what happens during building phase
- **Required:** Yes

#### `{{deployment_phase_time}}`
- **Data Source:** Project timeline
- **Format:** Duration
- **Word Count:** 2-3 words
- **Example (Eugene):** "1-2 weeks"
- **Extraction Rule:** Extract deployment/testing period
- **Required:** Yes

#### `{{deployment_phase_description}}`
- **Data Source:** Deployment activities
- **Format:** Short action description
- **Word Count:** 2-4 words
- **Example (Eugene):** "Testing & Launch"
- **Extraction Rule:** Describe deployment activities
- **Required:** Yes

#### `{{testing_phase_time}}`
- **Data Source:** Testing timeline
- **Format:** Duration
- **Word Count:** 2-3 words
- **Example (Eugene):** "2 weeks"
- **Extraction Rule:** Extract testing period or use standard estimate
- **Required:** Yes

#### `{{testing_phase_description}}`
- **Data Source:** Testing activities
- **Format:** Short action description
- **Word Count:** 2-4 words
- **Example (Eugene):** "Real Deal Validation"
- **Extraction Rule:** Describe testing approach
- **Required:** Yes

---

### Slide 6: What to Expect

#### `{{Client_expectations_list}}`
- **Data Source:** `/discovery/requirements/project_requirements.md` → "Dependencies" or "Assumptions" section listing client responsibilities
- **Format:** Bulleted markdown list
- **Word Count:** 5-7 items, 5-10 words each
- **Example (Eugene):**
  ```
  - Provide 3-5 sample documents per type
  - Share current ChatGPT prompts and workflow
  - PipeDrive API access and credentials
  - Feedback during testing phase
  - Availability for weekly progress check-ins
  ```
- **Extraction Rule:** Extract from "Eugene provides" or "Assumptions" sections - what client must provide
- **Required:** Yes

#### `{{Client_Name}}`
- **Data Source:** Project metadata
- **Format:** Company name or first name for personalization
- **Word Count:** 1-2 words
- **Example (Eugene):** "Eugene" or "AMA Capital"
- **Extraction Rule:** Use company name or client first name for casual tone
- **Required:** Yes

#### `{{oloxa_delivery_list}}`
- **Data Source:** `/discovery/requirements/project_requirements.md` → Deliverables or Success Criteria
- **Format:** Bulleted markdown list
- **Word Count:** 5-7 items, 5-10 words each
- **Example (Eugene):**
  ```
  - Customized document intake form
  - AI-powered document identification system
  - Organized Google Drive folder structure
  - PipeDrive CRM integration
  - Weekly progress updates and demos
  - Complete system documentation
  - Post-launch support for 30 days
  ```
- **Extraction Rule:** Extract from deliverables, success criteria, or "What" sections of phasing strategy
- **Required:** Yes

---

### Slide 7: Metrics

#### `{{metric_1_title}}`
- **Data Source:** `/discovery/analysis/key_insights.md` → "Success Metrics" or "Business Impact" conservative scenario
- **Format:** Metric heading
- **Word Count:** 3-6 words
- **Example (Eugene):** "Conservative Time Savings"
- **Extraction Rule:** Label for conservative/minimum expected outcome
- **Required:** Yes

#### `{{metric_1_description}}`
- **Data Source:** Conservative metrics
- **Format:** Description with specific numbers
- **Word Count:** 15-25 words
- **Example (Eugene):** "Reduce document processing from 10 hours to 2 hours per deal, enabling capacity increase from 6 to 10 deals annually"
- **Extraction Rule:** Extract minimum expected improvement with before/after numbers
- **Required:** Yes

#### `{{metric_2_title}}`
- **Data Source:** Optimistic scenario
- **Format:** Metric heading
- **Word Count:** 3-6 words
- **Example (Eugene):** "Optimistic Capacity Growth"
- **Extraction Rule:** Label for optimistic/maximum expected outcome
- **Required:** Yes

#### `{{metric_2_description}}`
- **Data Source:** Optimistic metrics
- **Format:** Description with specific numbers
- **Word Count:** 15-25 words
- **Example (Eugene):** "Achieve 80% time reduction, processing 1-2 hours per deal, scaling to 15-20 deals with €27-42K revenue increase"
- **Extraction Rule:** Extract maximum expected improvement with revenue impact
- **Required:** Yes

#### `{{metric_additional_title}}`
- **Data Source:** Key banner metric from success criteria
- **Format:** Bold summary statement
- **Word Count:** 6-12 words
- **Example (Eugene):** "50-80% reduction in document processing time"
- **Extraction Rule:** Extract most compelling metric as headline
- **Required:** Yes

#### `{{metric_additional_description}}`
- **Data Source:** Supporting context for banner metric
- **Format:** Additional detail or context
- **Word Count:** 10-20 words
- **Example (Eugene):** "Translates to 30-48 hours saved annually at current volume, 60-80 hours at target volume"
- **Extraction Rule:** Provide context or breakdown of banner metric
- **Required:** Optional

#### `{{question_1}}`
- **Data Source:** `/discovery/analysis/key_insights.md` → "Risk Assessment" section
- **Format:** Question about potential risk or concern
- **Word Count:** 6-12 words
- **Example (Eugene):** "What if AI accuracy falls below 95%?"
- **Extraction Rule:** Convert risk into question format
- **Required:** Yes

#### `{{answer_1}}`
- **Data Source:** Risk mitigation strategies
- **Format:** Answer addressing the risk
- **Word Count:** 15-25 words
- **Example (Eugene):** "Confidence scoring flags low-accuracy identifications for manual review, with prompt engineering ensuring 95%+ target"
- **Extraction Rule:** Extract mitigation strategy from "Risk Assessment" → "Mitigation" column
- **Required:** Yes

#### `{{question_2}}`, `{{question_3}}`, `{{question_4}}`
- **Data Source:** Additional risks from risk assessment
- **Format:** Risk-based questions
- **Word Count:** 6-12 words each
- **Example (Eugene):**
  - Q2: "What if clients send scanned documents?"
  - Q3: "What if email forwarding feels cumbersome?"
  - Q4: "What about PipeDrive integration failures?"
- **Extraction Rule:** Convert top 3-4 risks into questions
- **Required:** Yes

#### `{{answer_2}}`, `{{answer_3}}`, `{{answer_4}}`
- **Data Source:** Risk mitigation strategies
- **Format:** Answers addressing risks
- **Word Count:** 15-25 words each
- **Example (Eugene):**
  - A2: "System flags scanned PDFs for manual review with OCR capability added in Phase 2"
  - A3: "One-click forwarding with email templates; portal alternative in Phase 2 if needed"
  - A4: "Abstraction layer with retry logic and manual fallback ensures no data loss"
- **Extraction Rule:** Extract mitigation for each corresponding risk
- **Required:** Yes

---

### Slide 8: Investment

#### `{{time_based_cost}}`
- **Data Source:** Calculated from hourly rate × estimated hours
- **Format:** Currency formatted (e.g., "€2,500", "$5,000")
- **Word Count:** 1-2 words
- **Example (Eugene):** "€2,500"
- **Extraction Rule:**
  - Extract hourly rate from transcripts (Eugene: €180-200/hour)
  - Multiply by estimated build hours
  - Format with currency symbol and comma separators
- **Required:** Yes

#### `{{value_based_cost}}`
- **Data Source:** Calculated from client's ROI or value metrics
- **Format:** Currency formatted
- **Word Count:** 1-2 words
- **Example (Eugene):** "€15,000"
- **Extraction Rule:**
  - Extract client's annual savings or revenue increase
  - Calculate percentage (typically 10-30% of first year value)
  - Format with currency symbol
- **Required:** Yes

#### `{{value_based_description}}`
- **Data Source:** Calculation basis explanation
- **Format:** Explanatory sentence with numbers
- **Word Count:** 10-20 words
- **Example (Eugene):** "Based on client's first year time saving at €200/hour plus 30% revenue increase value"
- **Extraction Rule:** Explain how value_based_cost was calculated - reference client's hourly rate and savings
- **Required:** Yes

#### `{{client_investment_1}}`
- **Data Source:** Client commitments or testimonial agreements
- **Format:** What client provides in exchange
- **Word Count:** 10-20 words
- **Example (Eugene):** "Client provides one video + written testimonial upon satisfaction of Phase 1"
- **Extraction Rule:** Extract from agreements or proposal terms - what client commits beyond payment
- **Required:** Yes

#### `{{client_investment_2}}`
- **Data Source:** Client time/resource commitments
- **Format:** Time or resource commitment description
- **Word Count:** 10-20 words
- **Example (Eugene):** "Client's time spent on giving feedback and testing the product's integration"
- **Extraction Rule:** Describe client's time investment during implementation
- **Required:** Yes

---

### Slide 9: Next Steps

#### `{{step_1_description}}`
- **Data Source:** Project next steps or kickoff plan
- **Format:** First action item
- **Word Count:** 6-12 words
- **Example (Eugene):** "Schedule kickoff call to finalize requirements and timeline"
- **Extraction Rule:** Extract first action from "Next Steps" section
- **Required:** Yes

#### `{{step_2_description}}`
- **Data Source:** Second action item
- **Format:** Second action item
- **Word Count:** 6-12 words
- **Example (Eugene):** "Client provides sample documents and API credentials"
- **Extraction Rule:** Extract second action - typically client deliverables
- **Required:** Yes

#### `{{step_3_description}}`
- **Data Source:** Third action item
- **Format:** Third action item
- **Word Count:** 6-12 words
- **Example (Eugene):** "Begin Phase 1 development with weekly progress updates"
- **Extraction Rule:** Extract third action - typically start of work
- **Required:** Yes

---

### Slide 10: Thank You

#### `{{unique_client_thank_you_message}}`
- **Data Source:** Memorable moment from discovery calls (transcripts) or client's expressed excitement
- **Format:** Personal callback to specific moment in discovery process
- **Word Count:** 15-30 words
- **Example (Eugene):** "From 'Are you fucking kidding me?' to building your document automation dream - excited to eliminate that 80% time drain together!"
- **Extraction Rule:**
  - Search transcripts for emotional moments or breakthrough realizations
  - Reference specific quotes or "aha moments" from discovery
  - Keep tone warm but professional
  - Alternative: Reference client's vision or stated goal in their own words
- **Required:** Yes

---

## Discovery File Structure

Expected folder organization for optimal extraction:

```
/02-operations/projects/{client_name}/discovery/
├── analysis/
│   ├── key_insights.md           # Primary source for pain points, metrics, ROI
│   ├── quick_wins.md             # Potential source for solutions/benefits
│   └── comparative_analysis.md   # Market context (optional)
├── requirements/
│   └── project_requirements.md   # Technical requirements, timeline, deliverables
├── transcripts/
│   ├── {date}_discovery_call.md  # Raw conversations, quotes, hourly rates
│   └── {date}_second_call.md     # Follow-ups, clarifications
└── journey/
    └── client_journey_map.md     # Current vs future state (optional)
```

### Required Files
1. **key_insights.md** - Critical for: pain points, business metrics, ROI, phasing strategy
2. **project_requirements.md** - Critical for: deliverables, timeline, technical details, dependencies
3. **{latest}_discovery_call.md** - Critical for: quotes, hourly rate, emotional moments

### Optional Files
- quick_wins.md - Can supplement solutions/benefits
- comparative_analysis.md - Market positioning context
- client_journey_map.md - Visual reference for current/future state

---

## Extraction Rules by Pattern

### Pattern 1: Direct Quote Extraction
**Used for:** Pain point headings, client quotes
**Process:**
1. Search for section headers in key_insights.md
2. Extract first 2-5 words as heading
3. Validate against word count limit
4. Preserve original capitalization

**Example:**
```markdown
## Critical Pain Point

### The Document Labeling Bottleneck
```
→ Extract: "Document Labeling Bottleneck"

### Pattern 2: Quantified Metric Extraction
**Used for:** Time savings, revenue impact, capacity increases
**Process:**
1. Search for numerical values in Business Impact or Success Metrics sections
2. Extract format: "{number}{unit}" or "{range}{unit}"
3. Include percentage if present
4. Maintain currency symbols

**Example:**
```markdown
**Time reduction:** 80% (5-10 hours → 1-2 hours per deal)
```
→ Extract: "80%" and "5-10 hours" and "1-2 hours"

### Pattern 3: Calculated Values
**Used for:** Pricing, ROI calculations
**Process:**
1. Extract base values (hourly rate, time saved, revenue increase)
2. Apply formula based on pricing strategy
3. Format with appropriate currency symbol
4. Round to nearest significant figure

**Example:**
```
Hourly rate: €180-200/hour (from transcript)
Build estimate: 12-18 hours
Time-based cost: 15 hours × €190/hour = €2,850 → Round to €2,500
```

### Pattern 4: List Aggregation
**Used for:** Deliverables, expectations, client requirements
**Process:**
1. Scan multiple sections (deliverables, dependencies, success criteria)
2. Aggregate into unified list
3. Format as markdown bullets
4. Ensure 5-7 items for visual balance
5. Keep each item 5-10 words

**Example:**
```markdown
From "Dependencies" section:
- Eugene provides PipeDrive API access
- Eugene provides sample documents (3-5 examples per type)

From "Success Criteria":
- Eugene feedback during testing

→ Aggregated list:
- Provide PipeDrive API access and credentials
- Share 3-5 sample documents per type
- Give feedback during testing phase
```

### Pattern 5: Synthesized Summaries
**Used for:** Client descriptions, benefit descriptions, timeline descriptions
**Process:**
1. Read full section (one-liner, phase descriptions, etc.)
2. Identify key components (what, quantity, goal, constraint)
3. Synthesize into target word count
4. Validate readability and completeness

**Example:**
```markdown
From "One-Liner":
"Eugene is trapped spending 80% of his time manually labeling unlabeled German
real estate documents, preventing him from growing from 6 to 15+ deals per year."

→ Synthesized for {{client_company_description}}:
"A real estate debt advisor processing 6 deals/year aiming to scale to 15 deals
by reducing 80% time on manual document processing"
(25 words, includes business type, current state, goal, constraint)
```

---

## Validation Rules

### Word Count Validation
For each variable, enforce word count limits:
- **Headings (2-6 words):** Pain point titles, benefit titles, metric titles
- **Descriptions (12-25 words):** Benefits, pain point details, metrics
- **Summaries (25-40 words):** Client description, executive summary
- **Lists (5-7 items):** Deliverables, expectations

**Validation Process:**
1. Count words after extraction
2. If over limit: trim while preserving meaning
3. If under minimum: add clarifying details from source
4. Flag for human review if significantly outside range

### Format Validation
- **Currency:** Must include symbol (€, $, £) and proper separator (€2,500 not €2500)
- **Dates:** Must be "Month YYYY" format (December 2025 not Dec 2025 or 12/2025)
- **Percentages:** Include % symbol (80% not 80 or 0.8)
- **Durations:** Include unit (weeks, hours, days)
- **Lists:** Markdown bullet format with consistent structure

### Required Field Validation
All variables marked "Required: Yes" must have:
1. Non-empty value
2. Value within word count range
3. Proper formatting
4. Source file reference for traceability

**If missing:**
- Flag as missing in extraction report
- Request from user before generation
- Do not proceed to Google Slides generation

---

## Eugene Project - Complete Variable Map

Reference implementation showing actual values extracted:

### Slide 1
```yaml
company_name: "Oloxa.ai"
date: "December 2025"
```

### Slide 2
```yaml
client_company_description: "A real estate debt advisor processing 6 deals/year aiming to scale to 15 deals by reducing 80% time on manual document processing"
client_name: "Eugene (AMA Capital)"
```

### Slide 3
```yaml
pain_point_1: "Document Labeling Bottleneck"
pain_point_1_description: "Eugene spends 5-10 hours per deal manually opening, identifying, and labeling unlabeled German real estate documents"
pain_point_2: "Capacity Limitation"
pain_point_2_description: "Current bottleneck prevents scaling from 6 deals per year to potential 15-20 deals annually"
pain_point_3: "Revenue Loss"
pain_point_3_description: "Lost opportunity of €27,000-42,000 annually due to inability to handle increased deal volume"
```

### Slide 4
```yaml
product_benefit_1: "Email Forwarding Automation"
product_benefit_1_description: "AI automatically identifies, labels, and organizes documents from forwarded emails within 5 minutes"
product_benefit_2: "PipeDrive CRM Integration"
product_benefit_2_description: "Automatic deal updates with document checklists and status synchronization"
product_benefit_3: "80% Time Savings"
product_benefit_3_description: "Reduce document processing from 5-10 hours to 1-2 hours per deal"
```

### Slide 5
```yaml
building_phase_time: "8-12 weeks"
building_phase_description: "Core system development"
deployment_phase_time: "1-2 weeks"
deployment_phase_description: "Testing and launch"
testing_phase_time: "2 weeks"
testing_phase_description: "Real deal validation"
```

### Slide 6
```yaml
Client_expectations_list: |
  - Provide 3-5 sample documents per type
  - Share current ChatGPT prompts and workflow
  - PipeDrive API access and credentials
  - Feedback during testing phase
  - Availability for weekly progress check-ins

Client_Name: "Eugene"

oloxa_delivery_list: |
  - Customized document intake form
  - AI-powered document identification system
  - Organized Google Drive folder structure
  - PipeDrive CRM integration
  - Weekly progress updates and demos
  - Complete system documentation
  - 30 days post-launch support
```

### Slide 7
```yaml
metric_1_title: "Conservative Time Savings"
metric_1_description: "Reduce processing from 10 hours to 2 hours per deal, enabling 6 to 10 deals annually"
metric_2_title: "Optimistic Capacity Growth"
metric_2_description: "Achieve 80% time reduction, scaling to 15-20 deals with €27-42K revenue increase annually"
metric_additional_title: "50-80% reduction in document processing time"
metric_additional_description: "Translates to 30-48 hours saved annually at current volume, 60-80 hours at target capacity"

question_1: "What if AI accuracy falls below 95%?"
answer_1: "Confidence scoring flags low-accuracy identifications for manual review with prompt engineering ensuring target"

question_2: "What if clients send scanned documents?"
answer_2: "System flags scanned PDFs for manual review with OCR capability added in Phase 2"

question_3: "What if email forwarding feels cumbersome?"
answer_3: "One-click forwarding with templates; client portal alternative available in Phase 2"

question_4: "What about PipeDrive integration failures?"
answer_4: "Abstraction layer with retry logic and manual fallback ensures no data loss"
```

### Slide 8
```yaml
time_based_cost: "€2,500"
value_based_cost: "€15,000"
value_based_description: "Based on client's first year time savings at €200/hour plus revenue increase value"
client_investment_1: "Client provides one video + written testimonial upon satisfaction of Phase 1"
client_investment_2: "Client's time spent on giving feedback and testing the product's integration"
```

### Slide 9
```yaml
step_1_description: "Schedule kickoff call to finalize requirements"
step_2_description: "Client provides sample documents and API access"
step_3_description: "Begin Phase 1 development with weekly updates"
```

### Slide 10
```yaml
unique_client_thank_you_message: "From 'Are you fucking kidding me?' to building your document automation dream - excited to eliminate that 80% time drain together!"
```

---

## Customization Guide

### Adding New Variables
1. Add variable to appropriate slide section
2. Define all required fields:
   - Data Source (file path + section)
   - Format
   - Word Count
   - Example
   - Extraction Rule
   - Required status
3. Update extraction pattern reference if new pattern needed
4. Add example value to Eugene reference map
5. Test extraction with real discovery data

### Modifying Extraction Rules
1. Document reason for change
2. Update rule in appropriate section
3. Re-test with Eugene project data
4. Validate output quality
5. Update version number if significant change

### Creating Custom Templates
1. Copy this blueprint as starting point
2. Identify all variables in new template
3. Map to discovery sources (reuse existing where possible)
4. Define new extraction rules for unique variables
5. Create reference implementation
6. Validate with at least 2 client projects

---

## Version History

### v1.0 (2025-12-14)
- Initial blueprint creation
- 40+ variables documented across 10 slides
- Eugene (AMA Capital) reference implementation
- 5 extraction patterns defined
- Complete variable map included
