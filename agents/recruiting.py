from .base import BaseAgent
from django.db import connection
import json
import logging

logger = logging.getLogger(__name__)

class RecruitingAgent(BaseAgent):
    """
    Autonomous recruiting agent
    Sources candidates, screens resumes, schedules interviews
    """
    
    agent_type = "recruiting"
    
    def get_permissions(self):
        return [
            "post_jobs",
            "email_candidates",
            "schedule_interviews",
            "screen_resumes",
        ]
    
    def build_context(self):
        base_context = super().build_context()
        
        recruiting_context = f"""
{base_context}

YOUR ROLE:
You are the Recruiting Agent. Your job is to:
1. Source qualified candidates for open positions
2. Screen resumes and applications
3. Conduct initial outreach
4. Schedule interviews
5. Provide hiring recommendations

CAPABILITIES:
- Search LinkedIn for candidates (via API)
- Search GitHub for technical candidates
- Parse and evaluate resumes
- Score candidates against job requirements
- Draft personalized outreach emails
- Schedule calendar invitations

PROCESS:
1. Analyze job description and requirements
2. Source candidates from multiple channels
3. Screen and score each candidate (0-100)
4. Recommend top candidates to hiring manager
5. Handle initial outreach and scheduling
"""
        return recruiting_context
    
    def source_candidates(self, job_id):
        """
        Source candidates for a job posting
        Returns list of candidates with scores
        """
        connection.set_tenant(self.tenant)
        from candidates.models import Job
        
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return {"error": "Job not found"}
        
        prompt = f"""
I need to source candidates for this position:

TITLE: {job.title}
LOCATION: {job.location}
REQUIREMENTS:
{job.requirements}

DESCRIPTION:
{job.description}

Please:
1. Identify ideal candidate profile
2. Suggest search strategies for LinkedIn, GitHub, job boards
3. Draft Boolean search strings
4. Recommend sourcing channels

Return as JSON.
"""
        
        if self.mock_mode:
            return self._mock_source_candidates(job)

        response = self.call_claude(prompt)
        result = self.extract_text_response(response)
        
        try:
            # Attempt to extract JSON if Claude wrapped it in text
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0].strip()
            strategies = json.loads(result)
            return strategies
        except:
            return {"error": "Could not parse sourcing strategy", "raw_response": result}

    def _mock_source_candidates(self, job):
        """Mock sourcing strategy"""
        return {
            "ideal_profile": f"Senior professional with expertise in {job.title} requirements.",
            "search_strategies": ["LinkedIn keyword search", "GitHub repository contributors"],
            "boolean_searches": {
                "linkedin": f"(\"{job.title}\" OR \"Engineer\") AND \"Python\"",
                "github": f"location:\"{job.location}\" language:Python"
            },
            "sourcing_channels": ["LinkedIn", "GitHub", "Internal Referrals"]
        }
    
    def screen_resume(self, candidate_id, job_id):
        """
        AI screen a candidate's resume against job requirements
        Returns score (0-100) and reasoning
        """
        connection.set_tenant(self.tenant)
        from candidates.models import Job, Candidate
        
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            job = Job.objects.get(id=job_id)
        except (Candidate.DoesNotExist, Job.DoesNotExist):
            return {"error": "Candidate or Job not found"}
        
        prompt = f"""
Screen this candidate for the position:

JOB TITLE: {job.title}
REQUIREMENTS:
{job.requirements}

CANDIDATE:
Name: {candidate.name}
Email: {candidate.email}
Resume:
{candidate.resume_text}

Please evaluate and return JSON with score (0-100), strengths, weaknesses, recommendation, and reasoning.
"""
        
        if self.mock_mode:
            evaluation = self._mock_screen_resume(candidate, job)
        else:
            response = self.call_claude(prompt)
            result = self.extract_text_response(response)
            try:
                if "```json" in result:
                    result = result.split("```json")[1].split("```")[0].strip()
                evaluation = json.loads(result)
            except:
                return {"error": "Could not parse evaluation", "raw_response": result}
            
        # Save evaluation to candidate
        candidate.ai_score = evaluation.get("score", 0)
        candidate.ai_evaluation = evaluation
        candidate.save()
        
        return evaluation

    def _mock_screen_resume(self, candidate, job):
        """Mock resume screening"""
        return {
            "score": 85,
            "strengths": ["Relevant experience", "Strong technical skills"],
            "weaknesses": ["Missing specific industry domain knowledge"],
            "recommendation": "yes",
            "reasoning": f"Candidate {candidate.name} shows strong alignment with {job.title} requirements.",
            "questions_to_ask": ["Can you elaborate on your experience with X?"]
        }
    
    def draft_outreach(self, candidate_id, job_id):
        """
        Draft personalized outreach email
        """
        connection.set_tenant(self.tenant)
        from candidates.models import Job, Candidate
        
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            job = Job.objects.get(id=job_id)
        except (Candidate.DoesNotExist, Job.DoesNotExist):
            return {"error": "Candidate or Job not found"}
        
        prompt = f"""
Draft a personalized recruiting email for {candidate.name} for the position {job.title} at {self.tenant.name}.
"""
        
        if self.mock_mode:
            return f"Subject: Opportunity for {job.title} at {self.tenant.name}\n\nHi {candidate.name},\n\nI noticed your impressive background and think you'd be a great fit for our {job.title} role..."

        response = self.call_claude(prompt)
        return self.extract_text_response(response)
