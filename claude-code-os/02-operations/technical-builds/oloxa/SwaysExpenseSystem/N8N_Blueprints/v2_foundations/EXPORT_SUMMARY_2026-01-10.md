# Expense System Workflow Export Summary
**Export Date**: 2026-01-10
**Purpose**: Backup all active expense system workflows before deployment

---

## Exported Workflows

### W2: Gmail Receipt Monitor v2.1
- **Workflow ID**: `dHbwemg7hEB4vDmC`
- **Status**: ✅ Active
- **Last Updated**: 2026-01-10T12:14:28.996Z
- **File**: `workflow2_gmail_receipt_monitor_v2.1_2026-01-10.json`
- **Size**: ~83 KB
- **Nodes**: 24
- **Key Features**:
  - Dual Gmail account monitoring (sway@oloxa.ai + swayfromthehook@gmail.com)
  - Apple email HTML-to-PDF conversion
  - OCR with Google Vision API
  - Duplicate detection via MD5 hash
  - Automatic vendor classification

### W3: Transaction-Receipt-Invoice Matching v2.1
- **Workflow ID**: `CJtdqMreZ17esJAW`
- **Status**: ⏸️ Inactive (Manual trigger)
- **Last Updated**: 2026-01-10T12:14:33.586Z
- **File**: Exported from n8n (39 KB on disk - v2.1 from Jan 9)
- **Size**: ~39 KB
- **Nodes**: 29
- **Key Features**:
  - Expense transaction matching (receipts)
  - Income transaction matching (invoices from Drive)
  - Missing items report generation
  - Confidence-based matching

### W4: Monthly Folder Builder v2.1
- **Workflow ID**: `nASL6hxNQGrNBTV4`
- **Status**: ✅ Active (Webhook trigger)
- **Last Updated**: 2026-01-10T12:14:39.834Z
- **File**: Exported from n8n (39 KB on disk from Jan 9)
- **Size**: ~39 KB
- **Nodes**: 23
- **Key Features**:
  - VAT folder structure creation (Month YYYY)
  - 4 bank folders (ING Diba, Deutsche Bank, Barclays, Mastercard)
  - Statements/Receipts subfolders
  - Automated file organization from database
  - Income folder creation

### W6: Expensify PDF Parser v1.1
- **Workflow ID**: `l5fcp4Qnjn4Hzc8w`
- **Status**: ✅ Active (Google Drive trigger)
- **Last Updated**: 2026-01-10T12:14:44.841Z
- **File**: Exported from n8n (20 KB on disk from Jan 9)
- **Size**: ~20 KB
- **Nodes**: 14
- **Key Features**:
  - Anthropic Claude Vision API for PDF parsing
  - Transaction table extraction (pages 1-2)
  - Receipt metadata extraction (pages 3+)
  - ExpensifyNumber matching
  - Merge node race condition fix (v1.1)

---

## Archived Files

The following old v2.0 versions were moved to `.archive/`:
- `workflow2_gmail_receipt_monitor_v2.0_2026-01-09.json` (24 KB)
- `workflow3_transaction_receipt_matching_v2.0_2026-01-09.json` (16 KB)
- `workflow4_monthly_folder_builder_v2.0_2026-01-09.json` (14 KB)

**Note**: W3 v2.1 and W6 v1.1 already existed from Jan 9 deployment. W2 and W4 received v2.1 updates on Jan 10.

---

## Version Comparison

| Workflow | Old Version | New Version | Changes |
|----------|-------------|-------------|---------|
| W2 | v2.0 (Jan 9) | v2.1 (Jan 10) | Active deployment, latest fixes |
| W3 | v2.0 (Jan 9) | v2.1 (Jan 9) | No change (already v2.1) |
| W4 | v2.0 (Jan 9) | v2.1 (Jan 10) | Active deployment, latest fixes |
| W6 | v1.0 (initial) | v1.1 (Jan 9) | No change (already v1.1) |

---

## Notes

- **W1 (PDF Intake)**: Not included - this workflow was retired/replaced by W2 Gmail monitoring
- **Storage**: Workflows are stored both in n8n (live) and as JSON backups in this directory
- **Credentials**: All credential IDs are preserved in exports but credentials themselves are NOT exported (security)
- **Next Step**: Ready for test-runner-agent validation

---

## File Sizes Summary

```
Current v2_foundations folder:
- workflow1_pdf_intake_and_parsing_v2.0_2026-01-09.json: 19 KB (legacy)
- workflow2_gmail_receipt_monitor_v2.1_2026-01-10.json: 83 KB ✅ NEW
- workflow3_transaction_receipt_matching_v2.1_2026-01-09.json: 39 KB (existing)
- workflow4_monthly_folder_builder_v2.0_2026-01-09.json: 14 KB (archived)
- workflow6_expensify_pdf_parser_v1.1_2026-01-09.json: 20 KB (existing)

Archive folder (.archive/):
- workflow2_gmail_receipt_monitor_v2.0_2026-01-09.json: 24 KB
- workflow3_transaction_receipt_matching_v2.0_2026-01-09.json: 16 KB
- workflow4_monthly_folder_builder_v2.0_2026-01-09.json: 14 KB
```

**Total Backup Size**: ~215 KB (all workflows)
