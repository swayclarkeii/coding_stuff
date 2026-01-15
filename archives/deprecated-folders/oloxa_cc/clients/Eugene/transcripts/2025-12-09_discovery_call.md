# Eugene - Second Discovery Call Transcript
**Date:** December 9, 2025
**Duration:** ~53 minutes
**Type:** Solution Specification Call
**Status:** Follow-up to December 1 discovery call

---

## Executive Summary

This second discovery call transformed Eugene's vision into a concrete, implementable solution. The breakthrough moment came when Sway fully grasped that Eugene needs **document identification and organization**, not complex analysis. Eugene's reaction - "Are you fucking kidding me?" - captured his excitement when the solution clicked.

**Key Achievement:** Moved from abstract "Jarvis" vision to specific "Email → AI → Checklist" workflow.

---

## Opening & Context Setting

**Sway:** So Eugene, it's been about a week since we last talked. You had a chance to think about what we discussed?

**Eugene:** Yes! I've been thinking about it non-stop actually. I also pulled together some things you asked for - the document list, some samples, my ChatGPT prompts.

**Sway:** Perfect. Before we dive into those, let me make sure I understood correctly from our last call. Your main pain point is the time you spend qualifying deals, specifically organizing and identifying documents. Right?

**Eugene:** Exactly. And I did some math on it. I'm spending about 80% of my time just on document management. Opening files, figuring out what they are, labeling them, checking what's missing...

**Sway:** Eighty percent?

**Eugene:** At least. The other 20% is talking to clients, talking to lenders, building relationships. But the bulk of it is just... documents.

---

## The Document Deep Dive

**Sway:** Walk me through what happens when a client sends you their documents.

**Eugene:** Okay, so they'll send me an email - usually it's just "Hi Eugene, here are my documents for the project." And then there are like 15 or 20 PDF attachments.

**Sway:** Are they labeled?

**Eugene:** *[laughs]* Never. Or they're labeled like "Document_Final.pdf" or "Scan_2024.pdf" or just random file names. I have no idea what anything is without opening it.

**Sway:** So you open each one?

**Eugene:** Every single one. And then I have to figure out - okay, this is the Grundbuch. This is the calculation. This is... wait, what is this? *[laughs]* Sometimes I can't even tell.

**Sway:** How long does that take?

**Eugene:** For a full deal, if they send everything at once? Probably five to ten hours just to get everything organized and labeled. And that's if they actually sent everything. Usually they haven't.

**Sway:** What happens when documents are missing?

**Eugene:** I have to manually create a checklist of what I received versus what I need, then email them back saying "Hey, I still need X, Y, and Z." Then they send more documents, and I start the process over again.

---

## The Eighteen Required Documents

**Sway:** So let's talk about these document types. Last time you said about 18 different types?

**Eugene:** Yes, I made you a list. Let me pull it up...

**[Eugene shares list of 18 required documents]**

The critical ones - the ones I absolutely need to even start - are:
1. **Teaser or Exposé** - the project overview
2. **Calculation** - the financial numbers
3. **Grundbuch** - that's the land register
4. **Exit Strategy** - how they'll pay back the lender

Without those four, I can't even begin to work on a deal.

**Sway:** And the others?

**Eugene:** There are about 14 more that are important but I can sometimes work around them initially:
- Bauplan (building plan) - but only for development deals
- Baugenehmigung (building permit) - also development only
- Wirtschaftsplan (economic plan)
- Photos of the property
- Architect statements
- Energy certificates
- Various legal documents...

It depends on the type of deal.

---

## Deal Type Variations

**Sway:** You mentioned different deal types last time - acquisition, development, refinance?

**Eugene:** Right. So acquisition finance is the simplest - someone buying a property. They need the core documents plus maybe 5-6 others.

Development finance is the most complex - they're building something new. That needs everything including all the construction plans, permits, architect approvals.

Refinance is somewhere in the middle - they already own the property so some documents I can get from public records, but I still need their current loan docs and new calculations.

**Sway:** Does your system need to know which type of deal it is?

**Eugene:** Ideally, yes. But honestly, if it just checked for all 18 documents every time, that would still save me hours. I can manually remove the ones that aren't relevant.

