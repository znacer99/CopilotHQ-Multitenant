from django.contrib import admin
from .models import Document, DocumentCategory

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "employee", "category", "uploaded_at", "expiry_date")
    list_filter = ("category", "expiry_date")
    search_fields = ("title", "employee__user__username")
