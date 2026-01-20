import json

# Read the original blueprint
with open('/Users/swayclarke/Downloads/Lombok Property Scraper v1.blueprint (1).json', 'r') as f:
    data = json.load(f)

# Find module 5 (the problematic BasicAggregator)
for module in data['flow']:
    if module['id'] == 5:
        print("Found Array Aggregator (module 5)")
        print(f"Current feeder: {module['parameters'].get('feeder', 'not set')}")

        # The issue: it's only set to aggregate from module 19 (Task 1)
        # We need it to aggregate from ALL three modules (19, 20, 21)

        # Remove the single feeder parameter
        if 'feeder' in module['parameters']:
            del module['parameters']['feeder']

        # Add proper mapper configuration to merge all arrays
        # Note: In Make.com, to aggregate multiple sources, we need to use
        # the aggregator differently - aggregate items from multiple runs
        # OR use a Text Aggregator with array functions

        # Actually, the proper way is to keep this as is but change the approach:
        # Instead of aggregating from one source, we need to configure it properly

        # For Make.com Array Aggregator, the feeder should be the iterator
        # But we have 3 separate datasets, not 3 iterations of one dataset

        # The real fix: Remove aggregator and use sequential processing
        print("\n⚠️  Array Aggregator cannot merge 3 separate datasets directly in Make.com")
        print("The aggregator is designed to collect data from ITERATIONS, not from multiple parallel sources")

        break

print("\n" + "="*60)
print("THE CORRECT SOLUTION:")
print("="*60)
print("""
You have two practical options in Make.com:

OPTION A: Sequential Processing (Recommended)
-------------------------------------------
Webhook
  ↓
Get Task 1 → Iterator → Write RAW rows → (continue to next task)
  ↓
Get Task 2 → Iterator → Write RAW rows → (continue to next task)
  ↓
Get Task 3 → Iterator → Write RAW rows
  ↓
Create FILTERED sheet
  ↓
Same sequential process for filtered data
  ↓
Send Email

How to build this:
1. Delete the Array Aggregator (module 5)
2. Connect "Get Task 1 Results" directly to "Create RAW Data Sheet"
3. After writing all Task 1 rows, connect to "Get Task 2 Results"
4. After writing all Task 2 rows, connect to "Get Task 3 Results"
5. Continue the rest of the flow

OPTION B: Use Text Aggregator + toArray()
------------------------------------------
This is more complex but keeps parallel processing:

1. Replace Array Aggregator with "Tools > Compose a string"
2. Set value to: {{toString(19.array)}}{{toString(20.array)}}{{toString(21.array)}}
3. Use "Tools > Parse JSON" to convert back to array
4. Continue with Iterator

However, this is hacky and may hit size limits.
""")

print("\nI recommend OPTION A (Sequential). It's cleaner and more reliable.")
print("\nWould you like me to create a blueprint with Option A implemented?")