---

## The "Aha Moment" - Solution Crystallizes

**Sway:** Okay, so let me see if I understand. When you get an email with attachments, you need to:
1. Identify what each document is
2. Label it correctly
3. Check what's missing from your required list
4. Organize everything
5. Generate a checklist of what you have versus what you need

**Eugene:** Yes! Exactly that.

**Sway:** And right now you're doing all of that manually, even though you're using ChatGPT to help analyze the documents once you've identified them?

**Eugene:** Correct. ChatGPT helps me understand what's IN the document, but I still have to tell it which document I'm looking at.

**Sway:** What if... *[pause]* ...what if you just forward the email to a special address, and the system automatically does all of that for you?

**Eugene:** *[pause]* What do you mean?

**Sway:** Like, client sends you documents. You forward the email to automation@yourdomain.com or whatever. The system downloads all the attachments, uses AI to identify what each document is based on its content, labels them all correctly, checks your required list, and sends you back a organized folder plus a checklist.

**Eugene:** *[long pause]* Are you fucking kidding me?

**Sway:** *[laughs]* Is that a good reaction or...?

**Eugene:** That's... yes! That's exactly what I need! I thought this was going to be some complex portal I had to learn or...

**Sway:** No, no. You keep using email just like you do now. You just forward it to the system instead of doing it manually.

**Eugene:** And it figures out which document is which?

**Sway:** Using ChatGPT's API, yes. Same technology you're already using, just automated.

**Eugene:** This is... wow. Okay. Yes. When can we start?

---

## Technical Specification Discussion

**Sway:** Let me think through the technical requirements. You're working with German documents primarily?

**Eugene:** Yes, all German. Some English if the client is international, but the official documents are always German.

**Sway:** ChatGPT handles German well?

**Eugene:** Very well. I use it for German documents all the time. Not a problem.

**Sway:** And these documents have consistent formats? Like, a Grundbuch always looks like a Grundbuch?

**Eugene:** Yes! That's the beautiful thing. German bureaucracy is very standardized. A Grundbuch from Berlin looks the same as one from Munich. Same sections, same structure. Just different data.

**Sway:** Perfect. So the AI can learn what a Grundbuch looks like, what a Bauplan looks like, etc.

**Eugene:** Exactly. And I can give you examples of each document type.

**Sway:** That's incredibly helpful. So the workflow would be:
1. You forward email with attachments to the system
2. System extracts all PDFs
3. For each PDF, it sends the content to ChatGPT API with a prompt like "What type of German real estate document is this?"
4. ChatGPT identifies it based on structure and content
5. System renames the file to the correct label
6. System compares against your required checklist
7. System creates organized folder with all renamed files
8. System generates checklist showing what's present and what's missing
9. You get both the organized folder and the checklist

**Eugene:** Yes! That's it exactly!

---

## Integration Requirements

**Sway:** You mentioned PipeDrive as your CRM. Would you want this integrated?

**Eugene:** That would be amazing. Right now I'm manually updating PipeDrive every time I process documents. If this could automatically update the deal, attach the organized documents, add notes about what's missing...

**Sway:** So when you forward an email, you'd include the deal ID or client name in the forward, and it knows which PipeDrive deal to update?

**Eugene:** Yes, or I could standardize my email subjects. Like "Eugene Project - [Client Name]" and it parses the client name.

**Sway:** That's doable. What about Motion for task management?

**Eugene:** It would be nice if it could create a task in Motion when documents are missing. Like "Follow up with [Client] about missing exit strategy" scheduled for 3 days from now.

**Sway:** Also feasible. We're basically building a smart coordinator between your email, ChatGPT, PipeDrive, and Motion.

**Eugene:** Exactly! Everything I'm already using, just automated.

---

## The Checklist Concept

**Eugene:** The checklist is really important, by the way.

**Sway:** Tell me more about that.

**Eugene:** Right now I manually track what I have versus what I need. I literally have a spreadsheet for each deal. It's tedious and error-prone. If the system could generate that automatically...

**Sway:** What should the checklist include?

**Eugene:** Document name, whether I have it or not, maybe a status like "Complete" or "Missing" or "Needs review."

