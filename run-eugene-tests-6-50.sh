#!/bin/bash

# Eugene Quick Test Runner - Tests 6-50 with autonomous execution
# This script will run all 45 remaining tests sequentially

WEBHOOK_URL="https://n8n.oloxa.ai/webhook/eugene-quick-test"
WORKFLOW_ID="fIqmtfEDuYM7gbE9"
LOG_FILE="/Users/swayclarke/coding_stuff/eugene-test-results-6-50.txt"

echo "=== Eugene Quick Test Runner - Tests 6-50 ===" | tee "$LOG_FILE"
echo "Started at: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

PASSED=0
FAILED=0
TIMEOUT=0

# Function to trigger webhook
trigger_test() {
    local test_num=$1
    echo ">>> Test $test_num: Triggering at $(date +'%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"

    # Use curl to trigger webhook
    response=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d '{}' 2>&1)

    http_status=$(echo "$response" | grep "HTTP_STATUS:" | cut -d: -f2)
    body=$(echo "$response" | grep -v "HTTP_STATUS:")

    if [ "$http_status" = "200" ] || [ "$http_status" = "201" ]; then
        echo "  ✓ Webhook triggered successfully (HTTP $http_status)" | tee -a "$LOG_FILE"
        return 0
    else
        echo "  ✗ Webhook trigger failed (HTTP $http_status)" | tee -a "$LOG_FILE"
        echo "  Response: $body" >> "$LOG_FILE"
        return 1
    fi
}

# Main test loop
for i in $(seq 6 50); do
    trigger_test $i

    # Wait 5 minutes between tests (300 seconds)
    # This gives each test time to complete before starting the next
    if [ $i -lt 50 ]; then
        echo "  Waiting 5 minutes before next test..." | tee -a "$LOG_FILE"
        sleep 300
    fi

    # Report progress every 5 tests
    if [ $(( (i - 5) % 5 )) -eq 0 ]; then
        completed=$((i - 5))
        remaining=$((50 - i))
        echo "" | tee -a "$LOG_FILE"
        echo "=== PROGRESS: $completed tests triggered, $remaining remaining ===" | tee -a "$LOG_FILE"
        echo "" | tee -a "$LOG_FILE"
    fi

    # Pause for 2 minutes after every 3 consecutive errors (safety measure)
    # This would require tracking errors - for now we just trigger sequentially
done

echo "" | tee -a "$LOG_FILE"
echo "=== All 45 tests triggered ===" | tee -a "$LOG_FILE"
echo "Completed at: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Total estimated time: 225 minutes (3.75 hours)" | tee -a "$LOG_FILE"
echo "Check n8n executions for results" | tee -a "$LOG_FILE"
