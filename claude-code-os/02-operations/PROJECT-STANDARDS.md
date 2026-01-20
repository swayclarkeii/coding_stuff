# Project Standards - Simple & Consistent

**Purpose:** Keep project organization simple, consistent, and easy for humans and AI agents to navigate.

**Golden Rule:** If a folder or file name requires explanation, it's too complex. Keep it obvious.

---

## Standard Project Structure

Every client project follows this exact structure:

```
projects/
└── {client-name}/
    ├── project-brief.md           (1-page overview)
    ├── action-items.md            (tasks: Not Started / In Progress / Completed)
    ├── timeline.md                (milestones and dates)
    ├── decisions-log.md           (key decisions made)
    ├── feedback-received.md       (client quotes and reactions)
    ├── discovery/                 (detailed discovery docs)
    │   ├── transcripts/
    │   ├── analysis/
    │   ├── journey/
    │   └── requirements/
    └── reference/                 (PDFs, screenshots, other files)
        ├── pdfs/
        └── screenshots/
```

---

## Naming Conventions

### Client Folder Names
- **Rule:** Lowercase, use hyphens, keep short
- **Good:** `eugene`, `jennifer-spencer`, `lombok-invest-capital`
- **Bad:** `Eugene_Owusu_AMA_Capital`, `JenniferSpencer`, `Lombok Invest Capital LLC`

### Operational Files (Always the Same 5)
1. `project-brief.md` - One-page project overview
2. `action-items.md` - Task tracking
3. `timeline.md` - Key milestones
4. `decisions-log.md` - Important decisions
5. `feedback-received.md` - Client feedback and quotes

**Never rename these.** AI agents expect these exact names.

### Discovery Files
- **Folder:** `discovery/` (always lowercase)
- **Subfolders:** `transcripts/`, `analysis/`, `journey/`, `requirements/`
- **Files:** Use descriptive names with dates when relevant
  - Good: `2025-12-09_discovery_call.md`
  - Good: `key_insights.md`
  - Bad: `Eugene Discovery Call Notes Final v3 Dec.md`

### Reference Files
- **Folder:** `reference/` (always lowercase)
- **Subfolders:** `pdfs/`, `screenshots/` (only these two)
- **Files:** Keep original names for screenshots; use descriptive names for PDFs
  - Good: `Pipedrive_Stages_for_Deal.png`
  - Good: `Developer_Meeting_Doc_v1.pdf`
  - Bad: `Screenshot 2025-12-09 at 3.45.12 PM.png`

---

## What Goes Where

### Operational Files (Top Level)
**For daily use by you and AI agents.**
- Quick summaries
- Current action items
- Next steps
- Recent decisions

**Update frequency:** Weekly or after major milestones

---

### Discovery Folder
**For strategic reference and handoffs.**
- Full call transcripts
- Detailed analysis
- Business requirements
- Client journey maps

**Update frequency:** After discovery calls or major project phases

---

### Reference Folder
**For supporting documents.**
- PDFs (proposals, research, meeting docs)
- Screenshots (workflows, UI examples, diagrams)
- Other files (RTF, images, etc.)

**Update frequency:** As received from client or created

---

## Pre-Discovery Projects

If project hasn't had discovery call yet:

```
projects/
└── {client-name}/
    └── discovery/
        └── Discovery_Call_Prep.md
```

**No operational files yet.** Wait until after discovery to create the 5 standard files.

---

## File Types Allowed

### Operational & Discovery
- `.md` files ONLY (markdown)
- No PDFs, no Word docs, no presentations in these folders

### Reference Folder
- `.pdf` (proposals, meeting docs, research)
- `.png`, `.jpg` (screenshots, diagrams)
- `.rtf`, `.txt` (meeting notes if needed)
- **Keep it minimal.** Only files you'll actually reference.

---

## Why This Structure Works

### For Daily Planner Agent
- Reads the 5 operational files across all projects
- Gets status in under 30 seconds
- Suggests today's priorities

### For You
- Every project looks the same
- Know exactly where to find things
- Can hand off to team easily

### For Future Team
- Zero learning curve
- Consistent naming = easy automation
- Clear separation: operational vs. strategic vs. reference

---

## What NOT to Do

❌ **Don't create custom folders**
- Bad: `01_Latest_Discovery/`, `00_Archive/`, `v2_Updated/`
- Why: Each project should match the standard structure

❌ **Don't over-organize within folders**
- Bad: `discovery/phase-1/initial/draft-v3/`
- Why: Too many levels = confusion

❌ **Don't use version numbers in folder names**
- Bad: `discovery_v2/`, `reference_updated/`
- Why: Use git or file dates for versioning

❌ **Don't duplicate information**
- Bad: Having same info in operational AND discovery files
- Why: Creates sync issues. Operational = summary, Discovery = source of truth

