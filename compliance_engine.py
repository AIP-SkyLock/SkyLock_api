# backend/compliance_assess/compliance_engine.py

# --- Global storage for compliance results ---
compliance_report = []

# --- Compliance Framework Rules Definition ---
# (Rules class was empty, so I've removed it for simplicity)

def rule_storage_public_access(resource):
    violations = []
    if resource.get('type') == 'Microsoft.Storage/storageAccounts':
        if resource.get('properties', {}).get('allowBlobPublicAccess', False):
            violations.append("Storage Account has public blob access enabled.")
    return violations

def rule_storage_encryption(resource):
    violations = []
    if resource.get('type') == 'Microsoft.Storage/storageAccounts':
        encryption = resource.get('properties', {}).get('encryption', {})
        if encryption.get('keySource') != 'Microsoft.Storage':
            violations.append("Storage account encryption is not using Microsoft-managed keys.")
    return violations

def rule_nsg_inbound_denied(resource):
    violations = []
    if resource.get('type') == 'Microsoft.Network/networkSecurityGroups':
        rules = resource.get('properties', {}).get('securityRules', [])
        has_deny_all_inbound = False
        for rule in rules:
            if rule.get('properties', {}).get('priority') == 65500 and \
               rule.get('properties', {}).get('direction') == 'Inbound' and \
               rule.get('properties', {}).get('access') == 'Deny' and \
               rule.get('properties', {}).get('destinationPortRange') == '*' and \
               (rule.get('properties', {}).get('sourceAddressPrefix') == 'Internet' or \
                rule.get('properties', {}).get('sourceAddressPrefix') == '0.0.0.0/0'):
                has_deny_all_inbound = True
                break
        if not has_deny_all_inbound:
            violations.append("NSG does not have a default 'Deny All Inbound' rule (all traffic).")
    return violations

def rule_vm_diagnostics_enabled(resource):
    violations = []
    if resource.get('type') == 'Microsoft.Compute/virtualMachines':
        if 'diagnosticsProfile' not in resource.get('properties', {}):
            violations.append("VM appears to not have diagnostics enabled.")
    return violations

def rule_webapp_https_only(resource):
    violations = []
    if resource.get('type') == 'Microsoft.Web/sites':
        if not resource.get('properties', {}).get('httpsOnly', False):
            violations.append("Web App does not enforce HTTPS only.")
    return violations

def rule_all_resources_have_tags(resource):
    violations = []
    if not resource.get('tags'):
        violations.append("Resource does not have any tags.")
    return violations

def rule_resource_in_allowed_location(resource):
    violations = []
    allowed_locations = ['eastus', 'westus2', 'canadacentral']
    if resource.get('location') and resource['location'].lower() not in allowed_locations:
        violations.append(f"Resource is in an unapproved location: {resource['location']}.")
    return violations

# Map compliance frameworks to their respective rules
COMPLIANCE_FRAMEWORK_RULES = {
    "NIST": [
        rule_storage_public_access,
        rule_nsg_inbound_denied,
        rule_vm_diagnostics_enabled
    ],
    "HIPAA": [
        rule_storage_encryption,
        rule_webapp_https_only
    ],
    "PCI": [
        rule_webapp_https_only,
        rule_nsg_inbound_denied,
        rule_storage_public_access
    ],
    "ISO": [
        rule_storage_encryption,
        rule_all_resources_have_tags
    ],
    "Custom": [
        rule_all_resources_have_tags,
        rule_resource_in_allowed_location
    ]
}

def perform_compliance_assessment(selected_frameworks, collected_resources_data):
    """
    Performs compliance assessment against collected resources based on selected frameworks.
    Now takes collected_resources_data as an argument instead of relying on a global.
    """
    global compliance_report # Still using global to store the result for the GET endpoint
    compliance_report = [] # Clear previous report
    print(f"Starting compliance assessment for frameworks: {selected_frameworks}...")

    active_rules = []
    for framework in selected_frameworks:
        if framework in COMPLIANCE_FRAMEWORK_RULES:
            active_rules.extend(COMPLIANCE_FRAMEWORK_RULES[framework])
        else:
            print(f"Warning: Unknown framework '{framework}' requested. Skipping.")

    if not active_rules:
        print("No active compliance rules selected. Skipping assessment.")
        compliance_report = [{"message": "No compliance frameworks selected for assessment."}]
        return True

    for resource in collected_resources_data: # Use the passed data
        resource_id = resource.get('id', 'N/A')
        resource_name = resource.get('name', 'N/A')
        resource_type = resource.get('type', 'N/A')
        resource_location = resource.get('location', 'N/A')

        resource_violations = []

        for rule_func in active_rules:
            violations_from_rule = rule_func(resource)
            resource_violations.extend(violations_from_rule)

        is_compliant = not bool(resource_violations)

        compliance_report.append({
            "resourceId": resource_id,
            "resourceName": resource_name,
            "resourceType": resource_type,
            "resourceLocation": resource_location,
            "isCompliant": is_compliant,
            "violations": list(set(resource_violations))
        })

    print(f"Compliance assessment complete. Total assessed resources: {len(compliance_report)}")
    print(f"Non-compliant resources: {sum(1 for r in compliance_report if not r['isCompliant'])}")
    return True