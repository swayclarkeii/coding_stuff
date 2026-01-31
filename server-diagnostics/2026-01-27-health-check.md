# Server Diagnostic Report – n8n.oloxa.ai
**Date:** 2026-01-27 21:30 UTC
**Performed by:** server-ops-agent
**Server:** 157.230.21.230 (n8n.oloxa.ai)

---

## Status
- **Current Status:** Healthy (with minor WebSocket reconnection issues)
- **Issue Type:** None (routine health check)
- **Severity:** Low (502 errors on WebSocket reconnections are cosmetic)

---

## Findings

### n8n API Health
- **Status:** ✅ Healthy
- **API Responding:** Yes
- **Version:** 2.33.5 (latest)
- **Response Time:** 909ms (diagnostic mode)
- **MCP Tools Available:** 20 tools (all enabled)

### Disk Space
- **Total Disk:** 24GB
- **Used:** 14GB (57%)
- **Available:** 11GB (43%)
- **Status:** ✅ Healthy (well below 80% threshold)

### BinaryData Storage
- **Size:** 4.6MB
- **Status:** ✅ Excellent (minimal storage usage)
- **Previous Issue:** Disk was 100% full on 2026-01-09 (binaryData filled to 14GB)
- **Current State:** Cleanup was successful, no bloat

### Container Status
All containers running normally:

| Container | Status | Uptime | CPU % | Memory | Status |
|-----------|--------|--------|-------|---------|---------|
| **n8n-n8n-1** | Up | 10 minutes | 0.35% | 335.3MB / 1.9GB (17%) | ✅ Healthy |
| **n8n-postgres-1** | Up (healthy) | 37 hours | 0.00% | 107.6MB / 1.9GB (5.5%) | ✅ Healthy |
| **n8n-gotenberg-1** | Up | 37 hours | 0.06% | 14.75MB / 1.9GB (0.75%) | ✅ Healthy |

**Note:** n8n container shows recent restart (10 minutes uptime vs 37 hours for postgres/gotenberg)

### Memory Usage
- **Total RAM:** 1.9GB
- **Used:** 920MB (48%)
- **Free:** 144MB (7%)
- **Buff/Cache:** 1.2GB
- **Available:** 1.0GB (52%)
- **Swap:** 131MB / 2.0GB (6.5% used)
- **Status:** ✅ Healthy (plenty of available memory)

### Caddy Service (Reverse Proxy)
- **Status:** ✅ Active (running)
- **Uptime:** 1 day 23 hours
- **Memory:** 36.4MB (peak: 54.7M)
- **CPU Time:** 1min 35s
- **PID:** 811

**Recent Errors in Caddy Logs:**
- Multiple 502 errors from 21:12-21:17 UTC
- Error type: "connection reset by peer" and "EOF" on WebSocket push endpoints
- Pattern: `/rest/push?pushRef=*` (WebSocket connections)
- Impact: Browser clients reconnecting WebSockets (cosmetic, self-healing)

### Server Uptime & Date
- **Current Time:** Tue Jan 27 21:27:49 UTC 2026
- **Uptime:** 1 day, 23:02 (up since Jan 25 22:25 UTC)
- **Load Average:** 0.00, 0.05, 0.07 (very low, healthy)

### Active Workflows (23 workflows)
All workflows activated successfully on startup:
- Expense System (5 workflows)
- CRM/Brain Dump (2 workflows)
- Invoice Generator (2 workflows)
- Eugene Document Tracking
- Fathom Transcript Workflow
- AMA Email Senders (3 workflows)
- Google OAuth Monitor
- Staff Pre-Interview Questionnaire
- Agentic Loop Test POC
- Test orchestrators and helpers (7 workflows)

### Known Issues (Non-Critical)
1. **UptimeRobot HEAD requests blocked** - Expected behavior (n8n blocks bot requests)
2. **Unknown webhook "POST agentic-test-v2"** - Workflow likely disabled or webhook deleted
3. **WebSocket 502 errors (21:12-21:17 UTC)** - Browser reconnection attempts during n8n restart
4. **docker-compose.yml version warning** - Cosmetic warning (docker-compose.yml uses obsolete `version` attribute)

---

## Actions Taken

1. **Located SSH key** - Found at `/Users/swayclarke/coding_stuff/.credentials/n8n-server-ssh.key`
2. **Added server to known_hosts** - Resolved host key verification failure
3. **Performed comprehensive health check:**
   - Disk space analysis
   - Memory usage check
   - Container status verification
   - BinaryData folder size check
   - Caddy service status
   - n8n API health check
   - Resource usage monitoring
   - Log analysis

