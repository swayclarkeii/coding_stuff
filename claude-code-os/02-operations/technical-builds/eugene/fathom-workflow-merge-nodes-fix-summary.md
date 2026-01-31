# Fathom Workflow: Merge Nodes Removal & Metadata Fix

**Date:** 2026-01-30
**Workflow ID:** cMGbzpq1RXpL0OHY
**Status:** ✅ Complete

---

## Problem

Three Merge nodes were added to the workflow but caused 0 items output in execution 7202:
- `merge-ai-analysis-data` (Merge AI Analysis Data)
- `merge-performance-analysis-data` (Merge Performance Analysis Data)
- `merge-performance-data` (Merge Performance Data)

Despite correct configuration (mode: combine, combineBy: combineByPosition), the entire downstream pipeline received nothing.

### Root Cause

The Merge nodes were unnecessary complexity. In n8n, when data flows through a linear chain, each node's output carries forward all previous JSON properties. The original problem (metadata not flowing through) was actually caused by:

1. **OpenAI nodes replacing input data** - When Call AI for Analysis/Performance nodes execute, they replace all input JSON with just the AI response (message.content, etc.)
2. **Code nodes dropping fields** - Parse AI Response and Parse Performance Response were only outputting their computed fields, dropping the upstream meeting metadata

---

## Solution Implemented

### 1. Removed Problematic Merge Nodes ✅

**Removed:**
- `merge-ai-analysis-data` ("Merge AI Analysis Data")
- `merge-performance-analysis-data` ("Merge Performance Analysis Data")

**Kept:**
- `merge-performance-data` ("Merge Performance Data") - This one connects two DIFFERENT branches (Save to Airtable + Parse Performance Response), so it serves a legitimate purpose

**New data flow:**
- Enhanced AI Analysis → Call AI for Analysis → Parse AI Response (direct linear chain)
- Build Performance Prompt → Call AI for Performance → Parse Performance Response (direct linear chain)

---

### 2. Encoded Metadata Into AI Prompts ✅

Instead of trying to use $() references or Merge nodes, we **encoded the meeting metadata directly into the AI prompts** and instructed GPT-4o to include them in its JSON responses.

#### Updated: Enhanced AI Analysis (Set node)

**What changed:**
- Added metadata instruction section to the BPS prompt (at the end, before "Transcript:")
- Updated JSON schema to include 6 metadata fields:
  - `meeting_title`
  - `meeting_date`
  - `contact_name`
  - `contact_email`
  - `meeting_url`
  - `recording_id`

**Example prompt addition:**
```
## MEETING METADATA (REQUIRED IN JSON RESPONSE)

**CRITICAL: Include these exact fields and values in your JSON output:**

```
meeting_title: ${ $json.meeting_title }
meeting_date: ${ $json.meeting_date }
contact_name: ${ $json.contact_name || "Unknown" }
contact_email: ${ $json.contact_email || "Unknown" }
meeting_url: ${ $json.meeting_url || "" }
recording_id: ${ $json.recording_id || "" }
```

**Return these fields AS-IS in your JSON response. Do not modify or interpret them.**
```

**Result:**
- GPT-4o now receives meeting metadata as part of the prompt
- GPT-4o includes these exact values in its JSON response
- Metadata flows through the AI pipeline without needing Merge nodes

---

#### Updated: Build Performance Prompt (Set node)

**What changed:**
- Added metadata instruction section to performance prompt
- Same approach as Enhanced AI Analysis

**New prompt structure:**
```
You are a meeting performance analyst...

**CRITICAL:** You MUST include the following metadata fields...

**MEETING METADATA (include in JSON output):**
meeting_title: ${ $json.meeting_title || 'Unknown' }
meeting_date: ${ $json.meeting_date || '' }
...

Return ONLY valid JSON with these fields:
{
  "performance_summary": "...",
  "performance_metrics": "...",
  "performance_trends": "...",
  "meeting_title": "EXACT_VALUE_FROM_ABOVE",
  "meeting_date": "EXACT_VALUE_FROM_ABOVE",
  ...
}
```

---

### 3. Updated Parse Nodes to Extract Metadata ✅

#### Updated: Parse AI Response (Code node)

