# backend/models/azure/compliance_assess/azure_collector.py
from azure.identity import ClientSecretCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.web import WebSiteManagementClient

# Import configurations using absolute import
import config # Fixed: Changed from 'from . import config'

# --- Global storage for collected data ---
collected_resources = []

# --- Azure API Client Initialization ---
def get_azure_clients():
    """Initializes and returns Azure SDK clients."""
    credential = ClientSecretCredential(
        tenant_id=config.TENANT_ID,
        client_id=config.CLIENT_ID,
        client_secret=config.CLIENT_SECRET
    )
    return {
        "resource": ResourceManagementClient(credential, config.SUBSCRIPTION_ID),
        "compute": ComputeManagementClient(credential, config.SUBSCRIPTION_ID),
        "network": NetworkManagementClient(credential, config.SUBSCRIPTION_ID),
        "storage": StorageManagementClient(credential, config.SUBSCRIPTION_ID),
        "web": WebSiteManagementClient(credential, config.SUBSCRIPTION_ID),
    }

# --- Azure Resource Collection Logic ---
def collect_azure_resources_data():
    """
    Collects all generic Azure resources and their properties.
    """
    global collected_resources
    collected_resources = [] # Clear previous collection

    try:
        clients = get_azure_clients()
        print("Starting comprehensive Azure resource collection...")

        for resource in clients["resource"].resources.list():
            resource_dict = resource.as_dict()
            if 'properties' not in resource_dict:
                resource_dict['properties'] = {}
            collected_resources.append(resource_dict)

        print(f"Collection complete. Total resources collected: {len(collected_resources)}")
        return True
    except Exception as e:
        print(f"Error during Azure resource collection: {e}")
        return False
