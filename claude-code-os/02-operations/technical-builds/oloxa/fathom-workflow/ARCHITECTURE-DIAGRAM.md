# Fathom Workflow Multi-Call AI Architecture

## Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Enhanced AI Analysis (Set Node)                   │
│                                                                           │
│  Outputs:                                                                 │
│    • company_name (extracted from email)                                 │
│    • ai_prompt_discovery (for Call 1)                                    │
│    • ai_prompt_opportunity (for Call 2)                                  │
│    • ai_prompt_technical (for Call 3)                                    │
│    • ai_prompt_strategic (for Call 4)                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
        ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
        │  Call 1: GPT-4o│ │  Call 2: GPT-4o│ │  Call 3: GPT-4o│
        │   Discovery    │ │  Opportunity   │ │   Technical    │
        └───────────────┘ └───────────────┘ └───────────────┘
                    │               │               │
                    ▼               ▼               ▼
        ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
        │Parse Discovery│ │Parse Opportun.│ │Parse Technical│
        │                │ │                │ │                │
        │ • summary      │ │ • quick_wins   │ │ • complexity   │
        │ • key_insights │ │ • pricing      │ │ • requirements │
        │ • pain_points  │ │                │ │                │
        │ • action_items │ │                │ │                │
        └───────────────┘ └───────────────┘ └───────────────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    │
                    ┌───────────────┘
                    │
                    ▼
        ┌───────────────┐
        │  Call 4: GPT-4o│
        │   Strategic    │
        └───────────────┘
                    │
                    ▼
        ┌───────────────┐
        │Parse Strategic│
        │                │
        │ • roadmap      │
        │ • journey_map  │
        └───────────────┘
                    │
                    ▼
        ┌─────────────────────────────────────────────┐
        │          Merge All Analysis (Code Node)      │
        │                                              │
        │  Aggregates all 10 fields + metadata:        │
        │    1. summary                                │
        │    2. key_insights                           │
        │    3. pain_points                            │
        │    4. action_items                           │
        │    5. quick_wins                             │
        │    6. pricing_strategy                       │
        │    7. complexity_assessment                  │
        │    8. requirements                           │
        │    9. roadmap                                │
        │   10. client_journey_map                     │
        │   + company_name, meeting metadata           │
        └─────────────────────────────────────────────┘
                    │
        ┌───────────┴──────────┐
        │                      │
        ▼                      ▼
┌──────────────┐    ┌──────────────────┐
│Build Perform.│    │Merge Search Data │
│Prompt        │    │                  │
└──────────────┘    └──────────────────┘
        │                      │
        ▼                      ▼
   (Performance            (Airtable
    Analysis Path)          Preparation)
```

## Parallel Execution Timeline

```
Time →
────────────────────────────────────────────────────────────────

Enhanced AI Analysis: [■] (instant - Set node)
                       │
                       ├─────────────────────────────────────┐
                       │                                     │
Call 1: Discovery:     [■■■■■■■■■■■■■■■] (GPT-4o)          │
Call 2: Opportunity:   [■■■■■■■■■■■■■■■] (GPT-4o)          │ PARALLEL
Call 3: Technical:     [■■■■■■■■■■■■■■■] (GPT-4o)          │
Call 4: Strategic:     [■■■■■■■■■■■■■■■] (GPT-4o)          │
                       │                                     │
                       └─────────────────────────────────────┘
                                     │
Parse 1: Discovery:                  [■] (instant)
Parse 2: Opportunity:                [■] (instant)
Parse 3: Technical:                  [■] (instant)
Parse 4: Strategic:                  [■] (instant)
                                     │
Merge All Analysis:                  [■] (instant - Code node)
                                     │
                                     ▼
                              (Downstream continues)

