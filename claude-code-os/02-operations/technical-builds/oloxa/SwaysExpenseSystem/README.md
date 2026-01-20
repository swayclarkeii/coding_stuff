# Sway's Expense System

**Project**: Automated Expense Management System
**Status**: v1.2.0 - Gmail Receipt Monitor
**Owner**: Sway Clarke
**Created**: December 30, 2025

---

## 📋 Overview

This system automates monthly expense processing for 4 financial institutions (ING Bank, Deutsche Bank, Barclay Credit Card, Miles & More Credit Card), reducing manual work from **5-6 hours/month to 25-30 minutes/month**.

### Goals
- ✅ Auto-match bank/credit card transactions to receipts
- ✅ Organize files into structured Google Drive folders
- ✅ Extract transactions from German PDF statements using AI
- ✅ Monitor Gmail for receipt emails
- ✅ Handle edge cases (small expenses, annual invoices, unmatched alerts)

---

## 📁 Project Structure

```
SwaysExpenseSystem/
│
├── README.md                       ← You are here
│
├── workflows/                      ← Workflow documentation & diagrams
│   └── _archive/                   ← Deprecated workflow versions
│
├── N8N_Blueprints/                 ← n8n workflow JSON exports
│   ├── v1_foundation/              ← Current version (v1.0.0)
│   │   ├── VERSION_LOG.md          ← Version history & rollback guide
│   │   └── SYSTEM_DESIGN.md        ← Complete system specification
│   └── _archive/                   ← Historical versions
│
└── _archive/                       ← General project archives
```

---

## 🗂️ External Resources

### Google Drive Structure
**Root Folder**: Expenses-System
- **ID**: `1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15`
- **URL**: https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15

**Structure** (96+ folders):
```
📁 Expenses-System/
├── 📁 _Inbox/               ← Manual statement uploads
├── 📁 _Receipt-Pool/        ← Downloaded receipts before matching
├── 📁 _Unmatched/           ← Transactions without receipts
├── 📁 _Archive/             ← Historical statements
├── 📁 Income/               ← GEMA statements, invoices
├── 📁 _Reports/             ← Generated monthly summaries
├── 📁 2025/                 ← Monthly folders (all 12 months)
│   ├── 📁 01-January/
│   │   ├── 📁 ING/
│   │   │   ├── 📁 Statements/
│   │   │   └── 📁 Receipts/
│   │   ├── 📁 Deutsche-Bank/
│   │   ├── 📁 Barclay/
│   │   └── 📁 Miles-More/
│   └── ... (all months)
└── 📄 Expense-Database.gsheet
```

### Transaction Database
**Spreadsheet**: Expense-Database
- **ID**: `1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM`
- **URL**: https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM/edit

**Sheets**:
1. **Transactions** (16 columns) - All bank/credit card transactions
2. **Statements** (8 columns) - Processed statement metadata
3. **Receipts** (10 columns) - Downloaded receipt metadata
4. **VendorMappings** (4 columns) - Regex patterns for vendor matching

---

## 📚 Documentation

### Core Documents
1. **System Design** (850+ lines)
   - Location: [N8N_Blueprints/v1_foundation/SYSTEM_DESIGN.md](N8N_Blueprints/v1_foundation/SYSTEM_DESIGN.md)
   - Contains: Complete specifications, workflows, edge cases, vendor patterns

2. **Version Log** (living document)
   - Location: [N8N_Blueprints/v1_foundation/VERSION_LOG.md](N8N_Blueprints/v1_foundation/VERSION_LOG.md)
   - Contains: Version history, rollback procedures, archiving procedures, efficiency scoring

3. **Vendor Receipt Analysis** (new)
   - Location: [N8N_Blueprints/v1_foundation/VENDOR_RECEIPT_ANALYSIS.md](N8N_Blueprints/v1_foundation/VENDOR_RECEIPT_ANALYSIS.md)
   - Contains: Multi-account Gmail strategy, vendor categorization, discovery process

