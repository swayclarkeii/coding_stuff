# Cron Job Failure Diagnosis - n8n.oloxa.ai

**Date:** 2026-01-26
**Agent:** server-ops-agent
**Issue:** Automated cleanup cron job failed to prevent disk from filling to 100%

---

## Summary

**Root Cause Identified:** The cron job is running successfully every 4 hours, but the cleanup window (12 hours old files) is TOO SHORT for the rate of data generation. Files are being created faster than the cleanup can delete them.

**Severity:** HIGH - The current cron configuration is inadequate for the workload.

---

## Findings

### 1. Cron Job Configuration (EXISTS AND RUNS)

**Root crontab contents:**
```cron
0 */4 * * * find /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData -type f -mmin +720 -delete >> /var/log/n8n-cleanup.log 2>&1
30 */4 * * * docker system prune -f >> /var/log/n8n-docker-cleanup.log 2>&1
0 * * * * df -h / >> /var/log/n8n-disk-monitor.log 2>&1
```

**Status:** ✅ Cron jobs exist and are configured correctly

### 2. Cron Service Status

**Service:** cron.service
- **Status:** Active (running) since Sun 2026-01-25 22:25:33 UTC
- **Uptime:** 10+ hours
- **PID:** 813

**Status:** ✅ Cron service is healthy and running

### 3. Execution History

**Last cleanup executions (from /var/log/syslog):**
```
2026-01-26T00:00:01 - Cleanup ran (midnight)
2026-01-26T04:00:01 - Cleanup ran (4am)
2026-01-26T08:00:01 - Cleanup should have run (8am)
```

**Log files:**
- `/var/log/n8n-cleanup.log` - 156 bytes (minimal logging)
- `/var/log/n8n-docker-cleanup.log` - 52 bytes
- `/var/log/n8n-disk-monitor.log` - 890 bytes

**Status:** ✅ Cron jobs are executing on schedule

### 4. Disk Space Progression (from disk monitor log)

**Timeline showing disk filling up:**
```
Hour 00: 72% used (17GB / 24GB) - 6.6GB free
Hour 01: 76% used (18GB / 24GB) - 5.7GB free
Hour 02: 80% used (19GB / 24GB) - 4.8GB free
Hour 03: 84% used (20GB / 24GB) - 3.9GB free
Hour 04: 88% used (21GB / 24GB) - 3.0GB free  [Cleanup ran at 04:00]
Hour 05: 92% used (22GB / 24GB) - 2.1GB free
Hour 06: 96% used (23GB / 24GB) - 1.2GB free
Hour 07: 100% used (23GB / 24GB) - 195MB free
Hour 08: 100% used (24GB / 24GB) - 0 free  [Cleanup should have run]
```

**Rate of growth:** ~1GB per hour (extremely fast)

**Status:** ❌ Disk filled from 72% to 100% in ~8 hours despite cleanup running

---

## Root Cause Analysis

### Why the Cron Job Failed

**The cron job IS working - but it's inadequate for the workload:**

1. **Cleanup window too narrow:**
   - Current: Deletes files older than 720 minutes (12 hours)
   - Problem: Files are being created so rapidly that only 12-hour-old files get deleted
   - If workflows run constantly, the 12-hour buffer accumulates too much data

2. **Cleanup frequency insufficient:**
   - Current: Runs every 4 hours
   - Problem: Disk grows 4GB between cleanups (4 hours × 1GB/hour)
   - By the time cleanup runs, new files have already filled the disk

3. **No emergency threshold:**
   - Current: No disk space check before running cleanup
   - Problem: When disk hits 90%, cleanup should be more aggressive
   - No fallback to delete ALL old files when disk is critical

### What Actually Happened

**Between 04:00 (last cleanup) and 08:00 (disk full):**
1. 04:00 - Cleanup ran, deleted files >12 hours old
2. 04:00-08:00 - New workflows created ~4GB of new binaryData
3. 08:00 - Disk reached 100% BEFORE the next cleanup cycle
4. 08:00 - Cleanup tried to run but disk was already full
5. Result: Server crashed due to no disk space

---

## Recommended Fixes

### Fix 1: More Aggressive Cleanup Window

**Change from 12 hours to 6 hours:**
```cron
0 */4 * * * find /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData -type f -mmin +360 -delete >> /var/log/n8n-cleanup.log 2>&1
```

**Why:** Deletes files older than 6 hours instead of 12, reduces buffer size by 50%

### Fix 2: Increase Cleanup Frequency

**Change from every 4 hours to every 2 hours:**
```cron
0 */2 * * * find /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData -type f -mmin +360 -delete >> /var/log/n8n-cleanup.log 2>&1
```

**Why:** Runs twice as often, prevents 4-hour accumulation

### Fix 3: Add Emergency Cleanup Trigger

**Add threshold-based cleanup when disk >85%:**
```bash
#!/bin/bash
# /root/scripts/emergency-cleanup.sh

DISK_USAGE=$(df / | grep / | awk '{print $5}' | sed 's/%//')

if [ $DISK_USAGE -gt 85 ]; then
  echo "[$(date)] EMERGENCY: Disk at ${DISK_USAGE}% - Running aggressive cleanup"
  # Delete files older than 2 hours
  find /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData -type f -mmin +120 -delete
  # Restart n8n to clear memory
  cd /root/n8n && docker compose restart
  echo "[$(date)] Emergency cleanup complete"
fi
```

**Cron entry:**
```cron
*/30 * * * * /root/scripts/emergency-cleanup.sh >> /var/log/n8n-emergency-cleanup.log 2>&1
```

**Why:** Checks every 30 minutes and aggressively cleans when disk >85%

### Fix 4: Combined Recommended Configuration

**New crontab (recommended):**
```cron
# Regular cleanup every 2 hours (files older than 6 hours)
0 */2 * * * find /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData -type f -mmin +360 -delete >> /var/log/n8n-cleanup.log 2>&1

# Emergency cleanup every 30 minutes if disk >85%
*/30 * * * * /root/scripts/emergency-cleanup.sh >> /var/log/n8n-emergency-cleanup.log 2>&1

# Docker cleanup every 4 hours
30 */4 * * * docker system prune -f >> /var/log/n8n-docker-cleanup.log 2>&1

# Disk monitoring every hour
0 * * * * df -h / >> /var/log/n8n-disk-monitor.log 2>&1
```

---

## Actions Required

1. **Create emergency cleanup script** at `/root/scripts/emergency-cleanup.sh`
2. **Update root crontab** with new configuration above
3. **Test emergency script** manually to verify it works
4. **Monitor disk usage** over next 24 hours to confirm fix

---

## Alternative Solutions (Long-term)

If the above fixes still don't prevent disk from filling:

1. **Upgrade droplet size** - Move from 25GB to 50GB disk
2. **Configure n8n data retention** - Set n8n to auto-delete execution data after 24 hours
3. **Move binaryData to external storage** - Use S3 or DigitalOcean Spaces for large files
4. **Optimize workflows** - Reduce workflows that generate large binary outputs

---

## Next Steps

1. Wait for server SSH to become available again
2. Implement Fix 4 (combined configuration)
3. Create emergency cleanup script
4. Test the new cron configuration
5. Monitor for 24-48 hours to verify disk stays <80%

---

## Conclusion

**The cron job WAS working - it just wasn't aggressive enough.**

The cleanup script runs every 4 hours and deletes files older than 12 hours. However, with workflows generating ~1GB per hour, the disk fills faster than the cleanup can manage.

**Solution:** More frequent cleanup (every 2 hours) + shorter retention (6 hours) + emergency cleanup when disk >85%.
