# BPS Framework Evaluation for Chunk 2.5 Classification

**Date:** 2026-01-28
**Question:** Would BPS prompting framework improve document classification accuracy vs current approach?

---

## Current Approach Analysis

### Structure

**Tier 1 Prompt (Build AI Classification Prompt):**
- Direct classification instruction
- Keyword lists by category (OBJEKTUNTERLAGEN, WIRTSCHAFTLICHE, RECHTLICHE, SONSTIGES)
- DO NOT CONFUSE WITH sections
- Consistency rules (filename priority)
- JSON output format specification

**Tier 2 Prompts (Parse Classification Result):**
- 38 category-specific prompts
- Each has: keywords, examples, boundary rules ("DO NOT CONFUSE WITH")
- Phase 2 additions: detailed distinguishing rules
- JSON output format specification

### Strengths
✅ **Highly functional** - Gets straight to the task
✅ **Keyword-driven** - Matches the technical domain (German real estate docs)
✅ **Rule-based** - Clear boundaries between categories
✅ **Compact** - Relatively token-efficient (until Phase 2)
✅ **JSON-focused** - Output format is primary concern

### Weaknesses
❌ **No role establishment** - Doesn't define "who" is doing the classification
❌ **No context explanation** - Doesn't explain WHY accuracy matters
❌ **Scattered rules** - DO NOT CONFUSE sections are ad-hoc
❌ **Inconsistent structure** - Each category has slightly different format
❌ **Limited examples** - Some examples exist but not in standardized input→output format
❌ **No guardrails section** - Constraints are scattered throughout

---

## BPS Framework Analysis

### Structure (6 Sections)

1. **Role** - Establishes identity and expertise
2. **Task** - Step-by-step process
3. **Specifics** - Constraints, scope, deliverables, rules
4. **Context** - Purpose, goals, organizational impact
5. **Examples** - Input→output demonstrations
6. **Notes** - Principles, guardrails, edge cases

### Strengths for Classification Task
✅ **Role clarity** - "You are Eugene Document Classifier, an expert German real estate document analyst"
✅ **Context section** - Explains impact on folder routing, tracker accuracy, downstream workflows
✅ **Structured examples** - Shows exactly what good classification looks like
✅ **Centralized guardrails** - All "NEVER" and "ALWAYS" rules in one place
✅ **Consistency enforcement** - Same structure for all 38 categories
✅ **Training/iteration** - Notes section can document what we've learned

### Weaknesses for Classification Task
❌ **Verbosity** - BPS is MORE verbose than current approach (we just saw JSON parsing issues from verbosity)
❌ **Narrative style** - BPS is human-readable prose, our task needs technical lists
❌ **Two-tier complexity** - BPS assumes single-stage processing, we have Tier 1 + Tier 2
❌ **JSON output mismatch** - BPS examples show narrative outputs, we need strict JSON
❌ **Migration cost** - Would require rewriting ALL prompts from scratch
❌ **German terminology** - BPS is English-first, our domain has lots of German keywords

---

## Direct Comparison

| Aspect | Current Approach | BPS Framework | Winner |
|--------|------------------|---------------|--------|
| **Accuracy (proven)** | 88% (Iteration 2) | Unknown (untested) | Current (proven track record) |
| **Consistency** | 94% duplicate consistency | Potentially better with uniform structure | BPS (theoretical) |
| **Role clarity** | None | Explicit identity | BPS |
| **Task structure** | Implicit | Explicit numbered steps | BPS |
| **Context explanation** | None | Why accuracy matters | BPS |
| **Examples quality** | Ad-hoc | Standardized input→output | BPS |
| **Guardrails** | Scattered | Centralized in Notes | BPS |
| **Token efficiency** | Good (pre-Phase 2) | Poor (verbose by design) | Current |
| **JSON reliability** | Good (0 failures in Iter 2) | Unknown (verbosity risk) | Current |
| **Technical keyword handling** | Excellent (list-based) | Weaker (narrative-based) | Current |
| **Migration effort** | N/A | High (rewrite everything) | Current |
| **Two-tier workflow** | Native support | Awkward (single-stage design) | Current |

---

## Recommendation: Hybrid Approach

