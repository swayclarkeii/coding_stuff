# SOP Builder Workflow - Success Path Flow Diagram

## Complete Flow (Success Path: Score ≥85%)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     SOP BUILDER SUCCESS PATH                              │
│                        (Score ≥ 85%)                                      │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  Route Based on  │
│      Score       │◄─── Score: 87% (example)
│   (IF Node)      │
└────────┬─────────┘
         │ TRUE (≥85%)
         ▼
┌────────────────────────┐
│ Generate Success Email │
│      (Code Node)       │
│                        │
│ Creates HTML email:    │
│ • Congratulations msg  │
│ • Score display        │
│ • Improved SOP         │
│ • CTA button           │
└───────┬────────────────┘
        │
        │ Splits into 3 paths:
        │
        ├─────────────────────┐
        │                     │
        ▼                     ▼
┌────────────────┐    ┌──────────────────┐
│ Format for     │    │ Generate PDF     │
│   Airtable     │    │      HTML        │
│  (Code Node)   │    │   (Code Node)    │
│                │    │                  │
│ Prepares CRM   │    │ Creates PDF-     │
│ data fields    │    │ optimized HTML:  │
└────────┬───────┘    │ • White theme    │
         │            │ • OLOXA logo     │
         │            │ • Score badge    │
         │            │ • Metadata       │
         │            │ • Full SOP       │
         │            │ • Footer         │
         │            └─────────┬────────┘
         │                      │
         │                      ▼
         │              ┌──────────────────┐
         │              │ Convert HTML to  │
         │              │       PDF        │
         │              │ (HTTP Request)   │
         │              │                  │
         │              │ API: html2pdf    │
         │              │ Output: Binary   │
         │              └─────────┬────────┘
         │                        │
         │                        ▼
         │              ┌──────────────────┐
         │         ┌───┤  Merge Email +   │
         │         │   │       PDF        │
         │         │   │  (Merge Node)    │
         │         │   │                  │
         └─────────┼───│ Input 1: Email   │
                   └───│ Input 2: PDF     │
                       └─────────┬────────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │  Send HTML Email │
                       │   (Gmail Node)   │
                       │                  │
                       │ • HTML body      │
                       │ • PDF attached   │
                       │ • Filename set   │
                       └─────────┬────────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │ Respond to       │
                       │    Webhook       │
                       │                  │
                       │ Returns success  │
                       └──────────────────┘
```

## Improvement Path (Score < 85%)

```
┌──────────────────┐
│  Route Based on  │
│      Score       │◄─── Score: 72% (example)
│   (IF Node)      │
└────────┬─────────┘
         │ FALSE (<85%)
         ▼
┌──────────────────────────┐
│ Generate Improvement     │
│        Email             │
│     (Code Node)          │
│                          │
│ Creates improvement msg: │
│ • Areas to improve       │
│ • Missing elements       │
│ • Next steps             │
└───────┬──────────────────┘
        │
        │ Splits into 2 paths:
        │
        ├──────────────┐
        │              │
        ▼              ▼
┌────────────┐  ┌──────────────┐
│ Format for │  │ Send HTML    │
│  Airtable  │  │    Email     │
│            │  │              │
│ (No PDF)   │  │ (No PDF)     │
└────────────┘  └──────────────┘
```

## Key Differences

| Feature | Success Path (≥85%) | Improvement Path (<85%) |
|---------|---------------------|-------------------------|
| Email Type | Congratulations | Improvement suggestions |
| PDF Generation | ✅ YES | ❌ NO |
| PDF Content | Full SOP + score | N/A |
| Email Attachment | PDF file | None |
| CTA | Book discovery call | Improve and resubmit |

## New Nodes Summary

| Node Name | Type | Purpose | Position |
|-----------|------|---------|----------|
| Generate PDF HTML | Code | Creates PDF-ready HTML | After success email |
| Convert HTML to PDF | HTTP Request | Converts HTML → PDF binary | After PDF HTML |
| Merge Email + PDF | Merge | Combines email + PDF | Before Gmail send |

## Data Flow

```
Success Email Node Output:
{
  name: "John Smith",
  email: "john@example.com",
  sop_score: 87,
  improved_sop: "# Employee Onboarding SOP\n\n## Purpose...",
  html_report: "<html>...</html>",
  email_subject: "Congratulations! Your SOP Scored 87%",
  ...
}
          ↓
Generate PDF HTML Node:
{
  ...previous data,
  pdf_html: "<!DOCTYPE html><html>...PDF-optimized HTML...</html>"
}
          ↓
Convert to PDF Node:
{
  ...previous data,
  data: [Binary PDF file]
}
          ↓
Merge Node:
{
  name: "John Smith",           ← from email data
  email: "john@example.com",    ← from email data
  html_report: "<html>...</html>", ← from email data
  data: [Binary PDF file]       ← from PDF node
}
          ↓
Gmail Node:
• Body: html_report
• Attachment: data
• Filename: John_Smith_SOP_Analysis.pdf
```

## PDF Structure

```
┌────────────────────────────────────┐
│         OLOXA Logo (centered)      │
├────────────────────────────────────┤
│     SOP Analysis Report            │
│                                    │
│         ┌──────────────┐           │
│         │     87%      │           │
│         │ Completeness │           │
│         └──────────────┘           │
│          (Blue badge)              │
├────────────────────────────────────┤
│  SOP Details                       │
│  ─────────────                     │
│  Prepared for: John Smith          │
│  Goal: Employee onboarding         │
│  Department: HR                    │
│  End Users: HR Managers            │
│  Focus: Quality & Consistency      │
│  Generated: January 29, 2026       │
├────────────────────────────────────┤
│  Your Finalized SOP                │
│  ─────────────────                 │
│                                    │
│  [Full SOP content with proper     │
│   formatting, headers, lists,      │
│   numbered steps, etc.]            │
│                                    │
├────────────────────────────────────┤
│  Generated by OLOXA.AI SOP Builder │
│  January 29, 2026                  │
│  Visit sopbuilder.oloxa.ai         │
└────────────────────────────────────┘
```

## Testing Checklist

- [ ] Submit SOP with ≥85% score
- [ ] Verify email arrives with attachment
- [ ] Check PDF filename format
- [ ] Open PDF and verify:
  - [ ] Logo appears
  - [ ] Score badge visible
  - [ ] Metadata complete
  - [ ] SOP properly formatted
  - [ ] Footer present
- [ ] Test improvement path (<85%):
  - [ ] No PDF generated
  - [ ] Improvement email sent
- [ ] Verify Airtable logging still works
- [ ] Check webhook response
