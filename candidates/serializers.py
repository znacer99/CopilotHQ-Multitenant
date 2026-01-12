from rest_framework import serializers
from .models import Candidate, Job

class CandidateSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    
    class Meta:
        model = Candidate
        fields = [
            'id', 'name', 'email', 'phone', 'position', 
            'resume_text', 'linkedin_url', 'status', 
            'ai_score', 'ai_evaluation', 'job', 'job_title', 'created_at'
        ]

class JobSerializer(serializers.ModelSerializer):
    candidate_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = ['id', 'title', 'location', 'requirements', 'description', 'candidate_count', 'created_at']
    
    def get_candidate_count(self, obj):
        return obj.candidates.count()
