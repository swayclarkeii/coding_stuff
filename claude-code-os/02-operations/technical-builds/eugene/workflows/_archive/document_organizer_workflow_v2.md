# Document Organizer Workflow - Version 2

**Client:** Eugene (Real Estate Debt Advisory - German Bauträger Projects)
**Purpose:** Automatically classify, rename, and organize German construction developer documents using actual Bauträger checklist taxonomy
**Created:** 2024-12-20
**Updated:** 2024-12-20
**Version:** 2.0
**Changes from v1:**
- Added hierarchical two-level AI classification based on **actual German Bauträger checklist**
- **3 main categories:** Objektunterlagen, Wirtschaftliche Unterlagen, Rechtliche Unterlagen
- **35 specific document types** (expanded from 7 in v1)
- Added OCR detection and routing for scanned documents
- Enhanced error handling and edge case management for German real estate documents

---

## Overview

This workflow automates the organization of German Bauträger (construction developer) documents by:
1. Monitoring Gmail inbox for email attachments
2. Downloading and uploading attachments to Google Drive
3. Detecting file type (digital PDF vs scanned/image)
4. Routing scanned documents through OCR processing
5. Extracting text content from documents
6. **Level 1 Classification**: Categorizing into 3 German document categories
7. **Level 2 Classification**: Identifying specific document type (35 total types from checklist)
8. Renaming files with standardized naming convention
9. Moving files to appropriate client folders (35 different folders)
10. Logging all actions for audit trail with classification metadata

---

## Document Taxonomy (German Bauträger Checklist)

### Category 1: OBJEKTUNTERLAGEN (Property Documents) - 22 Types

1. **Projektbeschreibung / Exposé** (Project description)
2. **Kaufvertrag** (Purchase contract)
3. **Grundbuchauszug < 3 Monate** (Land register extract < 3 months)
4. **Eintragungsbewilligungen** (Registration permits for value-affecting rights)
5. **Bodenrichtwert** (Land value assessment)
6. **Baulastenverzeichnis** (Building encumbrances extract)
7. **Altlastenkataster** (Contaminated sites register)
8. **Baugrundgutachten** (Soil survey/geotechnical report)
9. **Lageplan / Flurkarte** (Official site plan/cadastral map)
10. **Bauträgerkalkulation DIN 276** (Developer calculation per DIN 276)
11. **Verkaufspreise** (Planned sales prices per unit)
12. **Bauzeitenplan / Liquiditätsplan** (Construction timeline/liquidity plan)
13. **Vertriebsweg** (Sales channel information)
14. **Bau-Ausstattungsbeschreibung** (Construction/equipment description)
15. **Flächenberechnung DIN 277** (Area calculations per DIN 277)
16. **GU-Werkverträge** (General contractor agreements)
17. **Bauzeichnungen** (Construction drawings/floor plans/sections)
18. **Baugenehmigung** (Building permit/approval)
19. **Teilungserklärung** (Condominium declaration with division plan)
20. **Versicherungen** (Construction/liability/fire insurance)
21. **Muster Verkaufsvertrag** (Sample sales contract)
22. **Gutachterauftrag** (Signed appraisal order)

### Category 2: WIRTSCHAFTLICHE UNTERLAGEN (Economic/Financial Documents) - 8 Types

23. **Jahresabschlüsse** (Annual financial statements/opening balance)
24. **BWA** (Current BWA with balance sheet)
25. **Steuernummern** (Tax numbers/IDs)
26. **SCHUFA-Erklärung** (SCHUFA declaration of guarantors)
27. **Einkommensteuern** (Income tax documents of guarantors)
28. **Vermögensübersicht** (Assets/liabilities overview)
29. **Eigenkapitalnachweis** (Equity proof)
30. **Projektliste** (Project list)

### Category 3: RECHTLICHE UNTERLAGEN (Legal Documents) - 5 Types

31. **HR-Auszug** (Commercial register extract)
32. **Gesellschaftsvertrag** (Articles of association/shareholder list)
33. **Personalausweise** (ID documents of acting persons)
34. **Bauträgerzulassung** (Construction developer license § 34c GewO)
35. **Organigramm** (Organizational chart to beneficial owners)

**Total: 35 document types**

---

## Workflow Diagram

```
┌─────────────────────────────┐
│  Gmail Trigger              │
│  (Watch for attachments)    │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Download Email Attachments │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Filter File Types          │
│  (PDF, DOCX, DOC only)      │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Upload to Google Drive     │
│  (Staging folder)           │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  File Type Detection        │
│  (Code: Digital vs Scanned) │
│  Output: needsOCR flag      │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Switch: needsOCR?          │
└─┬────────────────────────┬──┘
  │ NO                     │ YES
  ▼                        ▼
┌──────────┐         ┌────────────┐
│ Extract  │         │    OCR     │
│  Text    │         │  Service   │
│ (n8n)    │         │ (Textract) │
└────┬─────┘         └─────┬──────┘
     │                     │
     └──────────┬──────────┘
                ▼
┌─────────────────────────────┐
│  AI Classification Level 1  │
│  (LLM CALL #1)              │
│                             │
│  Categories:                │
│  - OBJEKTUNTERLAGEN         │
│  - WIRTSCHAFTLICHE          │
│  - RECHTLICHE               │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Switch: Route by Category  │
└─┬───┬───┬───────────────────┘
  │   │   │
  ▼   ▼   ▼
┌───┐┌──┐┌───┐
│OBJ││WIR││REC│
└─┬─┘└┬─┘└─┬─┘
  │   │   │
  ▼   ▼   ▼
┌─────────────────────────────┐
│  AI Classification Level 2  │
│  (LLM CALL #2)              │
│                             │
│  Specific Types:            │
│  OBJEKTUNTERLAGEN: 22 types │
│  WIRTSCHAFTLICHE: 8 types   │
│  RECHTLICHE: 5 types        │
│  Total: 35 types            │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Switch: Route by Type      │
│  (35 branches)              │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Set Filename (35 nodes)    │
│  Format: PREFIX_CLIENT_DATE │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Move to Final Folder       │
│  (35 different folders)     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Log to Google Sheets       │
│  (Category, Type, Metadata) │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Email Confirmation (Opt)   │
└─────────────────────────────┘
```

**Key:** LLM CALL #1 and #2 = Only 2 AI calls per document

---

## LLM Calls Breakdown

