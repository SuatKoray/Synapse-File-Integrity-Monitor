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
git clone [https://github.com/YOUR_USERNAME/Synapse.git](https://github.com/YOUR_USERNAME/Synapse.git)
cd Synapse