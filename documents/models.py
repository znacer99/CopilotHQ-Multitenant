# documents/models.py
from django.db import models
from django.conf import settings
from employees.models import Employee


class DocumentCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="documents")
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)

    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.employee.user.username})"
