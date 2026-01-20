# Agents Directory

Central location for all Claude Code agents in the Oloxa.ai system.

---

## How to Use Agents

Tell Claude: "Use the [agent-name] to help me with [task]"

Example: "Use the idea-architect-agent to help me plan a lead automation"

---

## Agent Index

### Solution Design & Build

| Agent | Color | Purpose | When to Use |
|-------|-------|---------|-------------|
| [idea-architect-agent](idea-architect-agent.md) | Blue | Ideation, workflow mapping, platform selection | You have an idea and need to plan before building |
| [solution-builder-agent](solution-builder-agent.md) | Orange | Technical implementation | Solution brief is approved, ready to build |

**Workflow:** Idea Architect → (approval) → Solution Builder

---

### Planning Agents

| Agent | Color | Purpose | Target Time |
|-------|-------|---------|-------------|
| [daily-planner-agent](daily-planner-agent.md) | Yellow | Daily planning & task prioritization | 5 minutes |
| [weekly-strategist-agent](weekly-strategist-agent.md) | Pink | Weekly strategy & goal setting | 10-15 minutes |
| [monthly-reviewer-agent](monthly-reviewer-agent.md) | Purple | Monthly reflection & analysis | 30-45 minutes |

---

### Transcript Processing Agents

| Agent | Color | Purpose | Target Time |
|-------|-------|---------|-------------|
| [transcript-processor-agent](transcript-processor-agent.md) | Cyan | Extract insights from meeting transcripts | Under 3 minutes |
| [project-organizer-agent](project-organizer-agent.md) | Teal | Organize project files & updates | Under 2 minutes |
| [knowledge-extractor-agent](knowledge-extractor-agent.md) | Magenta | Extract patterns for knowledge base | Under 3 minutes |
| [quick-wins-analyzer-agent](quick-wins-analyzer-agent.md) | Lime | Analyze discovery calls for opportunities | Under 3 minutes |

---

### Orchestrators

Orchestrators chain multiple agents together in a workflow. Located in `agents/orchestrators/`.

| Orchestrator | Color | Purpose | Target Time |
|--------------|-------|---------|-------------|
| [full-transcript-workflow](orchestrators/full-transcript-workflow-agent.md) | Red | Complete transcript → knowledge pipeline | 10-15 minutes |

---

## Color Reference

Colors appear in the Claude interface when agents are active:

| Color | Hex | Agents |
|-------|-----|--------|
| Blue | - | idea-architect-agent |
| Orange | - | solution-builder-agent |
| Yellow | - | daily-planner-agent |
| Pink | - | weekly-strategist-agent |
| Purple | - | monthly-reviewer-agent |
| Cyan | - | transcript-processor-agent |
| Teal | - | project-organizer-agent |
| Magenta | - | knowledge-extractor-agent |
| Lime | - | quick-wins-analyzer-agent |
| Red | - | full-transcript-workflow |

---

## Related Files

- [TOOLBOX.md](../TOOLBOX.md) - Platform decision matrix for automation tools
- [MY-JOURNEY.md](../../00-progress-advisor/MY-JOURNEY.md) - Current status and schedule

---

## Adding New Agents

1. Create a new `.md` file in this directory
2. Add YAML frontmatter:
```yaml
---
name: your-agent-name
description: What this agent does (shown in Claude interface)
tools: Read, Write, Edit, Bash, Grep, Glob
model: sonnet
color: [color]
---
```
3. Add agent content following the existing patterns
4. Update this README with the new agent
