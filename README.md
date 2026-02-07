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
Open your terminal and run the following commands:

```bash
git clone https://github.com/YOUR_USERNAME/Synapse.git
cd Synapse

### 2. Configure Settings

Edit the `config.json` file to set your target directory and Discord Webhook URL.

```json
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

```bash
python main.py


![alt text](image.png)

🧠 How It Works
1. Baseline Creation: On the first run, Synapse calculates SHA-256 hashes of all target files and saves them to a secure local database (data/baseline.json).

2. Continuous Polling: The system wakes up every X seconds (defined in config) to re-scan the directory.

3. Comparison Logic:

  • New File: Present in current scan but missing in baseline.

  • Deleted File: Present in baseline but missing in current scan.

  • Modified File: Hash mismatch between baseline and current scan.

4. Alerting: If a deviation is detected, it logs to the console and sends a payload to the Discord Webhook.


⚠️ Disclaimer
This tool is developed for educational and defensive purposes only. The developer is not responsible for any misuse of this software.


📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

