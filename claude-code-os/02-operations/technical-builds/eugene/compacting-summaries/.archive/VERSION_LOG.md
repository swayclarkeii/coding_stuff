# Eugene AMA Document Organizer - Version Log

**Project**: Email-based document organization system for AMA Capital real estate deals
**Location**: `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/compacting-summaries/`
**Current Version**: v1.5
**Last Updated**: January 5, 2026

---

## Quick Reference

| Version | Status | Date | Phase | Notes |
|---------|--------|------|-------|-------|
| v1.5 | ✅ Complete | 2026-01-05 | Production | Workflow cleanup - removed obsolete nodes |
| v1.4 | ✅ Complete | 2026-01-05 | Production | UNKNOWN client handling + email notifications |
| v1.3 | ✅ Complete | 2026-01-04 | Production | All workflows production ready |
| v1.2 | ✅ Complete | 2026-01-04 | Production | Chunk 0 validation fixes |
| v1.1 | ✅ Complete | 2026-01-03 | Testing | Chunk 1 live test successful |
| v1.0 | ✅ Complete | 2026-01-03 | Testing | Binary data handling + syntax migration |

---

## Versioning Scheme

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR (v1.x.x)**: Breaking changes, complete rewrites, new major milestones
  - Example: v1.0.0 = Foundation complete
  - Example: v2.0.0 = Full automation operational

- **MINOR (vx.1.x)**: New features, significant enhancements, backward compatible
  - Example: v1.1.0 = New workflow added
  - Example: v1.2.0 = Major feature enhancement

- **PATCH (vx.x.1)**: Bug fixes, small improvements, refinements
  - Example: v1.0.1 = Bug fix
  - Example: v1.0.2 = Configuration tweak

---

## Version History

### v1.5 - Workflow Cleanup & Architecture Simplification
**Date**: January 5, 2026
**Status**: ✅ Complete
**Phase**: Production

#### Components Modified
- **Chunk 1 (djsBWsrAEKbj2omB)**: Removed obsolete nodes from old architecture

#### What Was Removed
**Deleted (replaced by Pre-Chunk 0):**
- Gmail Trigger - Pre-Chunk 0 handles email monitoring
- Get Gmail Message - Pre-Chunk 0 extracts email data
- Normalize Email Data - Pre-Chunk 0 normalizes data
- Extract Attachments - Pre-Chunk 0 extracts PDFs from binary
- IF Has Attachments - Pre-Chunk 0 filters PDFs
- Filter Supported Files - Pre-Chunk 0 only passes PDFs
- Sequential Processing - Handled by Pre-Chunk 0's loop
- Upload to Staging - Replaced by "Move File to Staging" (active node)
- Normalize Output - Pre-Chunk 0 handles output format

**Preserved (deactivated for future use):**
- IF ZIP File - Will be moved to Pre-Chunk 0 in v2.0
- Extract ZIP (Decompress) - Future ZIP extraction feature
- Normalize ZIP Contents - Future ZIP extraction feature
- Merge File Streams - Will be used in Pre-Chunk 0 when ZIP feature added

#### Current Chunk 1 Flow (Simplified)
```
Receive from Pre-Chunk 0 → Move File to Staging
```

**That's it.** Chunk 1 is now a simple sub-workflow that only moves files.

#### Architecture Decision: ZIP Extraction Placement

**Decision**: ZIP extraction will be implemented in **Pre-Chunk 0**, not Chunk 1

**Rationale:**
- ZIP files may contain PDFs for **multiple different clients**
- If ZIP extraction happens in Chunk 1, routing has already occurred (too late)
- Pre-Chunk 0 can extract ZIP → get all PDFs → identify client **per PDF**
- Each PDF gets properly routed regardless of whether it came from ZIP or direct attachment

**Future v2.0 Flow (with ZIP):**
```
Pre-Chunk 0:
  Receive Email
      ↓
  Filter PDF/ZIP Attachments
      ↓
  IF ZIP File?
    YES → Extract ZIP → Get PDFs from ZIP
    NO → Pass through PDFs
      ↓
  Merge File Streams (all PDFs together)
      ↓
  FOR EACH PDF:
    → Extract Text
    → Identify Client
    → Route (UNKNOWN/NEW/EXISTING)
```

#### What Works
✅ Chunk 1 workflow simplified to 2 active nodes
✅ All obsolete nodes removed
✅ ZIP extraction nodes preserved (deactivated) for future implementation
✅ Architecture decision documented for v2.0

#### What Doesn't Work Yet
N/A - Cleanup complete, system functional

