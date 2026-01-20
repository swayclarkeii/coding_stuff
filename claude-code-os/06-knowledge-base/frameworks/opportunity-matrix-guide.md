# Opportunity Matrix Framework

## What It Is

The Opportunity Matrix is a prioritization framework that evaluates opportunities based on two dimensions:
1. **Effort** - Implementation difficulty (time, complexity, dependencies)
2. **Impact** - Business value (time savings, revenue, strategic importance)

By plotting opportunities on this matrix, we can identify "Quick Wins" - high-impact, low-effort solutions that should be prioritized first.

---

## When to Use It

Use the Opportunity Matrix when:
- **Discovery calls** - Analyzing client pain points and prioritizing solutions
- **Strategic planning** - Deciding which initiatives to pursue first
- **Opportunity analysis** - Evaluating multiple potential projects or features
- **Resource allocation** - Determining where to invest limited time/budget
- **Sprint planning** - Choosing which features deliver most value quickly

---

## The Matrix

```
                    HIGH IMPACT
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        │  QUICK WINS   │MAJOR PROJECTS │
        │  (Priority 1) │  (Priority 2) │
        │   DO FIRST    │  PLAN CAREFULLY│
        │               │               │
 LOW    ├───────────────┼───────────────┤   HIGH
EFFORT  │               │               │  EFFORT
        │  LOW VALUE    │STRATEGIC BETS │
        │  (Priority 4) │  (Priority 3) │
        │  DEPRIORITIZE │   CONSIDER    │
        │               │               │
        └───────────────┼───────────────┘
                        │
                    LOW IMPACT
```

---

## How to Assess Effort

### Low Effort
- **Time:** 1-2 weeks
- **Complexity:** Simple tech, straightforward implementation
- **Dependencies:** Minimal - can be done independently
- **Examples:** API integration, simple automation, data cleanup

### Medium Effort
- **Time:** 1-2 months
- **Complexity:** Moderate - requires some design/architecture
- **Dependencies:** Some integration with existing systems
- **Examples:** Multi-step workflow automation, CRM integration, custom dashboard

### High Effort
- **Time:** 3+ months
- **Complexity:** Complex tech, significant engineering
- **Dependencies:** Many moving parts, requires coordination
- **Examples:** Platform migration, full system rebuild, AI model training

---

## How to Assess Impact

### Low Impact
- **Improvement:** <10% improvement
- **Value:** Nice to have, minor convenience
- **Strategic:** Doesn't unlock growth or new capabilities
- **Examples:** UI polish, small UX tweaks, formatting

### Medium Impact
- **Improvement:** 10-30% improvement
- **Value:** Noticeable benefit, tangible time/cost savings
- **Strategic:** Improves existing processes
- **Examples:** Process optimization, better reporting, reduced manual work

### High Impact
- **Improvement:** 30%+ improvement or revenue unlock
- **Value:** Game-changer, transformational benefit
- **Strategic:** Unlocks scaling, new revenue, or competitive advantage
- **Examples:** Eliminating bottlenecks, automation of 80% of work, revenue-generating features

---

## Quadrant Meanings

### 1. Quick Wins (Low Effort, High Impact) - Priority 1 🎯
**What it means:** Maximum value for minimum investment

**Action:** DO THESE FIRST
- Immediate implementation
- Clear ROI in weeks/months
- Build momentum and credibility
- Often unlock other opportunities

**Example:** Email forwarding automation that eliminates 80% of manual work in 8-12 weeks

---

### 2. Major Projects (High Effort, High Impact) - Priority 2
**What it means:** Strategic investments with significant payoff

**Action:** PLAN CAREFULLY
- Worth the investment but needs careful planning
- Break into phases if possible
- Ensure resources and commitment
- Often build on Quick Wins

**Example:** Full platform rebuild that scales capacity 10x

---

### 3. Strategic Bets (High Effort, Medium Impact) - Priority 3
**What it means:** Long-term plays that might pay off

