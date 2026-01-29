#!/usr/bin/env python3
import json, sys
try:
    f = open("/Users/computer/.claude/projects/-Users-computer-coding-stuff/011369ca-2fa7-4508-bb6d-acffb55a91b7/tool-results/mcp-n8n-mcp-n8n_executions-1769636764603.txt")
    d = json.load(f)
    f.close()
    rd = d['data']['resultData']['runData']
    n = [x for x in rd.keys() if 'airtable' in x.lower()][0]
    fields = rd[n][0]['data']['main'][0][0]['json']['fields']
    fns = ['pain_points', 'quick_wins', 'key_insights', 'pricing_strategy', 'client_journey_map', 'requirements', 'complexity_assessment', 'roadmap']
    t = {'pain_points': 150, 'quick_wins': 100, 'key_insights': 300, 'pricing_strategy': 200, 'client_journey_map': 150, 'requirements': 200, 'complexity_assessment': 200, 'roadmap': 150}
    total = passes = fails = 0
    for fn in fns:
        if fn in fields:
            lines = len(fields[fn].split('\n'))
            total += lines
            if lines >= t[fn]: passes += 1
            else: fails += 1
            print(f"{fn:30} {lines:6} {'PASS' if lines >= t[fn] else 'FAIL'}")
    print(f"{'TOTAL':30} {total:6}")
    print(f"\n{passes} PASS / {fails} FAIL")
    print(f"OVERALL: {'PASS' if total >= 1200 else 'FAIL'}")
except Exception as e: print(f"ERROR: {e}", file=sys.stderr); sys.exit(1)
