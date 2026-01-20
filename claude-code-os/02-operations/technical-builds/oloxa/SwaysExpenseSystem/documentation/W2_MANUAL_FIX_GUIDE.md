# W2 Manual Fix Guide - Updated Instructions

**Status**: W3, W4, and W6 are production-ready. W2 requires 2 manual fixes before activation.

---

## ✅ What's Already Done

- **W3 v2.1**: 0 errors - READY ✅
- **W6 v1.1**: 0 errors - READY ✅
- **W4 v2.1**: 2 false positive warnings (confirmed via screenshots) - READY ✅
- **Service Account Audit**: W1, W3, W4, W6 all use OAuth2 correctly ✅

**Total automated fixes**: 17 of 19 errors (89.5% success rate)

---

## ⚠️ What You Need to Do (W2 Only)

### Fix #1: Remove Old Error Handling Property (3 nodes)

**Why**: These nodes have BOTH the old `continueOnFail` property AND the new `onError` property. n8n validation rejects this as a conflict.

**Which nodes:**
1. Build Vision API Request (position [1720, -112])
2. Extract Text with Vision API (position [1900, -112])
3. Parse Amount from OCR Text (position [2080, -112])

**How to fix (for EACH of the 3 nodes):**

```
1. Open W2 workflow in n8n
2. Find the node (they're all in a horizontal line in bottom-right area)
3. Double-click the node to open it
4. Click the "Settings" tab at the top
5. Find the "On Error" dropdown (currently shows "Continue Regular Output")
6. Change it to "Stop And Return Error"
7. Click "Save"
8. Open the node again
9. Change "On Error" back to "Continue Regular Output"
10. Save again
```

**Why this works**: Toggling the dropdown removes the old `continueOnFail` property from the node configuration while keeping the correct `onError` setting.

**What you WON'T see**: There's no "Continue On Fail" toggle/checkbox in newer n8n versions. If you don't see it, that's correct - just follow the steps above.

---

### Fix #2: Create Google OAuth2 API Credential

**Why**: The "Extract Text with Vision API" node is configured to use "Google Service Account API" which you're no longer using. You need to create a "Google OAuth2 API" credential for the Vision API.

**Step 1: Create the Credential**

```
1. In n8n, click your profile icon (top-right) → Settings
2. Click "Credentials" in the left sidebar
3. Click "Create New Credential" button (top-right)
4. Search for "Google OAuth2 API"
5. Select "Google OAuth2 API" from the list
   (NOT Google Drive, NOT Google Sheets - just "Google OAuth2 API")
6. Name it: "Google Cloud Vision API"
7. Click "Connect My Account"
8. Sign in with your Google account in the OAuth popup
9. Grant all requested permissions (including Cloud Vision API scope)
10. Click "Save"
```

**Step 2: Assign Credential to the Node**

```
1. Go to W2 workflow
2. Open "Extract Text with Vision API" node
3. Under "Authentication", keep "Predefined Credential Type"
4. Under "Credential Type" dropdown, select "Google OAuth2 API"
5. Under the credential dropdown, select "Google Cloud Vision API"
6. Save the node
```

**Credential Type Reference:**
- ✅ **Google OAuth2 API** ← Select THIS one
- ❌ Google Drive OAuth2 API (wrong - only for Drive)
- ❌ Google Sheets OAuth2 API (wrong - only for Sheets)
- ❌ Google Service Account API (wrong - deprecated)

---

## 🎯 After You Complete These Fixes

Once you've done both fixes above (the 3-node error handling fix + the credential setup):

1. Let me know you're done
2. I'll re-test W2 to verify all 5 errors are resolved
3. I'll activate all 4 workflows (W2, W3, W4, W6)
4. I'll run a final integration test across the entire expense system

---

## 📊 Current Validation Status

| Workflow | Errors | Status | Action Needed |
|----------|--------|--------|---------------|
| W1 | 0 | ✅ Active | None |
| W2 | 5 | ❌ Waiting | **2 manual fixes (you)** |
| W3 | 0 | ✅ Ready | None (activate after W2) |
| W4 | 2 (false positives) | ✅ Ready | None (activate after W2) |
| W6 | 0 | ✅ Ready | None (activate after W2) |

---

## 🔍 Finding the Nodes in W2

All 3 nodes are in the bottom-right section of the workflow canvas:

```
[Gmail] → [Upload] → [Merge Apple & Regular]
                              ↓
                   Build Vision API Request ← FIX 1
                              ↓
               Extract Text with Vision API ← FIX 1 + FIX 2
                              ↓
                 Parse Amount from OCR Text ← FIX 1
                              ↓
                      [Prepare Receipt Record]
```

They're horizontally aligned at Y-coordinate -112.

---

## ❓ If You Get Stuck

**Can't find the "On Error" dropdown?**
- It's in the "Settings" tab (not "Parameters" tab)
- If you still can't find it, send me a screenshot

**OAuth popup not appearing?**
- Check for popup blockers
- Try a different browser
- Make sure you're signed into your Google account

**Not sure which credential type?**
- You want "Google OAuth2 API" (generic Google API credential)
- NOT the specialized ones (Drive, Sheets, Calendar)

---

**Updated**: 2026-01-10
**Detailed documentation**: `/Users/swayclarke/coding_stuff/READY_FOR_MANUAL_FIXES.md`