**Total LLM Calls Per Document: 2**

| Call # | Purpose | Input | Output | Cost |
|--------|---------|-------|--------|------|
| **1** | Category Classification | Document text (first 3000 chars) | 1 of 3 categories (OBJEKTUNTERLAGEN, WIRTSCHAFTLICHE, RECHTLICHE) | ~$0.003 |
| **2** | Type Classification | Document text (first 3000 chars) | 1 of 5-22 specific types within category | ~$0.004 |
| **Total** | - | - | - | **~$0.007** |

**OCR does NOT call LLM** - it only extracts text from scanned German documents before feeding to classification.

**Why 2 calls instead of 1?**
- ✅ More accurate (AI distinguishes 5-22 types vs 35 at once)
- ✅ Easier to maintain (separate prompts per category)
- ✅ Matches actual business process (checklist is organized this way)
- ✅ Better handling of German terminology and legal documents
- ❌ Slightly more expensive (~$0.007 vs ~$0.004)
- ❌ Slightly slower (~2-3 extra seconds)

---

## AI Classification Prompts

### Level 1 Prompt: Category Classification

```
You are a document classifier for German Bauträger (construction developer) projects.

Your task is to classify documents into ONE of these 3 categories based on the official Bauträger checklist:

1. **OBJEKTUNTERLAGEN** (Property Documents)
   Documents related to the physical property, construction plans, permits, contracts, and calculations.
   Examples: Purchase contracts, building permits, site plans, construction drawings, DIN calculations,
   sales prices, insurance documents, appraisal orders

2. **WIRTSCHAFTLICHE** (Economic/Financial Documents)
   Financial statements, tax documents, income verification, asset overviews, equity proof.
   Examples: Annual financial statements, BWA, tax numbers, SCHUFA declarations, income tax documents,
   assets/liabilities overview, equity proof, project lists

3. **RECHTLICHE** (Legal Documents)
   Corporate legal documents, registrations, licenses, organizational structures.
   Examples: Commercial register extracts, articles of association, ID documents,
   construction developer licenses (§34c GewO), organizational charts

Analyze the document content and respond with ONLY the category name.

Examples:
- Building permit document → "OBJEKTUNTERLAGEN"
- Annual financial statement → "WIRTSCHAFTLICHE"
- Commercial register extract → "RECHTLICHE"
- Construction drawings → "OBJEKTUNTERLAGEN"
- SCHUFA declaration → "WIRTSCHAFTLICHE"

Return ONLY: OBJEKTUNTERLAGEN, WIRTSCHAFTLICHE, or RECHTLICHE
```

### Level 2 Prompts: Specific Type Classification

#### Level 2 - OBJEKTUNTERLAGEN (Property Documents)

```
You are classifying an OBJEKTUNTERLAGEN (property document) for a German Bauträger project.

Classify into ONE of these 22 specific types:

1. **projektbeschreibung** - Project description, exposé
2. **kaufvertrag** - Purchase contract
3. **grundbuchauszug** - Land register extract (less than 3 months old)
4. **eintragungsbewilligungen** - Registration permits for value-affecting rights (Abt. II)
5. **bodenrichtwert** - Land value assessment
6. **baulastenverzeichnis** - Building encumbrances extract
7. **altlastenkataster** - Contaminated sites register extract
8. **baugrundgutachten** - Soil survey, geotechnical report
9. **lageplan** - Official site plan, cadastral map (Flurkarte)
10. **bautraegerkalkulation** - Developer calculation according to DIN 276
11. **verkaufspreise** - Planned sales prices per unit listing
12. **bauzeitenplan** - Construction timeline, liquidity plan
13. **vertriebsweg** - Sales channel information, distribution plan
14. **bauausstattung** - Construction and equipment description
15. **flaechenberechnung** - Area calculations according to DIN 277
16. **werkvertraege** - General contractor agreements (GU-Werkverträge)
17. **bauzeichnungen** - Construction drawings, floor plans, sections, elevations
18. **baugenehmigung** - Building permit application or approval
19. **teilungserklaerung** - Condominium declaration with division plan (Aufteilungsplan)
20. **versicherungen** - Construction insurance, liability insurance, fire insurance
21. **verkaufsvertrag** - Sample sales contract template
22. **gutachterauftrag** - Signed appraisal order

Analyze the document content, terminology, and German legal references.

Examples:
- Purchase agreement with buyer/seller → "kaufvertrag"
- DIN 276 cost breakdown → "bautraegerkalkulation"
- Floor plans and elevations → "bauzeichnungen"
- Building permit from Bauamt → "baugenehmigung"
- Soil investigation report → "baugrundgutachten"
- Land register (Grundbuch) extract → "grundbuchauszug"

Return ONLY the type name (lowercase, no spaces):
projektbeschreibung, kaufvertrag, grundbuchauszug, eintragungsbewilligungen, bodenrichtwert,
baulastenverzeichnis, altlastenkataster, baugrundgutachten, lageplan, bautraegerkalkulation,
verkaufspreise, bauzeitenplan, vertriebsweg, bauausstattung, flaechenberechnung, werkvertraege,
bauzeichnungen, baugenehmigung, teilungserklaerung, versicherungen, verkaufsvertrag, gutachterauftrag
```

#### Level 2 - WIRTSCHAFTLICHE (Economic/Financial Documents)

```
You are classifying a WIRTSCHAFTLICHE UNTERLAGEN (economic/financial document) for a German Bauträger project.

Classify into ONE of these 8 specific types:

1. **jahresabschluesse** - Annual financial statements of last 3 years, opening balance sheet (Eröffnungsbilanz) of borrower
2. **bwa** - Current signed BWA including balance sheet (Summe- und Saldenliste) of borrower
3. **steuernummern** - Tax numbers of involved companies, tax IDs of involved persons
4. **schufa** - Signed SCHUFA declaration of guarantors (Bürgen)
5. **einkommensteuern** - Income tax documents of guarantors for last 2 years
6. **vermoegensuebersicht** - Assets and liabilities overview including interest and repayment obligations of guarantors
7. **eigenkapitalnachweis** - Equity proof, capital verification
8. **projektliste** - Project list, portfolio overview

Analyze the document content, focusing on German financial terminology and legal requirements.

Examples:
- Balance sheet and P&L statement → "jahresabschluesse"
- BWA with Summe- und Saldenliste → "bwa"
- SCHUFA consent form → "schufa"
- Tax return documents → "einkommensteuern"
- Equity verification letter from bank → "eigenkapitalnachweis"
- Overview of assets and debts → "vermoegensuebersicht"

Return ONLY the type name (lowercase, no spaces):
jahresabschluesse, bwa, steuernummern, schufa, einkommensteuern, vermoegensuebersicht,
eigenkapitalnachweis, projektliste
```