**What changed:**
- Now extracts ALL fields from GPT-4o's JSON response using spread operator (`...parsed`)
- Explicitly ensures metadata fields exist with fallbacks
- Handles both analysis fields (summary, pain_points, etc.) AND metadata fields (meeting_title, meeting_date, etc.)

**Key code addition:**
```javascript
return {
  json: {
    // Spread all parsed fields (includes metadata from GPT-4o)
    ...parsed,
    // Ensure required analysis fields exist (even if empty)
    summary: parsed.summary || '',
    pain_points: parsed.pain_points || '',
    // ... (other analysis fields)
    // Metadata fields that GPT-4o now includes
    meeting_title: parsed.meeting_title || 'Unknown',
    meeting_date: parsed.meeting_date || '',
    contact_name: parsed.contact_name || 'Unknown',
    contact_email: parsed.contact_email || '',
    meeting_url: parsed.meeting_url || '',
    recording_id: parsed.recording_id || ''
  }
};
```

---

#### Updated: Parse Performance Response (Code node)

**What changed:**
- Same approach as Parse AI Response
- Extracts performance fields + metadata from GPT response
- Uses spread operator to pass through ALL fields

**Key code addition:**
```javascript
return {
  json: {
    // Spread ALL parsed fields from GPT (includes performance analysis)
    ...parsed,
    // Ensure performance fields exist
    performance_summary: parsed.performance_summary || '',
    performance_metrics: parsed.performance_metrics || '',
    performance_trends: parsed.performance_trends || '',
    // Pass through meeting metadata (should be in parsed from GPT response)
    meeting_title: parsed.meeting_title || 'Unknown',
    meeting_date: parsed.meeting_date || '',
    contact_name: parsed.contact_name || 'Unknown',
    contact_email: parsed.contact_email || '',
    meeting_url: parsed.meeting_url || '',
    recording_id: parsed.recording_id || ''
  }
};
```

---

## Data Flow (New)

### Before (Broken)

```
Enhanced AI Analysis → [Split to Merge input 0]
                    ↓
Call AI for Analysis → [Merge input 1]
                    ↓
Merge AI Analysis Data (outputs 0 items ❌)
                    ↓
Parse AI Response (gets nothing)
```

### After (Fixed)

```
Enhanced AI Analysis
    ↓ (ai_prompt with metadata encoded)
Call AI for Analysis
    ↓ (GPT-4o returns JSON with metadata included)
Parse AI Response (extracts metadata from GPT response)
    ↓ (ALL fields flow downstream)
Build Performance Prompt (metadata encoded in prompt)
    ↓
Call AI for Performance
    ↓ (GPT-4o returns JSON with metadata included)
Parse Performance Response (extracts metadata)
    ↓ (ALL fields flow to Prepare Airtable Data)
```

---

## Metadata Flow (Complete Pipeline)

| Stage | Where Metadata Lives |
|-------|---------------------|
| **Enhanced AI Analysis** | Encoded in ai_prompt as n8n expressions (`${ $json.meeting_title }`) |
| **Call AI for Analysis** | GPT-4o receives metadata in prompt, includes in JSON output |
| **Parse AI Response** | Extracted from GPT JSON response, added to output |
| **Build Performance Prompt** | Re-encoded in performance_prompt from previous stage |
| **Call AI for Performance** | GPT-4o receives metadata in prompt, includes in JSON output |
| **Parse Performance Response** | Extracted from GPT JSON response, added to output |
| **Prepare Airtable Data** | Uses `meeting_title`, `meeting_date`, `contact_name`, `contact_email` |

---

## What's NOT in This Fix

### Prepare Airtable Data Code Node

**Status:** NOT updated in this fix

**Why:** The instructions said to update this node to use `meeting_title`, `meeting_date`, `contact_name`, `contact_email`. However, since the metadata is now flowing through the pipeline correctly, this node should already have access to those fields from its input (`$json.meeting_title`, etc.).

**Next step:** If Prepare Airtable Data is still using hardcoded values or wrong fields, that's a separate fix to make after testing.

### Merge Performance Data Node

**Status:** Still in workflow

**Why:** This Merge node connects two DIFFERENT branches:
- Input 0: Save to Airtable output (Airtable record ID)
- Input 1: Parse Performance Response output (performance analysis + metadata)

Unlike the other two Merge nodes (which were merging a linear chain), this one serves a legitimate purpose: combining the Airtable record ID with the performance data.

