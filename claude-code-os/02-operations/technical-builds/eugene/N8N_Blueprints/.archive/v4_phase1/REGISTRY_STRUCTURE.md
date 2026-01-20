# Master Client Registry - Google Sheet Structure

## Location
Create in: https://drive.google.com/drive/folders/1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm

## Sheet Name
`V4_Master_Client_Registry`

## Column Structure

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| client_name_raw | Text | Original client name from document | "Lombok Capital" |
| client_normalized | Text | Normalized name for folder creation | "lombok_capital" |
| root_folder_id | Text | Google Drive ID of client root folder | "1abc123..." |
| subfolder_ids_json | JSON | All 47 subfolder IDs as JSON object | {"FOLDER_01": "1def..."} |
| created_date | Date | When folders were created | "2025-12-29" |
| status | Select | Current status | "ACTIVE" / "PENDING" / "ARCHIVED" |

## Initial Data (Example Row)

```
Lombok Capital | lombok_capital | [TO BE FILLED] | {} | 2025-12-29 | PENDING
```

## Status Values
- **PENDING**: Client identified but folders not yet created
- **ACTIVE**: Folders created and operational
- **ARCHIVED**: Client no longer active

## Usage in n8n

**Lookup by normalized name:**
```javascript
// In Google Sheets node
Filter: client_normalized = lombok_capital
Returns: Full row with folder IDs
```

**Add new client:**
```javascript
// In Google Sheets node (Append Row)
Values: [rawName, normalizedName, rootFolderId, JSON.stringify(subfolderIds), today, "ACTIVE"]
```

## Notes
- Store spreadsheet ID in n8n credentials as `CLIENT_REGISTRY_SHEET_ID`
- Keep subfolder_ids_json as stringified JSON for easy parsing in n8n
- Use status field to filter out archived clients
