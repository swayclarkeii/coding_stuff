---
name: Advanced Architecture Patterns
description: Advanced n8n workflow architecture patterns and design best practices
---

# Advanced Architecture Patterns for Automation Design

**Purpose:** Deep-dive patterns for complex automation projects  
**Use when:** Building multi-step workflows with state, extraction, or migration requirements  
**Complements:** `idea-architect-agent.md` - use this for advanced or non-trivial scenarios

**Source:** Extracted and generalized from Document Organizer V3.5 implementation (18–24 hour build)

---

## When To Use This Guide

Use these patterns when your automation involves:

- ✅ Multiple workflow chunks (5+ logical sections)
- ✅ State tracking across submissions (remembering what happened before)
- ✅ Document or data extraction with OCR
- ✅ Migrating from an existing workflow to a new version
- ✅ Entity linking (connecting related data over time)
- ✅ Complex error handling with retries
- ✅ Avoiding duplicate processing and duplicate files

If you are building simple automation (1–3 steps, no state, no migration), stay with the main idea architect agent.

---

## Pattern 1: Modular Chunk-Based Architecture

### What It Is

Break a complex workflow into smaller, logical, testable chunks instead of building one huge monolithic flow.

### When To Use

- Workflow has roughly 20+ nodes
- You clearly see different phases  
  (for example: email processing → AI analysis → file operations)
- You want to test each section independently
- Different people work on different sections

### Example Split (V3.5)

