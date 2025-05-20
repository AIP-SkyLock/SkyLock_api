from .config_scanner import scan_config_rules
from .inspector_scanner import scan_inspector_findings
from .securityhub_scanner import scan_securityhub_findings


def run_aws_compliance_template(template_name):
    if template_name == 'cis':
        return {
            'template': 'CIS Benchmark',
            'config_compliance': scan_config_rules(),
            'security_findings': scan_securityhub_findings(),
        }
    elif template_name == 'pci':
        return {
            'template': 'PCI DSS',
            'inspector_findings': scan_inspector_findings(),
            'security_findings': scan_securityhub_findings()
        }
    elif template_name == 'hipaa':
        return {
            'template': 'HIPAA',
            'config_compliance': scan_config_rules(),
            'security_findings': scan_securityhub_findings()
        }
    elif template_name == 'nist':
        return {
            'template': 'NIST',
            'config_compliance': scan_config_rules()
        }
    elif template_name == 'gdpr':
        return {
            'template': 'GDPR',
            'security_findings': scan_securityhub_findings()
        }
    else:
        raise ValueError(f"Unknown compliance template: {template_name}")
