# n8n Test Report - Fathom Transcript Workflow Final

**Workflow ID:** cMGbzpq1RXpL0OHY
**Workflow Name:** Fathom Transcript Workflow Final_22.01.26
**Test Date:** 2026-01-29
**Tester:** test-runner-agent

---

## Summary

- **Total Tests:** 1
- **Passed:** 0
- **Failed:** 1

---

## Test Details

### Test: Webhook Trigger with AI Analysis

**Status:** FAIL

**Execution ID:** 6795
**Trigger Type:** Webhook
**Duration:** 36 seconds
**Final Status:** error

---

## Execution Flow

The workflow executed the following nodes successfully before failing:

1. **Webhook Trigger** → SUCCESS
2. **Route: Webhook or API** → SUCCESS (23ms)
3. **IF: Webhook or API?1** → SUCCESS (3ms)
4. **Enhanced AI Analysis** → SUCCESS (7ms, 3 items output)
5. **Call AI for Analysis** → SUCCESS (13.8s, but returned error responses)
6. **Parse AI Response** → FAIL (917ms)

---

## Root Cause Analysis

### Primary Error

**Node:** Parse AI Response
**Error Message:** "No content found in AI response (tried Anthropic and OpenAI formats)"
**Line:** 21 in Code node

### Upstream Issue

**Node:** Call AI for Analysis
**Type:** @n8n/n8n-nodes-langchain.openAi
**Issue:** AI node returned error responses instead of analysis

**Sample Error Output:**
```json
{
  "error": "Bad request - please check your parameters"
}
```

This error was returned for all 3 items processed.

---

## Detailed Findings

### 1. AI Node Configuration Issue

The "Call AI for Analysis" node is configured but returning "Bad request" errors. This indicates one or more of the following problems:

**Possible Causes:**
- Missing or invalid API credentials
- Incorrect model selection
- Malformed prompt/input
- Missing required parameters
- API quota/rate limit exceeded

**Evidence:**
- Node executed successfully (no connection/timeout errors)
- Returned structured error response: `{"error": "Bad request - please check your parameters"}`
- Execution time was normal (~13.8 seconds for 3 items)

### 2. Parse AI Response Node

The "Parse AI Response" code node expects AI-formatted responses in either:
- Anthropic format
- OpenAI format

But received error objects instead, causing the parsing to fail at line 21.

### 3. Workflow Validation Issues

The workflow has **2 critical errors** that will prevent future executions:

**Error 1: Save Transcript to Drive**
- Invalid operation value
- Must be one of: copy, createFromText, deleteFile, download, move, share, update, upload

**Error 2: Slack Notification**
- Invalid operation value
- Must be one of: delete, getPermalink, search, post, sendAndWait, update

These errors are in disabled branches currently, but would block execution if those paths were enabled.

### 4. Workflow Warnings (56 total)

Key warnings include:
- Outdated node versions (HTTP Request, Webhook, AI nodes)
- Deprecated `continueOnFail` usage (should use `onError`)
- Missing error handling on critical nodes
- Invalid `$` usage in code nodes
- Long linear chain (29 nodes - consider sub-workflows)

---

## Test Input

```json
{
  "meetingId": "test_12345",
  "title": "Test Meeting with Jane Smith",
  "startTime": "2026-01-29T10:00:00Z",
  "participants": ["Sway Clarke", "Jane Smith"],
  "transcript": "Sway Clarke: Hi Jane, thanks for joining today. I wanted to discuss your progress on the marketing campaign.\n\nJane Smith: Thanks Sway. I've been working hard on it. We launched the social media ads last week and already seeing a 15% increase in engagement.\n\nSway Clarke: That's excellent! How about the email campaign?\n\nJane Smith: The email campaign is ready to go. We've segmented the audience into three groups and personalized the messaging for each. I'm confident we'll see good results.\n\nSway Clarke: Great work. Any challenges you're facing?\n\nJane Smith: The biggest challenge is coordinating with the design team. They're a bit behind on the visual assets. I'm following up daily to keep things moving.\n\nSway Clarke: I'll reach out to them as well. Keep up the great work, Jane.\n\nJane Smith: Thanks Sway, I appreciate the support."
}
```

