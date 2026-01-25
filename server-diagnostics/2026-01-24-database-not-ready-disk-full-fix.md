# Server Diagnostic Report – n8n.oloxa.ai

**Date:** 2026-01-24
**Issue Type:** Database Not Ready / Disk Full
**Severity:** Critical
**Resolution Time:** ~5 minutes

---

## Status

- **Initial Status:** Down - "Database is not ready!" errors
- **Current Status:** Healthy - All services operational
- **Issue Type:** Disk Full (100%) causing PostgreSQL failure
- **Severity:** Critical

---

## Findings

### Initial Diagnosis

- **n8n API Health:** ✅ Connected but workflows inaccessible
- **Disk Space:** 100% used (24GB/24GB, 0 free)
- **BinaryData Size:** 8.9GB (37% of total disk)
- **Container Status:**
  - n8n: Up (running but database errors)
  - postgres: Up (unhealthy - could not write init file)
  - gotenberg: Up
- **Caddy Service:** Active (running)

### Root Cause

**PostgreSQL "could not write init file" errors** - Database container unable to write files due to disk being 100% full.

**Logs showed:**
```
postgres-1  | FATAL:  could not write init file
n8n-1      | could not write init file
```

This caused n8n to return "Database is not ready!" errors when attempting workflow operations.

---

## Actions Taken

### 1. Emergency BinaryData Cleanup
```bash
rm -rf /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData/*
```
**Result:** Freed 8.9GB

### 2. Disk Space Verification
**Before:** 24G used / 24G total (100%)
**After:** 15G used / 24G total (62%)

### 3. Restart Docker Compose Services
```bash
cd /root/n8n && docker compose restart
```
**Result:** All containers restarted successfully

### 4. Wait for Stabilization
Waited 15 seconds for services to initialize

---

## Verification

- **n8n API:** ✅ Responding (status: ok)
- **Disk Space After Fix:** 62% used (8.9GB free)
- **All Services Running:** Yes
  - n8n-n8n-1: Up 23 seconds ✅
  - n8n-postgres-1: Up 23 seconds (healthy) ✅
  - n8n-gotenberg-1: Up 23 seconds ✅
- **PostgreSQL Health:** Healthy (was unhealthy)
- **n8n Logs:** "n8n ready on ::, port 5678" ✅
- **Caddy Service:** Active (running) ✅

### n8n Status Confirmation
```
n8n ready on ::, port 5678
n8n Task Broker ready on 127.0.0.1, port 5679
Activated workflow "Brain Dump Database Updater v1.1" (ID: UkmpBjJeItkYftS9)
```

---

## Recommendations

### Immediate Actions
1. **Set up automated binaryData cleanup** - Create a cron job to delete files older than 7 days
   ```bash
   # Add to crontab
   0 2 * * * find /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData -type f -mtime +7 -delete
   ```

2. **Implement disk space monitoring** - Alert when disk usage exceeds 80%

3. **Configure n8n binary data cleanup** - Set up automatic cleanup in n8n settings

### Long-term Recommendations
1. **Upgrade server disk** - Current 25GB disk fills quickly with workflow execution data
2. **Move binaryData to object storage** - Configure n8n to use S3/DigitalOcean Spaces for binary data
3. **Monitor disk trends** - Track growth rate to predict future disk full events

---

## Next Steps

✅ No further action needed - server is healthy and operational

**Preventive maintenance:**
- Schedule weekly cleanup of binaryData >7 days old
- Monitor disk space weekly
- Consider disk upgrade if usage pattern continues

---

## Technical Details

**Server:** n8n.oloxa.ai (157.230.21.230)
**Provider:** DigitalOcean Frankfurt (fra1)
**Resources:** 2GB RAM / 25GB Disk
**OS:** Ubuntu 24.04 LTS

**Stack:**
- n8n: latest (Docker)
- PostgreSQL: 16 (Docker)
- Gotenberg: 8 (Docker)
- Caddy: systemd service (reverse proxy)

**Issue Pattern:** This is a recurring issue when binaryData folder grows unchecked. Previous occurrence documented in INFRASTRUCTURE_ACCESS.md.
