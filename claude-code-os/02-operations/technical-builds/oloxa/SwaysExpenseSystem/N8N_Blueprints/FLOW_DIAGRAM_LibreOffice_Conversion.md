# Pre-Chunk 0 Workflow - LibreOffice Conversion Flow

## Visual Flow Diagram

```
┌─────────────────────────────────┐
│ Gmail Trigger                   │
│ (Unread with Attachments)       │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ Extract Email Metadata          │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ Filter PDF/ZIP Attachments      │
│ ✨ NOW FILTERS:                 │
│   • PDF                         │
│   • ZIP                         │
│   • XLS/XLSX/XLSM              │
│   • DOC/DOCX                   │
│ ✨ ADDS: needsConversion flag  │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│ Split Into Batches              │
│ (Process Each PDF)              │
└────┬────────────────────────┬───┘
     │                        │
     │ Output 0 (Done)        │ Output 1 (Loop)
     │                        │
     ▼                        ▼
┌──────────────┐    ┌─────────────────────────────────┐
│ Aggregate    │    │ ✨ NEW: Check If Needs        │
│ All Results  │    │        Conversion               │
│              │    │ IF: needsConversion === true    │
└──────────────┘    └────┬─────────────────────┬──────┘
                         │                     │
                  TRUE   │                     │ FALSE
                         │                     │
                         ▼                     ▼
           ┌─────────────────────────┐  ┌─────────────────┐
           │ ✨ NEW: Convert to PDF  │  │ Upload PDF to   │
           │    with LibreOffice     │  │ Temp Folder     │
           │                         │  │                 │
           │ 1. Write to /tmp/       │  │ (Skip           │
           │ 2. Run soffice          │  │  conversion)    │
           │ 3. Read PDF result      │  │                 │
           │ 4. Cleanup temp files   │  │                 │
           └────────────┬────────────┘  └────────┬────────┘
                        │                        │
                        └────────────┬───────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │ Upload PDF to           │
                        │ Temp Folder             │
                        │                         │
                        │ (Both paths merge here) │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │ Extract File ID &       │
                        │ Metadata                │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │ Download PDF from Drive │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        [Rest of workflow continues...]
```

## Data Flow Examples

### Example 1: Excel File (Requires Conversion)

**Input:**
```json
{
  "emailId": "msg123",
  "filename": "expense-report.xlsx",
  "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  "originalExtension": "xlsx",
  "needsConversion": true
}
```

**After IF Node (TRUE path):**
```json
{
  "emailId": "msg123",
  "filename": "expense-report.pdf",
  "originalFilename": "expense-report.xlsx",
  "mimeType": "application/pdf",
  "originalExtension": "xlsx",
  "needsConversion": true,
  "wasConverted": true
}
```

### Example 2: PDF File (No Conversion)

**Input:**
```json
{
  "emailId": "msg456",
  "filename": "invoice.pdf",
  "mimeType": "application/pdf",
  "originalExtension": "pdf",
  "needsConversion": false
}
```

**After IF Node (FALSE path):**
```json
{
  "emailId": "msg456",
  "filename": "invoice.pdf",
  "mimeType": "application/pdf",
  "originalExtension": "pdf",
  "needsConversion": false
}
```

## Conversion Logic

### Supported File Types Matrix

| File Type | Extension | Needs Conversion | Handler |
|-----------|-----------|------------------|---------|
| PDF       | .pdf      | ❌ No            | Direct upload |
| ZIP       | .zip      | ❌ No            | Direct upload |
| Excel 2007+ | .xlsx   | ✅ Yes           | LibreOffice |
| Excel 2007+ Macro | .xlsm | ✅ Yes       | LibreOffice |
| Excel 97-2003 | .xls  | ✅ Yes           | LibreOffice |
| Word 2007+ | .docx    | ✅ Yes           | LibreOffice |
| Word 97-2003 | .doc   | ✅ Yes           | LibreOffice |

### LibreOffice Command

```bash
soffice --headless --convert-to pdf --outdir /tmp /tmp/{tempfile}.xlsx
```

**Result:** Creates `/tmp/{tempfile}.pdf`

## Node IDs & Types

| Node Name | Node ID | Type | Version |
|-----------|---------|------|---------|
| Filter PDF/ZIP Attachments | filter-attachments-001 | Code | 2 |
| Check If Needs Conversion | if-needs-conversion-001 | IF | 2.3 |
| Convert to PDF with LibreOffice | code-convert-to-pdf-001 | Code | 2 |
| Upload PDF to Temp Folder | upload-pdf-gdrive-001 | Google Drive | - |

## Connection Summary

**Before changes:**
- Split Batches (output 1) → Upload PDF (1 connection)

**After changes:**
- Split Batches (output 1) → Check If Needs Conversion (1 connection)
- Check If Needs Conversion (output 0 TRUE) → Convert to PDF (1 connection)
- Check If Needs Conversion (output 1 FALSE) → Upload PDF (1 connection)
- Convert to PDF → Upload PDF (1 connection)

**Total connections modified:** 4 operations (1 removed, 3 added)

---

✨ **Key Feature:** Transparent conversion - rest of workflow sees only PDFs
🔄 **Backward Compatible:** Existing PDF files skip conversion entirely
⚡ **Efficient:** Only converts when necessary based on file extension