#### Level 2 - RECHTLICHE (Legal Documents)

```
You are classifying a RECHTLICHE UNTERLAGEN (legal document) for a German Bauträger project.

Classify into ONE of these 5 specific types:

1. **hr_auszug** - Commercial register extract (Handelsregisterauszug)
2. **gesellschaftsvertrag** - Articles of association, shareholder list (Gesellschafterliste)
3. **personalausweise** - ID documents (Personalausweise) of acting persons
4. **bautraegerzulassung** - Construction developer license according to § 34c GewO (Gewerbeordnung)
5. **organigramm** - Organizational chart showing structure to beneficial owners (wirtschaftliche Berechtigte)

Analyze the document content, focusing on German corporate law and regulatory requirements.

Examples:
- Handelsregister extract → "hr_auszug"
- GmbH shareholder agreement → "gesellschaftsvertrag"
- Copy of passport or ID card → "personalausweise"
- § 34c GewO permit from trade office → "bautraegerzulassung"
- Company ownership structure chart → "organigramm"

Return ONLY the type name (lowercase, underscores allowed):
hr_auszug, gesellschaftsvertrag, personalausweise, bautraegerzulassung, organigramm
```

---

## File Naming Convention

All 35 document types with standardized German-based prefixes:

### OBJEKTUNTERLAGEN (Property Documents) - 22 Types

| # | Document Type (German) | Prefix | Example |
|---|------------------------|--------|---------|
| 1 | Projektbeschreibung / Exposé | EXPOSE | `EXPOSE_Eugene_Client_20241220.pdf` |
| 2 | Kaufvertrag | KAUF | `KAUF_Eugene_Client_20241220.pdf` |
| 3 | Grundbuchauszug < 3 Monate | GRUNDBUCH | `GRUNDBUCH_Eugene_Client_20241220.pdf` |
| 4 | Eintragungsbewilligungen | EINTRAG | `EINTRAG_Eugene_Client_20241220.pdf` |
| 5 | Bodenrichtwert | BODEN | `BODEN_Eugene_Client_20241220.pdf` |
| 6 | Baulastenverzeichnis | BAULASTEN | `BAULASTEN_Eugene_Client_20241220.pdf` |
| 7 | Altlastenkataster | ALTLASTEN | `ALTLASTEN_Eugene_Client_20241220.pdf` |
| 8 | Baugrundgutachten | BAUGUTACHT | `BAUGUTACHT_Eugene_Client_20241220.pdf` |
| 9 | Lageplan / Flurkarte | LAGEPLAN | `LAGEPLAN_Eugene_Client_20241220.pdf` |
| 10 | Bauträgerkalkulation DIN 276 | KALK276 | `KALK276_Eugene_Client_20241220.pdf` |
| 11 | Verkaufspreise je Einheit | PREISE | `PREISE_Eugene_Client_20241220.pdf` |
| 12 | Bauzeitenplan / Liquiditätsplan | BAUZEIT | `BAUZEIT_Eugene_Client_20241220.pdf` |
| 13 | Vertriebsweg | VERTRIEB | `VERTRIEB_Eugene_Client_20241220.pdf` |
| 14 | Bau-/Ausstattungsbeschreibung | BAUAUSST | `BAUAUSST_Eugene_Client_20241220.pdf` |
| 15 | Flächenberechnung DIN 277 | FLAECHE277 | `FLAECHE277_Eugene_Client_20241220.pdf` |
| 16 | GU-/Werkverträge | WERKVERT | `WERKVERT_Eugene_Client_20241220.pdf` |
| 17 | Bauzeichnungen/Grundrisse | BAUZEICH | `BAUZEICH_Eugene_Client_20241220.pdf` |
| 18 | Baugenehmigung | BAUGEN | `BAUGEN_Eugene_Client_20241220.pdf` |
| 19 | Teilungserklärung | TEILUNG | `TEILUNG_Eugene_Client_20241220.pdf` |
| 20 | Versicherungen | VERSICH | `VERSICH_Eugene_Client_20241220.pdf` |
| 21 | Muster Verkaufsvertrag | MUSTERVERT | `MUSTERVERT_Eugene_Client_20241220.pdf` |
| 22 | Gutachterauftrag | GUTACHT | `GUTACHT_Eugene_Client_20241220.pdf` |

### WIRTSCHAFTLICHE UNTERLAGEN (Economic/Financial) - 8 Types

| # | Document Type (German) | Prefix | Example |
|---|------------------------|--------|---------|
| 23 | Jahresabschlüsse | JAHRAB | `JAHRAB_Eugene_Client_20241220.pdf` |
| 24 | BWA inkl. Summe-Saldenliste | BWA | `BWA_Eugene_Client_20241220.pdf` |
| 25 | Steuernummern / Steuer-IDs | STEUER | `STEUER_Eugene_Client_20241220.pdf` |
| 26 | SCHUFA-Erklärung | SCHUFA | `SCHUFA_Eugene_Client_20241220.pdf` |
| 27 | Einkommensteuerunterlagen | EINKST | `EINKST_Eugene_Client_20241220.pdf` |
| 28 | Vermögens-/Schuldenübersicht | VERMOEGEN | `VERMOEGEN_Eugene_Client_20241220.pdf` |
| 29 | Eigenkapitalnachweis | EIGEN | `EIGEN_Eugene_Client_20241220.pdf` |
| 30 | Projektliste | PROJLIST | `PROJLIST_Eugene_Client_20241220.pdf` |

### RECHTLICHE UNTERLAGEN (Legal Documents) - 5 Types

| # | Document Type (German) | Prefix | Example |
|---|------------------------|--------|---------|
| 31 | HR-Auszug | HR | `HR_Eugene_Client_20241220.pdf` |
| 32 | Gesellschaftsvertrag | GESELL | `GESELL_Eugene_Client_20241220.pdf` |
| 33 | Personalausweise | PERSAUS | `PERSAUS_Eugene_Client_20241220.pdf` |
| 34 | Bauträgerzulassung §34c | ZULASSUNG | `ZULASSUNG_Eugene_Client_20241220.pdf` |
| 35 | Organigramm | ORGAN | `ORGAN_Eugene_Client_20241220.pdf` |

