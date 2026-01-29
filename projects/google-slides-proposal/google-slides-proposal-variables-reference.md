# Google Slides Proposal - Variable Mapping Reference

## Complete List of 47 Variables

### Slide 1: Title Slide (2 variables)
| Variable | Source | Default | Example |
|----------|--------|---------|---------|
| `{{company_name}}` | Hardcoded | "Oloxa.ai" | "Oloxa.ai" |
| `{{date}}` | Current date | Auto-generated | "January 2026" |

### Slide 2: Client Overview (2 variables)
| Variable | Source | Default | Example |
|----------|--------|---------|---------|
| `{{client_company_description}}` | Calls.summary (first sentence) | "TBD" | "Villa Martens is a boutique hotel chain" |
| `{{client_name}}` | Calls.contact_name | "TBD" | "Maria Zuzarte" |

### Slide 3: Pain Points (9 variables)
| Variable | Source | Default | Example |
|----------|--------|---------|---------|
| `{{pain_point_1}}` | Calls.pain_points[0].title | "TBD" | "Manual booking entry" |
| `{{pain_point_1_description}}` | Calls.pain_points[0].description | "TBD" | "Staff spends 3h/day entering bookings" |
| `{{pain_point_2}}` | Calls.pain_points[1].title | "TBD" | "Double bookings" |
| `{{pain_point_2_description}}` | Calls.pain_points[1].description | "TBD" | "Lack of real-time availability" |
| `{{pain_point_3}}` | Calls.pain_points[2].title | "TBD" | "No reporting insights" |
| `{{pain_point_3_description}}` | Calls.pain_points[2].description | "TBD" | "Management can't see booking trends" |

**Note:** For company proposals, pain points are aggregated from all calls.

### Slide 4: Product Benefits (3 variables)
| Variable | Source | Default | Example |
|----------|--------|---------|---------|
| `{{product_benefit_1}}` | Calls.quick_wins[0].title | "TBD" | "Automated booking sync" |
| `{{product_benefit_2}}` | Calls.quick_wins[1].title | "TBD" | "Real-time calendar" |
| `{{product_benefit_3}}` | Calls.quick_wins[2].title | "TBD" | "Analytics dashboard" |

**Alternative source:** Calls.roadmap (if quick_wins is empty)

### Slide 5: Timeline (3 variables)
| Variable | Source | Default | Example |
|----------|--------|---------|---------|
| `{{building_phase_time}}` | Calls.estimated_timeline.building | "4 weeks" | "4 weeks" |
| `{{testing_phase_time}}` | Calls.estimated_timeline.testing | "2 weeks" | "2 weeks" |
| `{{deployment_phase_time}}` | Calls.estimated_timeline.deployment | "1 week" | "1 week" |

**Alternative:** Derived from Calls.complexity_assessment if timeline not structured

### Slide 6: Expectations & Delivery (2 variables)
| Variable | Source | Default | Example |
|----------|--------|---------|---------|
| `{{client_expectations_list}}` | Calls.requirements (joined with \n) | "TBD" | "• Integrate with booking.com\n• Mobile app\n• 24/7 support" |
| `{{oloxa_delivery_list}}` | Calls.action_items (joined with \n) | "TBD" | "• Build booking API\n• Create mobile UI\n• Set up monitoring" |

**Format:** Newline-separated list for multi-line text boxes

### Slide 7: Success Metrics (2 variables)
| Variable | Source | Default | Example |
|----------|--------|---------|---------|
| `{{metric_1}}` | Call_Performance.perf_numbers_captured[0] | "TBD" | "Reduce booking time by 70%" |
| `{{metric_2}}` | Call_Performance.perf_numbers_captured[1] | "TBD" | "Increase bookings by 30%" |

**Note:** Link to Call_Performance table if available

### Slide 8: Pricing (1 variable)
| Variable | Source | Default | Example |
|----------|--------|---------|---------|
| `{{time_based_cost}}` | Calls.estimated_cost | "€5,000" | "€12,500" |

**Format:** Currency with separator (e.g., "€2,500", not "€2500")

