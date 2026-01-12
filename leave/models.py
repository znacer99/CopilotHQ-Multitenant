from django.db import models
from employees.models import Employee

class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('personal', 'Personal Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('unpaid', 'Unpaid Leave'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee.user.email} - {self.leave_type} ({self.status})"
    
    @property
    def days_requested(self):
        return (self.end_date - self.start_date).days + 1


class LeaveBalance(models.Model):
    """Tracks available leave balance per employee per leave type."""
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='leave_balances'
    )
    leave_type = models.CharField(max_length=20, choices=LeaveRequest.LEAVE_TYPES)
    total_days = models.IntegerField(default=21)  # Default annual allowance
    used_days = models.IntegerField(default=0)
    year = models.IntegerField()
    
    class Meta:
        unique_together = ['employee', 'leave_type', 'year']
    
    @property
    def remaining_days(self):
        return self.total_days - self.used_days
