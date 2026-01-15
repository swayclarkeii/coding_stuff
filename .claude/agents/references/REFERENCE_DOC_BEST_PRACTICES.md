---
name: Reference Doc Best Practices
description: Best practices for creating and maintaining technical reference documentation
---

# Reference Document Best Practices

## Purpose

This document explains how to create and use reference documents that agents will actually follow.

---

## The Problem This Document Was Created From

**Original Issue:**
- solution-builder-agent and architecture-feasibility-agent were suggesting n8n operations that don't exist
- Example: Suggesting "List files" for Google Drive when only "Search" operation exists
- Caused wasted time and incorrect workflow designs

**Root Cause:**
- Agents were guessing operation names instead of verifying
- No quick reference to check exact operation names
- Had to call expensive MCP tools for simple operation validation

---

## Core Principles for Reference Documents

### 1. One Purpose Per Document

**✅ GOOD:**
- `N8N_NODE_REFERENCE.md` - Lists exact operations for common nodes
- `N8N_IMPLEMENTATION_PATTERNS.md` - Code examples and debugging patterns
- `OAUTH_REFRESH_PROTOCOL.md` - OAuth refresh procedures

**❌ BAD:**
- `N8N_EVERYTHING.md` - Mixes operations, patterns, debugging, OAuth, and more
- Too long, agents won't read it fully
- Hard to find specific information quickly

**Rule:** If a document serves multiple purposes, split it.

### 2. Front-Load Critical Information

**Document structure:**
```markdown
# Title - What This Doc Does (1 line)

**CRITICAL RULE:** The most important thing (1-2 lines)

## Quick Reference (What agents need 80% of the time)
[Core information here - ~50-100 lines max]

---

## Additional Details (If needed)
[Extended information that's helpful but not always needed]
```

**Why this works:**
- Agents scan top of document first
- If critical info is at line 500, they might miss it
- Quick reference should answer most questions without scrolling

### 3. Use Scannable Format

**✅ GOOD - Easy to scan:**
```markdown
## Google Drive Operations

### File Resource
- **Copy** - Copy a file
- **Delete** - Delete a file
- **Download** - Download a file
- ❌ "List" - Does NOT exist

### Folder Resource
- **Create** - Create a folder
- **Delete** - Delete a folder
```

**❌ BAD - Wall of text:**
```markdown
Google Drive has several operations available. For files, you can use Copy to duplicate them, Delete to remove them, and Download to retrieve content. Note that there is no List operation. For folders...
```

**Rule:** Use bullet lists, tables, and clear headings. Avoid prose paragraphs.

### 4. Explicit Negative Cases

**✅ GOOD - Shows what NOT to do:**
```markdown
- ❌ "List files" - Does NOT exist. Use **Search** instead
- ❌ "Read file" - Does NOT exist. Use **Download** instead
```

**❌ BAD - Only shows what exists:**
```markdown
- **Search** - Search for files
- **Download** - Download a file
```

**Why explicit negatives matter:**
- Prevents agents from guessing common but wrong operations
- Addresses the actual mistakes they make
- Provides immediate correction

### 5. Placement: .claude/agents/references/

**Standard location:**
```
/Users/swayclarke/coding_stuff/
├── .claude/
│   ├── agents/
│   │   ├── solution-builder-agent.md
│   │   ├── architecture-feasibility-agent.md
│   │   └── references/
│   │       ├── N8N_NODE_REFERENCE.md
│   │       ├── N8N_IMPLEMENTATION_PATTERNS.md
│   │       ├── OAUTH_REFRESH_PROTOCOL.md
│   │       └── REFERENCE_DOC_BEST_PRACTICES.md
```

**Why this location:**
- Centralized: All agents can reference same docs
- Organized: Separated from agent definitions
- Predictable: Easy to find and maintain
- Versioned: Can track in git with rest of project

**Alternative for project-specific references:**
```
/Users/swayclarke/coding_stuff/
├── project-name/
│   ├── docs/
│   │   └── api-endpoints.md  (project-specific)
├── .claude/
│   └── agents/
│       └── references/
│           └── general-patterns.md  (cross-project)
```

---

## How to Direct Agents to Use References

### Concise Agent Instructions (Recommended)

**Pattern for agent prompts:**

```markdown
## **CRITICAL: [Topic] Reference**

**BEFORE [action], check:** `/path/to/reference.md`

**Rule:** If not in reference → verify with [fallback method]

**Common mistakes:**
- ❌ [Mistake 1] → Use [Correct approach]
- ❌ [Mistake 2] → Use [Correct approach]
```