---

## What Worked

1. **Webhook routing** - Successfully detected webhook vs API source
2. **Data preprocessing** - "Enhanced AI Analysis" node prepared data correctly
3. **Node connections** - All connections executed in correct order
4. **Error capture** - Workflow properly captured and reported AI node errors

---

## What Failed

1. **AI Analysis** - "Call AI for Analysis" node returned "Bad request" errors
2. **Response parsing** - Failed to extract analysis from error responses
3. **End-to-end execution** - Did not reach Airtable save or Slack notification

---

## Required Fixes

### Critical (Must Fix)

1. **Configure AI Node Credentials**
   - Node: "Call AI for Analysis"
   - Action: Verify OpenAI API credentials are set and valid
   - Check: Model selection matches available models
   - Verify: API key has quota/permissions

2. **Fix AI Node Parameters**
   - Review prompt structure in "Enhanced AI Analysis"
   - Ensure all required fields are populated
   - Check variable references are valid

3. **Fix Google Drive Node**
   - Node: "Save Transcript to Drive"
   - Issue: Invalid operation value
   - Action: Select valid operation from dropdown

4. **Fix Slack Node**
   - Node: "Slack Notification"
   - Issue: Invalid operation value
   - Action: Select valid operation from dropdown

### High Priority (Should Fix)

1. **Update node versions**
   - HTTP Request nodes (4.3 → 4.4)
   - Webhook node (2 → 2.1)
   - AI nodes (1.8 → 2.1)

2. **Replace deprecated error handling**
   - Replace `continueOnFail: true` with `onError: 'continueRegularOutput'`
   - Affects: List Meetings, Get Transcript, Create/Get Folder, Save Transcript, AI nodes

3. **Add error handling**
   - Add `onError` to Webhook, Airtable, and Slack nodes
   - Consider error trigger for critical failures

### Medium Priority (Nice to Have)

1. Fix resource locator formats in Google Drive nodes
2. Add error handling to code nodes
3. Fix `$` usage in code nodes
4. Consider breaking into sub-workflows (current chain: 29 nodes)

---

## Next Steps

1. **Verify AI node configuration** in n8n UI:
   - Open "Call AI for Analysis" node
   - Check credentials are connected
   - Verify model selection (should be valid OpenAI model)
   - Test with simple prompt

2. **Fix Google Drive and Slack nodes**:
   - Select valid operations from dropdowns
   - Save workflow

3. **Re-test** with same test payload

4. **If AI node still fails**:
   - Check OpenAI dashboard for API usage/errors
   - Verify API key has permissions
   - Check if rate limits are exceeded
   - Review prompt format in "Enhanced AI Analysis"

---

## Expected Behavior (Once Fixed)

After fixing AI configuration:

1. Webhook receives meeting data
2. Enhanced AI Analysis prepares prompt
3. Call AI for Analysis returns:
   - Meeting type classification
   - Summary
   - Key topics
   - Action items
4. Parse AI Response extracts structured data
5. Build Performance Prompt creates second AI call
6. Call AI for Performance analyzes participant performance
7. Parse Performance Response extracts ratings
8. Extract Participant Names → Search Contacts → Search Clients
9. Prepare Airtable Data combines all analysis
10. Save to Airtable (Meetings table)
11. Save Performance to Airtable (Performance table)
12. Build Slack Blocks formats message
13. Slack Notification sends update
14. Prepare Date Folder Name → Create folder → Save transcript to Drive

---

## Conclusion

The workflow structure is sound and routing works correctly. The test failed due to **AI node configuration issues** causing "Bad request" errors. Once the AI credentials and parameters are properly configured, the workflow should complete successfully.

**Recommendation:** Focus on fixing the "Call AI for Analysis" node configuration as the immediate blocker, then address the Google Drive and Slack validation errors before enabling those branches.

---

**Generated by:** test-runner-agent
**Execution Time:** ~36 seconds
**Nodes Executed:** 6/39 (workflow stopped at error)
