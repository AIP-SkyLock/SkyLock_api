import boto3
from flask import Blueprint, jsonify

# Create a Blueprint for routes
main_routes = Blueprint('main_routes', __name__)

# @main_routes.route('/')
# def landing():
#     return {"message": "Welcome to the Flask API!"}
# @main_routes.route('/test')
# def test():
#     return {"message": "Welcome to the test!"}


# app = Flask(__name__)
# CORS(app)

@main_routes.route('/')
def index():
    return "✅ Cloud Security Compliance Tool API is running."

@main_routes.route('/scan/aws/config', methods=['GET'])
def scan_config():
    try:
        config = boto3.client('config')
        response = config.describe_compliance_by_config_rule()
        return jsonify(response.get('ComplianceByConfigRules', []))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_routes.route('/scan/aws/inspector', methods=['GET'])
def scan_inspector():
    try:
        inspector = boto3.client('inspector2')
        response = inspector.list_findings(maxResults=10)
        return jsonify(response.get('findings', []))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_routes.route('/scan/aws/securityhub', methods=['GET'])
def scan_securityhub():
    try:
        sh = boto3.client('securityhub')
        response = sh.get_findings(MaxResults=10)
        return jsonify(response.get('Findings', []))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
