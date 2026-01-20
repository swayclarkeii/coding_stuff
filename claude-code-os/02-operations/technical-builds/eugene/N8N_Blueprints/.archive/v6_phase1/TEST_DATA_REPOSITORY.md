# Test Data Repository - Document Organizer V4

**Location:** Google Drive folder `dummy_files`
**Folder ID:** `1GG_OCKvT1ivR0F-uIVq0b1jhHreWg1Kh`
**Link:** https://drive.google.com/drive/folders/1GG_OCKvT1ivR0F-uIVq0b1jhHreWg1Kh

---

## Overview

This repository contains real client documents from two active projects, organized for testing the Document Organizer V4 autonomous system. These documents provide comprehensive coverage of German real estate development documentation types.

---

## Client Folders

### 1. Adolf-Martens-Straße (ADM10)
**Folder ID:** `18i4O8VhBUczeXXW13pucX3DxpPtIMIkf`
**Client Normalized Name:** `adolf_martens_strasse`

#### Available Documents

| File Name | Type | File ID | Use For Testing |
|-----------|------|---------|-----------------|
| ADM10_Exposé.pdf | Exposé/Project Description | 1SaAnbMGcyZgLkmYC4KZJyI9gN26N_l7L | ✅ Chunk 2, 2.5, 3 |
| Baubeschreibung Regelgeschoss.pdf | Building Description | 1gr8b69ZbRtyB1JB4xk9qlH_cNV7hzZm4 | ✅ Chunk 2, 2.5 |
| Baubeschreibung_Dachgeschoss.pdf | Building Description (Roof) | 1XhkQZEZk5ADByLXfye69wg8Y1olHP3aV | ✅ Chunk 2, 2.5 |
| OCP-Anfrage-AM10.pdf | OCP Request | 1dv68IRJGNsdXNbcU7Le1GoCsJnI3pmvx | ⚠️ Edge case testing |
| 250916 ADM10 - Budget.xlsm | Budget Excel | 1T_SDDMvxzGI2yxP2N5bcgBHrwQn9mB3v | ❌ Not PDF (skip) |

**Characteristics:**
- ✅ Well-structured project documentation
- ✅ Clean digital PDFs (no OCR needed)
- ✅ Standard German real estate documents
- ⚠️ Missing key documents (Kaufvertrag, Grundbuchauszug)
- 📁 Contains subfolder `Datenraum_ADM10` for deeper document hierarchy testing

---

### 2. Propos-Menrad
**Folder ID:** `1-jO4unjKgedFqVqtofR4QEM18xC09Fsk`
**Client Normalized Name:** `propos_menrad`

#### Available Documents

