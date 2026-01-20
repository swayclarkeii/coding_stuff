# Apify + Make.com Integration Setup Guide
## Lombok Property Scraper Automation

**Date:** 2026-01-08
**For:** Client handover preparation

---

## Current State Analysis

**Your v6 Blueprint Currently:**
- ❌ Does NOT trigger Apify actors automatically
- ✅ Only FETCHES data from existing datasets:
  - Task 1 Dataset: `a9zcGM6bQZbNLS9nf`
  - Task 2 Dataset: `R5FWB04ujtigD8Mo7`
  - Task 3 Dataset: `6kCy5ZnpavOkAxTjR`

**Problem:** You must manually run the Apify actors, then Make.com pulls the results.

**Solution:** Automate the entire flow so Make.com triggers the Apify actors every 2 weeks.

---

## Comparison: Two Approaches

| Feature | **Option 1: Make → Apify** | **Option 2: Apify → Make** |
|---------|----------------------------|---------------------------|
| **Complexity** | ⭐ Simple | ⭐⭐⭐ Complex |
| **Setup Time** | 30 minutes | 2+ hours |
| **Control Point** | Make.com (1 schedule) | Apify (3 schedules) |
| **Coordination** | Sequential (reliable) | Parallel (risky) |
| **Client Handover** | Easier | Harder |
| **Debugging** | Easier (see all in Make) | Harder (split logs) |
| **Recommendation** | ✅ **USE THIS** | ❌ Avoid |

---

## OPTION 1: Make.com Triggers Apify (RECOMMENDED)

### Architecture Flow

```
┌─────────────────┐
│  Make.com       │  Runs every 2 weeks
│  Scheduler      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Set Variables  │  Module 524
└────────┬────────┘
         │
         ├──────────────────┬──────────────────┐
         ▼                  ▼                  ▼
    ┌────────┐         ┌────────┐         ┌────────┐
    │ Run    │         │ Run    │         │ Run    │
    │ Task 1 │         │ Task 2 │         │ Task 3 │
    │ Actor  │         │ Actor  │         │ Actor  │
    └───┬────┘         └───┬────┘         └───┬────┘
        │                  │                  │
        │ (Apify scrapes)  │ (Apify scrapes)  │ (Apify scrapes)
        │ (Saves to        │ (Saves to        │ (Saves to
        │  dataset)        │  dataset)        │  dataset)
        │                  │                  │
        ▼                  ▼                  ▼
    ┌────────┐         ┌────────┐         ┌────────┐
    │ Fetch  │         │ Fetch  │         │ Fetch  │
    │ Task 1 │         │ Task 2 │         │ Task 3 │
    │ Data   │         │ Data   │         │ Data   │
    └───┬────┘         └───┬────┘         └───┬────┘
        │                  │                  │
        └──────────────────┴──────────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │  Process &     │
                  │  Email Results │
                  └────────────────┘
```

---

## PART A: Setting Up Your Test Account (Current)

### Step 1: Configure Apify Actors (One-Time Setup)

