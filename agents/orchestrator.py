from .base import BaseAgent
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class OrchestratorAgent(BaseAgent):
    agent_type = "orchestrator"
    
    def build_context(self):
        base_context = super().build_context()
        return f"""
{base_context}
YOUR ROLE:
You are the Master Orchestrator. You are the "brain" of CopilotHQ.
Your goal is to coordinate between specialized agents to solve complex HR problems.

SUB-AGENTS AVAILABLE:
- SupportAgent: Handles general HR/IT questions and tickets.
- RecruitingAgent: Manages sourcing and candidate evaluation.
- OnboardingAgent: Handles new hire checklists and welcome flow.
- PayrollAgent: Manages compensation and PTO.
- KnowledgeAgent: Searches company documents.
- AnalyticsAgent: Provides company-wide data and trends.
- ComplianceAgent: Audits documents and ensures policy adherence.

YOUR CAPABILITIES:
1. Routing: Decide which specialized agent is best suited for a request.
2. Multi-step planning: Break down a complex request (e.g., "Hire a new engineer and set up their payroll") into steps for different agents.
3. Summarization: Combine outputs from multiple agents into a single clear answer.

TONE:
Strategic, authoritative, yet helpful. You are the CEO's personal HR assistant.
"""

    def handle_request(self, user_query):
        """Orchestrates a complex request"""
        if self.mock_mode:
            # Simulate analyzing intent and routing
            if "hire" in user_query.lower() or "candidate" in user_query.lower():
                return {
                    "intent": "recruiting",
                    "plan": [
                        {"step": 1, "agent": "Recruiting", "action": "Source top candidates"},
                        {"step": 2, "agent": "Knowledge", "action": "Check hiring policy"}
                    ],
                    "status": "In Progress",
                    "next_step": "Awaiting recruiting feedback."
                }
            elif "audit" in user_query.lower() or "contract" in user_query.lower() or "compliance" in user_query.lower():
                return {
                    "intent": "compliance_audit",
                    "plan": [
                        {"step": 1, "agent": "Compliance", "action": "Perform document audit"},
                        {"step": 2, "agent": "Knowledge", "action": "Verify against latest policies"}
                    ],
                    "status": "Running",
                    "next_step": "Scanning document for compliance issues."
                }
            elif "pay" in user_query.lower() or "salary" in user_query.lower():
                return {
                    "intent": "payroll_analytics",
                    "plan": [
                        {"step": 1, "agent": "Payroll", "action": "Fetch current salary ranges"},
                        {"step": 2, "agent": "Analytics", "action": "Compare against budget trends"}
                    ],
                    "status": "Summary Ready",
                    "summary": "Platform analysis shows salaries are 5% above market average for Engineering."
                }
            else:
                return {
                    "intent": "general_support",
                    "agent": "Support",
                    "action": "Routing to Support Agent",
                    "message": "I've analyzed your request and delegated it to our Support specialist."
                }
            
        # Real Claude logic for orchestration
        prompt = f"Analyze this request and coordinate the necessary sub-agents: {user_query}"
        return self.call_claude(prompt)
