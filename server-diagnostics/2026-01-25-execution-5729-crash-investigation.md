# Server Diagnostic Report – Execution 5729 Crash Investigation

**Date:** 2026-01-25
**Execution:** 5729
**Crash Time:** 2026-01-25 20:46:45 UTC
**Server:** n8n.oloxa.ai (157.230.21.230)

---

## Executive Summary

**Root Cause:** Out of Memory (OOM) killer terminated the n8n process during execution 5729.

**Severity:** Critical - Combined memory exhaustion + disk space at 99% capacity.

**Status:** Server auto-recovered (n8n container restarted), but conditions remain critical.

---

## Timeline

- **20:40:25 UTC** - Execution 5729 started
- **20:46:45 UTC** - OOM killer terminated n8n process (PID 2392105)
- **~20:47:00 UTC** - Docker restarted n8n container automatically
- **21:57:00 UTC** - Investigation started
- **21:57:17 UTC** - Server still running but disk 99% full

---

## Detailed Findings

### 1. OOM Killer Event

**Evidence from dmesg:**
```
[Sun Jan 25 20:46:45 2026] oom-kill:constraint=CONSTRAINT_NONE
[Sun Jan 25 20:46:45 2026] Out of memory: Killed process 2392105 (node)
  total-vm:33393092kB, anon-rss:709012kB, file-rss:128kB
```

**Analysis:**
- n8n process (node) was using ~709MB RAM when killed
- Server has only 1.9GB total RAM (1.4GB used at investigation time)
- Available memory at investigation: 78MB free + 532MB available
- OOM killer triggered when system ran out of allocatable memory

### 2. Disk Space Critical

**Current Status (21:57 UTC):**
```
Filesystem: /dev/vda1
Size: 24GB
Used: 23GB (99%)
Available: 341MB
```

**Breakdown:**
- Docker volumes: 10.54GB total
- binaryData folder: 7.8GB (74% of volume space)
- Docker images: 5.19GB (unused/reclaimable)
- Containers: 57.3MB

**Critical threshold:** System is operating at 99% capacity, leaving minimal room for:
- Execution logs
- Temporary files
- Database writes
- Container operations

### 3. Container Status

**At investigation time (21:57 UTC):**
- `n8n-n8n-1`: Up about 1 hour (restarted after crash)
- `n8n-postgres-1`: Up 35 hours (healthy)
- `n8n-gotenberg-1`: Up 35 hours

**n8n container uptime** confirms crash and auto-restart around 20:47 UTC.

### 4. Memory Pressure

**System memory (21:57 UTC):**
```
Total: 1.9GB
Used: 1.4GB
Free: 78MB
Available: 532MB
Swap: 0B (no swap configured)
```

**Load average:** 0.62, 0.41, 0.31 (normal range)

**Key issue:** No swap space configured. When RAM fills, OOM killer must terminate processes immediately.

### 5. Automated Maintenance Status

**Cron jobs configured:**
- binaryData cleanup: Daily at 2 AM (deletes files >7 days old)
- Disk monitoring: Daily at 2:15 AM (logs when >80% full)

**Last cleanup:** Likely ran 2026-01-25 02:00 UTC (~19 hours before crash)

**Issue:** Cleanup is daily, but binaryData can accumulate faster than 24-hour cycle, especially with large executions.

---

## Root Cause Analysis

### Primary Cause: OOM Killer

1. **Execution 5729** started processing at 20:40:25 UTC
2. **Memory consumption** increased as execution progressed
3. **System ran out of RAM** at 20:46:45 UTC (no swap available)
4. **OOM killer terminated n8n** to free memory (standard Linux behavior)
5. **Docker auto-restarted** n8n container after crash

**Why this execution triggered OOM:**
- Execution ran for ~6 minutes before crash
- Process grew to ~709MB RAM (in a 1.9GB total system)
- Other services (postgres, gotenberg, system) consumed remaining RAM
- No headroom for memory spikes during data processing

### Contributing Factor: Disk Space

**Why 99% disk matters:**
- Limited space for execution logs
- No room for temporary files during processing
- Database write failures possible if disk fills completely
- Memory pressure increases when disk I/O fails

**Disk usage breakdown:**
- 7.8GB binaryData (execution outputs)
- 5.19GB Docker images (100% reclaimable - unused images)
- 2.74GB other (logs, postgres data, system files)

---

## Risk Assessment

### Immediate Risks (High Priority)

1. **Repeat OOM crashes** - High probability
   - Any large execution can trigger OOM again
   - No swap space to buffer memory spikes
   - Server currently at 1.4GB/1.9GB RAM usage

2. **Disk full** - High probability within 24-48 hours
   - Only 341MB free (1-2 large executions away from full)
   - Daily cleanup may not keep pace with accumulation
   - 100% disk = service failure (postgres can't write, n8n can't log)

3. **Data loss in executions** - Medium probability
   - `isArtificialRecoveredEventItem: true` indicates data loss
   - Execution outputs may be incomplete or corrupted
   - No transactional safety during OOM kill

