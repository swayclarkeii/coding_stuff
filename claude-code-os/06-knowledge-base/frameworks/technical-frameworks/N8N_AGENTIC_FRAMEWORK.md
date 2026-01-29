# n8n Agentic Building Framework

## Overview

This framework enables **autonomous n8n workflow building** where Claude Code:
1. Receives a goal in plain English
2. Figures out the implementation steps
3. Builds the workflow
4. Executes and catches errors
5. Fixes errors automatically
6. Iterates until success
7. Notifies you when complete

Based on the 3-layer "Agentic Stack" from the video, adapted for n8n.

---

## The 3-Layer Architecture

```
+------------------+     YOU define this
|   DIRECTIVE      |     (Plain English goals in markdown)
|   Layer 1        |     Location: directives/n8n/
+------------------+
         |
         v
+------------------+     CLAUDE handles this
|  ORCHESTRATION   |     (Breaks down steps, handles errors)
|   Layer 2        |     Location: Claude Code conversation
+------------------+
         |
         v
+------------------+     MCP TOOLS do this
|   EXECUTION      |     (n8n API calls, workflow operations)
|   Layer 3        |     Location: n8n server via MCP
+------------------+
```

### Layer 1: Directive (YOUR job)
- Plain English description of what you want
- Stored in markdown files in `directives/n8n/`
- Contains: goal, trigger, inputs, outputs, constraints
- **You only do this layer**

### Layer 2: Orchestration (CLAUDE's job)
- Breaks directive into steps
- Decides which tools/agents to use
- Handles errors and edge cases
- Routes to appropriate agents
- **Claude handles this automatically**

### Layer 3: Execution (MCP TOOLS' job)
- Actual n8n API calls
- Workflow creation/modification
- Testing and validation
- Error retrieval
- **MCP tools do the actual work**

---

## What You Need to Set Up

### 1. Directives Folder (NEW)

Create SOPs for different workflow types:

```
directives/
└── n8n/
    ├── _template.md              # Template for new directives
    ├── patterns/
    │   ├── webhook-to-action.md  # Common: webhook triggers action
    │   ├── schedule-monitor.md   # Common: scheduled monitoring
    │   ├── email-processor.md    # Common: email-based triggers
    │   └── multi-step-pipeline.md
    ├── client-projects/
    │   ├── eugene-expense-system.md
    │   └── fathom-transcript.md
    └── learnings/
        └── errors-and-fixes.md   # Self-annealing documentation
```

### 2. Agents (ALREADY HAVE - but need updates)

| Agent | Role | When Used |
|-------|------|-----------|
| **idea-architect-agent** | Design | "I want to build X" → Creates solution brief |
| **architecture-feasibility-agent** | Validate | Checks if design is realistic |
| **solution-builder-agent** | Build | Creates/modifies n8n workflows |
| **test-runner-agent** | Test | Executes workflows, retrieves errors |
| **workflow-optimizer-agent** | Optimize | Reduces cost/complexity |

**UPDATE NEEDED**: Add self-annealing loop to solution-builder-agent

### 3. Skills (NEW - need to create)

Skills are reusable commands. Create these:

| Skill | Purpose | Triggers |
|-------|---------|----------|
| `/build-n8n` | Full agentic build loop | User says "build workflow for X" |
| `/test-n8n` | Quick workflow test | User says "test workflow ID" |
| `/fix-n8n` | Error diagnosis and fix | User says "fix workflow ID" |
| `/deploy-n8n` | Activate and deploy | User says "deploy workflow ID" |

### 4. CLAUDE.md Updates (PARTIAL - need additions)

Add n8n agentic section to CLAUDE.md.

### 5. Continual Learning System (NEW)

When errors are fixed:
1. Document the error → fix in `directives/n8n/learnings/errors-and-fixes.md`
2. Update relevant pattern files
3. Add to N8N_PATTERNS.md if it's a reusable pattern

---

## The Self-Annealing Loop

This is the core innovation - the system gets stronger with each error:

```
Error Occurs
    |
    v
+-------------------+
| 1. Read Error     |  n8n_executions mode="error"
+-------------------+
    |
    v
+-------------------+
| 2. Diagnose       |  Claude analyzes error context
+-------------------+
    |
    v
+-------------------+
| 3. Fix            |  n8n_update_partial_workflow
+-------------------+
    |
    v
+-------------------+
| 4. Test Again     |  n8n_test_workflow
+-------------------+
    |
    +---> Error? Loop back to step 1
    |
    v (Success)
+-------------------+
| 5. Document Fix   |  Update directives/learnings
+-------------------+
    |
    v
+-------------------+
| 6. Update Pattern |  Add to N8N_PATTERNS.md
+-------------------+
    |
    v
System is now STRONGER
```

