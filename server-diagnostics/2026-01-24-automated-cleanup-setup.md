# Automated Cleanup Setup – n8n.oloxa.ai

## Date
2026-01-24

## Task
Set up automated binaryData cleanup and disk space monitoring on n8n server.

---

## Configuration Installed

### 1. Daily BinaryData Cleanup
**Cron Schedule**: Daily at 2:00 AM
**Command**:
```bash
0 2 * * * find /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData -type f -mtime +7 -delete && echo "[$(date)] Cleaned binaryData files older than 7 days" >> /var/log/n8n-cleanup.log
```

**What it does**:
- Runs every day at 2:00 AM UTC
- Deletes binaryData files older than 7 days
- Logs cleanup activity to `/var/log/n8n-cleanup.log`

### 2. Disk Space Monitoring
**Cron Schedule**: Daily at 2:15 AM
**Command**:
```bash
15 2 * * * df -h / | awk 'NR==2 {gsub("%","",$5); if ($5 > 80) print "["strftime("%Y-%m-%d %H:%M:%S")"] WARNING: Disk usage at "$5"%" }' >> /var/log/n8n-disk-monitor.log
```

**What it does**:
- Runs every day at 2:15 AM UTC (after cleanup)
- Checks disk usage on root partition
- Logs warning to `/var/log/n8n-disk-monitor.log` if usage exceeds 80%

---

## Verification Status

✅ **Crontab installed**: Both jobs added successfully
✅ **Cron service running**: Active since 2026-01-10
⚠️ **SSH connection lost**: Connection timed out during final verification

---

## Current Server Status (Before Connection Lost)

- **Disk Usage**: 63% (15GB/24GB) - Healthy
- **BinaryData Size**: 59MB - Very small
- **Previous Cron**: Weekly cleanup on Sundays at 3 AM (replaced)
- **New Cron**: Daily cleanup at 2 AM + monitoring at 2:15 AM

---

## What Changed

**Before**:
```bash
# Weekly cleanup on Sundays at 3 AM
0 3 * * 0 find /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData -type f -mtime +7 -delete
```

**After**:
```bash
# Daily cleanup at 2 AM
0 2 * * * find /var/lib/docker/volumes/n8n_n8n-data/_data/binaryData -type f -mtime +7 -delete && echo "[$(date)] Cleaned binaryData files older than 7 days" >> /var/log/n8n-cleanup.log

# Daily disk monitoring at 2:15 AM
15 2 * * * df -h / | awk 'NR==2 {gsub("%","",$5); if ($5 > 80) print "["strftime("%Y-%m-%d %H:%M:%S")"] WARNING: Disk usage at "$5"%" }' >> /var/log/n8n-disk-monitor.log
```

---

## Next Steps (When SSH Reconnects)

1. **Verify log files are created after first run** (2026-01-25 at 2:00 AM):
   ```bash
   ssh -i ~/.ssh/digitalocean_n8n root@157.230.21.230 "tail /var/log/n8n-cleanup.log"
   ```

2. **Check binaryData path** (connection dropped during verification):
   ```bash
   ssh -i ~/.ssh/digitalocean_n8n root@157.230.21.230 "ls -la /var/lib/docker/volumes/n8n_n8n-data/_data/"
   ```

3. **Monitor disk warnings** (if usage goes >80%):
   ```bash
   ssh -i ~/.ssh/digitalocean_n8n root@157.230.21.230 "tail /var/log/n8n-disk-monitor.log"
   ```

---

## Recommendations

1. **Check logs weekly** to ensure cleanup is running successfully
2. **Review binaryData path** once SSH reconnects (there was a warning during testing)
3. **Consider lowering retention** to 5 days if disk fills up frequently
4. **Set up email alerts** if disk monitoring warnings become frequent

---

## Status

**Overall**: ✅ Configuration installed successfully
**Cron Jobs**: ✅ Active and scheduled
**SSH Connection**: ⚠️ Lost during final verification (timeout)
**Next Check**: 2026-01-25 after first automated run
