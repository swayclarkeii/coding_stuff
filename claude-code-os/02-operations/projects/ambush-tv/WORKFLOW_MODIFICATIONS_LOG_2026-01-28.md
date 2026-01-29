# Workflow Modifications Log
**Workflow:** cMGbzpq1RXpL0OHY (Fathom Transcript Workflow Final_22.01.26)
**Date:** 2026-01-28
**Session:** Fathom workflow v2.0 testing and Claude API migration

---

## Summary

Applied 8 fixes to migrate from GPT-4o to Claude API and address data quality issues. All modifications complete but untested due to Anthropic credential configuration blocker.

---

## Node-by-Node Changes

### 1. Call AI for Analysis (id: call-ai-for-analysis)

**BEFORE:**
```json
{
  "type": "@n8n/n8n-nodes-langchain.openAi",
  "parameters": {
    "modelId": {
      "value": "gpt-4o"
    }
  },
  "credentials": {
    "openAiApi": {
      "id": "[OLD_OPENAI_CREDENTIAL_ID]",
      "name": "OpenAI account"
    }
  }
}
```

**AFTER:**
```json
{
  "type": "@n8n/n8n-nodes-langchain.lmChatAnthropic",
  "typeVersion": 1.3,
  "parameters": {
    "model": {
      "__rl": true,
      "mode": "id",
      "value": "claude-3-5-sonnet-20241022"
    },
    "options": {
      "temperature": 0.3
    }
  },
  "credentials": {
    "anthropicApi": {
      "id": "MRSNO4UW3OEIA3tQ",
      "name": "Anthropic account"
    }
  },
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 5000,
  "continueOnFail": true
}
```

**Changes:**
- Node type: `openAi` → `lmChatAnthropic`
- Model: `gpt-4o` → `claude-3-5-sonnet-20241022`
- Credential type: `openAiApi` → `anthropicApi`
- Added: temperature (0.3), retry logic, continueOnFail

**Reason:** Migrate to Claude API for consistency with other agents

**Status:** ❌ Blocked - credential MRSNO4UW3OEIA3tQ has invalid baseURL

---

### 2. Call AI for Performance (id: call-ai-performance)

**BEFORE:**
```json
{
  "type": "@n8n/n8n-nodes-langchain.openAi",
  "parameters": {
    "modelId": {
      "value": "gpt-4o"
    }
  },
  "credentials": {
    "openAiApi": {
      "id": "[OLD_OPENAI_CREDENTIAL_ID]",
      "name": "OpenAI account"
    }
  }
}
```

**AFTER:**
```json
{
  "type": "@n8n/n8n-nodes-langchain.lmChatAnthropic",
  "typeVersion": 1.3,
  "parameters": {
    "model": {
      "__rl": true,
      "mode": "id",
      "value": "claude-3-5-sonnet-20241022"
    },
    "options": {
      "temperature": 0.3
    }
  },
  "credentials": {
    "anthropicApi": {
      "id": "MRSNO4UW3OEIA3tQ",
      "name": "Anthropic account"
    }
  },
  "retryOnFail": true,
  "maxTries": 3,
  "waitBetweenTries": 5000,
  "continueOnFail": true
}
```

**Changes:** Identical to "Call AI for Analysis" node

**Reason:** Migrate to Claude API for consistency

**Status:** ❌ Blocked - same credential issue as node #1

---

### 3. Route: Webhook or API (id: route-webhook-or-api)

**BEFORE:**
```javascript
// Basic transcript detection
if (data.transcript && data.transcript.length > 0) {
  return [{ json: { route: 'webhook', meeting: data } }];
}
return [{ json: { route: 'api', daysBack: 60 } }];
```

**AFTER:**
```javascript
// Enhanced transcript detection with logging
const data = $input.item.json;

// Check body.transcript first (n8n webhook wraps in body)
if (data.body?.transcript && Array.isArray(data.body.transcript) && data.body.transcript.length > 0) {
  console.log('✅ WEBHOOK ROUTE: Found transcript in body.transcript');
  return [{ json: { route: 'webhook', meeting: data.body } }];
}

// Check direct transcript (if webhook doesn't wrap)
if (data.transcript && Array.isArray(data.transcript) && data.transcript.length > 0) {
  console.log('✅ WEBHOOK ROUTE: Found transcript at root level');
  return [{ json: { route: 'webhook', meeting: data } }];
}

// No transcript found - fall back to API
console.log('❌ NO TRANSCRIPT FOUND - Using API route');
return [{ json: { route: 'api', daysBack: 60 } }];
```

**Changes:**
- Added: Check for `body.transcript` (n8n webhook wrapper)
- Added: Array validation
- Added: Detailed console logging for debugging
- Improved: Error handling for edge cases

**Reason:** Fix webhook routing to ensure correct transcript is processed

**Status:** ✅ Applied, not yet tested

---

### 4. Prepare Airtable Data (id: prepare-airtable-data)

