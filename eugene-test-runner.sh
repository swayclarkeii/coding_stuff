#!/bin/bash

# Eugene Quick Test Runner - Tests 6-50
WEBHOOK_URL="https://n8n.oloxa.ai/webhook/eugene-quick-test"
WORKFLOW_ID="fIqmtfEDuYM7gbE9"
START_TEST=6
END_TEST=50
LOG_FILE="/Users/swayclarke/coding_stuff/eugene-test-log.txt"

echo "=== Eugene Quick Test Runner - Tests $START_TEST to $END_TEST ===" > "$LOG_FILE"
echo "Started at: $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

PASSED=0
FAILED=0
TIMEOUT=0

for i in $(seq $START_TEST $END_TEST); do
    echo ">>> Test $i: Triggering webhook at $(date +%H:%M:%S)" | tee -a "$LOG_FILE"

    # Fire webhook
    RESPONSE=$(curl -s -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d '{}')
    echo "Response: $RESPONSE" >> "$LOG_FILE"

    # Wait 30 seconds initial
    sleep 30

    # Poll for up to 8 minutes (480 seconds total - 30 = 450 seconds remaining)
    # Check every 60 seconds = 7-8 checks max
    MAX_POLLS=8
    POLL_COUNT=0
    COMPLETED=false

    while [ $POLL_COUNT -lt $MAX_POLLS ]; do
        POLL_COUNT=$((POLL_COUNT + 1))
        echo "  Poll $POLL_COUNT for test $i at $(date +%H:%M:%S)" >> "$LOG_FILE"

        sleep 60

        # We'll manually check n8n via MCP after this script runs
        # For now just log the timing
    done

    echo "  Test $i: Polling timeout reached after 8 minutes" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"

    # Report every 5 tests
    if [ $((i % 5)) -eq 0 ]; then
        echo "=== Progress Report: Test $i completed ===" | tee -a "$LOG_FILE"
        echo "Tests run: $((i - START_TEST + 1)) / 45" | tee -a "$LOG_FILE"
        echo "" >> "$LOG_FILE"
    fi
done

echo "" >> "$LOG_FILE"
echo "=== All tests triggered ===" >> "$LOG_FILE"
echo "Completed at: $(date)" >> "$LOG_FILE"
