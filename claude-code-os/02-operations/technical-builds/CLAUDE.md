# Technical Builds Instructions

## Purpose of This Folder

This folder contains **validated, implementation-ready technical proposals** for automation projects. These are NOT discovery documents - those live in `/02-operations/projects/[client]/`.

**Flow:**
1. Discovery happens in `/02-operations/projects/[client]/`
2. Idea Architect Agent creates solution brief
3. **Technical build proposal lives here** → `/02-operations/technical-builds/[client]/`
4. Implementation begins based on this proposal

---

## What Goes in a Technical Build Proposal

Use the Idea Architect Agent (v2.0+) output format. Every proposal must include:

### 1. Validation Questions Answered
Document ALL technical feasibility questions with specific answers:
- Integration verification (which nodes/APIs exist)
- LLM approach (prompt engineering vs fine-tuning)
- Platform capabilities (forms, file uploads, etc.)
- Infrastructure requirements (RAM, CPU, hosting)
- Cost breakdown (tokens, operations, monthly/annual)
- Alternative options considered

**Example from Eugene project:**
- "How exactly to train LLM?" → Answer: Prompt engineering, not fine-tuning
- "N8N customizable forms?" → Answer: YES, v2.3 supports full customization
- "OCR difficulty?" → Answer: Medium complexity, +4-6 hours via Google Cloud Vision API

### 2. Workflow Diagram (Mermaid)
Always include a visual workflow with:
- Numbered stages (1. INTAKE, 2. PROCESSING, etc.)
- Decision points clearly marked
- Re-upload/retry logic if applicable
- Error handling paths

### 3. Infrastructure Reality Check
**Critical learnings:**
- Don't assume hosting can handle the workflow
- Check RAM requirements vs current setup
- Example: "Basic Digital Ocean (1GB RAM) may not handle 20 PDFs in parallel"
- Document: Sequential vs parallel processing needs
- Include upgrade path if needed

### 4. Cost Analysis
**Calculate operational costs, not just platform fees:**
- Tokens/operations per execution
- Executions per month
- Monthly and annual totals
- Per-transaction cost

**Example format:**
```
| Item | Calculation | Monthly | Annual |
|------|-------------|---------|--------|
| OpenAI API | 15 deals × 45K tokens × $0.0025/1K | $1.69 | $20 |
| N8N Hosting | Digital Ocean 2GB | $12 | $144 |
| Total | | $13.69 | $164 |
```

### 5. Gap Analysis
**Systematically check for:**
- **Data flow gaps:** Re-upload handling, duplicate detection, merge logic
- **Edge cases:** Non-standard file formats, partial data, scanned documents
- **Process gaps:** Manual overrides, error correction, archival
- **Integration gaps:** API downtime, rate limits, retry logic

**Severity levels:**
- Critical (blocks launch)
- Medium (affects UX)
- Low (nice to have)

### 6. Phased Breakdown
**Key learning: Combine phases if needed for value delivery**

Example from Eugene:
- ❌ Phase 0 alone (just form) = 0% value
- ✅ Phase 0+1 combined (form + LLM identification) = 80% value

**Standard framework:**
- Phase 0: Proof of concept (de-risk)
- Phase 1: Core value (solve main pain)
- Phase 2: Automation (reduce manual work)
- Phase 3: Polish (enhancements)

Always identify: **"🎯 True Quick Win: Phase X + Y = Z hours = 80% of value"**

### 7. Effort Reality Check
**Translate hours → calendar time:**
- Use 4 hours/day (realistic, not ideal)
- Example: 18 hours ÷ 4 = 4.5 days ≈ 1 week

**Classifications:**
- True Quick Win: 1-3 days (4-12 hours)
- Small Project: 4-7 days (16-28 hours)
- Medium Project: 2-4 weeks (32-64 hours)
- Large Project: 1-3 months (64+ hours)

### 8. Open Questions for Client
List ALL questions that must be answered before implementation:
- Branding preferences
- Sample documents needed
- Current manual process details
- Success criteria
- Timeline expectations

---

## Integration Verification Process

**Before recommending a platform, verify integrations exist:**

### For N8N:
Use the N8N MCP server:
```
mcp__n8n-mcp__search_nodes with query="[integration name]"
mcp__n8n-mcp__get_node with nodeType="nodes-base.[nodeName]"
```

Example verification table:
| Component | N8N Node | Status | Operations Confirmed |
|-----------|----------|--------|---------------------|
| Google Drive | Google Drive | ✅ | Upload, folder, rename |
| OpenAI | OpenAI Chat Model | ✅ | GPT-4, JSON responses |

### For Make.com:
Check operations documentation and confirm:
- Native integration exists
- Required operations are available
- No workarounds needed

**Document concerns:** "⚠️ No native OCR - requires HTTP Request to external API"

---

## Folder Organization

### Structure
```
/technical-builds/
├── eugene/
│   └── build_proposal_v1.0_2025-12-10.md
├── lombok-invest-capital/
│   └── [their builds]
├── shared/
│   └── [reusable components]
└── [client-name]/
```

