# File Organization Rules

**CRITICAL: These rules MUST be followed to prevent file buildup in the root directory.**

---

## 🎯 Core Principle: Organize by PROJECT, Not by File Type

**BAD:** Having `/tests/`, `/test-reports/`, `/scripts/`, `/docs/` at root level
**GOOD:** Each project has its own `/tests/`, `/docs/`, `/scripts/` folders

---

## 📂 Root Directory - ONLY These Files Allowed

**4 Core Documentation Files:**
- `CLAUDE.md` - Main instructions
- `PROJECT_REFERENCE.md` - Project reference
- `README.md` - Repository overview
- `N8N_PATTERNS.md` - n8n technical patterns

**Everything else goes into organized folders!**

---

## 📁 Folder Structure Rules

### 1. Technical Builds → `/claude-code-os/02-operations/technical-builds/`

**Structure:**
```
/technical-builds/
├── [client-name]/
│   ├── [project-name]/
│   │   ├── documentation/
│   │   ├── tests/              ← All test files here
│   │   ├── n8n-workflows/      ← Project-specific n8n files
│   │   ├── scripts/            ← Project-specific scripts
│   │   ├── iterations/         ← Iteration logs
│   │   └── prompts/            ← Prompt improvements
```

**Examples:**
- `/technical-builds/oloxa/SwaysExpenseSystem/tests/`
- `/technical-builds/oloxa/SopBuilder/tests/`
- `/technical-builds/eugene/n8n-workflows/`

### 2. Client Projects → `/claude-code-os/02-operations/projects/`

**Structure:**
```
/projects/
├── [client-name]/
│   ├── tests/                  ← All test files here
│   ├── discovery/
│   ├── proposals/
│   ├── feedback-received.md
│   └── decisions-log.md
```

**Examples:**
- `/projects/ambush-tv/tests/` (Fathom workflow tests)
- `/projects/eugene/test-reports/`

### 3. System Documentation → `/claude-code-os/00-system-docs/`

**Only GLOBAL reference docs:**
- OAuth protocols
- MCP configuration
- Playwriter setup
- Backup procedures

### 4. Knowledge Base → `/claude-code-os/06-knowledge-base/`

**Structure:**
```
/06-knowledge-base/
├── frameworks/
│   ├── technical-frameworks/   ← N8N Agentic Framework, etc.
│   └── ai-audits/
└── patterns/
```

### 5. Utility Scripts → `/scripts/`

**ONLY truly global scripts that work across ALL projects:**
- MCP toggle scripts
- Backup scripts
- Global automation utilities

**Project-specific scripts go in project folders!**

### 6. Tools → `/tools/`

**Development tools and utilities:**
- Transcriber
- Dictation
- Notion utilities
- Video tools (Buttercut, Remotion)

### 7. Plans → `/plans/`

**Structure:**
```
/plans/
├── daily/
└── weekly/
    └── WEEKLY-SCHEDULE.md      ← Moved from root!
```

---

## 🚫 What NOT to Do

### ❌ DON'T create these at root level:
- `/tests/` - Tests go in project folders
- `/test-reports/` - Test reports go in project folders
- `/n8n-workflows/` - n8n files go in project folders
- `/iterations/` - Iterations go in project folders
- Scattered `.py`, `.sh`, `.js` files - Go in project scripts/ or /scripts/

### ❌ DON'T scatter files by type:
```
BAD:
/coding_stuff/
├── test-report-project-a.md
├── test-report-project-b.md
├── analyze-project-a.py
├── iteration-1-project-b.md
└── fix-summary-project-c.md
```

### ✅ DO organize by project:
```
GOOD:
/technical-builds/project-a/
├── tests/
│   ├── test-report-1.md
│   └── analyze.py
├── documentation/
│   └── fix-summary.md
└── iterations/
    └── iteration-1.md
```

---

## 📋 File Naming for Projects

When creating files related to a project:

1. **Identify the project** (Eugene, SopBuilder, Ambush TV, etc.)
2. **Determine the category** (test, documentation, iteration, script)
3. **Place in project folder** under appropriate subfolder

**Examples:**
- Eugene Chunk 2.5 analysis → `/technical-builds/eugene/documentation/chunk-2-5-analysis.md`
- SOP Builder test → `/technical-builds/oloxa/SopBuilder/tests/round-6-test.md`
- Expense system W6 fix → `/technical-builds/oloxa/SwaysExpenseSystem/documentation/w6-fix.md`
- Fathom workflow test script → `/projects/ambush-tv/tests/analyze_v2_output.py`

---

## 🔄 When Creating New Files

**Ask yourself these questions:**

1. **What project is this for?**
   → Find the project folder in technical-builds/ or projects/

2. **What type of file is this?**
   - Test → `/tests/` subfolder
   - Documentation → `/documentation/` subfolder
   - Script → `/scripts/` subfolder
   - Iteration/Prompt → `/iterations/` or `/prompts/` subfolder
   - n8n workflow → `/n8n-workflows/` subfolder

3. **Is this truly global?**
   - If NO → Goes in project folder
   - If YES → Goes in `/scripts/` or `/claude-code-os/00-system-docs/`

---

## 🧹 Cleanup Protocol

**If you find files in root that don't belong:**

1. **Identify project** by reading file content
2. **Move to project folder** under correct subfolder
3. **Delete if temporary/outdated**

**Monthly cleanup check:**
- Root should only have 4 MD files
- No `.py`, `.sh`, `.js`, `.json` files in root
- No scattered test reports or documentation

---

## ✅ Checklist for Claude

Before finishing ANY task:

- [ ] All test files moved to project `/tests/` folders
- [ ] All documentation moved to project `/documentation/` folders
- [ ] All scripts moved to project `/scripts/` or global `/scripts/`
- [ ] Root directory clean (only 4 core MD files)
- [ ] No temporary files (`.json`, `.py`, `.sh`) in root
- [ ] Files organized by PROJECT, not by type

---

**Remember: A clean root directory means files are where they belong - in their project folders!**
