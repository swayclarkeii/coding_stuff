# Eugene Document Organizer - V10 Phase 1

## Batch Analysis Architecture

**Started:** January 19, 2026
**Status:** Planning

---

## What's Different in V10

V9 analyzed documents **individually** → Unreliable client identification

V10 analyzes documents **in batches** → Find "common denominator" identifier

---

## Core Concept

When email arrives with multiple attachments:
1. Batch analyze ALL attachments together
2. Find the most common/consistent identifier across documents
3. Use sender email as secondary identifier
4. Match against registry (sender_email + project_name)

---

## Key Changes from V9

1. **New: Attachment Counter** - Single vs Multiple logic
2. **New: Batch PDF Converter** - Process all attachments together
3. **Modified: Claude Vision** - Accept multiple PDFs, find common identifier
4. **New: Registry Column** - `sender_email` for matching
5. **Modified: Decision Logic** - Same email + same/different project routing

---

## Folder Structure

```
v10_phase_1/
├── README.md           # This file
├── workflows/          # Exported workflow JSONs
├── tests/              # Test scenarios and results
└── docs/               # Design documents and summaries
    └── SESSION_SUMMARY_2026-01-19.md
```

---

## Previous Versions

- **V8** - Document AI OCR approach (archived)
- **V9** - Claude Vision (direct PDF reading) - Working, archived as backup

---

## Quick Links

- [Session Summary](docs/SESSION_SUMMARY_2026-01-19.md) - Full context and design
- [V9 Backup](../.archive/v9_phase_1/) - Last working version
