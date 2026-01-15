#!/usr/bin/env python3
"""
n8n Workflow Export Validator

Validates exported n8n workflow JSON to catch common issues before import.

Usage:
    python3 validate_n8n_export.py workflow.json
"""

import json
import sys


# Node types that require specific parameters
REQUIRED_PARAMETERS = {
    'n8n-nodes-base.googleSheets': {
        'required': ['operation'],
        'conditional': {
            'read': ['range'],
            'append': ['range'],
            'update': ['range']
        }
    },
    'n8n-nodes-base.googleDrive': {
        'required': ['operation']
    },
    'n8n-nodes-base.gmail': {
        'required': ['operation']
    },
    'n8n-nodes-base.openAi': {
        'required': ['operation', 'resource']
    },
    'n8n-nodes-base.httpRequest': {
        'required': ['method']
    }
}


def validate_workflow(filepath):
    """Validate n8n workflow JSON for common import issues."""

    errors = []
    warnings = []

    # Step 1: Load and validate JSON syntax
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"❌ Invalid JSON syntax: {e}"], []
    except FileNotFoundError:
        return [f"❌ File not found: {filepath}"], []

    # Step 2: Check required top-level fields
    required_fields = ['name', 'nodes', 'connections']
    for field in required_fields:
        if field not in data:
            errors.append(f"❌ Missing required field: {field}")

    if errors:
        return errors, warnings

    # Step 3: Validate nodes
    nodes = data['nodes']
    print(f"✅ Found {len(nodes)} nodes")

    # Step 4: Check for missing required parameters
    for node in nodes:
        node_type = node.get('type')
        node_name = node.get('name', 'Unknown')
        params = node.get('parameters', {})

        if node_type in REQUIRED_PARAMETERS:
            # Check required parameters
            required = REQUIRED_PARAMETERS[node_type]['required']
            for param in required:
                if param not in params:
                    errors.append(
                        f"❌ Node '{node_name}' ({node_type}) missing required parameter: {param}"
                    )

            # Check conditional parameters
            if 'conditional' in REQUIRED_PARAMETERS[node_type]:
                operation = params.get('operation')
                if operation in REQUIRED_PARAMETERS[node_type]['conditional']:
                    for param in REQUIRED_PARAMETERS[node_type]['conditional'][operation]:
                        if param not in params:
                            warnings.append(
                                f"⚠️  Node '{node_name}' with operation '{operation}' missing parameter: {param}"
                            )

    # Step 5: Check for resource locator issues
    for node in nodes:
        params = node.get('parameters', {})
        node_name = node.get('name', 'Unknown')

        for param_name, param_value in params.items():
            if isinstance(param_value, dict) and param_value.get('__rl'):
                # Check resource locator structure
                if 'mode' not in param_value:
                    warnings.append(
                        f"⚠️  Node '{node_name}' parameter '{param_name}' has __rl but missing 'mode'"
                    )
                if 'value' not in param_value:
                    warnings.append(
                        f"⚠️  Node '{node_name}' parameter '{param_name}' has __rl but missing 'value'"
                    )

    # Step 6: Check connections
    connections = data.get('connections', {})
    print(f"✅ Found {len(connections)} connection sources")

    # Count total connections
    total_connections = sum(
        len(outputs.get('main', [[]])[0])
        for outputs in connections.values()
    )
    print(f"✅ Total connections: {total_connections}")

    return errors, warnings


def auto_fix_workflow(filepath, output_filepath):
    """Automatically fix common issues in workflow JSON."""

    with open(filepath, 'r') as f:
        data = json.load(f)

    fixes_applied = []

    for node in data['nodes']:
        node_type = node.get('type')
        node_name = node.get('name', 'Unknown')
        params = node.get('parameters', {})

        # Fix missing operation parameters
        if node_type in REQUIRED_PARAMETERS:
            required = REQUIRED_PARAMETERS[node_type]['required']

            # Google Sheets: default to 'read' operation
            if node_type == 'n8n-nodes-base.googleSheets':
                if 'operation' not in params:
                    params['operation'] = 'read'
                    fixes_applied.append(f"✅ Added operation='read' to '{node_name}'")
                if 'range' not in params and params.get('operation') == 'read':
                    params['range'] = 'A:Z'
                    fixes_applied.append(f"✅ Added range='A:Z' to '{node_name}'")

            # OpenAI: default to 'message' operation
            if node_type == 'n8n-nodes-base.openAi':
                if 'operation' not in params:
                    params['operation'] = 'message'
                    fixes_applied.append(f"✅ Added operation='message' to '{node_name}'")
                if 'resource' not in params:
                    params['resource'] = 'text'
                    fixes_applied.append(f"✅ Added resource='text' to '{node_name}'")

            # Gmail: default to 'send' operation
            if node_type == 'n8n-nodes-base.gmail':
                if 'operation' not in params:
                    params['operation'] = 'send'
                    fixes_applied.append(f"✅ Added operation='send' to '{node_name}'")

            # Google Drive: default to 'upload' operation
            if node_type == 'n8n-nodes-base.googleDrive':
                if 'operation' not in params:
                    params['operation'] = 'upload'
                    fixes_applied.append(f"⚠️  Added operation='upload' to '{node_name}' (VERIFY THIS)")

    # Write fixed JSON
    with open(output_filepath, 'w') as f:
        json.dump(data, f, indent=2)

    return fixes_applied


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 validate_n8n_export.py <workflow.json> [--fix]")
        sys.exit(1)

    filepath = sys.argv[1]
    auto_fix = '--fix' in sys.argv

    print(f"\n🔍 Validating: {filepath}\n")

    errors, warnings = validate_workflow(filepath)

    # Print results
    if errors:
        print("\n❌ ERRORS FOUND:\n")
        for error in errors:
            print(f"  {error}")

    if warnings:
        print("\n⚠️  WARNINGS:\n")
        for warning in warnings:
            print(f"  {warning}")

    if not errors and not warnings:
        print("\n✅ No issues found! Workflow should import successfully.\n")
        sys.exit(0)

    # Offer auto-fix
    if auto_fix and errors:
        output_file = filepath.replace('.json', '_FIXED.json')
        print(f"\n🔧 Attempting auto-fix...\n")

        fixes = auto_fix_workflow(filepath, output_file)

        if fixes:
            print("Fixes applied:")
            for fix in fixes:
                print(f"  {fix}")
            print(f"\n✅ Fixed version saved to: {output_file}")
            print("\n🔍 Re-validating fixed version...\n")

            errors2, warnings2 = validate_workflow(output_file)

            if not errors2:
                print("\n✅ Fixed version passes validation!\n")
                sys.exit(0)
            else:
                print("\n⚠️  Some errors remain after auto-fix:")
                for error in errors2:
                    print(f"  {error}")
                sys.exit(1)
        else:
            print("\n⚠️  No auto-fixes available for these errors.\n")
            sys.exit(1)

    if errors:
        print("\n💡 Run with --fix to attempt automatic fixes:\n")
        print(f"   python3 {sys.argv[0]} {filepath} --fix\n")
        sys.exit(1)
    else:
        print("\n💡 Warnings are non-critical but should be reviewed.\n")
        sys.exit(0)
