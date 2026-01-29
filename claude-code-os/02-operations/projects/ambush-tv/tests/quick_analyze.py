import json
input_file = "/Users/computer/.claude/projects/-Users-computer-coding-stuff/011369ca-2fa7-4508-bb6d-acffb55a91b7/tool-results/mcp-n8n-mcp-n8n_executions-1769636764603.txt"
with open(input_file) as f: data = json.load(f)
rd = data['data']['resultData']['runData']
node = [n for n in rd.keys() if 'airtable' in n.lower()][0]
fields = rd[node][0]['data']['main'][0][0]['json']['fields']
fns = ['pain_points', 'quick_wins', 'key_insights', 'pricing_strategy', 'client_journey_map', 'requirements', 'complexity_assessment', 'roadmap']
thresholds = {'pain_points': 150, 'quick_wins': 100, 'key_insights': 300, 'pricing_strategy': 200, 'client_journey_map': 150, 'requirements': 200, 'complexity_assessment': 200, 'roadmap': 150}
total = 0
passes = 0
fails = 0
print("=== V2.0 VALIDATION RESULTS ===\n")
print(f"{'Field':30} {'Lines':>8} {'Threshold':>10} {'Status':>10}")
print("-" * 70)
for fn in fns:
    if fn in fields:
        lines = len(fields[fn].split('\n'))
        total += lines
        thresh = thresholds[fn]
        status = "PASS" if lines >= thresh else "FAIL"
        if status == "PASS": passes += 1
        else: fails += 1
        print(f"{fn:30} {lines:8} {thresh:>10} {status:>10}")
print("-" * 70)
print(f"{'TOTAL':30} {total:8}")
print(f"\nTests: {passes} PASS / {fails} FAIL")
print(f"OVERALL: {'PASS' if total >= 1200 else 'FAIL'} (target: >=1,200 lines, actual: {total})")
all_content = ' '.join([fields.get(fn, '') for fn in fns])
print("\n=== V2.0 FEATURES ===\n")
features = [('ASCII diagrams', ['┌', '├', '└', '│']), ('ROI formulas', ['×', '$', '=']), ('Line citations', ['[Line ', '(Line ']), ('Multi-paragraph', ['\n\n', '###'])]
for name, indicators in features:
    found = any(ind in all_content for ind in indicators)
    print(f"{name:25} {'PRESENT' if found else 'MISSING'}")
print(f"\nComparison: v1.0 (~45 lines) → v2.0 ({total} lines) = {total/45:.0f}x increase")
