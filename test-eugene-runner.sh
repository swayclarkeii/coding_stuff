#!/bin/bash

# Eugene Quick Test Runner - 5 Test Batch
# Tests production changes to verify file processing

WEBHOOK_URL="https://n8n.oloxa.ai/webhook/eugene-quick-test"
TEST_RUNNER_ID="fIqmtfEDuYM7gbE9"
CHUNK_25_ID="okg8wTqLtPUwjQ18"
MAX_WAIT_SECONDS=720  # 12 minutes max per test
POLL_INTERVAL=60      # Check every 60 seconds

echo "=== Eugene Quick Test Runner - 5 Test Batch ==="
echo "Started: $(date)"
echo ""

# Function to get latest execution ID for a workflow
get_latest_execution() {
    local workflow_id=$1
    curl -s "https://n8n.oloxa.ai/api/v1/executions?workflowId=${workflow_id}&limit=1" \
        -H "Accept: application/json" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4
}

# Function to check execution status
check_execution_status() {
    local exec_id=$1
    curl -s "https://n8n.oloxa.ai/api/v1/executions/${exec_id}" \
        -H "Accept: application/json" | grep -o '"status":"[^"]*"' | cut -d'"' -f4
}

# Run 5 tests
for test_num in {1..5}; do
    echo "----------------------------------------"
    echo "Test ${test_num}/5 - $(date)"
    echo "----------------------------------------"

    # Fire webhook
    echo "Firing webhook..."
    curl -X POST "${WEBHOOK_URL}" \
        -H "Content-Type: application/json" \
        -d '{}' \
        --silent \
        --max-time 15
    echo ""

    # Wait 30 seconds before polling
    echo "Waiting 30 seconds before polling..."
    sleep 30

    # Get baseline execution IDs
    test_runner_exec=$(get_latest_execution ${TEST_RUNNER_ID})
    chunk_25_exec=$(get_latest_execution ${CHUNK_25_ID})

    echo "Test Runner execution: ${test_runner_exec}"
    echo "Chunk 2.5 execution: ${chunk_25_exec}"

    # Poll for completion
    elapsed=0
    while [ $elapsed -lt $MAX_WAIT_SECONDS ]; do
        test_runner_status=$(check_execution_status ${test_runner_exec})
        chunk_25_status=$(check_execution_status ${chunk_25_exec})

        echo "[${elapsed}s] Test Runner: ${test_runner_status} | Chunk 2.5: ${chunk_25_status}"

        # Check if both completed
        if [[ "${test_runner_status}" == "success" || "${test_runner_status}" == "error" ]] && \
           [[ "${chunk_25_status}" == "success" || "${chunk_25_status}" == "error" ]]; then
            echo ""
            echo "✓ Test ${test_num} Complete:"
            echo "  - Test Runner (${test_runner_exec}): ${test_runner_status}"
            echo "  - Chunk 2.5 (${chunk_25_exec}): ${chunk_25_status}"
            break
        fi

        sleep $POLL_INTERVAL
        elapsed=$((elapsed + POLL_INTERVAL))
    done

    if [ $elapsed -ge $MAX_WAIT_SECONDS ]; then
        echo ""
        echo "✗ Test ${test_num} TIMEOUT after ${MAX_WAIT_SECONDS}s"
    fi

    echo ""
done

echo "=== All 5 Tests Complete ==="
echo "Finished: $(date)"
