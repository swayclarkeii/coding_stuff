# Project Reference - O-L-O-X-A

**Owner:** Sway Clarke
**Company:** O-L-O-X-A (spelled: O-L-O-X-A)
**GitHub Username:** swayclarkeii
**Last Updated:** January 15, 2026

---

## Core Databases

All PA agents (my-pa-agent, pa-crm-agent, pa-strategy-agent, pa-family-agent) should reference these database IDs.

### 1. CRM Spreadsheet (Google Sheets)

**Spreadsheet ID:** `1PwIqO1nfEeABoRRvTml3dN9q1rUjHIMVXsqOLtouemk`

**Link:** https://docs.google.com/spreadsheets/d/1PwIqO1nfEeABoRRvTml3dN9q1rUjHIMVXsqOLtouemk/edit

**Purpose:** Client relationship management, prospect tracking, pipeline stages

**Access:** pa-crm-agent (primary), my-pa-agent (orchestrator)

---

### 2. Notion Tasks Database

**Data Source ID:** `39b8b725-0dbd-4ec2-b405-b3bba0c1d97e`

**Link:** https://www.notion.so/889fff971c29490ba57c322c0736e90a

**Purpose:** Personal and business task management

**Access:** pa-strategy-agent (primary), pa-family-agent, my-pa-agent (orchestrator)

---

### 3. Notion O-L-O-X-A Projects Database

**Data Source ID:** `2d01c288-bb28-81ef-a640-000ba0da69d4`

**Link:** https://www.notion.so/2d01c288bb2881f6a1bee57188992200

**Purpose:** Project tracking with Timeline and Kanban views

**Access:** pa-strategy-agent (primary), my-pa-agent (orchestrator)

**Views:**
- Timeline view (for project scheduling)
- Kanban view (for project phases)

---

## Common Projects

### Active Projects (as of Jan 14, 2026)

1. **AMA System** (for Eugene) - Currently in Testing phase
2. **Personal Accounting System** - Currently in Testing phase
3. **Lombok Invest Capital** - Currently in Deployment phase
4. **Tax System** - Check if exists, create if missing

---

## Important Notes

- **Company Name:** O-L-O-X-A (always spell it out)
- **Reference:** CLAUDE.md for agent delegation rules
- **MCP Modes:** Use pa-mode for CRM/Notion work, core-mode for automation work
