from rest_framework import viewsets, permissions
from .models import LeaveRequest, LeaveBalance
from .serializers import LeaveRequestSerializer, LeaveBalanceSerializer

class LeaveRequestViewSet(viewsets.ModelViewSet):
    """API endpoint for managing leave requests."""
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')

class LeaveBalanceViewSet(viewsets.ModelViewSet):
    """API endpoint for managing leave balances."""
    queryset = LeaveBalance.objects.all()
    serializer_class = LeaveBalanceSerializer
    permission_classes = [permissions.IsAuthenticated]
