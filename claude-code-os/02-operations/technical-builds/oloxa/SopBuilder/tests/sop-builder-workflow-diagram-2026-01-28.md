# SOP Builder Workflow - Updated Flow Diagram

## Complete Workflow Flow (After Updates)

```
┌─────────────────────────────────────────────────────────────────┐
│                        WEBHOOK TRIGGER                           │
│                     (POST /sop-builder)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     PARSE FORM DATA ✓                            │
│  Extracts: email, name, goal, department, process_steps,        │
│            end_user ✓, lead_id ✓, has_audio, audio_data         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                      ┌──────────────┐
                      │ Has Audio?   │
                      └──┬────────┬──┘
                    YES  │        │  NO
                         │        │
        ┌────────────────┘        └──────────────────┐
        │                                             │
        ▼                                             ▼
┌───────────────────┐                       ┌─────────────────┐
│ Upload to Drive   │                       │  (Skip Audio)   │
│ Transcribe Audio  │                       │                 │
│ Set Transcription │                       │                 │
└────────┬──────────┘                       └────────┬────────┘
         │                                            │
         └──────────────┬────────────────────────────┘
                        │
                        ▼
               ┌────────────────────┐
               │ MERGE AUDIO/TEXT   │
               │      PATHS         │
               └─────────┬──────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              LLM: VALIDATE COMPLETENESS ✓                        │
│  Updated prompt with:                                            │
│  - End Users field added ✓                                       │
│  - top_3_quick_wins in JSON schema ✓                             │
│  Returns: scores, missing_elements, top_3_quick_wins             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│            EXTRACT VALIDATION RESPONSE ✓                         │
│  Parses JSON to extract:                                         │
│  - validation_feedback                                           │
│  - top_3_quick_wins array ✓                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│            LLM: GENERATE IMPROVED SOP ✓                          │
│  Updated prompt with End Users field ✓                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                EXTRACT IMPROVED SOP                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  GENERATE LEAD ID ✅ NEW                         │
│  If no lead_id: generate UUID-style ID                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 CALCULATE SOP SCORE ✓                            │
│  Passes through: top_3_quick_wins, end_user ✓                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                      ┌──────────────┐
                      │ Score ≥ 75%? │
                      └──┬────────┬──┘
                    YES  │        │  NO
                         │        │
        ┌────────────────┘        └──────────────────┐
        │                                             │
        ▼                                             ▼
┌─────────────────────┐                    ┌──────────────────────┐
│ GENERATE SUCCESS    │                    │ GENERATE IMPROVEMENT │
│    EMAIL ✓          │                    │    EMAIL ✓           │
│                     │                    │                      │
│ Updates:            │                    │ MAJOR REDESIGN:      │
│ - h1: 28px ✓        │                    │ - h1: 28px ✓         │
│ - Add end_user ✓    │                    │ - Add end_user ✓     │
│ - Calendly CTA      │                    │ - 3 Quick Wins ✓     │
│                     │                    │ - Progress badge ✓   │
│                     │                    │ - Resubmit CTA ✓     │
│                     │                    │ - Amber "fix" text ✓ │
└──────────┬──────────┘                    └──────────┬───────────┘
           │                                           │
           └──────────────┬────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                FORMAT FOR AIRTABLE ✓                             │
│  Adds: end_user, lead_id, submission_count:1, score_history ✓   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              CHECK EXISTING LEAD ✅ NEW                          │
│  Airtable search by email                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                      ┌──────────────┐
                      │ Record Found?│
                      └──┬────────┬──┘
                    YES  │        │  NO
                         │        │
        ┌────────────────┘        └──────────────────┐
        │                                             │
        ▼                                             ▼
┌─────────────────────┐                    ┌──────────────────────┐
│ PREPARE UPDATE DATA │                    │ PREPARE NEW LEAD     │
│      ✅ NEW         │                    │      DATA ✅ NEW     │
│                     │                    │                      │
│ - Increment count   │                    │ - submission_count:1 │
│ - Append score      │                    │ - is_returning:false │
│ - Store prev_score  │                    │ - previous_score:null│
│ - is_returning:true │                    │                      │
└──────────┬──────────┘                    └──────────┬───────────┘
           │                                           │
           └──────────────┬────────────────────────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ MERGE AIRTABLE  │
                 │   PATHS ✅ NEW  │
                 └────────┬────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │ is_returning?│
                   └──┬────────┬──┘
                 YES  │        │  NO
                      │        │
     ┌────────────────┘        └──────────────────┐
     │                                             │
     ▼                                             ▼
┌────────────────────┐                    ┌───────────────────┐
│ UPDATE LEAD IN     │                    │ LOG LEAD IN       │
│ AIRTABLE ✅ NEW    │                    │ AIRTABLE          │
│                    │                    │ (existing node)   │
│ Updates existing   │                    │ Creates new       │
│ record with new    │                    │ record            │
│ score & count      │                    │                   │
└─────────┬──────────┘                    └─────────┬─────────┘
          │                                          │
          └─────────────┬────────────────────────────┘
                        │
                        ▼
               ┌────────────────────┐
               │  SEND HTML EMAIL   │
               └─────────┬──────────┘
                         │
                         ▼
               ┌────────────────────┐
               │ RESPOND TO WEBHOOK │
               └────────────────────┘
```

---

## Key New Features

### 1. Lead ID Generation
```
Generate Lead ID (NEW)
├─ If lead_id exists → Use it
└─ If no lead_id → Generate: "lead_" + random + timestamp
```

### 2. Returning User Detection
```
Check Existing Lead → Check If Returning User
├─ YES → Prepare Update Data
│         ├─ submission_count++
│         ├─ score_history += new_score
│         └─ previous_score stored
│
└─ NO → Prepare New Lead Data
         ├─ submission_count = 1
         └─ score_history = first_score
```

### 3. Email Design Updates

**Improvement Email (<75%):**
- Header: 28px (consistent with success)
- 3 Quick Wins section (replaces full improved SOP)
- Progress badge if returning user
- Amber/orange "how to fix" text
- Resubmit CTA with lead_id tracking

**Success Email (≥75%):**
- Header: 28px
- Added "Who will use this" field
- Calendly CTA for qualified leads

---

## Data Flow Summary

```
Form Submission
  ↓
Parse (end_user, lead_id)
  ↓
LLM Validation (generates top_3_quick_wins)
  ↓
Extract quick wins array
  ↓
LLM Improved SOP (considers end_user)
  ↓
Generate lead_id if missing
  ↓
Calculate score (passes through all fields)
  ↓
Route by score → Generate appropriate email
  ↓
Format for Airtable (all new fields)
  ↓
Check if email exists in Airtable
  ↓
Prepare data (update vs create)
  ↓
Merge paths
  ↓
Route to Update or Create
  ↓
Send email & respond
```

---

## Legend

- ✓ = Modified existing node
- ✅ NEW = Added new node
- ┌─┐ = Decision point
- │ = Flow direction
- └─┘ = Connection
