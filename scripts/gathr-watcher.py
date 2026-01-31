#!/usr/bin/env python3
"""
Gathr Folder Watcher
Watches local folders for new PDF files and uploads them to n8n webhooks.
Supports multiple watched folders with different webhook endpoints.
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

# ── Folder Configurations ──────────────────────────────────────────
GATHR_BASE = os.environ.get("GATHR_BASE", "/Users/swayclarke/gathr")

WATCHERS = {
    "bank_statements": {
        "folder": os.path.join(GATHR_BASE, "bank_statements"),
        "webhook": os.environ.get(
            "BANK_STATEMENT_WEBHOOK",
            "https://n8n.oloxa.ai/webhook/expense-bank-statement-upload",
        ),
        "extensions": [".pdf"],
    },
    "receipts_invoices": {
        "folder": os.path.join(GATHR_BASE, "receipts_invoices"),
        "webhook": os.environ.get(
            "RECEIPTS_WEBHOOK",
            "https://n8n.oloxa.ai/webhook/expense-receipts-upload",
        ),
        "extensions": [".pdf"],
    },
}

LOG_FILE = os.path.expanduser("~/Library/Logs/gathr-watcher.log")

# Processing settings
MAX_RETRIES = 3
RETRY_DELAY = 30
BETWEEN_FILES_DELAY = 10
UPLOAD_TIMEOUT = 300  # 5 minutes - large PDFs need time for Anthropic Vision

# ── Logging ────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout),
    ],
)
log = logging.getLogger("gathr-watcher")

# Queue for sequential processing
file_queue = queue.Queue()


def ensure_dirs(base: str):
    for sub in ("", "processed", "errors"):
        os.makedirs(os.path.join(base, sub), exist_ok=True)


def is_valid_file(path: str, extensions: list) -> bool:
    name = os.path.basename(path)
    if name.startswith("."):
        return False
    return any(name.lower().endswith(ext) for ext in extensions)


def upload_file(filepath: str, webhook_url: str) -> bool:
    log.info("Uploading %s -> %s", filepath, webhook_url)
    try:
        with open(filepath, "rb") as f:
            resp = requests.post(
                webhook_url,
                files={"data": (os.path.basename(filepath), f, "application/pdf")},
                timeout=UPLOAD_TIMEOUT,
            )
        if resp.status_code == 200:
            log.info("Upload successful for %s: %s", filepath, resp.text[:200])
            return True
        else:
            log.error(
                "Upload failed for %s: HTTP %s - %s",
                filepath, resp.status_code, resp.text[:500],
            )
            return False
    except Exception as e:
        log.error("Upload error for %s: %s", filepath, e)
        return False


def process_file(filepath: str, base: str, webhook_url: str):
    if not os.path.isfile(filepath):
        return
    log.info("Processing %s", filepath)
    time.sleep(2)  # wait for file to finish writing

    success = False
    for attempt in range(1, MAX_RETRIES + 1):
        success = upload_file(filepath, webhook_url)
        if success:
            break
        if attempt < MAX_RETRIES:
            log.info("Retry %d/%d for %s in %ds", attempt, MAX_RETRIES, filepath, RETRY_DELAY)
            time.sleep(RETRY_DELAY)

    dest_dir = os.path.join(base, "processed" if success else "errors")
    dest = os.path.join(dest_dir, os.path.basename(filepath))

    if os.path.exists(dest):
        stem = Path(dest).stem
        ext = Path(dest).suffix
        dest = os.path.join(dest_dir, f"{stem}_{int(time.time())}{ext}")

    try:
        shutil.move(filepath, dest)
        log.info("Moved %s -> %s", filepath, dest)
    except FileNotFoundError:
        log.warning("File already moved or deleted: %s", filepath)


def queue_worker():
    while True:
        filepath, base, webhook_url = file_queue.get()
        try:
            process_file(filepath, base, webhook_url)
            if not file_queue.empty():
                log.info("Waiting %ds before next file...", BETWEEN_FILES_DELAY)
                time.sleep(BETWEEN_FILES_DELAY)
        except Exception as e:
            log.error("Unexpected error processing %s: %s", filepath, e)
        finally:
            file_queue.task_done()


class FileHandler(FileSystemEventHandler):
    def __init__(self, base: str, webhook_url: str, extensions: list):
        self.base = base
        self.webhook_url = webhook_url
        self.extensions = extensions

    def on_created(self, event):
        if event.is_directory:
            return
        if is_valid_file(event.src_path, self.extensions):
            log.info("Queued: %s", event.src_path)
            file_queue.put((event.src_path, self.base, self.webhook_url))


def run_once(watcher_names: list):
    for name in watcher_names:
        cfg = WATCHERS[name]
        base = cfg["folder"]
        webhook = cfg["webhook"]
        extensions = cfg["extensions"]
        ensure_dirs(base)

        log.info("Processing existing files in %s -> %s", base, webhook)
        files = sorted(
            f for f in os.listdir(base)
            if os.path.isfile(os.path.join(base, f)) and is_valid_file(f, extensions)
        )
        if not files:
            log.info("No files found in %s", base)
            continue

        count = 0
        for fname in files:
            filepath = os.path.join(base, fname)
            process_file(filepath, base, webhook)
            count += 1
            if count < len(files):
                log.info("Waiting %ds before next file...", BETWEEN_FILES_DELAY)
                time.sleep(BETWEEN_FILES_DELAY)
        log.info("Processed %d files from %s", count, name)


def watch(watcher_names: list):
    worker = threading.Thread(target=queue_worker, daemon=True)
    worker.start()

    observer = Observer()
    for name in watcher_names:
        cfg = WATCHERS[name]
        base = cfg["folder"]
        ensure_dirs(base)
        handler = FileHandler(base, cfg["webhook"], cfg["extensions"])
        observer.schedule(handler, base, recursive=False)
        log.info("Watching %s -> %s", base, cfg["webhook"])

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("Shutting down watcher")
    observer.stop()
    observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gathr folder watcher")
    parser.add_argument("--once", action="store_true", help="Process existing files and exit")
    parser.add_argument(
        "--folders", nargs="+", choices=list(WATCHERS.keys()) + ["all"],
        default=["all"],
        help="Which folders to watch (default: all)",
    )
    args = parser.parse_args()

    folder_names = list(WATCHERS.keys()) if "all" in args.folders else args.folders

    for name in folder_names:
        cfg = WATCHERS[name]
        log.info("Folder: %s -> %s", cfg["folder"], cfg["webhook"])

    if args.once:
        run_once(folder_names)
    else:
        watch(folder_names)
