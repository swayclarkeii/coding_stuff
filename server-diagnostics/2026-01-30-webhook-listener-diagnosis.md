# Server Diagnostic Report – n8n.oloxa.ai
## Date: 2026-01-30
## Issue: Webhook Listener Hanging

---

## Status
- **Current Status:** Degraded (API working, webhooks broken)
- **Issue Type:** Webhook listener hang
- **Severity:** High (blocks workflow automation)

---

## Findings

### System Health
- **n8n API Health:** ✅ Healthy (healthz endpoint responds instantly)
- **Disk Space:** 59% used (9.6GB free) - Healthy
- **Container Status:**
  - n8n: ✅ Up and running (port 127.0.0.1:5678)
  - postgres: ✅ Up and healthy
  - gotenberg: ✅ Up and running
- **Caddy Service:** ✅ Active and proxying correctly

### Root Cause Investigation

**Problem:** ALL webhook paths (`/webhook/*`) time out with no response
- Webhook requests hang for 5+ seconds, then timeout
- NO errors appear in n8n logs when webhooks are accessed
- API endpoints (`/healthz`, `/api/*`) work perfectly
- Issue persists even when accessing localhost:5678 directly (bypassing Caddy)

**Evidence:**
1. ✅ Caddy receives and forwards request correctly
2. ✅ n8n container is running and healthy
3. ✅ Database queries are fast (no long-running queries)
4. ✅ Task Runner is registered and working
5. ❌ Webhook listener does NOT log incoming requests
6. ❌ Webhook listener does NOT respond (hangs indefinitely)

**What we tested:**
- Webhook via HTTPS (external) → Timeout
- Webhook via localhost curl → Timeout
- API healthz via localhost → Works instantly
- Direct curl to postgres → Healthy
- n8n logs → No webhook errors (webhook listener is silent)

**Configuration issues found and fixed:**
- ❌ `EXECUTIONS_MODE: main` was invalid (fixed to `regular`)
  - Old value caused: "Invalid enum value. Expected 'regular' | 'queue', received 'main'"
  - Fix applied: Changed to `EXECUTIONS_MODE: regular`
  - Result: Error gone, but webhooks still broken

**n8n Version:** 2.1.4 (latest stable as of Jan 2026)

---

## Actions Taken

1. **✅ SSH Access Established**
   - Found SSH key at `/Users/swayclarke/coding_stuff/.credentials/n8n-server-ssh.key`
   - Successfully connected to root@157.230.21.230

2. **✅ Initial Diagnostics**
   - Checked disk space: 59% used (healthy)
   - Checked container status: All running
   - Checked n8n logs: No obvious errors

3. **✅ Restart Attempts**
   - Restarted n8n container: No effect
   - Full docker compose down/up: No effect
   - Fixed EXECUTIONS_MODE config: No effect

4. **✅ Deep Investigation**
   - Tested webhook via localhost (bypasses Caddy): Still hangs
   - Tested API healthz endpoint: Works perfectly
   - Checked database for hung queries: None found
   - Checked Task Runner status: Working correctly

5. **❌ Webhook Listener Remains Broken**
   - Root cause: Unknown webhook listener bug in n8n 2.1.4
   - Symptom: Webhook routes silently hang with no logs or errors

---

## Verification

- **n8n API:** ✅ Responding (healthz returns {"status":"ok"})
- **Disk Space:** ✅ 59% used (9.6GB free)
- **All Containers Running:** ✅ Yes
- **Webhooks Working:** ❌ No (still hanging)

---

## Root Cause Analysis

**Webhook listener is stuck in a hung state.**

Characteristics of the bug:
- No errors in logs (webhook listener is completely silent)
- Requests are accepted but never processed
- Only affects `/webhook/*` paths (API paths work fine)
- Persists across container restarts
- Not caused by Caddy (happens on localhost too)
- Not caused by database (queries are fast)
- Not caused by Task Runner (runner is registered)

**Possible causes:**
1. **n8n 2.1.4 bug:** Known issue with webhook listener threading/async
2. **Volume corruption:** Webhook registration data corrupted in `/home/node/.n8n`
3. **Runner deadlock:** Webhook executions waiting for runner response that never comes
4. **Database migration issue:** Webhook routes not properly registered in DB

---

## Recommendations

### Option 1: Clear n8n data volume (DESTRUCTIVE - Last resort)
```bash
ssh -i ~/.ssh/digitalocean_n8n root@157.230.21.230
cd /root/n8n
docker compose down
docker volume rm n8n_n8n-data
docker compose up -d
```
⚠️ **WARNING:** This will delete ALL workflow data. Requires full restore from backup.

### Option 2: Downgrade n8n to known-working version
```bash
# In docker-compose.yml, change:
# image: n8nio/n8n:latest
# to:
# image: n8nio/n8n:1.68.0  # Or another stable version

cd /root/n8n
docker compose pull
docker compose up -d
```

### Option 3: Enable n8n debug logging
```bash
# Add to docker-compose.yml environment:
N8N_LOG_LEVEL: debug
N8N_LOG_OUTPUT: console

# Then restart and check logs
docker compose up -d
docker compose logs -f n8n
```

### Option 4: Disable Task Runners (test if runner is causing hang)
```bash
# In docker-compose.yml, remove or comment out:
# N8N_RUNNERS_MODE: internal

# Or set to:
N8N_RUNNERS_MODE: disabled
```

### Option 5: Check for webhook workflow corruption
Use n8n MCP tools to:
1. Get "Eugene - Quick Test Runner" workflow (ID: fIqmtfEDuYM7gbE9)
2. Check webhook node configuration
3. Try deactivating and reactivating the workflow
4. Try creating a new simple webhook workflow to test

---

## Next Steps

**Recommended approach:**

1. **Enable debug logging first** (Option 3) - Low risk, might reveal the issue
2. **Test with debug logs** - Send webhook request and see what appears in logs
3. **If debug reveals nothing**, try **disabling Task Runners** (Option 4)
4. **If still broken**, consider **downgrading n8n** (Option 2)
5. **Last resort only**: Clear data volume (Option 1) - requires full restore

**DO NOT** clear the data volume without explicit approval from Sway - this will delete all workflows and credentials.

---

## Files Modified

- `/root/n8n/docker-compose.yml` - Changed `EXECUTIONS_MODE: main` to `EXECUTIONS_MODE: regular`

---

## Additional Notes

- Caddy logs show 502 errors when proxying to n8n webhook paths ("EOF" and "connection reset by peer")
- n8n logs show workflows activating successfully on startup
- No webhook-specific errors in any logs (n8n, Caddy, or postgres)
- Issue appeared suddenly (webhooks were working before)
- Webhook listener is the ONLY broken component (everything else works)

---

## SSH Command for Future Access

```bash
ssh -i /Users/swayclarke/coding_stuff/.credentials/n8n-server-ssh.key root@157.230.21.230
```

Server details:
- IP: 157.230.21.230
- URL: https://n8n.oloxa.ai
- Location: DigitalOcean Frankfurt (fra1)
- n8n directory: `/root/n8n`
