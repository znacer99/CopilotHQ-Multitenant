import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CopilotHQ.settings.base')
django.setup()

from tenants.models import Client
from agents.compliance import ComplianceAgent
from agents.orchestrator import OrchestratorAgent

def verify_compliance():
    # Get the test tenant
    try:
        tenant = Client.objects.get(schema_name='tenant1')
        print(f"Testing with tenant: {tenant.name}")
    except Client.DoesNotExist:
        print("Tenant 'tenant1' not found. Please run create_test_data.py first.")
        return

    # 1. Test ComplianceAgent Initialization
    agent = ComplianceAgent(tenant)
    print(f"\n--- Testing ComplianceAgent ---")
    print(f"Agent Type: {agent.agent_type}")
    print(f"Mock Mode: {agent.mock_mode}")
    
    # 2. Test Audit (Mock)
    mock_contract = "This contract dictates that the employee will work 100 hours per week and has no right to PTO."
    audit_result = agent.audit_document(mock_contract)
    print("\nAudit Result (Mock):")
    print(audit_result)

    # 3. Test Orchestrator Routing
    print("\n--- Testing Orchestrator Routing ---")
    orchestrator = OrchestratorAgent(tenant)
    query = "Can you audit this new employment contract for compliance?"
    routing_result = orchestrator.handle_request(query)
    print(f"Query: '{query}'")
    print(f"Intent: {routing_result.get('intent')}")
    print(f"Plan: {routing_result.get('plan')}")

if __name__ == "__main__":
    verify_compliance()
