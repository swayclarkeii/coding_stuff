# Project Requirements - Jennifer Spencer Medium
**Client:** Jennifer Spencer & Steve Fernandez
**Prepared by:** Sway Clarke / Oloxa.ai
**Date:** December 10, 2025
**Source:** Initial Discovery Call (December 2, 2025)

---

## Project Overview

**Objective:** Systematize and automate content creation, marketing workflows, and backend operations to enable Jennifer Spencer Medium to scale from ~$6K-$7.5K/month to higher revenue while reducing operational burden on Jennifer.

**Core Challenge:** Jennifer is the sole content creator and face of the brand. Current workflow requires her to manually rewrite all AI-generated scripts to match her authentic voice, creating a 2-3 hour/week bottleneck.

---

## Requirements by Priority

### Priority 1: Content Creation Workflow (CRITICAL)

#### R1.1: Authentic Voice Script Generation
**Problem:** Current ChatGPT scripts feel inauthentic; Jennifer must manually rewrite everything
**Requirement:** AI-assisted script writing that sounds like Jennifer on first draft

**Acceptance Criteria:**
- Jennifer can record 80%+ of generated script without rewriting
- Scripts maintain authentic, vulnerable, personal storytelling style
- System trained on Jennifer's content (not competitor Quinlan)
- Voice model captures:
  - Personal anecdotes and storytelling approach
  - Informal, conversational tone
  - Vulnerability and relatability
  - "Want to be her friend" energy

**Technical Approach:**
- Collect Jennifer's 20-30 best-performing pieces
- Analyze linguistic patterns, sentence structure, vocabulary
- Create custom GPT or fine-tuned model
- Include examples of:
  - How she opens topics
  - How she shares personal stories
  - Her closing/CTA style
  - Her use of questions/engagement

#### R1.2: Content Calendar & Organization System
**Problem:** No system for organizing what content to create when, what events to promote
**Requirement:** Centralized calendar showing what needs to be created and when

**Acceptance Criteria:**
- Single view of all content needs across all products
- Shows: Product (retreat/workshop/etc), Content type (reel/story/newsletter), Due date, Status
- Jennifer receives weekly/daily briefing: "Today you're recording these 3 scripts"
- Automated reminders for time-sensitive content (e.g., "5 spots left" posts)
- Integrates product launch dates with content production timeline

