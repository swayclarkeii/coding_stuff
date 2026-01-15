---
name: Automation Toolbox
description: Collection of reusable automation components and utility patterns
---

Yep, this all makes sense — you're remembering correctly:
	•	One bucket = TOOLBOX.md (global rules, decisions, MCP stuff, optimization patterns).
	•	The “other place” I kept pointing to is an Advanced Architecture Patterns guide (like advanced-architecture-patterns.md) plus a couple of small, reusable guides (results verification + duplicate detection) so your agents can stay lean.

I’ll do three things for you:
	1.	Recap what lives where.
	2.	Give you a full updated Automation Toolbox Reference (drop-in replacement).
	3.	Give you suggested contents for the extra external files:
	•	advanced-architecture-patterns.md
	•	results-verification-guide.md
	•	datastore-duplicate-detection.md

You can tweak filenames, but structurally this will work.

⸻

1. What goes where (quick recap)

TOOLBOX.md (what you pasted) should hold:
	•	Platform decision logic (Make vs n8n vs GH Actions vs Custom).
	•	Split & merge comparison (Make can’t merge, n8n can).
	•	Internal vs client deployment rules (n8n Cloud vs self-host, Make tiers).
	•	Subscription tier checks (Canva, Gamma, Make, etc).
	•	Output platform selection (Slides vs Gamma vs Canva).
	•	MCP usage reference (n8n-mcp, make-mcp).
	•	General workflow optimization patterns (early filtering, redundant module removal, etc).
	•	High-level lessons (Lombok case study).

advanced-architecture-patterns.md
	•	The 10 advanced patterns you already referenced in idea-architect-agent Step 3.13:
	•	Modular chunks, multiple AI passes, OCR, idempotent operations, state tracking, migration, retry logic, unique file storage, linked data, completion tracking/notifications.
	•	Each with a short description and “when to use”.

results-verification-guide.md
	•	The generic process that’s now buried in the Solution Builder:
	•	Export before / after.
	•	Compare counts.
	•	Spot-check.
	•	Filter equivalence proof.
	•	When verification fails.

datastore-duplicate-detection.md
	•	The Make.com Data Store duplicate pattern:
	•	When to use.
	•	3-module architecture (Search → Add → Process).
	•	Testing mode toggle.
	•	Cost/savings logic.

Your agents can then just say:

“If workflow is complex, consult advanced-architecture-patterns.md.”
“For optimizations, follow TOOLBOX + results-verification-guide.md + datastore-duplicate-detection.md.”

⸻

2. Updated Automation Toolbox Reference (drop-in)

Here’s a full version you can paste over your current toolbox.

# Automation Toolbox Reference

A decision guide for choosing the right platform and patterns when building automation solutions.

---

## Platform Decision Matrix

| Criteria | Make.com | N8N | GitHub Actions | Custom Code |
|----------|----------|-----|----------------|-------------|
| **Cost** | $9–29/mo + operations | Free (self-hosted) | Free (≈2,000 min/mo) | Hosting costs |
| **Complexity** | Low–Medium | Medium–High | Medium | High |
| **Brand Integrations** | Excellent (Apify, Airtable, etc.) | Good | Limited | Full control |
| **HTML/Memory Intensive** | Limited | Better | N/A | Best |
| **Client Handoff** | Easy | Harder | Medium | Hardest |
| **Sway's Familiarity** | High | Medium | Medium | High |
| **Visual Builder** | Yes | Yes | No (YAML) | No |
| **Error Handling** | Built-in | Built-in | Manual | Manual |

---

## When to Use What

### Make.com

**Best for:**
- Quick client builds with lots of integrations (Apify, Airtable, Sheets, Slack, etc.).
- Visual workflows that non-technical clients can understand and maintain.
- Low–medium complexity where “router + filters” are enough.
- Projects where client handoff and simplicity matter more than raw power.

**Avoid when:**
- You need **native merge semantics** across routes (no merge node).
- Heavy HTML parsing / large in-memory structures.
- Operation costs will explode (high-frequency or high-volume workflows).
- You need complex, arbitrary logic — you’ll fight the platform.

**Key notes:**
- Great for “glue” + orchestration.
- Use Make Cloud for **client-facing** deployments (Core/Pro tiers).

---

### N8N (Self-Hosted / Cloud)

**Best for:**
- Architecturally complex workflows (split/merge, multiple branches, advanced logic).
- Heavy data transformation or pre-processing.
- Work where you want JavaScript/Python nodes.
- Internal workflows where you control the infrastructure.

**Avoid when:**
- Client must maintain/modify the workflow themselves (unless n8n Cloud).
- You need super-fast “from zero to working” for a very simple use case.
- The client cannot handle self-hosted infra (almost always true).

**Key notes:**
- For **you (internal)**: self-hosted is fine if you accept infra overhead.
- For **clients**: strongly prefer **n8n Cloud**, not self-hosted.
- Has native **Merge** node (big advantage over Make for split/merge flows).

---

### GitHub Actions

**Best for:**
- Code-related workflows (CI/CD, linting, tests).
- Scheduled cron jobs where everything lives in git.
- Low-frequency automations where free minutes are enough.

