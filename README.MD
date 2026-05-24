# Integrated Password Security Suite & Mini-SIEM Dashboard

A local Security Operations Center (SOC) simulation environment and defensive security toolkit. This project features a robust password complexity analyzer, an encrypted local credential logging system, a multi-threaded port scanner, and a centralized mini-SIEM layout that tracks, ingests, and alerts on local authentication and network event activities.

---

## 🛠️ System Architecture & Features

### 1. Advanced Password Analyzer (`checker.py`, `password.py`)
*   **Entropy & Complexity Evaluation:** Checks password strength based on length, character variation (uppercase, lowercase, digits, and special characters).
*   **Encrypted Log Management:** Utilizes Fernet symmetric encryption (`cryptography` library) to securely archive local analysis histories into `password_history.enc` using a protected `secret.key`.

### 2. Multi-Threaded Port Scanner (`modules/port_scanner.py`)
*   **Network Footprinting:** Scans targets for open ports to identify potentially vulnerable entry points or misconfigured services.
*   **SIEM Event Forwarding:** Automatically generates structured event signatures for every scan performed, tracking target scopes and connection states.

### 3. Mini-SIEM & Log Ingestion Engine (`mini_siem/app.py`)
*   **Centralized Ingestion:** Monitors log pipelines (`logs.json`) to parse and record activities generated across security modules.
*   **Rule-Based Alerting:** Employs basic security analytics rules to tag incoming events with severity flags (`INFO`, `WARNING`, `CRITICAL`), mocking a real-world SOC monitoring experience.
*   **Web Dashboard Interface:** A local Flask web portal displaying real-time security events, authentication timelines, and system health statistics.

---

## 🚀 Getting Started

### Prerequisites
Ensure you have Python 3.x installed along with the required libraries. This environment is built and tested on **Kali Linux**.

```bash
pip install flask cryptography