#### Known Issues
None

#### Blockers
None

#### Rollback Instructions
**To roll back from v1.5 to v1.4**:

1. **Chunk 1 workflow (djsBWsrAEKbj2omB)**:
   - Use n8n UI: Workflow > Versions > Select v1.4 timestamp (before cleanup)
   - This will restore all deactivated nodes
   - No functional impact - deactivated nodes weren't running anyway

2. **Verification**:
   - Test Pre-Chunk 0 → Chunk 0 → Chunk 1 flow still works
   - Should be identical behavior (cleanup was cosmetic)

#### Files & Resources
**Workflows Modified:**
- Chunk 1: `djsBWsrAEKbj2omB` (v1.5 = cleaned up version)

**No changes to:**
- Pre-Chunk 0: `70n97A6OmYCsHMmV` (still v1.4)
- Chunk 0: `zbxHkXOoD1qaz6OS` (still v1.4)

#### Next Version Goal
**v2.0 - ZIP File Extraction Support**
- Implement ZIP extraction in Pre-Chunk 0
- Move IF ZIP File, Extract ZIP, Normalize ZIP Contents nodes from Chunk 1 to Pre-Chunk 0
- Add Merge File Streams after ZIP extraction
- Test with ZIP files containing multiple client PDFs

---

### v1.4 - UNKNOWN Client Handling & Email Notifications
**Date**: January 5, 2026
**Status**: ✅ Complete
**Phase**: Production

#### Components Created
- **UNKNOWN Client Routing Path**: New decision gate output (Output 0) for unidentified clients
- **Folder Structure for UNKNOWN**: Creates full 37-folder structure + 38_Unknowns subfolder
- **Email Notification System**: Sends alert to swayclarkeii@gmail.com when UNKNOWN client document arrives
- **Client_Registry Status Tracking**: Adds `PENDING_IDENTIFICATION` status for UNKNOWN clients

#### Workflow Modifications
**Pre-Chunk 0 (70n97A6OmYCsHMmV):**
- Node 1: "Prepare UNKNOWN Client Data" - Generates static "UNKNOWN_CLIENT" identifier
- Node 2: "Check If UNKNOWN Path" - IF node routing UNKNOWN vs NEW vs EXISTING paths
- Node 3: "Extract 38_Unknowns Folder ID" - Parses Chunk 0 response for folder ID
- Node 4: "Move PDF to 38_Unknowns" - Uploads PDF to correct subfolder
- Node 5: "Prepare Email Notification Data" - Extracts metadata for alert
- Node 6: "Build Email HTML Body" - Renders professional HTML email template
- Node 7: "Send Email Notification" - Gmail send operation

**Chunk 0 (zbxHkXOoD1qaz6OS):**
- Modified "Prepare Registry Entry" - Detects UNKNOWN clients and sets status to `PENDING_IDENTIFICATION`

#### What Works
✅ Three-path routing: UNKNOWN / NEW / EXISTING clients all function correctly
✅ UNKNOWN client folder creation with full 37-folder structure
✅ PDF upload to `38_Unknowns` subfolder (NOT _Staging)
✅ Email notifications with clickable links to PDF and root folder
✅ Client_Registry entries with status tracking
✅ Clean static naming: "UNKNOWN_CLIENT" (not timestamp-based)

#### What Doesn't Work Yet
N/A - All features functional

#### Known Issues
⚠️ **Test data cleanup required**: 14 test entries were created during development and manually cleaned from Client_Registry (rows 2-15)
- Pattern: Entries with corrupted "n_a" values from timestamp extraction issues
- Resolution: Use simple static naming ("UNKNOWN_CLIENT") instead of timestamps

#### Blockers
None - System fully operational

#### Rollback Instructions
**To roll back from v1.4 to v1.3**:

1. **Pre-Chunk 0 workflow (70n97A6OmYCsHMmV)**:
   - Use n8n UI: Workflow > Versions > Select v1.3 timestamp (pre-UNKNOWN feature)
   - Delete 7 UNKNOWN-related nodes (Prepare UNKNOWN, Check If UNKNOWN, Extract folder ID, Move PDF, Email notification nodes)
   - Reconnect Decision Gate Output 0 to original "Handle Unidentified Client" node

2. **Chunk 0 workflow (zbxHkXOoD1qaz6OS)**:
   - Revert "Prepare Registry Entry" node to remove UNKNOWN status detection
   - Change back to: `const clientStatus = 'ACTIVE';` (remove conditional logic)

