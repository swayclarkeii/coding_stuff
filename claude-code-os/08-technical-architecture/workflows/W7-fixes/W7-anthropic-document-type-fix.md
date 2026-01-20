# W7 Anthropic Document Type Fix

**Date:** 2026-01-12
**Workflow:** 6x1sVuv4XKN0002B (Expense System - Workflow 7: Downloads Folder Monitor)
**Node:** Build Anthropic Request (node #6)
**Issue:** Anthropic API rejecting PDFs with error about image media_type

## Problem

Execution 1584 failed with:
```
messages.0.content.1.image.source.base64.media_type: Input should be 'image/jpeg', 'image/png', 'image/gif' or 'image/webp'
```

The Anthropic Messages API requires:
- **PDFs**: `type: "document"` with `media_type: "application/pdf"`
- **Images**: `type: "image"` with `media_type: "image/jpeg"`, etc.

## Fix Applied

Updated the "Build Anthropic Request" node to dynamically select content type:

```javascript
// Determine MIME type and content type for Anthropic API
let mimeType = 'application/pdf';
let contentType = 'document'; // default for PDFs

if (fileName.match(/\.jpe?g$/i)) {
  mimeType = 'image/jpeg';
  contentType = 'image';
} else if (fileName.match(/\.png$/i)) {
  mimeType = 'image/png';
  contentType = 'image';
} else if (fileName.match(/\.gif$/i)) {
  mimeType = 'image/gif';
  contentType = 'image';
} else if (fileName.match(/\.webp$/i)) {
  mimeType = 'image/webp';
  contentType = 'image';
}

// Then in requestBody:
{
  type: contentType, // 'document' for PDFs, 'image' for images
  source: {
    type: 'base64',
    media_type: mimeType,
    data: base64String
  }
}
```

## Current Status

✅ **Code verified in workflow** - The fix is present in the active version (versionId: d76c67d1-f8f2-4959-8006-d8527754d2ab)
✅ **Workflow is active** - Currently running
⚠️ **Needs testing** - Upload a test PDF to verify the fix works

## Testing Steps

1. Upload a PDF invoice to Downloads folder (Google Drive: 1O3udIURR14LsEP3Wt4o1QnxzGsR2gciN)
2. Wait for workflow trigger (polls every minute)
3. Check execution completes successfully
4. Verify Anthropic API accepts the request
5. Verify extraction results are logged to Google Sheets

## Troubleshooting

If error persists:

1. **Check execution details** - Look at the actual JSON being sent to Anthropic API
2. **Verify workflow version** - Ensure active version is d76c67d1-f8f2-4959-8006-d8527754d2ab
3. **Try manual execution** - Run workflow manually with test data to see if fix works
4. **Restart n8n** - If workflow cache is stale, restart n8n to reload code

## File Type Detection

The code detects file type by extension:
- `.pdf` → `type: "document"`, `media_type: "application/pdf"`
- `.jpg`, `.jpeg` → `type: "image"`, `media_type: "image/jpeg"`
- `.png` → `type: "image"`, `media_type: "image/png"`
- `.gif` → `type: "image"`, `media_type: "image/gif"`
- `.webp` → `type: "image"`, `media_type: "image/webp"`

All file types use the same binary data handling via `this.helpers.getBinaryDataBuffer()`.
