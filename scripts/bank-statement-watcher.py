#!/usr/bin/env python3
"""
Bank Statement Folder Watcher
Watches a local folder for new PDF files and uploads them to n8n webhook.
Processes files sequentially with delays to avoid overwhelming the server.
"""

import argparse
import logging
import os
import queue
import shutil
import sys
import threading
import time
from pathlib import Path

import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration via environment variables
WATCH_FOLDER = os.environ.get(
    "BANK_STATEMENT_FOLDER",
    "/Users/swayclarke/bank_statements",
)
WEBHOOK_URL = os.environ.get(
    "BANK_STATEMENT_WEBHOOK_URL",
    "https://n8n.oloxa.ai/webhook/expense-bank-statement-upload",
)
LOG_FILE = os.path.expanduser("~/Library/Logs/bank-statement-watcher.log")

# Processing settings
MAX_RETRIES = 3
RETRY_DELAY = 30  # seconds between retries
BETWEEN_FILES_DELAY = 10  # seconds between processing files

# Setup logging
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("bank-statement-watcher")

# Queue for sequential processing
file_queue = queue.Queue()


def ensure_dirs(base: str):
    """Create watch folder and subfolders if needed."""
    for sub in ("", "processed", "errors"):
        os.makedirs(os.path.join(base, sub), exist_ok=True)


def is_valid_pdf(path: str) -> bool:
    name = os.path.basename(path)
    return name.lower().endswith(".pdf") and not name.startswith(".")


def upload_file(filepath: str) -> bool:
    """POST file to webhook. Returns True on success."""
    log.info("Uploading %s", filepath)
    try:
        with open(filepath, "rb") as f:
            resp = requests.post(
                WEBHOOK_URL,
                files={"data": (os.path.basename(filepath), f, "application/pdf")},
                timeout=180,
            )
        if resp.status_code == 200:
            log.info("Upload successful for %s: %s", filepath, resp.text[:200])
            return True
        else:
            log.error("Upload failed for %s: HTTP %s - %s", filepath, resp.status_code, resp.text[:500])
            return False
    except Exception as e:
        log.error("Upload error for %s: %s", filepath, e)
        return False


def process_file(filepath: str, base: str):
    """Upload a PDF with retries, then move to processed/ or errors/."""
    if not os.path.isfile(filepath):
        return
    if not is_valid_pdf(filepath):
        return

    log.info("Processing %s", filepath)
    time.sleep(2)  # wait for file to finish writing

    success = False
    for attempt in range(1, MAX_RETRIES + 1):
        success = upload_file(filepath)
        if success:
            break
        if attempt < MAX_RETRIES:
            log.info("Retry %d/%d for %s in %ds", attempt, MAX_RETRIES, filepath, RETRY_DELAY)
            time.sleep(RETRY_DELAY)

    dest_dir = os.path.join(base, "processed" if success else "errors")
    dest = os.path.join(dest_dir, os.path.basename(filepath))

    # Handle name collisions
    if os.path.exists(dest):
        stem = Path(dest).stem
        ext = Path(dest).suffix
        dest = os.path.join(dest_dir, f"{stem}_{int(time.time())}{ext}")

    try:
        shutil.move(filepath, dest)
        log.info("Moved %s -> %s", filepath, dest)
    except FileNotFoundError:
        log.warning("File already moved or deleted: %s", filepath)


def queue_worker(base: str):
    """Process files from queue sequentially with delays."""
    while True:
        filepath = file_queue.get()
        try:
            process_file(filepath, base)
            # Delay between files to avoid server overload
            if not file_queue.empty():
                log.info("Waiting %ds before next file...", BETWEEN_FILES_DELAY)
                time.sleep(BETWEEN_FILES_DELAY)
        except Exception as e:
            log.error("Unexpected error processing %s: %s", filepath, e)
        finally:
            file_queue.task_done()


class PDFHandler(FileSystemEventHandler):
    def __init__(self, base: str):
        self.base = base

    def on_created(self, event):
        if event.is_directory:
            return
        if is_valid_pdf(event.src_path):
            log.info("Queued: %s", event.src_path)
            file_queue.put(event.src_path)


def run_once(base: str):
    """Process all existing PDFs sequentially and exit."""
    log.info("Running once mode - processing existing PDFs in %s", base)
    count = 0
    files = sorted(
        f for f in os.listdir(base)
        if os.path.isfile(os.path.join(base, f)) and is_valid_pdf(os.path.join(base, f))
    )
    for name in files:
        filepath = os.path.join(base, name)
        process_file(filepath, base)
        count += 1
        if count < len(files):
            log.info("Waiting %ds before next file...", BETWEEN_FILES_DELAY)
            time.sleep(BETWEEN_FILES_DELAY)
    log.info("Processed %d files", count)


def watch(base: str):
    """Watch folder indefinitely for new PDFs."""
    log.info("Watching %s for new PDF files", base)

    # Start queue worker thread
    worker = threading.Thread(target=queue_worker, args=(base,), daemon=True)
    worker.start()

    observer = Observer()
    observer.schedule(PDFHandler(base), base, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("Shutting down watcher")
    observer.stop()
    observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bank statement folder watcher")
    parser.add_argument("--once", action="store_true", help="Process existing PDFs and exit")
    args = parser.parse_args()

    ensure_dirs(WATCH_FOLDER)
    log.info("Watch folder: %s", WATCH_FOLDER)
    log.info("Webhook URL: %s", WEBHOOK_URL)

    if args.once:
        run_once(WATCH_FOLDER)
    else:
        watch(WATCH_FOLDER)
