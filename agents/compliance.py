from .base import BaseAgent
from django.db import connection
import json
import logging

logger = logging.getLogger(__name__)

class ComplianceAgent(BaseAgent):
    """
    Internal Auditor and Regulatory Guide.
    Ensures company actions align with internal policies and labor laws.
    """
    
    agent_type = "compliance"
    
    def get_permissions(self):
        return [
            "read_contracts",
            "read_employee_records",
            "read_policies",
            "audit_actions",
        ]
    
    def build_context(self):
        """Enhanced context for compliance agent"""
        base_context = super().build_context()
        
        compliance_context = f"""
{base_context}

YOUR ROLE:
You are the HR Compliance Agent. Your job is to:
1. Audit documents (contracts, offers, performance reviews) for compliance errors.
2. Ensure new hire data follows company and regulatory standards.
3. Check for "Policy Drift" where actions (e.g., salary updates) might deviate from policy.
4. Provide guidance on labor law queries (using knowledge base documents).

COMPLIANCE GUIDELINES:
1. Be meticulous and detail-oriented.
2. Flag anything that looks suspicious or deviates from the official Knowledge Base.
3. If a document is missing mandatory clauses, specify exactly what is missing.
4. Always cross-reference with the Knowledge Agent tools.

AVAILABLE TOOLS:
- audit_document: Scan text for compliance issues against a specific policy type.
- check_policy_drift: Compare a specific action or value against company rules.
- lookup_regulatory_info: Search Knowledge Base for specific compliance standards.
"""
        return compliance_context

    def audit_document(self, document_text, doc_type="contract"):
        """
        Scan a document for compliance issues.
        """
        connection.set_tenant(self.tenant)
        
        tools = [
            {
                "name": "lookup_regulatory_info",
                "description": "Search Knowledge Base for specific compliance standards/policy required for this doc type",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "The compliance topic to look up (e.g., 'contract clauses', 'NDA requirements')"
                        }
                    },
                    "required": ["topic"]
                }
            }
        ]

        prompt = f"""Please audit the following {doc_type} for compliance issues:

--- DOCUMENT START ---
{document_text}
--- DOCUMENT END ---

Compare this against our standard policies. Look for:
1. Missing mandatory clauses.
2. Language that contradicts our company policy.
3. Potential legal risks.

If you are unsure of the current policy, use the 'lookup_regulatory_info' tool first.
"""
        
        response = self.call_claude(prompt, tools=tools)
        return self._process_response_with_tools(response)

    def check_policy_drift(self, action_data):
        """
        Check if an action (e.g. salary change, role change) deviates from policy.
        action_data: dict e.g. {"employee_id": 1, "field": "salary", "new_value": 50000}
        """
        connection.set_tenant(self.tenant)
        
        prompt = f"""
Perform a 'Policy Drift' check for the following action:
{json.dumps(action_data, indent=2)}

Cross-reference with company policy/compensation bands in the Knowledge Base to see if this is compliant.
"""
        response = self.call_claude(prompt)
        return self.extract_text_response(response)

    def _process_response_with_tools(self, response):
        """Helper to handle tool calls in response"""
        answer = self.extract_text_response(response)
        
        if not self.mock_mode:
            for block in response.content:
                if block.type == "tool_use":
                    tool_result = self.execute_tool(block.name, block.input)
                    
                    # Follow up with tool results
                    follow_up = self.call_claude(
                        f"Tool result for {block.name}: {json.dumps(tool_result)}\n\nPlease provide final audit findings."
                    )
                    answer = self.extract_text_response(follow_up)
        
        return answer

    def execute_tool(self, tool_name, tool_input):
        """Execute compliance tools"""
        connection.set_tenant(self.tenant)
        
        if tool_name == "lookup_regulatory_info":
            from .knowledge import KnowledgeAgent
            ka = KnowledgeAgent(self.tenant)
            return ka.search_knowledge(tool_input.get("topic"))
        
        return None