**Don't migrate to pure BPS. Instead, borrow BPS principles to enhance current approach.**

### What to Adopt from BPS

1. **Add Role Section (at top of Tier 1)**
   ```markdown
   # Role

   You are Eugene Document Classifier, an expert German real estate document analyst specializing in property development projects.

   Your expertise combines:
   - Deep knowledge of German real estate terminology (Bauträger, Baugenehmigung, DIN276, etc.)
   - Pattern recognition across 38 document categories
   - Filename-based reasoning prioritization

   Your classifications directly determine:
   - Correct folder routing for 5 folder destinations
   - Accurate Google Sheets tracker updates across 33 columns
   - Downstream workflow reliability for Chunks 3, 4, and 5
   ```

2. **Add Context Section (at top of Tier 1)**
   ```markdown
   # Context

   This classification system powers Eugene Document Organizer, automating document management for OCP property development projects.

   Accuracy matters because:
   - Misrouted documents delay project decisions
   - Incorrect tracker data causes manual cleanup work
   - Duplicate inconsistency breaks trust in the system

   You operate in two-tier mode:
   - Tier 1: Broad category (4 options)
   - Tier 2: Specific document type (38 options)
   ```

3. **Standardize Examples (in each Tier 2 category)**
   ```markdown
   # Examples

   ### Example 1: Clear DIN276 Calculation

   **Input:**
   - Filename: "251103_Bautraegerkalkulation_Schlossberg.pdf"
   - Content: DIN276 cost groups (100-800), HK calculation, profit margin

   **Output:**
   ```json
   {
     "documentType": "10_Bautraegerkalkulation_DIN276",
     "confidence": 97,
     "reasoning": "Filename contains 'Bautraegerkalkulation' and content shows DIN276 cost structure..."
   }
   ```

   ### Example 2: Ambiguous Case (Kalkulation with Kaufpreise)

   **Input:**
   - Filename: "Kalkulation_Projekt_X.pdf"
   - Content: Mix of DIN276 costs AND customer sales prices

   **Output:**
   ```json
   {
     "documentType": "10_Bautraegerkalkulation_DIN276",
     "confidence": 85,
     "reasoning": "FILENAME PRIORITY: Contains 'Kalkulation'. Content analysis: Dominant section is DIN276 cost breakdown..."
   }
   ```
   ```

4. **Add Guardrails Section (at end of Tier 1 & Tier 2)**
   ```markdown
   # Guardrails

   **Always:**
   - Return valid JSON only (no explanatory text before/after)
   - Use filename as primary signal (consistency rule)
   - Provide reasoning for your classification

   **Never:**
   - Return plain text explanations instead of JSON
   - Ignore filename when it contains clear keywords
   - Classify as 37_Others without checking all specific categories first

   **Edge Cases:**
   - Mixed content → Classify by DOMINANT content type
   - German + English → Prioritize German keywords
   - Ambiguous filename → Content analysis becomes primary
   ```

### What to Keep from Current Approach

