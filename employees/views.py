from rest_framework import viewsets, permissions
from .models import Employee
from .serializers import EmployeeSerializer, EmployeeCreateSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employees to be viewed or edited.
    Tenant-aware: Returns only employees for the current tenant.
    """
    queryset = Employee.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return EmployeeCreateSerializer
        return EmployeeSerializer

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')