Total Time ≈ Time of longest GPT-4o call (not sum of all 4)
```

## Data Structure Flow

### Input to Enhanced AI Analysis
```json
{
  "meeting_title": "Discovery Call - Acme Corp",
  "meeting_date": "2026-01-30",
  "contact_name": "John Doe",
  "contact_email": "john@acmecorp.com",
  "combined_transcript": "Full transcript text..."
}
```

### Output from Enhanced AI Analysis
```json
{
  "company_name": "Acmecorp",
  "ai_prompt_discovery": "You are an expert...\nTranscript: {{transcript}}",
  "ai_prompt_opportunity": "Analyze for opportunities...\nTranscript: {{transcript}}",
  "ai_prompt_technical": "Analyze complexity...\nTranscript: {{transcript}}",
  "ai_prompt_strategic": "Create roadmap...\nTranscript: {{transcript}}"
}
```

### Output from Parse Discovery Response
```json
{
  "summary": "Executive summary markdown...",
  "key_insights": "Comprehensive analysis markdown...",
  "pain_points": "Detailed pain points markdown...",
  "action_items": "Action items checklist markdown...",
  "meeting_title": "Discovery Call - Acme Corp",
  "meeting_date": "2026-01-30",
  "contact_name": "John Doe",
  "contact_email": "john@acmecorp.com"
}
```

### Output from Parse Opportunity Response
```json
{
  "quick_wins": "Priority opportunities markdown...",
  "pricing_strategy": "Pricing analysis markdown...",
  "meeting_title": "Discovery Call - Acme Corp",
  "meeting_date": "2026-01-30",
  "contact_name": "John Doe",
  "contact_email": "john@acmecorp.com"
}
```

### Output from Parse Technical Response
```json
{
  "complexity_assessment": "Component breakdown markdown...",
  "requirements": "Requirements document markdown...",
  "meeting_title": "Discovery Call - Acme Corp",
  "meeting_date": "2026-01-30",
  "contact_name": "John Doe",
  "contact_email": "john@acmecorp.com"
}
```

### Output from Parse Strategic Response
```json
{
  "roadmap": "6-12 month roadmap markdown...",
  "client_journey_map": "Client journey documentation markdown...",
  "meeting_title": "Discovery Call - Acme Corp",
  "meeting_date": "2026-01-30",
  "contact_name": "John Doe",
  "contact_email": "john@acmecorp.com"
}
```

### Output from Merge All Analysis (Final)
```json
{
  "summary": "Executive summary markdown...",
  "key_insights": "Comprehensive analysis markdown...",
  "pain_points": "Detailed pain points markdown...",
  "action_items": "Action items checklist markdown...",
  "quick_wins": "Priority opportunities markdown...",
  "pricing_strategy": "Pricing analysis markdown...",
  "complexity_assessment": "Component breakdown markdown...",
  "requirements": "Requirements document markdown...",
  "roadmap": "6-12 month roadmap markdown...",
  "client_journey_map": "Client journey documentation markdown...",
  "company_name": "Acmecorp",
  "meeting_title": "Discovery Call - Acme Corp",
  "meeting_date": "2026-01-30",
  "contact_name": "John Doe",
  "contact_email": "john@acmecorp.com"
}
```

## Field Mapping to Airtable

```
Merge All Analysis Output → Airtable Calls Table
═══════════════════════════════════════════════════

meeting_title          → Title (with contact_name)
meeting_date           → Date
contact_email          → Contact
company_name           → Company ⭐ NEW
(auto-detected)        → Call Type
(from upstream)        → Transcript Link

summary                → Summary
key_insights           → Key Insights
pain_points            → Pain Points
action_items           → Action Items
quick_wins             → Quick Wins ⭐ NEW
pricing_strategy       → Pricing Strategy ⭐ NEW
complexity_assessment  → Complexity Assessment ⭐ NEW
requirements           → Requirements ⭐ NEW
roadmap                → Roadmap ⭐ NEW
client_journey_map     → Client Journey Map ⭐ NEW

(from separate path)   → Performance Score
(from separate path)   → Improvement Areas
```

## Node Positions (Visual Layout)

```
Y-axis (vertical)
↓
64px   Enhanced AI Analysis ───┐
                                │
136px  Call AI: Discovery ──────┤
264px  Call AI: Opportunity ────┤ ← 4 parallel calls
392px  Call AI: Technical ──────┤
520px  Call AI: Strategic ──────┘
                                │
64px   Parse Discovery ─────────┤
264px  Parse Opportunity ───────┤ ← 4 parsers
392px  Parse Technical ─────────┤
520px  Parse Strategic ─────────┘
                                │
280px  Merge All Analysis ──────┘ ← Single merge point
                                │
                                ▼
                          (Downstream)
```

## Error Handling Strategy

```
Each AI Call Node:
  ├─ retryOnFail: true (3 attempts)
  ├─ waitBetweenTries: 5000ms
  ├─ continueOnFail: true
  └─ If fails → empty fields in that category

Parsers:
  ├─ 6-tier JSON parsing
  ├─ Fallback to empty strings
  └─ Never blocks workflow

Merge Node:
  ├─ Aggregates all available data
  ├─ Handles missing fields gracefully
  └─ Extracts company_name as fallback
```

## Performance Characteristics

| Metric | Before | After |
|--------|--------|-------|
| AI Model | GPT-4o-mini | GPT-4o (4x) |
| Number of Calls | 1 | 4 (parallel) |
| Execution Time | ~30s | ~30-40s (parallel) |
| Token Cost | Low | 4x higher but parallel |
| Output Fields | 6 basic | 10 detailed |
| Analysis Depth | Basic | Expert-level |
| Company Field | No | Yes (auto-extracted) |
| Format Quality | Mixed | Pre-formatted markdown |

## Benefits of Multi-Call Architecture

1. **Specialization:** Each call focuses on one domain (Discovery, Opportunity, Technical, Strategic)
2. **Depth:** More detailed prompts per domain = better output quality
3. **Parallel Execution:** Time = longest call, not sum of all calls
4. **Resilience:** One call failing doesn't block others
5. **Extensibility:** Easy to add/modify individual analysis types
6. **Cost Efficiency:** Parallel execution means no extra wall-clock time
7. **Maintenance:** Each prompt can be updated independently