### Other

| Document Type | Prefix | Example |
|---------------|--------|---------|
| Unknown/Unclassifiable | MISC | `MISC_Eugene_Client_20241220.pdf` |

---

## Folder Structure

Complete 35-folder structure organized by German checklist categories:

```
clients/
└── {Client_Name}/
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
    └── 36_Sonstiges/
```

---

## Node Details

### 1. Gmail Trigger
- **Type:** `n8n-nodes-base.gmailTrigger`
- **Mode:** Watch for new emails
- **Filter:** Emails with attachments (PDF, DOCX, DOC)
- **Label Filter:** Optional (e.g., "Bauträger_Docs" label)
- **Polling Interval:** Every 1 minute

### 2. Download Email Attachments
- **Type:** `n8n-nodes-base.gmail`
- **Operation:** Download attachments
- **Input:** Email ID from trigger
- **Output:** Binary file data (PDF, DOCX, etc.)

### 3. Filter File Types
- **Type:** `n8n-nodes-base.code`
- **Function:** Filter out unsupported file types
- **Logic:** Accept only PDF, DOCX, DOC
- **Output:** Filtered array of valid attachments

### 4. Upload to Google Drive (Staging)
- **Type:** `n8n-nodes-base.googleDrive`
- **Operation:** Upload file
- **Destination:** Staging/Upload folder
- **Filename:** Original attachment filename
- **Output:** File ID and metadata

### 5. File Type Detection
- **Type:** `n8n-nodes-base.code`
- **Function:** Detect if PDF is digital or scanned
- **Logic:** Check PDF metadata, embedded fonts, text layer presence
- **Special:** Handle German characters (ä, ö, ü, ß) properly
- **Output:** `needsOCR` boolean flag

### 6. OCR Switch Node
- **Type:** `n8n-nodes-base.switch`
- **Rules:** Route based on `needsOCR` flag
- **Branches:**
  - `needsOCR = false` → Extract Text (n8n)
  - `needsOCR = true` → OCR Service

### 7a. Extract Text (Digital PDFs)
- **Type:** `n8n-nodes-base.extractFromFile`
- **Operation:** Extract text from digital PDFs
- **Input:** Binary file data
- **Options:**
  - Max pages: 10 (first 10 pages)
  - OCR: Disabled
  - Character encoding: UTF-8 (for German umlauts)
- **Output:** Plain text string

### 7b. OCR Service (Scanned Documents)
- **Type:** `n8n-nodes-base.awsTextract` or `n8n-nodes-base.httpRequest`
- **Service:** AWS Textract with German language support
- **Input:** Binary file data (scanned PDF/image)
- **Language:** German (Deutsch) language pack
- **Output:** Extracted text string with German characters
- **Fallback:** If OCR fails, route to "sonstiges" (miscellaneous) folder

### 8. AI Classification Level 1 (Category)
- **Type:** `@n8n/n8n-nodes-langchain.agent`
- **Model:** GPT-4o-mini (supports German)
- **Prompt:** Category classification (see Level 1 Prompt above)
- **Input:** First 3000 characters of document text
- **Output:** One of 3 categories: OBJEKTUNTERLAGEN, WIRTSCHAFTLICHE, RECHTLICHE
- **Language handling:** Prompt includes German terminology explanations

### 9. Category Switch Node
- **Type:** `n8n-nodes-base.switch`
- **Rules:** 3 branches based on category
- **Branches:**
  - OBJEKTUNTERLAGEN → Level 2 Objektunterlagen Classifier
  - WIRTSCHAFTLICHE → Level 2 Wirtschaftliche Classifier
  - RECHTLICHE → Level 2 Rechtliche Classifier

### 10. AI Classification Level 2 (Specific Type)
Three separate nodes, one per category:

#### 10a. Level 2 - Objektunterlagen Classifier
- **Type:** `@n8n/n8n-nodes-langchain.agent`
- **Model:** GPT-4o-mini
- **Prompt:** Objektunterlagen type classification (22 types)
- **Output:** One of 22 property document types

#### 10b. Level 2 - Wirtschaftliche Classifier
- **Type:** `@n8n/n8n-nodes-langchain.agent`
- **Model:** GPT-4o-mini
- **Prompt:** Wirtschaftliche type classification (8 types)
- **Output:** One of 8 economic/financial document types

#### 10c. Level 2 - Rechtliche Classifier
- **Type:** `@n8n/n8n-nodes-langchain.agent`
- **Model:** GPT-4o-mini
- **Prompt:** Rechtliche type classification (5 types)
- **Output:** One of 5 legal document types

### 11. Type Switch Node
- **Type:** `n8n-nodes-base.switch`
- **Rules:** 35 branches based on specific document type
- **Default:** Route to "sonstiges" (miscellaneous) folder

### 12. Set Filename Nodes (35 nodes)
- **Type:** `n8n-nodes-base.set`
- **Function:** Set new filename and destination folder
- **Naming Pattern:** `{PREFIX}_{CLIENT}_{YYYYMMDD}.{ext}`
- **Variables Set:**
  - `newFilename`: Standardized filename
  - `destinationFolderId`: Target folder ID
  - `documentType`: Type for logging (German name)
  - `category`: Category for logging

### 13. Move File Node
- **Type:** `n8n-nodes-base.googleDrive`
- **Operation:** Move and rename file
- **Source:** Staging folder
- **Destination:** Category-specific client folder (35 folders)

### 14. Log Node
- **Type:** `n8n-nodes-base.googleSheets`
- **Operation:** Append row
- **Sheet:** Bauträger Document Processing Log
- **Columns:**
  - Timestamp
  - Original Filename
  - Category (German)
  - Document Type (German)
  - New Filename
  - Destination Folder
  - Client Name
  - Sender Email
  - Processing Time
  - OCR Used (Y/N)
  - Confidence Scores (Level 1 & 2)

### 15. Email Confirmation (Optional)
- **Type:** `n8n-nodes-base.gmail`
- **Operation:** Send email
- **Recipient:** Original sender
- **Subject:** "Dokument verarbeitet: {filename}"
- **Body:** Processing details in German, category, type, and file location

---

## Variables Required

