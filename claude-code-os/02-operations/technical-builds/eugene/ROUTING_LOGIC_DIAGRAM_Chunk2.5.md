# Chunk 2.5 Routing Logic - Before vs After

## BEFORE (Old Logic)

```
Document Classification
         ↓
Determine Action Type
         ↓
    ┌────┴────┐
    │ Switch  │
    └────┬────┘
         ↓
   ┌─────┴─────┬─────────┬──────────┐
   │           │         │          │
CORE      SECONDARY   LOW_CONF   UNKNOWN
   │           │         │          │
   ↓           ↓         ↓          ↓
Specific   37_Others  38_Unknowns  38_Unknowns
Folders
(01,03,
10,36)
```

**Issues:**
- Relied on AI's `actionType` determination
- Complex multi-step decision tree
- 38_Unknowns used for uncertain classifications
- Harder to predict document routing

---

## AFTER (New Simplified Logic)

```
Document Classification
         ↓
    documentType
         ↓
   ┌─────┴─────┐
   │           │
Is Core 4?   NO
   │           │
   YES         ↓
   │      37_Others
   ↓
Specific Folders
┌──┬──┬──┬──┐
│01│03│10│36│
└──┴──┴──┴──┘
```

**Core 4 Document Types:**
- `01_Projektbeschreibung` (Exposé)
- `03_Grundbuchauszug` (Grundbuch)
- `10_Bautraegerkalkulation_DIN276` (Calculation)
- `36_Exit_Strategie` (Exit Strategy)

**Routing Rules:**
1. IF `documentType` is in Core 4 list → Route to specific folder (01, 03, 10, or 36)
2. IF `documentType` is ANYTHING ELSE → Route to 37_Others

**Benefits:**
- Simple binary decision (Core 4 vs Others)
- Predictable routing based on hardcoded list
- No reliance on AI's action type determination
- 38_Unknowns folder no longer used
- Tracker still gets updated with full classification

---

## Code Implementation

**Core 4 Check:**
```javascript
const CORE_4_TYPES = [
  '01_Projektbeschreibung',
  '03_Grundbuchauszug',
  '10_Bautraegerkalkulation_DIN276',
  '36_Exit_Strategie'
];

if (CORE_4_TYPES.includes(documentType)) {
  // Route to specific folder
} else {
  // Route to 37_Others
}
```

---

## Example Routing Outcomes

| Document Type | Old Logic | New Logic | Tracker Update |
|---------------|-----------|-----------|----------------|
| `01_Projektbeschreibung` | Folder 01 (if CORE) | ✅ Folder 01 | `01_Projektbeschreibung` |
| `03_Grundbuchauszug` | Folder 03 (if CORE) | ✅ Folder 03 | `03_Grundbuchauszug` |
| `10_Bautraegerkalkulation_DIN276` | Folder 10 (if CORE) | ✅ Folder 10 | `10_Bautraegerkalkulation_DIN276` |
| `36_Exit_Strategie` | Folder 36 (if CORE) | ✅ Folder 36 | `36_Exit_Strategie` |
| `05_Kaufvertrag` | 37_Others (if SECONDARY) or 38_Unknowns | ✅ 37_Others | `05_Kaufvertrag` |
| `12_Baugenehmigung` | 37_Others (if SECONDARY) or 38_Unknowns | ✅ 37_Others | `12_Baugenehmigung` |
| `Unknown_Type` | 38_Unknowns | ✅ 37_Others | `Unknown_Type` |

**Key Change:** ALL non-Core-4 documents go to 37_Others, regardless of AI confidence or action type.

---

## Tracker Update Behavior (Unchanged)

**The tracker ALWAYS gets updated with the classified document type, regardless of routing:**

```
Document: "Expose.pdf"
   ↓
Classification: "01_Projektbeschreibung"
   ↓
   ├─ Routing: Folder 01 ✅
   └─ Tracker: "01_Projektbeschreibung" ✅
```

```
Document: "Contract.pdf"
   ↓
Classification: "05_Kaufvertrag"
   ↓
   ├─ Routing: 37_Others ✅
   └─ Tracker: "05_Kaufvertrag" ✅
```

---

## Debug Fields Available

**New:**
- `debug_isCore4` - Boolean showing if document matched Core 4 list

**Existing:**
- `debug_variableNameSearched` - Which folder variable was looked up
- `debug_folderLookupSize` - Number of folder mappings loaded
- `destinationFolderName` - Human-readable folder name
- `documentType` - The classified document type
- `tier1Category` - Broad category classification

---

## Migration Notes

**What Changed:**
- Routing decision logic only (1 node: "Get Destination Folder ID")
- No changes to classification, tracker updates, or error handling

**What Stayed the Same:**
- All classification logic (Claude Vision, GPT-4, parsing)
- Tracker update mechanism
- Error handling and notifications
- File movement operations

**Unreachable Nodes After Change:**
- "Lookup 38_Unknowns Folder" (sheets-4)
- "Get 38_Unknowns Folder ID" (code-6)
- "Move File to 38_Unknowns" (drive-2)

These nodes still exist in the workflow but are no longer called with the new routing logic. They could be removed in future cleanup.

---

**Last Updated:** 2026-01-25
**Workflow:** Chunk 2.5 - Client Document Tracking (Eugene Document Organizer)
**Workflow ID:** okg8wTqLtPUwjQ18