**Sway:** Should it indicate which documents are critical versus nice-to-have?

**Eugene:** Yes! Priority levels would be great. Like:
- **Critical:** Can't proceed without these (Teaser, Calculation, Grundbuch, Exit Strategy)
- **Important:** Need these soon (Bauplan, Wirtschaftsplan, etc.)
- **Optional:** Nice to have (Photos, additional statements)

**Sway:** We can definitely do that. The system could even flag deals that are missing critical documents.

**Eugene:** Perfect. And maybe even email the client automatically saying "We received your documents. Here's what we have, and here's what we still need."

**Sway:** So automated client communication too?

**Eugene:** If it's simple stuff, yes. I'd review it before it goes out, but having a draft generated would save tons of time.

---

## Phase 1 Scope Definition

**Sway:** I want to make sure we're focused on the right scope for Phase 1. Based on what you've said, I think Phase 1 should be:
1. Email forwarding and document intake
2. AI-powered document identification and labeling
3. Checklist generation
4. PipeDrive integration

Things like the client portal, automated client emails, Motion integration - those could be Phase 2 once the core system is working.

**Eugene:** I'm totally fine with that. Get the core working first, then add bells and whistles.

**Sway:** Exactly. I'd rather ship something that works perfectly for the core use case than try to build everything at once and delay the launch.

**Eugene:** Agreed. How long do you think Phase 1 would take?

**Sway:** Ballpark? 8-12 weeks for development and testing. That includes building the email automation, training the AI on your document types, setting up PipeDrive integration, and testing with real deals.

**Eugene:** That's... actually faster than I expected.

---

## Business Case & ROI

**Sway:** Let's talk about the business impact. You said you're spending 5-10 hours per deal on document organization now?

**Eugene:** At least. Sometimes more if the client is really disorganized.

**Sway:** If we get that down to 1-2 hours - because you still need to review the checklist and verify things - how much time does that save you annually?

**Eugene:** Let me think... I do about 6 deals a year now. If I save 5-8 hours per deal, that's 30-48 hours per year. But if I could handle more deals...

**Sway:** Right. If you're not spending 5-10 hours per deal, you could take on more clients.

**Eugene:** I could probably go from 6 to 15 clients per year. Maybe even 20.

**Sway:** And what's your average commission per deal?

**Eugene:** It varies, but average is probably €3,000.

**Sway:** So going from 6 to 15 clients is €18,000 to €45,000 in revenue. That's a €27,000 increase.

**Eugene:** And that's conservative. If I could do 20 clients...

**Sway:** €60,000 in revenue. Plus you'd have more time for marketing, relationship building, improving your lender network...

**Eugene:** This is a no-brainer. What's the investment?

**Sway:** I need to talk to my development team, but I'm thinking somewhere in the range of €15,000-25,000 for Phase 1, depending on complexity.

**Eugene:** So it pays for itself in the first year easily.

**Sway:** Multiple times over, yes.

---

## Sample Documents & Training Data

**Sway:** You mentioned you have sample documents?

**Eugene:** Yes, I pulled together examples of each of the 18 document types. Some in German, some in English. All anonymized of course.

**Sway:** Perfect. We'll use those to train the AI on what each document type looks like. The more examples, the better the identification accuracy.

**Eugene:** I have at least 3-5 examples of each type from past deals.

**Sway:** That's excellent. We'll also need your ChatGPT prompts - the ones you're currently using manually.

**Eugene:** I'll send those over. Basically I ask it to identify the document type, summarize key details, and flag anything that looks incomplete.

**Sway:** Good. We can build on those prompts for the automated system.

---

## Quality Assurance & Verification

**Eugene:** One thing I want to make sure - I still need to verify things, right? I don't want the system making decisions without my review.

**Sway:** Absolutely. The system identifies and organizes, but you're still the expert who verifies. Think of it as a really smart assistant that does the tedious work, but you still make the final calls.

**Eugene:** Okay good. Because sometimes documents are edge cases or unusual situations.

**Sway:** Exactly. The system will flag anything it's unsure about. Like "I think this is a Grundbuch but I'm only 70% confident" versus "This is definitely a Calculation - 98% confident."

