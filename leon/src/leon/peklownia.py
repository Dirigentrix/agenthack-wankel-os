import json
from datetime import datetime
from typing import Dict, List, Any

class PeklowniaBatch:
    """
    Base class for tracking curing batches. 
    Provides basic structure for records and reporting.
    """
    def __init__(self, batch_id: str):
        self.batch_id = batch_id
        self.created_at = datetime.now().isoformat()
        self.haccp_records: List[Dict[str, Any]] = []

    def add_record(self, record_type: str, data: Dict[str, Any]):
        record = {
            "timestamp": datetime.now().isoformat(),
            "type": record_type,
            "data": data
        }
        self.haccp_records.append(record)

    def to_json(self) -> str:
        return json.dumps({
            "batch_id": self.batch_id,
            "created_at": self.created_at,
            "records": self.haccp_records
        }, indent=2)
