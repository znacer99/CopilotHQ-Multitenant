from .base import BaseAgent
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class PayrollAgent(BaseAgent):
    agent_type = "payroll"
    
    def build_context(self):
        base_context = super().build_context()
        return f"""
{base_context}
YOUR ROLE:
You are the Payroll Agent. Your goal is to ensure accuracy and transparency in compensation.
Your responsibilities include:
- Answering questions about paystubs and taxes.
- Explaining PTO (Paid Time Off) calculations.
- Identifying potential errors in payroll processing.
- Providing summaries of total compensation including benefits.

TOOLS AVAILABLE:
- calculate_pto_balance(employee_id): Get current available vacation/sick hours.
- explain_tax_withholding(employee_id, state): Explain why specific taxes were deducted.
- verify_salary_consistency(employee_id): Check if last paystub matches contract salary.

TONE:
Precise, confidential, and helpful. Numbers are critical here.
"""

    def get_pto_summary(self, employee_id):
        """Returns a PTO summary for an employee"""
        if self.mock_mode:
            return {
                "employee_id": employee_id,
                "pto_accrued": 120.0,
                "pto_used": 40.0,
                "pto_available": 80.0,
                "next_accrual_date": "2026-02-01"
            }
            
        prompt = f"Calculate current PTO balance for employee {employee_id} and provide an accrual projection."
        return self.call_claude(prompt)

    def explain_compensation(self, employee_id):
        """Provides a total compensation breakdown"""
        if self.mock_mode:
            return {
                "base_salary": 95000,
                "bonus_target": "10%",
                "benefits_value": 15000,
                "total_comp": 110000,
                "breakdown": [
                    {"category": "Base", "amount": 95000},
                    {"category": "Health Insurance", "amount": 8000},
                    {"category": "401k Match", "amount": 4500},
                    {"category": "Other Perks", "amount": 2500}
                ]
            }
        
        prompt = f"Provide a complete total compensation breakdown for employee {employee_id} including benefits value."
        return self.call_claude(prompt)
