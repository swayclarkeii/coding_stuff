# Brain Dump Database Updater v1.1 - 4 Tasks Test Report

**Date:** 2026-01-19
**Workflow ID:** UkmpBjJeItkYftS9
**Workflow Name:** Brain Dump Database Updater v1.1
**Execution ID:** 4539
**Test Type:** Task creation with 4 real tasks from Sway's weekly brain dump

---

## Executive Summary

**Total tests executed:** 1 (4 tasks in single payload)
**Tasks created:** 4 (but with critical data quality issues)
**Test Result:** PARTIAL FAILURE

**Status:** Workflow successfully created 4 Notion tasks, but ALL task titles, priorities, types, and due dates are BLANK/NULL. The workflow has a critical field mapping bug in the "Create Notion Task" node.

**Comparison to Direct Notion MCP:** While direct Notion MCP has a parameter encoding bug that prevents task creation entirely, this workflow DOES create tasks, but with incomplete data. This is arguably worse - silent data loss instead of clear failure.

---

## Test Input

**Test Case:** Real weekly brain dump with 4 tasks

**Payload Structure:**
```json
{
  "crm": {},
  "tasks": [
    {
      "title": "Follow up with Benito (Lombok) for testimonial",
      "dueDate": "2026-01-22",
      "priority": "Medium",
      "type": "Work"
    },
    {
      "title": "Upload Sebastiao transcript + convert to text",
      "dueDate": "2026-01-20",
      "priority": "High",
      "type": "Work"
    },
    {
      "title": "Research recruitment/staffing AI niche",
      "dueDate": "2026-01-24",
      "priority": "Medium",
      "type": "Work"
    },
    {
      "title": "Complete Ambush TV proposal",
      "dueDate": "2026-01-21",
      "priority": "High",
      "type": "Work"
    }
  ],
  "projects": [],
  "calendar": {}
}
```

**Context:** These are real tasks from Sway's weekly brain dump. The Lombok Capital project reference relates to a completed project.

---

## Execution Results

### Overall Execution

- **Execution ID:** 4539
- **Status:** success
- **Duration:** 3,559ms
- **Start:** 2026-01-19T18:27:02.037Z
- **End:** 2026-01-19T18:27:05.596Z
- **Trigger:** Webhook (POST to /webhook/brain-dump)

### Workflow Response

```json
{
  "status": "success",
  "summary": {
    "crm": "No CRM updates",
    "tasks": "Created 1 tasks",
    "projects": "No project updates",
    "calendar": "No calendar events"
  },
  "errors": []
}
```

**ISSUE 1:** Response says "Created 1 tasks" but actually created 4 tasks. The summary count is incorrect.

---

## Node-by-Node Analysis

### 1. Webhook Trigger
- **Status:** Success
- **Execution Time:** 1ms
- **Items Output:** 1
- **Payload Received:** All 4 tasks with complete data (titles, dates, priorities, types)

### 2. Parse & Validate Input
- **Status:** Success
- **Execution Time:** 24ms
- **Items Output:** 1
- **Validation:** Passed - recognized 4 tasks with correct structure
- **Output:** Correctly parsed all 4 tasks with all fields intact

### 3. Split By Update Type
- **Status:** Success
- **Execution Time:** 35ms
- **Items Output:** 1
- **Routing:** Correctly identified tasks branch for processing

### 4. Route Tasks
- **Status:** Success
- **Execution Time:** Not specified
- **Items Output:** 1 (routed to Process Tasks)

### 5. Process Tasks
- **Status:** Success
- **Execution Time:** 22ms
- **Items Input:** 1
- **Items Output:** 4 (correctly split into 4 separate task items)
- **Data Quality:** All 4 items have correct priority and type values
- **Sample Output:**
```json
[
  {"operation": "create", "status": "To-do", "priority": "Medium", "type": "Work"},
  {"operation": "create", "status": "To-do", "priority": "High", "type": "Work"},
  {"operation": "create", "status": "To-do", "priority": "Medium", "type": "Work"},
  {"operation": "create", "status": "To-do", "priority": "High", "type": "Work"}
]
```

**OBSERVATION:** This node correctly split the tasks but the output doesn't show titles or due dates. This suggests the "Process Tasks" code node might not be passing these fields forward.

### 6. Task Is Delete?
- **Status:** Success
- **Routed to:** Create path (not delete)

### 7. Create Notion Task
- **Status:** Success (but with data quality issues)
- **Execution Time:** 3,393ms (majority of workflow time)
- **Items Input:** 4
- **Items Output:** 4
- **Notion Database:** 39b8b725-0dbd-4ec2-b405-b3bba0c1d97e
- **Tasks Created:**