#### 1.1 Access Apify Console
1. Go to [https://console.apify.com](https://console.apify.com)
2. Log in with your account
3. Navigate to **Actors** in left sidebar

#### 1.2 Identify Your Actors
You need to know the **Actor IDs** or **Actor Names** for your 3 tasks:
- **Task 1**: (e.g., `apify/web-scraper` or custom actor)
- **Task 2**: (e.g., `apify/web-scraper` or custom actor)
- **Task 3**: (e.g., `apify/web-scraper` or custom actor)

**To find Actor ID:**
1. Click on the actor you're using
2. Look at the URL: `https://console.apify.com/actors/ACTOR_ID_HERE`
3. Or find it under **Settings → General → Actor ID**

#### 1.3 Export Actor Input Configurations

For **each** of your 3 tasks:

1. Go to the Actor page in Apify console
2. Click on **"Input"** tab (or "Last run" to see previous config)
3. You'll see the JSON configuration, for example:
   ```json
   {
     "startUrls": [
       {
         "url": "https://www.bali-home-immo.com/realestate-property?keyword=Lombok"
       }
     ],
     "pageFunction": "...",
     "proxyConfiguration": {...},
     "maxConcurrency": 10,
     ...
   }
   ```
4. **Copy the ENTIRE JSON** → Save to a file:
   - `task1_actor_input.json`
   - `task2_actor_input.json`
   - `task3_actor_input.json`

**Why:** You'll need this exact configuration for the client's account.

#### 1.4 Note Dataset Behavior

**Important Understanding:**
- When Apify actors run, they create/update a **"Default dataset"** automatically
- You can configure actors to use a **specific named dataset** (stays consistent)
- Your current setup uses specific dataset IDs (which is fine but static)

**Two approaches for datasets:**

**Approach A: Use Default Datasets (Recommended for client handover)**
- Pro: No dataset ID configuration needed
- Pro: Actor automatically manages it
- Con: Dataset ID changes if you delete/recreate actor

**Approach B: Use Named Datasets (Current approach)**
- Pro: Dataset ID stays consistent
- Con: Requires manual dataset creation and ID configuration

**Decision Point:** For easier client handover, I recommend **switching to default datasets**.

---

### Step 2: Update Make.com Scenario (Add "Run Actor" Modules)

#### 2.1 Access Make.com Scenario Editor
1. Go to Make.com
2. Open your **"Lombok invest capital Property Scraper v6"** scenario
3. You'll be modifying the flow

#### 2.2 Add "Run Actor" Module BEFORE Each "Fetch" Module

**Current structure (Router with 3 paths):**
```
Router
  ├─ Route 0: Fetch Task 1 Data → Process
  ├─ Route 1: Fetch Task 2 Data → Process
  └─ Route 2: Fetch Task 3 Data → Process
```

**New structure needed:**
```
Router
  ├─ Route 0: RUN Task 1 Actor → Fetch Task 1 Data → Process
  ├─ Route 1: RUN Task 2 Actor → Fetch Task 2 Data → Process
  └─ Route 2: RUN Task 3 Actor → Fetch Task 3 Data → Process
```

#### 2.3 Configure "Run Actor" Module for Task 1

1. **Click on the router path** for Task 1
2. **Add new module BEFORE** "Get Task 1 Results"
3. **Search for** "Apify"
4. **Select** "Run an Actor" or "Run a Task" module
5. **Configure**:

   **Connection:** Select your existing Apify connection (or create new)

   **Actor ID:** Enter the actor ID from Step 1.2 (e.g., `apify/web-scraper`)

   **Actor Input:** Click "Switch to JSON" and paste your `task1_actor_input.json` content

   **Build:** Select "latest" (or specific version if you have one)

   **Timeout:** 300 (seconds) - adjust based on scraping duration

   **Wait for finish:** YES (toggle ON) ← **CRITICAL**

   **Dataset:** Leave empty to use default dataset

6. **Save** the module

#### 2.4 Update "Fetch Dataset" Module for Task 1

**After adding Run Actor module:**

1. Click on your existing **"Get Task 1 Results"** (Fetch Dataset Items) module
2. **Change Dataset ID mapping**:

   **OLD (hardcoded):**
   ```
   Dataset ID: a9zcGM6bQZbNLS9nf
   ```

   **NEW (dynamic from Run Actor output):**
   ```
   Dataset ID: {{[ID of Run Actor module].defaultDatasetId}}
   ```

   Example: If Run Actor module is ID 525, use:
   ```
   Dataset ID: {{525.defaultDatasetId}}
   ```

3. **Save** the module

#### 2.5 Repeat for Task 2 and Task 3

**For Task 2:**
- Add "Run Actor" module in Route 1
- Configure with `task2_actor_input.json`
- Update Fetch module to use `{{[Run Actor ID].defaultDatasetId}}`

**For Task 3:**
- Add "Run Actor" module in Route 2
- Configure with `task3_actor_input.json`
- Update Fetch module to use `{{[Run Actor ID].defaultDatasetId}}`

#### 2.6 Set Make.com Schedule

1. **At the bottom of the scenario** (where you are in the screenshot):
2. Click the **⏰ Schedule dropdown** (currently shows "Every 15 minutes")
3. Select **"Custom"**
4. Configure:
   - **Frequency:** Every 2 weeks
   - **Day:** Select specific day (e.g., Monday)
   - **Time:** Select time (e.g., 9:00 AM)
   - **Timezone:** Your timezone
5. **Toggle the schedule ON**
6. **Save scenario**

#### 2.7 Test the Flow

1. **Turn OFF the schedule temporarily** (toggle to OFF)
2. Click **"Run once"** button
3. **Watch the execution**:
   - Each "Run Actor" module should trigger Apify
   - Apify will scrape (may take 5-10 minutes)
   - "Fetch Dataset" modules retrieve results
   - Data processes and email sends
4. **Check for errors** in Make.com execution log
5. **Verify email** was received with correct data
6. If successful → **Turn schedule back ON**

---

## PART B: Client Account Setup (Future Handover)

### Step 3: Prepare for Client Migration

#### 3.1 What You Need from Client

Before you can set up the client's account, collect:

1. **Apify Account:**
   - Apify account email/username
   - Access to their Apify console (they can add you as team member)
   - OR they create account and give you credentials

2. **Make.com Account:**
   - Make.com account email/username
   - Access to their Make.com organization (invite you as team member)
   - OR they create account and give you credentials

3. **Google Account for Spreadsheets/Email:**
   - Gmail address for notifications
   - Access to create Google Sheets in their account

#### 3.2 Migration Checklist (Do NOT do this yet!)

**When client is ready, follow this sequence:**

---

### Step 4: Migrate to Client's Apify Account

#### 4.1 Create Actors in Client's Apify

For **each** of the 3 tasks:

1. **Log into client's Apify console**: [https://console.apify.com](https://console.apify.com)

2. **Create Actor/Task:**
   - If using public actors (e.g., `apify/web-scraper`):
     - Navigate to **Actors → Public actors**
     - Search for the actor you used
     - Click **"Create task"** or just note the Actor ID

   - If using custom actors:
     - You'll need to recreate/import the custom actor code
     - Contact Apify support for actor migration assistance

3. **Configure Actor Input:**
   - Open the actor/task
   - Go to **Input** tab
   - Click **"JSON"** mode
   - Paste your saved JSON from `task1_actor_input.json`
   - Adjust any account-specific values (e.g., URLs, login credentials if any)
   - Click **"Save"**

4. **Run a Test:**
   - Click **"Run"** to test the actor
   - Wait for completion
   - Verify the data is correct
   - **Note the Dataset ID** that was created (you'll see it in results)

5. **Repeat** for Task 2 and Task 3

#### 4.2 Get Client's Apify API Token

1. In client's Apify console → **Settings → Integrations**
2. Copy the **API Token**
3. Save securely (you'll need this for Make.com connection)

---

### Step 5: Migrate to Client's Make.com Account

#### 5.1 Export Your v6 Blueprint

From YOUR Make.com account:

1. Open your **"Lombok invest capital Property Scraper v6"** scenario
2. Click the **"..."** menu (top right)
3. Select **"Download Blueprint"**
4. Save as: `lombok_blueprint_for_client.json`

#### 5.2 Update Blueprint JSON Before Import

**You MUST update these values in the JSON before giving to client:**

1. **Open** `lombok_blueprint_for_client.json` in a text editor

2. **Find and replace** the following:

   **Apify Connection (will need to be recreated):**
   - Client will need to create their own Apify connection in Make.com
   - Connection IDs will be different, so this will show errors on import (expected)

   **Dataset IDs** (if using static datasets):
   - If you're using the dynamic approach (recommended), this won't matter
   - If using static: Replace old dataset IDs with new ones from Step 4.1

   **Emails:**
   - Already using variable `{{524.notificationEmail}}` ✅
   - Client will update this in the Variables module

   **Spreadsheet IDs:**
   - Already using variables `{{524.raw_spreadsheet_Id}}` ✅
   - Client will update in Variables module

   **Data Store ID:**
   - Currently hardcoded as `81942` in 17 places ❌
   - Either: Keep as is and have client create data store with same structure
   - OR: Use v7 which uses variable `{{524.dataStoreId}}`

3. **Save** the updated JSON

#### 5.3 Import Blueprint to Client's Make.com

In CLIENT'S Make.com account:

1. Navigate to **Scenarios**
2. Click **"Create a new scenario"**
3. Click **"..."** menu (top right)
4. Select **"Import Blueprint"**
5. **Upload** your `lombok_blueprint_for_client.json`
6. Click **"Import"**

**Expected Warnings:**
- ⚠️ "Connection not found" for Apify → You'll reconnect in next step
- ⚠️ "Connection not found" for Gmail → You'll reconnect
- ⚠️ "Data store not found" → You'll create/select in client's account

#### 5.4 Reconnect Apify Connection

1. **Find any Apify module** in the imported scenario (e.g., "Run Actor" module)
2. Click on it → You'll see **"Connection" field with error**
3. Click **"Add"** to create new connection
4. **Enter client's Apify API Token** (from Step 4.2)
5. **Save**
6. Make.com will ask: **"Update all modules with this connection?"** → Click **YES**
7. All Apify modules now use client's connection ✅

#### 5.5 Update Variables Module (524)

1. **Find the "Set Variables" module** (ID 524 or similar)
2. **Update these values**:
   - `userEmail`: Client's email
   - `notificationEmail`: Client's notification email
   - `raw_spreadsheet_Id`: New Google Sheet ID (create in client's account)
   - `filter_spreadsheet_id`: New filter sheet ID (if applicable)
   - `dataStoreId`: Client's data store ID (create below)
   - `workflowName`: Can keep or rename

#### 5.6 Create Data Store in Client's Account

1. In Make.com left sidebar → **Data stores**
2. Click **"Add data store"**
3. **Name**: "lombok-properties" (or similar)
4. **Data structure**:
   ```
   Key (Text)
   Value (Text or Number)
   ```
5. Click **"Save"**
6. **Copy the Data Store ID** (you'll see it in the list)
7. **Paste** into Variables module → `dataStoreId` field

**OR** if using v7 with variable references, it will automatically use `{{524.dataStoreId}}`

#### 5.7 Reconnect Gmail Connection

1. **Find the email module** (Module 515 "Send New Leads")
2. Click on it → **"Account" field** will show error
3. Click **"Add"** to create new Gmail connection
4. **Authorize** with client's Gmail account
5. **Save**
6. Update other email modules if any

#### 5.8 Create Google Sheets in Client's Account

**You need 2 Google Sheets:**

1. **Raw Data Sheet** (for all scraped properties):
   - Go to Google Sheets in client's account
   - Create new sheet: "Lombok Raw Properties"
   - **Copy the Spreadsheet ID** from URL:
     ```
     https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
     ```
   - Update in Variables module → `raw_spreadsheet_Id`

2. **Filtered Data Sheet** (for filtered properties):
   - Create another sheet: "Lombok Filtered Properties"
   - Copy Spreadsheet ID
   - Update in Variables module → `filter_spreadsheet_id`

**Set up Sheet Structure:**
- You'll need to replicate the column headers from your test sheets
- Recommended columns: Property Title, URL, Price, Location, Date Added, etc.
- Make.com modules expect specific column structure

#### 5.9 Update Google Sheets Modules

**For each "Add Row" or "Update Row" Google Sheets module:**

1. Click on the module
2. **Reconnect** to client's Google account (if not done automatically)
3. **Select the new Spreadsheet** from dropdown (or use variable)
4. **Verify column mappings** are correct
5. **Save**

#### 5.10 Test the Client's Scenario

1. **Turn OFF scheduling** (don't auto-run yet)
2. Click **"Run once"**
3. **Monitor execution**:
   - Check each module for errors
   - Verify Apify actors run successfully
   - Verify data appears in Google Sheets
   - Verify email is sent
4. **Fix any errors**:
   - Connection issues → Reconnect
   - Missing data → Check actor outputs
   - Sheet errors → Verify column structure
5. **Once successful** → Enable scheduling

#### 5.11 Set Client's Schedule

1. Bottom bar → **⏰ Schedule dropdown**
2. Configure:
   - **Every 2 weeks**
   - **Day/Time** client prefers
   - **Timezone**: Client's timezone
3. **Toggle ON**
4. **Save scenario**

---

## PART C: OPTION 2 - Apify Triggers Make (NOT Recommended)

### Why This is Complex:

1. **Need 3 separate Apify Schedules** (one per actor)
2. **Need 3 webhooks** in Make.com (one per task)
3. **Coordination issues**: What if actors don't finish at same time?
4. **Make.com must wait** for all 3 webhooks before sending email
5. **Harder to debug**: Logs split between Apify and Make.com

### If You Still Want This Approach:

#### Step 1: Create Webhooks in Make.com

1. Create a new scenario or modify existing
2. Add **"Custom Webhook"** module as the trigger
3. Click **"Add"** → Copy the webhook URL (e.g., `https://hook.make.com/abc123`)
4. Create **3 separate webhook modules**:
   - Webhook 1: For Task 1 completion
   - Webhook 2: For Task 2 completion
   - Webhook 3: For Task 3 completion

#### Step 2: Configure Apify Actors to Call Webhooks

For each actor:

1. Go to Apify console → Open the actor
2. Go to **Settings → Post-run webhook**
3. **Webhook URL**: Paste the Make.com webhook URL
4. **Payload**: Configure to send dataset ID and results
5. **Save**

#### Step 3: Schedule Actors in Apify

For each actor:

1. Go to **Schedules** in Apify console
2. Click **"Create schedule"**
3. Configure:
   - **Frequency**: Every 2 weeks
   - **Day/Time**: Same for all 3 actors
   - **Actor**: Select the task actor
4. **Save**

#### Step 4: Make.com Aggregation Logic

This is the complex part:

1. Make.com receives 3 separate webhook calls
2. You need to **aggregate** the results (wait for all 3)
3. Use **"Aggregator" module** to combine
4. Set timeout in case one actor fails
5. Process and send email only when all 3 complete

**Problem**: If one actor fails, the whole flow breaks.

---

## PART D: Recommended Final Checklist

### Before Client Handover:

- [ ] Test your complete flow in YOUR account (end-to-end)
- [ ] Export all 3 actor input JSON configurations
- [ ] Export Make.com blueprint JSON
- [ ] Document any custom configurations or notes
- [ ] Create Google Sheets templates with correct headers
- [ ] Write client-specific setup instructions
- [ ] Plan training session for client (optional)

### During Client Setup:

- [ ] Client creates Apify account (or adds you as team member)
- [ ] Client creates Make.com account (or adds you)
- [ ] Create 3 actors/tasks in client's Apify with your saved inputs
- [ ] Test each actor individually in client's Apify
- [ ] Get client's Apify API token
- [ ] Import blueprint to client's Make.com
- [ ] Reconnect all connections (Apify, Gmail, Sheets)
- [ ] Create data store in client's account
- [ ] Create Google Sheets in client's account
- [ ] Update Variables module with client's values
- [ ] Test complete flow end-to-end
- [ ] Set bi-weekly schedule
- [ ] Enable scheduling

### After Handover:

- [ ] Monitor first automated run
- [ ] Provide support documentation to client
- [ ] Schedule follow-up check after first 2-3 runs

---

## Quick Reference: Module Connections

### Your Current Setup (Before Changes):

```
Variable Module (524)
  ↓
Router
  ├─ Route 0: Fetch Dataset (a9zcGM6bQZbNLS9nf) → Process → Store
  ├─ Route 1: Fetch Dataset (R5FWB04ujtigD8Mo7) → Process → Store
  └─ Route 2: Fetch Dataset (6kCy5ZnpavOkAxTjR) → Process → Email
```

### Recommended New Setup (After Changes):

```
Schedule (Every 2 weeks)
  ↓
Variable Module (524)
  ↓
Router
  ├─ Route 0: Run Actor 1 → Fetch Dataset ({{actor1.defaultDatasetId}}) → Process → Store
  ├─ Route 1: Run Actor 2 → Fetch Dataset ({{actor2.defaultDatasetId}}) → Process → Store
  └─ Route 2: Run Actor 3 → Fetch Dataset ({{actor3.defaultDatasetId}}) → Process → Email
```

---

## Contact & Support

**If you encounter issues during migration:**

- **Apify Documentation**: https://docs.apify.com
- **Make.com Documentation**: https://www.make.com/en/help
- **Apify Support**: support@apify.com
- **Make.com Support**: support@make.com

**For blueprint JSON errors:**
- Validate JSON at: https://jsonlint.com
- Use Make.com's blueprint validator (import will show specific errors)

---

## Summary

**Easiest Path:**
1. ✅ **Use Option 1** (Make triggers Apify)
2. ✅ **Use default datasets** (no hardcoded IDs)
3. ✅ **Set schedule in Make.com** (bi-weekly)
4. ✅ **Test thoroughly in YOUR account first**
5. ✅ **Export everything before client migration**
6. ✅ **Follow Step 4 & 5** when client is ready

**Total Time Estimate:**
- Your account setup: 1-2 hours
- Testing: 1 hour
- Client migration: 2-3 hours
- Client training: 1 hour

**Good luck with the handover!** 🚀
