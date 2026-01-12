from rest_framework import serializers
from .models import LeaveRequest, LeaveBalance

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_email = serializers.CharField(source='employee.user.email', read_only=True)
    days_requested = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'employee_email', 'leave_type', 
            'start_date', 'end_date', 'days_requested', 
            'reason', 'status', 'created_at', 'reviewed_at'
        ]

class LeaveBalanceSerializer(serializers.ModelSerializer):
    employee_email = serializers.CharField(source='employee.user.email', read_only=True)
    remaining_days = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = LeaveBalance
        fields = [
            'id', 'employee', 'employee_email', 'leave_type',
            'total_days', 'used_days', 'remaining_days', 'year'
        ]