| File Name | Type | File ID | Use For Testing |
|-----------|------|---------|-----------------|
| 251103_Kalkulation Schlossberg.pdf | Cost Calculation (DIN276) | 1BRz-SaE8gSW1BqeLOh4e4tsg9iG94xvC | ✅ Chunk 2, 2.5, 3 |
| 251103_Kaufpreise Schlossberg.pdf | Sales Prices | 1km2a6MU7mLI9NfeJQGvGujKkEEnI8G5B | ✅ Chunk 2, 2.5, 3 |
| Baugrund_und_Gründungsgutachten.pdf | Building Ground Assessment | 1xx0rJEk5h1vAx757rcNPZainf_kYvfyi | ✅ Chunk 2, 2.5, 3 |
| Bebauungsplan.pdf | Development Plan (Zoning) | 1rFEyF1FYJdCDVmt4gd41str-fEsyAyeJ | ✅ Chunk 2, 2.5 |
| Bodenschutz-u.Altlastenkataster.pdf | Contamination Register | 1c8ttlunVUconQP5ZXsXSaF2dnFZWm6Mz | ✅ Chunk 2, 2.5 |
| Baulasten und Denkmalschutz.pdf | Building Charges/Monument Protection | 188pg_qflwJdriuTUMWvV8Rwn10e2fgao | ✅ Chunk 2, 2.5 |
| 20251015_Bauvorbescheid.pdf | Preliminary Building Permit | 1ZeM7xdFh6M-c-ODSV0AKtqpWhH6sFooD | ✅ Chunk 2, 2.5, 3 (⚠️ may be scanned) |
| 251104_Übersicht Banken Finanzierungen PROPOS-Gruppe.pdf | Bank Financing Overview | 1Afaa_ovQg2uCe92TTjlox5lsxX1Ht6FM | ✅ Chunk 2, 2.5, 3 |
| 250616_Schloßberg_funktionale Leistungsbeschreibung.pdf | Functional Performance Description | 115BW-LoSvTd0P9ioJlR8WaRSnxhZKZ81 | ✅ Chunk 2, 2.5 |
| 250623_Abstandsflächen.pdf | Distance Areas/Spacing | 1Ekk9cWfC8t3tnOCvj2sYnOfH1GSKLqjo | ⚠️ Edge case testing |
| 250814_Schloßberg 13.pdf | Project Plan | 1v5zR3dogaBik0vxrWndq-COxg1q6I82M | ✅ Chunk 2, 2.5 |
| 251030_Schlossberg_Verkaufsbaubeschreibung_Entwurf.pdf | Sales Building Description (Draft) | 1uxFzjVzizeoVPJTD-VPchC9DYVMnM7nL | ✅ Chunk 2, 2.5 |
| AN25700_GU_Werkvertraege_Richtpreisangebot 09_25[54].pdf | General Contractor Work Contracts | 1pfOKcBMuxolYvC0G5f1sGdg2RnSJ3C8e | ✅ Chunk 2, 2.5 |
| Warburg_Angebot Schlossberg Tübingen.pdf | Warburg Offer | 1ttQgfskI9atUcItJOi-O_hZdsPXb1Zkv | ✅ Chunk 2, 2.5, 3 |
| 251115_Kalkulation Schlossberg KSK Martin.xlsx | Calculation Excel | 1WXzzCmIXO7TAwHe5FxkUwMnoDKo7Jq7n | ❌ Not PDF (skip) |
| Propos Fragen.docx | Questions Document | 1rzGD6n-ujdIZSc71E1jOfm4xA1clzeuh | ❌ Not PDF (skip) |

**Characteristics:**
- ✅ Comprehensive document set (15+ PDFs)
- ✅ Covers multiple document categories
- ✅ Real-world complexity and naming variations
- ⚠️ Some documents may be scanned (OCR testing)
- ⚠️ Missing core legal documents (Kaufvertrag, Grundbuchauszug)
- 📁 Contains subfolder `251203_Calluna` for hierarchical testing

---

## Test Cases Coverage

The `test_cases.json` file defines **10 comprehensive test cases** covering:

### Document Type Coverage (Chunk 2 Testing)
- ✅ **01_PROJEKTBESCHREIBUNG** - Exposé (ADM10)
- ✅ **06_BAULASTENVERZEICHNIS** - Building charges (Propos)
- ✅ **07_ALTLASTENKATASTER** - Contamination register (Propos)
- ✅ **08_BAUGRUNDGUTACHTEN** - Ground assessment (Propos)
- ✅ **09_LAGEPLAN** - Development plan (Propos)
- ✅ **10_BAUTRAEGERKALKULATION_DIN276** - Cost calculation (Propos)
- ✅ **11_VERKAUFSPREISE** - Sales prices (Propos)
- ✅ **14_BAU_AUSSTATTUNGSBESCHREIBUNG** - Building description (ADM10)
- ✅ **18_BAUGENEHMIGUNG** - Building permit (Propos)
- ✅ **26_FINANZIERUNGSBESTAETIGUNG** - Financing confirmation (Propos)

### Validation Testing (Chunk 2.5)
- ✅ Complete document sets vs incomplete sets
- ✅ Missing critical documents detection
- ✅ Missing supporting documents detection

### Deal Scoring (Chunk 3)
- ✅ High-quality deals (score >= 7.5)
- ✅ Review-required deals (score 4.0-7.0)
- ✅ Documents with financing lined up
- ✅ Documents missing critical legal foundation

---

## Document Categories Not Covered

