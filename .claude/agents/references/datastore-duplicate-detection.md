---
name: Datastore Duplicate Detection
description: Patterns for detecting and handling duplicate records in datastores
---

# Make.com Data Store – Duplicate Detection Pattern

## Use this pattern when you want to avoid re-processing the same items across scenario runs (e.g. properties, leads, documents).

---

## 1. When to Use

- Daily/weekly scrapers (properties, listings, posts).
- Webhook-based flows where the same payload might be delivered multiple times.
- Any workflow where “process once, then skip next time” is desired.

---

## 2. Core Idea

Use a Make **Data Store** as a simple memory:

- Key = a unique identifier (e.g. URL, ID).
- Value = metadata (processedAt, maybe a hash).

On each run:

1. **Search** for the key.
2. **If not found**, add it and process the item.
3. **If found**, skip processing (unless in testing mode).

---

## 3. Minimal 3-Module Architecture

Assume `uniqueId` exists on each item.

1. **Data Store Search**
   - Module: `datastore:SearchKeys`
   - Filter: skip when testingMode = true (so tests ignore the store).
   - Output: `exists = true/false`.

2. **Data Store Add**
   - Module: `datastore:AddKey`
   - Filter: `testingMode == false` AND `exists == false`.
   - Write: `key = uniqueId`, value = JSON string with metadata.

3. **Processing Module**
   - Add filter: `testingMode == true` OR `exists == false`.
   - This ensures:
     - In production: only new items are processed.
     - In testing: everything is processed regardless of the store.

---

## 4. Testing Mode Toggle

Add a scenario variable:

```json
{
  "name": "testingMode",
  "type": "boolean",
  "value": false
}

	•	For real runs: testingMode = false.
	•	For tests / dry runs: testingMode = true (bypasses the store).

---

## 5. Cost & Savings

Example:
	•	100 items per run.
	•	Without dedupe:
	•	100 items processed every run.
	•	With dedupe (after first run):
	•	Only new items hit the expensive part.
	•	Re-runs on same data ≈ “search only” → much cheaper.

Rough logic:
	•	First run: a bit more expensive (search + add).
	•	Later runs: much cheaper (search, then skip).

---

## 6. Key Decisions
	•	Key choice:
	•	Usually url or id is enough.
	•	Only go to composite keys/hashes if you have a strong reason.
	•	Store location:
	•	One data store per “entity type” is usually enough (e.g. properties).
	•	Retention policy:
	•	Decide whether keys ever expire or if they live forever.

---

## 7. Verification
	•	Run with testingMode = true:
	•	Should behave like the original (no dedupe), good for debugging.
	•	Run with testingMode = false:
	•	First run: process everything, store fills.
	•	Second run (same data): very few (or zero) items processed.

Document behaviour alongside results verification if this is client-facing.

---
