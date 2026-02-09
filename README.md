# 🛡️ SYNAPSE - File Integrity Monitor (FIM)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Security](https://img.shields.io/badge/Security-Blue%20Team-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=for-the-badge)

**Synapse**, a lightweight, zero-dependency File Integrity Monitoring (FIM) tool written in Python. It detects unauthorized file creations, modifications, and deletions in real-time using SHA-256 hashing algorithms.

Designed for **Blue Team** operations and **PCI-DSS** compliance monitoring needs.

---

## 🚀 Features

- **🔎 Real-Time Monitoring:** Continuously scans critical directories for changes.
- **🔐 SHA-256 Hashing:** Uses cryptographic hashing to detect even the slightest byte-level modifications.
- **⚡ Memory Efficient:** Implements "Chunking" (4KB blocks) to handle large files (GBs/TBs) without memory overflow.
- **🔔 Discord Integration:** Sends instant alerts to your Discord channel via Webhooks.
- **⚙️ Configurable:** JSON-based configuration for easy management without touching the code.
- **📦 Zero Dependencies:** Runs on standard Python libraries (`hashlib`, `json`, `os`, `urllib`). No `pip install` required.

---

## 🛠️ Installation & Usage

### 1. Clone the Repository
 ```bash
 git clone [https://github.com/SuatKoray/Synapse.git](https://github.com/SuatKoray/Synapse.git)
 cd Synapse
```

### 2. Configure Settings
Rename config.example.json to config.json and edit it with your preferences.

JSON

{
    "monitor_path": ".",
    "file_extensions": [".txt", ".py", ".json", ".exe"],
    "webhook_url": "YOUR_DISCORD_WEBHOOK_URL_HERE",
    "monitoring_interval": 5,
    "log_file": "logs/synapse.log",
    "db_file": "data/baseline.json"
}

### 3. Run Synapse
Simply run the script with Python:

Bash

python main.py


![alt text](image.png)

🧠 How It Works
Baseline Creation: On the first startup, Synapse calculates SHA-256 hashes of all target files and saves them to a secure local database (data/baseline.json).

Continuous Polling: The system wakes up every X seconds (defined in config) to silently re-scan the directory.

Comparison Logic:

⚠️ New File: File exists in current scan but missing in baseline.

🚨 Deleted File: File exists in baseline but missing in current scan.

🔥 Modified File: Hash mismatch between baseline and current scan (Critical).

Alerting: If a deviation is detected, it logs to the console and pushes a payload to the Discord Webhook.

⚠️ Disclaimer
This tool is developed for educational and defensive purposes only. The developer is not responsible for any misuse of this software. Always obtain permission before monitoring systems you do not own.

📜 License
This project is licensed under the MIT License - see the [LICENCE](LICENCE) file for details.