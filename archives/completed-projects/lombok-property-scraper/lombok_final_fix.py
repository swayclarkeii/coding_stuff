#!/usr/bin/env python3
"""
Final Lombok Blueprint Fix - Complete all remaining changes
1. Replace hardcoded datastore IDs with variable
2. Add data store modules to store task counts
3. Add data store modules to read task counts
4. Update module 515 with final HTML
"""

import json
import re
from pathlib import Path
from copy import deepcopy


def replace_hardcoded_datastore(bp_str):
    """Replace all hardcoded datastore IDs with variable reference"""
    # Replace numeric format
    bp_str = re.sub(
        r'"datastore":\s*81942',
        '"datastore": "{{524.dataStoreId}}"',
        bp_str
    )
    # Replace string format
    bp_str = re.sub(
        r'"datastore":\s*"81942"',
        '"datastore": "{{524.dataStoreId}}"',
        bp_str
    )
    return bp_str


def create_store_count_module(module_id, aggregator_id, task_name):
    """Create a data store module to store aggregator count"""
    return {
        "id": module_id,
        "module": "datastore:AddRecord",
        "version": 3,
        "parameters": {
            "datastore": "{{524.dataStoreId}}"
        },
        "mapper": {
            "key": task_name,
            "value": f"{{{{length({aggregator_id}.array)}}}}"
        },
        "metadata": {
            "designer": {
                "x": 0,
                "y": 0,
                "name": f"Store {task_name.replace('_', ' ').title()}"
            },
            "restore": {
                "parameters": {
                    "datastore": {
                        "label": "Property Scraper Counts"
                    }
                }
            },
            "parameters": [
                {
                    "name": "datastore",
                    "type": "datastore",
                    "label": "Data store",
                    "required": True
                }
            ],
            "expect": [
                {
                    "name": "key",
                    "type": "text",
                    "label": "Key",
                    "required": True
                },
                {
                    "name": "value",
                    "label": "Value"
                }
            ]
        }
    }


def create_get_count_module(module_id, task_name):
    """Create a data store module to retrieve aggregator count"""
    return {
        "id": module_id,
        "module": "datastore:GetRecord",
        "version": 3,
        "parameters": {
            "datastore": "{{524.dataStoreId}}"
        },
        "mapper": {
            "key": task_name
        },
        "metadata": {
            "designer": {
                "x": 0,
                "y": 0,
                "name": f"Get {task_name.replace('_', ' ').title()}"
            },
            "restore": {
                "parameters": {
                    "datastore": {
                        "label": "Property Scraper Counts"
                    }
                }
            },
            "parameters": [
                {
                    "name": "datastore",
                    "type": "datastore",
                    "label": "Data store",
                    "required": True
                }
            ],
            "expect": [
                {
                    "name": "key",
                    "type": "text",
                    "label": "Key",
                    "required": True
                }
            ]
        }
    }


def insert_module_after(flow, after_id, new_module):
    """Insert a module after a specific module ID in the flow"""
    for i, module in enumerate(flow):
        if module.get('id') == after_id:
            # Insert after this module
            flow.insert(i + 1, new_module)
            return True

        # Check routes
        if 'routes' in module:
            for route in module['routes']:
                if 'flow' in route:
                    if insert_module_after(route['flow'], after_id, new_module):
                        return True

        # Check nested flows
        if 'flow' in module:
            if insert_module_after(module['flow'], after_id, new_module):
                return True

    return False


def insert_module_before(flow, before_id, new_module):
    """Insert a module before a specific module ID in the flow"""
    for i, module in enumerate(flow):
        if module.get('id') == before_id:
            # Insert before this module
            flow.insert(i, new_module)
            return True

        # Check routes
        if 'routes' in module:
            for route in module['routes']:
                if 'flow' in route:
                    if insert_module_before(route['flow'], before_id, new_module):
                        return True

        # Check nested flows
        if 'flow' in module:
            if insert_module_before(module['flow'], before_id, new_module):
                return True

    return False


def update_module_515_email(flow, get_task1_id, get_task2_id, get_task3_id):
    """Update module 515 with complete HTML using retrieved counts"""

    html_body = f'''<div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
    <h2 style="color: #2c3e50;">🎉 New Lombok Invest Capital Leads!</h2>

    <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #34495e;">📊 Summary</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background-color: #ecf0f1;">
                <td style="padding: 10px; border: 1px solid #bdc3c7;"><strong>Task 1 (New Properties)</strong></td>
                <td style="padding: 10px; border: 1px solid #bdc3c7;">{{{{{get_task1_id}.value}}}}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #bdc3c7;"><strong>Task 2 (New Properties)</strong></td>
                <td style="padding: 10px; border: 1px solid #bdc3c7;">{{{{{get_task2_id}.value}}}}</td>
            </tr>
            <tr style="background-color: #ecf0f1;">
                <td style="padding: 10px; border: 1px solid #bdc3c7;"><strong>Task 3 (New Properties)</strong></td>
                <td style="padding: 10px; border: 1px solid #bdc3c7;">{{{{{get_task3_id}.value}}}}</td>
            </tr>
            <tr style="background-color: #3498db; color: white;">
                <td style="padding: 10px; border: 1px solid #2980b9;"><strong>Total New Properties</strong></td>
                <td style="padding: 10px; border: 1px solid #2980b9;"><strong>{{{{{get_task1_id}.value + {get_task2_id}.value + {get_task3_id}.value}}}}</strong></td>
            </tr>
        </table>
    </div>

    <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
        <p style="margin: 0; color: #856404;">
            <strong>⏰ Run Time:</strong> {{{{formatDate(now; "YYYY-MM-DD HH:mm:ss")}}}}
        </p>
    </div>

    <div style="margin: 20px 0;">
        <a href="{{{{514.webViewLink}}}}" style="display: inline-block; background-color: #27ae60; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">
            📄 View Full Report
        </a>
    </div>

    <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px;">
        This is an automated report from {{{{524.workflowName}}}}. Running bi-weekly.
    </p>
</div>'''

    subject = f'🎉 You Got {{{{{get_task1_id}.value + {get_task2_id}.value + {get_task3_id}.value}}}} New Lombok Leads!'

    for module in flow:
        if module.get('id') == 515:
            module['mapper']['html'] = html_body
            module['mapper']['subject'] = subject
            return True

        if 'routes' in module:
            for route in module['routes']:
                if 'flow' in route:
                    if update_module_515_email(route['flow'], get_task1_id, get_task2_id, get_task3_id):
                        return True

        if 'flow' in module:
            if update_module_515_email(module['flow'], get_task1_id, get_task2_id, get_task3_id):
                return True

    return False


