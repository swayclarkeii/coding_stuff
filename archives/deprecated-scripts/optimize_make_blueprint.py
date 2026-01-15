#!/usr/bin/env python3
"""
Optimize Make.com Blueprint for Credit Reduction
- Remove unused Module 151, 152, 153 (Data Quality Check modules)
- Add early filters after Module 10 (RAW write) before price normalization
- Simplify filters on Modules 171, 172, 173 to only check price
"""

import json
import sys
from pathlib import Path

def add_filter_to_module(module, filter_conditions):
    """Add filter conditions to a module"""
    module["filter"] = {
        "name": "Early Filter - Before Price Normalization",
        "conditions": [filter_conditions]
    }
    return module

def simplify_filtered_write_filter(module):
    """Simplify filter to only check priceUSD <= 300000"""
    # Keep only the price filter condition
    if "filter" in module and "conditions" in module["filter"]:
        # Find the price condition
        for condition_group in module["filter"]["conditions"]:
            price_condition = None
            for condition in condition_group:
                if "priceUSD" in condition.get("a", ""):
                    price_condition = condition
                    break

            if price_condition:
                module["filter"]["conditions"] = [[price_condition]]
                module["filter"]["name"] = "Price Filter Only"

    return module

def optimize_blueprint(input_file, output_file):
    """Main optimization function"""

    print(f"Loading blueprint from: {input_file}")
    with open(input_file, 'r') as f:
        blueprint = json.load(f)

    if "flow" not in blueprint:
        print("ERROR: No 'flow' found in blueprint")
        return False

    # Step 1: Find and remove modules 151, 152, 153
    modules_to_remove = {151, 152, 153}
    original_count = len(blueprint["flow"])

    blueprint["flow"] = [
        module for module in blueprint["flow"]
        if module.get("id") not in modules_to_remove
    ]

    removed_count = original_count - len(blueprint["flow"])
    print(f"✅ Removed {removed_count} unused Data Quality Check modules (151, 152, 153)")

    # Step 2: Add early filters to Modules 141, 142, 143 (Price Normalization)
    # These filters apply BEFORE price normalization
    early_filter_conditions = [
        {
            "a": "{{23.hasKuta}}",  # Task 1 uses module 23
            "b": "{{true}}",
            "o": "text:equal"
        },
        {
            "a": "{{23.url}}",
            "b": "-land",
            "o": "text:notcontain:ci"
        },
        {
            "a": "{{23.url}}",
            "b": "-sold",
            "o": "text:notcontain:ci"
        },
        {
            "a": "{{23.constructionStatus}}",
            "b": "Off-Plan",
            "o": "text:notequal:ci"
        },
        {
            "a": "{{23.constructionStatus}}",
            "b": "Under Construction",
            "o": "text:notequal:ci"
        }
    ]

    # Task 2 early filter (uses module 232)
    early_filter_task2 = [
        {
            "a": "{{232.hasKuta}}",
            "b": "{{true}}",
            "o": "text:equal"
        },
        {
            "a": "{{232.url}}",
            "b": "-land",
            "o": "text:notcontain:ci"
        },
        {
            "a": "{{232.url}}",
            "b": "-sold",
            "o": "text:notcontain:ci"
        },
        {
            "a": "{{232.constructionStatus}}",
            "b": "Off-Plan",
            "o": "text:notequal:ci"
        },
        {
            "a": "{{232.constructionStatus}}",
            "b": "Under Construction",
            "o": "text:notequal:ci"
        }
    ]

    # Task 3 early filter (uses module 233)
    early_filter_task3 = [
        {
            "a": "{{233.hasKuta}}",
            "b": "{{true}}",
            "o": "text:equal"
        },
        {
            "a": "{{233.url}}",
            "b": "-land",
            "o": "text:notcontain:ci"
        },
        {
            "a": "{{233.url}}",
            "b": "-sold",
            "o": "text:notcontain:ci"
        },
        {
            "a": "{{233.constructionStatus}}",
            "b": "Off-Plan",
            "o": "text:notequal:ci"
        },
        {
            "a": "{{233.constructionStatus}}",
            "b": "Under Construction",
            "o": "text:notequal:ci"
        }
    ]

    for module in blueprint["flow"]:
        module_id = module.get("id")

        # Add early filter to price normalization modules
        if module_id == 141:  # Task 1 - Normalize Price USD
            add_filter_to_module(module, early_filter_conditions)
            print(f"✅ Added early filter to Module 141 (Task 1 - Normalize Price USD)")

        elif module_id == 142:  # Task 2 - Normalize Price USD
            add_filter_to_module(module, early_filter_task2)
            print(f"✅ Added early filter to Module 142 (Task 2 - Normalize Price USD)")

        elif module_id == 143:  # Task 3 - Normalize Price USD
            add_filter_to_module(module, early_filter_task3)
            print(f"✅ Added early filter to Module 143 (Task 3 - Normalize Price USD)")

        # Simplify filters on FILTERED write modules
        elif module_id == 171:  # Task 1 - Write FILTERED
            simplify_filtered_write_filter(module)
            print(f"✅ Simplified filter on Module 171 (Task 1 - Write FILTERED) to price-only")

        elif module_id == 172:  # Task 2 - Write FILTERED
            simplify_filtered_write_filter(module)
            print(f"✅ Simplified filter on Module 172 (Task 2 - Write FILTERED) to price-only")

        elif module_id == 173:  # Task 3 - Write FILTERED
            simplify_filtered_write_filter(module)
            print(f"✅ Simplified filter on Module 173 (Task 3 - Write FILTERED) to price-only")

    # Step 3: Save optimized blueprint
    print(f"\nSaving optimized blueprint to: {output_file}")
    with open(output_file, 'w') as f:
        json.dump(blueprint, f, indent=2)

    print(f"\n✅ Optimization complete!")
    print(f"📊 Estimated credit savings: ~56% per run")
    print(f"📁 Output file: {output_file}")

    return True

if __name__ == "__main__":
    input_file = "/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v2 (testing).blueprint (1).json"
    output_file = "/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v3 (optimized).json"

    if not Path(input_file).exists():
        print(f"ERROR: Input file not found: {input_file}")
        sys.exit(1)

    success = optimize_blueprint(input_file, output_file)
    sys.exit(0 if success else 1)
