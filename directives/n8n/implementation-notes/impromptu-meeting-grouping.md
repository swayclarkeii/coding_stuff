# Impromptu Meeting Grouping Implementation

## Implementation Complete - Fathom Transcript Workflow

**Date:** 2026-01-28
**Workflow ID:** cMGbzpq1RXpL0OHY
**Status:** ✅ Built and validated
**Node Modified:** "Process Each Meeting" (id: group-related-meetings)

---

## 1. Overview

- **Platform:** n8n
- **Workflow:** Fathom Transcript Workflow Final_22.01.26
- **Status:** Updated existing workflow with grouping logic
- **Files touched:**
  - Modified node: "Process Each Meeting" (group-related-meetings)

---

## 2. Workflow Changes

### Modified Node: "Process Each Meeting"

**Previous behavior:**
- Processed each meeting individually
- No grouping of related meetings
- Simple pass-through logic

**New behavior:**
- Groups related meetings before processing
- Merges transcripts chronologically
- Deduplicates participants
- Sums durations for grouped meetings

---

## 3. Grouping Rules

### Rule 1: Same Contact + Impromptu Keyword

**Criteria:**
- Meeting titles share ≥2 common words (length >3 chars)
- AND candidate meeting contains "impromptu", "continued", or "follow-up"

**Example:**
- "James Smith - Discovery" (2pm)
- "James Smith impromptu" (2:30pm)
- → **Merged into single meeting**

### Rule 2: Time-Based Grouping

**Criteria:**
- Meetings within 2 hours of each other
- AND share ≥1 common word in title

**Example:**
- "Sindbad call" (2pm)
- "Sindbad follow-up" (3pm)
- → **Merged into single meeting**

---

## 4. Merge Logic

When meetings are grouped, the code:

1. **Combines transcripts chronologically:**
   ```
   [First meeting transcript]

   --- Continued (Part 2) ---

   [Second meeting transcript]
   ```

2. **Uses earliest meeting's metadata:**
   - Title: `"[Original Title] (X parts)"`
   - URL: First meeting's URL
   - Recording ID: First meeting's ID
   - Meeting date: Earliest timestamp

3. **Merges participant lists:**
   - Deduplicates by name and email
   - Creates array of unique participants

4. **Sums durations:**
   - Total duration = sum of all grouped meetings

5. **Adds metadata:**
   - `is_grouped: true`
   - `grouped_meeting_count: X`
   - `total_duration: XXX`
   - `participants: [...]`

---

## 5. Implementation Details

### Code Structure

```javascript
// 1. Sort meetings by date (earliest first)
meetings.sort((a, b) => dateA - dateB);

// 2. Track processed meetings to avoid duplicates
const processed = new Set();

// 3. For each meeting, find related meetings
for (let i = 0; i < meetings.length; i++) {
  if (processed.has(i)) continue;

  // Find related meetings using Rules 1 & 2
  const relatedIndices = [i];

  for (let j = i + 1; j < meetings.length; j++) {
    // Check Rule 1: Same contact + impromptu
    // Check Rule 2: Time-based (within 2 hours)
  }

  // 4. Merge if multiple meetings found
  if (relatedIndices.length > 1) {
    // Combine transcripts, participants, durations
  }
}
```

### Data Flow

**Before grouping:**
```
[
  {meeting: "James Smith - Discovery", time: 2pm},
  {meeting: "James Smith impromptu", time: 2:30pm},
  {meeting: "Other Meeting", time: 3pm}
]
```

**After grouping:**
```
[
  {
    meeting: "James Smith - Discovery (2 parts)",
    time: 2pm,
    combined_transcript: "[Discovery]\n\n--- Continued (Part 2) ---\n\n[Impromptu]",
    is_grouped: true,
    grouped_meeting_count: 2
  },
  {meeting: "Other Meeting", time: 3pm, is_grouped: false}
]
```

---

## 6. Testing Plan

### Happy-Path Tests

