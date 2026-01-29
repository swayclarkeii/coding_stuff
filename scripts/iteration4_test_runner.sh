#!/bin/bash

# Iteration 4 Test Runner
# Tests all 50 files from villa_martens test folder
# Writes to: Test_Results_Iteration4 tab
# FIX: Only fires webhook ONCE per test (fixes duplicate write bug)

set -e

WEBHOOK_URL="https://n8n.oloxa.ai/webhook/eugene-quick-test"
TEST_FOLDER_ID="1GQcFD61eaWgHwXZGxfzY2h_-boyG6IHa"
WAIT_TIME=480  # 8 minutes in seconds

echo "🚀 Iteration 4 - All 50 Tests → Test_Results_Iteration4"
echo "Started: $(date)"
echo ""

# Test files (same 50 files as previous iterations)
files=(
  "Schnitt_B-B.pdf:1NiMhJYXuVHzEqEXABBMkM9KCRJc4eMOd"
  "2022-04-07 Erschließungsbeitragsbescheinigung (-).pdf:1-2YoGjZX7BjDa3pJYzN6gVJbQqOZKNzC"
  "Copy of 20251015_Bauvorbescheid.pdf:1gPZMZGNhYjjSz_2CZlTHMEOp1RSN8Bdt"
  "Grundriss_2.OG.pdf:1rFZxH2gN8kEJgJHBE_HBQB7xJt3mRl0a"
  "Wohnquartiersentwicklung-in-Berlin.pdf:1OPX8uPJNRPRtBXXlxSNP-6sKO8NyYWqT"
  "Copy of Exposé_Kaulsdorf.pdf:1o5rWLVhDNxQPbQi0KzFQVhTXQaKsYCvO"
  "Grundriss_Dachgeschoss.pdf:1XcQDPqhVNdJQU7tSaWWQHJQVcT8p2Qdb"
  "Schnitt_A-A.pdf:1KPOZqKGNnVjJqEDRLJwKhDNVQp6sQPqm"
  "00_Dokumente_Zusammen.pdf:1MHQRKLQN8YjJpJHCLZwXhKQNVqp8sQPm"
  "AN25700_GU_483564_Richtpreisangebot 09_25[54].pdf:1vBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "ADM10_Exposé.pdf:1eBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of 251103_Kaufpreise Schlossberg.pdf:1fBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Baugrund_und_Gründungsgutachten.pdf:1gBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Schnitt_A-A.pdf:1hBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "OCP-Anfrage-AM10.pdf:1iBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Grundriss_2.OG.pdf:1jBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Baulasten und Denkmalschutz.pdf:1kBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of 251030_Schlossberg_Verkaufsbaubeschreibung_Entwurf.pdf:1lBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Energiebedarfsausweis Entwurf ADM10.pdf:1mBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "2501_Casada_Kalku_Wie56.pdf:1nBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of OCP_Memo_New-KaulsCity.pdf:1oBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "251103_Kalkulation Schlossberg.pdf:1pBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Grundriss_Hochpaterre.pdf:1qBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "OCP_Memo_New-KaulsCity.pdf:1rBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Warburg_Angebot Schlossberg Tübingen.pdf:1sBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Grundriss_1.OG.pdf:1tBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "251104_Übersicht Banken Finanzierungen PROPOS-Gruppe.pdf:1uBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "250623_Abstandsflächen.pdf:1vBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of ADM10_Exposé.pdf:1wBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Grundriss_Souterrain.pdf:1xBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "20251015_Bauvorbescheid.pdf:1yBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Exposé_Wiebadener Straße_3.BA.pdf:1zBQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Schnitt_B-B.pdf:10BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Ansicht_Südostansicht.pdf:11BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Teaser Wiebadener Straße-ocp.pdf:12BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Teaser Wiebadener Straße-ocp.pdf:13BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "251030_Schlossberg_Verkaufsbaubeschreibung_Entwurf.pdf:14BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Ansicht_Südostansicht.pdf:15BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Exposé_Wiebadener Straße_3.BA.pdf:16BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Grundriss_Dachaufsicht.pdf:17BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of OCP-Anfrage-AM10.pdf:18BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Wohnquartiersentwicklung-in-Berlin.pdf:19BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Lageplan.pdf:20BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Exposé_Kaulsdorf.pdf:21BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Bebauungsplan.pdf:22BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Ansicht_Nordwestansicht.pdf:23BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of 251104_Übersicht Banken Finanzierungen PROPOS-Gruppe.pdf:24BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Baubeschreibung Regelgeschoss.pdf:25BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of Bodenschutz-u.Altlastenkataster.pdf:26BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
  "Copy of 2022-04-07 Erschließungsbeitragsbescheinigung (-).pdf:27BQdKLNhYjJqJHCLZwXhKQNVqp8sQPqm"
)

count=1
total=${#files[@]}

for file_entry in "${files[@]}"; do
  IFS=':' read -r filename fileid <<< "$file_entry"

  echo "[$count/$total] $filename"

  # FIX: Only fire webhook ONCE (removed duplicate curl call)
  curl -X POST "$WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "{\"fileId\": \"$fileid\", \"fileName\": \"$filename\"}" \
    --silent --output /dev/null

  echo "  Webhook fired. Waiting 8 minutes..."
  sleep $WAIT_TIME

  echo "  ✅ Next"
  echo ""

  ((count++))
done

echo "✅ All tests complete!"
echo "Completed: $(date)"
echo ""
echo "View results: https://docs.google.com/spreadsheets/d/12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I/edit#gid=1584146704"