3. **Client_Registry cleanup**:
   - Delete any entries with `Client_Name: "UNKNOWN_CLIENT"`
   - Delete any entries with `status: "PENDING_IDENTIFICATION"`

4. **Verification**:
   - Test with identifiable client (should route to NEW or EXISTING)
   - Verify no UNKNOWN path executions occur

#### Files & Resources

**n8n Workflows:**
- Pre-Chunk 0: `70n97A6OmYCsHMmV` (v1.4 includes UNKNOWN routing)
- Chunk 0: `zbxHkXOoD1qaz6OS` (v1.4 includes status detection)
- Chunk 1: `djsBWsrAEKbj2omB` (unchanged from v1.3)

**Google Sheets:**
- Client_Registry: `1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI` (GID: 762792134)
- AMA_Folder_IDs: `1-CPnCr3locAORVX5tUEoh6r0i-x3tQ_ROTN0VXatOAU`

**Google Drive:**
- Client Root Parent: `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm`
- dummy_files (test PDFs): `1GG_OCKvT1ivR0F-uIVq0b1jhHreWg1Kh`

**Test Data:**
- Execution #427: First UNKNOWN test (failed - routed to EXISTING with corrupted "n_a")
- Execution #429: Final UNKNOWN test (success - clean "UNKNOWN_CLIENT" folder naming)

**Documentation:**
- Plan file: `/Users/swayclarke/.claude/plans/keen-bouncing-tiger.md`
- PROJECT_STATE_v1.3: Session 5 completion state

#### Next Version Goal
**v1.5 - Webhook Integration for Test Email Sender**
- Fix webhook trigger for Test Email Sender workflow (RZyOIeBy7o3Agffa)
- Webhook URL: `https://n8n.oloxa.ai/webhook/0743d128-ce67-4a01-9d8f-37b369708d48`
- Current workaround: Manual execution from n8n UI

---

### v1.3 - All Workflows Production Ready
**Date**: January 4, 2026
**Status**: ✅ Complete
**Phase**: Production

#### Components Modified
- Pre-Chunk 0: Column name mismatch fixed (`Intake_Folder_ID` → `Staging_Folder_ID`)
- Chunk 0: Google Sheets validation errors fixed (added `range` parameters)
- Client_Registry: Empty row cleanup from failed execution

#### What Works
✅ Pre-Chunk 0: All node fixes applied and verified
✅ Chunk 0: 0 validation errors (was 2 errors)
✅ Chunk 1: Live test successful with 3 PDFs
✅ Test Email Sender: Working via manual execution
✅ OAuth credentials: swayfromthehook@gmail.com authenticated

#### Known Issues
⚠️ Webhook trigger not working on Test Email Sender workflow
- Workflow active but webhook doesn't trigger execution
- Workaround: Manual execution from n8n UI

#### Rollback Instructions
**To roll back from v1.3 to v1.2**:
1. Revert Chunk 0 "Write to Client Registry" field mapping back to `Intake_Folder_ID`
2. Revert Pre-Chunk 0 "Filter Staging Folder ID" to read from `Intake_Folder_ID`
3. Remove `range` parameters from Google Sheets append nodes

---

### v1.2 - Chunk 0 Validation Fixes
**Date**: January 4, 2026
**Status**: ✅ Complete
**Phase**: Testing

#### Components Modified
- Chunk 0: "Write Folder IDs to Sheet" - Added `range: "A:C"`
- Chunk 0: "Write to Client Registry" - Added complete configuration + `range: "A:F"`

#### What Works
✅ Chunk 0 validation: 0 errors (was 2 errors)
✅ Google Sheets append operations now valid

#### Known Issues
⚠️ Column name mismatch still present (fixed in v1.3)
- `Intake_Folder_ID` vs `Staging_Folder_ID` inconsistency

---

### v1.1 - Chunk 1 Live Test Successful
**Date**: January 3, 2026
**Status**: ✅ Complete
**Phase**: Testing

#### Components Tested
- Chunk 1: Email to Staging workflow (djsBWsrAEKbj2omB)
- Test execution #182: 3 PDFs uploaded successfully to Google Drive

#### What Works
✅ Gmail Trigger: Binary data extraction working
✅ splitInBatches loop: Sequential processing working
✅ Google Drive upload: All 3 files uploaded correctly

#### What Doesn't Work Yet
❌ Staging folder routing: PDFs going to wrong folder (fixed in later testing)

---

### v1.0 - Binary Data Handling & Syntax Migration
**Date**: January 3, 2026
**Status**: ✅ Complete
**Phase**: Foundation

