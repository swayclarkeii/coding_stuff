#!/bin/bash
WEBHOOK_URL="https://n8n.oloxa.ai/webhook/eugene-quick-test"
WAIT_TIME=480
TOTAL_TESTS=50
START_FROM=${1:-2}

echo "Iteration 5 - Tests $START_FROM to $TOTAL_TESTS → Test_Results_Iteration5"
echo "Started: $(date)"
echo ""

for i in $(seq $START_FROM $TOTAL_TESTS); do
  echo "[$i/$TOTAL_TESTS] $(date +%H:%M:%S) Firing test webhook..."
  curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d '{}' --silent --output /dev/null --max-time 10 || true
  echo "  Webhook fired. Waiting 8 minutes..."
  sleep $WAIT_TIME
  echo "  ✅ Next"
  echo ""
done

echo "✅ All tests complete!"
echo "Completed: $(date)"