❌ **Don't create "temp" or "working" folders**
- Bad: `temp/`, `working/`, `scratch/`
- Why: Either it's worth keeping (put it somewhere) or delete it

---

## Migration from Old Systems

When migrating client files from other locations:

1. **Create standard structure first** (5 operational files + discovery folder)
2. **Copy all .md files** into appropriate discovery subfolders
3. **Copy PDFs and screenshots** into reference folder
4. **Extract summaries** from discovery docs into operational files
5. **Delete old location** only after verification

**Never keep client files in multiple places.** `claude-code-os/02-operations/projects/` is the single source of truth.

---

## Examples

### Eugene (Active Project)

**projects/eugene/** (client documentation)
```
eugene/
├── project-brief.md
├── action-items.md
├── timeline.md
├── decisions-log.md
├── feedback-received.md
├── discovery/
│   ├── README.md
│   ├── NEXT_STEPS.md
│   ├── transcripts/
│   │   ├── 2025-12-01_first_discovery_call.md
│   │   └── 2025-12-09_discovery_call.md
│   ├── analysis/
│   │   ├── key_insights.md
│   │   ├── call_progression_dec1_to_dec9.md
│   │   └── comparative_analysis.md
│   ├── journey/
│   │   └── client_journey_map.md
│   └── requirements/
│       └── project_requirements.md
└── reference/
    ├── pdfs/
    │   ├── Developer_Meeting_Doc_v1.pdf
    │   ├── v3_Discovery_Questions.pdf
    │   ├── v2_Quick_Reference_Cheat_Sheet.pdf
    │   └── v1_Full_Research_Document.pdf
    └── screenshots/
        ├── Pipedrive_Stages_for_Deal.png
        ├── Opportunity_Matrix.png
        ├── Entire_SOP.png
        └── Clarification_Stage_ToDos.png
```

**technical-builds/eugene/** (future - when development starts)
```
eugene/
├── scripts/
├── apify-configs/
└── make-blueprints/
```

**Note:** Same name (`eugene`) used in both locations for consistency.

### Jennifer (Pre-Discovery)
```
jennifer-spencer/
└── discovery/
    └── Discovery_Call_Prep.md
```

### Lombok Invest Capital (Operational + Technical Builds)

**projects/lombok-invest-capital/** (client documentation)
```
lombok-invest-capital/
├── project-brief.md
├── action-items.md
├── timeline.md
├── decisions-log.md
└── feedback-received.md
```

**technical-builds/lombok-invest-capital/** (implementation files)
```
lombok-invest-capital/
├── scripts/
│   ├── FINAL_analyze_blueprint_29.py
│   ├── create_optimized_blueprint_2025-12-04.py
│   ├── create_sequential_blueprint_2025-12-04.py
│   ├── fix_aggregator_2025-12-04.py
│   └── fix_blueprint_2025-12-04.py
├── apify-configs/
│   └── (9 JSON configurations)
└── make-blueprints/
    └── (21 workflow files)
```

**Note:** Same name (`lombok-invest-capital`) used in both locations. No discovery folder because project started mid-stream.

---

## Technical Implementation Files

**Centralized in `technical-builds/` folder.**

**CRITICAL: Use EXACT SAME NAME as project folder.**
- If project is `lombok-invest-capital/` → technical-builds is `lombok-invest-capital/`
- If project is `eugene/` → technical-builds is `eugene/`
- If project is `jennifer-spencer/` → technical-builds is `jennifer-spencer/`

**Never abbreviate or shorten names.** Consistency is essential.

### Structure
```
technical-builds/
├── {client-name}/           (EXACT SAME as projects/{client-name})
│   ├── scripts/            (Python, bash, etc.)
│   ├── apify-configs/      (Apify JSON configurations)
│   └── make-blueprints/    (Make.com/n8n workflows)
└── shared/                  (reusable across clients)
    ├── scripts/
    ├── configs/
    └── templates/
```

### When to Use `shared/`
✅ **Use shared/ when:**
- Code/config is used by 2+ clients
- Generic utility scripts that aren't client-specific
- Reusable templates or starter configs

❌ **Keep in client folder when:**
- Implementation is client-specific
- Code is experimental (move to shared/ when proven)
- Custom logic that won't be reused

### Why This Works
- **For you:** All builds in one place, easy to reference
- **For Claude Code:** Can analyze patterns across clients, identify reusable components
- **For team:** Clear separation between docs (projects/) and builds (technical-builds/)

**Reason:** Client documentation = strategic context. Technical files = implementation artifacts. Both important, kept separate but accessible.

---

## Summary: The Three Rules

1. **Every project follows the same structure** (5 operational files + discovery + reference)
2. **Use simple, obvious names** (lowercase, hyphens, no versions in names)
3. **One location only** (claude-code-os is the single source of truth)

---

*Last Updated: December 10, 2024*
*These standards apply to all projects in claude-code-os/02-operations/projects/*
