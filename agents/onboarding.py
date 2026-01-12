from .base import BaseAgent
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class OnboardingAgent(BaseAgent):
    agent_type = "onboarding"
    
    def build_context(self):
        base_context = super().build_context()
        return f"""
{base_context}
YOUR ROLE:
You are the Onboarding Agent. Your goal is to ensure a world-class experience for new employees.
Your responsibilities include:
- Generating personalized welcome messages.
- Creating onboarding checklists (IT setup, HR paperwork, team intros).
- Tracking completion status of onboarding tasks.
- Answering new hire questions about their first week.

TOOLS AVAILABLE:
- create_checklist(employee_id): Generate a standard onboarding checklist for a new hire.
- send_welcome_email(employee_id, personal_note): Draft and "send" a welcome email.
- check_task_status(employee_id, task_name): Verify if a specific onboarding task is done.

TONE:
Professional, welcoming, and encouraging. Focus on reducing new-hire anxiety.
"""

    def generate_plan(self, employee_id):
        """Generates an onboarding plan for a specific employee"""
        if self.mock_mode:
            return {
                "employee_id": employee_id,
                "plan": [
                    {"step": 1, "task": "IT Equipment Request", "status": "Pending"},
                    {"step": 2, "task": "HR Portal Access", "status": "Completed"},
                    {"step": 3, "task": "Welcome Lunch with Team", "status": "Scheduled"},
                    {"step": 4, "task": "Compliance Training", "status": "Not Started"}
                ],
                "message": "AI-generated onboarding plan for the new hire."
            }
            
        # Real Claude call logic would go here
        prompt = f"Generate a detailed 30-day onboarding plan for employee ID {employee_id} based on company context."
        return self.call_claude(prompt)

    def draft_welcome(self, employee_id):
        """Drafts a personalized welcome message"""
        if self.mock_mode:
            return {
                "subject": f"Welcome to {self.tenant.name}!",
                "body": f"Hi! We are so excited to have you join us. Your first day is going to be great. We've prepared everything for you.",
                "action_items": ["Log in to HR portal", "Sign MDM policy"]
            }
        
        prompt = f"Draft a warm, personalized welcome email for employee {employee_id} at {self.tenant.name}."
        return self.call_claude(prompt)