| Task # | Notion ID | Title | Priority | Type | Due Date | Status |
|--------|-----------|-------|----------|------|----------|--------|
| 1 | 2ed1c288-bb28-8177-ad5d-c4be12e10b0c | BLANK | NULL | NULL | NULL | To-do |
| 2 | 2ed1c288-bb28-812c-a68bdd2336c70a4b | BLANK | NULL | NULL | NULL | To-do |
| 3 | 2ed1c288-bb28-810086e3fb00f2f7cd21 | BLANK | NULL | NULL | NULL | To-do |
| 4 | 2ed1c288-bb288197ba2de6c39bf1e10f | BLANK | NULL | NULL | NULL | To-do |

**URLs:**
- https://www.notion.so/2ed1c288bb288177ad5dc4be12e10b0c
- https://www.notion.so/2ed1c288bb28812ca68bdd2336c70a4b
- https://www.notion.so/2ed1c288bb28810086e3fb00f2f7cd21
- https://www.notion.so/2ed1c288bb288197ba2de6c39bf1e10f

**CRITICAL ISSUE:** All 4 tasks were created in Notion, but with completely blank/null data:
- `property_name`: "" (empty - should be task titles)
- `property_priority`: null (should be "Medium" or "High")
- `property_type`: null (should be "Work")
- `property_when`: null (should be due dates: 2026-01-22, 2026-01-20, 2026-01-24, 2026-01-21)
- `property_status`: "To-do" (correct)
- `property_complete`: false (correct)

### 8. Log Task Result
- **Status:** Success
- **Execution Time:** 22ms
- **Items Input:** 4
- **Items Output:** 1 (SHOULD BE 4)
- **Message:** "Created task: undefined"

**ISSUE 2:** This node aggregated 4 tasks into 1 log item, losing the count. Also, the task title shows as "undefined", confirming titles were not mapped.

### 9. Merge All Results
- **Status:** Success
- **Execution Time:** 2ms
- **Items Output:** 1

### 10. Build Response
- **Status:** Success
- **Execution Time:** 24ms
- **Output:** Generated response summary with incorrect count ("Created 1 tasks")

### 11. Respond to Webhook
- **Status:** Error (but response was sent successfully)
- **Error Message:** "Unknown error"
- **Note:** This is a known harmless error - the webhook response was delivered despite the error status.

---

## Critical Bugs Identified

### Bug 1: Field Mapping in "Create Notion Task" Node

**Severity:** CRITICAL
**Impact:** 100% data loss for task titles, priorities, types, and due dates

**Root Cause:** The "Create Notion Task" node is not correctly mapping input fields to Notion database properties:

| Input Field | Expected Notion Property | Actual Result |
|-------------|-------------------------|---------------|
| `title` | `property_name` (Name) | Empty string "" |
| `priority` | `property_priority` (Priority) | null |
| `type` | `property_type` (Type) | null |
| `dueDate` | `property_when` (When) | null |

**Expected Behavior:**
- Task 1 should have name "Follow up with Benito (Lombok) for testimonial", priority "Medium", type "Work", due date "2026-01-22"
- Task 2 should have name "Upload Sebastiao transcript + convert to text", priority "High", type "Work", due date "2026-01-20"
- Etc.

**Actual Behavior:**
- All tasks created with blank names and null metadata
- Only status ("To-do") and complete (false) fields populated correctly

**Suspected Cause:**
The "Process Tasks" code node might not be outputting the `title`, `dueDate`, `priority`, and `type` fields in its output, OR the "Create Notion Task" node has incorrect field mapping expressions.

### Bug 2: Incorrect Task Count in Summary

**Severity:** MEDIUM
**Impact:** Misleading feedback to user

**Root Cause:** The "Log Task Result" node aggregates 4 task items into 1 log item, causing the count to be lost.

**Expected:** "Created 4 tasks"
**Actual:** "Created 1 tasks"

### Bug 3: Task Title Shows as "undefined"

**Severity:** HIGH
**Impact:** Confirms field mapping issue

**Evidence:** Log message says "Created task: undefined" instead of showing actual task titles.

---

## Comparison: n8n Workflow vs Direct Notion MCP

