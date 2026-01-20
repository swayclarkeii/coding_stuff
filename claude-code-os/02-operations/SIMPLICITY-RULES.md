# Simplicity Rules - Keep It Lean

**Purpose:** Prevent over-organization and keep systems simple. These rules help maintain clarity and avoid unnecessary complexity.

---

## Core Rules

### 1. Two-Folder Maximum Depth
**Good:** `projects/eugene/discovery/`
**Bad:** `projects/eugene/v2/latest/discovery/phase-1/`

**Why:** Deep nesting makes files hard to find. If you need more than 2 levels, you're probably over-organizing.

---

### 2. No Version Folders
**Good:** Use git commits or file dates for versioning
**Bad:** `v1/`, `v2/`, `_old/`, `_backup/`, `archive/`

**Why:** Git already tracks versions. Version folders create confusion about which is current.

**Exception:** `reference/pdfs/` can have versioned PDF names (e.g., `v1_Research_Document.pdf`) because PDFs aren't tracked in git.

---

### 3. No Temporary Folders
**Good:** Either keep it (put it somewhere permanent) or delete it
**Bad:** `temp/`, `working/`, `scratch/`, `draft/`, `testing/`

**Why:** Temporary folders accumulate and never get cleaned up. If it's worth keeping, give it a proper home.

---

### 4. Simple Names
**Good:** `eugene`, `transcripts`, `scripts`, `reference`
**Bad:** `Eugene_Owusu_AMA_Capital_v2_Final`, `Discovery_Phase_1_Updated`, `Scripts_Working_Copy`

**Why:** Complex names are hard to type and remember. Use lowercase, hyphens for multi-word, no version numbers.

**Naming Pattern:**
- Client folders: `{client-name}` (e.g., `eugene`, `jennifer-spencer`, `lombok-invest-capital`)
- Standard folders: `discovery`, `reference`, `transcripts`, `analysis`
- Technical folders: `scripts`, `apify-configs`, `make-blueprints`

**CRITICAL: Matching Names Across Folders**
- If project is `projects/eugene/` → technical-builds is `technical-builds/eugene/`
- If project is `projects/lombok-invest-capital/` → technical-builds is `technical-builds/lombok-invest-capital/`
- **NEVER abbreviate or shorten.** Use the EXACT SAME name in both locations.

**Why this matters:**
- ✅ Easy to find related files
- ✅ No confusion about which build belongs to which project
- ✅ Consistency makes automation easier
- ✅ Claude Code can easily connect documentation to builds

---

### 5. Standard Structure Only
**For client projects:**
```
{client-name}/
├── project-brief.md
├── action-items.md
├── timeline.md
├── decisions-log.md
├── feedback-received.md
├── discovery/
│   ├── transcripts/
│   ├── analysis/
│   ├── journey/
│   └── requirements/
└── reference/
    ├── pdfs/
    └── screenshots/
```

**For technical builds:**
```
technical-builds/
├── {client-name}/              (EXACT SAME as projects/{client-name})
│   ├── scripts/
│   ├── apify-configs/
│   └── make-blueprints/
└── shared/
    ├── scripts/
    ├── configs/
    └── templates/
```

**Example - Lombok Invest Capital:**
- Projects folder: `projects/lombok-invest-capital/`
- Technical folder: `technical-builds/lombok-invest-capital/`

**Example - Eugene:**
- Projects folder: `projects/eugene/`
- Technical folder: `technical-builds/eugene/`

**Don't invent new structures.** If you need something that doesn't fit, ask: "Is this really necessary?"

---

## When Adding New Folders

Before creating a new folder, ask yourself:

### 1. Does this fit an existing pattern?
If yes → Use the existing pattern instead

**Example:**
- ❌ Creating `eugene/emails/` for email threads
- ✅ Put emails in `eugene/reference/` or `eugene/discovery/transcripts/`

### 2. Will I remember what this is in 6 months?
If no → Simplify the name or merge into existing folder

**Example:**
- ❌ `temp_analysis_working_copy/`
- ✅ Just work in `analysis/` and commit when done

