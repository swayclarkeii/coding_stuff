#!/bin/bash

# Eugene Quick Test Runner - Rapid fire tests 6-50
# Triggers tests every 30 seconds, letting n8n handle concurrency

WEBHOOK_URL="https://n8n.oloxa.ai/webhook/eugene-quick-test"
LOG_FILE="/Users/swayclarke/coding_stuff/eugene-rapid-fire-log.txt"

echo "=== Eugene Rapid Fire Test Runner - Tests 6-50 ===" | tee "$LOG_FILE"
echo "Started at: $(date)" | tee -a "$LOG_FILE"
echo "Strategy: Fire every 30 seconds, let n8n handle parallel execution" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

SUCCESS=0
FAILED=0

for i in $(seq 6 50); do
    timestamp=$(date +'%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] Test $i: Triggering..." | tee -a "$LOG_FILE"

    # Trigger webhook
    http_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d '{}')

    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
        echo "  ✓ HTTP $http_code - Triggered" | tee -a "$LOG_FILE"
        SUCCESS=$((SUCCESS + 1))
    else
        echo "  ✗ HTTP $http_code - Failed" | tee -a "$LOG_FILE"
        FAILED=$((FAILED + 1))
    fi

    # Progress report every 5 tests
    if [ $(( (i - 5) % 5 )) -eq 0 ]; then
        completed=$((i - 5))
        remaining=$((50 - i))
        echo "" | tee -a "$LOG_FILE"
        echo ">>> PROGRESS: $completed/$45 tests triggered ($remaining remaining)" | tee -a "$LOG_FILE"
        echo "    Successful triggers: $SUCCESS, Failed: $FAILED" | tee -a "$LOG_FILE"
        echo "" | tee -a "$LOG_FILE"
    fi

    # Wait 30 seconds before next test (unless it's the last one)
    if [ $i -lt 50 ]; then
        sleep 30
    fi
done

echo "" | tee -a "$LOG_FILE"
echo "=== All 45 tests triggered ===" | tee -a "$LOG_FILE"
echo "Completed at: $(date)" | tee -a "$LOG_FILE"
echo "Total successful triggers: $SUCCESS" | tee -a "$LOG_FILE"
echo "Total failed triggers: $FAILED" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Total trigger time: ~22.5 minutes (45 tests × 30 sec spacing)" | tee -a "$LOG_FILE"
echo "Actual execution time: Tests will complete over next 30-45 minutes" | tee -a "$LOG_FILE"
echo "Check Google Sheet for results: 12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I" | tee -a "$LOG_FILE"

chmod +x "$0"
