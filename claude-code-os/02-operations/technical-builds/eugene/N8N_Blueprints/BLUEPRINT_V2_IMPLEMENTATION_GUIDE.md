> ⚠️ **REFERENCE ONLY - Superseded by V4**
>
> This guide documents V2 setup process (superseded).
> For V4 implementation, see: `v4_phase1/WORKFLOW_V4_SUMMARY.md`
> Kept as reference for setup patterns only.

---

# N8N Blueprint V2 Implementation Guide

**Document Organizer v2.0 - German Bauträger Edition**
**Date:** 2024-12-20
**Purpose:** Complete implementation guide for the n8n workflow blueprint with all 36 document types

---

## Overview

This guide provides complete implementation details for the Document Organizer v2.0 workflow, including:
- **35 document types** from the official German Bauträger checklist
- **1 custom document type**: Exit Strategy (exitstrategie)
- **Total: 36 document types** organized into 4 main categories

---

## Complete Document Type Mapping

### Category 1: OBJEKTUNTERLAGEN (Property Documents) - 22 Types

| # | Type ID | German Name | File Prefix | Folder Name | Folder ID Variable |
|---|---------|-------------|-------------|-------------|-------------------|
| 1 | projektbeschreibung | Projektbeschreibung / Exposé | EXPOSE | 01_Projektbeschreibung | $vars.folder_01_projektbeschreibung |
| 2 | kaufvertrag | Kaufvertrag | KAUF | 02_Kaufvertrag | $vars.folder_02_kaufvertrag |
| 3 | grundbuchauszug | Grundbuchauszug < 3 Monate | GRUNDBUCH | 03_Grundbuchauszug | $vars.folder_03_grundbuchauszug |
| 4 | eintragungsbewilligungen | Eintragungsbewilligungen | EINTRAG | 04_Eintragungsbewilligungen | $vars.folder_04_eintragungsbewilligungen |
| 5 | bodenrichtwert | Bodenrichtwert | BODEN | 05_Bodenrichtwert | $vars.folder_05_bodenrichtwert |
| 6 | baulastenverzeichnis | Baulastenverzeichnis | BAULASTEN | 06_Baulastenverzeichnis | $vars.folder_06_baulastenverzeichnis |
| 7 | altlastenkataster | Altlastenkataster | ALTLASTEN | 07_Altlastenkataster | $vars.folder_07_altlastenkataster |
| 8 | baugrundgutachten | Baugrundgutachten | BAUGUTACHT | 08_Baugrundgutachten | $vars.folder_08_baugrundgutachten |
| 9 | lageplan | Lageplan / Flurkarte | LAGEPLAN | 09_Lageplan_Flurkarte | $vars.folder_09_lageplan |
| 10 | bautraegerkalkulation | Bauträgerkalkulation DIN 276 | KALK276 | 10_Bautraegerkalkulation_DIN276 | $vars.folder_10_bautraegerkalkulation |
| 11 | verkaufspreise | Verkaufspreise je Einheit | PREISE | 11_Verkaufspreise | $vars.folder_11_verkaufspreise |
| 12 | bauzeitenplan | Bauzeitenplan / Liquiditätsplan | BAUZEIT | 12_Bauzeitenplan_Liquiditaet | $vars.folder_12_bauzeitenplan |
| 13 | vertriebsweg | Vertriebsweg | VERTRIEB | 13_Vertriebsweg | $vars.folder_13_vertriebsweg |
| 14 | bauausstattung | Bau-/Ausstattungsbeschreibung | BAUAUSST | 14_Bau_Ausstattungsbeschreibung | $vars.folder_14_bauausstattung |
| 15 | flaechenberechnung | Flächenberechnung DIN 277 | FLAECHE277 | 15_Flaechenberechnung_DIN277 | $vars.folder_15_flaechenberechnung |
| 16 | werkvertraege | GU-/Werkverträge | WERKVERT | 16_GU_Werkvertraege | $vars.folder_16_werkvertraege |
| 17 | bauzeichnungen | Bauzeichnungen/Grundrisse | BAUZEICH | 17_Bauzeichnungen | $vars.folder_17_bauzeichnungen |
| 18 | baugenehmigung | Baugenehmigung | BAUGEN | 18_Baugenehmigung | $vars.folder_18_baugenehmigung |
| 19 | teilungserklaerung | Teilungserklärung | TEILUNG | 19_Teilungserklaerung | $vars.folder_19_teilungserklaerung |
| 20 | versicherungen | Versicherungen | VERSICH | 20_Versicherungen | $vars.folder_20_versicherungen |
| 21 | verkaufsvertrag | Muster Verkaufsvertrag | MUSTERVERT | 21_Muster_Verkaufsvertrag | $vars.folder_21_verkaufsvertrag |
| 22 | gutachterauftrag | Gutachterauftrag | GUTACHT | 22_Gutachterauftrag | $vars.folder_22_gutachterauftrag |