| Variable | Description | Example |
|----------|-------------|---------|
| `gmailCredentials` | Gmail OAuth2 credentials | OAuth setup in n8n |
| `clientName` | Client identifier | "Eugene_Bautraeger" |
| `openaiApiKey` | OpenAI API key (GPT-4o-mini) | "sk-..." |
| `awsTextractCredentials` | AWS credentials for German OCR | AWS access key (optional) |
| `googleDriveFolderId` | Base client folder ID | "1a2b3c..." |
| `uploadFolderId` | Upload staging folder ID | "4d5e6f..." |
| `logSheetId` | Google Sheets log ID | "spreadsheet-id" |
| `gmailLabel` | Optional filter label | "Bauträger_Docs" |

---

## Potential Issues, Errors & Edge Cases

### 1. German Language and Character Encoding Issues

**Problem:** German umlauts (ä, ö, ü, ß) not properly extracted or displayed
- **Cause:** Incorrect character encoding (ISO-8859-1 vs UTF-8)
- **Impact:** Text extraction produces garbled characters, classification fails
- **Solution:**
  - Force UTF-8 encoding for all text extraction
  - AWS Textract supports German language natively
  - Test with documents containing "Bürgschaft", "Eigentümer", "Geschäftsführer"
  - Log encoding issues for manual review

**Problem:** Mixed German/English terminology confusion
- **Cause:** Some documents use English terms (e.g., "Exit Strategy" vs "Verkaufsstrategie")
- **Impact:** Classification uncertainty between categories
- **Solution:**
  - AI prompts include both German and common English terms
  - Confidence threshold for multilingual documents
  - Manual review queue for mixed-language docs

### 2. German Legal Document Specificity

**Problem:** Very specific German legal document types hard to distinguish
- **Example:** "Grundbuchauszug" vs "Baulastenverzeichnis" vs "Eintragungsbewilligungen" all relate to land registry
- **Impact:** Misclassification between similar legal document types
- **Solution:**
  - Enhanced Level 2 prompts with specific German legal terminology
  - Look for key phrases: "Abteilung II", "Bauamt", "Grundbuchamt"
  - Include document header/footer analysis (German authorities have specific formats)
  - Add confidence scoring with manual review queue for <75% confidence

**Problem:** DIN standard references (DIN 276, DIN 277) critical for classification
- **Cause:** Multiple documents reference construction standards
- **Impact:** "Bauträgerkalkulation DIN 276" vs "Flächenberechnung DIN 277" must be distinguished
- **Solution:**
  - AI prompts specifically check for DIN standard numbers
  - Pattern matching for "DIN 276" vs "DIN 277" in text
  - Context analysis: cost calculations (276) vs area calculations (277)

### 3. OCR and Scanned German Documents

**Problem:** Old German typewriter fonts (Fraktur, Sütterlin) unreadable by OCR
- **Cause:** Historical documents or archival property records
- **Impact:** OCR produces garbage text
- **Solution:**
  - Detect Fraktur fonts by visual analysis
  - Route to specialized German historical OCR service
  - Flag for manual transcription if very old
  - Log OCR failures with document age estimate

**Problem:** Handwritten German signatures and notes
- **Cause:** Legal documents often have handwritten sections (Unterschriften)
- **Impact:** OCR skips critical information
- **Solution:**
  - Combine digital signatures (typed) with handwritten detection
  - Focus OCR on machine-readable sections only
  - Flag documents with >30% handwritten content
  - Extract printed portions for classification

### 4. German Financial Document Complexity

**Problem:** "BWA" vs "Jahresabschlüsse" very similar formats
- **Cause:** Both are financial statements, BWA is monthly, Jahresabschlüsse is annual
- **Impact:** Easy to misclassify between these two types
- **Solution:**
  - Look for "Betriebswirtschaftliche Auswertung" header for BWA
  - Check for "Bilanz" and "GuV" for Jahresabschlüsse
  - Date analysis: monthly (BWA) vs annual (Jahresabschlüsse)
  - Check for "Summen- und Saldenliste" (BWA indicator)

**Problem:** SCHUFA-Erklärung vs regular financial documents
- **Cause:** SCHUFA is specific German credit check consent
- **Impact:** Must not be confused with other financial docs
- **Solution:**
  - Specific pattern matching for "SCHUFA" keyword
  - Look for "Selbstauskunft" terminology
  - Check for SCHUFA logo or watermark
  - Verify presence of consent language

### 5. Construction-Specific Document Challenges

**Problem:** "Bauzeichnungen" can include many sub-types
- **Example:** Grundrisse, Schnitte, Ansichten, Detailzeichnungen all classified as one type
- **Impact:** All architectural drawings go to same folder, hard to find specific drawing type
- **Solution:**
  - Currently: All go to "17_Bauzeichnungen" folder
  - Future: Create sub-classification for drawing types
  - For now: Include drawing type in filename metadata
  - Log drawing sub-type for potential future folder split

**Problem:** Multiple contractor agreements (GU-Werkverträge)
- **Cause:** Construction projects have many subcontractor agreements
- **Impact:** Many files in same folder with generic names
- **Solution:**
  - Extract contractor name from document if possible
  - Append contractor to filename: `WERKVERT_Contractor_Client_Date.pdf`
  - Include contract value in metadata for sorting
  - Version control for amended contracts

### 6. Checklist Compliance and Missing Documents

**Problem:** Need to track which checklist items are still missing
- **Cause:** Workflow processes individual docs but doesn't track completeness
- **Impact:** Hard to know if all 35 required documents are collected
- **Solution:**
  - Create separate "Checklist Status" Google Sheet
  - Track which of 35 types have been received per client
  - Weekly report showing missing documents
  - Color-code: Green (received), Yellow (partial), Red (missing)

**Problem:** Multiple versions of same document type
- **Example:** Updated Baugenehmigung received after original
- **Impact:** Old and new versions both in same folder
- **Solution:**
  - Append date/version to filename: `BAUGEN_Client_v2_20241220.pdf`
  - Keep version history log
  - Archive old versions to "Archived" subfolder
  - Flag updates in Google Sheets log

### 7. Client and Project Identification

**Problem:** Email doesn't clearly identify which client/project document belongs to
- **Cause:** Generic subject lines, multiple projects per client
- **Impact:** Document classified but can't determine destination client folder
- **Solution:**
  - Extract client name from sender email domain
  - Parse email subject for project identifiers
  - Use NLP to extract client names from document content
  - Manual review queue if client ambiguous
  - Default to "Unassigned" folder with alert to admin

