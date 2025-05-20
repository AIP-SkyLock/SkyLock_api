import boto3

def scan_securityhub_findings():
    client = boto3.client('securityhub')
    response = client.get_findings(MaxResults=10)
    return response.get('Findings', [])
