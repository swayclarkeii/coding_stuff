# Plan: Eugene Document Classification Prompt Engineering Workflow

## TL;DR

**Platform**: Claude.ai Projects (you have Max) → best for multi-document prompt development
**Process**:
1. Upload all sample docs from multiple clients to a Claude.ai Project
2. Develop 3 tiered prompts interactively with BPS framework
3. Test with holdout samples in same project
4. Export to Claude Code → prompt-analysis-agent → version control
5. Deploy to n8n and validate

---

## Problem Statement

Sway needs to build **3 tiered classification prompts** for the Eugene workflow using Cloud Vision:

### The 3 Prompts

| Prompt | Purpose | Input | Output |
|--------|---------|-------|--------|
| **1. Client Info Parser** | Extract client/project info | Any document | Project name, street name, client details → folder structure |
| **2. Tier 1 Classifier** | Route to category | Any document | One of 4 categories: Financial, Expose, [Category 3], [Category 4] |
| **3. Tier 2 Classifier(s)** | Sub-classify within category | Category-specific doc | Specific doc type (e.g., 1 of 6 financial types) |

### The Challenges

1. **Cross-client generalization**: Prompts must work for DIFFERENT clients with varying doc formats
2. **Tiered accuracy**: Each tier must be accurate or downstream classification fails
3. **Testing matrix**: Each prompt × each client × multiple doc types
4. **Quality**: Must follow BPS framework and be production-ready
5. **Iteration**: Need fast feedback loop for refinement

## Core Question

**Where/how to do this prompt engineering work?**

Requirements:
- [ ] LLM can see sample documents from MULTIPLE clients
- [ ] LLM can reference the BPS framework
- [ ] Can iterate quickly on prompt drafts
- [ ] Can test prompts against holdout samples
- [ ] Can version control final prompts
- [ ] Can validate cross-client generalization

---

## Why Claude.ai Projects is the Best Option

| Option | Development Speed | Testing | Version Control | Cross-Client Visibility |
|--------|-------------------|---------|-----------------|-------------------------|
| **Claude.ai Projects** | Fast (interactive) | Manual but instant | Manual export | Excellent |
| Claude Code | Slow (tokens) | Manual | Built-in | Limited (context) |
| Anthropic Console | Medium | Built-in | Basic | Limited |
| n8n Testing | N/A (production) | Automated | External | N/A |

**Recommendation**: Use Claude.ai Projects for development + Claude Code/prompt-analysis-agent for formalization + n8n for production validation.

---

## Recommended Approach: Claude.ai Projects + Systematic Testing

**Why Claude.ai Projects (Max subscription):**
- You have Max subscription ✓
- Can upload ALL sample documents from ALL clients
- Claude sees everything in context
- Interactive iteration with instant feedback
- No token limits like Claude Code

### Phase 1: Setup (Claude.ai)

1. **Create Claude.ai Project**: "Eugene Document Classification"

2. **Organize and upload sample documents**:
   ```
   Naming convention for uploads:
   - client1_invoice_sample1.pdf
   - client1_invoice_sample2.pdf
   - client2_invoice_sample1.pdf
   - client1_w2_sample1.pdf
   - client2_expose_sample1.pdf
   ...
   ```
   - Include 2-3 examples per doc type PER CLIENT
   - This lets Claude see how the same doc type varies across clients

3. **Upload BPS framework**: Add BPS_FRAMEWORK.md to Project Knowledge

### Phase 2: Develop Each Prompt (Claude.ai)

**Develop in order (tiered):**

**Prompt 1: Client Info Parser**
```
"I need a prompt that extracts client/project information from any uploaded document.
Look at these sample documents and identify:
- What text/visual patterns indicate the project name?
- What patterns indicate the street name?
- What patterns indicate client details?

Draft a Cloud Vision prompt following the BPS framework that extracts this info reliably across all client document formats."
```

**Prompt 2: Tier 1 Classifier**
```
"Now I need a prompt that classifies documents into 4 categories:
1. Financial documents
2. Expose documents
3. [Category 3]
4. [Category 4]

Look at my uploaded samples. What distinguishes each category?
Draft a BPS-compliant prompt that routes documents accurately."
```

**Prompt 3: Tier 2 Classifier (repeat for each category)**
```
"For documents classified as 'Financial', I need to sub-classify into:
1. [Financial doc type 1]
2. [Financial doc type 2]
...
6. [Financial doc type 6]

Analyze the financial document samples. What distinguishes each sub-type?
Draft a BPS-compliant sub-classification prompt."
```

### Phase 3: Test in Claude.ai

**Holdout testing:**
1. Keep 1 sample per doc type per client as "holdout" (don't use in prompt development)
2. After drafting prompts, upload holdouts one by one
3. Ask Claude to classify using the drafted prompt
4. Track accuracy: `Client X, Doc Type Y: Correct/Incorrect`

**Cross-client validation:**
- Test that prompts work for Client 1 docs AND Client 2 docs
- If fails, analyze why and refine prompt

### Phase 4: Formalization (Claude Code)

1. **Export working prompts** from Claude.ai Projects (copy text)

2. **Run through prompt-analysis-agent**:
   - Ensures BPS compliance is perfect
   - Versions prompts properly
   - Saves to project folder

3. **Store in Eugene project**:
   ```
   eugene-workflow/prompts/
     client-info-parser-v1.md
     tier1-classifier-v1.md
     tier2-financial-classifier-v1.md
     tier2-expose-classifier-v1.md
     ...
   ```

### Phase 5: Production Validation (n8n)

1. **Deploy prompts to n8n workflow**

2. **Run test batch**:
   - Process sample docs through actual workflow
   - Compare output to expected results
   - If issues, iterate in Claude.ai Projects

---

## File Structure

```
claude-code-os/projects/technical-builds/eugene-workflow/
  prompts/
    client-info-parser-v1.md          # Extracts project/street/client info
    tier1-classifier-v1.md            # Routes to 4 categories
    tier2-financial-classifier-v1.md  # Sub-classifies financial docs
    tier2-expose-classifier-v1.md     # Sub-classifies expose docs
    tier2-[category3]-classifier-v1.md
    tier2-[category4]-classifier-v1.md
  samples/
    client1/
      invoices/
      w2/
      expose/
    client2/
      invoices/
      w2/
      expose/
```

---

## Action Items

**First: Save this plan to Eugene project folder**
- Location: `claude-code-os/projects/technical-builds/eugene/prompts/`
- Filename: `Eugene-Document-Classification-Prompt-Engineering-Workflow-Plan.md`

**Then proceed with development:**

1. [ ] Create Claude.ai Project "Eugene Document Classification"
2. [ ] Gather sample documents from 2-3 clients (2-3 per doc type per client)
3. [ ] Upload samples with clear naming: `{client}_{doctype}_{n}.pdf`
4. [ ] Upload BPS_FRAMEWORK.md to project
5. [ ] Develop Prompt 1: Client Info Parser
6. [ ] Test Prompt 1 with holdout samples
7. [ ] Develop Prompt 2: Tier 1 Classifier
8. [ ] Test Prompt 2 with holdout samples
9. [ ] Develop Prompt 3(s): Tier 2 Classifiers for each category
10. [ ] Test Tier 2 prompts with holdout samples
11. [ ] Export all prompts to Claude Code
12. [ ] Run through prompt-analysis-agent for BPS formalization
13. [ ] Deploy to n8n and validate end-to-end
