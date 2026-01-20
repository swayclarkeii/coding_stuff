# Eugene AMA Document Organizer - Quick Start Guide

**Status:** ✅ PRODUCTION READY
**Date:** January 4, 2026
**Next Action:** Manual activation required

---

## What's Ready

All 4 workflows are validated, tested, and ready for production:

| Workflow | Status | Action Required |
|----------|--------|-----------------|
| **Pre-Chunk 0** (Intake) | ✅ Active | None |
| **Chunk 0** (Folders) | ✅ Active | None |
| **Test Orchestrator** | ✅ Active | None |
| **Document Organizer V4** | ⏳ Ready | Activate manually |
| **Automated Email Test** | ⏳ Ready | Activate manually |

**Test Results:** 5/5 scenarios passing (HP-01, HP-02, EC-01, EC-02, EC-08)

---

## Manual Activation (Required)

n8n MCP tools don't support workflow activation. Complete these steps manually:

### Step 1: Activate Document Organizer V4

1. **Navigate to:** https://n8n.oloxa.ai/workflow/j1B7fy24Jftmksmg
2. **Click:** "Active" toggle (top right)
3. **Verify:** Gmail trigger shows "Listening for events"

### Step 2: Activate Automated Email Test

1. **Navigate to:** https://n8n.oloxa.ai/workflow/HtwT0krXJCcI7tC8
2. **Click:** "Active" toggle (top right)
3. **Run:** Manual test execution to verify

### Step 3: Send Test Email

**Test email format:**
- **To:** swayfromthehook@gmail.com (or configured email)
- **Subject:** Test Document Upload
- **Attachment:** Any PDF from `/dummy_files/` folder
- **Label:** Apply "AMA Document Uploads" label after sending

**Expected result:**
1. Document Organizer V4 triggers
2. PDF uploaded to staging folder
3. OCR extracts text (if scanned)
4. AI classifies document type
5. File moved to correct project folder
6. Project Tracker updated
7. Execution completes in ~60-90s

---

## Critical Fixes Applied (Jan 4, 2026)

All blocking issues resolved:

✅ **Chunk 0 validation errors** - Range parameters added
✅ **Column name mappings** - `Staging_Folder_ID` corrected
✅ **Client Registry cleaned** - Test data removed
✅ **OAuth credentials refreshed** - All active
✅ **AWS Textract configured** - OCR ready

---

## Workflow IDs (Quick Reference)

| Workflow | ID |
|----------|-----|
| Pre-Chunk 0 | `koJAMDJv2Gk7HzdS` |
| Chunk 0 | `Ui2rQFpMu9G1RTE1` |
| Test Orchestrator | `EzPj1xtEZOy2UY3V` |
| Document Organizer V4 | `j1B7fy24Jftmksmg` |
| Automated Email Test | `HtwT0krXJCcI7tC8` |

---

## Credentials Configured

All 5 credential types active:

- ✅ Gmail: `o11Tv2e4SgGDcVpo`
- ✅ Google Drive: `7vK12cTuYm7XlNAy`
- ✅ Google Sheets: `3AIbwgVoWqlgyVKF`
- ✅ OpenAI: `JVWV15NdieQqgSuU`
- ✅ AWS: `1kAZ5ROHQfttq23z`

---

## Google Drive Folder Structure

**Parent Folder:** AMA Capital Documents
**Folder ID:** `1bPAhZYzHI04JwqoBDUAtMXQhk3RhY56v`

**37 folders created per client:**
- 00_INBOX
- 01_Client_Info
- 02_Property_Details
- 03_Financial_Docs
- 04_Legal_Contracts
- ... (32 more)

---

## Google Sheets Integration

**Client Registry:**
- Sheet ID: `1cg-eQ0jdWbEk5OzpvTLOhHumI8zfyg8WyC-cKGdnQCE`
- Tab: `Client_Registry`
- Status: Clean (header row only)

**Project Tracker:**
- Sheet ID: `1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI`
- Purpose: Document classification tracking

---

## Document Types Supported

1. **Exposé** (Property Listings)
2. **Grundbuch** (Land Registry)
3. **Calculation DIN 276** (Cost Estimates)
4. **Exit Strategy** (Investment Analysis)
5. **Others** (Miscellaneous)
6. **Unknown** (Unclassifiable)

**Fuzzy matching:** 80% similarity for German company names

---

## Versioning System

**Filename format:**
```
{TYPE}_{PROJECT}_{DATE}_{TIME}_{CONFIDENCE%}_v{VERSION}.pdf
```

**Example:**
```
Expose_Schmidt_GmbH_20260104_143052_95%_v1.pdf
```

**Versioning:**
- v1 = First upload
- v2 = Second upload (v1 moved to `_Archive`)
- v3 = Third upload (v2 moved to `_Archive`)

---

## Performance Expectations

| Operation | Expected Time |
|-----------|--------------|
| New client folder creation | ~70s |
| Existing client processing | ~60s |
| Error scenario (skip) | ~500ms |
| PDF with OCR | +2-4s per page |

---

## Costs (Monthly)

| Service | Cost |
|---------|------|
| OpenAI API | $1.69 |
| AWS Textract | $0.45 |
| n8n Hosting | $12.00 |
| **Total** | **$14.14/month** |

**Per-transaction cost:** ~$0.14/deal
**Client value per deal:** €1,800-€2,800

---

## Troubleshooting

### Workflow not triggering?

1. Check Gmail label is applied: "AMA Document Uploads"
2. Verify workflow is Active (toggle on)
3. Check execution logs for errors

### Document not appearing in folder?

1. Check execution completed successfully
2. Verify client name extracted correctly
3. Check staging folder for uploaded file
4. Review Project Tracker for classification results

### OCR failing?

**This is expected and handled:**
- Workflow continues even if OCR fails
- Text extraction falls back to standard PDF parsing
- Error handling: `onError: continueRegularOutput`

### OAuth token expired?

**Solution:** Use browser-ops-agent to reauthorize
1. Navigate to n8n credentials page
2. Click credential to reauthorize
3. Follow OAuth flow automatically

---

## Emergency Rollback

**If Document Organizer V4 fails:**

1. **Deactivate workflow** in n8n UI (toggle off)
2. **Check execution logs** for specific error
3. **Contact support** if issue persists

**Low risk:**
- Rollback documented in VERSION_LOG.md
- No data loss (executions isolated)
- Can revert to manual processing immediately

---

## Support Resources

**Documentation:**
- VERSION_LOG.md - Complete version history
- PRODUCTION_READINESS_REPORT_v1.0_2026-01-04.md - Full technical details
- This guide (Quick Start)

**Blueprint Files:**
- Location: `/N8N_Blueprints/v4_phase1/`
- All workflows exported and versioned
- Archived versions in `_archived/` subfolder

**Credentials:**
- Secure storage: `.credentials/aws/`
- Never committed to git (.gitignore configured)

---

## Next Steps After Activation

1. **Monitor first 5 executions** for any edge cases
2. **Test with real client documents** (if available)
3. **Verify all document types** classify correctly
4. **Check versioning system** creates v1, v2, v3 correctly
5. **Review confidence scores** (should be >70%)

**Expected outcome:** Smooth production deployment with minimal issues

---

## Questions?

Review the detailed **Production Readiness Report** for:
- Complete validation results
- Technical architecture details
- Cost analysis and projections
- Rollback procedures
- Lessons learned

**File:** `PRODUCTION_READINESS_REPORT_v1.0_2026-01-04.md`

---

**Document Version:** v1.0
**Last Updated:** January 4, 2026
**Status:** ✅ Ready for production activation
