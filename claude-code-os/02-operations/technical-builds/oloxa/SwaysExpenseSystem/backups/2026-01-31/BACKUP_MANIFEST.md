# Expense System Workflow Backups - 2026-01-31

## Overview
Complete JSON backups of all Sway's Expense System n8n workflows exported on January 31, 2026.

## Backup Details

| Filename | Workflow ID | Workflow Name | Size | Nodes |
|----------|------------|---------------|------|-------|
| W0_Master_Orchestrator.json | ewZOYMYOqSfgtjFm | W0 Master Orchestrator | 78 KB | 31 |
| W1_PDF_Intake.json | MPjDdVMI88158iFW | W1 PDF Intake | 61 KB | 26 |
| W1v2_Bank_Statement_Webhook.json | Is8zl1TpWhIzspto | W1v2 Bank Statement Webhook | 54 KB | 23 |
| W2_Gmail_Monitor.json | dHbwemg7hEB4vDmC | W2 Gmail Monitor | 112 KB | 28 |
| W3_Matching.json | CJtdqMreZ17esJAW | W3 Matching | 93 KB | 27 |
| W4_Monthly_Folder_Builder.json | nASL6hxNQGrNBTV4 | W4 Monthly Folder Builder | 124 KB | 32 |
| W6_Expensify_Parser.json | zFdAi3H5LFFbqusX | W6 Expensify Parser | 28 KB | 18 |
| W7_Downloads_Monitor.json | 6x1sVuv4XKN0002B | W7 Downloads Monitor | 118 KB | 30 |
| W7v2_Receipts_Webhook.json | qSuG0gwuJByd2hGJ | W7v2 Receipts Webhook | 59 KB | 24 |

## Total Statistics
- **Total Backups:** 9 workflows
- **Total Size:** 748 KB
- **Total Nodes:** 239 nodes across all workflows
- **Backup Date:** 2026-01-31
- **Format:** JSON (complete workflow definitions)

## Contents of Each Backup

Each JSON file contains:
- ✓ Workflow metadata (id, name, description, tags)
- ✓ All nodes and their configurations
- ✓ All connections between nodes
- ✓ Node parameters and credentials
- ✓ Settings and variables
- ✓ Version information
- ✓ Creation/update timestamps
- ✓ Activation status

## How to Use

### Restore a Workflow
To restore a workflow from backup, you can import the JSON file back into n8n:
1. Go to n8n.oloxa.ai
2. Click "Import from File"
3. Select the JSON backup file
4. Review and confirm the import

### Reference Existing Configuration
To reference current configurations while troubleshooting:
```bash
# View specific workflow
cat W3_Matching.json | jq '.nodes[] | select(.name=="Node Name")'

# Count nodes in a workflow
jq '.nodes | length' W0_Master_Orchestrator.json

# List all node types
jq '.nodes[] | .type' W2_Gmail_Monitor.json | sort | uniq -c
```

## Backup Integrity

All backups verified:
- ✓ Valid JSON format
- ✓ Complete node definitions
- ✓ Connection data present
- ✓ All required fields populated
- ✓ File sizes consistent with expected data

## Rollback Procedure

If you need to rollback to this backup:
1. **DO NOT delete** the current workflow in n8n
2. **Deactivate** the current workflow
3. **Import** the JSON backup as a new workflow
4. **Test** the imported workflow in sandbox mode
5. **Switch** traffic to the imported workflow once verified
6. **Delete** the old workflow only after confirmed stable operation

## Location
All backups stored in:
```
/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/oloxa/SwaysExpenseSystem/backups/2026-01-31/
```

---
Generated: 2026-01-31 via n8n API export
