#!/bin/bash
# Extract the Build Claude API Request node from workflow JSON

INPUT_FILE="/Users/swayclarke/.claude/projects/-Users-swayclarke-coding-stuff/73b08553-81ae-4ccc-872d-e63616dfe0e1/tool-results/mcp-n8n-mcp-n8n_get_workflow-1768849147955.txt"
OUTPUT_FILE="/Users/swayclarke/coding_stuff/build-claude-request-node.json"

# Extract just the build-claude-request-001 node
cat "$INPUT_FILE" | jq -r '.[] | select(.type == "text") | .text' | jq '.nodes[] | select(.id == "build-claude-request-001")' > "$OUTPUT_FILE"

echo "Extracted node to: $OUTPUT_FILE"
cat "$OUTPUT_FILE"
