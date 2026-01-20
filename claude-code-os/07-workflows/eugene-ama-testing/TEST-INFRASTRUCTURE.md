# Eugene AMA Document Processing - Test Infrastructure

**Created**: December 30, 2025
**Last Updated**: December 30, 2025

---

## Architecture

```
                         TEST ORCHESTRATOR WORKFLOW
                              (EzPj1xtEZOy2UY3V)
                                     │
    ┌────────────────────────────────┼────────────────────────────────┐
    │                                │                                │
    ▼                                ▼                                ▼
┌─────────────┐              ┌──────────────┐              ┌─────────────────┐
│   Webhook   │──────────────│  Prepare     │──────────────│  Route          │
│   Trigger   │              │  Test Data   │              │  Scenario       │
└─────────────┘              └──────────────┘              └─────────────────┘
                                                                  │
                              ┌───────────────────────────────────┼───────────────┐
                              │                                   │               │
                     (simulateError)                        (normal path)         │
                              │                                   │               │
                              ▼                                   ▼               │
                    ┌─────────────────┐                  ┌────────────────┐       │
                    │ Handle Error    │                  │ Execute        │       │
                    │ Simulation      │                  │ Chunk 0        │       │
                    └─────────────────┘                  └────────────────┘       │
                              │                                   │               │
                              │                                   ▼               │
                              │                          ┌────────────────┐       │
                              │                          │ Check Client   │       │
                              │                          │ Registry       │       │
                              │                          │ (Google Sheets)│       │
                              │                          └────────────────┘       │
                              │                                   │               │
                              └───────────────┬───────────────────┘               │
                                              │                                   │
                                              ▼                                   │
                                    ┌─────────────────┐                           │
                                    │  Merge Results  │◄──────────────────────────┘
                                    └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │ Verify Results  │
                                    │ (Cross-Platform)│
                                    └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │ Respond to      │
                                    │ Webhook         │
                                    └─────────────────┘
```

---

## Test Scenarios

### Happy Path
| ID | Scenario | Expected |
|----|----------|----------|
| HP-01 | New client, valid PDF | Folders created, registry updated |
| HP-02 | Existing client | Routes to Chunk 3 path |

### Edge Cases
| ID | Scenario | Expected Behavior |
|----|----------|-------------------|
| EC-01 | Corrupted PDF | Graceful error, quarantine, notification |
| EC-02 | No client name in PDF | Route to manual review |
| EC-03 | Ambiguous client | AI picks most likely match |
| EC-04 | Empty email | Skip, no error |
| EC-05 | Wrong file type | Filter out non-PDFs |
| EC-06 | Duplicate email | Skip (already processed) |
| EC-07 | Very large PDF | Handle timeout, chunk processing |
| EC-08 | Special characters in name | Sanitize folder name |
| EC-09 | Password protected PDF | Manual intervention required |
| EC-10 | Mixed valid/invalid attachments | Partial success |

---

## Workflow IDs

| Workflow | ID | Status |
|----------|-----|--------|
| Pre-Chunk 0 (Intake) | `Kj4AI5N1hWptreH6` | Active |
| Chunk 0 (Folders) | `Ui2rQFpMu9G1RTE1` | Active |
| **Test Orchestrator** | `EzPj1xtEZOy2UY3V` | Ready |

---

## Resource IDs

| Resource | ID |
|----------|-----|
| Client Registry Sheet | `1T-jL-cLgplVeZ3EMroQxvGEqI5G7t81jRZ2qINDvXNI` |
| Folder ID Sheet | `1-CPnCr3locAORVX5tUEoh6r0i-x3tQ_ROTN0VXatOAU` |
| AMA Parent Folder | `1ikw3k-EgpVg_h2ySDdqdUFB7-FQyYDFm` |
| Google Drive Credential | `7vK12cTuYm7XlNAy` |
| Google Sheets Credential | `3AIbwgVoWqlgyVKF` |

---

## Verification Points

| Platform | MCP Tool | Check |
|----------|----------|-------|
| n8n | `n8n_executions` | Status = success |
| Google Drive | `google-drive__search` | Folders exist |
| Google Sheets | `google-sheets__read_rows` | Registry updated |

---

## How to Run Tests

### Via Webhook (Production)
```bash
curl -X POST https://n8n.oloxa.ai/webhook/test-chunk-integration \
  -H "Content-Type: application/json" \
  -d '{"scenarioId": "HP-01"}'
```

### Available Scenario IDs
- `HP-01`: New client with valid PDF (default)
- `HP-02`: Existing client (Eugene Wei)
- `EC-01`: Corrupted PDF simulation
- `EC-02`: Missing client name simulation
- `EC-08`: Special characters in name

### Via Claude Code MCP
```
mcp__n8n-mcp__n8n_test_workflow({
  workflowId: "EzPj1xtEZOy2UY3V",
  data: { scenarioId: "HP-01" }
})
```

---

## Test Report Format

```json
{
  "testId": "test_1735516123456",
  "scenario": {
    "id": "HP-01",
    "name": "New Client Valid PDF",
    "clientName": "Test Corp Alpha 1735516123456"
  },
  "status": "PASS",
  "statusReason": "All verifications passed",
  "verifications": {
    "n8n": {
      "workflowExecuted": true,
      "chunk0Ran": true
    },
    "googleSheets": {
      "registryChecked": true,
      "clientFound": true
    },
    "googleDrive": {
      "folderCreated": true,
      "folderId": "1abc123xyz..."
    }
  }
}
```
