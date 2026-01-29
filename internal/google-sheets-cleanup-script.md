# Google Sheets Duplicate Cleanup Script

## Spreadsheet Details
- **Sheet ID**: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
- **Tab**: Transactions
- **Problem**: Same transaction appearing 3-4 times (duplicates from multiple PDF processing runs)

## Examples of Duplicates
- €1,572.94 Lastschrift appears 3x
- €5,000 Sway Clarke appears 3x
- Multiple other transactions duplicated

## Cleanup Strategy

### Option 1: Manual Cleanup in Google Sheets UI
1. Open spreadsheet: https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM/edit
2. Go to Transactions tab
3. Use Data > Remove duplicates feature
4. Select all columns
5. Keep first occurrence, remove rest

### Option 2: Python Script Using Google Sheets API
```python
#!/usr/bin/env python3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from collections import defaultdict

# Setup credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Open spreadsheet
spreadsheet_id = '1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM'
sheet = client.open_by_key(spreadsheet_id).worksheet('Transactions')

# Get all records
all_records = sheet.get_all_records()

# Find duplicates using unique key: Date_Bank_Amount_Description
seen = {}
duplicates_to_delete = []

for idx, row in enumerate(all_records, start=2):  # Start at 2 (row 1 is header)
    key = f"{row['Date']}_{row['Bank']}_{row['Amount']}_{row['Description']}"

    if key in seen:
        # This is a duplicate - mark for deletion
        duplicates_to_delete.append(idx)
        print(f"Duplicate found at row {idx}: {row['Date']} | {row['Vendor']} | €{row['Amount']}")
    else:
        seen[key] = idx

# Delete duplicates (in reverse order to maintain row indices)
print(f"\\nDeleting {len(duplicates_to_delete)} duplicate rows...")
for row_num in sorted(duplicates_to_delete, reverse=True):
    sheet.delete_rows(row_num)
    print(f"Deleted row {row_num}")

print(f"\\nCleanup complete! Removed {len(duplicates_to_delete)} duplicates.")
```

### Option 3: n8n Workflow for One-Time Cleanup
Create a simple workflow:
1. Read Transactions sheet (all rows)
2. Code node: Group by Date_Bank_Amount_Description
3. For each group with count > 1:
   - Keep first occurrence
   - Delete remaining rows using Google Sheets "Delete Row" operation

### Option 4: Clear All and Re-import (Nuclear Option)
**⚠️ ONLY if you have backups of the PDFs**

1. Export Transactions tab as CSV backup
2. Clear all rows in Transactions tab (except header)
3. Place all bank statement PDFs back in Bank-Statements folder
4. Re-run W1 workflow (with new deduplication logic)
5. All transactions will be re-imported without duplicates

## Recommended Approach

**Use Option 1 (Manual UI cleanup)** for now since:
- Fast and safe
- Google Sheets has built-in deduplication
- No risk of accidentally deleting unique transactions
- Visual confirmation of what's being removed

After cleanup:
- W1 deduplication logic will prevent future duplicates
- W0 filter fix will stop flagging income as missing receipts

## Verification After Cleanup

Run this query to check for remaining duplicates:
```sql
SELECT Date, Bank, Amount, Description, COUNT(*) as occurrences
FROM Transactions
GROUP BY Date, Bank, Amount, Description
HAVING COUNT(*) > 1
```

Expected result: **0 rows** (no duplicates remaining)
