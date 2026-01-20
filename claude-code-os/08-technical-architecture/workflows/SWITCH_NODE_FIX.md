# CRITICAL: Switch Node Connection Fix

**Workflow**: AMA Pre-Chunk 0: Intake & Client Identification
**Issue**: Switch node has all 3 paths connected to same output - workflow stops after routing
**Fix Time**: 30 seconds in n8n UI

---

## The Problem

The "Route by Client Status" Switch node has all three downstream merge nodes connected to output[0] instead of being distributed across three separate outputs.

**Current (BROKEN)**:
```
Switch output[0] → All 3 nodes (NEW, EXISTING, UNKNOWN)
Switch output[1] → Nothing
Switch output[2] → Nothing
```

**When EXISTING client is detected**, Switch routes to output[1], but nothing is connected, so workflow stops.

**When UNKNOWN client is detected**, Switch routes to output[2], but nothing is connected, so workflow stops.

Only NEW clients work because they route to output[0].

---

## Manual Fix (30 seconds)

1. **Open workflow**: https://n8n.oloxa.ai/workflow/6MPoDSf8t0u8qXQq

2. **Click the "Route by Client Status" Switch node** to select it

3. **Look at the connection dots on the right side** - you'll see 3 labeled outputs:
   - NEW (top)
   - EXISTING (middle)
   - UNKNOWN (bottom)

4. **Delete ALL existing connections from Switch node**:
   - Right-click each connection line
   - Click "Delete"
   - Do this for all 3 connections

5. **Reconnect properly**:

   **From "NEW" output (top dot)**:
   - Drag to → "Merge File + Client Data (NEW)"

   **From "EXISTING" output (middle dot)**:
   - Drag to → "Merge File + Client Data (EXISTING)"

   **From "UNKNOWN" output (bottom dot)**:
   - Drag to → "Merge File + Unknowns Data"

6. **Save the workflow** (Cmd+S or Save button)

7. **Toggle workflow off and on** to reload cache

---

## Why This Happened

The Switch node v3.4 uses named outputs with `alwaysOutputData: false`. This means:
- When a condition matches, ONLY that specific output gets data
- Other outputs remain empty
- Each output MUST have its own separate connection

The MCP tools couldn't properly restructure this because the connection format is a nested array that needs exact structure.

---

## How to Verify Fix Worked

After reconnecting:

1. **Look at the connections** - you should see:
   - NEW output → one line to NEW merge
   - EXISTING output → one line to EXISTING merge
   - UNKNOWN output → one line to UNKNOWN merge

2. **Send a test email** with an EXISTING client (villa_martens)
   - Workflow should now complete all the way through
   - Should execute ~20+ nodes instead of stopping at 12

3. **Check execution** in n8n UI
   - Go to "Executions" tab
   - Latest execution should show SUCCESS
   - Should see nodes executed beyond the Switch

---

## Next Steps After Fix

1. ✅ Fix Switch connections (this)
2. Clear Master Client Registry (you mentioned doing this)
3. Send NEW client test to verify Chunk 0 registry fix
4. Fix email notification routing (UNKNOWN only)

---

**Status**: Ready to fix manually in UI
**Last Updated**: 2026-01-07T00:13:30+01:00