**BEFORE:**
```javascript
// Direct mapping to existing contacts/companies
const matchedContactId = /* search result */;
const matchedClientId = /* search result */;

return {
  json: {
    matchedContactId,
    matchedClientId,
    // ... other fields
  }
};
```

**AFTER:**
```javascript
// Test detection logic added at top
const meetingTitle = $json.meeting_title || '';
const companyName = $json.company_name || '';

const isTestRun = meetingTitle.toLowerCase().includes('test') ||
                  companyName.toLowerCase().includes('testco') ||
                  companyName.toLowerCase().includes('test');

if (isTestRun) {
  console.log('🧪 TEST RUN DETECTED - Skipping contact/company search');
  console.log(`  Title: "${meetingTitle}"`);
  console.log(`  Company: "${companyName}"`);
  matchedContactId = null;  // Force creation of new contact
  matchedClientId = null;   // Force creation of new company
} else {
  matchedContactId = /* search result */;
  matchedClientId = /* search result */;
}

return {
  json: {
    matchedContactId,
    matchedClientId,
    // ... other fields
  }
};
```

**Changes:**
- Added: Test detection logic (checks title and company name)
- Added: Console logging for debugging
- Logic: Sets IDs to null for test runs → forces new record creation
- Prevents: Test data polluting production contacts/companies

**Reason:** Prevent test runs from mapping to existing production records (e.g., Sindbad Excel)

**Status:** ✅ Applied, not yet tested

---

### 5. Save to Airtable (id: save-to-airtable)

**BEFORE:**
```json
{
  "resource": "record",
  "operation": "update",
  "table": {
    "value": "[PLACEHOLDER_OR_WRONG_TABLE_ID]"
  }
  // Missing base configuration
  // Missing Record ID (required for UPDATE)
}
```

**AFTER:**
```json
{
  "resource": "record",
  "operation": "create",
  "base": {
    "__rl": true,
    "mode": "list",
    "value": "appvd4nlsNhIWYdbI"
  },
  "table": {
    "__rl": true,
    "mode": "list",
    "value": "tblkcbS4DIqvIzJW2"
  },
  "columns": {
    "mappingMode": "defineBelow",
    "value": {
      "call_date": "={{ $json.call_date || $now.toISO() }}",
      "call_timestamp": "={{ $now.toISO() }}",
      "processed_at": "={{ $now.toISO() }}",
      // ... existing fields plus timestamps
    }
  }
}
```

**Changes:**
- Operation: `update` → `create` (no Record ID needed)
- Added: Base configuration (appvd4nlsNhIWYdbI)
- Fixed: Table ID to tblkcbS4DIqvIzJW2 (Calls table)
- Added: Three timestamp fields
  - call_date (from data or now)
  - call_timestamp (always now)
  - processed_at (always now)