### Category 2: WIRTSCHAFTLICHE UNTERLAGEN (Economic/Financial) - 8 Types

| # | Type ID | German Name | File Prefix | Folder Name | Folder ID Variable |
|---|---------|-------------|-------------|-------------|-------------------|
| 23 | jahresabschluesse | Jahresabschlüsse | JAHRAB | 23_Jahresabschluesse | $vars.folder_23_jahresabschluesse |
| 24 | bwa | BWA inkl. Summe-Saldenliste | BWA | 24_BWA | $vars.folder_24_bwa |
| 25 | steuernummern | Steuernummern / Steuer-IDs | STEUER | 25_Steuernummern | $vars.folder_25_steuernummern |
| 26 | schufa | SCHUFA-Erklärung | SCHUFA | 26_SCHUFA_Erklaerung | $vars.folder_26_schufa |
| 27 | einkommensteuern | Einkommensteuerunterlagen | EINKST | 27_Einkommensteuern | $vars.folder_27_einkommensteuern |
| 28 | vermoegensuebersicht | Vermögens-/Schuldenübersicht | VERMOEGEN | 28_Vermoegensuebersicht | $vars.folder_28_vermoegensuebersicht |
| 29 | eigenkapitalnachweis | Eigenkapitalnachweis | EIGEN | 29_Eigenkapitalnachweis | $vars.folder_29_eigenkapitalnachweis |
| 30 | projektliste | Projektliste | PROJLIST | 30_Projektliste | $vars.folder_30_projektliste |

### Category 3: RECHTLICHE UNTERLAGEN (Legal Documents) - 5 Types

| # | Type ID | German Name | File Prefix | Folder Name | Folder ID Variable |
|---|---------|-------------|-------------|-------------|-------------------|
| 31 | hr_auszug | HR-Auszug | HR | 31_HR_Auszug | $vars.folder_31_hr_auszug |
| 32 | gesellschaftsvertrag | Gesellschaftsvertrag | GESELL | 32_Gesellschaftsvertrag | $vars.folder_32_gesellschaftsvertrag |
| 33 | personalausweise | Personalausweise | PERSAUS | 33_Personalausweise | $vars.folder_33_personalausweise |
| 34 | bautraegerzulassung | Bauträgerzulassung §34c | ZULASSUNG | 34_Bautraegerzulassung | $vars.folder_34_bautraegerzulassung |
| 35 | organigramm | Organigramm | ORGAN | 35_Organigramm | $vars.folder_35_organigramm |

### Category 4: SONSTIGES (Other/Custom Documents) - 2 Types

| # | Type ID | German Name | File Prefix | Folder Name | Folder ID Variable |
|---|---------|-------------|-------------|-------------|-------------------|
| 36 | exitstrategie | Exit-Strategie | EXIT | 36_Exit_Strategie | $vars.folder_36_exitstrategie |
| 37 | sonstiges | Sonstige Dokumente | MISC | 37_Sonstiges | $vars.folder_37_sonstiges |

