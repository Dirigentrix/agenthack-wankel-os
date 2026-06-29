# 🌀 WANKEL OS: Continuous Cold Chain Compliance

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Dirigentrix/agenthack-wankel-os/blob/main/LICENSE)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/release/python-314/)
[![UiPath AgentHack](https://img.shields.io/badge/Hackathon-UiPath%20AgentHack-orange)](https://agenthack.devpost.com/)

**WANKEL OS** (Stabilized Operational Integration Flow) is a master-level hybrid architecture designed for **Continuous Cold Chain Compliance (C4)**. Developed for the UiPath AgentHack, it bridges local SCADA-level telemetry with cloud-based orchestration to ensure rigorous HACCP (Hazard Analysis and Critical Control Points) validation in real-time.

---

## 🚀 Project Vision: Continuous Cold Chain Compliance

In the pharmaceutical and high-end food industries, a single temperature deviation can result in millions of dollars in losses and significant safety risks. **WANKEL OS** solves this by treating compliance not as a static record, but as a continuous, agentic process.

### Core Innovation: The Local/Cloud Bridge
- **Local (The "Organism"):** Edge-running Python 3.14 agents (`agro_organism_00`) monitor CCPs (Critical Control Points) and sensor health.
- **Cloud (The "Maestro"):** UiPath Maestro orchestrates high-level business logic, exception handling, and cross-system handoffs.

---

## 🛠 UiPath Ecosystem Integration

WANKEL OS leverages the full UiPath Agentic Platform to move beyond traditional RPA into true autonomous orchestration.

| Component | Role in WANKEL OS |
| :--- | :--- |
| **UiPath Maestro** | The central nervous system. Orchestrates dynamic workflows between local Python agents and human stakeholders. |
| **Agent Builder** | Used to define the decision-making logic and safety guardrails for the autonomous compliance agents. |
| **Coded Agents** | The engine. High-performance, specialized agents written in Python that handle the complex HACCP validation logic and telemetry processing. |

**Agent Type:** `Coded Agents` (Python-based for maximum flexibility and SCADA integration).

---

## 📂 Repository Structure

```text
.
├── main.py                 # Core Flask-based API for the C4 Bridge
├── agro_organism_00/       # Edge Agent deployment (Mocked for SCADA-local)
│   └── main.py             # Agent execution loop
├── config/                 # YAML-based HACCP and SCADA configurations
├── scada_docs/             # HACCP logic and document automation engine
├── uipath-adapter/         # Integration hooks for UiPath Maestro/Coded Agents
└── visualization_core.py   # Telemetry visualization and reporting engine
```

---

## 🔧 Setup & Execution (Python 3.14)

Follow these steps to deploy the **agro_organism_00** compliance agent and the WANKEL OS bridge.

### 1. Prerequisites
- Python 3.14+
- `pip` (Python package manager)

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone https://github.com/Dirigentrix/agenthack-wankel-os.git
cd agenthack-wankel-os
pip install -r requirements.txt
```

### 3. Configure the Agent
Ensure your HACCP parameters are set in `config/peklownia_config.yaml`. The system expects critical temperature thresholds for the `agro_organism_00` environment.

### 4. Running the WANKEL Bridge
Start the main integration server:
```bash
python main.py
```
The bridge will start on `http://0.0.0.0:8080`, ready to receive telemetry from local sensors and instructions from **UiPath Maestro**.

### 5. Executing the Edge Agent (agro_organism_00)
To simulate or run the edge monitoring agent:
```bash
cd agro_organism_00
python main.py
```

---

## 📜 HACCP Validation Logic
The system validates incoming data against:
- **CCP-1 (Cold Storage):** Range -18°C to -24°C.
- **CCP-2 (Processing):** Max +4°C.
- **Sensor Integrity:** Automatic detection of sensor drift or "frozen" values.

---

## 🏆 Devpost Submission Details
This repository is the official technical core for the **DARTRIX OS / WANKEL OS** submission to the UiPath AgentHack. 

**Team:** Dirigentrix
**Project:** Continuous Cold Chain Compliance (C4)
**Tech Stack:** Python 3.14, UiPath Maestro, Agent Builder, Flask, YAML.

---
*Built with ❤️ by the Dirigentrix Team for a safer, more compliant world.*