**Test 1: Same Contact + Impromptu**
- Input:
  - Meeting 1: "John Doe - Strategy Session" (2pm)
  - Meeting 2: "John Doe impromptu follow-up" (2:30pm)
- Expected:
  - Single grouped meeting: "John Doe - Strategy Session (2 parts)"
  - Combined transcript with "--- Continued (Part 2) ---" separator
  - `grouped_meeting_count: 2`

**Test 2: Time-Based Grouping**
- Input:
  - Meeting 1: "Sarah call" (1pm)
  - Meeting 2: "Sarah continued" (2pm)
- Expected:
  - Single grouped meeting (within 2-hour window)
  - Merged participants and summed duration

**Test 3: No Grouping Needed**
- Input:
  - Meeting 1: "Team Standup" (9am)
  - Meeting 2: "Client Review" (3pm)
- Expected:
  - Two separate meetings (no common words + >2 hours apart)
  - Each with `is_grouped: false`

### How to Run Tests

1. **Manual trigger in n8n:**
   - Go to workflow: `cMGbzpq1RXpL0OHY`
   - Click "Execute Workflow" button
   - Check that meetings are grouped correctly in the output

2. **Check execution logs:**
   - Verify `grouped_meeting_count` field
   - Verify `is_grouped` flag
   - Verify combined_transcript format

3. **Expected outcome:**
   - Meetings with impromptu keywords should be grouped
   - Total meeting count should be reduced
   - Transcripts should have "--- Continued ---" separators

---

## 7. Configuration Notes

### No Credentials Required
- This change only modifies logic, no new integrations

### Key Fields in Output

| Field | Type | Description |
|-------|------|-------------|
| `is_grouped` | boolean | True if this meeting was merged with others |
| `grouped_meeting_count` | number | How many meetings were combined |
| `total_duration` | number | Sum of all grouped meeting durations |
| `participants` | array | Deduplicated list of all participants |
| `combined_transcript` | string | Merged transcripts with separators |

---

## 8. Handoff

### How to Modify Grouping Rules

**To adjust time window (currently 2 hours):**
```javascript
// Line ~90 in "Process Each Meeting" code
if (timeDiffHours <= 2 && commonWords.length >= 1) {
  // Change 2 to desired hours
}
```

**To adjust keyword matching:**
```javascript
// Line ~75 in "Process Each Meeting" code
const hasImpromptu = candidateTitle.includes('impromptu')
  || candidateTitle.includes('continued')
  || candidateTitle.includes('follow-up');
// Add more keywords as needed
```

**To adjust word matching threshold:**
```javascript
// Line ~80 in "Process Each Meeting" code
if (commonWords.length >= 2 && hasImpromptu) {
  // Change >= 2 to require more/fewer common words
}
```

---

## 9. Known Limitations

1. **Only groups forward in time** - Earlier meetings can absorb later ones, but not vice versa
2. **Simple keyword matching** - May miss variations like "follow up" vs "followup"
3. **No fuzzy name matching** - "James Smith" and "J Smith" won't match
4. **Fixed 2-hour window** - No adaptive window based on meeting type

---

## 10. Suggested Next Steps

✅ **Ready for test-runner-agent** to validate with sample data

**Optional enhancements:**
1. Add fuzzy name matching (Levenshtein distance)
2. Make time window configurable via workflow parameter
3. Add ML-based grouping for better accuracy
4. Support bidirectional grouping (earlier + later meetings)

---

## 11. Validation Results

**Workflow validation:**
- Structure: ✅ Valid
- Connections: ✅ Valid (33 connections)
- Node count: 37 nodes
- Autofix: No fixes needed (high confidence)

**Warnings:**
- Some code nodes lack error handling (pre-existing)
- Some nodes use deprecated `continueOnFail` (pre-existing)
- These do not affect grouping logic

---

## Final Notes

The grouping logic has been implemented successfully and is ready for testing. The workflow will now automatically detect and merge related meetings, reducing duplicate processing and creating more comprehensive meeting records.

To test, trigger the workflow manually and check that meetings with matching names and impromptu keywords are properly grouped with combined transcripts.