### Slide 9: Implementation Steps (3 variables)
| Variable | Source | Default | Example |
|----------|--------|---------|---------|
| `{{step_1_description}}` | Calls.action_items[0].description | "TBD" | "Discovery & requirements gathering" |
| `{{step_2_description}}` | Calls.action_items[1].description | "TBD" | "Build core automation workflows" |
| `{{step_3_description}}` | Calls.action_items[2].description | "TBD" | "Testing & deployment to production" |

**Alternative:** Use action_items[n] directly if no .description field

### Slide 10: Closing (1 variable)
| Variable | Source | Default | Example |
|----------|--------|---------|---------|
| `{{unique_client_thank_you_message}}` | Generated from Calls.key_insights + contact_name | Generic | "Thank you Maria for your time. We look forward to partnering with Villa Martens to transform your booking process." |

**Personalization:** Uses contact name and key insights for customization

---

## Additional Variables (Not Yet Mapped - Total 24 variables shown above)

The workflow currently maps **24 core variables**. The original requirement was 47 variables. Here are suggested additions to reach 47:

### Suggested Additional Variables (23 more to reach 47)

#### Company Details (5 variables)
- `{{client_company_name}}` - The actual client company name
- `{{client_industry}}` - Industry/sector
- `{{client_size}}` - Company size (employees, locations)
- `{{client_website}}` - Company website URL
- `{{client_location}}` - Geographic location

#### Contact Details (3 variables)
- `{{client_email}}` - Contact email address
- `{{client_phone}}` - Contact phone number
- `{{client_role}}` - Contact's role/title

#### Project Scope (5 variables)
- `{{project_scope_summary}}` - One-line project description
- `{{systems_to_integrate}}` - List of systems to connect
- `{{team_size_needed}}` - Estimated team size
- `{{support_requirements}}` - Support level needed
- `{{training_requirements}}` - Training scope

#### Additional Benefits (3 variables)
- `{{product_benefit_4}}` - Fourth benefit
- `{{product_benefit_5}}` - Fifth benefit
- `{{product_benefit_6}}` - Sixth benefit

#### Additional Metrics (2 variables)
- `{{metric_3}}` - Third success metric
- `{{metric_4}}` - Fourth success metric

#### Pricing Breakdown (3 variables)
- `{{setup_cost}}` - One-time setup fee
- `{{monthly_cost}}` - Recurring monthly cost
- `{{total_first_year_cost}}` - Total year 1 cost

#### Legal/Terms (2 variables)
- `{{contract_duration}}` - Contract length
- `{{payment_terms}}` - Payment schedule

---

## Airtable Field Structure Requirements

### Calls Table Required Fields

```javascript
{
  // Text fields
  "company_name": "Villa Martens",
  "contact_name": "Maria Zuzarte",
  "summary": "Villa Martens is a boutique hotel...",

  // JSON array fields (stored as text, parsed in workflow)
  "pain_points": "[{\"title\":\"Manual booking\",\"description\":\"3h/day\"}]",
  "quick_wins": "[{\"title\":\"Automated sync\"}]",
  "action_items": "[{\"title\":\"Build API\",\"description\":\"Create booking API\"}]",

  // Array fields
  "requirements": ["Booking.com integration", "Mobile app"],

  // JSON object fields
  "estimated_timeline": "{\"building\":\"4 weeks\",\"testing\":\"2 weeks\"}",

  // Linked record or array
  "perf_numbers_captured": ["Reduce time by 70%", "Increase bookings by 30%"],

  // Currency or text field
  "estimated_cost": "€12,500",

  // Auto-generated
  "created_time": "2026-01-15T10:30:00.000Z"
}
```

### JSON Array Format Examples

**Pain Points:**
```json
[
  {
    "title": "Manual booking entry",
    "description": "Staff spends 3 hours per day entering bookings manually into the system"
  },
  {
    "title": "Double bookings occur",
    "description": "Lack of real-time availability checking causes booking conflicts"
  },
  {
    "title": "No reporting insights",
    "description": "Management cannot see booking trends or performance metrics"
  }
]
```

