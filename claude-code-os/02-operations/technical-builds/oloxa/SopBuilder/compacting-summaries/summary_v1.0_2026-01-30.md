# SOP Builder Lead Magnet - Build Summary v1.0

**Date:** January 30, 2026
**Workflow ID:** `ikVyMpDI0az6Zk4t`
**Workflow URL:** https://n8n.oloxa.ai/workflow/ikVyMpDI0az6Zk4t
**Frontend URL:** https://sopbuilder.oloxa.ai
**Status:** Production-ready (pending final visual QA)

---

## What This Is

A lead magnet tool where users submit their process information via a web form and receive:
- An AI-scored SOP completeness assessment
- A professionally formatted, improved SOP via email
- If score >= 85%: PDF attachment with the improved SOP
- If score < 85%: Improvement suggestions + resubmission link
- All leads logged to Airtable

---

## Architecture

### Frontend
- **Location (server):** `/var/www/sopbuilder/` on `157.230.21.230`
- **Local copies:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/oloxa/SopBuilder/`
- **Files:** `index.html`, `app.js`, `styles.css`, `logo.png`, `logo-black-transparent.png`
- **SSH key:** `/Users/swayclarke/coding_stuff/.credentials/n8n-server-ssh.key`
- **Web server:** Caddy (auto-HTTPS)

### n8n Workflow (43 nodes)
**Trigger:** Webhook at `https://n8n.oloxa.ai/webhook/sop-builder`

**Key flow:**
```
Webhook → Parse Form → Check Audio → [Audio path: Upload/Transcribe OR Text path] → Merge →
Prepare LLM Request → LLM: Generate Improved SOP (OpenAI gpt-4o-mini) →
Extract Improved SOP → Format Check → Generate Lead ID → Calculate Score →
Route Based on Score →
  ≥85%: Generate Success Email → Generate PDF HTML → Convert to PDF → Send HTML Email (with PDF) → Airtable → Respond
  <85%: Generate Improvement Email → Send Improvement Email (no PDF) → Airtable → Respond
```

### Key Nodes

| Node ID | Name | Purpose |
|---------|------|---------|
| `webhook-trigger` | Webhook Trigger | Receives form submissions |
| `parse-form` | Parse Form Data | Extracts fields incl. company_name |
| `prepare-llm-body` | Prepare LLM Request | **BPS-framework prompt** for OpenAI |
| `llm-automation` | LLM: Generate Improved SOP | OpenAI gpt-4o-mini call |
| `format-check` | Format Check | Regex-based markdown cleanup |
| `calculate-score` | Calculate SOP Score | Scores completeness/clarity/usability |
| `route-email` | Route Based on Score | ≥85% success, <85% improvement |
| `generate-success-email` | Generate Success Email (≥85%) | HTML email + "Congratulations, {name}!" |
| `generate-improvement-email` | Generate Improvement Email (<85%) | HTML email + quick wins + resubmit link |
| `generate-pdf-html` | Generate PDF HTML | Markdown→HTML converter + PDF template |
| `convert-to-pdf` | Convert HTML to PDF | html2pdf.app API |
| `send-email` | Send HTML Email | Gmail with PDF attachment (success path) |
| `send-improvement-email` | Send Improvement Email | Gmail without attachment (improvement path) |

### Credentials
| Service | Credential ID | Name |
|---------|--------------|------|
| Gmail | `aYzk7sZF8ZVyfOan` | Gmail account |
| OpenAI | `xmJ7t6kaKgMwA1ce` | OpenAi account |
| html2pdf.app | API key in node | `bKXk6fNavTofZUsJMdvwEkGIt45rSB3W7s7ePH0r1jPp7mUYkfr3aO4LDHiGxRDr` |
| Airtable | In node | Table `tblEHjJlvorWTgptU` |

---

## Key Technical Details

### BPS Framework Prompt (prepare-llm-body)
The OpenAI system prompt uses the BPS Prompting Framework (Role → Task → Specifics → Context → Examples → Notes) to enforce consistent markdown output:
- `####` for process step headings
- Bold field labels (Owner:, Actions:, Verification:, Escalation:) on own lines
- Bullet points for action items only
- Sequential numbering (1, 2, 3...)
- 5 required sections: Purpose, Preparation, Process Flow, Verification Checklist, Document Control
- Temperature: 0.4 (low for consistency)
- Max tokens: 3000

