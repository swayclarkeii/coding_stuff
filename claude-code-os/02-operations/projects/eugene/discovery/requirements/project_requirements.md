# Eugene - Project Requirements Document

**Project Name:** Document Processing Automation System
**Client:** Eugene - Real Estate Finance Broker
**Last Updated:** December 9, 2025
**Status:** Requirements Complete - Ready for Architecture Phase

---

## Executive Summary

### Project Vision
Build an automated document identification and organization system that reduces Eugene's document processing time from 5-10 hours to 1-2 hours per deal, enabling him to increase capacity from 6 to 15-20 deals annually.

### Core Problem
Eugene receives unlabeled document attachments from clients. He spends 80% of his time manually opening files, identifying document types, labeling them, organizing folders, and generating checklists of missing documents.

### Proposed Solution
**Phase 1:** Email forwarding system that automatically identifies, labels, and organizes documents using AI, then generates a checklist of what's present vs. missing and updates PipeDrive CRM.

**Phase 2:** Client-facing data room portal for self-service document upload and real-time status tracking.

### Success Metrics
- **Time reduction:** 80% (5-10 hours → 1-2 hours per deal)
- **Capacity increase:** 2.5-3x (6 → 15-20 deals/year)
- **AI accuracy:** 95%+ document identification rate
- **ROI timeline:** 3-6 months

---

## Phase 1 Requirements (Core System)

### 1. Email Forwarding & Intake

#### FR1.1: Email Forwarding
**Requirement:** System must accept forwarded emails to a dedicated email address (e.g., automation@domain.com)

**Acceptance Criteria:**
- Eugene can forward any email with attachments
- System processes emails automatically within 5 minutes
- System handles emails with 1-50 attachments
- System supports PDF, DOC, DOCX, XLS, XLSX, JPG, PNG file formats
- System extracts client name from email subject or body

**Priority:** ⭐⭐⭐⭐⭐ Critical

#### FR1.2: Attachment Extraction
**Requirement:** System must automatically extract all attachments from forwarded emails

**Acceptance Criteria:**
- Extracts all attached files regardless of naming convention
- Preserves original file formats
- Handles compressed files (ZIP, RAR) by extracting contents
- Associates all files with the same email/batch/client

**Priority:** ⭐⭐⭐⭐⭐ Critical

#### FR1.3: Client Identification
**Requirement:** System must identify which client/deal the documents belong to

**Acceptance Criteria:**
- Parses client name from email subject line
- Parses client name from email body if not in subject
- Creates unique identifier for each client/deal
- Links to PipeDrive deal if deal ID provided

**Priority:** ⭐⭐⭐⭐⭐ Critical

---

### 2. AI Document Identification

#### FR2.1: Document Type Recognition
**Requirement:** System must identify document type for each attachment using AI

**Acceptance Criteria:**
- Correctly identifies documents from the 18 required types (see section 5)
- Returns document type label (e.g., "Grundbuch", "Calculation", "Exit Strategy")
- Returns confidence score (0-100%)
- Handles German language documents
- Handles English language documents
- Recognizes documents based on content/structure, not filename

**Priority:** ⭐⭐⭐⭐⭐ Critical

**Technical Notes:**
- Use ChatGPT API (GPT-4 or equivalent)
- Send document content with specialized prompt
- German real estate documents have standardized structures
- Sample documents available for prompt engineering

#### FR2.2: Confidence Scoring
**Requirement:** System must provide confidence level for each identification

**Acceptance Criteria:**
- Returns confidence percentage (0-100%)
- High confidence: ≥90%
- Medium confidence: 70-89%
- Low confidence: <70%
- Flags low-confidence identifications for manual review

**Priority:** ⭐⭐⭐⭐ High

#### FR2.3: Multi-Page Document Handling
**Requirement:** System must handle multi-page PDFs correctly

**Acceptance Criteria:**
- Analyzes full document, not just first page
- Handles documents up to 100 pages
- Maintains document integrity (no splitting)

**Priority:** ⭐⭐⭐⭐ High

#### FR2.4: Unknown Document Handling
**Requirement:** System must gracefully handle unrecognizable documents

**Acceptance Criteria:**
- Labels unknown documents as "Unclassified"
- Provides brief description of content if possible
- Flags for manual review
- Doesn't fail processing if one document is unrecognizable

**Priority:** ⭐⭐⭐⭐ High

---

### 3. Document Organization & Labeling

#### FR3.1: File Renaming
**Requirement:** System must rename files to standardized format