**System Features:**
- Calendar view (monthly/weekly/daily)
- Content batching recommendations
- Priority flagging
- Dependencies (e.g., can't post "5 spots left" before main retreat announcement)

#### R1.3: Content Ideation from One-on-One Sessions
**Problem:** Each session generates 25 pain points, but system to convert these to content is manual
**Requirement:** Automated pipeline from session → transcription → themes → content bank

**Current Workflow That Works:**
1. Jennifer does one-on-one session
2. Steve transcribes recording
3. ChatGPT identifies 25 pain points
4. Saved to Google Doc
5. Jennifer highlights favorites
6. [BOTTLENECK] Manual script creation

**Improved Workflow:**
1. Session recorded (automated)
2. Auto-transcription
3. AI extracts pain points + recommended content angles
4. Populated into content bank
5. Jennifer approves topics (quick yes/no review)
6. Auto-generates scripts in Jennifer's voice
7. Jennifer records in batch
8. Auto-scheduled to content calendar

#### R1.4: Dual Content Type Management
**Problem:** Two distinct content types with different purposes
**Requirement:** System distinguishes and manages both content tracks

**Two Content Types:**
1. **Brand/Authority Content** - General spiritual guidance, doesn't sell
   - Goal: Followers, engagement, trust
   - Frequency: Ideally daily
   - Examples: Spirit guide messages, personal revelations, teaching moments

2. **Product Marketing Content** - Sells specific offering
   - Goal: Conversions, sales
   - Frequency: Campaign-based (leading up to event/launch)
   - Examples: Retreat promotions, workshop deadlines, one-on-one availability

**System Requirements:**
- Tag content by type (brand vs. product)
- Track which product each marketing piece promotes
- Balance: Maintain ratio (e.g., 4:1 brand to marketing)
- Campaign view: All content for a specific product launch

---

### Priority 2: Meditation Content as Podcast (QUICK WIN)

#### R2.1: Podcast Distribution Setup
**Problem:** Hundreds of edited meditation MP3s sitting behind membership paywall, generating minimal revenue (~$1,250-$2K/month from 50 members)
**Requirement:** Release as free podcast on major platforms

**Technical Requirements:**
- Upload to podcast hosting platform (e.g., Libsyn, Anchor, Transistor)
- Distribute to:
  - Spotify
  - Apple Podcasts
  - Google Podcasts
  - YouTube (audio-only versions)
- RSS feed setup
- Show notes template
- Artwork/branding

**Content Strategy:**
- Delay strategy: Release content 6 months after live session (keeps exclusivity for members)
- OR: Curated selection (not all episodes)
- Episode frequency: 2-3x/week to match current live schedule
- Each episode: 30 minutes (visualization, soundbath, talk)

#### R2.2: Freemium Value Stack Design
**Problem:** Current members pay for access to recordings; may feel value decreases if podcast goes free
**Requirement:** Enhanced member benefits to justify continued membership

**Free Podcast Listeners Get:**
- Delayed or selected meditation recordings
- Standard content

**Paying Members Continue to Get:**
- Live participation (8:30am EST Mon/Tue/Wed)
- Accountability/wake-up call aspect
- Real-time community
- Facebook group access
- First access to new sessions (6 month early access)
- Member-only Q&As or extended sessions
- Downloadable resources/guides

**Similar Models:**
- Sam Harris: Free podcast + paid Wake Up app
- Tim Ferriss: Free podcast + paid inner circle

---

### Priority 3: Backend Automation

#### R3.1: Workshop/Event Reminder System
**Problem:** Manual reminder emails for upcoming workshops
**Requirement:** Automated email sequences based on event date

**Email Sequences Needed:**

**For Group Workshops:**
- Confirmation (immediately after purchase)
- 1 week before: "Preparing for your workshop"
- 24 hours before: Zoom link + preparation instructions
- Day of: Reminder email (morning of)
- Post-event: Thank you + testimonial request + offer

**For Retreats:**
- Confirmation (immediately after purchase)
- 4 weeks before: Packing list, travel info
- 2 weeks before: Detailed itinerary
- 1 week before: Final prep, weather, contact info
- Day before: Travel reminders
- During retreat: Welcome email
- Post-retreat: Thank you, testimonial request, next retreat announcement

**For One-on-Ones:**
- Confirmation + intake form
- 24 hours before: Prep instructions
- Immediately after: Recording delivery
- 1 week after: Follow-up offer (next session discount)

#### R3.2: Member Onboarding Automation
**Problem:** Manual onboarding for meditation membership
**Requirement:** Automated welcome sequence for new members

**Sequence:**
- Welcome email (immediately)
- Facebook group invitation
- How to access recordings library
- Schedule of live sessions (with calendar invites)
- Day 3: Check-in email
- Day 7: First week experience survey
- Day 14: End of trial reminder (if applicable)
- Monthly: Community engagement prompts

#### R3.3: Content Posting Automation
**Requirement:** Once content is created and approved, auto-post according to schedule

**Platform Requirements:**
- Instagram: Reels, posts, stories
- Newsletter: Email to subscriber list
- Future: TikTok, YouTube

**Features:**
- Schedule posts in advance
- Optimal timing recommendations
- Cross-posting capability
- Preview before publishing
- Performance tracking

---

### Priority 4: Multi-Channel Content Expansion (Future)

#### R4.1: TikTok Presence
**Current State:** Wants to be consistent but lacks capacity
**Requirement:** Repurpose Instagram content for TikTok with minimal additional effort

**Strategy:**
- Same content, different platform
- Auto-reformat for TikTok specs
- Scheduled posting
- Different captions/hashtags optimized for TikTok

#### R4.2: YouTube Channel
**Current State:** Wants channel but lacks capacity
**Requirement:** Long-form content strategy leveraging existing assets

**Potential Content:**
- Podcast episodes (video + audio)
- Extended teaching content
- Retreat recaps/vlogs
- One-on-one session examples (with permission)
- Behind-the-scenes

#### R4.3: Newsletter Consistency
**Current State:** Inconsistent, sometimes repurposes IG content
**Requirement:** Regular newsletter cadence with unique value

**Options:**
A) Weekly digest: Best IG content + exclusive thoughts
B) Bi-weekly deep dive: Long-form content not on IG
C) Monthly community update: Events, offerings, personal updates

---

## Product-Specific Requirements

### One-on-One Sessions (Currently Working Well)

**Existing System:**
- Calendly booking
- Manual email of recording after session

**Enhancement Requirements:**
- Automated recording delivery
- Session notes/summary auto-generated
- Follow-up sequence
- Intake form integration
- CRM integration to track client history

**Current Volume:** 15-17/month @ $250 = $3,750-$4,250/month
**Goal:** Maintain current volume, improve backend efficiency

### Group Workshops (Need Optimization)

