import json
import copy

# Read the original blueprint
with open('/Users/swayclarke/Downloads/Lombok Property Scraper v1.blueprint (1).json', 'r') as f:
    data = json.load(f)

# Create modules lookup
modules_by_id = {m['id']: m for m in data['flow']}

# Create new flow
new_flow = []

# 1. Keep Webhook (module 1)
new_flow.append(modules_by_id[1])

# 2. Keep Get Dataset modules (19, 20, 21)
new_flow.append(modules_by_id[19])
new_flow.append(modules_by_id[20])
new_flow.append(modules_by_id[21])

# 3. Skip module 5 (BasicAggregator) - this is the problematic one

# 4. Keep Create RAW Sheet (module 22)
new_flow.append(modules_by_id[22])

# 5. Keep Write RAW Headers (module 8)
new_flow.append(modules_by_id[8])

# 6. Create 3 separate Feeder + Write Row pairs for RAW data

# TASK 1 RAW DATA PATH
feeder1 = copy.deepcopy(modules_by_id[23])
feeder1['id'] = 231
feeder1['mapper']['array'] = '{{19.array}}'
feeder1['metadata']['designer'] = {'x': 2400, 'y': -300}
new_flow.append(feeder1)

write_row1 = copy.deepcopy(modules_by_id[10])
write_row1['id'] = 101
# Update all references from {{23.xxx}} to {{231.xxx}}
if 'values' in write_row1['mapper'] and isinstance(write_row1['mapper']['values'], dict):
    for key in write_row1['mapper']['values']:
        val = write_row1['mapper']['values'][key]
        if isinstance(val, str):
            write_row1['mapper']['values'][key] = val.replace('{{23.', '{{231.')
write_row1['metadata']['designer'] = {'x': 2700, 'y': -300, 'name': 'Write RAW (Task 1)'}
new_flow.append(write_row1)

# TASK 2 RAW DATA PATH
feeder2 = copy.deepcopy(modules_by_id[23])
feeder2['id'] = 232
feeder2['mapper']['array'] = '{{20.array}}'
feeder2['metadata']['designer'] = {'x': 2400, 'y': 0}
new_flow.append(feeder2)

write_row2 = copy.deepcopy(modules_by_id[10])
write_row2['id'] = 102
if 'values' in write_row2['mapper'] and isinstance(write_row2['mapper']['values'], dict):
    for key in write_row2['mapper']['values']:
        val = write_row2['mapper']['values'][key]
        if isinstance(val, str):
            write_row2['mapper']['values'][key] = val.replace('{{23.', '{{232.')
write_row2['metadata']['designer'] = {'x': 2700, 'y': 0, 'name': 'Write RAW (Task 2)'}
new_flow.append(write_row2)

# TASK 3 RAW DATA PATH
feeder3 = copy.deepcopy(modules_by_id[23])
feeder3['id'] = 233
feeder3['mapper']['array'] = '{{21.array}}'
feeder3['metadata']['designer'] = {'x': 2400, 'y': 300}
new_flow.append(feeder3)

write_row3 = copy.deepcopy(modules_by_id[10])
write_row3['id'] = 103
if 'values' in write_row3['mapper'] and isinstance(write_row3['mapper']['values'], dict):
    for key in write_row3['mapper']['values']:
        val = write_row3['mapper']['values'][key]
        if isinstance(val, str):
            write_row3['mapper']['values'][key] = val.replace('{{23.', '{{233.')
write_row3['metadata']['designer'] = {'x': 2700, 'y': 300, 'name': 'Write RAW (Task 3)'}
new_flow.append(write_row3)

# 7. Keep Create FILTERED Sheet (module 24)
new_flow.append(modules_by_id[24])

# 8. Keep Write FILTERED Headers (module 12)
new_flow.append(modules_by_id[12])

# 9. For FILTERED data, we need to combine all 3 datasets
# We'll create 3 feeder paths that all write to FILTERED sheet

# TASK 1 FILTERED PATH
feeder_f1 = copy.deepcopy(modules_by_id[25])
feeder_f1['id'] = 251
feeder_f1['mapper']['array'] = '{{19.array}}'
feeder_f1['metadata']['designer'] = {'x': 3900, 'y': -300}
new_flow.append(feeder_f1)

# Set priceUSD variable (module 14) for Task 1
price_var1 = copy.deepcopy(modules_by_id[14])
price_var1['id'] = 141
# Update references from {{25.xxx}} to {{251.xxx}}
if 'value' in price_var1['mapper']:
    price_var1['mapper']['value'] = price_var1['mapper']['value'].replace('25.', '251.')
price_var1['metadata']['designer'] = {'x': 4200, 'y': -300}
new_flow.append(price_var1)

# Set dataCompleteness variable (module 15) for Task 1
completeness_var1 = copy.deepcopy(modules_by_id[15])
completeness_var1['id'] = 151
if 'value' in completeness_var1['mapper']:
    completeness_var1['mapper']['value'] = completeness_var1['mapper']['value'].replace('25.', '251.')
completeness_var1['metadata']['designer'] = {'x': 4500, 'y': -300}
new_flow.append(completeness_var1)