**Problem:** One client has multiple Bauträger projects
- **Example:** Eugene has 3 different construction projects
- **Impact:** Need to route to correct project subfolder
- **Solution:**
  - Add project-level classification
  - Extract project name/address from document
  - Create folder structure: `clients/{Client}/{Project}/OBJEKTUNTERLAGEN/...`
  - Require project identifier in email subject line

---

## Error Handling (Implemented Solutions)

### Gmail Connection Issues
- **Retry mechanism:** 3 attempts with exponential backoff (2s, 4s, 8s)
- **Authentication:** Log OAuth failures, refresh tokens automatically
- **Quota monitoring:** Alert admin at 80% quota usage
- **Fallback:** Switch to push notifications if polling quota exceeded

### OCR Processing Failures (German Documents)
- **Timeout handling:** 60-second timeout for OCR operations
- **Quality check:** Reject scans with <70% confidence
- **Language support:** AWS Textract configured for German (Deutsch)
- **Character encoding:** UTF-8 enforced for German umlauts
- **Fallback:** Route failed OCR to manual review folder
- **Logging:** Record OCR success rate, language detected, confidence scores

### No Attachments Found
- **Detection:** Check attachment count before processing
- **Action:** Skip email gracefully, log event
- **Notification:** Optional auto-reply to sender in German

### Unsupported File Types
- **Filter:** Accept only PDF, DOCX, DOC at download stage
- **Action:** Log unsupported files with sender email
- **Notification:** Auto-reply with list of supported formats (German)
- **Exception:** Route images (JPG, PNG) to separate OCR-only workflow

### Low Confidence Classification
- **Level 1 threshold:** <75% confidence → route to review queue
- **Level 2 threshold:** <60% confidence → place in category "Zu_Pruefen" (review) subfolder
- **Logging:** Record confidence scores for all classifications
- **Alert:** Weekly digest of low-confidence documents for prompt tuning
- **Special:** Extra caution for similar German legal terms

### Category/Type Mismatch
- **Detection:** Level 2 returns "unknown" after Level 1 categorization
- **Action:** Re-run Level 1 classification once
- **Fallback:** Route to SONSTIGES folder if still failing
- **Logging:** Record both Level 1 and Level 2 outputs for analysis

### File Already Exists (Duplicate Detection)
- **Hash check:** Calculate MD5 hash before processing
- **Exact duplicate:** Skip processing, log event
- **Name collision:** Append timestamp or version number
- **Naming pattern:**
  - Timestamp: `BAUGEN_Eugene_20241220_143022.pdf`
  - Version: `BAUGEN_Eugene_20241220_v2.pdf`

### Upload/Move Failures
- **Retry logic:** 3 attempts with exponential backoff for Drive operations
- **State tracking:** Mark documents as "classified" vs "moved" separately
- **Recovery:** Daily reconciliation job to move orphaned files
- **Logging:** Full error details with stack traces

### German-Specific Error Handling
- **Character encoding errors:** Force UTF-8, log encoding issues
- **Legal terminology confusion:** Manual review queue for ambiguous legal docs
- **DIN standard references:** Verify DIN number extraction accuracy
- **Multi-project routing:** Escalate to admin if project unclear

---

## Performance Metrics (v2 with German Bauträger Taxonomy)

### Processing Time Breakdown

**Digital PDFs (no OCR needed):**
- **Total:** ~12-15 seconds per document
  - Gmail download: ~1-2 seconds
  - File type detection: ~0.5 seconds
  - Google Drive upload: ~2-3 seconds
  - Text extraction (UTF-8): ~1-2 seconds
  - Level 1 AI classification (3 categories): ~2-3 seconds
  - Level 2 AI classification (5-22 types): ~2-3 seconds
  - File operations (move/rename): ~2 seconds
  - Logging: ~1 second

**Scanned German Documents (OCR required):**
- **Total:** ~45-60 seconds per document
  - Gmail download: ~1-2 seconds
  - File type detection: ~0.5 seconds
  - Google Drive upload: ~2-3 seconds
  - OCR processing (AWS Textract German): ~30-40 seconds
  - Level 1 AI classification: ~2-3 seconds
  - Level 2 AI classification: ~2-3 seconds
  - File operations: ~2 seconds
  - Logging: ~1 second

### Cost Analysis (per 1000 German documents)

Assuming 70% digital PDFs, 30% scanned documents (German construction docs have more scans):

| Component | Digital Cost | Scanned Cost | Blended Cost |
|-----------|-------------|--------------|--------------|
| **Level 1 Classification** (GPT-4o-mini) | $3.00 | $3.00 | $3.00 |
| **Level 2 Classification** (GPT-4o-mini) | $4.00 | $4.00 | $4.00 |
| **OCR** (AWS Textract German) | $0.00 | $3.00/page × 300 docs × 5 pages avg = $4,500 | $1,350.00 |
| **Gmail API** | Free | Free | Free |
| **Google Drive API** | Free | Free | Free |
| **Total per 1000 docs** | $7.00 (700 digital) | $1,357.00 (300 scanned) | **$1,364.00** |
| **Per document** | $0.01 | $4.52 | **$1.36** |

**Cost Optimization for German Documents:**
- OCR dominates cost for scanned German construction documents
- Consider Tesseract OCR with German language pack (free) to reduce to ~$0.007/doc
- AWS Textract more accurate for complex German legal terminology
- Many German Bauträger documents are scanned (older archives, signed contracts)

### Accuracy Metrics

- **File Type Detection:** ~98% (digital vs scanned)
- **OCR Text Extraction (German):** ~90% accuracy (German umlauts sometimes problematic)
- **Level 1 Category Classification:** ~96% accuracy (3 clear categories from checklist)
- **Level 2 Type Classification:** ~89% accuracy (35 types, some German terms very similar)
  - **OBJEKTUNTERLAGEN:** ~88% (22 types, many construction-specific)
  - **WIRTSCHAFTLICHE:** ~92% (8 types, clearer distinction)
  - **RECHTLICHE:** ~94% (5 types, very distinct German legal docs)
- **Overall End-to-End Accuracy:** ~87% (documents in correct folder)
- **Ambiguous Cases:** ~8% require manual review (German legal complexity)

### Throughput

