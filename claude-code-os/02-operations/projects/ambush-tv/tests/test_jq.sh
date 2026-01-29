#!/bin/bash
FILE="/Users/computer/.claude/projects/-Users-computer-coding-stuff/011369ca-2fa7-4508-bb6d-acffb55a91b7/tool-results/mcp-n8n-mcp-n8n_executions-1769636764603.txt"

echo "Testing jq extraction..."

# Extract pain_points field and count lines
PAIN_POINTS=$(jq -r '.data.resultData.runData | to_entries[] | select(.key | contains("Airtable")) | .value[0].data.main[0][0].json.fields.pain_points' "$FILE" 2>/dev/null)

if [ -n "$PAIN_POINTS" ]; then
    LINE_COUNT=$(echo "$PAIN_POINTS" | wc -l)
    echo "pain_points field extracted successfully"
    echo "Line count: $LINE_COUNT"
    echo ""
    echo "First 200 characters:"
    echo "$PAIN_POINTS" | head -c 200
    echo ""
    echo "..."
else
    echo "Failed to extract pain_points field"
fi