---

## Verification

- **n8n API:** ✅ Responding normally (909ms diagnostic response)
- **Disk Space:** ✅ 57% used (11GB free)
- **All Containers Running:** ✅ Yes (n8n, postgres, gotenberg)
- **Caddy Service:** ✅ Active and running
- **Memory Available:** ✅ 1.0GB available (52%)
- **BinaryData Cleanup:** ✅ Successfully reduced from 14GB to 4.6MB

---

## Recommendations

### Immediate Actions
✅ **None required** - Server is healthy and operating normally

### Short-Term Monitoring (Next 24-48 Hours)
1. **Monitor WebSocket stability** - Watch for recurring 502 errors on `/rest/push` endpoints
2. **Track n8n container stability** - Container restarted 10 minutes ago; monitor for crashes

### Medium-Term Improvements (Next 1-2 Weeks)
1. **Fix docker-compose.yml warning** - Remove obsolete `version` attribute from `/root/n8n/docker-compose.yml`
2. **Clean up unknown webhook** - Investigate "agentic-test-v2" webhook registration
3. **Review UptimeRobot config** - Consider allowing HEAD requests or switching to GET

### Long-Term Prevention (Next 1-3 Months)
1. **Set up automated binaryData cleanup** - Cron job to delete files >7 days old
2. **Configure disk usage alerts** - Alert when disk exceeds 75%
3. **Add container health monitoring** - Alert when containers restart unexpectedly
4. **Review n8n log retention** - Prevent log files from consuming disk space

---

## Technical Notes

### SSH Access
- **Key Location:** `/Users/swayclarke/coding_stuff/.credentials/n8n-server-ssh.key`
- **Permissions:** 600 (correct)
- **Command:** `ssh -i /Users/swayclarke/coding_stuff/.credentials/n8n-server-ssh.key root@157.230.21.230`
- **Note:** Update INFRASTRUCTURE_ACCESS.md to reflect actual key location (not `~/.ssh/digitalocean_n8n`)

### Recent Server History
- **Jan 25 22:25 UTC:** Server power cycled (based on uptime and Caddy start time)
- **Jan 9 (estimated):** Disk filled to 100% (binaryData folder reached 14GB)
- **Jan 9-25 (estimated):** BinaryData cleanup performed (reduced to 4.6MB)
- **Jan 27 21:17 UTC:** n8n container restarted (10 minutes before this health check)

### BinaryData Cleanup Success
Previous issue: `/var/lib/docker/volumes/n8n_n8n-data/_data/binaryData/` filled disk to 100%
Current state: 4.6MB (99.97% reduction)
Method used: Likely `rm -rf /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData/*`

---

## Next Steps

**No immediate action required.** Server is healthy and all services are running normally.

**Optional maintenance tasks:**
1. Update INFRASTRUCTURE_ACCESS.md with correct SSH key path
2. Set up automated binaryData cleanup cron job
3. Investigate recent n8n container restart (10 minutes ago)

**If issues arise:**
1. Check disk space first: `ssh -i [key] root@157.230.21.230 "df -h"`
2. Restart n8n services: `ssh -i [key] root@157.230.21.230 "cd /root/n8n && docker compose restart"`
3. Check logs: `ssh -i [key] root@157.230.21.230 "cd /root/n8n && docker compose logs --tail 50 n8n"`

---

## Summary for Sway

Your n8n server is **healthy and running normally**. Disk usage is at a safe 57% (11GB free), memory is good at 52% available, and all containers are up and running. The binaryData cleanup from the previous disk full issue was very successful (reduced from 14GB to 4.6MB).

The only minor observation is that the n8n container restarted about 10 minutes ago (while postgres and gotenberg have been up for 37 hours). This restart caused some temporary WebSocket 502 errors in Caddy logs around 21:12-21:17 UTC, but these are cosmetic - browsers automatically reconnect and everything is working normally now.

**Key findings:**
- **SSH key found:** `/Users/swayclarke/coding_stuff/.credentials/n8n-server-ssh.key`
- **n8n API healthy:** Version 2.33.5 (latest), responding in 909ms
- **Disk space excellent:** 57% used, 11GB free (was 100% full on Jan 9)
- **BinaryData cleaned:** 4.6MB (down from 14GB)
- **23 workflows active:** All activated successfully on startup
- **No action required:** Server is stable and healthy

For future reference, INFRASTRUCTURE_ACCESS.md should be updated to reflect the actual SSH key location at `/Users/swayclarke/coding_stuff/.credentials/n8n-server-ssh.key` instead of `~/.ssh/digitalocean_n8n`.
