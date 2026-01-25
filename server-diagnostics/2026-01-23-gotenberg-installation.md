# Server Maintenance Report - Gotenberg Installation

## Task
Install Gotenberg document conversion service on n8n server

## Date
2026-01-23

## Status
**Result:** Success

All tasks completed successfully.

## Summary

Added Gotenberg document conversion service to the n8n server's docker-compose.yml configuration. Gotenberg is now running and accessible to n8n workflows for converting Office documents (xlsx, docx, etc.) to PDF.

## Actions Taken

1. **SSH Connection**
   - Connected to server: 157.230.21.230 (root access)
   - Used SSH key: `~/.ssh/digitalocean_n8n`

2. **Verified Current State**
   - Checked n8n API health: Healthy (v2.33.4)
   - Read existing docker-compose.yml structure
   - Confirmed existing services: postgres, n8n

3. **Updated docker-compose.yml**
   - Added Gotenberg service with configuration:
     - Image: gotenberg/gotenberg:8
     - Restart policy: always
     - Ports: 3000:3000 (exposed to host)
     - Command options:
       - `--chromium-disable-javascript=true` (security)
       - `--api-timeout=300s` (5 minute timeout for large conversions)
     - Network: n8n-network (shared with n8n and postgres)

4. **Started Gotenberg Service**
   - Ran: `docker compose up -d`
   - Successfully pulled gotenberg/gotenberg:8 image
   - Container started: n8n-gotenberg-1

5. **Verified Installation**
   - Container status: Up and running
   - Health check: Passed (chromium and libreoffice both up)
   - Network connectivity: Confirmed all containers on n8n-network
   - Container IPs:
     - n8n-postgres-1: 172.18.0.2/16
     - n8n-n8n-1: 172.18.0.3/16
     - n8n-gotenberg-1: 172.18.0.4/16

## Service Details

**Gotenberg Container:**
- Name: n8n-gotenberg-1
- Image: gotenberg/gotenberg:8
- Status: Up
- Ports: 0.0.0.0:3000->3000/tcp, [::]:3000->3000/tcp
- Network: n8n-network

**Gotenberg Health Status:**
```json
{
  "status": "up",
  "details": {
    "chromium": {
      "status": "up",
      "timestamp": "2026-01-23T18:16:13.381238328Z"
    },
    "libreoffice": {
      "status": "up",
      "timestamp": "2026-01-23T18:16:13.38123226Z"
    }
  }
}
```

## n8n Integration

**How to use Gotenberg in n8n workflows:**

1. **HTTP Request Node Configuration:**
   - Method: POST
   - URL: `http://gotenberg:3000/forms/libreoffice/convert`
   - Authentication: None required
   - Body Type: Multipart Form Data

2. **Example: Convert XLSX to PDF:**
   ```
   URL: http://gotenberg:3000/forms/libreoffice/convert
   Method: POST
   Body:
     - files: [binary data from previous node]
   ```

3. **Example: Convert DOCX to PDF:**
   ```
   URL: http://gotenberg:3000/forms/libreoffice/convert
   Method: POST
   Body:
     - files: [binary data from previous node]
   ```

4. **Response:**
   - Returns PDF as binary data
   - Can be saved using Write Binary File node
   - Or sent via email, uploaded to cloud storage, etc.

## Notes

- Gotenberg is accessible from n8n at `http://gotenberg:3000` (internal Docker network)
- Also accessible from host at `http://localhost:3000` or `http://157.230.21.230:3000`
- Supports LibreOffice conversions (docx, xlsx, pptx, etc. to PDF)
- Supports Chromium conversions (HTML to PDF)
- API timeout set to 300 seconds for large file conversions
- JavaScript disabled in Chromium for security

## Next Steps

- Use Gotenberg in n8n workflows via HTTP Request nodes
- Test conversions with actual Office files
- Monitor resource usage if processing large files frequently

## Server Health After Installation

- **n8n API**: Healthy
- **Disk Space**: Not checked (no issues reported)
- **Container Status**:
  - n8n-postgres-1: Up (healthy)
  - n8n-n8n-1: Up
  - n8n-gotenberg-1: Up
- **Network**: All containers on n8n-network

---

**Maintenance performed by:** server-ops-agent
**Documentation:** /Users/swayclarke/coding_stuff/server-diagnostics/2026-01-23-gotenberg-installation.md
