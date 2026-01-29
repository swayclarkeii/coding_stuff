# Leonor Transcript Test Expectations

**Date:** 2026-01-28
**Transcript:** Leonor @ Ambushed.tv - January 27th, 2026
**Purpose:** Validate BPS prompts extract quantified data (not invent it)

---

## Expected Quantified Data to Extract

### From Transcript Lines

**Rate Management Process:**
- Line 251: "Per person, I would say like five minutes, not even" → 5 min/call for rate raises
- Line 268: "raised to 20 euros per hour on 27th of Jan" → €20/hour rate
- Line 284: "So in our dashboard, they're earning 17 an hour" → €17/hour current rate
- Line 287: "that person's charging is 18.5, but the dashboard says 17" → Rate discrepancy example
- Line 299: "once every three months, the discrepancy... maybe 10 minutes to sort it out" → 10 min to fix, every 3 months

**Onboarding Process:**
- Line 190: "I try to update it weekly with people that reach out because we do get people, like, reaching out weekly" → Weekly frequency
- Line 198: "every month, two months" → Frequency of deep reviews
- Line 204: "A couple of hours to half your day?" → Time estimate for onboarding sheet updates
- Line 331-333: "how many freelancers new you get a month? Five freelancers a month?" → 5 new/month
- Line 353-356: "Like five minutes?... to ten, depending on how specific Pierre's email is" → 5-10 min per freelancer

**Sanitizing Projects:**
- Line 385-386: "We should be doing it like once every three months. Once every three months to do a full sanitizing" → Every 3 months
- Line 413-414: "I would say like up to three hours. Up to three hours for one" → 3 hours per sanitization
- Line 460: "I usually send like six per person" → 6 projects per freelancer
- Line 519: "Yeah, and each of these take three hours" → 3 hrs each

**Weekly Workflow:**
- Line 34: "Tuesday morning, we have a little meeting that we call the HR review" → Tuesday HR meetings
- Line 38: "I input every week what projects the newbies were on" → Weekly tracking
- Line 57-58: "That's every Monday or is that every day? I usually try to do them every Monday" → Monday feedback collection
- Line 119: "It's a weekly discussion usually" → Weekly rate discussions
- Line 127: "I would say it happens bi-weekly to kind of like average it out" → Bi-weekly for actual rate changes
- Line 141-142: "I pile up a whole week's worth of projects on a Monday" → Batch weekly work

---

## Pain Points with Quantification

**Pain Point 1: Manual Rate Updates Across 3 Sheets**
- Time: 5 min per person for calls
- Frequency: Bi-weekly (average)
- Error rate: Discrepancies "once every three months"
- Fix time: 10 minutes per discrepancy
- Sheets involved: Team Directory, FCA, Dashboard

**Pain Point 2: Onboarding Master Sheet**
- Line 163: "I hate it to the point that I tend to avoid it"
- Update frequency: Should be weekly, actually is "every month, two months"
- Time per deep update: "couple of hours to half your day"
- Volume: 5 new freelancers per month
- Time per freelancer: 5-10 minutes

**Pain Point 3: Project Sanitization Coordination**
- Frequency: Should be every 3 months
- Time per project: Up to 3 hours
- Projects per freelancer: 6
- Coordination overhead: Gap time (unquantified)

---

## What AI Should NOT Invent

❌ **Do NOT invent:**
- Specific hourly rates not mentioned (only €17, €18.5, €20 mentioned)
- Total cost calculations (no labor rates for Leonor given)
- Annual values (no annual extrapolation in transcript)
- Error counts (only "once every three months" mentioned)
- Team sizes (70-80 freelancers mentioned but not for calculations)

✅ **Should extract exactly as stated:**
- "5 minutes" per rate raise call
- "10 minutes" to fix discrepancies
- "3 hours" per sanitization
- "every three months" frequency
- "5 freelancers a month" new onboarding
- "bi-weekly" rate changes

---

## Expected JSON Output Structure

### Client Insights (Call AI for Analysis)