**Total: 37 document types (36 + 1 fallback for unclassified)**

---

## Google Drive Folder Structure

```
clients/
└── {Client_Name}/                          # e.g., "Eugene_Bautraeger_2024"
    │
    ├── 00_Upload_Staging/                  # Temporary upload folder
    │
    ├── OBJEKTUNTERLAGEN/
    │   ├── 01_Projektbeschreibung/
    │   ├── 02_Kaufvertrag/
    │   ├── 03_Grundbuchauszug/
    │   ├── 04_Eintragungsbewilligungen/
    │   ├── 05_Bodenrichtwert/
    │   ├── 06_Baulastenverzeichnis/
    │   ├── 07_Altlastenkataster/
    │   ├── 08_Baugrundgutachten/
    │   ├── 09_Lageplan_Flurkarte/
    │   ├── 10_Bautraegerkalkulation_DIN276/
    │   ├── 11_Verkaufspreise/
    │   ├── 12_Bauzeitenplan_Liquiditaet/
    │   ├── 13_Vertriebsweg/
    │   ├── 14_Bau_Ausstattungsbeschreibung/
    │   ├── 15_Flaechenberechnung_DIN277/
    │   ├── 16_GU_Werkvertraege/
    │   ├── 17_Bauzeichnungen/
    │   ├── 18_Baugenehmigung/
    │   ├── 19_Teilungserklaerung/
    │   ├── 20_Versicherungen/
    │   ├── 21_Muster_Verkaufsvertrag/
    │   └── 22_Gutachterauftrag/
    │
    ├── WIRTSCHAFTLICHE_UNTERLAGEN/
    │   ├── 23_Jahresabschluesse/
    │   ├── 24_BWA/
    │   ├── 25_Steuernummern/
    │   ├── 26_SCHUFA_Erklaerung/
    │   ├── 27_Einkommensteuern/
    │   ├── 28_Vermoegensuebersicht/
    │   ├── 29_Eigenkapitalnachweis/
    │   └── 30_Projektliste/
    │
    ├── RECHTLICHE_UNTERLAGEN/
    │   ├── 31_HR_Auszug/
    │   ├── 32_Gesellschaftsvertrag/
    │   ├── 33_Personalausweise/
    │   ├── 34_Bautraegerzulassung/
    │   └── 35_Organigramm/
    │
    └── SONSTIGES/
        ├── 36_Exit_Strategie/
        └── 37_Sonstiges/
```

---

## Blueprint Architecture

### Current Implementation Status

The blueprint JSON file (`document_organizer_blueprint_v2.json`) includes:

✅ **Completed Nodes:**
1. Gmail Trigger
2. Download Email Attachments
3. Filter File Types
4. Upload to Google Drive Staging
5. File Type Detection
6. OCR Switch
7. Extract Text (Digital PDF)
8. OCR Service (AWS Textract German)
9. Merge Text Results
10. AI Classification Level 1 (Category)
11. Category Switch (4-way)
12. AI Level 2 - Objektunterlagen (22 types)
13. AI Level 2 - Wirtschaftliche (8 types)
14. AI Level 2 - Rechtliche (5 types)
15. AI Level 2 - Sonstiges (2 types: exitstrategie, sonstiges)

⚠️ **Missing Nodes (Need to Add):**
16. Type Switch (37-way routing)
17. Set Filename Nodes (37 nodes)
18. Move File Node
19. Log to Google Sheets
20. Email Confirmation (Optional)

---

## Implementation Instructions

### Step 1: Create All Required Variables

In n8n, create these workflow variables (Settings → Variables):

