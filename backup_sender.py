#!/usr/bin/env python3
# backup_sender.py

import os
import time
from paramiko import SSHClient, AutoAddPolicy, SSHException
from scp import SCPClient
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Remote server settings
LOCAL_DIR = os.getenv("BACKUP_DIR")  # Now from .env
REMOTE_HOST = os.getenv("REMOTE_HOST")
REMOTE_PORT = int(os.getenv("REMOTE_PORT", 22))
REMOTE_USER = os.getenv("REMOTE_USER")
REMOTE_PASSWORD = os.getenv("REMOTE_PASSWORD")
REMOTE_DIR = os.getenv("REMOTE_DIR")

LOG_FILES = ["backup_fartak.log", "backup.log"]

# Keep track of sent files
sent_files = set()

def send_file(local_path, remote_path):
    """Send a file via SCP."""
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(REMOTE_HOST, port=REMOTE_PORT, username=REMOTE_USER, password=REMOTE_PASSWORD)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(local_path, remote_path)
    ssh.close()
    print(f"Sent: {local_path}")

def main():
    """Monitor backup folder and send new backups with logs every minute."""
    global sent_files

    while True:
        # List all backup files
        all_files = [f for f in os.listdir(LOCAL_DIR) if f.endswith(".bak")]
        
        # Filter unsent files
        new_files = [f for f in all_files if f not in sent_files]

        if new_files:
            try:
                for f in new_files:
                    local_path = os.path.join(LOCAL_DIR, f)
                    remote_path = os.path.join(REMOTE_DIR, f)
                    send_file(local_path, remote_path)

                    # Send logs with new backup
                    for log_file in LOG_FILES:
                        log_local_path = os.path.join(LOCAL_DIR, log_file)
                        if os.path.exists(log_local_path):
                            send_file(log_local_path, os.path.join(REMOTE_DIR, log_file))

                    # Mark backup as sent
                    sent_files.add(f)

            except SSHException as e:
                print(f"SSH connection failed: {e}. Retrying in 1 minute.")
        else:
            print("No new backups found.")

        time.sleep(60)

if __name__ == "__main__":
    main()
