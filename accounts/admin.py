# accounts/admin.py
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "role", "access_code", "is_active", "created_at")
    list_filter = ("role", "is_active")
    search_fields = ("full_name", "user__username", "user__email", "access_code")
