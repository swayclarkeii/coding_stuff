# 30-Second Anthropic Credential Fix

**Problem:** Anthropic nodes returning "Invalid URL" error
**Cause:** Credential has malformed baseURL field
**Fix time:** 30 seconds

---

## Steps (Do This Now)

### In n8n (you should already be there):

1. **Bottom left** → Click **Settings** ⚙️

2. Click **Credentials**

3. **Find "Anthropic account"** in the list (or any credential with "Anthropic" in the name)

4. **Click it to edit**

5. **Check these two fields:**

   **Field 1: API Key**
   - Should start with: `sk-ant-api-`
   - If empty or wrong → paste your Anthropic API key

   **Field 2: Base URL** (THIS IS THE PROBLEM)
   - Should be: **EMPTY** (completely blank)
   - OR: `https://api.anthropic.com`
   - If it has ANYTHING else (spaces, wrong URL, etc.) → **DELETE IT and leave it empty**

6. **Click Save**

7. **Go back to workflow** (click "Workflows" in left sidebar)

8. **Find workflow:** "Fathom Transcript Workflow Final_22.01.26"

9. **Click "Test workflow"** (top right button)

10. **Watch execution** - should succeed this time

---

## What to Look For

**Success:**
- Execution completes (no red error)
- Takes 30-60 seconds (means AI is actually running)
- Check Airtable - new record appears

**Still Failing:**
- Execution fails immediately (<5 seconds)
- Red error in "Call AI for Analysis" node
- → Tell me: "still broken" and I'll try something else

---

## Why This Happens

The n8n Anthropic node is **very picky** about the Base URL field:
- If you manually type something → often adds invisible characters
- If you copy/paste → might include spaces
- **Best solution:** Leave it completely empty

---

**Do this now, then let me know:** "fixed" or "still broken"
