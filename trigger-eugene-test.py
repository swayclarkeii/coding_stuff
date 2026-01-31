#!/usr/bin/env python3
import requests
import sys
from datetime import datetime

webhook_url = "https://n8n.oloxa.ai/webhook/eugene-quick-test"

test_number = sys.argv[1] if len(sys.argv) > 1 else "unknown"

print(f"[Test {test_number}] Triggering webhook at {datetime.now().strftime('%H:%M:%S')}")

try:
    response = requests.post(webhook_url, json={}, timeout=30)
    print(f"[Test {test_number}] Response status: {response.status_code}")
    print(f"[Test {test_number}] Response body: {response.text}")
except Exception as e:
    print(f"[Test {test_number}] ERROR: {str(e)}")
    sys.exit(1)
