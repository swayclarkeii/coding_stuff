# Meeting Notes: Ambush TV - Admin Team Discovery Call

**Date:** January 15, 2026
**Attendees:** Sway Clarke, Leonor Zuzarte, Madalena Ribeiro da Fonseca, Alice Carreto
**Duration:** ~20 minutes
**Meeting Type:** Discovery Call / Admin Team Consultation
**Context:** Follow-up to initial Sindbad discovery call (Jan 8, 2026)

---

## Executive Summary

Focused discovery call with Ambush TV's admin team (Leonor, Madalena, Alice) to understand rate management workflow and pain points. Primary issue identified: manual rate synchronization across three separate Google Sheets (Team Directory → Freelancer Cost Assumptions → Dashboard) creates high error risk and consumes significant time during bulk rate changes. Secondary opportunities: call recording/transcription for rate change conversations, project calendar automation for month-end reminders, and sheet interactivity improvements.

---

## Attendee Information

### Leonor Zuzarte
- **Role:** Rate management and freelancer raises
- **Responsibilities:**
  - Conducts weekly team performance reviews with core team
  - Delivers personalized feedback to freelancers being raised
  - Updates rates across 3 separate sheets (Team Directory, FCA, Dashboard)
  - Primary pain point: Manual rate synchronization error-prone
- **Frequency:** Batch raises (multiple freelancers at once)
- **Emotional State:** Aware of error potential, wants automation to reduce manual admin burden

