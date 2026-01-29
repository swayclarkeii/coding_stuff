#!/bin/bash

# Apply all remaining Code node fixes to SOP Builder Lead Magnet workflow
# Workflow ID: ikVyMpDI0az6Zk4t

WORKFLOW_ID="ikVyMpDI0az6Zk4t"

# Array of remaining nodes (already fixed: use-text-input, generate-lead-id)
declare -a nodes=(
  "parse-form:Parse Form Data"
  "set-transcription:Set Transcription as Steps"
  "extract-validation:Extract Validation Response"
  "extract-automation:Extract Improved SOP"
  "error-handler:Error Handler"
  "calculate-score:Calculate SOP Score"
  "format-for-airtable:Format for Airtable"
  "prepare-update-data:Prepare Update Data"
  "prepare-new-data:Prepare New Lead Data"
  "generate-improvement-email:Generate Improvement Email (<75%)"
  "generate-success-email:Generate Success Email (≥75%)"
)

echo "==================================="
echo "SOP Builder Code Node Fixes"
echo "==================================="
echo ""

success=0
failed=0

for node_entry in "${nodes[@]}"; do
  node_id="${node_entry%%:*}"
  node_name="${node_entry##*:}"

  echo "Applying fix for: $node_name"

  # Read the fixed code from file
  code_file="/tmp/code_${node_id}_fixed.js"

  if [ ! -f "$code_file" ]; then
    echo "  ✗ Code file not found: $code_file"
    ((failed++))
    continue
  fi

  # Create operation JSON
  code=$(cat "$code_file" | jq -Rs .)
  operation=$(cat <<EOF
[{
  "type": "updateNode",
  "nodeId": "$node_id",
  "updates": {
    "parameters": {
      "jsCode": $code
    }
  }
}]
EOF
)

  # Save operation to temp file
  echo "$operation" > "/tmp/apply_op_${node_id}.json"

  echo "  → Operation saved to /tmp/apply_op_${node_id}.json"
  echo "  → Use this MCP call to apply:"
  echo "     mcp__n8n-mcp__n8n_update_partial_workflow("
  echo "       id: \"$WORKFLOW_ID\","
  echo "       operations: <contents-of-/tmp/apply_op_${node_id}.json>"
  echo "     )"
  echo ""

  ((success++))
done

echo "==================================="
echo "Summary:"
echo "  ✓ Operation files created: $success"
echo "  ✗ Failed: $failed"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Use Claude Code to apply each operation file via MCP"
echo "2. Or manually copy the JSON from each /tmp/apply_op_*.json file"
echo "3. After all applied, validate with: mcp__n8n-mcp__n8n_validate_workflow(id: \"$WORKFLOW_ID\")"
