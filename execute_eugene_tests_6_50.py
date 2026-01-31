#!/usr/bin/env python3
"""
Eugene Quick Test Runner - Tests 6-50
Triggers 45 tests with 30-second spacing
"""

import requests
import time
from datetime import datetime
import json

WEBHOOK_URL = "https://n8n.oloxa.ai/webhook/eugene-quick-test"
START_TEST = 6
END_TEST = 50
DELAY_BETWEEN_TESTS = 30  # seconds

LOG_FILE = "/Users/swayclarke/coding_stuff/eugene_tests_6_50_execution.log"

def log(message):
    """Log to both console and file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    with open(LOG_FILE, 'a') as f:
        f.write(log_message + "\n")

def trigger_test(test_number):
    """Trigger a single test via webhook"""
    try:
        response = requests.post(
            WEBHOOK_URL,
            json={},
            timeout=30
        )
        return {
            'success': True,
            'status_code': response.status_code,
            'response': response.text[:200]  # First 200 chars
        }
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Timeout after 30 seconds'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Main execution loop"""
    log("=" * 60)
    log("Eugene Quick Test Runner - Tests 6-50")
    log(f"Triggering {END_TEST - START_TEST + 1} tests")
    log(f"Delay between tests: {DELAY_BETWEEN_TESTS} seconds")
    log("=" * 60)

    results = {
        'triggered': 0,
        'failed': 0,
        'errors': []
    }

    for test_num in range(START_TEST, END_TEST + 1):
        log(f"Test {test_num}: Triggering webhook...")

        result = trigger_test(test_num)

        if result['success']:
            log(f"  ✓ HTTP {result['status_code']} - Triggered successfully")
            results['triggered'] += 1
        else:
            log(f"  ✗ Failed: {result.get('error', 'Unknown error')}")
            results['failed'] += 1
            results['errors'].append({
                'test': test_num,
                'error': result.get('error')
            })

        # Progress report every 5 tests
        if (test_num - START_TEST + 1) % 5 == 0:
            completed = test_num - START_TEST + 1
            remaining = END_TEST - test_num
            log("")
            log(f">>> PROGRESS: {completed}/45 tests triggered ({remaining} remaining)")
            log(f"    Success: {results['triggered']}, Failed: {results['failed']}")
            log("")

        # Wait before next test (unless it's the last one)
        if test_num < END_TEST:
            time.sleep(DELAY_BETWEEN_TESTS)

    # Final summary
    log("")
    log("=" * 60)
    log("EXECUTION COMPLETE")
    log(f"Total tests triggered: {results['triggered']}")
    log(f"Total failed: {results['failed']}")
    log("=" * 60)

    if results['errors']:
        log("")
        log("Failed tests:")
        for err in results['errors']:
            log(f"  Test {err['test']}: {err['error']}")

    log("")
    log("Next steps:")
    log("1. Tests will complete over next 30-45 minutes")
    log("2. Check Google Sheet: 12N2C8iWeHkxJQ2qz7m3aTyZw3X1gXbyyyFa-rP0tD7I")
    log("3. Monitor n8n executions for failures")

    # Save summary JSON
    summary_file = "/Users/swayclarke/coding_stuff/eugene_tests_6_50_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(results, f, indent=2)
    log(f"Summary saved to: {summary_file}")

if __name__ == "__main__":
    main()