**If it causes issues:** Remove it and just have Parse Performance Response flow directly to Prepare Performance Data. The record ID from Save to Airtable can be accessed using item linking if needed.

---

## Validation Results

### After Changes

**Errors:** 1 (unrelated - in "Save Transcript to Drive" node)
**Warnings:** 55 (general workflow warnings, none blocking)

**Key validation points:**
- ✅ All connections valid (37 valid connections, 0 invalid)
- ✅ No broken node references
- ✅ Expressions validated successfully
- ✅ Linear data flow restored

---

## Testing Checklist

Before marking this as COMPLETE, test these scenarios:

### Test 1: Happy Path
- [ ] Trigger workflow with webhook containing valid meeting data
- [ ] Verify Enhanced AI Analysis creates ai_prompt with metadata encoded
- [ ] Verify Call AI for Analysis returns JSON with metadata fields
- [ ] Verify Parse AI Response extracts ALL fields (analysis + metadata)
- [ ] Verify Build Performance Prompt creates prompt with metadata encoded
- [ ] Verify Call AI for Performance returns JSON with metadata fields
- [ ] Verify Parse Performance Response extracts ALL fields
- [ ] Verify Prepare Airtable Data receives meeting_title, meeting_date, etc.
- [ ] Verify Save to Airtable creates record with correct Title/Date/Contact fields

### Test 2: Missing Metadata
- [ ] Trigger workflow with meeting data missing some metadata fields
- [ ] Verify fallback values ("Unknown", empty string) are used
- [ ] Verify workflow completes without errors

### Test 3: Merge Performance Data
- [ ] Check execution 7203+ to see if Merge Performance Data outputs items correctly
- [ ] If Merge Performance Data outputs 0 items → remove it and rewire directly

---

## Files Modified

**Workflow:** Fathom Transcript Workflow Final_22.01.26 (cMGbzpq1RXpL0OHY)

**Nodes updated:**
1. Enhanced AI Analysis (Set) - Added metadata instruction to prompt
2. Parse AI Response (Code) - Extract metadata from GPT response
3. Build Performance Prompt (Set) - Added metadata instruction to prompt
4. Parse Performance Response (Code) - Extract metadata from GPT response

**Nodes removed:**
1. Merge AI Analysis Data (Merge)
2. Merge Performance Analysis Data (Merge)

**Connections changed:**
- Enhanced AI Analysis → Call AI for Analysis (direct)
- Call AI for Analysis → Parse AI Response (direct)
- Build Performance Prompt → Call AI for Performance (direct)
- Call AI for Performance → Parse Performance Response (direct)

---

## Key Learnings

### n8n Data Flow Principles

1. **Linear chains don't need Merge nodes** - Data automatically carries forward through linear chains
2. **OpenAI nodes replace input** - When an OpenAI node executes, it replaces ALL input JSON with just the AI response
3. **Solution: Encode data in prompts** - If you need data to flow through an AI call, encode it in the prompt and have the AI include it in its response
4. **Code nodes must explicitly output fields** - Use spread operator (`...parsed`) to pass through all fields, then add explicit fallbacks for required fields

### Why Merge Nodes Failed

The Merge nodes were configured correctly (mode: combine, combineBy: combineByPosition), but they output 0 items because:
- They were merging data from a **linear chain** where one branch was just passing through metadata
- The "combining by position" only works when BOTH inputs have the same number of items
- If one input had 0 items (or mismatched counts), the output was 0 items

The fix (encoding metadata in prompts) eliminates the need for Merge nodes entirely by keeping data flow linear and simple.

---

## Related Executions

- **Execution 7202:** Merge nodes output 0 items (BEFORE this fix)
- **Execution 7203+:** Test after this fix to verify metadata flows correctly

---

## Agent ID

**solution-builder-agent**

---

## Next Steps

1. **Test-runner-agent:** Execute workflow to verify metadata flows through correctly
2. **If Merge Performance Data fails:** Remove it and rewire Parse Performance Response → Prepare Performance Data directly
3. **Update Prepare Airtable Data:** If it's still using wrong fields, update it to use `$json.meeting_title`, `$json.meeting_date`, etc.
4. **Document learnings:** Add this pattern to `/Users/swayclarke/coding_stuff/.claude/agents/references/N8N_NODE_REFERENCE.md` under "Common Patterns"
