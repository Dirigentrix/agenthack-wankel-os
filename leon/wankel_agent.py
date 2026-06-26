import random
import time
import math
from typing import Dict, Any, List

class WankelAgent:
    """
    WankelAgent implements a rotational agent logic based on the 3-chamber 
    Wankel engine principle. Each cycle rotates through three distinct 
    botanical/robotic phases simultaneously.
    """
    def __init__(self, agent_id: str = "Wankel-01"):
        self.agent_id = agent_id
        self.current_phase = 0  # 0: LEAF, 1: STEM, 2: FRUIT
        self.resonance = 156.0
        self.history: List[Dict[str, Any]] = []
        self.state = {
            "intencja": "IDLE",
            "sync_level": 0.0,
            "chamber_status": ["READY", "READY", "READY"]
        }

    def _update_resonance(self):
        """Maintains the 156 Hz micro-drift (±0.5 Hz)."""
        drift = random.uniform(-0.5, 0.5)
        self.resonance = 156.0 + drift

    def _process_leaf(self, intencja: str):
        """Phase 0: LEAF / Sensory / Intencja."""
        self.state["intencja"] = intencja
        self.state["chamber_status"][0] = "INGESTING"
        # Simulate sensory processing
        time.sleep(0.01)
        self.state["chamber_status"][0] = "COMPLETE"

    def _process_stem(self):
        """Phase 1: STEM / Processing / KARTRIX."""
        self.state["chamber_status"][1] = "PROCESSING"
        # Simulate hydraulic/KARTRIX logic
        load = random.uniform(0.1, 0.4)
        time.sleep(0.01)
        self.state["chamber_status"][1] = f"STABLE_LOAD_{load:.2f}"

    def _process_fruit(self):
        """Phase 2: FRUIT / Akcja / Clone Robotic."""
        self.state["chamber_status"][2] = "EXECUTING"
        self.state["sync_level"] = random.uniform(92.0, 99.9)
        time.sleep(0.01)
        self.state["chamber_status"][2] = "ROBOTIC_SYNC_OK"

    def rotate_cycle(self, intencja: str) -> Dict[str, Any]:
        """
        Advances the Wankel rotation. In a real Wankel, all 3 chambers 
        are active at once at different stages. This simulates one 
        full rotation of the triangle.
        """
        self._update_resonance()
        
        # Rotational execution
        # In this simplified model, we sequence them but they represent 
        # the concurrent state of the rotor faces.
        self._process_leaf(intencja)
        self._process_stem()
        self._process_fruit()

        # Advance phase pointer
        self.current_phase = (self.current_phase + 1) % 3

        result = {
            "agent_id": self.agent_id,
            "phase": ["LEAF", "STEM", "FRUIT"][self.current_phase],
            "resonance_hz": round(self.resonance, 3),
            "intencja": self.state["intencja"],
            "sync": f"{self.state['sync_level']:.2f}%",
            "chambers": list(self.state["chamber_status"]),
            "timestamp": time.time()
        }
        
        self.history.append(result)
        if len(self.history) > 100:
            self.history.pop(0)
            
        return result

if __name__ == "__main__":
    agent = WankelAgent()
    print(f"Starting {agent.agent_id} Core Loop...")
    for i in range(3):
        cycle_report = agent.rotate_cycle("REPAIR_SYSTEM")
        print(f"Rotation {i+1}: {cycle_report}")