```text
Chunk 0: Folder Initialization (one-time setup) - 12 nodes
Chunk 1: Email → Staging (7 nodes)
Chunk 2: Text Extraction + OCR (6 nodes)
Chunk 2.5: Project Tracking (8 nodes)
Chunk 3: AI Classification (14 nodes)
Chunk 4: File Ops + Logging (8 nodes)
Chunk 5: Error Handling (15 nodes)

Key Principle

Build in slices you can understand and debug.
Do not build more than you can test.

Implementation Steps

Step 1: Identify chunk boundaries

Look for natural handoffs:
	•	Email in → raw attachments
	•	Raw attachments → extracted text
	•	Extracted text → AI classification
	•	Classification → storage and tracking

Each chunk should have:
	•	A clear input
	•	A clear output
	•	A simple responsibility

Aim for about 5–15 nodes per chunk.

Step 2: Define chunk interfaces

Write down for each chunk:

Chunk Input:  What data comes in?
Chunk Output: What data goes out?
Dependencies: What must run before this chunk?

This will save you from hidden dependencies later.

Step 3: Build in order
	1.	Build Chunk 1 alone and test it end to end.
	2.	Build Chunk 2, connect it to Chunk 1, and test 1+2 together.
	3.	Continue chunk by chunk.
	4.	Only hook all chunks together once each one works alone.

Platform Notes

n8n
	•	Use a single workflow for the whole system.
	•	During testing, disable or bypass later chunks while you work on early ones.
	•	Use manual execution and start execution from mid points to test chunks.

Make.com
	•	You can start with separate scenarios per chunk.
	•	Connect them later using webhooks or “Run scenario” style patterns.
	•	Or merge into one scenario once everything is stable.

GitHub Actions
	•	Each chunk can be a separate job in a workflow file.
	•	Use needs: to express dependencies.
	•	Run jobs in parallel when they do not depend on each other.

Questions To Ask
	•	What are the natural chunk boundaries in this workflow?
	•	Can I test this chunk without running everything else?
	•	What data flows between chunks?
	•	Do I need a one-time setup chunk (for folders, tables, data stores)?

Red Flags
	•	One chunk depends on 3+ other chunks for basic data
	•	A single chunk has 30+ nodes
	•	You cannot test a chunk without triggering the whole workflow

⸻

Pattern 2: Multi-Phase Data Collection And Caching

What It Is

If you need multiple AI analyses on the same content, extract and prepare that content once, then reuse it.

When To Use
	•	You do several AI calls on the same document or blob of text.
	•	OCR or scraping is expensive.
	•	You need different views on the same data (classification, entities, sentiment).

Good Approach (Optimized)

Document
  → Extract Text ONCE
      ↓
      ├→ AI Call 1: Category classification
      ├→ AI Call 2: Type classification
      └→ AI Call 3: Project or entity extraction

You pay extraction cost once.

Bad Approach (Wasteful)

Document
  → AI Call 1: Extract + classify category
  → AI Call 2: Extract + classify type
  → AI Call 3: Extract + extract project name

You re-do extraction 3 times.

Implementation Steps

Step 1: Spot reuse

Ask:

Will several operations use the same source data?

If yes, you should extract once and cache.

Step 2: Design the extraction stage

Input: raw source (PDF, image, HTML, API response)
Process: extract or parse text once
Output: a reusable field (for example extractedText) accessible to downstream steps.

Step 3: Parallel processing

From the cached text:

Cached Text
  ├→ AI Classification
  ├→ Sentiment Analysis
  └→ Entity Extraction

These can run as separate branches.

Platform Notes

n8n
	•	Use a Set node or a Code node to store extractedText on the item.
	•	All later nodes can reference this field.

Make.com
	•	Use a “Set variable” or “Set” step after extraction.
	•	Reference {{variables.extractedText}} in later modules.
	•	A Router can split into parallel branches.

Questions To Ask
	•	Will multiple AI calls reuse the same content?
	•	Can I pay once to extract, then reuse?
	•	What is my extraction strategy (OCR vs parser vs API)?

⸻

Pattern 3: Extraction / OCR Strategy Framework

What It Is

A step-by-step way to choose how to extract text from files and web data.

When To Use
	•	You process PDFs, image scans, or screenshots.
	•	You mix digital PDFs with scanned PDFs.
	•	You care about language support and cost.

Decision Flow

Step 1: Source format
  PDF      → Is it digital or scanned?
  Image    → Needs OCR
  DOCX/HTML → Native extraction
  API      → Parse JSON or XML

Step 2: Extraction method
  Digital PDF   → Native PDF parser (cheap, fast)
  Scanned PDF   → OCR service
  Image         → OCR service
  HTML          → HTML parser
  API response  → JSON parse

Step 3: Language support
  English only         → Almost any OCR
  European languages   → AWS Textract / Google Vision
  Asian languages      → Google Vision often best
  Many languages       → Azure or similar

Step 4: Truncation for AI
  Does the AI truly need the full document?
  - For AI input: often first 3k–8k characters are enough.
  - For indexing: maybe you want headings plus summaries.

Step 5: Fallback
  If extraction fails:
  - Send to an “Unknowns” folder or queue
  - Log and optionally notify a human

Example (V3.5)
	•	If PDF has selectable text → digital path using native extraction.
	•	Else → scanned path using OCR with German language support.
	•	For AI input, limit to first 3000 characters to save cost and tokens.
	•	If extraction fails, route that file into an “Unknowns” folder and add a log record.

Questions To Ask
	•	What formats am I receiving? (PDF, images, HTML, DOCX)
	•	Do I need OCR or can I use cheaper digital extraction?
	•	What languages must I support?
	•	Do I really need the full text for AI?

⸻

Pattern 4: Idempotent Operations Design

What It Is

Make workflows safe to run multiple times without creating duplicates or breaking things.

When To Use
	•	One-time setup tasks (folder creation, data store initialization).
	•	Workflows that can fail halfway (you want to resume safely).
	•	Workflows triggered by humans who may double-click or resend.

Core Pattern: Check Before Create

Trigger → Check if resource exists
  → Exists: use it, do not create again
  → Does not exist: create it, then continue

Example: Folder Initialization

Manual Trigger
  → Check if parent folder exists
     → If yes: reuse folder ID
     → If no: create parent

  → For each expected subfolder:
       Check if it exists
         → If yes: reuse ID
         → If no: create

You can re-run this script as many times as you want, and you still end up with one folder tree.

Implementation Strategies
	•	Search first, then create.
	•	Use “upsert” logic where possible (update if exists, insert if not).
	•	Use unique keys (names, IDs, or a combination) to identify resources.

Questions To Ask
	•	Can someone accidentally run this workflow twice?
	•	If it fails halfway, what happens when I run it again?
	•	Do I check for existing data before inserting?

⸻

Pattern 5: State Storage Design

What It Is

Choose where to keep long-term state so the system can remember what happened in past runs.

When To Use
	•	You track progress across multiple events or submissions.
	•	You need project status over time (for example 2 of 4 docs received).
	•	Humans need to see or edit this state.

Decision Steps

Q1: Does state need to persist between runs?
  No  → Use workflow variables only
  Yes → Continue

Q2: What type of state?
  Few simple flags or counters → Sheets or variables
  Structured project data      → Notion, Airtable, database
  Heavy data / many rows       → Database or Airtable

Q3: Who needs to see it?
  Only automation       → Any storage
  Humans view or edit   → Google Sheets, Notion, Airtable

Storage Options (Simple View)
	•	Google Sheets
Good for simple tables and formulas. Great for dashboards for non-technical users.
	•	Notion or Airtable
Good for richer project data and relationships.
	•	Database (Postgres/MySQL)
Good for high volume and complex queries.
	•	Workflow variables only
Good for temporary, per-run state.

Example: Project Tracker Sheet

Columns:
	•	Project Name
	•	Expose (checkbox)
	•	Grundbuch (checkbox)
	•	Calculation (checkbox)
	•	Exit Strategy (checkbox)
	•	Total Complete (formula COUNTIF)
	•	Status (for example 3/4 or COMPLETE)
	•	Last Updated

Workflow:
	•	For each processed document, extract project name.
	•	Find or create row for that project.
	•	Mark the matching document column as TRUE.
	•	Recalculate completion.

Questions To Ask
	•	What does this workflow need to remember later?
	•	Who needs to look at that information?
	•	Is a simple table enough, or do I need a proper database?

⸻

Pattern 6: Migration Path Design

What It Is

Plan how to move from an old workflow (V2) to a new one (V3) without breaking production.

When To Use
	•	You replace any long-running system.
	•	You move from Make.com to n8n or the other way around.
	•	You rebuild architecture in a big way.

Three Strategies

Option A: Fresh Start In Parallel (Recommended for important systems)

1. Keep V2 running for production.
2. Build V3 in parallel.
3. Feed the same input to V2 and V3 for a while.
4. Compare their results.
5. When V3 matches or beats V2, switch traffic to V3.
6. Keep V2 as backup for a short time, then archive it.

Pros:
	•	Very low risk.
	•	You can compare outputs.
	•	Easy rollback.

Cons:
You maintain two workflows for a period.

Option B: Direct Cut-Over
You shut down V2, build V3, test it, then turn it on.

Pros:
	•	Fast.
	•	Clean.

Cons:
	•	Higher risk.
	•	Harder rollback if something fails.

Option C: Phased Migration
Move non-critical features first, then gradually move the critical ones.

Example (V3.5)
	•	Keep V2 email processing workflow running.
	•	Build V3.5 side by side, reading from the same label, but writing into separate folders and trackers.
	•	Compare file sets and logs between V2 and V3.5.
	•	When confident, stop V2 and keep only V3.5.

Questions To Ask
	•	Is this system critical?
	•	Can I run old and new side by side?
	•	What is the rollback plan?
	•	How do I know the new flow is correct?

⸻

Pattern 7: Exponential Backoff And Retry Logic

What It Is

A way to retry failing operations with increasing wait times, instead of hammering a failing service.

When To Use
	•	API rate limits.
	•	Temporary network issues.
	•	Cloud services that sometimes return 5xx errors.

Types Of Errors

Retry-able:
	•	429 Too Many Requests
	•	500 or 503 server errors
	•	Timeouts

Not retry-able:
	•	400 Bad Request
	•	401 Unauthorized
	•	403 Forbidden
	•	404 Not Found
	•	Obvious validation errors (for example missing required field)

Example Retry Pattern

Attempt 1 fails → wait 5s → Attempt 2
Attempt 2 fails → wait 15s → Attempt 3
Attempt 3 fails → wait 45s → Attempt 4
Attempt 4 fails → log error, alert, move item to "failed"

Use about 3–4 attempts in most cases.

What To Do When All Retries Fail
	•	Log the error with context (id, time, operation).
	•	Move the record into a “failed” state for manual review.
	•	Optionally send an email or Slack alert.

Questions To Ask
	•	Which operations might fail temporarily?
	•	How many retries are acceptable?
	•	How long can we afford to wait before giving up?

⸻

Pattern 8: Filename Uniqueness Strategy

What It Is

Avoid user confusion and bugs caused by duplicate filenames in systems that allow them.

When To Use
	•	Google Drive or similar (allows same name in same folder).
	•	High-volume file workflows.
	•	Many sources writing into the same path.

The Problem

Google Drive allows:

EXPOSE_Eugene_20251221.pdf (id 123)
EXPOSE_Eugene_20251221.pdf (id 456)

Users see two identical names in the UI and do not know which is which.

Simple Strategy: Timestamp In Filename

Use a pattern like:

{PREFIX}_{CLIENT}_{YYYYMMDD}_{HHMMSS}.{ext}

Example:

EXPOSE_Eugene_20251221_143052.pdf

This is unique per second, human readable, and sortable.

When You Need Stronger Uniqueness
	•	Millisecond timestamps for very high throughput.
	•	UUIDs if human readability does not matter.
	•	Content hash if you want to prevent storing the same file twice.

Questions To Ask
	•	Does this storage system allow duplicate names?
	•	Do users browse by filename?
	•	Do I care about human readable names, or only IDs?

⸻

Pattern 9: Entity Extraction For Linking Data

What It Is

Use AI to extract a stable identifier (for example project name or address) to link separate submissions together.

When To Use
	•	Related documents arrive at different times.
	•	You need to track “project” or “customer” across many emails or uploads.
	•	You want progress over time per entity (for example 3 of 4 docs received).

Stateless vs Stateful

Stateless:
	•	Each email is processed alone.
	•	No link between documents from the same project.

Stateful with entity extraction:
	•	AI pulls out a project or property name from the content.
	•	You link all documents with the same entity into the same row in your tracker.

Steps
	1.	Extract text from the document.
	2.	Call AI to extract project or entity name.
	3.	Search the tracker for a close match.
	4.	If found, update that row; if not, create a new row.
	5.	Mark which document type has arrived and update completion.

You can use fuzzy matching so that small naming differences still match.

Questions To Ask
	•	Will related data arrive over days or weeks?
	•	What is the “entity” that should connect these items?
	•	Can AI reasonably extract that entity from the text?

⸻

Pattern 10: Completion Tracking UX

What It Is

Show users both what is done and what is missing. Do not only say “3 documents processed”.

When To Use
	•	Multi-step processes (onboarding, document collection).
	•	Anywhere you want someone to see clearly what is left.

Good UX Example

Project: Müller Building
Completion: 3/4 priority documents

✓ Exposé
✓ Grundbuch
✓ Calculation
✗ Exit Strategy (MISSING)

This invites action. The user knows exactly what to ask for.

Implementation Steps
	1.	Decide which items are required.
	2.	Track completion in a sheet or database (booleans).
	3.	Compute x/y completion.
	4.	Build notifications that list both checkmarks and missing items.
	5.	Optionally add reminders if a project stays incomplete for too long.

Questions To Ask
	•	What is the complete checklist for this process?
	•	What is required vs optional?
	•	How do I want to communicate progress and missing pieces?

⸻

Pattern 11: Duplicate Detection With Data Stores

What It Is

Use a data store or table to remember which items you have already processed, so you do not handle the same item twice across runs.

When To Use
	•	You scrape or fetch records repeatedly from the same source.
	•	You do daily or hourly runs over a list that mostly does not change.
	•	Duplicate processing is expensive or confusing.

Core Idea

Assign a stable key for each item (for example URL, ID, or hash), then:

For each item:
  Look up key in data store.
    If found:
      It is a duplicate → skip heavy processing.
    If not found:
      Process item → add key to data store.

Typical Architecture

Data Fetch
  → Data Store Search (check if key exists)
      → If exists: mark as old
      → If not exists: mark as new
  → Process only new items
  → For new items: add keys to data store

Picking A Key
	•	URL or external ID
Easiest. Good when each record has a stable URL or id.
	•	Composite key
Combine fields like address + city + client, if there is no single ID.
	•	Hash
Use a hash of important fields if you want to detect identical content.

Simple Example (Property Scraper)
	•	Key: listing URL.
	•	Data store: a table with url and firstSeenAt.
	•	On each run:
	•	Fetch all listings.
	•	For each listing:
	•	Search by URL in data store.
	•	If not found: process as new, store URL.
	•	If found: skip heavy steps (no AI, no notifications).

Benefits
	•	Save credits and CPU by skipping old items.
	•	Make logs cleaner by focusing on new records.
	•	Prevent sending duplicate emails or alerts.

Questions To Ask
	•	Do I have a simple unique key for each item?
	•	Is processing the same item twice a real problem?
	•	Where should I store keys: Google Sheets, data store, or database?

⸻

How This Doc Connects To The Idea Architect Agent

In idea-architect-agent.md, add a short step like:

## Step: Advanced Architecture Check

If your workflow involves any of the following, open advanced-architecture-patterns.md:

- 20+ nodes or 5+ logical sections → Pattern 1
- Multiple AI passes over the same content → Pattern 2
- Heavy document or OCR work → Pattern 3
- One-time setup or risk of double runs → Pattern 4
- State or progress between runs → Pattern 5
- Replacing an existing system → Pattern 6
- External APIs that may fail or rate-limit → Pattern 7
- File naming on systems that allow duplicates → Pattern 8
- Linking related data across time → Pattern 9
- Multi-step checklists with human users → Pattern 10
- Avoiding duplicate processing across runs → Pattern 11

Use the main agent for high-level design, and come to this file when you see any of these complexity signals.

⸻

Real-World Example: Document Organizer V3.5

Patterns used together:
	•	Pattern 1: modular chunks (7 chunks).
	•	Pattern 2: extraction cached for multiple AI calls.
	•	Pattern 3: smart PDF vs OCR strategy.
	•	Pattern 4: idempotent folder creation.
	•	Pattern 5: Google Sheets project tracker.
	•	Pattern 6: parallel migration from V2.
	•	Pattern 7: exponential backoff on Gmail, Drive, and AI APIs.
	•	Pattern 8: timestamped filenames to avoid duplicates in Drive.
	•	Pattern 9: AI-based project name extraction for linking.
	•	Pattern 10: clear 3/4 style completion UX in emails.
	•	Pattern 11: data store pattern (for other scrapers) to avoid reprocessing old items.

Result in that project:
	•	Much simpler architecture than the earlier version.
	•	Safer reruns and easier debugging.
	•	Lower operations and API cost.
	•	Clearer view of project status for the human operator.

⸻


