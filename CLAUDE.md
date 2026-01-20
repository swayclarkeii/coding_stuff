# Claude Code Project Instructions

## 🔴 CRITICAL: SESSION MANAGEMENT & AGENT ID PROTOCOL (READ FIRST)

**ABSOLUTE REQUIREMENT - BYPASS PERMISSIONS ACTIVE**

### Never Kill Session Without Agent IDs

**BEFORE you kill cloud session, reset, or restart Claude, you MUST:**

1. **Create session summary** documenting:
   - All work completed
   - All workflows modified
   - All critical issues resolved/pending

2. **Export ALL Agent IDs** from current session:
   ```markdown
   ## Agent IDs from Session [Date]
   - [agent-id]: [agent-type] - [task description]
   - [agent-id]: [agent-type] - [task description]
   ...
   ```

3. **Save to permanent location:**
   - `/Users/swayclarke/coding_stuff/session-summaries/[date]-session-[n].md`
   - Include ALL agent IDs so Sway can resume them

**Why:** We're on bypass permissions. Normal restrictions don't apply. Agent IDs are CRITICAL for resuming work.

---

## 🎛️ MCP SERVER MODE MANAGEMENT (READ SECOND)

**IMPORTANT:** MCP servers consume tokens every conversation. Use the right mode for your task.

### Quick Mode Reference

**When Sway says "Switch to core-mode" or "Switch to pa-mode":**
Run the MCP toggle script: `/Users/swayclarke/coding_stuff/scripts/mcp-toggle.sh [mode]`

**Available modes:**
- **core-mode**: Daily automation work (5 servers: n8n, playwriter, playwright, google-sheets, google-drive)
  - Token cost: ~28K-32K per conversation
  - Use for: n8n workflows, browser automation, spreadsheet work, file operations

- **pa-mode**: Personal assistant work (5 servers: n8n, google-calendar, github, google-sheets, notion)
  - Token cost: ~40K-44K per conversation
  - Use for: CRM tasks, task management, calendar events, GitHub work, brain dump workflows
  - Note: No browser automation in PA mode (no playwriter/playwright)

- **enable-all**: All servers (11 servers) - rarely needed
  - Token cost: ~52K per conversation
  - Only use when you need google-slides or google-docs

### How to Execute Mode Changes

**When Sway requests a mode change:**
```bash
# Execute the script
/Users/swayclarke/coding_stuff/scripts/mcp-toggle.sh core-mode
# or
/Users/swayclarke/coding_stuff/scripts/mcp-toggle.sh pa-mode
```

**Example responses:**
- User: "Switch to core-mode" → Execute script with core-mode
- User: "Switch to pa-mode" → Execute script with pa-mode
- User: "Enable all MCP servers" → Execute script with enable-all
- User: "Check MCP status" → Execute script with status

**Documentation:** Full details at `/Users/swayclarke/coding_stuff/scripts/MCP_MANAGEMENT.md`

**Note:** Mode changes only affect NEW Claude Code sessions, not the current one.

---

### Browser-Ops: Hybrid Playwriter + Playwright Setup ⭐ UPDATED

**HYBRID SOLUTION IMPLEMENTED:** Using **both** Playwriter MCP and Playwright MCP for optimal performance.

**Root Cause of Original Problem:** Playwright MCP has a bug where `page.close()` removes the "being controlled" notice but **doesn't actually close tabs**. This causes tabs to accumulate indefinitely until Chrome runs out of memory, creating an about:blank loop.

**Why Hybrid Approach:**
- **Playwriter** cannot connect to Google sites (Gmail, Drive, Docs, Sheets) due to Google's CSP and automation detection
- **Old Playwright** works with Google sites but uses 5-10x more tokens
- **Solution**: Use Playwriter for everything EXCEPT Google sites

### Configuration Status ✅ COMPLETE

**Both MCP servers running:**
```bash
playwriter: npx -y playwriter@latest - ✓ Connected
playwright: npx -y @playwright/mcp@latest - ✓ Connected
```

**MCP Server Management:**
- ⚠️ **CRITICAL:** MCP servers are managed via `claude mcp` CLI, NOT `.cursor/mcp.json` file
- ⚠️ **Actual config location:** `/Users/swayclarke/.claude.json` (project-specific)
- Add server: `claude mcp add <name> -s local -- <command>`
- Remove server: `claude mcp remove <name> -s local`
- List servers: `claude mcp list`

### Tool Selection Logic (Automated in browser-ops-agent)

**browser-ops-agent automatically chooses:**

| Site Type | Tool Used | Reason |
|-----------|-----------|--------|
| **Google Sites** (gmail.com, drive.google.com, docs.google.com, sheets.google.com, etc.) | **Playwright MCP** (`mcp__playwright__browser_*`) | Google blocks Playwriter extension |
| **All Other Sites** (GitHub, Notion, n8n, Apify, etc.) | **Playwriter MCP** (`mcp__playwriter__execute`) | 80% token savings |