# Write FILTERED row (module 17) for Task 1
write_filtered1 = copy.deepcopy(modules_by_id[17])
write_filtered1['id'] = 171
if 'values' in write_filtered1['mapper'] and isinstance(write_filtered1['mapper']['values'], dict):
    for key in write_filtered1['mapper']['values']:
        val = write_filtered1['mapper']['values'][key]
        if isinstance(val, str):
            write_filtered1['mapper']['values'][key] = val.replace('{{25.', '{{251.').replace('{{14.', '{{141.').replace('{{15.', '{{151.')
write_filtered1['metadata']['designer'] = {'x': 4800, 'y': -300, 'name': 'Write FILTERED (Task 1)'}
new_flow.append(write_filtered1)

# TASK 2 FILTERED PATH
feeder_f2 = copy.deepcopy(modules_by_id[25])
feeder_f2['id'] = 252
feeder_f2['mapper']['array'] = '{{20.array}}'
feeder_f2['metadata']['designer'] = {'x': 3900, 'y': 0}
new_flow.append(feeder_f2)

price_var2 = copy.deepcopy(modules_by_id[14])
price_var2['id'] = 142
if 'value' in price_var2['mapper']:
    price_var2['mapper']['value'] = price_var2['mapper']['value'].replace('25.', '252.')
price_var2['metadata']['designer'] = {'x': 4200, 'y': 0}
new_flow.append(price_var2)

completeness_var2 = copy.deepcopy(modules_by_id[15])
completeness_var2['id'] = 152
if 'value' in completeness_var2['mapper']:
    completeness_var2['mapper']['value'] = completeness_var2['mapper']['value'].replace('25.', '252.')
completeness_var2['metadata']['designer'] = {'x': 4500, 'y': 0}
new_flow.append(completeness_var2)

write_filtered2 = copy.deepcopy(modules_by_id[17])
write_filtered2['id'] = 172
if 'values' in write_filtered2['mapper'] and isinstance(write_filtered2['mapper']['values'], dict):
    for key in write_filtered2['mapper']['values']:
        val = write_filtered2['mapper']['values'][key]
        if isinstance(val, str):
            write_filtered2['mapper']['values'][key] = val.replace('{{25.', '{{252.').replace('{{14.', '{{142.').replace('{{15.', '{{152.')
write_filtered2['metadata']['designer'] = {'x': 4800, 'y': 0, 'name': 'Write FILTERED (Task 2)'}
new_flow.append(write_filtered2)

# TASK 3 FILTERED PATH
feeder_f3 = copy.deepcopy(modules_by_id[25])
feeder_f3['id'] = 253
feeder_f3['mapper']['array'] = '{{21.array}}'
feeder_f3['metadata']['designer'] = {'x': 3900, 'y': 300}
new_flow.append(feeder_f3)

price_var3 = copy.deepcopy(modules_by_id[14])
price_var3['id'] = 143
if 'value' in price_var3['mapper']:
    price_var3['mapper']['value'] = price_var3['mapper']['value'].replace('25.', '253.')
price_var3['metadata']['designer'] = {'x': 4200, 'y': 300}
new_flow.append(price_var3)

completeness_var3 = copy.deepcopy(modules_by_id[15])
completeness_var3['id'] = 153
if 'value' in completeness_var3['mapper']:
    completeness_var3['mapper']['value'] = completeness_var3['mapper']['value'].replace('25.', '253.')
completeness_var3['metadata']['designer'] = {'x': 4500, 'y': 300}
new_flow.append(completeness_var3)

write_filtered3 = copy.deepcopy(modules_by_id[17])
write_filtered3['id'] = 173
if 'values' in write_filtered3['mapper'] and isinstance(write_filtered3['mapper']['values'], dict):
    for key in write_filtered3['mapper']['values']:
        val = write_filtered3['mapper']['values'][key]
        if isinstance(val, str):
            write_filtered3['mapper']['values'][key] = val.replace('{{25.', '{{253.').replace('{{14.', '{{143.').replace('{{15.', '{{153.')
write_filtered3['metadata']['designer'] = {'x': 4800, 'y': 300, 'name': 'Write FILTERED (Task 3)'}
new_flow.append(write_filtered3)

# 10. Keep Statistics (module 18) - but this needs to reference all the data
# For now, let's skip this as it requires aggregation across all paths

# 11. Keep Email (module 26) - but update positioning
email_module = copy.deepcopy(modules_by_id[26])
email_module['metadata']['designer'] = {'x': 5400, 'y': 0}
new_flow.append(email_module)

# Update the data
data['flow'] = new_flow

# Save the corrected blueprint
output_path = '/Users/swayclarke/oloxa_stuff/Lombok Invest Capital/lombok-scraper-make-blueprint-v2-fixed.json'
with open(output_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Created corrected blueprint with {len(new_flow)} modules")
print(f"✅ Saved to: {output_path}")
print(f"\nModule flow:")
print(f"1. Webhook")
print(f"2-4. Get Task 1, 2, 3 Results (parallel)")
print(f"5. Create RAW Sheet")
print(f"6. Write RAW Headers")
print(f"7-12. Three separate paths to write RAW data")
print(f"13. Create FILTERED Sheet")
print(f"14. Write FILTERED Headers")
print(f"15-26. Three separate paths to write FILTERED data")
print(f"27. Send Email")