**Current Performance:**
- 30-40 people @ $88
- ~1 every 2 months
- Goal: 2-3/month

**Marketing Requirements:**
- Workshop announcement sequence (2 weeks before)
- Countdown posts (7 days, 3 days, 24 hours)
- Spots remaining updates
- Testimonials from past workshops
- Social proof elements

**CRM Requirements:**
- Track workshop attendance
- Identify repeat attendees
- Upsell path to retreats
- Post-workshop survey

**Topics Needed:**
Track which workshop topics convert best

### Retreats (Best ROI - Primary Focus)

**Current Performance:**
- Example: Sedona Jan 29-Feb 1
- 20 spots sold out
- $28K gross, $20K net
- Minimal marketing spend

**Marketing Requirements:**
- Early bird announcement (8-12 weeks before)
- Full campaign timeline:
  - Week 1-2: Announcement + early bird
  - Week 3-6: Value selling (what makes this special)
  - Week 7-8: Countdown + scarcity
  - Week 9-10: Last chance
  - Week 11+: Sold out + waitlist

**Content Needed per Retreat:**
- Announcement reel (location feature)
- Itinerary breakdown posts
- Past retreat testimonials
- Behind-the-scenes preview
- Jennifer's personal story with location
- Countdown posts
- Sold out celebration
- Waitlist management

**System Requirements:**
- Retreat landing page
- Payment plans option
- Travel information hub
- Post-retreat testimonial collection
- Photo/video sharing platform

### Meditation Membership (Needs Repositioning)

**Current State:**
- 50 members @ $25-40/month
- 3x/week live sessions (Mon/Tue/Wed 8:30am EST)
- Facebook group community
- Hundreds of recordings library

**New Strategy (Post-Podcast Launch):**
- Free podcast = top of funnel
- Membership = premium experience
- Repositioned as: Live community, not just recordings

**System Requirements:**
- Podcast hosting + distribution
- Enhanced member portal
- Community features beyond Facebook
- Member-only perks/bonuses
- Graduation path: Membership → One-on-one → Retreat

---

## Technical Infrastructure Requirements

### CRM System
**Purpose:** Centralized client relationship management

**Features Needed:**
- Contact database
- Purchase history tracking
- Interaction history (sessions, workshops, retreats)
- Segmentation (one-on-one clients, retreat alumni, members, etc.)
- Email integration
- Tag system for personalization

**Integrations:**
- Calendly (booking)
- Email platform
- Payment processor
- Facebook group (if possible)
- Website forms

### Email Marketing Platform
**Purpose:** Automated sequences + broadcast campaigns

**Features Needed:**
- Automation workflows (conditional logic)
- Segmentation
- A/B testing
- Templates
- Analytics
- Integration with CRM

**Recommended:** ConvertKit, ActiveCampaign, or Klaviyo

### Content Management System
**Purpose:** Organize, schedule, and track all content

**Features Needed:**
- Content calendar view
- Script library/bank
- Status tracking (idea → draft → approved → scheduled → published)
- Multi-platform scheduling
- Performance analytics
- Collaboration (Jennifer + Steve)

**Options:** Notion + Buffer/Later, Airtable + Zapier, dedicated tool like CoSchedule

### Project Management Tool
**Purpose:** Track backend tasks and operations

**For:** Steve and any future team members

**Features:**
- Task management
- Project timelines
- File storage
- Notes/documentation
- Integration with other tools

**Options:** Notion, ClickUp, Asana

---

## Success Metrics

### Content Creation Efficiency
- **Current:** 2-3 hours/week script writing
- **Goal:** <30 min/week script finalization
- **Measure:** Time Jennifer spends rewriting scripts

### Content Output Volume
- **Current:** Inconsistent, reactive
- **Goal:** 5-7 IG posts/week, 2-3 stories/day, 1 newsletter/week
- **Measure:** Scheduled posts in content calendar

### Revenue Growth
- **Current:** ~$6K-$7.5K/month base + retreat spikes
- **Goal:** To be defined with client
- **Potential Targets:**
  - $15K/month base within 6 months
  - $25K/month base within 12 months
  - Include quarterly retreat revenue

### Product Mix Optimization
- **Current:** Heavy on one-on-ones (energy drain)
- **Goal:** Shift to group experiences
- **Measure:**
  - Workshops: 1 every 2 months → 2-3/month
  - Retreats: 1-2/year → 3-4/year
  - One-on-ones: Maintain 15-17/month (funnel role)

### Audience Growth
- **Current:** 119K IG followers
- **Goal:**
  - 150K IG within 6 months
  - 200K IG within 12 months
  - Podcast listeners: 10K downloads/month within 6 months