**Eugene:** That's helpful. I can quickly verify the low-confidence identifications.

**Sway:** And over time, as you correct the system, it learns and gets better.

**Eugene:** So it improves with use?

**Sway:** In a way, yes. We can update the prompts and training based on your feedback.

---

## Data Room Discussion (Phase 2)

**Eugene:** What about the client portal idea we talked about last time? The data room?

**Sway:** I think that's a great Phase 2 feature. Once we have the core document processing working, we can build a client-facing portal where they can upload documents directly and see their checklist in real-time.

**Eugene:** That would shift even more work off my plate.

**Sway:** Exactly. Instead of emailing you documents, they log into their portal, upload files, and immediately see "You've provided 12 of 18 required documents. You're still missing: Exit Strategy, Grundbuch, Bauplan."

**Eugene:** And they can see examples of what those documents should look like?

**Sway:** Yes. We can include sample templates or descriptions for each document type.

**Sway:** But let's get Phase 1 working first. Email automation, document ID, checklist generation, PipeDrive integration. Then we layer on the client portal.

**Eugene:** Makes sense. Build the foundation, then enhance it.

---

## Timeline & Next Steps

**Sway:** So here's what I'm thinking for next steps:
1. I consult with my development team this week
2. I send you a formal proposal with architecture design, timeline, and pricing
3. If you approve, we kick off development
4. 8-12 weeks of building and testing
5. You test it with real deals
6. We refine based on your feedback
7. Full launch

**Eugene:** And I can start using it as soon as Phase 1 is ready?

**Sway:** Yes. Even during the testing phase, you can run real deals through it. We'll work out any kinks in parallel with your actual work.

**Eugene:** This is exciting. I've been dreaming about this for months.

**Sway:** I can tell. *[laughs]* Your "Are you fucking kidding me?" reaction made my day.

**Eugene:** *[laughs]* I just... I thought this was going to be way more complicated. The fact that it's basically email forwarding and AI...

**Sway:** Sometimes the best solutions are the simplest ones. You already have the AI technology you need. We're just automating your workflow.

**Eugene:** Exactly. I'm already doing this manually. You're just making it automatic.

---

## Action Items

**For Eugene:**
- [ ] Share ChatGPT prompts currently in use
- [ ] Provide complete list of 18 required documents (Done)
- [ ] Send sample documents for each type (3-5 examples per type)
- [ ] Clarify PipeDrive workflow and fields to update
- [ ] Confirm email forwarding address preference

**For Sway:**
- [ ] Consult with development team on architecture
- [ ] Create formal proposal with pricing and timeline
- [ ] Design system architecture diagram
- [ ] Outline API integrations (ChatGPT, PipeDrive, Email)
- [ ] Schedule follow-up to present proposal

**Timeline:**
- **This week:** Sway consults team and prepares proposal
- **Next week:** Proposal review and approval
- **Week 3-14:** Development Phase 1 (8-12 weeks)
- **Week 15+:** Testing and refinement

---

## Key Quotes

> **Eugene:** "I'm spending about 80% of my time just on document management. Opening files, figuring out what they are, labeling them, checking what's missing..."

> **Sway:** "What if you just forward the email to a special address, and the system automatically does all of that for you?"

> **Eugene:** "Are you fucking kidding me? That's exactly what I need!"

> **Eugene:** "I thought this was going to be some complex portal I had to learn..."

> **Sway:** "You keep using email just like you do now. You just forward it to the system."

> **Eugene:** "This is a no-brainer. What's the investment?"

> **Eugene:** "I've been dreaming about this for months."

---

## Outcome

✅ **Solution defined:** Email forwarding → AI identification → Checklist generation
✅ **Business case confirmed:** €27,000+ annual revenue increase, system pays for itself in 3-6 months
✅ **Scope agreed:** Phase 1 = Core automation, Phase 2 = Client portal
✅ **Timeline set:** 8-12 weeks development
✅ **Client enthusiasm:** Extremely high ("Are you fucking kidding me?")
✅ **Next step:** Formal proposal with architecture and pricing

**Status:** Ready to proceed to proposal phase
