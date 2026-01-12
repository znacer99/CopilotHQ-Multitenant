from .base import BaseAgent
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class AnalyticsAgent(BaseAgent):
    agent_type = "analytics"
    
    def build_context(self):
        base_context = super().build_context()
        return f"""
{base_context}
YOUR ROLE:
You are the Analytics Agent. You provide data-driven insights into the company's workforce.
Your responsibilities include:
- Generating reports on headcount trends.
- Analyzing turnover and retention rates.
- Comparing salary bands across departments.
- Identifying trends in hiring speed (Time-to-Hire).

TOOLS AVAILABLE:
- get_headcount_stats(): Get current employee counts by department and location.
- analyze_turnover(months): Analyze how many people left and why over a period.
- salary_benchmarking(role_id): Compare internal salaries for a role against industry averages.

TONE:
Analytical, data-heavy, and professional. Use numbers to back up all claims.
"""

    def get_dashboard_stats(self):
        """Returns high-level dashboard metrics for the tenant"""
        if self.mock_mode:
            return {
                "headcount": 142,
                "avg_salary": 85000,
                "engagement_score": 4.2,
                "open_roles": 8,
                "growth_metrics": {
                    "monthly_new_hires": 12,
                    "turnover_rate": "2.1%"
                },
                "department_split": [
                    {"name": "Engineering", "count": 60},
                    {"name": "Product", "count": 25},
                    {"name": "Sales", "count": 40},
                    {"name": "HR", "count": 17}
                ]
            }
            
        # Real SQL aggregation logic would go here
        return {"error": "Real analytics require active database metrics."}

    def predict_attrition(self):
        """AI-powered attrition risk prediction"""
        if self.mock_mode:
            return {
                "risk_level": "Low",
                "predicted_turnover_next_quarter": "3.5%",
                "key_risk_factors": ["Commute distance", "Time since last promotion"],
                "recommendation": "Consider remote flexibility for teams in High Silicon Valley area."
            }
        
        prompt = "Based on historical turnover data, predict next quarter's attrition risk."
        return self.call_claude(prompt)
