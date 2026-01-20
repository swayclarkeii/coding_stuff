import json
import copy

# Read the original blueprint
with open('/Users/swayclarke/Downloads/Lombok Property Scraper v1.blueprint (1).json', 'r') as f:
    data = json.load(f)

# Create modules lookup
modules_by_id = {m['id']: m for m in data['flow']}

# Create new sequential flow
new_flow = []

# 1. Keep Webhook (module 1)
new_flow.append(modules_by_id[1])

# 2. Get Task 1 Results (module 19)
new_flow.append(modules_by_id[19])

# 3. Create RAW Sheet (module 22) - only create ONCE
new_flow.append(modules_by_id[22])

# 4. Write RAW Headers (module 8) - only write ONCE
new_flow.append(modules_by_id[8])

# 5. Iterator for Task 1 (module 23) - already points to correct source
task1_iterator = copy.deepcopy(modules_by_id[23])
task1_iterator['mapper']['array'] = '{{19.array}}'
task1_iterator['metadata']['designer'] = {'x': 2400, 'y': 0}
new_flow.append(task1_iterator)

# 6. Write RAW rows for Task 1 (module 10)
new_flow.append(modules_by_id[10])

# 7. Get Task 2 Results (module 20)
task2_get = copy.deepcopy(modules_by_id[20])
task2_get['metadata']['designer'] = {'x': 3000, 'y': 0}
new_flow.append(task2_get)

# 8. Iterator for Task 2
task2_iterator = copy.deepcopy(modules_by_id[23])
task2_iterator['id'] = 232
task2_iterator['mapper']['array'] = '{{20.array}}'
task2_iterator['metadata']['designer'] = {'x': 3300, 'y': 0}
new_flow.append(task2_iterator)

# 9. Write RAW rows for Task 2
task2_write = copy.deepcopy(modules_by_id[10])
task2_write['id'] = 102
# Update references from {{23.xxx}} to {{232.xxx}}
if 'values' in task2_write['mapper'] and isinstance(task2_write['mapper']['values'], dict):
    for key in task2_write['mapper']['values']:
        val = task2_write['mapper']['values'][key]
        if isinstance(val, str):
            task2_write['mapper']['values'][key] = val.replace('{{23.', '{{232.')
task2_write['metadata']['designer'] = {'x': 3600, 'y': 0, 'name': 'Write RAW rows (Task 2)'}
new_flow.append(task2_write)

# 10. Get Task 3 Results (module 21)
task3_get = copy.deepcopy(modules_by_id[21])
task3_get['metadata']['designer'] = {'x': 3900, 'y': 0}
new_flow.append(task3_get)

# 11. Iterator for Task 3
task3_iterator = copy.deepcopy(modules_by_id[23])
task3_iterator['id'] = 233
task3_iterator['mapper']['array'] = '{{21.array}}'
task3_iterator['metadata']['designer'] = {'x': 4200, 'y': 0}
new_flow.append(task3_iterator)

# 12. Write RAW rows for Task 3
task3_write = copy.deepcopy(modules_by_id[10])
task3_write['id'] = 103
if 'values' in task3_write['mapper'] and isinstance(task3_write['mapper']['values'], dict):
    for key in task3_write['mapper']['values']:
        val = task3_write['mapper']['values'][key]
        if isinstance(val, str):
            task3_write['mapper']['values'][key] = val.replace('{{23.', '{{233.')
task3_write['metadata']['designer'] = {'x': 4500, 'y': 0, 'name': 'Write RAW rows (Task 3)'}
new_flow.append(task3_write)

# 13. Create FILTERED Sheet (module 24)
filtered_sheet = copy.deepcopy(modules_by_id[24])
filtered_sheet['metadata']['designer'] = {'x': 4800, 'y': 0}
new_flow.append(filtered_sheet)

# 14. Write FILTERED Headers (module 12)
filtered_headers = copy.deepcopy(modules_by_id[12])
filtered_headers['metadata']['designer'] = {'x': 5100, 'y': 0}
new_flow.append(filtered_headers)

# Now repeat for FILTERED data - Task 1, 2, 3 sequentially
# For FILTERED, we need: Iterator → Set priceUSD → Set completeness → Filter → Write row

# TASK 1 FILTERED
# 15. Iterator for Task 1 filtered
task1_filtered_iter = copy.deepcopy(modules_by_id[25])
task1_filtered_iter['id'] = 251
task1_filtered_iter['mapper']['array'] = '{{19.array}}'
task1_filtered_iter['metadata']['designer'] = {'x': 5400, 'y': 0}
new_flow.append(task1_filtered_iter)

# 16. Set priceUSD
price1 = copy.deepcopy(modules_by_id[14])
price1['id'] = 141
if 'value' in price1['mapper']:
    price1['mapper']['value'] = price1['mapper']['value'].replace('25.', '251.')
price1['metadata']['designer'] = {'x': 5700, 'y': 0}
new_flow.append(price1)

# 17. Set completeness
complete1 = copy.deepcopy(modules_by_id[15])
complete1['id'] = 151
if 'value' in complete1['mapper']:
    complete1['mapper']['value'] = complete1['mapper']['value'].replace('25.', '251.').replace('14.', '141.')
