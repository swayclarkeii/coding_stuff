# Best Practices for Processing Long Transcripts

**Created:** 2026-01-18
**Context:** Lessons learned from processing 5 Ambush TV/Sindbad Iksel discovery transcripts
**Purpose:** Reference guide for future transcript processing

---

## Summary

Long transcripts (40K-50K+ tokens) from tools like Fathom present unique challenges when processing with AI assistants. This document captures best practices developed during the Ambush TV discovery transcript processing.

---

## The Challenge

### What We Encountered
- 5 Fathom transcript files
- JSON format with nested structure (speaker, text, timestamp)
- File sizes: 40K-47K tokens each (single-line JSON)
- Read tool limit: 25K tokens per read
- Total content: ~200K+ tokens across all transcripts

### Initial Problems
1. **Empty files:** Google Drive sync hadn't completed (files showed 0 bytes)
2. **Token overflow:** Single-line JSON exceeded 25K token read limit
3. **Incomplete reads:** Only partial content captured in first attempts
4. **Context loss:** Important details at end of transcripts missed

---

## Solution: JSON to Plain Text Conversion

### The Approach
Convert raw Fathom JSON into readable line-by-line plain text format before processing.

### Python Conversion Script

```python
import json
import os

# List of transcript files to convert
files = [
    "Sindbad Iksel - 2026-01-15 17H-01m.txt",
    "Sindbad - 2026-01-08 11H-01m.txt",
    "Impromptu Google Meet Meeting - 2026-01-15 11H-00m.txt",
    "Impromptu Google Meet Meeting - 2026-01-15 11H-59m.txt",
    "Sindbad Iksel - 2026-01-15 10H-00m.txt"
]

for filename in files:
    try:
        with open(filename, 'r') as f:
            data = json.loads(f.read())
            transcript = data.get('transcript', [])

            # Create plain text version
            plain_name = filename.replace('.txt', '-plain.txt')

            with open(plain_name, 'w') as out:
                for entry in transcript:
                    speaker = entry.get('speaker', {}).get('display_name', 'Unknown')
                    text = entry.get('text', '')
                    timestamp = entry.get('timestamp', '')
                    out.write(f"[{timestamp}] {speaker}: {text}\n")

            print(f"Converted {filename} -> {plain_name}")

    except Exception as e:
        print(f"Error processing {filename}: {e}")
```

### Output Format
```
[00:01:15] Speaker Name: First utterance text here.
[00:01:22] Other Speaker: Response text here.
[00:01:30] Speaker Name: Continuation of conversation.
```

---

## Reading Strategy for Long Transcripts

### Step 1: Convert to Plain Text First
Always convert Fathom JSON to plain text before attempting to read. This:
- Breaks single-line JSON into multiple lines
- Removes unnecessary metadata
- Preserves speaker attribution and timestamps
- Enables chunked reading

### Step 2: Read in Chunks
For transcripts with 600+ entries, read in 400-line chunks:

```
# First chunk
Read file offset=1, limit=400

# Second chunk
Read file offset=401, limit=400

# Continue until end of file
```

### Step 3: Parallel Reading When Possible
When processing multiple transcripts, read chunks from different files in parallel to speed up processing.

### Step 4: Track What You've Read
Maintain a mental or written log of:
- Which transcripts have been fully read
- Which portions remain
- Key topics/insights from each section

---

## Processing Strategy

### Before Starting
1. **Count the files:** Know how many transcripts exist
2. **Check file sizes:** Estimate total content volume
3. **Verify sync status:** Ensure cloud files are fully synced (non-zero bytes)
4. **Convert format:** Run JSON-to-plain-text conversion

### During Processing
1. **Don't skip content:** Read every portion of every transcript
2. **Take section notes:** Capture key points after each chunk
3. **Cross-reference:** Note connections between transcripts
4. **Track timestamps:** Use timestamps to identify important moments

### After Processing
1. **Synthesize across transcripts:** Combine insights from all sources
2. **Identify contradictions:** Note where different transcripts conflict
3. **Extract quotes:** Pull direct quotes for documentation
4. **Create timeline:** Map events/discussions chronologically

---

## Fathom-Specific Considerations

### JSON Structure
```json
{
  "transcript": [
    {
      "speaker": {
        "display_name": "Speaker Name",
        "id": "speaker_id"
      },
      "text": "Utterance text here",
      "timestamp": "00:01:15",
      "start_time": 75.123,
      "end_time": 82.456
    }
  ],
  "meeting_info": { ... },
  "summary": "...",
  "action_items": [...]
}
```