**Acceptance Criteria:**
- Renames files with format: `[DocumentType]_[ClientName]_[Date].pdf`
- Example: `Grundbuch_Schmidt_2025-12-09.pdf`
- Handles duplicate document types with numbering: `Calculation_1.pdf`, `Calculation_2.pdf`
- Preserves original file extension

**Priority:** ⭐⭐⭐⭐⭐ Critical

#### FR3.2: Folder Structure
**Requirement:** System must organize files into structured folders

**Acceptance Criteria:**
- Creates folder: `[ClientName]_[Date]/`
- Subfolders: `Critical/`, `Important/`, `Optional/`, `Unclassified/`
- Organizes documents into appropriate subfolders based on priority
- Maintains all files in one organized package

**Priority:** ⭐⭐⭐⭐ High

#### FR3.3: Package Delivery
**Requirement:** System must deliver organized folder to Eugene

**Acceptance Criteria:**
- Zips organized folder structure
- Emails ZIP file to Eugene (or uploads to accessible location)
- Includes checklist in email/folder
- Process completes within 5 minutes of email forward

**Priority:** ⭐⭐⭐⭐⭐ Critical

---

### 4. Checklist Generation

#### FR4.1: Document Checklist
**Requirement:** System must generate checklist comparing received documents vs. required documents

**Acceptance Criteria:**
- Lists all 18 required document types
- Indicates status for each: ✅ Present, ❌ Missing, ⚠️ Needs Review (low confidence)
- Groups by priority: Critical, Important, Optional
- Highlights critical missing documents
- Includes confidence scores for identified documents

**Priority:** ⭐⭐⭐⭐⭐ Critical

**Example Checklist Format:**
```
CLIENT: Schmidt Property Development
DATE: 2025-12-09
DEAL TYPE: Development Finance

CRITICAL DOCUMENTS (Must have to proceed):
✅ Teaser/Exposé (98% confidence)
✅ Calculation (95% confidence)
❌ Grundbuch - MISSING
✅ Exit Strategy (92% confidence)

IMPORTANT DOCUMENTS:
✅ Bauplan (89% confidence)
⚠️ Baugenehmigung (68% confidence) - NEEDS REVIEW
✅ Wirtschaftsplan (94% confidence)
❌ Energy Certificate - MISSING
...
```

#### FR4.2: Summary Statistics
**Requirement:** Checklist must include summary statistics

**Acceptance Criteria:**
- Total documents received
- Total documents identified successfully
- Number of critical documents present
- Number of missing critical documents
- Overall completion percentage

**Priority:** ⭐⭐⭐ Medium

#### FR4.3: Checklist Format
**Requirement:** Checklist must be easily readable and actionable

**Acceptance Criteria:**
- Available as PDF
- Available as plain text in email
- Available as CSV/Excel for tracking
- Formatted for quick scanning (colors, icons, clear labels)

**Priority:** ⭐⭐⭐⭐ High

---

### 5. Required Document Types

#### 18 Standard German Real Estate Finance Documents

