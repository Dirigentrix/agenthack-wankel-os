# DARTRIX OS: Deterministic Agentic System for Continuous Cold Chain Compliance

## Overview
DARTRIX OS is a professional-grade, deterministic agentic system designed to ensure 1:1 compliance in continuous cold chain logistics. By leveraging real-time telemetry and advanced HACCP (Hazard Analysis and Critical Control Points) validation, DARTRIX provides an autonomous bridge between physical environmental sensors and cloud-based management systems.

## UiPath AgentHack Integration
DARTRIX is architected to meet the high standards of the UiPath AgentHack:
- **UiPath Maestro**: Orchestrates and monitors the hybrid edge/cloud data stream, ensuring high availability and system resilience.
- **Agent Builder**: Used to define the high-level logic and state transitions of the DARTRIX Core.
- **Coded Agents**: The heart of the system. We explicitly utilize **Coded Agents** to validate real-time HACCP rules with mathematical precision, ensuring that safety protocols are never breached.

## Setup & Running
### Prerequisites
- **Python 3.14**: DARTRIX is optimized for the latest Python runtime.
- **PowerShell**: Recommended for Windows environments.

### Step-by-Step Instructions
1. **Clone the Repository**:
   ```powershell
   git clone https://github.com/Dirigentrix/agenthack-wankel-os.git
   cd agenthack-wankel-os
   ```
2. **Environment Configuration**:
   - Copy `.env.example` to `.env`.
   - Update `GEMINI_API_KEY` and `BRIDGE_URL` with your credentials.
3. **Dependency Installation**:
   Ensure you use `python -m pip` to avoid path conflicts:
   ```powershell
   python -m pip install -r requirements.txt
   ```
4. **Execution**:
   Run the main agent loop:
   ```powershell
   python main.py
   ```
   *Note: If using PowerShell, ensure you use `curl.exe` instead of the `curl` alias if performing manual API pings.*

## Project Structure
- `main.py`: The entry point for the DARTRIX Coded Agent.
- `haccp_layer.py`: Deterministic safety rule engine.
- `bridge_client.py`: Secure communication with the UiPath Maestro bridge.
- `src/`: Core TypeScript/React dashboard components.

---
*Developed for UiPath AgentHack 2026*
