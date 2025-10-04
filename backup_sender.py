#!/usr/bin/env python3
# backup_sender.py

import os
import time
from datetime import datetime, timezone
from paramiko import SSHClient, AutoAddPolicy, SSHException
from scp import SCPClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Remote server settings
LOCAL_DIR = os.getenv("BACKUP_DIR")
REMOTE_HOST = os.getenv("REMOTE_HOST")
REMOTE_PORT = int(os.getenv("REMOTE_PORT", 22))
REMOTE_USER = os.getenv("REMOTE_USER")
REMOTE_PASSWORD = os.getenv("REMOTE_PASSWORD")
REMOTE_DIR = os.getenv("REMOTE_DIR")

LOG_FILES = ["backup_fartak.log", "backup.log"]

# ---- Schedule settings ----
CHECK_MINUTE_UTC = 10   # Run every hour at minute 10 (e.g., 00:10, 01:10, 02:10)
FILE_STABLE_MINUTES = 5 # File must be unchanged for at least 5 minutes

sent_files = set()

def send_file(local_path, remote_path):
    """Send a file via SCP."""
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(REMOTE_HOST, port=REMOTE_PORT, username=REMOTE_USER, password=REMOTE_PASSWORD)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(local_path, remote_path)
    ssh.close()
    print(f"✅ Sent: {local_path}")

def is_file_stable(file_path):
    """Check if file hasn't changed for FILE_STABLE_MINUTES."""
    mtime = os.path.getmtime(file_path)
    age_minutes = (time.time() - mtime) / 60
    return age_minutes >= FILE_STABLE_MINUTES

def process_backups():
    """Check directory for new backups and send them."""
    global sent_files

    print("🔍 Checking for new backup files...")
    all_files = [f for f in os.listdir(LOCAL_DIR) if f.endswith(".bak")]
    new_files = [f for f in all_files if f not in sent_files]

    if not new_files:
        print("No new backups found.")
        return

    try:
        for f in new_files:
            local_path = os.path.join(LOCAL_DIR, f)
            remote_path = os.path.join(REMOTE_DIR, f)

            if not is_file_stable(local_path):
                print(f"⚠️ Skipping {f} — file still being written.")
                continue

            send_file(local_path, remote_path)

            # Send logs
            for log_file in LOG_FILES:
                log_local_path = os.path.join(LOCAL_DIR, log_file)
                if os.path.exists(log_local_path) and is_file_stable(log_local_path):
                    send_file(log_local_path, os.path.join(REMOTE_DIR, log_file))

            sent_files.add(f)

    except SSHException as e:
        print(f"❌ SSH connection failed: {e}")

def main():
    """Send all existing backups once, then check hourly at minute X."""
    # Step 1: Send all existing backups immediately
    print("🚀 Initial run: sending all existing backups...")
    process_backups()

    # Step 2: Then check every hour at CHECK_MINUTE_UTC
    print(f"⏰ Scheduled to run at minute {CHECK_MINUTE_UTC:02d} of every UTC hour...")
    while True:
        now_utc = datetime.now(timezone.utc)
        if now_utc.minute == CHECK_MINUTE_UTC:
            process_backups()
            print("⏳ Waiting until next hour...")
            time.sleep(3000)  # Wait ~50 minutes to avoid multiple runs in the same hour
        else:
            time.sleep(60)

if __name__ == "__main__":
    main()