**Critical Documents** (Can't proceed without these):
1. **Teaser/Exposé** - Project overview and summary
2. **Calculation** - Financial calculations and projections
3. **Grundbuch** - Land register (must be recent)
4. **Exit Strategy** - Lender repayment plan

**Important Documents** (Required but can sometimes work around):
5. **Bauplan** - Building plan (Development deals only)
6. **Baugenehmigung** - Building permit (Development deals only)
7. **Wirtschaftsplan** - Economic plan
8. **Energy Certificate** - Energy efficiency documentation
9. **Property Photos** - Visual documentation
10. **Architect Statements** - Professional certifications
11. **Site Survey** - Property boundaries and measurements
12. **Rental Agreement** - Current tenant contracts (if applicable)
13. **Insurance Documentation** - Property insurance details
14. **Title Deed** - Ownership proof
15. **Tax Assessment** - Property tax valuation

**Optional Documents** (Nice to have):
16. **Previous Loan Documentation** - For refinance deals
17. **Market Analysis** - Comparable properties
18. **Environmental Reports** - Contamination assessments

**Deal Type Variations:**
- **Acquisition Finance:** Requires documents 1-4, 7-8, 10-15
- **Development Finance:** Requires ALL documents (1-18)
- **Refinance:** Requires documents 1-4, 7-8, 12-16

**Note:** System should check for all 18 by default. Eugene will manually ignore irrelevant ones.

---

### 6. PipeDrive CRM Integration

#### FR6.1: Deal Matching
**Requirement:** System must match processed documents to PipeDrive deals

**Acceptance Criteria:**
- Searches PipeDrive for client name
- Matches to existing deal if found
- Creates new deal if not found
- Uses PipeDrive API with Eugene's credentials

**Priority:** ⭐⭐⭐⭐⭐ Critical

#### FR6.2: Deal Update
**Requirement:** System must automatically update PipeDrive deal status

**Acceptance Criteria:**
- Updates deal stage based on document completeness
- Adds note with checklist summary
- Attaches organized document folder (or link)
- Updates custom fields (if configured)
- Logs activity: "Documents processed on [Date]"

**Priority:** ⭐⭐⭐⭐⭐ Critical

#### FR6.3: Document Attachment
**Requirement:** System must attach processed documents to PipeDrive deal

**Acceptance Criteria:**
- Uploads all renamed documents to deal
- Organizes in PipeDrive files section
- Maintains folder structure if possible
- Provides download link if direct upload not feasible

**Priority:** ⭐⭐⭐⭐ High

#### FR6.4: Status Tracking
**Requirement:** System must update deal status based on document completeness

**Acceptance Criteria:**
- If all critical docs present → Stage: "Qualified"
- If critical docs missing → Stage: "Pending Documents"
- If major issues detected → Stage: "Needs Review"
- Eugene can customize stage mapping

**Priority:** ⭐⭐⭐ Medium

---

### 7. Error Handling & Notifications

#### FR7.1: Processing Confirmation
**Requirement:** Eugene must receive confirmation when processing completes

**Acceptance Criteria:**
- Email sent within 1 minute of processing completion
- Includes: client name, number of docs processed, checklist summary
- Includes link/attachment to organized folder
- Clear subject line: "[ClientName] Documents Processed"

**Priority:** ⭐⭐⭐⭐⭐ Critical

#### FR7.2: Error Notifications
**Requirement:** Eugene must be notified if processing fails

**Acceptance Criteria:**
- Email sent if processing fails
- Includes error description
- Suggests resolution if possible
- Includes original forwarded email for reference

**Priority:** ⭐⭐⭐⭐ High

#### FR7.3: Low Confidence Alerts
**Requirement:** Eugene must be alerted to low-confidence document identifications

**Acceptance Criteria:**
- Email highlights documents with <70% confidence
- Provides AI's reasoning if available
- Suggests manual review
- Doesn't block processing

**Priority:** ⭐⭐⭐⭐ High

#### FR7.4: Missing Critical Documents Alert
**Requirement:** Eugene must be notified if critical documents are missing

**Acceptance Criteria:**
- Email clearly highlights missing critical docs
- Lists: Teaser, Calculation, Grundbuch, Exit Strategy status
- Suggests follow-up with client
- Doesn't block processing

**Priority:** ⭐⭐⭐⭐ High

---

### 8. Technical Requirements

#### FR8.1: ChatGPT API Integration
**Requirement:** System must integrate with ChatGPT API for document identification

**Technical Specs:**
- API: OpenAI ChatGPT API (GPT-4 or GPT-4 Turbo recommended)
- Authentication: API key (Eugene to provide or Sway's team manages)
- Prompt engineering: Specialized prompts for German real estate documents
- Rate limiting: Handle API rate limits gracefully
- Fallback: Queue documents if API unavailable

**Priority:** ⭐⭐⭐⭐⭐ Critical

#### FR8.2: Email Service Integration
**Requirement:** System must integrate with email service for intake and notifications

**Technical Specs:**
- Inbound: Dedicated email address (automation@domain.com)
- Outbound: Eugene's email for notifications
- Protocols: IMAP/SMTP or email service API (SendGrid, etc.)
- Attachment handling: Support up to 25MB per email

**Priority:** ⭐⭐⭐⭐⭐ Critical

#### FR8.3: PipeDrive API Integration
**Requirement:** System must integrate with PipeDrive CRM API

**Technical Specs:**
- API: PipeDrive REST API
- Authentication: Eugene's PipeDrive API token
- Operations: Search deals, update deals, upload files, add notes
- Error handling: Graceful failures if PipeDrive unavailable

**Priority:** ⭐⭐⭐⭐⭐ Critical

#### FR8.4: Data Storage
**Requirement:** System must securely store documents temporarily during processing

**Technical Specs:**
- Encryption: At rest and in transit
- Retention: Delete after 30 days or after confirmation
- Backup: Ensure no data loss during processing
- GDPR compliance: EU data residency if required

**Priority:** ⭐⭐⭐⭐ High

#### FR8.5: Processing Performance
**Requirement:** System must process document batches quickly

**Technical Specs:**
- Target: <5 minutes for 20 documents
- Parallel processing: Identify multiple documents concurrently
- Timeout handling: Individual document timeout at 60 seconds
- Queue system: Handle multiple batches concurrently

**Priority:** ⭐⭐⭐⭐ High

---

### 9. Language Support

#### FR9.1: German Language Primary
**Requirement:** System must excel at processing German language documents

**Acceptance Criteria:**
- ChatGPT prompts optimized for German
- Recognizes German bureaucratic language
- Understands German real estate terminology
- Handles German special characters (ä, ö, ü, ß)

**Priority:** ⭐⭐⭐⭐⭐ Critical

#### FR9.2: English Language Secondary
**Requirement:** System must handle English language documents

**Acceptance Criteria:**
- Recognizes same document types in English
- Handles mixed German/English documents
- International client support

**Priority:** ⭐⭐⭐ Medium

#### FR9.3: Language Auto-Detection
**Requirement:** System should automatically detect document language

**Acceptance Criteria:**
- Detects German vs. English documents
- Adjusts processing accordingly
- Doesn't require manual language selection

**Priority:** ⭐⭐⭐ Medium

---

## Phase 2 Requirements (Future Enhancement)

### 10. Client-Facing Data Room Portal

#### FR10.1: Client Portal Access
**Requirement:** Clients can access secure portal to upload documents

**Acceptance Criteria:**
- Unique URL per client/deal
- Simple login (email + password or magic link)
- Mobile-friendly interface
- No technical knowledge required

**Priority:** ⭐⭐⭐⭐ High (Phase 2)

#### FR10.2: Real-Time Checklist
**Requirement:** Clients see real-time status of their document checklist

**Acceptance Criteria:**
- Visual checklist with ✅/❌ indicators
- Updates immediately after upload
- Shows what's still needed
- Provides examples/templates for each document type

**Priority:** ⭐⭐⭐⭐ High (Phase 2)

#### FR10.3: Document Upload
**Requirement:** Clients can drag-and-drop upload documents directly

**Acceptance Criteria:**
- Drag-and-drop interface
- Supports same file types as Phase 1
- Immediate processing after upload
- Progress indicator

**Priority:** ⭐⭐⭐⭐ High (Phase 2)

#### FR10.4: Automated Client Communication
**Requirement:** System sends automated emails to clients about missing documents

**Acceptance Criteria:**
- Eugene reviews and approves before sending
- Template emails for common scenarios
- Personalized with client name and specific missing docs
- Includes portal link

**Priority:** ⭐⭐⭐ Medium (Phase 2)

---

### 11. Motion Integration (Phase 2)

#### FR11.1: Task Creation
**Requirement:** System creates tasks in Motion for follow-ups

**Acceptance Criteria:**
- Creates task when critical documents missing
- Due date: 3 days from document processing
- Task description includes client name and missing docs
- Links to PipeDrive deal

**Priority:** ⭐⭐⭐ Medium (Phase 2)

---

### 12. Advanced Verification (Phase 2)

#### FR12.1: Document Quality Checks
**Requirement:** System verifies document quality beyond identification

**Acceptance Criteria:**
- Checks Grundbuch date (must be <6 months old)
- Validates calculation completeness
- Flags incomplete or low-quality scans
- Checks for required signatures

**Priority:** ⭐⭐⭐ Medium (Phase 2)

#### FR12.2: Data Extraction
**Requirement:** System extracts key data points from documents

**Acceptance Criteria:**
- Loan amount from calculation
- Property address from Grundbuch
- Exit strategy timeline
- Populates PipeDrive custom fields

**Priority:** ⭐⭐⭐ Medium (Phase 2)

---

## Non-Functional Requirements

### NFR1: Security
- All data encrypted in transit (TLS 1.2+)
- All data encrypted at rest (AES-256)
- API keys stored securely (not in code)
- Access control: Only Eugene and authorized team
- GDPR compliance for EU client data
- Regular security audits

**Priority:** ⭐⭐⭐⭐⭐ Critical

### NFR2: Reliability
- 99%+ uptime target
- Automatic retry on transient failures
- No data loss during processing
- Graceful degradation if APIs unavailable
- Error logging and monitoring

**Priority:** ⭐⭐⭐⭐⭐ Critical

### NFR3: Scalability
- Handle 20 concurrent document batches
- Support up to 50 documents per batch
- Process 100+ deals per month
- No performance degradation with increased load

**Priority:** ⭐⭐⭐⭐ High

### NFR4: Usability
- Eugene requires zero training
- Email forwarding is only action needed
- Clear, actionable checklists
- Minimal clicks/steps
- Intuitive error messages

**Priority:** ⭐⭐⭐⭐⭐ Critical

### NFR5: Maintainability
- Clean, documented code
- Modular architecture
- Easy to update prompts and document types
- Eugene can add new document types without dev work (future)

**Priority:** ⭐⭐⭐⭐ High

---

## Assumptions

1. **Eugene provides:**
   - PipeDrive API credentials
   - Sample documents for all 18 types (3-5 examples each)
   - Current ChatGPT prompts
   - Feedback during testing

2. **Client behavior:**
   - Clients send documents via email (primary method)
   - Documents are in PDF, DOC, DOCX, or image formats
   - Most documents are German, some English
   - Clients sometimes send duplicate or mislabeled files

3. **Technical:**
   - ChatGPT API remains available and performant
   - PipeDrive API remains stable
   - Internet connectivity stable for API calls
   - Email service supports attachments up to 25MB

4. **Legal:**
   - Eugene has rights to process client documents
   - No legal restrictions on automated document processing in Germany
   - GDPR compliance maintained throughout

---

## Out of Scope (Phase 1)

❌ Client-facing portal (Phase 2)
❌ Direct client uploads (Phase 2)
❌ Automated client emails (Phase 2)
❌ Motion integration (Phase 2)
❌ Advanced document verification (Phase 2)
❌ Data extraction from documents (Phase 2)
❌ Mobile app
❌ Document editing or modification
❌ Lender communication features
❌ Multi-user access (only Eugene for Phase 1)

---

## Success Criteria

### Phase 1 Launch Success:
✅ Eugene can forward email with attachments
✅ System processes within 5 minutes
✅ 95%+ document identification accuracy
✅ Organized folder delivered to Eugene
✅ Checklist clearly shows present vs. missing documents
✅ PipeDrive deal updated automatically
✅ Eugene saves 80% of document processing time (5-10 hrs → 1-2 hrs)
✅ Zero critical bugs in production
✅ Eugene uses system for all new deals

### Business Success:
✅ Eugene processes 10-12 deals in Phase 1 launch quarter (vs. 6 previously)
✅ System ROI positive within 6 months (€15-25K investment vs. €10.8-24K annual savings)
✅ Eugene satisfied enough to proceed to Phase 2
✅ Potential for expansion to other brokers in Eugene's network

---

## Dependencies

### External:
- OpenAI ChatGPT API availability
- PipeDrive API availability
- Email service reliability
- Eugene's sample documents provided

### Internal:
- Development team capacity
- Architecture design approval
- Testing environment setup
- Eugene's availability for testing and feedback

---

## Risk Mitigation

**Risk:** AI accuracy below 95%
**Mitigation:** Extensive prompt engineering, sample document training, confidence scoring, manual review workflow

**Risk:** Email forwarding too cumbersome
**Mitigation:** Simplify to one-click forwarding, provide templates, add automation rules if needed

**Risk:** PipeDrive integration issues
**Mitigation:** Build abstraction layer, implement retry logic, provide manual fallback

**Risk:** Client documents in unexpected formats
**Mitigation:** Support multiple formats (PDF, DOC, images), OCR for scanned docs, handle unknowns gracefully

**Risk:** Scope creep during development
**Mitigation:** Strict Phase 1 vs. Phase 2 boundaries, change request process, regular alignment meetings

---

## Next Steps

1. **Architecture Design** (This week)
   - System architecture diagram
   - API integration flows
   - Data model
   - Security architecture

2. **Formal Proposal** (This week)
   - Pricing: €15,000-25,000 estimate
   - Timeline: 8-12 weeks
   - Deliverables summary
   - Terms and conditions

3. **Kickoff** (Week 2-3)
   - Contract signed
   - Development environment setup
   - Access to PipeDrive API
   - Sample documents received

4. **Development** (Weeks 3-14)
   - Sprint-based development
   - Weekly progress updates
   - Bi-weekly demos

5. **Testing & Launch** (Weeks 11-15)
   - Eugene tests with real deals
   - Refinements based on feedback
   - Production launch

---

*This requirements document incorporates insights from both December 1 and December 9 discovery calls. Ready for architecture and proposal phase.*
