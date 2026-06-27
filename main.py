import os
import logging
from flask import Flask, jsonify, request
from scada_docs.aviation_haccp import AviationHACCP
from scada_docs.document_automator import GoogleSheetMock, TranslationEngine, DocumentMapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SCADA_Main")

app = Flask(__name__)

# Note: Integration with real Google Sheets will require credentials.json
# and 'google-auth', 'google-api-python-client' in requirements.txt
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "REJESTR_ZLECONYCH_ID")

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "version": "1.5.0",
        "engine": "Guardian AviationHACCP",
        "ready_for_sheets": os.path.exists("credentials.json")
    })

@app.route('/api/validate-batch', methods=['POST'])
def validate_batch():
    data = request.json
    batch_id = data.get("batch_id", "UNKNOWN_BATCH")
    measurements = data.get("measurements", {})
    cold_chain = data.get("cold_chain", [])

    logger.info(f"Received validation request for batch: {batch_id}")
    
    haccp = AviationHACCP(batch_id)
    
    for ccp_id, val in measurements.items():
        haccp.validate_ccp(ccp_id, val)
        
    for stage, temp in cold_chain:
        haccp.register_cold_chain(stage, temp)
        
    report = haccp.generate_report()
    
    return jsonify({
        "batch_id": batch_id,
        "status": "Processed",
        "report": report,
        "critical_alerts_count": len(haccp.critical_alerts),
        "sensor_failures_count": len(haccp.sensor_failures)
    })

@app.route('/api/sheets/config', methods=['GET'])
def get_sheets_config():
    return jsonify({
        "spreadsheet_id": SPREADSHEET_ID,
        "credentials_status": "Found" if os.path.exists("credentials.json") else "Missing",
        "instructions": "Upload credentials.json to the root directory to enable Google Sheets sync."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