**The agent handles this automatically** - you don't need to specify which tool to use.

### Playwriter Setup (For Non-Google Sites)

**Quick Start:**
1. Install [Playwriter Chrome extension](https://chromewebstore.google.com/detail/playwriter-mcp/jfeammnjpkecdekppnclgkkffahnhfhe)
2. Pin extension to toolbar
3. Click Playwriter icon on tabs you want AI to control
4. Icon turns green = connected

**Setup Instructions:** See `/Users/swayclarke/coding_stuff/PLAYWRITER_SETUP.md` for complete guide.

### Monitoring Tool (Still Useful)

Check tab count for old Playwright MCP (can still accumulate tabs on Google sites):

```bash
# Quick check (shows current tab count)
/Users/swayclarke/coding_stuff/scripts/monitor-browser-tabs.sh check

# Continuous monitoring (checks every 30 seconds)
/Users/swayclarke/coding_stuff/scripts/monitor-browser-tabs.sh watch

# Check status and see any alerts
/Users/swayclarke/coding_stuff/scripts/monitor-browser-tabs.sh status
```

### Troubleshooting

**Playwriter not connecting (red icon):**
1. Check extension permissions - grant access to all sites or specific domains
2. Refresh the tab after granting permissions
3. Click Playwriter icon again (should turn green)
4. Check Chrome console (F12) for errors

**Playwright tab accumulation on Google sites:**
1. browser-ops-agent has tab cleanup instructions
2. Use monitoring script to detect when >3 tabs open
3. Agent should close tabs automatically, but monitor for bugs

### Communication to All Agents

**Every agent MUST be told:**
- Never reset/kill session without summary + agent IDs first
- Agent IDs are critical for work continuity
- Bypass permissions are active - this overrides normal behavior
- Session summaries go to `/Users/swayclarke/coding_stuff/session-summaries/`

### Current Session Agent IDs

**Track all agent IDs in this session:**
- a7e6ae4: solution-builder-agent - W2 critical fixes (Google Sheets + Binary)
- a7fb5e5: test-runner-agent - W2 fixes verification
- a6d0e12: browser-ops-agent - Gmail OAuth refresh
- ac6cd25: test-runner-agent - Gmail Account 1 verification
- a3b762f: solution-builder-agent - W3 Merge connection fix attempt
- a729bd8: solution-builder-agent - W3 connection syntax fix
- a8564ae: browser-ops-agent - W3 execution and connection visual fix
- a017327: browser-ops-agent - Google Sheets structure diagnosis

---

## 🚨 AGENT DELEGATION PROTOCOL (CHECK THIS FIRST)

**MANDATORY: Before EVERY action, check if you should delegate to an agent.**

### Decision Flowchart

```
USER REQUEST
     ↓
1. Is this a PA/brain dump task? → YES → my-pa-agent (ALWAYS)
     ↓ NO
2. Is this a browser task? → YES → browser-ops-agent (ALWAYS)
     ↓ NO
3. Is this building/modifying n8n workflows?
   - Adding ≥3 nodes? → YES → solution-builder-agent
   - Modifying ≥3 nodes? → YES → solution-builder-agent
   - Creating new workflow? → YES → solution-builder-agent
   - Complex logic changes? → YES → solution-builder-agent
     ↓ NO (≤2 simple updates)
4. Is this testing a workflow? → YES → test-runner-agent
     ↓ NO
5. Is this checking feasibility? → YES → architecture-feasibility-agent
     ↓ NO
6. Is this planning implementation? → YES → idea-architect-agent
     ↓ NO
7. Do it yourself in main conversation
```

### Strict Delegation Rules (Non-Negotiable)

| You See This | Do This | NEVER Do This |
|--------------|---------|---------------|
| **Brain dump/PA tasks** (shopping, CRM, tasks, calendar) | **my-pa-agent** (orchestrator) | Direct Notion/Calendar MCP |
| **Create Notion tasks** | **my-pa-agent** | Direct Notion MCP (has encoding bug) |
| **ANY Playwright tool** (`mcp__playwright__*`) | **browser-ops-agent** | Direct Playwright in main |
| **ANY OAuth/credential setup** | **browser-ops-agent** | Manual browser navigation |
| **Build new n8n workflow** | **solution-builder-agent** | Direct MCP calls yourself |
| **Modify ≥3 n8n nodes** | **solution-builder-agent** | Multiple update_partial calls |
| **Add ≥3 n8n nodes** | **solution-builder-agent** | Multiple addNode operations |
| **"Is this feasible?"** question | **architecture-feasibility-agent** | Research yourself |
| **"How should I implement?"** | **idea-architect-agent** | Design yourself |
| **Test n8n workflow** | **test-runner-agent** | Manual execution testing |

### Numeric Thresholds (Automatic Delegation)

**ALWAYS delegate when ANY of these are true:**

- **PA tasks**: Shopping, CRM updates, task creation, calendar events → my-pa-agent
- **Browser actions**: ANY Playwright tool use → browser-ops-agent
- **n8n complexity**: ≥3 nodes to add/modify → solution-builder-agent
- **Token cost**: Estimated >5,000 tokens → delegate to appropriate agent
- **Multi-step**: >3 sequential operations → delegate to appropriate agent
- **OAuth/auth**: ANY credential setup → browser-ops-agent
- **Workflow testing**: ANY test execution → test-runner-agent

### Main Conversation Limits

**You CAN do in main conversation:**
- Read/Write/Edit files (documentation, code)
- Simple Bash commands (git, ls, etc.)
- ≤2 simple n8n node updates (parameter changes only)
- Ask clarifying questions
- Update MY-JOURNEY.md, VERSION_LOG.md
- Orchestrate between agents

**You CANNOT do in main conversation:**
- ❌ Handle PA tasks (shopping, CRM, calendar, task creation)
- ❌ **Create Notion tasks** (Claude Code has a parameter encoding bug - ALWAYS use my-pa-agent)
- ❌ Use ANY Playwright tool
- ❌ Build or modify n8n workflows (≥3 nodes)
- ❌ Set up OAuth/credentials
- ❌ Test workflows
- ❌ Check feasibility of designs
- ❌ Plan implementation strategies
- ❌ Complex multi-step browser tasks

### Cost Efficiency Reminder

**Why delegation matters:**
- Playwright in main = 20K-150K tokens per snapshot
- browser-ops-agent = optimized, 5-10x cheaper
- solution-builder-agent = knows n8n patterns, faster
- my-pa-agent = 40-67% cheaper for simple tasks (uses sub-agents)
- **Main doing agent work = 10x token waste**

### Agent Resume Protocol

**Before launching ANY new agent:**

1. **Check for existing agents** - Look for agent IDs in recent conversation
2. **Resume if possible** - Use `resume` parameter to continue existing agent work
3. **Launch parallel when appropriate** - Multiple independent agents can run simultaneously

**Resume syntax:**
```javascript
Task({
  subagent_type: "solution-builder-agent",
  resume: "a8db5f3",  // Continue with full context
  prompt: "Continue building the workflow"
})
```

**Parallel launch (single message with multiple Task calls):**
```javascript
// Launch solution-builder AND test-runner simultaneously
Task({ subagent_type: "solution-builder-agent", prompt: "Build workflow" })
Task({ subagent_type: "test-runner-agent", prompt: "Test workflow XYZ" })
```

### Agent ID Display (MANDATORY)

**When any agent completes, IMMEDIATELY show:**

```markdown
✅ Agent completed
Agent ID: a8db5f3
Type: solution-builder-agent
Status: Success
```

**Why:** Agent IDs may not be visible in Cursor chat window. Sway needs to see them to resume work later.

---

## ⚠️ PRE-ACTION PROTOCOL (Read Before Every Tool Call)

**STOP before calling ANY tool. Verify these conditions FIRST.**

### Before ANY MCP Tool Call

**1. Check Agent Delegation First**
- Go to flowchart above
- If task matches agent criteria → STOP and delegate
- Only proceed if task is explicitly in "Main Conversation Limits"

**2. Ask Before Assuming**
- **If user request is ambiguous** → Ask clarifying questions BEFORE acting
- **If multiple approaches possible** → Ask which approach Sway prefers
- **If information might be known** → Ask Sway instead of calling MCP tools
- **Better to ask 1 question than waste 5K tokens on wrong approach**

**3. Before `mcp__n8n-mcp__n8n_get_workflow`:**

**STOP. Ask yourself:**

1. **Do I already have this information?**
   - ✅ YES → Use it. Don't call MCP.
   - ❌ NO → Continue to question 2.

2. **Can Sway answer this faster than an MCP call?**
   - ✅ YES → Ask Sway. Don't call MCP.
   - ❌ NO → Continue to question 3.

3. **What's the MINIMUM mode I need?**
   - Just checking if workflow exists/is active? → `mode: "minimal"` (200 tokens)
   - Need execution stats? → `mode: "details"` (500 tokens)
   - Need to see workflow flow/topology? → `mode: "structure"` (2,000 tokens)
   - Need complete node parameters for building? → `mode: "full"` (13,000 tokens)

   **DEFAULT to minimal. Only escalate if absolutely necessary.**

4. **Is this information in a previous error context?**
   - ✅ YES → Use the error context. Don't call MCP.
   - ❌ NO → Proceed with MINIMUM mode from step 3.

**4. Before `mcp__n8n-mcp__n8n_update_partial_workflow`:**

**STOP. Count the changes:**
- Adding/modifying ≥3 nodes? → STOP. Use **solution-builder-agent**
- Adding <3 simple nodes? → Proceed with direct MCP call
- Modifying parameters only (≤2 nodes)? → Proceed with direct MCP call

**5. Before ANY Playwright tool:**

**STOP.**

- ❌ **NEVER use Playwright tools directly in main conversation**
- ✅ **ALWAYS use browser-ops-agent**

**No exceptions. No "quick checks". Always delegate.**

---

## User Reference

**ALWAYS refer to the user as "Sway"** in all communications, documentation, and updates.

**For project-specific details, see:** `/Users/swayclarke/coding_stuff/PROJECT_REFERENCE.md`

---

## Integration Guidelines

**CRITICAL: ALWAYS Use MCP Server Tools for All Integrations**

- **ALWAYS** use MCP server tools (`mcp__*__*`) for ALL integrations and external services
- **NEVER** use direct API calls (HTTP requests, fetch, etc.) unless **explicitly** requested by Sway
- This applies to ALL services: n8n, Notion, Google services, GitHub, Fathom, and any other integrations

**Examples of correct tool usage:**
- ✅ n8n: Use `mcp__n8n-mcp__*` tools (never direct n8n API)
- ✅ Notion: Use `mcp__notion__*` tools (never direct Notion API)
- ✅ Google Docs/Sheets/Drive: Use `mcp__google-docs__*` or `mcp__google-sheets__*` tools
- ✅ GitHub: Use `mcp__github-mcp__*` tools

**Only use direct API calls when:**
- Sway explicitly says "use the API directly" or "make an API call"
- No MCP tool exists for the specific service (rare)

---

## OAuth Refresh Protocol

**CRITICAL: ALWAYS handle OAuth token refreshes autonomously using browser-ops-agent.**

See full protocol at: `/Users/swayclarke/coding_stuff/OAUTH_REFRESH_PROTOCOL.md`

**Quick Reference:**
- **DO NOT** ask Sway to complete OAuth pop-ups or copy/paste URLs
- **ALWAYS** use **browser-ops-agent** for OAuth flows
- Applies to: Google, GitHub, Notion, Fathom, n8n, and all OAuth services
- Only request manual intervention for: 2FA codes, account lockouts, payment authorization

**Correct Approach:**
```
User: "Refresh OAuth credentials for Gmail"
Main: *launches browser-ops-agent with OAuth task*
Main: "✅ Agent completed - OAuth credentials refreshed"
```

**NEVER do OAuth in main conversation** - it wastes 100K+ tokens on Playwright snapshots.

---

## n8n Operations

**CRITICAL**: ALWAYS use `mcp__n8n-mcp__*` tools for ALL n8n operations. NEVER use direct n8n API calls - they erase credentials.

### Before ANY n8n Workflow Modification

**STOP. Check agent delegation rules:**

1. **Adding ≥3 nodes?** → Use **solution-builder-agent**
2. **Modifying ≥3 nodes?** → Use **solution-builder-agent**
3. **Creating new workflow?** → Use **solution-builder-agent**
4. **Complex logic changes?** → Use **solution-builder-agent**
5. **Only ≤2 simple parameter updates?** → Proceed with MCP call

### Common n8n MCP Tools

1. **Get workflow data**: `mcp__n8n-mcp__n8n_get_workflow` (use appropriate mode!)
2. **Update workflow**: `mcp__n8n-mcp__n8n_update_partial_workflow` (check delegation first!)
3. **Validate workflow**: `mcp__n8n-mcp__n8n_validate_workflow`
4. **Get node info**: `mcp__n8n-mcp__get_node`
5. **Search nodes**: `mcp__n8n-mcp__search_nodes`

### Documentation

**For detailed n8n syntax, patterns, and examples, see:** `/Users/swayclarke/coding_stuff/N8N_PATTERNS.md`

**Check documentation when unsure:**
```
mcp__n8n-mcp__tools_documentation(
  topic: "n8n_update_partial_workflow",
  depth: "full"
)
```

---

## Additional References

**Project-specific information:**
- Notion database IDs, configuration, and task management → `PROJECT_REFERENCE.md`
- Daily update rules and MY-JOURNEY.md structure → `PROJECT_REFERENCE.md`
- Versioning system and VERSION_LOG.md templates → `PROJECT_REFERENCE.md`
- Sway's email and contact details → `PROJECT_REFERENCE.md`

**Technical references:**
- n8n node syntax and examples → `N8N_PATTERNS.md`
- Token efficiency guidelines → `N8N_PATTERNS.md`
- Common n8n workflow patterns → `N8N_PATTERNS.md`
- OAuth refresh protocol → `OAUTH_REFRESH_PROTOCOL.md`