### Ongoing Risks (Medium Priority)

1. **Performance degradation** - Currently occurring
   - High disk usage slows I/O operations
   - Low memory forces aggressive caching eviction
   - Load spikes can cascade into crashes

2. **Service unavailability** - Possible during peak usage
   - OOM can kill postgres instead of n8n next time
   - Multiple services competing for limited 1.9GB RAM

---

## Recommendations

### Immediate Actions (Critical)

1. **Free disk space immediately:**
   ```bash
   # Clean binaryData older than 3 days (emergency cleanup)
   find /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData -type f -mtime +3 -delete

   # Remove unused Docker images (5.19GB reclaimable)
   docker image prune -a
   ```
   **Expected recovery:** ~13GB total (5.19GB images + ~8GB old binaryData)

2. **Add swap space (buffer memory spikes):**
   ```bash
   # Create 2GB swap file
   fallocate -l 2G /swapfile
   chmod 600 /swapfile
   mkswap /swapfile
   swapon /swapfile
   echo '/swapfile none swap sw 0 0' >> /etc/fstab
   ```
   **Impact:** Prevents OOM kills during memory spikes (uses disk as overflow)

### Short-term Improvements (High Priority)

3. **Increase cleanup frequency:**
   ```bash
   # Change cron to run every 6 hours instead of daily
   0 */6 * * * find /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData -type f -mtime +7 -delete
   ```
   **Impact:** Reduces disk accumulation lag from 24h to 6h

4. **Add disk alert webhook:**
   ```bash
   # Alert when disk >90% (before critical 99%)
   */15 * * * * df -h / | awk 'NR==2 {gsub("%","",$5); if ($5 > 90) system("curl -X POST https://n8n.oloxa.ai/webhook/disk-alert?usage="$5) }'
   ```
   **Impact:** Early warning system for disk issues

### Long-term Solutions (Medium Priority)

5. **Upgrade server resources:**
   - **RAM:** 1.9GB → 4GB minimum (handles large executions)
   - **Disk:** 25GB → 50GB (more breathing room)
   - **Cost:** DigitalOcean $12/mo → $24/mo (2GB → 4GB droplet)

6. **Implement external storage for binaryData:**
   - Store execution outputs in S3/DigitalOcean Spaces
   - Keep only recent data on local disk
   - Reduces disk pressure significantly

7. **Add resource monitoring:**
   - Install Prometheus + Grafana for metrics
   - Track memory/disk trends over time
   - Predict capacity issues before they occur

---

## Verification Steps

**To confirm server stability after fixes:**

1. Check disk space freed:
   ```bash
   df -h /
   ```
   Target: <70% used

2. Verify swap is active:
   ```bash
   free -h
   ```
   Should show 2GB swap

3. Test workflow execution:
   - Run a test workflow with large data output
   - Monitor memory usage: `docker stats --no-stream`
   - Verify no OOM events: `dmesg | tail -20`

4. Monitor for 24 hours:
   - Check disk growth rate
   - Verify cron cleanup runs successfully
   - Ensure no repeat OOM events

---

## Next Steps

**Recommended priority:**

1. **Immediate (today):**
   - Clean binaryData (emergency 3-day threshold)
   - Remove unused Docker images
   - Add 2GB swap space
   - Verify disk <70% after cleanup

2. **This week:**
   - Increase cron cleanup frequency to 6-hourly
   - Add disk alert webhook (90% threshold)
   - Monitor execution patterns for 3-5 days

3. **Next month:**
   - Evaluate server upgrade based on usage trends
   - Consider external storage for binaryData
   - Implement comprehensive monitoring (Prometheus/Grafana)

---

## Technical Notes

**n8n Error Message Context:**
```
"isArtificialRecoveredEventItem: true"
```

This flag indicates n8n detected a crash during execution recovery. When n8n restarts after OOM kill:
1. Checks database for in-progress executions
2. Marks them as "artificially recovered" (incomplete)
3. Data from crashed execution may be partial or missing

**OOM Killer Behavior:**
- Linux kernel feature (not a bug)
- Triggered when system exhausts RAM + swap
- Selects process with highest oom_score (usually largest RAM consumer)
- Terminates process immediately (SIGKILL, no cleanup possible)

**Why no swap is problematic:**
- Modern servers often disable swap for performance
- n8n is better suited for occasional swap usage than no swap at all
- Swap acts as overflow buffer during processing spikes

---

## Conclusion

**Execution 5729 crashed due to OOM killer terminating n8n when system RAM was exhausted.** Server auto-recovered but remains in critical state with 99% disk usage and no swap space.

**Immediate action required:** Free disk space and add swap to prevent repeat crashes.

**Long-term:** Server resources (1.9GB RAM / 25GB disk) are insufficient for current workload. Upgrade to 4GB RAM / 50GB disk recommended.

---

**Report Generated:** 2026-01-25 21:57 UTC
**Investigated By:** server-ops-agent
**Status:** Critical - Immediate action required