**Missing for Complete Testing:**
- ❌ **02_KAUFVERTRAG** (Purchase Contract) - Critical legal document
- ❌ **03_GRUNDBUCHAUSZUG** (Land Registry Extract) - Critical ownership document
- ❌ **04_EINTRAGUNGSBEWILLIGUNGEN** (Entry Approvals)
- ❌ **05_BODENRICHTWERT** (Land Value Assessment)
- ❌ **12_BAUZEITENPLAN_LIQUIDITAET** (Construction Schedule/Liquidity)
- ❌ **13_VERTRIEBSWEG** (Sales Channel)
- ❌ **15_FLAECHENBERECHNUNG_DIN277** (Area Calculation DIN277)
- ❌ **17_BAUZEICHNUNGEN** (Construction Drawings)
- ❌ **19_TEILUNGSERKLAERUNG** (Condominium Declaration)
- ❌ **20_VERSICHERUNGEN** (Insurances)
- ❌ **21_MUSTER_VERKAUFSVERTRAG** (Sample Sales Contract)
- ❌ **22_GUTACHTERAUFTRAG** (Expert Appraisal Order)
- ❌ **23_UMSATZSTEUERVORANMELDUNG** (VAT Advance Return)
- ❌ **24_BWA** (Business Evaluation)
- ❌ **25_JAHRESABSCHLUSS** (Annual Financial Statement)
- ❌ **27_DARLEHENSVERTRAG** (Loan Agreement)
- ❌ **28_GESELLSCHAFTSVERTRAG** (Partnership Agreement)
- ❌ **29_HANDELSREGISTERAUSZUG** (Commercial Register Extract)
- ❌ **30_GEWERBEANMELDUNG** (Business Registration)
- ❌ **31_STEUER_ID** (Tax ID)
- ❌ **32_FREISTELLUNGSBESCHEINIGUNG** (Exemption Certificate)
- ❌ **33_VOLLMACHTEN** (Powers of Attorney)
- ❌ **34_KORRESPONDENZ** (Correspondence)
- ❌ **35_SONSTIGES_ALLGEMEIN** (Miscellaneous General)
- ❌ **36_EXIT_STRATEGIE** (Exit Strategy)
- ❌ **37_OTHERS** (Others)
- ❌ **38_UNKNOWNS** (Unknowns)

**Impact:** Current test coverage is ~26% of all document types (10/38). This is sufficient for initial testing but should be expanded for production validation.

---

## Using Test Cases

### Layer 1 Testing (Simulated)
Use `test_runner_agent` with simulated input:

```json
{
  "file_id": "1SaAnbMGcyZgLkmYC4KZJyI9gN26N_l7L",
  "file_name": "ADM10_Exposé.pdf",
  "client_normalized": "adolf_martens_strasse"
}
```

**Validate against:** `test_cases.json` → `chunk_2_expected`, `chunk_2_5_expected`, `chunk_3_expected`

---

### Layer 2 Testing (Real Gmail Trigger)
Call Email Sender webhook:

```bash
curl -X POST https://n8n.oloxa.ai/webhook/ama-send-test-email \
  -H "Content-Type: application/json" \
  -d '{
    "test_case_id": "TC_CHUNK2_EXPOSE_ADM10",
    "pdf_file_id": "1SaAnbMGcyZgLkmYC4KZJyI9gN26N_l7L",
    "pdf_file_name": "ADM10_Exposé.pdf",
    "target_chunk": "2"
  }'
```

**System will:**
1. Download PDF from Drive
2. Send email with attachment to Pre-Chunk 0 trigger
3. Wait 15 seconds for workflow execution
4. Query n8n API for execution result
5. Validate chunk output against expected values
6. Log results to `Layer_2_Tests` sheet

---

## Validation Rules

### Chunk 2 (Document Classification)
- **Required fields:** `documentType`, `confidence`, `extractionMethod`
- **Confidence threshold:** >= 0.9 (high quality)
- **Valid document types:** 38 categories (see `valid_document_types` in test_cases.json)

### Chunk 2.5 (Completeness Validation)
- **Required fields:** `validation_result`, `missing_docs`
- **Valid results:** `complete`, `incomplete`, `critical_missing`
- **Critical documents:** Kaufvertrag, Grundbuchauszug, Baugenehmigung

