# Company Name Implementation - SOP Builder Lead Magnet

**Date:** 2026-01-30
**Workflow ID:** ikVyMpDI0az6Zk4t
**Agent:** solution-builder-agent

## Summary

Added `company_name` support throughout the SOP Builder Lead Magnet workflow. The frontend can now send a `companyName` field in form submissions, and it will be used in email subjects, PDF titles, and metadata throughout the workflow.

Also updated the PDF logo from the old wide banner to the new square black logo with proper sizing.

## Changes Made

### 1. Parse Form Data (ID: `parse-form`)

**Type:** Code node
**Change:** Added company_name mapping to pass through from form submission

**Updated code:**
```javascript
company_name: body.company_name || body.companyName || ''
```

**Supports both camelCase and snake_case from frontend.**

---

### 2. Generate Success Email (≥85%) (ID: `generate-success-email`)

**Type:** Code node
**Changes:**
- Read `company_name` from input data
- Updated email subject to use company name: `"[Company]'s Improved SOP: [Process] - Scored XX%"`
- Passes company_name through to output

**Key code:**
```javascript
const companyName = data.company_name || '';
const emailSubject = (companyName ? companyName + "'s " : "Your ") + "Improved SOP: " + (data.goal || "Process") + " - Scored " + score + "%";
```

**Examples:**
- With company: "Acme Corp's Improved SOP: Customer Onboarding - Scored 92%"
- Without company: "Your Improved SOP: Customer Onboarding - Scored 92%"

---

### 3. Generate Improvement Email (<85%) (ID: `generate-improvement-email`)

**Type:** Code node
**Changes:**
- Read `company_name` from input data
- Updated email subject to use company name: `"[Company]'s SOP Analysis - Score: XX%"`
- Passes company_name through to output

**Key code:**
```javascript
const companyName = data.company_name || '';
const emailSubject = (companyName ? companyName + "'s " : "") + "SOP Analysis" + (companyName ? "" : " for " + name) + " - Score: " + score + "%";
```

**Examples:**
- With company: "Acme Corp's SOP Analysis - Score: 67%"
- Without company: "SOP Analysis for John Smith - Score: 67%"

---

### 4. Generate PDF HTML (ID: `generate-pdf-html`)

**Type:** Code node
**Changes:**
1. Read `company_name` from input data
2. Use in document title: `"[Company]'s [Process Name]"` if company provided
3. Show company name in PDF metadata section
4. **Updated logo URL** from `logo.png` to `logo-black-transparent.png`
5. **Fixed logo sizing** to `height: 50px; width: auto;` (was 60x60 square)

**Key code:**
```javascript
const companyName = data.company_name || '';
const documentTitle = companyName ? `${companyName}'s ${processName}` : processName;
```

**Logo change:**
```html
<!-- OLD -->
<img src="https://sopbuilder.oloxa.ai/logo.png" alt="Oloxa Logo" class="logo" />
<style>.logo { width: 60px; height: 60px; }</style>

<!-- NEW -->
<img src="https://sopbuilder.oloxa.ai/logo-black-transparent.png" alt="Oloxa Logo" class="logo" />
<style>.logo { height: 50px; width: auto; }</style>
```

**Metadata section (new):**
```html
<p><strong>Process Name:</strong> ${documentTitle}</p>
${companyName ? `\n    <p><strong>Company:</strong> ${companyName}</p>` : ''}
<p><strong>Prepared for:</strong> ${userName}</p>
```

---

### 5. Format for Airtable (ID: `format-for-airtable`)

**Type:** Code node
**Change:** Added company_name to data sent to Airtable for lead tracking

**Updated code:**
```javascript
company_name: data.company_name || ''
```

---

## Frontend Integration

**The frontend should send:**
```javascript
{
  email: "user@example.com",
  name: "John Smith",
  companyName: "Acme Corp",  // NEW FIELD (optional)
  processName: "Customer Onboarding",
  processSteps: "1. ...",
  // ... other fields
}
```

**Both `companyName` (camelCase) and `company_name` (snake_case) are supported.**

---

## Testing Checklist

### With Company Name
- [ ] Submit form with company name
- [ ] Verify email subject includes company name
- [ ] Verify PDF title is "[Company]'s [Process]"
- [ ] Verify PDF metadata shows company name
- [ ] Verify Airtable record includes company_name
- [ ] Verify new logo displays correctly in PDF (50px height, square)

### Without Company Name (Backward Compatibility)
- [ ] Submit form without company name
- [ ] Verify email subject says "Your Improved SOP"
- [ ] Verify PDF title is just process name
- [ ] Verify PDF metadata doesn't show empty company field
- [ ] Verify Airtable record has empty company_name (not broken)
- [ ] Verify new logo displays correctly in PDF

### Logo Visual Check
- [ ] PDF header shows square black logo (not old wide banner)
- [ ] Logo is approximately 50px tall
- [ ] Logo maintains aspect ratio (width scales with height)
- [ ] Logo displays clearly in PDF (not blurry or pixelated)

---

## Validation Results

**Workflow validated:** ✅ No critical errors
**Total nodes:** 36
**Warnings:** 52 (mostly outdated typeVersions and missing error handling - non-critical)

**Note:** The validation error "Cannot return primitive values directly" on Generate PDF HTML is a false positive. The node correctly returns `[{ json: { ...data, pdf_html: pdfHtml } }]`.

---

## Files Modified

1. **Parse Form Data** - Added company_name passthrough
2. **Generate Success Email (≥85%)** - Company name in subject
3. **Generate Improvement Email (<85%)** - Company name in subject
4. **Generate PDF HTML** - Company name in title, metadata, and logo update
5. **Format for Airtable** - Company name in lead data

---

## Backward Compatibility

✅ **All changes are backward compatible.**

- If `company_name` is not provided, workflow behaves exactly as before
- Uses empty string fallback: `company_name || ''`
- Conditional rendering in templates prevents empty company fields from showing

---

## Next Steps

1. **Frontend:** Add company name field to form (optional)
2. **Test:** Run end-to-end test with and without company name
3. **Airtable:** Verify company_name column exists (or add it)
4. **Visual:** Check PDF with new logo rendering

---

## Logo Specifications

**Old Logo:**
- URL: `https://sopbuilder.oloxa.ai/logo.png`
- Dimensions: Wide banner format
- Size in PDF: 60x60px square (forced)

**New Logo:**
- URL: `https://sopbuilder.oloxa.ai/logo-black-transparent.png`
- Dimensions: 1250x1250px (square)
- Size in PDF: 50px height, auto width (maintains aspect ratio)
- Format: Black logo on transparent background

---

## Implementation Status

✅ **COMPLETE**

All nodes updated successfully. Workflow is ready for frontend integration.
