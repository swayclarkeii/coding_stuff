#!/usr/bin/env python3
import json
outfile = "/Users/computer/coding_stuff/claude-code-os/02-operations/projects/ambush-tv/test-results/exact-counts.txt"
try:
    with open("/Users/computer/.claude/projects/-Users-computer-coding-stuff/011369ca-2fa7-4508-bb6d-acffb55a91b7/tool-results/mcp-n8n-mcp-n8n_executions-1769636764603.txt") as f:
        data = json.load(f)
    rd = data['data']['resultData']['runData']
    node = [n for n in rd.keys() if 'airtable' in n.lower()][0]
    fields = rd[node][0]['data']['main'][0][0]['json']['fields']
    fns = ['pain_points', 'quick_wins', 'key_insights', 'pricing_strategy', 'client_journey_map', 'requirements', 'complexity_assessment', 'roadmap', 'one_liner']
    t = {'pain_points': 150, 'quick_wins': 100, 'key_insights': 300, 'pricing_strategy': 200, 'client_journey_map': 150, 'requirements': 200, 'complexity_assessment': 200, 'roadmap': 150, 'one_liner': 1}
    total = passes = fails = 0
    with open(outfile, 'w') as out:
        out.write(f"{'Field':30} {'Lines':>8} {'Threshold':>10} {'Status':>10}\n")
        out.write("-" * 70 + "\n")
        for fn in fns:
            if fn in fields:
                lines = len(fields[fn].split('\n'))
                total += lines
                status = "PASS" if lines >= t[fn] else "FAIL"
                if status == "PASS": passes += 1
                else: fails += 1
                out.write(f"{fn:30} {lines:8} {t[fn]:>10} {status:>10}\n")
        out.write("-" * 70 + "\n")
        out.write(f"{'TOTAL':30} {total:8}\n\n")
        out.write(f"Tests: {passes} PASS / {fails} FAIL\n")
        out.write(f"OVERALL: {'PASS' if total >= 1200 and fails == 0 else 'FAIL'}\n\n")
        out.write(f"v1.0 baseline: ~45 lines\n")
        out.write(f"v2.0 actual: {total} lines\n")
        out.write(f"Improvement: {total / 45:.0f}x more comprehensive\n")
    print(f"SUCCESS: Counts saved to {outfile}")
except Exception as e:
    with open(outfile, 'w') as out:
        out.write(f"ERROR: {str(e)}\n")
    print(f"ERROR: {e}")
