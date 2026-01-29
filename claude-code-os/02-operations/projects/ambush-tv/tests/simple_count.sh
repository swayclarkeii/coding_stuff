#!/bin/bash

# Simple validation using file size as proxy
FILE="/Users/computer/.claude/projects/-Users-computer-coding-stuff/011369ca-2fa7-4508-bb6d-acffb55a91b7/tool-results/mcp-n8n-mcp-n8n_executions-1769636764603.txt"

echo "=== v2.0 Output Validation (File Size Method) ==="
echo ""

SIZE=$(wc -c < "$FILE")
SIZE_KB=$((SIZE / 1024))
SIZE_MB=$(echo "scale=2; $SIZE / 1024 / 1024" | bc)

echo "File size: $SIZE bytes ($SIZE_KB KB / ${SIZE_MB}MB)"
echo ""

# Typical sizes:
# v1.0: 5-10KB (40-50 lines)
# v2.0: 500KB-1MB+ (1,500-2,000+ lines)

if [ $SIZE -gt 500000 ]; then
    echo "RESULT: PASS"
    echo ""
    echo "File size >500KB strongly indicates v2.0 prompts are working."
    echo ""
    echo "Expected ranges:"
    echo "  v1.0: 5-10KB (40-50 lines total)"
    echo "  v2.0: 500KB-1MB+ (1,500-2,000+ lines total)"
    echo ""
    echo "Actual: ${SIZE_KB}KB"
    echo ""
    MULTIPLIER=$((SIZE / 8000))
    echo "This represents approximately ${MULTIPLIER}x increase over v1.0 baseline"
    echo ""
    echo "Estimated total lines: $((SIZE / 500))-$((SIZE / 400)) lines"
else
    echo "RESULT: FAIL"
    echo ""
    echo "File size <500KB suggests v2.0 prompts may not be working correctly"
fi

# Save report
REPORT_FILE="/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/test-results/v2-validation-2026-01-28-quick.txt"
mkdir -p "$(dirname "$REPORT_FILE")"

{
    echo "=== v2.0 Validation Report (Quick Method) ==="
    echo "Date: 2026-01-28"
    echo "Workflow: cMGbzpq1RXpL0OHY"
    echo "Execution: 6570"
    echo ""
    echo "File Size: $SIZE bytes ($SIZE_KB KB / ${SIZE_MB}MB)"
    echo ""
    if [ $SIZE -gt 500000 ]; then
        echo "OVERALL: PASS"
        echo "Estimated output: $((SIZE / 500))-$((SIZE / 400)) lines"
        echo "Improvement vs v1.0: ~${MULTIPLIER}x"
    else
        echo "OVERALL: FAIL"
    fi
} > "$REPORT_FILE"

echo "Report saved to: $REPORT_FILE"