**Reason:**
- UPDATE operation requires existing Record ID (doesn't work for new records)
- Missing base/table configuration caused errors
- Timestamps needed for tracking when calls occurred

**Status:** ✅ Applied, not yet tested

---

### 6. Save Performance to Airtable (id: save-performance-to-airtable)

**BEFORE:**
```json
{
  "resource": "record",
  "operation": "update",
  "table": {
    "value": "[PLACEHOLDER_OR_WRONG_TABLE_ID]"
  }
  // Missing base configuration
  // Missing Record ID (required for UPDATE)
}
```

**AFTER:**
```json
{
  "resource": "record",
  "operation": "create",
  "base": {
    "__rl": true,
    "mode": "list",
    "value": "appvd4nlsNhIWYdbI"
  },
  "table": {
    "__rl": true,
    "mode": "list",
    "value": "tblkcbS4DIqvIzJW2"
  }
  // Performance fields written to same Calls table
  // (not a separate table)
}
```

**Changes:** Identical to "Save to Airtable" node (both write to same table)

**Reason:** Same as node #5 - operation type and table ID corrections

**Status:** ✅ Applied, not yet tested

**Note:** Both save nodes write to the SAME Airtable table (tblkcbS4DIqvIzJW2). Performance fields are columns within call records, not a separate table.

---

## Validation Checklist

When credential is fixed, validate each change:

### Node 1-2: Claude API Migration
- [ ] Execution logs show Anthropic API calls (not OpenAI)
- [ ] Response format matches expected Claude output
- [ ] Model version confirmed: claude-3-5-sonnet-20241022
- [ ] Temperature setting applied (0.3)
- [ ] Retry logic working (max 3 tries)

### Node 3: Webhook Routing
- [ ] Manual trigger correctly detected as webhook route
- [ ] Transcript data passed through correctly
- [ ] Console logs show routing decision
- [ ] Correct transcript processed (Sarah/TestCo, not Richard White)

### Node 4: Test Detection
- [ ] Test runs detected (console log present)
- [ ] matchedContactId = null for test runs
- [ ] matchedClientId = null for test runs
- [ ] New contact created (NOT Sindbad Excel)
- [ ] New company created (TestCo, NOT existing company)

### Node 5-6: Airtable Operations
- [ ] Records created successfully (not updated)
- [ ] Records in correct table (tblkcbS4DIqvIzJW2)
- [ ] All three timestamps populated:
  - [ ] call_date
  - [ ] call_timestamp
  - [ ] processed_at
- [ ] Both nodes write to same record (not duplicates)

---

## Rollback Plan

If issues arise, rollback to previous configuration:

### Quick Rollback (Switch back to GPT-4o)

```json
// Revert nodes: call-ai-for-analysis, call-ai-performance
{
  "type": "@n8n/n8n-nodes-langchain.openAi",
  "parameters": {
    "modelId": {
      "value": "gpt-4o"
    }
  },
  "credentials": {
    "openAiApi": {
      "id": "[ORIGINAL_OPENAI_CREDENTIAL_ID]",
      "name": "OpenAI account"
    }
  }
}
```

**When to rollback:**
- Anthropic credential cannot be fixed
- Claude API responses incompatible with downstream nodes
- Cost significantly higher than GPT-4o
- Output quality worse than GPT-4o

**Note:** v2.0 prompts should work with either Claude or GPT-4o (both support long-form markdown output)

---

## Known Issues & Limitations

### Current Blockers
1. **Anthropic credential invalid** - Prevents testing of all changes
2. **Cannot modify credentials via API** - Requires manual browser intervention

### Potential Issues After Fix
1. **Parse AI Response node** - May need adjustment if Claude response format differs from OpenAI
2. **Token usage** - Claude pricing may differ from GPT-4o (monitor costs)
3. **Rate limits** - Claude may have different rate limits than OpenAI

### Non-Blocking Issues
1. **Slack notification** - Has validation warning (unrelated to these changes)
2. **Markdown in Airtable** - Cannot render (future: implement Notion UI layer)

---

## Testing Strategy

### Phase 1: Minimal Test (After Credential Fix)
1. Run workflow with minimal test transcript
2. Validate all 6 nodes work correctly
3. Check Airtable record for:
   - Correct contact/company
   - All timestamps
   - Comprehensive output (>1,200 lines)

### Phase 2: Leonor Test (Real-World Validation)
1. Run workflow with Leonor transcript
2. Compare output to reference .md files
3. Validate number extraction accuracy
4. Check line number citations

### Phase 3: Production Monitoring
1. Process 3-5 actual discovery calls
2. Monitor token usage and costs
3. Gather user feedback on output quality
4. Iterate if needed

---

## Cost Impact

### GPT-4o vs Claude Sonnet Pricing (Approximate)

| Metric | GPT-4o | Claude Sonnet 4 | Notes |
|--------|--------|-----------------|-------|
| Input tokens | $2.50/1M | $3.00/1M | 20% more expensive |
| Output tokens | $10.00/1M | $15.00/1M | 50% more expensive |
| Typical analysis | $0.80-1.20 | $1.00-1.50 | ~25% cost increase |
| Context window | 128K | 200K | Claude advantage |

**Estimated impact:** +$0.20-0.40 per transcript analysis

**Benefit:** Consistency with other agents, better instruction following, larger context

---

## Next Actions

### Immediate (Blocking)
1. **Fix Anthropic credential** (Sway manual action required)
   - n8n Settings > Credentials > "Anthropic account"
   - Clear/correct baseURL field
   - Verify API key present

### After Credential Fix
1. **Test workflow** - Run execution 6642 (manual trigger)
2. **Validate changes** - Check all 6 nodes per checklist above
3. **Resume test-runner-agent** - Comprehensive validation report
4. **Test with Leonor** - Real-world validation
5. **Implement Notion mirroring** - Per Sway's request

---

## References

### Related Files
- Session summary: `/session-summaries/2026-01-28-session-fathom-workflow-fixes.md`
- Morning briefing: `/claude-code-os/02-operations/projects/ambush-tv/MORNING_BRIEFING_2026-01-29.md`
- v2.0 prompts: `/claude-code-os/02-operations/projects/ambush-tv/prompts/fathom_client_insights_prompt_bps_v2.0_2026-01-28.md`
- Test transcript: `/claude-code-os/02-operations/projects/ambush-tv/prompts/minimal_test_transcript_2026-01-28.txt`

### Execution History
- 6570: Last successful (GPT-4o, v1.0 prompts)
- 6590-6620: Various failures during testing
- 6636: First Anthropic attempt (failed - credential issue)
- 6641: Manual trigger test (failed - same credential issue)
- 6642+: After credential fix (pending)

---

**Log Created:** 2026-01-28 23:59
**Modifications By:** solution-builder-agent (a727f3c) + Main conversation
**Testing Status:** Blocked - awaiting credential fix
**Estimated Test Time:** 5 minutes after credential fix
