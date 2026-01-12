from .base import BaseAgent
from .models import ConversationHistory
from django.db import connection
import json

class SupportAgent(BaseAgent):
    """
    24/7 employee support agent
    Answers questions about policies, benefits, time off, etc.
    """
    
    agent_type = "support"
    
    def get_permissions(self):
        return [
            "read_policies",
            "read_employee_data",
            "read_leave_balances",
            "read_org_chart",
        ]
    
    def build_context(self):
        """Enhanced context for support agent"""
        base_context = super().build_context()
        
        # Add support-specific context
        support_context = f"""
{base_context}

YOUR ROLE:
You are the HR Support Agent. Your job is to help employees with:
- Policy questions (vacation, sick leave, remote work, etc.)
- Benefits information
- Leave balance inquiries
- Organizational questions
- General HR guidance

RESPONSE GUIDELINES:
1. Be friendly and professional
2. Give specific answers based on company policies
3. If you need to look up data, use the provided tools
4. If you can't answer, escalate to human HR
5. Always cite policy sources when relevant

AVAILABLE TOOLS:
- lookup_leave_balance: Get employee's leave balance
- lookup_policy: Search company policies
- create_ticket: Escalate to human HR
"""
        return support_context
    
    def answer_question(self, employee, question):
        """
        Answer an employee question
        
        Args:
            employee: User object
            question: String question
            
        Returns:
            dict with answer and metadata
        """
        connection.set_tenant(self.tenant)
        
        # Load conversation history
        conversation, created = ConversationHistory.objects.get_or_create(
            tenant=self.tenant,
            employee=employee
        )
        
        # Build message history
        messages = conversation.messages + [
            {"role": "user", "content": question}
        ]
        
        # Define tools
        tools = [
            {
                "name": "lookup_leave_balance",
                "description": "Get employee's current leave balance",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "employee_id": {
                            "type": "integer",
                            "description": "Employee ID"
                        }
                    },
                    "required": ["employee_id"]
                }
            },
            {
                "name": "lookup_policy",
                "description": "Search company HR policies",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "policy_topic": {
                            "type": "string",
                            "description": "Topic to search (e.g., 'vacation', 'remote work')"
                        }
                    },
                    "required": ["policy_topic"]
                }
            },
            {
                "name": "create_ticket",
                "description": "Escalate complex issue to human HR",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "issue": {
                            "type": "string",
                            "description": "Description of the issue"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "Priority level"
                        }
                    },
                    "required": ["issue", "priority"]
                }
            }
        ]
        
        # Call Claude (or Mock)
        prompt = f"""Employee {employee.email} asks:

{question}

Please provide a helpful answer. Use the available tools if needed to look up specific information.
"""
        
        response = self.call_claude(prompt, tools=tools)
        
        # Handle tool use if not in mock mode (mock mode just returns text for now)
        answer = self.extract_text_response(response)
        tool_calls = []
        
        if not self.mock_mode:
            for block in response.content:
                if block.type == "tool_use":
                    tool_result = self.execute_tool(block.name, block.input)
                    tool_calls.append({
                        "tool": block.name,
                        "input": block.input,
                        "result": tool_result
                    })
                    
                    # If tool was used, make follow-up call with results
                    if tool_result:
                        follow_up = self.call_claude(
                            f"Tool result: {json.dumps(tool_result)}\n\nPlease provide final answer."
                        )
                        answer = self.extract_text_response(follow_up)
        
        # Update conversation history
        conversation.messages = messages + [
            {"role": "assistant", "content": answer}
        ]
        conversation.save()
        
        return {
            "answer": answer,
            "tool_calls": tool_calls,
            "conversation_id": conversation.id
        }
    
    def execute_tool(self, tool_name, tool_input):
        """Execute tool calls"""
        connection.set_tenant(self.tenant)
        
        if tool_name == "lookup_leave_balance":
            return self._lookup_leave_balance(tool_input.get("employee_id"))
            
        elif tool_name == "lookup_policy":
            return self._lookup_policy(tool_input.get("policy_topic"))
            
        elif tool_name == "create_ticket":
            return self._create_ticket(tool_input)
            
        return None
    
    def _lookup_leave_balance(self, employee_id):
        """Look up employee leave balance"""
        from employees.models import Employee
        # Assuming a LeaveBalance model exists or we use a standard policy
        try:
            employee = Employee.objects.get(id=employee_id)
            return {
                "employee": employee.user.username,
                "vacation_days": 15,  # Placeholder/Standard
                "sick_days": 5, 
            }
        except Employee.DoesNotExist:
            return {"error": "Employee not found"}
    
    def _lookup_policy(self, topic):
        """Search company policies using the real KnowledgeAgent system"""
        from .knowledge import KnowledgeAgent
        
        knowledge_agent = KnowledgeAgent(self.tenant)
        result = knowledge_agent.search_knowledge(topic)
        
        return {
            "topic": topic,
            "policy": result.get("summary", "Policy not found in the official records."),
            "source_matches": [r["title"] for r in result.get("results", [])]
        }
    
    def _create_ticket(self, data):
        """Create HR ticket"""
        # TODO: Implement actual ticket system
        return {
            "ticket_id": "TICKET-" + str(hash(data.get("issue", "no issue")))[:6],
            "status": "created",
            "message": "Ticket created. HR will respond within 24 hours."
        }