#### Components Created
- Pre-Chunk 0: V4 Pre-Chunk 0: Intake & Client Identification (70n97A6OmYCsHMmV)
- Chunk 0: Folder Initialization (zbxHkXOoD1qaz6OS)
- Chunk 1: Email to Staging (djsBWsrAEKbj2omB)
- Test Orchestrator: Automated testing workflow (K1kYeyvokVHtOhoE)

#### What Works
✅ Pre-Chunk 0: Binary data handling fixed
✅ Pre-Chunk 0: All deprecated `$input.item(0)` → `$input.all()` conversions
✅ Pre-Chunk 0: Field reference mismatches corrected
✅ Pre-Chunk 0: Decision Gate boolean comparison fixed
✅ Chunk 0: Integration with Pre-Chunk 0 verified (10/10 successful calls)
✅ Chunk 0: Folder creation working (48 folders in 56 seconds)

#### What Doesn't Work Yet
❌ Chunk 1: Binary data handling not yet fixed (fixed in v1.1)

#### Known Issues
⚠️ Gmail Trigger stores attachments in `item.binary`, not `item.json.attachments`
⚠️ n8n v2.x requires `$input.all()` instead of deprecated `$input.item(0)`

#### Rollback Instructions
**To roll back from v1.0 to initial state**:
1. Revert all Code node syntax to v1.x format (`$input.item(0)`)
2. Revert binary data handling to read from `item.json.attachments`
3. Export current workflow JSONs as backups before reverting

#### Files & Resources
- FINAL_TEST_RESULTS_20260103.md: Initial test analysis
- LESSONS_LEARNED_v1.0_20260104.md: Binary data fix lessons

---

## Component Inventory

### n8n Workflows
| Workflow | ID | Version | Status |
|----------|----|---------| ------|
| V4 Pre-Chunk 0: Intake & Client Identification | `70n97A6OmYCsHMmV` | v1.4 | ✅ Active |
| Chunk 0: Folder Initialization (V4 - Parameterized) | `zbxHkXOoD1qaz6OS` | v1.4 | ✅ Active |
| Chunk 1: Email to Staging | `djsBWsrAEKbj2omB` | v1.5 | ✅ Active |
| Test Email Sender - swayfromthehook to swayclarkeii | `RZyOIeBy7o3Agffa` | v1.3 | ⚠️ Active (webhook broken) |
| Autonomous Test Runner - Chunk Integration | `K1kYeyvokVHtOhoE` | v1.3 | ✅ Active |

### Google Sheets
| Sheet | ID | Version | Status |
|-------|----|---------| ------|
| Client_Registry | `1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI` | v1.4 | ✅ Active |
| AMA_Folder_IDs | `1-CPnCr3locAORVX5tUEoh6r0i-x3tQ_ROTN0VXatOAU` | v1.0 | ✅ Active |
| Test Results | `1af9ZsSm5IDVWIYb5IMX8ys8a5SUUnQcb77xi9tJQVo8` | v1.0 | ✅ Active |

### Google Drive Resources
| Component | ID | Version | Status |
|-----------|----|---------| ------|
| Client Root (Parent) | `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm` | v1.0 | ✅ Active |
| dummy_files | `1GG_OCKvT1ivR0F-uIVq0b1jhHreWg1Kh` | v1.0 | ✅ Active |

### Documentation Files
| File | Location | Version | Status |
|------|----------|---------|--------|
| VERSION_LOG | `/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/compacting-summaries/VERSION_LOG.md` | v1.4 | ✅ Active |
| PROJECT_STATE_v1.3 | `PROJECT_STATE_v1.3_20260104.md` | v1.3 | 📁 Archived |
| LESSONS_LEARNED | `LESSONS_LEARNED_v1.0_20260104.md` | v1.0 | ✅ Reference |

---

## Rollback Procedures

### General Rollback Process
1. **Identify target version** from version history
2. **Review what changed** between current and target
3. **Follow specific rollback instructions** for that version
4. **Verify all components** match target version state
5. **Update "Current Version"** at top of this document
6. **Test system** to ensure rollback successful

### Component-Specific Rollback

#### n8n Workflows
1. Navigate to workflow in n8n UI (`https://n8n.oloxa.ai`)
2. Click ... menu > Versions
3. Export current workflow JSON as backup first
4. Select target version timestamp to restore
5. Click "Restore" button
6. Reactivate workflow if needed
7. Test execution with sample data

#### Google Sheets
1. Navigate to sheet in Google Drive
2. File > Version history > See version history
3. Find version matching target timestamp
4. Export current version as CSV backup
5. Click "Restore this version"
6. Verify column headers and data structure

