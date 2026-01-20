# Client Discovery Patterns

Reusable patterns and insights from client discovery processes.

---

## Pattern: The Real Problem vs. Stated Problem

**Observed In:** Bold Move TV - Jan 8, 2026

### Context
Client (Sindbad) came with two specific requests:
1. Automate payment reconciliation (Ambushed)
2. Build lead tracking system (Bold Move TV)

### Discovery Approach
Instead of jumping to solutions, asked to include stakeholders (admin team, business partner) in follow-up calls.

### Key Insight
**Sway's Quote:** "Sometimes it's not those two things. Sometimes the real problem is something else... my job is to really find out what that thing is, because at the end of the day, I've got to build something for you that works, that's valuable, that you use."

### Why It Matters
- Initial problem statement may be symptom, not root cause
- People who do the work often have different perspective than decision makers
- Deeper discovery prevents building wrong solution

### Application Pattern
1. Listen to stated problem without immediately proposing solution
2. Ask: "Who else is involved in this process?"
3. Request multi-stakeholder discovery calls
4. Map complete workflow before designing automation
5. Validate that solving stated problem achieves desired outcome

### Success Indicators
- Client agrees to stakeholder inclusion: ✅ "Yeah, Good idea."
- Client acknowledges uncertainty: ✅ "Maybe I need to work out my strategy first"
- Client shows trust: ✅ Shared confidential partnership information

