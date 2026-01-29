#!/bin/bash

# Iteration 4 Test Runner (FIXED)
# Lets Eugene Quick Test Runner pick random files from test folder
# Writes to: Test_Results_Iteration4 tab

WEBHOOK_URL="https://n8n.oloxa.ai/webhook/eugene-quick-test"
WAIT_TIME=480  # 8 minutes in seconds
TOTAL_TESTS=50
START_FROM=${1:-1}  # Pass start number as argument, default 1

echo "🚀 Iteration 4 - All 50 Tests → Test_Results_Iteration4"
echo "Started: $(date)"
echo ""
echo "NOTE: Workflow will randomly select files from test folder"
echo ""

for i in $(seq $START_FROM $TOTAL_TESTS); do
  echo "[$i/$TOTAL_TESTS] Firing test webhook..."

  # Call webhook WITHOUT file parameters
  # Workflow will pick random file from test folder
  curl -X POST "$WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d '{}' \
    --silent --output /dev/null || true

  echo "  Webhook fired. Waiting 8 minutes..."
  sleep $WAIT_TIME

  echo "  ✅ Next"
  echo ""
done

echo "✅ All tests complete!"
echo "Completed: $(date)"
echo ""
echo "View results: https://docs.google.com/spreadsheets/d/12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I/edit?gid=597616325#gid=597616325"
