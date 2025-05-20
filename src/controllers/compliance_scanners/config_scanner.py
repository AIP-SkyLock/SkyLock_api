import boto3

def scan_config_rules():
    client = boto3.client('config')
    response = client.describe_compliance_by_config_rule()
    return response.get('ComplianceByConfigRules', [])
