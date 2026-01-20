# Lombok Invest Capital - Property Scraper Automation
## Complete Handover Documentation

**Created:** January 15, 2026
**Client:** Benito (Lombok Invest Capital)
**System Status:** ✅ Fully Operational - Automated Bi-Weekly Runs

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Account Access & Credentials](#account-access--credentials)
3. [How the Automation Works](#how-the-automation-works)
4. [Quick Start Guide](#quick-start-guide)
5. [Configuration Details](#configuration-details)
6. [Google Sheets Reference](#google-sheets-reference)
7. [Troubleshooting](#troubleshooting)
8. [Maintenance & Monitoring](#maintenance--monitoring)
9. [Contact & Support](#contact--support)

---

## 🎯 System Overview

### What This Automation Does

Your property scraper automation runs **automatically every 2 weeks** (on the 1st and 15th of each month) and:

1. **Scrapes 10 property websites** in Lombok for new listings
2. **Filters properties** to show only:
   - ✅ Completed/built properties (ready to move in)
   - ✅ Located in Kuta or Selong
   - ✅ Freehold or Leasehold ownership
   - ❌ Excludes: Off-plan, under construction, or properties in other locations
3. **Removes duplicates** - Only shows properties you haven't seen before
4. **Sends email notification** with new properties found
5. **Updates Google Sheets** with all data for your review

### Next Scheduled Run

**Next run:** February 1, 2026 at 2:00 AM (Jakarta time)
**Following run:** February 15, 2026 at 2:00 AM (Jakarta time)

The system will continue running automatically on the 1st and 15th of every month.

---

## 🔐 Account Access & Credentials

### Master Gmail Account

**Email:** lombokinvestcapitalnow@gmail.com
**Password:** [Provided separately by Sway]

**This account is used for:**
- Gmail notifications (receiving scraped property emails)
- Google Sheets storage (all property data)
- Google Cloud Platform (OAuth for Make.com integrations)

**Important:** This is your central account - all other services connect through it.

---

### Apify Account (Web Scraper)

**Login URL:** https://console.apify.com
**Email:** lombokinvestcapitalnow@gmail.com
**Password:** [Provided separately]

**What it does:** Runs the web scraping tasks on property websites

**Your Apify Tasks:**
- **Task 1:** Scrapes 4 primary Lombok property sites (~20 properties)
- **Task 2:** Scrapes 4 mixed sites with Bali filtering (~45 properties)
- **Task 3:** Scrapes 2 international sites (~20 properties)

**Cron Schedules (Auto-run every 2 weeks):**
- Task 1: `0 2 1,15 * *` (2:00 AM on 1st & 15th)
- Task 2: `0 3 1,15 * *` (3:00 AM on 1st & 15th)
- Task 3: `0 4 1,15 * *` (4:00 AM on 1st & 15th)

**Status:** ✅ Schedules enabled - Next run February 1, 2026

---

### Make.com Account (Automation Workflow)

**Login URL:** https://www.make.com/en/login
**Email:** lombokinvestcapitalnow@gmail.com
**Password:** [Provided separately]

**What it does:** Receives scraped data, filters it, removes duplicates, and sends you email notifications

**Your Make.com Scenario:**
- **Name:** "Lombok Invest Capital Property Scraper v7"
- **Trigger:** Webhook (receives data from Apify Task 3 completion)
- **Processing:** Filters, deduplicates, formats data
- **Output:** Email + Google Sheets update

**Status:** ✅ Active and configured

---

### Google Cloud Platform (OAuth App)

**Login URL:** https://console.cloud.google.com
**Email:** lombokinvestcapitalnow@gmail.com
**Password:** [Same as Gmail]

**What it does:** Allows Make.com to access your Google Sheets without re-authenticating every 7 days

**OAuth App Details:**
- **App Name:** Lombok Invest Capital Property Scraper
- **Status:** ✅ Published to Production (no 7-day re-auth required)
- **Scopes:** Google Sheets API, Google Drive API

**Client ID:** [Provided separately]
**Client Secret:** [Provided separately]

**Important:** This is already configured in Make.com. You only need these credentials if you need to reconnect.

---

## ⚙️ How the Automation Works

### Complete Workflow Diagram

```
Every 2 weeks (1st & 15th of month)
         │
         ▼
┌─────────────────────────────────────┐
│  APIFY SCRAPING (Sequential)        │
│                                      │
│  2:00 AM → Task 1 runs (48 min)     │
│            ├─ Reef Property Lombok  │
│            ├─ Island Properties     │
│            ├─ Discover Lombok       │
│            └─ Nour Estates          │
│                                      │
│  3:00 AM → Task 2 runs (15 min)     │
│            ├─ Bali Exception        │
│            ├─ Estate Lombok         │
│            ├─ South Lombok Land     │
│            └─ Maju Properties       │
│                                      │
│  4:00 AM → Task 3 runs (9 min)      │
│            ├─ Bali Home Immo        │
│            └─ Invest Lombok         │
│                                      │
│  Task 3 completes → Sends webhook   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  MAKE.COM PROCESSING                │
│                                      │
│  1. Receives webhook from Task 3    │
│  2. Fetches Task 1 latest dataset   │
│  3. Fetches Task 2 latest dataset   │
│  4. Fetches Task 3 latest dataset   │
│  5. Combines all data (~85 props)   │
│  6. Filters:                         │
│     ✅ Kuta or Selong only          │
│     ✅ Completed/built only         │
│     ✅ Freehold or Leasehold        │
│     ❌ No off-plan/construction     │
│  7. Checks Data Store for duplicates│
│  8. Keeps only NEW properties       │
│  9. Updates Google Sheets           │
│ 10. Sends email notification        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  YOU RECEIVE                         │
│                                      │
│  📧 Email: "X new properties found" │
│  📊 Google Sheet updated with data  │
└─────────────────────────────────────┘
```

### What Each Component Does

**Apify (Scraping Layer):**
- Visits each property website
- Extracts property details (title, price, location, ownership, status)
- Detects construction status ("Built", "Off-Plan", "Under Construction")
- Saves results to datasets (one per task)

**Make.com (Processing Layer):**
- Receives completion notification from Apify
- Fetches all 3 datasets
- Applies your filters (location, ownership, construction status)
- Removes properties you've already seen (using Data Store)
- Formats data nicely
- Sends you an email + updates Google Sheets

**Google Sheets (Storage Layer):**
- **Raw Data Sheet:** All properties from all websites (before filtering)
- **Filtered Data Sheet:** Only properties matching your criteria
- **Data Store:** Invisible database tracking which properties you've seen

---

## 🚀 Quick Start Guide

### For First-Time Use

If this is your first time accessing the system:

1. **Check Your Email**
   - Look for emails from `notifications@make.com`
   - Subject: "New Lombok Properties Found - [Date]"
   - Opens to a formatted list of properties

2. **Review Google Sheets**
   - **Raw Data Sheet:** https://docs.google.com/spreadsheets/d/1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54/edit
   - **Filtered Data Sheet:** https://docs.google.com/spreadsheets/d/1Ksmb1UMBzruLc_arwWKe7uph1Sx84BFPG55Mi41jR1k/edit
   - **Error Log Sheet:** https://docs.google.com/spreadsheets/d/1mAh4jU9Tky5hfdSg0-uY_oyIwo7sPNgAXmuCSBuwZcA/edit

3. **Monitor Apify (Optional)**
   - Login to https://console.apify.com
   - Check **"Runs"** to see scraping history
   - Verify all 3 tasks completed successfully

4. **Monitor Make.com (Optional)**
   - Login to https://www.make.com
   - Open your scenario: "Lombok Invest Capital Property Scraper v7"
   - Click **"History"** to see execution logs

### Regular Use

**What you need to do:** Nothing! The system runs automatically.

**How to check if it's working:**
1. After the 1st or 15th of each month, check your email for new properties
2. If you receive "0 new properties found" - that's normal (no new listings)
3. If you receive "X new properties found" - open the email to review

**When to take action:**
- If you **don't receive an email** after the 1st or 15th → Check troubleshooting section
- If properties seem **incorrect or off-plan** → Check filtering configuration

---

## 🔧 Configuration Details

### Apify Task IDs

**Task 1 Dataset ID:** `a9zcGM6bQZbNLS9nf`
**Task 2 Dataset ID:** `R5FWB04ujtigD8Mo7`
**Task 3 Dataset ID:** `6kCy5ZnpavOkAxTjR`

**Note:** These IDs are used by Make.com to fetch the latest scraped data. They don't change unless you delete and recreate the Apify tasks.

### Make.com Variable Configuration

The Make.com scenario has a **"Set Variables"** module (Module 524) that stores all configuration:

| Variable | Value | Description |
|----------|-------|-------------|
| `userEmail` | lombokinvestcapitalnow@gmail.com | Your email |
| `notificationEmail` | lombokinvestcapitalnow@gmail.com | Where notifications are sent |
| `raw_spreadsheet_Id` | 1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54 | Raw data Google Sheet |
| `filter_spreadsheet_id` | 1Ksmb1UMBzruLc_arwWKe7uph1Sx84BFPG55Mi41jR1k | Filtered data Google Sheet |
| `error_log_spreadsheet_id` | 1mAh4jU9Tky5hfdSg0-uY_oyIwo7sPNgAXmuCSBuwZcA | Error log Google Sheet |
| `dataStoreId` | 87067 | Duplicate tracking database |
| `workflowName` | Lombok Property Scraper | Name shown in notifications |

**To update these:**
1. Login to Make.com
2. Open your scenario
3. Click on the "Set Variables" module (Module 524)
4. Edit the values
5. Click "OK" → "Save" scenario

### Filtering Logic

**Properties are INCLUDED if:**
- ✅ Location contains "Kuta" OR "Selong"
- ✅ Construction status is "Completed" OR "Built"
- ✅ Ownership is "Freehold" OR "Leasehold" (or contains "HGB")
- ✅ NOT previously seen (checked against Data Store)

**Properties are EXCLUDED if:**
- ❌ Location is NOT Kuta or Selong (e.g., Bali, Senggigi, other areas)
- ❌ Construction status is "Off-Plan" OR "Under Construction" OR "In Progress"
- ❌ Already seen in a previous run (duplicate)

### Websites Being Scraped

| Website | URL | Task | Properties |
|---------|-----|------|------------|
| Reef Property Lombok | reefpropertylombok.com | Task 1 | ~5 |
| Island Properties Lombok | islandpropertylombok.com | Task 1 | ~4 |
| Discover Lombok Property | discoverlombokproperty.com | Task 1 | ~6 |
| Nour Estates | nourestates.com | Task 1 | ~5 |
| Bali Exception | baliexception.com | Task 2 | ~10 |
| Estate Lombok | estate-lombok.com | Task 2 | ~12 |
| South Lombok Land Sales | southlomboklandsales.com | Task 2 | ~8 |
| Maju Properties | majuproperties.com | Task 2 | ~15 |
| Bali Home Immo | bali-home-immo.com | Task 3 | ~13 |
| Invest Lombok | invest-lombok.com | Task 3 | ~7 |
| **TOTAL** | | | **~85 properties** |

---

## 📊 Google Sheets Reference

### Sheet Structure

Your automation uses **3 separate Google Sheets:**

#### 1. Raw Data Sheet
**URL:** https://docs.google.com/spreadsheets/d/1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54/edit

**Contains:** All properties scraped from all websites (before filtering)

**Columns:**
- **Property Title:** Name of the property
- **URL:** Direct link to property listing
- **Price (Raw):** Original price as shown on website
- **Price (Normalized USD):** Converted to USD for comparison
- **Location:** City/area (Kuta, Selong, Bali, etc.)
- **Ownership:** Freehold, Leasehold, HGB
- **Property Type:** Villa, House, Land, etc.
- **Construction Status:** Completed, Off-Plan, Under Construction, Unknown
- **Year Built:** Year property was built (if available)
- **Source Website:** Which website it came from
- **Scraped At:** Date/time when data was collected

**Use this tab to:**
- See ALL properties regardless of filters
- Review pricing trends across all locations
- Check what's being scraped from each website

---

#### 2. Filtered Data Sheet
**URL:** https://docs.google.com/spreadsheets/d/1Ksmb1UMBzruLc_arwWKe7uph1Sx84BFPG55Mi41jR1k/edit

**Contains:** Only properties matching your criteria (Kuta/Selong, Completed, Freehold/Leasehold)

**Columns:** Same as Raw Data Sheet

**Use this tab to:**
- Review properties you should actually consider
- See only investment-ready properties
- Track new opportunities

---

#### 3. Error Log Sheet
**URL:** https://docs.google.com/spreadsheets/d/1mAh4jU9Tky5hfdSg0-uY_oyIwo7sPNgAXmuCSBuwZcA/edit

**Contains:** Errors and issues encountered during scraping or processing

**Columns:**
- **Timestamp:** When the error occurred
- **Error Type:** Type of error (scraping, filtering, data processing)
- **Error Message:** Detailed error description
- **Property URL:** URL that caused the error (if applicable)
- **Source Website:** Which website was being scraped
- **Resolution Status:** Fixed, pending, or ignored

**Use this sheet to:**
- Monitor system health
- Identify problematic websites or properties
- Track recurring issues
- Provide error details when contacting support

**Note:** Most errors are minor and automatically handled by the system. Only contact support if you see the same error repeatedly.

---

### How to Use the Sheets

**After each automation run:**

1. **Start with the Filtered Data Sheet**
   - Open: https://docs.google.com/spreadsheets/d/1Ksmb1UMBzruLc_arwWKe7uph1Sx84BFPG55Mi41jR1k/edit
   - Look for new rows at the bottom (sorted by date)
   - Review each property:
     - Check price vs. comparable properties
     - Click URL to see full listing
     - Note any that interest you

2. **Review Raw Data (optional)**
   - Open: https://docs.google.com/spreadsheets/d/1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54/edit
   - See ALL properties (including off-plan, other locations)
   - Use Google Sheets filters to explore different areas/types

3. **Check Error Log (if needed)**
   - Open: https://docs.google.com/spreadsheets/d/1mAh4jU9Tky5hfdSg0-uY_oyIwo7sPNgAXmuCSBuwZcA/edit
   - Review any errors or issues
   - Most errors are handled automatically

**Pro tip:** Add a column called "My Notes" or "Status" to track which properties you've contacted about or visited.

---

## 🔍 Troubleshooting

### Problem: No Email Received After Scheduled Run

**Check these in order:**

1. **Check your spam folder**
   - Emails come from `notifications@make.com`
   - Mark as "Not Spam" if found

2. **Verify Apify tasks ran successfully:**
   - Login to https://console.apify.com
   - Click **"Runs"** in left sidebar
   - Look for runs on the 1st or 15th of the month
   - All 3 tasks should show "Succeeded" status
   - **If failed:** Click on the run → Check error message → See "Apify Errors" section below

3. **Verify Make.com scenario executed:**
   - Login to https://www.make.com
   - Open your scenario
   - Click **"History"** tab
   - Look for execution on the date
   - **If no execution:** Webhook may not have fired → See "Webhook Issues" section below
   - **If execution shows errors:** Click on it → See which module failed → See "Make.com Errors" section below

4. **Check if 0 new properties were found:**
   - Sometimes all properties are duplicates (already seen)
   - Email may say "0 new properties found" or not be sent at all
   - This is normal - it means no NEW listings appeared

---

### Problem: Properties Showing "Off-Plan" or "Under Construction" in Results

**This shouldn't happen** - filtering should exclude these.

**To fix:**

1. Login to Make.com → Open your scenario
2. Find the **"Filter Module"** (usually around Module 527-530)
3. Verify the filter condition includes:
   ```
   Construction Status NOT EQUAL TO "Off-Plan"
   AND
   Construction Status NOT EQUAL TO "Under Construction"
   AND
   Construction Status NOT EQUAL TO "In Progress"
   ```
4. If missing → Edit the filter → Add these conditions → Save scenario

**If problem persists:**
- Check the **Raw Data Sheet** → See if construction status is being detected correctly
- Some websites may use different terminology (e.g., "Pre-construction", "Being built")
- Contact Sway for filter updates

---

### Problem: Apify Tasks Failing

**Common Apify errors:**

#### Error: "Page timeout"
**Cause:** Website took too long to load
**Fix:** Apify will automatically retry. If it keeps failing:
1. Login to Apify → Open the failed task
2. Click **"Run"** to manually re-run
3. If still fails → Website may be down temporarily

#### Error: "Maximum retries exceeded"
**Cause:** Website blocking the scraper
**Fix:**
1. Wait 24 hours (website may have temporary rate limits)
2. Try running again manually
3. If persists → Contact Sway for proxy configuration

#### Error: "No data extracted"
**Cause:** Website changed its structure
**Fix:** This requires code updates. Contact Sway immediately.

---

### Problem: Webhook Not Triggering Make.com

**Symptoms:**
- Apify tasks run successfully
- But Make.com scenario doesn't execute
- No email received

**To diagnose:**

1. **Check Apify Task 3 webhook configuration:**
   - Login to Apify → Go to Task 3
   - Click **Settings** → **"Post-run webhook"**
   - Verify webhook URL is set (should look like `https://hook.make.com/...`)
   - If missing or wrong → Contact Sway for correct URL

2. **Check Make.com webhook module:**
   - Login to Make.com → Open scenario
   - First module should be "Webhook"
   - Click on it → Copy the webhook URL
   - Compare to Apify Task 3 webhook URL
   - If different → Update Apify with correct URL

---

### Problem: Google Sheets Not Updating

**Check these:**

1. **Verify Make.com execution succeeded:**
   - Login to Make.com → Scenario History
   - If execution failed at a Google Sheets module → Connection may have expired

2. **Reconnect Google Sheets:**
   - Open your scenario
   - Find any Google Sheets module (e.g., "Add a Row")
   - Click on it
   - Click **"Account"** field → **"Reconnect"**
   - Authorize with lombokinvestcapitalnow@gmail.com
   - Save scenario

3. **Check spreadsheet ID:**
   - Make sure Variables module (524) has the correct spreadsheet ID
   - Verify the spreadsheet still exists and you have edit access

---

### Problem: Receiving Duplicate Properties

**Symptoms:**
- Same property appears in multiple emails
- Properties you've seen before keep showing up

**Cause:** Data Store may have been cleared or corrupted

**To fix:**

1. Login to Make.com
2. Go to **Data stores** in left sidebar
3. Find your data store: **ID 87067** (named "lombok-properties")
4. Or access directly: https://eu1.make.com/829332/data-stores/browse/87067
5. Check if it contains property URLs
6. **If empty:** It got cleared. The system will now re-learn which properties are duplicates.
7. **If you want to reset completely:**
   - Delete all entries in Data Store
   - Next run will treat all properties as "new"

---

## 🛠️ Maintenance & Monitoring

### Monthly Checks (Recommended)

**Do this once a month to ensure everything is working:**

1. **Review email notifications:**
   - Check that you received notifications on the 1st and 15th
   - Verify property count seems reasonable (~5-20 new properties per run)

2. **Check Apify usage:**
   - Login to Apify → Dashboard
   - Verify you're not hitting usage limits
   - Free tier: 100 actor runs/month (you use 6/month = well within limits)

3. **Check Make.com operations:**
   - Login to Make.com → Dashboard
   - Verify operations count is reasonable
   - Free tier: 1,000 operations/month (you use ~200/month = OK)

4. **Audit Google Sheets:**
   - Open your spreadsheet
   - Check row count (shouldn't exceed 10,000 rows)
   - If getting large → Archive old data or increase sheet size

---

### When to Contact Support

**Contact Sway if:**

- ❌ No emails received for 2+ consecutive runs (1st & 15th)
- ❌ Apify tasks consistently failing with errors
- ❌ Properties in results don't match filter criteria
- ❌ Website structure changed (no data being scraped)
- ❌ Google Sheets stops updating
- ❌ You want to change filter criteria (location, construction status, etc.)
- ❌ You want to add or remove websites from scraping list

**DON'T contact support for:**

- ✅ "0 new properties found" emails (this is normal)
- ✅ Occasional task failures (Apify auto-retries)
- ✅ One-time webhook miss (will resume next run)

---

### System Costs & Limits

**Apify (Free Tier):**
- **Limit:** 100 actor runs/month
- **Your usage:** 6 runs/month (3 tasks × 2 runs/month)
- **Status:** ✅ Well within limits

**Make.com (Free Tier):**
- **Limit:** 1,000 operations/month
- **Your usage:** ~200 operations/month (100 per run × 2 runs)
- **Status:** ✅ Well within limits

**Google Cloud Platform (OAuth):**
- **Cost:** Free (no API charges for Sheets/Drive)
- **Status:** ✅ No costs

**Total Monthly Cost:** $0 (all free tiers)

**Note:** If you need more frequent runs or add more websites, you may need to upgrade:
- Apify Pro: $49/month (unlimited runs)
- Make.com Pro: $9/month (10,000 operations)

---

## 📞 Contact & Support

### Primary Contact: Sway Clarke

**Email:** sway@oloxa.ai
**For:** Technical issues, changes to automation, adding websites, filter updates

**Response time:** Within 24-48 hours

---

### Platform Support Links

**Apify:**
- Documentation: https://docs.apify.com
- Support: support@apify.com
- Status page: https://status.apify.com

**Make.com:**
- Documentation: https://www.make.com/en/help
- Support: support@make.com
- Community forum: https://community.make.com

**Google Cloud Platform:**
- Documentation: https://cloud.google.com/docs
- Support: https://support.google.com/cloud

---

## 📚 Additional Resources

### Video Walkthrough

**URL:** https://drive.google.com/file/d/1T4CCjyLnsfOoNS7dVeBT3M5MHad6vrqO/view?usp=drive_link

**Covers:**
- How to access all accounts
- How to check if automation is working
- How to review Google Sheets
- Basic troubleshooting
- Step-by-step walkthrough of the complete system

---

### Configuration Files (Advanced)

If you need to recreate the automation or understand the technical details:

**Apify Actor Configurations:**
- Task 1 JSON: `/technical-builds/lombok-invest-capital/apify-configs/json/Lombok Invest Capital (Task 1) - v7 - Dec-17-2024.json`
- Task 2 JSON: `/technical-builds/lombok-invest-capital/apify-configs/json/Lombok Invest Capital (Task 2) 11_12_2025 - v4 - Dec-14-2024.json`
- Task 3 JSON: `/technical-builds/lombok-invest-capital/apify-configs/json/Lombok Invest Capital (Task 3) 11_12_2025 - v4 - Dec-14-2024.json`

**Make.com Blueprint:**
- File: `/technical-builds/lombok-invest-capital/make-blueprints/Lombok_Property_Scraper_v7_Blueprint.json`

**Technical Documentation:**
- Setup Guide: `APIFY_MAKE_SETUP_GUIDE.md`
- Technical Specs: `CLAUDE.md`
- Handover Checklist: `CLIENT_HANDOVER_CHECKLIST.md`

---

## ✅ Final Checklist

Before considering the handover complete, verify:

**Accounts:**
- [x] Gmail account accessible (lombokinvestcapitalnow@gmail.com)
- [x] Apify account accessible and tasks configured
- [x] Make.com account accessible and scenario active
- [x] Google Cloud Console OAuth app published to production

**Configuration:**
- [x] Apify cron schedules enabled (1st & 15th of month)
- [x] Make.com webhook configured and connected
- [x] Google Sheets created with correct structure
- [x] Email notifications working

**Testing:**
- [x] End-to-end test completed successfully
- [x] Received email notification with property data
- [x] Google Sheets updated correctly
- [x] Data Store tracking duplicates properly

**Documentation:**
- [x] All credentials provided securely
- [x] Video walkthrough recorded (https://drive.google.com/file/d/1T4CCjyLnsfOoNS7dVeBT3M5MHad6vrqO/view)
- [x] This handover document complete with all IDs and URLs
- [x] Client understands how to monitor and troubleshoot

---

## 🎉 You're All Set!

The automation is now fully operational and running on your behalf.

**Next steps:**
1. Wait for the next scheduled run (February 1, 2026)
2. Check your email for new property notifications
3. Review the Google Sheets for full data
4. Reach out to Sway if you have any questions

**Remember:** The system runs automatically. You don't need to do anything unless you want to check the results or make changes.

Happy property hunting! 🏡

---

**Document Version:** 1.0
**Last Updated:** January 15, 2026
**Created by:** Sway Clarke (Oloxa.ai)
**For:** Benito - Lombok Invest Capital
