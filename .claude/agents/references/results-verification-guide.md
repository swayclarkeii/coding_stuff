---
name: Results Verification Guide
description: Guide for verifying workflow execution results and test outputs
---

# Results Verification Guide

Use this whenever you optimize, refactor, or migrate a workflow and need to prove that outputs are unchanged (or changed in known ways).

---

## 1. When to Verify

- You changed filter positions (early vs late).
- You removed modules.
- You moved from one platform to another.
- You applied heavy optimization (e.g. 50% operation reduction).

---

## 2. Basic Verification Steps

### Step 1 – Baseline (Before Changes)

- Run the **original** workflow with a representative input set.
- Export or capture:
  - Total result count.
  - A sample of the results (e.g. first 10).
  - Any important IDs/fields.

### Step 2 – After Changes

- Run the **new** workflow with the same inputs.
- Export/capture:
  - Total result count.
  - Sample results (same fields).

### Step 3 – Compare

- Counts must match (unless you intentionally changed logic).
- Sample data (IDs, key fields) should match.
- If counts differ, investigate before deploying.

---

## 3. Filter Equivalence Check (For Reordering Filters)

**Goal:** Prove mathematically that moving filters didn’t change which items pass.

Example:

- Original:
  - Normalize price → Filter `(A AND B AND C)`
- New:
  - Filter `(A AND B)` → Normalize price → Filter `(C)`

If:
- A = location filter
- B = keyword filter
- C = price filter (after normalization)

And A/B are independent of normalization:

- Original: `A AND B AND C`
- New: `A AND B AND C` (just applied in two steps)

So the final set of items is the same.

Write a one-paragraph note in the brief explaining this.

---

## 4. Documentation Template

Use this structure when documenting verification:

```markdown
## Verification Results – [Workflow Name]

**Original Workflow**
- Date: [YYYY-MM-DD]
- Inputs: [description or link]
- Total results: [N]
- Sample IDs: [id1, id2, id3, …]

**New Workflow**
- Date: [YYYY-MM-DD]
- Inputs: [same set]
- Total results: [N]
- Sample IDs: [id1, id2, id3, …]

**Comparison**
- Count match: [Yes/No – explanation]
- Sample match: [Yes/No – explanation]
- Intentional changes: [if any]

**Conclusion**
- [Safe to deploy / Needs further investigation]

5. When Verification Fails

If results differ and they’re not supposed to:
	1.	Log the difference:
	•	Original: N results.
	•	New: M results.
	2.	Check:
	•	Filter conditions.
	•	Module removal side effects.
	•	Mapping differences (IDs pointing somewhere else).
	3.	Fix the logic.
	4.	Re-run verification.

Do not deploy until you understand and accept the difference.

⸻

6. Where to Store This
	•	Keep this file in a shared docs/ folder.
	•	Reference it from:
	•	idea-architect-agent
	•	solution-builder-agent
	•	test-runner-agent (optional, for test design).