**Avoid when:**
- You want non-devs to understand or edit flows.
- You need visual design or lots of third-party SaaS integrations.
- You need long-lived state across runs.

**Key use cases:**  
Deployment pipelines, nightly data pulls, repository maintenance.

---

### Custom Code

**Best for:**
- Memory-intensive operations (like Lombok HTML parsing) that no-code tools choke on.
- Complex algorithms and special cases that don’t map nicely to nodes/modules.
- Tight performance & control needs.

**Avoid when:**
- You want speed-to-first-version over perfection.
- Handoff to a non-technical client is required.
- A no-code/low-code platform can get you 90% of the way.

**Languages to default to:**
- Python for data/ETL.
- Node.js for web+APIs.
- Go only when performance becomes a real bottleneck.

---

## Split & Merge Capabilities

**Critical difference between Make.com and N8N.**

| Platform | Split Capability | Merge Capability | Notes |
|----------|------------------|------------------|-------|
| **Make.com** | ✅ Router | ❌ No native merge | Can fake merge with Data Stores / Variables / HTTP, but it’s clumsy. |
| **N8N** | ✅ IF/Switch nodes | ✅ Merge node | True split/merge flows, cleaner data modelling. |
| **GitHub Actions** | ✅ Matrix / conditionals | ⚠️ Only via sequential jobs | Not a general-purpose orchestrator. |
| **Custom Code** | ✅ Anything | ✅ Anything | You own all the logic. |

**Rule of thumb:**
- If you need **real merge semantics** (join multiple routes back into one stream), prefer **N8N** unless cost/infra makes it impossible.
- If it’s simple routing with no merge, Make.com is usually fine.

---

## Internal vs Client Deployment Rules

**Who is this for?** drives platform AND hosting choices.

| Scenario | N8N Recommendation | Make.com Recommendation |
|----------|-------------------|-------------------------|
| **Internal (you)** | Self-host OK (cheapest) | Core/Pro; you own account |
| **External client** | **n8n Cloud ONLY** (no self-host) | Client uses their own Make account (Core/Pro) |

**Guidelines:**

- **Never** design a client solution that **requires** them to self-host n8n unless they explicitly want to run their own infra (rare).
- For Make.com:
  - Client-friendly: they can see and adjust scenarios.
  - Keep your account separate from theirs — avoid shared billing mess.
- For internal experiments:
  - Use whatever is easiest for you (self-hosted n8n, Make, or pure code).

---

## Subscription Tier Validation (Quick Check)

Before you commit to an architecture, validate that the **tier** supports the features:

**Questions to ask:**
1. Whose subscription is this? (yours vs client’s)
2. Which tier are they on? (Free / Core / Pro / Enterprise / etc.)
3. Does the tier support:
   - API access?
   - Webhooks?
   - Needed modules/integrations?
4. Is the feature you’re relying on **Enterprise-only** (e.g. Canva Autofill API)?

**Examples to keep in mind:**
- **Canva** – Autofill API is **Enterprise**, not Pro.
- **Gamma** – API or advanced export often needs paid tiers.
- **Make.com** – operation limits differ a lot between Free/Core/Pro.
- **Google Workspace** – quotas vary by business vs personal.

**Rule:**
- Always check tier **before** you promise something in a solution brief.

---

## Output Platform Selection (Visual Deliverables)

When the automation produces **visual outputs** (slide decks, PDFs, designs, etc.), you need to choose where that lives.

**Questions:**
1. What is the output format? (Slides, PDF, doc, web page, design)
2. Is the main goal **branding consistency** or **speed**?
3. Where do branding assets live now? (Slides template, Canva brand kit, etc.)
4. Does the client want to edit the output manually?

### Quick comparison

| Factor | Template-based (Google Slides / PPT) | AI-generated (Gamma / Canva Docs) |
|--------|--------------------------------------|-----------------------------------|
| Visual quality | Depends on your template | Usually “wow” out of the box |
| Branding control | Full, pixel-precise | Limited to themes & brand kits |
| Setup effort | Higher | Lower |
| Per-output cost | Free after setup | Consumes credits / subscription |
| Best for | Consistent, on-brand output | Fast “good enough” visuals |

**Rule of thumb:**
- If this becomes a **repeatable asset** (client uses it monthly/weekly), invest in templates (Slides/PPT).
- If it’s a one-off or low-frequency, AI-generated visuals can be fine.

---

## Quick Platform Decision Flowchart

