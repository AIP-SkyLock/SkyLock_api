# backend/models/azure/compliance_assess/api_routes.py
from flask import Blueprint, jsonify, request
# Import azure_collector and compliance_engine using absolute imports
import azure_collector # Fixed: Changed from 'from . import azure_collector'
import compliance_engine # Fixed: Changed from 'from . import compliance_engine'

# Create a Blueprint instance
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/collect_and_assess', methods=['POST'])
def collect_and_assess_endpoint():
    """
    Triggers the collection of Azure resources and then runs the compliance assessment
    based on the frameworks provided in the request body.
    """
    data = request.get_json()
    selected_frameworks = data.get('frameworks', [])
    print(f"Received request to collect and assess with frameworks: {selected_frameworks}")

    # Step 1: Collect resources
    if not azure_collector.collect_azure_resources_data():
        return jsonify({"status": "error", "message": "Failed to collect Azure resources. Check backend logs for details."}), 500

    # Step 2: Perform assessment using the collected data
    if not compliance_engine.perform_compliance_assessment(
        selected_frameworks, azure_collector.collected_resources
    ):
        return jsonify({"status": "error", "message": "Failed to perform compliance assessment. Check backend logs for details."}), 500

    return jsonify({"status": "success", "message": "Collection and assessment complete."}), 200

@api_bp.route('/resources', methods=['GET'])
def get_resources_endpoint():
    """
    Returns the currently collected Azure resources (full dictionary/JSON).
    """
    return jsonify(azure_collector.collected_resources), 200

@api_bp.route('/compliance_report', methods=['GET'])
def get_compliance_report_endpoint():
    """
    Returns the latest compliance assessment report.
    """
    return jsonify(compliance_engine.compliance_report), 200

@api_bp.route('/frameworks', methods=['GET'])
def get_frameworks_endpoint():
    """
    Returns the list of available compliance frameworks.
    """
    return jsonify(list(compliance_engine.COMPLIANCE_FRAMEWORK_RULES.keys())), 200