4. **Testing Preparation Guide** (new)
   - Location: [N8N_Blueprints/v1_foundation/TESTING_PREPARATION.md](N8N_Blueprints/v1_foundation/TESTING_PREPARATION.md)
   - Contains: Pre-testing checklist, test data requirements, success criteria, troubleshooting

5. **Environment Setup Guide** (new)
   - Location: [N8N_Blueprints/v1_foundation/ENVIRONMENT_SETUP.md](N8N_Blueprints/v1_foundation/ENVIRONMENT_SETUP.md)
   - Contains: Step-by-step environment variable configuration, API credential setup

---

## 🔄 Workflows

### Phase 1: Foundation (v1.0.0) ✅ Complete
- [x] Google Drive folder structure (96+ folders)
- [x] Transaction Database with 4 sheets
- [x] System design documentation
- [x] Project organization structure

### Phase 2: Core Automation (v1.1.0 - v1.4.0) ⏳ In Progress
- [x] **Workflow 1**: PDF Intake & Parsing (v1.1.0) ✅
  - Monitor `_Inbox/Bank-Statements/`
  - Parse German PDFs with OpenAI Vision API
  - Extract transactions to database
  - Move to Archive
  - **Status**: Built (Workflow ID: `BggZuzOVZ7s87psQ`)

- [x] **Workflow 2**: Gmail Receipt Monitor (v1.2.0) ✅
  - Search Gmail for receipt emails
  - Download attachments based on vendor patterns
  - Store in `_Receipt-Pool/`
  - Log in Receipts sheet
  - **Status**: Built (Workflow ID: `2CA0zQTsdHA8bZKF`)

- [ ] **Workflow 3**: Transaction-Receipt Matching (v1.3.0)
  - Match transactions to receipts (date ±3 days, amount exact/±€0.50)
  - Confidence scoring (0.0-1.0)
  - Update database with matches
  - Move receipts to organized folders

- [ ] **Workflow 4**: File Organization (v1.4.0)
  - Sort receipts from pool to monthly folders
  - Handle unmatched transactions
  - Archive old statements

### Phase 3: Full Integration (v2.0.0+) 📋 Planned
- [ ] Edge case handling (small expenses, annual invoices, GEMA reminders)
- [ ] Expensify integration
- [ ] Weekly digest reports
- [ ] Monthly summary generation

---

## 🎯 Current Status

**Version**: v1.2.0 (Gmail Receipt Monitor)
**Efficiency Score**: 4.0/10
**Target Score**: 7.0/10 for MVP (v2.0.0)

### What Works ✅
- Complete Google Drive infrastructure (96+ folders)
- Transaction Database with proper schema and populated VendorMappings
- **Workflow 1**: PDF statement parsing with OpenAI Vision (8 nodes)
- **Workflow 2**: Automated Gmail receipt monitoring (9 nodes)
- Comprehensive system design approved
- Organized project structure in technical-builds
- Daily automated receipt downloads from 6 vendors
- Bank statement transaction extraction

### What's Missing ❌
- File organization automation (Workflow 4) - not built yet
- Testing with real data (all 3 workflows untested)
- Multi-account Gmail support (v1.2.1) - planned but not implemented
- Vendor discovery audit (need to identify all vendors beyond current 7)

### Blockers 🔴
- **Required for Workflow 1**: OpenAI API key and credits ($5+ recommended)
- **Required for Workflow 2**: Gmail OAuth2 credentials configured
- **Required for Testing**: Sample German bank statement PDF
- **Multi-Account**: Need Gmail account addresses to configure additional monitoring
- **Vendor Discovery**: Need results from vendor audit (see [VENDOR_RECEIPT_ANALYSIS.md](N8N_Blueprints/v1_foundation/VENDOR_RECEIPT_ANALYSIS.md))

---

## 🚀 Quick Start

