import boto3

def scan_inspector_findings():
    client = boto3.client('inspector2')
    response = client.list_findings(maxResults=10)
    return response.get('findings', [])
