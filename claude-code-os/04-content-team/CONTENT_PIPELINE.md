# Content Team Pipeline Documentation

## Overview

This document describes the 5-agent content pipeline for YouTube content creation, from idea to B-roll shot list.

## Pipeline Flow

```
Idea Miner (ongoing) → generates content ideas
    ↓
Idea → Hook Generator → Script Architect → Quote Finder → B-Roll Generator → Film
```

## Agents

### 1. Hook Generator Agent
**Purpose:** Find and adapt hooks from the 404-row Kallaway Hook Database

**Location:** `/.claude/agents/hook-generator-agent.md`

**When to use:** BEFORE creating a script - the hook defines the angle

**Input:**
- Topic/idea (raw brain dump is fine)
- Content type (educational, case study, story, contrarian)

**Output:**
- 3 hook options with frameworks and justifications
- Visual hook suggestions

**Run command:**
```
"Run hook generator for: [your topic]"
```

---

### 2. Script Architect Agent
**Purpose:** Turn brain dumps into structured video outlines with timing estimates

**Location:** `/.claude/agents/script-architect-agent.md`

**When to use:** AFTER selecting a hook from Hook Generator

**Input:**
- Selected hook from Hook Generator
- Brain dump / raw content ideas

**Output:**
- Structured script outline
- Timing estimates for each section
- Scripted intro/outro, bullet points for body
- Sparring notes (potential issues, alternatives)

**Run command:**
```
"Run script architect with hook: [selected hook] and brain dump: [your ideas]"
```

---

### 3. B-Roll Generator Agent
**Purpose:** Create shot lists with Kling.ai prompts for AI video generation

**Location:** `/.claude/agents/broll-generator-agent.md`

**When to use:** AFTER script is approved

**Input:**
- Script/outline from Script Architect
- Selected hook (for visual style)

**Output:**
- Shot list with 5-8 B-roll moments
- Kling.ai prompts (ready to copy-paste)
- Canva stock alternatives for each shot

**Run command:**
```
"Run B-roll generator for: [path to script]"
```

---

### 4. Idea Miner Agent (Proactive)
**Purpose:** Scan Fathom transcripts for content ideas

**Location:** `/.claude/agents/idea-miner-agent.md`

**When to use:** Weekly, or whenever you need fresh content ideas

**Input:**
- Time range (last 7 days, last 30 days)
- Optional: specific themes to look for

**Output:**
- 3-5 content ideas with source quotes
- Suggested hook categories for each
- Saved to `/04-content-team/ideas/`

**Run command:**
```
"Run idea miner for last 7 days"
```

---

### 5. Quote Finder Agent (Reactive)
**Purpose:** Search transcripts for supporting content when developing a specific video

**Location:** `/.claude/agents/quote-finder-agent.md`

**When to use:** AFTER script outline is created, to find supporting quotes

**Input:**
- Topic you're working on
- Keywords to search for
- Optional: script context

**Output:**
- Supporting quotes with sources
- Client stories that could be examples
- Suggestions for how to use each in the content

**Run command:**
```
"Run quote finder for topic: [your topic]"
```

---

## Full Pipeline Mode

To run the complete pipeline with all agents chained together:

**Agent:** `content-pipeline-workflow`
**Location:** `/.claude/agents/content-pipeline-workflow.md`

**Run command:**
```
"Run content pipeline for: [your brain dump / topic idea]"
```

**What happens:**
1. Hook Generator runs → you select from 3 options
2. Script Architect runs → you approve the outline
3. Quote Finder runs → supporting content added
4. B-Roll Generator runs → shot list created
5. Complete package saved to `/04-content-team/drafts/[topic]/`

---

## Folder Structure

```
/claude-code-os/04-content-team/
├── CONTENT_PIPELINE.md          # This documentation
├── VERSION_LOG.md               # Version history
│
├── resources/                   # Reference materials
│   ├── hooks-essential.csv     # Cleaned 404-row hook database
│   ├── Kallaway Hook Database...# Original database
│   └── [storytelling resources]
│
├── drafts/                      # Active work
│   └── [topic-slug]/           # e.g., "customer-journey-ai"
│       ├── hooks_v1.0_YYYY-MM-DD.md
│       ├── script_v1.0_YYYY-MM-DD.md
│       ├── supporting-quotes.md
│       ├── broll_v1.0_YYYY-MM-DD.md
│       ├── README.md
│       └── .archive/
│
├── ideas/                       # From Idea Miner
│   └── ideas_YYYY-MM-DD.md
│
├── published/                   # Completed videos
│   └── [video-title]/
│       ├── final-script.md
│       └── performance.md
│
└── style-references/            # Tone files (add these)
    ├── short-form-scripts.txt
    └── linkedin-examples.txt
```

---

## Hook Database

**Location:** `/04-content-team/resources/hooks-essential.csv`

**Columns:**
- `Hook` - Actual spoken hook from viral content
- `Framework` - Template with [X], [Y], [Z] placeholders
- `Category` - One of 8 hook types
- `Visual_Suggestion` - Visual style recommendation
- `Text_Suggestion` - Text/caption style
- `Views` - Original video view count

**Hook Categories (8 types):**
| Category | Count | Best For |
|----------|-------|----------|
| Educational/Tutorial | 146 | How-to, teaching |
| Secret Reveal | 117 | Insider knowledge |
| Contrarian/Negative | 48 | Hot takes, opinions |
| Raw Shock | 30 | Surprising facts |
| Question | 29 | Engaging, rhetorical |
| Experimentation | 14 | Tests, results |
| Fortuneteller | 10 | Predictions, trends |
| Comparison | 10 | Before/after, X vs Y |

---

## Versioning

**File naming:** `{component}_v{MAJOR.MINOR}_{YYYY-MM-DD}.md`

**Version increments:**
| Change | Version |
|--------|---------|
| Initial creation | v1.0 |
| Minor tweaks | v1.1, v1.2 |
| Major rewrite | v2.0 |

**Archive rule:** When version bumps to MAJOR.0, move previous to `.archive/`

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| Generate hook ideas | "Run hook generator for: [topic]" |
| Create script outline | "Run script architect with hook: [hook]" |
| Find supporting quotes | "Run quote finder for: [topic]" |
| Create B-roll shot list | "Run B-roll generator for: [script path]" |
| Mine transcripts for ideas | "Run idea miner for last 7 days" |
| Full pipeline | "Run content pipeline for: [brain dump]" |

---

## Deferred Features (Build Later)

- **LinkedIn Repurposer Agent** - Transform videos into posts
- **Researcher Agent** - Track thought leaders and trends
- **Content Review Agent** - Feedback loop from video performance

---

## Style References (Available)

Style references have been provided and organized:

**Tone Guide:**
- [x] `/style-references/TONE_GUIDE.md` - Comprehensive voice/style guide extracted from samples

**Script Samples (for tone, not topic):**
- [x] `/resources/Short-form scripts from parent coaching/` - 14 script samples
- Best examples: EP. 18 (story + reframe), EP. 24 (list + contrarian)

**Newsletter/LinkedIn Samples:**
- [x] `/resources/Newsletter/LinkedIn examples/` - Email sequences and LinkedIn posts
- Best examples: `complete-email-sequence.md`, `summer_nurture_sequence.md`

**Note:** Reference content is parenting-focused. New content will be **business, tech, and AI** - the TONE patterns apply, not the topics.