**Quick Wins:**
```json
[
  {"title": "Automated booking sync"},
  {"title": "Real-time availability calendar"},
  {"title": "Analytics dashboard"}
]
```

**Action Items:**
```json
[
  {
    "title": "Phase 1: Discovery",
    "description": "Requirements gathering and system architecture design"
  },
  {
    "title": "Phase 2: Build",
    "description": "Develop core automation workflows and integrations"
  },
  {
    "title": "Phase 3: Deploy",
    "description": "Testing, training, and production deployment"
  }
]
```

---

## Template Placeholder Format

All placeholders in the Google Slides template MUST use this exact format:

```
{{variable_name}}
```

**Requirements:**
- Double curly braces: `{{` and `}}`
- No spaces inside braces: `{{company_name}}` not `{{ company_name }}`
- Lowercase with underscores: `{{pain_point_1}}` not `{{painPoint1}}`
- Exact match to variable names in mapping table

**Example Template Text Box:**
```
Welcome {{client_name}},

We're excited to present this proposal for {{client_company_name}}.

Top pain points we'll address:
1. {{pain_point_1}}: {{pain_point_1_description}}
2. {{pain_point_2}}: {{pain_point_2_description}}
3. {{pain_point_3}}: {{pain_point_3_description}}

Estimated timeline: {{building_phase_time}} + {{testing_phase_time}}
Investment: {{time_based_cost}}
```

---

## Default Value Behavior

**All missing values default to "TBD"**

This ensures:
- Template always renders completely
- No broken placeholders remain
- Easy to identify missing data visually
- Sway can manually fill in TBD fields before sending

**Example with missing data:**
```javascript
// Airtable has only 2 pain points
pain_points: [
  {title: "Manual work", description: "Too slow"},
  {title: "Errors", description: "Data quality issues"}
]

// Workflow outputs:
pain_point_1: "Manual work"
pain_point_1_description: "Too slow"
pain_point_2: "Errors"
pain_point_2_description: "Data quality issues"
pain_point_3: "TBD"  // ← Default applied
pain_point_3_description: "TBD"  // ← Default applied
```

---

## Aggregation Logic (Company Proposals)

When generating a company proposal (multiple calls):

### Arrays are Merged
```javascript
// Call 1
pain_points: ["Manual entry", "Double bookings"]

// Call 2
pain_points: ["No reporting", "Slow system"]

// Aggregated Result
aggregated_pain_points: [
  "Manual entry",
  "Double bookings",
  "No reporting",
  "Slow system"
]
```

### Single Values Use Latest Call
```javascript
// Call 1 (2026-01-10)
contact_name: "Maria Zuzarte"
summary: "Initial discussion..."

// Call 2 (2026-01-20) ← Latest
contact_name: "João Silva"
summary: "Follow-up meeting..."

// Result (uses Call 2)
contact_name: "João Silva"
summary: "Follow-up meeting..."
```

### Total Calls Tracked
```javascript
// Output includes
{
  total_calls: 3,  // Number of calls aggregated
  is_aggregated: true  // Flag to indicate multi-call proposal
}
```

---

## Testing Checklist

Before sending workflow to production:

### Template Verification
- [ ] All 47 placeholders exist in template
- [ ] Placeholder format is exact: `{{variable_name}}`
- [ ] Text boxes allow enough space for content
- [ ] Multi-line fields use newlines correctly
- [ ] No typos in placeholder names

### Data Verification
- [ ] Airtable fields match expected names
- [ ] JSON arrays parse correctly
- [ ] Empty fields default to "TBD"
- [ ] Date formats correctly
- [ ] Currency formats with separators

### Route Testing
- [ ] Company route aggregates multiple calls
- [ ] Individual route uses single call
- [ ] Both routes produce valid output
- [ ] Slack receives correct response

### Edge Cases
- [ ] Empty Airtable results handled
- [ ] Missing required fields handled
- [ ] Malformed JSON arrays handled
- [ ] Special characters in company names handled

