#!/bin/bash

# Iteration 4 Resilient Test Runner
# - No set -e (won't crash on single failure)
# - Long curl timeout to catch webhook response (success vs error)
# - Logs progress and errors
# - Retry on transient failures
# - Resumes from where it left off

WEBHOOK_URL="https://n8n.oloxa.ai/webhook/eugene-quick-test"
TOTAL_TESTS=50
START_FROM=${1:-5}  # Pass start number as argument, default 5
LOG_FILE="/Users/swayclarke/coding_stuff/scripts/iteration4_resilient.log"
CURL_TIMEOUT=600  # 10 min max per test (workflow takes 3-5 min)

# Counters
passed=0
failed=0
skipped=0
consecutive_errors=0

echo "============================================" | tee -a "$LOG_FILE"
echo "Iteration 4 Resilient Test Runner" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "Tests: $START_FROM to $TOTAL_TESTS" | tee -a "$LOG_FILE"
echo "============================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

for i in $(seq "$START_FROM" "$TOTAL_TESTS"); do
  echo "[$i/$TOTAL_TESTS] $(date '+%H:%M:%S') Firing test..." | tee -a "$LOG_FILE"

  # Fire webhook with long timeout — webhook responds when workflow completes
  response_file="/tmp/eugene_test_${i}_response.txt"
  http_code=$(curl -X POST "$WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d '{}' \
    --silent --max-time "$CURL_TIMEOUT" \
    -o "$response_file" -w "%{http_code}" 2>/dev/null || echo "000")

  if [ "$http_code" = "200" ]; then
    echo "  SUCCESS (HTTP 200)" | tee -a "$LOG_FILE"
    passed=$((passed + 1))
    consecutive_errors=0
  elif [ "$http_code" = "000" ]; then
    echo "  TIMEOUT/CONNECTION ERROR — retrying once..." | tee -a "$LOG_FILE"
    sleep 15
    http_code=$(curl -X POST "$WEBHOOK_URL" \
      -H "Content-Type: application/json" \
      -d '{}' \
      --silent --max-time "$CURL_TIMEOUT" \
      -o "$response_file" -w "%{http_code}" 2>/dev/null || echo "000")

    if [ "$http_code" = "200" ]; then
      echo "  SUCCESS on retry (HTTP 200)" | tee -a "$LOG_FILE"
      passed=$((passed + 1))
      consecutive_errors=0
    else
      echo "  FAILED on retry (HTTP $http_code). Skipping." | tee -a "$LOG_FILE"
      skipped=$((skipped + 1))
      consecutive_errors=$((consecutive_errors + 1))
    fi
  elif [ "$http_code" = "500" ] || [ "$http_code" = "502" ] || [ "$http_code" = "503" ]; then
    # Workflow errored — n8n returns 500 on workflow execution error
    echo "  WORKFLOW ERROR (HTTP $http_code)" | tee -a "$LOG_FILE"
    # Try to extract error info from response
    if [ -f "$response_file" ]; then
      error_snippet=$(head -c 300 "$response_file" 2>/dev/null)
      echo "  Response: $error_snippet" | tee -a "$LOG_FILE"
    fi
    failed=$((failed + 1))
    consecutive_errors=$((consecutive_errors + 1))
  else
    echo "  UNEXPECTED (HTTP $http_code)" | tee -a "$LOG_FILE"
    failed=$((failed + 1))
    consecutive_errors=$((consecutive_errors + 1))
  fi

  # Clean up response file
  rm -f "$response_file" 2>/dev/null

  # Progress update every 5 tests
  completed=$((passed + failed + skipped))
  if [ $((completed % 5)) -eq 0 ] && [ "$completed" -gt 0 ]; then
    echo "" | tee -a "$LOG_FILE"
    echo "--- PROGRESS [$i/$TOTAL_TESTS]: $passed passed | $failed failed | $skipped skipped ---" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
  fi

  # Stall detection: 3 consecutive errors = pause 5 min
  if [ "$consecutive_errors" -ge 3 ]; then
    echo "" | tee -a "$LOG_FILE"
    echo "  STALL: 3 consecutive failures. Pausing 5 minutes before continuing..." | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
    sleep 300
    consecutive_errors=0
  fi

  # Brief pause between tests
  sleep 5
done

echo "" | tee -a "$LOG_FILE"
echo "============================================" | tee -a "$LOG_FILE"
echo "ITERATION 4 COMPLETE" | tee -a "$LOG_FILE"
echo "Completed: $(date)" | tee -a "$LOG_FILE"
echo "Passed: $passed" | tee -a "$LOG_FILE"
echo "Failed: $failed" | tee -a "$LOG_FILE"
echo "Skipped: $skipped" | tee -a "$LOG_FILE"
total=$((passed + failed + skipped))
echo "Total: $total" | tee -a "$LOG_FILE"
if [ $((passed + failed)) -gt 0 ]; then
  accuracy=$(python3 -c "print(f'{$passed / ($passed + $failed) * 100:.1f}%')" 2>/dev/null || echo "N/A")
  echo "Accuracy (excl skipped): $accuracy" | tee -a "$LOG_FILE"
fi
echo "============================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "Results: https://docs.google.com/spreadsheets/d/12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I/edit#gid=597616325" | tee -a "$LOG_FILE"
echo "Log: $LOG_FILE" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "To resume if interrupted: bash /Users/swayclarke/coding_stuff/scripts/iteration4_resilient_runner.sh [next_test_number]" | tee -a "$LOG_FILE"
