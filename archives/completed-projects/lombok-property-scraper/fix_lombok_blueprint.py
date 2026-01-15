#!/usr/bin/env python3
"""
Fix circular variable references in Lombok v6 blueprint
"""

import json
from pathlib import Path


def fix_blueprint(input_file, output_file):
    """Fix the circular variable references"""

    print("🔧 Fixing circular variable references...")

    with open(input_file, 'r', encoding='utf-8') as f:
        blueprint = json.load(f)

    # Find and fix the variable module (should be first)
    if blueprint['flow'] and blueprint['flow'][0].get('module') == 'builtin:SetVariables':
        variables = blueprint['flow'][0]['mapper']['variables']

        # Fix each variable
        for var in variables:
            if var['name'] == 'notificationEmail' and '{{' in var['value']:
                var['value'] = 'sway@oloxa.ai'
                print("  ✓ Fixed notificationEmail")

            elif var['name'] == 'spreadsheetId' and '{{' in var['value']:
                var['value'] = '1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54'
                print("  ✓ Fixed spreadsheetId")

            elif var['name'] == 'dataStoreId' and '{{' in var['value']:
                var['value'] = '81942'
                print("  ✓ Fixed dataStoreId")

    # Save fixed blueprint
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(blueprint, f, indent=4, ensure_ascii=False)

    print(f"✅ Fixed blueprint saved to: {output_file}")


if __name__ == "__main__":
    input_file = Path("/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v6.blueprint.json")
    output_file = Path("/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v6-FIXED.blueprint.json")

    fix_blueprint(input_file, output_file)