### Chunk 3 (Deal Scoring)
- **Required fields:** `deal_score`, `pass_fail`
- **Score range:** 0-10
- **Thresholds:**
  - PASS: >= 7.0
  - REVIEW: 4.0-6.9
  - FAIL: < 4.0

---

## Edge Cases Covered

1. **Ambiguous Document Types**
   - Baubeschreibung vs Ausstattungsbeschreibung (ADM10)
   - Bebauungsplan vs Lageplan (Propos)

2. **Potentially Scanned Documents**
   - `20251015_Bauvorbescheid.pdf` (Propos) - Test OCR path

3. **Document Naming Variations**
   - Date prefixes: `251103_`, `250616_`, `20251015_`
   - Project suffixes: `Schlossberg`, `ADM10`, `PROPOS-Gruppe`

4. **Incomplete Document Sets**
   - Both clients missing critical legal documents
   - Tests validation and deal scoring with partial information

5. **Multi-category Documents**
   - `Verkaufsbaubeschreibung` (Sales + Building description)
   - `Funktionale Leistungsbeschreibung` (Functional performance spec)

---

## Test Execution Workflow

### Automated Testing via Test Orchestrator
1. **Schedule Trigger** runs every 1 hour
2. **Load Status** from `Chunk_Status` sheet
3. **Determine Next Chunk** to build (2.5, 3, 4, 5)
4. **Build Chunk** using agent orchestration
5. **Layer 1 Test** with simulated data from test_cases.json
6. **Layer 2 Test** with real email via Email Sender
7. **Validate Results** against expected outputs
8. **Create Backup** if all tests pass
9. **Update Status Tracker** with results

### Manual Testing
1. Select test case from `test_cases.json`
2. Use `test_case_id` for tracking
3. Run Layer 1 (simulated) via test-runner-agent
4. Run Layer 2 (real email) via Email Sender webhook
5. Compare actual vs expected outputs
6. Document failures in Status Tracker

---

## Expanding Test Coverage

### To Add More Test Cases:

1. **Identify missing document type** from list above
2. **Find or create sample document** (ask Sway or generate)
3. **Add to dummy_files folder** (either client folder)
4. **Update test_cases.json** with new test case:
   ```json
   {
     "test_case_id": "TC_CHUNK2_KAUFVERTRAG_ADM10",
     "description": "Test Chunk 2 with purchase contract",
     "client": "adolf_martens_strasse",
     "file_id": "DRIVE_FILE_ID",
     "file_name": "Kaufvertrag.pdf",
     "document_type_expected": "KAUFVERTRAG",
     "chunk_2_expected": { ... },
     "chunk_2_5_expected": { ... },
     "chunk_3_expected": { ... }
   }
   ```
5. **Run test** via Test Orchestrator or manually
6. **Update validation rules** if needed

### Priority Documents to Add:
1. **02_KAUFVERTRAG** (Purchase Contract) - Highest priority
2. **03_GRUNDBUCHAUSZUG** (Land Registry) - Highest priority
3. **18_BAUGENEHMIGUNG** (Building Permit) - High priority
4. **27_DARLEHENSVERTRAG** (Loan Agreement) - High priority
5. **17_BAUZEICHNUNGEN** (Construction Drawings) - Medium priority

---

## Notes

- ✅ Test data is **real client data** - handle with care
- ✅ **Both client folders** are available for testing
- ✅ Coverage is **26% of document types** - sufficient for MVP
- ⚠️ **Missing critical documents** limits completeness testing
- ⚠️ Some documents may be **German-specific** legal terms
- 📊 **10 test cases** provide good baseline for initial autonomous testing

---

## Related Files

- **test_cases.json** - Test case definitions and expected outputs
- **AUTONOMOUS_TESTING_SYSTEM_V2.md** - Full testing system design
- **Status Tracker Sheet** - `1af9ZsSm5IDVWIYb5IMX8ys8a5SUUnQcb77xi9tJQVo8`
- **Email Sender Workflow** - `8l1ZxZMZvoWISSkJ`
- **Test Orchestrator Workflow** - `nUgGCv8d073VBuP0`

---

**Last Updated:** 2026-01-08
**Version:** 1.0
**Status:** ✅ Ready for Testing