```json
{
  "summary": "HR coordinator struggles with manual rate synchronization across 3 Google Sheets (5 min/call bi-weekly) and onboarding sheet maintenance (avoiding due to frustration, causing month+ delays). Sanitization process requires 3 hrs/project every 3 months.",

  "pain_points": "• **Manual rate updates:** 5 min per person for rate raise calls, updates required in 3 separate sheets (Team Directory, FCA, Dashboard). Rate discrepancies occur once every 3 months, requiring 10 min to fix\n• **Onboarding sheet avoidance:** \"Hate it to the point that I tend to avoid it\" causes weekly updates to slip to monthly or bi-monthly. Deep updates take 2-4 hours. Processing 5 new freelancers/month at 5-10 min each\n• **Sanitization coordination:** Up to 3 hours per project sanitization, should happen every 3 months, sends 6 projects per freelancer",

  "quick_wins": "• **Rate sync automation:** Single source of truth (Team Directory) auto-syncs to FCA and Dashboard (eliminates 5 min/call × bi-weekly × multiple freelancers = estimated [time not quantified in call])\n• **Onboarding sheet redesign:** Make it non-frustrating so Leonor doesn't avoid it (saves 1-2 month delays in updates)\n• **Rate discrepancy alerts:** Real-time notifications when rates don't match across sheets (eliminates quarterly 10-min fire drills)",

  "action_items": "• Share current onboarding master sheet structure - Owner: Leonor, Deadline: This week\n• Document exact rate update workflow with screenshots of 3 sheets - Owner: Leonor, Deadline: Within 5 days\n• List all fields in Team Directory, FCA, and Dashboard that need sync - Owner: Leonor/Madalena, Deadline: This week",

  "key_insights": "• Leonor avoids tasks she finds frustrating (onboarding sheet) causing delays - UX/design matters for adoption\n• Rate updates happen in batches bi-weekly, not continuously - automation needs batch support\n• Discrepancies are caught eventually (once per 3 months) - current system has built-in error detection, just slow\n• ADHD mentioned - interruption-heavy workflow is challenging, needs focused time blocks",

  "pricing_strategy": "[Not quantified in call - no labor rate for Leonor provided, cannot calculate time savings value. Need follow-up to get Leonor's hourly rate and annual raise volume]",

  "client_journey_map": "1. Bi-weekly HR review → Decision to raise multiple freelancers → 2. Leonor conducts 5-min feedback calls (batch in one day) → 3. Update Team Directory with new rate (€20/hour example) → **[PAIN: manual entry]** → 4. Update FCA sheet with same rate → **[PAIN: manual entry, risk of forgetting]** → 5. Verify Dashboard auto-populated from FCA → **[PAIN: sometimes requires manual correction]** → 6. Quarterly discovery of rate discrepancy → **[PAIN: 10 min to diagnose and fix]**",

  "requirements": "• Google Sheets API access (OAuth2 for Team Directory, FCA, Dashboard)\n• Rate change detection (webhook or polling)\n• Data sync logic (Team Directory → FCA → Dashboard)\n• Real-time discrepancy alerts\n• Audit trail of rate changes with timestamps\n• Onboarding sheet UX redesign (make it less frustrating to use)\n• Batch operation support (multiple rate changes at once)"
}
```

### Performance Analysis (Call AI for Performance)

```json
{
  "performance_score": 78,

  "improvement_areas": "• Good workflow walkthrough with specific time estimates (5 min/call, 3 hrs/sanitization, 10 min fixes)\n• Could have quantified total monthly time on rate updates (how many freelancers raised bi-weekly?)\n• Could have probed exact onboarding sheet pain points (what makes it frustrating?)\n• Missing budget discussion - no pricing context established",

  "complexity_assessment": "Low — Single-workflow automation (Google Sheets API sync across 3 sheets), well-documented API, straightforward data mapping. Estimated 1-2 week build. Risk: Need to validate sheet structure and formula dependencies that rely on FCA.",

  "roadmap": "Phase 1 (1-2 weeks): Rate synchronization automation (Team Directory → FCA → Dashboard)\nPhase 2 (1 week): Real-time discrepancy alerts\nPhase 3 (1-2 weeks): Onboarding sheet UX redesign (requires user testing with Leonor)",

  "call_quality_notes": "Good call. Leonor provided specific time estimates (5 min, 10 min, 3 hours) and frequencies (bi-weekly, every 3 months, weekly). Clear pain point articulation ('hate it to the point that I avoid it'). However, no budget discussion and no total monthly time quantification. Missing labor rate for Leonor (cannot calculate ROI). Engagement was high, detailed workflow description. Recommended: Follow-up to get Leonor's hourly rate, total monthly freelancer raise volume, and onboarding sheet field structure."
}
```

---

## Validation Flags Expected

**Should NOT flag as invented:**
- 5 minutes (line 251)
- 10 minutes (line 299)
- 3 hours (lines 413, 519)
- €20/hour (line 268)
- €17/hour (line 284)
- Every 3 months (lines 299, 385)
- Bi-weekly (line 127)

**Should flag as low-confidence if extrapolated:**
- Total monthly time on rate updates (would require: # raises × 5 min/call - not provided)
- Annual cost savings (would require: Leonor's rate × time saved - rate not provided)
- Error prevention value (frequency given but impact not quantified)

---

## Success Criteria

✅ **Pass:** AI extracts exact numbers mentioned in transcript
✅ **Pass:** AI marks extrapolations as "[estimated]" or "[not quantified in call]"
✅ **Pass:** Pricing strategy acknowledges missing data ("cannot calculate without labor rate")
✅ **Pass:** Action items request missing quantification data

❌ **Fail:** AI invents numbers not in transcript (e.g., "saves €2,000/year" without rate data)
❌ **Fail:** AI invents quotes not spoken by Leonor or Sway
❌ **Fail:** AI calculates ROI without having Leonor's hourly rate

---

*Test prepared: 2026-01-28*
*Ready for execution with test-runner-agent*
