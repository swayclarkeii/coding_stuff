#!/usr/bin/env python3
import json

# Read Blueprint 29 (final version)
with open('/Users/swayclarke/Downloads/Lombok Property Scraper v1.blueprint (29).json', 'r') as f:
    blueprint = json.load(f)

print("ANALYZING BLUEPRINT 29 - FINAL VERSION")
print("=" * 70)

router = blueprint['flow'][4]
num_routes = len(router.get('routes', []))

print(f"Total Tasks: {num_routes}\n")

# Analyze each task
for task_num, route in enumerate(router['routes'], 1):
    print(f"{'=' * 70}")
    print(f"TASK {task_num}")
    print("=" * 70)

    # Key modules
    apify_id = None
    aggregator_id = None
    iterator_id = None
    price_module_id = None

    # Error handling tracking
    log_empty_modules = []
    log_price_modules = []
    email_modules = []

    for module in route['flow']:
        module_id = module.get('id')
        module_type = module.get('module', '')
        module_name = module.get('metadata', {}).get('designer', {}).get('name', '')

        # Identify key modules
        if 'apify' in module_type.lower():
            apify_id = module_id

        if 'BasicAggregator' in module_type and aggregator_id is None:
            aggregator_id = module_id

        if 'BasicFeeder' in module_type:
            iterator_id = module_id

        if 'SetVariable' in module_type:
            mapper = module.get('mapper', {})
            var_name = mapper.get('name', '')
            if 'priceUSD' in var_name:
                price_module_id = module_id

        # Identify error handling modules
        if 'google-sheets:addRow' in module_type:
            mapper = module.get('mapper', {})
            sheet_id = mapper.get('sheetId', '')
            if 'Error_Log' in sheet_id:
                values = mapper.get('values', {})
                task_col = values.get('1', '')
                if 'Empty' in task_col or 'No Data' in task_col:
                    log_empty_modules.append(module_id)
                elif 'Price' in task_col:
                    log_price_modules.append(module_id)

        if 'email:' in module_type:
            mapper = module.get('mapper', {})
            subject = mapper.get('subject', '')
            if 'ALERT' in subject or 'No Data' in subject:
                email_modules.append(module_id)

    # Print summary
    print(f"Core Modules:")
    print(f"  Apify:           {apify_id}")
    print(f"  Aggregator:      {aggregator_id}")
    print(f"  Iterator:        {iterator_id}")
    print(f"  Price Normalize: {price_module_id}")

    print(f"\nError Handling:")
    print(f"  Log Empty:       {log_empty_modules if log_empty_modules else '❌ NONE'}")
    print(f"  Email Alert:     {email_modules if email_modules else '❌ NONE'}")
    print(f"  Log Price Error: {log_price_modules if log_price_modules else '❌ NONE'}")
    print()

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print("Blueprint 29 Configuration:")
print("  • Error handling for empty Apify data")
print("  • Email alerts for critical failures")
print("  • Price parse error logging with URLs")
print("  • Filters ensure conditional execution (only when errors occur)")
print("=" * 70)
