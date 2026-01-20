#!/bin/bash

# Eugene Document Organizer - Workflow Backup Script
# Run this when n8n database is available

API_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlOWJkOTExMi1jMmUzLTRmNjctODczYS1lMTAwMWJhZWFmZDgiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY3MzgzODM0fQ.EDsEy9tZ-kHtpzir8jD_I-I3YbKgtOJcx_ZmH5SZLT4"
BASE_URL="https://n8n.oloxa.ai"
BACKUP_DIR="/Users/swayclarke/coding_stuff/claude-code-os/02-operations/technical-builds/eugene/N8N_Blueprints/v5_phase1"
DATE=$(date +%Y%m%d)

echo "Eugene Document Organizer - Workflow Backup"
echo "==========================================="
echo ""

# Check if database is available
echo "Checking n8n database availability..."
response=$(curl -s "$BASE_URL/api/v1/workflows/YGXWjWcBIk66ArvT" -H "X-N8N-API-KEY: $API_KEY")

if echo "$response" | grep -q "Database is not ready"; then
  echo "✗ n8n database is still unavailable"
  echo "Please try again in a few minutes."
  exit 1
fi

echo "✓ Database is available"
echo ""

# Backup Pre-Chunk 0
echo "Backing up Pre-Chunk 0 (YGXWjWcBIk66ArvT)..."
curl -s "$BASE_URL/api/v1/workflows/YGXWjWcBIk66ArvT" \
  -H "X-N8N-API-KEY: $API_KEY" \
  -o "$BACKUP_DIR/pre-chunk-0_v5.0_$DATE.json"

if [ $? -eq 0 ] && [ -s "$BACKUP_DIR/pre-chunk-0_v5.0_$DATE.json" ]; then
  size=$(stat -f%z "$BACKUP_DIR/pre-chunk-0_v5.0_$DATE.json" 2>/dev/null || stat -c%s "$BACKUP_DIR/pre-chunk-0_v5.0_$DATE.json")
  echo "✓ Pre-Chunk 0 backed up ($size bytes)"
else
  echo "✗ Pre-Chunk 0 backup failed"
fi

sleep 1

# Backup Chunk 2
echo "Backing up Chunk 2 (g9J5kjVtqaF9GLyc)..."
curl -s "$BASE_URL/api/v1/workflows/g9J5kjVtqaF9GLyc" \
  -H "X-N8N-API-KEY: $API_KEY" \
  -o "$BACKUP_DIR/chunk-2_v5.0_$DATE.json"

if [ $? -eq 0 ] && [ -s "$BACKUP_DIR/chunk-2_v5.0_$DATE.json" ]; then
  size=$(stat -f%z "$BACKUP_DIR/chunk-2_v5.0_$DATE.json" 2>/dev/null || stat -c%s "$BACKUP_DIR/chunk-2_v5.0_$DATE.json")
  echo "✓ Chunk 2 backed up ($size bytes)"
else
  echo "✗ Chunk 2 backup failed"
fi

sleep 1

# Backup Chunk 2.5
echo "Backing up Chunk 2.5 (okg8wTqLtPUwjQ18)..."
curl -s "$BASE_URL/api/v1/workflows/okg8wTqLtPUwjQ18" \
  -H "X-N8N-API-KEY: $API_KEY" \
  -o "$BACKUP_DIR/chunk-2.5_v5.0_$DATE.json"

if [ $? -eq 0 ] && [ -s "$BACKUP_DIR/chunk-2.5_v5.0_$DATE.json" ]; then
  size=$(stat -f%z "$BACKUP_DIR/chunk-2.5_v5.0_$DATE.json" 2>/dev/null || stat -c%s "$BACKUP_DIR/chunk-2.5_v5.0_$DATE.json")
  echo "✓ Chunk 2.5 backed up ($size bytes)"
else
  echo "✗ Chunk 2.5 backup failed"
fi

echo ""
echo "Backup complete!"
echo ""
echo "Files saved to:"
ls -lh "$BACKUP_DIR/"*_v5.0_$DATE.json 2>/dev/null || echo "No backups created"