| Aspect | n8n Workflow | Direct Notion MCP | Winner |
|--------|--------------|-------------------|--------|
| **Task Creation** | Creates tasks (4/4) | Fails completely due to encoding bug | n8n Workflow |
| **Data Quality** | All fields blank/null | N/A (doesn't create) | Neither |
| **Error Visibility** | Silent data loss (says "success") | Clear failure with error message | Direct MCP |
| **Usability** | Unusable - creates junk data | Unusable - can't create at all | Neither |
| **Overall Result** | WORSE (silent corruption) | BETTER (fails clearly) | Direct MCP |

**Conclusion:** The n8n workflow is actually WORSE than the broken direct Notion MCP approach, because it silently creates corrupt data instead of failing clearly. Users won't know their tasks are broken until they check Notion and find blank entries.

---

## Test Cleanup Required

**Action:** Delete 4 junk Notion tasks created by this test

**Notion Database:** Tasks (39b8b725-0dbd-4ec2-b405-b3bba0c1d97e)
**Link:** https://www.notion.so/889fff971c29490ba57c322c0736e90a

**Tasks to Delete:**
1. https://www.notion.so/2ed1c288bb288177ad5dc4be12e10b0c (blank task, created 2026-01-19 18:27:00 UTC)
2. https://www.notion.so/2ed1c288bb28812ca68bdd2336c70a4b (blank task, created 2026-01-19 18:27:00 UTC)
3. https://www.notion.so/2ed1c288bb28810086e3fb00f2f7cd21 (blank task, created 2026-01-19 18:27:00 UTC)
4. https://www.notion.so/2ed1c288bb288197ba2de6c39bf1e10f (blank task, created 2026-01-19 18:27:00 UTC)

**Filter:** All 4 tasks have:
- Name: (blank)
- Status: To-do
- Created: 2026-01-19T18:27:00.000Z

---

## Recommendations

### Immediate Actions Required

1. **DO NOT USE this workflow for task creation** until field mapping is fixed
2. **Delete the 4 junk tasks** from Notion Tasks database
3. **Fix "Process Tasks" node** to ensure it outputs all required fields:
   - Verify the code outputs `title`, `dueDate`, `priority`, `type`
   - Check field name consistency (title vs taskTitle, etc.)

4. **Fix "Create Notion Task" node** field mappings:
   - Map input `title` field to Notion "Name" property
   - Map input `priority` field to Notion "Priority" property
   - Map input `type` field to Notion "Type" property
   - Map input `dueDate` field to Notion "When" property
   - Ensure date format is compatible with Notion (ISO 8601)

5. **Fix "Log Task Result" node** to preserve item count:
   - Change aggregation mode to preserve 4 separate items
   - OR update summary calculation to count correctly
   - Fix task title extraction (currently shows "undefined")

### Verification Tests After Fix

**Test 1:** Single task creation
- Input: 1 task with all fields
- Expected: 1 task in Notion with correct title, priority, type, due date

**Test 2:** Multiple tasks creation
- Input: 3-4 tasks with varied data
- Expected: All tasks created with correct data, summary shows correct count

**Test 3:** Edge cases
- Input: Tasks with missing optional fields (no priority, no due date)
- Expected: Tasks created with available data, no errors

---

## Context: Why This Test Was Run

Sway requested this test to compare the n8n brain dump workflow against direct Notion MCP (which has a known parameter encoding bug). The goal was to determine if the workflow approach is more reliable.

**Key Finding:** The workflow does NOT solve the Notion integration problem. While it avoids the encoding bug by using a different code path, it introduces a worse bug: silent data corruption.

**Strategic Recommendation:**
- Option A: Fix the field mapping bugs in this workflow (2-3 node updates required)
- Option B: Fix the parameter encoding bug in Claude Code's Notion MCP integration (root cause fix)
- Option C: Use my-pa-agent which may have different Notion handling

Given the complexity of this workflow (53 nodes, 52 connections), Option B or C might be more maintainable long-term.

---

## Technical Notes

### Workflow Complexity
- **Total Nodes:** 53
- **Total Connections:** 52
- **Branches:** 4 (CRM, Tasks, Projects, Calendar)
- **Notion Integration Points:** 8 nodes across Tasks and Projects branches

### Performance
- **Total Duration:** 3,559ms
- **Notion API Time:** 3,393ms (95% of total time)
- **Processing Time:** 166ms (5% of total time)

The workflow is performant - most time is spent waiting for Notion API responses, which is expected.

### Previous Test History

Based on earlier test report (FINAL-VERIFICATION-REPORT.md):
- **Test 1 (CRM):** PASSED - Google Sheets integration working
- **Test 2 (Tasks):** FAILED - 404 database access error
- **Test 3 (Projects):** FAILED - Validation error

**Status Change:** Test 2 (Tasks) previously failed with 404 error (database not accessible). This test shows the database IS now accessible (tasks were created), but field mapping is broken.

**Possible Cause:** Database sharing was fixed between previous test and this test, but the field mapping issue was always present and masked by the 404 error.

---

## Conclusion

**Test Result:** PARTIAL FAILURE

The Brain Dump Database Updater v1.1 workflow successfully:
- Accepts webhook payloads
- Validates input structure
- Routes to correct branch (tasks)
- Connects to Notion database
- Creates 4 tasks in Notion

But critically fails to:
- Map task titles to Notion name field (100% data loss)
- Map priorities to Notion priority field (100% data loss)
- Map types to Notion type field (100% data loss)
- Map due dates to Notion when field (100% data loss)
- Report correct task count in summary

**Is this better than direct Notion MCP?** NO. Silent data corruption is worse than clear failure.

**Can this be fixed?** YES. Field mapping fixes in 2-3 nodes should resolve all issues.

**Should Sway use this workflow?** NOT YET. Wait for field mapping fixes and re-test.

---

**Report Generated:** 2026-01-19 19:30 CET
**Test Runner:** test-runner-agent
**Agent ID:** (to be assigned)
**Next Steps:** Fix field mappings in Process Tasks and Create Notion Task nodes, then retest with same payload