### Madalena Ribeiro da Fonseca
- **Role:** Systems and automation coordinator
- **Responsibilities:**
  - Built current dashboard formulas (using ChatGPT)
  - Set up Freelancer Cost Assumptions sheet to auto-populate dashboard
  - Attempted project directory automation (couldn't complete)
  - Interested in tool integrations (Fathom, Notion, etc.)
- **Technical Level:** Self-taught automation (Google Sheets scripting, ChatGPT prompts)
- **Emotional State:** Frustrated by tool limitations and integration gaps
- **On Holiday:** Jan 22 - Feb 9 (available Mondays Jan 26 & Feb 2)

### Alice Carreto
- **Role:** Admin team member
- **Responsibilities:** Not detailed in this call
- **Participation:** Minimal speaking, attended as stakeholder

---

## Business Context

### Ambush TV Company Profile
- **Industry:** Advertising pitch presentations for commercial directors
- **Team:** 9 core people + 70-80 freelancers
- **Volume:** ~50 pitches per month
- **Revenue:** 90% of Sindbad's income (pays his bills)
- **Business Partner:** Pierre (handles recruitment, diverging visions with Sindbad)
- **Admin Team:** Leonor (rates/raises), Madalena (systems/automation), Alice

### Rate Management System
- **Sliding Scale:** Freelancers start low, progress toward top rate over time
- **Raise Frequency:**
  - New hires: 2-3 raises in first year
  - Mid-level: 1-2 raises per year
  - Senior level: Slower progression
  - Example: One freelancer received 4 raises in 2024, 2 raises in 2025
- **Process:** Weekly team meetings review performance, batch raises decided, Leonor conducts individual calls

---

## Pain Points Identified

### Pain Point 1: Manual Rate Synchronization Across 3 Sheets

**Current Process:**
1. **Weekly team meeting:** Core team discusses freelancer performance, identifies who to raise
2. **Leonor's calls:** Individual feedback calls with each freelancer being raised (personalized, performance-based)
3. **Team Directory update:** Leonor manually changes rate in Team Directory sheet
4. **Freelancer Cost Assumptions (FCA) update:** Leonor manually changes rate in FCA sheet
5. **Dashboard update:** Rate should auto-populate from FCA, but manual verification needed

**Problem:** Three separate manual updates per raise, multiplied across batch raises

**Time Cost:**
> "Because we do these in bunches, I feel like maybe it's just me, but I do feel like there's a lot of space for human error because I'm having these calls and sometimes I'm like, oh, okay, wait, I'll just like change everyone's admin later, but then later, like something comes up."

**Error Scenarios:**
- Rate changed in Team Directory but not FCA
- Rate changed in FCA but not Team Directory
- Discrepancies between sheets create confusion
- Verification day: "Whole day a month where I go and I spend like two hours making sure that everything is right and corresponds"

**Emotional Impact:** Feels administrative, repetitive, error-prone, distracts from strategic work

**Leonor's Insight:**
> "I just feel like for me personally, it opens me up to a lot of error."

---

### Pain Point 2: No Call Recording for Rate Change Conversations

**Context:** Sway asked if Leonor records feedback calls with freelancers

**Current State:**
- No recording of feedback/raise calls
- No transcription system
- Manual note-taking during calls
- Must remember details for admin updates later
- Information stored only in memory

**Opportunity Identified by Sway:**
- Use Fathom (free) to record and transcribe calls
- Auto-extract rate changes, feedback notes, action items
- Send summary to Leonor post-call via email/Slack/Google Drive
- Reduce "remember to update admin later" mental burden

**Leonor's Response:**
> "I really should, shouldn't I?"

**Constraint:** Ambush uses Discord (not Slack), Google Workspace (not Notion for paid collaboration)

---

### Pain Point 3: Tool Integration Gaps

**Current Tool Ecosystem:**
- **Google Workspace:** Sheets, Docs, Gmail, Calendar (all free)
- **Discord:** Team communication (free, like Slack but for gaming/Twitch)
- **No Notion:** Too expensive for team collaboration
- **No Slack:** Using Discord instead
- **No Salesforce/CRM:** Budget constraints
- **Attempted:** Fireflies, Otter (hit limits, abandoned)

**Madalena's Frustration:**
> "These all have certain integrations with certain services that normal companies would use. But because we are cutting costs at every corner, like, this says it integrates with Slack or Salesforce or Notion... We don't use Slack. We use Discord, which is almost exactly the same, but it's like a, it's like, you know, Discord. It's like a Twitch streaming group... it doesn't, it's not something that would have integrations with other things because it's another, like, it's another free program."

**The Problem:** Standard automation tools assume paid enterprise stack (Slack, Notion, Salesforce), but Ambush uses free alternatives

**Sway's Solution:**
> "You have direct integrations, and then you have API integrations, meaning that an API integration means I can integrate any system with any system."

**Example Given:** Fathom → Email via automation platform (n8n, Make.com) → Can send to Discord, Google Drive, Gmail, etc.

---

### Pain Point 4: Month-End Invoicing Delays

**Current Process:**
- Projects have estimated start/end dates in Dashboard
- End dates sometimes shift (project extends)
- Need to collect all freelancer hours post-project
- Need to send client invoice after hours collected
- Delays cascade: Project ends → wait for hours → wait for invoicing → client payment delayed

**Madalena's Insight:**
> "Sometimes we get to the end of them, like, we haven't started invoicing for January for any projects that were completed, like on the, I mean, now it's not too bad, like the 10th, because we want to make sure December is closed. But obviously, by like the 25th of January, if we're still closing December, and we haven't..."

**Automation Opportunity:**
- Calendar-driven reminders (project end date → trigger)
- 4 days post-project: Reminder to collect hours
- 7 days post-project: Reminder to send client invoice
- Prevent month-end pile-up

**Mental Load:**
> "Even even freeing up mental space, if we had some sort of way of like, the calendar, because at the moment, the dashboard, we input the estimated beginning date and estimated like end date, but sometimes the end shifts."

**Example Problem:**
> "Like, the Unibet of January is going to get left to the bottom of February, and if we were just on top of it earlier, it could be better, it's also really awkward for us to go back, like, a month and a half later and be like, hi, I'm sorry we didn't say anything, it's because your project sucked, please pay us so much, and there's overhours, and there's this."

---

### Pain Point 5: Attempted Automations Failed

**Madalena's Previous Attempts:**
1. **ChatGPT + Google Sheets formulas:** Got basic dashboard working
2. **Project Directory auto-copy:** Tried to copy sanitized projects to another sheet automatically
   - Spent 2 hours on this
   - Could not get it working
   - Gave up
3. **Free call recording tools:** Fireflies, Otter, etc. all hit limits
   - Transcripts sit in tabs no one opens
   - Data not flowing into daily tools (Sheets, Discord)

**The Core Issue:** Automation tools work, but outputs don't integrate with daily workflow

**Madalena's Observation:**
> "You get the transcripts and you get the summaries with the action items and stuff, but then that just sits in that tab of that AI thing that none of us are opening because we have like 60 sheets open instead."

---

## Decisions Made

### D1: Explore Fathom for Call Recording
**Date:** January 15, 2026
**Decision:** Team will evaluate Fathom (free) for recording rate change calls and team meetings
**Rationale:** Fathom is free, integrates via API/automation platforms, can send outputs to Gmail/Discord
**Owner:** Leonor and Madalena to test
**Context:** Solves "I need to remember to update admin later" problem

### D2: API-Based Integration Approach
**Date:** January 15, 2026
**Decision:** Use automation platforms (n8n, Make.com) for API-level integrations instead of direct tool integrations
**Rationale:** Discord, free Google Workspace, and other budget tools don't have direct integrations with enterprise automation tools
**Owner:** Sway to design via automation workflows
**Context:** Unlocks integration between free tools (Discord, Gmail, Google Sheets, Fathom)

### D3: Schedule Follow-Up Call
**Date:** January 15, 2026
**Decision:** Book follow-up call for Jan 22, Jan 26, Feb 2, or after Feb 9 (when Madalena returns)
**Rationale:** Need to review proposals, align on priorities, get buy-in before implementation
**Owner:** Sway to send calendar link with options
**Context:** Madalena on holiday Jan 22 - Feb 9 (available Mondays)

---

## Action Items

### Leonor's Action Items

**A1:** Test Fathom for recording feedback calls with freelancers
**Due:** Before next meeting
**Priority:** Medium
**Context:** Free trial, see if transcription quality is good enough

### Madalena's Action Items

**A2:** Share Team Directory, FCA, and Dashboard sheet structures with Sway
**Due:** Before next meeting
**Priority:** High
**Context:** Sway needs to understand schema for rate sync automation

**A3:** Document current rate change workflow (step-by-step)
**Due:** Before next meeting
**Priority:** High
**Context:** Ensure all edge cases are captured for automation

### Alice's Action Items

**A4:** Review pain points and contribute any additional admin workflow issues
**Due:** Before next meeting
**Priority:** Low
**Context:** Alice was quiet in this call, may have insights to share

### Sway's Action Items

**A5:** Send calendar link with Jan 22, 26, Feb 2, and post-Feb 9 options
**Due:** This week
**Priority:** High
**Context:** Madalena's availability constraints

**A6:** Design API-based automation architecture for rate sync
**Due:** Before next meeting
**Priority:** High
**Context:** Google Sheets API → single source of truth → sync across all sheets

**A7:** Create Fathom → Gmail/Discord automation example
**Due:** Before next meeting
**Priority:** Medium
**Context:** Show how call transcripts can flow into daily tools automatically

---

## Key Quotes

### On Rate Management Pain
> "From my end, I think in terms of automatization, there's just one big thing that pops into mind, which is regarding the rates. So currently, whenever I raise someone or their rates change... I have to manually integrate it into the team directory. And then from the team directory, I have to then make sure that it's changed in the freelancer cost assumptions sheet so that it will show up correctly on the dashboard." - Leonor

### On Error Risk
> "I feel like maybe it's just me, but I do feel like there's a lot of space for human error because I'm having these calls and sometimes I'm like, oh, okay, wait, I'll just like change everyone's admin later, but then later, like something comes up. And so maybe it's changed in the team directory, but it's not changed in the FCA, or maybe it's changed in the FCA, but I haven't changed it yet in the team directory." - Leonor

### On Verification Burden
> "It just creates this like whole day a month where I go and I spend like two hours making sure that everything is right and corresponds and like that the people's time sheets also corresponds and that they like really actually understood that they were raised." - Leonor

### On Tool Integration Frustration
> "These all have certain integrations with certain services that normal companies would use. But because we are cutting costs at every corner... We don't use Slack. We use Discord, which is almost exactly the same, but it's like, you know, Discord. It's like a Twitch streaming group... it's not something that would have integrations with other things because it's another free program." - Madalena

### On ChatGPT Automation Attempts
> "This is all in chat GPT and I still had to like, almost anything that's automated was either there. Like just Googling chat GPT-ing and always like trying out several iterations because at one point I was like trying to get the project directory to copy itself to another sheet only if there was a sanitized thing or maybe something else like that and I just couldn't get it to like I spent maybe two hours trying to do that and I just couldn't get it to do." - Madalena

### On Data Not Flowing
> "You get the transcripts and you get the summaries with the action items and stuff, but then that just sits in that tab of that AI thing that none of us are opening because we have like 60 sheets open instead." - Madalena

### On Month-End Delays
> "It's also really awkward for us to go back, like, a month and a half later and be like, hi, I'm sorry we didn't say anything, it's because your project sucked, please pay us so much, and there's overhours, and there's this." - Madalena

### On Automation Philosophy (Sway)
> "You have direct integrations, and then you have API integrations, meaning that an API integration means I can integrate any system with any system."

### On Fathom Setup (Sway)
> "I can send it to Notion via an API or an HTTP... And so the systems that you have systems that are things like automation systems, which are things like companies like Make, brands like Make or N8N, and these are basic automation systems that allow you to do the back-end connection."

### On Brain Dump Example (Sway)
> "I've set up a system that it'll go through this conversation that I have with it, and it will pull out, these are to-do tasks, and if they're to-do tasks, put them in my Notion Tasks to Database, and if these are calendar bookings, like I need to do something on a certain date, then it will pull that out, and it will set it up in my Gmail account, or my Gmail, or not Gmail, my Google Calendar."

### On Strategic Focus (Sway)
> "The question is always, is it important enough to build a system for... I want to take some time and go through our conversation now, and really kind of get a sense of where and what, and then I would love to have another conversation with you three, at least, to sit down and be like, are these the most painful things, right?"

---

## Technical Details

### Current Google Sheets Structure

**Team Directory:**
- Contains all freelancer information
- Rate column (updated manually by Leonor)
- Raise history (dates and amounts)
- Example: Freelancers at €22/hour were raised between 2024-2025
- One freelancer: 1 raise in 2023, 4 raises in 2024, 2 raises in 2025

**Freelancer Cost Assumptions (FCA):**
- Rate per freelancer by month
- Auto-populates Dashboard via VLOOKUP or similar
- Updated manually by Leonor after Team Directory changes
- Madalena built the formulas (ChatGPT-assisted)

**Dashboard:**
- Monthly tabs for each project
- Pulls rates from FCA automatically
- Shows freelancer hours, rates, total costs
- Used by Sindbad for invoice validation

**The Problem:** No single source of truth - rates exist in 3 places, manual sync required

---

### Current Tool Stack

**Communication:**
- Discord (free, team chat)
- Gmail (email)

**Project Management:**
- Google Sheets (Dashboard, FCA, Team Directory)
- Google Calendar (project timelines)

**Call Recording:**
- None currently
- Previously tried: Fireflies, Otter (abandoned due to limits)

**Attempted:**
- Notion (too expensive)
- ChatGPT (formula building, partial success)

**Potential Additions:**
- Fathom (free call recording)
- n8n or Make.com (API automation)

---

## Automation Opportunities Discussed

### Opportunity 1: Rate Sync Automation
**Problem:** Manual updates across 3 sheets
**Solution:** Single source of truth (Team Directory) → API sync to FCA and Dashboard
**Technology:** Google Sheets API + n8n/Make.com
**Impact:** Eliminate 2 hours/month verification time, reduce error risk

### Opportunity 2: Call Recording & Transcription
**Problem:** No record of feedback calls, must remember admin changes
**Solution:** Fathom recording → auto-transcription → extract rate changes → send to Leonor via email/Discord
**Technology:** Fathom + n8n/Make.com + Gmail/Discord API
**Impact:** Eliminate "remember to update later" mental burden, create audit trail

### Opportunity 3: Project Calendar Automation
**Problem:** Month-end delays because manual tracking of project end dates
**Solution:** Calendar-driven automation → 4 days post-project: reminder for hours → 7 days: reminder for invoicing
**Technology:** Google Calendar API + n8n/Make.com + Discord/Email
**Impact:** Prevent cascade delays, reduce awkward late invoicing conversations

### Opportunity 4: Dashboard Validation Rules
**Problem:** Errors in data entry only caught during Sindbad's manual review
**Solution:** Real-time validation in Google Sheets (missing projects, rate discrepancies, hour thresholds)
**Technology:** Google Apps Script (Sheets scripting)
**Impact:** Catch errors earlier, reduce Sindbad's review burden

---

## Follow-Up Topics for Next Call

### Sheet Interactivity Deep Dive
1. Exact schema of Team Directory, FCA, and Dashboard
2. Current formulas and data flows
3. Rate change edge cases (currency changes, retroactive raises)
4. Single source of truth architecture design
5. Migration path (current → automated)

### Tool Integration Requirements
1. Discord API capabilities (webhooks, bots)
2. Gmail integration for call summaries
3. Google Calendar automation for reminders
4. Fathom API for transcript extraction

### Admin Team Workflow Optimization
1. Madalena's previous automation attempts (what worked, what didn't)
2. Alice's input on admin pain points
3. Batch raise workflow (how many per month on average)
4. Freelancer communication preferences

