# Coaching Session: Richard Igbinoba
**Date:** December 12, 2024
**Duration:** 85 minutes
**Recording:** https://fathom.video/share/zq7zoy5ccocsszVGegtzCyyrNjwZyirs

---

## General Insights

### Project Scoping & MVP Strategy

**The Strategic Exclusion Approach**
- Deliberately leave features OUT of the MVP to create upsell opportunities
- Example: Client manually follows up on missing docs → see system value → request automation
- Rationale: Demonstrate value before proposing more complex build
- Result: Clear path for Phase 2 expansion

**Pricing Strategy: Dual Anchoring**
- Use BOTH time-based AND value-based calculations to establish worth
- Time-based: Hours × hourly rate (concrete, defensible)
- Value-based: Percentage of client's time savings (outcome-focused)
- Example: 40 hrs @ €62.50/hr = €2,500 AND 25% of €6,400 annual savings = €1,600
- Anchor at higher number (€2,500) to establish perceived value

**The "Free for Testimonial" Framework**
- Frame MVP as €2,500 value exchanged for testimonial (not "free")
- Positions consultant as premium service, not desperate for work
- Creates reciprocity: client receives value, feels obligation to deliver great testimonial
- Sets expectation that Phase 2+ will be paid

### Advanced AI Development Tools

**Anti-gravity vs Cursor: Key Difference**
- **Cursor limitation:** Can't mix LLMs within same session (context resets when switching)
- **Anti-gravity advantage:** Mix Claude + Gemini + other LLMs in single session with preserved context
- **Why it matters:** Different models excel at different tasks - combining them > single model
- **Richard's use case:** Self-learning agent that logs all N8N errors and use cases
- **Goal:** "One-shot" agent that builds complex workflows from single prompt

**LLM Architecture Decision Framework**
- **Simple tasks:** Single system prompt with clear instructions
- **Complex tasks:** Separate specialized agents per document type/task
- **Decision point:** If accuracy is low with simple approach, add complexity
- **Principle:** Start simple, add complexity only when needed

### Sequential vs Parallel Processing

**When to Process Sequentially (one at a time):**
- Managing resource usage and costs
- Complex analysis that requires deep focus per item
- When order matters or previous results inform next steps

**When to Process in Parallel:**
- Simple, independent tasks
- Time-sensitive operations
- When resources allow

---

## Client-Specific: Eugene's Document Automation

### Refined MVP Scope

**Problem:**
- Eugene spends 5-10 hours per lead manually processing documents
- Often wastes time on prospects who aren't good fit
- Receives unlabeled, jumbled attachments via email

**MVP Solution (Phase 1):**
1. **Trigger:** New email with attachments
2. **Automated Process:**
   - Download all attachments to Google Drive
   - Use LLM to identify 4 mandatory documents (Grundbuch, teaser, calculation, exit strategy)
   - Rename and organize into folders ("Mandatory", "Other")
   - Update Google Sheet with lead status ("4/4 docs", "3/4 docs", etc.)
3. **Human Checkpoint:** Eugene manually follows up on missing docs

**Deliberately Excluded (for Phase 2 upsell):**
- ❌ Automated email requests for missing documents
- ❌ Running Eugene's analysis prompt to qualify leads
- ❌ Full data room processing (only 4 mandatory docs)

### Implementation Plan

**Timeline:**
- 3 weeks development
- 1 week deployment
- Total: 4 weeks

**LLM Approach:**
- Sequential processing (one doc at a time)
- Single system prompt for 4 mandatory docs
- If accuracy low → pivot to separate agents per doc type

**Testing Plan:**
- Validate in OpenAI playground before building
- Test accuracy and processing time
- Refine prompt based on results

### Pricing Breakdown

**Established Value: ~€2,500**

**Calculation Method 1 (Time-based):**
- 40 hours @ €62.50/hr = €2,500

**Calculation Method 2 (Value-based):**
- Eugene's time savings: 7.5 hrs/client × 6 clients × €200/hr = €6,400/year
- Taking 25% of savings = €1,600

**Delivery:**
- Free MVP in exchange for testimonial
- Positioned as €2,500 value (not "free work")

### Strategic Upsell Path

**Phase 1 (MVP):** Document collection + organization + status dashboard
**Phase 2 (Upsell #1):** Automated follow-ups for missing docs + AI analysis prompt
**Phase 3 (Upsell #2):** Full data room processing (all 18 docs, not just 4 mandatory)

---

## Key Takeaways

**MVP Strategy:**
- ✅ Deliberately exclude features to create upsell opportunities
- ✅ Focus on immediate time-savers (download, rename, organize)
- ✅ Leave manual pain points visible so client requests automation

**Pricing:**
- ✅ Calculate value TWO ways: time-based AND value-based
- ✅ Anchor at higher number to establish perceived worth
- ✅ "Free for testimonial" ≠ "I work for free" (frame as exchange of value)

**Technical:**
- ✅ Start with simplest architecture (single prompt)
- ✅ Add complexity only when accuracy demands it
- ✅ Test in playground before building
- ✅ Sequential processing for complex LLM tasks

**Tools Worth Exploring:**
- 🔧 Anti-gravity: Mix LLMs within single session (preserves context)
- 🔧 Self-learning agents: Log errors + use cases → one-shot workflow builder

**Next Actions (from call):**
- [ ] Present refined MVP to Eugene on Dec 15 (Monday)
- [ ] Test LLM doc analysis in OpenAI playground
- [ ] Schedule follow-up with Richard on advanced agent dev
