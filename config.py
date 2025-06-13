# backend/compliance_assess/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file (ensure this is called where the app starts as well)
load_dotenv()

# --- Azure Configuration ---
TENANT_ID = os.environ.get("AZURE_TENANT_ID")
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID")

if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET, SUBSCRIPTION_ID]):
    raise ValueError("Azure credentials environment variables not set. Check your .env file.")

# You can add other configurations here if needed
# For example: FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "True").lower() == "true"