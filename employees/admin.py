from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "position", "status", "contract_type", "hire_date")
    list_filter = ("status", "contract_type", "department")
    search_fields = ("user__username", "user__email", "position")
