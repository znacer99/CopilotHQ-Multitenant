from rest_framework import viewsets, permissions
from .models import Candidate, Job
from .serializers import CandidateSerializer, JobSerializer

class CandidateViewSet(viewsets.ModelViewSet):
    """API endpoint for managing candidates in the recruitment pipeline."""
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

class JobViewSet(viewsets.ModelViewSet):
    """API endpoint for managing job postings."""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
