# Eugene AMA Document Organizer - Summary

**Version:** v9.2
**Last Updated:** January 26, 2026
**Status:** Production Ready - New Streamlined Tracker Implemented

---

## Agent IDs (Resume Work)

**CRITICAL:** Use these agent IDs to resume work in new conversations.

### This Session (2026-01-26)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| a419858 | solution-builder-agent | Updated workflow for new Dokumenten_Tracker sheet | ✅ Complete |

### Previous Session (2026-01-25/26)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| a06ac33 | solution-builder-agent | Built Eugene Workflow Monitor (hourly checks) | ✅ Complete |
| a0340d3 | server-ops-agent | Server crash investigation (execution 5729) | ✅ Complete |
| ad50cf8 | server-ops-agent | Cleanup/swap fix attempt (SSH unresponsive) | ✅ Complete |

### Older Sessions (Still Relevant)

| Agent ID | Type | Task | Status |
|----------|------|------|--------|
| aaeb712 | server-ops-agent | Database fix + disk cleanup (100% disk full) | ✅ Complete |
| af2478a | server-ops-agent | Automated binaryData cleanup cron job setup | ✅ Complete |
| a469a55 | solution-builder-agent | Tracker update fix (Google Sheets API) | ✅ Complete |
| aca266b | solution-builder-agent | Routing logic fix (Core 4 vs Others) | ✅ Complete |
| a9087b3 | solution-builder-agent | Test workflow creation (Chunk 2.5 TEST MODE) | ✅ Complete |

**Usage:** In new conversation: "Resume agent a419858" or reference this summary

---

## Current To-Do List

### ✅ Completed This Session (v9.2)

- [x] Created new streamlined "Dokumenten_Tracker" sheet (35 columns, German names)
- [x] Updated workflow to use new sheet
- [x] Added English/German aliases for document type mapping
- [x] Changed column C header from "01_Projektbeschreibung" to "01_Exposé"
- [x] Updated questions-for-eugene.md with calculation types question
- [x] Marked tracker structure confusion as RESOLVED

### ⏳ Pending

- [ ] **Delete old "Client_Tracker" sheet** (no longer needed)
- [ ] **Test with real document** to verify checkmarks appear correctly
- [ ] **Activate Eugene Workflow Monitor** (ID: EKAOWgdA5FMZaQdW)
- [ ] Get Eugene to clarify calculation types (Bautraegerkalkulation vs other calculations)
- [ ] Reprocess 8 files from Wilhelmsmuehlenweg 3 staging folder
- [ ] Monitor production executions

### ⚠️ Questions for Eugene

1. **Calculation types:** Is it always Bautraegerkalkulation_DIN276, or are there other calculation types?
2. **Baubeschreibung:** What is it and where should it be classified?
3. **Core 4 confirmation:** Are Exposé, Grundbuch, Bautraegerkalkulation, Exit_Strategie correct?

---

## Key Changes This Session

### 1. New Streamlined Tracker Sheet

**Old:** "Client_Tracker" with 70+ columns (confusing doubled structure)
**New:** "Dokumenten_Tracker" with 35 columns (clean German names)

**New Structure:**
| Column | Header | Purpose |
|--------|--------|---------|
| A | Mandant | Client name |
| B | Letzte_Aktualisierung | Last updated timestamp |
| C | 01_Exposé | Core 4 - Exposé/Project description |
| D | 02_Grundbuchauszug | Core 4 - Land registry |
| E | 03_Bautraegerkalkulation_DIN276 | Core 4 - Calculation |
| F | 04_Exit_Strategie | Core 4 - Exit strategy |
| G-AI | 05-33 | Other document types |

### 2. Workflow Updates

**Nodes modified:**
- Lookup Client in Client_Tracker → Now uses "Dokumenten_Tracker"
- Find Client Row and Validate → Looks for "Mandant" field
- Prepare Tracker Update Data → New column mapping with aliases
- Build Google Sheets API Update Request → German columns (C-AI)

**Aliases added:**
- "Expose", "Exposé", "01_Expose" → all map to column C
- "Grundbuch", "Grundbuchauszug" → column D
- "Calculation", "DIN276", "Bautraegerkalkulation" → column E
- "Exit Strategy", "Exit_Strategy" → column F

---

## Important IDs / Paths / Workflow Names

### n8n Workflows

| Workflow Name | ID | Purpose | Status |
|--------------|-----|---------|--------|
| Pre-Chunk 0 - REBUILT v1 | p0X9PrpCShIgxxMP | Email intake, PDF conversion | ✅ Active |
| Chunk 2.5 - Client Document Tracking | okg8wTqLtPUwjQ18 | Classification, routing, tracking | ✅ Active |
| Chunk 2.5 - TEST MODE | FL8cPoYixTTKXY8Z | Rapid testing | ✅ Active |
| Eugene Workflow Monitor | EKAOWgdA5FMZaQdW | Hourly execution health checks | ⏳ Needs Activation |

### Google Sheets

| Sheet Name | Spreadsheet ID | Status |
|------------|----------------|--------|
| Dokumenten_Tracker | 12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I | ✅ Active (NEW) |
| Client_Tracker | 12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I | ❌ Delete this |
| AMA_Folder_IDs | 1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm | ✅ Active |

### File Paths

| File | Purpose |
|------|---------|
| /eugene/questions-for-eugene.md | Questions for client meeting |
| /eugene/ISSUES_BACKLOG.md | Known issues and future improvements |
| /eugene/compacting-summaries/summary_v9.2_2026-01-26.md | This summary |

---

## Server Status

### n8n Server (n8n.oloxa.ai)

- **Status:** Healthy
- **Disk:** ~70% used
- **Swap:** 2GB available
- **Cleanup:** Every 4 hours, 12-hour retention

---

## Technical Notes

### Document Classification Flow

```
Document arrives via email
    ↓
Pre-Chunk 0: Convert to PDF, move to _Staging
    ↓
Chunk 2.5:
    ├── Download from staging
    ├── Claude Vision Tier 1 (category)
    ├── Claude Vision Tier 2 (specific type)
    ├── Map document type → column letter
    ├── Update Dokumenten_Tracker (checkmark + timestamp)
    └── Move to destination folder (Core 4 → specific, others → 37_Others)
```

### Column Mapping Logic

```javascript
// AI returns document type → mapped to internal type → mapped to column
'01_Expose' → '01_Projektbeschreibung' → Column C (header: "01_Exposé")
'Grundbuchauszug' → '02_Grundbuchauszug' → Column D
'Calculation' → '03_Bautraegerkalkulation_DIN276' → Column E
'Exit_Strategy' → '04_Exit_Strategie' → Column F
// Unknown types → '33_Unbekannt' → Column AI
```

---

## Next Steps

1. **Delete old Client_Tracker sheet** (confirm it's no longer needed)
2. **Test with a real document** - send email with PDF, verify:
   - Client lookup works against Dokumenten_Tracker
   - Checkmark appears in correct column
   - Timestamp updates in column B
3. **Activate Eugene Workflow Monitor** in n8n UI
4. **Meet with Eugene** to clarify calculation types and confirm Core 4

---

**Document Version:** summary_v9.2_2026-01-26.md
**Generated:** 2026-01-26 01:15 CET
**Author:** Claude Code (Sway's automation assistant)