```text
START: What are you building?
│
├─► Is it mostly glue between SaaS tools, low–medium complexity?
│     └─► YES → Make.com
│
├─► Does it need real split + merge logic, complex branching, or heavy transforms?
│     └─► YES → N8N (Cloud for clients, self-hosted for you)
│
├─► Is it code-related CI/CD or git-native automation?
│     └─► YES → GitHub Actions
│
├─► Is it memory-intensive / HTML-heavy / algorithmic?
│     └─► YES → Custom Code
│
└─► Not sure?
      └─► Start with Idea Architect Agent + Feasibility Agent


⸻

Cost Comparison (Monthly Rough)

Volume	Make.com	N8N (self-host)	GitHub Actions
Light (~1k ops)	≈$9	$0 (maybe $5 VPS)	$0
Medium (~10k ops)	≈$29	$0 (same host)	$0
Heavy (50k+ ops)	$59+	$5–20 hosting	Possibly $0 (if under minutes limit)

Always combine:
	•	Platform cost (subscription + ops),
	•	Infra cost (for self-hosted),
	•	Your time (complex vs simple architectures).

⸻

MCP Access Reference

CRITICAL: Always use MCP server tools (mcp__*__*) for integrations when they exist.
Do not handcraft HTTP calls to n8n/Make APIs unless you have a very specific reason.

N8N MCP

Check documentation first:

mcp__n8n-mcp__tools_documentation(
  topic: "n8n_update_partial_workflow",
  depth: "full"
)

Common tools:

# Search nodes
mcp__n8n-mcp__search_nodes({query: "webhook"})

# Get node docs
mcp__n8n-mcp__get_node({nodeType: "nodes-base.webhook", mode: "docs"})

# Get workflow data
mcp__n8n-mcp__n8n_get_workflow({id: "workflowId", mode: "full"})

# Partial update
mcp__n8n-mcp__n8n_update_partial_workflow({id: "...", operations: [...]})

# Validation
mcp__n8n-mcp__validate_node({nodeType: "...", config: {...}, mode: "full"})
mcp__n8n-mcp__validate_workflow({workflow: {...}})

Correct connection syntax (partial update):

{
  "type": "addConnection",
  "source": "Loop Subfolders",  // exact node name
  "sourceOutput": "done",       // output name as STRING
  "target": "List All Folders",
  "targetInput": "main"
}

Key rules:
	•	Use source / target (NOT sourceNode / targetNode).
	•	sourceOutput / targetInput are strings (“main”, “done”), not numbers.
	•	Node names are case-sensitive and must match exactly.

Patterns to remember:
	•	splitInBatches:
	•	$('NodeName').all() does not accumulate inside the loop.
	•	If you need “all items”, fetch them outside the loop.
	•	Google Drive search:
	•	Always scope by folderId and recursive: true when searching under a folder.
	•	Avoid “search all of My Drive” on big accounts.

Example:

{
  "folderId": {
    "__rl": true,
    "value": "={{$('Create Root Folder').first().json.id}}",
    "mode": "id"
  },
  "options": {
    "recursive": true
  }
}


⸻

Make.com MCP

# Org ID (example)
organizationId: 435122

# List scenarios
mcp__make__scenarios_list({teamId: ...})

# List modules for an app
mcp__make__app-modules_list({
  organizationId: 435122,
  appName: "airtable",
  appVersion: 1
})

# Get module docs
mcp__make__app-module_get({
  organizationId: 435122,
  appName: "airtable",
  appVersion: 1,
  moduleName: "CreateARecord",
  format: "instructions"
})

# Validate configuration
mcp__make__validate_module_configuration({
  organizationId: 435122,
  teamId: ...,
  appName: "airtable",
  appVersion: 1,
  moduleName: "CreateARecord",
  parameters: {...},
  mapper: {...}
})


⸻

Workflow Optimization Patterns (High-Level)

Applies to Make.com, N8N, Zapier, GitHub Actions, etc.

Pattern 1 – Early Filtering (Biggest Win)

Bad:

Raw data (100 items)
 → API Call (100 ops)
 → Normalize (100 ops)
 → Filter (10 items left)

Good:

Raw data (100 items)
 → Filter (10 items left)
 → API Call (10 ops)
 → Normalize (10 ops)

	•	Typical savings: 40–90% operations.
	•	Move cheap checks (location, keywords, status) before expensive steps.

⸻

Pattern 2 – Redundant Module Removal
	•	Find modules whose outputs:
	•	Are never referenced downstream, and
	•	Have no side effects (no writes/emails/etc).
	•	Remove them.
	•	This reduces mental load and operations.

⸻

Pattern 3 – Split Filter Logic (Early vs Late)

Idea:
	•	Split filters into:
	•	Early: cheap criteria (strings, booleans).
	•	Late: expensive criteria (derived metrics, API-enriched fields).

Example:

Early: hasKuta == true AND url NOT CONTAIN "land"
 → Expensive: Normalize price
 → Late: price <= 300000

You still enforce all criteria, just in a smarter order.

⸻

Optimization Method
	1.	Map modules and count operations (rough).
	2.	Spot where most operations happen.
	3.	Propose a re-order (filters earlier, redundant modules removed).
	4.	Run verification (see separate results-verification-guide.md).
	5.	Only then, ship it.

⸻

Real-World Example – Lombok Capital
	•	Before: 555 operations per run.
	•	After: 240 operations per run.
	•	Savings: 56%.
	•	Output: still 15 properties before and after.
	•	Verification: counts + sample data + filter equivalence check.

Key moves:
	•	Early filtering (location/keywords/status first).
	•	Removed redundant “data quality” modules.
	•	Kept price filter after normalization but on fewer items.
