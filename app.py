# backend/models/azure/compliance_assess/app.py
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import your configuration and API blueprint using direct/absolute imports
import config
from api_routes import api_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(api_bp)

@app.route('/')
def home():
    return "Backend is running. Access API endpoints like /api/resources, /api/compliance_report, etc."

if __name__ == '__main__':
    app.run(debug=True, port=5000)