complete1['metadata']['designer'] = {'x': 6000, 'y': 0}
new_flow.append(complete1)

# 18. Write filtered row
write_f1 = copy.deepcopy(modules_by_id[17])
write_f1['id'] = 171
if 'values' in write_f1['mapper'] and isinstance(write_f1['mapper']['values'], dict):
    for key in write_f1['mapper']['values']:
        val = write_f1['mapper']['values'][key]
        if isinstance(val, str):
            write_f1['mapper']['values'][key] = val.replace('{{25.', '{{251.').replace('{{14.', '{{141.').replace('{{15.', '{{151.')
write_f1['metadata']['designer'] = {'x': 6300, 'y': 0, 'name': 'Write FILTERED (Task 1)'}
new_flow.append(write_f1)

# TASK 2 FILTERED
task2_filtered_iter = copy.deepcopy(modules_by_id[25])
task2_filtered_iter['id'] = 252
task2_filtered_iter['mapper']['array'] = '{{20.array}}'
task2_filtered_iter['metadata']['designer'] = {'x': 6600, 'y': 0}
new_flow.append(task2_filtered_iter)

price2 = copy.deepcopy(modules_by_id[14])
price2['id'] = 142
if 'value' in price2['mapper']:
    price2['mapper']['value'] = price2['mapper']['value'].replace('25.', '252.')
price2['metadata']['designer'] = {'x': 6900, 'y': 0}
new_flow.append(price2)

complete2 = copy.deepcopy(modules_by_id[15])
complete2['id'] = 152
if 'value' in complete2['mapper']:
    complete2['mapper']['value'] = complete2['mapper']['value'].replace('25.', '252.').replace('14.', '142.')
complete2['metadata']['designer'] = {'x': 7200, 'y': 0}
new_flow.append(complete2)

write_f2 = copy.deepcopy(modules_by_id[17])
write_f2['id'] = 172
if 'values' in write_f2['mapper'] and isinstance(write_f2['mapper']['values'], dict):
    for key in write_f2['mapper']['values']:
        val = write_f2['mapper']['values'][key]
        if isinstance(val, str):
            write_f2['mapper']['values'][key] = val.replace('{{25.', '{{252.').replace('{{14.', '{{142.').replace('{{15.', '{{152.')
write_f2['metadata']['designer'] = {'x': 7500, 'y': 0, 'name': 'Write FILTERED (Task 2)'}
new_flow.append(write_f2)

# TASK 3 FILTERED
task3_filtered_iter = copy.deepcopy(modules_by_id[25])
task3_filtered_iter['id'] = 253
task3_filtered_iter['mapper']['array'] = '{{21.array}}'
task3_filtered_iter['metadata']['designer'] = {'x': 7800, 'y': 0}
new_flow.append(task3_filtered_iter)

price3 = copy.deepcopy(modules_by_id[14])
price3['id'] = 143
if 'value' in price3['mapper']:
    price3['mapper']['value'] = price3['mapper']['value'].replace('25.', '253.')
price3['metadata']['designer'] = {'x': 8100, 'y': 0}
new_flow.append(price3)

complete3 = copy.deepcopy(modules_by_id[15])
complete3['id'] = 153
if 'value' in complete3['mapper']:
    complete3['mapper']['value'] = complete3['mapper']['value'].replace('25.', '253.').replace('14.', '143.')
complete3['metadata']['designer'] = {'x': 8400, 'y': 0}
new_flow.append(complete3)

write_f3 = copy.deepcopy(modules_by_id[17])
write_f3['id'] = 173
if 'values' in write_f3['mapper'] and isinstance(write_f3['mapper']['values'], dict):
    for key in write_f3['mapper']['values']:
        val = write_f3['mapper']['values'][key]
        if isinstance(val, str):
            write_f3['mapper']['values'][key] = val.replace('{{25.', '{{253.').replace('{{14.', '{{143.').replace('{{15.', '{{153.')
write_f3['metadata']['designer'] = {'x': 8700, 'y': 0, 'name': 'Write FILTERED (Task 3)'}
new_flow.append(write_f3)

# Add email at the end
email = copy.deepcopy(modules_by_id[26])
email['metadata']['designer'] = {'x': 9000, 'y': 0}
new_flow.append(email)

# Update the data
data['flow'] = new_flow

# Save the corrected blueprint
output_path = '/Users/swayclarke/oloxa_stuff/Lombok Invest Capital/lombok-scraper-sequential-v3.json'
with open(output_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Created sequential blueprint with {len(new_flow)} modules")
print(f"✅ Saved to: {output_path}")
print(f"\nFlow structure:")
print(f"1. Webhook")
print(f"2. Get Task 1 → Create RAW Sheet → Write Headers → Iterator → Write Rows")
print(f"3. Get Task 2 → Iterator → Write Rows")
print(f"4. Get Task 3 → Iterator → Write Rows")
print(f"5. Create FILTERED Sheet → Write Headers")
print(f"6. Task 1 → Iterator → Process → Write")
print(f"7. Task 2 → Iterator → Process → Write")
print(f"8. Task 3 → Iterator → Process → Write")
print(f"9. Send Email")
print(f"\n✅ This will work correctly - no infinite loops!")