### Useful Metadata to Preserve
- **Speaker display_name:** For attribution
- **Timestamp:** For context and cross-referencing
- **Meeting info:** Date, duration, participants

### Metadata to Ignore (During Conversion)
- Speaker IDs
- Start/end times (keep timestamp instead)
- Audio URLs
- Internal meeting IDs

---

## Common Pitfalls to Avoid

### 1. Reading Only Partial Content
**Problem:** First 400 lines read, rest skipped
**Solution:** Always calculate total lines and read all chunks

### 2. Relying on Agent Summaries Alone
**Problem:** Agent summarizes but misses important details
**Solution:** Read raw transcripts yourself when thoroughness required

### 3. Assuming JSON Can Be Read Directly
**Problem:** 40K+ token JSON exceeds read limits
**Solution:** Always convert to plain text first

### 4. Processing Transcripts in Isolation
**Problem:** Missing connections between calls
**Solution:** Read all transcripts, then synthesize

### 5. Not Verifying File Sync
**Problem:** Empty files (cloud sync incomplete)
**Solution:** Check file sizes before processing

---

## Recommended Folder Structure

```
/project-name/
├── discovery/
│   └── transcripts/
│       ├── raw/
│       │   ├── Meeting Name - YYYY-MM-DD HHH-MMm.txt (original JSON)
│       │   ├── Meeting Name - YYYY-MM-DD HHH-MMm-plain.txt (converted)
│       │   └── convert_transcripts.py (conversion script)
│       └── Meeting Name - Summary.md (processed summary)
```

---

## Token Efficiency Tips

### For Extraction Tasks
- Convert to plain text (removes JSON overhead)
- Use timestamps to skip irrelevant sections
- Filter by speaker when focused on specific person

### For Analysis Tasks
- Read all content but summarize in sections
- Use chunked reading with notes between chunks
- Create summary file as you go

### For Quote Mining
- Convert to plain text
- Search for keywords using Grep
- Pull relevant sections only

---

## Tool Selection Guide

| Task | Best Tool | Notes |
|------|-----------|-------|
| Convert JSON to plain text | Bash (Python script) | Run locally |
| Read transcript chunks | Read tool | Use offset/limit |
| Search for keywords | Grep tool | Faster than reading |
| Full transcript processing | Read + manual notes | No agent shortcut |
| Summary generation | Agent (after reading) | Provide context |

---

## Quality Checklist

Before marking transcript processing complete:

- [ ] All transcript files identified
- [ ] All files converted to plain text
- [ ] All content read (verify total lines)
- [ ] Key quotes extracted
- [ ] Timeline of discussions created
- [ ] Cross-references between transcripts noted
- [ ] Pain points documented
- [ ] Action items extracted
- [ ] Stakeholders identified
- [ ] Technical requirements captured

---

## Example Workflow

### 1. Discovery
```bash
# Find all transcript files
Glob pattern: **/transcripts/raw/*.txt
```

### 2. Conversion
```bash
# Run Python script in transcript directory
python convert_transcripts.py
```

### 3. Reading
```
# For each -plain.txt file:
Read file_path, offset=1, limit=400
# Take notes
Read file_path, offset=401, limit=400
# Continue until done
```

### 4. Documentation
```
# Create summary files
Write /transcripts/2026-01-15-meeting-summary.md
```

### 5. Analysis
```
# Cross-reference and synthesize
Write /analysis/key_insights.md
Write /analysis/quick_wins.md
```

---

## Lessons from Ambush TV Processing

### What Worked Well
1. Python script for JSON conversion (reusable)
2. Parallel reading of multiple transcript chunks
3. Cross-referencing Bold Move TV documentation
4. Chunked reading with note-taking between

### What Could Be Improved
1. Earlier verification of file sync status
2. More systematic chunk tracking
3. Automated line counting before reading
4. Template for extraction (pain points, quotes, action items)

### Key Success Factor
**Explicit instruction to "read all transcripts completely, do not skip any"** was critical. Without this, partial processing would have missed significant content.

---

## Automation Opportunity

For frequent transcript processing, consider building:

1. **Transcript Ingestion Workflow**
   - Watch for new Fathom exports
   - Auto-convert JSON to plain text
   - Notify when ready for processing

2. **Summary Extraction Template**
   - Standard fields to extract
   - Quote mining patterns
   - Pain point identification

3. **Cross-Reference System**
   - Link transcripts to projects
   - Track which have been processed
   - Note connections between calls

---

*Document created: 2026-01-18*
*Based on processing 5 Ambush TV discovery transcripts*