### Related Patterns
- [Stakeholder Inclusion Strategy](#pattern-stakeholder-inclusion-strategy)
- [Discovery Before Design](#pattern-discovery-before-design)

---

## Pattern: Stakeholder Inclusion Strategy

**Observed In:** Bold Move TV - Jan 8, 2026

### Context
Payment reconciliation problem involved:
- Sindbad (who pays invoices)
- Admin team (who enter data)
- Freelancers (who receive payments)
- Business partner (who shares P&L impact)

### Strategic Decision
Recommend including admin team in discovery call, despite initial call being only with decision maker.

### Rationale
**Stated:** "I'd like to talk with your administrators, because I think it's, I would like to understand the full system before saying, this is what we're going to build here... The people who are actually putting the information there, I'd like to understand their problem."

### Benefits Achieved
1. **Complete picture:** Data entry pain points may differ from payment pain points
2. **Buy-in:** Team involved in design = higher adoption
3. **Hidden problems:** Admin team might reveal inefficiencies Sindbad doesn't see
4. **Better solutions:** Solve team problems, not just founder problems

### Client Response Pattern
**Initial:** Sindbad focused on his own 20 hrs/month pain
**After suggestion:** "I would be interested in not only, you know, speeding up my process, but also theirs [admin team]"

**Shift:** From personal efficiency to team efficiency mindset

### Application Guidelines
**When to use:**
- Process involves multiple people
- Decision maker not closest to day-to-day work
- Risk of building solution that doesn't fit actual workflow

**Who to include:**
- People who do the data entry
- People who use the output
- People who handle exceptions
- People impacted by timing/frequency

**How to propose:**
- Frame as "understanding full system"
- Emphasize building something that "works" not just something that's "done"
- Highlight team benefit, not just decision maker benefit

### Anti-Pattern to Avoid
**DON'T:** Build based only on decision maker's description of process
**WHY:** They may not know day-to-day pain points or workarounds
**RISK:** Solution that decision maker loves but team resents/won't use

---

## Pattern: Human-in-the-Loop Automation Design

**Observed In:** Bold Move TV - Jan 8, 2026

### Context
Client concerned about fully automated systems, wants to maintain control and quality oversight.

### Client Signal
**Quote:** "I wouldn't want to do a batch payment before I've checked everything. But if AI could check things and, you know, tell me if there was a discrepancy..."

### Design Philosophy
**Sway's Response:** "It doesn't have to be an all or nothing. It doesn't have to be a Sindbad is in the process, or he's not in the process at all, and it's automated, right? You can always add in like a human checkpoint."

### Architecture Pattern
```
Current State:
Manual review (5 hrs) → Manual payment (1 hr) → Done
Total: 6 hours

Full Automation (Rejected):
Auto-check → Auto-pay → Done
Total: 0 hours (but no control)

Human-in-the-Loop (Accepted):
Auto-check → Human approval (15 min) → Auto-pay → Done
Total: 15-30 minutes (maintains control)
```

### When to Apply
**Use human checkpoints when:**
- High-stakes decisions (payments, contracts, client communication)
- Regulatory or compliance requirements
- Client expresses concern about full automation
- Error cost is high
- Trust needs to be built gradually

**Skip human checkpoints when:**
- Low-stakes, high-volume tasks
- Easily reversible actions
- Client explicitly wants hands-off automation
- Error cost is minimal

### Communication Framework
1. **Acknowledge concern:** "I hear you want to maintain oversight"
2. **Offer spectrum:** "It doesn't have to be all or nothing"
3. **Propose checkpoint:** "What if AI does the work, you approve, then it executes?"
4. **Quantify time:** "Instead of 6 hours, maybe 20 minutes"
5. **Highlight control:** "You stay in control but save 95% of the time"

### Client Acceptance Indicators
- ✅ "Exactly. That's true."
- ✅ "Yeah, completely."
- ✅ Relief in tone when control preserved

### Progressive Automation Path
**Phase 1:** Human reviews everything, AI assists
**Phase 2:** Human reviews only flagged items, AI handles clean cases
**Phase 3:** Human reviews sample, AI handles everything with exception reporting
**Phase 4:** (Maybe never) Full automation with periodic audits

**Key:** Client decides when to move phases, not forced progression

---

## Pattern: Discovery Before Design

**Observed In:** Bold Move TV - Jan 8, 2026

### Anti-Pattern (What NOT to do)
**Client says:** "I need to automate payments"
**Bad response:** "Great, I'll build you a payment automation system"
**Result:** Solution might not fit actual workflow, requirements change mid-build

### Correct Pattern (What to do)
**Client says:** "I need to automate payments"
**Good response:** "Let me understand your full payment process first. Who's involved? What tools do you use? Where do errors occur? Can we map this together?"
**Result:** Build solution that fits real workflow, fewer change requests

### Discovery Depth Indicators

**Surface level (insufficient):**
- What: "I pay 20 invoices per week"
- Tool: "I use Google Sheets and Wise"

**Deep level (sufficient):**
- **Why weekly:** "Cash flow issues if I do it bi-weekly"
- **Who enters data:** "Admin team enters hours and rates"
- **Where errors happen:** "10% have wrong rates or missing projects"
- **What checking involves:** "I verify hours, check project codes, confirm rates"
- **Why manual:** "I don't trust one person to do both entry and payment"
- **Tools integration:** "Sheets has API, Wise has batch payment capability"

### Discovery Call Structure
**Agenda:**
1. **Context** (10 min): Business background, team structure
2. **Current state** (20 min): Walk through actual process, use real examples
3. **Pain points** (15 min): What's frustrating, time-consuming, error-prone?
4. **Constraints** (10 min): Budget, timeline, must-haves vs. nice-to-haves
5. **Stakeholders** (5 min): Who else needs to be involved in next call?

### Questions That Reveal Real Requirements
- "Walk me through your last time doing this task"
- "What happens when something goes wrong?"
- "Why do you do it this way instead of [alternative]?"
- "Who else is affected by this process?"
- "What would perfect look like?"
- "What have you tried before?"

### Red Flags That More Discovery Needed
- ⚠️ Client says "I'm not sure" to workflow questions
- ⚠️ Client describes process but hasn't done it recently
- ⚠️ "Probably" or "usually" instead of concrete details
- ⚠️ Can't estimate volume, frequency, or time spent
- ⚠️ Mentions "they" (other people) without involving them

### Green Lights That Discovery Is Complete
- ✅ Client walks through actual recent example
- ✅ Specific numbers (20 invoices, 5 hours, 10% error rate)
- ✅ Screenshots or live demo of current system
- ✅ Stakeholders identified and willing to participate
- ✅ Edge cases and exceptions documented

---

## Pattern: Two-Problem Prioritization

**Observed In:** Bold Move TV - Jan 8, 2026

### Scenario
Client presented two problems in initial call:
1. **Ambushed payment reconciliation:** 20 hrs/month, profitable business, measurable ROI
2. **Bold Move TV lead generation:** Unknown time, struggling business, unclear ROI

### Decision Framework

#### Problem 1: Ambushed Payment System
- **Time spent:** Quantified (5-6 hrs/week = 20-24 hrs/month)
- **Business status:** Profitable, established
- **ROI clarity:** Clear (20 hrs × hourly rate = €X saved)
- **Budget:** Available (company has revenue)
- **Stakeholders:** Admin team identified, can involve immediately
- **Solution clarity:** Process-based, API integrations feasible
- **Risk:** Low (optimization of working system)

#### Problem 2: Bold Move TV Lead System
- **Time spent:** Unknown (manual, ad-hoc currently)
- **Business status:** Struggling, not profitable yet
- **ROI clarity:** Unclear (leads converted → revenue, but unknown conversion rate)
- **Budget:** Constrained ("a little bit tight")
- **Stakeholders:** Partner and sales person need involvement
- **Solution clarity:** Strategy unclear ("maybe I need to work out my strategy first")
- **Risk:** Medium (might build wrong thing if strategy unclear)

### Prioritization Recommendation
**Phase 1:** Ambushed payment system (high ROI, clear requirements)
**Phase 2:** Bold Move TV lead generation (after strategy clarification)

### Benefits of Sequencing
1. **Quick win:** Ambushed delivers immediate time savings
2. **Build trust:** Successful first delivery builds confidence for second
3. **Fund second project:** Ambushed ROI can fund Bold Move TV work
4. **Strategy time:** Delay allows Bold Move TV strategy to solidify
5. **Learning:** Insights from first project inform second approach

### When to Reverse Priority
**Do Bold Move TV first if:**
- Sales pipeline is completely dry (survival issue)
- Clear strategy already exists (no discovery needed)
- Partner strongly advocates for it (buy-in factor)
- Ambushed admin team unavailable (blocking issue)

### Communication Approach
**Don't say:** "Bold Move TV seems less important"
**Do say:** "Ambushed has clearer ROI and immediate impact. Let's start there and get you 20 hours/month back. Meanwhile, you can clarify Bold Move TV strategy with your partner, and we'll tackle that next."

---

## Pattern: Creative Industry Sales Sensitivity

**Observed In:** Bold Move TV - Jan 8, 2026

### Context
Client operates in creative industries (film/TV, advertising) where relationships and reputation matter deeply.

### Concern Expressed
**Quote:** "I don't want to get on people's nerves, you know, like I think that's always a risk... I don't really like to be bombarded with newsletters and things like that."

### Cultural Insight
Creative professionals value:
- **Authenticity:** Over volume
- **Quality:** Over quantity
- **Relationships:** Over transactions
- **Taste:** Over efficiency

### Anti-Patterns for Creative Industries
**DON'T:**
- Mass automated email campaigns
- Aggressive follow-up sequences
- Generic LinkedIn outreach at scale
- Newsletter content for the sake of frequency
- Cold calling scripts

**WHY NOT:**
- Seen as "spammy" and damages reputation
- Goes against personal values of client
- Creative clients have good BS detectors
- Relationship quality matters more than lead quantity

### Correct Patterns for Creative Industries
**DO:**
- Tactical, personalized reactivation of warm leads
- Thoughtful, infrequent communication
- Case studies and portfolio showcasing
- Referral and word-of-mouth systems
- Network effect automation (make it easy for clients to refer)

### Design Implications
**For lead reactivation:**
- Provide data/insights, don't auto-send
- Flag opportunities, don't auto-contact
- Suggest messages, don't auto-execute
- Track relationships, don't spam contacts

**Client stays in driver's seat, automation supports quality over quantity**

### Application Questions
**Before recommending automation, ask:**
- "How would you feel receiving this message?"
- "Does this feel authentic to your brand?"
- "Would this damage relationships if it went wrong?"
- "Is this how you want to be known in your industry?"

---

## Pattern: The 90/10 Revenue-Effort Inversion

**Observed In:** Bold Move TV - Jan 8, 2026

### Scenario
**Ambushed:** 90% revenue, 10% effort
**Bold Move TV:** 10% revenue, 90% effort

**Quote:** "Before, it was like 90% effort for boldmove, 10% revenue versus, you know, 10% effort for ambush and 90% revenue."

### Business Context
- Ambushed: Established, word-of-mouth, operational execution focus
- Bold Move TV: New, requires sales, strategic growth focus
- Goal: Flip Bold Move TV to be primary revenue driver

### Strategic Automation Priority
**Counterintuitive insight:** Automate the 10%-effort/90%-revenue business (Ambushed) FIRST

**Why:**
1. **Free up time:** 20 hrs/month from Ambushed → invest in Bold Move TV growth
2. **Fund investment:** Ambushed profits → pay for Bold Move TV initiatives
3. **Proven process:** Ambushed has clear, repeatable workflow (easier to automate)
4. **Strategy clarity:** Bold Move TV needs strategy work, not premature automation

### Pattern Recognition
**When you see:**
- Established business subsidizing new business
- Founder time-trapped in operational tasks
- New business needs strategic attention

**Then prioritize:**
1. Automate established business operations
2. Free founder for new business strategy/sales
3. Use efficiency gains to fund growth initiatives

### Anti-Pattern
**Don't:** Automate the struggling business hoping automation fixes the struggle
**Why:** If strategy isn't clear, automation just scales confusion

---

## Pattern: Partnership Tension as Hidden Constraint

**Observed In:** Bold Move TV - Jan 8, 2026

### Signal
**Quote (marked confidential):** "That's just between me and you. The sad thing about Ambush is, my business partner and I, like, really, we were very good at the beginning. And now, it's just, I don't think we have the same vision... I would almost prefer that he did like the bare minimum."

### Business Impact
- 50/50 partnership with diverging visions
- Partner started side venture without full disclosure
- No budget for buyout
- Sindbad started separate company (Bold Move TV) as response
- Tension affects decision-making and priorities

### Design Implications
**For Ambushed solutions:**
- Keep Sindbad as primary decision maker
- Don't require partner buy-in for operational improvements
- Document ROI clearly (financial benefits might align partner)
- Consider solutions that reduce dependencies between partners
- Respect confidentiality of partnership dynamics

**For Bold Move TV solutions:**
- Treat as completely independent from Ambushed
- Separate pricing, separate timeline
- Don't assume Ambushed success transfers to Bold Move TV

### Warning Signs of Partnership Issues
- Client marks information "just between us"
- Describes starting separate business to work alone
- Mentions partner's separate projects
- Hesitates to involve partner in decisions
- Describes preferring "bare minimum" involvement

### How to Navigate
1. **Acknowledge without prying:** Don't dig into drama
2. **Focus on client's goals:** What does Sindbad want to achieve?
3. **Offer flexibility:** Solutions that don't require partner consensus
4. **Maintain neutrality:** Don't take sides or offer relationship advice
5. **Document carefully:** Keep sensitive information confidential

---

**Knowledge Base Entry Created:** 2026-01-12
**Source:** Bold Move TV Discovery Call (Jan 8, 2026)
**Patterns Documented:** 8
**Next Review:** After additional client engagements validate patterns

---

*Patterns extracted for reusable application across future client engagements*
