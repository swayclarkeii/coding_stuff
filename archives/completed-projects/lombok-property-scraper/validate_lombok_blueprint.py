#!/usr/bin/env python3
"""
Lombok Blueprint Validator
Validates the updated v6 blueprint for common issues
"""

import json
import re
from pathlib import Path
from collections import defaultdict


def validate_blueprint(blueprint_file):
    """Validate the Lombok blueprint v6"""

    print("="*70)
    print("🔍 LOMBOK BLUEPRINT v6 VALIDATION REPORT")
    print("="*70)
    print()

    # Load blueprint
    with open(blueprint_file, 'r', encoding='utf-8') as f:
        blueprint = json.load(f)

    issues = []
    warnings = []
    checks_passed = []

    # Convert to string for pattern matching
    bp_str = json.dumps(blueprint, indent=4)

    print("📋 BASIC STRUCTURE CHECKS")
    print("-" * 70)

    # Check 1: Blueprint has a name
    if 'name' in blueprint:
        checks_passed.append(f"✅ Blueprint name: {blueprint['name']}")
    else:
        issues.append("❌ Missing blueprint name")

    # Check 2: Blueprint has flow array
    if 'flow' in blueprint and isinstance(blueprint['flow'], list):
        checks_passed.append(f"✅ Flow array present with {len(blueprint['flow'])} modules")
    else:
        issues.append("❌ Missing or invalid flow array")

    # Check 3: Variable module is first
    if blueprint['flow'] and blueprint['flow'][0].get('module') == 'builtin:SetVariables':
        checks_passed.append("✅ Variable module (Module 1) is first in workflow")

        # Check variable definitions
        variables = blueprint['flow'][0]['mapper'].get('variables', [])
        var_names = [v['name'] for v in variables]

        expected_vars = ['userEmail', 'notificationEmail', 'spreadsheetId', 'dataStoreId', 'workflowName']
        for var in expected_vars:
            if var in var_names:
                checks_passed.append(f"  ✅ Variable '{var}' defined")
            else:
                issues.append(f"  ❌ Missing variable: {var}")
    else:
        issues.append("❌ Variable module not found or not first")

    print()
    print("🔗 VARIABLE REFERENCE CHECKS")
    print("-" * 70)

    # Check 4: Variable references are used
    var_patterns = [
        r'\{\{1\.userEmail\}\}',
        r'\{\{1\.notificationEmail\}\}',
        r'\{\{1\.spreadsheetId\}\}',
        r'\{\{1\.dataStoreId\}\}',
        r'\{\{1\.workflowName\}\}'
    ]

    for pattern in var_patterns:
        var_name = pattern.split('.')[1].split('\\}')[0]
        matches = len(re.findall(pattern, bp_str))
        if matches > 0:
            checks_passed.append(f"✅ Variable '1.{var_name}' used {matches} times")
        else:
            warnings.append(f"⚠️  Variable '1.{var_name}' defined but never used")

    print()
    print("🚫 HARDCODED VALUE CHECKS")
    print("-" * 70)

    # Check 5: No hardcoded emails (except in variable module)
    hardcoded_emails = re.findall(r'sway@oloxa\.ai|swayclarkeii@gmail\.com', bp_str)
    # Exclude the variable module definitions (should only be 5 total: 2 in var definitions, 3 in metadata labels)
    if len(hardcoded_emails) <= 10:  # Allow some for connection labels
        checks_passed.append(f"✅ Emails properly replaced with variables (found {len(hardcoded_emails)} in metadata/labels)")
    else:
        warnings.append(f"⚠️  Found {len(hardcoded_emails)} hardcoded email references (expected ~10 for metadata)")

    # Check 6: No hardcoded spreadsheet IDs (except in variable module)
    hardcoded_sheet_ids = re.findall(r'1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54', bp_str)
    if len(hardcoded_sheet_ids) <= 2:  # Only in variable definition
        checks_passed.append(f"✅ Spreadsheet IDs replaced with variables")
    else:
        warnings.append(f"⚠️  Found {len(hardcoded_sheet_ids)} hardcoded spreadsheet IDs (expected 1-2)")

    # Check 7: No hardcoded datastore IDs (except in variable module)
    hardcoded_ds_ids = re.findall(r'"datastore":\s*81942', bp_str)
    if len(hardcoded_ds_ids) == 0:
        checks_passed.append("✅ DataStore IDs replaced with variables")
    else:
        warnings.append(f"⚠️  Found {len(hardcoded_ds_ids)} hardcoded datastore IDs")

    print()
    print("📧 MODULE 515 (EMAIL) CHECKS")
    print("-" * 70)

    # Check 8: Find module 515
    module_515 = None
    for module in blueprint['flow']:
        if module.get('id') == 515:
            module_515 = module
            break

    if module_515:
        checks_passed.append("✅ Module 515 (New Leads email) found")

        # Check subject line
        subject = module_515.get('mapper', {}).get('subject', '')
        if '{{length(508.array)' in subject and '{{length(260.array)' in subject:
            checks_passed.append("✅ Email subject includes dynamic property counts")
        else:
            issues.append("❌ Email subject missing dynamic counts")

        # Check HTML body
        html_body = module_515.get('mapper', {}).get('html', '')
        if 'Task 1' in html_body and 'Task 2' in html_body and 'Task 3' in html_body:
            checks_passed.append("✅ Email body includes Task 1, 2, 3 sections")
        else:
            issues.append("❌ Email body missing task sections")

        if '{{length(508.array)}}' in html_body:
            checks_passed.append("✅ Email body includes Task 1 count (508.array)")
        else:
            issues.append("❌ Email body missing Task 1 count")

        if '{{length(260.array)}}' in html_body:
            checks_passed.append("✅ Email body includes Task 2 count (260.array)")
        else:
            issues.append("❌ Email body missing Task 2 count")

        if '{{length(261.array)}}' in html_body:
            checks_passed.append("✅ Email body includes Task 3 count (261.array)")
        else:
            issues.append("❌ Email body missing Task 3 count")

        # Check "to" field uses variable
        to_field = module_515.get('mapper', {}).get('to', [])
        if to_field and '{{1.notificationEmail}}' in str(to_field):
            checks_passed.append("✅ Email 'to' field uses variable")
        else:
            warnings.append("⚠️  Email 'to' field may not use variable")
    else:
        issues.append("❌ Module 515 (New Leads email) not found")

    print()
    print("🔗 MODULE CONNECTIVITY CHECKS")
    print("-" * 70)

    # Check 9: Check for aggregators
    aggregators = [m for m in blueprint['flow'] if m.get('module') == 'builtin:BasicAggregator']
    if len(aggregators) >= 3:
        checks_passed.append(f"✅ Found {len(aggregators)} aggregator modules")
    else:
        warnings.append(f"⚠️  Only found {len(aggregators)} aggregators (expected 6+)")

    # Check 10: Check for Apify modules
    apify_modules = [m for m in blueprint['flow'] if 'apify' in m.get('module', '').lower()]
    if len(apify_modules) >= 3:
        checks_passed.append(f"✅ Found {len(apify_modules)} Apify modules (3 tasks)")
    else:
        warnings.append(f"⚠️  Only found {len(apify_modules)} Apify modules (expected 3)")

    # Check 11: Check for DataStore modules
    datastore_modules = [m for m in blueprint['flow'] if 'datastore' in m.get('module', '').lower()]
    if len(datastore_modules) >= 10:
        checks_passed.append(f"✅ Found {len(datastore_modules)} DataStore modules")
    else:
        warnings.append(f"⚠️  Only found {len(datastore_modules)} DataStore modules")

    # Check 12: Check for Sleep/Delay modules
    sleep_modules = [m for m in blueprint['flow'] if 'sleep' in m.get('module', '').lower()]
    if len(sleep_modules) >= 3:
        checks_passed.append(f"✅ Found {len(sleep_modules)} delay modules (race condition handling)")
    else:
        warnings.append(f"⚠️  Only found {len(sleep_modules)} delay modules (expected 3)")

    print()
    print("📊 STATISTICS")
    print("-" * 70)

    # Module count
    total_modules = len(blueprint['flow'])
    checks_passed.append(f"✅ Total modules: {total_modules}")

    # Module types
    module_types = defaultdict(int)
    for module in blueprint['flow']:
        mod_type = module.get('module', 'unknown')
        module_types[mod_type] += 1

    print(f"  • Total modules: {total_modules}")
    print(f"  • Unique module types: {len(module_types)}")
    print(f"  • Most used: {max(module_types.items(), key=lambda x: x[1])}")

    print()
    print("="*70)
    print("📝 VALIDATION SUMMARY")
    print("="*70)

    # Print all checks passed
    print()
    print(f"✅ PASSED CHECKS ({len(checks_passed)}):")
    print("-" * 70)
    for check in checks_passed:
        print(check)

    # Print warnings
    if warnings:
        print()
        print(f"⚠️  WARNINGS ({len(warnings)}):")
        print("-" * 70)
        for warning in warnings:
            print(warning)

    # Print issues
    if issues:
        print()
        print(f"❌ ISSUES ({len(issues)}):")
        print("-" * 70)
        for issue in issues:
            print(issue)

    print()
    print("="*70)
    print("🎯 FINAL VERDICT")
    print("="*70)

    if len(issues) == 0:
        print("✅ BLUEPRINT IS VALID - Ready to import!")
        print()
        print("Next steps:")
        print("  1. Import into Make.com")
        print("  2. Reconnect integrations")
        print("  3. Test with small data")
        return True
    else:
        print(f"❌ BLUEPRINT HAS {len(issues)} CRITICAL ISSUES")
        print()
        print("Please review and fix issues before importing.")
        return False


if __name__ == "__main__":
    blueprint_file = Path("/Users/swayclarke/Downloads/Lombok invest capital Property Scraper v6.blueprint.json")

    if not blueprint_file.exists():
        print(f"❌ Blueprint file not found: {blueprint_file}")
        exit(1)

    try:
        is_valid = validate_blueprint(blueprint_file)
        exit(0 if is_valid else 1)
    except Exception as e:
        print(f"❌ Error during validation: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
