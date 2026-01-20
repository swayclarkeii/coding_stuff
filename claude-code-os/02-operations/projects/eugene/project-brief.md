# Project Brief - Eugene (AMA Capital)

**Client:** Eugene Owusu - AMA Capital
**Start Date:** December 2024
**Status:** Proposal Phase
**Primary Contact:** Eugene

---

## Project Overview

**Goal:** Build automated document processing system to reduce Eugene's document management time from 5-10 hours to 1-2 hours per deal

**Scope:**
- Email forwarding automation to special address
- AI-powered document identification (18 German real estate document types)
- Automatic file labeling and organization
- Checklist generation (present vs. missing documents)
- PipeDrive CRM integration

**Success Criteria:**
- 95%+ AI document identification accuracy
- 80% time reduction per deal (5-10 hours → 1-2 hours)
- Capacity increase from 6 to 15-20 deals annually
- Processing time < 5 minutes per batch
- ROI positive within 3-6 months

---

## The Problem

Eugene spends 80% of his time manually:
- Opening unlabeled document attachments
- Identifying document types (Grundbuch, Calculation, Exit Strategy, etc.)
- Labeling files with proper names
- Organizing into folders
- Creating checklists of missing documents
- Emailing clients about gaps

This prevents him from scaling beyond 6 deals per year.

---

## The Solution

**Phase 1: Email Forwarding Automation** (8-12 weeks)
- Eugene forwards client emails to automation@domain.com
- System extracts attachments
- ChatGPT API identifies each document type
- Files automatically renamed and organized
- Checklist generated showing present vs. missing documents
- PipeDrive deal automatically updated

**Phase 2: Client Portal** (Future)
- Client-facing data room
- Direct document uploads
- Real-time checklist visibility
- Automated client communication
- Motion task integration

---

## Business Impact

**Current State:**
- 6 deals per year
- €18,000 annual revenue
- 80% time on documents, 20% on relationships

**Phase 1 Target:**
- 10-12 deals per year
- €30,000-36,000 annual revenue
- 10% time on documents, 90% on relationships

**Phase 2 Target:**
- 15-20 deals per year
- €45,000-60,000 annual revenue
- Full automation with client self-service

**ROI:** €15,000-25,000 investment pays back in 3-6 months

---

## Stakeholders

| Name | Role | Involvement |
|------|------|-------------|
| Eugene | Client / End User | Daily user, provides requirements and testing feedback |
| Sway | Project Lead / Oloxa.ai | Solution architect, client liaison |
| Development Team | Builders | Design, development, testing, deployment |

---

## Timeline

**Start:** December 2024
**Proposal Phase:** December 9-16, 2024
**Target Kickoff:** December 23-30, 2024
**Target Launch:** Mid-March 2026 (12 weeks from kickoff)
**Key Milestones:** [See timeline.md]

---

## Technical Stack

- **AI:** ChatGPT API (GPT-4) for German document identification
- **Email:** Dedicated forwarding address with IMAP/SMTP integration
- **CRM:** PipeDrive API integration
- **Storage:** Secure cloud storage with encryption
- **Languages:** German (primary), English (secondary)

---

## Notes

- Client extremely enthusiastic - breakthrough moment Dec 9
- Already using ChatGPT manually (proof of concept validated)
- Sample documents and prompts being provided
- German documents have standardized structures (bureaucracy helps accuracy)
- Phase 1 focused on backend automation only
- Client portal deferred to Phase 2 to avoid scope creep
- PipeDrive integration critical; Motion integration nice-to-have