**Action:** CONSIDER CAREFULLY
- Evaluate if impact justifies effort
- Look for ways to reduce effort or increase impact
- Often better as Phase 2 after Quick Wins prove value
- May be necessary for strategic reasons

**Example:** Client-facing portal that improves experience but requires significant client adoption

---

### 4. Low Value (Any Effort, Low Impact) - Priority 4
**What it means:** Not worth pursuing right now

**Action:** DEPRIORITIZE OR DEFER
- Even if easy, low impact means low priority
- Revisit only after higher priorities done
- Often premature optimization
- May become relevant later

**Example:** Fancy UI animations when core functionality is still manual

---

## Priority Order for Ranking Opportunities

When analyzing multiple opportunities, rank them in this order:

1. **Priority 1:** Low Effort + High Impact (Quick Wins) - DO FIRST
2. **Priority 2:** Medium Effort + High Impact (High Value) - DO NEXT
3. **Priority 3:** Low Effort + Medium Impact (Easy Wins) - CONSIDER
4. **Priority 3:** High Effort + High Impact (Major Projects) - PLAN CAREFULLY
5. **Priority 4:** Medium Effort + Medium Impact - EVALUATE
6. **Priority 5:** High Effort + Medium Impact (Strategic Bets) - DEFER UNLESS STRATEGIC
7. **Priority 6:** Any Effort + Low Impact - DEPRIORITIZE

---

## Usage Example

### Scenario: Discovery call with real estate finance broker

**Pain Point:** Spending 5-10 hours per deal manually opening and labeling unlabeled PDF documents

**Opportunities Identified:**

| Opportunity | Effort | Impact | Quadrant | Priority | Rationale |
|------------|--------|--------|----------|----------|-----------|
| Email forwarding automation | Medium (8-12 weeks) | High (80% time reduction) | High Value | P2 | Eliminates main bottleneck |
| PipeDrive integration | Low (1-2 weeks) | Medium (indirect value) | Easy Win | P3 | Quick add-on to automation |
| Document AI training | Low (2-3 weeks) | High (95%+ accuracy) | Quick Win | P1 | Maximizes automation value |
| Client portal | High (3-4 months) | Medium (better UX) | Strategic Bet | P4 | Not needed for Phase 1 |

**Result:** Start with Document AI training (P1), then Email automation (P2), then PipeDrive (P3). Defer portal (P4) to Phase 2.

---

## Tips for Effective Use

1. **Be honest about effort** - Don't underestimate complexity
2. **Focus on business impact** - Not technical elegance
3. **Consider ROI** - Quick Wins often have 3-6 month payback
4. **Think sequentially** - Quick Wins often unlock Major Projects
5. **Validate assumptions** - Ask "what makes this high impact?"
6. **Be ruthless** - Most things are NOT Quick Wins
7. **Iterate** - Re-evaluate as you learn more

---

## Common Mistakes to Avoid

❌ **Overestimating impact** - "This will change everything!" (But will it really?)
❌ **Underestimating effort** - "Should be quick" (Famous last words)
❌ **Ignoring dependencies** - "Just need to..." (Forgetting the 10 other things)
❌ **Chasing shiny objects** - Cool tech that solves no real problem
❌ **Perfectionism** - Turning Quick Wins into Major Projects
❌ **Analysis paralysis** - Spending more time analyzing than doing

---

## Visual Reference

See [Opportunity_Matrix.png](./Opportunity_Matrix.png) for the visual representation of the framework.

---

## Related Frameworks

This framework pairs well with:
- **Value Proposition Canvas** - Understanding customer jobs/pains/gains
- **SWOT Analysis** - Identifying strengths to leverage for Quick Wins
- **Impact Mapping** - Connecting opportunities to business goals
- **Lean Canvas** - Validating problem/solution fit before building

---

## Version History

- **v1.0** (2025-12-10) - Initial framework documentation
