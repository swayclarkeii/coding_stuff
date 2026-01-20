# Templates Department - Implementation Plan

## Department Purpose
Reusable prompts, agent blueprints, and document templates for Oloxa.ai operations.

## Status: AVAILABLE (Growing)
Start adding templates as you create useful patterns.

---

## What This Department Will Do

### Prompt Templates
Reusable prompts for common tasks:
- Client communication
- Content creation
- Analysis and research
- Problem-solving

### Document Templates
Standard documents you'll use repeatedly:
- Proposals
- Contracts
- Project briefs
- Status reports

### Agent Blueprints
Templates for creating new agents:
- Agent structure template
- Testing checklist
- Iteration framework

---

## Starter Templates for Oloxa.ai

### Prompt: Client Status Update
```
Write a brief status update email for [CLIENT NAME] regarding [PROJECT].

Include:
- Progress this week
- Next steps
- Any blockers or needs
- Timeline reminder

Tone: Professional but friendly
Length: 3-4 short paragraphs
```

### Prompt: Meeting Prep
```
Help me prepare for a call with [PROSPECT/CLIENT NAME].

Context:
- [What you know about them]
- [Purpose of the call]
- [What you want to achieve]

Generate:
1. 5 questions to ask
2. Key points to cover
3. Potential objections and responses
4. Clear next step to propose
```

### Prompt: Project Scoping
```
Help me scope a project for [CLIENT] who wants to [GOAL].

I need to understand:
1. Current state (what they have now)
2. Desired state (what they want)
3. Constraints (budget, timeline, technical)
4. Success criteria (how we measure done)

Based on this, provide:
- Recommended approach
- High-level deliverables
- Rough timeline
- Questions to clarify
```

---

## Adding New Templates

When you find yourself writing similar prompts repeatedly:

1. **Save it** - Create a new file in this folder
2. **Name it clearly** - `prompt-[category]-[purpose].md`
3. **Include variables** - Use [BRACKETS] for customizable parts
4. **Add context** - Explain when to use it

---

## Template Categories (Planned)

### Communication
- Client emails
- Proposal drafts
- Follow-up sequences
- Rejection responses (nice nos)

### Analysis
- Competitor research
- Market analysis
- Technical assessment
- Process audit

### Content
- YouTube scripts
- Social posts
- Case studies
- Blog outlines

### Sales
- Discovery call prep
- Proposal outline
- Objection handling
- Close sequences

---

## Template File Structure

```markdown
# [Template Name]

## When to Use
[Describe the situation]

## Variables
- [VARIABLE_1]: [Description]
- [VARIABLE_2]: [Description]

## Template
[The actual template content]

## Example Output
[What it looks like when used]

## Notes
[Any tips or considerations]
```

---

## Integration Points

| Receives From | Sends To |
|---------------|----------|
| All departments (proven prompts) | All departments (reusable templates) |
| HR Department (agent prompts) | Quick reference |
| Content Team (content frameworks) | Consistent output |
