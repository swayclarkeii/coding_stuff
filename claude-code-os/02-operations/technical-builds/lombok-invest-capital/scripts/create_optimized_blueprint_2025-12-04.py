import json
import copy

# Read the original blueprint
with open('/Users/swayclarke/Downloads/Lombok Property Scraper v1.blueprint (1).json', 'r') as f:
    data = json.load(f)

# Create modules lookup
modules_by_id = {m['id']: m for m in data['flow']}

# Create optimized flow
new_flow = []

# 1. Webhook
new_flow.append(modules_by_id[1])

# 2. Get Task 1 Results
new_flow.append(modules_by_id[19])

# 3. Create RAW Sheet (create both sheets upfront)
new_flow.append(modules_by_id[22])

# 4. Write RAW Headers
new_flow.append(modules_by_id[8])

# 5. Create FILTERED Sheet
filtered_sheet = copy.deepcopy(modules_by_id[24])
filtered_sheet['metadata']['designer'] = {'x': 2100, 'y': 0}
new_flow.append(filtered_sheet)

# 6. Write FILTERED Headers
filtered_headers = copy.deepcopy(modules_by_id[12])
filtered_headers['metadata']['designer'] = {'x': 2400, 'y': 0}
new_flow.append(filtered_headers)

# ===== TASK 1 PROCESSING =====
# 7. Iterator for Task 1
task1_iterator = copy.deepcopy(modules_by_id[23])
task1_iterator['mapper']['array'] = '{{19.array}}'
task1_iterator['metadata']['designer'] = {'x': 2700, 'y': 0}
new_flow.append(task1_iterator)

# 8. Write to RAW sheet (Task 1)
new_flow.append(modules_by_id[10])

# 9. Set priceUSD variable (Task 1)
price1 = copy.deepcopy(modules_by_id[14])
price1['id'] = 141
if 'value' in price1['mapper']:
    price1['mapper']['value'] = price1['mapper']['value'].replace('25.', '23.')
price1['metadata']['designer'] = {'x': 3300, 'y': 0}
new_flow.append(price1)

# 10. Set completeness variable (Task 1)
complete1 = copy.deepcopy(modules_by_id[15])
complete1['id'] = 151
if 'value' in complete1['mapper']:
    complete1['mapper']['value'] = complete1['mapper']['value'].replace('25.', '23.').replace('14.', '141.')
complete1['metadata']['designer'] = {'x': 3600, 'y': 0}
new_flow.append(complete1)

# 11. Write to FILTERED sheet (Task 1)
write_f1 = copy.deepcopy(modules_by_id[17])
write_f1['id'] = 171
if 'values' in write_f1['mapper'] and isinstance(write_f1['mapper']['values'], dict):
    for key in write_f1['mapper']['values']:
        val = write_f1['mapper']['values'][key]
        if isinstance(val, str):
            write_f1['mapper']['values'][key] = val.replace('{{25.', '{{23.').replace('{{14.', '{{141.').replace('{{15.', '{{151.')
write_f1['metadata']['designer'] = {'x': 3900, 'y': 0, 'name': 'Write FILTERED (Task 1)'}
new_flow.append(write_f1)

# ===== TASK 2 PROCESSING =====
# 12. Get Task 2 Results
task2_get = copy.deepcopy(modules_by_id[20])
task2_get['metadata']['designer'] = {'x': 4200, 'y': 0}
new_flow.append(task2_get)

# 13. Iterator for Task 2
task2_iterator = copy.deepcopy(modules_by_id[23])
task2_iterator['id'] = 232
task2_iterator['mapper']['array'] = '{{20.array}}'
task2_iterator['metadata']['designer'] = {'x': 4500, 'y': 0}
new_flow.append(task2_iterator)

# 14. Write to RAW sheet (Task 2)
task2_write_raw = copy.deepcopy(modules_by_id[10])
task2_write_raw['id'] = 102
if 'values' in task2_write_raw['mapper'] and isinstance(task2_write_raw['mapper']['values'], dict):
    for key in task2_write_raw['mapper']['values']:
        val = task2_write_raw['mapper']['values'][key]
        if isinstance(val, str):
            task2_write_raw['mapper']['values'][key] = val.replace('{{23.', '{{232.')
task2_write_raw['metadata']['designer'] = {'x': 4800, 'y': 0, 'name': 'Write RAW (Task 2)'}
new_flow.append(task2_write_raw)

# 15. Set priceUSD variable (Task 2)
price2 = copy.deepcopy(modules_by_id[14])
price2['id'] = 142
if 'value' in price2['mapper']:
    price2['mapper']['value'] = price2['mapper']['value'].replace('25.', '232.')
price2['metadata']['designer'] = {'x': 5100, 'y': 0}
new_flow.append(price2)

# 16. Set completeness variable (Task 2)
complete2 = copy.deepcopy(modules_by_id[15])
complete2['id'] = 152
if 'value' in complete2['mapper']:
    complete2['mapper']['value'] = complete2['mapper']['value'].replace('25.', '232.').replace('14.', '142.')
