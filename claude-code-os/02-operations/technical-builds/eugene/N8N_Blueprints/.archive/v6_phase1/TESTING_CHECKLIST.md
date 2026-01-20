# Testing Checklist: Pre-Chunk 0 Fix

**Date:** 2026-01-08
**Fix Applied:** Passed extracted text from Pre-Chunk 0 to Chunk 2
**Workflow ID:** YGXWjWcBIk66ArvT

---

## ✅ Pre-Test Setup

- [ ] Pre-Chunk 0 is ACTIVE (workflow ID: YGXWjWcBIk66ArvT)
- [ ] Chunk 2 is ACTIVE (workflow ID: g9J5kjVtqaF9GLyc)
- [ ] Gmail account accessible (swayclarkeii@gmail.com)
- [ ] Test PDF available (e.g., OCP-Anfrage-AM10.pdf)

---

## 🧪 Test 1: EXISTING Client (Villa Martens)

**Purpose:** Verify fix works for existing client flow

### Steps

1. [ ] Open Gmail as `swayfromthehook@gmail.com`
2. [ ] Compose new email:
   - To: `swayclarkeii@gmail.com`
   - Subject: `Test - Fix Validation - Villa Martens`
   - Body: (any text)
   - Attachment: `OCP-Anfrage-AM10.pdf` (from test repository)
3. [ ] Send email
4. [ ] Wait 2-3 minutes for Gmail trigger
5. [ ] Open n8n and check executions

### Expected Results

- [ ] ✅ Pre-Chunk 0 execution appears
- [ ] ✅ Pre-Chunk 0 status = SUCCESS
- [ ] ✅ Chunk 2 execution appears
- [ ] ✅ Chunk 2 status = SUCCESS
- [ ] ❌ NO 404 error in Chunk 2

### Verification Points

**Check Pre-Chunk 0 execution:**
- [ ] "Evaluate Extraction Quality" node has `extractedText` field (populated)
- [ ] "Prepare for Chunk 2 (EXISTING)" output has:
  - `extractedText`: (long text string)
  - `extractionMethod`: "digital_pre_chunk"
  - `textLength`: (number > 100)
  - `skipDownload`: true

**Check Chunk 2 execution:**
- [ ] "Normalize Input" node receives `extractedText` in input
- [ ] "Normalize Input" output has `skipDownload: true`
- [ ] Download node was **SKIPPED** (not executed in flow)
- [ ] "Detect Scan vs Digital" receives text directly

### Success Criteria

✅ **PASS** if all checkboxes above are checked
❌ **FAIL** if any 404 error or missing data

---

## 🧪 Test 2: NEW Client

**Purpose:** Verify fix works for new client flow (with Chunk 0 folder creation)

### Steps

1. [ ] Edit client registry Google Sheet
2. [ ] Temporarily remove "Villa Martens" from registry (or use different client name)
3. [ ] Send email with PDF (same steps as Test 1)
4. [ ] Wait 2-3 minutes for Gmail trigger
5. [ ] Check n8n executions

### Expected Results

- [ ] ✅ Pre-Chunk 0 execution SUCCESS
- [ ] ✅ Chunk 0 execution appears (folder creation)
- [ ] ✅ Chunk 0 status = SUCCESS
- [ ] ✅ Chunk 2 execution SUCCESS
- [ ] ❌ NO 404 error in Chunk 2

### Verification Points

**Check Pre-Chunk 0 execution:**
- [ ] "Prepare for Chunk 2 (NEW)" output has:
  - `extractedText`: (populated)
  - `extractionMethod`: "digital_pre_chunk"
  - `textLength`: (number > 100)
  - `skipDownload`: true

**Check Chunk 2 execution:**
- [ ] Same verification as Test 1
- [ ] Download node was **SKIPPED**

### Success Criteria

✅ **PASS** if all checkboxes above are checked
❌ **FAIL** if any 404 error or missing data

---