### For Configuration (Do This First!)
1. **Folder IDs (Already Configured!)**:
   - ✅ Workflow 1 monitors: `_Inbox/Bank-Statements/` (ID: `1stmB5nWmoViQKKuQqpkWICPrfPQ_GDN1`)
   - ✅ Workflow 1 archives to: `_Archive/Statements/` (ID: `1uohhbtaE6qvS08awMEYdVP6BqgRLxgjH`)
   - ✅ Workflow 2 stores to: `_Receipt-Pool/` (ID: `12SVQzuWtKva48LvdGbszg3UcKl7iy-1x`)
   - **Note**: Folder IDs are hardcoded in workflows (free n8n doesn't support environment variables)
2. **Configure API credentials**:
   - OpenAI API key (for PDF parsing) - see [ENVIRONMENT_SETUP.md](N8N_Blueprints/v1_foundation/ENVIRONMENT_SETUP.md)
   - Gmail OAuth2 (for receipt monitoring)
   - Verify Google Drive/Sheets credentials
3. **Ready to test!** All folder configuration is complete

### For Testing (After Configuration)
1. **Review testing guide**: [TESTING_PREPARATION.md](N8N_Blueprints/v1_foundation/TESTING_PREPARATION.md)
2. **Complete vendor audit**: Follow [VENDOR_RECEIPT_ANALYSIS.md](N8N_Blueprints/v1_foundation/VENDOR_RECEIPT_ANALYSIS.md)
3. **Start with Workflow 2** (Gmail Receipt Monitor) - lowest risk, fastest validation
4. **Progress to Workflow 3** (Transaction Matching) - uses data from Workflow 2
5. **Test Workflow 1 last** (PDF Parser) - requires OpenAI API credits

### For Developers
1. Review system design: [SYSTEM_DESIGN.md](N8N_Blueprints/v1_foundation/SYSTEM_DESIGN.md)
2. Check version log: [VERSION_LOG.md](N8N_Blueprints/v1_foundation/VERSION_LOG.md)
3. Access Google Drive: https://drive.google.com/drive/folders/1fgJLso3FuZxX6JjUtN_PHsrIc-VCyl15
4. Access Database: https://docs.google.com/spreadsheets/d/1l1uA8qA0DCGzGLBhmP2HqTzaajjbkURY2SLeqSuHMXM/edit
5. Access n8n: https://n8n.oloxa.ai

### For End Users (After Testing)
1. Upload bank statements to: `Expenses-System/_Inbox/Bank-Statements/`
2. System automatically processes and organizes
3. Review matched transactions in monthly folders
4. Check unmatched transactions in: `Expenses-System/_Unmatched/`

---

## 📊 Financial Institutions Supported

| Institution | Type | Folder Name | Status |
|-------------|------|-------------|--------|
| ING Bank | Checking | `ING/` | ✅ Ready |
| Deutsche Bank | Checking | `Deutsche-Bank/` | ✅ Ready |
| Barclay | Credit Card | `Barclay/` | ✅ Ready |
| Miles & More | Credit Card | `Miles-More/` | ✅ Ready |

---

## 🔐 Security & Privacy

- All expense data stored in personal Google Drive (not shared)
- n8n workflows run on private instance: https://n8n.oloxa.ai
- OpenAI API used only for PDF text extraction (no data retention)
- Gmail API has read-only access to receipt emails
- No third-party services have write access to files

---

## 📞 Support & Maintenance

### Version Control
- Version history: [N8N_Blueprints/v1_foundation/VERSION_LOG.md](N8N_Blueprints/v1_foundation/VERSION_LOG.md)
- Rollback procedures documented in version log
- n8n workflow JSONs exported for each version

### Troubleshooting
1. Check version log for known issues
2. Review rollback procedures if system is unstable
3. Consult system design doc for specifications
4. Verify all component IDs match version manifest

---

## 🎓 Learning Resources

- **System Design**: [SYSTEM_DESIGN.md](N8N_Blueprints/v1_foundation/SYSTEM_DESIGN.md)
- **Version History**: [VERSION_LOG.md](N8N_Blueprints/v1_foundation/VERSION_LOG.md)
- **n8n Documentation**: https://docs.n8n.io
- **Google Drive API**: https://developers.google.com/drive
- **Gmail API**: https://developers.google.com/gmail/api

---

**Last Updated**: December 30, 2025
**Maintained By**: Sway Clarke
**License**: Private/Personal Use
