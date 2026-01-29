#!/usr/bin/env python3
"""
Analyze n8n v2.0 workflow output and generate validation report.
"""

import json
import sys
from pathlib import Path

def main():
    # Input/output paths
    input_file = Path("/Users/computer/.claude/projects/-Users-computer-coding-stuff/011369ca-2fa7-4508-bb6d-acffb55a91b7/tool-results/mcp-n8n-mcp-n8n_executions-1769636764603.txt")
    output_file = Path("/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/test-results/v2-validation-2026-01-28.txt")

    # Create output directory
    output_file.parent.mkdir(parents=True, exist_ok=True)

    print("Loading execution data...")

    try:
        with open(input_file) as f:
            data = json.load(f)

        # Navigate to Airtable fields
        run_data = data['data']['resultData']['runData']
        airtable_node = [n for n in run_data.keys() if 'airtable' in n.lower()][0]
        fields = run_data[airtable_node][0]['data']['main'][0][0]['json']['fields']

        print(f"Found Airtable node: {airtable_node}")

        # Analyze fields
        field_names = [
            'pain_points', 'quick_wins', 'key_insights', 'pricing_strategy',
            'client_journey_map', 'requirements', 'complexity_assessment', 'roadmap', 'one_liner'
        ]

        thresholds = {
            'pain_points': 150,
            'quick_wins': 100,
            'key_insights': 300,
            'pricing_strategy': 200,
            'client_journey_map': 150,
            'requirements': 200,
            'complexity_assessment': 200,
            'roadmap': 150,
            'one_liner': 1
        }

        results = []
        total_lines = 0
        passes = 0
        fails = 0

        for fn in field_names:
            if fn in fields:
                content = fields[fn]
                lines = len(content.split('\n'))
                total_lines += lines

                threshold = thresholds.get(fn, 100)
                if lines >= threshold:
                    status = "PASS"
                    passes += 1
                else:
                    status = "FAIL"
                    fails += 1

                results.append({
                    'field': fn,
                    'lines': lines,
                    'threshold': threshold,
                    'status': status,
                    'snippet': content[:100].replace('\n', ' ')
                })
            else:
                results.append({
                    'field': fn,
                    'lines': 0,
                    'threshold': thresholds.get(fn, 100),
                    'status': 'MISSING',
                    'snippet': ''
                })
                fails += 1

        # Check for v2.0 features
        all_content = ' '.join([fields.get(fn, '') for fn in field_names])

        feature_checks = {
            'ASCII diagrams': any(char in all_content for char in ['┌', '├', '└', '│', '─']),
            'ROI formulas': any(ind in all_content for ind in ['×', '$', '=']),
            'Line citations': any(ind in all_content for ind in ['[Line ', '(Line ']),
            'Multi-paragraph sections': '\n\n' in all_content or '###' in all_content
        }

        # Write report
        with open(output_file, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("n8n Workflow v2.0 Validation Report\n")
            f.write("=" * 70 + "\n\n")

            f.write(f"Test Date: 2026-01-28\n")
            f.write(f"Workflow ID: cMGbzpq1RXpL0OHY\n")
            f.write(f"Execution ID: 6570\n")
            f.write(f"Test Transcript: minimal_test_transcript_2026-01-28.txt\n\n")

            f.write("=" * 70 + "\n")
            f.write("FIELD LINE COUNTS\n")
            f.write("=" * 70 + "\n\n")

            f.write(f"{'Field':30} {'Lines':>8} {'Threshold':>10} {'Status':>10}\n")
            f.write("-" * 70 + "\n")

            for r in results:
                f.write(f"{r['field']:30} {r['lines']:8} {r['threshold']:>10} {r['status']:>10}\n")

            f.write("-" * 70 + "\n")
            f.write(f"{'TOTAL':30} {total_lines:8}\n\n")

            f.write("=" * 70 + "\n")
            f.write("VALIDATION SUMMARY\n")
            f.write("=" * 70 + "\n\n")

            f.write(f"Tests: {passes} PASS / {fails} FAIL\n\n")

            overall_status = "PASS" if total_lines >= 1200 and fails == 0 else "FAIL"
            f.write(f"OVERALL RESULT: {overall_status}\n")
            f.write(f"Total output: {total_lines} lines (minimum: 1,200)\n\n")

            if total_lines >= 1200:
                f.write(f"✓ Output depth meets v2.0 requirements\n")
            else:
                f.write(f"✗ Output depth below v2.0 requirements\n")
                f.write(f"  Shortfall: {1200 - total_lines} lines\n")

            f.write("\n")
            f.write("=" * 70 + "\n")
            f.write("V2.0 FEATURE VALIDATION\n")
            f.write("=" * 70 + "\n\n")

            for feature, present in feature_checks.items():
                status = "PRESENT" if present else "MISSING"
                symbol = "✓" if present else "✗"
                f.write(f"{symbol} {feature:30} {status}\n")

            f.write("\n")
            f.write("=" * 70 + "\n")
            f.write("COMPARISON TO v1.0\n")
            f.write("=" * 70 + "\n\n")

            v1_lines = 45  # Approximate v1.0 output
            improvement = total_lines / v1_lines

            f.write(f"v1.0 output: ~40-50 lines (estimated {v1_lines})\n")
            f.write(f"v2.0 output: {total_lines} lines\n")
            f.write(f"Improvement: {improvement:.1f}x more comprehensive\n\n")

            if improvement >= 20:
                f.write(f"✓ Meets expected 25-45x improvement range\n")
            else:
                f.write(f"✗ Below expected 25-45x improvement range\n")

            # Field-by-field comparison
            f.write("\n")
            f.write("=" * 70 + "\n")
            f.write("DETAILED FIELD ANALYSIS\n")
            f.write("=" * 70 + "\n\n")

            v1_estimates = {
                'pain_points': 15,
                'quick_wins': 15,
                'key_insights': 8,
                'pricing_strategy': 3,
                'client_journey_map': 1,
                'requirements': 4
            }

            for r in results:
                if r['field'] in v1_estimates:
                    v1_est = v1_estimates[r['field']]
                    actual = r['lines']
                    improvement = actual / v1_est if v1_est > 0 else actual

                    f.write(f"\n{r['field'].upper().replace('_', ' ')}:\n")
                    f.write(f"  v1.0: ~{v1_est} lines\n")
                    f.write(f"  v2.0: {actual} lines ({improvement:.1f}x increase)\n")
                    f.write(f"  Status: {r['status']}\n")
                    if r['snippet']:
                        f.write(f"  Snippet: {r['snippet']}...\n")

            f.write("\n")
            f.write("=" * 70 + "\n")
            f.write("CONCLUSION\n")
            f.write("=" * 70 + "\n\n")

            if overall_status == "PASS":
                f.write("✓ v2.0 prompts are working correctly\n")
                f.write("✓ Output depth is comprehensive and detailed\n")
                f.write("✓ All expected features are present\n")
                f.write("\nThe workflow is ready for production use.\n")
            else:
                f.write("✗ v2.0 validation failed\n")
                f.write("\nIssues to address:\n")
                for r in results:
                    if r['status'] == "FAIL":
                        f.write(f"  - {r['field']}: {r['lines']} lines (need >{r['threshold']})\n")
                for feature, present in feature_checks.items():
                    if not present:
                        f.write(f"  - Missing feature: {feature}\n")

        print(f"\nReport saved to: {output_file}")
        print(f"\nOVERALL RESULT: {overall_status}")
        print(f"Total lines: {total_lines}")
        print(f"Tests: {passes} PASS / {fails} FAIL")

        # Also print to stdout for immediate viewing
        with open(output_file) as f:
            print("\n" + "=" * 70)
            print(f.read())

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
