import json
from datetime import datetime
from typing import Dict, List, Any
from peklownia import PeklowniaBatch

class AviationHACCPBatch(PeklowniaBatch):
    """
    AviationHACCPBatch extends PeklowniaBatch to include IATA-compliant monitoring 
    and cold-chain compliance for aviation catering.
    """
    def __init__(self, batch_id: str, flight_number: str = None):
        super().__init__(batch_id)
        self.flight_number = flight_number
        # Ensure haccp_records is initialized safely even if super doesn't
        if not hasattr(self, 'haccp_records') or self.haccp_records is None:
            self.haccp_records = []
        self.allergens: List[str] = []

    def register_cold_chain(self, temperature: float, location: str):
        """Register a temperature check for cold-chain monitoring."""
        record_data = {
            "temperature": temperature,
            "location": location,
            "compliant": temperature <= 5.0  # Standard IATA cold chain threshold
        }
        self.add_record("cold_chain_check", record_data)

    def register_flight_handover(self, recipient: str, signature_id: str):
        """Register the handover of catering to the flight crew."""
        record_data = {
            "recipient": recipient,
            "signature_id": signature_id,
            "handover_time": datetime.now().isoformat()
        }
        self.add_record("flight_handover", record_data)

    def register_allergens(self, allergens: List[str]):
        """Register known allergens in the batch."""
        self.allergens = allergens
        self.add_record("allergen_declaration", {"allergens": allergens})

    def iata_compliance_check(self) -> Dict[str, Any]:
        """Check if all cold chain records are within IATA compliance limits."""
        if not self.haccp_records:
            return {"status": "INCOMPLETE", "violations": 0}
        
        violations = [
            r for r in self.haccp_records 
            if r.get("type") == "cold_chain_check" and not r.get("data", {}).get("compliant", False)
        ]
        
        return {
            "status": "PASS" if not violations else "FAIL",
            "violations": len(violations),
            "details": violations
        }

    def get_iata_report(self) -> Dict[str, Any]:
        """Generate a structured report for IATA compliance auditing."""
        compliance = self.iata_compliance_check()
        return {
            "batch_id": self.batch_id,
            "flight_number": self.flight_number,
            "timestamp": datetime.now().isoformat(),
            "compliance_status": compliance["status"],
            "total_records": len(self.haccp_records),
            "allergens": self.allergens
        }

    def to_json(self) -> str:
        """Serialize the batch data including IATA specific fields."""
        report = self.get_iata_report()
        data = {
            "batch_id": self.batch_id,
            "flight_number": self.flight_number,
            "created_at": self.created_at,
            "haccp_records": self.haccp_records,
            "iata_summary": report
        }
        return json.dumps(data, indent=2)