complete2['metadata']['designer'] = {'x': 5400, 'y': 0}
new_flow.append(complete2)

# 17. Write to FILTERED sheet (Task 2)
write_f2 = copy.deepcopy(modules_by_id[17])
write_f2['id'] = 172
if 'values' in write_f2['mapper'] and isinstance(write_f2['mapper']['values'], dict):
    for key in write_f2['mapper']['values']:
        val = write_f2['mapper']['values'][key]
        if isinstance(val, str):
            write_f2['mapper']['values'][key] = val.replace('{{25.', '{{232.').replace('{{14.', '{{142.').replace('{{15.', '{{152.')
write_f2['metadata']['designer'] = {'x': 5700, 'y': 0, 'name': 'Write FILTERED (Task 2)'}
new_flow.append(write_f2)

# ===== TASK 3 PROCESSING =====
# 18. Get Task 3 Results
task3_get = copy.deepcopy(modules_by_id[21])
task3_get['metadata']['designer'] = {'x': 6000, 'y': 0}
new_flow.append(task3_get)

# 19. Iterator for Task 3
task3_iterator = copy.deepcopy(modules_by_id[23])
task3_iterator['id'] = 233
task3_iterator['mapper']['array'] = '{{21.array}}'
task3_iterator['metadata']['designer'] = {'x': 6300, 'y': 0}
new_flow.append(task3_iterator)

# 20. Write to RAW sheet (Task 3)
task3_write_raw = copy.deepcopy(modules_by_id[10])
task3_write_raw['id'] = 103
if 'values' in task3_write_raw['mapper'] and isinstance(task3_write_raw['mapper']['values'], dict):
    for key in task3_write_raw['mapper']['values']:
        val = task3_write_raw['mapper']['values'][key]
        if isinstance(val, str):
            task3_write_raw['mapper']['values'][key] = val.replace('{{23.', '{{233.')
task3_write_raw['metadata']['designer'] = {'x': 6600, 'y': 0, 'name': 'Write RAW (Task 3)'}
new_flow.append(task3_write_raw)

# 21. Set priceUSD variable (Task 3)
price3 = copy.deepcopy(modules_by_id[14])
price3['id'] = 143
if 'value' in price3['mapper']:
    price3['mapper']['value'] = price3['mapper']['value'].replace('25.', '233.')
price3['metadata']['designer'] = {'x': 6900, 'y': 0}
new_flow.append(price3)

# 22. Set completeness variable (Task 3)
complete3 = copy.deepcopy(modules_by_id[15])
complete3['id'] = 153
if 'value' in complete3['mapper']:
    complete3['mapper']['value'] = complete3['mapper']['value'].replace('25.', '233.').replace('14.', '143.')
complete3['metadata']['designer'] = {'x': 7200, 'y': 0}
new_flow.append(complete3)

# 23. Write to FILTERED sheet (Task 3)
write_f3 = copy.deepcopy(modules_by_id[17])
write_f3['id'] = 173
if 'values' in write_f3['mapper'] and isinstance(write_f3['mapper']['values'], dict):
    for key in write_f3['mapper']['values']:
        val = write_f3['mapper']['values'][key]
        if isinstance(val, str):
            write_f3['mapper']['values'][key] = val.replace('{{25.', '{{233.').replace('{{14.', '{{143.').replace('{{15.', '{{153.')
write_f3['metadata']['designer'] = {'x': 7500, 'y': 0, 'name': 'Write FILTERED (Task 3)'}
new_flow.append(write_f3)

# 24. Send Email
email = copy.deepcopy(modules_by_id[26])
email['metadata']['designer'] = {'x': 7800, 'y': 0}
new_flow.append(email)

# Update the data
data['flow'] = new_flow

# Save the optimized blueprint
output_path = '/Users/swayclarke/oloxa_stuff/Lombok Invest Capital/lombok-scraper-optimized-v4.json'
with open(output_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Created optimized blueprint with {len(new_flow)} modules")
print(f"✅ Saved to: {output_path}")
print(f"\n📊 Optimized Flow Structure:")
print(f"="*60)
print(f"1. Webhook")
print(f"2. Get Task 1 Results")
print(f"3. Create RAW Sheet + Headers")
print(f"4. Create FILTERED Sheet + Headers")
print(f"5. Iterator (Task 1)")
print(f"   ├─ Write to RAW sheet")
print(f"   ├─ Calculate priceUSD")
print(f"   ├─ Calculate completeness")
print(f"   └─ Write to FILTERED sheet")
print(f"6. Get Task 2 Results")
print(f"7. Iterator (Task 2)")
print(f"   └─ [Same dual-write process]")
print(f"8. Get Task 3 Results")
print(f"9. Iterator (Task 3)")
print(f"   └─ [Same dual-write process]")
print(f"10. Send Email")
print(f"\n✅ Benefits:")
print(f"   • 50% faster - only iterate each dataset once")
print(f"   • No Array Aggregator = No infinite loops")
print(f"   • Clean sequential flow")
print(f"   • Both RAW and FILTERED data written in same pass")