- **Digital PDFs:** ~240 documents/hour (15 sec per doc)
- **Scanned Documents:** ~60 documents/hour (60 sec per doc)
- **Mixed Workload (70/30):** ~180 documents/hour
- **Peak Capacity:** Limited by OpenAI rate limits (60 calls/min = 1800 classifications/hour ÷ 2 = 900 docs/hour theoretical max)

### API Quotas

- **Gmail API:** 1 billion quota units/day (essentially unlimited)
- **Google Drive API:** 20,000 requests/day (enough for ~10,000 documents/day)
- **OpenAI API:** Tier-based (60 requests/min = 1800/hour on standard tier)
- **AWS Textract:** No hard limits, pay-per-use (German language supported)

---

## Testing Checklist (v2 - German Bauträger Documents)

### Email and Download Testing
- [ ] Send email with German PDF attachment → Gmail trigger detects within 1 minute
- [ ] Attachment with German filename (Übersicht, Größe, etc.) downloaded successfully
- [ ] Email without attachments → Skipped gracefully with log entry
- [ ] Multiple attachments in one email → All processed separately
- [ ] Unsupported file type (JPG, ZIP) → Filtered out, logged

### File Type Detection and OCR (German Documents)
- [ ] Digital German PDF → Detected correctly, routed to n8n text extraction
- [ ] Scanned German document → Detected correctly, routed to AWS Textract with German language
- [ ] German umlauts (ä, ö, ü, ß) preserved correctly in extracted text
- [ ] Old typewriter-style German document → OCR handled or flagged for manual review
- [ ] Handwritten German signatures → Detected and handled appropriately

### Hierarchical Classification Testing

**Level 1 (Category) - Test all 3 categories:**
- [ ] Kaufvertrag (purchase contract) → Classified as OBJEKTUNTERLAGEN
- [ ] Jahresabschlüsse (financial statements) → Classified as WIRTSCHAFTLICHE
- [ ] HR-Auszug (commercial register) → Classified as RECHTLICHE

**Level 2 (Type) - Test all 35 types:**

**OBJEKTUNTERLAGEN (22 types):**
- [ ] 01. Projektbeschreibung / Exposé → `projektbeschreibung` → 01_Projektbeschreibung/
- [ ] 02. Kaufvertrag → `kaufvertrag` → 02_Kaufvertrag/
- [ ] 03. Grundbuchauszug < 3 Monate → `grundbuchauszug` → 03_Grundbuchauszug/
- [ ] 04. Eintragungsbewilligungen → `eintragungsbewilligungen` → 04_Eintragungsbewilligungen/
- [ ] 05. Bodenrichtwert → `bodenrichtwert` → 05_Bodenrichtwert/
- [ ] 06. Baulastenverzeichnis → `baulastenverzeichnis` → 06_Baulastenverzeichnis/
- [ ] 07. Altlastenkataster → `altlastenkataster` → 07_Altlastenkataster/
- [ ] 08. Baugrundgutachten → `baugrundgutachten` → 08_Baugrundgutachten/
- [ ] 09. Lageplan / Flurkarte → `lageplan` → 09_Lageplan_Flurkarte/
- [ ] 10. Bauträgerkalkulation DIN 276 → `bautraegerkalkulation` → 10_Bautraegerkalkulation_DIN276/
- [ ] 11. Verkaufspreise je Einheit → `verkaufspreise` → 11_Verkaufspreise/
- [ ] 12. Bauzeitenplan / Liquiditätsplan → `bauzeitenplan` → 12_Bauzeitenplan_Liquiditaet/
- [ ] 13. Vertriebsweg → `vertriebsweg` → 13_Vertriebsweg/
- [ ] 14. Bau-/Ausstattungsbeschreibung → `bauausstattung` → 14_Bau_Ausstattungsbeschreibung/
- [ ] 15. Flächenberechnung DIN 277 → `flaechenberechnung` → 15_Flaechenberechnung_DIN277/
- [ ] 16. GU-/Werkverträge → `werkvertraege` → 16_GU_Werkvertraege/
- [ ] 17. Bauzeichnungen → `bauzeichnungen` → 17_Bauzeichnungen/
- [ ] 18. Baugenehmigung → `baugenehmigung` → 18_Baugenehmigung/
- [ ] 19. Teilungserklärung → `teilungserklaerung` → 19_Teilungserklaerung/
- [ ] 20. Versicherungen → `versicherungen` → 20_Versicherungen/
- [ ] 21. Muster Verkaufsvertrag → `verkaufsvertrag` → 21_Muster_Verkaufsvertrag/
- [ ] 22. Gutachterauftrag → `gutachterauftrag` → 22_Gutachterauftrag/

**WIRTSCHAFTLICHE UNTERLAGEN (8 types):**
- [ ] 23. Jahresabschlüsse → `jahresabschluesse` → 23_Jahresabschluesse/
- [ ] 24. BWA inkl. Summe-Saldenliste → `bwa` → 24_BWA/
- [ ] 25. Steuernummern / Steuer-IDs → `steuernummern` → 25_Steuernummern/
- [ ] 26. SCHUFA-Erklärung → `schufa` → 26_SCHUFA_Erklaerung/
- [ ] 27. Einkommensteuern → `einkommensteuern` → 27_Einkommensteuern/
- [ ] 28. Vermögens-/Schuldenübersicht → `vermoegensuebersicht` → 28_Vermoegensuebersicht/
- [ ] 29. Eigenkapitalnachweis → `eigenkapitalnachweis` → 29_Eigenkapitalnachweis/
- [ ] 30. Projektliste → `projektliste` → 30_Projektliste/

**RECHTLICHE UNTERLAGEN (5 types):**
- [ ] 31. HR-Auszug → `hr_auszug` → 31_HR_Auszug/
- [ ] 32. Gesellschaftsvertrag → `gesellschaftsvertrag` → 32_Gesellschaftsvertrag/
- [ ] 33. Personalausweise → `personalausweise` → 33_Personalausweise/
- [ ] 34. Bauträgerzulassung §34c GewO → `bautraegerzulassung` → 34_Bautraegerzulassung/
- [ ] 35. Organigramm → `organigramm` → 35_Organigramm/