```javascript
// Client Configuration
clientName: "Eugene_Bautraeger"
gmailCredentials: "gmail-oauth-id"
googleDriveCredentials: "gdrive-oauth-id"
openaiApiKey: "sk-..."
awsCredentials: "aws-access-key"
awsRegion: "us-east-1"

// Upload Staging Folder
uploadFolderId: "google-drive-upload-folder-id"

// Log Sheet
logSheetId: "google-sheets-log-spreadsheet-id"

// All 37 Folder IDs (OBJEKTUNTERLAGEN)
folder_01_projektbeschreibung: "gdrive-folder-id"
folder_02_kaufvertrag: "gdrive-folder-id"
folder_03_grundbuchauszug: "gdrive-folder-id"
folder_04_eintragungsbewilligungen: "gdrive-folder-id"
folder_05_bodenrichtwert: "gdrive-folder-id"
folder_06_baulastenverzeichnis: "gdrive-folder-id"
folder_07_altlastenkataster: "gdrive-folder-id"
folder_08_baugrundgutachten: "gdrive-folder-id"
folder_09_lageplan: "gdrive-folder-id"
folder_10_bautraegerkalkulation: "gdrive-folder-id"
folder_11_verkaufspreise: "gdrive-folder-id"
folder_12_bauzeitenplan: "gdrive-folder-id"
folder_13_vertriebsweg: "gdrive-folder-id"
folder_14_bauausstattung: "gdrive-folder-id"
folder_15_flaechenberechnung: "gdrive-folder-id"
folder_16_werkvertraege: "gdrive-folder-id"
folder_17_bauzeichnungen: "gdrive-folder-id"
folder_18_baugenehmigung: "gdrive-folder-id"
folder_19_teilungserklaerung: "gdrive-folder-id"
folder_20_versicherungen: "gdrive-folder-id"
folder_21_verkaufsvertrag: "gdrive-folder-id"
folder_22_gutachterauftrag: "gdrive-folder-id"

// WIRTSCHAFTLICHE UNTERLAGEN
folder_23_jahresabschluesse: "gdrive-folder-id"
folder_24_bwa: "gdrive-folder-id"
folder_25_steuernummern: "gdrive-folder-id"
folder_26_schufa: "gdrive-folder-id"
folder_27_einkommensteuern: "gdrive-folder-id"
folder_28_vermoegensuebersicht: "gdrive-folder-id"
folder_29_eigenkapitalnachweis: "gdrive-folder-id"
folder_30_projektliste: "gdrive-folder-id"

// RECHTLICHE UNTERLAGEN
folder_31_hr_auszug: "gdrive-folder-id"
folder_32_gesellschaftsvertrag: "gdrive-folder-id"
folder_33_personalausweise: "gdrive-folder-id"
folder_34_bautraegerzulassung: "gdrive-folder-id"
folder_35_organigramm: "gdrive-folder-id"

// SONSTIGES
folder_36_exitstrategie: "gdrive-folder-id"
folder_37_sonstiges: "gdrive-folder-id"
```

### Step 2: Create Google Drive Folder Structure

**Option A: Manual Creation**
1. Create client folder: `Eugene_Bautraeger_2024`
2. Create 4 category folders
3. Create all 37 subfolders as shown above
4. Copy each folder ID into n8n variables

**Option B: Automated Script** (Recommended)
Create a separate n8n workflow that auto-creates all folders and stores IDs.

### Step 3: Add Type Switch Node

After the 4 Level 2 AI classification nodes, add a Type Switch node with 37 outputs:

