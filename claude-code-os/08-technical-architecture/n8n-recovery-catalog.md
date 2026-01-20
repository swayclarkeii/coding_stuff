# N8N Workflow Recovery Catalog
**Date**: December 31, 2025
**Reason**: Complete data loss during Docker uninstallation
**Source**: Local JSON blueprint files

---

## LATEST WORKFLOWS TO REBUILD

### Eugene Project (5 workflows)

####1. Pre-Chunk 0: Client Intake & PDF Processing
- **Version**: v1.0
- **Blueprint**: `V4_PreChunk0_Intake_v1.json`
- **Location**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/N8N_Blueprints/v4_phase1/V4_PreChunk0_Intake_v1.json`
- **Old Workflow ID**: `koJAMDJv2Gk7HzdS`
- **Purpose**: Receives PDF uploads via webhook, extracts client names, prepares data for Chunk 0
- **Status**: Needs rebuild

#### 2. Chunk 0: Folder Initialization & Master Registry
- **Version**: v1.2 (LATEST)
- **Blueprint**: `chunk0_v1.2_parameterized_20251230.json`
- **Location**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/N8N_Blueprints/v4_phase1/chunk0_v1.2_parameterized_20251230.json`
- **Old Workflow ID**: `Ui2rQFpMu9G1RTE1`
- **Purpose**: Creates 37-folder structure in Google Drive, updates Master Client Registry
- **Status**: Needs rebuild

#### 3. Test Orchestrator: Autonomous Testing Infrastructure
- **Version**: v1.1 (LATEST)
- **Blueprint**: `test_orchestrator_v1.1_20251230.json`
- **Location**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/N8N_Blueprints/v4_phase1/test_orchestrator_v1.1_20251230.json`
- **Old Workflow ID**: `EzPj1xtEZOy2UY3V`
- **Purpose**: Automated end-to-end testing with 5 test scenarios
- **Status**: Needs rebuild

#### 4. Document Organizer V4: Complete Workflow ⭐ **41 NODES**
- **Version**: v4.0 (LATEST)
- **Blueprint**: `document_organizer_v4_complete.json`
- **Location**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/N8N_Blueprints/v4_phase1/document_organizer_v4_complete.json`
- **Old Workflow ID**: `j1B7fy24Jftmksmg`
- **Purpose**: End-to-end German real estate document processing - intake, OCR, classification, versioning
- **Architecture**: 41 nodes across 7 processing stages
- **Status**: Needs rebuild + AWS credentials

#### 5. Automated Email Test - Document Organizer V4
- **Version**: v1.0
- **Old Workflow ID**: `HtwT0krXJCcI7tC8`
- **Purpose**: Automated end-to-end testing for Document Organizer V4
- **Status**: Needs rebuild (likely not exported to JSON - may need to recreate)

---

### Sway's Expense System (3 workflows)

#### 1. Workflow 1: PDF Intake & Parsing
- **Version**: v1.0
- **Blueprint**: `workflow1_pdf_intake_v1.0.json`
- **Location**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/workflow1_pdf_intake_v1.0.json`
- **Old Workflow ID**: `BggZuzOVZ7s87psQ`
- **Node Count**: 8 nodes
- **Purpose**: Monitors inbox for bank statement PDFs, parses using OpenAI Vision
- **Status**: Needs rebuild

#### 2. Workflow 2: Gmail Receipt Monitor
- **Version**: v1.2.0 (LATEST)
- **Blueprint**: `workflow2_gmail_receipt_monitor_v1.2.0.json`
- **Location**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/workflow2_gmail_receipt_monitor_v1.2.0.json`
- **Old Workflow ID**: `2CA0zQTsdHA8bZKF`
- **Node Count**: 9 nodes
- **Purpose**: Daily Gmail search for receipts from 6 vendors, downloads attachments
- **Status**: Needs rebuild

#### 3. Workflow 3: Transaction-Receipt Matching
- **Version**: v1.3.0 (LATEST)
- **Blueprint**: `workflow3_transaction_receipt_matching_v1.3.0.json`
- **Location**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/SwaysExpenseSystem/N8N_Blueprints/v1_foundation/workflow3_transaction_receipt_matching_v1.3.0.json`
- **Old Workflow ID**: `LUPoW9jO3VfYIbgC`
- **Purpose**: Matches transactions with receipts using date/amount algorithms
- **Status**: Needs rebuild

---

### Other Workflows (1 workflow)

#### 1. Fathom Meeting Notification
- **Version**: v1.0
- **Blueprint**: `fathom-workflow.json`
- **Location**: `/Users/swayclarke/coding_stuff/fathom-workflow.json`
- **Old Workflow ID**: None (not deployed before)
- **Purpose**: Webhook for Fathom meetings, sends email notifications
- **Status**: Needs rebuild

---

## CREDENTIAL REQUIREMENTS

All credentials need to be recreated using Playwright automation:

### Google Services
- **Gmail OAuth2** (`gmailOAuth2`) - for Gmail triggers and operations
- **Google Drive OAuth2** (`googleDriveOAuth2Api`) - for file operations
- **Google Sheets OAuth2** (`googleSheetsOAuth2Api`) - for database operations

### API Keys
- **OpenAI API** - for PDF parsing and document classification
- **AWS Credentials** - for Textract OCR (Document Organizer V4)

### Webhook Credentials
- None required (webhooks are public endpoints)

---

## REBUILD SEQUENCE

**Phase 1: Credential Setup** (Playwright automation)
1. Create Gmail OAuth2 credential
2. Create Google Drive OAuth2 credential
3. Create Google Sheets OAuth2 credential
4. Create OpenAI API credential
5. Create AWS credential

**Phase 2: Eugene Workflows** (Priority: High)
1. Import Pre-Chunk 0 Intake
2. Import Chunk 0 v1.2
3. Import Document Organizer V4 ⭐ (41 nodes)
4. Import Test Orchestrator v1.1
5. Skip Automated Email Test (can recreate if needed)

**Phase 3: Expense System Workflows** (Priority: Medium)
1. Import Workflow 1: PDF Intake
2. Import Workflow 2: Gmail Receipt Monitor
3. Import Workflow 3: Transaction-Receipt Matching

**Phase 4: Other Workflows** (Priority: Low)
1. Import Fathom Meeting Notification

**Phase 5: Verification**
1. Check all credentials are connected
2. Test Eugene Test Orchestrator workflow
3. Verify webhook URLs are updated
4. Document new workflow IDs in VERSION_LOG files

---

## CRITICAL NOTES

- All old workflow IDs are LOST - new IDs will be generated
- Webhook URLs will change - need to update external systems
- Credentials must be recreated from scratch using Playwright
- Must update VERSION_LOG.md files with new workflow IDs after rebuild
- Document Organizer V4 (41 nodes) is the most complex - rebuild carefully

---

## TOTAL WORKFLOWS TO REBUILD: 9

✅ Found all latest blueprints locally
⏳ Ready to begin rebuild using n8n MCP tools