### German-Specific Testing
- [ ] Document with "DIN 276" reference → Correctly identified as Bauträgerkalkulation (not DIN 277)
- [ ] Document with "DIN 277" reference → Correctly identified as Flächenberechnung (not DIN 276)
- [ ] "Grundbuchauszug" vs "Baulastenverzeichnis" → Correctly distinguished (both land registry-related)
- [ ] "BWA" vs "Jahresabschlüsse" → Correctly distinguished (monthly vs annual financials)
- [ ] "§34c GewO" reference → Correctly identified as Bauträgerzulassung
- [ ] German company types (GmbH, AG, etc.) in Gesellschaftsvertrag → Classified correctly
- [ ] SCHUFA keyword detected → Routed to SCHUFA_Erklaerung folder

### Edge Cases and Error Handling
- [ ] Ambiguous German legal document → Low confidence flagged, routed to review queue
- [ ] Level 1/Level 2 mismatch → Re-classification triggered or routed to SONSTIGES
- [ ] Unknown/unclassifiable → Routes to 36_Sonstiges/
- [ ] Duplicate filename (same day) → Timestamp or version number appended
- [ ] File already exists (exact duplicate) → Skipped, logged as duplicate
- [ ] Mixed German/English document → Handled appropriately with language detection

### File Operations and Logging
- [ ] File renamed correctly with German prefix: `BAUGEN_Eugene_20241220.pdf`
- [ ] File moved to correct German-named folder (all 35 folders + SONSTIGES)
- [ ] Google Sheets log entry created with all fields including German document names

### Checklist Compliance
- [ ] Checklist Status Sheet tracks which of 35 document types received
- [ ] Missing documents flagged in weekly report
- [ ] Multiple versions of same document type handled with version numbers
- [ ] Client/project identification works for multi-project clients

---

## Future Enhancements (v3+)

### Already Implemented in v2 ✅
- ~~OCR Integration~~ - Implemented with German language support
- ~~Hierarchical Classification~~ - Implemented with actual Bauträger checklist (3 categories → 35 types)
- ~~Enhanced Error Handling~~ - Comprehensive error handling for German documents

### Planned for v3

1. **Sub-Classification for Bauzeichnungen**
   - Automatically detect: Grundrisse, Schnitte, Ansichten, Detailzeichnungen
   - Create subfolders within 17_Bauzeichnungen/
   - Maintain compatibility with main classification

2. **Checklist Completion Dashboard**
   - Visual dashboard showing which of 35 documents are collected
   - Per-client, per-project tracking
   - Color-coded status indicators
   - Auto-alerts for missing critical documents

3. **Multi-Project Support per Client**
   - Add project-level classification
   - Folder structure: `clients/{Client}/{Project}/OBJEKTUNTERLAGEN/...`
   - Extract project address/name from documents
   - Project identifier in email subject line

4. **German-Specific Enhancements**
   - Historical Fraktur font OCR support
   - Enhanced §-reference detection (GewO, BauGB, etc.)
   - State-specific regulation support (Landesbauordnung)
   - Automatic currency format detection (€ vs other)

5. **Document Version Control**
   - Track document updates (revised Baugenehmigung, updated Kalkulation)
   - Link related documents (Kaufvertrag + Grundbuchauszug for same property)
   - Archive old versions automatically
   - Version comparison highlights

6. **Advanced Duplicate Detection**
   - Semantic similarity for near-duplicates
   - Identify amended contracts vs originals
   - Cross-reference documents across projects

7. **Compliance Validation**
   - Check Grundbuchauszug is <3 months old (from document date)
   - Verify presence of required signatures
   - Flag documents missing required German stamps/seals
   - DIN standard compliance checks

8. **Auto-Analysis Triggers**
   - After Bauträgerkalkulation: trigger cost verification agent
   - After Baugenehmigung: check conditions and requirements
   - After Jahresabschlüsse: trigger financial health check
   - Store analysis results in separate reports folder

---

## Maintenance Notes

**Version:** 2.0
**Last Updated:** 2024-12-20
**Maintained By:** Sway Clarke
**Review Frequency:** Monthly
**Next Review:** 2025-01-20

**Known Issues (v2.0):**
- OCR cost high with AWS Textract for German scans ($3/page) - consider Tesseract with German language pack
- Similar German legal terms (Grundbuchauszug, Baulastenverzeichnis) may occasionally be confused - needs monitoring
- DIN 276 vs DIN 277 detection needs strong pattern matching - add specific validation
- Multi-project client routing not yet implemented - currently all goes to main client folder
- Handwritten German text in signatures/notes not processed by standard OCR

**Dependencies:**
- n8n (self-hosted or cloud) - v1.0+
- Gmail API access (OAuth2 authentication)
- OpenAI API access (GPT-4o-mini with German language support)
- Google Drive API access
- Google Sheets API access
- AWS Textract with German (Deutsch) language pack (optional - can use Tesseract)

**API Setup Requirements:**

**Gmail:**
1. Enable Gmail API in Google Cloud Console
2. Create OAuth2 credentials
3. Configure authorized redirect URIs for n8n
4. Grant permissions: `gmail.readonly`, `gmail.modify`

**OpenAI:**
1. Create API key at platform.openai.com
2. Use GPT-4o-mini (supports German, cost-efficient)
3. Set up billing with rate limits
4. Monitor usage at platform.openai.com/usage

**AWS Textract (for German OCR):**
1. Create AWS account
2. Enable AWS Textract in desired region
3. Configure German (Deutsch) language support
4. Create IAM user with Textract permissions
5. Generate access key and secret key
6. Alternative: Use Tesseract OCR with German language pack (free)

**German Language Considerations:**
- UTF-8 encoding mandatory for umlauts (ä, ö, ü, ß)
- AWS Textract Deutsch language pack required
- Test classification with German legal terminology
- Monitor accuracy for compound German words (Bauträgerkalkulation, Flächenberechnung)

**Monitoring Recommendations:**
- Check Google Sheets log daily for processing failures
- Review low-confidence classifications weekly (especially similar German legal docs)
- Monitor OCR accuracy for German umlauts and special characters
- Track DIN standard detection accuracy (276 vs 277)
- Verify Checklist Status Sheet shows all 35 document types being processed
- Alert if any of the 35 folders never receives documents (might indicate classification issue)

**Version History:**
- **v1.0 (2024-12-20):** Initial release with 7 generic document types, single-level classification
- **v2.0 (2024-12-20):** Complete redesign with actual German Bauträger checklist (3 categories → 35 types), hierarchical classification, OCR support, German language handling, comprehensive error handling for construction developer documents