### PDF HTML Converter (generate-pdf-html)
9-step markdown-to-HTML pipeline:
1. H4 headers (`####` → `<h4>`)
2. H3 headers (`###` → `<h3>`)
3. H2 headers (`##` → `<h2>`)
4. H1 headers (`#` → `<h1>`)
5. Horizontal rules
6. Checkboxes
7. Numbered lists → H3 step headers
8. Field labels (Owner/Actions/etc.) → `<p class="field-label">` (NOT bullets)
9. Bullet lists (action items only get bullets)
10. Paragraph wrapping

### CSS Heading Hierarchy
- H1: 28px, bold, border-bottom red
- H2: 22px, bold, gold left border (section headers)
- H3: 18px, bold, 35px top margin (process steps)
- H4: 16px, bold, 30px top margin (sub-steps)
- Field labels: 14px, bold, no bullets

### Email Features
- **Success email:** Dark theme, score display, "Congratulations, {name}!", SOP content, celebration section, blue "Book a Discovery Call →" CTA linking to `https://calendly.com/sway-oloxa/discovery-call`
- **Improvement email:** Dark theme, score display, top 3 quick wins, "Let's Improve My SOP →" resubmit button with pre-filled data
- **Subject format:** `{Company}'s Improved SOP: {Title} - Scored {Score}%`

### Frontend Features
- Multi-step form (5 steps with progress bar)
- Company name field (Step 3)
- Audio upload OR text input
- Capitalized dropdown values (Operations, Sales, Marketing, etc.)
- Resubmission support (pre-fills from URL params)
- Success page with celebration emoji

---

## Known Issues / Pending

1. **Gmail credential:** `aYzk7sZF8ZVyfOan` may need re-auth with swayclarkeii@gmail.com (was previously authenticated with thebluebottle.io)
2. **Airtable company_name:** Column doesn't exist in Airtable table — company_name is stripped from Format for Airtable output. Add column if tracking is needed.
3. **Format Check node:** Has pre-existing validation warnings (non-blocking)

---

## Session Agent IDs (January 30, 2026)

| Agent ID | Type | Task |
|----------|------|------|
| `abdcdfb` | solution-builder | PDF markdown converter (initial) |
| `a2dafe2` | test-runner | Initial PDF test |
| `af087c3` | solution-builder | Email node split (separate improvement email) |
| `a9aba85` | solution-builder | Company name support (5 nodes) |
| `a970cd4` | server-ops | SSH key discovery |
| `a08a67d` | solution-builder | Email subject + PDF template fixes |
| `ad63583` | solution-builder | Format Check code node |
| `a6633b7` | solution-builder | Final email/PDF polish (celebration, logo, title) |
| `a61be77` | solution-builder | PDF process flow formatting fix |
| `ae3715a` | solution-builder | BPS framework prompt update |
| `a992efb` | test-runner | BPS prompt testing (2 tests) |
| `af674a5` | solution-builder | CTA button, name greeting, field label fixes |
| `ac06419` | solution-builder | H4 pound signs, spacing, Calendly link fix |

---

## How to Resume Work

```
Workflow ID: ikVyMpDI0az6Zk4t
Frontend: /var/www/sopbuilder/ (SSH key: /Users/swayclarke/coding_stuff/.credentials/n8n-server-ssh.key)
Server: 157.230.21.230

Key nodes to modify:
- LLM prompt: prepare-llm-body
- PDF template: generate-pdf-html
- Success email: generate-success-email
- Improvement email: generate-improvement-email
- Scoring: calculate-score
- Format cleanup: format-check

Test command:
curl -X POST "https://n8n.oloxa.ai/webhook/sop-builder" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "email=swayclarkeii@gmail.com" \
  --data-urlencode "companyName=Oloxa" \
  --data-urlencode "name=Sway" \
  --data-urlencode "goal=Employee Onboarding SOP" \
  --data-urlencode "department=Operations" \
  --data-urlencode "end_user=HR coordinators" \
  --data-urlencode "improvement_type=Quality" \
  --data-urlencode "process_steps=[comprehensive steps with PURPOSE, PREPARATION, PROCESS STEPS with Owner/Verification, VERIFICATION CHECKLIST, DOCUMENT CONTROL]" \
  --data-urlencode "validation_feedback=Comprehensive SOP with all required sections."
```

To deploy frontend changes:
```bash
scp -i /Users/swayclarke/coding_stuff/.credentials/n8n-server-ssh.key [file] root@157.230.21.230:/var/www/sopbuilder/
```
