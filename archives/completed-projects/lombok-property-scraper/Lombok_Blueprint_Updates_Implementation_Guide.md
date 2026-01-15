# Lombok Invest Capital Property Scraper - Implementation Guide

**Date:** 2026-01-08
**Blueprint:** Lombok invest capital Property Scraper v5
**Purpose:** Add variables, error handling, and enhanced reporting

---

## Table of Contents
1. [Variable Module Setup](#1-variable-module-setup)
2. [Enhanced Summary Email](#2-enhanced-summary-email)
3. [Error Handling Additions](#3-error-handling-additions)
4. [Hardcoded Values to Replace](#4-hardcoded-values-to-replace)
5. [Implementation Order](#5-implementation-order)

---

## 1. Variable Module Setup

### Where to Place:
**At the very beginning of the workflow** (first module, before module 22)

### JSON Code:
```json
{
    "id": 1,
    "module": "builtin:SetVariables",
    "version": 1,
    "parameters": {},
    "mapper": {
        "variables": [
            {
                "name": "userEmail",
                "value": "swayclarkeii@gmail.com"
            },
            {
                "name": "notificationEmail",
                "value": "sway@oloxa.ai"
            },
            {
                "name": "spreadsheetId",
                "value": "1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54"
            },
            {
                "name": "dataStoreId",
                "value": "81942"
            },
            {
                "name": "workflowName",
                "value": "Lombok Invest Capital Property Scraper"
            }
        ],
        "scope": "roundtrip"
    },
    "metadata": {
        "designer": {
            "x": -300,
            "y": 0,
            "name": "🔧 Configuration Variables"
        },
        "restore": {},
        "parameters": [],
        "expect": [
            {
                "name": "variables",
                "spec": [
                    {
                        "name": "name",
                        "type": "text",
                        "label": "Variable name",
                        "required": true
                    },
                    {
                        "name": "value",
                        "label": "Variable value"
                    }
                ],
                "type": "array",
                "label": "Variables"
            },
            {
                "name": "scope",
                "type": "select",
                "label": "Variable lifetime",
                "validate": {
                    "enum": [
                        "roundtrip",
                        "execution"
                    ]
                }
            }
        ]
    }
}
```

### How to Add:
1. Open the blueprint JSON file
2. Find the `"flow": [` array (around line 3)
3. Insert the above JSON as the FIRST item in the array
4. Add a comma after the closing `}` of this module
5. Update all subsequent module IDs if needed (or keep them as-is, Make.com handles duplicates)

---

## 2. Enhanced Summary Email (Module 515)

### Current Email Body:
```
That's right, check them out here! {{514.webViewLink}}
```

### NEW Enhanced Email Body:
```html
<div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
    <h2 style="color: #2c3e50;">🎉 New Lombok Invest Capital Leads!</h2>

    <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #34495e;">📊 Summary</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background-color: #ecf0f1;">
                <td style="padding: 10px; border: 1px solid #bdc3c7;"><strong>Task 1 (New Properties)</strong></td>
                <td style="padding: 10px; border: 1px solid #bdc3c7;">{{length(508.array)}}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border: 1px solid #bdc3c7;"><strong>Task 2 (New Properties)</strong></td>
                <td style="padding: 10px; border: 1px solid #bdc3c7;">{{length(260.array)}}</td>
            </tr>
            <tr style="background-color: #ecf0f1;">
                <td style="padding: 10px; border: 1px solid #bdc3c7;"><strong>Task 3 (New Properties)</strong></td>
                <td style="padding: 10px; border: 1px solid #bdc3c7;">{{length(261.array)}}</td>
            </tr>
            <tr style="background-color: #3498db; color: white;">
                <td style="padding: 10px; border: 1px solid #2980b9;"><strong>Total New Properties</strong></td>
                <td style="padding: 10px; border: 1px solid #2980b9;"><strong>{{length(508.array) + length(260.array) + length(261.array)}}</strong></td>
            </tr>
        </table>
    </div>

    <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
        <p style="margin: 0; color: #856404;">
            <strong>⏰ Run Time:</strong> {{formatDate(now; "YYYY-MM-DD HH:mm:ss")}}
        </p>
    </div>

    <div style="margin: 20px 0;">
        <a href="{{514.webViewLink}}" style="display: inline-block; background-color: #27ae60; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">
            📄 View Full Report
        </a>
    </div>

    <p style="color: #7f8c8d; font-size: 12px; margin-top: 30px;">
        This is an automated report from {{1.workflowName}}. Running bi-weekly.
    </p>
</div>
```

### How to Update Module 515:
1. Find module 515 in the JSON (around line 12941)
2. Locate the `"html"` field (line 12957)
3. Replace the entire value with the new HTML above
4. Update the `"to"` field to use the variable: `["{{1.notificationEmail}}"]`

### Updated Module 515 JSON (Key Fields):
```json
{
    "id": 515,
    "module": "email:ActionSendEmail",
    "mapper": {
        "to": ["{{1.notificationEmail}}"],
        "subject": "🎉 You Got {{length(508.array) + length(260.array) + length(261.array)}} New Lombok Leads!",
        "html": "[INSERT THE ENHANCED EMAIL BODY HTML FROM ABOVE]",
        "attachments": [
            {
                "cid": "{{514.id}}",
                "data": "{{514.data}}",
                "fileName": "{{514.name}}"
            }
        ]
    }
}
```

---

## 3. Error Handling Additions

### A. Google Sheets API Quota Error Handler

**Where:** After each `google-sheets:addRow` or `google-sheets:addSheet` module

**JSON to Add:**
```json
{
    "id": 999,
    "module": "gateway:ErrorHandler",
    "version": 1,
    "parameters": {},
    "mapper": {},
    "metadata": {
        "designer": {
            "x": 0,
            "y": 0,
            "name": "Google Sheets Error Handler"
        }
    },
    "flow": [
        {
            "id": 1000,
            "module": "builtin:Router",
            "version": 1,
            "mapper": {},
            "metadata": {
                "designer": {
                    "x": 300,
                    "y": 0
                }
            },
            "routes": [
                {
                    "flow": [
                        {
                            "id": 1001,
                            "module": "email:ActionSendEmail",
                            "version": 7,
                            "parameters": {
                                "account": 3439042,
                                "accountImap": 3439042
                            },
                            "filter": {
                                "name": "If Quota Exceeded",
                                "conditions": [
                                    [
                                        {
                                            "a": "{{1000.message}}",
                                            "b": "quota",
                                            "o": "text:contains"
                                        }
                                    ],
                                    [
                                        {
                                            "a": "{{1000.message}}",
                                            "b": "rate limit",
                                            "o": "text:contains"
                                        }
                                    ]
                                ]
                            },
                            "mapper": {
                                "to": ["{{1.notificationEmail}}"],
                                "subject": "⚠️ Google Sheets API Quota Exceeded - {{1.workflowName}}",
                                "html": "<h2>Google Sheets API Error</h2><p><strong>Error Type:</strong> API Quota or Rate Limit Exceeded</p><p><strong>Error Message:</strong> {{1000.message}}</p><p><strong>Time:</strong> {{formatDate(now; \"YYYY-MM-DD HH:mm:ss\")}}</p><p><strong>Action Required:</strong> Check your Google Cloud Console quotas or wait for quota reset.</p>",
                                "contentType": "html"
                            }
                        }
                    ]
                },
                {
                    "flow": [
                        {
                            "id": 1002,
                            "module": "email:ActionSendEmail",
                            "version": 7,
                            "parameters": {
                                "account": 3439042,
                                "accountImap": 3439042
                            },
                            "filter": {
                                "name": "Other Sheets Errors",
                                "conditions": []
                            },
                            "mapper": {
                                "to": ["{{1.notificationEmail}}"],
                                "subject": "⚠️ Google Sheets Error - {{1.workflowName}}",
                                "html": "<h2>Google Sheets Error</h2><p><strong>Error Message:</strong> {{1000.message}}</p><p><strong>Module:</strong> {{1000.module}}</p><p><strong>Time:</strong> {{formatDate(now; \"YYYY-MM-DD HH:mm:ss\")}}</p>",
                                "contentType": "html"
                            }
                        }
                    ]
                }
            ]
        }
    ]
}
```

**How to Add:**
- In the Make.com UI, right-click on a Google Sheets module → "Add Error Handler" → Insert the JSON above
- OR manually add to the JSON after the module's closing bracket

---

### B. DataStore Error Handler

**Where:** After each `datastore:AddRecord`, `datastore:ExistRecord`, or `datastore:DeleteRecord` module

**JSON to Add:**
```json
{
    "id": 1003,
    "module": "gateway:ErrorHandler",
    "version": 1,
    "parameters": {},
    "mapper": {},
    "metadata": {
        "designer": {
            "x": 0,
            "y": 0,
            "name": "DataStore Error Handler"
        }
    },
    "flow": [
        {
            "id": 1004,
            "module": "email:ActionSendEmail",
            "version": 7,
            "parameters": {
                "account": 3439042,
                "accountImap": 3439042
            },
            "mapper": {
                "to": ["{{1.notificationEmail}}"],
                "subject": "⚠️ DataStore Operation Failed - {{1.workflowName}}",
                "html": "<h2>DataStore Error</h2><p><strong>Operation:</strong> {{1004.module}}</p><p><strong>Error Message:</strong> {{1004.message}}</p><p><strong>DataStore ID:</strong> {{1.dataStoreId}}</p><p><strong>Time:</strong> {{formatDate(now; \"YYYY-MM-DD HH:mm:ss\")}}</p><p><strong>Possible Causes:</strong></p><ul><li>DataStore quota exceeded</li><li>DataStore record size limit exceeded</li><li>Network connectivity issue</li></ul>",
                "contentType": "html"
            },
            "metadata": {
                "designer": {
                    "x": 300,
                    "y": 0
                }
            }
        }
    ]
}
```

---

### C. Gmail Send Failure Handler

**Where:** After module 515 (the final New Leads email)

**JSON to Add:**
```json
{
    "id": 1005,
    "module": "gateway:ErrorHandler",
    "version": 1,
    "parameters": {},
    "mapper": {},
    "metadata": {
        "designer": {
            "x": 0,
            "y": 0,
            "name": "Gmail Send Error Handler"
        }
    },
    "flow": [
        {
            "id": 1006,
            "module": "google-sheets:addRow",
            "version": 2,
            "parameters": {
                "__IMTCONN__": 3894159
            },
            "mapper": {
                "mode": "map",
                "values": {
                    "Timestamp": "{{formatDate(now; \"YYYY-MM-DD HH:mm:ss\")}}",
                    "Error Type": "Gmail Send Failure",
                    "Error Message": "{{1005.message}}",
                    "Module": "515 - Send New Leads",
                    "Action Required": "Check Gmail connection and quota"
                },
                "sheetId": "Email Errors",
                "spreadsheetId": "{{1.spreadsheetId}}"
            },
            "metadata": {
                "designer": {
                    "x": 300,
                    "y": 0,
                    "name": "Log Email Error to Sheet"
                }
            }
        }
    ]
}
```

**Note:** This logs errors to a sheet instead of sending another email (since email is failing). You'll need to create an "Email Errors" sheet in your spreadsheet.

---

## 4. Hardcoded Values to Replace

### Search and Replace List:

| Current Value | Replace With | Occurrences |
|--------------|--------------|-------------|
| `swayclarkeii@gmail.com` | `{{1.userEmail}}` | ~30+ |
| `sway@oloxa.ai` | `{{1.notificationEmail}}` | ~10+ |
| `1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54` | `{{1.spreadsheetId}}` | ~20+ |
| `81942` | `{{1.dataStoreId}}` | ~15+ |

### Locations to Update:

**Google Sheets modules:**
- `"spreadsheetId": "1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54"` → `"spreadsheetId": "{{1.spreadsheetId}}"`

**Gmail modules:**
- `"to": ["sway@oloxa.ai"]` → `"to": ["{{1.notificationEmail}}"]`
- Connection labels can stay as-is (they're just UI labels)

**DataStore modules:**
- `"datastore": 81942` → `"datastore": "{{1.dataStoreId}}"`

### How to Do This:
**Option 1: Manual Find & Replace (Safest)**
1. Open the JSON in VS Code
2. Use Find & Replace (Cmd+F / Ctrl+F)
3. Search for: `"1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54"`
4. Replace with: `"{{1.spreadsheetId}}"`
5. Repeat for each value

**Option 2: Automated Script (I can create this for you)**

---

## 5. Implementation Order

### Step-by-Step Process:

1. **✅ Backup First**
   - Download a copy of the current blueprint
   - Save as `Lombok invest capital Property Scraper v5 - BACKUP.json`

2. **Add Variable Module**
   - Insert the Variable module JSON at the beginning
   - Save as `Lombok invest capital Property Scraper v6.json`

3. **Update Module 515 (Summary Email)**
   - Replace the email body with enhanced HTML
   - Update subject line to include count
   - Change `to` field to use `{{1.notificationEmail}}`

4. **Add Error Handlers**
   - Add Google Sheets error handler after key Sheets modules
   - Add DataStore error handler after DataStore modules
   - Add Gmail error handler after module 515

5. **Replace Hardcoded Values**
   - Use Find & Replace for all spreadsheet IDs
   - Update all email addresses
   - Update datastore IDs

6. **Create Error Tracking Sheet**
   - Use Google Sheets MCP to create "Email Errors" sheet in the AA folder spreadsheet
   - Add columns: Timestamp, Error Type, Error Message, Module, Action Required

7. **Test Import**
   - Import the updated JSON into Make.com
   - Check all connections are still valid
   - Do a test run with small data

8. **Validate**
   - Confirm variable module is first
   - Confirm email shows property counts
   - Confirm error handlers are attached

---

## 6. Google Sheets Setup for Error Tracking

### Sheet to Create:
**Name:** `Email Errors`
**Location:** Same spreadsheet as your other data (ID: `1W2rnvacmbVl-OZ8EPacS8L89uN80TA8xxmw2uAEdn54`)

### Columns:
1. Timestamp
2. Error Type
3. Error Message
4. Module
5. Action Required

---

## Additional Notes

### Error Handling Strategy:
- **Critical errors** (Apify empty, Gmail failures) → Send email alert
- **Non-critical errors** (Sheets quota) → Log to sheet + email
- **DataStore errors** → Email alert (since workflow depends on deduplication)

### Operations Impact:
With all error handlers added, you're adding approximately **15-20 extra operations per run** (only triggered on errors).

Normal run: ~150-200 operations
With errors: ~165-220 operations

### Maintenance:
Once variables are set up, you only need to update Module 1 (Variable module) to change:
- Email addresses
- Spreadsheet IDs
- DataStore IDs

---

## Need Help?

If you need me to:
1. ✅ Create the automated Find & Replace script
2. ✅ Create the Google Sheet in your AA folder
3. ✅ Generate the complete updated JSON file
4. ✅ Create a testing checklist

Just let me know which one(s) you want!

---

**End of Implementation Guide**