### Operational Time Savings
- **Current:** Unknown hours/week on admin
- **Goal:** 50% reduction in admin time
- **Measure:** Weekly time tracking

---

## Constraints & Considerations

### Jennifer's Capacity
- **Energy Drain:** One-on-ones take significant energy
- **Shutdown Risk:** Overwhelm leads to shutdown mode
- **Authenticity Priority:** Won't compromise authentic voice for scale
- **Live Focus:** Committed to live experiences over recorded courses

### Budget Constraints
- **Unknown:** Budget not discussed in discovery call
- **Recent Change:** Financial pressure applied ~2 months ago
- **Steve's Note:** Current revenue (~$6-7K/month) "not a lot of money" for effort invested

### Brand Positioning
- **Strength:** Authentic, vulnerable, "want to be your friend" energy
- **Risk:** Over-polished content could damage trust
- **Differentiation:** NOT Quinlan (young, sassy, performative)
- **Target Audience:** Women 35-60, seeking transformation not entertainment

### Technical Skill Level
- **Jennifer:** Can edit video in Descript, posts to IG
- **Steve:** ChatGPT workflows, transcription, Google Docs
- **Need:** Systems should be low-tech-barrier, intuitive

---

## Project Phases (Proposed)

### Phase 1: Foundation (Weeks 1-4)
- Voice model training (authentic Jennifer scripts)
- Content calendar system implementation
- CRM selection and setup
- Email platform integration
- Quick win: Podcast launch

### Phase 2: Automation (Weeks 5-8)
- Email sequences for workshops/retreats/sessions
- Member onboarding automation
- Content posting automation
- Reminder systems
- Analytics dashboard

### Phase 3: Optimization (Weeks 9-12)
- Multi-channel expansion (TikTok, YouTube)
- Advanced segmentation
- A/B testing workflows
- Revenue optimization strategies
- Team/VA SOPs

### Phase 4: Scale (Month 4+)
- Retreat frequency increase
- Workshop volume increase
- Podcast monetization strategies
- Partnership/affiliate opportunities
- Product expansion (if applicable)

---

## Questions to Clarify

**Before project kickoff, need to determine:**

1. **Budget:** What's the investment range for tools + services?
2. **Timeline:** What's the urgency? (Retreat scheduled Jan 29-Feb 1)
3. **Goals:** Specific revenue targets for 6 months and 12 months?
4. **Pause + Expand:** How does corporate wellness side integrate with this?
5. **Tech Stack:** Current tools for payments, email, CRM?
6. **Team:** Any existing support (VA, social media manager)?
7. **Time Commitment:** How many hours/week can Jennifer commit to content batching?
8. **Decision Making:** Who makes final calls on strategy, tools, budget?

---

## Recommended Next Steps

1. **Define concrete goals:** Revenue, audience, time savings targets
2. **Audit existing tech stack:** What's working, what's not
3. **Prioritize requirements:** Must-have vs. nice-to-have
4. **Budget allocation:** Tools, services, potential team member
5. **Voice model training:** Immediate start on authentic script generation
6. **Podcast launch plan:** Timeline, platform selection, content strategy
7. **Content calendar:** Populate next 30-60 days
8. **Quick wins:** Identify 2-3 things that can be implemented in first 2 weeks

---

## Appendix: Tools Consideration

### Content Creation & Scheduling
- **Notion:** Content calendar, script library, project management
- **Airtable:** Database approach, highly customizable
- **Later / Buffer:** Social media scheduling
- **CoSchedule:** All-in-one content marketing calendar

### Email & CRM
- **ConvertKit:** Creator-focused, simple
- **ActiveCampaign:** Powerful automation, higher learning curve
- **HubSpot:** All-in-one, can be overkill for solo business
- **Kajabi:** If planning digital courses/memberships

### AI & Automation
- **Custom GPT:** Trained on Jennifer's voice
- **Descript:** Already using, could expand usage
- **Zapier / Make:** Connect tools, automate workflows
- **Otter.ai:** Transcription

### Podcast Hosting
- **Transistor:** Clean, simple, good analytics
- **Libsyn:** Established, reliable
- **Anchor (Spotify):** Free, basic features
- **Captivate:** Marketing features built-in

### Community
- **Circle:** Modern alternative to Facebook groups
- **Mighty Networks:** Built for creators
- **Kajabi:** If going all-in on digital products
- **Facebook Groups:** Currently using, familiar

---

*This requirements document is a living document and will be updated based on client feedback, budget constraints, and implementation learnings.*
