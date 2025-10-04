# Backup Sender SCP

A simple Python tool to automatically send new backup files from a local directory to a remote server via SSH/SCP. The script periodically checks for new `.bak` files and transfers them, along with log files, to a specified remote directory.

---

## Features

- **Automatic Backup Transfer:** Monitors a local backup folder and sends new backups to a remote server.
- **SCP over SSH:** Uses secure SSH/SCP for file transfer.
- **Log File Sync:** Sends specified log files with each new backup.
- **Environment Configuration:** All credentials and paths are managed via a `.env` file.

---

## How It Works

1. The script checks the backup directory every minute for new `.bak` files.
2. If new backups are found, it sends them to the remote server using SCP.
3. Alongside each backup, it also sends log files (`backup_fartak.log`, `backup.log`) if present.
4. Sent backups are tracked to avoid duplicate transfers.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/backup-sender-scp.git
cd backup-sender-scp
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with the following content:

```env
BACKUP_DIR=/path/to/local/backup/folder
REMOTE_HOST=your.remote.server
REMOTE_PORT=22
REMOTE_USER=your_ssh_username
REMOTE_PASSWORD=your_ssh_password
REMOTE_DIR=/path/to/remote/backup/folder
```

> **Note:** Never commit your `.env` file with sensitive credentials to public repositories.

### 5. Run the Script

```bash
python backup_sender.py
```

The script will now monitor your backup folder and send new backups to the remote server automatically.

---

## Requirements

- Python 3.6+
- [paramiko](https://pypi.org/project/paramiko/)
- [scp](https://pypi.org/project/scp/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

All dependencies are listed in `requirements.txt`.

---

## License

MIT License

---

## 🧑‍💻 Contribution

If you have suggestions or encounter an issue, please open a new Issue or submit a Pull Request.

---

## 📞 Contact

For questions or support, you can reach out via [GitHub Issues](https://github.com/ahamxdev/backup-telebot/issues) or directly contact the maintainer.

---

## 👤 Author

**Name:** AmirHossein AliMohammadi
**GitHub:** [github.com/ahamxdev](https://github.com/ahamxdev)

Good luck! 🚀