✅ **Keyword lists** - Continue using bulleted lists of German terms
✅ **DO NOT CONFUSE WITH** - Keep this structure (it's working)
✅ **Two-tier workflow** - Don't force single-stage BPS structure
✅ **Technical language** - Keep list-based, technical style
✅ **Compact rules** - Don't make everything narrative prose

---

## Testing Plan: Hybrid BPS Approach

### Phase 1: Single Category Pilot (Safe)

**Target Category:** 10_Bautraegerkalkulation_DIN276 (our problem child)

**Steps:**
1. Create BPS-enhanced version of ONLY this Tier 2 category prompt
2. Add: Role, Context, Structured Examples, Guardrails
3. Keep: Keyword list, DO NOT CONFUSE WITH, technical style
4. Test on 10 documents that contain "Kalkulation"
5. Compare: Accuracy, consistency, JSON reliability

**Success Criteria:**
- No JSON parsing errors (must be ≤ current approach)
- Improved accuracy on DIN276 vs Verkaufspreise distinction
- Duplicate consistency maintained or improved

**Rollback:** Simply revert Tier 2 prompt for category 10 to Iteration 3 version

### Phase 2: Expand to Problem Categories (If Phase 1 succeeds)

**Target Categories:**
- 16_GU_Werkvertraege (contractor quotes)
- 26_Finanzierungsbestaetigung (financing memos)
- 11_Verkaufspreise (sales prices)

**Test on:** 20 documents across these categories

### Phase 3: Full Migration (If Phase 2 succeeds)

**Migrate all 38 categories** to hybrid BPS structure

---

## Specific Implementation Recommendations

### For Tier 1 Prompt

**Add at TOP (before current content):**
```markdown
# Role

You are Eugene Document Classifier, an expert German real estate document analyst.

Your expertise: German property development terminology, 38-category classification system, filename-based reasoning.

---

# Context

This classification powers Eugene Document Organizer for OCP property projects.

Your accuracy directly impacts:
- Folder routing correctness (5 destinations)
- Tracker data quality (33 columns)
- Downstream workflow reliability

---

# Task

Your task: Analyze document filename and content to determine Tier 1 category.

Process:
1. Analyze filename for category keywords
2. If filename unclear, analyze content (first 2-3 pages)
3. Apply FILENAME PRIORITY consistency rule
4. Return JSON with category, confidence, reasoning

---
```

**Keep everything else the same** (keyword lists, DO NOT CONFUSE WITH, etc.)

**Add at BOTTOM:**
```markdown
---

# Guardrails

**Always:**
- Return valid JSON only
- Use filename as primary signal
- Explain your reasoning

**Never:**
- Return plain text instead of JSON
- Ignore clear filename keywords
- Skip content analysis when filename is ambiguous
```

### For Tier 2 Prompts (Each Category)

**Add examples section** (2-3 examples per category showing input→output)

**Add guardrails** specific to that category's confusion points

**Keep keyword lists, DO NOT CONFUSE WITH** exactly as they are

---

## Risk Assessment

### Low Risk ✅
- Adding Role/Context sections at top (doesn't change logic)
- Adding Guardrails at bottom (reinforces existing rules)
- Single-category pilot test (easy rollback)

### Medium Risk ⚠️
- Making prompts more verbose (we already saw JSON parsing issues)
- Changing prompt structure (might confuse model)
- Migrating all 38 categories (time investment)

### High Risk ❌
- Switching to pure BPS narrative style (loses technical precision)
- Removing keyword lists (domain requires them)
- Forcing single-tier structure (architecture requires two tiers)

---

## Immediate Next Steps

**Don't implement yet.** Wait for Iteration 3 results first.

**After Iteration 3 completes:**
1. If JSON parsing errors >5%: **Don't add BPS yet** (prompts already too verbose)
2. If DIN276 regression persists: **Pilot BPS on category 10** (structured examples might help)
3. If everything works well: **Consider hybrid BPS for Iteration 4** (measured improvement)

**Safe pilot approach:**
- Create `/Users/computer/coding_stuff/PROMPT_IMPROVEMENTS_ITERATION_4_BPS_PILOT.md`
- Test on 10 documents only
- Measure impact before full migration

---

## Conclusion

**Should you use BPS framework?**

**Not pure BPS, but hybrid BPS:**
- ✅ Adopt: Role, Context, Structured Examples, Centralized Guardrails
- ❌ Reject: Narrative prose style, single-tier structure, verbose explanations
- ⚠️ Keep: Keyword lists, DO NOT CONFUSE WITH, technical precision, two-tier workflow

**Why hybrid?**
- BPS principles improve clarity and consistency
- But pure BPS doesn't fit technical, keyword-heavy domain
- And we're already struggling with prompt verbosity (JSON parsing errors)

**Best path forward:**
1. Complete Iteration 3 testing (in progress)
2. Analyze results (especially JSON parsing errors)
3. If stable: Pilot hybrid BPS on 1 category
4. If successful: Expand incrementally
5. If unstable: Simplify Phase 2 prompts first, then consider BPS later

**Bottom line:** BPS has valuable principles, but don't wholesale replace your working system. Enhance it selectively where it adds value without increasing risk.

---

**Prepared by:** Claude Code
**Date:** 2026-01-28
**Status:** Recommendation - Do not implement until Iteration 3 completes
