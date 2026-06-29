import time
import requests
import random
import logging

# Configure logging for the edge agent
logging.basicConfig(level=logging.INFO, format='%(asctime)s - AGENT_00 - %(levelname)s - %(message)s')
logger = logging.getLogger("AgroOrganism00")

BRIDGE_URL = "http://localhost:8080/api/validate-batch"

def simulate_telemetry():
    """Simulates real-time HACCP telemetry from local sensors."""
    return {
        "batch_id": f"BATCH-{random.randint(1000, 9999)}",
        "measurements": {
            "CCP-1": round(random.uniform(-22.0, -18.0), 2),
            "CCP-2": round(random.uniform(1.0, 3.8), 2)
        },
        "cold_chain": [
            ("Loading", round(random.uniform(-20.0, -18.5), 2)),
            ("Transit", round(random.uniform(-21.0, -19.0), 2))
        ]
    }

def run_agent():
    logger.info("Starting agro_organism_00 Edge Agent (Continuous Cold Chain Compliance)...")
    logger.info(f"Targeting WANKEL Bridge at {BRIDGE_URL}")
    
    try:
        while True:
            telemetry = simulate_telemetry()
            logger.info(f"Sending telemetry for {telemetry['batch_id']}...")
            
            try:
                response = requests.post(BRIDGE_URL, json=telemetry, timeout=5)
                if response.status_code == 200:
                    result = response.json()
                    logger.info(f"Bridge Response: {result['status']} | Alerts: {result['critical_alerts_count']}")
                else:
                    logger.error(f"Bridge error: Status {response.status_code}")
            except requests.exceptions.ConnectionError:
                logger.warning("Could not connect to WANKEL Bridge. Is main.py running?")
            
            time.sleep(10) # Monitor every 10 seconds
            
    except KeyboardInterrupt:
        logger.info("Agent stopped by user.")

if __name__ == "__main__":
    run_agent()