---

## Business Context & Insights

### Rate Management Complexity
- **Sliding scale system:** Incentivizes freelancer growth
- **Batch raises:** 5-10 freelancers at once (estimate)
- **Personalized feedback:** Leonor values individual conversations
- **High frequency:** New hires get 2-3 raises in first year
- **Volume:** 70-80 freelancers total, subset raised regularly

### Budget Constraints Reality
- **Cutting costs at every corner** (Madalena's words)
- **Free tools only:** Google Workspace, Discord, Fathom
- **Paid tools rejected:** Notion, Slack, Salesforce
- **Impact:** Standard automation workflows assume paid enterprise stack
- **Opportunity:** API-based custom integrations unlock free tool power

### Team Dynamics
- **Leonor:** Focused on people management, feedback, relationships
- **Madalena:** Technical problem-solver, frustrated by tool limitations
- **Alice:** Quiet participant, role unclear in this call
- **Sindbad:** Not present (handles finances, partner relationship tension)

### Cultural Considerations
- **European business context:** Portugal-based team
- **Creative industry:** Advertising pitch presentations
- **Freelancer-heavy:** 70-80 freelancers vs 9 core team
- **Word-of-mouth driven:** High demand, sometimes can't meet capacity

---

## Next Steps

1. **Immediate (This Week):**
   - Sway sends calendar link with Jan 22, 26, Feb 2, post-Feb 9 options
   - Leonor tests Fathom for call recording
   - Madalena shares sheet structures with Sway

2. **Before Next Call:**
   - Sway designs rate sync automation architecture
   - Sway creates Fathom → Gmail/Discord example workflow
   - Admin team documents current rate change workflow

3. **Next Call Agenda:**
   - Review rate sync automation proposal
   - Demonstrate API-based integration approach
   - Prioritize quick wins vs long-term builds
   - Align on implementation timeline

---

## Meeting Metadata

**Recording:** Fathom AI transcription (JSON format)
**Transcript Quality:** High (speaker identification accurate)
**Technical Issues:** None
**Meeting End:** ~20 minutes (short, focused call)
**Relationship Quality:** Collaborative, open dialogue, team engaged
**Cultural Notes:** European business context, budget-conscious, creative industry

---

*Meeting notes compiled from Fathom transcript by Sway's AI system*
*File created: 2026-01-18*
