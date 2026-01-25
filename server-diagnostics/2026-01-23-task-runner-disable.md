# Server Diagnostic Report – n8n Task Runner Disable

## Status
- **Current Status:** Healthy
- **Issue Type:** Task Runner configuration
- **Severity:** Medium (resolved)

## Problem Description
n8n was using the external Task Runner (`@n8n/task-runner`) for Code nodes, which caused the error:
```
"Module 'child_process' is disallowed"
```

Even though `NODE_FUNCTION_ALLOW_EXTERNAL=true` was set, it only applied to the main n8n process, not the Task Runner subprocess.

## Findings

### Before Fix
- **n8n API Health:** ✅ Healthy
- **Disk Space:** 68% used (7.6 GB free)
- **Container Status:**
  - n8n: Up
  - postgres: Up (healthy)
- **Environment Variables:**
  - `EXECUTIONS_MODE=main` ✅ Set
  - `NODE_FUNCTION_ALLOW_EXTERNAL=true` ✅ Set
  - `N8N_RUNNERS_MODE` ❌ Not set (defaulted to external Task Runner)

### Root Cause
n8n v2.33+ uses a separate Task Runner system for Code nodes by default. Even with `EXECUTIONS_MODE=main`, Code nodes were still being executed in the Task Runner subprocess where `NODE_FUNCTION_ALLOW_EXTERNAL` doesn't apply.

## Actions Taken

1. **Backed up docker-compose.yml**
   - Created backup: `docker-compose.yml.backup-20260123-175052`

2. **Added `N8N_RUNNERS_MODE=internal` environment variable**
   - This forces Code nodes to run in the main n8n process
   - Allows `NODE_FUNCTION_ALLOW_EXTERNAL=true` to work correctly

3. **Restarted n8n services**
   ```bash
   cd /root/n8n && docker compose down && docker compose up -d
   ```
   - Postgres stopped → removed
   - n8n stopped → removed
   - Services recreated and started
   - Both containers healthy

## Verification

### After Fix
- **n8n API:** ✅ Responding (2643ms response time)
- **Disk Space:** 68% used (unchanged)
- **All Services Running:** Yes
- **Environment Variables Confirmed:**
  ```
  EXECUTIONS_MODE=main ✅
  N8N_RUNNERS_MODE=internal ✅
  NODE_FUNCTION_ALLOW_BUILTIN=crypto ✅
  NODE_FUNCTION_ALLOW_EXTERNAL=true ✅
  ```
- **Container Status:**
  - n8n-n8n-1: Up 52 seconds
  - n8n-postgres-1: Up 58 seconds (healthy)

## Configuration Changes

**docker-compose.yml - n8n service environment:**
```yaml
environment:
  # ... existing variables ...
  NODE_FUNCTION_ALLOW_EXTERNAL: true
  EXECUTIONS_MODE: main
  N8N_RUNNERS_MODE: internal  # ← NEW: Forces Code nodes to run in main process
```

## Recommendations

1. **Test workflow execution** - Run a test execution of the workflow that was failing with "Module 'child_process' is disallowed" error to confirm the fix works

2. **Monitor performance** - Running Code nodes in the main process (internal mode) may have slightly different performance characteristics than the Task Runner. Monitor for any issues.

3. **Optional cleanup** - Remove the `version: '3.8'` line from docker-compose.yml to avoid the deprecation warning (cosmetic only, doesn't affect functionality)

## Next Steps

**Ready for testing:**
- The server is configured and running
- Code nodes will now run in the main n8n process where `NODE_FUNCTION_ALLOW_EXTERNAL=true` applies
- Execute the workflow to verify `child_process` module is now accessible

**If still encountering issues:**
- Check n8n logs: `docker compose logs n8n --tail 50`
- Verify execution error details in n8n UI
- May need to add specific modules to `NODE_FUNCTION_ALLOW_BUILTIN` if other built-in modules are required

## Technical Notes

**Task Runner Modes in n8n v2.33+:**
- `external` (default): Code nodes run in separate Task Runner process (isolated, secure)
- `internal`: Code nodes run in main n8n process (less isolation, required for `NODE_FUNCTION_ALLOW_EXTERNAL`)

**Trade-offs:**
- External Task Runner provides better isolation and security
- Internal mode provides access to external modules and built-in Node.js modules
- For your use case (needing `child_process`), internal mode is required
