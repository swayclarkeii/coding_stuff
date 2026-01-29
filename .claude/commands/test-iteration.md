# /test-iteration - Resilient Batch Test Runner

Run N tests against an n8n workflow, monitor progress, diagnose errors, handle stalls, and report accuracy. Self-healing: detects failures, skips bad inputs, retries on transient errors, and keeps going until all tests are done.

## Usage
```
/test-iteration [workflow-id or name] [number-of-tests]
/test-iteration [workflow-id] [N] resume from [M]
/test-iteration [workflow-id] [N] with [options]
```

## Examples
```
/test-iteration Eugene Quick Test Runner 50
/test-iteration fIqmtfEDuYM7gbE9 50 resume from 5
/test-iteration Eugene Quick Test Runner 50 skip Schloßberg
/test-iteration fIqmtfEDuYM7gbE9 20 with results sheet Test_Results_Iteration5
```

## What This Command Does

1. **Parse & Validate**
   - Identify workflow by ID or name
   - Set total test count (default: 50)
   - Check for resume point or skip list
   - Verify workflow has webhook trigger and is active

2. **Run Test Loop**
   - Fire webhook for each test
   - Wait for execution to complete (poll n8n executions, don't just sleep)
   - Check execution result: success or error
   - Log result to progress tracker

3. **Handle Errors (Self-Healing)**
   - **Transient error** (API timeout, network): retry up to 2 times
   - **Bad input** (same file fails twice): add to skip list, fire next test
   - **Workflow error** (JSON parse, node failure): log error details, continue
   - **Stall** (no execution completes in 15 min): alert and retry

4. **Track Progress**
   - Maintain running count: passed / failed / skipped / remaining
   - Update progress every 5 tests
   - Write progress to scratchpad log file

5. **Report Results**
   - Final accuracy: passed / total
   - Error breakdown by type
   - List of skipped/failed files
   - Comparison to previous iteration if available
   - Link to results sheet

## Arguments

- `$ARGUMENTS` - Workflow ID or name, test count, optional resume point, optional skip list

## Instructions for Claude

When this command is invoked:

1. **Parse the request**:
   - Extract workflow reference (ID or name like "Eugene Quick Test Runner")
   - Extract test count N (default: 50)
   - Extract resume point if "resume from M" specified
   - Extract skip list if "skip [filename]" specified
   - Extract results sheet name if specified

2. **Resolve workflow**:
   - If ID: use directly
   - If name: search known workflows or use `mcp__n8n-mcp__n8n_list_workflows`
   - Known mappings:
     - "Eugene Quick Test Runner" = `fIqmtfEDuYM7gbE9`
     - Webhook URL: `https://n8n.oloxa.ai/webhook/eugene-quick-test`
   - Verify workflow is active via `mcp__n8n-mcp__n8n_get_workflow(id, mode="minimal")`

3. **Determine current progress** (for resume):
   - If "resume from M": start from test M
   - If no resume specified: check the results Google Sheet to count existing rows
     - Eugene results sheet: `12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I`
     - Read the iteration tab to count completed tests
     - Also check `mcp__n8n-mcp__n8n_executions(action="list", workflowId="[id]", limit=10)` for recent activity
   - Calculate: start_from = existing_completed_tests + 1

4. **Initialize tracking**:
   ```
   Create scratchpad log file:
   /private/tmp/claude-501/-Users-swayclarke-coding-stuff/[session]/scratchpad/iteration_test_run.log

   Initialize counters:
   - passed = 0
   - failed = 0
   - skipped = 0
   - errors_by_type = {}
   - skip_list = [user-provided files]
   - failed_files = []  (files that error - track to detect repeats)
   ```

5. **Run the test loop**:
   ```
   For test_number from start_from to N:

     a. FIRE TEST:
        - Use mcp__n8n-mcp__n8n_test_workflow OR curl via Bash:
          curl -X POST "[webhook_url]" -H "Content-Type: application/json" -d '{}'

     b. WAIT FOR COMPLETION (smart polling, not blind sleep):
        - Wait 30 seconds initial
        - Then poll every 60 seconds:
          mcp__n8n-mcp__n8n_executions(action="list", workflowId="[id]", limit=1)
        - Check if latest execution started AFTER our webhook fire time
        - If execution status = "success": proceed to step c
        - If execution status = "error": proceed to step d
        - If no new execution after 5 minutes: fire again (retry)
        - If no new execution after 10 minutes: log stall, skip this test
        - MAX WAIT: 12 minutes per test

     c. ON SUCCESS:
        - passed += 1
        - Log: "[test_number/N] SUCCESS - Execution #[id]"

     d. ON ERROR:
        - Get error details:
          mcp__n8n-mcp__n8n_executions(action="get", id="[exec_id]", mode="error")
        - Extract: failed node, error message, file name
        - Classify error:
          * "Bad request" at Claude Vision → bad_input (file issue)
          * "Could not extract JSON" → json_parse_error
          * Timeout/network → transient_error
          * Other → unknown_error
        - If bad_input AND file already in failed_files → add to skip_list
        - If transient_error AND retries < 2 → retry this test
        - Otherwise: failed += 1, log error details, continue

     e. PROGRESS UPDATE (every 5 tests):
        - Print status:
          "[test_number/N] Progress: [passed] passed, [failed] failed, [skipped] skipped"
        - Write to log file

     f. STALL DETECTION:
        - If 3 consecutive errors → pause, diagnose, report to user
        - If same file fails 3+ times → add to skip_list permanently
   ```

6. **Handle known Eugene-specific patterns**:
   - `250814_Schloßberg 13.pdf` is a known bad file — if detected in errors, auto-skip
   - JSON parse errors from Claude wrapping response in markdown fences — log but continue (Chunk 2.5 issue, not test runner issue)
   - Random file picker may re-select same file — this is expected, not an error

7. **Final report** (when all N tests complete or max attempts exhausted):
   ```markdown
   ## Iteration Test Complete

   **Workflow**: [Name] (ID: [id])
   **Tests Run**: [passed + failed] / [N] ([skipped] skipped)

   ### Accuracy
   - **Passed**: [passed] ([percentage]%)
   - **Failed**: [failed]
   - **Skipped**: [skipped]

   ### Error Breakdown
   | Error Type | Count | Example File |
   |------------|-------|-------------|
   | [type] | [N] | [filename] |

   ### Skipped Files
   - [filename] - [reason]

   ### Comparison to Previous Iteration
   - Iteration [N-1]: [X]% accuracy
   - Iteration [N]: [Y]% accuracy
   - Delta: [+/-Z]%

   ### Results Sheet
   [Link to Google Sheet]

   ### Recommendations
   - [If accuracy >= 97.5%]: Ready for production deployment
   - [If accuracy < 97.5%]: Investigate [error types], consider Iteration [N+1]
   - [If specific files failing]: [File-specific recommendations]
   ```

8. **Save progress on interruption**:
   - If session is ending or user interrupts, immediately write current state:
     - Tests completed so far
     - Current counters
     - Skip list
     - Resume command for next session
   - Save to scratchpad AND print resume command:
     ```
     To resume: /test-iteration [workflow-id] [N] resume from [next_test_number]
     ```

## Key Rules

- **Real execution** - Each test triggers a real n8n workflow execution
- **Smart polling, not blind sleep** - Poll execution status instead of sleeping a fixed time
- **Self-healing** - Automatically retries transient errors, skips known-bad files
- **Never silently stall** - If no progress for 10+ minutes, report the issue
- **Resume-friendly** - Can pick up from where it left off
- **Autonomous** - Runs without asking permission until done or hitting an unrecoverable blocker
- **Progress visibility** - Updates every 5 tests so Sway can see what's happening
- **3 consecutive errors = pause** - Don't burn through all tests if something is systematically broken