---

## Agent Pipeline for n8n Building

### For New Workflows

```
User: "Build me a workflow that does X"
           |
           v
    idea-architect-agent
    (Creates Solution Brief)
           |
           v
    architecture-feasibility-agent
    (Validates design is realistic)
           |
           v
    solution-builder-agent
    (Builds the workflow)
           |
           v
    test-runner-agent
    (Tests with sample data)
           |
           +---> Error? → solution-builder-agent (fix)
           |
           v (Success)
    DONE - notify user
```

### For Existing Workflows

```
User: "Fix/modify workflow ID"
           |
           v
    test-runner-agent
    (Get current state + errors)
           |
           v
    solution-builder-agent
    (Apply fixes/modifications)
           |
           v
    test-runner-agent
    (Verify fix worked)
           |
           +---> Error? → Loop
           |
           v (Success)
    DONE - notify user
```

---

## Running Autonomously with Claude Command

### Option 1: Interactive (Current)
```bash
claude
# Then type your request
```
You'll need to approve tool calls.

### Option 2: Autonomous (Bypass Permissions)
```bash
claude --dangerously-skip-permissions
# Or use the bypass permissions setting
```
Claude runs without interruption.

### Option 3: Headless/Background
```bash
claude -p "Build an n8n workflow that monitors Gmail for invoices and saves them to Google Drive" --output-format json
```
Runs in background, returns JSON result.

### Option 4: With Specific Agent
```bash
claude -p "Build workflow for lead tracking" --allowedTools "Task(solution-builder-agent)"
```

### Recommended Setup for Agentic Building:
1. Enable bypass permissions in Claude Code settings
2. Use the `/build-n8n` skill (once created)
3. Let it run autonomously
4. Review results when notified

---

## File Structure After Setup

```
coding_stuff/
├── CLAUDE.md                    # Updated with n8n agentic section
├── N8N_PATTERNS.md              # Existing - add learnings here
├── N8N_AGENTIC_FRAMEWORK.md     # This file
│
├── directives/                  # NEW
│   └── n8n/
│       ├── _template.md
│       ├── patterns/
│       │   ├── webhook-to-action.md
│       │   └── ...
│       └── learnings/
│           └── errors-and-fixes.md
│
├── .claude/
│   ├── agents/
│   │   ├── solution-builder-agent.md  # UPDATE with self-annealing
│   │   ├── test-runner-agent.md
│   │   └── ...
│   │
│   └── commands/               # Skills/commands
│       ├── build-n8n.md        # NEW
│       ├── test-n8n.md         # NEW
│       └── fix-n8n.md          # NEW
│
└── solutions/                  # Output location
    └── [client-name]/
        ├── solution-brief.md
        ├── workflow-v1.json
        └── test-results.md
```

---

## Quick Start Checklist

### Phase 1: Foundation (Do First)
- [ ] Create `directives/n8n/` folder structure
- [ ] Create directive template
- [ ] Create `errors-and-fixes.md` for learning
- [ ] Update CLAUDE.md with agentic protocol

### Phase 2: Skills (Do Second)
- [ ] Create `/build-n8n` skill
- [ ] Create `/test-n8n` skill
- [ ] Create `/fix-n8n` skill

### Phase 3: Agent Updates (Do Third)
- [ ] Update solution-builder-agent with self-annealing loop
- [ ] Update test-runner-agent to support agentic loop
- [ ] Create orchestrator skill that chains agents

### Phase 4: Test & Iterate
- [ ] Run a full build cycle manually
- [ ] Run autonomous with bypass permissions
- [ ] Document any issues in learnings

---

## Example Directive (What You Write)

```markdown
# Directive: Lead Follow-up Automation

## Goal
When a new lead submits the contact form, automatically:
1. Save to Airtable
2. Send welcome email
3. Notify sales team on Slack

## Trigger
- Webhook from Typeform

## Inputs
- Name, email, company, message from form

## Outputs
- Airtable record created
- Email sent to lead
- Slack message posted

## Constraints
- Must handle missing company field gracefully
- Email should be personalized with name
- Slack notification should include all details

## Success Criteria
- Lead receives email within 1 minute
- Sales team sees Slack notification
- Record exists in Airtable with all fields
```

That's it. You write THIS, Claude handles everything else.

---

## Next Steps

1. **Approve this framework** - Let me know if this structure works
2. **I'll create the folder structure** - Set up directives/
3. **I'll create the skills** - /build-n8n, /test-n8n, /fix-n8n
4. **Update agents** - Add self-annealing to solution-builder
5. **Test the loop** - Run a full autonomous build

Ready to proceed?