#### Client_Registry Cleanup
When rolling back from UNKNOWN feature:
```
Use mcp__google-sheets__edit_row to clear rows with:
- Client_Name: "UNKNOWN_CLIENT"
- status: "PENDING_IDENTIFICATION"
```

---

## Critical Technical Notes

### UNKNOWN Client Routing Pattern
**Problem**: How to handle documents where AI cannot identify client name
**Solution**: Three-path decision routing with dedicated UNKNOWN folder structure

**Implementation**:
```
Decision Gate (IF node):
  Output 0: client_normalized is empty → UNKNOWN path
  Output 1: client is NEW (not in registry) → NEW path
  Output 2: client EXISTING (in registry) → EXISTING path
```

**Applied In**: Pre-Chunk 0 workflow (70n97A6OmYCsHMmV) "Decision Gate" node

**Benefits**:
- No orphaned documents
- Email alerts for manual review
- Full folder structure maintained (no flat fallback)
- Status tracking in Client_Registry

**Caveats**:
- Email notification to single recipient only (swayclarkeii@gmail.com)
- V2 feature deferred: Email metadata matching for duplicate prevention

---

### Client_Registry Status Field Pattern
**Problem**: Distinguish UNKNOWN clients from normal ACTIVE clients in registry
**Solution**: Conditional status assignment based on client name pattern

**Implementation**:
```javascript
// In Chunk 0 "Prepare Registry Entry" node
const isUnknownClient = clientNameRaw.startsWith('UNKNOWN_');
const clientStatus = isUnknownClient ? 'PENDING_IDENTIFICATION' : 'ACTIVE';
```

**Applied In**: Chunk 0 workflow (zbxHkXOoD1qaz6OS)

**Benefits**:
- Clear visual distinction in registry
- Future cleanup queries easy (`WHERE status = 'PENDING_IDENTIFICATION'`)
- No need for separate UNKNOWN tracking sheet

---

### Static Naming vs Timestamp-Based for UNKNOWN Clients
**Problem**: How to name UNKNOWN client folders uniquely
**Initial Approach**: Timestamp-based naming (`UNKNOWN_2026-01-05_1141`)
**Issue**: Timestamp extraction caused corrupted "n_a" values in Client_Registry

**Final Solution**: Simple static naming (`UNKNOWN_CLIENT`)

**Rationale**:
- Simplicity wins over uniqueness
- User renames folder after identifying client anyway
- No timestamp parsing errors
- Clear "pending action" signal

**Applied In**: Pre-Chunk 0 "Prepare UNKNOWN Client Data" node

---

### Binary Data Preservation in Code Nodes
**Problem**: n8n Code nodes must explicitly preserve binary data or it gets lost
**Solution**: Always include `binary: $input.first().binary` in return statements

**Example**:
```javascript
return {
  json: { /* your data */ },
  binary: $input.first().binary  // ✅ CRITICAL
};
```

**Applied In**: All Code nodes across all workflows

**Reference**: N8N_NODE_REFERENCE.md lines 251-307

---

## Blueprint File Naming Convention

**Format**: `{workflow_name}_v{version}_{date}.json`

**Examples**:
- `pre_chunk_0_v1.4_20260105.json` (current)
- `chunk_0_v1.4_20260105.json` (current)
- `chunk_1_v1.3_20260104.json`

**Archive Format**: `_archived/{workflow_name}_v{version}_{date}_ARCHIVED.json`

**Archive Structure**:
```
/N8N_Blueprints/
├── v1_foundation/
│   ├── pre_chunk_0_v1.0_20260103.json
│   └── chunk_0_v1.0_20260103.json
├── v1_production/
│   ├── pre_chunk_0_v1.4_20260105.json
│   └── chunk_0_v1.4_20260105.json
└── _archived/
    └── [older versions]
```

---

## Notes

- **Version numbers are permanent** - never reuse or skip
- **Document ALL breaking changes** clearly in version notes
- **Always test rollback procedures** before considering version complete
- **Keep JSON exports** of all workflows for each version in N8N_Blueprints/
- **This is a living document** - update as system evolves
- **UNKNOWN feature** is forward-compatible - can add V2 email matching later

---

## Questions & Support

For questions about this project:
1. Review the version history for specific feature details
2. Check component inventory for current workflow IDs
3. Review known issues for current blockers
4. Consult rollback procedures for recovery steps
5. See PROJECT_REFERENCE.md for Google Sheet IDs and folder locations

**Last reviewed**: January 5, 2026
