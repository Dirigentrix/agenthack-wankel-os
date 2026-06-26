import os
import logging
from flask import Flask, jsonify, request
from scada_docs.document_automator import GoogleSheetMock, TranslationEngine, DocumentMapper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SCADA_Docs_Flask")

app = Flask(__name__)

# Initialize components
sheet_client = GoogleSheetMock()
translator = TranslationEngine()
mapper = DocumentMapper(translator)

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "service": "SCADA Documentation Automator",
        "repository": "Dirigentrix/agenthack-wankel-os"
    })

@app.route('/api/process-shipments', methods=['POST'])
def process_shipments():
    """
    Endpoint to trigger the automation flow.
    Connects to mock sheet, translates data, and maps to IATA templates.
    """
    logger.info("Manual process-shipments trigger received.")
    
    try:
        shipments = sheet_client.get_shipment_data()
        results = []
        
        for shipment in shipments:
            logger.info(f"Processing shipment: {shipment['id']} from REJESTR_ZLECONYCH")
            
            awb = mapper.create_awb_json(shipment)
            dgd = mapper.create_dgd_json(shipment)
            
            results.append({
                "shipment_id": shipment['id'],
                "awb": awb,
                "dgd": dgd,
                "status": "Automated - Human Error Mitigated"
            })
            
        return jsonify({
            "success": True,
            "processed_count": len(results),
            "data": results
        })
    except Exception as e:
        logger.error(f"Automation failed: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    # Defaulting to 8080 for Replit compatibility
    app.run(host='0.0.0.0', port=8080)
