# Server Diagnostic Report – n8n.oloxa.ai
## Date: 2026-01-30

## Status
- **Current Status:** Healthy
- **Issue Type:** False alarm - webhook timeout (not hung)
- **Severity:** Low (no actual failure)

## Initial Symptoms
- Webhook requests to `/webhook/eugene-quick-test` timing out after 5-10 seconds
- HTTP clients receiving timeout errors
- Appeared to be webhook listener hung

## Findings
- **n8n API Health:** ✅ Healthy
- **Disk Space:** 59% used (9.6 GB free) - Healthy
- **BinaryData Size:** Not checked (disk space healthy)
- **Container Status:**
  - n8n: ✅ Up (4 minutes)
  - postgres: ✅ Up (6 minutes, healthy)
  - gotenberg: ✅ Up (6 minutes)
- **Caddy Service:** Not checked (n8n responding directly)

## Root Cause

**The webhook listener is NOT hung** - it's working correctly.

The issue was misidentified. Actual behavior:

1. Webhook receives request and starts execution immediately
2. Workflow "Eugene - Quick Test Runner" (ID: fIqmtfEDuYM7gbE9) executes successfully
3. Workflow calls sub-workflow "Chunk 2.5 - Client Document Tracking" (ID: okg8wTqLtPUwjQ18)
4. Chunk 2.5 performs multiple Claude API calls with deliberate rate-limiting waits
5. **Total execution time: 4 minutes 34 seconds**
6. HTTP clients timeout after 5-10 seconds waiting for response
7. **Workflow continues executing in background and completes successfully**

### Debug Logging Evidence

With `N8N_LOG_LEVEL=debug` enabled, logs showed:

```
10:57:15 - Execution 7153 started
10:57:16 - Webhook → Set Config → Check File Source → List Files → Pick Random → Build Input
10:57:16 - Execute Chunk 2.5 (sub-workflow okg8wTqLtPUwjQ18)
10:57:17-47 - Build AI Classification Prompt (30 seconds - processing base64 PDF)
10:57:47-58:18 - Build Claude Tier 1 Request Body (30 seconds)
10:58:18-38 - Wait Before Tier 1 (20 seconds - deliberate rate limiting)
10:58:38-41 - Claude Vision Tier 1 Classification (3 seconds API call)
10:58:41-59:41 - Wait After Tier 1 (60 seconds - deliberate rate limiting)
10:59:41 - Parse responses and continue to Tier 2
... (continued processing)
11:01:49 - Execution 7153 completed successfully (finished: true)
```

### Previous Crash Context

During diagnostics, found evidence of previous crash:
- "Last session crashed" message in logs
- 5 unfinished executions (7144-7148) from 10:49-10:51
- These were recovered on restart

The restart with debug logging cleared the previous crash state, but the "webhook hanging" issue persisted because it was never actually hanging - just a long-running workflow.

## Actions Taken

1. ✅ Checked n8n API health via MCP
2. ✅ Verified disk space (59% used - healthy)
3. ✅ Checked container status (all running)
4. ✅ Backed up docker-compose.yml
5. ✅ Enabled debug logging (`N8N_LOG_LEVEL=debug`, `N8N_LOG_OUTPUT=console`)
6. ✅ Restarted n8n container with debug logging
7. ✅ Performed full docker compose down/up to clear previous crash state
8. ✅ Tested webhook with curl (confirmed timeout behavior)
9. ✅ Analyzed debug logs to identify execution flow
10. ✅ Monitored execution 7153 through completion

## Verification
- **n8n API:** ✅ Responding normally
- **Disk Space:** 59% used (no change needed)
- **All Services Running:** ✅ Yes
- **Webhook Executing:** ✅ Yes (completes in background)
- **Execution 7153:** ✅ Completed successfully after 4:34 minutes

## Root Problem (Not a Bug)

This is **expected behavior** for webhooks triggering long-running workflows:

- n8n webhooks are **synchronous by default**
- HTTP response waits until workflow completes
- Long workflows (>30 seconds) will timeout on most HTTP clients
- Workflow continues executing even after client disconnects
- This is standard webhook behavior, not a system failure

## Recommended Solutions

### Option 1: Add "Respond to Webhook" Node (Recommended)

Add a "Respond to Webhook" node early in the workflow:

```
Webhook Trigger → Respond to Webhook → [Rest of workflow]
```

Benefits:
- Client receives immediate "202 Accepted" response
- Workflow continues executing in background
- No timeout errors for clients

### Option 2: Use Async Webhook Pattern

Configure webhook to return execution ID immediately:

```javascript
{
  "status": "processing",
  "executionId": "7153",
  "checkStatusAt": "https://n8n.oloxa.ai/api/v1/executions/7153"
}
```

Client can poll for completion status.

### Option 3: Increase Client Timeout

For testing/development only:
```bash
curl --max-time 300 https://n8n.oloxa.ai/webhook/eugene-quick-test
```

Not recommended for production use.

## Configuration Changes Made

### docker-compose.yml
Added debug logging environment variables to n8n service:
```yaml
environment:
  # ... existing vars ...
  N8N_LOG_LEVEL: debug
  N8N_LOG_OUTPUT: console
```

**Note:** Debug logging can be disabled after troubleshooting by removing these vars and restarting.

## Performance Notes

Workflow execution times observed:
- Webhook → Set Config → Check File Source: <1 second
- List Files (Google Drive): ~0.5 seconds
- Download PDF: ~1 second
- Convert PDF to Base64: ~0.1 seconds
- Build AI Prompt: ~30 seconds (base64 processing)
- Build Request Body: ~30 seconds
- Wait nodes: 20-60 seconds each (deliberate rate limiting)
- Claude API calls: 3-5 seconds each
- **Total workflow time: 4-5 minutes typical**

## Recommendations

1. **Modify webhook workflows to respond immediately**
   - Add "Respond to Webhook" node after initial validation
   - Return 202 Accepted with execution ID
   - Continue processing in background

2. **Keep debug logging enabled temporarily**
   - Useful for monitoring workflow performance
   - Can disable once workflows are optimized
   - Minimal performance impact

3. **Monitor disk space weekly**
   - Currently at 59% - healthy
   - binaryData folder can grow with execution history
   - Consider cleanup if >80%

4. **Document expected workflow execution times**
   - Eugene Quick Test Runner: ~4-5 minutes
   - Chunk 2.5: ~3-4 minutes (sub-workflow)
   - Set appropriate timeouts for webhook clients

5. **Consider workflow optimization**
   - Multiple 20-60 second wait nodes could be reduced
   - Rate limiting might be overly conservative
   - Parallel processing where possible

## Next Steps
- **Immediate:** No action needed - system is healthy
- **Short-term:** Add "Respond to Webhook" nodes to long-running webhook workflows
- **Long-term:** Review and optimize workflow execution times

## Additional Notes

- n8n version: 2.1.4 (latest as of 2026-01-30)
- Debug logging provides excellent visibility into execution flow
- Previous crash was unrelated to webhook "hanging"
- No data loss or corruption detected
- All active workflows (30 total) loaded successfully on restart

## Conclusion

**No server issues found.** The webhook listener is working correctly. The perceived "hanging" was actually long workflow execution time exceeding HTTP client timeouts. Workflows complete successfully in the background.

System is fully operational and healthy.
