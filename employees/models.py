# employees/models.py
from django.db import models
from django.conf import settings
from departments.models import Department


class Employee(models.Model):
    CONTRACT_TYPES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("contract", "Contract"),
        ("intern", "Intern"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("on_leave", "On Leave"),
        ("terminated", "Terminated"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile"
    )
    
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees"
    )

    position = models.CharField(max_length=120)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPES, default="full_time")
    hire_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    national_id = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    emergency_contact_name = models.CharField(max_length=150, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=50, blank=True, null=True)

    profile_photo = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} — {self.position}"