**Example:**
```markdown
## **CRITICAL: n8n Node Operations**

**BEFORE suggesting operations, check:** `/.claude/agents/references/N8N_NODE_REFERENCE.md`

**Rule:** If operation not in reference → Call `mcp__n8n-mcp__get_node`

**Common mistakes:**
- ❌ Google Drive "List files" → Use **Search**
- ❌ Notion "Delete page" → Use **Archive**
```

**Why this works:**
- ~10 lines instead of ~50 lines
- Clear call-to-action: "check this doc"
- Provides fallback if doc doesn't have answer
- Shows most common mistakes inline (no need to open doc for 80% of cases)

### Where to Place Instructions in Agent Prompts

**✅ GOOD - Early in prompt, before workflow sections:**

```markdown
---
name: agent-name
description: ...
---

[Agent starting message]

## **CRITICAL: Reference Checks**
[Reference instructions here - 3-4 critical references max]

---

## Role
[Agent role description]

## Workflow
[Agent workflow steps]
```

**❌ BAD - Buried in middle of workflow:**

```markdown
## Step 3 - Build the structure
...do this, do that...

By the way, check N8N_NODE_REFERENCE.md for operations.

Continue with step 4...
```

**Why early placement matters:**
- Agents see it before they start working
- Sets expectations upfront
- More likely to be followed

### Reinforcement Technique

**For critical references, mention in TWO places:**

1. **Top of prompt** (before workflow):
```markdown
## **CRITICAL: n8n Operations**
Check N8N_NODE_REFERENCE.md BEFORE suggesting any operation.
```

