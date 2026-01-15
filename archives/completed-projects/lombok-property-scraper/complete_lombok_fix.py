#!/usr/bin/env python3
"""
Complete Lombok Blueprint Fix - Actually update everything
"""

import json
import re
from pathlib import Path


def fix_blueprint_complete(input_file, output_file):
    """Complete fix with all replacements"""

    print("🔧 Starting complete blueprint fix...")

    with open(input_file, 'r', encoding='utf-8') as f:
        blueprint = json.load(f)

    changes = {
        'spreadsheet_ids': 0,
        'email_updated': False,
        'datastore_verified': 0
    }

    # Convert to string for regex replacements
    bp_str = json.dumps(blueprint, indent=4)

    # 1. Replace spreadsheet IDs that weren't caught
    # The issue is the spreadsheet ID appears in a path format
    print("\n1. Fixing spreadsheet ID references...")

    # Pattern: "spreadsheetId": "/path/to/1W2rnvacmbVl-..."
    pattern = r'"spreadsheetId":\s*"[^"]*1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54"'
    matches = re.findall(pattern, bp_str)
    print(f"   Found {len(matches)} spreadsheet ID references in paths")

    bp_str = re.sub(
        r'"spreadsheetId":\s*"[^"]*1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54"',
        '"spreadsheetId": "{{1.spreadsheetId}}"',
        bp_str
    )
    changes['spreadsheet_ids'] = len(matches)

    # Convert back to JSON
    blueprint = json.loads(bp_str)

    # 2. Update Module 515 email body and subject
    print("\n2. Updating Module 515 (New Leads email)...")

    def find_and_update_module_515(flow):
        """Recursively find and update module 515"""
        for module in flow:
            if module.get('id') == 515:
                # Update subject
                if 'mapper' in module:
                    module['mapper']['subject'] = "🎉 You Got {{length(508.array) + length(260.array) + length(261.array)}} New Lombok Leads!"

                    # Update HTML body
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
                    print("   ✅ Module 515 email body and subject updated")
                    return True

            # Check nested flows (routers, error handlers)
            if 'routes' in module:
                for route in module['routes']:
                    if 'flow' in route:
                        if find_and_update_module_515(route['flow']):
                            return True

            if 'flow' in module:
                if find_and_update_module_515(module['flow']):
                    return True

        return False

    changes['email_updated'] = find_and_update_module_515(blueprint['flow'])

    # 3. Verify datastore replacements
    bp_str = json.dumps(blueprint, indent=4)
    changes['datastore_verified'] = len(re.findall(r'"datastore":\s*"{{1\.dataStoreId}}"', bp_str))

    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(blueprint, f, indent=4, ensure_ascii=False)

    print("\n" + "="*70)
    print("✅ COMPLETE FIX APPLIED")
    print("="*70)
    print(f"📊 Changes Made:")
    print(f"  • Spreadsheet IDs replaced: {changes['spreadsheet_ids']}")
    print(f"  • Module 515 email updated: {'✅ YES' if changes['email_updated'] else '❌ NO'}")
    print(f"  • DataStore IDs verified: {changes['datastore_verified']}")
    print(f"\n💾 Saved to: {output_file}")
    print("="*70)

    return changes


if __name__ == "__main__":
    input_file = Path("/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v6-FIXED.blueprint.json")
    output_file = Path("/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v6-COMPLETE.blueprint.json")

    changes = fix_blueprint_complete(input_file, output_file)

    if changes['spreadsheet_ids'] > 0 and changes['email_updated']:
        print("\n🎉 SUCCESS! Blueprint is now complete.")
    else:
        print("\n⚠️  Some changes may not have applied. Review output above.")