### Naming Convention
Follow parent folder rules:
- Format: `descriptive_name_v{major.minor}_{YYYY-MM-DD}.md`
- Example: `build_proposal_v1.0_2025-12-10.md`
- Version on major changes only

### When to Archive
When creating v2.0 of a proposal, move v1.0 to `.archive/`:
```
/technical-builds/eugene/
├── build_proposal_v2.0_2025-12-15.md
└── .archive/
    └── build_proposal_v1.0_2025-12-10.md
```

---

## ⚠️ File Versioning Protocol (MANDATORY)

**This rule applies to ALL technical build projects and configuration files.**

### When Modifying Configuration Files

**BEFORE modifying ANY configuration file** (JSON, YAML, XML, etc.), you MUST:

1. **Create `.archive/` directory** in the configuration folder (if not exists)
2. **Copy original file to archive** with version number and date:
   - Format: `[Original Filename] - v[N] - [DATE].[ext]`
   - Example: `Lombok Invest Capital (Task 1) 11_12_2025 - v1 - Dec-11-2024.json`
3. **Rename modified file** with incremented version number:
   - Example: `Lombok Invest Capital (Task 1) 11_12_2025 - v2 - Dec-11-2024.json`
4. **Keep all versions** for rollback capability

### Applies To:
- Apify JSON configurations
- Make.com blueprints
- N8N workflow exports
- API configuration files
- Database schemas
- Environment configs
- Any technical configuration that could break functionality

### Why This Matters:
- **Rollback capability** - Can revert to any previous version instantly
- **Change tracking** - Clear history of what changed when
- **Testing safety** - Test new versions without losing originals
- **Client confidence** - Show you protect their working systems

### Example Structure:
```
/apify-configs/
├── Config Name - v3 - Dec-12-2024.json  ← Current working version
└── .archive/
    ├── Config Name - v1 - Dec-10-2024.json  ← Original
    └── Config Name - v2 - Dec-11-2024.json  ← Previous version
```

### Version Number Guidelines:
- **v1** = Original file (never modified)
- **v2** = First modification
- **v3** = Second modification
- Continue incrementing for each change

**Remember:** This is NON-NEGOTIABLE. Never modify a config file without archiving the original first.

---

## Key Lessons from Past Projects

### 1. Phase 0 Alone Often Has No Value
**Eugene project learning:**
- Phase 0 (just form + Drive) = 0% value solved
- Phase 0+1 (form + LLM identification) = 80% value solved
- **Action:** Combine phases when necessary for meaningful delivery

### 2. Infrastructure Can Be a Blocker
**Eugene project learning:**
- Basic hosting (1GB RAM) can't handle 20 PDFs in parallel
- Must process sequentially OR upgrade hosting
- **Action:** Always verify infrastructure BEFORE finalizing platform choice

### 3. OCR Adds Complexity but May Be Worth It
**Eugene project learning:**
- OCR = +4-6 hours but covers 100% vs 95% of documents
- Cost negligible (~$0.03/deal)
- **Action:** Consider as "bonus if time permits" rather than exclude

### 4. Operational Costs Often Negligible
**Eugene project learning:**
- OpenAI: $1-2/month for 15 deals/year
- Infrastructure: $5-12/month
- Total: $71-180/year vs €27-42K revenue increase
- **Action:** Calculate costs but don't let them block good solutions

### 5. Email Matching for Re-uploads
**Eugene project learning:**
- Clients need to re-submit/add documents
- Email as unique key in Google Sheet
- **Action:** Always consider "what if client uploads more later?"

---

## Before Implementation Checklist

- [ ] All validation questions answered
- [ ] Workflow diagram created (Mermaid)
- [ ] Integrations verified (actual nodes/APIs confirmed)
- [ ] Infrastructure verified (hosting can handle workload)
- [ ] Costs calculated (monthly + annual operational costs)
- [ ] Gaps identified (edge cases documented)
- [ ] Phases defined (quick win extracted)
- [ ] Client questions compiled (what you need from them)
- [ ] Reality check done (hours → calendar time)
- [ ] Platform decision justified (why this tool, not alternatives)

---

## Common Mistakes to Avoid

❌ **Don't assume integrations exist** - Verify with MCP or docs
❌ **Don't skip infrastructure check** - "Basic hosting" may not be enough
❌ **Don't calculate platform cost only** - Include API/token costs
❌ **Don't ignore re-upload scenarios** - Clients WILL need to add files later
❌ **Don't propose Phase 0 alone** - Usually delivers 0% value
❌ **Don't use ideal hours** - Use 4 hrs/day realistic calendar time
❌ **Don't forget edge cases** - Scanned PDFs, non-standard formats, etc.

---

## Template Checklist

When creating a new build proposal, use the Idea Architect Agent v2.0+ which includes:

✅ Validation Questions section
✅ Workflow diagram (Mermaid)
✅ Infrastructure Reality Check section
✅ Cost Analysis section
✅ Gap Analysis section
✅ Phased Breakdown section
✅ Estimated Effort (with reality classification)
✅ Ready for Solution Builder checklist
✅ Open Questions for Client

**Run the agent with:**
```
Use the Idea Architect Agent to design this solution
```

The agent will guide you through all 9 steps and produce a complete, validated proposal.