2. **In relevant workflow step** (when they'd use it):
```markdown
### Step 4 – Build the structure

1. **Verify operations** (see CRITICAL section above):
   - Check N8N_NODE_REFERENCE.md
   - If not found, call mcp__n8n-mcp__get_node
```

**Don't overdo it:**
- Maximum 2 mentions per reference
- Don't repeat full instructions, just remind

---

## Maintaining References

### When to Update

**Update reference when:**
- ✅ New pattern discovered (after 2-3 similar issues)
- ✅ Common mistake identified
- ✅ New service/node added to workflows
- ✅ Breaking change in tool behavior

**Don't update for:**
- ❌ One-off edge cases
- ❌ Project-specific details (put in project docs instead)
- ❌ Temporary workarounds

**Rule:** If you see the same problem 3 times, add it to reference.

### Version Tracking

**Add version footer:**
```markdown
---

**Last Updated:** 2026-01-05
**Version:** 1.2
**Changes:** Added Gmail operations, fixed Google Drive Search description
```

**Why:**
- Helps identify stale references
- Provides change history
- Useful when troubleshooting "why did this change?"

### Review Schedule

**Quarterly review checklist:**
- [ ] Are all services still relevant?
- [ ] Have any operations changed?
- [ ] Are there new common mistakes to add?
- [ ] Can any sections be removed?
- [ ] Is doc still under 300 lines? (If no, consider splitting)

---

## Extracting Learnings from Conversations

### Process for Creating New References

**Step 1: Identify pattern**
- Same mistake appears in 2-3 different conversations
- Same question asked multiple times
- Same research repeated by different agents

**Step 2: Extract core information**
- What was the mistake/question?
- What's the correct answer?
- What's the lookup process?

**Step 3: Create focused reference**
```markdown
# [Topic] Reference

**Purpose:** [One sentence]

**CRITICAL RULE:** [Most important thing to remember]

## Quick Reference
[Core information - scannable format]

## Common Mistakes
[What NOT to do]

## When to Use [Alternative/Tool]
[Fallback when reference doesn't have answer]
```

**Step 4: Add to 1-2 relevant agent prompts**
- Keep instructions concise (~10 lines)
- Place early in prompt
- Test with next similar task

**Step 5: Iterate**
- If agents still make mistakes, instructions aren't clear enough
- If agents never use it, it's probably not valuable
- If it grows beyond 300 lines, split into multiple focused docs

### Example: Creating OAuth Reference

**Pattern identified:**
```
Conversation 1: "How do I refresh Google OAuth?"
Conversation 2: "Gmail API says invalid credentials"
Conversation 3: "OAuth token expired, need to refresh"
```

**Extract core info:**
- Problem: OAuth tokens expire
- Solution: Use browser-ops-agent, not main conversation
- Reason: Main conversation wastes 100K tokens on Playwright snapshots

**Create reference:**
```markdown
# OAuth Refresh Protocol

**Purpose:** How to refresh OAuth tokens efficiently

**CRITICAL RULE:** ALWAYS use browser-ops-agent for OAuth, NEVER main conversation

## Quick Process
1. Detect expired token (401 error)
2. Launch browser-ops-agent with service name
3. Agent handles OAuth flow
4. Resume workflow

## Common Mistakes
- ❌ Using Playwright tools in main conversation (wastes 100K+ tokens)
- ❌ Asking user to complete OAuth manually (poor UX)
```

**Add to agent prompts:**
```markdown
## **CRITICAL: OAuth Refresh**
BEFORE handling OAuth: Launch **browser-ops-agent** (see OAUTH_REFRESH_PROTOCOL.md)
NEVER use Playwright in main conversation.
```

---

## Reference Document Templates

### Template 1: Operations/Commands Reference

**Use for:** Listing available operations, commands, or endpoints

```markdown
# [Service] Operations Reference

**Purpose:** Exact operations available for [service] nodes

**CRITICAL RULE:** If operation not listed, it does NOT exist

---

## [Service Name] (node-type-identifier)

### Resource: [Resource Name]
- **Operation** - Description
- **Operation** - Description

**Common Mistakes:**
- ❌ "[Wrong operation]" - Use **[Correct operation]** instead

---

## Quick Reference Table
| Service | Key Resources | Notes |
|---------|---------------|-------|

---

**Last Updated:** [Date]
**Version:** [X.Y]
```

### Template 2: Process/Protocol Reference

**Use for:** Step-by-step procedures, protocols, workflows

```markdown
# [Process Name] Protocol

**Purpose:** [One sentence describing when to use this]

**CRITICAL RULE:** [Most important constraint]

---

## When to Use

Use this protocol when:
- [Condition 1]
- [Condition 2]

---

## Quick Process

1. **[Step 1]** - [What to do]
2. **[Step 2]** - [What to do]
3. **[Step 3]** - [What to do]

---

## Common Mistakes

- ❌ [Mistake] - [Why it's wrong] → ✅ [Correct approach]

---

## Troubleshooting

**If [problem]:**
- [Solution]

---

**Last Updated:** [Date]
**Version:** [X.Y]
```

### Template 3: Patterns/Examples Reference

**Use for:** Code patterns, implementation examples, debugging

```markdown
# [Topic] Patterns Reference

**Purpose:** Common patterns and solutions for [topic]

---

## Pattern 1: [Pattern Name]

**Use when:** [Scenario]

**✅ CORRECT:**
\`\`\`[language]
[Code example]
\`\`\`

**❌ WRONG:**
\`\`\`[language]
[Anti-pattern example]
\`\`\`

**Key Learning:** [One sentence]

---

[Repeat for each pattern]

---

**Last Updated:** [Date]
**Version:** [X.Y]
```

---

## Metrics for Success

**A good reference document:**
- ✅ Agents use it without being reminded
- ✅ Reduces repeat questions by 80%+
- ✅ Eliminates specific category of mistakes
- ✅ Under 300 lines (if longer, split)
- ✅ Updated less than once per month (stable)

**A bad reference document:**
- ❌ Agents ask questions answered in doc
- ❌ Same mistakes still happen
- ❌ Over 500 lines (too long to scan)
- ❌ Updated weekly (unstable/too detailed)
- ❌ Never mentioned by agents (not valuable)

---

## Example: Current N8N_NODE_REFERENCE.md Analysis

**Current state:** 933 lines

**Lines 1-233:** Core operations reference
- ✅ Perfect for original problem (operation validation)
- ✅ Scannable, clear structure
- ✅ Explicit negatives (❌ "List" does NOT exist)

**Lines 233-933:** Implementation patterns and code examples
- ⚠️ Valuable but different purpose
- ⚠️ Makes doc 4x longer than needed for operation validation
- ⚠️ Belongs in separate doc: N8N_IMPLEMENTATION_PATTERNS.md

**Recommendation:**
1. **Keep in N8N_NODE_REFERENCE.md (lines 1-233):**
   - Service operations listings
   - Common mistakes
   - Quick reference table
   - When to call MCP tools

2. **Move to new N8N_IMPLEMENTATION_PATTERNS.md (lines 233-933):**
   - JavaScript code patterns
   - Binary data access
   - HTTP Request configurations
   - Debugging patterns
   - Google Drive trigger behavior
   - OAuth scope requirements

**Result:**
- N8N_NODE_REFERENCE.md: ~230 lines, focused on operation validation
- N8N_IMPLEMENTATION_PATTERNS.md: ~700 lines, focused on code implementation
- Each doc serves ONE clear purpose
- Agents can check operations quickly without wading through code examples

---

**Last Updated:** 2026-01-05
**Version:** 1.0