## 🧪 Test 3: Fallback Path (Poor Text Extraction)

**Purpose:** Verify Chunk 2 still downloads when extraction fails

### Setup

Use a **scanned PDF** with poor text extraction (if available)

### Steps

1. [ ] Send email with scanned PDF attachment
2. [ ] Wait 2-3 minutes
3. [ ] Check executions

### Expected Results

- [ ] ✅ Pre-Chunk 0 execution SUCCESS
- [ ] ✅ "Evaluate Extraction Quality" detects poor quality
  - `needsOCR`: true
  - `extractionQuality`: "poor"
  - `wordCount`: < 10
- [ ] ✅ "Prepare for Chunk 2" output has:
  - `extractedText`: (empty or very short)
  - `textLength`: < 100
  - `skipDownload`: **false**
- [ ] ✅ Chunk 2 downloads file (download node executes)
- [ ] ✅ Chunk 2 processes file successfully

### Success Criteria

✅ **PASS** if Chunk 2 downloads file when `skipDownload: false`
❌ **FAIL** if Chunk 2 skips download when text is missing

---

## 🔍 Debugging Tips

### If Test 1 or Test 2 Fails

**Check Pre-Chunk 0 Execution:**
```bash
# Get recent executions
curl -s "https://n8n.oloxa.ai/api/v1/executions?workflowId=YGXWjWcBIk66ArvT&limit=1" \
  -H "X-N8N-API-KEY: [API_KEY]"

# Get execution details (replace [EXECUTION_ID])
curl -s "https://n8n.oloxa.ai/api/v1/executions/[EXECUTION_ID]" \
  -H "X-N8N-API-KEY: [API_KEY]" | jq '.data'
```

**Check Chunk 2 Execution:**
```bash
# Get recent executions
curl -s "https://n8n.oloxa.ai/api/v1/executions?workflowId=g9J5kjVtqaF9GLyc&limit=1" \
  -H "X-N8N-API-KEY: [API_KEY]"

# Get execution details
curl -s "https://n8n.oloxa.ai/api/v1/executions/[EXECUTION_ID]" \
  -H "X-N8N-API-KEY: [API_KEY]" | jq '.data'
```

**Common Issues:**

1. **404 error still appears:**
   - Check if `skipDownload` is actually `true` in Chunk 2 input
   - Check if Chunk 2's "Normalize Input" is detecting the flag
   - Verify Chunk 2 has skip-download logic implemented

2. **Missing extractedText:**
   - Check "Evaluate Extraction Quality" node output
   - Verify "Prepare for Chunk 2" nodes are retrieving from correct node

3. **skipDownload is false when it should be true:**
   - Check `textLength` value (must be > 100)
   - Check if extraction actually succeeded in Pre-Chunk 0

---

## 📊 Success Metrics

**After testing, the system should achieve:**

- ✅ 0 "404 NOT FOUND" errors in Chunk 2
- ✅ 100% success rate for Pre-Chunk 0 → Chunk 2 flow
- ✅ Download node skipped in 90%+ of cases (only scanned PDFs need download)
- ✅ Faster execution time (no redundant downloads)

---

## 📝 Test Results

### Test 1 (EXISTING Client)
- Date/Time: _______________
- Status: [ ] PASS  [ ] FAIL
- Notes: ________________________________

### Test 2 (NEW Client)
- Date/Time: _______________
- Status: [ ] PASS  [ ] FAIL
- Notes: ________________________________

### Test 3 (Fallback)
- Date/Time: _______________
- Status: [ ] PASS  [ ] FAIL
- Notes: ________________________________

---

## ✅ Final Approval

- [ ] All tests passed
- [ ] No 404 errors observed
- [ ] System ready for production use
- [ ] Ready to build Chunks 2.5-5

**Signed off by:** _______________
**Date:** _______________

---

**Full Fix Report:** `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/v6_phase1/PRE_CHUNK_0_FIX_REPORT_2026-01-08.md`