```json
{
  "parameters": {
    "dataType": "string",
    "value1": "={{ $json.choices[0].message.content }}",
    "rules": {
      "rules": [
        // OBJEKTUNTERLAGEN (22 types)
        {"operation": "contains", "value2": "projektbeschreibung", "output": 0},
        {"operation": "contains", "value2": "kaufvertrag", "output": 1},
        {"operation": "contains", "value2": "grundbuchauszug", "output": 2},
        {"operation": "contains", "value2": "eintragungsbewilligungen", "output": 3},
        {"operation": "contains", "value2": "bodenrichtwert", "output": 4},
        {"operation": "contains", "value2": "baulastenverzeichnis", "output": 5},
        {"operation": "contains", "value2": "altlastenkataster", "output": 6},
        {"operation": "contains", "value2": "baugrundgutachten", "output": 7},
        {"operation": "contains", "value2": "lageplan", "output": 8},
        {"operation": "contains", "value2": "bautraegerkalkulation", "output": 9},
        {"operation": "contains", "value2": "verkaufspreise", "output": 10},
        {"operation": "contains", "value2": "bauzeitenplan", "output": 11},
        {"operation": "contains", "value2": "vertriebsweg", "output": 12},
        {"operation": "contains", "value2": "bauausstattung", "output": 13},
        {"operation": "contains", "value2": "flaechenberechnung", "output": 14},
        {"operation": "contains", "value2": "werkvertraege", "output": 15},
        {"operation": "contains", "value2": "bauzeichnungen", "output": 16},
        {"operation": "contains", "value2": "baugenehmigung", "output": 17},
        {"operation": "contains", "value2": "teilungserklaerung", "output": 18},
        {"operation": "contains", "value2": "versicherungen", "output": 19},
        {"operation": "contains", "value2": "verkaufsvertrag", "output": 20},
        {"operation": "contains", "value2": "gutachterauftrag", "output": 21},

        // WIRTSCHAFTLICHE (8 types)
        {"operation": "contains", "value2": "jahresabschluesse", "output": 22},
        {"operation": "contains", "value2": "bwa", "output": 23},
        {"operation": "contains", "value2": "steuernummern", "output": 24},
        {"operation": "contains", "value2": "schufa", "output": 25},
        {"operation": "contains", "value2": "einkommensteuern", "output": 26},
        {"operation": "contains", "value2": "vermoegensuebersicht", "output": 27},
        {"operation": "contains", "value2": "eigenkapitalnachweis", "output": 28},
        {"operation": "contains", "value2": "projektliste", "output": 29},

        // RECHTLICHE (5 types)
        {"operation": "contains", "value2": "hr_auszug", "output": 30},
        {"operation": "contains", "value2": "gesellschaftsvertrag", "output": 31},
        {"operation": "contains", "value2": "personalausweise", "output": 32},
        {"operation": "contains", "value2": "bautraegerzulassung", "output": 33},
        {"operation": "contains", "value2": "organigramm", "output": 34},

        // SONSTIGES (2 types)
        {"operation": "contains", "value2": "exitstrategie", "output": 35},
        {"operation": "contains", "value2": "sonstiges", "output": 36}
      ]
    }
  },
  "name": "Type Switch (37-way)",
  "type": "n8n-nodes-base.switch",
  "typeVersion": 3
}
```

### Step 4: Create Set Filename Nodes

Create 37 "Set Filename" nodes (one for each document type). Example for Type #1:

```json
{
  "parameters": {
    "mode": "manual",
    "fields": {
      "values": [
        {
          "name": "newFilename",
          "stringValue": "EXPOSE_{{ $vars.clientName }}_{{ $now.format('YYYYMMDD') }}.pdf"
        },
        {
          "name": "destinationFolderId",
          "stringValue": "={{ $vars.folder_01_projektbeschreibung }}"
        },
        {
          "name": "documentType",
          "stringValue": "Projektbeschreibung / Exposé"
        },
        {
          "name": "category",
          "stringValue": "OBJEKTUNTERLAGEN"
        },
        {
          "name": "typePrefix",
          "stringValue": "EXPOSE"
        }
      ]
    }
  },
  "name": "Set Filename - Projektbeschreibung",
  "type": "n8n-nodes-base.set",
  "typeVersion": 3
}
```

Repeat for all 37 types with corresponding prefixes and folder IDs.

### Step 5: Add Move File Node