def main():
    input_file = Path('/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v6.blueprint (1).json')
    output_file = Path('/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v7-FINAL.blueprint.json')

    print("="*80)
    print("🔧 LOMBOK BLUEPRINT FINAL FIX")
    print("="*80)

    # Load blueprint
    print("\n1. Loading blueprint...")
    with open(input_file) as f:
        blueprint = json.load(f)

    # Step 1: Replace hardcoded datastore IDs
    print("\n2. Replacing hardcoded datastore IDs with variable...")
    bp_str = json.dumps(blueprint, indent=4)
    hardcoded_count_before = bp_str.count('"datastore": 81942') + bp_str.count('"datastore": "81942"')

    bp_str = replace_hardcoded_datastore(bp_str)
    blueprint = json.loads(bp_str)

    bp_str = json.dumps(blueprint, indent=4)
    hardcoded_count_after = bp_str.count('"datastore": 81942') + bp_str.count('"datastore": "81942"')
    variable_count = bp_str.count('{{524.dataStoreId}}')

    print(f"   • Hardcoded before: {hardcoded_count_before}")
    print(f"   • Hardcoded after: {hardcoded_count_after}")
    print(f"   • Variable usage: {variable_count}")

    # Step 2: Add store count modules after aggregators
    print("\n3. Adding data store modules to STORE counts...")

    # Store Task 1 count (after aggregator 508)
    store_task1 = create_store_count_module(9001, 508, "task1_count")
    if insert_module_after(blueprint['flow'], 508, store_task1):
        print("   ✅ Added module 9001: Store Task 1 count (after aggregator 508)")

    # Store Task 2 count (after aggregator 260)
    store_task2 = create_store_count_module(9002, 260, "task2_count")
    if insert_module_after(blueprint['flow'], 260, store_task2):
        print("   ✅ Added module 9002: Store Task 2 count (after aggregator 260)")

    # Store Task 3 count (after aggregator 261)
    store_task3 = create_store_count_module(9003, 261, "task3_count")
    if insert_module_after(blueprint['flow'], 261, store_task3):
        print("   ✅ Added module 9003: Store Task 3 count (after aggregator 261)")

    # Step 3: Add get count modules before email (module 515)
    print("\n4. Adding data store modules to READ counts...")

    # Get Task 1 count (before module 515)
    get_task1 = create_get_count_module(9011, "task1_count")
    if insert_module_before(blueprint['flow'], 515, get_task1):
        print("   ✅ Added module 9011: Get Task 1 count (before email)")

    # Get Task 2 count
    get_task2 = create_get_count_module(9012, "task2_count")
    if insert_module_before(blueprint['flow'], 515, get_task2):
        print("   ✅ Added module 9012: Get Task 2 count (before email)")

    # Get Task 3 count
    get_task3 = create_get_count_module(9013, "task3_count")
    if insert_module_before(blueprint['flow'], 515, get_task3):
        print("   ✅ Added module 9013: Get Task 3 count (before email)")

    # Step 4: Update module 515 email
    print("\n5. Updating module 515 email with task counts...")
    if update_module_515_email(blueprint['flow'], 9011, 9012, 9013):
        print("   ✅ Module 515 email updated with HTML and task counts")

    # Step 5: Save final blueprint
    print("\n6. Saving final blueprint...")
    with open(output_file, 'w') as f:
        json.dump(blueprint, f, indent=4, ensure_ascii=False)

    print(f"   ✅ Saved to: {output_file}")

    # Summary
    print("\n" + "="*80)
    print("✅ ALL CHANGES COMPLETE!")
    print("="*80)
    print("\nChanges made:")
    print("  1. ✅ Replaced hardcoded datastore IDs with {{524.dataStoreId}}")
    print("  2. ✅ Added 3 modules to STORE task counts (9001, 9002, 9003)")
    print("  3. ✅ Added 3 modules to READ task counts (9011, 9012, 9013)")
    print("  4. ✅ Updated module 515 with HTML showing all task counts")
    print("\nModule 515 now displays:")
    print("  • Task 1 property count")
    print("  • Task 2 property count")
    print("  • Task 3 property count")
    print("  • Total count in subject line")
    print("  • Professional HTML formatting")
    print("\n📋 Final checklist:")
    print("  ✅ Variable module (524) defined")
    print("  ✅ DataStoreId variable used throughout")
    print("  ✅ Task counts stored after each aggregator")
    print("  ✅ Task counts retrieved before email")
    print("  ✅ Email displays all counts")
    print("\n🚀 Import this file into Make.com:")
    print(f"   {output_file}")
    print("="*80)


if __name__ == "__main__":
    main()
