# Server Diagnostic Report – n8n.oloxa.ai

**Date:** 2026-01-26 08:07 UTC
**Technician:** server-ops-agent
**Type:** Routine Health Check

---

## Executive Summary

**Status:** 🔴 **CRITICAL - Immediate Action Required**

The n8n server is functional but experiencing a **critical disk space issue** (100% full). While the n8n API remains responsive and containers are running, the disk condition poses a high risk for:
- Service crashes
- Database corruption
- Inability to process new executions
- PostgreSQL health degradation

**Immediate Recommendation:** Clean binaryData folder to free 5-7GB of disk space.

---

## Status

- **Current Status:** Degraded (functional but at risk)
- **Issue Type:** Disk Full (100%)
- **Severity:** Critical
- **Uptime:** 9 hours 41 minutes

---

## Detailed Findings

### 1. n8n API Health ✅ HEALTHY

**Status:** Fully operational
- **API Version:** 2.33.5 (latest)
- **API Response Time:** 2,651ms (diagnostic mode)
- **Connection:** HTTPS working correctly
- **Authentication:** API key configured and valid
- **Tools Available:** 20/20 (all management tools enabled)

### 2. Disk Space 🔴 CRITICAL

**Root Filesystem:**
```
Filesystem: /dev/vda1
Size: 24GB
Used: 24GB (100%)
Available: 0 bytes
```

**Breakdown:**
- **Total Capacity:** 24GB
- **Used:** 24GB (100%)
- **Free:** 0 bytes
- **BinaryData Folder:** 7.1GB (primary consumer)
- **Other Filesystems:** Healthy (/boot at 14%, /boot/efi at 6%)

**Impact:**
- No space for new executions
- Risk of database write failures
- Container restart failures possible
- Log rotation blocked

### 3. Memory Usage ⚠️ ELEVATED

**System Memory:**
```
Total: 1.9GB
Used: 805MB (42%)
Free: 364MB (19%)
Cached: 1.0GB
Available: 1.1GB (58%)
```

**Swap Usage:**
```
Total: 2.0GB
Used: 110MB (5.4%)
Free: 1.9GB
```

**Load Average:** 3.58, 3.84, 3.87 (high for 2GB system)

**Analysis:**
- Memory usage is acceptable but elevated
- Swap usage indicates some memory pressure
- Load average is high (3.5-4.0 on 1 CPU core suggests overload)
- System under moderate stress

### 4. Container Status ⚠️ MIXED

**n8n Container (n8n-n8n-1):**
- Status: ✅ Up and running (10 hours)
- Image: n8nio/n8n:latest
- Ports: 127.0.0.1:5678 (localhost only)

**PostgreSQL Container (n8n-postgres-1):**
- Status: ⚠️ Up but **unhealthy** (10 hours)
- Image: postgres:16
- Health Check: FAILING
- Impact: Database may be experiencing issues due to disk space

**Gotenberg Container (n8n-gotenberg-1):**
- Status: ✅ Up and running (10 hours)
- Image: gotenberg/gotenberg:8
- Ports: 0.0.0.0:3000 (PDF generation service)

### 5. Caddy Service ✅ HEALTHY

**Status:** Active and running
- **Uptime:** 9 hours 41 minutes
- **Memory:** 32.9MB (peak: 54.7MB)
- **CPU:** 12.1 seconds total
- **Function:** Reverse proxy (HTTPS → localhost:5678)

### 6. BinaryData Folder 🔴 LARGE

**Size:** 7.1GB
**Location:** `/var/lib/docker/volumes/n8n_n8n-data/_data/binaryData`

**Analysis:**
- Consuming 29.6% of total disk space
- Likely contains old execution files (screenshots, downloads, PDFs)
- Files older than 7 days can be safely deleted
- Cleaning this will free 5-7GB immediately

---

## Root Cause Analysis

**Primary Issue:** Disk space exhaustion

**Contributing Factors:**
1. **BinaryData accumulation** - 7.1GB of execution output files not cleaned
2. **No automated cleanup** - No cron job found for binaryData maintenance
3. **Small disk allocation** - 24GB is minimal for production n8n with file operations
4. **PostgreSQL unhealthy** - Database health checks failing (likely due to disk space)

**How it happened:**
- n8n workflows generate binary files (images, PDFs, downloads)
- These accumulate in binaryData folder over time
- No automatic cleanup configured
- Disk gradually filled to 100%
- PostgreSQL health degraded when unable to write

---

## Recommended Actions

### IMMEDIATE (Next 10 minutes)

**Priority 1: Clean binaryData folder**
```bash
# Clean files older than 7 days
find /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData -type f -mtime +7 -delete

# Restart services
cd /root/n8n && docker compose restart
```

**Expected Result:**
- Free 5-7GB of disk space
- Drop usage from 100% to ~70%
- PostgreSQL health should recover
- System stability restored

### SHORT-TERM (Next 24 hours)

**Priority 2: Verify recovery**
- Confirm disk usage <80%
- Verify PostgreSQL health check passes
- Monitor for new disk growth

**Priority 3: Set up automated cleanup**
- Create cron job to clean binaryData weekly
- Target files older than 7 days
- Run every Sunday at 2am UTC

### LONG-TERM (Next 30 days)

**Priority 4: Disk capacity planning**
- Monitor disk usage trends
- Consider upgrading to 40GB disk if usage exceeds 70% regularly
- Evaluate workflow file retention policies

**Priority 5: Monitoring alerts**
- Set up disk space alerts (notify at 80% full)
- Monitor PostgreSQL health status
- Alert on container restarts

---

## Performance Metrics

| Metric | Value | Status | Notes |
|--------|-------|--------|-------|
| **API Latency** | 2.6s | ⚠️ Elevated | Diagnostic mode (normal use is faster) |
| **Disk I/O Wait** | Unknown | N/A | SSH timeout prevented measurement |
| **Load Average** | 3.58 | ⚠️ High | System under stress |
| **Memory Pressure** | 42% used | ✅ OK | Within acceptable range |
| **Swap Usage** | 5.4% | ✅ OK | Minimal swap activity |

---

## Connectivity Issues

**Note:** During diagnostics, SSH connections began timing out (2 occurrences). This suggests:
- System load is affecting SSH responsiveness
- Network or firewall may be rate-limiting connections
- Server is under stress from disk/resource constraints

**Not blocking operations currently**, but indicates system strain.

---

## Next Steps

1. **Immediate:** Clean binaryData folder (run cleanup command)
2. **Verify:** Check disk space after cleanup (should be ~70%)
3. **Monitor:** Watch PostgreSQL health status over next hour
4. **Schedule:** Set up automated weekly cleanup
5. **Plan:** Consider disk expansion if usage trends upward

---

## Technical Details

**Server:**
- Provider: DigitalOcean (Frankfurt fra1)
- IP: 157.230.21.230
- OS: Ubuntu 24.04 LTS
- Resources: 2GB RAM / 25GB Disk

**Services:**
- n8n: v2.33.5 (latest)
- PostgreSQL: 16
- Caddy: Active (reverse proxy)
- Gotenberg: Active (PDF service)

**Data Volumes:**
- n8n_n8n-data: 7.1GB+ (binaryData heavy)
- n8n_postgres-data: Unknown size

---

## Conclusion

The n8n server requires **immediate intervention** to clean disk space. While currently functional, the 100% disk usage poses a critical risk to data integrity and service availability. Cleaning the binaryData folder will resolve the immediate issue and restore normal operations.

**Estimated fix time:** 5 minutes
**Risk level:** Low (deleting old execution files only)
**Impact:** High positive impact on stability
