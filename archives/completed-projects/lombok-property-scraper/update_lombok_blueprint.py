#!/usr/bin/env python3
"""
Lombok Blueprint Update Script
Automates the replacement of hardcoded values with variables
"""

import json
import sys
from pathlib import Path


def update_blueprint(input_file, output_file):
    """Update the Lombok blueprint with variables and improvements"""

    print(f"📖 Reading blueprint from: {input_file}")

    with open(input_file, 'r', encoding='utf-8') as f:
        blueprint = json.load(f)

    # Statistics
    replacements = {
        'spreadsheet_id': 0,
        'email_addresses': 0,
        'datastore_id': 0
    }

    # Replacement mappings
    replacements_map = {
        '1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54': '{{1.spreadsheetId}}',
        'sway@oloxa.ai': '{{1.notificationEmail}}',
        '81942': '{{1.dataStoreId}}'
    }

    # Variable module to insert
    variable_module = {
        "id": 1,
        "module": "builtin:SetVariables",
        "version": 1,
        "parameters": {},
        "mapper": {
            "variables": [
                {
                    "name": "userEmail",
                    "value": "swayclarkeii@gmail.com"
                },
                {
                    "name": "notificationEmail",
                    "value": "sway@oloxa.ai"
                },
                {
                    "name": "spreadsheetId",
                    "value": "1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54"
                },
                {
                    "name": "dataStoreId",
                    "value": "81942"
                },
                {
                    "name": "workflowName",
                    "value": "Lombok Invest Capital Property Scraper"
                }
            ],
            "scope": "roundtrip"
        },
        "metadata": {
            "designer": {
                "x": -300,
                "y": 0,
                "name": "🔧 Configuration Variables"
            },
            "restore": {},
            "parameters": [],
            "expect": [
                {
                    "name": "variables",
                    "spec": [
                        {
                            "name": "name",
                            "type": "text",
                            "label": "Variable name",
                            "required": True
                        },
                        {
                            "name": "value",
                            "label": "Variable value"
                        }
                    ],
                    "type": "array",
                    "label": "Variables"
                },
                {
                    "name": "scope",
                    "type": "select",
                    "label": "Variable lifetime",
                    "validate": {
                        "enum": [
                            "roundtrip",
                            "execution"
                        ]
                    }
                }
            ]
        }
    }

    # Insert variable module at the beginning
    print("✨ Adding variable module at the start...")
    blueprint['flow'].insert(0, variable_module)

    # Convert blueprint to string for replacements
    blueprint_str = json.dumps(blueprint, indent=4)

    # Perform replacements
    print("🔄 Replacing hardcoded values...")

    for old_value, new_value in replacements_map.items():
        count = blueprint_str.count(f'"{old_value}"')
        if count > 0:
            blueprint_str = blueprint_str.replace(f'"{old_value}"', f'"{new_value}"')
            print(f"  ✓ Replaced {count} occurrences of: {old_value[:40]}...")

            if 'spreadsheet' in new_value.lower():
                replacements['spreadsheet_id'] += count
            elif 'email' in new_value.lower():
                replacements['email_addresses'] += count
            elif 'datastore' in new_value.lower():
                replacements['datastore_id'] += count

    # Also handle integer datastore ID (not in quotes)
    count = blueprint_str.count(': 81942')
    blueprint_str = blueprint_str.replace(': 81942', ': "{{1.dataStoreId}}"')
    replacements['datastore_id'] += count
    print(f"  ✓ Replaced {count} occurrences of datastore ID (unquoted)")

    # Convert back to JSON
    blueprint = json.loads(blueprint_str)

    # Update module 515 (New Leads email)
    print("📧 Updating module 515 (New Leads email)...")
    for module in blueprint['flow']:
        if module.get('id') == 515:
            # Update subject
            if 'mapper' in module and 'subject' in module['mapper']:
                module['mapper']['subject'] = "🎉 You Got {{length(508.array) + length(260.array) + length(261.array)}} New Lombok Leads!"

            # Update HTML body
            if 'mapper' in module and 'html' in module['mapper']:
                module['mapper']['html'] = '''<div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
    <h2 style="color: #2c3e50;">🎉 New Lombok Invest Capital Leads!</h2>

    <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #34495e;">📊 Summary</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background-color: #ecf0f1;">
                <td style="padding: 10px; border: 1px solid #bdc3c7;"><strong>Task 1 (New Properties)</strong></td>
                <td style="padding: 10px; border: 1px solid #bdc3c7;">{{length(508.array)}}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #bdc3c7;"><strong>Task 2 (New Properties)</strong></td>
                <td style="padding: 10px; border: 1px solid #bdc3c7;">{{length(260.array)}}</td>
            </tr>
            <tr style="background-color: #ecf0f1;">
                <td style="padding: 10px; border: 1px solid #bdc3c7;"><strong>Task 3 (New Properties)</strong></td>
                <td style="padding: 10px; border: 1px solid #bdc3c7;">{{length(261.array)}}</td>
            </tr>
            <tr style="background-color: #3498db; color: white;">
                <td style="padding: 10px; border: 1px solid #2980b9;"><strong>Total New Properties</strong></td>
                <td style="padding: 10px; border: 1px solid #2980b9;"><strong>{{length(508.array) + length(260.array) + length(261.array)}}</strong></td>
            </tr>
        </table>
    </div>

    <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
        <p style="margin: 0; color: #856404;">
            <strong>⏰ Run Time:</strong> {{formatDate(now; "YYYY-MM-DD HH:mm:ss")}}
        </p>
    </div>

    <div style="margin: 20px 0;">
        <a href="{{514.webViewLink}}" style="display: inline-block; background-color: #27ae60; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">
            📄 View Full Report
        </a>
    </div>

    <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px;">
        This is an automated report from {{1.workflowName}}. Running bi-weekly.
    </p>
</div>'''
            print("  ✓ Module 515 email body and subject updated")
            break

    # Save updated blueprint
    print(f"💾 Saving updated blueprint to: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(blueprint, f, indent=4, ensure_ascii=False)

    # Print summary
    print("\n" + "="*60)
    print("✅ BLUEPRINT UPDATE COMPLETE!")
    print("="*60)
    print(f"📊 Replacements Made:")
    print(f"  • Spreadsheet IDs: {replacements['spreadsheet_id']}")
    print(f"  • Email addresses: {replacements['email_addresses']}")
    print(f"  • DataStore IDs: {replacements['datastore_id']}")
    print(f"\n✨ Enhancements:")
    print(f"  • Variable module added at position 0")
    print(f"  • Module 515 email enhanced with property counts")
    print(f"  • Subject line now includes dynamic count")
    print(f"\n📝 Next Steps:")
    print(f"  1. Review the output file: {output_file}")
    print(f"  2. Import into Make.com")
    print(f"  3. Add error handlers manually (see implementation guide)")
    print(f"  4. Test with small data set")
    print("="*60)


if __name__ == "__main__":
    # File paths
    input_file = Path("/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v5.blueprint (1).json")
    output_file = Path("/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v6.blueprint.json")

    if not input_file.exists():
        print(f"❌ Error: Input file not found: {input_file}")
        sys.exit(1)

    try:
        update_blueprint(input_file, output_file)
    except Exception as e:
        print(f"❌ Error updating blueprint: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
