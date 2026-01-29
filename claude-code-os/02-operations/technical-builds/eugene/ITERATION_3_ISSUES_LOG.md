# Iteration 3 Testing - Issues Log

**Date:** 2026-01-28
**Test Run:** Iteration 3 with Phase 2 prompt improvements

---

## Issue #1: JSON Parsing Failure - Test 9

**Time:** 21:45:31 CET
**Test:** 9/50
**Document:** 00_Dokumente_Zusammen.pdf
**File ID:** 1_8lhHGuOl04PVqyJiEx3f0P38z7nNPo9

### Error Details

**Error Type:** Could not extract JSON from Claude response
**Node:** Execute Chunk 2.5 (okg8wTqLtPUwjQ18)
**Execution ID:** 6591

**Error Message:**
```
Unknown error [line 62]
Could not extract JSON from Claude response. First 200 chars:
Looking at the filename "00_Dokumente_Zusammen.pdf" and analyzing the document content:

The document contains architectural drawings and floor plans showing:
- Building elevations (Nordostansicht, No...
```

### Root Cause Analysis

**Likely Cause:** Phase 2 prompt additions made the prompts too verbose, causing Claude to occasionally respond with explanatory text instead of pure JSON structure.

**Evidence:**
- Tier 1 prompt increased: 4,390 → 5,215 characters (+825 chars)
- Tier 2 prompt increased: 19,233 → 22,445 characters (+3,212 chars)
- Total prompt size now significantly larger
- Model may be confused about whether to explain or just return JSON

### Impact Assessment

**Success Rate So Far:** 8/9 tests successful (89%)
**Expected Impact:** If this is systemic, could affect 10-15% of classifications

**Decision:** Continue test run to determine if this is:
- Isolated incident (document-specific issue)
- Systemic problem (prompt design flaw)

### Potential Fixes (For Future Implementation)

1. **Add JSON enforcement instruction** at the end of prompts:
   ```
   CRITICAL: Return ONLY valid JSON. Do not include explanatory text before or after the JSON structure.
   ```

2. **Simplify Phase 2 additions** - Keep rules but reduce wordiness

3. **Add JSON schema example** to prompts to reinforce expected format

4. **Test with different model temperature** - Lower temperature for more deterministic JSON output

### Follow-Up Actions

- [ ] Monitor remaining 41 tests for additional JSON parsing failures
- [ ] Calculate final failure rate once all 50 tests complete
- [ ] If failure rate >5%, implement fix #1 (JSON enforcement)
- [ ] If failure rate >10%, implement fixes #1 + #2 (simplify prompts)
- [ ] Document which documents fail (pattern analysis)

### Notes

- Test run continuing despite this failure
- Comparative analysis will account for failed tests
- This issue did NOT exist in Iteration 2 (0 JSON failures)
- Regression introduced by Phase 2 prompt verbosity

---

## Test Progress Tracking

| Test # | Document | Status | Notes |
|--------|----------|--------|-------|
| 1 | Schnitt_B-B.pdf | ✅ Success | |
| 2 | 2022-04-07 Erschließungsbeitragsbescheinigung | ✅ Success | |
| 3 | Copy of 20251015_Bauvorbescheid.pdf | ✅ Success | |
| 4 | Grundriss_2.OG.pdf | ✅ Success | |
| 5 | Wohnquartiersentwicklung-in-Berlin.pdf | ✅ Success | |
| 6 | Copy of Exposé_Kaulsdorf.pdf | ✅ Success | |
| 7 | Grundriss_Dachgeschoss.pdf | ✅ Success | |
| 8 | Schnitt_A-A.pdf | ✅ Success | |
| 9 | 00_Dokumente_Zusammen.pdf | ❌ JSON Parse Error | First failure |
| 10 | AN25700_GU_483564_Richtpreisangebot | 🔄 Running | |
| 11-50 | ... | Pending | |

**Current Success Rate:** 8/9 = 89%

---

**Status:** Active monitoring
**Next Update:** After test 20 or next failure (whichever comes first)