```json
{
  "parameters": {
    "operation": "move",
    "fileId": "={{ $json.id }}",
    "driveId": {
      "__rl": true,
      "mode": "list",
      "value": "My Drive"
    },
    "folderId": {
      "__rl": true,
      "mode": "list",
      "value": "={{ $json.destinationFolderId }}"
    },
    "options": {
      "newName": "={{ $json.newFilename }}"
    }
  },
  "name": "Move and Rename File",
  "type": "n8n-nodes-base.googleDrive",
  "typeVersion": 3
}
```

### Step 6: Add Google Sheets Log Node

```json
{
  "parameters": {
    "operation": "appendRow",
    "documentId": "={{ $vars.logSheetId }}",
    "sheetName": "Processing Log",
    "valueInputMode": "manual",
    "values": {
      "values": [
        {"column": "Timestamp", "value": "={{ $now.format('YYYY-MM-DD HH:mm:ss') }}"},
        {"column": "Original Filename", "value": "={{ $json.filename }}"},
        {"column": "Category", "value": "={{ $json.category }}"},
        {"column": "Document Type (German)", "value": "={{ $json.documentType }}"},
        {"column": "New Filename", "value": "={{ $json.newFilename }}"},
        {"column": "Destination Folder", "value": "={{ $json.destinationFolderId }}"},
        {"column": "Client Name", "value": "={{ $vars.clientName }}"},
        {"column": "Sender Email", "value": "={{ $('Gmail Trigger').item.json.from }}"},
        {"column": "OCR Used", "value": "={{ $json.needsOCR ? 'Yes' : 'No' }}"},
        {"column": "Text Length", "value": "={{ $json.textLength }}"}
      ]
    }
  },
  "name": "Log to Google Sheets",
  "type": "n8n-nodes-base.googleSheets",
  "typeVersion": 4
}
```

### Step 7: Add Email Confirmation Node (Optional)

```json
{
  "parameters": {
    "operation": "send",
    "message": {
      "to": "={{ $('Gmail Trigger').item.json.from }}",
      "subject": "Dokument verarbeitet: {{ $json.documentType }}",
      "body": "Ihr Dokument wurde erfolgreich klassifiziert und gespeichert.\n\nDetails:\n- Kategorie: {{ $json.category }}\n- Dokumenttyp: {{ $json.documentType }}\n- Neuer Dateiname: {{ $json.newFilename }}\n- Ordner: {{ $json.destinationFolderId }}\n\nMit freundlichen Grüßen,\nIhr Dokumenten-Organizer"
    }
  },
  "name": "Send Confirmation Email (German)",
  "type": "n8n-nodes-base.gmail",
  "typeVersion": 2
}
```

---

## Testing Strategy

### Phase 1: Individual Node Testing
1. Test Gmail trigger with sample email
2. Test file type detection with digital and scanned PDFs
3. Test OCR path with scanned German document
4. Test Level 1 classification with documents from each category
5. Test Level 2 classification for each of the 37 types

### Phase 2: End-to-End Testing
Test all 37 document types:

**OBJEKTUNTERLAGEN (22 types):**
- [ ] Projektbeschreibung → EXPOSE prefix → 01_Projektbeschreibung/
- [ ] Kaufvertrag → KAUF prefix → 02_Kaufvertrag/
- [ ] Grundbuchauszug → GRUNDBUCH prefix → 03_Grundbuchauszug/
- [ ] ... (all 22 types)

**WIRTSCHAFTLICHE (8 types):**
- [ ] Jahresabschlüsse → JAHRAB prefix → 23_Jahresabschluesse/
- [ ] BWA → BWA prefix → 24_BWA/
- [ ] ... (all 8 types)

**RECHTLICHE (5 types):**
- [ ] HR-Auszug → HR prefix → 31_HR_Auszug/
- [ ] ... (all 5 types)

**SONSTIGES (2 types):**
- [ ] Exit-Strategie → EXIT prefix → 36_Exit_Strategie/
- [ ] Sonstiges → MISC prefix → 37_Sonstiges/