### 3. Is this temporary?
If yes → Don't create a folder. Work directly, then commit or delete.

**Example:**
- ❌ Creating `draft/` folder for work-in-progress
- ✅ Work in the actual location and commit when ready

---

## Your Tendency and the Solution

**Your Tendency:** Creating too many folders and projects

**Why This Happens:**
- Desire to organize everything "perfectly"
- Fear of losing work-in-progress
- Wanting to keep multiple versions "just in case"

**The Solution:**
1. **Stick to documented patterns** (see [PROJECT-STANDARDS.md](./PROJECT-STANDARDS.md))
2. **When in doubt, keep it simpler** than your first instinct
3. **Use git for versions** instead of folder copies
4. **Delete ruthlessly** - if you haven't used it in 3 months, delete it
5. **Trust the standards** - they're designed for scalability

---

## Red Flags (Stop and Reconsider)

### 🚩 You're creating more than 3 subfolders under a single folder
**Solution:** Flatten the structure or use a different organization approach

### 🚩 You're creating a folder with "temp", "working", "draft", "old", or "backup" in the name
**Solution:** Don't. Either commit the work or delete it.

### 🚩 You're creating a folder that doesn't match the standard patterns
**Solution:** Review [PROJECT-STANDARDS.md](./PROJECT-STANDARDS.md) first. If it still doesn't fit, reconsider if you really need it.

### 🚩 You're creating parallel folder structures (v1/, v2/, latest/)
**Solution:** Use git branches or tags instead. Keep one current version in the main folder.

### 🚩 You're creating a folder just for one file
**Solution:** Put that file in an existing folder. Single-file folders are a sign of over-organization.

---

## When to Break the Rules

**Very rarely.** If you think you need to break these rules, you probably don't.

**Valid exceptions:**
1. Client explicitly requires specific structure for deliverables
2. External tool (GitHub Actions, Make.com) requires exact folder names
3. Legal/compliance requirement for document retention

**Even then:** Keep the exception isolated. Don't let it spread to the rest of your system.

---

## Benefits of Following These Rules

### For You
- ✅ Know exactly where to find things
- ✅ No "which folder is current?" confusion
- ✅ Can hand off projects easily to team
- ✅ Faster navigation and file access

### For Claude Code
- ✅ Can parse and understand structure instantly
- ✅ Knows where to look for information
- ✅ Can provide better suggestions based on patterns
- ✅ Daily planner works efficiently

### For Future Team
- ✅ Zero learning curve
- ✅ Consistent patterns = easy automation
- ✅ Clear expectations for where things go

---

## Examples: Good vs. Bad

### ❌ Bad Example (Over-Organized)
```
eugene/
├── v1_discovery/
│   ├── draft/
│   ├── final/
│   └── archive/
├── v2_discovery_updated/
│   ├── latest/
│   └── working/
├── proposal/
│   ├── draft_v1/
│   ├── draft_v2/
│   └── final/
└── temp_work/
```

**Problems:** Version folders, temp folders, deep nesting, unclear which is current

### ✅ Good Example (Simple)
```
eugene/
├── project-brief.md
├── action-items.md
├── timeline.md
├── decisions-log.md
├── feedback-received.md
├── discovery/
│   ├── transcripts/
│   └── analysis/
└── reference/
    └── pdfs/
```

**Benefits:** Flat structure, standard pattern, clear locations, git handles versions

---

## Quick Reference

| Instead of... | Do this... |
|---------------|------------|
| `v1/`, `v2/`, `final/` | Use git commits |
| `temp/`, `working/`, `draft/` | Work directly in actual location |
| `Eugene_AMA_Capital_Dec_2025/` | `eugene/` |
| `discovery/phase1/initial/drafts/` | `discovery/transcripts/` |
| `Scripts_Working_Copy_v3/` | `scripts/` |
| New custom folder type | Use existing standard pattern |

---

## Summary: The Golden Rule

**If a folder or file name requires explanation, it's too complex.**

Keep it obvious. Keep it simple. Keep it standard.

---

*When tempted to create a new folder: Stop. Read this file. Choose simplicity.*