### Phase 3: Error Handling Testing
- [ ] Email without attachments
- [ ] Unsupported file type (JPG, ZIP)
- [ ] Scanned document with poor quality
- [ ] Ambiguous German legal document
- [ ] Duplicate filename collision
- [ ] Missing folder ID variable

---

## Deployment Checklist

- [ ] Create all 37 folders in Google Drive
- [ ] Store all folder IDs in n8n variables
- [ ] Configure Gmail OAuth credentials
- [ ] Configure Google Drive OAuth credentials
- [ ] Configure OpenAI API key
- [ ] Configure AWS Textract credentials (optional)
- [ ] Import blueprint JSON into n8n
- [ ] Add Type Switch node with 37 branches
- [ ] Create all 37 Set Filename nodes
- [ ] Add Move File node
- [ ] Add Log to Google Sheets node
- [ ] Create Google Sheets log with proper columns
- [ ] Add Email Confirmation node (optional)
- [ ] Connect all nodes properly
- [ ] Test with sample documents
- [ ] Monitor first 100 documents
- [ ] Adjust AI prompts if needed
- [ ] Enable workflow in production

---

## Maintenance

### Weekly Tasks
- Review Google Sheets log for misclassifications
- Check low-confidence classifications
- Monitor folder distribution (ensure all 37 folders receive documents)

### Monthly Tasks
- Review AI classification accuracy per document type
- Update prompts if new German terminology emerges
- Check for missing documents in checklist
- Archive old versions of updated documents

### Quarterly Tasks
- Review OCR costs and accuracy
- Consider switching to Tesseract if AWS costs high
- Update folder structure if new document types added
- Review and update this guide

---

## Cost Optimization

**Current Cost Structure (per 1000 docs):**
- Digital PDFs (70%): $7.00 (AI classification only)
- Scanned PDFs (30%): $1,357.00 (AI + AWS Textract OCR)
- **Total: $1,364.00 or $1.36/document**

**Cost Reduction Options:**
1. **Switch to Tesseract OCR** (free) → Reduces to ~$7.00 per 1000 docs
2. **Use GPT-4o-mini more efficiently** → Reduce prompt sizes
3. **Batch processing** → Process multiple documents in parallel

---

## Exit Strategy Document Handling

The **exitstrategie** document type has been added as Type #36 in the SONSTIGES category:
- **Type ID:** exitstrategie
- **File Prefix:** EXIT
- **Folder:** 36_Exit_Strategie
- **Category:** SONSTIGES
- **AI Prompt:** Detects exit strategies, liquidation plans, ROI projections, property sale timelines

This addresses the user requirement: *"exit strategy has not been mapped anywhere"*

---

## Support and Troubleshooting

### Common Issues

**Issue 1: Document routes to wrong folder**
- Check AI prompt for that document type
- Review extracted text in log
- Adjust confidence threshold

**Issue 2: OCR fails on German documents**
- Ensure AWS Textract German language pack enabled
- Check character encoding (UTF-8)
- Consider Tesseract with German language support

**Issue 3: Gmail trigger not detecting emails**
- Check OAuth credentials
- Verify Gmail label filter
- Check polling interval

**Issue 4: Folder ID not found**
- Verify all 37 folder IDs in n8n variables
- Check Google Drive permissions
- Ensure folders not deleted

---

## Conclusion

This implementation guide provides everything needed to build a fully functional Document Organizer v2.0 workflow with:
- **37 document types** (35 from checklist + exit strategy + miscellaneous)
- **Hierarchical AI classification** (2 levels)
- **German language support** (OCR, AI prompts, folder names)
- **Complete folder structure** matching Bauträger checklist requirements
- **Scalable architecture** for future additions

The blueprint JSON provides the core workflow structure. Use this guide to complete the implementation with all routing logic, filename nodes, and folder mappings.
